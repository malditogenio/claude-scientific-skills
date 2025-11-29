---
skill_name: bigquery
display_name: Google BigQuery
description: Google Cloud data warehouse for marketing analytics, GA4 integration, and customer insights
category: cdp-data
tags: [data-warehouse, google-cloud, analytics, sql, marketing-analytics]
complexity: intermediate
dependencies: [google-cloud-bigquery, pandas-gbq]
---

# Google BigQuery

## Overview

Google BigQuery is a serverless, highly scalable cloud data warehouse optimized for analytics. For marketing teams, BigQuery provides seamless integration with Google's marketing stack (GA4, Google Ads, YouTube) and enables powerful customer analytics at scale.

BigQuery excels at:
- **Native GA4 Integration**: Direct access to raw Google Analytics 4 data
- **Google Marketing Platform**: Unified analytics across Ads, Analytics, YouTube
- **Real-Time Analytics**: Query billions of rows with sub-second performance
- **ML-Powered Insights**: Built-in ML for predictions and audience discovery
- **Cost-Effective**: Pay only for queries and storage you use
- **Data Activation**: Export audiences to Google Ads and DV360

## When to Use

Use BigQuery when you need to:
- **GA4 Advanced Analytics**: Query raw event-level GA4 data
- **Google Ads Attribution**: Combine ad data with conversion data
- **Customer 360 with Google Data**: Unify GA4, Ads, YouTube, and CRM data
- **Predictive Analytics**: Build ML models for LTV, churn, propensity
- **Real-Time Dashboards**: Power Looker/Data Studio with live data
- **Audience Activation**: Export segments to Google Ads and DV360
- **Cross-Channel Attribution**: Analyze full customer journey across Google platforms

## Core Capabilities

### 1. GA4 Data Analysis

**Querying GA4 Export Data**

```sql
-- GA4 data is automatically exported to BigQuery
-- Standard schema: events_YYYYMMDD, events_intraday_YYYYMMDD

-- Analyze user acquisition sources
SELECT
    DATE(TIMESTAMP_MICROS(event_timestamp)) as date,
    traffic_source.source as utm_source,
    traffic_source.medium as utm_medium,
    traffic_source.name as utm_campaign,
    COUNT(DISTINCT user_pseudo_id) as users,
    COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN event_timestamp END) as conversions,
    SUM(CASE WHEN event_name = 'purchase'
        THEN (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'value')
        ELSE 0 END) / 1000000 as revenue
FROM `project.analytics_PROPERTY_ID.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20241101' AND '20241130'
    AND traffic_source.source IS NOT NULL
GROUP BY date, utm_source, utm_medium, utm_campaign
ORDER BY revenue DESC;

-- User engagement metrics
SELECT
    DATE(TIMESTAMP_MICROS(event_timestamp)) as date,
    COUNT(DISTINCT user_pseudo_id) as total_users,
    COUNT(DISTINCT CASE WHEN event_name = 'session_start' THEN event_timestamp END) as sessions,
    COUNT(DISTINCT CASE WHEN event_name = 'page_view' THEN event_timestamp END) as page_views,
    AVG(CASE WHEN event_name = 'session_start'
        THEN (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'engagement_time_msec')
        END) / 1000 as avg_session_duration_sec,
    COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_pseudo_id END) as purchasers,
    ROUND(COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_pseudo_id END) /
        COUNT(DISTINCT user_pseudo_id) * 100, 2) as conversion_rate
FROM `project.analytics_PROPERTY_ID.events_*`
WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
    AND FORMAT_DATE('%Y%m%d', CURRENT_DATE())
GROUP BY date
ORDER BY date DESC;

-- eCommerce product performance
SELECT
    items.item_name,
    items.item_category,
    COUNT(DISTINCT CASE WHEN event_name = 'view_item' THEN user_pseudo_id END) as viewers,
    COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_pseudo_id END) as add_to_carts,
    COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_pseudo_id END) as purchasers,
    SUM(CASE WHEN event_name = 'purchase' THEN items.quantity ELSE 0 END) as units_sold,
    SUM(CASE WHEN event_name = 'purchase' THEN items.price ELSE 0 END) as revenue,
    ROUND(COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_pseudo_id END) /
        NULLIF(COUNT(DISTINCT CASE WHEN event_name = 'view_item' THEN user_pseudo_id END), 0) * 100, 2) as view_to_cart_rate,
    ROUND(COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_pseudo_id END) /
        NULLIF(COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_pseudo_id END), 0) * 100, 2) as cart_to_purchase_rate
FROM `project.analytics_PROPERTY_ID.events_*`,
    UNNEST(items) as items
WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
    AND FORMAT_DATE('%Y%m%d', CURRENT_DATE())
    AND event_name IN ('view_item', 'add_to_cart', 'purchase')
GROUP BY items.item_name, items.item_category
HAVING viewers > 100
ORDER BY revenue DESC;
```

**User Journey Analysis with GA4**

```sql
-- Build user journey paths from GA4 events
WITH user_sessions AS (
    SELECT
        user_pseudo_id,
        (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id') as session_id,
        event_name,
        event_timestamp,
        traffic_source.source as utm_source,
        traffic_source.medium as utm_medium,
        traffic_source.name as utm_campaign,
        CASE WHEN event_name = 'purchase'
            THEN (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'value')
            ELSE 0 END as transaction_value
    FROM `project.analytics_PROPERTY_ID.events_*`
    WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
        AND FORMAT_DATE('%Y%m%d', CURRENT_DATE())
),
user_paths AS (
    SELECT
        user_pseudo_id,
        session_id,
        STRING_AGG(event_name, ' > ' ORDER BY event_timestamp) as event_path,
        MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) as converted,
        SUM(transaction_value) / 1000000 as revenue,
        MIN(utm_source) as first_source,
        MIN(utm_campaign) as first_campaign
    FROM user_sessions
    WHERE event_name IN ('session_start', 'page_view', 'view_item', 'add_to_cart', 'begin_checkout', 'purchase')
    GROUP BY user_pseudo_id, session_id
)
SELECT
    event_path,
    COUNT(*) as session_count,
    SUM(converted) as conversions,
    SUM(revenue) as total_revenue,
    ROUND(SUM(converted) / COUNT(*) * 100, 2) as conversion_rate,
    ROUND(SUM(revenue) / COUNT(*), 2) as revenue_per_session
FROM user_paths
GROUP BY event_path
HAVING session_count > 10
ORDER BY conversions DESC
LIMIT 20;
```

### 2. Customer 360 with Google Marketing Data

**Unified Customer Profile**

```sql
-- Combine GA4, Google Ads, and CRM data
CREATE OR REPLACE TABLE `project.marketing_data.customer_360` AS
WITH ga4_users AS (
    SELECT
        user_id,
        MIN(TIMESTAMP_MICROS(event_timestamp)) as first_seen_ga4,
        MAX(TIMESTAMP_MICROS(event_timestamp)) as last_seen_ga4,
        COUNT(DISTINCT DATE(TIMESTAMP_MICROS(event_timestamp))) as active_days,
        COUNT(DISTINCT CASE WHEN event_name = 'session_start'
            THEN (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id') END) as sessions,
        COUNT(DISTINCT CASE WHEN event_name = 'page_view' THEN event_timestamp END) as page_views,
        SUM(CASE WHEN event_name = 'purchase'
            THEN (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'value')
            ELSE 0 END) / 1000000 as ga4_revenue
    FROM `project.analytics_PROPERTY_ID.events_*`
    WHERE _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY))
        AND user_id IS NOT NULL
    GROUP BY user_id
),
google_ads_data AS (
    SELECT
        user_id,
        SUM(cost_micros) / 1000000 as ad_spend_attributed,
        COUNT(DISTINCT campaign_id) as campaigns_clicked,
        MAX(click_timestamp) as last_ad_click
    FROM `project.google_ads.clicks`
    WHERE click_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
        AND user_id IS NOT NULL
    GROUP BY user_id
),
crm_data AS (
    SELECT
        user_id,
        email,
        name,
        customer_tier,
        subscription_status,
        created_at
    FROM `project.crm.customers`
)
SELECT
    c.user_id,
    c.email,
    c.name,
    c.customer_tier,
    c.subscription_status,
    c.created_at,
    -- GA4 metrics
    g.first_seen_ga4,
    g.last_seen_ga4,
    g.active_days,
    g.sessions,
    g.page_views,
    g.ga4_revenue,
    -- Google Ads metrics
    a.ad_spend_attributed,
    a.campaigns_clicked,
    a.last_ad_click,
    -- Computed metrics
    ROUND(g.ga4_revenue / NULLIF(a.ad_spend_attributed, 0), 2) as customer_roas,
    DATE_DIFF(CURRENT_DATE(), DATE(g.last_seen_ga4), DAY) as days_since_last_visit,
    -- Segments
    CASE
        WHEN g.ga4_revenue > 1000 THEN 'high_value'
        WHEN g.ga4_revenue > 500 THEN 'medium_value'
        WHEN g.ga4_revenue > 0 THEN 'low_value'
        ELSE 'prospect'
    END as value_segment,
    CASE
        WHEN g.active_days >= 20 THEN 'highly_engaged'
        WHEN g.active_days >= 10 THEN 'engaged'
        WHEN g.active_days >= 3 THEN 'casual'
        ELSE 'inactive'
    END as engagement_segment
FROM crm_data c
LEFT JOIN ga4_users g ON c.user_id = g.user_id
LEFT JOIN google_ads_data a ON c.user_id = a.user_id;
```

**Audience Segmentation**

```sql
-- High-intent prospects from GA4 behavior
CREATE OR REPLACE TABLE `project.marketing_data.high_intent_prospects` AS
WITH user_behavior AS (
    SELECT
        user_pseudo_id,
        user_id,
        COUNT(DISTINCT CASE WHEN event_name = 'view_item' THEN event_timestamp END) as product_views,
        COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN event_timestamp END) as cart_adds,
        MAX(CASE WHEN event_name = 'begin_checkout' THEN 1 ELSE 0 END) as reached_checkout,
        MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) as purchased,
        MAX(TIMESTAMP_MICROS(event_timestamp)) as last_activity
    FROM `project.analytics_PROPERTY_ID.events_*`
    WHERE _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
    GROUP BY user_pseudo_id, user_id
)
SELECT
    user_pseudo_id,
    user_id,
    product_views,
    cart_adds,
    reached_checkout,
    last_activity,
    'high_intent_prospect' as audience_name,
    CURRENT_TIMESTAMP() as audience_updated_at
FROM user_behavior
WHERE product_views >= 3
    AND cart_adds >= 1
    AND purchased = 0
    AND last_activity >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY);

-- Export to Google Ads
-- BigQuery can directly sync to Google Ads Customer Match
```

### 3. Marketing Attribution with Google Ads Integration

**Multi-Touch Attribution**

```sql
-- Combine GA4 and Google Ads for attribution
CREATE OR REPLACE TABLE `project.marketing_data.attribution_analysis` AS
WITH touchpoints AS (
    SELECT
        user_pseudo_id,
        event_timestamp,
        traffic_source.source as source,
        traffic_source.medium as medium,
        traffic_source.name as campaign,
        ROW_NUMBER() OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp) as touch_number,
        COUNT(*) OVER (PARTITION BY user_pseudo_id) as total_touches
    FROM `project.analytics_PROPERTY_ID.events_*`
    WHERE _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
        AND traffic_source.source IS NOT NULL
),
conversions AS (
    SELECT
        user_pseudo_id,
        event_timestamp as conversion_timestamp,
        (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'value') / 1000000 as revenue,
        (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') as transaction_id
    FROM `project.analytics_PROPERTY_ID.events_*`
    WHERE _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
        AND event_name = 'purchase'
),
attributed_touches AS (
    SELECT
        t.source,
        t.medium,
        t.campaign,
        c.revenue,
        c.transaction_id,
        -- First touch
        CASE WHEN t.touch_number = 1 THEN 1.0 ELSE 0 END as first_touch_weight,
        -- Last touch
        CASE WHEN t.touch_number = t.total_touches THEN 1.0 ELSE 0 END as last_touch_weight,
        -- Linear
        1.0 / t.total_touches as linear_weight,
        -- Time decay
        POW(0.5, TIMESTAMP_DIFF(c.conversion_timestamp, t.event_timestamp, DAY) / 7.0) /
            SUM(POW(0.5, TIMESTAMP_DIFF(c.conversion_timestamp, t.event_timestamp, DAY) / 7.0))
                OVER (PARTITION BY c.transaction_id) as time_decay_weight
    FROM touchpoints t
    JOIN conversions c ON t.user_pseudo_id = c.user_pseudo_id
    WHERE TIMESTAMP_MICROS(t.event_timestamp) <= c.conversion_timestamp
)
SELECT
    source,
    medium,
    campaign,
    COUNT(DISTINCT transaction_id) as conversions,
    SUM(revenue * first_touch_weight) as first_touch_revenue,
    SUM(revenue * last_touch_weight) as last_touch_revenue,
    SUM(revenue * linear_weight) as linear_revenue,
    SUM(revenue * time_decay_weight) as time_decay_revenue
FROM attributed_touches
GROUP BY source, medium, campaign
ORDER BY time_decay_revenue DESC;

-- Join with Google Ads cost data for ROI
SELECT
    a.*,
    g.cost_micros / 1000000 as ad_spend,
    ROUND(a.time_decay_revenue / NULLIF(g.cost_micros / 1000000, 0), 2) as roas,
    ROUND((a.time_decay_revenue - g.cost_micros / 1000000) /
        NULLIF(g.cost_micros / 1000000, 0) * 100, 2) as roi_percent
FROM `project.marketing_data.attribution_analysis` a
LEFT JOIN (
    SELECT
        campaign_name,
        SUM(cost_micros) as cost_micros
    FROM `project.google_ads.campaign_stats`
    WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
    GROUP BY campaign_name
) g ON LOWER(a.campaign) = LOWER(g.campaign_name)
ORDER BY time_decay_revenue DESC;
```

### 4. ML-Powered Predictions and Audiences

**Predict Customer LTV**

```sql
-- Use BigQuery ML to predict customer lifetime value
CREATE OR REPLACE MODEL `project.marketing_data.ltv_prediction_model`
OPTIONS(
    model_type='LINEAR_REG',
    input_label_cols=['lifetime_value']
) AS
SELECT
    active_days,
    sessions,
    page_views,
    days_since_last_visit,
    ga4_revenue as lifetime_value
FROM `project.marketing_data.customer_360`
WHERE ga4_revenue > 0;

-- Predict LTV for prospects
SELECT
    user_id,
    email,
    predicted_lifetime_value,
    predicted_lifetime_value_standard_error
FROM ML.PREDICT(
    MODEL `project.marketing_data.ltv_prediction_model`,
    (
        SELECT
            user_id,
            email,
            active_days,
            sessions,
            page_views,
            days_since_last_visit
        FROM `project.marketing_data.customer_360`
        WHERE ga4_revenue = 0
    )
)
ORDER BY predicted_lifetime_value DESC
LIMIT 1000;
```

**Churn Prediction**

```sql
-- Predict customer churn
CREATE OR REPLACE MODEL `project.marketing_data.churn_prediction_model`
OPTIONS(
    model_type='LOGISTIC_REG',
    input_label_cols=['churned']
) AS
SELECT
    active_days,
    sessions,
    page_views,
    days_since_last_visit,
    ga4_revenue,
    CASE WHEN days_since_last_visit > 60 THEN 1 ELSE 0 END as churned
FROM `project.marketing_data.customer_360`
WHERE ga4_revenue > 0;

-- Identify high churn risk customers
CREATE OR REPLACE TABLE `project.marketing_data.churn_risk_audience` AS
SELECT
    user_id,
    email,
    predicted_churned_probs[OFFSET(1)].prob as churn_probability,
    'churn_risk' as audience_name
FROM ML.PREDICT(
    MODEL `project.marketing_data.churn_prediction_model`,
    (
        SELECT
            user_id,
            email,
            active_days,
            sessions,
            page_views,
            days_since_last_visit,
            ga4_revenue
        FROM `project.marketing_data.customer_360`
        WHERE ga4_revenue > 0
            AND days_since_last_visit <= 60
    )
)
WHERE predicted_churned_probs[OFFSET(1)].prob > 0.7
ORDER BY churn_probability DESC;
```

## Installation and Authentication

### Python Client Library

```bash
pip install google-cloud-bigquery
pip install pandas-gbq
```

**Authentication with Service Account**

```python
from google.cloud import bigquery
from google.oauth2 import service_account

# Load credentials
credentials = service_account.Credentials.from_service_account_file(
    'path/to/service-account-key.json'
)

# Create client
client = bigquery.Client(
    credentials=credentials,
    project='your-project-id'
)

# Run query
query = """
SELECT user_id, email, ga4_revenue
FROM `project.marketing_data.customer_360`
WHERE ga4_revenue > 1000
LIMIT 100
"""

df = client.query(query).to_dataframe()
print(df.head())
```

**Using pandas-gbq**

```python
import pandas_gbq

# Query with pandas
sql = """
SELECT * FROM `project.marketing_data.customer_360`
WHERE value_segment = 'high_value'
"""

df = pandas_gbq.read_gbq(
    sql,
    project_id='your-project-id',
    credentials=credentials
)
```

## Quick Start

### Complete Marketing Analytics Workflow

```python
from google.cloud import bigquery
import pandas as pd

# Initialize client
client = bigquery.Client(project='your-project-id')

# 1. Analyze GA4 conversion funnel
funnel_query = """
SELECT
    DATE(TIMESTAMP_MICROS(event_timestamp)) as date,
    COUNT(DISTINCT CASE WHEN event_name = 'page_view' THEN user_pseudo_id END) as visitors,
    COUNT(DISTINCT CASE WHEN event_name = 'view_item' THEN user_pseudo_id END) as product_viewers,
    COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_pseudo_id END) as cart_users,
    COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_pseudo_id END) as purchasers,
    SUM(CASE WHEN event_name = 'purchase'
        THEN (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'value') ELSE 0 END) / 1000000 as revenue
FROM `project.analytics_PROPERTY_ID.events_*`
WHERE _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
GROUP BY date
ORDER BY date DESC
"""

funnel_df = client.query(funnel_query).to_dataframe()
print("\nConversion Funnel:")
print(funnel_df.head())

# 2. Get high-value audience for Google Ads
audience_query = """
SELECT user_id, email
FROM `project.marketing_data.customer_360`
WHERE value_segment = 'high_value'
    AND days_since_last_visit <= 30
LIMIT 10000
"""

audience_df = client.query(audience_query).to_dataframe()
print(f"\nHigh-value audience size: {len(audience_df)}")

# 3. Calculate campaign ROI
roi_query = """
SELECT * FROM `project.marketing_data.attribution_analysis`
WHERE time_decay_revenue > 0
ORDER BY time_decay_revenue DESC
LIMIT 10
"""

roi_df = client.query(roi_query).to_dataframe()
print("\nTop Campaigns by Attributed Revenue:")
print(roi_df)
```

## References

- **Official Documentation**: https://cloud.google.com/bigquery/docs
- **Python Client**: https://cloud.google.com/python/docs/reference/bigquery/latest
- **GA4 BigQuery Export**: https://support.google.com/analytics/answer/9358801
- **GA4 Export Schema**: https://support.google.com/analytics/answer/7029846
- **BigQuery ML**: https://cloud.google.com/bigquery-ml/docs
- **Google Ads Integration**: https://cloud.google.com/bigquery/docs/google-ads-integration
- **SQL Reference**: https://cloud.google.com/bigquery/docs/reference/standard-sql/
- **Best Practices**: https://cloud.google.com/bigquery/docs/best-practices
- **Cost Optimization**: https://cloud.google.com/bigquery/docs/best-practices-costs
- **Data Transfer Service**: https://cloud.google.com/bigquery-transfer/docs/introduction

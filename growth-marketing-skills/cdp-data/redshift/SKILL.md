---
skill_name: redshift
display_name: Amazon Redshift
description: AWS cloud data warehouse for marketing analytics, customer data, and cross-channel attribution
category: cdp-data
tags: [data-warehouse, aws, analytics, sql, marketing-analytics]
complexity: intermediate
dependencies: [psycopg2, sqlalchemy, pandas]
---

# Amazon Redshift

## Overview

Amazon Redshift is a fast, fully managed cloud data warehouse on AWS that enables petabyte-scale analytics. For marketing teams, Redshift provides a cost-effective platform for unifying customer data, analyzing attribution, and powering audience activation.

Redshift excels at:
- **AWS Ecosystem Integration**: Native integration with S3, Lambda, SageMaker
- **Marketing Data Consolidation**: Centralize data from CDPs, ad platforms, and CRM
- **Cost-Effective Analytics**: Columnar storage and compression for efficient queries
- **Scalable Performance**: Handle billions of events with automatic scaling
- **Spectrum for Data Lakes**: Query S3 data without loading into Redshift
- **Redshift ML**: Build ML models for predictions directly in SQL

## When to Use

Use Redshift when you need to:
- **AWS-Native Architecture**: Leverage existing AWS infrastructure
- **Cost-Optimized Warehouse**: Lower costs compared to competitors for large datasets
- **S3 Data Lake Integration**: Query raw data in S3 with Redshift Spectrum
- **Customer 360 Analytics**: Build unified customer profiles from multiple sources
- **Marketing Attribution**: Analyze multi-touch attribution across channels
- **Audience Segmentation**: Create complex segments for activation
- **Predictive Analytics**: Use Redshift ML for churn, LTV, and propensity models

## Core Capabilities

### 1. Marketing Data Ingestion

**Loading CDP Data from S3**

```sql
-- Create schema for marketing data
CREATE SCHEMA marketing_data;

-- Create table for CDP events (Segment/RudderStack format)
CREATE TABLE marketing_data.events (
    id VARCHAR(255),
    user_id VARCHAR(255),
    anonymous_id VARCHAR(255),
    event VARCHAR(255),
    timestamp TIMESTAMP,
    properties VARCHAR(65535),  -- JSON string
    context VARCHAR(65535),  -- JSON string
    revenue DECIMAL(10,2),
    utm_source VARCHAR(255),
    utm_medium VARCHAR(255),
    utm_campaign VARCHAR(255),
    utm_content VARCHAR(255)
)
DISTKEY(user_id)
SORTKEY(timestamp);

-- Load from S3 using COPY command (most efficient)
COPY marketing_data.events
FROM 's3://your-bucket/segment-data/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftS3Role'
FORMAT AS JSON 'auto'
TIMEFORMAT 'auto'
REGION 'us-east-1';

-- Create table for user identities
CREATE TABLE marketing_data.user_identities (
    user_id VARCHAR(255),
    anonymous_id VARCHAR(255),
    email VARCHAR(255),
    name VARCHAR(255),
    traits VARCHAR(65535),  -- JSON
    first_seen TIMESTAMP,
    last_seen TIMESTAMP
)
DISTKEY(user_id)
SORTKEY(user_id);

-- Parse JSON properties for common fields
CREATE OR REPLACE VIEW marketing_data.events_parsed AS
SELECT
    id,
    user_id,
    event,
    timestamp,
    -- Parse JSON properties
    JSON_EXTRACT_PATH_TEXT(properties, 'revenue') ::DECIMAL(10,2) as revenue,
    JSON_EXTRACT_PATH_TEXT(properties, 'order_id') as order_id,
    JSON_EXTRACT_PATH_TEXT(properties, 'product_id') as product_id,
    JSON_EXTRACT_PATH_TEXT(properties, 'category') as category,
    -- Parse UTM parameters from context
    JSON_EXTRACT_PATH_TEXT(context, 'campaign', 'source') as utm_source,
    JSON_EXTRACT_PATH_TEXT(context, 'campaign', 'medium') as utm_medium,
    JSON_EXTRACT_PATH_TEXT(context, 'campaign', 'name') as utm_campaign,
    JSON_EXTRACT_PATH_TEXT(context, 'campaign', 'content') as utm_content
FROM marketing_data.events;
```

**Loading Ad Platform Data**

```python
import psycopg2
import pandas as pd
from io import StringIO

def load_ad_platform_data(conn, platform_name, df):
    """Load ad platform data into Redshift"""

    # Create table for ad platform
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS marketing_data.{platform_name}_ads (
        date DATE,
        campaign_id VARCHAR(255),
        campaign_name VARCHAR(500),
        ad_id VARCHAR(255),
        ad_name VARCHAR(500),
        impressions BIGINT,
        clicks BIGINT,
        spend DECIMAL(10,2),
        conversions BIGINT,
        conversion_value DECIMAL(10,2),
        loaded_at TIMESTAMP DEFAULT GETDATE()
    )
    DISTKEY(campaign_id)
    SORTKEY(date);
    """

    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()

    # Use COPY from S3 for large datasets (recommended)
    # Or use INSERT for smaller datasets
    insert_sql = f"""
    INSERT INTO marketing_data.{platform_name}_ads
    (date, campaign_id, campaign_name, ad_id, ad_name, impressions, clicks, spend, conversions, conversion_value)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Batch insert
    data_tuples = list(df.itertuples(index=False, name=None))
    cursor.executemany(insert_sql, data_tuples)
    conn.commit()
    cursor.close()

# Example usage
import psycopg2

conn = psycopg2.connect(
    host='your-cluster.region.redshift.amazonaws.com',
    port=5439,
    dbname='marketing',
    user='your_user',
    password='your_password'
)

# Load Facebook Ads data
facebook_ads_df = pd.DataFrame({
    'date': ['2024-11-29'],
    'campaign_id': ['123456'],
    'campaign_name': ['Black Friday Sale'],
    'ad_id': ['789012'],
    'ad_name': ['BF Promo Ad'],
    'impressions': [10000],
    'clicks': [500],
    'spend': [250.00],
    'conversions': [25],
    'conversion_value': [1250.00]
})

load_ad_platform_data(conn, 'facebook', facebook_ads_df)
```

### 2. Customer 360 Views

**Unified Customer Profile**

```sql
-- Create comprehensive customer 360 view
CREATE OR REPLACE VIEW marketing_data.customer_360 AS
WITH user_profile AS (
    SELECT
        user_id,
        email,
        JSON_EXTRACT_PATH_TEXT(traits, 'name') as name,
        JSON_EXTRACT_PATH_TEXT(traits, 'plan') as plan,
        JSON_EXTRACT_PATH_TEXT(traits, 'company') as company,
        MIN(first_seen) as first_seen,
        MAX(last_seen) as last_seen
    FROM marketing_data.user_identities
    GROUP BY user_id, email, name, plan, company
),
user_behavior AS (
    SELECT
        user_id,
        COUNT(DISTINCT DATE(timestamp)) as active_days_90d,
        COUNT(DISTINCT CASE WHEN event = 'Page Viewed' THEN id END) as page_views_90d,
        COUNT(DISTINCT CASE WHEN event LIKE '%Product%' THEN id END) as product_interactions_90d,
        MAX(timestamp) as last_activity_date
    FROM marketing_data.events
    WHERE timestamp >= DATEADD(day, -90, GETDATE())
    GROUP BY user_id
),
user_revenue AS (
    SELECT
        user_id,
        COUNT(DISTINCT CASE WHEN event = 'Order Completed'
            THEN JSON_EXTRACT_PATH_TEXT(properties, 'order_id') END) as total_orders,
        SUM(CASE WHEN event = 'Order Completed'
            THEN JSON_EXTRACT_PATH_TEXT(properties, 'revenue')::DECIMAL(10,2) ELSE 0 END) as lifetime_revenue,
        SUM(CASE WHEN event = 'Order Completed'
            AND timestamp >= DATEADD(day, -90, GETDATE())
            THEN JSON_EXTRACT_PATH_TEXT(properties, 'revenue')::DECIMAL(10,2) ELSE 0 END) as revenue_90d,
        MAX(CASE WHEN event = 'Order Completed' THEN timestamp END) as last_purchase_date
    FROM marketing_data.events
    GROUP BY user_id
),
user_attribution AS (
    SELECT DISTINCT
        user_id,
        FIRST_VALUE(utm_source IGNORE NULLS) OVER (
            PARTITION BY user_id ORDER BY timestamp
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) as first_touch_source,
        FIRST_VALUE(utm_campaign IGNORE NULLS) OVER (
            PARTITION BY user_id ORDER BY timestamp
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) as first_touch_campaign,
        LAST_VALUE(utm_source IGNORE NULLS) OVER (
            PARTITION BY user_id ORDER BY timestamp
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) as last_touch_source,
        LAST_VALUE(utm_campaign IGNORE NULLS) OVER (
            PARTITION BY user_id ORDER BY timestamp
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) as last_touch_campaign
    FROM marketing_data.events_parsed
    WHERE utm_source IS NOT NULL
)
SELECT
    p.user_id,
    p.email,
    p.name,
    p.plan,
    p.company,
    p.first_seen,
    p.last_seen,
    -- Behavior metrics
    COALESCE(b.active_days_90d, 0) as active_days_90d,
    COALESCE(b.page_views_90d, 0) as page_views_90d,
    COALESCE(b.product_interactions_90d, 0) as product_interactions_90d,
    b.last_activity_date,
    -- Revenue metrics
    COALESCE(r.total_orders, 0) as total_orders,
    COALESCE(r.lifetime_revenue, 0) as lifetime_revenue,
    COALESCE(r.revenue_90d, 0) as revenue_90d,
    r.last_purchase_date,
    DATEDIFF(day, r.last_purchase_date, GETDATE()) as days_since_purchase,
    -- Attribution
    a.first_touch_source,
    a.first_touch_campaign,
    a.last_touch_source,
    a.last_touch_campaign,
    -- Segments
    CASE
        WHEN r.revenue_90d > 1000 THEN 'high_value'
        WHEN r.revenue_90d > 500 THEN 'medium_value'
        WHEN r.total_orders > 0 THEN 'low_value'
        ELSE 'prospect'
    END as customer_tier,
    CASE
        WHEN b.active_days_90d >= 20 THEN 'highly_engaged'
        WHEN b.active_days_90d >= 10 THEN 'engaged'
        WHEN b.active_days_90d >= 3 THEN 'casual'
        ELSE 'inactive'
    END as engagement_level
FROM user_profile p
LEFT JOIN user_behavior b ON p.user_id = b.user_id
LEFT JOIN user_revenue r ON p.user_id = r.user_id
LEFT JOIN user_attribution a ON p.user_id = a.user_id;
```

**Audience Segmentation**

```sql
-- High-value customers
CREATE TABLE marketing_data.audience_high_value AS
SELECT
    user_id,
    email,
    name,
    lifetime_revenue,
    revenue_90d,
    'high_value_customers' as audience_name,
    GETDATE() as created_at
FROM marketing_data.customer_360
WHERE revenue_90d > 1000
    AND days_since_purchase <= 90;

-- Churn risk segment
CREATE TABLE marketing_data.audience_churn_risk AS
SELECT
    user_id,
    email,
    name,
    lifetime_revenue,
    days_since_purchase,
    'churn_risk' as audience_name,
    GETDATE() as created_at
FROM marketing_data.customer_360
WHERE total_orders > 0
    AND days_since_purchase BETWEEN 60 AND 180
    AND lifetime_revenue > 500;

-- High-intent prospects
CREATE TABLE marketing_data.audience_high_intent AS
SELECT
    user_id,
    email,
    name,
    product_interactions_90d,
    page_views_90d,
    'high_intent_prospects' as audience_name,
    GETDATE() as created_at
FROM marketing_data.customer_360
WHERE total_orders = 0
    AND product_interactions_90d >= 3
    AND active_days_90d >= 5;
```

### 3. Marketing Attribution

**Multi-Touch Attribution**

```sql
-- Build multi-touch attribution model
CREATE OR REPLACE VIEW marketing_data.attribution_analysis AS
WITH touchpoints AS (
    SELECT
        user_id,
        timestamp,
        utm_source,
        utm_medium,
        utm_campaign,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp) as touch_number,
        COUNT(*) OVER (PARTITION BY user_id) as total_touches
    FROM marketing_data.events_parsed
    WHERE utm_source IS NOT NULL
),
conversions AS (
    SELECT
        user_id,
        JSON_EXTRACT_PATH_TEXT(properties, 'order_id') as order_id,
        timestamp as conversion_time,
        JSON_EXTRACT_PATH_TEXT(properties, 'revenue')::DECIMAL(10,2) as revenue
    FROM marketing_data.events
    WHERE event = 'Order Completed'
),
attributed_touches AS (
    SELECT
        t.user_id,
        c.order_id,
        c.revenue,
        t.utm_source,
        t.utm_medium,
        t.utm_campaign,
        t.touch_number,
        t.total_touches,
        -- Attribution weights
        CASE WHEN t.touch_number = 1 THEN 1.0 ELSE 0 END as first_touch_weight,
        CASE WHEN t.touch_number = t.total_touches THEN 1.0 ELSE 0 END as last_touch_weight,
        1.0 / t.total_touches as linear_weight,
        -- Time decay (7-day half-life)
        POW(0.5, DATEDIFF(day, t.timestamp, c.conversion_time) / 7.0) as time_decay_base
    FROM touchpoints t
    JOIN conversions c ON t.user_id = c.user_id
    WHERE t.timestamp <= c.conversion_time
),
time_decay_normalized AS (
    SELECT
        *,
        time_decay_base / SUM(time_decay_base) OVER (PARTITION BY order_id) as time_decay_weight
    FROM attributed_touches
)
SELECT
    utm_source,
    utm_medium,
    utm_campaign,
    COUNT(DISTINCT order_id) as total_conversions,
    SUM(revenue * first_touch_weight) as first_touch_revenue,
    SUM(revenue * last_touch_weight) as last_touch_revenue,
    SUM(revenue * linear_weight) as linear_revenue,
    SUM(revenue * time_decay_weight) as time_decay_revenue
FROM time_decay_normalized
GROUP BY utm_source, utm_medium, utm_campaign
ORDER BY time_decay_revenue DESC;
```

**Campaign ROI Analysis**

```sql
-- Combine ad spend with attributed revenue
CREATE OR REPLACE VIEW marketing_data.campaign_roi AS
WITH ad_spend AS (
    SELECT
        date,
        'facebook' as platform,
        campaign_name,
        SUM(spend) as spend,
        SUM(impressions) as impressions,
        SUM(clicks) as clicks
    FROM marketing_data.facebook_ads
    GROUP BY date, campaign_name

    UNION ALL

    SELECT
        date,
        'google' as platform,
        campaign_name,
        SUM(spend) as spend,
        SUM(impressions) as impressions,
        SUM(clicks) as clicks
    FROM marketing_data.google_ads
    GROUP BY date, campaign_name
),
campaign_revenue AS (
    SELECT
        utm_campaign,
        SUM(time_decay_revenue) as attributed_revenue,
        COUNT(DISTINCT order_id) as conversions
    FROM marketing_data.attribution_analysis
    GROUP BY utm_campaign
)
SELECT
    s.date,
    s.platform,
    s.campaign_name,
    s.spend,
    s.impressions,
    s.clicks,
    ROUND(s.spend / NULLIF(s.clicks, 0), 2) as cpc,
    COALESCE(r.attributed_revenue, 0) as attributed_revenue,
    COALESCE(r.conversions, 0) as conversions,
    ROUND(COALESCE(r.attributed_revenue, 0) / NULLIF(s.spend, 0), 2) as roas,
    ROUND(s.spend / NULLIF(r.conversions, 0), 2) as cpa,
    ROUND((COALESCE(r.attributed_revenue, 0) - s.spend) / NULLIF(s.spend, 0) * 100, 2) as roi_percent
FROM ad_spend s
LEFT JOIN campaign_revenue r ON LOWER(s.campaign_name) = LOWER(r.utm_campaign)
ORDER BY s.date DESC, attributed_revenue DESC;
```

### 4. Redshift ML for Predictive Marketing

**Predict Customer LTV**

```sql
-- Create LTV prediction model
CREATE MODEL marketing_data.ltv_prediction_model
FROM (
    SELECT
        active_days_90d,
        page_views_90d,
        product_interactions_90d,
        days_since_purchase,
        total_orders,
        lifetime_revenue as target
    FROM marketing_data.customer_360
    WHERE lifetime_revenue > 0
)
TARGET target
FUNCTION predict_ltv
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftMLRole'
SETTINGS (
    S3_BUCKET 'your-ml-bucket',
    MAX_RUNTIME 5400
);

-- Predict LTV for prospects
SELECT
    user_id,
    email,
    marketing_data.predict_ltv(
        active_days_90d,
        page_views_90d,
        product_interactions_90d,
        days_since_purchase,
        total_orders
    ) as predicted_ltv
FROM marketing_data.customer_360
WHERE total_orders = 0
ORDER BY predicted_ltv DESC
LIMIT 1000;
```

**Churn Prediction**

```sql
-- Create churn prediction model
CREATE MODEL marketing_data.churn_prediction_model
FROM (
    SELECT
        active_days_90d,
        page_views_90d,
        days_since_purchase,
        lifetime_revenue,
        CASE WHEN days_since_purchase > 90 THEN 1 ELSE 0 END as is_churned
    FROM marketing_data.customer_360
    WHERE total_orders > 0
)
TARGET is_churned
FUNCTION predict_churn
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftMLRole'
SETTINGS (
    S3_BUCKET 'your-ml-bucket',
    MODEL_TYPE 'XGBOOST',
    OBJECTIVE 'BINARY:LOGISTIC'
);

-- Identify churn risk customers
SELECT
    user_id,
    email,
    lifetime_revenue,
    marketing_data.predict_churn(
        active_days_90d,
        page_views_90d,
        days_since_purchase,
        lifetime_revenue
    ) as churn_probability
FROM marketing_data.customer_360
WHERE total_orders > 0
    AND days_since_purchase <= 90
HAVING churn_probability > 0.7
ORDER BY churn_probability DESC;
```

## Installation and Authentication

### Python Connection (psycopg2)

```bash
pip install psycopg2-binary
pip install sqlalchemy
pip install pandas
```

```python
import psycopg2
import pandas as pd

# Connect to Redshift
conn = psycopg2.connect(
    host='your-cluster.region.redshift.amazonaws.com',
    port=5439,
    dbname='marketing',
    user='your_user',
    password='your_password'
)

# Query data
query = "SELECT * FROM marketing_data.customer_360 LIMIT 100"
df = pd.read_sql(query, conn)

print(df.head())
conn.close()
```

### SQLAlchemy for Pandas

```python
from sqlalchemy import create_engine
import pandas as pd

# Create engine
engine = create_engine(
    'postgresql://your_user:your_password@your-cluster.region.redshift.amazonaws.com:5439/marketing'
)

# Query with pandas
df = pd.read_sql(
    "SELECT * FROM marketing_data.customer_360 WHERE customer_tier = 'high_value'",
    engine
)
```

## Quick Start

### Complete Marketing Analytics Setup

```python
import psycopg2
import pandas as pd

# Connect to Redshift
conn = psycopg2.connect(
    host='your-cluster.region.redshift.amazonaws.com',
    port=5439,
    dbname='marketing',
    user='your_user',
    password='your_password'
)

cursor = conn.cursor()

# 1. Create marketing schema
cursor.execute("CREATE SCHEMA IF NOT EXISTS marketing_data")
conn.commit()

# 2. Query customer 360
query = """
SELECT
    customer_tier,
    engagement_level,
    COUNT(*) as customers,
    SUM(lifetime_revenue) as total_revenue,
    AVG(lifetime_revenue) as avg_revenue
FROM marketing_data.customer_360
GROUP BY customer_tier, engagement_level
ORDER BY total_revenue DESC
"""

customer_segments = pd.read_sql(query, conn)
print("\nCustomer Segments:")
print(customer_segments)

# 3. Get campaign ROI
roi_query = """
SELECT
    platform,
    campaign_name,
    SUM(spend) as total_spend,
    SUM(attributed_revenue) as total_revenue,
    AVG(roas) as avg_roas
FROM marketing_data.campaign_roi
WHERE date >= DATEADD(day, -30, GETDATE())
GROUP BY platform, campaign_name
ORDER BY total_revenue DESC
LIMIT 10
"""

campaign_roi = pd.read_sql(roi_query, conn)
print("\nTop Campaigns:")
print(campaign_roi)

# 4. Export high-value audience
audience_query = """
SELECT user_id, email, lifetime_revenue
FROM marketing_data.audience_high_value
"""

audience_df = pd.read_sql(audience_query, conn)
audience_df.to_csv('high_value_audience.csv', index=False)
print(f"\nExported {len(audience_df)} high-value customers")

cursor.close()
conn.close()
```

## References

- **Official Documentation**: https://docs.aws.amazon.com/redshift/
- **Python Client (psycopg2)**: https://www.psycopg.org/docs/
- **COPY Command**: https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html
- **Redshift Spectrum**: https://docs.aws.amazon.com/redshift/latest/dg/c-using-spectrum.html
- **Redshift ML**: https://docs.aws.amazon.com/redshift/latest/dg/machine_learning.html
- **SQL Reference**: https://docs.aws.amazon.com/redshift/latest/dg/c_SQL_commands.html
- **Best Practices**: https://docs.aws.amazon.com/redshift/latest/dg/best-practices.html
- **Performance Tuning**: https://docs.aws.amazon.com/redshift/latest/dg/c-optimizing-query-performance.html
- **Data Loading**: https://docs.aws.amazon.com/redshift/latest/dg/t_Loading_data.html
- **Security**: https://docs.aws.amazon.com/redshift/latest/mgmt/security.html

---
skill_name: snowflake
display_name: Snowflake
description: Cloud data warehouse for marketing analytics, customer 360, and multi-touch attribution
category: cdp-data
tags: [data-warehouse, analytics, sql, cloud, marketing-analytics]
complexity: intermediate
dependencies: [snowflake-connector-python, snowflake-sqlalchemy]
---

# Snowflake Data Warehouse

## Overview

Snowflake is a cloud-native data warehouse platform optimized for analytics workloads. For marketing teams, Snowflake serves as the central repository for customer data, enabling sophisticated attribution modeling, customer 360 views, and audience activation.

Snowflake excels at:
- **Unified Customer Data**: Centralize data from CDPs, ad platforms, CRM, and analytics tools
- **Marketing Attribution**: Build complex multi-touch attribution models
- **Audience Segmentation**: Create sophisticated customer segments at scale
- **Real-Time Analytics**: Query billions of events with sub-second latency
- **Data Sharing**: Securely share data with partners and agencies
- **Cost Optimization**: Separate compute from storage for efficient scaling

## When to Use

Use Snowflake when you need to:
- **Centralize Marketing Data**: Unify data from all marketing platforms
- **Customer 360 Analytics**: Build complete customer profiles across touchpoints
- **Attribution Modeling**: Analyze multi-touch attribution across channels
- **Audience Building**: Create complex segments for activation
- **Campaign Performance**: Analyze ROI across all marketing campaigns
- **Predictive Analytics**: Build ML models for churn, LTV, propensity
- **Data Collaboration**: Share data securely with agencies and partners

## Core Capabilities

### 1. Marketing Data Ingestion

**Loading CDP Data (Segment/RudderStack)**

```sql
-- Create database for marketing data
CREATE DATABASE marketing_data;
CREATE SCHEMA marketing_data.customer_events;

-- Segment/RudderStack automatically creates tables
-- Standard schema: identifies, tracks, pages, groups

-- Query event data
SELECT
    user_id,
    event,
    timestamp,
    properties,
    context
FROM marketing_data.customer_events.tracks
WHERE event = 'Order Completed'
    AND DATE(timestamp) = CURRENT_DATE;

-- Create optimized views for analysis
CREATE OR REPLACE VIEW marketing_data.analytics.user_events AS
SELECT
    user_id,
    event,
    timestamp,
    -- Extract common properties
    properties:revenue::FLOAT as revenue,
    properties:order_id::STRING as order_id,
    properties:product_id::STRING as product_id,
    -- Extract UTM parameters
    context:campaign:source::STRING as utm_source,
    context:campaign:medium::STRING as utm_medium,
    context:campaign:name::STRING as utm_campaign,
    context:campaign:content::STRING as utm_content,
    -- Extract device info
    context:device:type::STRING as device_type,
    context:os:name::STRING as os_name
FROM marketing_data.customer_events.tracks;
```

**Loading Ad Platform Data**

```python
# Use Fivetran, Airbyte, or custom scripts to load ad platform data
from snowflake.connector import connect
import pandas as pd

def load_facebook_ads_data(conn, ads_data):
    """Load Facebook Ads performance data"""

    # Create table for ad performance
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS marketing_data.ad_platforms.facebook_ads (
        date DATE,
        campaign_id VARCHAR,
        campaign_name VARCHAR,
        ad_set_id VARCHAR,
        ad_set_name VARCHAR,
        ad_id VARCHAR,
        ad_name VARCHAR,
        impressions NUMBER,
        clicks NUMBER,
        spend FLOAT,
        conversions NUMBER,
        conversion_value FLOAT,
        loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
    );
    """

    cursor = conn.cursor()
    cursor.execute(create_table_sql)

    # Insert data
    ads_data.to_sql(
        'facebook_ads',
        schema='marketing_data.ad_platforms',
        con=conn,
        if_exists='append',
        index=False,
        method='multi'
    )

    cursor.close()

# Similar tables for Google Ads, LinkedIn, etc.
def create_ad_platform_tables(conn):
    """Create standardized tables for all ad platforms"""

    tables = {
        'google_ads': """
            CREATE TABLE IF NOT EXISTS marketing_data.ad_platforms.google_ads (
                date DATE,
                campaign_id VARCHAR,
                campaign_name VARCHAR,
                ad_group_id VARCHAR,
                ad_group_name VARCHAR,
                keyword VARCHAR,
                impressions NUMBER,
                clicks NUMBER,
                cost FLOAT,
                conversions NUMBER,
                conversion_value FLOAT,
                loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            );
        """,
        'linkedin_ads': """
            CREATE TABLE IF NOT EXISTS marketing_data.ad_platforms.linkedin_ads (
                date DATE,
                campaign_id VARCHAR,
                campaign_name VARCHAR,
                creative_id VARCHAR,
                impressions NUMBER,
                clicks NUMBER,
                spend FLOAT,
                conversions NUMBER,
                loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            );
        """
    }

    cursor = conn.cursor()
    for table_sql in tables.values():
        cursor.execute(table_sql)
    cursor.close()
```

### 2. Customer 360 Views and Segmentation

**Build Unified Customer Profiles**

```sql
-- Create comprehensive customer 360 view
CREATE OR REPLACE VIEW marketing_data.analytics.customer_360 AS
WITH user_profile AS (
    -- Latest user attributes from identifies table
    SELECT
        user_id,
        email,
        traits:name::STRING as name,
        traits:plan::STRING as plan,
        traits:company::STRING as company,
        MIN(timestamp) as first_seen,
        MAX(timestamp) as last_seen
    FROM marketing_data.customer_events.identifies
    GROUP BY user_id, email, traits:name, traits:plan, traits:company
),
user_behavior AS (
    -- Aggregate user behavior metrics
    SELECT
        user_id,
        COUNT(DISTINCT DATE(timestamp)) as active_days,
        COUNT(DISTINCT CASE WHEN event = 'Page Viewed' THEN id END) as page_views,
        COUNT(DISTINCT CASE WHEN event = 'Product Viewed' THEN id END) as products_viewed,
        COUNT(DISTINCT CASE WHEN event LIKE '%Added%' THEN id END) as cart_adds,
        MAX(timestamp) as last_active_date
    FROM marketing_data.customer_events.tracks
    WHERE timestamp >= CURRENT_DATE - INTERVAL '90 days'
    GROUP BY user_id
),
user_revenue AS (
    -- Revenue metrics
    SELECT
        user_id,
        COUNT(DISTINCT CASE WHEN event = 'Order Completed' THEN properties:order_id END) as total_orders,
        SUM(CASE WHEN event = 'Order Completed' THEN properties:revenue::FLOAT ELSE 0 END) as lifetime_revenue,
        SUM(CASE WHEN event = 'Order Completed'
            AND timestamp >= CURRENT_DATE - INTERVAL '90 days'
            THEN properties:revenue::FLOAT ELSE 0 END) as revenue_90d,
        MAX(CASE WHEN event = 'Order Completed' THEN timestamp END) as last_purchase_date,
        MIN(CASE WHEN event = 'Order Completed' THEN timestamp END) as first_purchase_date
    FROM marketing_data.customer_events.tracks
    GROUP BY user_id
),
user_attribution AS (
    -- First and last touch attribution
    SELECT
        user_id,
        FIRST_VALUE(context:campaign:source) OVER (
            PARTITION BY user_id ORDER BY timestamp
        ) as first_touch_source,
        FIRST_VALUE(context:campaign:campaign) OVER (
            PARTITION BY user_id ORDER BY timestamp
        ) as first_touch_campaign,
        LAST_VALUE(context:campaign:source) OVER (
            PARTITION BY user_id ORDER BY timestamp
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) as last_touch_source,
        LAST_VALUE(context:campaign:campaign) OVER (
            PARTITION BY user_id ORDER BY timestamp
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) as last_touch_campaign
    FROM marketing_data.customer_events.tracks
    WHERE context:campaign:source IS NOT NULL
    QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp DESC) = 1
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
    COALESCE(b.active_days, 0) as active_days_90d,
    COALESCE(b.page_views, 0) as page_views_90d,
    COALESCE(b.products_viewed, 0) as products_viewed_90d,
    COALESCE(b.last_active_date, p.last_seen) as last_active_date,
    -- Revenue metrics
    COALESCE(r.total_orders, 0) as total_orders,
    COALESCE(r.lifetime_revenue, 0) as lifetime_revenue,
    COALESCE(r.revenue_90d, 0) as revenue_90d,
    r.last_purchase_date,
    r.first_purchase_date,
    DATEDIFF('day', r.last_purchase_date, CURRENT_DATE) as days_since_purchase,
    -- Attribution
    a.first_touch_source,
    a.first_touch_campaign,
    a.last_touch_source,
    a.last_touch_campaign,
    -- Computed segments
    CASE
        WHEN r.revenue_90d > 1000 THEN 'high_value'
        WHEN r.revenue_90d > 500 THEN 'medium_value'
        WHEN r.total_orders > 0 THEN 'low_value'
        ELSE 'prospect'
    END as customer_tier,
    CASE
        WHEN b.active_days >= 20 THEN 'highly_engaged'
        WHEN b.active_days >= 10 THEN 'engaged'
        WHEN b.active_days >= 3 THEN 'casual'
        ELSE 'inactive'
    END as engagement_level
FROM user_profile p
LEFT JOIN user_behavior b ON p.user_id = b.user_id
LEFT JOIN user_revenue r ON p.user_id = r.user_id
LEFT JOIN user_attribution a ON p.user_id = a.user_id;
```

**Audience Segmentation for Activation**

```sql
-- High-value customers for retention campaigns
CREATE OR REPLACE VIEW marketing_data.audiences.high_value_customers AS
SELECT
    user_id,
    email,
    name,
    lifetime_revenue,
    revenue_90d,
    total_orders,
    last_purchase_date,
    'high_value_retention' as audience_name,
    CURRENT_TIMESTAMP as audience_updated_at
FROM marketing_data.analytics.customer_360
WHERE lifetime_revenue > 1000
    AND days_since_purchase <= 90;

-- Churn risk segment
CREATE OR REPLACE VIEW marketing_data.audiences.churn_risk AS
SELECT
    user_id,
    email,
    name,
    lifetime_revenue,
    days_since_purchase,
    last_purchase_date,
    'churn_risk' as audience_name,
    CURRENT_TIMESTAMP as audience_updated_at
FROM marketing_data.analytics.customer_360
WHERE total_orders > 0
    AND days_since_purchase > 60
    AND days_since_purchase < 180
    AND lifetime_revenue > 500;

-- High-intent prospects
CREATE OR REPLACE VIEW marketing_data.audiences.high_intent_prospects AS
SELECT
    user_id,
    email,
    name,
    products_viewed_90d,
    page_views_90d,
    active_days_90d,
    'high_intent_prospect' as audience_name,
    CURRENT_TIMESTAMP as audience_updated_at
FROM marketing_data.analytics.customer_360
WHERE total_orders = 0
    AND products_viewed_90d >= 3
    AND active_days_90d >= 5;

-- Cart abandoners
CREATE OR REPLACE VIEW marketing_data.audiences.cart_abandoners AS
WITH recent_carts AS (
    SELECT
        user_id,
        MAX(timestamp) as last_cart_add,
        COUNT(DISTINCT properties:product_id) as products_in_cart
    FROM marketing_data.customer_events.tracks
    WHERE event IN ('Product Added', 'Cart Updated')
        AND timestamp >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY user_id
),
recent_purchases AS (
    SELECT DISTINCT user_id
    FROM marketing_data.customer_events.tracks
    WHERE event = 'Order Completed'
        AND timestamp >= CURRENT_DATE - INTERVAL '7 days'
)
SELECT
    c.user_id,
    i.email,
    i.traits:name::STRING as name,
    c.last_cart_add,
    c.products_in_cart,
    'cart_abandoner' as audience_name,
    CURRENT_TIMESTAMP as audience_updated_at
FROM recent_carts c
JOIN marketing_data.customer_events.identifies i
    ON c.user_id = i.user_id
WHERE c.user_id NOT IN (SELECT user_id FROM recent_purchases)
    AND c.products_in_cart >= 1
QUALIFY ROW_NUMBER() OVER (PARTITION BY c.user_id ORDER BY i.timestamp DESC) = 1;
```

### 3. Marketing Attribution Analytics

**Multi-Touch Attribution Model**

```sql
-- Build comprehensive attribution model
CREATE OR REPLACE VIEW marketing_data.analytics.multi_touch_attribution AS
WITH user_touchpoints AS (
    SELECT
        user_id,
        timestamp as touchpoint_time,
        context:campaign:source::STRING as source,
        context:campaign:medium::STRING as medium,
        context:campaign:name::STRING as campaign,
        context:campaign:content::STRING as content,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp) as touch_number,
        COUNT(*) OVER (PARTITION BY user_id) as total_touches
    FROM marketing_data.customer_events.tracks
    WHERE context:campaign:source IS NOT NULL
),
conversions AS (
    SELECT
        user_id,
        properties:order_id::STRING as order_id,
        timestamp as conversion_time,
        properties:revenue::FLOAT as revenue
    FROM marketing_data.customer_events.tracks
    WHERE event = 'Order Completed'
),
attributed_touches AS (
    SELECT
        t.user_id,
        c.order_id,
        c.conversion_time,
        c.revenue,
        t.source,
        t.medium,
        t.campaign,
        t.touch_number,
        t.total_touches,
        t.touchpoint_time,
        DATEDIFF('hour', t.touchpoint_time, c.conversion_time) as hours_to_conversion,
        -- Attribution weights
        -- First touch
        CASE WHEN t.touch_number = 1 THEN 1.0 ELSE 0 END as first_touch_credit,
        -- Last touch
        CASE WHEN t.touch_number = t.total_touches THEN 1.0 ELSE 0 END as last_touch_credit,
        -- Linear (equal credit)
        1.0 / t.total_touches as linear_credit,
        -- Time decay (exponential decay with 7-day half-life)
        EXP(-0.693 * DATEDIFF('day', t.touchpoint_time, c.conversion_time) / 7.0) /
            SUM(EXP(-0.693 * DATEDIFF('day', t.touchpoint_time, c.conversion_time) / 7.0))
                OVER (PARTITION BY t.user_id, c.order_id) as time_decay_credit,
        -- U-shaped (40% first, 40% last, 20% middle)
        CASE
            WHEN t.total_touches = 1 THEN 1.0
            WHEN t.touch_number = 1 THEN 0.4
            WHEN t.touch_number = t.total_touches THEN 0.4
            ELSE 0.2 / (t.total_touches - 2)
        END as u_shaped_credit
    FROM user_touchpoints t
    JOIN conversions c ON t.user_id = c.user_id
    WHERE t.touchpoint_time <= c.conversion_time
)
SELECT
    source,
    medium,
    campaign,
    -- Conversions by attribution model
    COUNT(DISTINCT order_id) as total_conversions,
    -- Revenue by attribution model
    SUM(revenue * first_touch_credit) as first_touch_revenue,
    SUM(revenue * last_touch_credit) as last_touch_revenue,
    SUM(revenue * linear_credit) as linear_revenue,
    SUM(revenue * time_decay_credit) as time_decay_revenue,
    SUM(revenue * u_shaped_credit) as u_shaped_revenue,
    -- Average time to conversion
    AVG(CASE WHEN first_touch_credit > 0 THEN hours_to_conversion END) as avg_hours_to_conversion,
    -- Touch point position
    AVG(touch_number) as avg_touch_position,
    COUNT(*) as total_touchpoints
FROM attributed_touches
GROUP BY source, medium, campaign
ORDER BY time_decay_revenue DESC;
```

**Campaign ROI Analysis**

```sql
-- Combine ad spend with attributed revenue
CREATE OR REPLACE VIEW marketing_data.analytics.campaign_roi AS
WITH ad_spend AS (
    -- Union all ad platforms
    SELECT
        date,
        'facebook' as platform,
        campaign_name,
        SUM(spend) as spend,
        SUM(impressions) as impressions,
        SUM(clicks) as clicks
    FROM marketing_data.ad_platforms.facebook_ads
    GROUP BY date, campaign_name

    UNION ALL

    SELECT
        date,
        'google' as platform,
        campaign_name,
        SUM(cost) as spend,
        SUM(impressions) as impressions,
        SUM(clicks) as clicks
    FROM marketing_data.ad_platforms.google_ads
    GROUP BY date, campaign_name

    UNION ALL

    SELECT
        date,
        'linkedin' as platform,
        campaign_name,
        SUM(spend) as spend,
        SUM(impressions) as impressions,
        SUM(clicks) as clicks
    FROM marketing_data.ad_platforms.linkedin_ads
    GROUP BY date, campaign_name
),
campaign_revenue AS (
    -- Get attributed revenue by campaign
    SELECT
        DATE(conversion_time) as date,
        campaign,
        SUM(linear_revenue) as attributed_revenue,
        COUNT(DISTINCT order_id) as attributed_conversions
    FROM marketing_data.analytics.multi_touch_attribution
    GROUP BY DATE(conversion_time), campaign
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
    COALESCE(r.attributed_conversions, 0) as conversions,
    ROUND(COALESCE(r.attributed_revenue, 0) / NULLIF(s.spend, 0), 2) as roas,
    ROUND(s.spend / NULLIF(r.attributed_conversions, 0), 2) as cpa,
    ROUND((COALESCE(r.attributed_revenue, 0) - s.spend) / NULLIF(s.spend, 0) * 100, 2) as roi_percent
FROM ad_spend s
LEFT JOIN campaign_revenue r
    ON s.date = r.date
    AND LOWER(s.campaign_name) = LOWER(r.campaign)
ORDER BY s.date DESC, attributed_revenue DESC;
```

### 4. Audience Export for Ad Platform Sync

**Python: Export Audiences from Snowflake**

```python
import snowflake.connector
import pandas as pd
from datetime import datetime

class SnowflakeAudienceExport:
    def __init__(self, account, user, password, warehouse, database, schema):
        self.conn = snowflake.connector.connect(
            account=account,
            user=user,
            password=password,
            warehouse=warehouse,
            database=database,
            schema=schema
        )

    def export_audience(self, audience_view, destination='csv'):
        """Export audience from Snowflake view"""

        query = f"SELECT * FROM {audience_view}"
        df = pd.read_sql(query, self.conn)

        if destination == 'csv':
            filename = f"{audience_view}_{datetime.now().strftime('%Y%m%d')}.csv"
            df.to_csv(filename, index=False)
            return filename

        return df

    def export_for_facebook(self, audience_view):
        """Export audience formatted for Facebook Custom Audiences"""

        query = f"""
        SELECT
            LOWER(email) as email,
            REGEXP_REPLACE(phone, '[^0-9]', '') as phone,
            LOWER(name) as fn
        FROM {audience_view}
        WHERE email IS NOT NULL
        """

        df = pd.read_sql(query, self.conn)
        filename = f"facebook_audience_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False)

        return filename, len(df)

    def export_for_google_ads(self, audience_view):
        """Export audience formatted for Google Customer Match"""

        query = f"""
        SELECT
            LOWER(email) as Email,
            REGEXP_REPLACE(phone, '[^0-9]', '') as Phone,
            SPLIT_PART(name, ' ', 1) as "First Name",
            SPLIT_PART(name, ' ', -1) as "Last Name",
            country as Country,
            zip_code as "Zip Code"
        FROM {audience_view}
        WHERE email IS NOT NULL
        """

        df = pd.read_sql(query, self.conn)
        filename = f"google_customer_match_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False)

        return filename, len(df)

    def get_audience_stats(self, audience_view):
        """Get statistics about an audience"""

        query = f"""
        SELECT
            COUNT(*) as audience_size,
            COUNT(DISTINCT email) as unique_emails,
            SUM(lifetime_revenue) as total_ltv,
            AVG(lifetime_revenue) as avg_ltv,
            MAX(audience_updated_at) as last_updated
        FROM {audience_view}
        """

        return pd.read_sql(query, self.conn).iloc[0].to_dict()

# Example usage
exporter = SnowflakeAudienceExport(
    account='your_account',
    user='your_user',
    password='your_password',
    warehouse='COMPUTE_WH',
    database='marketing_data',
    schema='audiences'
)

# Export high-value customers to Facebook
fb_file, fb_count = exporter.export_for_facebook('high_value_customers')
print(f"Exported {fb_count} users to {fb_file}")

# Get audience stats
stats = exporter.get_audience_stats('high_value_customers')
print(f"Audience size: {stats['audience_size']}")
print(f"Total LTV: ${stats['total_ltv']:,.2f}")
```

## Installation and Authentication

### Python Connector

```bash
pip install snowflake-connector-python
pip install snowflake-sqlalchemy
```

```python
import snowflake.connector

# Connect to Snowflake
conn = snowflake.connector.connect(
    account='your_account',
    user='your_username',
    password='your_password',
    warehouse='COMPUTE_WH',
    database='marketing_data',
    schema='analytics'
)

# Create cursor
cursor = conn.cursor()

# Execute query
cursor.execute("SELECT CURRENT_VERSION()")
print(cursor.fetchone())

cursor.close()
conn.close()
```

### SQLAlchemy (for Pandas)

```python
from sqlalchemy import create_engine
import pandas as pd

# Create engine
engine = create_engine(
    'snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}'.format(
        user='your_user',
        password='your_password',
        account='your_account',
        database='marketing_data',
        schema='analytics',
        warehouse='COMPUTE_WH'
    )
)

# Query with pandas
df = pd.read_sql("SELECT * FROM customer_360 LIMIT 1000", engine)
```

## Quick Start

### Complete Marketing Analytics Setup

```python
import snowflake.connector
import pandas as pd

# Connect
conn = snowflake.connector.connect(
    account='your_account',
    user='your_user',
    password='your_password',
    warehouse='COMPUTE_WH'
)

cursor = conn.cursor()

# 1. Set up marketing database
cursor.execute("CREATE DATABASE IF NOT EXISTS marketing_data")
cursor.execute("USE DATABASE marketing_data")
cursor.execute("CREATE SCHEMA IF NOT EXISTS analytics")
cursor.execute("CREATE SCHEMA IF NOT EXISTS audiences")

# 2. Query customer 360 for high-value segment
high_value_query = """
SELECT user_id, email, lifetime_revenue, revenue_90d
FROM marketing_data.analytics.customer_360
WHERE revenue_90d > 1000
ORDER BY revenue_90d DESC
LIMIT 10000
"""

high_value_df = pd.read_sql(high_value_query, conn)

# 3. Analyze campaign ROI
roi_query = """
SELECT
    platform,
    campaign_name,
    SUM(spend) as total_spend,
    SUM(attributed_revenue) as total_revenue,
    AVG(roas) as avg_roas
FROM marketing_data.analytics.campaign_roi
WHERE date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY platform, campaign_name
ORDER BY total_revenue DESC
"""

roi_df = pd.read_sql(roi_query, conn)
print("\nTop Campaigns by Revenue:")
print(roi_df.head())

cursor.close()
conn.close()
```

## References

- **Official Documentation**: https://docs.snowflake.com/
- **Python Connector**: https://docs.snowflake.com/en/user-guide/python-connector
- **Data Loading**: https://docs.snowflake.com/en/user-guide/data-load-overview
- **SQL Reference**: https://docs.snowflake.com/en/sql-reference
- **Snowflake Marketplace**: https://www.snowflake.com/data-marketplace/
- **Data Sharing**: https://docs.snowflake.com/en/user-guide/data-sharing-intro
- **Best Practices**: https://docs.snowflake.com/en/user-guide/best-practices
- **Security**: https://docs.snowflake.com/en/user-guide/security
- **Cost Optimization**: https://docs.snowflake.com/en/user-guide/cost-understanding
- **Integration Partners**: https://www.snowflake.com/technology-partners/

---
name: dbt-transforms
description: "Data transformations for marketing analytics. SQL-based ELT, marketing data models, attribution tables, customer 360, campaign analytics, incremental models, testing."
---

# dbt for Marketing Data Transformations

## Overview

dbt (data build tool) enables SQL-based data transformations for marketing analytics. This skill covers building marketing data models, creating attribution tables, customer 360 views, campaign performance marts, cohort analysis tables, and implementing data quality testing for marketing warehouses.

## When to Use This Skill

- Building marketing data warehouse with dimensional models
- Creating customer 360 views from multiple sources
- Implementing multi-touch attribution models
- Building cohort analysis tables
- Creating campaign performance marts
- Implementing incremental models for large datasets
- Adding data quality tests to marketing pipelines
- Documenting marketing data lineage

## Core Capabilities

### 1. Marketing Data Warehouse Setup

```sql
-- dbt_project.yml
name: 'marketing_analytics'
version: '1.0.0'
config-version: 2

profile: 'marketing_warehouse'

models:
  marketing_analytics:
    staging:
      +materialized: view
      +schema: staging
    intermediate:
      +materialized: view
      +schema: intermediate
    marts:
      +materialized: table
      +schema: marts
      marketing:
        +materialized: table
      customers:
        +materialized: table
      attribution:
        +materialized: table
```

```yaml
# profiles.yml
marketing_warehouse:
  target: prod
  outputs:
    prod:
      type: snowflake
      account: your-account
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASSWORD') }}"
      role: TRANSFORMER
      database: MARKETING_DW
      warehouse: TRANSFORM_WH
      schema: ANALYTICS
      threads: 4
```

### 2. Staging Models - Data Source Integration

```sql
-- models/staging/google_ads/stg_google_ads__campaigns.sql
{{
  config(
    materialized='view',
    tags=['staging', 'google_ads']
  )
}}

with source as (
    select * from {{ source('google_ads', 'campaigns_raw') }}
),

renamed as (
    select
        campaign_id,
        campaign_name,
        campaign_status,
        campaign_type,
        budget_amount,
        budget_currency,
        start_date,
        end_date,
        _loaded_at as loaded_at

    from source
    where campaign_status != 'REMOVED'
)

select * from renamed
```

```sql
-- models/staging/meta_ads/stg_meta_ads__insights.sql
{{
  config(
    materialized='view',
    tags=['staging', 'meta_ads']
  )
}}

with source as (
    select * from {{ source('meta_ads', 'insights_raw') }}
),

transformed as (
    select
        date_start as report_date,
        campaign_id,
        campaign_name,
        adset_id,
        adset_name,
        ad_id,
        ad_name,

        -- Metrics
        cast(impressions as integer) as impressions,
        cast(clicks as integer) as clicks,
        cast(spend as decimal(10,2)) as spend,
        cast(conversions as integer) as conversions,
        cast(revenue as decimal(10,2)) as revenue,

        -- Calculated metrics
        case
            when impressions > 0
            then (clicks::decimal / impressions) * 100
            else 0
        end as ctr,

        case
            when clicks > 0
            then spend / clicks
            else 0
        end as cpc,

        case
            when spend > 0
            then revenue / spend
            else 0
        end as roas,

        _loaded_at as loaded_at

    from source
)

select * from transformed
```

```sql
-- models/staging/hubspot/stg_hubspot__contacts.sql
{{
  config(
    materialized='view',
    tags=['staging', 'crm']
  )
}}

with source as (
    select * from {{ source('hubspot', 'contacts_raw') }}
),

contacts as (
    select
        id as contact_id,
        email,
        firstname,
        lastname,
        concat(firstname, ' ', lastname) as full_name,
        lifecyclestage as lifecycle_stage,
        lead_source,
        created_at as contact_created_at,
        updated_at as contact_updated_at,
        first_conversion_date,
        first_touch_channel,
        last_touch_channel

    from source
    where email is not null
)

select * from contacts
```

### 3. Intermediate Models - Business Logic

```sql
-- models/intermediate/int_campaign_performance.sql
{{
  config(
    materialized='view',
    tags=['intermediate', 'campaigns']
  )
}}

with google_ads as (
    select * from {{ ref('stg_google_ads__campaigns') }}
),

meta_ads as (
    select * from {{ ref('stg_meta_ads__insights') }}
),

unified_campaigns as (
    -- Google Ads
    select
        campaign_id,
        campaign_name,
        'Google Ads' as platform,
        report_date,
        impressions,
        clicks,
        spend,
        conversions,
        revenue,
        ctr,
        roas
    from google_ads

    union all

    -- Meta Ads
    select
        campaign_id,
        campaign_name,
        'Meta Ads' as platform,
        report_date,
        impressions,
        clicks,
        spend,
        conversions,
        revenue,
        ctr,
        roas
    from meta_ads
),

campaign_metrics as (
    select
        platform,
        campaign_id,
        campaign_name,
        report_date,

        -- Engagement metrics
        sum(impressions) as impressions,
        sum(clicks) as clicks,
        avg(ctr) as avg_ctr,

        -- Conversion metrics
        sum(conversions) as conversions,
        case
            when sum(clicks) > 0
            then (sum(conversions)::decimal / sum(clicks)) * 100
            else 0
        end as conversion_rate,

        -- Financial metrics
        sum(spend) as spend,
        sum(revenue) as revenue,
        sum(revenue) - sum(spend) as profit,
        case
            when sum(spend) > 0
            then sum(revenue) / sum(spend)
            else 0
        end as roas,
        case
            when sum(conversions) > 0
            then sum(spend) / sum(conversions)
            else 0
        end as cpa

    from unified_campaigns
    group by 1, 2, 3, 4
)

select * from campaign_metrics
```

```sql
-- models/intermediate/int_customer_journey.sql
{{
  config(
    materialized='view',
    tags=['intermediate', 'attribution']
  )
}}

with touchpoints as (
    select
        user_id,
        session_id,
        timestamp,
        channel,
        campaign_id,
        utm_source,
        utm_medium,
        utm_campaign,
        row_number() over (partition by user_id order by timestamp) as touchpoint_number,
        count(*) over (partition by user_id) as total_touchpoints

    from {{ ref('stg_analytics__sessions') }}
),

conversions as (
    select
        user_id,
        min(conversion_date) as first_conversion_date,
        sum(revenue) as total_revenue

    from {{ ref('stg_analytics__conversions') }}
    group by 1
),

journey as (
    select
        t.user_id,
        t.session_id,
        t.timestamp,
        t.channel,
        t.utm_source,
        t.utm_medium,
        t.utm_campaign,
        t.touchpoint_number,
        t.total_touchpoints,

        -- Mark first and last touch
        case when t.touchpoint_number = 1 then true else false end as is_first_touch,
        case when t.touchpoint_number = t.total_touchpoints then true else false end as is_last_touch,

        -- Join conversion data
        c.first_conversion_date,
        c.total_revenue,
        case when c.user_id is not null then true else false end as converted

    from touchpoints t
    left join conversions c on t.user_id = c.user_id
)

select * from journey
```

### 4. Mart Models - Analytics Tables

```sql
-- models/marts/marketing/fct_campaign_performance.sql
{{
  config(
    materialized='table',
    tags=['mart', 'campaigns']
  )
}}

with campaign_performance as (
    select * from {{ ref('int_campaign_performance') }}
),

final as (
    select
        {{ dbt_utils.generate_surrogate_key(['platform', 'campaign_id', 'report_date']) }} as performance_id,

        -- Dimensions
        platform,
        campaign_id,
        campaign_name,
        report_date,
        date_trunc('week', report_date) as report_week,
        date_trunc('month', report_date) as report_month,

        -- Metrics
        impressions,
        clicks,
        conversions,
        spend,
        revenue,
        profit,

        -- Rates and ratios
        avg_ctr as ctr,
        conversion_rate,
        roas,
        cpa,

        -- Performance indicators
        case
            when roas >= 3.0 then 'Excellent'
            when roas >= 2.0 then 'Good'
            when roas >= 1.0 then 'Break Even'
            else 'Poor'
        end as roas_category,

        case
            when conversion_rate >= 5.0 then 'High'
            when conversion_rate >= 2.0 then 'Medium'
            else 'Low'
        end as conversion_category,

        current_timestamp() as dbt_updated_at

    from campaign_performance
)

select * from final
```

```sql
-- models/marts/customers/dim_customers.sql
{{
  config(
    materialized='table',
    tags=['mart', 'customers']
  )
}}

with contacts as (
    select * from {{ ref('stg_hubspot__contacts') }}
),

orders as (
    select * from {{ ref('stg_orders__transactions') }}
),

customer_orders as (
    select
        contact_id,
        min(order_date) as first_order_date,
        max(order_date) as last_order_date,
        count(distinct order_id) as total_orders,
        sum(order_amount) as lifetime_value,
        avg(order_amount) as avg_order_value,
        datediff(day, min(order_date), max(order_date)) as customer_tenure_days

    from orders
    group by 1
),

customer_360 as (
    select
        c.contact_id,
        c.email,
        c.full_name,
        c.lifecycle_stage,
        c.lead_source,
        c.contact_created_at,
        c.first_conversion_date,
        c.first_touch_channel,
        c.last_touch_channel,

        -- Order metrics
        coalesce(o.total_orders, 0) as total_orders,
        coalesce(o.lifetime_value, 0) as lifetime_value,
        coalesce(o.avg_order_value, 0) as avg_order_value,
        o.first_order_date,
        o.last_order_date,
        o.customer_tenure_days,

        -- Recency
        case
            when o.last_order_date is not null
            then datediff(day, o.last_order_date, current_date())
            else null
        end as days_since_last_order,

        -- Customer segmentation (RFM)
        case
            when o.total_orders >= 5 and datediff(day, o.last_order_date, current_date()) <= 30 then 'Champion'
            when o.total_orders >= 3 and datediff(day, o.last_order_date, current_date()) <= 60 then 'Loyal'
            when o.total_orders = 1 and datediff(day, o.first_order_date, current_date()) <= 30 then 'New'
            when datediff(day, o.last_order_date, current_date()) > 180 then 'At Risk'
            when datediff(day, o.last_order_date, current_date()) > 365 then 'Lost'
            else 'Potential'
        end as customer_segment,

        current_timestamp() as dbt_updated_at

    from contacts c
    left join customer_orders o on c.contact_id = o.contact_id
)

select * from customer_360
```

```sql
-- models/marts/attribution/fct_attribution.sql
{{
  config(
    materialized='table',
    tags=['mart', 'attribution']
  )
}}

with customer_journey as (
    select * from {{ ref('int_customer_journey') }}
),

-- First Touch Attribution
first_touch as (
    select
        'First Touch' as attribution_model,
        channel,
        utm_source,
        utm_campaign,
        count(distinct user_id) as attributed_conversions,
        sum(total_revenue) as attributed_revenue

    from customer_journey
    where is_first_touch and converted
    group by 1, 2, 3, 4
),

-- Last Touch Attribution
last_touch as (
    select
        'Last Touch' as attribution_model,
        channel,
        utm_source,
        utm_campaign,
        count(distinct user_id) as attributed_conversions,
        sum(total_revenue) as attributed_revenue

    from customer_journey
    where is_last_touch and converted
    group by 1, 2, 3, 4
),

-- Linear Attribution
linear as (
    select
        'Linear' as attribution_model,
        channel,
        utm_source,
        utm_campaign,
        count(distinct user_id) as attributed_conversions,
        sum(total_revenue / total_touchpoints) as attributed_revenue

    from customer_journey
    where converted
    group by 1, 2, 3, 4
),

combined as (
    select * from first_touch
    union all
    select * from last_touch
    union all
    select * from linear
)

select
    {{ dbt_utils.generate_surrogate_key(['attribution_model', 'channel', 'utm_source', 'utm_campaign']) }} as attribution_id,
    attribution_model,
    channel,
    utm_source,
    utm_campaign,
    attributed_conversions,
    attributed_revenue,
    case
        when attributed_conversions > 0
        then attributed_revenue / attributed_conversions
        else 0
    end as revenue_per_conversion,
    current_timestamp() as dbt_updated_at

from combined
```

### 5. Incremental Models for Large Datasets

```sql
-- models/marts/marketing/fct_daily_metrics.sql
{{
  config(
    materialized='incremental',
    unique_key='metric_id',
    tags=['mart', 'incremental']
  )
}}

with daily_data as (
    select
        report_date,
        platform,
        campaign_id,
        sum(impressions) as impressions,
        sum(clicks) as clicks,
        sum(spend) as spend,
        sum(conversions) as conversions,
        sum(revenue) as revenue

    from {{ ref('int_campaign_performance') }}

    {% if is_incremental() %}
        -- Only process new/updated data
        where report_date > (select max(report_date) from {{ this }})
    {% endif %}

    group by 1, 2, 3
)

select
    {{ dbt_utils.generate_surrogate_key(['report_date', 'platform', 'campaign_id']) }} as metric_id,
    report_date,
    platform,
    campaign_id,
    impressions,
    clicks,
    spend,
    conversions,
    revenue,
    current_timestamp() as dbt_updated_at

from daily_data
```

### 6. Data Quality Tests

```yaml
# models/marts/marketing/schema.yml
version: 2

models:
  - name: fct_campaign_performance
    description: "Daily campaign performance metrics across all platforms"
    columns:
      - name: performance_id
        description: "Unique identifier for each performance record"
        tests:
          - unique
          - not_null

      - name: campaign_id
        description: "Campaign identifier"
        tests:
          - not_null

      - name: report_date
        description: "Date of the report"
        tests:
          - not_null

      - name: spend
        description: "Total spend for the day"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              inclusive: true

      - name: revenue
        description: "Total revenue generated"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              inclusive: true

      - name: roas
        description: "Return on ad spend"
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 100
              inclusive: true

  - name: dim_customers
    description: "Customer 360 dimension table"
    columns:
      - name: contact_id
        description: "Unique customer identifier"
        tests:
          - unique
          - not_null

      - name: email
        description: "Customer email address"
        tests:
          - not_null
          - dbt_utils.not_empty_string

      - name: customer_segment
        description: "Customer segmentation based on RFM"
        tests:
          - accepted_values:
              values: ['Champion', 'Loyal', 'New', 'At Risk', 'Lost', 'Potential']
```

### 7. Macros for Marketing Calculations

```sql
-- macros/calculate_roas.sql
{% macro calculate_roas(revenue_column, spend_column) %}
    case
        when {{ spend_column }} > 0
        then {{ revenue_column }}::decimal / {{ spend_column }}
        else 0
    end
{% endmacro %}
```

```sql
-- macros/marketing_metrics.sql
{% macro marketing_metrics(
    impressions_column,
    clicks_column,
    conversions_column,
    spend_column,
    revenue_column
) %}
    -- CTR
    case
        when {{ impressions_column }} > 0
        then ({{ clicks_column }}::decimal / {{ impressions_column }}) * 100
        else 0
    end as ctr,

    -- Conversion Rate
    case
        when {{ clicks_column }} > 0
        then ({{ conversions_column }}::decimal / {{ clicks_column }}) * 100
        else 0
    end as conversion_rate,

    -- CPC
    case
        when {{ clicks_column }} > 0
        then {{ spend_column }}::decimal / {{ clicks_column }}
        else 0
    end as cpc,

    -- CPA
    case
        when {{ conversions_column }} > 0
        then {{ spend_column }}::decimal / {{ conversions_column }}
        else 0
    end as cpa,

    -- ROAS
    {{ calculate_roas(revenue_column, spend_column) }} as roas
{% endmacro %}
```

Usage in model:
```sql
select
    campaign_id,
    sum(impressions) as impressions,
    sum(clicks) as clicks,
    sum(conversions) as conversions,
    sum(spend) as spend,
    sum(revenue) as revenue,

    {{ marketing_metrics('sum(impressions)', 'sum(clicks)', 'sum(conversions)', 'sum(spend)', 'sum(revenue)') }}

from campaign_data
group by 1
```

## Installation

```bash
# Install dbt for your data warehouse
uv pip install dbt-core dbt-snowflake  # or dbt-bigquery, dbt-redshift, etc.

# Initialize new dbt project
dbt init marketing_analytics

# Install dbt packages (add to packages.yml first)
dbt deps
```

```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: calogica/dbt_expectations
    version: 0.10.0
```

## Quick Start

```bash
# Run all models
dbt run

# Run specific model
dbt run --select fct_campaign_performance

# Run tests
dbt test

# Generate documentation
dbt docs generate
dbt docs serve

# Run full refresh of incremental model
dbt run --select fct_daily_metrics --full-refresh
```

## Best Practices

1. **Staging layer** - Always create staging models for raw data
2. **Incremental models** - Use for large fact tables to improve performance
3. **Testing** - Add tests for primary keys and critical metrics
4. **Documentation** - Document all models and columns in schema.yml
5. **Macros** - Create reusable macros for common calculations
6. **Naming conventions** - Use prefixes: stg_, int_, fct_, dim_
7. **Version control** - Use Git for dbt project management

## Common Marketing Models

- **fct_campaign_performance** - Daily campaign metrics
- **dim_customers** - Customer 360 view
- **fct_attribution** - Multi-touch attribution
- **fct_cohorts** - Cohort analysis tables
- **fct_customer_lifetime_value** - CLV calculations
- **dim_utm_parameters** - UTM parameter taxonomy
- **fct_email_engagement** - Email marketing metrics

## References

- [dbt Documentation](https://docs.getdbt.com/)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)
- [dbt Utils Package](https://github.com/dbt-labs/dbt-utils)
- [dbt Discourse](https://discourse.getdbt.com/)

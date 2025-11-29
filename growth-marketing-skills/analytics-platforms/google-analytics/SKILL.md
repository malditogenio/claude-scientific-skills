---
name: google-analytics
description: "Google Analytics 4 integration. Traffic analysis, conversion tracking, audience insights, attribution reports, BigQuery export, API access."
---

# Google Analytics 4 Integration

## Overview

Google Analytics 4 (GA4) is the primary web and app analytics platform. This skill covers accessing GA4 data via the API, common analysis patterns, BigQuery integration, and building custom reports.

## When to Use This Skill

- Analyzing website and app traffic
- Understanding user behavior and journeys
- Measuring conversion funnels
- Attribution analysis
- Audience building and analysis
- Exporting data to BigQuery for advanced analysis

## Core Capabilities

### 1. GA4 Data API Setup

```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, Metric, RunReportRequest,
    FilterExpression, Filter, OrderBy
)
from google.oauth2 import service_account
import pandas as pd

# Authentication
credentials = service_account.Credentials.from_service_account_file(
    'service-account.json',
    scopes=['https://www.googleapis.com/auth/analytics.readonly']
)

client = BetaAnalyticsDataClient(credentials=credentials)
property_id = 'YOUR_GA4_PROPERTY_ID'

# Basic report request
request = RunReportRequest(
    property=f"properties/{property_id}",
    date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
    dimensions=[
        Dimension(name="date"),
        Dimension(name="sessionDefaultChannelGroup")
    ],
    metrics=[
        Metric(name="sessions"),
        Metric(name="totalUsers"),
        Metric(name="conversions"),
        Metric(name="totalRevenue")
    ]
)

response = client.run_report(request)

# Convert to DataFrame
rows = []
for row in response.rows:
    rows.append({
        'date': row.dimension_values[0].value,
        'channel': row.dimension_values[1].value,
        'sessions': int(row.metric_values[0].value),
        'users': int(row.metric_values[1].value),
        'conversions': int(row.metric_values[2].value),
        'revenue': float(row.metric_values[3].value)
    })

df = pd.DataFrame(rows)
print(df.head())
```

### 2. Traffic Source Analysis

```python
# Traffic by source/medium
request = RunReportRequest(
    property=f"properties/{property_id}",
    date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
    dimensions=[
        Dimension(name="sessionSource"),
        Dimension(name="sessionMedium"),
        Dimension(name="sessionCampaignName")
    ],
    metrics=[
        Metric(name="sessions"),
        Metric(name="engagedSessions"),
        Metric(name="conversions"),
        Metric(name="totalRevenue")
    ],
    order_bys=[
        OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)
    ],
    limit=50
)

response = client.run_report(request)

# Process results
traffic_data = []
for row in response.rows:
    traffic_data.append({
        'source': row.dimension_values[0].value,
        'medium': row.dimension_values[1].value,
        'campaign': row.dimension_values[2].value,
        'sessions': int(row.metric_values[0].value),
        'engaged_sessions': int(row.metric_values[1].value),
        'conversions': int(row.metric_values[2].value),
        'revenue': float(row.metric_values[3].value)
    })

df = pd.DataFrame(traffic_data)
df['engagement_rate'] = df['engaged_sessions'] / df['sessions'] * 100
df['conversion_rate'] = df['conversions'] / df['sessions'] * 100
df['roas'] = df['revenue'] / df['sessions']  # Revenue per session

print(df.sort_values('revenue', ascending=False).head(20))
```

### 3. Conversion Funnel Analysis

```python
# E-commerce funnel events
request = RunReportRequest(
    property=f"properties/{property_id}",
    date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
    dimensions=[
        Dimension(name="eventName")
    ],
    metrics=[
        Metric(name="eventCount"),
        Metric(name="totalUsers")
    ],
    dimension_filter=FilterExpression(
        filter=Filter(
            field_name="eventName",
            in_list_filter=Filter.InListFilter(
                values=["page_view", "view_item", "add_to_cart",
                       "begin_checkout", "purchase"]
            )
        )
    )
)

response = client.run_report(request)

# Build funnel
funnel_order = ["page_view", "view_item", "add_to_cart", "begin_checkout", "purchase"]
funnel_data = {}

for row in response.rows:
    event = row.dimension_values[0].value
    users = int(row.metric_values[1].value)
    funnel_data[event] = users

# Calculate funnel metrics
print("\nConversion Funnel:")
prev_users = None
for event in funnel_order:
    users = funnel_data.get(event, 0)
    if prev_users:
        step_rate = users / prev_users * 100
        print(f"  {event}: {users:,} users ({step_rate:.1f}% from previous)")
    else:
        print(f"  {event}: {users:,} users")
    prev_users = users

overall_rate = funnel_data.get("purchase", 0) / funnel_data.get("page_view", 1) * 100
print(f"\nOverall Conversion Rate: {overall_rate:.2f}%")
```

### 4. User Segments Analysis

```python
# Analyze behavior by user segment
segments = [
    ("New Users", Filter(field_name="newVsReturning", string_filter=Filter.StringFilter(value="new"))),
    ("Returning Users", Filter(field_name="newVsReturning", string_filter=Filter.StringFilter(value="returning")))
]

segment_metrics = []
for segment_name, segment_filter in segments:
    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
        metrics=[
            Metric(name="totalUsers"),
            Metric(name="sessions"),
            Metric(name="averageSessionDuration"),
            Metric(name="screenPageViewsPerSession"),
            Metric(name="conversions"),
            Metric(name="totalRevenue")
        ],
        dimension_filter=FilterExpression(filter=segment_filter)
    )

    response = client.run_report(request)

    if response.rows:
        row = response.rows[0]
        segment_metrics.append({
            'segment': segment_name,
            'users': int(row.metric_values[0].value),
            'sessions': int(row.metric_values[1].value),
            'avg_session_duration': float(row.metric_values[2].value),
            'pages_per_session': float(row.metric_values[3].value),
            'conversions': int(row.metric_values[4].value),
            'revenue': float(row.metric_values[5].value)
        })

df = pd.DataFrame(segment_metrics)
df['conversion_rate'] = df['conversions'] / df['users'] * 100
df['revenue_per_user'] = df['revenue'] / df['users']

print(df)
```

### 5. BigQuery Export Analysis

```python
from google.cloud import bigquery
import pandas as pd

# Initialize BigQuery client
client = bigquery.Client()

# Query GA4 export data
query = """
SELECT
    event_date,
    traffic_source.source AS source,
    traffic_source.medium AS medium,
    traffic_source.name AS campaign,
    COUNT(DISTINCT user_pseudo_id) AS users,
    COUNT(*) AS events,
    SUM(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS purchases,
    SUM(ecommerce.purchase_revenue) AS revenue
FROM
    `your-project.analytics_123456789.events_*`
WHERE
    _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
    AND FORMAT_DATE('%Y%m%d', CURRENT_DATE())
GROUP BY
    1, 2, 3, 4
ORDER BY
    revenue DESC
LIMIT 100
"""

df = client.query(query).to_dataframe()
print(df.head(20))

# User journey analysis from BigQuery
journey_query = """
WITH user_journeys AS (
    SELECT
        user_pseudo_id,
        ARRAY_AGG(
            STRUCT(event_timestamp, event_name)
            ORDER BY event_timestamp
        ) AS events,
        MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS converted
    FROM
        `your-project.analytics_123456789.events_*`
    WHERE
        _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', CURRENT_DATE())
    GROUP BY
        user_pseudo_id
)
SELECT
    converted,
    COUNT(*) AS users,
    AVG(ARRAY_LENGTH(events)) AS avg_events
FROM
    user_journeys
GROUP BY
    converted
"""

journey_df = client.query(journey_query).to_dataframe()
print(journey_df)
```

### 6. Custom Audience Export

```python
# Get audience data for ad platform sync
request = RunReportRequest(
    property=f"properties/{property_id}",
    date_ranges=[DateRange(start_date="90daysAgo", end_date="today")],
    dimensions=[
        Dimension(name="deviceCategory"),
        Dimension(name="country"),
        Dimension(name="city")
    ],
    metrics=[
        Metric(name="totalUsers"),
        Metric(name="purchasers"),
        Metric(name="totalRevenue")
    ],
    dimension_filter=FilterExpression(
        filter=Filter(
            field_name="purchasers",
            numeric_filter=Filter.NumericFilter(
                operation=Filter.NumericFilter.Operation.GREATER_THAN,
                value={"int64_value": 0}
            )
        )
    ),
    order_bys=[
        OrderBy(metric=OrderBy.MetricOrderBy(metric_name="totalRevenue"), desc=True)
    ]
)

response = client.run_report(request)

# Process for audience building
audience_data = []
for row in response.rows:
    audience_data.append({
        'device': row.dimension_values[0].value,
        'country': row.dimension_values[1].value,
        'city': row.dimension_values[2].value,
        'users': int(row.metric_values[0].value),
        'purchasers': int(row.metric_values[1].value),
        'revenue': float(row.metric_values[2].value)
    })

df = pd.DataFrame(audience_data)
df['purchase_rate'] = df['purchasers'] / df['users'] * 100

# High-value segments for lookalike audiences
high_value = df[df['revenue'] > df['revenue'].quantile(0.75)]
print("High-Value Audience Segments:")
print(high_value)
```

## Installation

```bash
uv pip install google-analytics-data google-cloud-bigquery pandas
```

## Authentication

1. Create a service account in Google Cloud Console
2. Enable the Google Analytics Data API
3. Add the service account email to your GA4 property with Viewer access
4. Download the service account JSON key

## Quick Start

```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric

client = BetaAnalyticsDataClient()

request = RunReportRequest(
    property="properties/YOUR_PROPERTY_ID",
    date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
    metrics=[Metric(name="activeUsers")]
)

response = client.run_report(request)
print(f"Active Users (7d): {response.rows[0].metric_values[0].value}")
```

## Key Metrics Reference

- **activeUsers**: Users who engaged with your site/app
- **sessions**: Total number of sessions
- **engagedSessions**: Sessions lasting >10s or with conversions/2+ page views
- **conversions**: Total conversion events
- **totalRevenue**: Total revenue from purchases
- **averageSessionDuration**: Average session length in seconds
- **screenPageViewsPerSession**: Average pages per session

## References

- [GA4 Data API Documentation](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [GA4 Dimensions & Metrics Explorer](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema)
- [BigQuery Export Schema](https://support.google.com/analytics/answer/7029846)

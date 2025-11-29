---
name: posthog
description: "Open source product analytics. Self-hosted or cloud, feature flags, A/B testing, session recording, SQL access, privacy-focused analytics."
---

# PostHog Product Analytics

## Overview

PostHog is an open-source product analytics platform that offers complete control over your data with self-hosting options. It combines analytics, feature flags, session recording, and experimentation in one platform. This skill covers API access, event tracking, funnel analysis, and leveraging PostHog's SQL interface.

## When to Use This Skill

- Open-source, privacy-focused product analytics
- Self-hosted analytics with full data control
- Feature flag management and experimentation
- Session recording and user replay
- Real-time event tracking and analysis
- Custom SQL queries on analytics data
- Product-led growth analytics

## Core Capabilities

### 1. PostHog API Setup

```python
import requests
import pandas as pd
from datetime import datetime, timedelta
import json

class PostHogAnalytics:
    def __init__(self, api_key, host='https://app.posthog.com'):
        self.api_key = api_key
        self.host = host
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, endpoint, method='GET', params=None, data=None):
        """Make authenticated request to PostHog API"""
        url = f"{self.host}/api/{endpoint}"

        if method == 'GET':
            response = requests.get(url, headers=self.headers, params=params)
        else:
            response = requests.post(url, headers=self.headers, json=data)

        response.raise_for_status()
        return response.json()

    def query_events(self, event_name=None, date_from=None, date_to=None,
                     properties=None):
        """Query events with filters"""
        params = {}
        if event_name:
            params['event'] = event_name
        if date_from:
            params['date_from'] = date_from
        if date_to:
            params['date_to'] = date_to
        if properties:
            params['properties'] = json.dumps(properties)

        return self._make_request('event', params=params)

    def get_insights(self, insight_id):
        """Get saved insight data"""
        return self._make_request(f'insight/{insight_id}')

    def create_cohort(self, name, filters):
        """Create user cohort"""
        data = {
            'name': name,
            'filters': filters
        }
        return self._make_request('cohort', method='POST', data=data)

# Initialize PostHog client
posthog = PostHogAnalytics(
    api_key='YOUR_API_KEY',
    host='https://app.posthog.com'  # or your self-hosted instance
)

# Query recent events
events = posthog.query_events(
    date_from=(datetime.now() - timedelta(days=7)).isoformat(),
    date_to=datetime.now().isoformat()
)

print(f"Events: {events}")
```

### 2. Event Tracking and Analysis

```python
def track_event_to_posthog(api_key, project_id, distinct_id, event_name,
                          properties=None):
    """
    Send events to PostHog
    """
    url = "https://app.posthog.com/capture/"

    event_data = {
        'api_key': api_key,
        'event': event_name,
        'properties': {
            'distinct_id': distinct_id,
            **(properties or {})
        },
        'timestamp': datetime.now().isoformat()
    }

    response = requests.post(url, json=event_data)
    response.raise_for_status()

    return response.status_code

# Track custom events
track_event_to_posthog(
    api_key='YOUR_PROJECT_API_KEY',
    project_id='your_project',
    distinct_id='user_12345',
    event_name='feature_used',
    properties={
        'feature_name': 'advanced_search',
        'search_query': 'analytics tools',
        'results_count': 42,
        'plan_type': 'enterprise'
    }
)

# Track purchase events
track_event_to_posthog(
    api_key='YOUR_PROJECT_API_KEY',
    project_id='your_project',
    distinct_id='user_67890',
    event_name='purchase_completed',
    properties={
        'product_id': 'PROD_123',
        'amount': 99.99,
        'currency': 'USD',
        'payment_method': 'stripe'
    }
)
```

### 3. Funnel Analysis with PostHog

```python
def analyze_funnel(posthog, funnel_steps, date_from, date_to):
    """
    Create and analyze conversion funnel
    """
    # Create funnel using Insights API
    funnel_data = {
        'insight': 'FUNNELS',
        'events': [
            {'id': step['event'], 'name': step['event'], 'type': 'events'}
            for step in funnel_steps
        ],
        'date_from': date_from,
        'date_to': date_to,
        'funnel_window_days': 14
    }

    result = posthog._make_request('insight', method='POST', data=funnel_data)

    # Process funnel results
    if 'result' in result:
        funnel_df = pd.DataFrame([
            {
                'step': i + 1,
                'event': step['name'],
                'count': step['count'],
                'conversion_rate': step.get('conversion_rate', 1.0) * 100
            }
            for i, step in enumerate(result['result'])
        ])

        # Calculate drop-offs
        funnel_df['drop_off'] = 100 - funnel_df['conversion_rate']

        return funnel_df

    return None

# Define signup funnel
funnel_steps = [
    {'event': 'visited_pricing_page'},
    {'event': 'clicked_signup_button'},
    {'event': 'form_submitted'},
    {'event': 'email_verified'},
    {'event': 'first_session'}
]

funnel = analyze_funnel(
    posthog,
    funnel_steps,
    date_from='-30d',
    date_to='now'
)

if funnel is not None:
    print("\nSignup Funnel Analysis:")
    print(funnel)

    # Identify biggest drop-off
    max_drop = funnel.loc[funnel['drop_off'].idxmax()]
    print(f"\nBiggest drop-off at step {max_drop['step']}: {max_drop['event']}")
    print(f"Drop-off rate: {max_drop['drop_off']:.1f}%")
```

### 4. SQL Query Interface

```python
def query_posthog_sql(posthog, sql_query):
    """
    Execute SQL query on PostHog data
    Available in PostHog Cloud and self-hosted
    """
    data = {
        'query': {
            'kind': 'HogQLQuery',
            'query': sql_query
        }
    }

    result = posthog._make_request('query', method='POST', data=data)
    return result

# Daily active users by feature
dau_query = """
SELECT
    toDate(timestamp) as date,
    properties.$feature_name as feature,
    count(DISTINCT distinct_id) as dau
FROM events
WHERE
    event = 'feature_used'
    AND timestamp >= now() - INTERVAL 30 DAY
GROUP BY date, feature
ORDER BY date DESC, dau DESC
"""

dau_results = query_posthog_sql(posthog, dau_query)

# Convert to DataFrame
if 'results' in dau_results:
    df = pd.DataFrame(dau_results['results'], columns=['date', 'feature', 'dau'])
    print("\nDaily Active Users by Feature:")
    print(df.head(20))

# Revenue analysis query
revenue_query = """
SELECT
    toDate(timestamp) as date,
    properties.plan_type as plan,
    count() as purchases,
    sum(toFloat(properties.amount)) as revenue,
    avg(toFloat(properties.amount)) as avg_order_value
FROM events
WHERE
    event = 'purchase_completed'
    AND timestamp >= now() - INTERVAL 90 DAY
GROUP BY date, plan
ORDER BY date DESC, revenue DESC
"""

revenue_results = query_posthog_sql(posthog, revenue_query)

if 'results' in revenue_results:
    revenue_df = pd.DataFrame(
        revenue_results['results'],
        columns=['date', 'plan', 'purchases', 'revenue', 'aov']
    )
    print("\nRevenue Analysis:")
    print(revenue_df.groupby('plan').agg({
        'purchases': 'sum',
        'revenue': 'sum',
        'aov': 'mean'
    }))
```

### 5. Cohort Analysis and Retention

```python
def create_retention_analysis(posthog, start_event, return_event,
                             date_from, date_to):
    """
    Analyze user retention cohorts
    """
    retention_data = {
        'insight': 'RETENTION',
        'target_entity': {
            'id': start_event,
            'type': 'events'
        },
        'returning_entity': {
            'id': return_event,
            'type': 'events'
        },
        'date_from': date_from,
        'date_to': date_to,
        'retention_type': 'retention_first_time',
        'period': 'Week'
    }

    result = posthog._make_request('insight', method='POST', data=retention_data)

    if 'result' in result:
        # Process retention data
        cohorts = []
        for cohort in result['result']:
            cohort_row = {
                'date': cohort['date'],
                'cohort_size': cohort['values'][0]['count'] if cohort['values'] else 0
            }

            # Add retention by period
            for i, period in enumerate(cohort['values']):
                cohort_row[f'period_{i}'] = (
                    period['count'] / cohort_row['cohort_size'] * 100
                    if cohort_row['cohort_size'] > 0 else 0
                )

            cohorts.append(cohort_row)

        cohort_df = pd.DataFrame(cohorts)

        print("\nRetention Analysis:")
        print(cohort_df)

        # Average retention
        period_cols = [c for c in cohort_df.columns if c.startswith('period_')]
        avg_retention = cohort_df[period_cols].mean()
        print("\nAverage Retention by Period:")
        print(avg_retention)

        return cohort_df

    return None

# Analyze weekly retention
retention = create_retention_analysis(
    posthog,
    start_event='user_signed_up',
    return_event='session_start',
    date_from='-90d',
    date_to='now'
)
```

### 6. Feature Flags and Experimentation

```python
def get_feature_flag_status(posthog, flag_key, distinct_id, properties=None):
    """
    Check feature flag status for a user
    """
    params = {
        'distinct_id': distinct_id,
        'groups': json.dumps(properties or {})
    }

    result = posthog._make_request(
        f'feature_flag/{flag_key}/my_flags',
        params=params
    )

    return result

def analyze_experiment_results(posthog, experiment_key):
    """
    Analyze A/B test experiment results
    """
    # Query events split by feature flag
    query = f"""
    SELECT
        properties.$feature/{experiment_key} as variant,
        count(DISTINCT distinct_id) as users,
        countIf(event = 'conversion_event') as conversions,
        countIf(event = 'conversion_event') / count(DISTINCT distinct_id) as conversion_rate
    FROM events
    WHERE
        timestamp >= now() - INTERVAL 30 DAY
        AND properties.$feature/{experiment_key} IS NOT NULL
    GROUP BY variant
    """

    results = query_posthog_sql(posthog, query)

    if 'results' in results:
        exp_df = pd.DataFrame(
            results['results'],
            columns=['variant', 'users', 'conversions', 'conversion_rate']
        )

        exp_df['conversion_rate'] = exp_df['conversion_rate'] * 100

        print(f"\nExperiment Results for {experiment_key}:")
        print(exp_df)

        # Calculate lift
        if len(exp_df) >= 2:
            control = exp_df[exp_df['variant'] == 'control']
            test = exp_df[exp_df['variant'] == 'test']

            if not control.empty and not test.empty:
                lift = (
                    (test['conversion_rate'].values[0] -
                     control['conversion_rate'].values[0]) /
                    control['conversion_rate'].values[0] * 100
                )
                print(f"\nLift: {lift:.2f}%")

        return exp_df

    return None

# Check if feature is enabled for user
flag_status = get_feature_flag_status(
    posthog,
    flag_key='new_checkout_flow',
    distinct_id='user_12345',
    properties={'plan': 'premium'}
)

# Analyze experiment
experiment_results = analyze_experiment_results(
    posthog,
    experiment_key='new_onboarding'
)
```

### 7. Session Recording Analysis

```python
def get_session_recordings(posthog, filters=None, date_from=None, date_to=None):
    """
    Get session recordings with filters
    """
    params = {
        'date_from': date_from or '-7d',
        'date_to': date_to or 'now'
    }

    if filters:
        params['filters'] = json.dumps(filters)

    recordings = posthog._make_request('session_recording', params=params)

    return recordings

def analyze_session_patterns(posthog, event_filter):
    """
    Find sessions containing specific events
    """
    # Query sessions with error events
    query = f"""
    SELECT
        session_id,
        distinct_id,
        min(timestamp) as session_start,
        max(timestamp) as session_end,
        count() as event_count,
        countIf(event = '{event_filter}') as target_events
    FROM events
    WHERE
        timestamp >= now() - INTERVAL 7 DAY
        AND session_id IS NOT NULL
    GROUP BY session_id, distinct_id
    HAVING target_events > 0
    ORDER BY target_events DESC
    LIMIT 100
    """

    results = query_posthog_sql(posthog, query)

    if 'results' in results:
        sessions_df = pd.DataFrame(
            results['results'],
            columns=['session_id', 'user_id', 'start', 'end', 'events', 'target_events']
        )

        print(f"\nSessions with '{event_filter}' events:")
        print(sessions_df.head(20))

        return sessions_df

    return None

# Get recordings of users who encountered errors
error_sessions = analyze_session_patterns(posthog, 'error_occurred')

# Get recordings of high-value conversions
conversion_recordings = get_session_recordings(
    posthog,
    filters={
        'events': [{'id': 'purchase_completed', 'type': 'events'}],
        'properties': [
            {'key': 'amount', 'value': 100, 'operator': 'gt', 'type': 'event'}
        ]
    },
    date_from='-30d'
)
```

### 8. Person and Group Analytics

```python
def analyze_user_properties(posthog):
    """
    Analyze user properties and segments
    """
    query = """
    SELECT
        properties.$initial_utm_source as source,
        properties.plan_type as plan,
        count(DISTINCT distinct_id) as users,
        avg(toFloat(properties.sessions_count)) as avg_sessions,
        countIf(event = 'purchase_completed') / count(DISTINCT distinct_id) as purchase_rate
    FROM persons
    LEFT JOIN events USING (distinct_id)
    WHERE
        timestamp >= now() - INTERVAL 90 DAY
    GROUP BY source, plan
    ORDER BY users DESC
    """

    results = query_posthog_sql(posthog, query)

    if 'results' in results:
        user_df = pd.DataFrame(
            results['results'],
            columns=['source', 'plan', 'users', 'avg_sessions', 'purchase_rate']
        )

        user_df['purchase_rate'] = user_df['purchase_rate'] * 100

        print("\nUser Segment Analysis:")
        print(user_df)

        return user_df

    return None

# Analyze company/account analytics (B2B)
def analyze_group_properties(posthog, group_type='company'):
    """
    Analyze group-level analytics for B2B
    """
    query = f"""
    SELECT
        groups.{group_type}_id as group_id,
        groups.properties.industry as industry,
        groups.properties.size as company_size,
        count(DISTINCT events.distinct_id) as active_users,
        count() as total_events
    FROM events
    JOIN groups ON events.properties.$group_0 = groups.{group_type}_id
    WHERE
        timestamp >= now() - INTERVAL 30 DAY
    GROUP BY group_id, industry, company_size
    ORDER BY total_events DESC
    """

    results = query_posthog_sql(posthog, query)

    if 'results' in results:
        group_df = pd.DataFrame(
            results['results'],
            columns=['group_id', 'industry', 'size', 'active_users', 'events']
        )

        print("\nCompany-Level Analytics:")
        print(group_df.head(20))

        return group_df

    return None

user_analysis = analyze_user_properties(posthog)
group_analysis = analyze_group_properties(posthog)
```

## Installation

```bash
# PostHog Python library
uv pip install posthog pandas requests

# For self-hosted deployment
docker run -d --name posthog \
  -p 8000:8000 \
  -v postgres:/var/lib/postgresql/data \
  posthog/posthog:latest
```

## Authentication

1. Sign up at https://app.posthog.com or deploy self-hosted
2. Navigate to Project Settings
3. Copy your Project API Key
4. For personal API access, go to Personal API Keys and create one

## Quick Start

```python
from posthog import Posthog

# Initialize client
posthog = Posthog(
    project_api_key='YOUR_PROJECT_API_KEY',
    host='https://app.posthog.com'
)

# Track an event
posthog.capture(
    distinct_id='user_12345',
    event='button_clicked',
    properties={
        'button_name': 'signup_cta',
        'page': '/pricing'
    }
)

# Identify user
posthog.identify(
    distinct_id='user_12345',
    properties={
        'email': 'user@example.com',
        'plan': 'enterprise',
        'company': 'Acme Corp'
    }
)

# Feature flags
is_enabled = posthog.feature_enabled(
    'new-feature',
    'user_12345'
)

print(f"Feature enabled: {is_enabled}")
```

## Key Features

- **Open Source**: Self-host for complete data control
- **Privacy First**: GDPR compliant, data stays on your infrastructure
- **All-in-One**: Analytics, feature flags, A/B testing, session replay
- **SQL Access**: Query data directly with HogQL (PostHog's SQL dialect)
- **Real-time**: Instant insights and real-time dashboards
- **Unlimited Events**: No sampling, track everything

## References

- [PostHog Documentation](https://posthog.com/docs)
- [PostHog API Reference](https://posthog.com/docs/api)
- [HogQL Query Guide](https://posthog.com/docs/hogql)
- [PostHog Python Library](https://posthog.com/docs/libraries/python)
- [Feature Flags](https://posthog.com/docs/feature-flags)
- [Session Recording](https://posthog.com/docs/session-replay)

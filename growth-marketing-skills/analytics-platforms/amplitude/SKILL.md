---
name: amplitude
description: "Product analytics platform. User behavior tracking, event analysis, cohort analysis, funnel optimization, retention metrics, behavioral cohorting, API access."
---

# Amplitude Product Analytics

## Overview

Amplitude is a leading product analytics platform that helps teams understand user behavior, measure engagement, and optimize product experiences. This skill covers accessing Amplitude data via the Analytics API, performing cohort analysis, funnel optimization, and building retention reports.

## When to Use This Skill

- Analyzing user behavior and engagement patterns
- Building and tracking product funnels
- Creating behavioral cohorts for user segmentation
- Measuring feature adoption and usage
- Tracking retention and churn metrics
- A/B testing analysis and experimentation
- Product-led growth initiatives

## Core Capabilities

### 1. Amplitude API Setup

```python
import requests
import pandas as pd
from datetime import datetime, timedelta
import json

class AmplitudeAnalytics:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = "https://amplitude.com/api/2"

    def _make_request(self, endpoint, params):
        """Make authenticated request to Amplitude API"""
        response = requests.get(
            f"{self.base_url}/{endpoint}",
            auth=(self.api_key, self.secret_key),
            params=params
        )
        response.raise_for_status()
        return response.json()

    def get_active_users(self, start_date, end_date, interval='day'):
        """Get active users over time"""
        params = {
            'start': start_date,
            'end': end_date,
            'm': 'active',
            'i': interval
        }
        return self._make_request('users', params)

    def get_event_segmentation(self, event_name, start_date, end_date,
                               group_by=None, filters=None):
        """Segment events by properties"""
        params = {
            'e': json.dumps({
                'event_type': event_name,
                'filters': filters or []
            }),
            'start': start_date,
            'end': end_date
        }
        if group_by:
            params['g'] = group_by

        return self._make_request('events/segmentation', params)

# Initialize client
amplitude = AmplitudeAnalytics(
    api_key='YOUR_API_KEY',
    secret_key='YOUR_SECRET_KEY'
)

# Get active users for last 30 days
end_date = datetime.now().strftime('%Y%m%d')
start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')

users_data = amplitude.get_active_users(start_date, end_date)
print(f"Active Users: {users_data}")
```

### 2. Event Analysis and Segmentation

```python
def analyze_feature_usage(amplitude, feature_event, start_date, end_date):
    """Analyze feature usage patterns"""
    # Get event counts by user property
    usage_data = amplitude.get_event_segmentation(
        event_name=feature_event,
        start_date=start_date,
        end_date=end_date,
        group_by='user_type'
    )

    # Process results
    if 'data' in usage_data:
        series = usage_data['data']['series']
        xValues = usage_data['data']['xValues']

        # Create DataFrame
        df = pd.DataFrame({
            'date': xValues,
            **{s['segmentValue']: s['values'] for s in series}
        })

        return df
    return None

# Analyze button click events
feature_usage = analyze_feature_usage(
    amplitude,
    'Button Clicked',
    start_date='20240101',
    end_date='20240131'
)

if feature_usage is not None:
    print("\nFeature Usage by User Type:")
    print(feature_usage.head())

    # Calculate totals
    print("\nTotal Events by Segment:")
    for col in feature_usage.columns[1:]:
        print(f"  {col}: {feature_usage[col].sum():,}")
```

### 3. Funnel Analysis

```python
def analyze_funnel(amplitude, funnel_steps, start_date, end_date,
                   conversion_window='30_days'):
    """
    Analyze conversion funnel

    funnel_steps: List of event names in order
    conversion_window: Time window for conversion (e.g., '1_day', '7_days', '30_days')
    """
    # Build funnel request
    funnel_events = [
        {'event_type': step} for step in funnel_steps
    ]

    params = {
        'e': json.dumps(funnel_events),
        'start': start_date,
        'end': end_date,
        'mode': 'unordered',  # or 'ordered' for sequential
        'n': conversion_window
    }

    response = amplitude._make_request('funnels', params)

    # Process funnel data
    if 'data' in response:
        steps_data = response['data']['steps']

        funnel_df = pd.DataFrame([
            {
                'step': i + 1,
                'event': funnel_steps[i],
                'count': step['count'],
                'overall_conv_ratio': step.get('overall_conv_ratio', 0) * 100,
                'step_conv_ratio': step.get('step_conv_ratio', 0) * 100 if i > 0 else 100
            }
            for i, step in enumerate(steps_data)
        ])

        return funnel_df
    return None

# E-commerce funnel
funnel_steps = [
    'Product Viewed',
    'Add to Cart',
    'Begin Checkout',
    'Payment Info Entered',
    'Purchase Complete'
]

funnel_data = analyze_funnel(
    amplitude,
    funnel_steps,
    start_date='20240101',
    end_date='20240131',
    conversion_window='7_days'
)

if funnel_data is not None:
    print("\nConversion Funnel:")
    print(funnel_data)

    # Calculate drop-off
    funnel_data['drop_off'] = 100 - funnel_data['step_conv_ratio']
    print("\nDrop-off by Step:")
    print(funnel_data[['step', 'event', 'count', 'drop_off']])
```

### 4. Cohort Analysis and Retention

```python
def get_retention_analysis(amplitude, start_event, return_event,
                          start_date, end_date, interval='daily'):
    """
    Analyze user retention

    start_event: Initial event (e.g., 'Sign Up')
    return_event: Return event (e.g., 'Session Start')
    """
    params = {
        'se': json.dumps({'event_type': start_event}),
        're': json.dumps({'event_type': return_event}),
        'start': start_date,
        'end': end_date,
        'i': interval,
        'm': 'retention'
    }

    response = amplitude._make_request('retention', params)

    if 'data' in response:
        retention_data = response['data']

        # Build retention matrix
        cohorts = []
        for cohort_date, values in retention_data.items():
            cohort_row = {
                'cohort_date': cohort_date,
                'cohort_size': values[0] if values else 0
            }
            # Add retention percentages for each period
            for i, value in enumerate(values[1:], 1):
                cohort_row[f'day_{i}'] = (value / values[0] * 100) if values[0] > 0 else 0

            cohorts.append(cohort_row)

        return pd.DataFrame(cohorts)
    return None

# Analyze 30-day retention
retention = get_retention_analysis(
    amplitude,
    start_event='Sign Up',
    return_event='Session Start',
    start_date='20240101',
    end_date='20240131',
    interval='daily'
)

if retention is not None:
    print("\nRetention Analysis:")
    print(retention.head())

    # Calculate average retention by day
    day_columns = [col for col in retention.columns if col.startswith('day_')]
    avg_retention = retention[day_columns].mean()
    print("\nAverage Retention by Day:")
    for day, rate in avg_retention.items():
        print(f"  {day}: {rate:.1f}%")
```

### 5. User Segmentation and Behavioral Cohorts

```python
def create_behavioral_cohort(amplitude, event_conditions, property_conditions=None):
    """
    Create behavioral cohorts based on user actions

    event_conditions: List of events and their frequency
    property_conditions: User property filters
    """
    # Example: Users who completed onboarding but haven't purchased
    cohort_definition = {
        'conditions': [
            {
                'event_type': 'Onboarding Completed',
                'count_operator': '>=',
                'count': 1
            },
            {
                'event_type': 'Purchase',
                'count_operator': '=',
                'count': 0
            }
        ]
    }

    # In practice, cohorts are typically created in Amplitude UI
    # then accessed via API for analysis
    return cohort_definition

# Analyze cohort behavior
def analyze_cohort_metrics(amplitude, cohort_id, metrics, start_date, end_date):
    """Get metrics for a specific cohort"""
    params = {
        's': json.dumps([{'cohort_id': cohort_id}]),
        'start': start_date,
        'end': end_date
    }

    results = {}
    for metric_event in metrics:
        params['e'] = json.dumps({'event_type': metric_event})
        response = amplitude._make_request('events/segmentation', params)
        results[metric_event] = response

    return results

# Power user cohort analysis
power_user_metrics = analyze_cohort_metrics(
    amplitude,
    cohort_id='power_users_cohort',
    metrics=['Feature A Used', 'Feature B Used', 'Shared Content'],
    start_date='20240101',
    end_date='20240131'
)
```

### 6. Revenue and LTV Analysis

```python
def analyze_revenue_metrics(amplitude, start_date, end_date):
    """Analyze revenue events and user LTV"""
    # Get purchase events with revenue
    params = {
        'e': json.dumps({
            'event_type': 'Purchase',
            'group_by': [
                {'type': 'event', 'value': 'revenue'}
            ]
        }),
        'start': start_date,
        'end': end_date
    }

    revenue_data = amplitude._make_request('events/segmentation', params)

    # Process revenue over time
    if 'data' in revenue_data:
        series = revenue_data['data']['series']
        dates = revenue_data['data']['xValues']

        revenue_df = pd.DataFrame({
            'date': dates,
            'revenue': [sum(s['values']) for s in series]
        })

        # Calculate metrics
        total_revenue = revenue_df['revenue'].sum()
        avg_daily_revenue = revenue_df['revenue'].mean()

        print(f"Total Revenue: ${total_revenue:,.2f}")
        print(f"Average Daily Revenue: ${avg_daily_revenue:,.2f}")

        return revenue_df

    return None

# Get LTV by acquisition channel
def get_ltv_by_channel(amplitude, start_date, end_date):
    """Calculate LTV segmented by acquisition channel"""
    params = {
        'e': json.dumps({
            'event_type': 'Purchase'
        }),
        'start': start_date,
        'end': end_date,
        'g': 'utm_source'  # Group by acquisition source
    }

    response = amplitude._make_request('revenue/ltv', params)

    if 'data' in response:
        ltv_data = []
        for segment in response['data']['series']:
            ltv_data.append({
                'channel': segment['segmentValue'],
                'ltv': segment['value'],
                'user_count': segment['userCount']
            })

        ltv_df = pd.DataFrame(ltv_data)
        ltv_df['ltv_per_user'] = ltv_df['ltv'] / ltv_df['user_count']

        return ltv_df.sort_values('ltv_per_user', ascending=False)

    return None

# Run revenue analysis
revenue_df = analyze_revenue_metrics(amplitude, '20240101', '20240331')
ltv_df = get_ltv_by_channel(amplitude, '20240101', '20240331')

if ltv_df is not None:
    print("\nLTV by Acquisition Channel:")
    print(ltv_df)
```

### 7. Real-time Event Tracking

```python
def track_events_to_amplitude(api_key, events):
    """
    Send events to Amplitude HTTP API

    events: List of event dictionaries
    """
    url = "https://api2.amplitude.com/2/httpapi"

    payload = {
        'api_key': api_key,
        'events': events
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    return response.json()

# Track custom events
events_to_track = [
    {
        'user_id': 'user_123',
        'event_type': 'Campaign Email Clicked',
        'time': int(datetime.now().timestamp() * 1000),
        'event_properties': {
            'campaign_id': 'spring_sale_2024',
            'email_subject': 'Spring Sale - 50% Off',
            'link_clicked': 'shop_now_button'
        },
        'user_properties': {
            'subscription_tier': 'premium',
            'account_age_days': 180
        }
    },
    {
        'user_id': 'user_456',
        'event_type': 'Product Added to Wishlist',
        'time': int(datetime.now().timestamp() * 1000),
        'event_properties': {
            'product_id': 'PROD_789',
            'product_category': 'Electronics',
            'price': 299.99
        }
    }
]

# Send events
result = track_events_to_amplitude('YOUR_API_KEY', events_to_track)
print(f"Events tracked: {result}")
```

## Installation

```bash
uv pip install requests pandas numpy
```

For the official Amplitude Python SDK:

```bash
uv pip install amplitude-analytics
```

## Authentication

1. Log in to Amplitude and navigate to Settings > Projects
2. Select your project
3. Go to the "General" tab
4. Copy your API Key and Secret Key
5. For data export, you may need to enable the Amplitude Analytics API

## Quick Start

```python
import requests
from datetime import datetime, timedelta

# Amplitude API credentials
API_KEY = 'your_api_key'
SECRET_KEY = 'your_secret_key'

# Get active users for last 7 days
end_date = datetime.now().strftime('%Y%m%d')
start_date = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')

response = requests.get(
    'https://amplitude.com/api/2/users',
    auth=(API_KEY, SECRET_KEY),
    params={
        'start': start_date,
        'end': end_date,
        'm': 'active'
    }
)

data = response.json()
print(f"Active users (7d): {data}")
```

## Key Metrics Reference

- **Active Users**: Users who performed any event in the time period
- **New Users**: First-time users in the time period
- **DAU/WAU/MAU**: Daily/Weekly/Monthly Active Users
- **Stickiness**: DAU/MAU ratio indicating engagement
- **Retention**: Percentage of users returning after initial action
- **Session Length**: Average time users spend in the product
- **Events per Session**: Average number of events per session
- **Conversion Rate**: Percentage of users completing a funnel

## References

- [Amplitude Analytics API Documentation](https://developers.amplitude.com/docs/analytics-api)
- [Amplitude HTTP API for Event Tracking](https://developers.amplitude.com/docs/http-api-v2)
- [Amplitude Dashboard API](https://developers.amplitude.com/docs/dashboard-rest-api)
- [Amplitude Cohort API](https://developers.amplitude.com/docs/behavioral-cohorts-api)
- [Amplitude Python SDK](https://github.com/amplitude/Amplitude-Python)

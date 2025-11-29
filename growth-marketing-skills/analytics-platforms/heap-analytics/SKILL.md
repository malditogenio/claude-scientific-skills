---
name: heap-analytics
description: "Automatic event tracking platform. Session replay, retroactive analysis, user journey mapping, funnel analysis, no-code event definition."
---

# Heap Analytics

## Overview

Heap is a digital insights platform that automatically captures every user interaction on your website or app without requiring manual event tracking. This skill covers accessing Heap data via the API, analyzing user sessions, performing retroactive analysis, and leveraging automatic event capture for insights.

## When to Use This Skill

- Automatic capture of all user interactions without manual instrumentation
- Retroactive analysis of user behavior (analyze events you didn't explicitly track)
- Session replay and user journey analysis
- No-code event definition and analysis
- Funnel and conversion optimization
- Feature adoption tracking
- Understanding user paths and drop-off points

## Core Capabilities

### 1. Heap API Setup

```python
import requests
import pandas as pd
from datetime import datetime, timedelta
import json

class HeapAnalytics:
    def __init__(self, app_id, api_key):
        self.app_id = app_id
        self.api_key = api_key
        self.base_url = "https://api.heap.io/v1"
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, endpoint, method='GET', params=None, data=None):
        """Make authenticated request to Heap API"""
        url = f"{self.base_url}/{endpoint}"

        if method == 'GET':
            response = requests.get(url, headers=self.headers, params=params)
        else:
            response = requests.post(url, headers=self.headers, json=data)

        response.raise_for_status()
        return response.json()

    def get_event_definitions(self):
        """Get all event definitions"""
        return self._make_request(f'apps/{self.app_id}/events')

    def query_events(self, event_name, start_date, end_date, filters=None):
        """Query event data"""
        data = {
            'event': event_name,
            'from_date': start_date,
            'to_date': end_date,
            'filters': filters or []
        }
        return self._make_request(f'apps/{self.app_id}/events/query',
                                 method='POST', data=data)

# Initialize Heap client
heap = HeapAnalytics(
    app_id='YOUR_APP_ID',
    api_key='YOUR_API_KEY'
)

# Get all tracked events
events = heap.get_event_definitions()
print(f"Total events tracked: {len(events['events'])}")
for event in events['events'][:10]:
    print(f"  - {event['name']}")
```

### 2. Automatic Event Analysis

```python
def analyze_page_views(heap, start_date, end_date):
    """
    Analyze page views and user paths
    Heap automatically tracks all pageviews
    """
    # Query pageview events
    pageviews = heap.query_events(
        event_name='pageview',
        start_date=start_date,
        end_date=end_date
    )

    # Process pageview data
    if 'data' in pageviews:
        pv_data = []
        for record in pageviews['data']:
            pv_data.append({
                'timestamp': record.get('time'),
                'user_id': record.get('user_id'),
                'session_id': record.get('session_id'),
                'path': record.get('path'),
                'referrer': record.get('referrer'),
                'device': record.get('device_type')
            })

        df = pd.DataFrame(pv_data)

        # Analyze top pages
        top_pages = df['path'].value_counts().head(20)
        print("\nTop 20 Pages:")
        print(top_pages)

        # Analyze traffic sources
        if 'referrer' in df.columns:
            df['referrer_domain'] = df['referrer'].apply(
                lambda x: x.split('/')[2] if pd.notna(x) and '/' in str(x) else 'Direct'
            )
            top_sources = df['referrer_domain'].value_counts().head(10)
            print("\nTop Traffic Sources:")
            print(top_sources)

        return df

    return None

# Analyze last 30 days
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

pageview_df = analyze_page_views(
    heap,
    start_date.strftime('%Y-%m-%d'),
    end_date.strftime('%Y-%m-%d')
)
```

### 3. Session Analysis and Replay

```python
def get_user_sessions(heap, user_id, start_date, end_date):
    """Get all sessions for a specific user"""
    data = {
        'user_id': user_id,
        'from_date': start_date,
        'to_date': end_date
    }

    sessions = heap._make_request(
        f'apps/{heap.app_id}/sessions',
        method='POST',
        data=data
    )

    return sessions

def analyze_session_details(heap, session_id):
    """Get detailed event timeline for a session"""
    session_data = heap._make_request(
        f'apps/{heap.app_id}/sessions/{session_id}/events'
    )

    if 'events' in session_data:
        # Build session timeline
        timeline = []
        for event in session_data['events']:
            timeline.append({
                'timestamp': event.get('time'),
                'event_type': event.get('event_type'),
                'event_name': event.get('event_name'),
                'target': event.get('target_text', ''),
                'path': event.get('path', '')
            })

        df = pd.DataFrame(timeline)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')

        return df

    return None

# Analyze user journey
user_sessions = get_user_sessions(
    heap,
    user_id='user_12345',
    start_date='2024-01-01',
    end_date='2024-01-31'
)

if user_sessions and 'sessions' in user_sessions:
    print(f"Total sessions: {len(user_sessions['sessions'])}")

    # Analyze first session
    if user_sessions['sessions']:
        first_session = user_sessions['sessions'][0]
        session_timeline = analyze_session_details(heap, first_session['id'])

        if session_timeline is not None:
            print("\nSession Event Timeline:")
            print(session_timeline)
```

### 4. Retroactive Funnel Analysis

```python
def create_retroactive_funnel(heap, funnel_steps, start_date, end_date):
    """
    Create funnel analysis retroactively
    Define events after data collection
    """
    funnel_data = {
        'name': 'Retroactive Conversion Funnel',
        'steps': funnel_steps,
        'from_date': start_date,
        'to_date': end_date,
        'analysis_type': 'unique_users'
    }

    # Create funnel
    result = heap._make_request(
        f'apps/{heap.app_id}/funnels',
        method='POST',
        data=funnel_data
    )

    if 'funnel_id' in result:
        # Get funnel results
        funnel_results = heap._make_request(
            f'apps/{heap.app_id}/funnels/{result["funnel_id"]}/results'
        )

        # Process results
        if 'steps' in funnel_results:
            funnel_df = pd.DataFrame([
                {
                    'step': i + 1,
                    'event': step['event_name'],
                    'users': step['unique_users'],
                    'conversion_rate': step['conversion_rate'] * 100,
                    'drop_off': (1 - step['conversion_rate']) * 100 if i > 0 else 0
                }
                for i, step in enumerate(funnel_results['steps'])
            ])

            return funnel_df

    return None

# Define funnel steps retroactively
funnel_steps = [
    {'event': 'pageview', 'filters': [{'property': 'path', 'operator': 'contains', 'value': '/pricing'}]},
    {'event': 'click', 'filters': [{'property': 'target_text', 'operator': 'equals', 'value': 'Start Free Trial'}]},
    {'event': 'pageview', 'filters': [{'property': 'path', 'operator': 'equals', 'value': '/signup'}]},
    {'event': 'submit', 'filters': [{'property': 'form_name', 'operator': 'equals', 'value': 'signup_form'}]},
    {'event': 'pageview', 'filters': [{'property': 'path', 'operator': 'equals', 'value': '/dashboard'}]}
]

funnel_df = create_retroactive_funnel(
    heap,
    funnel_steps,
    start_date='2024-01-01',
    end_date='2024-01-31'
)

if funnel_df is not None:
    print("\nRetroactive Funnel Analysis:")
    print(funnel_df)
```

### 5. User Journey Mapping

```python
def map_user_journeys(heap, start_date, end_date, conversion_event):
    """
    Map paths users take to conversion
    """
    # Get users who converted
    converters = heap.query_events(
        event_name=conversion_event,
        start_date=start_date,
        end_date=end_date
    )

    if 'data' in converters:
        converter_ids = [record['user_id'] for record in converters['data']]

        # Get journey for each converter
        journeys = []
        for user_id in converter_ids[:100]:  # Limit to first 100
            sessions = get_user_sessions(heap, user_id, start_date, end_date)

            if sessions and 'sessions' in sessions:
                for session in sessions['sessions']:
                    session_events = analyze_session_details(heap, session['id'])
                    if session_events is not None:
                        # Extract path sequence
                        path_sequence = ' → '.join(
                            session_events['path'].unique()
                        )
                        journeys.append({
                            'user_id': user_id,
                            'session_id': session['id'],
                            'journey': path_sequence,
                            'events_count': len(session_events)
                        })

        journey_df = pd.DataFrame(journeys)

        # Find common paths
        common_journeys = journey_df['journey'].value_counts().head(20)
        print("\nMost Common Conversion Journeys:")
        print(common_journeys)

        return journey_df

    return None

# Map purchase journeys
journey_df = map_user_journeys(
    heap,
    start_date='2024-01-01',
    end_date='2024-01-31',
    conversion_event='purchase_complete'
)
```

### 6. Cohort Analysis

```python
def create_cohort_analysis(heap, cohort_event, return_event,
                          start_date, end_date):
    """
    Analyze cohort retention based on Heap events
    """
    cohort_data = {
        'initial_event': cohort_event,
        'return_event': return_event,
        'from_date': start_date,
        'to_date': end_date,
        'time_interval': 'week'
    }

    result = heap._make_request(
        f'apps/{heap.app_id}/cohorts/retention',
        method='POST',
        data=cohort_data
    )

    if 'cohorts' in result:
        # Process cohort data
        cohorts = []
        for cohort in result['cohorts']:
            cohort_row = {
                'cohort_date': cohort['date'],
                'cohort_size': cohort['size']
            }

            # Add retention by period
            for i, retention in enumerate(cohort['retention']):
                cohort_row[f'week_{i}'] = retention * 100

            cohorts.append(cohort_row)

        cohort_df = pd.DataFrame(cohorts)

        # Calculate average retention
        week_cols = [c for c in cohort_df.columns if c.startswith('week_')]
        avg_retention = cohort_df[week_cols].mean()

        print("\nCohort Retention Analysis:")
        print(cohort_df)
        print("\nAverage Retention by Week:")
        print(avg_retention)

        return cohort_df

    return None

# Analyze signup retention
cohort_df = create_cohort_analysis(
    heap,
    cohort_event='signup_complete',
    return_event='pageview',  # Any activity
    start_date='2024-01-01',
    end_date='2024-03-31'
)
```

### 7. Custom Event Tracking

```python
def track_server_side_event(app_id, event_name, identity, properties=None):
    """
    Track server-side events to Heap
    Useful for backend events not captured by auto-tracking
    """
    url = "https://heapanalytics.com/api/track"

    event_data = {
        'app_id': app_id,
        'identity': identity,
        'event': event_name,
        'properties': properties or {},
        'timestamp': datetime.now().isoformat()
    }

    response = requests.post(url, json=event_data)
    response.raise_for_status()

    return response.json()

# Track subscription events from backend
track_server_side_event(
    app_id='YOUR_APP_ID',
    event_name='Subscription Renewed',
    identity='user_12345',
    properties={
        'plan': 'premium',
        'amount': 99.00,
        'billing_cycle': 'monthly',
        'payment_method': 'credit_card'
    }
)

# Track custom business events
track_server_side_event(
    app_id='YOUR_APP_ID',
    event_name='Support Ticket Created',
    identity='user_67890',
    properties={
        'ticket_id': 'TICKET_5432',
        'priority': 'high',
        'category': 'billing',
        'source': 'email'
    }
)
```

### 8. Event Property Analysis

```python
def analyze_event_properties(heap, event_name, start_date, end_date,
                            property_name):
    """
    Analyze distribution of event properties
    Heap automatically captures element properties
    """
    events = heap.query_events(
        event_name=event_name,
        start_date=start_date,
        end_date=end_date
    )

    if 'data' in events:
        # Extract property values
        property_values = []
        for record in events['data']:
            if property_name in record:
                property_values.append({
                    'value': record[property_name],
                    'user_id': record.get('user_id'),
                    'timestamp': record.get('time')
                })

        df = pd.DataFrame(property_values)

        # Analyze distribution
        value_counts = df['value'].value_counts()
        print(f"\n{property_name} Distribution:")
        print(value_counts.head(20))

        # Unique users per value
        unique_users = df.groupby('value')['user_id'].nunique()
        print(f"\nUnique Users by {property_name}:")
        print(unique_users.head(20))

        return df

    return None

# Analyze button clicks by button text
button_analysis = analyze_event_properties(
    heap,
    event_name='click',
    start_date='2024-01-01',
    end_date='2024-01-31',
    property_name='target_text'
)

# Analyze form submissions by form type
form_analysis = analyze_event_properties(
    heap,
    event_name='submit',
    start_date='2024-01-01',
    end_date='2024-01-31',
    property_name='form_name'
)
```

## Installation

```bash
uv pip install requests pandas numpy
```

For client-side tracking (JavaScript):

```html
<script type="text/javascript">
  window.heap=window.heap||[],heap.load=function(e,t){window.heap.appid=e,window.heap.config=t=t||{};
  // ... (Heap snippet - get from Heap dashboard)
  heap.load("YOUR_APP_ID");
</script>
```

## Authentication

1. Log in to Heap and navigate to Account > Manage > Projects
2. Select your project
3. Go to Settings > Setup
4. Copy your App ID
5. Generate an API key under Settings > API

## Quick Start

```python
import requests

# Heap API credentials
APP_ID = 'your_app_id'
API_KEY = 'your_api_key'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Get all events
response = requests.get(
    f'https://api.heap.io/v1/apps/{APP_ID}/events',
    headers=headers
)

events = response.json()
print(f"Total events: {len(events.get('events', []))}")

# Query specific event
event_query = {
    'event': 'pageview',
    'from_date': '2024-01-01',
    'to_date': '2024-01-31'
}

response = requests.post(
    f'https://api.heap.io/v1/apps/{APP_ID}/events/query',
    headers=headers,
    json=event_query
)

data = response.json()
print(f"Pageviews: {len(data.get('data', []))}")
```

## Key Features

- **Automatic Capture**: Every click, pageview, form submission automatically tracked
- **Retroactive Analysis**: Define and analyze events after data collection
- **Session Replay**: Visual playback of user sessions
- **No Code Required**: Define events through UI without engineering
- **Complete Data**: Never miss an event - everything is captured
- **User Journeys**: Full path analysis from first touch to conversion

## References

- [Heap API Documentation](https://developers.heap.io/reference)
- [Heap Data Model](https://developers.heap.io/docs/data-model)
- [Heap Server-Side API](https://developers.heap.io/docs/server-side-api)
- [Heap JavaScript API](https://developers.heap.io/docs/web)
- [Heap SQL Query Guide](https://developers.heap.io/docs/heap-sql-query-guide)

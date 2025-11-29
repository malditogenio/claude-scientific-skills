---
name: fullstory
description: "Digital experience analytics. Session replay, funnel analysis, user journey mapping, error tracking, product analytics, conversion optimization."
---

# FullStory Digital Experience Analytics

## Overview

FullStory is a digital experience intelligence platform that captures and analyzes every user interaction. It provides session replay, advanced search, funnel analysis, and insights into user frustration and behavior. This skill covers API access, session analysis, and extracting actionable insights from user interactions.

## When to Use This Skill

- Analyzing complete user sessions and journeys
- Debugging user-reported issues with session replay
- Understanding friction points in user experience
- Measuring feature adoption and usage patterns
- Analyzing conversion funnels and drop-offs
- Identifying and fixing rage clicks and error clicks
- Product analytics and optimization

## Core Capabilities

### 1. FullStory API Setup

```python
import requests
import pandas as pd
from datetime import datetime, timedelta
import json

class FullStoryAnalytics:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.fullstory.com"
        self.headers = {
            'Authorization': f'Basic {api_key}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, endpoint, method='GET', params=None, data=None):
        """Make authenticated request to FullStory API"""
        url = f"{self.base_url}/{endpoint}"

        if method == 'GET':
            response = requests.get(url, headers=self.headers, params=params)
        elif method == 'POST':
            response = requests.post(url, headers=self.headers, json=data)

        response.raise_for_status()
        return response.json()

    def search_sessions(self, query, limit=100):
        """Search for sessions using FullStory query language"""
        data = {
            'query': query,
            'limit': limit
        }
        return self._make_request('v1/sessions', method='POST', data=data)

    def get_session_data(self, session_id):
        """Get detailed data for a specific session"""
        return self._make_request(f'v1/sessions/{session_id}')

    def get_events(self, query, limit=1000):
        """Search for events"""
        data = {
            'query': query,
            'limit': limit
        }
        return self._make_request('v1/events', method='POST', data=data)

# Initialize FullStory client
fullstory = FullStoryAnalytics(api_key='YOUR_API_KEY')

# Search for sessions from last 7 days
sessions = fullstory.search_sessions(
    query='created >= now() - 7 days'
)

print(f"Found {len(sessions.get('sessions', []))} sessions")
```

### 2. Session Search and Analysis

```python
def analyze_conversion_sessions(fullstory, conversion_event, days=7):
    """
    Analyze sessions that converted
    """
    # Search for sessions with conversion event
    query = f"""
        created >= now() - {days} days AND
        event: '{conversion_event}'
    """

    sessions = fullstory.search_sessions(query, limit=500)

    if 'sessions' in sessions:
        session_data = []
        for session in sessions['sessions']:
            session_data.append({
                'session_id': session['id'],
                'user_id': session.get('userId'),
                'created': session['createdTime'],
                'duration': session.get('durationMs', 0) / 1000,  # Convert to seconds
                'pages': session.get('pageViews', 0),
                'device': session.get('deviceType'),
                'browser': session.get('browser'),
                'location': session.get('location')
            })

        sessions_df = pd.DataFrame(session_data)

        print(f"\nConversion Sessions Analysis:")
        print(f"Total converting sessions: {len(sessions_df)}")
        print(f"Average session duration: {sessions_df['duration'].mean():.0f}s")
        print(f"Average pages viewed: {sessions_df['pages'].mean():.1f}")

        # Device breakdown
        print("\nDevice Distribution:")
        print(sessions_df['device'].value_counts())

        return sessions_df

    return None

# Analyze purchase completions
purchase_sessions = analyze_conversion_sessions(
    fullstory,
    conversion_event='purchase_complete',
    days=30
)

# Analyze signup sessions
signup_sessions = analyze_conversion_sessions(
    fullstory,
    conversion_event='signup_complete',
    days=7
)
```

### 3. Funnel Analysis

```python
def create_fullstory_funnel(fullstory, funnel_steps, days=30):
    """
    Create and analyze funnel using FullStory events
    """
    funnel_data = []

    for i, step in enumerate(funnel_steps):
        # Build query for this step and all subsequent steps
        step_query = f"created >= now() - {days} days AND event: '{step['event']}'"

        # Add filters if specified
        if 'filters' in step:
            for filter_key, filter_value in step['filters'].items():
                step_query += f" AND {filter_key}: '{filter_value}'"

        # Get sessions for this step
        sessions = fullstory.search_sessions(step_query, limit=10000)

        step_count = len(sessions.get('sessions', []))

        funnel_data.append({
            'step': i + 1,
            'event': step['event'],
            'sessions': step_count
        })

    funnel_df = pd.DataFrame(funnel_data)

    # Calculate conversion rates
    if not funnel_df.empty:
        funnel_df['conversion_rate'] = (
            funnel_df['sessions'] / funnel_df['sessions'].iloc[0] * 100
        )
        funnel_df['drop_off'] = 100 - funnel_df['conversion_rate']

        print("\nFunnel Analysis:")
        print(funnel_df)

        # Identify critical drop-off points
        if len(funnel_df) > 1:
            funnel_df['step_drop'] = funnel_df['sessions'].diff().abs()
            critical_step = funnel_df.loc[funnel_df['step_drop'].idxmax()]
            print(f"\nCritical drop-off at step {critical_step['step']}: {critical_step['event']}")

    return funnel_df

# Define e-commerce funnel
funnel_steps = [
    {'event': 'product_viewed'},
    {'event': 'add_to_cart'},
    {'event': 'checkout_started'},
    {'event': 'payment_info_entered'},
    {'event': 'purchase_complete'}
]

funnel = create_fullstory_funnel(fullstory, funnel_steps, days=30)
```

### 4. Rage Click and Frustration Analysis

```python
def analyze_frustration_signals(fullstory, days=7):
    """
    Identify sessions with frustration signals
    (rage clicks, error clicks, dead clicks)
    """
    # Search for sessions with rage clicks
    rage_query = f"""
        created >= now() - {days} days AND
        hasRageClick is true
    """

    rage_sessions = fullstory.search_sessions(rage_query, limit=500)

    # Search for sessions with errors
    error_query = f"""
        created >= now() - {days} days AND
        hasError is true
    """

    error_sessions = fullstory.search_sessions(error_query, limit=500)

    rage_count = len(rage_sessions.get('sessions', []))
    error_count = len(error_sessions.get('sessions', []))

    print(f"\nFrustration Analysis (Last {days} days):")
    print(f"Sessions with rage clicks: {rage_count}")
    print(f"Sessions with errors: {error_count}")

    # Analyze rage click sessions
    if rage_count > 0:
        rage_data = []
        for session in rage_sessions['sessions'][:100]:
            rage_data.append({
                'session_id': session['id'],
                'user_id': session.get('userId'),
                'duration': session.get('durationMs', 0) / 1000,
                'page_url': session.get('startUrl'),
                'device': session.get('deviceType')
            })

        rage_df = pd.DataFrame(rage_data)

        print("\nTop Pages with Rage Clicks:")
        print(rage_df['page_url'].value_counts().head(10))

        return rage_df

    return None

frustration_sessions = analyze_frustration_signals(fullstory, days=7)

def get_specific_frustration_events(fullstory, page_url, days=7):
    """Get frustration events for a specific page"""
    query = f"""
        created >= now() - {days} days AND
        pageUrl: '{page_url}' AND
        (hasRageClick is true OR hasError is true)
    """

    events = fullstory.get_events(query)

    if 'events' in events:
        event_data = []
        for event in events['events']:
            event_data.append({
                'event_type': event.get('eventType'),
                'target': event.get('targetText', ''),
                'selector': event.get('selector', ''),
                'timestamp': event.get('timestamp')
            })

        events_df = pd.DataFrame(event_data)

        print(f"\nFrustration Events on {page_url}:")
        print(f"Total events: {len(events_df)}")

        if 'target' in events_df.columns:
            print("\nMost Problematic Elements:")
            print(events_df['target'].value_counts().head(10))

        return events_df

    return None

# Analyze specific problematic page
checkout_frustration = get_specific_frustration_events(
    fullstory,
    page_url='https://yoursite.com/checkout',
    days=7
)
```

### 5. User Journey Mapping

```python
def map_user_journey(fullstory, user_id, days=30):
    """
    Map complete journey for a specific user
    """
    query = f"""
        created >= now() - {days} days AND
        userId: '{user_id}'
    """

    sessions = fullstory.search_sessions(query)

    if 'sessions' in sessions:
        journeys = []
        for session in sessions['sessions']:
            session_id = session['id']

            # Get detailed session data
            session_details = fullstory.get_session_data(session_id)

            if 'events' in session_details:
                # Extract page path
                pages = [event.get('pageUrl', '') for event in session_details['events']
                        if event.get('eventType') == 'navigate']

                journeys.append({
                    'session_id': session_id,
                    'date': session['createdTime'],
                    'duration': session.get('durationMs', 0) / 1000,
                    'pages_visited': len(set(pages)),
                    'journey': ' → '.join(pages[:10])  # First 10 pages
                })

        journey_df = pd.DataFrame(journeys)

        print(f"\nUser Journey for {user_id}:")
        print(f"Total sessions: {len(journey_df)}")
        print(f"Average duration: {journey_df['duration'].mean():.0f}s")

        print("\nSession Timeline:")
        print(journey_df[['date', 'duration', 'pages_visited']])

        return journey_df

    return None

# Map specific user journey
user_journey = map_user_journey(fullstory, user_id='user_12345', days=30)

def find_common_paths(fullstory, conversion_event, days=7):
    """Find common paths to conversion"""
    query = f"""
        created >= now() - {days} days AND
        event: '{conversion_event}'
    """

    sessions = fullstory.search_sessions(query, limit=200)

    if 'sessions' in sessions:
        paths = []
        for session in sessions['sessions']:
            session_details = fullstory.get_session_data(session['id'])

            if 'events' in session_details:
                # Extract navigation events
                nav_events = [e for e in session_details['events']
                            if e.get('eventType') == 'navigate']

                if nav_events:
                    path = ' → '.join([e.get('pageUrl', '') for e in nav_events[:5]])
                    paths.append(path)

        # Count most common paths
        from collections import Counter
        path_counts = Counter(paths)

        print(f"\nMost Common Paths to {conversion_event}:")
        for path, count in path_counts.most_common(10):
            print(f"  ({count}x) {path}")

        return pd.DataFrame(path_counts.most_common(), columns=['path', 'count'])

    return None

common_paths = find_common_paths(fullstory, 'purchase_complete', days=30)
```

### 6. Event Analytics

```python
def analyze_feature_usage(fullstory, feature_event, days=30):
    """
    Analyze feature usage patterns
    """
    query = f"""
        created >= now() - {days} days AND
        event: '{feature_event}'
    """

    events = fullstory.get_events(query, limit=5000)

    if 'events' in events:
        event_data = []
        for event in events['events']:
            event_data.append({
                'timestamp': event.get('timestamp'),
                'user_id': event.get('userId'),
                'session_id': event.get('sessionId'),
                'page_url': event.get('pageUrl'),
                'target': event.get('targetText', ''),
                'device': event.get('deviceType')
            })

        events_df = pd.DataFrame(event_data)
        events_df['timestamp'] = pd.to_datetime(events_df['timestamp'])
        events_df['date'] = events_df['timestamp'].dt.date

        print(f"\nFeature Usage Analysis: {feature_event}")
        print(f"Total events: {len(events_df)}")
        print(f"Unique users: {events_df['user_id'].nunique()}")

        # Daily usage
        daily_usage = events_df.groupby('date').agg({
            'user_id': 'nunique',
            'session_id': 'count'
        }).rename(columns={'user_id': 'unique_users', 'session_id': 'events'})

        print("\nDaily Usage:")
        print(daily_usage.tail(7))

        # Device breakdown
        print("\nDevice Breakdown:")
        print(events_df['device'].value_counts())

        return events_df

    return None

# Analyze button clicks
button_usage = analyze_feature_usage(
    fullstory,
    feature_event='button_clicked',
    days=30
)

# Analyze search usage
search_usage = analyze_feature_usage(
    fullstory,
    feature_event='search_performed',
    days=30
)
```

### 7. Conversion Attribution

```python
def analyze_conversion_attribution(fullstory, conversion_event, days=30):
    """
    Analyze what actions lead to conversions
    """
    # Get converting sessions
    query = f"""
        created >= now() - {days} days AND
        event: '{conversion_event}'
    """

    sessions = fullstory.search_sessions(query, limit=500)

    if 'sessions' in sessions:
        attribution_data = []

        for session in sessions['sessions']:
            session_details = fullstory.get_session_data(session['id'])

            if 'events' in session_details:
                # Get all events before conversion
                events = session_details['events']

                # Extract key touchpoints
                pages_visited = set()
                features_used = []

                for event in events:
                    if event.get('eventType') == 'navigate':
                        pages_visited.add(event.get('pageUrl', ''))
                    elif event.get('eventType') == 'click':
                        features_used.append(event.get('targetText', ''))

                attribution_data.append({
                    'session_id': session['id'],
                    'pages_count': len(pages_visited),
                    'clicks_count': len(features_used),
                    'duration': session.get('durationMs', 0) / 1000,
                    'first_page': list(pages_visited)[0] if pages_visited else None
                })

        attr_df = pd.DataFrame(attribution_data)

        print(f"\nConversion Attribution Analysis:")
        print(f"Average pages before conversion: {attr_df['pages_count'].mean():.1f}")
        print(f"Average clicks before conversion: {attr_df['clicks_count'].mean():.1f}")
        print(f"Average time to conversion: {attr_df['duration'].mean():.0f}s")

        # Landing pages for conversions
        print("\nTop Landing Pages for Conversions:")
        print(attr_df['first_page'].value_counts().head(10))

        return attr_df

    return None

conversion_attribution = analyze_conversion_attribution(
    fullstory,
    conversion_event='purchase_complete',
    days=30
)
```

### 8. Segment Analysis

```python
def analyze_user_segments(fullstory, segment_property, days=30):
    """
    Compare behavior across user segments
    """
    segments = ['free', 'premium', 'enterprise']  # Example segments
    segment_data = []

    for segment in segments:
        query = f"""
            created >= now() - {days} days AND
            {segment_property}: '{segment}'
        """

        sessions = fullstory.search_sessions(query, limit=1000)

        if 'sessions' in sessions:
            session_list = sessions['sessions']

            segment_data.append({
                'segment': segment,
                'sessions': len(session_list),
                'avg_duration': sum(s.get('durationMs', 0) for s in session_list) / len(session_list) / 1000 if session_list else 0,
                'avg_pages': sum(s.get('pageViews', 0) for s in session_list) / len(session_list) if session_list else 0
            })

    segment_df = pd.DataFrame(segment_data)

    print("\nUser Segment Comparison:")
    print(segment_df)

    return segment_df

segment_comparison = analyze_user_segments(
    fullstory,
    segment_property='planType',
    days=30
)
```

## Installation

```bash
uv pip install requests pandas numpy
```

FullStory JavaScript snippet (add to website):

```html
<script>
window['_fs_debug'] = false;
window['_fs_host'] = 'fullstory.com';
window['_fs_script'] = 'edge.fullstory.com/s/fs.js';
window['_fs_org'] = 'YOUR_ORG_ID';
window['_fs_namespace'] = 'FS';
(function(m,n,e,t,l,o,g,y){
    // FullStory snippet...
})();
</script>
```

## Authentication

1. Log in to FullStory
2. Navigate to Settings > Integrations & API Keys
3. Create a new API Key
4. Copy the key (base64 encoded for Basic Auth)

## Quick Start

```python
import requests
import base64

# Encode API key for Basic Auth
api_key = 'your_api_key'
encoded_key = base64.b64encode(f'{api_key}:'.encode()).decode()

headers = {
    'Authorization': f'Basic {encoded_key}',
    'Content-Type': 'application/json'
}

# Search for sessions
query = {
    'query': 'created >= now() - 7 days',
    'limit': 10
}

response = requests.post(
    'https://api.fullstory.com/v1/sessions',
    headers=headers,
    json=query
)

sessions = response.json()
print(f"Sessions: {len(sessions.get('sessions', []))}")
```

## Key Features

- **Session Replay**: Watch exact user interactions
- **Omnisearch**: Powerful query language for finding sessions
- **Frustration Signals**: Rage clicks, error clicks, dead clicks
- **Conversion Funnels**: Analyze drop-off points
- **Event Analytics**: Track custom events and interactions
- **Console Logs**: See JavaScript errors in context
- **User Journey Maps**: Visualize complete user paths

## References

- [FullStory API Documentation](https://developer.fullstory.com/api)
- [FullStory Query Language](https://help.fullstory.com/hc/en-us/articles/360020623234)
- [Session Replay Guide](https://www.fullstory.com/platform/session-replay/)
- [FullStory JavaScript API](https://developer.fullstory.com/browser/getting-started/)

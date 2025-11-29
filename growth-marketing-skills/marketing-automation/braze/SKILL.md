---
name: braze
description: "Braze customer engagement platform. Multi-channel messaging (email, push, SMS, in-app), user segmentation, Canvas journeys, analytics, real-time personalization."
---

# Braze Integration

## Overview

Braze is a comprehensive customer engagement platform for orchestrating multi-channel marketing campaigns across email, push notifications, SMS, and in-app messages. This skill covers using the Braze API for user management, campaign creation, Canvas journeys, and analytics.

## When to Use This Skill

- Multi-channel customer engagement
- Mobile app push notifications
- In-app messaging
- Cross-channel user journeys (Canvas)
- Real-time personalization
- User behavior tracking and segmentation
- Lifecycle marketing campaigns
- A/B testing across channels

## Core Capabilities

### 1. User Profile Management

```python
import requests
import json
from datetime import datetime

# Braze API configuration
API_KEY = 'your-rest-api-key'
REST_ENDPOINT = 'https://rest.iad-01.braze.com'  # Your cluster endpoint

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}

# Track user attributes
def track_user_attributes(external_id, attributes):
    url = f'{REST_ENDPOINT}/users/track'

    data = {
        'attributes': [
            {
                'external_id': external_id,
                **attributes
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example usage
result = track_user_attributes(
    'user_12345',
    {
        'email': 'user@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'country': 'US',
        'subscription_status': 'subscribed',
        'custom_attributes': {
            'loyalty_tier': 'gold',
            'total_purchases': 15,
            'lifetime_value': 1250.50
        }
    }
)

print(f"User tracked: {result}")

# Batch track users
def batch_track_users(users_data):
    url = f'{REST_ENDPOINT}/users/track'

    data = {
        'attributes': [
            {
                'external_id': user['external_id'],
                **user['attributes']
            }
            for user in users_data
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Track custom events
def track_custom_event(external_id, event_name, properties=None):
    url = f'{REST_ENDPOINT}/users/track'

    data = {
        'events': [
            {
                'external_id': external_id,
                'name': event_name,
                'time': datetime.now().isoformat(),
                'properties': properties or {}
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example: Track purchase event
track_custom_event(
    'user_12345',
    'Made Purchase',
    {
        'product_id': 'SKU-999',
        'product_name': 'Premium Widget',
        'price': 99.99,
        'quantity': 2,
        'category': 'Electronics'
    }
)

# Track purchases for revenue
def track_purchase(external_id, product_id, currency, price, quantity=1, properties=None):
    url = f'{REST_ENDPOINT}/users/track'

    data = {
        'purchases': [
            {
                'external_id': external_id,
                'product_id': product_id,
                'currency': currency,
                'price': price,
                'quantity': quantity,
                'time': datetime.now().isoformat(),
                'properties': properties or {}
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()
```

### 2. Campaign Management

```python
# Send campaign to users
def send_campaign(campaign_id, recipient_ids, overrides=None):
    url = f'{REST_ENDPOINT}/campaigns/trigger/send'

    data = {
        'campaign_id': campaign_id,
        'recipients': [
            {
                'external_user_id': user_id,
                'trigger_properties': overrides.get(user_id, {}) if overrides else {}
            }
            for user_id in recipient_ids
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Send campaign with audience targeting
def send_targeted_campaign(campaign_id, segment_id=None, trigger_properties=None):
    url = f'{REST_ENDPOINT}/campaigns/trigger/send'

    data = {
        'campaign_id': campaign_id,
        'broadcast': True
    }

    if segment_id:
        data['segment_id'] = segment_id

    if trigger_properties:
        data['trigger_properties'] = trigger_properties

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Get campaign details
def get_campaign_details(campaign_id):
    url = f'{REST_ENDPOINT}/campaigns/details'

    params = {'campaign_id': campaign_id}

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Get campaign analytics
def get_campaign_analytics(campaign_id, length=7, end_time=None):
    url = f'{REST_ENDPOINT}/campaigns/data_series'

    params = {
        'campaign_id': campaign_id,
        'length': length,
        'ending_at': end_time or datetime.now().isoformat()
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Example: Send personalized campaign
personalization = {
    'user_001': {'discount_code': 'SAVE20'},
    'user_002': {'discount_code': 'SAVE15'}
}

send_campaign(
    'campaign_abc123',
    ['user_001', 'user_002'],
    overrides=personalization
)

# Get campaign performance
analytics = get_campaign_analytics('campaign_abc123', length=30)
print(f"Campaign Analytics: {analytics}")
```

### 3. Canvas Journey Orchestration

```python
# Trigger Canvas journey
def trigger_canvas(canvas_id, recipient_ids, trigger_properties=None):
    url = f'{REST_ENDPOINT}/canvas/trigger/send'

    data = {
        'canvas_id': canvas_id,
        'recipients': [
            {
                'external_user_id': user_id,
                'canvas_entry_properties': trigger_properties or {}
            }
            for user_id in recipient_ids
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Get Canvas details
def get_canvas_details(canvas_id):
    url = f'{REST_ENDPOINT}/canvas/details'

    params = {'canvas_id': canvas_id}

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Get Canvas analytics
def get_canvas_analytics(canvas_id, length=7):
    url = f'{REST_ENDPOINT}/canvas/data_series'

    params = {
        'canvas_id': canvas_id,
        'length': length
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Example: Trigger onboarding journey
trigger_canvas(
    'canvas_onboarding_123',
    ['new_user_001', 'new_user_002'],
    trigger_properties={
        'signup_source': 'website',
        'plan_type': 'premium'
    }
)

# Example: Monitor Canvas performance
canvas_stats = get_canvas_analytics('canvas_onboarding_123', length=30)

for step in canvas_stats.get('data', {}).get('stats', []):
    print(f"Step: {step['name']}")
    print(f"  Entries: {step.get('entries', 0)}")
    print(f"  Conversions: {step.get('conversions', 0)}")
```

### 4. Segments and Targeting

```python
# Export segment users
def export_segment(segment_id, callback_endpoint=None):
    url = f'{REST_ENDPOINT}/users/export/segment'

    data = {
        'segment_id': segment_id,
        'fields_to_export': [
            'external_id',
            'email',
            'first_name',
            'last_name',
            'custom_attributes'
        ]
    }

    if callback_endpoint:
        data['callback_endpoint'] = callback_endpoint

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Query users by identifier
def export_users_by_ids(external_ids):
    url = f'{REST_ENDPOINT}/users/export/ids'

    data = {
        'external_ids': external_ids,
        'fields_to_export': [
            'external_id',
            'email',
            'custom_attributes',
            'campaigns_received',
            'purchases'
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Get segment list
def list_segments():
    url = f'{REST_ENDPOINT}/segments/list'

    response = requests.get(url, headers=headers)
    return response.json()

# Get segment details
def get_segment_details(segment_id):
    url = f'{REST_ENDPOINT}/segments/details'

    params = {'segment_id': segment_id}

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Example: Export high-value customers
segment_export = export_segment('segment_high_value_123')
export_id = segment_export.get('export_id')

print(f"Segment export initiated: {export_id}")

# Get specific users
users_data = export_users_by_ids(['user_001', 'user_002', 'user_003'])
print(f"Exported {len(users_data.get('users', []))} users")
```

### 5. Multi-Channel Messaging

```python
# Send transactional email
def send_transactional_email(campaign_id, email, trigger_properties):
    url = f'{REST_ENDPOINT}/campaigns/trigger/send'

    data = {
        'campaign_id': campaign_id,
        'recipients': [
            {
                'external_user_id': email,
                'trigger_properties': trigger_properties
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Send push notification
def send_push_notification(user_ids, message, title=None, deep_link=None):
    url = f'{REST_ENDPOINT}/messages/send'

    data = {
        'broadcast': False,
        'external_user_ids': user_ids,
        'messages': {
            'apple_push': {
                'alert': message,
                'extra': {
                    'deep_link': deep_link
                } if deep_link else {}
            },
            'android_push': {
                'title': title or 'Notification',
                'alert': message,
                'extra': {
                    'deep_link': deep_link
                } if deep_link else {}
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Send SMS
def send_sms(subscription_group_id, phone_numbers, message):
    url = f'{REST_ENDPOINT}/messages/send'

    data = {
        'broadcast': False,
        'phone_numbers': phone_numbers,
        'messages': {
            'sms': {
                'subscription_group_id': subscription_group_id,
                'message_variation_id': None,
                'body': message
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example: Send order confirmation
send_transactional_email(
    'campaign_order_confirmation',
    'customer@example.com',
    {
        'order_number': '12345',
        'order_total': '$99.99',
        'estimated_delivery': '3-5 business days'
    }
)

# Send cart abandonment push
send_push_notification(
    ['user_12345'],
    'You left items in your cart! Complete your purchase now.',
    title='Cart Reminder',
    deep_link='app://cart'
)
```

### 6. Analytics and Reporting

```python
import pandas as pd
from datetime import timedelta

# Get engagement stats
def get_engagement_stats(start_date, end_date):
    url = f'{REST_ENDPOINT}/kpi/dau/data_series'

    params = {
        'length': (end_date - start_date).days,
        'ending_at': end_date.isoformat()
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Get revenue data
def get_revenue_data(start_date, end_date):
    url = f'{REST_ENDPOINT}/purchases/revenue_series'

    data = {
        'length': (end_date - start_date).days,
        'ending_at': end_date.isoformat(),
        'unit': 'day'
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Get campaign performance summary
def get_campaigns_summary():
    url = f'{REST_ENDPOINT}/campaigns/list'

    response = requests.get(url, headers=headers)
    campaigns = response.json()

    summary = []

    for campaign in campaigns.get('campaigns', []):
        campaign_id = campaign['id']
        analytics = get_campaign_analytics(campaign_id, length=30)

        summary.append({
            'campaign_name': campaign['name'],
            'campaign_id': campaign_id,
            'last_sent': campaign.get('last_sent'),
            'analytics': analytics
        })

    return summary

# Generate comprehensive report
def generate_marketing_report(days=30):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Get engagement
    engagement = get_engagement_stats(start_date, end_date)

    # Get revenue
    revenue = get_revenue_data(start_date, end_date)

    # Get campaign performance
    campaigns = get_campaigns_summary()

    report = {
        'period': f'{start_date.date()} to {end_date.date()}',
        'engagement': engagement,
        'revenue': revenue,
        'campaigns': campaigns
    }

    return report

# Example usage
report = generate_marketing_report(30)
print(f"Marketing Report: {report['period']}")
print(f"Total Campaigns: {len(report['campaigns'])}")
```

## Installation

```bash
uv pip install requests pandas
```

## Authentication

Get your API credentials from Braze:
1. Log in to Braze Dashboard
2. Go to Settings > API Keys
3. Create a new REST API Key with appropriate permissions
4. Note your REST Endpoint URL (cluster-specific)

```python
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}
```

## Quick Start

```python
import requests
from datetime import datetime

API_KEY = 'your-rest-api-key'
REST_ENDPOINT = 'https://rest.iad-01.braze.com'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}

# Track user and event
data = {
    'attributes': [
        {
            'external_id': 'user_12345',
            'email': 'user@example.com',
            'first_name': 'Jane'
        }
    ],
    'events': [
        {
            'external_id': 'user_12345',
            'name': 'App Opened',
            'time': datetime.now().isoformat()
        }
    ]
}

response = requests.post(
    f'{REST_ENDPOINT}/users/track',
    headers=headers,
    json=data
)

print(f"Response: {response.json()}")
```

## Key Features Reference

- **Users**: Profile management, attributes, events
- **Campaigns**: One-time sends across channels
- **Canvas**: Multi-step customer journeys
- **Segments**: Dynamic audience targeting
- **Email**: Rich email campaigns
- **Push**: Mobile and web push notifications
- **In-App**: Native app messaging
- **SMS**: Text message campaigns
- **Content Cards**: Persistent in-app content
- **Analytics**: Engagement, retention, revenue tracking

## References

- [Braze API Documentation](https://www.braze.com/docs/api/home/)
- [REST API Endpoints](https://www.braze.com/docs/api/endpoints/)
- [Canvas Documentation](https://www.braze.com/docs/user_guide/engagement_tools/canvas/)
- [User Tracking Guide](https://www.braze.com/docs/api/endpoints/user_data/post_user_track/)
- [Campaign Triggering](https://www.braze.com/docs/api/endpoints/messaging/send_messages/post_send_triggered_campaigns/)

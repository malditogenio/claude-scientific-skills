---
name: customer-io
description: "Customer.io behavioral messaging platform. Event-driven campaigns, customer segmentation, email/SMS/push automation, transactional messaging, A/B testing."
---

# Customer.io Integration

## Overview

Customer.io is a versatile customer engagement platform focused on behavioral messaging across email, SMS, push, and in-app channels. This skill covers using the Customer.io API for event tracking, campaign management, and customer journey automation.

## When to Use This Skill

- Behavioral email and messaging automation
- Event-driven customer communications
- Transactional emails (receipts, notifications)
- User onboarding and lifecycle campaigns
- Customer segmentation based on behavior
- Multi-channel messaging orchestration
- Real-time personalization
- Customer journey mapping

## Core Capabilities

### 1. Customer Profile Management

```python
import requests
import json
from datetime import datetime

# Customer.io API configuration
SITE_ID = 'your-site-id'
API_KEY = 'your-api-key'
TRACK_API_URL = 'https://track.customer.io/api/v1'
APP_API_URL = 'https://api.customer.io/v1/api'

# Track API uses Basic Auth
from requests.auth import HTTPBasicAuth
track_auth = HTTPBasicAuth(SITE_ID, API_KEY)

# App API uses Bearer token
APP_API_KEY = 'your-app-api-key'
app_headers = {
    'Authorization': f'Bearer {APP_API_KEY}',
    'Content-Type': 'application/json'
}

# Create or update customer
def identify_customer(customer_id, attributes):
    url = f'{TRACK_API_URL}/customers/{customer_id}'

    response = requests.put(
        url,
        auth=track_auth,
        json=attributes
    )

    return response.status_code == 200

# Example usage
success = identify_customer(
    'user_12345',
    {
        'email': 'user@example.com',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'created_at': int(datetime.now().timestamp()),
        'plan': 'premium',
        'total_revenue': 499.95,
        'custom_attributes': {
            'favorite_category': 'electronics',
            'preference_email_frequency': 'weekly'
        }
    }
)

print(f"Customer identified: {success}")

# Delete customer
def delete_customer(customer_id):
    url = f'{TRACK_API_URL}/customers/{customer_id}'

    response = requests.delete(url, auth=track_auth)
    return response.status_code == 200

# Add customer to segment
def add_to_segment(segment_id, customer_ids):
    url = f'{TRACK_API_URL}/segments/{segment_id}/add_customers'

    data = {'ids': customer_ids}

    response = requests.post(
        url,
        auth=track_auth,
        json=data
    )

    return response.status_code == 200

# Remove from segment
def remove_from_segment(segment_id, customer_ids):
    url = f'{TRACK_API_URL}/segments/{segment_id}/remove_customers'

    data = {'ids': customer_ids}

    response = requests.post(
        url,
        auth=track_auth,
        json=data
    )

    return response.status_code == 200
```

### 2. Event Tracking

```python
# Track custom event
def track_event(customer_id, event_name, event_data=None):
    url = f'{TRACK_API_URL}/customers/{customer_id}/events'

    data = {
        'name': event_name,
        'data': event_data or {},
        'timestamp': int(datetime.now().timestamp())
    }

    response = requests.post(
        url,
        auth=track_auth,
        json=data
    )

    return response.status_code == 200

# Track anonymous event
def track_anonymous_event(event_name, event_data=None):
    url = f'{TRACK_API_URL}/events'

    data = {
        'name': event_name,
        'data': event_data or {},
        'timestamp': int(datetime.now().timestamp())
    }

    response = requests.post(
        url,
        auth=track_auth,
        json=data
    )

    return response.status_code == 200

# Example: Track product view
track_event(
    'user_12345',
    'product_viewed',
    {
        'product_id': 'SKU-999',
        'product_name': 'Premium Widget',
        'price': 99.99,
        'category': 'Electronics',
        'url': 'https://store.com/products/premium-widget'
    }
)

# Track purchase
track_event(
    'user_12345',
    'purchase',
    {
        'order_id': 'ORDER-123',
        'total': 249.97,
        'items': [
            {'id': 'SKU-999', 'name': 'Premium Widget', 'price': 99.99, 'quantity': 2},
            {'id': 'SKU-111', 'name': 'Accessory', 'price': 49.99, 'quantity': 1}
        ],
        'currency': 'USD'
    }
)

# Track page view
track_event(
    'user_12345',
    'page_view',
    {
        'url': 'https://example.com/pricing',
        'title': 'Pricing Page',
        'referrer': 'https://google.com'
    }
)
```

### 3. Transactional Messaging

```python
# Send transactional email
def send_transactional_email(transactional_message_id, recipient, message_data):
    url = f'{APP_API_URL}/send/email'

    data = {
        'transactional_message_id': transactional_message_id,
        'to': recipient,
        'identifiers': {
            'email': recipient
        },
        'message_data': message_data
    }

    response = requests.post(
        url,
        headers=app_headers,
        json=data
    )

    return response.json()

# Send transactional push notification
def send_transactional_push(transactional_message_id, customer_id, message_data):
    url = f'{APP_API_URL}/send/push'

    data = {
        'transactional_message_id': transactional_message_id,
        'identifiers': {
            'id': customer_id
        },
        'message_data': message_data
    }

    response = requests.post(
        url,
        headers=app_headers,
        json=data
    )

    return response.json()

# Example: Send order confirmation
send_transactional_email(
    '1',  # Transactional message ID
    'customer@example.com',
    {
        'order_number': 'ORDER-12345',
        'order_total': '$99.99',
        'items': [
            {'name': 'Product A', 'quantity': 2, 'price': '$49.99'}
        ],
        'shipping_address': '123 Main St, City, State 12345',
        'estimated_delivery': 'Jan 20, 2025'
    }
)

# Send password reset
send_transactional_email(
    '2',  # Password reset message ID
    'user@example.com',
    {
        'reset_link': 'https://example.com/reset?token=abc123',
        'expires_in': '24 hours'
    }
)
```

### 4. Campaign Management

```python
# Trigger broadcast campaign
def trigger_broadcast(broadcast_id, data=None, recipients=None):
    url = f'{APP_API_URL}/campaigns/{broadcast_id}/triggers'

    payload = {}

    if data:
        payload['data'] = data

    if recipients:
        payload['recipients'] = recipients

    response = requests.post(
        url,
        headers=app_headers,
        json=payload
    )

    return response.json()

# Get campaign details
def get_campaign(campaign_id):
    url = f'{APP_API_URL}/campaigns/{campaign_id}'

    response = requests.get(url, headers=app_headers)
    return response.json()

# Get campaign metrics
def get_campaign_metrics(campaign_id):
    url = f'{APP_API_URL}/campaigns/{campaign_id}/metrics'

    response = requests.get(url, headers=app_headers)
    return response.json()

# List campaigns
def list_campaigns():
    url = f'{APP_API_URL}/campaigns'

    response = requests.get(url, headers=app_headers)
    return response.json()

# Example: Trigger flash sale campaign
trigger_broadcast(
    '123',  # Broadcast ID
    data={
        'sale_name': 'Flash Sale',
        'discount_percentage': 30,
        'end_time': '2025-12-31T23:59:59Z'
    }
)

# Get campaign performance
metrics = get_campaign_metrics('123')
print(f"Campaign Metrics:")
print(f"  Recipients: {metrics.get('recipients', 0)}")
print(f"  Opened: {metrics.get('opened', 0)}")
print(f"  Clicked: {metrics.get('clicked', 0)}")
print(f"  Conversions: {metrics.get('converted', 0)}")
```

### 5. Customer Journeys and Workflows

```python
# Add customer to workflow
def add_to_workflow(workflow_id, customer_id, data=None):
    url = f'{TRACK_API_URL}/customers/{customer_id}/events'

    event_data = {
        'name': f'workflow_{workflow_id}_trigger',
        'data': data or {},
        'timestamp': int(datetime.now().timestamp())
    }

    response = requests.post(
        url,
        auth=track_auth,
        json=event_data
    )

    return response.status_code == 200

# Manual trigger via API-triggered campaign
def trigger_campaign_for_customer(campaign_id, customer_id, data=None):
    url = f'{APP_API_URL}/campaigns/{campaign_id}/triggers'

    payload = {
        'recipients': {
            'ids': [customer_id]
        }
    }

    if data:
        payload['data'] = data

    response = requests.post(
        url,
        headers=app_headers,
        json=payload
    )

    return response.json()

# Example: Trigger onboarding workflow
add_to_workflow(
    'onboarding_v2',
    'user_12345',
    {
        'signup_date': datetime.now().isoformat(),
        'source': 'website',
        'plan': 'trial'
    }
)

# Trigger win-back campaign
trigger_campaign_for_customer(
    '456',  # Win-back campaign ID
    'user_inactive_789',
    {
        'days_inactive': 90,
        'last_purchase_date': '2024-09-15',
        'special_offer': '50% off first purchase'
    }
)
```

### 6. Segments and Attributes

```python
# Create manual segment
def create_manual_segment(name, description=None):
    url = f'{APP_API_URL}/segments'

    data = {
        'segment': {
            'name': name,
            'description': description or '',
            'type': 'manual'
        }
    }

    response = requests.post(
        url,
        headers=app_headers,
        json=data
    )

    return response.json()

# List segments
def list_segments():
    url = f'{APP_API_URL}/segments'

    response = requests.get(url, headers=app_headers)
    return response.json()

# Get segment membership
def get_segment_membership(segment_id):
    url = f'{APP_API_URL}/segments/{segment_id}/membership'

    response = requests.get(url, headers=app_headers)
    return response.json()

# Update customer attributes
def update_customer_attributes(customer_id, attributes):
    return identify_customer(customer_id, attributes)

# Example: Create and populate VIP segment
vip_segment = create_manual_segment(
    'VIP Customers',
    'High-value customers with $1000+ lifetime spend'
)

segment_id = vip_segment['segment']['id']

# Add VIP customers
vip_customer_ids = ['user_001', 'user_002', 'user_003']
add_to_segment(segment_id, vip_customer_ids)

# Update customer with VIP attributes
update_customer_attributes(
    'user_001',
    {
        'vip_status': True,
        'vip_since': int(datetime.now().timestamp()),
        'lifetime_value': 1250.00
    }
)
```

### 7. Reporting and Analytics

```python
import pandas as pd

# Get customer activities
def get_customer_activities(customer_id, start=None, end=None):
    url = f'{APP_API_URL}/customers/{customer_id}/activities'

    params = {}
    if start:
        params['start'] = start
    if end:
        params['end'] = end

    response = requests.get(
        url,
        headers=app_headers,
        params=params
    )

    return response.json()

# Get message metrics
def get_message_metrics(message_id, metric_type='opened'):
    url = f'{APP_API_URL}/messages/{message_id}/metrics'

    params = {'type': metric_type}

    response = requests.get(
        url,
        headers=app_headers,
        params=params
    )

    return response.json()

# Export customer data
def export_customer_data(segment_id=None):
    url = f'{APP_API_URL}/exports/customers'

    data = {}
    if segment_id:
        data['segment_id'] = segment_id

    response = requests.post(
        url,
        headers=app_headers,
        json=data
    )

    return response.json()

# Analyze campaign performance
def analyze_campaigns():
    campaigns = list_campaigns()

    performance_data = []

    for campaign in campaigns.get('campaigns', []):
        campaign_id = campaign['id']
        metrics = get_campaign_metrics(campaign_id)

        performance_data.append({
            'campaign_name': campaign.get('name'),
            'campaign_id': campaign_id,
            'created': campaign.get('created_at'),
            'sent': metrics.get('sent', 0),
            'delivered': metrics.get('delivered', 0),
            'opened': metrics.get('opened', 0),
            'clicked': metrics.get('clicked', 0),
            'converted': metrics.get('converted', 0)
        })

    df = pd.DataFrame(performance_data)

    # Calculate rates
    df['delivery_rate'] = (df['delivered'] / df['sent'] * 100).round(2)
    df['open_rate'] = (df['opened'] / df['delivered'] * 100).round(2)
    df['click_rate'] = (df['clicked'] / df['delivered'] * 100).round(2)
    df['conversion_rate'] = (df['converted'] / df['delivered'] * 100).round(2)

    return df

# Example usage
performance_report = analyze_campaigns()
print("Top Performing Campaigns:")
print(performance_report.sort_values('conversion_rate', ascending=False).head(10))
```

## Installation

```bash
uv pip install requests pandas
```

## Authentication

Get your credentials from Customer.io:
1. Log in to Customer.io
2. Go to Settings > API Credentials
3. Note your Site ID and API Key (for Track API)
4. Create an App API Key (for App API)

```python
# Track API (Basic Auth)
from requests.auth import HTTPBasicAuth
track_auth = HTTPBasicAuth(SITE_ID, API_KEY)

# App API (Bearer Token)
app_headers = {
    'Authorization': f'Bearer {APP_API_KEY}',
    'Content-Type': 'application/json'
}
```

## Quick Start

```python
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

SITE_ID = 'your-site-id'
API_KEY = 'your-api-key'
TRACK_API_URL = 'https://track.customer.io/api/v1'

track_auth = HTTPBasicAuth(SITE_ID, API_KEY)

# Identify customer
customer_data = {
    'email': 'newuser@example.com',
    'first_name': 'John',
    'created_at': int(datetime.now().timestamp())
}

response = requests.put(
    f'{TRACK_API_URL}/customers/user_12345',
    auth=track_auth,
    json=customer_data
)

print(f"Customer identified: {response.status_code == 200}")

# Track event
event_data = {
    'name': 'signed_up',
    'data': {'source': 'website'},
    'timestamp': int(datetime.now().timestamp())
}

response = requests.post(
    f'{TRACK_API_URL}/customers/user_12345/events',
    auth=track_auth,
    json=event_data
)

print(f"Event tracked: {response.status_code == 200}")
```

## Key Features Reference

- **Customers**: Profile management, attributes, segments
- **Events**: Behavioral tracking, custom events
- **Campaigns**: Broadcast and triggered messages
- **Workflows**: Visual journey builder automations
- **Transactional**: System-generated emails/push/SMS
- **Segments**: Dynamic and manual audience targeting
- **A/B Testing**: Message and journey optimization
- **Reporting**: Analytics and customer activity tracking

## References

- [Customer.io API Documentation](https://customer.io/docs/api/)
- [Track API Reference](https://customer.io/docs/api/track/)
- [App API Reference](https://customer.io/docs/api/app/)
- [Transactional API](https://customer.io/docs/transactional-api/)
- [Journeys Guide](https://customer.io/docs/journeys/)

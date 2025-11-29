---
name: iterable
description: "Iterable growth marketing platform. Cross-channel campaigns, workflow automation, A/B testing, user segmentation, dynamic content, mobile messaging."
---

# Iterable Integration

## Overview

Iterable is a growth marketing platform that enables cross-channel customer engagement through email, push, SMS, and in-app messaging. This skill covers using the Iterable API for user management, campaign creation, workflow automation, and analytics.

## When to Use This Skill

- Growth marketing campaigns across channels
- User lifecycle automation
- Personalized messaging at scale
- A/B testing and experimentation
- Mobile app engagement
- Dynamic content personalization
- Customer journey orchestration
- Marketing analytics and attribution

## Core Capabilities

### 1. User Profile Management

```python
import requests
import json

# Iterable API configuration
API_KEY = 'your-api-key'
BASE_URL = 'https://api.iterable.com/api'

headers = {
    'Api-Key': API_KEY,
    'Content-Type': 'application/json'
}

# Update user profile
def update_user(email, data_fields):
    url = f'{BASE_URL}/users/update'

    data = {
        'email': email,
        'dataFields': data_fields,
        'mergeNestedObjects': True
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example usage
user = update_user(
    'user@example.com',
    {
        'firstName': 'John',
        'lastName': 'Doe',
        'signupSource': 'website',
        'subscriptionTier': 'premium',
        'totalPurchases': 5,
        'lifetimeValue': 499.95
    }
)

print(f"User updated: {user}")

# Bulk update users
def bulk_update_users(users):
    url = f'{BASE_URL}/users/bulkUpdate'

    data = {
        'users': [
            {
                'email': user['email'],
                'dataFields': user['data']
            }
            for user in users
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Delete user
def delete_user(email):
    url = f'{BASE_URL}/users/delete'

    params = {'email': email}

    response = requests.delete(url, headers=headers, params=params)
    return response.json()

# Get user by email
def get_user(email):
    url = f'{BASE_URL}/users/{email}'

    response = requests.get(url, headers=headers)
    return response.json()

# Example: Batch update
users_to_update = [
    {
        'email': 'user1@example.com',
        'data': {'segment': 'active', 'last_login': '2025-01-15'}
    },
    {
        'email': 'user2@example.com',
        'data': {'segment': 'churned', 'last_login': '2024-06-01'}
    }
]

bulk_result = bulk_update_users(users_to_update)
print(f"Bulk update completed: {bulk_result}")
```

### 2. Event Tracking

```python
from datetime import datetime

# Track custom event
def track_event(email, event_name, data_fields=None):
    url = f'{BASE_URL}/events/track'

    data = {
        'email': email,
        'eventName': event_name,
        'dataFields': data_fields or {},
        'createdAt': int(datetime.now().timestamp() * 1000)
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Track purchase
def track_purchase(email, items, total, order_id):
    url = f'{BASE_URL}/commerce/trackPurchase'

    data = {
        'user': {'email': email},
        'items': items,
        'total': total,
        'id': order_id,
        'createdAt': int(datetime.now().timestamp() * 1000)
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Update cart
def update_cart(email, items):
    url = f'{BASE_URL}/commerce/updateCart'

    data = {
        'user': {'email': email},
        'items': items
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example: Track product view
track_event(
    'customer@example.com',
    'Product Viewed',
    {
        'productId': 'SKU-12345',
        'productName': 'Premium Widget',
        'price': 99.99,
        'category': 'Electronics'
    }
)

# Track purchase event
purchase = track_purchase(
    'customer@example.com',
    items=[
        {
            'id': 'SKU-12345',
            'name': 'Premium Widget',
            'price': 99.99,
            'quantity': 2
        },
        {
            'id': 'SKU-67890',
            'name': 'Widget Accessory',
            'price': 19.99,
            'quantity': 1
        }
    ],
    total=219.97,
    order_id='ORDER-98765'
)

print(f"Purchase tracked: {purchase}")

# Track cart abandonment
update_cart(
    'customer@example.com',
    items=[
        {
            'id': 'SKU-11111',
            'name': 'Abandoned Product',
            'price': 49.99,
            'quantity': 1
        }
    ]
)
```

### 3. Campaign Management

```python
# Send triggered campaign
def send_triggered_campaign(campaign_id, email, data_fields=None):
    url = f'{BASE_URL}/email/target'

    data = {
        'campaignId': campaign_id,
        'recipientEmail': email,
        'dataFields': data_fields or {}
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Send campaign to list
def send_campaign_to_list(campaign_id, list_id, data_fields=None):
    url = f'{BASE_URL}/campaigns/create'

    data = {
        'campaignId': campaign_id,
        'listIds': [list_id],
        'dataFields': data_fields or {},
        'sendAt': datetime.now().isoformat()
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Get campaign metrics
def get_campaign_metrics(campaign_id, start_date=None, end_date=None):
    url = f'{BASE_URL}/campaigns/metrics'

    params = {
        'campaignId': campaign_id
    }

    if start_date:
        params['startDateTime'] = start_date
    if end_date:
        params['endDateTime'] = end_date

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# List campaigns
def list_campaigns():
    url = f'{BASE_URL}/campaigns'

    response = requests.get(url, headers=headers)
    return response.json()

# Example: Send personalized email
send_triggered_campaign(
    123456,  # Campaign ID
    'customer@example.com',
    {
        'firstName': 'John',
        'discountCode': 'SAVE20',
        'recommendedProducts': ['SKU-111', 'SKU-222', 'SKU-333']
    }
)

# Get campaign performance
metrics = get_campaign_metrics(123456)
print(f"Campaign Metrics:")
print(f"  Sent: {metrics.get('emailSendCount', 0)}")
print(f"  Opens: {metrics.get('uniqueOpenCount', 0)}")
print(f"  Clicks: {metrics.get('uniqueClickCount', 0)}")
```

### 4. Lists and Segmentation

```python
# Subscribe user to list
def subscribe_to_list(list_id, subscribers):
    url = f'{BASE_URL}/lists/subscribe'

    data = {
        'listId': list_id,
        'subscribers': [
            {'email': sub['email'], 'dataFields': sub.get('data', {})}
            for sub in subscribers
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Unsubscribe from list
def unsubscribe_from_list(list_id, subscribers):
    url = f'{BASE_URL}/lists/unsubscribe'

    data = {
        'listId': list_id,
        'subscribers': [
            {'email': email} for email in subscribers
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Get lists
def get_lists():
    url = f'{BASE_URL}/lists'

    response = requests.get(url, headers=headers)
    return response.json()

# Get list users
def get_list_users(list_id):
    url = f'{BASE_URL}/lists/getUsers'

    params = {'listId': list_id}

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Example: Add users to VIP list
vip_subscribers = [
    {
        'email': 'vip1@example.com',
        'data': {'vip_tier': 'gold', 'join_date': '2025-01-01'}
    },
    {
        'email': 'vip2@example.com',
        'data': {'vip_tier': 'platinum', 'join_date': '2024-12-15'}
    }
]

subscribe_to_list(12345, vip_subscribers)

# Get all lists
lists = get_lists()
for list_item in lists.get('lists', []):
    print(f"List: {list_item['name']} (ID: {list_item['id']})")
```

### 5. Workflow Automation

```python
# Trigger workflow
def trigger_workflow(workflow_id, email, data_fields=None):
    url = f'{BASE_URL}/workflows/triggerWorkflow'

    data = {
        'workflowId': workflow_id,
        'email': email,
        'dataFields': data_fields or {}
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Get workflow details
def get_workflow(workflow_id):
    url = f'{BASE_URL}/workflows/{workflow_id}'

    response = requests.get(url, headers=headers)
    return response.json()

# Example: Trigger onboarding workflow
trigger_workflow(
    67890,  # Workflow ID
    'newuser@example.com',
    {
        'signupDate': datetime.now().isoformat(),
        'referralSource': 'google',
        'accountType': 'trial'
    }
)

# Trigger abandoned cart workflow
trigger_workflow(
    11111,  # Abandoned cart workflow ID
    'shopper@example.com',
    {
        'cartItems': ['SKU-123', 'SKU-456'],
        'cartTotal': 149.98,
        'abandonedAt': datetime.now().isoformat()
    }
)
```

### 6. Templates and Content

```python
# Get email template
def get_template(template_id):
    url = f'{BASE_URL}/templates/email/get'

    params = {'templateId': template_id}

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Update email template
def update_template(template_id, html_content, subject=None):
    url = f'{BASE_URL}/templates/email/update'

    data = {
        'templateId': template_id,
        'html': html_content
    }

    if subject:
        data['subject'] = subject

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Upsert template (create or update)
def upsert_template(client_template_id, name, html_content, subject):
    url = f'{BASE_URL}/templates/email/upsert'

    data = {
        'clientTemplateId': client_template_id,
        'name': name,
        'html': html_content,
        'subject': subject,
        'fromName': 'Your Company',
        'fromEmail': 'marketing@example.com'
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example: Create personalized template
template_html = """
<html>
<body>
    <h1>Hello {{firstName}}!</h1>
    <p>Thanks for being a {{subscriptionTier}} member.</p>
    <p>Your exclusive offer: {{discountCode}}</p>
</body>
</html>
"""

upsert_template(
    'welcome_email_v2',
    'Welcome Email V2',
    template_html,
    'Welcome to {{companyName}}, {{firstName}}!'
)
```

### 7. Analytics and Reporting

```python
import pandas as pd

# Get export data
def export_data(data_type, range_start, range_end):
    url = f'{BASE_URL}/export/data.json'

    params = {
        'dataTypeName': data_type,
        'range': 'Today',
        'startDateTime': range_start,
        'endDateTime': range_end
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Get user events
def get_user_events(email):
    url = f'{BASE_URL}/events/{email}'

    response = requests.get(url, headers=headers)
    return response.json()

# Get campaign analytics
def get_all_campaign_analytics():
    campaigns = list_campaigns()

    analytics = []

    for campaign in campaigns.get('campaigns', []):
        campaign_id = campaign['id']
        metrics = get_campaign_metrics(campaign_id)

        analytics.append({
            'campaign_name': campaign['name'],
            'campaign_id': campaign_id,
            'sent': metrics.get('emailSendCount', 0),
            'opens': metrics.get('uniqueOpenCount', 0),
            'clicks': metrics.get('uniqueClickCount', 0),
            'bounces': metrics.get('emailBounceCount', 0),
            'unsubscribes': metrics.get('unsubscribeCount', 0)
        })

    df = pd.DataFrame(analytics)

    # Calculate rates
    df['open_rate'] = (df['opens'] / df['sent'] * 100).round(2)
    df['click_rate'] = (df['clicks'] / df['sent'] * 100).round(2)

    return df

# Get revenue attribution
def get_revenue_report(start_date, end_date):
    purchase_data = export_data('purchase', start_date, end_date)

    revenue_by_campaign = {}

    for purchase in purchase_data.get('data', []):
        campaign_id = purchase.get('campaignId')
        total = purchase.get('total', 0)

        if campaign_id not in revenue_by_campaign:
            revenue_by_campaign[campaign_id] = 0

        revenue_by_campaign[campaign_id] += total

    return revenue_by_campaign

# Example usage
campaign_performance = get_all_campaign_analytics()
print("Top Performing Campaigns:")
print(campaign_performance.sort_values('click_rate', ascending=False).head(10))

# Get user journey
user_events = get_user_events('customer@example.com')
print(f"\nUser Events: {len(user_events.get('events', []))}")
```

## Installation

```bash
uv pip install requests pandas
```

## Authentication

Get your API key from Iterable:
1. Log in to Iterable
2. Go to Integrations > API Keys
3. Create a new API Key with appropriate permissions

```python
headers = {
    'Api-Key': API_KEY,
    'Content-Type': 'application/json'
}
```

## Quick Start

```python
import requests

API_KEY = 'your-api-key'
BASE_URL = 'https://api.iterable.com/api'

headers = {
    'Api-Key': API_KEY,
    'Content-Type': 'application/json'
}

# Create/update user
user_data = {
    'email': 'newuser@example.com',
    'dataFields': {
        'firstName': 'Jane',
        'lastName': 'Smith',
        'signupDate': '2025-01-15'
    }
}

response = requests.post(
    f'{BASE_URL}/users/update',
    headers=headers,
    json=user_data
)

print(f"User created: {response.json()}")

# Track event
event_data = {
    'email': 'newuser@example.com',
    'eventName': 'App Installed'
}

response = requests.post(
    f'{BASE_URL}/events/track',
    headers=headers,
    json=event_data
)

print(f"Event tracked: {response.json()}")
```

## Key Features Reference

- **Users**: Profile management, custom fields, preferences
- **Events**: Behavioral tracking, custom events, commerce
- **Campaigns**: One-time sends, A/B testing
- **Workflows**: Multi-step automation journeys
- **Lists**: Static user segments
- **Templates**: Email and push templates
- **In-App**: Mobile in-app messaging
- **Push**: Mobile push notifications
- **SMS**: Text message campaigns
- **Experiments**: A/B and multivariate testing

## References

- [Iterable API Documentation](https://api.iterable.com/api/docs)
- [API Authentication](https://support.iterable.com/hc/en-us/articles/360043464871)
- [Event Tracking Guide](https://support.iterable.com/hc/en-us/articles/208013936)
- [Workflow API](https://api.iterable.com/api/docs#workflows)
- [Commerce API](https://api.iterable.com/api/docs#commerce)

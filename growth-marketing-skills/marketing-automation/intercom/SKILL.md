---
name: intercom
description: "Intercom customer messaging platform. Live chat, chatbots, help desk, product tours, email campaigns, customer engagement, support automation."
---

# Intercom Integration

## Overview

Intercom is a customer messaging platform that combines live chat, chatbots, help desk, and marketing automation. This skill covers using the Intercom API for user management, messaging, conversations, and customer engagement automation.

## When to Use This Skill

- Live chat and customer support
- In-app messaging and product tours
- Chatbot automation
- Customer onboarding workflows
- Help desk and ticket management
- Targeted email campaigns
- User segmentation and engagement
- Product announcements

## Core Capabilities

### 1. Contact (User and Lead) Management

```python
import requests
import json

# Intercom API configuration
ACCESS_TOKEN = 'your-access-token'
BASE_URL = 'https://api.intercom.io'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Create or update contact
def create_or_update_contact(email=None, user_id=None, role='user', custom_attributes=None):
    url = f'{BASE_URL}/contacts'

    data = {
        'role': role  # 'user' or 'lead'
    }

    if email:
        data['email'] = email
    if user_id:
        data['external_id'] = user_id
    if custom_attributes:
        data['custom_attributes'] = custom_attributes

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example usage
contact = create_or_update_contact(
    email='customer@example.com',
    user_id='user_12345',
    role='user',
    custom_attributes={
        'plan': 'premium',
        'signup_date': '2025-01-15',
        'total_purchases': 5,
        'lifetime_value': 499.95
    }
)

print(f"Contact created: {contact['id']}")

# Get contact by ID
def get_contact(contact_id):
    url = f'{BASE_URL}/contacts/{contact_id}'

    response = requests.get(url, headers=headers)
    return response.json()

# Search contacts
def search_contacts(query):
    url = f'{BASE_URL}/contacts/search'

    data = {'query': query}

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Delete contact
def delete_contact(contact_id):
    url = f'{BASE_URL}/contacts/{contact_id}'

    response = requests.delete(url, headers=headers)
    return response.status_code == 200

# Example: Search for premium users
premium_users = search_contacts({
    'field': 'custom_attributes.plan',
    'operator': '=',
    'value': 'premium'
})

print(f"Found {len(premium_users.get('data', []))} premium users")

# Update contact
def update_contact(contact_id, updates):
    url = f'{BASE_URL}/contacts/{contact_id}'

    response = requests.put(url, headers=headers, json=updates)
    return response.json()
```

### 2. Messaging and Conversations

```python
# Send message to user
def send_message_to_user(user_id, message_type='email', subject=None, body=None, template_id=None):
    url = f'{BASE_URL}/messages'

    data = {
        'message_type': message_type,  # 'email' or 'inapp'
        'from': {
            'type': 'admin',
            'id': 'your-admin-id'
        },
        'to': {
            'type': 'user',
            'id': user_id
        }
    }

    if template_id:
        data['template_id'] = template_id
    else:
        if message_type == 'email':
            data['subject'] = subject
        data['body'] = body

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Create conversation
def create_conversation(from_user_id, body):
    url = f'{BASE_URL}/conversations'

    data = {
        'from': {
            'type': 'user',
            'id': from_user_id
        },
        'body': body
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Reply to conversation
def reply_to_conversation(conversation_id, message_type, body, admin_id):
    url = f'{BASE_URL}/conversations/{conversation_id}/reply'

    data = {
        'message_type': message_type,  # 'comment', 'note'
        'type': 'admin',
        'admin_id': admin_id,
        'body': body
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Get conversation
def get_conversation(conversation_id):
    url = f'{BASE_URL}/conversations/{conversation_id}'

    response = requests.get(url, headers=headers)
    return response.json()

# Search conversations
def search_conversations(query):
    url = f'{BASE_URL}/conversations/search'

    data = {'query': query}

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example: Send onboarding email
send_message_to_user(
    user_id='user_12345',
    message_type='email',
    subject='Welcome to Our Platform!',
    body='<p>Hi there! We\'re excited to have you on board.</p>'
)

# Example: Get open conversations
open_conversations = search_conversations({
    'field': 'state',
    'operator': '=',
    'value': 'open'
})
```

### 3. Events and Activity Tracking

```python
from datetime import datetime

# Track event
def track_event(user_id, event_name, metadata=None):
    url = f'{BASE_URL}/events'

    data = {
        'event_name': event_name,
        'created_at': int(datetime.now().timestamp()),
        'user_id': user_id
    }

    if metadata:
        data['metadata'] = metadata

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example: Track product events
track_event(
    'user_12345',
    'product_viewed',
    metadata={
        'product_id': 'SKU-999',
        'product_name': 'Premium Widget',
        'price': 99.99,
        'category': 'Electronics'
    }
)

track_event(
    'user_12345',
    'purchase_completed',
    metadata={
        'order_id': 'ORDER-456',
        'total': 249.97,
        'items': ['SKU-999', 'SKU-111']
    }
)

# Track custom events
track_event(
    'user_12345',
    'feature_used',
    metadata={
        'feature_name': 'export_report',
        'usage_count': 5
    }
)
```

### 4. Tags and Segments

```python
# Add tag to contact
def tag_contact(contact_id, tag_name):
    url = f'{BASE_URL}/contacts/{contact_id}/tags'

    data = {
        'id': tag_name
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Remove tag from contact
def untag_contact(contact_id, tag_id):
    url = f'{BASE_URL}/contacts/{contact_id}/tags/{tag_id}'

    response = requests.delete(url, headers=headers)
    return response.status_code == 200

# List all tags
def list_tags():
    url = f'{BASE_URL}/tags'

    response = requests.get(url, headers=headers)
    return response.json()

# Create segment
def create_segment(name, predicates):
    url = f'{BASE_URL}/segments'

    data = {
        'name': name,
        'predicates': predicates
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example: Tag high-value customers
tag_contact('contact_id_123', 'vip')
tag_contact('contact_id_123', 'high-value')

# Create engaged users segment
engaged_segment = create_segment(
    'Engaged Users',
    [
        {
            'attribute': 'custom_attributes.total_purchases',
            'comparison': '>',
            'value': 3,
            'type': 'integer'
        }
    ]
)
```

### 5. Articles and Help Center

```python
# Create article
def create_article(title, body, author_id):
    url = f'{BASE_URL}/articles'

    data = {
        'title': title,
        'body': body,
        'author_id': author_id,
        'state': 'published'
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Get article
def get_article(article_id):
    url = f'{BASE_URL}/articles/{article_id}'

    response = requests.get(url, headers=headers)
    return response.json()

# List articles
def list_articles():
    url = f'{BASE_URL}/articles'

    response = requests.get(url, headers=headers)
    return response.json()

# Update article
def update_article(article_id, updates):
    url = f'{BASE_URL}/articles/{article_id}'

    response = requests.put(url, headers=headers, json=updates)
    return response.json()

# Example: Create help article
article = create_article(
    title='How to Get Started',
    body='<h2>Getting Started</h2><p>Follow these steps...</p>',
    author_id='admin_123'
)
```

### 6. Data Attributes and Custom Fields

```python
# Create data attribute
def create_data_attribute(name, model, data_type):
    url = f'{BASE_URL}/data_attributes'

    data = {
        'name': name,
        'model': model,  # 'contact', 'company', 'conversation'
        'data_type': data_type,  # 'string', 'integer', 'float', 'boolean', 'date'
        'description': f'{name} custom field'
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# List data attributes
def list_data_attributes():
    url = f'{BASE_URL}/data_attributes'

    response = requests.get(url, headers=headers)
    return response.json()

# Example: Create custom fields
create_data_attribute('subscription_tier', 'contact', 'string')
create_data_attribute('lifetime_value', 'contact', 'float')
create_data_attribute('trial_end_date', 'contact', 'date')
```

### 7. Campaigns and Broadcasts

```python
# Note: Campaigns are typically managed through the UI
# But you can trigger them via events and contact updates

# Trigger campaign via contact update
def trigger_campaign_via_attribute(contact_id, trigger_attribute, trigger_value):
    # Update contact with triggering attribute
    return update_contact(
        contact_id,
        {
            'custom_attributes': {
                trigger_attribute: trigger_value
            }
        }
    )

# Example: Trigger welcome campaign
trigger_campaign_via_attribute(
    'contact_123',
    'onboarding_stage',
    'welcome_email_sent'
)

# Send targeted message to segment
def send_segment_message(segment_id, message_template_id):
    # Get segment members
    segment_contacts = search_contacts({
        'field': 'segment_id',
        'operator': '=',
        'value': segment_id
    })

    # Send message to each
    results = []
    for contact in segment_contacts.get('data', []):
        result = send_message_to_user(
            contact['id'],
            message_type='email',
            template_id=message_template_id
        )
        results.append(result)

    return results
```

### 8. Analytics and Reporting

```python
import pandas as pd

# Get contact counts by attribute
def get_contact_stats():
    # Search for different segments
    stats = {}

    # Count by plan type
    plans = ['free', 'premium', 'enterprise']

    for plan in plans:
        contacts = search_contacts({
            'field': 'custom_attributes.plan',
            'operator': '=',
            'value': plan
        })

        stats[plan] = len(contacts.get('data', []))

    return stats

# Get conversation metrics
def get_conversation_metrics():
    # Get conversations by state
    states = ['open', 'closed', 'snoozed']

    metrics = {}

    for state in states:
        convos = search_conversations({
            'field': 'state',
            'operator': '=',
            'value': state
        })

        metrics[state] = len(convos.get('conversations', []))

    return metrics

# Example usage
contact_stats = get_contact_stats()
print(f"Contact Distribution:")
for plan, count in contact_stats.items():
    print(f"  {plan}: {count}")

conversation_metrics = get_conversation_metrics()
print(f"\nConversation Metrics:")
for state, count in conversation_metrics.items():
    print(f"  {state}: {count}")
```

## Installation

```bash
uv pip install requests pandas
```

## Authentication

Get your access token from Intercom:
1. Log in to Intercom
2. Go to Settings > Developers > Developer Hub
3. Create or select an app
4. Copy the Access Token

```python
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}
```

## Quick Start

```python
import requests

ACCESS_TOKEN = 'your-access-token'
BASE_URL = 'https://api.intercom.io'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Create contact
contact_data = {
    'role': 'user',
    'email': 'newuser@example.com',
    'custom_attributes': {
        'plan': 'trial',
        'signup_date': '2025-01-15'
    }
}

response = requests.post(
    f'{BASE_URL}/contacts',
    headers=headers,
    json=contact_data
)

contact = response.json()
print(f"Contact created: {contact['id']}")

# Track event
event_data = {
    'event_name': 'signed_up',
    'user_id': contact['id'],
    'created_at': 1737158400  # Unix timestamp
}

response = requests.post(
    f'{BASE_URL}/events',
    headers=headers,
    json=event_data
)

print(f"Event tracked: {response.status_code == 202}")
```

## Key Features Reference

- **Contacts**: Users and leads with custom attributes
- **Conversations**: Chat, email, and support tickets
- **Messages**: Targeted in-app and email messages
- **Events**: Behavioral tracking and triggers
- **Tags**: Contact categorization
- **Segments**: Dynamic audience targeting
- **Articles**: Help center content
- **Data Attributes**: Custom fields
- **Inbox**: Team collaboration on conversations
- **Bots**: Automated chat workflows

## References

- [Intercom API Documentation](https://developers.intercom.com/docs/references/rest-api/)
- [Contacts API](https://developers.intercom.com/docs/references/rest-api/api.intercom.io/Contacts/)
- [Conversations API](https://developers.intercom.com/docs/references/rest-api/api.intercom.io/Conversations/)
- [Events API](https://developers.intercom.com/docs/references/rest-api/api.intercom.io/Events/)
- [Messages API](https://developers.intercom.com/docs/references/rest-api/api.intercom.io/Messages/)

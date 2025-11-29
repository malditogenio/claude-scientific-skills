---
name: activecampaign
description: "ActiveCampaign email marketing automation. CRM, email campaigns, marketing automation, lead scoring, segmentation, site tracking, sales automation."
---

# ActiveCampaign Integration

## Overview

ActiveCampaign is a customer experience automation platform combining email marketing, CRM, and sales automation. This skill covers using the ActiveCampaign API for contact management, campaign creation, automation workflows, and analytics.

## When to Use This Skill

- Email marketing automation
- CRM and contact management
- Lead scoring and qualification
- Sales pipeline automation
- Customer segmentation
- Behavioral email triggers
- Site and event tracking
- Marketing attribution

## Core Capabilities

### 1. Contact Management

```python
import requests
import json

# ActiveCampaign API configuration
API_URL = 'https://youracccount.api-us1.com'  # Replace with your account URL
API_KEY = 'your-api-key'

headers = {
    'Api-Token': API_KEY,
    'Content-Type': 'application/json'
}

# Create or update contact
def create_contact(email, first_name=None, last_name=None, phone=None, field_values=None):
    url = f'{API_URL}/api/3/contact/sync'

    data = {
        'contact': {
            'email': email,
            'firstName': first_name or '',
            'lastName': last_name or '',
            'phone': phone or ''
        }
    }

    if field_values:
        data['contact']['fieldValues'] = field_values

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example usage
contact = create_contact(
    email='customer@example.com',
    first_name='John',
    last_name='Doe',
    phone='+1234567890',
    field_values=[
        {'field': '1', 'value': 'premium'},  # Custom field: subscription tier
        {'field': '2', 'value': '1250.50'}   # Custom field: lifetime value
    ]
)

print(f"Contact created: {contact}")

# Get contact by email
def get_contact(email):
    url = f'{API_URL}/api/3/contacts'

    params = {'email': email}

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Update contact
def update_contact(contact_id, updates):
    url = f'{API_URL}/api/3/contacts/{contact_id}'

    data = {'contact': updates}

    response = requests.put(url, headers=headers, json=data)
    return response.json()

# Delete contact
def delete_contact(contact_id):
    url = f'{API_URL}/api/3/contacts/{contact_id}'

    response = requests.delete(url, headers=headers)
    return response.status_code == 200

# Add contact to list
def add_contact_to_list(contact_id, list_id, status='1'):
    url = f'{API_URL}/api/3/contactLists'

    data = {
        'contactList': {
            'list': list_id,
            'contact': contact_id,
            'status': status  # 1 = active, 2 = unsubscribed
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()
```

### 2. Tags and Segmentation

```python
# Add tag to contact
def add_tag_to_contact(contact_id, tag_id):
    url = f'{API_URL}/api/3/contactTags'

    data = {
        'contactTag': {
            'contact': contact_id,
            'tag': tag_id
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Create tag
def create_tag(tag_name, description=None):
    url = f'{API_URL}/api/3/tags'

    data = {
        'tag': {
            'tag': tag_name,
            'tagType': 'contact',
            'description': description or ''
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Get all tags
def get_tags():
    url = f'{API_URL}/api/3/tags'

    response = requests.get(url, headers=headers)
    return response.json()

# Remove tag from contact
def remove_tag_from_contact(contact_tag_id):
    url = f'{API_URL}/api/3/contactTags/{contact_tag_id}'

    response = requests.delete(url, headers=headers)
    return response.status_code == 200

# Example: Tag high-value customers
vip_tag = create_tag('VIP Customer', 'Lifetime value > $1000')
add_tag_to_contact(contact_id=123, tag_id=vip_tag['tag']['id'])
```

### 3. Campaign Management

```python
# Create campaign
def create_campaign(name, campaign_type, subject, html_content, list_ids):
    url = f'{API_URL}/api/3/campaigns'

    data = {
        'campaign': {
            'type': campaign_type,  # 'single', 'recurring', 'split', 'responder', 'reminder', 'special', 'activerss', 'text'
            'name': name,
            'sdate': None,  # Schedule date (ISO format) or None for draft
            'status': 0,  # 0 = draft, 1 = scheduled, 2 = sending, 3 = paused, 4 = stopped, 5 = completed
            'public': 1,
            'tracklinks': 'all',
            'trackreads': '1',
            'htmlcontent': html_content,
            'p[{list_id}]': '1' for list_id in list_ids
        }
    }

    # Set subject and other message details
    data['message'] = {
        'subject': subject,
        'fromemail': 'marketing@example.com',
        'fromname': 'Marketing Team',
        'reply2': 'noreply@example.com'
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Send campaign
def send_campaign(campaign_id):
    url = f'{API_URL}/api/3/campaigns/{campaign_id}'

    data = {
        'campaign': {
            'status': 1  # Set to scheduled/sending
        }
    }

    response = requests.put(url, headers=headers, json=data)
    return response.json()

# Get campaign report
def get_campaign_report(campaign_id):
    url = f'{API_URL}/api/3/campaigns/{campaign_id}'

    response = requests.get(url, headers=headers)
    return response.json()
```

### 4. Marketing Automation

```python
# Add contact to automation
def add_contact_to_automation(contact_id, automation_id):
    url = f'{API_URL}/api/3/contactAutomations'

    data = {
        'contactAutomation': {
            'contact': contact_id,
            'automation': automation_id
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Get automation details
def get_automation(automation_id):
    url = f'{API_URL}/api/3/automations/{automation_id}'

    response = requests.get(url, headers=headers)
    return response.json()

# List all automations
def list_automations():
    url = f'{API_URL}/api/3/automations'

    response = requests.get(url, headers=headers)
    return response.json()

# Remove contact from automation
def remove_contact_from_automation(contact_automation_id):
    url = f'{API_URL}/api/3/contactAutomations/{contact_automation_id}'

    response = requests.delete(url, headers=headers)
    return response.status_code == 200

# Example: Enroll new users in onboarding automation
automations = list_automations()

onboarding_automation = next(
    (auto for auto in automations.get('automations', [])
     if 'onboarding' in auto['name'].lower()),
    None
)

if onboarding_automation:
    add_contact_to_automation(
        contact_id=123,
        automation_id=onboarding_automation['id']
    )
```

### 5. Deals and CRM

```python
# Create deal
def create_deal(title, contact_id, pipeline_id, stage_id, value, currency='usd'):
    url = f'{API_URL}/api/3/deals'

    data = {
        'deal': {
            'title': title,
            'contact': contact_id,
            'value': value,
            'currency': currency,
            'group': pipeline_id,
            'stage': stage_id,
            'status': 0  # 0 = open, 1 = won, 2 = lost
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Update deal stage
def update_deal(deal_id, stage_id=None, status=None, value=None):
    url = f'{API_URL}/api/3/deals/{deal_id}'

    updates = {}
    if stage_id:
        updates['stage'] = stage_id
    if status is not None:
        updates['status'] = status
    if value:
        updates['value'] = value

    data = {'deal': updates}

    response = requests.put(url, headers=headers, json=data)
    return response.json()

# Get all deals
def get_deals():
    url = f'{API_URL}/api/3/deals'

    all_deals = []
    offset = 0
    limit = 100

    while True:
        params = {'limit': limit, 'offset': offset}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        deals = data.get('deals', [])
        all_deals.extend(deals)

        if len(deals) < limit:
            break

        offset += limit

    return all_deals

# Example: Create sales opportunity
deal = create_deal(
    title='Enterprise License - Acme Corp',
    contact_id=123,
    pipeline_id=1,
    stage_id=2,  # Qualification stage
    value=50000
)

print(f"Deal created: {deal['deal']['id']}")
```

### 6. Event Tracking

```python
# Track event
def track_event(event_name, event_data, contact_email=None, contact_id=None):
    url = f'{API_URL}/api/3/eventTrackingEvents'

    data = {
        'eventTrackingEvent': {
            'event': event_name,
            'eventdata': event_data
        }
    }

    if contact_email:
        data['eventTrackingEvent']['email'] = contact_email
    if contact_id:
        data['eventTrackingEvent']['contact'] = contact_id

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Track site visit
def track_site_visit(contact_email, url, title=None):
    return track_event(
        'visit',
        json.dumps({
            'url': url,
            'title': title or url
        }),
        contact_email=contact_email
    )

# Example: Track product view
track_event(
    'product_view',
    json.dumps({
        'product_id': 'SKU-123',
        'product_name': 'Premium Widget',
        'price': 99.99,
        'category': 'Electronics'
    }),
    contact_email='customer@example.com'
)

# Track purchase
track_event(
    'purchase',
    json.dumps({
        'order_id': 'ORDER-456',
        'total': 249.97,
        'items': [
            {'id': 'SKU-123', 'quantity': 2, 'price': 99.99}
        ]
    }),
    contact_email='customer@example.com'
)
```

### 7. Lead Scoring

```python
# Add score to contact
def add_score_to_contact(contact_id, score_value):
    url = f'{API_URL}/api/3/contactScores'

    data = {
        'contactScore': {
            'contact': contact_id,
            'score': score_value
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Get contact score
def get_contact_score(contact_id):
    url = f'{API_URL}/api/3/contacts/{contact_id}/scoreValues'

    response = requests.get(url, headers=headers)
    return response.json()

# Calculate and update lead score
def calculate_lead_score(contact_id):
    # Get contact details
    contact_data = get_contact_by_id(contact_id)

    score = 0

    # Score based on engagement
    if contact_data.get('opened_count', 0) > 10:
        score += 20
    if contact_data.get('clicked_count', 0) > 5:
        score += 30

    # Score based on profile completeness
    if contact_data.get('firstName'):
        score += 10
    if contact_data.get('phone'):
        score += 10

    # Update score
    return add_score_to_contact(contact_id, score)

# Helper function
def get_contact_by_id(contact_id):
    url = f'{API_URL}/api/3/contacts/{contact_id}'
    response = requests.get(url, headers=headers)
    return response.json().get('contact', {})
```

### 8. Analytics and Reporting

```python
import pandas as pd

# Get campaign stats
def get_all_campaign_stats():
    url = f'{API_URL}/api/3/campaigns'

    response = requests.get(url, headers=headers)
    campaigns = response.json().get('campaigns', [])

    stats = []

    for campaign in campaigns:
        stats.append({
            'name': campaign.get('name'),
            'status': campaign.get('status'),
            'sent': campaign.get('total_sent', 0),
            'opens': campaign.get('unique_opens', 0),
            'clicks': campaign.get('unique_clicks', 0),
            'unsubscribes': campaign.get('unsubscribes', 0),
            'bounces': campaign.get('bounces', 0)
        })

    df = pd.DataFrame(stats)

    # Calculate rates
    df['open_rate'] = (df['opens'] / df['sent'] * 100).round(2)
    df['click_rate'] = (df['clicks'] / df['sent'] * 100).round(2)

    return df

# Get contact activity
def get_contact_activities(contact_id):
    url = f'{API_URL}/api/3/contacts/{contact_id}/contactActivities'

    response = requests.get(url, headers=headers)
    return response.json()

# Example usage
campaign_performance = get_all_campaign_stats()
print("Campaign Performance:")
print(campaign_performance.sort_values('open_rate', ascending=False).head(10))
```

## Installation

```bash
uv pip install requests pandas
```

## Authentication

Get your API credentials from ActiveCampaign:
1. Log in to ActiveCampaign
2. Go to Settings > Developer
3. Copy your API URL and API Key

```python
headers = {
    'Api-Token': API_KEY,
    'Content-Type': 'application/json'
}
```

## Quick Start

```python
import requests

API_URL = 'https://youracccount.api-us1.com'
API_KEY = 'your-api-key'

headers = {
    'Api-Token': API_KEY,
    'Content-Type': 'application/json'
}

# Create contact
contact_data = {
    'contact': {
        'email': 'newuser@example.com',
        'firstName': 'Jane',
        'lastName': 'Smith'
    }
}

response = requests.post(
    f'{API_URL}/api/3/contact/sync',
    headers=headers,
    json=contact_data
)

contact = response.json()
print(f"Contact created: {contact['contact']['id']}")

# Add to list
list_data = {
    'contactList': {
        'list': 1,  # List ID
        'contact': contact['contact']['id'],
        'status': 1
    }
}

response = requests.post(
    f'{API_URL}/api/3/contactLists',
    headers=headers,
    json=list_data
)

print(f"Added to list: {response.json()}")
```

## Key Features Reference

- **Contacts**: CRM database, custom fields, activity tracking
- **Lists**: Static contact segmentation
- **Tags**: Dynamic categorization
- **Campaigns**: Email marketing sends
- **Automations**: Behavioral workflows
- **Deals**: Sales pipeline management
- **Event Tracking**: Behavioral data collection
- **Lead Scoring**: Automated qualification
- **Site Tracking**: Website visitor tracking

## References

- [ActiveCampaign API Documentation](https://developers.activecampaign.com/reference/overview)
- [API v3 Reference](https://developers.activecampaign.com/reference/api-overview)
- [Webhooks Guide](https://developers.activecampaign.com/reference/webhooks)
- [Event Tracking](https://developers.activecampaign.com/reference/event-tracking-overview)

---
name: drift
description: "Drift conversational marketing platform. Live chat, chatbots, meeting scheduler, ABM, sales automation, conversation intelligence, email integration."
---

# Drift Integration

## Overview

Drift is a conversational marketing and sales platform that uses chat, chatbots, and video to connect with website visitors and qualified leads. This skill covers using the Drift API for contact management, conversation tracking, and automation.

## When to Use This Skill

- Conversational marketing and sales
- Live chat with website visitors
- Chatbot automation and qualification
- Meeting scheduling automation
- Account-based marketing (ABM)
- Lead routing and assignment
- Conversation analytics
- CRM integration

## Core Capabilities

### 1. Contact Management

```python
import requests
import json

# Drift API configuration
ACCESS_TOKEN = 'your-access-token'
BASE_URL = 'https://drifting.drift.com'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

# Create contact
def create_contact(email, attributes=None):
    url = f'{BASE_URL}/contacts'

    data = {
        'attributes': {
            'email': email,
            **(attributes or {})
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Update contact
def update_contact(contact_id, attributes):
    url = f'{BASE_URL}/contacts/{contact_id}'

    data = {
        'attributes': attributes
    }

    response = requests.patch(url, headers=headers, json=data)
    return response.json()

# Get contact
def get_contact(contact_id):
    url = f'{BASE_URL}/contacts/{contact_id}'

    response = requests.get(url, headers=headers)
    return response.json()

# List contacts
def list_contacts(email=None, limit=100):
    url = f'{BASE_URL}/contacts'

    params = {'limit': limit}

    if email:
        params['email'] = email

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Example usage
contact = create_contact(
    'lead@example.com',
    attributes={
        'name': 'John Doe',
        'phone': '+1234567890',
        'company': 'Acme Corp',
        'job_title': 'VP Marketing'
    }
)

print(f"Contact created: {contact['data']['id']}")

# Update contact with custom attributes
update_contact(
    contact['data']['id'],
    {
        'lifecycle_stage': 'qualified',
        'lead_score': 85,
        'product_interest': 'Enterprise Plan'
    }
)
```

### 2. Conversations

```python
# Get conversation
def get_conversation(conversation_id):
    url = f'{BASE_URL}/conversations/{conversation_id}'

    response = requests.get(url, headers=headers)
    return response.json()

# List conversations
def list_conversations(contact_id=None, status=None, limit=50):
    url = f'{BASE_URL}/conversations'

    params = {'limit': limit}

    if contact_id:
        params['contact_id'] = contact_id
    if status:
        params['status'] = status  # 'open', 'closed', 'pending'

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Get conversation messages
def get_conversation_messages(conversation_id):
    url = f'{BASE_URL}/conversations/{conversation_id}/messages'

    response = requests.get(url, headers=headers)
    return response.json()

# Send message in conversation
def send_message(conversation_id, message_body, author_type='user'):
    url = f'{BASE_URL}/conversations/{conversation_id}/messages'

    data = {
        'body': message_body,
        'type': 'chat',
        'author': {
            'type': author_type  # 'user', 'bot', 'contact'
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example: Get contact's conversations
contact_convos = list_conversations(contact_id=12345, status='open')

for convo in contact_convos.get('data', []):
    print(f"Conversation {convo['id']}: {convo.get('subject', 'No subject')}")

# Get conversation transcript
messages = get_conversation_messages(conversation_id=67890)
for msg in messages.get('data', []):
    print(f"{msg['author']['type']}: {msg['body']}")
```

### 3. Meetings and Scheduling

```python
# Create meeting
def create_meeting(contact_id, start_time, end_time, meeting_type='demo'):
    url = f'{BASE_URL}/meetings'

    data = {
        'contactId': contact_id,
        'startTime': start_time,  # ISO 8601 format
        'endTime': end_time,
        'type': meeting_type,
        'status': 'scheduled'
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Get meeting
def get_meeting(meeting_id):
    url = f'{BASE_URL}/meetings/{meeting_id}'

    response = requests.get(url, headers=headers)
    return response.json()

# List meetings
def list_meetings(contact_id=None, status=None):
    url = f'{BASE_URL}/meetings'

    params = {}

    if contact_id:
        params['contactId'] = contact_id
    if status:
        params['status'] = status  # 'scheduled', 'completed', 'cancelled'

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Update meeting
def update_meeting(meeting_id, updates):
    url = f'{BASE_URL}/meetings/{meeting_id}'

    response = requests.patch(url, headers=headers, json=updates)
    return response.json()

# Example: Schedule demo meeting
meeting = create_meeting(
    contact_id=12345,
    start_time='2025-01-20T14:00:00Z',
    end_time='2025-01-20T14:30:00Z',
    meeting_type='demo'
)

print(f"Meeting scheduled: {meeting['data']['id']}")
```

### 4. Playbooks (Chatbot Flows)

```python
# Get playbook
def get_playbook(playbook_id):
    url = f'{BASE_URL}/playbooks/{playbook_id}'

    response = requests.get(url, headers=headers)
    return response.json()

# List playbooks
def list_playbooks():
    url = f'{BASE_URL}/playbooks'

    response = requests.get(url, headers=headers)
    return response.json()

# Get playbook metrics
def get_playbook_metrics(playbook_id, start_date=None, end_date=None):
    url = f'{BASE_URL}/playbooks/{playbook_id}/metrics'

    params = {}
    if start_date:
        params['startDate'] = start_date
    if end_date:
        params['endDate'] = end_date

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Example: Get active playbooks
playbooks = list_playbooks()

for playbook in playbooks.get('data', []):
    if playbook.get('status') == 'active':
        print(f"Active Playbook: {playbook['name']}")

        # Get metrics
        metrics = get_playbook_metrics(playbook['id'])
        print(f"  Conversations: {metrics.get('conversationCount', 0)}")
        print(f"  Meetings Booked: {metrics.get('meetingsBooked', 0)}")
```

### 5. Users and Teams

```python
# List users
def list_users():
    url = f'{BASE_URL}/users'

    response = requests.get(url, headers=headers)
    return response.json()

# Get user
def get_user(user_id):
    url = f'{BASE_URL}/users/{user_id}'

    response = requests.get(url, headers=headers)
    return response.json()

# Get user availability
def get_user_availability(user_id, start_date, end_date):
    url = f'{BASE_URL}/users/{user_id}/availability'

    params = {
        'startDate': start_date,
        'endDate': end_date
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Example: Get sales team members
users = list_users()

sales_team = [
    user for user in users.get('data', [])
    if user.get('role') == 'sales_rep'
]

print(f"Sales team members: {len(sales_team)}")
```

### 6. Events and Webhooks

```python
# Track custom event
def track_event(contact_id, event_name, event_data=None):
    url = f'{BASE_URL}/events'

    data = {
        'contactId': contact_id,
        'event': event_name,
        'properties': event_data or {}
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example: Track product events
track_event(
    contact_id=12345,
    event_name='product_demo_viewed',
    event_data={
        'demo_type': 'video',
        'duration_seconds': 180,
        'product': 'Enterprise Plan'
    }
)

track_event(
    contact_id=12345,
    event_name='pricing_page_viewed',
    event_data={
        'plan_viewed': 'Enterprise',
        'annual_selected': True
    }
)

# Track engagement
track_event(
    contact_id=12345,
    event_name='whitepaper_downloaded',
    event_data={
        'title': 'ROI of Conversational Marketing',
        'format': 'pdf'
    }
)
```

### 7. Account-Based Marketing (ABM)

```python
# Create account
def create_account(domain, attributes=None):
    url = f'{BASE_URL}/accounts'

    data = {
        'domain': domain,
        'attributes': attributes or {}
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Update account
def update_account(account_id, attributes):
    url = f'{BASE_URL}/accounts/{account_id}'

    data = {
        'attributes': attributes
    }

    response = requests.patch(url, headers=headers, json=data)
    return response.json()

# Get account
def get_account(account_id):
    url = f'{BASE_URL}/accounts/{account_id}'

    response = requests.get(url, headers=headers)
    return response.json()

# List accounts
def list_accounts(limit=100):
    url = f'{BASE_URL}/accounts'

    params = {'limit': limit}

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Example: Create target account
account = create_account(
    'acmecorp.com',
    attributes={
        'name': 'Acme Corporation',
        'employees': 5000,
        'industry': 'Technology',
        'target_tier': 'Enterprise'
    }
)

print(f"Account created: {account['data']['id']}")
```

### 8. Analytics and Reporting

```python
import pandas as pd
from datetime import datetime, timedelta

# Get conversation analytics
def get_conversation_analytics(start_date, end_date):
    conversations = list_conversations()

    analytics = {
        'total_conversations': len(conversations.get('data', [])),
        'by_status': {},
        'avg_response_time': []
    }

    for convo in conversations.get('data', []):
        status = convo.get('status', 'unknown')
        analytics['by_status'][status] = analytics['by_status'].get(status, 0) + 1

    return analytics

# Get meeting analytics
def get_meeting_analytics():
    meetings = list_meetings()

    analytics = {
        'total_meetings': len(meetings.get('data', [])),
        'by_status': {},
        'by_type': {}
    }

    for meeting in meetings.get('data', []):
        status = meeting.get('status', 'unknown')
        meeting_type = meeting.get('type', 'unknown')

        analytics['by_status'][status] = analytics['by_status'].get(status, 0) + 1
        analytics['by_type'][meeting_type] = analytics['by_type'].get(meeting_type, 0) + 1

    return analytics

# Generate performance report
def generate_performance_report():
    # Get playbooks and metrics
    playbooks = list_playbooks()

    report_data = []

    for playbook in playbooks.get('data', []):
        metrics = get_playbook_metrics(playbook['id'])

        report_data.append({
            'playbook_name': playbook['name'],
            'status': playbook.get('status'),
            'conversations': metrics.get('conversationCount', 0),
            'meetings_booked': metrics.get('meetingsBooked', 0),
            'qualified_leads': metrics.get('qualifiedLeads', 0)
        })

    df = pd.DataFrame(report_data)

    # Calculate conversion rates
    df['booking_rate'] = (df['meetings_booked'] / df['conversations'] * 100).round(2)
    df['qualification_rate'] = (df['qualified_leads'] / df['conversations'] * 100).round(2)

    return df

# Example usage
convo_analytics = get_conversation_analytics(
    datetime.now() - timedelta(days=30),
    datetime.now()
)

print(f"Conversation Analytics (Last 30 Days):")
print(f"  Total: {convo_analytics['total_conversations']}")
print(f"  By Status: {convo_analytics['by_status']}")

performance_report = generate_performance_report()
print("\nPlaybook Performance:")
print(performance_report)
```

## Installation

```bash
uv pip install requests pandas
```

## Authentication

Get your access token from Drift:
1. Log in to Drift
2. Go to Settings > App Settings > Dev Settings
3. Create or copy your OAuth Access Token

```python
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}
```

## Quick Start

```python
import requests

ACCESS_TOKEN = 'your-access-token'
BASE_URL = 'https://drifting.drift.com'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

# Create contact
contact_data = {
    'attributes': {
        'email': 'newlead@example.com',
        'name': 'Jane Smith',
        'company': 'Tech Startup'
    }
}

response = requests.post(
    f'{BASE_URL}/contacts',
    headers=headers,
    json=contact_data
)

contact = response.json()
print(f"Contact created: {contact['data']['id']}")

# Track event
event_data = {
    'contactId': contact['data']['id'],
    'event': 'demo_requested',
    'properties': {
        'product': 'Enterprise'
    }
}

response = requests.post(
    f'{BASE_URL}/events',
    headers=headers,
    json=event_data
)

print(f"Event tracked: {response.status_code == 200}")
```

## Key Features Reference

- **Contacts**: Lead and customer database
- **Conversations**: Chat transcripts and history
- **Meetings**: Automated scheduling
- **Playbooks**: Chatbot workflows and qualification
- **Accounts**: ABM target accounts
- **Events**: Custom event tracking
- **Users**: Team member management
- **Webhooks**: Real-time notifications
- **Video**: Video messaging and meetings
- **Email**: Email integration and tracking

## References

- [Drift API Documentation](https://devdocs.drift.com/)
- [Contacts API](https://devdocs.drift.com/docs/contact-model)
- [Conversations API](https://devdocs.drift.com/docs/conversation-overview)
- [Playbooks API](https://devdocs.drift.com/docs/playbook-model)
- [Webhooks](https://devdocs.drift.com/docs/webhook-events-1)

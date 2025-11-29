---
name: mailchimp
description: "Mailchimp email marketing platform. Audience management, email campaigns, automation workflows, templates, analytics, A/B testing, landing pages."
---

# Mailchimp Integration

## Overview

Mailchimp is a leading email marketing and automation platform. This skill covers using the Mailchimp API to manage audiences, create campaigns, build automations, track analytics, and integrate email marketing into your growth stack.

## When to Use This Skill

- Managing email subscribers and audiences
- Creating and sending email campaigns
- Building email automation workflows
- Designing email templates
- A/B testing email content
- Tracking email performance metrics
- Creating landing pages
- Segmenting audiences for targeted campaigns

## Core Capabilities

### 1. Audience Management

```python
import requests
import json
from hashlib import md5

# Mailchimp API configuration
API_KEY = 'your-api-key'
SERVER_PREFIX = 'us19'  # Extract from your API key (text after the dash)
BASE_URL = f'https://{SERVER_PREFIX}.api.mailchimp.com/3.0'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Get all lists/audiences
def get_lists():
    url = f'{BASE_URL}/lists'

    response = requests.get(url, headers=headers)
    return response.json()

# Add subscriber to list
def add_subscriber(list_id, email, merge_fields=None, tags=None):
    url = f'{BASE_URL}/lists/{list_id}/members'

    data = {
        'email_address': email,
        'status': 'subscribed',
        'merge_fields': merge_fields or {},
        'tags': tags or []
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Update subscriber
def update_subscriber(list_id, email, merge_fields=None, tags=None):
    subscriber_hash = md5(email.lower().encode()).hexdigest()
    url = f'{BASE_URL}/lists/{list_id}/members/{subscriber_hash}'

    data = {
        'merge_fields': merge_fields or {},
        'tags': tags or []
    }

    response = requests.patch(url, headers=headers, json=data)
    return response.json()

# Example usage
lists = get_lists()
list_id = lists['lists'][0]['id']

# Add new subscriber
new_subscriber = add_subscriber(
    list_id,
    'newuser@example.com',
    merge_fields={
        'FNAME': 'John',
        'LNAME': 'Doe',
        'COMPANY': 'Acme Corp'
    },
    tags=['lead', 'webinar-signup']
)

print(f"Subscriber added: {new_subscriber['email_address']}")

# Batch subscribe
def batch_subscribe(list_id, subscribers):
    url = f'{BASE_URL}/lists/{list_id}'

    operations = []
    for sub in subscribers:
        operations.append({
            'method': 'POST',
            'path': f'/lists/{list_id}/members',
            'body': json.dumps({
                'email_address': sub['email'],
                'status': 'subscribed',
                'merge_fields': sub.get('merge_fields', {})
            })
        })

    batch_url = f'{BASE_URL}/batches'
    batch_data = {'operations': operations}

    response = requests.post(batch_url, headers=headers, json=batch_data)
    return response.json()

# Example batch upload
subscribers_to_add = [
    {
        'email': 'user1@example.com',
        'merge_fields': {'FNAME': 'Alice', 'LNAME': 'Smith'}
    },
    {
        'email': 'user2@example.com',
        'merge_fields': {'FNAME': 'Bob', 'LNAME': 'Johnson'}
    }
]

batch_result = batch_subscribe(list_id, subscribers_to_add)
print(f"Batch operation ID: {batch_result['id']}")
```

### 2. Email Campaign Creation

```python
# Create email campaign
def create_campaign(list_id, subject, from_name, reply_to, template_id=None):
    url = f'{BASE_URL}/campaigns'

    campaign_data = {
        'type': 'regular',
        'recipients': {
            'list_id': list_id
        },
        'settings': {
            'subject_line': subject,
            'from_name': from_name,
            'reply_to': reply_to,
            'title': f'Campaign - {subject}'
        }
    }

    if template_id:
        campaign_data['settings']['template_id'] = template_id

    response = requests.post(url, headers=headers, json=campaign_data)
    return response.json()

# Set campaign content
def set_campaign_content(campaign_id, html_content):
    url = f'{BASE_URL}/campaigns/{campaign_id}/content'

    data = {
        'html': html_content
    }

    response = requests.put(url, headers=headers, json=data)
    return response.json()

# Send test email
def send_test_email(campaign_id, test_emails):
    url = f'{BASE_URL}/campaigns/{campaign_id}/actions/test'

    data = {
        'test_emails': test_emails,
        'send_type': 'html'
    }

    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 204

# Schedule campaign
def schedule_campaign(campaign_id, schedule_time):
    url = f'{BASE_URL}/campaigns/{campaign_id}/actions/schedule'

    data = {
        'schedule_time': schedule_time  # ISO 8601 format
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Send campaign immediately
def send_campaign(campaign_id):
    url = f'{BASE_URL}/campaigns/{campaign_id}/actions/send'

    response = requests.post(url, headers=headers)
    return response.status_code == 204

# Example: Create and send campaign
campaign = create_campaign(
    list_id,
    subject='Your Monthly Newsletter',
    from_name='Marketing Team',
    reply_to='marketing@example.com'
)

html_content = """
<html>
<body>
    <h1>Hello *|FNAME|*!</h1>
    <p>Welcome to our monthly newsletter.</p>
    <a href="https://example.com">Visit our site</a>
</body>
</html>
"""

set_campaign_content(campaign['id'], html_content)
send_test_email(campaign['id'], ['test@example.com'])

# Send or schedule
send_campaign(campaign['id'])
# Or schedule for later
# schedule_campaign(campaign['id'], '2025-12-01T10:00:00Z')
```

### 3. Campaign Analytics

```python
import pandas as pd

# Get campaign report
def get_campaign_report(campaign_id):
    url = f'{BASE_URL}/reports/{campaign_id}'

    response = requests.get(url, headers=headers)
    return response.json()

# Get email activity for campaign
def get_email_activity(campaign_id):
    url = f'{BASE_URL}/reports/{campaign_id}/email-activity'

    all_activity = []
    params = {'count': 1000, 'offset': 0}

    while True:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        all_activity.extend(data.get('emails', []))

        if len(data.get('emails', [])) < params['count']:
            break

        params['offset'] += params['count']

    return all_activity

# Get click details
def get_click_details(campaign_id):
    url = f'{BASE_URL}/reports/{campaign_id}/click-details'

    response = requests.get(url, headers=headers)
    return response.json()

# Analyze campaign performance
def analyze_campaign_performance(campaign_id):
    report = get_campaign_report(campaign_id)

    stats = {
        'emails_sent': report['emails_sent'],
        'opens': report['opens']['opens_total'],
        'unique_opens': report['opens']['unique_opens'],
        'clicks': report['clicks']['clicks_total'],
        'unique_clicks': report['clicks']['unique_clicks'],
        'unsubscribes': report['unsubscribed'],
        'open_rate': report['opens']['open_rate'] * 100,
        'click_rate': report['clicks']['click_rate'] * 100,
        'unsubscribe_rate': (report['unsubscribed'] / report['emails_sent'] * 100) if report['emails_sent'] > 0 else 0
    }

    return stats

# Get performance across all campaigns
def get_all_campaigns_performance():
    url = f'{BASE_URL}/reports'

    params = {'count': 100, 'offset': 0}
    all_reports = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        all_reports.extend(data.get('reports', []))

        if len(data.get('reports', [])) < params['count']:
            break

        params['offset'] += params['count']

    # Create DataFrame for analysis
    performance_data = []
    for report in all_reports:
        performance_data.append({
            'campaign_title': report.get('campaign_title'),
            'send_time': report.get('send_time'),
            'emails_sent': report.get('emails_sent'),
            'opens': report.get('opens', {}).get('unique_opens', 0),
            'clicks': report.get('clicks', {}).get('unique_clicks', 0),
            'open_rate': report.get('opens', {}).get('open_rate', 0) * 100,
            'click_rate': report.get('clicks', {}).get('click_rate', 0) * 100
        })

    df = pd.DataFrame(performance_data)
    return df

# Example usage
campaign_stats = analyze_campaign_performance('campaign_id_here')
print(f"Campaign Performance:")
print(f"  Open Rate: {campaign_stats['open_rate']:.2f}%")
print(f"  Click Rate: {campaign_stats['click_rate']:.2f}%")

all_campaigns = get_all_campaigns_performance()
print(f"\nAverage Performance Across All Campaigns:")
print(f"  Avg Open Rate: {all_campaigns['open_rate'].mean():.2f}%")
print(f"  Avg Click Rate: {all_campaigns['click_rate'].mean():.2f}%")
```

### 4. Audience Segmentation

```python
# Create segment
def create_segment(list_id, name, conditions):
    url = f'{BASE_URL}/lists/{list_id}/segments'

    segment_data = {
        'name': name,
        'static_segment': [],
        'options': {
            'match': 'all',  # or 'any'
            'conditions': conditions
        }
    }

    response = requests.post(url, headers=headers, json=segment_data)
    return response.json()

# Example: Create engaged subscribers segment
engaged_segment = create_segment(
    list_id,
    name='Highly Engaged Subscribers',
    conditions=[
        {
            'condition_type': 'EmailClient',
            'field': 'email_client',
            'op': 'open'
        },
        {
            'condition_type': 'Automation',
            'field': 'automation_id',
            'op': 'any',
            'value': 'automation_id_here'
        }
    ]
)

# Create segment based on member rating
high_value_segment = create_segment(
    list_id,
    name='High Value Subscribers',
    conditions=[
        {
            'condition_type': 'StaticSegment',
            'field': 'static_segment',
            'op': 'static_is',
            'value': 4  # 4-5 star rating
        }
    ]
)

# Get segment members
def get_segment_members(list_id, segment_id):
    url = f'{BASE_URL}/lists/{list_id}/segments/{segment_id}/members'

    all_members = []
    params = {'count': 1000, 'offset': 0}

    while True:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        all_members.extend(data.get('members', []))

        if len(data.get('members', [])) < params['count']:
            break

        params['offset'] += params['count']

    return all_members

# Send campaign to segment
def create_segment_campaign(list_id, segment_id, subject, content):
    url = f'{BASE_URL}/campaigns'

    campaign_data = {
        'type': 'regular',
        'recipients': {
            'list_id': list_id,
            'segment_opts': {
                'saved_segment_id': segment_id
            }
        },
        'settings': {
            'subject_line': subject,
            'from_name': 'Your Company',
            'reply_to': 'marketing@example.com'
        }
    }

    response = requests.post(url, headers=headers, json=campaign_data)
    campaign = response.json()

    # Set content
    set_campaign_content(campaign['id'], content)

    return campaign
```

### 5. Automation Workflows

```python
# Get automation workflows
def get_automations():
    url = f'{BASE_URL}/automations'

    response = requests.get(url, headers=headers)
    return response.json()

# Get automation details
def get_automation(workflow_id):
    url = f'{BASE_URL}/automations/{workflow_id}'

    response = requests.get(url, headers=headers)
    return response.json()

# Add subscriber to automation
def add_to_automation(workflow_id, email_id, email_address):
    url = f'{BASE_URL}/automations/{workflow_id}/emails/{email_id}/queue'

    data = {
        'email_address': email_address
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Pause automation
def pause_automation(workflow_id):
    url = f'{BASE_URL}/automations/{workflow_id}/actions/pause-all-emails'

    response = requests.post(url, headers=headers)
    return response.status_code == 204

# Start automation
def start_automation(workflow_id):
    url = f'{BASE_URL}/automations/{workflow_id}/actions/start-all-emails'

    response = requests.post(url, headers=headers)
    return response.status_code == 204

# Get automation queue
def get_automation_queue(workflow_id):
    url = f'{BASE_URL}/automations/{workflow_id}/emails'

    response = requests.get(url, headers=headers)
    emails_data = response.json()

    queue_data = []
    for email in emails_data.get('emails', []):
        queue_url = f"{BASE_URL}/automations/{workflow_id}/emails/{email['id']}/queue"
        queue_response = requests.get(queue_url, headers=headers)
        queue_data.append({
            'email_id': email['id'],
            'email_title': email.get('settings', {}).get('title'),
            'queue': queue_response.json()
        })

    return queue_data

# Example usage
automations = get_automations()
print(f"Active automations: {len(automations.get('automations', []))}")

for automation in automations.get('automations', [])[:5]:
    print(f"  - {automation['settings']['title']}: {automation['status']}")
```

### 6. Tags and Contact Management

```python
# Add tags to subscriber
def add_tags(list_id, email, tags):
    subscriber_hash = md5(email.lower().encode()).hexdigest()
    url = f'{BASE_URL}/lists/{list_id}/members/{subscriber_hash}/tags'

    data = {
        'tags': [{'name': tag, 'status': 'active'} for tag in tags]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Remove tags from subscriber
def remove_tags(list_id, email, tags):
    subscriber_hash = md5(email.lower().encode()).hexdigest()
    url = f'{BASE_URL}/lists/{list_id}/members/{subscriber_hash}/tags'

    data = {
        'tags': [{'name': tag, 'status': 'inactive'} for tag in tags]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Get all tags for a list
def get_list_tags(list_id):
    url = f'{BASE_URL}/lists/{list_id}/tag-search'

    response = requests.get(url, headers=headers)
    return response.json()

# Get subscribers by tag
def get_subscribers_by_tag(list_id, tag_name):
    url = f'{BASE_URL}/lists/{list_id}/members'

    params = {
        'count': 1000,
        'offset': 0,
        'tags': tag_name
    }

    all_members = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        all_members.extend(data.get('members', []))

        if len(data.get('members', [])) < params['count']:
            break

        params['offset'] += params['count']

    return all_members

# Example: Tag management workflow
add_tags(list_id, 'user@example.com', ['premium', 'engaged', 'q4-2024'])

premium_users = get_subscribers_by_tag(list_id, 'premium')
print(f"Premium users count: {len(premium_users)}")
```

## Installation

```bash
# Using requests library
uv pip install requests pandas

# Or using official Mailchimp SDK
uv pip install mailchimp-marketing
```

## Authentication

Get your API key from Mailchimp:
1. Log in to Mailchimp
2. Go to Account > Extras > API Keys
3. Create a new API key
4. Note the server prefix (e.g., 'us19') from your API key

```python
# Using requests
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Using official SDK
import mailchimp_marketing as MailchimpMarketing

client = MailchimpMarketing.Client()
client.set_config({
    'api_key': 'your-api-key',
    'server': 'us19'  # Your server prefix
})
```

## Quick Start

```python
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

# Initialize client
client = MailchimpMarketing.Client()
client.set_config({
    'api_key': 'your-api-key',
    'server': 'us19'
})

# Get lists
try:
    response = client.lists.get_all_lists()
    list_id = response['lists'][0]['id']
    print(f"Using list: {response['lists'][0]['name']}")

    # Add subscriber
    member_info = {
        'email_address': 'newuser@example.com',
        'status': 'subscribed',
        'merge_fields': {
            'FNAME': 'John',
            'LNAME': 'Doe'
        }
    }

    response = client.lists.add_list_member(list_id, member_info)
    print(f"Subscriber added: {response['email_address']}")

except ApiClientError as error:
    print(f"Error: {error.text}")
```

## Key Features Reference

- **Audiences**: Subscriber lists, merge fields, tags
- **Campaigns**: Email creation, scheduling, A/B testing
- **Automations**: Triggered workflows, drip campaigns
- **Templates**: Pre-built and custom email designs
- **Reports**: Campaign analytics, engagement metrics
- **Segments**: Dynamic and static audience targeting
- **Landing Pages**: Lead capture pages
- **Forms**: Embedded signup forms

## References

- [Mailchimp API Documentation](https://mailchimp.com/developer/marketing/api/)
- [Python SDK](https://github.com/mailchimp/mailchimp-marketing-python)
- [API Playground](https://mailchimp.com/developer/tools/api-playground/)
- [Marketing Guides](https://mailchimp.com/developer/marketing/guides/)

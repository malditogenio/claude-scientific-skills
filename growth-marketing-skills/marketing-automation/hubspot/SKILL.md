---
name: hubspot
description: "HubSpot CRM and marketing automation platform. Contact management, email campaigns, lead scoring, workflows, analytics, sales pipeline, forms, landing pages."
---

# HubSpot Integration

## Overview

HubSpot is an all-in-one CRM, marketing automation, and sales platform. This skill covers using the HubSpot API to manage contacts, create email campaigns, build workflows, track analytics, and integrate with your marketing stack.

## When to Use This Skill

- Managing contacts and CRM data
- Creating and sending email campaigns
- Building marketing automation workflows
- Lead scoring and qualification
- Landing page and form creation
- Sales pipeline management
- Marketing analytics and attribution
- Integrating HubSpot with other tools

## Core Capabilities

### 1. Contact Management

```python
import requests
import json

# HubSpot API configuration
API_KEY = 'your-hubspot-api-key'
BASE_URL = 'https://api.hubapi.com'

# Create or update contact
def create_or_update_contact(email, properties):
    url = f'{BASE_URL}/contacts/v1/contact/createOrUpdate/email/{email}'

    data = {
        'properties': [
            {'property': key, 'value': value}
            for key, value in properties.items()
        ]
    }

    response = requests.post(
        url,
        params={'hapikey': API_KEY},
        json=data
    )

    return response.json()

# Example usage
contact = create_or_update_contact(
    'user@example.com',
    {
        'firstname': 'John',
        'lastname': 'Doe',
        'company': 'Acme Corp',
        'jobtitle': 'Marketing Director',
        'lifecyclestage': 'lead',
        'hs_lead_status': 'NEW'
    }
)

print(f"Contact created: {contact['vid']}")

# Get contact by email
def get_contact(email):
    url = f'{BASE_URL}/contacts/v1/contact/email/{email}/profile'

    response = requests.get(
        url,
        params={'hapikey': API_KEY}
    )

    return response.json()

# Batch update contacts
def batch_update_contacts(contacts_data):
    url = f'{BASE_URL}/contacts/v1/contact/batch/'

    response = requests.post(
        url,
        params={'hapikey': API_KEY},
        json=contacts_data
    )

    return response.json()

# Example: Update multiple contacts
batch_data = [
    {
        'email': 'user1@example.com',
        'properties': [
            {'property': 'lead_score', 'value': '85'},
            {'property': 'hs_lead_status', 'value': 'QUALIFIED'}
        ]
    },
    {
        'email': 'user2@example.com',
        'properties': [
            {'property': 'lead_score', 'value': '92'},
            {'property': 'hs_lead_status', 'value': 'QUALIFIED'}
        ]
    }
]

batch_update_contacts(batch_data)
```

### 2. Email Campaign Management

```python
# Using hubspot-api-client (recommended)
from hubspot import HubSpot
from hubspot.marketing.emails import ApiException

api_client = HubSpot(access_token='your-access-token')

# Create email campaign
def create_email_campaign(name, subject, html_content):
    try:
        email = api_client.marketing.emails.basic_api.create(
            marketing_email_create_request_params={
                'name': name,
                'subject': subject,
                'htmlBody': html_content,
                'emailType': 'BATCH_EMAIL',
                'campaign': 'Newsletter Campaign'
            }
        )
        return email
    except ApiException as e:
        print(f"Error creating email: {e}")

# Send test email
def send_test_email(email_id, test_email_address):
    api_client.marketing.emails.basic_api.send_test_email(
        email_id=email_id,
        test_email_address=test_email_address
    )

# Schedule email send
def schedule_email(email_id, send_datetime):
    api_client.marketing.emails.basic_api.schedule(
        email_id=email_id,
        send_time=send_datetime.isoformat()
    )

# Get email statistics
def get_email_stats(email_id):
    stats = api_client.marketing.emails.basic_api.get_email_stats(
        email_id=email_id
    )

    return {
        'sent': stats.counters.sent,
        'delivered': stats.counters.delivered,
        'opens': stats.counters.open,
        'clicks': stats.counters.click,
        'bounces': stats.counters.bounce,
        'unsubscribes': stats.counters.unsubscribed
    }

# Example usage
email = create_email_campaign(
    name='Monthly Newsletter - Jan 2025',
    subject='Your Monthly Marketing Insights',
    html_content='<html><body><h1>Hello!</h1><p>Content here</p></body></html>'
)

stats = get_email_stats(email.id)
print(f"Email performance: {stats}")
```

### 3. Marketing Automation Workflows

```python
# Create workflow enrollment via API
def enroll_contact_in_workflow(contact_id, workflow_id):
    url = f'{BASE_URL}/automation/v2/workflows/{workflow_id}/enrollments/contacts/{contact_id}'

    response = requests.post(
        url,
        params={'hapikey': API_KEY}
    )

    return response.json()

# Get workflow details
def get_workflow(workflow_id):
    url = f'{BASE_URL}/automation/v3/workflows/{workflow_id}'

    response = requests.get(
        url,
        params={'hapikey': API_KEY}
    )

    return response.json()

# List all workflows
def list_workflows():
    url = f'{BASE_URL}/automation/v3/workflows'

    response = requests.get(
        url,
        params={'hapikey': API_KEY}
    )

    return response.json()

# Unenroll contact from workflow
def unenroll_contact(contact_id, workflow_id):
    url = f'{BASE_URL}/automation/v2/workflows/{workflow_id}/enrollments/contacts/{contact_id}'

    response = requests.delete(
        url,
        params={'hapikey': API_KEY}
    )

    return response.status_code == 204

# Example: Enroll qualified leads in nurture workflow
qualified_leads = [123, 456, 789]  # Contact IDs
nurture_workflow_id = 12345

for contact_id in qualified_leads:
    result = enroll_contact_in_workflow(contact_id, nurture_workflow_id)
    print(f"Enrolled contact {contact_id}: {result}")
```

### 4. Deal and Pipeline Management

```python
# Create deal
def create_deal(deal_name, amount, pipeline_stage, contact_ids):
    url = f'{BASE_URL}/deals/v1/deal'

    data = {
        'properties': [
            {'name': 'dealname', 'value': deal_name},
            {'name': 'amount', 'value': amount},
            {'name': 'dealstage', 'value': pipeline_stage},
            {'name': 'pipeline', 'value': 'default'}
        ],
        'associations': {
            'associatedVids': contact_ids
        }
    }

    response = requests.post(
        url,
        params={'hapikey': API_KEY},
        json=data
    )

    return response.json()

# Update deal stage
def update_deal_stage(deal_id, new_stage):
    url = f'{BASE_URL}/deals/v1/deal/{deal_id}'

    data = {
        'properties': [
            {'name': 'dealstage', 'value': new_stage}
        ]
    }

    response = requests.put(
        url,
        params={'hapikey': API_KEY},
        json=data
    )

    return response.json()

# Get pipeline analytics
def get_pipeline_analytics():
    url = f'{BASE_URL}/deals/v1/deal/paged'

    all_deals = []
    params = {'hapikey': API_KEY, 'limit': 100}

    while True:
        response = requests.get(url, params=params)
        data = response.json()

        all_deals.extend(data.get('deals', []))

        if not data.get('hasMore'):
            break

        params['offset'] = data.get('offset')

    # Analyze by stage
    stage_analysis = {}
    for deal in all_deals:
        stage = next(
            (p['value'] for p in deal['properties'] if p['name'] == 'dealstage'),
            'unknown'
        )
        amount = float(next(
            (p['value'] for p in deal['properties'] if p['name'] == 'amount'),
            0
        ))

        if stage not in stage_analysis:
            stage_analysis[stage] = {'count': 0, 'total_value': 0}

        stage_analysis[stage]['count'] += 1
        stage_analysis[stage]['total_value'] += amount

    return stage_analysis

# Example usage
deal = create_deal(
    deal_name='Enterprise License - Acme Corp',
    amount='50000',
    pipeline_stage='qualifiedtobuy',
    contact_ids=[12345, 67890]
)

print(f"Deal created: {deal['dealId']}")

pipeline_stats = get_pipeline_analytics()
print(f"Pipeline breakdown: {pipeline_stats}")
```

### 5. Lead Scoring and Segmentation

```python
import pandas as pd

# Get contacts with specific properties
def get_contacts_for_scoring(properties_to_fetch):
    url = f'{BASE_URL}/contacts/v1/lists/all/contacts/all'

    params = {
        'hapikey': API_KEY,
        'count': 100,
        'property': properties_to_fetch
    }

    all_contacts = []

    while True:
        response = requests.get(url, params=params)
        data = response.json()

        all_contacts.extend(data.get('contacts', []))

        if not data.get('has-more'):
            break

        params['vidOffset'] = data.get('vid-offset')

    return all_contacts

# Calculate lead score
def calculate_lead_score(contact_data):
    score = 0

    # Email engagement
    if contact_data.get('hs_email_open', 0) > 5:
        score += 20
    if contact_data.get('hs_email_click', 0) > 3:
        score += 30

    # Website activity
    if contact_data.get('num_pageviews', 0) > 10:
        score += 25

    # Profile completeness
    if contact_data.get('jobtitle'):
        score += 10
    if contact_data.get('company'):
        score += 10

    # Lifecycle stage
    lifecycle = contact_data.get('lifecyclestage', '')
    if lifecycle == 'marketingqualifiedlead':
        score += 40
    elif lifecycle == 'salesqualifiedlead':
        score += 60

    return min(score, 100)  # Cap at 100

# Score and update all contacts
def score_all_contacts():
    properties = [
        'email', 'firstname', 'lastname', 'jobtitle', 'company',
        'lifecyclestage', 'hs_email_open', 'hs_email_click',
        'num_pageviews'
    ]

    contacts = get_contacts_for_scoring(properties)

    for contact in contacts:
        props = {p['name']: p['value'] for p in contact.get('properties', [])}

        score = calculate_lead_score(props)

        # Update contact with new score
        update_url = f'{BASE_URL}/contacts/v1/contact/vid/{contact["vid"]}/profile'

        requests.post(
            update_url,
            params={'hapikey': API_KEY},
            json={
                'properties': [
                    {'property': 'hs_lead_score', 'value': str(score)}
                ]
            }
        )

    print(f"Scored {len(contacts)} contacts")

# Create smart list based on score
def create_high_score_list():
    url = f'{BASE_URL}/contacts/v1/lists'

    list_data = {
        'name': 'High Score Leads (80+)',
        'dynamic': True,
        'filters': [
            [
                {
                    'filterFamily': 'PropertyValue',
                    'property': 'hs_lead_score',
                    'type': 'number',
                    'operation': 'GTE',
                    'value': '80'
                }
            ]
        ]
    }

    response = requests.post(
        url,
        params={'hapikey': API_KEY},
        json=list_data
    )

    return response.json()
```

### 6. Analytics and Reporting

```python
from datetime import datetime, timedelta
import pandas as pd

# Get email performance report
def get_email_performance_report(days=30):
    url = f'{BASE_URL}/email/public/v1/campaigns'

    params = {
        'hapikey': API_KEY,
        'limit': 100
    }

    response = requests.get(url, params=params)
    campaigns = response.json().get('campaigns', [])

    report_data = []

    for campaign in campaigns:
        if campaign.get('counters'):
            counters = campaign['counters']

            sent = counters.get('sent', 0)
            delivered = counters.get('delivered', 0)
            opens = counters.get('open', 0)
            clicks = counters.get('click', 0)

            report_data.append({
                'campaign_name': campaign.get('name'),
                'subject': campaign.get('subject'),
                'sent': sent,
                'delivered': delivered,
                'opens': opens,
                'clicks': clicks,
                'open_rate': (opens / delivered * 100) if delivered > 0 else 0,
                'click_rate': (clicks / delivered * 100) if delivered > 0 else 0,
                'ctr': (clicks / opens * 100) if opens > 0 else 0
            })

    df = pd.DataFrame(report_data)
    return df.sort_values('sent', ascending=False)

# Get form submissions
def get_form_submissions(form_id, start_date=None):
    url = f'{BASE_URL}/form-integrations/v1/submissions/forms/{form_id}'

    params = {'hapikey': API_KEY}
    if start_date:
        params['after'] = int(start_date.timestamp() * 1000)

    response = requests.get(url, params=params)
    return response.json()

# Website analytics
def get_website_analytics():
    # Get page view analytics
    url = f'{BASE_URL}/analytics/v2/reports/totals'

    params = {
        'hapikey': API_KEY,
        'start': int((datetime.now() - timedelta(days=30)).timestamp() * 1000),
        'end': int(datetime.now().timestamp() * 1000)
    }

    response = requests.get(url, params=params)
    return response.json()

# Example: Generate comprehensive report
print("Email Performance Report:")
email_report = get_email_performance_report(30)
print(email_report.head(10))

print(f"\nAverage Open Rate: {email_report['open_rate'].mean():.2f}%")
print(f"Average Click Rate: {email_report['click_rate'].mean():.2f}%")
```

## Installation

```bash
# Using official Python client (recommended)
uv pip install hubspot-api-client

# Or using requests for REST API
uv pip install requests pandas
```

## Authentication

HubSpot supports two authentication methods:

### API Key (Legacy - for simple use cases)
```python
# Use hapikey parameter in requests
params = {'hapikey': 'your-api-key'}
```

### OAuth 2.0 (Recommended)
```python
from hubspot import HubSpot

api_client = HubSpot(access_token='your-access-token')

# Or with API key
api_client = HubSpot(api_key='your-api-key')
```

To get credentials:
1. Go to HubSpot Settings > Integrations > API Key (or Private Apps)
2. Generate API key or create a Private App with OAuth
3. Copy the access token/API key

## Quick Start

```python
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput

# Initialize client
api_client = HubSpot(access_token='your-access-token')

# Create a contact
contact_input = SimplePublicObjectInput(
    properties={
        'email': 'newlead@example.com',
        'firstname': 'Jane',
        'lastname': 'Smith',
        'company': 'Tech Startup Inc',
        'lifecyclestage': 'lead'
    }
)

new_contact = api_client.crm.contacts.basic_api.create(
    simple_public_object_input=contact_input
)

print(f"Contact created with ID: {new_contact.id}")

# Get contact
contact = api_client.crm.contacts.basic_api.get_by_id(
    contact_id=new_contact.id,
    properties=['email', 'firstname', 'lastname', 'company']
)

print(f"Retrieved contact: {contact.properties}")
```

## Key Features Reference

- **Contacts**: CRM database, custom properties, lifecycle stages
- **Companies**: Account-based organization and tracking
- **Deals**: Sales pipeline and revenue tracking
- **Email Marketing**: Campaign creation, A/B testing, analytics
- **Workflows**: Marketing automation, lead nurturing
- **Forms**: Lead capture, progressive profiling
- **Landing Pages**: Conversion-optimized pages
- **Lead Scoring**: Automated qualification
- **Lists**: Segmentation and targeting
- **Analytics**: Attribution, ROI tracking, dashboards

## References

- [HubSpot API Documentation](https://developers.hubspot.com/docs/api/overview)
- [Python Client SDK](https://github.com/HubSpot/hubspot-api-python)
- [CRM API Reference](https://developers.hubspot.com/docs/api/crm/understanding-the-crm)
- [Marketing Email API](https://developers.hubspot.com/docs/api/marketing/marketing-email)
- [Workflows API](https://developers.hubspot.com/docs/api/automation/workflows)

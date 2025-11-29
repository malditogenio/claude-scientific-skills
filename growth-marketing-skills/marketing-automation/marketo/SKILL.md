---
name: marketo
description: "Marketo B2B marketing automation platform. Lead management, email marketing, revenue attribution, account-based marketing, CRM integration, scoring."
---

# Marketo Integration

## Overview

Marketo is an enterprise B2B marketing automation platform with advanced lead management, nurturing, and revenue attribution capabilities. This skill covers using the Marketo REST API for lead management, campaign execution, and analytics.

## When to Use This Skill

- B2B lead management and nurturing
- Email marketing automation
- Lead scoring and grading
- Account-based marketing (ABM)
- Revenue attribution and reporting
- CRM synchronization (Salesforce, Dynamics)
- Progressive profiling
- Multi-touch attribution

## Core Capabilities

### 1. Lead Management

```python
import requests
import json
from datetime import datetime

# Marketo API configuration
MUNCHKIN_ID = 'your-munchkin-id'
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
BASE_URL = f'https://{MUNCHKIN_ID}.mktorest.com'

# Get access token
def get_access_token():
    url = f'{BASE_URL}/identity/oauth/token'

    params = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.get(url, params=params)
    return response.json()['access_token']

# Initialize token
ACCESS_TOKEN = get_access_token()

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

# Create or update lead
def create_or_update_lead(leads):
    url = f'{BASE_URL}/rest/v1/leads.json'

    data = {
        'action': 'createOrUpdate',
        'lookupField': 'email',
        'input': leads
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example usage
result = create_or_update_lead([
    {
        'email': 'lead@example.com',
        'firstName': 'John',
        'lastName': 'Doe',
        'company': 'Acme Corp',
        'title': 'Marketing Director',
        'leadScore': 85,
        'leadSource': 'Website'
    }
])

print(f"Lead created/updated: {result}")

# Get lead by ID
def get_lead_by_id(lead_id, fields=None):
    url = f'{BASE_URL}/rest/v1/lead/{lead_id}.json'

    params = {}
    if fields:
        params['fields'] = ','.join(fields)

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Get leads by filter
def get_leads_by_filter(filter_type, filter_values, fields=None):
    url = f'{BASE_URL}/rest/v1/leads.json'

    params = {
        'filterType': filter_type,
        'filterValues': ','.join(filter_values)
    }

    if fields:
        params['fields'] = ','.join(fields)

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Example: Get leads by email
leads = get_leads_by_filter(
    'email',
    ['lead1@example.com', 'lead2@example.com'],
    fields=['email', 'firstName', 'lastName', 'company', 'leadScore']
)

print(f"Found {len(leads.get('result', []))} leads")

# Delete lead
def delete_lead(lead_ids):
    url = f'{BASE_URL}/rest/v1/leads.json'

    data = {'input': [{'id': lead_id} for lead_id in lead_ids]}

    response = requests.delete(url, headers=headers, json=data)
    return response.json()
```

### 2. Smart Lists and Segmentation

```python
# Get smart lists
def get_smart_lists(folder_id=None):
    url = f'{BASE_URL}/rest/asset/v1/smartLists.json'

    params = {}
    if folder_id:
        params['folder'] = json.dumps({'id': folder_id, 'type': 'Folder'})

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Get smart list by ID
def get_smart_list(smart_list_id):
    url = f'{BASE_URL}/rest/asset/v1/smartList/{smart_list_id}.json'

    response = requests.get(url, headers=headers)
    return response.json()

# Get leads in smart list
def get_smart_list_leads(smart_list_id, batch_size=300):
    url = f'{BASE_URL}/rest/v1/lists/{smart_list_id}/leads.json'

    all_leads = []
    next_page_token = None

    while True:
        params = {'batchSize': batch_size}
        if next_page_token:
            params['nextPageToken'] = next_page_token

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        all_leads.extend(data.get('result', []))

        if not data.get('moreResult'):
            break

        next_page_token = data.get('nextPageToken')

    return all_leads

# Example: Get all leads in MQL smart list
smart_lists = get_smart_lists()

mql_list = next(
    (sl for sl in smart_lists.get('result', [])
     if 'MQL' in sl['name']),
    None
)

if mql_list:
    mqls = get_smart_list_leads(mql_list['id'])
    print(f"Found {len(mqls)} MQLs")
```

### 3. Email Programs and Campaigns

```python
# Get email programs
def get_email_programs():
    url = f'{BASE_URL}/rest/asset/v1/programs.json'

    params = {'maxReturn': 200}

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Request campaign
def request_campaign(campaign_id, leads, tokens=None):
    url = f'{BASE_URL}/rest/v1/campaigns/{campaign_id}/trigger.json'

    data = {
        'input': {
            'leads': [{'id': lead_id} for lead_id in leads]
        }
    }

    if tokens:
        data['input']['tokens'] = [
            {'name': f'{{{{my.{key}}}}}', 'value': value}
            for key, value in tokens.items()
        ]

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Schedule campaign
def schedule_campaign(campaign_id, run_at, tokens=None):
    url = f'{BASE_URL}/rest/v1/campaigns/{campaign_id}/schedule.json'

    data = {
        'runAt': run_at,  # ISO 8601 format
        'tokens': tokens or []
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Get campaign details
def get_campaign(campaign_id):
    url = f'{BASE_URL}/rest/v1/campaigns/{campaign_id}.json'

    response = requests.get(url, headers=headers)
    return response.json()

# Example: Trigger nurture campaign for new leads
new_lead_ids = [123, 456, 789]

request_campaign(
    campaign_id=1001,
    leads=new_lead_ids,
    tokens={
        'firstName': 'Valued',
        'offerCode': 'WELCOME20'
    }
)
```

### 4. Activities and Engagement

```python
# Get lead activities
def get_lead_activities(lead_ids, activity_type_ids=None, next_page_token=None):
    url = f'{BASE_URL}/rest/v1/activities/leadChanges.json'

    params = {
        'leadIds': ','.join(map(str, lead_ids))
    }

    if activity_type_ids:
        params['activityTypeIds'] = ','.join(map(str, activity_type_ids))

    if next_page_token:
        params['nextPageToken'] = next_page_token

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Get activity types
def get_activity_types():
    url = f'{BASE_URL}/rest/v1/activities/types.json'

    response = requests.get(url, headers=headers)
    return response.json()

# Get paging token for activities
def get_paging_token(since_datetime):
    url = f'{BASE_URL}/rest/v1/activities/pagingtoken.json'

    params = {
        'sinceDatetime': since_datetime  # ISO 8601 format
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()['nextPageToken']

# Track custom activity
def add_custom_activity(lead_id, activity_type_id, primary_attribute_value, attributes=None):
    url = f'{BASE_URL}/rest/v1/activities/external.json'

    data = {
        'input': [
            {
                'leadId': lead_id,
                'activityDate': datetime.now().isoformat(),
                'activityTypeId': activity_type_id,
                'primaryAttributeValue': primary_attribute_value,
                'attributes': attributes or []
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example: Track webinar attendance
add_custom_activity(
    lead_id=12345,
    activity_type_id=100001,  # Custom webinar activity type
    primary_attribute_value='Q4 Product Launch Webinar',
    attributes=[
        {'name': 'Attended', 'value': 'Yes'},
        {'name': 'Duration', 'value': '45 minutes'},
        {'name': 'Questions Asked', 'value': '2'}
    ]
)
```

### 5. Lead Scoring and Grading

```python
# Update lead score
def update_lead_score(lead_id, score_change, reason=None):
    # Use lead update API
    updates = [
        {
            'id': lead_id,
            'leadScore': score_change
        }
    ]

    return create_or_update_lead(updates)

# Get lead score changes
def get_score_changes(since_datetime):
    url = f'{BASE_URL}/rest/v1/activities.json'

    # Get paging token
    paging_token = get_paging_token(since_datetime)

    params = {
        'nextPageToken': paging_token,
        'activityTypeIds': '13'  # Score Changed activity type
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Calculate and update lead score
def calculate_lead_score(lead):
    score = 0

    # Demographic scoring
    if lead.get('title') and any(title in lead['title'].lower() for title in ['vp', 'director', 'manager']):
        score += 20

    # Company size scoring
    if lead.get('numberOfEmployees', 0) > 1000:
        score += 15

    # Engagement scoring (based on activities)
    if lead.get('emailOpens', 0) > 5:
        score += 10
    if lead.get('emailClicks', 0) > 3:
        score += 15

    # Content downloads
    if lead.get('contentDownloads', 0) > 0:
        score += 10

    return score

# Batch score update
def batch_update_scores(lead_ids):
    results = []

    for lead_id in lead_ids:
        lead_data = get_lead_by_id(lead_id)
        lead = lead_data.get('result', [{}])[0]

        new_score = calculate_lead_score(lead)

        result = update_lead_score(lead_id, new_score, reason='Automated scoring')
        results.append(result)

    return results
```

### 6. Program Membership

```python
# Add leads to program
def add_leads_to_program(program_id, lead_ids, status='Member'):
    url = f'{BASE_URL}/rest/v1/programs/{program_id}/members.json'

    data = {
        'input': [
            {
                'leadId': lead_id,
                'status': status
            }
            for lead_id in lead_ids
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Get program members
def get_program_members(program_id):
    url = f'{BASE_URL}/rest/v1/leads/programs/{program_id}.json'

    all_members = []
    next_page_token = None

    while True:
        params = {'batchSize': 300}
        if next_page_token:
            params['nextPageToken'] = next_page_token

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        all_members.extend(data.get('result', []))

        if not data.get('moreResult'):
            break

        next_page_token = data.get('nextPageToken')

    return all_members

# Change program member status
def change_program_status(program_id, lead_ids, status):
    url = f'{BASE_URL}/rest/v1/programs/{program_id}/members/status.json'

    data = {
        'input': [
            {
                'leadId': lead_id,
                'status': status
            }
            for lead_id in lead_ids
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example: Mark webinar attendees
webinar_attendees = [101, 102, 103]

change_program_status(
    program_id=5001,
    lead_ids=webinar_attendees,
    status='Attended'
)
```

### 7. Analytics and Reporting

```python
import pandas as pd

# Get campaign performance
def get_campaign_metrics():
    # Get all campaigns
    campaigns_url = f'{BASE_URL}/rest/v1/campaigns.json'
    campaigns_response = requests.get(campaigns_url, headers=headers)
    campaigns = campaigns_response.json().get('result', [])

    metrics = []

    for campaign in campaigns:
        campaign_id = campaign['id']

        # Get campaign details with stats
        details = get_campaign(campaign_id)

        if details.get('result'):
            campaign_data = details['result'][0]

            metrics.append({
                'campaign_name': campaign_data.get('name'),
                'campaign_id': campaign_id,
                'type': campaign_data.get('type'),
                'active': campaign_data.get('active'),
                'created_at': campaign_data.get('createdAt')
            })

    df = pd.DataFrame(metrics)
    return df

# Export lead data for analysis
def export_leads_to_dataframe(smart_list_id, fields):
    leads = get_smart_list_leads(smart_list_id)

    # Convert to DataFrame
    df = pd.DataFrame(leads)

    # Select relevant fields
    if fields:
        available_fields = [f for f in fields if f in df.columns]
        df = df[available_fields]

    return df

# Revenue attribution report
def generate_revenue_report():
    # Get opportunities (assuming integration with CRM)
    # This would typically involve querying opportunities/deals
    # linked to Marketo programs

    # Placeholder for demonstration
    programs = get_email_programs()

    report_data = []

    for program in programs.get('result', [])[:10]:
        program_id = program['id']

        # Get program members
        members = get_program_members(program_id)

        # Calculate metrics
        report_data.append({
            'program_name': program['name'],
            'program_id': program_id,
            'members': len(members),
            'type': program.get('type')
        })

    df = pd.DataFrame(report_data)
    return df

# Example usage
campaign_performance = get_campaign_metrics()
print("Campaign Performance:")
print(campaign_performance.head(10))
```

## Installation

```bash
uv pip install requests pandas
```

## Authentication

Get your API credentials from Marketo:
1. Log in to Marketo
2. Go to Admin > Integration > LaunchPoint
3. Create a new service with API User role
4. Note Client ID and Client Secret
5. Go to Admin > Integration > Web Services to get Munchkin ID and REST API endpoint

```python
# OAuth 2.0 authentication
def get_access_token():
    url = f'{BASE_URL}/identity/oauth/token'

    params = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.get(url, params=params)
    return response.json()['access_token']

ACCESS_TOKEN = get_access_token()

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}
```

## Quick Start

```python
import requests

MUNCHKIN_ID = 'your-munchkin-id'
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
BASE_URL = f'https://{MUNCHKIN_ID}.mktorest.com'

# Get token
token_response = requests.get(
    f'{BASE_URL}/identity/oauth/token',
    params={
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
)

access_token = token_response.json()['access_token']

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Create lead
lead_data = {
    'action': 'createOrUpdate',
    'lookupField': 'email',
    'input': [
        {
            'email': 'newlead@example.com',
            'firstName': 'Jane',
            'lastName': 'Smith',
            'company': 'Tech Startup'
        }
    ]
}

response = requests.post(
    f'{BASE_URL}/rest/v1/leads.json',
    headers=headers,
    json=lead_data
)

print(f"Lead created: {response.json()}")
```

## Key Features Reference

- **Leads**: Contact database, custom fields, scoring
- **Smart Lists**: Dynamic segmentation
- **Campaigns**: Smart campaigns, batch campaigns, trigger campaigns
- **Programs**: Email, event, engagement, default programs
- **Activities**: Lead activity tracking, custom activities
- **Assets**: Emails, landing pages, forms, files
- **Opportunities**: Revenue attribution (via CRM sync)
- **Custom Objects**: Extended data model

## References

- [Marketo REST API Documentation](https://developers.marketo.com/rest-api/)
- [API Endpoint Reference](https://developers.marketo.com/rest-api/endpoint-reference/)
- [Lead Database API](https://developers.marketo.com/rest-api/lead-database/)
- [Asset API](https://developers.marketo.com/rest-api/assets/)
- [Bulk Extract API](https://developers.marketo.com/rest-api/bulk-extract/)

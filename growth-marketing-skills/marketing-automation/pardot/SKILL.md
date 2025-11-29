---
name: pardot
description: "Salesforce Pardot (Marketing Cloud Account Engagement) B2B marketing automation. Lead nurturing, email marketing, ROI reporting, Salesforce integration."
---

# Pardot (Marketing Cloud Account Engagement) Integration

## Overview

Pardot is Salesforce's B2B marketing automation platform (now called Marketing Cloud Account Engagement). This skill covers using the Pardot API for prospect management, email marketing, lead nurturing, and Salesforce synchronization.

## When to Use This Skill

- B2B lead generation and nurturing
- Salesforce-integrated marketing automation
- Email marketing campaigns
- Lead scoring and grading
- ROI and attribution reporting
- Progressive profiling
- Account-based marketing
- Sales and marketing alignment

## Core Capabilities

### 1. Prospect Management

```python
import requests
import json
from datetime import datetime

# Pardot API configuration
BUSINESS_UNIT_ID = 'your-business-unit-id'
API_KEY = 'your-api-key'
BASE_URL = 'https://pi.pardot.com/api'

# Note: Pardot API v5 uses OAuth 2.0 with Salesforce
# This example shows v4 for simplicity

headers = {
    'Authorization': f'Pardot api_key={API_KEY}, user_key=YOUR_USER_KEY',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Pardot-Business-Unit-Id': BUSINESS_UNIT_ID
}

# Create prospect
def create_prospect(email, data):
    url = f'{BASE_URL}/prospect/version/4/do/create'

    params = {
        'email': email,
        **data
    }

    response = requests.post(url, headers=headers, params=params)
    return response.text

# Update prospect
def update_prospect(prospect_id=None, email=None, updates=None):
    url = f'{BASE_URL}/prospect/version/4/do/update'

    params = updates or {}

    if prospect_id:
        url += f'/id/{prospect_id}'
    elif email:
        url += f'/email/{email}'

    response = requests.post(url, headers=headers, params=params)
    return response.text

# Example usage
prospect = create_prospect(
    'lead@example.com',
    {
        'first_name': 'John',
        'last_name': 'Doe',
        'company': 'Acme Corp',
        'job_title': 'VP Marketing',
        'score': 50
    }
)

print(f"Prospect created: {prospect}")

# Query prospects
def query_prospects(criteria=None, sort_by='created_at', sort_order='descending'):
    url = f'{BASE_URL}/prospect/version/4/do/query'

    params = {
        'sort_by': sort_by,
        'sort_order': sort_order
    }

    if criteria:
        params.update(criteria)

    response = requests.post(url, headers=headers, params=params)
    return response.text

# Read prospect
def read_prospect(prospect_id=None, email=None):
    if prospect_id:
        url = f'{BASE_URL}/prospect/version/4/do/read/id/{prospect_id}'
    elif email:
        url = f'{BASE_URL}/prospect/version/4/do/read/email/{email}'
    else:
        return None

    response = requests.post(url, headers=headers)
    return response.text

# Assign prospect
def assign_prospect(prospect_id, user_email):
    url = f'{BASE_URL}/prospect/version/4/do/assign/id/{prospect_id}'

    params = {'user_email': user_email}

    response = requests.post(url, headers=headers, params=params)
    return response.text

# Example: Query high-score prospects
high_score_prospects = query_prospects(
    criteria={
        'score_greater_than': 75
    }
)
```

### 2. Lists and Segmentation

```python
# Create list
def create_list(name, description=None):
    url = f'{BASE_URL}/list/version/4/do/create'

    params = {
        'name': name,
        'description': description or ''
    }

    response = requests.post(url, headers=headers, params=params)
    return response.text

# Add prospect to list
def add_prospect_to_list(list_id, prospect_id):
    url = f'{BASE_URL}/listMembership/version/4/do/create'

    params = {
        'list_id': list_id,
        'prospect_id': prospect_id
    }

    response = requests.post(url, headers=headers, params=params)
    return response.text

# Remove prospect from list
def remove_prospect_from_list(list_id, prospect_id):
    url = f'{BASE_URL}/listMembership/version/4/do/delete'

    params = {
        'list_id': list_id,
        'prospect_id': prospect_id
    }

    response = requests.post(url, headers=headers, params=params)
    return response.text

# Query lists
def query_lists():
    url = f'{BASE_URL}/list/version/4/do/query'

    response = requests.post(url, headers=headers)
    return response.text

# Example: Create VIP list and add prospects
vip_list = create_list('VIP Prospects', 'High-value enterprise prospects')

# Add prospects to VIP list
prospect_ids = [101, 102, 103]
for prospect_id in prospect_ids:
    add_prospect_to_list(vip_list_id, prospect_id)
```

### 3. Email and Email Templates

```python
# Send one-to-one email
def send_one_to_one_email(prospect_id, campaign_id, email_template_id):
    url = f'{BASE_URL}/email/version/4/do/send'

    params = {
        'prospect_id': prospect_id,
        'campaign_id': campaign_id,
        'email_template_id': email_template_id
    }

    response = requests.post(url, headers=headers, params=params)
    return response.text

# Send list email
def send_list_email(campaign_id, email_template_id, list_ids=None, suppression_list_ids=None):
    url = f'{BASE_URL}/emailClick/version/4/do/listEmail'

    params = {
        'campaign_id': campaign_id,
        'email_template_id': email_template_id
    }

    if list_ids:
        params['list_ids'] = ','.join(map(str, list_ids))

    if suppression_list_ids:
        params['suppression_list_ids'] = ','.join(map(str, suppression_list_ids))

    response = requests.post(url, headers=headers, params=params)
    return response.text

# Read email template
def read_email_template(template_id):
    url = f'{BASE_URL}/emailTemplate/version/4/do/read/id/{template_id}'

    response = requests.post(url, headers=headers)
    return response.text

# Query email templates
def query_email_templates():
    url = f'{BASE_URL}/emailTemplate/version/4/do/query'

    response = requests.post(url, headers=headers)
    return response.text

# Example: Send personalized email to prospects
send_one_to_one_email(
    prospect_id=12345,
    campaign_id=100,
    email_template_id=500
)
```

### 4. Campaigns

```python
# Create campaign
def create_campaign(name, cost=None):
    url = f'{BASE_URL}/campaign/version/4/do/create'

    params = {'name': name}

    if cost:
        params['cost'] = cost

    response = requests.post(url, headers=headers, params=params)
    return response.text

# Update campaign
def update_campaign(campaign_id, updates):
    url = f'{BASE_URL}/campaign/version/4/do/update/id/{campaign_id}'

    response = requests.post(url, headers=headers, params=updates)
    return response.text

# Query campaigns
def query_campaigns():
    url = f'{BASE_URL}/campaign/version/4/do/query'

    response = requests.post(url, headers=headers)
    return response.text

# Read campaign
def read_campaign(campaign_id):
    url = f'{BASE_URL}/campaign/version/4/do/read/id/{campaign_id}'

    response = requests.post(url, headers=headers)
    return response.text

# Example: Create Q4 campaign
campaign = create_campaign(
    'Q4 Product Launch',
    cost=50000
)
```

### 5. Forms and Landing Pages

```python
# Query forms
def query_forms():
    url = f'{BASE_URL}/form/version/4/do/query'

    response = requests.post(url, headers=headers)
    return response.text

# Read form
def read_form(form_id):
    url = f'{BASE_URL}/form/version/4/do/read/id/{form_id}'

    response = requests.post(url, headers=headers)
    return response.text

# Query landing pages
def query_landing_pages():
    url = f'{BASE_URL}/landingPage/version/4/do/query'

    response = requests.post(url, headers=headers)
    return response.text

# Read landing page
def read_landing_page(page_id):
    url = f'{BASE_URL}/landingPage/version/4/do/read/id/{page_id}'

    response = requests.post(url, headers=headers)
    return response.text
```

### 6. Visitor Activity Tracking

```python
# Query visitor activities
def query_visitor_activities(prospect_id=None, visitor_id=None):
    url = f'{BASE_URL}/visitorActivity/version/4/do/query'

    params = {}

    if prospect_id:
        params['prospect_id'] = prospect_id
    elif visitor_id:
        params['visitor_id'] = visitor_id

    response = requests.post(url, headers=headers, params=params)
    return response.text

# Read visitor
def read_visitor(visitor_id):
    url = f'{BASE_URL}/visitor/version/4/do/read/id/{visitor_id}'

    response = requests.post(url, headers=headers)
    return response.text

# Assign visitor to prospect
def assign_visitor_to_prospect(visitor_id, prospect_id):
    url = f'{BASE_URL}/visitor/version/4/do/assign/id/{visitor_id}'

    params = {'prospect_id': prospect_id}

    response = requests.post(url, headers=headers, params=params)
    return response.text

# Example: Get prospect activity
activities = query_visitor_activities(prospect_id=12345)
print(f"Prospect activities: {activities}")
```

### 7. Opportunities (Salesforce Integration)

```python
# Create opportunity
def create_opportunity(name, value, probability, campaign_id):
    url = f'{BASE_URL}/opportunity/version/4/do/create'

    params = {
        'name': name,
        'value': value,
        'probability': probability,
        'campaign_id': campaign_id
    }

    response = requests.post(url, headers=headers, params=params)
    return response.text

# Query opportunities
def query_opportunities(criteria=None):
    url = f'{BASE_URL}/opportunity/version/4/do/query'

    params = criteria or {}

    response = requests.post(url, headers=headers, params=params)
    return response.text

# Update opportunity
def update_opportunity(opportunity_id, updates):
    url = f'{BASE_URL}/opportunity/version/4/do/update/id/{opportunity_id}'

    response = requests.post(url, headers=headers, params=updates)
    return response.text

# Example: Create opportunity for qualified lead
opportunity = create_opportunity(
    name='Acme Corp - Enterprise License',
    value=100000,
    probability=60,
    campaign_id=100
)
```

### 8. Analytics and Reporting

```python
import pandas as pd
import xml.etree.ElementTree as ET

# Parse XML response (Pardot v4 returns XML)
def parse_pardot_xml(xml_string):
    root = ET.fromstring(xml_string)
    return root

# Get campaign performance
def get_campaign_performance():
    campaigns_xml = query_campaigns()
    root = parse_pardot_xml(campaigns_xml)

    campaigns = []

    for campaign in root.findall('.//campaign'):
        campaigns.append({
            'id': campaign.find('id').text if campaign.find('id') is not None else None,
            'name': campaign.find('name').text if campaign.find('name') is not None else None,
            'cost': campaign.find('cost').text if campaign.find('cost') is not None else 0
        })

    df = pd.DataFrame(campaigns)
    return df

# Get prospect conversion report
def get_prospect_conversion_report():
    prospects_xml = query_prospects()
    root = parse_pardot_xml(prospects_xml)

    prospects = []

    for prospect in root.findall('.//prospect'):
        prospects.append({
            'email': prospect.find('email').text if prospect.find('email') is not None else None,
            'score': prospect.find('score').text if prospect.find('score') is not None else 0,
            'grade': prospect.find('grade').text if prospect.find('grade') is not None else None,
            'created_at': prospect.find('created_at').text if prospect.find('created_at') is not None else None
        })

    df = pd.DataFrame(prospects)

    # Calculate conversion metrics
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    df['qualified'] = df['score'] >= 50

    return df

# Example usage
campaign_performance = get_campaign_performance()
print("Campaign Performance:")
print(campaign_performance)

conversion_report = get_prospect_conversion_report()
print(f"\nQualified Prospects: {conversion_report['qualified'].sum()}")
print(f"Average Score: {conversion_report['score'].mean():.2f}")
```

## Installation

```bash
uv pip install requests pandas
```

## Authentication

Pardot API v5 uses Salesforce OAuth 2.0:

1. Create a Connected App in Salesforce
2. Get Client ID and Client Secret
3. Obtain access token via OAuth flow
4. Use Business Unit ID from Pardot

```python
import requests

# OAuth 2.0 authentication (v5)
def get_salesforce_token(client_id, client_secret, username, password):
    url = 'https://login.salesforce.com/services/oauth2/token'

    data = {
        'grant_type': 'password',
        'client_id': client_id,
        'client_secret': client_secret,
        'username': username,
        'password': password
    }

    response = requests.post(url, data=data)
    return response.json()['access_token']

# Use token in headers
headers = {
    'Authorization': f'Bearer {access_token}',
    'Pardot-Business-Unit-Id': BUSINESS_UNIT_ID
}
```

## Quick Start

```python
import requests

# V4 API example
API_KEY = 'your-api-key'
USER_KEY = 'your-user-key'
BASE_URL = 'https://pi.pardot.com/api'

headers = {
    'Authorization': f'Pardot api_key={API_KEY}, user_key={USER_KEY}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Create prospect
response = requests.post(
    f'{BASE_URL}/prospect/version/4/do/create',
    headers=headers,
    params={
        'email': 'newlead@example.com',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'company': 'Tech Corp'
    }
)

print(f"Prospect created: {response.text}")
```

## Key Features Reference

- **Prospects**: Lead database, scoring, grading
- **Lists**: Static segmentation
- **Dynamic Lists**: Automated segmentation
- **Campaigns**: Campaign tracking and ROI
- **Emails**: One-to-one and list emails
- **Forms**: Lead capture forms
- **Landing Pages**: Conversion pages
- **Opportunities**: Revenue tracking (Salesforce sync)
- **Custom Fields**: Extended prospect data
- **Engagement Studio**: Automated nurture programs

## References

- [Pardot API Documentation](https://developer.salesforce.com/docs/marketing/pardot/guide/overview.html)
- [Pardot API v5](https://developer.salesforce.com/docs/marketing/pardot/guide/pardot-api-v5.html)
- [Salesforce Marketing Cloud Account Engagement](https://help.salesforce.com/s/articleView?id=sf.pardot_welcome.htm)
- [OAuth Authentication](https://developer.salesforce.com/docs/marketing/pardot/guide/authentication.html)

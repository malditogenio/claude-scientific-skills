---
name: pipedrive
description: "Pipedrive sales CRM. Pipeline management, deal tracking, activity scheduling, sales automation, visual pipeline, forecasting, contact management."
---

# Pipedrive Integration

## Overview

Pipedrive is a sales-focused CRM designed around pipeline management and deal flow visualization. This skill covers using the Pipedrive API to manage deals, track sales activities, automate workflows, and analyze pipeline health with a focus on marketing-sales handoff and lead qualification.

## When to Use This Skill

- Visual pipeline management and deal tracking
- Sales activity scheduling and automation
- Lead qualification and handoff from marketing
- Pipeline forecasting and win probability
- Sales rep performance tracking
- Integration with marketing automation platforms
- Deal stage automation and workflows
- Revenue forecasting and pipeline analytics

## Core Capabilities

### 1. Lead and Contact Management

```python
import requests
import json
from datetime import datetime

# Pipedrive API configuration
API_TOKEN = 'your-pipedrive-api-token'
COMPANY_DOMAIN = 'your-company'
BASE_URL = f'https://{COMPANY_DOMAIN}.pipedrive.com/api/v1'

def api_request(endpoint, method='GET', data=None):
    """Make Pipedrive API request."""
    url = f'{BASE_URL}/{endpoint}'
    params = {'api_token': API_TOKEN}

    if method == 'GET':
        response = requests.get(url, params=params)
    elif method == 'POST':
        response = requests.post(url, params=params, json=data)
    elif method == 'PUT':
        response = requests.put(url, params=params, json=data)
    elif method == 'DELETE':
        response = requests.delete(url, params=params)

    return response.json()

# Create person (contact)
def create_contact(name, email, phone=None, org_name=None, marketing_data=None):
    """Create contact with marketing attribution data."""
    # First, create or get organization
    org_id = None
    if org_name:
        org_id = create_or_get_organization(org_name)

    person_data = {
        'name': name,
        'email': email,
        'phone': phone,
        'org_id': org_id,
        # Custom fields for marketing attribution
        'lead_source': marketing_data.get('source') if marketing_data else None,
        'utm_campaign': marketing_data.get('utm_campaign') if marketing_data else None,
        'utm_medium': marketing_data.get('utm_medium') if marketing_data else None,
        'utm_source': marketing_data.get('utm_source') if marketing_data else None,
        'lead_score': marketing_data.get('lead_score', 0) if marketing_data else 0
    }

    result = api_request('persons', method='POST', data=person_data)
    return result['data']['id']

# Create organization
def create_or_get_organization(org_name):
    """Create organization or get existing."""
    # Search for existing org
    search = api_request(f'organizations/search?term={org_name}')

    if search['data'] and len(search['data']['items']) > 0:
        return search['data']['items'][0]['item']['id']

    # Create new org
    org_data = {'name': org_name}
    result = api_request('organizations', method='POST', data=org_data)
    return result['data']['id']

# Update contact with lead score
def update_contact_score(person_id, score, scoring_factors):
    """Update contact lead score."""
    person_data = {
        'lead_score': score,
        'scoring_factors': scoring_factors,
        'last_score_update': datetime.now().isoformat()
    }

    result = api_request(f'persons/{person_id}', method='PUT', data=person_data)
    return result['success']

# Get contacts by filter
def get_qualified_leads(min_score=70):
    """Get contacts above minimum lead score."""
    # Note: Use custom filter created in Pipedrive UI
    filter_id = 'your_filter_id'  # Set up filter for lead_score >= min_score

    result = api_request(f'persons?filter_id={filter_id}')
    return result['data']

# Example: Create contact from marketing form
contact_id = create_contact(
    name='Emily Chen',
    email='emily.chen@startup.io',
    phone='+1-555-0123',
    org_name='Startup IO',
    marketing_data={
        'source': 'Website Demo Request',
        'utm_campaign': 'product-demo-2025',
        'utm_medium': 'organic',
        'utm_source': 'google',
        'lead_score': 78
    }
)

print(f"Contact created: {contact_id}")
```

### 2. Pipeline and Deal Management

```python
import pandas as pd

# Create deal with marketing attribution
def create_deal(title, person_id, org_id, value, pipeline_id=None, stage_id=None, marketing_data=None):
    """Create deal with full marketing context."""
    deal_data = {
        'title': title,
        'person_id': person_id,
        'org_id': org_id,
        'value': value,
        'currency': 'USD',
        'pipeline_id': pipeline_id,
        'stage_id': stage_id,
        # Marketing attribution
        'marketing_source': marketing_data.get('source') if marketing_data else None,
        'first_touch_campaign': marketing_data.get('first_touch') if marketing_data else None,
        'last_touch_campaign': marketing_data.get('last_touch') if marketing_data else None,
        'campaign_touches': marketing_data.get('campaign_touches', 0) if marketing_data else 0,
        'marketing_qualified_date': marketing_data.get('mql_date') if marketing_data else None
    }

    result = api_request('deals', method='POST', data=deal_data)
    return result['data']

# Update deal stage
def move_deal_to_stage(deal_id, stage_id, win_probability=None):
    """Move deal to new pipeline stage."""
    deal_data = {
        'stage_id': stage_id
    }

    if win_probability is not None:
        deal_data['probability'] = win_probability

    result = api_request(f'deals/{deal_id}', method='PUT', data=deal_data)
    return result['success']

# Get pipeline analytics
def get_pipeline_analytics(pipeline_id=None):
    """Analyze pipeline health and metrics."""
    # Get all deals
    endpoint = 'deals'
    if pipeline_id:
        endpoint += f'?pipeline_id={pipeline_id}'

    deals_response = api_request(endpoint)
    deals = deals_response['data']

    if not deals:
        return {}

    # Convert to DataFrame for analysis
    df = pd.DataFrame([{
        'deal_id': deal['id'],
        'title': deal['title'],
        'value': float(deal.get('value', 0)),
        'currency': deal.get('currency', 'USD'),
        'stage_id': deal.get('stage_id'),
        'status': deal.get('status'),
        'probability': deal.get('probability'),
        'expected_close_date': deal.get('expected_close_date'),
        'add_time': deal.get('add_time'),
        'update_time': deal.get('update_time'),
        'won_time': deal.get('won_time'),
        'lost_time': deal.get('lost_time')
    } for deal in deals])

    # Calculate metrics
    analytics = {
        'total_deals': len(df),
        'total_value': df['value'].sum(),
        'average_deal_size': df['value'].mean(),
        'open_deals': len(df[df['status'] == 'open']),
        'won_deals': len(df[df['status'] == 'won']),
        'lost_deals': len(df[df['status'] == 'lost']),
        'win_rate': len(df[df['status'] == 'won']) / len(df[df['status'].isin(['won', 'lost'])]) * 100
        if len(df[df['status'].isin(['won', 'lost'])]) > 0 else 0
    }

    # Weighted pipeline value
    df_open = df[df['status'] == 'open'].copy()
    df_open['weighted_value'] = df_open['value'] * (df_open['probability'] / 100)
    analytics['weighted_pipeline'] = df_open['weighted_value'].sum()

    # Stage breakdown
    stage_breakdown = df[df['status'] == 'open'].groupby('stage_id').agg({
        'deal_id': 'count',
        'value': 'sum'
    }).rename(columns={'deal_id': 'count', 'value': 'total_value'})

    analytics['stage_breakdown'] = stage_breakdown.to_dict()

    return analytics

# Calculate sales velocity
def calculate_sales_velocity(days=90):
    """Calculate sales velocity for forecasting."""
    # Get won deals from last N days
    deals_response = api_request(
        f'deals?status=won&start_date={datetime.now().date() - timedelta(days=days)}'
    )
    won_deals = deals_response['data']

    if not won_deals:
        return {}

    # Calculate metrics
    total_won = len(won_deals)
    total_value = sum(float(deal.get('value', 0)) for deal in won_deals)
    avg_deal_size = total_value / total_won if total_won > 0 else 0

    # Calculate average sales cycle
    cycle_lengths = []
    for deal in won_deals:
        if deal.get('add_time') and deal.get('won_time'):
            add_date = datetime.fromisoformat(deal['add_time'].replace('Z', '+00:00'))
            won_date = datetime.fromisoformat(deal['won_time'].replace('Z', '+00:00'))
            cycle_lengths.append((won_date - add_date).days)

    avg_cycle = sum(cycle_lengths) / len(cycle_lengths) if cycle_lengths else 0

    # Get current open deals
    open_response = api_request('deals?status=open')
    open_deals = len(open_response['data']) if open_response['data'] else 0

    # Win rate
    all_closed = api_request(f'deals?status=all_not_deleted&start_date={datetime.now().date() - timedelta(days=days)}')
    total_closed = len([d for d in all_closed['data'] if d['status'] in ['won', 'lost']]) if all_closed['data'] else 0
    win_rate = (total_won / total_closed) if total_closed > 0 else 0

    # Sales velocity = (Number of Opps * Avg Deal Size * Win Rate) / Sales Cycle
    velocity = (open_deals * avg_deal_size * win_rate) / max(avg_cycle, 1)

    return {
        'total_won_deals': total_won,
        'total_won_value': total_value,
        'average_deal_size': avg_deal_size,
        'average_sales_cycle_days': avg_cycle,
        'open_deals': open_deals,
        'win_rate': win_rate * 100,
        'sales_velocity_per_day': velocity
    }

# Example usage
pipeline_metrics = get_pipeline_analytics()
velocity = calculate_sales_velocity(90)

print(f"Pipeline Value: ${pipeline_metrics['total_value']:,.2f}")
print(f"Weighted Pipeline: ${pipeline_metrics['weighted_pipeline']:,.2f}")
print(f"Win Rate: {pipeline_metrics['win_rate']:.1f}%")
print(f"Sales Velocity: ${velocity['sales_velocity_per_day']:,.2f}/day")
```

### 3. Sales Activity Tracking

```python
# Create activity (call, meeting, email)
def create_activity(subject, activity_type, person_id, deal_id=None, due_date=None, note=None):
    """Create sales activity."""
    activity_data = {
        'subject': subject,
        'type': activity_type,  # call, meeting, task, deadline, email, lunch
        'person_id': person_id,
        'deal_id': deal_id,
        'due_date': due_date or datetime.now().date().isoformat(),
        'note': note,
        'done': 0  # 0 = not done, 1 = done
    }

    result = api_request('activities', method='POST', data=activity_data)
    return result['data']['id']

# Mark activity as done
def complete_activity(activity_id, outcome_note=None):
    """Mark activity as completed with outcome."""
    activity_data = {
        'done': 1
    }

    if outcome_note:
        activity_data['note'] = outcome_note

    result = api_request(f'activities/{activity_id}', method='PUT', data=activity_data)
    return result['success']

# Get activity summary for rep
def get_rep_activity_summary(user_id, days=30):
    """Get activity summary for sales rep."""
    start_date = (datetime.now().date() - timedelta(days=days)).isoformat()

    activities = api_request(
        f'activities?user_id={user_id}&start_date={start_date}'
    )

    if not activities['data']:
        return {}

    # Analyze activities
    df = pd.DataFrame(activities['data'])

    summary = {
        'total_activities': len(df),
        'completed_activities': len(df[df['done'] == True]),
        'pending_activities': len(df[df['done'] == False]),
        'completion_rate': len(df[df['done'] == True]) / len(df) * 100 if len(df) > 0 else 0
    }

    # Activity type breakdown
    type_breakdown = df.groupby('type').size().to_dict()
    summary['activity_breakdown'] = type_breakdown

    return summary

# Schedule follow-up sequence
def schedule_follow_up_sequence(person_id, deal_id):
    """Schedule automated follow-up activities."""
    follow_ups = [
        {
            'subject': 'Initial call follow-up',
            'type': 'task',
            'days_offset': 1,
            'note': 'Send follow-up email with meeting notes'
        },
        {
            'subject': 'Check-in call',
            'type': 'call',
            'days_offset': 3,
            'note': 'Check if they have any questions'
        },
        {
            'subject': 'Send case study',
            'type': 'email',
            'days_offset': 5,
            'note': 'Share relevant case study'
        },
        {
            'subject': 'Proposal follow-up',
            'type': 'call',
            'days_offset': 7,
            'note': 'Discuss proposal and next steps'
        }
    ]

    activity_ids = []
    for follow_up in follow_ups:
        due_date = (datetime.now().date() + timedelta(days=follow_up['days_offset'])).isoformat()

        activity_id = create_activity(
            subject=follow_up['subject'],
            activity_type=follow_up['type'],
            person_id=person_id,
            deal_id=deal_id,
            due_date=due_date,
            note=follow_up['note']
        )

        activity_ids.append(activity_id)

    return activity_ids
```

### 4. Data Enrichment and Lead Scoring

```python
# Calculate and update lead score
def score_lead(person_id):
    """Calculate lead score based on engagement and firmographics."""
    # Get person details
    person = api_request(f'persons/{person_id}')['data']

    score = 0
    factors = []

    # Email domain scoring
    email = person.get('email', [{}])[0].get('value', '') if person.get('email') else ''
    if email and not any(domain in email for domain in ['gmail.com', 'yahoo.com', 'hotmail.com']):
        score += 20
        factors.append('Business email')

    # Organization size (if available)
    if person.get('org_id'):
        org = api_request(f'organizations/{person["org_id"]["value"]}')['data']
        employee_count = org.get('people_count', 0)

        if employee_count > 100:
            score += 25
            factors.append('Large organization')
        elif employee_count > 10:
            score += 15
            factors.append('Mid-size organization')

    # Activity engagement
    activities = api_request(f'persons/{person_id}/activities')
    if activities['data']:
        activity_count = len(activities['data'])
        if activity_count >= 5:
            score += 30
            factors.append('High engagement')
        elif activity_count >= 2:
            score += 15
            factors.append('Some engagement')

    # Deal association
    if person.get('open_deals_count', 0) > 0:
        score += 20
        factors.append('Active deals')

    # Update person with score
    update_contact_score(person_id, min(score, 100), ', '.join(factors))

    return {
        'person_id': person_id,
        'score': min(score, 100),
        'factors': factors
    }

# Batch score all leads
def score_all_recent_leads(days=30):
    """Score all leads created in last N days."""
    start_date = (datetime.now().date() - timedelta(days=days)).isoformat()

    persons = api_request(f'persons?start_date={start_date}')

    if not persons['data']:
        return []

    scores = []
    for person in persons['data']:
        result = score_lead(person['id'])
        scores.append(result)

    return scores
```

## Installation

```bash
# Pipedrive doesn't have an official Python SDK
# Use requests library for API calls
uv pip install requests pandas python-dateutil
```

## Authentication

```python
# Pipedrive uses API token authentication
API_TOKEN = 'your-pipedrive-api-token'
COMPANY_DOMAIN = 'your-company'
BASE_URL = f'https://{COMPANY_DOMAIN}.pipedrive.com/api/v1'

# Make authenticated request
def api_request(endpoint):
    url = f'{BASE_URL}/{endpoint}'
    params = {'api_token': API_TOKEN}
    response = requests.get(url, params=params)
    return response.json()
```

To get API token:
1. Log into Pipedrive
2. Go to Settings > Personal Preferences > API
3. Copy your Personal API token
4. For company-wide apps, create an OAuth app

## Quick Start

```python
import requests

# Configuration
API_TOKEN = 'your-api-token'
COMPANY_DOMAIN = 'your-company'
BASE_URL = f'https://{COMPANY_DOMAIN}.pipedrive.com/api/v1'

# Create a deal
deal_data = {
    'title': 'Enterprise License - Acme Corp',
    'value': 50000,
    'currency': 'USD',
    'person_id': 123,  # Existing contact ID
    'org_id': 456,     # Existing organization ID
}

response = requests.post(
    f'{BASE_URL}/deals',
    params={'api_token': API_TOKEN},
    json=deal_data
)

deal = response.json()['data']
print(f"Deal created: {deal['id']} - {deal['title']}")

# Get pipeline overview
pipeline_response = requests.get(
    f'{BASE_URL}/deals',
    params={'api_token': API_TOKEN, 'status': 'open'}
)

deals = pipeline_response.json()['data']
total_value = sum(float(deal.get('value', 0)) for deal in deals)
print(f"Total pipeline value: ${total_value:,.2f}")
```

## Key Features Reference

- **Visual Pipeline**: Drag-and-drop deal management
- **Activity Scheduling**: Automated follow-up reminders
- **Custom Fields**: Flexible data model for any sales process
- **Email Integration**: Gmail, Outlook sync
- **Mobile Apps**: iOS and Android
- **Workflow Automation**: Triggered actions and notifications
- **Sales Reporting**: Pipeline analytics and forecasting
- **Integrations**: 300+ apps via marketplace
- **Smart Contact Data**: Automatic enrichment
- **Web Visitors**: Track website visitors

## References

- [Pipedrive API Documentation](https://developers.pipedrive.com/docs/api/v1)
- [API Reference](https://developers.pipedrive.com/docs/api/v1/rest)
- [Webhooks Guide](https://pipedrive.readme.io/docs/guide-for-webhooks)
- [OAuth Guide](https://pipedrive.readme.io/docs/marketplace-oauth-authorization)
- [Postman Collection](https://developers.pipedrive.com/docs/api/v1/postman-collections)

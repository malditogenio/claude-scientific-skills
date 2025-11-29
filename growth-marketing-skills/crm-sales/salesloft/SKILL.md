---
name: salesloft
description: "SalesLoft sales engagement platform. Cadences, email automation, call dialer, analytics, CRM sync, conversation intelligence, pipeline management."
---

# SalesLoft Integration

## Overview

SalesLoft is a comprehensive sales engagement platform that combines cadences, conversation intelligence, and pipeline management. This skill covers using the SalesLoft API to manage people, execute cadences, track activities, and analyze sales performance with emphasis on revenue operations and marketing-sales alignment.

## When to Use This Skill

- Multi-touch sales cadence management
- Email and call activity automation
- Sales conversation analytics
- Pipeline forecasting and management
- Marketing-to-sales lead handoff
- Sales team performance tracking
- Revenue attribution modeling
- A/B testing sales messaging
- CRM data synchronization

## Core Capabilities

### 1. People and Account Management

```python
import requests
import json
from datetime import datetime, timedelta
import pandas as pd

# SalesLoft API configuration
API_KEY = 'your-salesloft-api-key'
BASE_URL = 'https://api.salesloft.com/v2'

def api_request(endpoint, method='GET', data=None, params=None):
    """Make SalesLoft API request."""
    url = f'{BASE_URL}/{endpoint}'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    if method == 'GET':
        response = requests.get(url, headers=headers, params=params)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=data)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, json=data)
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers)

    return response.json()

# Create person
def create_person(email, first_name, last_name, title=None, account_id=None, custom_fields=None):
    """Create person with marketing attribution data."""
    person_data = {
        'email_address': email,
        'first_name': first_name,
        'last_name': last_name,
        'title': title,
        'account_id': account_id,
        'custom_fields': custom_fields or {}
    }

    result = api_request('people', method='POST', data=person_data)
    return result.get('data', {})

# Update person with marketing data
def update_person_attribution(person_id, attribution_data):
    """Update person with marketing attribution."""
    update_data = {
        'custom_fields': {
            'lead_source': attribution_data.get('source'),
            'utm_campaign': attribution_data.get('utm_campaign'),
            'utm_medium': attribution_data.get('utm_medium'),
            'utm_source': attribution_data.get('utm_source'),
            'lead_score': attribution_data.get('lead_score', 0),
            'mql_date': attribution_data.get('mql_date'),
            'first_touch_campaign': attribution_data.get('first_touch'),
            'last_touch_campaign': attribution_data.get('last_touch'),
            'marketing_qualified': True
        }
    }

    result = api_request(f'people/{person_id}', method='PUT', data=update_data)
    return result

# Get people by filter
def get_people(filter_params=None, per_page=100):
    """Get people with optional filters."""
    params = {'per_page': per_page}

    if filter_params:
        params.update(filter_params)

    result = api_request('people', params=params)
    return result.get('data', [])

# Create account
def create_account(name, domain=None, custom_fields=None):
    """Create account (company)."""
    account_data = {
        'name': name,
        'domain': domain,
        'custom_fields': custom_fields or {}
    }

    result = api_request('accounts', method='POST', data=account_data)
    return result.get('data', {})

# Get account by domain
def get_account_by_domain(domain):
    """Find account by domain."""
    params = {'domain': domain}
    result = api_request('accounts', params=params)

    accounts = result.get('data', [])
    return accounts[0] if accounts else None

# Example: Create person from MQL
account = get_account_by_domain('techcorp.com')
if not account:
    account = create_account(
        name='TechCorp Inc',
        domain='techcorp.com',
        custom_fields={'industry': 'Software', 'employee_count': 250}
    )

person = create_person(
    email='sarah.chen@techcorp.com',
    first_name='Sarah',
    last_name='Chen',
    title='VP of Marketing',
    account_id=account['id'],
    custom_fields={
        'lead_source': 'Website Demo',
        'utm_campaign': 'demo-request-q1',
        'lead_score': 85,
        'mql_date': datetime.now().isoformat(),
        'marketing_qualified': True
    }
)

print(f"Person created: {person['id']} - {person['email_address']}")
```

### 2. Cadences and Sequences

```python
# Get cadences
def get_cadences():
    """Get all active cadences."""
    result = api_request('cadences', params={'per_page': 100})
    return result.get('data', [])

# Add person to cadence
def add_to_cadence(person_id, cadence_id, user_id=None):
    """Add person to cadence."""
    cadence_membership_data = {
        'person_id': person_id,
        'cadence_id': cadence_id,
        'user_id': user_id  # Sales rep assigned
    }

    result = api_request('cadence_memberships', method='POST', data=cadence_membership_data)
    return result.get('data', {})

# Remove from cadence
def remove_from_cadence(cadence_membership_id):
    """Remove person from cadence."""
    result = api_request(f'cadence_memberships/{cadence_membership_id}', method='DELETE')
    return result

# Get cadence performance
def get_cadence_analytics(cadence_id):
    """Get performance metrics for cadence."""
    # Get cadence details
    cadence = api_request(f'cadences/{cadence_id}')['data']

    # Get cadence memberships
    memberships = api_request('cadence_memberships', params={
        'cadence_id': cadence_id,
        'per_page': 1000
    })['data']

    # Get steps for cadence
    steps = api_request('steps', params={
        'cadence_id': cadence_id
    })['data']

    # Calculate metrics
    total_people = len(memberships)
    active = len([m for m in memberships if m['current_state'] == 'active'])
    completed = len([m for m in memberships if m['current_state'] == 'completed'])
    bounced = len([m for m in memberships if m.get('bounced')])

    analytics = {
        'cadence_id': cadence_id,
        'cadence_name': cadence['name'],
        'total_steps': len(steps),
        'total_people': total_people,
        'active': active,
        'completed': completed,
        'bounced': bounced,
        'completion_rate': (completed / total_people * 100) if total_people > 0 else 0
    }

    return analytics

# Smart cadence routing
def route_mql_to_cadence(person_data):
    """Route marketing qualified lead to appropriate cadence."""
    custom_fields = person_data.get('custom_fields', {})
    lead_score = custom_fields.get('lead_score', 0)
    company_size = custom_fields.get('company_size', 'Unknown')

    # Define routing rules
    routing_rules = {
        'enterprise_hot': {
            'criteria': lambda: lead_score >= 80 and company_size == 'Enterprise',
            'cadence_id': 'cadence_enterprise_hot'
        },
        'hot_leads': {
            'criteria': lambda: lead_score >= 80,
            'cadence_id': 'cadence_hot_leads'
        },
        'warm_leads': {
            'criteria': lambda: 60 <= lead_score < 80,
            'cadence_id': 'cadence_warm_leads'
        },
        'nurture': {
            'criteria': lambda: lead_score < 60,
            'cadence_id': 'cadence_nurture'
        }
    }

    # Apply routing
    for segment, rule in routing_rules.items():
        if rule['criteria']():
            result = add_to_cadence(
                person_id=person_data['id'],
                cadence_id=rule['cadence_id']
            )

            print(f"Routed to {segment} cadence")
            return result

    return None

# Get step analytics
def get_step_performance(cadence_id):
    """Analyze performance by cadence step."""
    steps = api_request('steps', params={
        'cadence_id': cadence_id
    })['data']

    step_analytics = []

    for step in steps:
        # Get actions for this step
        actions = api_request('actions', params={
            'step_id': step['id'],
            'per_page': 1000
        })['data']

        completed = len([a for a in actions if a.get('status') == 'completed'])
        total = len(actions)

        step_analytics.append({
            'step_number': step['day'],
            'step_type': step['type'],
            'total_actions': total,
            'completed': completed,
            'completion_rate': (completed / total * 100) if total > 0 else 0
        })

    return pd.DataFrame(step_analytics)
```

### 3. Sales Activity Tracking

```python
# Get calls
def get_calls(person_id=None, user_id=None, start_date=None):
    """Get call activities."""
    params = {'per_page': 100}

    if person_id:
        params['person_id'] = person_id

    if user_id:
        params['user_id'] = user_id

    if start_date:
        params['created_at[gt]'] = start_date

    result = api_request('calls', params=params)
    return result.get('data', [])

# Get emails
def get_emails(person_id=None, user_id=None, start_date=None):
    """Get email activities."""
    params = {'per_page': 100}

    if person_id:
        params['person_id'] = person_id

    if user_id:
        params['user_id'] = user_id

    if start_date:
        params['updated_at[gt]'] = start_date

    result = api_request('emails', params=params)
    return result.get('data', [])

# Create note
def create_note(person_id, content, call_id=None):
    """Create note on person."""
    note_data = {
        'person_id': person_id,
        'content': content,
        'call_id': call_id
    }

    result = api_request('notes', method='POST', data=note_data)
    return result.get('data', {})

# Track email engagement
def get_email_engagement(person_id):
    """Get email engagement for person."""
    emails = get_emails(person_id=person_id)

    engagement = {
        'person_id': person_id,
        'total_emails': len(emails),
        'emails_sent': len([e for e in emails if e.get('status') == 'sent']),
        'emails_opened': len([e for e in emails if e.get('view_count', 0) > 0]),
        'emails_clicked': len([e for e in emails if e.get('click_count', 0) > 0]),
        'emails_replied': len([e for e in emails if e.get('reply_count', 0) > 0]),
        'total_opens': sum(e.get('view_count', 0) for e in emails),
        'total_clicks': sum(e.get('click_count', 0) for e in emails)
    }

    if engagement['emails_sent'] > 0:
        engagement['open_rate'] = (engagement['emails_opened'] / engagement['emails_sent']) * 100
        engagement['click_rate'] = (engagement['emails_clicked'] / engagement['emails_sent']) * 100
        engagement['reply_rate'] = (engagement['emails_replied'] / engagement['emails_sent']) * 100

    return engagement

# Get user activity summary
def get_rep_activity_summary(user_id, days=30):
    """Get activity summary for sales rep."""
    start_date = (datetime.now() - timedelta(days=days)).isoformat()

    # Get calls
    calls = get_calls(user_id=user_id, start_date=start_date)

    # Get emails
    emails = get_emails(user_id=user_id, start_date=start_date)

    summary = {
        'user_id': user_id,
        'period_days': days,
        'calls': {
            'total': len(calls),
            'completed': len([c for c in calls if c.get('disposition') == 'completed']),
            'no_answer': len([c for c in calls if c.get('disposition') == 'no_answer']),
            'voicemail': len([c for c in calls if c.get('disposition') == 'voicemail']),
            'total_duration': sum(c.get('duration', 0) for c in calls),
            'avg_duration': sum(c.get('duration', 0) for c in calls) / len(calls) if calls else 0
        },
        'emails': {
            'total_sent': len([e for e in emails if e.get('status') == 'sent']),
            'opened': len([e for e in emails if e.get('view_count', 0) > 0]),
            'clicked': len([e for e in emails if e.get('click_count', 0) > 0]),
            'replied': len([e for e in emails if e.get('reply_count', 0) > 0])
        }
    }

    # Calculate rates
    if summary['emails']['total_sent'] > 0:
        summary['emails']['open_rate'] = (summary['emails']['opened'] / summary['emails']['total_sent']) * 100
        summary['emails']['reply_rate'] = (summary['emails']['replied'] / summary['emails']['total_sent']) * 100

    if summary['calls']['total'] > 0:
        summary['calls']['connect_rate'] = (summary['calls']['completed'] / summary['calls']['total']) * 100

    return summary
```

### 4. Pipeline and Revenue Analytics

```python
# Get opportunities (called "deals" in SalesLoft)
def get_opportunities(stage=None):
    """Get pipeline opportunities."""
    params = {'per_page': 100}

    if stage:
        params['stage'] = stage

    # Note: SalesLoft integrates with CRM for opportunities
    # This accesses synced CRM data

    result = api_request('crm_activities', params=params)
    return result.get('data', [])

# Revenue attribution analysis
def analyze_revenue_attribution():
    """Analyze pipeline influenced by SalesLoft activities."""
    # Get all people with opportunities
    people = get_people({'has_opportunity': True})

    attribution_data = []

    for person in people:
        person_id = person['id']

        # Get email engagement
        email_engagement = get_email_engagement(person_id)

        # Get cadence memberships
        cadences = api_request('cadence_memberships', params={
            'person_id': person_id
        })['data']

        # Get opportunities (from CRM sync)
        # This would need CRM integration details

        attribution_data.append({
            'person_id': person_id,
            'email': person.get('email_address'),
            'company': person.get('account', {}).get('name'),
            'lead_source': person.get('custom_fields', {}).get('lead_source'),
            'lead_score': person.get('custom_fields', {}).get('lead_score', 0),
            'cadences_enrolled': len(cadences),
            'emails_sent': email_engagement['emails_sent'],
            'emails_opened': email_engagement['emails_opened'],
            'emails_replied': email_engagement['emails_replied'],
            'engagement_score': (
                email_engagement.get('open_rate', 0) * 0.3 +
                email_engagement.get('reply_rate', 0) * 0.7
            )
        })

    df = pd.DataFrame(attribution_data)

    # Calculate metrics
    metrics = {
        'total_people': len(df),
        'avg_lead_score': df['lead_score'].mean(),
        'avg_cadences_per_person': df['cadences_enrolled'].mean(),
        'avg_emails_per_person': df['emails_sent'].mean(),
        'avg_engagement_score': df['engagement_score'].mean()
    }

    # Attribution by lead source
    source_attribution = df.groupby('lead_source').agg({
        'person_id': 'count',
        'engagement_score': 'mean'
    }).rename(columns={
        'person_id': 'count',
        'engagement_score': 'avg_engagement'
    }).sort_values('count', ascending=False)

    metrics['by_lead_source'] = source_attribution.to_dict()

    return metrics

# A/B test cadences
def analyze_cadence_ab_test(cadence_a_id, cadence_b_id):
    """Compare performance between two cadences."""
    cadence_a = get_cadence_analytics(cadence_a_id)
    cadence_b = get_cadence_analytics(cadence_b_id)

    comparison = {
        'cadence_a': {
            'name': cadence_a['cadence_name'],
            'total_people': cadence_a['total_people'],
            'completion_rate': cadence_a['completion_rate'],
            'bounce_rate': (cadence_a['bounced'] / cadence_a['total_people'] * 100)
            if cadence_a['total_people'] > 0 else 0
        },
        'cadence_b': {
            'name': cadence_b['cadence_name'],
            'total_people': cadence_b['total_people'],
            'completion_rate': cadence_b['completion_rate'],
            'bounce_rate': (cadence_b['bounced'] / cadence_b['total_people'] * 100)
            if cadence_b['total_people'] > 0 else 0
        }
    }

    # Determine winner
    if cadence_a['completion_rate'] > cadence_b['completion_rate']:
        comparison['winner'] = 'A'
        comparison['improvement'] = (
            (cadence_a['completion_rate'] - cadence_b['completion_rate']) /
            cadence_b['completion_rate'] * 100
        ) if cadence_b['completion_rate'] > 0 else 0
    else:
        comparison['winner'] = 'B'
        comparison['improvement'] = (
            (cadence_b['completion_rate'] - cadence_a['completion_rate']) /
            cadence_a['completion_rate'] * 100
        ) if cadence_a['completion_rate'] > 0 else 0

    return comparison
```

## Installation

```bash
# SalesLoft doesn't have an official Python SDK
# Use requests library for API calls
uv pip install requests pandas python-dateutil
```

## Authentication

```python
import requests

# SalesLoft uses OAuth 2.0 or API Key authentication
API_KEY = 'your-salesloft-api-key'
BASE_URL = 'https://api.salesloft.com/v2'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Make request
response = requests.get(
    f'{BASE_URL}/people',
    headers=headers,
    params={'per_page': 10}
)
```

To get API key:
1. Log into SalesLoft
2. Go to Settings > API
3. Create API key
4. Copy the key

## Quick Start

```python
import requests

# Configuration
API_KEY = 'your-api-key'
BASE_URL = 'https://api.salesloft.com/v2'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Create a person
person_data = {
    'email_address': 'john.doe@acme.com',
    'first_name': 'John',
    'last_name': 'Doe',
    'title': 'VP of Sales',
    'custom_fields': {
        'lead_source': 'Marketing Campaign',
        'lead_score': 85
    }
}

response = requests.post(
    f'{BASE_URL}/people',
    headers=headers,
    json=person_data
)

person = response.json()['data']
print(f"Person created: {person['id']} - {person['email_address']}")

# Add to cadence
cadence_membership = {
    'person_id': person['id'],
    'cadence_id': 'your-cadence-id'
}

cadence_response = requests.post(
    f'{BASE_URL}/cadence_memberships',
    headers=headers,
    json=cadence_membership
)

print(f"Added to cadence: {cadence_response.json()['data']['id']}")
```

## Key Features Reference

- **Cadences**: Multi-step, multi-channel sales sequences
- **Rhythm**: AI-powered workflow automation
- **Conversations**: Call recording and analysis
- **Deals**: Pipeline management and forecasting
- **Analytics**: Revenue and activity insights
- **Integrations**: Salesforce, Dynamics, LinkedIn
- **Dialer**: Power dialer with local presence
- **Email**: Tracking, templates, A/B testing
- **Messenger**: In-app communication
- **Mobile Apps**: iOS and Android

## References

- [SalesLoft API Documentation](https://developers.salesloft.com/docs/api/)
- [API Reference](https://developers.salesloft.com/api.html#!/overview)
- [Authentication](https://developers.salesloft.com/docs/api/authentication/)
- [People API](https://developers.salesloft.com/api.html#!/People)
- [Cadences API](https://developers.salesloft.com/api.html#!/Cadences)
- [Rate Limits](https://developers.salesloft.com/docs/api/rate-limits/)

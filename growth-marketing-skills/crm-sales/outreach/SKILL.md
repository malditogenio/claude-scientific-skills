---
name: outreach
description: "Outreach sales engagement platform. Multi-channel sequences, email automation, call dialer, analytics, A/B testing, CRM sync, sales workflows."
---

# Outreach Integration

## Overview

Outreach is a leading sales engagement platform that enables multi-channel outreach sequences, sales automation, and performance analytics. This skill covers using the Outreach API to manage prospects, execute sequences, track engagement, and analyze sales effectiveness with focus on marketing-sales handoff and attribution.

## When to Use This Skill

- Multi-channel sales engagement (email, call, social)
- Automated prospect sequencing and cadences
- Sales team productivity optimization
- A/B testing email messaging and timing
- Lead handoff from marketing to sales
- Sales activity tracking and reporting
- Revenue attribution and pipeline analytics
- CRM synchronization and data enrichment
- Sales coaching and performance analysis

## Core Capabilities

### 1. Prospect and Contact Management

```python
import requests
import json
from datetime import datetime
import pandas as pd

# Outreach API configuration
API_KEY = 'your-outreach-api-key'
BASE_URL = 'https://api.outreach.io/api/v2'

def api_request(endpoint, method='GET', data=None, params=None):
    """Make Outreach API request."""
    url = f'{BASE_URL}/{endpoint}'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/vnd.api+json'
    }

    if method == 'GET':
        response = requests.get(url, headers=headers, params=params)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=data)
    elif method == 'PATCH':
        response = requests.patch(url, headers=headers, json=data)

    return response.json()

# Create prospect
def create_prospect(email, first_name, last_name, title=None, company=None, custom_fields=None):
    """Create prospect with marketing attribution."""
    prospect_data = {
        'data': {
            'type': 'prospect',
            'attributes': {
                'emails': [email],
                'firstName': first_name,
                'lastName': last_name,
                'title': title,
                'company': company,
                'customFields': custom_fields or {}
            }
        }
    }

    result = api_request('prospects', method='POST', data=prospect_data)
    return result['data']

# Update prospect with marketing data
def update_prospect_attribution(prospect_id, attribution_data):
    """Update prospect with marketing attribution fields."""
    update_data = {
        'data': {
            'type': 'prospect',
            'id': prospect_id,
            'attributes': {
                'customFields': {
                    'leadSource': attribution_data.get('source'),
                    'utmCampaign': attribution_data.get('utm_campaign'),
                    'utmMedium': attribution_data.get('utm_medium'),
                    'utmSource': attribution_data.get('utm_source'),
                    'leadScore': attribution_data.get('lead_score', 0),
                    'mqlDate': attribution_data.get('mql_date'),
                    'firstTouchCampaign': attribution_data.get('first_touch'),
                    'lastTouchCampaign': attribution_data.get('last_touch')
                }
            }
        }
    }

    result = api_request(f'prospects/{prospect_id}', method='PATCH', data=update_data)
    return result

# Get prospects by filter
def get_prospects(filter_params=None, page_size=50):
    """Get prospects with optional filters."""
    params = {
        'page[size]': page_size
    }

    if filter_params:
        for key, value in filter_params.items():
            params[f'filter[{key}]'] = value

    result = api_request('prospects', params=params)
    return result['data']

# Search prospects
def search_prospects(query):
    """Search prospects by name, email, or company."""
    params = {
        'filter[search]': query,
        'page[size]': 100
    }

    result = api_request('prospects', params=params)
    return result['data']

# Example: Create prospect from marketing qualified lead
prospect = create_prospect(
    email='sarah.johnson@techcorp.com',
    first_name='Sarah',
    last_name='Johnson',
    title='VP of Marketing',
    company='TechCorp Inc',
    custom_fields={
        'leadSource': 'Website Demo Request',
        'utmCampaign': 'product-demo-q1-2025',
        'utmSource': 'google',
        'utmMedium': 'cpc',
        'leadScore': 85,
        'mqlDate': datetime.now().isoformat()
    }
)

print(f"Prospect created: {prospect['id']} - {prospect['attributes']['emails'][0]}")
```

### 2. Sequences and Cadences

```python
# Get available sequences
def get_sequences():
    """Get all active sequences."""
    result = api_request('sequences', params={'page[size]': 100})
    return result['data']

# Add prospect to sequence
def add_to_sequence(prospect_id, sequence_id, mailbox_id=None):
    """Add prospect to outreach sequence."""
    sequence_state_data = {
        'data': {
            'type': 'sequenceState',
            'relationships': {
                'prospect': {
                    'data': {'type': 'prospect', 'id': prospect_id}
                },
                'sequence': {
                    'data': {'type': 'sequence', 'id': sequence_id}
                },
                'mailbox': {
                    'data': {'type': 'mailbox', 'id': mailbox_id}
                } if mailbox_id else None
            }
        }
    }

    result = api_request('sequenceStates', method='POST', data=sequence_state_data)
    return result['data']

# Remove prospect from sequence
def remove_from_sequence(sequence_state_id, reason='Unresponsive'):
    """Remove prospect from sequence."""
    update_data = {
        'data': {
            'type': 'sequenceState',
            'id': sequence_state_id,
            'attributes': {
                'state': 'finished',
                'stateChangedAt': datetime.now().isoformat(),
                'bounced': False,
                'replied': False,
                'errorReason': reason
            }
        }
    }

    result = api_request(f'sequenceStates/{sequence_state_id}', method='PATCH', data=update_data)
    return result

# Get sequence performance
def get_sequence_analytics(sequence_id):
    """Get performance metrics for sequence."""
    # Get sequence details
    sequence = api_request(f'sequences/{sequence_id}')

    # Get sequence states (prospects in sequence)
    states = api_request('sequenceStates', params={
        'filter[sequenceId]': sequence_id,
        'page[size]': 1000
    })

    total_enrolled = len(states['data'])
    active = len([s for s in states['data'] if s['attributes']['state'] == 'active'])
    finished = len([s for s in states['data'] if s['attributes']['state'] == 'finished'])
    replied = len([s for s in states['data'] if s['attributes'].get('replied')])
    bounced = len([s for s in states['data'] if s['attributes'].get('bounced')])

    analytics = {
        'sequence_id': sequence_id,
        'sequence_name': sequence['data']['attributes']['name'],
        'total_enrolled': total_enrolled,
        'active': active,
        'finished': finished,
        'replied': replied,
        'bounced': bounced,
        'reply_rate': (replied / total_enrolled * 100) if total_enrolled > 0 else 0,
        'bounce_rate': (bounced / total_enrolled * 100) if total_enrolled > 0 else 0
    }

    return analytics

# Automated lead routing to sequences
def route_mql_to_sequence(prospect_data):
    """Route marketing qualified lead to appropriate sequence based on criteria."""
    # Routing logic based on lead attributes
    lead_score = prospect_data.get('customFields', {}).get('leadScore', 0)
    company_size = prospect_data.get('customFields', {}).get('companySize')

    # Define sequence routing rules
    routing_rules = {
        'hot_leads': {
            'criteria': lambda p: p.get('customFields', {}).get('leadScore', 0) >= 80,
            'sequence_id': 'seq_hot_leads_123'
        },
        'warm_leads': {
            'criteria': lambda p: 60 <= p.get('customFields', {}).get('leadScore', 0) < 80,
            'sequence_id': 'seq_warm_leads_456'
        },
        'enterprise': {
            'criteria': lambda p: p.get('customFields', {}).get('companySize') == 'Enterprise',
            'sequence_id': 'seq_enterprise_789'
        }
    }

    # Apply routing
    for segment, rule in routing_rules.items():
        if rule['criteria'](prospect_data):
            result = add_to_sequence(
                prospect_id=prospect_data['id'],
                sequence_id=rule['sequence_id']
            )

            print(f"Routed to {segment} sequence: {result['id']}")
            return result

    return None
```

### 3. Sales Activity Tracking

```python
# Get mailings (emails sent)
def get_mailings(prospect_id=None, start_date=None):
    """Get email activity."""
    params = {'page[size]': 100}

    if prospect_id:
        params['filter[prospectId]'] = prospect_id

    if start_date:
        params['filter[createdAt][gte]'] = start_date

    result = api_request('mailings', params=params)
    return result['data']

# Get calls
def get_calls(prospect_id=None, start_date=None):
    """Get call activity."""
    params = {'page[size]': 100}

    if prospect_id:
        params['filter[prospectId]'] = prospect_id

    if start_date:
        params['filter[createdAt][gte]'] = start_date

    result = api_request('calls', params=params)
    return result['data']

# Create task
def create_task(prospect_id, assigned_to_id, subject, due_date, note=None):
    """Create follow-up task."""
    task_data = {
        'data': {
            'type': 'task',
            'attributes': {
                'subject': subject,
                'dueAt': due_date,
                'note': note,
                'taskType': 'call'
            },
            'relationships': {
                'prospect': {
                    'data': {'type': 'prospect', 'id': prospect_id}
                },
                'owner': {
                    'data': {'type': 'user', 'id': assigned_to_id}
                }
            }
        }
    }

    result = api_request('tasks', method='POST', data=task_data)
    return result['data']

# Get email engagement metrics
def get_email_engagement(mailing_id):
    """Get email open/click data."""
    mailing = api_request(f'mailings/{mailing_id}')

    engagement = {
        'mailing_id': mailing_id,
        'state': mailing['data']['attributes']['state'],
        'opened': mailing['data']['attributes'].get('clickCount', 0) > 0 or
                  mailing['data']['attributes'].get('openCount', 0) > 0,
        'clicks': mailing['data']['attributes'].get('clickCount', 0),
        'opens': mailing['data']['attributes'].get('openCount', 0),
        'replied': mailing['data']['attributes'].get('repliedAt') is not None,
        'bounced': mailing['data']['attributes'].get('bouncedAt') is not None
    }

    return engagement

# Get user (rep) activity summary
def get_rep_activity_summary(user_id, days=30):
    """Get activity summary for sales rep."""
    start_date = (datetime.now() - timedelta(days=days)).isoformat()

    # Get mailings
    mailings = get_mailings(start_date=start_date)
    user_mailings = [m for m in mailings if m['relationships'].get('user', {}).get('data', {}).get('id') == user_id]

    # Get calls
    calls = get_calls(start_date=start_date)
    user_calls = [c for c in calls if c['relationships'].get('user', {}).get('data', {}).get('id') == user_id]

    summary = {
        'user_id': user_id,
        'period_days': days,
        'emails': {
            'total_sent': len(user_mailings),
            'opened': len([m for m in user_mailings if m['attributes'].get('openCount', 0) > 0]),
            'clicked': len([m for m in user_mailings if m['attributes'].get('clickCount', 0) > 0]),
            'replied': len([m for m in user_mailings if m['attributes'].get('repliedAt')]),
            'bounced': len([m for m in user_mailings if m['attributes'].get('bouncedAt')])
        },
        'calls': {
            'total': len(user_calls),
            'connected': len([c for c in user_calls if c['attributes'].get('outcome') == 'connected']),
            'voicemail': len([c for c in user_calls if c['attributes'].get('outcome') == 'voicemail']),
            'no_answer': len([c for c in user_calls if c['attributes'].get('outcome') == 'no_answer'])
        }
    }

    # Calculate rates
    if summary['emails']['total_sent'] > 0:
        summary['emails']['open_rate'] = (summary['emails']['opened'] / summary['emails']['total_sent']) * 100
        summary['emails']['reply_rate'] = (summary['emails']['replied'] / summary['emails']['total_sent']) * 100

    if summary['calls']['total'] > 0:
        summary['calls']['connect_rate'] = (summary['calls']['connected'] / summary['calls']['total']) * 100

    return summary
```

### 4. Analytics and Attribution

```python
# Get opportunities (deals)
def get_opportunities(stage=None):
    """Get opportunities from Outreach."""
    params = {'page[size]': 100}

    if stage:
        params['filter[stage]'] = stage

    result = api_request('opportunities', params=params)
    return result['data']

# Attribution analysis
def analyze_outreach_attribution():
    """Analyze pipeline contribution from Outreach sequences."""
    # Get all opportunities
    opportunities = get_opportunities()

    # Get prospects associated with opportunities
    attribution_data = []

    for opp in opportunities:
        opp_id = opp['id']
        opp_attrs = opp['attributes']

        # Get associated prospect
        prospect_rel = opp['relationships'].get('prospect', {}).get('data')

        if prospect_rel:
            prospect_id = prospect_rel['id']
            prospect = api_request(f'prospects/{prospect_id}')['data']

            # Get sequence states for prospect
            sequence_states = api_request('sequenceStates', params={
                'filter[prospectId]': prospect_id
            })['data']

            # Get mailing history
            mailings = get_mailings(prospect_id=prospect_id)

            attribution_data.append({
                'opportunity_id': opp_id,
                'opportunity_name': opp_attrs.get('name'),
                'amount': opp_attrs.get('amount', 0),
                'stage': opp_attrs.get('stage'),
                'probability': opp_attrs.get('probability', 0),
                'prospect_email': prospect['attributes']['emails'][0] if prospect['attributes'].get('emails') else None,
                'sequences_touched': len(sequence_states),
                'emails_received': len(mailings),
                'lead_source': prospect['attributes'].get('customFields', {}).get('leadSource'),
                'first_touch': prospect['attributes'].get('customFields', {}).get('firstTouchCampaign'),
                'lead_score': prospect['attributes'].get('customFields', {}).get('leadScore', 0)
            })

    df = pd.DataFrame(attribution_data)

    # Calculate metrics
    metrics = {
        'total_opportunities': len(df),
        'total_pipeline_value': df['amount'].sum(),
        'weighted_pipeline': (df['amount'] * df['probability'] / 100).sum(),
        'avg_sequences_per_opp': df['sequences_touched'].mean(),
        'avg_emails_per_opp': df['emails_received'].mean(),
        'avg_lead_score': df['lead_score'].mean()
    }

    # Attribution by lead source
    source_attribution = df.groupby('lead_source').agg({
        'opportunity_id': 'count',
        'amount': 'sum'
    }).rename(columns={
        'opportunity_id': 'opportunities',
        'amount': 'pipeline_value'
    }).sort_values('pipeline_value', ascending=False)

    metrics['by_lead_source'] = source_attribution.to_dict()

    return metrics

# A/B test analysis
def analyze_sequence_ab_test(sequence_a_id, sequence_b_id):
    """Compare performance between two sequences."""
    seq_a_metrics = get_sequence_analytics(sequence_a_id)
    seq_b_metrics = get_sequence_analytics(sequence_b_id)

    comparison = {
        'sequence_a': {
            'name': seq_a_metrics['sequence_name'],
            'enrolled': seq_a_metrics['total_enrolled'],
            'reply_rate': seq_a_metrics['reply_rate'],
            'bounce_rate': seq_a_metrics['bounce_rate']
        },
        'sequence_b': {
            'name': seq_b_metrics['sequence_name'],
            'enrolled': seq_b_metrics['total_enrolled'],
            'reply_rate': seq_b_metrics['reply_rate'],
            'bounce_rate': seq_b_metrics['bounce_rate']
        },
        'winner': None,
        'improvement': 0
    }

    # Determine winner by reply rate
    if seq_a_metrics['reply_rate'] > seq_b_metrics['reply_rate']:
        comparison['winner'] = 'A'
        comparison['improvement'] = (
            (seq_a_metrics['reply_rate'] - seq_b_metrics['reply_rate']) /
            seq_b_metrics['reply_rate'] * 100
        ) if seq_b_metrics['reply_rate'] > 0 else 0
    else:
        comparison['winner'] = 'B'
        comparison['improvement'] = (
            (seq_b_metrics['reply_rate'] - seq_a_metrics['reply_rate']) /
            seq_a_metrics['reply_rate'] * 100
        ) if seq_a_metrics['reply_rate'] > 0 else 0

    return comparison
```

## Installation

```bash
# Outreach doesn't have an official Python SDK
# Use requests library for API calls
uv pip install requests pandas python-dateutil
```

## Authentication

```python
import requests

# Outreach uses OAuth 2.0 authentication
# For API access, you'll need to obtain an access token

API_KEY = 'your-oauth-access-token'
BASE_URL = 'https://api.outreach.io/api/v2'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/vnd.api+json'
}

# Make request
response = requests.get(
    f'{BASE_URL}/prospects',
    headers=headers,
    params={'page[size]': 10}
)
```

To get OAuth token:
1. Log into Outreach
2. Go to Settings > Integrations > API
3. Create OAuth application
4. Use OAuth flow to get access token
5. Or use Application Token for server-to-server

## Quick Start

```python
import requests

# Configuration
API_KEY = 'your-access-token'
BASE_URL = 'https://api.outreach.io/api/v2'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/vnd.api+json'
}

# Create a prospect
prospect_data = {
    'data': {
        'type': 'prospect',
        'attributes': {
            'emails': ['john.doe@acme.com'],
            'firstName': 'John',
            'lastName': 'Doe',
            'title': 'VP of Sales',
            'company': 'Acme Corp'
        }
    }
}

response = requests.post(
    f'{BASE_URL}/prospects',
    headers=headers,
    json=prospect_data
)

prospect = response.json()['data']
print(f"Prospect created: {prospect['id']}")

# Add to sequence
sequence_state_data = {
    'data': {
        'type': 'sequenceState',
        'relationships': {
            'prospect': {
                'data': {'type': 'prospect', 'id': prospect['id']}
            },
            'sequence': {
                'data': {'type': 'sequence', 'id': 'your-sequence-id'}
            }
        }
    }
}

seq_response = requests.post(
    f'{BASE_URL}/sequenceStates',
    headers=headers,
    json=sequence_state_data
)

print(f"Added to sequence: {seq_response.json()['data']['id']}")
```

## Key Features Reference

- **Multi-Channel Sequences**: Email, call, SMS, social in one workflow
- **A/B Testing**: Test subject lines, messaging, timing
- **Email Tracking**: Open, click, reply detection
- **Built-in Dialer**: Power dialer and click-to-call
- **CRM Sync**: Salesforce, Microsoft Dynamics bidirectional sync
- **Analytics**: Revenue attribution, rep performance
- **Triggers**: Automated actions based on prospect behavior
- **Snippets**: Reusable email templates
- **Governance**: Compliance and approval workflows
- **Kaia (AI)**: AI-powered email assistance

## References

- [Outreach API Documentation](https://api.outreach.io/api/v2/docs)
- [API Authentication](https://api.outreach.io/api/v2/docs#authentication)
- [Prospects API](https://api.outreach.io/api/v2/docs#prospect)
- [Sequences API](https://api.outreach.io/api/v2/docs#sequence)
- [Mailings API](https://api.outreach.io/api/v2/docs#mailing)
- [Rate Limits](https://api.outreach.io/api/v2/docs#rate-limiting)

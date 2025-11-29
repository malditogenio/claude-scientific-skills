---
name: close-crm
description: "Close CRM for sales communication. Built-in calling, SMS, email sequences, lead management, pipeline tracking, sales automation, reporting."
---

# Close CRM Integration

## Overview

Close is a CRM built for high-velocity sales teams with integrated calling, email, and SMS. This skill covers using the Close API to manage leads, execute multi-channel outreach sequences, track communication, and analyze sales performance with focus on outbound sales and lead response optimization.

## When to Use This Skill

- High-velocity outbound sales operations
- Multi-channel sales outreach (email, call, SMS)
- Inside sales team management
- Lead response time optimization
- Sales communication tracking and analytics
- Automated follow-up sequences
- Call recording and analysis
- Sales productivity and performance tracking

## Core Capabilities

### 1. Lead and Contact Management

```python
import requests
import json
from datetime import datetime, timedelta

# Close API configuration
API_KEY = 'your-close-api-key'
BASE_URL = 'https://api.close.com/api/v1'

def api_request(endpoint, method='GET', data=None):
    """Make Close API request with authentication."""
    url = f'{BASE_URL}/{endpoint}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {API_KEY}'  # API key is used as username in basic auth
    }

    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=data)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, json=data)
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers)

    return response.json()

# Create lead with contacts
def create_lead(company_name, contacts, custom_fields=None):
    """Create lead with associated contacts and marketing data."""
    lead_data = {
        'name': company_name,
        'contacts': contacts,
        'custom': custom_fields or {}
    }

    result = api_request('lead/', method='POST', data=lead_data)
    return result

# Create contact within lead
def add_contact_to_lead(lead_id, name, emails=None, phones=None, title=None):
    """Add contact to existing lead."""
    contact_data = {
        'lead_id': lead_id,
        'name': name,
        'title': title,
        'emails': emails or [],
        'phones': phones or []
    }

    result = api_request('contact/', method='POST', data=contact_data)
    return result['id']

# Update lead with marketing attribution
def update_lead_with_attribution(lead_id, attribution_data):
    """Update lead with marketing source and campaign data."""
    custom_fields = {
        'custom.cf_LeadSource': attribution_data.get('source'),
        'custom.cf_UTMCampaign': attribution_data.get('utm_campaign'),
        'custom.cf_UTMMedium': attribution_data.get('utm_medium'),
        'custom.cf_UTMSource': attribution_data.get('utm_source'),
        'custom.cf_FirstTouchDate': attribution_data.get('first_touch_date'),
        'custom.cf_LeadScore': attribution_data.get('lead_score', 0),
        'custom.cf_MQLDate': attribution_data.get('mql_date')
    }

    result = api_request(f'lead/{lead_id}/', method='PUT', data=custom_fields)
    return result

# Search leads
def search_leads(query=None, status_id=None, custom_filters=None):
    """Search leads with filters."""
    params = {}

    if query:
        params['query'] = f'name:"{query}"'

    if status_id:
        params['status_id'] = status_id

    if custom_filters:
        # Example: custom.cf_LeadScore >= 70
        for field, value in custom_filters.items():
            params[f'custom.{field}'] = value

    result = api_request('lead/', method='GET')
    return result.get('data', [])

# Get high-value leads
def get_qualified_leads(min_score=70):
    """Get leads with score above threshold."""
    # Use Close's query syntax
    query_params = f'custom.cf_LeadScore >= {min_score}'

    result = api_request(f'lead/?query={query_params}')
    return result.get('data', [])

# Example: Create lead from marketing form
lead = create_lead(
    company_name='TechStartup Inc',
    contacts=[
        {
            'name': 'Mike Roberts',
            'title': 'CEO',
            'emails': [{'email': 'mike@techstartup.io', 'type': 'office'}],
            'phones': [{'phone': '+14155551234', 'type': 'office'}]
        }
    ],
    custom_fields={
        'cf_LeadSource': 'Website Demo',
        'cf_UTMCampaign': 'demo-request-q1',
        'cf_UTMSource': 'google',
        'cf_UTMMedium': 'cpc',
        'cf_LeadScore': 85,
        'cf_MQLDate': datetime.now().isoformat()
    }
)

print(f"Lead created: {lead['id']} - {lead['name']}")
```

### 2. Pipeline and Opportunity Management

```python
import pandas as pd

# Create opportunity
def create_opportunity(lead_id, value, confidence=None, note=None):
    """Create opportunity for a lead."""
    opp_data = {
        'lead_id': lead_id,
        'value': value,
        'value_period': 'one_time',  # one_time, monthly, annual
        'confidence': confidence or 0,  # 0-100
        'note': note,
        'date_won': None
    }

    result = api_request('opportunity/', method='POST', data=opp_data)
    return result

# Update opportunity stage
def update_opportunity_status(opportunity_id, status_id, confidence=None):
    """Update opportunity status and win probability."""
    opp_data = {
        'status_id': status_id
    }

    if confidence is not None:
        opp_data['confidence'] = confidence

    result = api_request(f'opportunity/{opportunity_id}/', method='PUT', data=opp_data)
    return result

# Get pipeline analytics
def get_pipeline_metrics():
    """Analyze pipeline health and forecasting."""
    # Get all opportunities
    opps = api_request('opportunity/')['data']

    if not opps:
        return {}

    df = pd.DataFrame([{
        'id': opp['id'],
        'lead_id': opp['lead_id'],
        'value': float(opp.get('value', 0)),
        'confidence': int(opp.get('confidence', 0)),
        'status': opp.get('status_label', 'Unknown'),
        'status_type': opp.get('status_type', 'active'),
        'date_created': opp.get('date_created'),
        'date_won': opp.get('date_won'),
        'user_id': opp.get('user_id')
    } for opp in opps])

    # Calculate metrics
    active_opps = df[df['status_type'] == 'active']
    won_opps = df[df['status_type'] == 'won']
    lost_opps = df[df['status_type'] == 'lost']

    metrics = {
        'total_opportunities': len(df),
        'active_opportunities': len(active_opps),
        'total_pipeline_value': active_opps['value'].sum(),
        'weighted_pipeline': (active_opps['value'] * active_opps['confidence'] / 100).sum(),
        'won_count': len(won_opps),
        'won_value': won_opps['value'].sum(),
        'lost_count': len(lost_opps),
        'win_rate': len(won_opps) / (len(won_opps) + len(lost_opps)) * 100
        if (len(won_opps) + len(lost_opps)) > 0 else 0,
        'average_deal_size': active_opps['value'].mean() if len(active_opps) > 0 else 0
    }

    # Rep performance
    rep_performance = active_opps.groupby('user_id').agg({
        'id': 'count',
        'value': 'sum'
    }).rename(columns={'id': 'opportunity_count', 'value': 'pipeline_value'})

    metrics['rep_performance'] = rep_performance.to_dict()

    return metrics

# Example usage
pipeline = get_pipeline_metrics()
print(f"Pipeline Value: ${pipeline['total_pipeline_value']:,.2f}")
print(f"Weighted Pipeline: ${pipeline['weighted_pipeline']:,.2f}")
print(f"Win Rate: {pipeline['win_rate']:.1f}%")
```

### 3. Sales Activity and Communication Tracking

```python
# Create call activity
def log_call(lead_id, contact_id, direction, duration, disposition, note=None, recording_url=None):
    """Log a call activity."""
    call_data = {
        'lead_id': lead_id,
        'contact_id': contact_id,
        'direction': direction,  # 'inbound' or 'outbound'
        'duration': duration,  # seconds
        'disposition': disposition,  # 'connected', 'voicemail', 'no_answer', etc.
        'note': note,
        'recording_url': recording_url
    }

    result = api_request('activity/call/', method='POST', data=call_data)
    return result['id']

# Send email
def send_email(lead_id, contact_id, subject, body, template_id=None, thread_id=None):
    """Send email to contact."""
    email_data = {
        'lead_id': lead_id,
        'contact_id': contact_id,
        'subject': subject,
        'body_html': body,
        'status': 'outbox',  # Will be sent
        'template_id': template_id,
        'thread_id': thread_id  # For email threading
    }

    result = api_request('activity/email/', method='POST', data=email_data)
    return result['id']

# Send SMS
def send_sms(lead_id, contact_id, text, local_phone=None):
    """Send SMS to contact."""
    sms_data = {
        'lead_id': lead_id,
        'contact_id': contact_id,
        'text': text,
        'local_phone': local_phone,  # Your Close phone number
        'status': 'outbox'
    }

    result = api_request('activity/sms/', method='POST', data=sms_data)
    return result['id']

# Get activity timeline for lead
def get_lead_activity_timeline(lead_id):
    """Get all activities for a lead."""
    activities = api_request(f'activity/?lead_id={lead_id}')
    return activities.get('data', [])

# Track email opens and clicks
def get_email_engagement(email_id):
    """Get email engagement metrics."""
    email = api_request(f'activity/email/{email_id}/')

    engagement = {
        'email_id': email_id,
        'status': email.get('status'),
        'opens': email.get('opens', 0),
        'clicks': email.get('clicks', 0),
        'first_opened': email.get('date_opened'),
        'first_clicked': email.get('date_clicked')
    }

    return engagement

# Create task/reminder
def create_task(lead_id, assigned_to, text, due_date, task_type='lead'):
    """Create follow-up task."""
    task_data = {
        'lead_id': lead_id,
        'assigned_to': assigned_to,
        'text': text,
        'due_date': due_date,
        'is_complete': False,
        'object_type': task_type
    }

    result = api_request('task/', method='POST', data=task_data)
    return result['id']

# Get sales rep activity summary
def get_rep_activity_summary(user_id, days=30):
    """Get activity summary for sales rep."""
    start_date = (datetime.now() - timedelta(days=days)).isoformat()

    # Get calls
    calls = api_request(f'activity/call/?user_id={user_id}&date_created__gte={start_date}')
    call_data = calls.get('data', [])

    # Get emails
    emails = api_request(f'activity/email/?user_id={user_id}&date_created__gte={start_date}')
    email_data = emails.get('data', [])

    # Get SMS
    sms = api_request(f'activity/sms/?user_id={user_id}&date_created__gte={start_date}')
    sms_data = sms.get('data', [])

    summary = {
        'calls': {
            'total': len(call_data),
            'connected': len([c for c in call_data if c.get('disposition') == 'connected']),
            'voicemail': len([c for c in call_data if c.get('disposition') == 'voicemail']),
            'total_duration': sum(c.get('duration', 0) for c in call_data),
            'average_duration': sum(c.get('duration', 0) for c in call_data) / len(call_data)
            if call_data else 0
        },
        'emails': {
            'total': len(email_data),
            'sent': len([e for e in email_data if e.get('status') == 'sent']),
            'opened': len([e for e in email_data if e.get('opens', 0) > 0]),
            'clicked': len([e for e in email_data if e.get('clicks', 0) > 0]),
            'open_rate': len([e for e in email_data if e.get('opens', 0) > 0]) / len(email_data) * 100
            if email_data else 0
        },
        'sms': {
            'total': len(sms_data),
            'sent': len([s for s in sms_data if s.get('status') == 'sent'])
        }
    }

    return summary
```

### 4. Sales Sequences and Automation

```python
# Create email sequence template
def create_sequence_template(name, steps):
    """Create multi-step email sequence."""
    # Note: Close sequences are created via UI
    # This demonstrates the structure

    sequence = {
        'name': name,
        'steps': steps  # List of sequence steps
    }

    # Each step structure:
    # {
    #     'delay_days': 0,  # Days after previous step
    #     'type': 'email',  # email, call, sms
    #     'template_id': 'template_xxx',
    #     'subject': 'Email subject',
    #     'body': 'Email body with {{variables}}'
    # }

    return sequence

# Enroll lead in sequence
def enroll_in_sequence(lead_id, sequence_id, contact_id=None):
    """Enroll lead/contact in sales sequence."""
    enrollment_data = {
        'lead_id': lead_id,
        'sequence_id': sequence_id,
        'contact_id': contact_id,
        'sender_account_id': 'your_account_id'
    }

    result = api_request('sequence_subscription/', method='POST', data=enrollment_data)
    return result

# Automated lead response workflow
def auto_respond_to_new_lead(lead_id):
    """Automatically respond to new inbound lead."""
    # 1. Get lead details
    lead = api_request(f'lead/{lead_id}/')

    # 2. Send immediate response email
    if lead.get('contacts'):
        contact = lead['contacts'][0]

        email_id = send_email(
            lead_id=lead_id,
            contact_id=contact['id'],
            subject='Thanks for your interest!',
            body='''
            <p>Hi {name},</p>
            <p>Thanks for reaching out! I'll be in touch within the next hour to discuss how we can help.</p>
            <p>Best regards,<br>Sales Team</p>
            '''.format(name=contact.get('name', 'there')),
            template_id='quick_response_template'
        )

    # 3. Create immediate follow-up task
    task_id = create_task(
        lead_id=lead_id,
        assigned_to='user_xxx',  # Round-robin or assigned rep
        text='New inbound lead - Call within 5 minutes',
        due_date=datetime.now().isoformat(),
        task_type='lead'
    )

    # 4. Schedule follow-up sequence if no response
    # This would be triggered by workflow automation

    return {
        'email_sent': email_id,
        'task_created': task_id
    }
```

## Installation

```bash
# Close doesn't have an official Python SDK
# Use requests library for API calls
uv pip install requests pandas python-dateutil
```

## Authentication

```python
import requests
import base64

# Close uses API key authentication (HTTP Basic Auth)
API_KEY = 'your-close-api-key'

# Encode API key for Basic Auth (API key is username, password is empty)
auth_string = base64.b64encode(f'{API_KEY}:'.encode()).decode()

headers = {
    'Authorization': f'Basic {auth_string}',
    'Content-Type': 'application/json'
}

# Make request
response = requests.get(
    'https://api.close.com/api/v1/lead/',
    headers=headers
)
```

To get API key:
1. Log into Close
2. Go to Settings > API Keys
3. Create new API key
4. Copy the key (starts with `api_`)

## Quick Start

```python
import requests
import base64

# Setup
API_KEY = 'your-api-key'
BASE_URL = 'https://api.close.com/api/v1'

# Prepare auth
auth_string = base64.b64encode(f'{API_KEY}:'.encode()).decode()
headers = {
    'Authorization': f'Basic {auth_string}',
    'Content-Type': 'application/json'
}

# Create a lead
lead_data = {
    'name': 'Acme Corporation',
    'contacts': [
        {
            'name': 'John Smith',
            'title': 'CEO',
            'emails': [{'email': 'john@acme.com', 'type': 'office'}],
            'phones': [{'phone': '+14155551234', 'type': 'office'}]
        }
    ],
    'custom': {
        'cf_LeadSource': 'Inbound Demo Request',
        'cf_LeadScore': 85
    }
}

response = requests.post(
    f'{BASE_URL}/lead/',
    headers=headers,
    json=lead_data
)

lead = response.json()
print(f"Lead created: {lead['id']} - {lead['name']}")

# Make a call
call_data = {
    'lead_id': lead['id'],
    'direction': 'outbound',
    'disposition': 'connected',
    'duration': 420,  # 7 minutes
    'note': 'Discussed pricing and next steps. Very interested!'
}

call_response = requests.post(
    f'{BASE_URL}/activity/call/',
    headers=headers,
    json=call_data
)

print(f"Call logged: {call_response.json()['id']}")
```

## Key Features Reference

- **Built-in Communication**: Native calling, email, SMS
- **Power Dialer**: Automated calling workflows
- **Email Sequences**: Multi-step automated follow-ups
- **Smart Views**: Customizable lead filters and segments
- **Predictive Dialer**: AI-powered call routing
- **Call Recording**: Automatic recording and transcription
- **Email Tracking**: Open and click tracking
- **SMS Messaging**: Two-way text messaging
- **Reporting**: Activity and pipeline analytics
- **Mobile Apps**: iOS and Android with full functionality

## References

- [Close API Documentation](https://developer.close.com/)
- [API Reference](https://developer.close.com/resources/getting-started/)
- [Webhooks](https://developer.close.com/resources/webhooks/)
- [Custom Fields](https://developer.close.com/resources/custom-fields/)
- [Rate Limits](https://developer.close.com/resources/rate-limiting/)

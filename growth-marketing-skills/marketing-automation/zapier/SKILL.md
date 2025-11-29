---
name: zapier
description: "Zapier workflow automation platform. Connect 6000+ apps, automate workflows, triggers and actions, multi-step Zaps, data transformation, no-code automation."
---

# Zapier Integration

## Overview

Zapier is a workflow automation platform that connects over 6,000 apps to automate repetitive tasks without coding. This skill covers using Python to interact with Zapier, create integrations, and trigger workflows programmatically.

## When to Use This Skill

- Automating workflows between different apps
- Triggering actions based on events
- Data synchronization across platforms
- No-code/low-code automation
- Integration development
- Webhook-based workflows
- Multi-step automated processes
- Data transformation and routing

## Core Capabilities

### 1. Webhooks by Zapier

```python
import requests
import json

# Zapier Webhook configuration
WEBHOOK_URL = 'https://hooks.zapier.com/hooks/catch/YOUR_HOOK_ID/'

# Send data to Zapier webhook
def trigger_zapier_webhook(data):
    response = requests.post(
        WEBHOOK_URL,
        json=data,
        headers={'Content-Type': 'application/json'}
    )

    return {
        'status_code': response.status_code,
        'response': response.text
    }

# Example: Trigger new lead workflow
lead_data = {
    'email': 'newlead@example.com',
    'first_name': 'John',
    'last_name': 'Doe',
    'company': 'Acme Corp',
    'lead_source': 'Website Form',
    'lead_score': 75
}

result = trigger_zapier_webhook(lead_data)
print(f"Webhook triggered: {result['status_code']}")

# Example: Trigger order confirmation
order_data = {
    'order_id': 'ORDER-12345',
    'customer_email': 'customer@example.com',
    'total': 249.97,
    'items': [
        {'name': 'Product A', 'quantity': 2, 'price': 99.99},
        {'name': 'Product B', 'quantity': 1, 'price': 49.99}
    ],
    'status': 'completed'
}

trigger_zapier_webhook(order_data)

# Example: Trigger customer support ticket
ticket_data = {
    'ticket_id': 'TICKET-789',
    'customer_email': 'support@example.com',
    'priority': 'high',
    'subject': 'Product integration issue',
    'description': 'Customer needs help with API integration'
}

trigger_zapier_webhook(ticket_data)
```

### 2. Batch Webhook Triggers

```python
# Send multiple records to Zapier
def batch_trigger_webhook(webhook_url, records):
    results = []

    for record in records:
        response = requests.post(
            webhook_url,
            json=record,
            headers={'Content-Type': 'application/json'}
        )

        results.append({
            'record_id': record.get('id'),
            'status': response.status_code,
            'success': response.status_code == 200
        })

    return results

# Example: Sync contacts to CRM
contacts = [
    {
        'id': 1,
        'email': 'user1@example.com',
        'name': 'Alice Smith',
        'company': 'Tech Co'
    },
    {
        'id': 2,
        'email': 'user2@example.com',
        'name': 'Bob Johnson',
        'company': 'Marketing Inc'
    },
    {
        'id': 3,
        'email': 'user3@example.com',
        'name': 'Carol White',
        'company': 'Sales Corp'
    }
]

results = batch_trigger_webhook(WEBHOOK_URL, contacts)

successful = sum(1 for r in results if r['success'])
print(f"Successfully synced {successful}/{len(contacts)} contacts")
```

### 3. Custom App Integration (Platform API)

```python
# Note: Zapier Platform API requires authentication
# This is for developers building Zapier integrations

ZAPIER_API_URL = 'https://api.zapier.com/v1'
API_KEY = 'your-zapier-api-key'

headers = {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

# Get Zaps (requires Zapier Platform subscription)
def get_zaps():
    url = f'{ZAPIER_API_URL}/zaps'

    response = requests.get(url, headers=headers)
    return response.json()

# Get Zap history
def get_zap_history(zap_id):
    url = f'{ZAPIER_API_URL}/zaps/{zap_id}/history'

    response = requests.get(url, headers=headers)
    return response.json()

# Example usage (requires appropriate permissions)
# zaps = get_zaps()
# print(f"Active Zaps: {len(zaps)}")
```

### 4. Common Workflow Patterns

```python
# Pattern 1: New lead to CRM workflow
def sync_lead_to_crm(lead_data, crm_webhook_url):
    # Transform data for CRM
    crm_payload = {
        'contact': {
            'email': lead_data['email'],
            'first_name': lead_data['first_name'],
            'last_name': lead_data['last_name'],
            'company': lead_data['company']
        },
        'source': 'Website',
        'timestamp': lead_data.get('created_at')
    }

    # Trigger Zapier webhook
    response = requests.post(crm_webhook_url, json=crm_payload)
    return response.status_code == 200

# Pattern 2: E-commerce order to fulfillment
def process_order_workflow(order, fulfillment_webhook_url):
    # Prepare order for fulfillment system
    fulfillment_payload = {
        'order_number': order['order_id'],
        'customer': {
            'email': order['customer_email'],
            'shipping_address': order['shipping_address']
        },
        'items': order['items'],
        'shipping_method': order.get('shipping_method', 'standard')
    }

    # Trigger fulfillment workflow
    response = requests.post(fulfillment_webhook_url, json=fulfillment_payload)
    return response.status_code == 200

# Pattern 3: Event-driven notifications
def send_event_notification(event_type, event_data, notification_webhook_url):
    # Format notification
    notification = {
        'event_type': event_type,
        'data': event_data,
        'notification_channels': ['email', 'slack'],
        'priority': event_data.get('priority', 'normal')
    }

    # Trigger notification workflow
    response = requests.post(notification_webhook_url, json=notification)
    return response.status_code == 200

# Example: Use patterns
lead = {
    'email': 'prospect@example.com',
    'first_name': 'Jane',
    'last_name': 'Doe',
    'company': 'Enterprise Co',
    'created_at': '2025-01-15T10:00:00Z'
}

sync_lead_to_crm(lead, 'https://hooks.zapier.com/hooks/catch/CRM_HOOK/')
```

### 5. Error Handling and Retry Logic

```python
import time

# Trigger webhook with retry logic
def trigger_with_retry(webhook_url, data, max_retries=3, retry_delay=5):
    for attempt in range(max_retries):
        try:
            response = requests.post(
                webhook_url,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )

            if response.status_code == 200:
                return {
                    'success': True,
                    'attempt': attempt + 1,
                    'response': response.text
                }

            # If not successful, wait and retry
            if attempt < max_retries - 1:
                time.sleep(retry_delay)

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                return {
                    'success': False,
                    'error': str(e),
                    'attempts': max_retries
                }

    return {
        'success': False,
        'error': 'Max retries exceeded',
        'attempts': max_retries
    }

# Example: Reliable webhook trigger
result = trigger_with_retry(
    WEBHOOK_URL,
    {'important_data': 'must_be_delivered'},
    max_retries=5,
    retry_delay=10
)

if result['success']:
    print(f"Data delivered successfully after {result['attempt']} attempt(s)")
else:
    print(f"Failed to deliver data: {result['error']}")
```

### 6. Data Transformation for Zapier

```python
# Transform data for different Zapier integrations
def transform_for_salesforce(contact_data):
    return {
        'FirstName': contact_data.get('first_name'),
        'LastName': contact_data.get('last_name'),
        'Email': contact_data.get('email'),
        'Company': contact_data.get('company'),
        'LeadSource': 'Website',
        'Status': 'Open - Not Contacted'
    }

def transform_for_hubspot(contact_data):
    return {
        'properties': {
            'email': contact_data.get('email'),
            'firstname': contact_data.get('first_name'),
            'lastname': contact_data.get('last_name'),
            'company': contact_data.get('company'),
            'lifecyclestage': 'lead'
        }
    }

def transform_for_mailchimp(contact_data):
    return {
        'email_address': contact_data.get('email'),
        'status': 'subscribed',
        'merge_fields': {
            'FNAME': contact_data.get('first_name'),
            'LNAME': contact_data.get('last_name'),
            'COMPANY': contact_data.get('company')
        }
    }

# Example: Send to multiple platforms
contact = {
    'email': 'multi@example.com',
    'first_name': 'Multi',
    'last_name': 'Platform',
    'company': 'Integration Co'
}

# Transform and send to each platform
salesforce_data = transform_for_salesforce(contact)
trigger_zapier_webhook(salesforce_data)  # Salesforce Zap

hubspot_data = transform_for_hubspot(contact)
trigger_zapier_webhook(hubspot_data)  # HubSpot Zap

mailchimp_data = transform_for_mailchimp(contact)
trigger_zapier_webhook(mailchimp_data)  # Mailchimp Zap
```

### 7. Scheduled and Conditional Workflows

```python
from datetime import datetime, timedelta

# Schedule-based trigger
def should_send_weekly_report():
    # Send report every Monday at 9 AM
    now = datetime.now()
    return now.weekday() == 0 and now.hour == 9

def trigger_weekly_report(report_webhook_url):
    if should_send_weekly_report():
        report_data = {
            'report_type': 'weekly_summary',
            'week_start': (datetime.now() - timedelta(days=7)).isoformat(),
            'week_end': datetime.now().isoformat(),
            'generate_pdf': True,
            'send_to': ['team@example.com']
        }

        return trigger_zapier_webhook(report_data)

    return None

# Conditional workflow
def conditional_workflow(customer_data, webhook_url):
    # Different workflows based on customer value
    lifetime_value = customer_data.get('lifetime_value', 0)

    if lifetime_value > 10000:
        # VIP customer workflow
        payload = {
            'customer': customer_data,
            'workflow_type': 'vip_onboarding',
            'assign_to': 'account_manager',
            'priority': 'high'
        }
    elif lifetime_value > 1000:
        # Premium customer workflow
        payload = {
            'customer': customer_data,
            'workflow_type': 'premium_onboarding',
            'assign_to': 'sales_team',
            'priority': 'medium'
        }
    else:
        # Standard customer workflow
        payload = {
            'customer': customer_data,
            'workflow_type': 'standard_onboarding',
            'assign_to': 'support_team',
            'priority': 'normal'
        }

    return trigger_zapier_webhook(payload)

# Example usage
customer = {
    'email': 'vip@example.com',
    'name': 'VIP Customer',
    'lifetime_value': 15000
}

conditional_workflow(customer, WEBHOOK_URL)
```

### 8. Analytics and Monitoring

```python
import pandas as pd
from datetime import datetime

# Track webhook triggers
webhook_log = []

def tracked_webhook_trigger(webhook_url, data, event_type):
    start_time = datetime.now()

    response = requests.post(
        webhook_url,
        json=data,
        headers={'Content-Type': 'application/json'}
    )

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # Log the event
    webhook_log.append({
        'timestamp': start_time,
        'event_type': event_type,
        'status_code': response.status_code,
        'success': response.status_code == 200,
        'duration_seconds': duration,
        'payload_size': len(json.dumps(data))
    })

    return response.status_code == 200

# Generate analytics report
def generate_webhook_analytics():
    df = pd.DataFrame(webhook_log)

    if df.empty:
        return "No webhook data available"

    analytics = {
        'total_triggers': len(df),
        'successful': df['success'].sum(),
        'failed': len(df) - df['success'].sum(),
        'success_rate': (df['success'].sum() / len(df) * 100).round(2),
        'avg_duration': df['duration_seconds'].mean().round(3),
        'by_event_type': df.groupby('event_type')['success'].agg(['count', 'sum']).to_dict()
    }

    return analytics

# Example: Track multiple events
events = [
    {'type': 'new_lead', 'data': {'email': 'lead1@example.com'}},
    {'type': 'new_order', 'data': {'order_id': '001'}},
    {'type': 'new_lead', 'data': {'email': 'lead2@example.com'}}
]

for event in events:
    tracked_webhook_trigger(WEBHOOK_URL, event['data'], event['type'])

# Get analytics
analytics = generate_webhook_analytics()
print(f"Webhook Analytics:")
print(f"  Total Triggers: {analytics['total_triggers']}")
print(f"  Success Rate: {analytics['success_rate']}%")
print(f"  Average Duration: {analytics['avg_duration']}s")
```

## Installation

```bash
uv pip install requests pandas
```

## Authentication

For webhook-based Zapier integration:
1. Create a Zap in Zapier
2. Add "Webhooks by Zapier" as the trigger
3. Choose "Catch Hook"
4. Copy the webhook URL provided
5. Use the URL in your Python code

No API key required for webhooks!

## Quick Start

```python
import requests

# Your Zapier webhook URL
WEBHOOK_URL = 'https://hooks.zapier.com/hooks/catch/YOUR_HOOK_ID/'

# Send data to Zapier
data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'message': 'This is a test from Python!'
}

response = requests.post(WEBHOOK_URL, json=data)

if response.status_code == 200:
    print("Data sent to Zapier successfully!")
else:
    print(f"Failed to send data: {response.status_code}")
```

## Key Features Reference

- **Webhooks**: Trigger Zaps from any application
- **Multi-Step Zaps**: Complex workflows with multiple actions
- **Filters**: Conditional logic in workflows
- **Paths**: Branch workflows based on conditions
- **Delay**: Time-based workflow controls
- **Formatter**: Data transformation utilities
- **Code**: Python/JavaScript custom code steps
- **Storage**: Simple key-value data storage
- **Integrations**: 6000+ app connections

## Common Use Cases

1. Lead capture to CRM sync
2. Order processing automation
3. Support ticket routing
4. Email marketing automation
5. Social media management
6. Data synchronization
7. Notification workflows
8. Report generation and distribution

## References

- [Zapier Webhooks Documentation](https://zapier.com/page/webhooks/)
- [Zapier API Documentation](https://platform.zapier.com/reference/api)
- [Webhooks by Zapier](https://zapier.com/apps/webhook/integrations)
- [Zapier Developer Platform](https://platform.zapier.com/)
- [Zapier Integration Guide](https://zapier.com/help/create/basics/learn-key-concepts-in-zapier)

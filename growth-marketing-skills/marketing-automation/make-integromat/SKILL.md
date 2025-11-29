---
name: make-integromat
description: "Make (formerly Integromat) advanced automation platform. Visual workflow builder, complex scenarios, data mapping, routers, iterators, webhooks, API integration."
---

# Make (Integromat) Integration

## Overview

Make (formerly Integromat) is an advanced automation platform that enables complex workflow automation with visual scenario building. This skill covers using Make's API and webhooks to create sophisticated integrations and data transformations.

## When to Use This Skill

- Complex multi-step automation workflows
- Advanced data transformation and mapping
- Conditional logic and routing
- API integration and orchestration
- Scheduled automation scenarios
- Error handling and retry logic
- Data aggregation and processing
- Custom business process automation

## Core Capabilities

### 1. Webhook Triggers

```python
import requests
import json
from datetime import datetime

# Make Webhook configuration
WEBHOOK_URL = 'https://hook.integromat.com/YOUR_WEBHOOK_ID'

# Send data to Make webhook
def trigger_make_webhook(data):
    response = requests.post(
        WEBHOOK_URL,
        json=data,
        headers={'Content-Type': 'application/json'}
    )

    return {
        'status_code': response.status_code,
        'accepted': response.status_code == 200,
        'response': response.text
    }

# Example: Trigger customer onboarding scenario
customer_data = {
    'customer_id': 'CUST-12345',
    'email': 'newcustomer@example.com',
    'first_name': 'Jane',
    'last_name': 'Smith',
    'company': 'Tech Startup Inc',
    'plan': 'premium',
    'signup_date': datetime.now().isoformat(),
    'trial_ends': '2025-02-15',
    'custom_fields': {
        'industry': 'Technology',
        'employees': '50-100',
        'use_case': 'Marketing Automation'
    }
}

result = trigger_make_webhook(customer_data)
print(f"Webhook triggered: {result['accepted']}")

# Example: Trigger order processing
order_data = {
    'order_id': 'ORDER-98765',
    'customer_email': 'customer@example.com',
    'order_total': 499.99,
    'currency': 'USD',
    'items': [
        {
            'sku': 'PROD-001',
            'name': 'Premium Widget',
            'quantity': 2,
            'price': 199.99
        },
        {
            'sku': 'PROD-002',
            'name': 'Widget Pro',
            'quantity': 1,
            'price': 99.99
        }
    ],
    'shipping_address': {
        'street': '123 Main St',
        'city': 'San Francisco',
        'state': 'CA',
        'zip': '94102',
        'country': 'USA'
    },
    'payment_method': 'credit_card',
    'status': 'paid'
}

trigger_make_webhook(order_data)
```

### 2. Complex Data Structures

```python
# Send nested and complex data structures
def send_complex_scenario_data(webhook_url, scenario_data):
    # Make handles complex nested structures well
    complex_payload = {
        'scenario_type': scenario_data['type'],
        'timestamp': datetime.now().isoformat(),
        'data': {
            'customer': {
                'profile': scenario_data.get('customer', {}),
                'preferences': scenario_data.get('preferences', {}),
                'history': scenario_data.get('history', [])
            },
            'actions': scenario_data.get('actions', []),
            'metadata': scenario_data.get('metadata', {})
        }
    }

    response = requests.post(
        webhook_url,
        json=complex_payload,
        headers={'Content-Type': 'application/json'}
    )

    return response.status_code == 200

# Example: Send complex customer journey data
journey_data = {
    'type': 'customer_journey',
    'customer': {
        'id': 'CUST-12345',
        'email': 'journey@example.com',
        'name': 'John Doe'
    },
    'preferences': {
        'email_frequency': 'weekly',
        'content_types': ['blog', 'webinar', 'case_study'],
        'product_interests': ['marketing_automation', 'analytics']
    },
    'history': [
        {'event': 'page_view', 'page': '/pricing', 'timestamp': '2025-01-10T10:00:00Z'},
        {'event': 'download', 'asset': 'whitepaper', 'timestamp': '2025-01-11T14:30:00Z'},
        {'event': 'demo_request', 'product': 'enterprise', 'timestamp': '2025-01-12T09:15:00Z'}
    ],
    'actions': [
        {'type': 'send_email', 'template': 'nurture_sequence_1'},
        {'type': 'create_task', 'assigned_to': 'sales_rep_123'},
        {'type': 'update_crm', 'status': 'qualified'}
    ],
    'metadata': {
        'source': 'python_script',
        'priority': 'high',
        'tags': ['qualified_lead', 'enterprise_interest']
    }
}

send_complex_scenario_data(WEBHOOK_URL, journey_data)
```

### 3. Array and Bulk Operations

```python
# Send array data for iterator processing in Make
def send_bulk_data(webhook_url, items):
    payload = {
        'operation': 'bulk_process',
        'items': items,
        'total_count': len(items)
    }

    response = requests.post(
        webhook_url,
        json=payload,
        headers={'Content-Type': 'application/json'}
    )

    return response.json() if response.status_code == 200 else None

# Example: Bulk contact import
contacts = [
    {
        'email': 'contact1@example.com',
        'name': 'Alice Johnson',
        'company': 'Tech Co',
        'tags': ['customer', 'premium']
    },
    {
        'email': 'contact2@example.com',
        'name': 'Bob Smith',
        'company': 'Marketing Inc',
        'tags': ['prospect', 'trial']
    },
    {
        'email': 'contact3@example.com',
        'name': 'Carol White',
        'company': 'Sales Corp',
        'tags': ['customer', 'standard']
    }
]

send_bulk_data(WEBHOOK_URL, contacts)

# Example: Batch invoice processing
invoices = [
    {
        'invoice_id': 'INV-001',
        'customer_id': 'CUST-100',
        'amount': 1000.00,
        'due_date': '2025-02-01',
        'status': 'pending'
    },
    {
        'invoice_id': 'INV-002',
        'customer_id': 'CUST-101',
        'amount': 2500.00,
        'due_date': '2025-02-05',
        'status': 'pending'
    }
]

send_bulk_data(WEBHOOK_URL, invoices)
```

### 4. Make API Integration

```python
# Make API configuration (for scenario management)
API_KEY = 'your-make-api-key'
ORGANIZATION_ID = 'your-org-id'
API_BASE_URL = 'https://us1.make.com/api/v2'

api_headers = {
    'Authorization': f'Token {API_KEY}',
    'Content-Type': 'application/json'
}

# Get scenarios
def get_scenarios():
    url = f'{API_BASE_URL}/organizations/{ORGANIZATION_ID}/scenarios'

    response = requests.get(url, headers=api_headers)
    return response.json()

# Get scenario details
def get_scenario(scenario_id):
    url = f'{API_BASE_URL}/scenarios/{scenario_id}'

    response = requests.get(url, headers=api_headers)
    return response.json()

# Run scenario manually
def run_scenario(scenario_id):
    url = f'{API_BASE_URL}/scenarios/{scenario_id}/run'

    response = requests.post(url, headers=api_headers)
    return response.json()

# Get scenario execution history
def get_scenario_history(scenario_id, limit=10):
    url = f'{API_BASE_URL}/scenarios/{scenario_id}/history'

    params = {'limit': limit}

    response = requests.get(url, headers=api_headers, params=params)
    return response.json()

# Example: List all scenarios
# scenarios = get_scenarios()
# for scenario in scenarios.get('scenarios', []):
#     print(f"Scenario: {scenario['name']} (ID: {scenario['id']})")
```

### 5. Router and Conditional Logic

```python
# Send data with routing instructions for Make
def send_with_routing(webhook_url, data, routing_key):
    payload = {
        'routing_key': routing_key,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }

    response = requests.post(
        webhook_url,
        json=payload,
        headers={'Content-Type': 'application/json'}
    )

    return response.status_code == 200

# Example: Route based on customer value
def route_customer_by_value(customer):
    value = customer.get('lifetime_value', 0)

    if value > 10000:
        routing_key = 'vip_customer'
    elif value > 1000:
        routing_key = 'premium_customer'
    else:
        routing_key = 'standard_customer'

    payload = {
        'customer_id': customer['id'],
        'email': customer['email'],
        'name': customer['name'],
        'lifetime_value': value,
        'segment': routing_key
    }

    return send_with_routing(WEBHOOK_URL, payload, routing_key)

# Example: Route by event type
def route_by_event_type(event):
    event_routes = {
        'purchase': 'order_fulfillment',
        'refund': 'customer_service',
        'support_ticket': 'support_queue',
        'feedback': 'product_team'
    }

    routing_key = event_routes.get(event['type'], 'default_queue')

    return send_with_routing(WEBHOOK_URL, event, routing_key)

# Usage
customer = {
    'id': 'CUST-999',
    'email': 'vip@example.com',
    'name': 'VIP Customer',
    'lifetime_value': 15000
}

route_customer_by_value(customer)
```

### 6. Data Transformation and Aggregation

```python
import pandas as pd

# Prepare aggregated data for Make
def aggregate_and_send(webhook_url, raw_data, aggregation_type):
    df = pd.DataFrame(raw_data)

    if aggregation_type == 'daily_summary':
        # Aggregate by day
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        summary = df.groupby('date').agg({
            'revenue': 'sum',
            'orders': 'count',
            'customers': 'nunique'
        }).reset_index()

        payload = {
            'report_type': 'daily_summary',
            'data': summary.to_dict('records')
        }

    elif aggregation_type == 'customer_summary':
        # Aggregate by customer
        summary = df.groupby('customer_id').agg({
            'order_value': 'sum',
            'order_id': 'count'
        }).reset_index()
        summary.columns = ['customer_id', 'total_spent', 'order_count']

        payload = {
            'report_type': 'customer_summary',
            'data': summary.to_dict('records')
        }

    else:
        payload = {
            'report_type': aggregation_type,
            'data': raw_data
        }

    response = requests.post(
        webhook_url,
        json=payload,
        headers={'Content-Type': 'application/json'}
    )

    return response.status_code == 200

# Example: Send daily sales report
sales_data = [
    {'timestamp': '2025-01-15T10:00:00', 'revenue': 100, 'orders': 1, 'customers': 1},
    {'timestamp': '2025-01-15T14:00:00', 'revenue': 250, 'orders': 1, 'customers': 1},
    {'timestamp': '2025-01-16T09:00:00', 'revenue': 500, 'orders': 1, 'customers': 1}
]

aggregate_and_send(WEBHOOK_URL, sales_data, 'daily_summary')
```

### 7. Error Handling and Retry

```python
import time

# Trigger with advanced retry logic
def trigger_with_exponential_backoff(webhook_url, data, max_retries=5):
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
                    'response': response.json() if response.text else None
                }

            # Exponential backoff
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 2  # 2, 4, 8, 16, 32 seconds
                print(f"Attempt {attempt + 1} failed. Retrying in {wait_time}s...")
                time.sleep(wait_time)

        except requests.exceptions.RequestException as e:
            print(f"Request error on attempt {attempt + 1}: {e}")

            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 2
                time.sleep(wait_time)

    return {
        'success': False,
        'error': 'Max retries exceeded',
        'attempts': max_retries
    }

# Example: Critical data with retry
critical_data = {
    'type': 'critical_alert',
    'priority': 'urgent',
    'message': 'System threshold exceeded',
    'requires_action': True
}

result = trigger_with_exponential_backoff(WEBHOOK_URL, critical_data)

if result['success']:
    print(f"Alert sent successfully after {result['attempt']} attempt(s)")
else:
    print(f"Failed to send alert: {result['error']}")
```

### 8. Scheduled and Batch Processing

```python
from datetime import datetime, timedelta

# Generate batch report for scheduled scenario
def generate_scheduled_report(webhook_url, report_type, date_range):
    report_data = {
        'report_type': report_type,
        'generated_at': datetime.now().isoformat(),
        'period': {
            'start': date_range['start'],
            'end': date_range['end']
        },
        'metrics': {
            'total_revenue': 50000,
            'total_orders': 250,
            'new_customers': 45,
            'returning_customers': 205
        },
        'top_products': [
            {'name': 'Product A', 'revenue': 15000, 'units': 100},
            {'name': 'Product B', 'revenue': 12000, 'units': 80},
            {'name': 'Product C', 'revenue': 10000, 'units': 75}
        ]
    }

    response = requests.post(
        webhook_url,
        json=report_data,
        headers={'Content-Type': 'application/json'}
    )

    return response.status_code == 200

# Example: Weekly report
weekly_report = generate_scheduled_report(
    WEBHOOK_URL,
    'weekly_sales_summary',
    {
        'start': (datetime.now() - timedelta(days=7)).isoformat(),
        'end': datetime.now().isoformat()
    }
)

# Example: Monthly report
monthly_report = generate_scheduled_report(
    WEBHOOK_URL,
    'monthly_performance',
    {
        'start': (datetime.now() - timedelta(days=30)).isoformat(),
        'end': datetime.now().isoformat()
    }
)
```

## Installation

```bash
uv pip install requests pandas
```

## Authentication

For webhook-based Make integration:
1. Create a Scenario in Make
2. Add a "Webhook" trigger module
3. Choose "Custom webhook"
4. Copy the webhook URL
5. Use the URL in your Python code

For API-based integration:
1. Go to Make Profile Settings
2. Navigate to API section
3. Generate API token
4. Use token in API requests

## Quick Start

```python
import requests

# Your Make webhook URL
WEBHOOK_URL = 'https://hook.integromat.com/YOUR_WEBHOOK_ID'

# Send data to Make scenario
data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'event': 'signup',
    'timestamp': '2025-01-15T10:00:00Z'
}

response = requests.post(
    WEBHOOK_URL,
    json=data,
    headers={'Content-Type': 'application/json'}
)

if response.status_code == 200:
    print("Data sent to Make successfully!")
    print(f"Response: {response.text}")
else:
    print(f"Failed to send data: {response.status_code}")
```

## Key Features Reference

- **Webhooks**: Custom and instant webhooks
- **Routers**: Conditional branching logic
- **Iterators**: Process arrays and collections
- **Aggregators**: Combine multiple items
- **Data Stores**: Temporary data storage
- **HTTP Modules**: API requests and responses
- **Transformers**: Data manipulation tools
- **Error Handlers**: Scenario error management
- **Scheduling**: Time-based triggers
- **Filters**: Conditional execution

## Advanced Capabilities

1. Visual workflow builder
2. Complex data mapping
3. Multi-route scenarios
4. Data transformation tools
5. Error handling and rollback
6. Scenario templates
7. API integration
8. Custom functions
9. Webhook queue management
10. Execution history and logs

## References

- [Make Documentation](https://www.make.com/en/help/home)
- [Webhooks in Make](https://www.make.com/en/help/tools/webhooks)
- [Make API Documentation](https://www.make.com/en/api-documentation)
- [Scenario Building Guide](https://www.make.com/en/help/scenarios)
- [Data Structures](https://www.make.com/en/help/tools/data-structures)

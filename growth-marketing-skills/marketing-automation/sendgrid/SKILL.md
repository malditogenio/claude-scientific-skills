---
name: sendgrid
description: "SendGrid email delivery platform. Transactional emails, marketing campaigns, email API, SMTP relay, deliverability optimization, templates, analytics."
---

# SendGrid Integration

## Overview

SendGrid is a cloud-based email delivery platform specializing in transactional and marketing emails. This skill covers using the SendGrid API for sending emails, managing contacts, creating campaigns, and tracking deliverability.

## When to Use This Skill

- Transactional email delivery (confirmations, receipts, notifications)
- Marketing email campaigns
- High-volume email sending
- Email deliverability optimization
- Dynamic email templates
- Email validation and verification
- SMTP relay services
- Email analytics and tracking

## Core Capabilities

### 1. Sending Transactional Emails

```python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment
import base64

# SendGrid configuration
SENDGRID_API_KEY = 'your-api-key'
sg = SendGridAPIClient(SENDGRID_API_KEY)

# Send simple email
def send_simple_email(to_email, subject, html_content, from_email='noreply@example.com'):
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    try:
        response = sg.send(message)
        return {
            'status_code': response.status_code,
            'message_id': response.headers.get('X-Message-Id')
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
result = send_simple_email(
    'customer@example.com',
    'Welcome to Our Service',
    '<h1>Hello!</h1><p>Thanks for signing up.</p>'
)

print(f"Email sent: {result}")

# Send email with personalization
def send_personalized_email(to_emails, subject, template_id, dynamic_data):
    message = Mail(
        from_email='marketing@example.com',
        to_emails=to_emails
    )

    message.template_id = template_id

    # Add dynamic template data
    for email, data in dynamic_data.items():
        message.personalizations[0].dynamic_template_data = data

    try:
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(f"Error: {e}")
        return None

# Send email with attachment
def send_email_with_attachment(to_email, subject, content, file_path):
    message = Mail(
        from_email='support@example.com',
        to_emails=to_email,
        subject=subject,
        html_content=content
    )

    # Attach file
    with open(file_path, 'rb') as f:
        file_data = f.read()

    encoded_file = base64.b64encode(file_data).decode()

    attachment = Attachment(
        file_content=encoded_file,
        file_type='application/pdf',
        file_name='document.pdf',
        disposition='attachment'
    )

    message.attachment = attachment

    try:
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(f"Error: {e}")
        return None

# Batch send to multiple recipients
def send_batch_emails(recipients, subject, html_content):
    message = Mail(
        from_email='noreply@example.com',
        subject=subject,
        html_content=html_content
    )

    # Add recipients
    personalization = message.personalizations[0]
    for recipient in recipients:
        personalization.add_to(Email(recipient))

    try:
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(f"Error: {e}")
        return None
```

### 2. Dynamic Templates

```python
# Send email using dynamic template
def send_template_email(to_email, template_id, template_data, from_email='noreply@example.com'):
    message = Mail(
        from_email=from_email,
        to_emails=to_email
    )

    message.template_id = template_id
    message.dynamic_template_data = template_data

    try:
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example: Send order confirmation using template
send_template_email(
    'customer@example.com',
    'd-1234567890abcdef',  # Template ID
    {
        'first_name': 'John',
        'order_number': 'ORDER-12345',
        'order_total': '$99.99',
        'items': [
            {'name': 'Product A', 'quantity': 2, 'price': '$49.99'},
            {'name': 'Product B', 'quantity': 1, 'price': '$49.99'}
        ],
        'shipping_address': '123 Main St, City, State 12345',
        'tracking_number': 'TRACK-999'
    }
)

# Send password reset email
send_template_email(
    'user@example.com',
    'd-passwordreset123',
    {
        'reset_link': 'https://example.com/reset?token=abc123',
        'expires_in': '24 hours',
        'user_email': 'user@example.com'
    }
)

# Send welcome email with multiple dynamic sections
send_template_email(
    'newuser@example.com',
    'd-welcome789',
    {
        'first_name': 'Jane',
        'signup_date': 'January 15, 2025',
        'trial_days': 14,
        'onboarding_steps': [
            {'step': 1, 'title': 'Complete your profile'},
            {'step': 2, 'title': 'Invite team members'},
            {'step': 3, 'title': 'Create your first project'}
        ],
        'support_email': 'support@example.com'
    }
)
```

### 3. Contact Management

```python
import requests

# SendGrid Marketing API
MARKETING_API_URL = 'https://api.sendgrid.com/v3'

headers = {
    'Authorization': f'Bearer {SENDGRID_API_KEY}',
    'Content-Type': 'application/json'
}

# Add contacts
def add_contacts(contacts):
    url = f'{MARKETING_API_URL}/marketing/contacts'

    data = {
        'contacts': [
            {
                'email': contact['email'],
                'first_name': contact.get('first_name', ''),
                'last_name': contact.get('last_name', ''),
                'custom_fields': contact.get('custom_fields', {})
            }
            for contact in contacts
        ]
    }

    response = requests.put(url, headers=headers, json=data)
    return response.json()

# Example: Add contacts
new_contacts = [
    {
        'email': 'user1@example.com',
        'first_name': 'Alice',
        'last_name': 'Smith',
        'custom_fields': {
            'e1_T': 'premium',  # Subscription tier
            'e2_N': 1250.00     # Lifetime value
        }
    },
    {
        'email': 'user2@example.com',
        'first_name': 'Bob',
        'last_name': 'Johnson',
        'custom_fields': {
            'e1_T': 'free',
            'e2_N': 0.00
        }
    }
]

result = add_contacts(new_contacts)
print(f"Contacts added: {result}")

# Search contacts
def search_contacts(query):
    url = f'{MARKETING_API_URL}/marketing/contacts/search'

    data = {'query': query}

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Delete contact
def delete_contact(contact_id):
    url = f'{MARKETING_API_URL}/marketing/contacts'

    params = {'ids': contact_id}

    response = requests.delete(url, headers=headers, params=params)
    return response.status_code == 202

# Example: Search for premium subscribers
premium_contacts = search_contacts('subscription_tier = "premium"')
print(f"Premium contacts: {len(premium_contacts.get('result', []))}")
```

### 4. List and Segment Management

```python
# Create list
def create_list(list_name):
    url = f'{MARKETING_API_URL}/marketing/lists'

    data = {'name': list_name}

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Add contacts to list
def add_contacts_to_list(list_id, contact_ids):
    url = f'{MARKETING_API_URL}/marketing/lists/{list_id}/contacts'

    data = {'contact_ids': contact_ids}

    response = requests.put(url, headers=headers, json=data)
    return response.json()

# Create segment
def create_segment(name, query_dsl):
    url = f'{MARKETING_API_URL}/marketing/segments'

    data = {
        'name': name,
        'query_dsl': query_dsl
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example: Create VIP segment
vip_segment = create_segment(
    'VIP Customers',
    {
        'and': [
            {
                'or': [
                    {
                        'field': 'lifetime_value',
                        'comparison': {
                            'type': 'greater_than',
                            'value': 1000
                        }
                    }
                ]
            }
        ]
    }
)

# Get all lists
def get_lists():
    url = f'{MARKETING_API_URL}/marketing/lists'

    response = requests.get(url, headers=headers)
    return response.json()

# Get all segments
def get_segments():
    url = f'{MARKETING_API_URL}/marketing/segments'

    response = requests.get(url, headers=headers)
    return response.json()
```

### 5. Marketing Campaigns

```python
# Create single send campaign
def create_single_send(name, subject, sender_id, list_ids, html_content):
    url = f'{MARKETING_API_URL}/marketing/singlesends'

    data = {
        'name': name,
        'send_to': {
            'list_ids': list_ids
        },
        'email_config': {
            'subject': subject,
            'html_content': html_content,
            'sender_id': sender_id,
            'suppression_group_id': 12345  # Unsubscribe group
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Schedule single send
def schedule_single_send(single_send_id, send_at):
    url = f'{MARKETING_API_URL}/marketing/singlesends/{single_send_id}/schedule'

    data = {'send_at': send_at}

    response = requests.put(url, headers=headers, json=data)
    return response.json()

# Get single send stats
def get_single_send_stats(single_send_id):
    url = f'{MARKETING_API_URL}/marketing/stats/singlesends/{single_send_id}'

    response = requests.get(url, headers=headers)
    return response.json()

# Example: Create and schedule newsletter
newsletter = create_single_send(
    name='Monthly Newsletter - Jan 2025',
    subject='Your Monthly Marketing Insights',
    sender_id=123456,
    list_ids=['list-id-1', 'list-id-2'],
    html_content='<h1>Newsletter</h1><p>Content here...</p>'
)

schedule_single_send(
    newsletter['id'],
    '2025-01-20T10:00:00Z'
)

# Get campaign stats
stats = get_single_send_stats(newsletter['id'])
print(f"Campaign Stats:")
print(f"  Delivered: {stats.get('delivered', 0)}")
print(f"  Opens: {stats.get('unique_opens', 0)}")
print(f"  Clicks: {stats.get('unique_clicks', 0)}")
```

### 6. Email Validation and Verification

```python
# Validate email address
def validate_email(email):
    url = f'{MARKETING_API_URL}/validations/email'

    data = {
        'email': email,
        'source': 'signup'
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Bulk email validation
def validate_emails_bulk(emails):
    results = []

    for email in emails:
        result = validate_email(email)
        results.append({
            'email': email,
            'verdict': result.get('verdict', 'unknown'),
            'score': result.get('score', 0)
        })

    return results

# Example: Validate signup email
validation = validate_email('newuser@example.com')

if validation.get('verdict') == 'Valid':
    print(f"Email is valid, score: {validation.get('score')}")
else:
    print(f"Email validation failed: {validation.get('verdict')}")
```

### 7. Analytics and Reporting

```python
import pandas as pd
from datetime import datetime, timedelta

# Get global stats
def get_global_stats(start_date, end_date, aggregated_by='day'):
    url = f'{MARKETING_API_URL}/stats'

    params = {
        'start_date': start_date,
        'end_date': end_date,
        'aggregated_by': aggregated_by
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Get category stats
def get_category_stats(categories, start_date, end_date):
    url = f'{MARKETING_API_URL}/categories/stats'

    params = {
        'categories': ','.join(categories),
        'start_date': start_date,
        'end_date': end_date,
        'aggregated_by': 'day'
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Get bounce statistics
def get_bounces(start_date, end_date):
    url = f'{MARKETING_API_URL}/suppression/bounces'

    params = {
        'start_time': int(start_date.timestamp()),
        'end_time': int(end_date.timestamp())
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Generate deliverability report
def generate_deliverability_report(days=30):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    stats = get_global_stats(
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )

    report_data = []

    for day_stat in stats:
        report_data.append({
            'date': day_stat['date'],
            'requests': day_stat['stats'][0]['metrics'].get('requests', 0),
            'delivered': day_stat['stats'][0]['metrics'].get('delivered', 0),
            'opens': day_stat['stats'][0]['metrics'].get('unique_opens', 0),
            'clicks': day_stat['stats'][0]['metrics'].get('unique_clicks', 0),
            'bounces': day_stat['stats'][0]['metrics'].get('bounces', 0),
            'spam_reports': day_stat['stats'][0]['metrics'].get('spam_reports', 0)
        })

    df = pd.DataFrame(report_data)

    # Calculate rates
    df['delivery_rate'] = (df['delivered'] / df['requests'] * 100).round(2)
    df['open_rate'] = (df['opens'] / df['delivered'] * 100).round(2)
    df['click_rate'] = (df['clicks'] / df['delivered'] * 100).round(2)
    df['bounce_rate'] = (df['bounces'] / df['requests'] * 100).round(2)

    return df

# Example usage
report = generate_deliverability_report(30)
print("Deliverability Report (Last 30 Days):")
print(report)
print(f"\nAverage Delivery Rate: {report['delivery_rate'].mean():.2f}%")
print(f"Average Open Rate: {report['open_rate'].mean():.2f}%")
```

## Installation

```bash
# Official SendGrid Python SDK
uv pip install sendgrid

# For additional functionality
uv pip install requests pandas
```

## Authentication

Get your API key from SendGrid:
1. Log in to SendGrid
2. Go to Settings > API Keys
3. Create a new API Key with appropriate permissions
4. Store securely (never commit to version control)

```python
from sendgrid import SendGridAPIClient

SENDGRID_API_KEY = 'SG.your-api-key-here'
sg = SendGridAPIClient(SENDGRID_API_KEY)
```

## Quick Start

```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = 'your-api-key'
sg = SendGridAPIClient(SENDGRID_API_KEY)

# Send email
message = Mail(
    from_email='noreply@example.com',
    to_emails='customer@example.com',
    subject='Hello from SendGrid',
    html_content='<strong>This is a test email</strong>'
)

try:
    response = sg.send(message)
    print(f"Email sent! Status: {response.status_code}")
    print(f"Message ID: {response.headers.get('X-Message-Id')}")
except Exception as e:
    print(f"Error: {e}")
```

## Key Features Reference

- **Transactional Email**: System-generated emails via API
- **Marketing Campaigns**: Bulk email sends to lists/segments
- **Dynamic Templates**: Personalized email templates
- **Contact Management**: Lists, segments, custom fields
- **Email Validation**: Real-time email verification
- **Deliverability**: Spam testing, bounce management
- **Analytics**: Open/click tracking, engagement metrics
- **SMTP Relay**: Alternative to API sending
- **Webhooks**: Real-time event notifications

## References

- [SendGrid API Documentation](https://docs.sendgrid.com/api-reference)
- [Python SDK](https://github.com/sendgrid/sendgrid-python)
- [Dynamic Templates Guide](https://docs.sendgrid.com/ui/sending-email/how-to-send-an-email-with-dynamic-templates)
- [Marketing Campaigns API](https://docs.sendgrid.com/api-reference/marketing-campaigns)
- [Email Validation API](https://docs.sendgrid.com/api-reference/e-mail-address-validation)

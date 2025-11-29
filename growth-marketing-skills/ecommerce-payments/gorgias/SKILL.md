---
name: gorgias
description: "Gorgias e-commerce customer support platform API. Track support tickets, customer satisfaction, response times, revenue impact, agent performance, customer retention."
---

# Gorgias Integration

## Overview

Gorgias is a helpdesk platform built specifically for e-commerce businesses, integrating customer support with sales data. This skill covers using the Gorgias API to analyze support performance, track customer satisfaction, measure revenue impact of support interactions, and optimize customer service operations for retention and growth.

## When to Use This Skill

- Customer support performance analytics
- Ticket volume and response time tracking
- Customer satisfaction (CSAT) measurement
- Revenue impact of support interactions
- Agent performance and productivity analysis
- Support-driven churn prevention
- Customer sentiment analysis
- Support operations optimization

## Core Capabilities

### 1. Ticket Management and Analytics

```python
import requests
import pandas as pd
from datetime import datetime, timedelta

# Gorgias API Configuration
DOMAIN = "your-domain"
API_KEY = "your_api_key"
EMAIL = "your_email"
BASE_URL = f"https://{DOMAIN}.gorgias.com/api"

# Basic Auth
auth = (EMAIL, API_KEY)

# Get tickets
def get_tickets(start_date=None, status=None, limit=100):
    """Fetch support tickets"""
    url = f"{BASE_URL}/tickets"

    params = {
        'limit': limit,
        'order_by': 'created_datetime:desc'
    }

    # Add filters
    if start_date:
        params['created_datetime_gte'] = start_date.isoformat()

    if status:
        params['status'] = status

    all_tickets = []
    cursor = None

    while True:
        if cursor:
            params['cursor'] = cursor

        response = requests.get(url, auth=auth, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        tickets = data.get('data', [])

        if not tickets:
            break

        all_tickets.extend(tickets)

        # Check for next page
        meta = data.get('meta', {})
        cursor = meta.get('next_cursor')

        if not cursor:
            break

    return all_tickets

# Calculate support metrics
def calculate_support_metrics(days=30):
    """Comprehensive support analytics"""
    start_date = datetime.now() - timedelta(days=days)
    tickets = get_tickets(start_date=start_date)

    ticket_data = []

    for ticket in tickets:
        created_at = pd.to_datetime(ticket['created_datetime'])
        closed_at = pd.to_datetime(ticket.get('closed_datetime')) if ticket.get('closed_datetime') else None

        # Calculate resolution time
        if closed_at:
            resolution_time_hours = (closed_at - created_at).total_seconds() / 3600
        else:
            resolution_time_hours = None

        ticket_data.append({
            'ticket_id': ticket['id'],
            'created_at': created_at,
            'closed_at': closed_at,
            'status': ticket['status'],
            'channel': ticket.get('channel'),
            'via': ticket.get('via'),
            'subject': ticket.get('subject', ''),
            'customer_id': ticket.get('customer', {}).get('id'),
            'customer_email': ticket.get('customer', {}).get('email'),
            'assignee_user_id': ticket.get('assignee_user', {}).get('id'),
            'tags': ticket.get('tags', []),
            'priority': ticket.get('priority'),
            'spam': ticket.get('spam', False),
            'resolution_time_hours': resolution_time_hours,
            'messages_count': ticket.get('messages_count', 0)
        })

    df = pd.DataFrame(ticket_data)

    if len(df) == 0:
        return {}, df, None

    df['date'] = df['created_at'].dt.date

    # Calculate metrics
    closed_tickets = df[df['status'] == 'closed']

    metrics = {
        'total_tickets': len(df),
        'closed_tickets': len(closed_tickets),
        'open_tickets': len(df[df['status'] == 'open']),
        'avg_resolution_time_hours': closed_tickets['resolution_time_hours'].mean(),
        'median_resolution_time_hours': closed_tickets['resolution_time_hours'].median(),
        'tickets_by_channel': df['channel'].value_counts().to_dict(),
        'tickets_by_status': df['status'].value_counts().to_dict(),
        'unique_customers': df['customer_id'].nunique(),
        'avg_messages_per_ticket': df['messages_count'].mean()
    }

    # Daily trends
    daily_stats = df.groupby('date').agg({
        'ticket_id': 'count',
        'customer_id': 'nunique'
    }).rename(columns={'ticket_id': 'tickets', 'customer_id': 'unique_customers'})

    return metrics, df, daily_stats

# Response time analysis
def analyze_response_times(days=30):
    """Track first response and average response times"""
    start_date = datetime.now() - timedelta(days=days)
    tickets = get_tickets(start_date=start_date)

    response_data = []

    for ticket in tickets:
        ticket_id = ticket['id']

        # Get messages for this ticket
        messages_url = f"{BASE_URL}/tickets/{ticket_id}/messages"
        messages_response = requests.get(messages_url, auth=auth)

        if messages_response.status_code != 200:
            continue

        messages = messages_response.json().get('data', [])

        if not messages:
            continue

        ticket_created = pd.to_datetime(ticket['created_datetime'])

        # Find first agent response
        first_response_time = None

        for msg in messages:
            if msg.get('source', {}).get('type') == 'agent':
                msg_time = pd.to_datetime(msg['created_datetime'])
                first_response_time = (msg_time - ticket_created).total_seconds() / 60  # minutes
                break

        response_data.append({
            'ticket_id': ticket_id,
            'channel': ticket.get('channel'),
            'first_response_minutes': first_response_time,
            'total_messages': len(messages)
        })

    df = pd.DataFrame(response_data)

    if len(df) == 0:
        return None

    # Filter out tickets without responses
    df = df[df['first_response_minutes'].notna()]

    response_metrics = {
        'avg_first_response_minutes': df['first_response_minutes'].mean(),
        'median_first_response_minutes': df['first_response_minutes'].median(),
        'response_time_by_channel': df.groupby('channel')['first_response_minutes'].mean().to_dict()
    }

    return response_metrics, df

# Example usage
metrics, tickets_df, daily_stats = calculate_support_metrics(days=30)
if metrics:
    print(f"30-Day Support Metrics:")
    print(f"  Total Tickets: {metrics['total_tickets']}")
    print(f"  Closed: {metrics['closed_tickets']}")
    print(f"  Open: {metrics['open_tickets']}")
    print(f"  Avg Resolution Time: {metrics['avg_resolution_time_hours']:.1f} hours")
    print(f"  Unique Customers: {metrics['unique_customers']}")
```

### 2. Customer Satisfaction and Sentiment

```python
# Get satisfaction ratings
def get_satisfaction_surveys(days=30):
    """Fetch CSAT survey responses"""
    url = f"{BASE_URL}/satisfaction-surveys"

    start_date = datetime.now() - timedelta(days=days)

    params = {
        'created_datetime_gte': start_date.isoformat(),
        'limit': 100
    }

    all_surveys = []
    cursor = None

    while True:
        if cursor:
            params['cursor'] = cursor

        response = requests.get(url, auth=auth, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        surveys = data.get('data', [])

        if not surveys:
            break

        all_surveys.extend(surveys)

        meta = data.get('meta', {})
        cursor = meta.get('next_cursor')

        if not cursor:
            break

    return all_surveys

# Calculate CSAT metrics
def calculate_csat_metrics(days=30):
    """Analyze customer satisfaction scores"""
    surveys = get_satisfaction_surveys(days=days)

    survey_data = []

    for survey in surveys:
        survey_data.append({
            'survey_id': survey['id'],
            'ticket_id': survey.get('ticket_id'),
            'score': survey.get('score'),
            'scored_at': pd.to_datetime(survey.get('scored_datetime')),
            'comment': survey.get('comment', ''),
            'customer_id': survey.get('customer', {}).get('id')
        })

    df = pd.DataFrame(survey_data)

    if len(df) == 0:
        return {}, df

    # Filter out null scores
    df = df[df['score'].notna()]

    # CSAT is typically scored 1-5, with 4-5 being "satisfied"
    df['satisfied'] = df['score'] >= 4

    metrics = {
        'total_responses': len(df),
        'average_score': df['score'].mean(),
        'csat_score': (df['satisfied'].sum() / len(df) * 100),
        'score_distribution': df['score'].value_counts().sort_index().to_dict(),
        'response_rate': None  # Would need to calculate against total tickets
    }

    return metrics, df

# Sentiment analysis from ticket content
def analyze_ticket_sentiment(days=30):
    """Analyze sentiment from ticket tags and content"""
    start_date = datetime.now() - timedelta(days=days)
    tickets = get_tickets(start_date=start_date)

    sentiment_data = []

    for ticket in tickets:
        tags = ticket.get('tags', [])

        # Categorize sentiment based on tags
        # This is simplified - real implementation would use NLP
        negative_tags = ['angry', 'frustrated', 'complaint', 'refund', 'cancel']
        positive_tags = ['happy', 'thanks', 'praise', 'satisfied']

        tag_list = [tag.get('name', '').lower() for tag in tags]

        has_negative = any(neg in ' '.join(tag_list) for neg in negative_tags)
        has_positive = any(pos in ' '.join(tag_list) for pos in positive_tags)

        if has_negative:
            sentiment = 'Negative'
        elif has_positive:
            sentiment = 'Positive'
        else:
            sentiment = 'Neutral'

        sentiment_data.append({
            'ticket_id': ticket['id'],
            'sentiment': sentiment,
            'tags': tag_list,
            'status': ticket['status']
        })

    df = pd.DataFrame(sentiment_data)

    if len(df) == 0:
        return None

    sentiment_dist = df['sentiment'].value_counts()

    return sentiment_dist, df

# Example usage
csat_metrics, surveys_df = calculate_csat_metrics(days=30)
if csat_metrics:
    print(f"CSAT Metrics:")
    print(f"  Total Responses: {csat_metrics['total_responses']}")
    print(f"  Average Score: {csat_metrics['average_score']:.2f}")
    print(f"  CSAT: {csat_metrics['csat_score']:.1f}%")
```

### 3. Revenue Impact and Customer Value

```python
# Get customers with support history
def get_customers_with_tickets():
    """Fetch customer data with support interactions"""
    url = f"{BASE_URL}/customers"

    params = {'limit': 100}

    all_customers = []
    cursor = None

    while True:
        if cursor:
            params['cursor'] = cursor

        response = requests.get(url, auth=auth, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        customers = data.get('data', [])

        if not customers:
            break

        all_customers.extend(customers)

        meta = data.get('meta', {})
        cursor = meta.get('next_cursor')

        if not cursor:
            break

    return all_customers

# Analyze customer value by support level
def analyze_customer_value_by_support(days=180):
    """Correlate support tickets with customer value"""
    start_date = datetime.now() - timedelta(days=days)
    tickets = get_tickets(start_date=start_date)

    # Count tickets per customer
    customer_tickets = {}

    for ticket in tickets:
        customer_id = ticket.get('customer', {}).get('id')

        if not customer_id:
            continue

        if customer_id not in customer_tickets:
            customer_tickets[customer_id] = {
                'ticket_count': 0,
                'email': ticket.get('customer', {}).get('email'),
                'channels': []
            }

        customer_tickets[customer_id]['ticket_count'] += 1
        customer_tickets[customer_id]['channels'].append(ticket.get('channel'))

    # Get customer data with revenue info
    customers = get_customers_with_tickets()

    customer_data = []

    for customer in customers:
        customer_id = customer['id']
        ticket_info = customer_tickets.get(customer_id, {'ticket_count': 0})

        # Extract revenue data from customer meta (if integrated with e-commerce)
        meta = customer.get('meta', {})
        total_spent = float(meta.get('total_spent', 0))

        customer_data.append({
            'customer_id': customer_id,
            'email': customer.get('email'),
            'ticket_count': ticket_info['ticket_count'],
            'total_spent': total_spent,
            'created_at': pd.to_datetime(customer.get('created_datetime'))
        })

    df = pd.DataFrame(customer_data)

    if len(df) == 0:
        return {}, df

    # Segment by support level
    df['support_level'] = pd.cut(
        df['ticket_count'],
        bins=[-1, 0, 2, 5, float('inf')],
        labels=['No Support', 'Low Support', 'Medium Support', 'High Support']
    )

    # Analyze value by support level
    support_value = df.groupby('support_level').agg({
        'total_spent': ['mean', 'sum', 'count'],
        'customer_id': 'count'
    }).round(2)

    support_value.columns = ['avg_spent', 'total_revenue', 'count', 'customer_count']

    metrics = {
        'customers_with_support': len(df[df['ticket_count'] > 0]),
        'avg_value_with_support': df[df['ticket_count'] > 0]['total_spent'].mean(),
        'avg_value_no_support': df[df['ticket_count'] == 0]['total_spent'].mean()
    }

    return metrics, df, support_value

# Support-driven sales analysis
def analyze_support_driven_revenue(days=30):
    """Track revenue generated through support interactions"""
    start_date = datetime.now() - timedelta(days=days)
    tickets = get_tickets(start_date=start_date)

    # Look for tags indicating sales
    sales_tags = ['order_placed', 'sale', 'converted', 'purchase']

    revenue_tickets = []

    for ticket in tickets:
        tags = [tag.get('name', '').lower() for tag in ticket.get('tags', [])]

        has_sales_tag = any(sales_tag in ' '.join(tags) for sales_tag in sales_tags)

        if has_sales_tag:
            # Extract revenue from ticket meta
            meta = ticket.get('meta', {})
            order_value = float(meta.get('order_value', 0))

            revenue_tickets.append({
                'ticket_id': ticket['id'],
                'order_value': order_value,
                'created_at': pd.to_datetime(ticket['created_datetime']),
                'tags': tags
            })

    df = pd.DataFrame(revenue_tickets)

    if len(df) == 0:
        return None

    metrics = {
        'support_driven_tickets': len(df),
        'total_revenue': df['order_value'].sum(),
        'avg_order_value': df['order_value'].mean()
    }

    return metrics, df

# Example usage
value_metrics, customers_df, support_value = analyze_customer_value_by_support(days=180)
if value_metrics:
    print(f"Customer Value by Support:")
    print(f"  Customers with Support: {value_metrics['customers_with_support']}")
    print(f"  Avg Value (with support): ${value_metrics['avg_value_with_support']:,.2f}")
    print(f"  Avg Value (no support): ${value_metrics['avg_value_no_support']:,.2f}")
```

### 4. Agent Performance and Operations

```python
# Get agents (users)
def get_agents():
    """Fetch support agents"""
    url = f"{BASE_URL}/users"

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        return []

# Analyze agent performance
def analyze_agent_performance(days=30):
    """Track individual agent metrics"""
    start_date = datetime.now() - timedelta(days=days)
    tickets = get_tickets(start_date=start_date)
    agents = get_agents()

    # Build agent lookup
    agent_lookup = {agent['id']: agent.get('name', 'Unknown') for agent in agents}

    # Count tickets by agent
    agent_performance = {}

    for ticket in tickets:
        assignee_id = ticket.get('assignee_user', {}).get('id')

        if not assignee_id:
            continue

        if assignee_id not in agent_performance:
            agent_performance[assignee_id] = {
                'name': agent_lookup.get(assignee_id, 'Unknown'),
                'tickets_handled': 0,
                'tickets_closed': 0,
                'resolution_times': []
            }

        agent_performance[assignee_id]['tickets_handled'] += 1

        if ticket['status'] == 'closed':
            agent_performance[assignee_id]['tickets_closed'] += 1

            created = pd.to_datetime(ticket['created_datetime'])
            closed = pd.to_datetime(ticket.get('closed_datetime'))

            if closed:
                resolution_time = (closed - created).total_seconds() / 3600
                agent_performance[assignee_id]['resolution_times'].append(resolution_time)

    # Build dataframe
    agent_data = []

    for agent_id, data in agent_performance.items():
        avg_resolution = (
            sum(data['resolution_times']) / len(data['resolution_times'])
            if data['resolution_times'] else None
        )

        agent_data.append({
            'agent_id': agent_id,
            'agent_name': data['name'],
            'tickets_handled': data['tickets_handled'],
            'tickets_closed': data['tickets_closed'],
            'close_rate': (data['tickets_closed'] / data['tickets_handled'] * 100) if data['tickets_handled'] > 0 else 0,
            'avg_resolution_hours': avg_resolution
        })

    df = pd.DataFrame(agent_data)

    if len(df) == 0:
        return None

    df = df.sort_values('tickets_handled', ascending=False)

    return df

# Channel performance
def analyze_channel_performance(days=30):
    """Analyze support by channel (email, chat, social)"""
    start_date = datetime.now() - timedelta(days=days)
    tickets = get_tickets(start_date=start_date)

    channel_data = []

    for ticket in tickets:
        channel_data.append({
            'channel': ticket.get('channel', 'unknown'),
            'status': ticket['status'],
            'messages_count': ticket.get('messages_count', 0)
        })

    df = pd.DataFrame(channel_data)

    if len(df) == 0:
        return None

    channel_stats = df.groupby('channel').agg({
        'status': lambda x: (x == 'closed').sum() / len(x) * 100,
        'messages_count': 'mean'
    }).round(2)

    channel_stats.columns = ['close_rate', 'avg_messages']
    channel_stats['ticket_count'] = df['channel'].value_counts()

    return channel_stats.sort_values('ticket_count', ascending=False)

# Example usage
agent_performance = analyze_agent_performance(days=30)
if agent_performance is not None:
    print("Agent Performance:")
    print(agent_performance.head(10))

channel_performance = analyze_channel_performance(days=30)
if channel_performance is not None:
    print("\nChannel Performance:")
    print(channel_performance)
```

## Installation

```bash
# Install required packages
uv pip install requests pandas python-dateutil
```

## Authentication

### API Key

1. Log in to Gorgias
2. Go to Settings > REST API
3. Create a new API key
4. Copy the API key and your email

```python
import requests

DOMAIN = "your-domain"  # e.g., "mystore"
EMAIL = "your@email.com"
API_KEY = "your_api_key"
BASE_URL = f"https://{DOMAIN}.gorgias.com/api"

auth = (EMAIL, API_KEY)

# Test connection
response = requests.get(f"{BASE_URL}/tickets", auth=auth, params={'limit': 1})

if response.status_code == 200:
    print("Connected to Gorgias API successfully!")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

## Quick Start

```python
import requests
from datetime import datetime, timedelta

# Configuration
DOMAIN = "your-domain"
EMAIL = "your@email.com"
API_KEY = "your_api_key"
BASE_URL = f"https://{DOMAIN}.gorgias.com/api"

auth = (EMAIL, API_KEY)

# Get recent tickets
start_date = datetime.now() - timedelta(days=7)

response = requests.get(
    f"{BASE_URL}/tickets",
    auth=auth,
    params={
        'created_datetime_gte': start_date.isoformat(),
        'limit': 10
    }
)

tickets = response.json().get('data', [])

print(f"Recent Tickets: {len(tickets)}")

for ticket in tickets:
    print(f"Ticket #{ticket['id']}: {ticket.get('subject', 'No subject')} - {ticket['status']}")

# Get ticket statistics
open_tickets = len([t for t in tickets if t['status'] == 'open'])
closed_tickets = len([t for t in tickets if t['status'] == 'closed'])

print(f"\nOpen: {open_tickets}, Closed: {closed_tickets}")
```

## Key Metrics Reference

### Volume Metrics
- **Total Tickets**: All support requests
- **Tickets by Status**: Open, closed, pending, spam
- **Tickets by Channel**: Email, chat, social media, phone
- **New vs Returning**: First-time vs repeat contacts

### Performance Metrics
- **First Response Time (FRT)**: Time to first agent reply
- **Average Resolution Time**: Time from open to close
- **Close Rate**: Closed tickets / total tickets
- **Response Rate**: Tickets responded to / total tickets

### Satisfaction Metrics
- **CSAT Score**: Customer satisfaction percentage (4-5 stars)
- **Average Rating**: Mean satisfaction score
- **NPS (Net Promoter Score)**: Likelihood to recommend
- **Response Rate**: Survey responses / surveys sent

### Agent Metrics
- **Tickets Per Agent**: Workload distribution
- **Agent Close Rate**: Individual resolution rate
- **Average Handle Time**: Time spent per ticket
- **Agent CSAT**: Satisfaction by agent

## References

- [Gorgias API Documentation](https://developers.gorgias.com/reference)
- [Tickets API](https://developers.gorgias.com/reference/get_api-tickets)
- [Customers API](https://developers.gorgias.com/reference/get_api-customers)
- [Satisfaction Surveys API](https://developers.gorgias.com/reference/get_api-satisfaction-surveys)
- [Gorgias Support Analytics](https://docs.gorgias.com/en-us/analytics)

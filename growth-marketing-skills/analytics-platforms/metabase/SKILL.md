---
name: metabase
description: "Open source BI tool. SQL queries, visual query builder, dashboards, embedding, automated reports, database connections."
---

# Metabase Open Source BI

## Overview

Metabase is an open-source business intelligence tool that makes it easy to ask questions about your data and create dashboards. This skill covers using the Metabase API, automating queries, building dashboards programmatically, and integrating Metabase into marketing analytics workflows.

## When to Use This Skill

- Open-source alternative to commercial BI tools
- Self-service analytics for marketing teams
- Quick dashboard creation without coding
- Automated report generation and distribution
- Embedding analytics in applications
- SQL and visual query building
- Multi-database analytics

## Core Capabilities

### 1. Metabase API Setup

```python
import requests
import pandas as pd
from datetime import datetime, timedelta
import json

class MetabaseAPI:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session_token = None

    def authenticate(self, username, password):
        """Authenticate and get session token"""
        url = f"{self.base_url}/api/session"

        payload = {
            'username': username,
            'password': password
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()

        self.session_token = response.json()['id']
        print("Authenticated successfully")

    def _make_request(self, endpoint, method='GET', params=None, data=None):
        """Make authenticated request to Metabase API"""
        if not self.session_token:
            raise Exception("Not authenticated. Call authenticate() first.")

        headers = {
            'X-Metabase-Session': self.session_token,
            'Content-Type': 'application/json'
        }

        url = f"{self.base_url}/api/{endpoint}"

        if method == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)

        response.raise_for_status()
        return response.json() if response.content else None

    def query_database(self, database_id, query):
        """Execute native SQL query"""
        data = {
            'database': database_id,
            'native': {
                'query': query
            },
            'type': 'native'
        }

        return self._make_request('dataset', method='POST', data=data)

    def get_card(self, card_id):
        """Get saved question (card)"""
        return self._make_request(f'card/{card_id}')

    def run_card(self, card_id, parameters=None):
        """Execute saved question"""
        endpoint = f'card/{card_id}/query'

        data = {}
        if parameters:
            data['parameters'] = parameters

        return self._make_request(endpoint, method='POST', data=data)

    def get_dashboards(self):
        """Get all dashboards"""
        return self._make_request('dashboard')

# Initialize Metabase API
metabase = MetabaseAPI(base_url='http://localhost:3000')  # or your Metabase URL

metabase.authenticate(
    username='your_email@company.com',
    password='your_password'
)
```

### 2. Running SQL Queries

```python
def analyze_campaign_performance(metabase, database_id):
    """
    Query campaign performance from database
    """
    sql_query = """
    SELECT
        DATE(created_at) as date,
        campaign_name,
        utm_source,
        utm_medium,
        COUNT(DISTINCT user_id) as users,
        COUNT(*) as sessions,
        SUM(CASE WHEN converted = true THEN 1 ELSE 0 END) as conversions,
        SUM(revenue) as revenue,
        SUM(cost) as cost
    FROM marketing_events
    WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY 1, 2, 3, 4
    ORDER BY revenue DESC
    """

    result = metabase.query_database(database_id, sql_query)

    # Convert to DataFrame
    if 'data' in result:
        columns = [col['name'] for col in result['data']['cols']]
        rows = result['data']['rows']

        df = pd.DataFrame(rows, columns=columns)

        # Calculate metrics
        df['conversion_rate'] = df['conversions'] / df['sessions'] * 100
        df['cpa'] = df['cost'] / df['conversions']
        df['roas'] = df['revenue'] / df['cost']

        print("\nCampaign Performance:")
        print(df.head(20))

        print(f"\nTotal Revenue: ${df['revenue'].sum():,.2f}")
        print(f"Total Cost: ${df['cost'].sum():,.2f}")
        print(f"Overall ROAS: {df['revenue'].sum() / df['cost'].sum():.2f}")

        return df

    return None

# Analyze campaigns
campaign_data = analyze_campaign_performance(metabase, database_id=1)

def get_user_cohorts(metabase, database_id):
    """Analyze user cohorts"""
    sql_query = """
    WITH cohorts AS (
        SELECT
            user_id,
            DATE_TRUNC('month', first_purchase_date) as cohort_month,
            DATE_TRUNC('month', purchase_date) as purchase_month,
            SUM(amount) as revenue
        FROM purchases
        WHERE first_purchase_date >= CURRENT_DATE - INTERVAL '6 months'
        GROUP BY 1, 2, 3
    )
    SELECT
        cohort_month,
        purchase_month,
        COUNT(DISTINCT user_id) as users,
        SUM(revenue) as total_revenue,
        AVG(revenue) as avg_revenue_per_user
    FROM cohorts
    GROUP BY 1, 2
    ORDER BY 1, 2
    """

    result = metabase.query_database(database_id, sql_query)

    if 'data' in result:
        columns = [col['name'] for col in result['data']['cols']]
        df = pd.DataFrame(result['data']['rows'], columns=columns)

        # Pivot for cohort matrix
        cohort_pivot = df.pivot(
            index='cohort_month',
            columns='purchase_month',
            values='users'
        )

        print("\nUser Cohort Analysis:")
        print(cohort_pivot)

        return df

    return None

cohort_data = get_user_cohorts(metabase, database_id=1)
```

### 3. Working with Saved Questions (Cards)

```python
def run_saved_question(metabase, card_id, parameters=None):
    """
    Run saved question with optional parameters
    """
    # Get question metadata
    card = metabase.get_card(card_id)

    print(f"Question: {card['name']}")
    print(f"Description: {card.get('description', 'N/A')}")

    # Run the question
    result = metabase.run_card(card_id, parameters)

    if 'data' in result:
        columns = [col['name'] for col in result['data']['cols']]
        rows = result['data']['rows']

        df = pd.DataFrame(rows, columns=columns)

        print(f"\nResults: {len(df)} rows")
        print(df.head())

        return df

    return None

# Run saved marketing metrics question
# marketing_metrics = run_saved_question(
#     metabase,
#     card_id=123,
#     parameters=[
#         {
#             'type': 'date/range',
#             'target': ['variable', ['template-tag', 'date_range']],
#             'value': '2024-01-01~2024-01-31'
#         }
#     ]
# )

def create_question(metabase, name, database_id, query, collection_id=None):
    """
    Create new saved question
    """
    question_data = {
        'name': name,
        'dataset_query': {
            'database': database_id,
            'type': 'native',
            'native': {
                'query': query
            }
        },
        'display': 'table',
        'visualization_settings': {}
    }

    if collection_id:
        question_data['collection_id'] = collection_id

    card = metabase._make_request('card', method='POST', data=question_data)

    print(f"Created question: {name} (ID: {card['id']})")

    return card

# Create marketing KPIs question
kpi_query = """
SELECT
    'Today' as period,
    COUNT(DISTINCT user_id) as dau,
    SUM(revenue) as revenue,
    COUNT(DISTINCT CASE WHEN converted THEN user_id END) as conversions
FROM events
WHERE DATE(created_at) = CURRENT_DATE

UNION ALL

SELECT
    'Yesterday' as period,
    COUNT(DISTINCT user_id) as dau,
    SUM(revenue) as revenue,
    COUNT(DISTINCT CASE WHEN converted THEN user_id END) as conversions
FROM events
WHERE DATE(created_at) = CURRENT_DATE - 1
"""

# kpi_card = create_question(
#     metabase,
#     name='Daily Marketing KPIs',
#     database_id=1,
#     query=kpi_query
# )
```

### 4. Dashboard Management

```python
def get_dashboard_data(metabase, dashboard_id):
    """
    Get all data from dashboard
    """
    # Get dashboard details
    dashboard = metabase._make_request(f'dashboard/{dashboard_id}')

    print(f"Dashboard: {dashboard['name']}")
    print(f"Cards: {len(dashboard.get('ordered_cards', []))}")

    dashboard_data = {}

    # Run each card in the dashboard
    for card_info in dashboard.get('ordered_cards', []):
        card_id = card_info['card']['id']
        card_name = card_info['card']['name']

        try:
            result = metabase.run_card(card_id)

            if 'data' in result:
                columns = [col['name'] for col in result['data']['cols']]
                rows = result['data']['rows']
                dashboard_data[card_name] = pd.DataFrame(rows, columns=columns)

                print(f"  {card_name}: {len(rows)} rows")

        except Exception as e:
            print(f"  Error running {card_name}: {e}")

    return dashboard_data

# Get marketing dashboard data
# dashboard_data = get_dashboard_data(metabase, dashboard_id=5)
#
# # Access specific card data
# if 'Revenue by Channel' in dashboard_data:
#     channel_revenue = dashboard_data['Revenue by Channel']
#     print("\nRevenue by Channel:")
#     print(channel_revenue)

def create_dashboard(metabase, name, description, collection_id=None):
    """
    Create new dashboard
    """
    dashboard_data = {
        'name': name,
        'description': description
    }

    if collection_id:
        dashboard_data['collection_id'] = collection_id

    dashboard = metabase._make_request('dashboard', method='POST', data=dashboard_data)

    print(f"Created dashboard: {name} (ID: {dashboard['id']})")

    return dashboard

def add_card_to_dashboard(metabase, dashboard_id, card_id, row=0, col=0,
                         size_x=4, size_y=4):
    """
    Add card to dashboard
    """
    card_data = {
        'cardId': card_id,
        'row': row,
        'col': col,
        'sizeX': size_x,
        'sizeY': size_y
    }

    result = metabase._make_request(
        f'dashboard/{dashboard_id}/cards',
        method='POST',
        data=card_data
    )

    print(f"Added card {card_id} to dashboard {dashboard_id}")

    return result

# Create marketing dashboard
# dashboard = create_dashboard(
#     metabase,
#     name='Marketing Overview',
#     description='Key marketing metrics and trends'
# )
#
# # Add cards to dashboard
# add_card_to_dashboard(metabase, dashboard['id'], card_id=123, row=0, col=0)
# add_card_to_dashboard(metabase, dashboard['id'], card_id=124, row=0, col=4)
```

### 5. Embedding and Sharing

```python
def get_public_sharing_url(metabase, card_id):
    """
    Enable public sharing and get URL
    """
    # Enable public sharing
    share_data = {
        'enabled': True
    }

    result = metabase._make_request(
        f'card/{card_id}/public_link',
        method='POST',
        data=share_data
    )

    public_uuid = result['uuid']
    public_url = f"{metabase.base_url}/public/question/{public_uuid}"

    print(f"Public URL: {public_url}")

    return public_url

# Get public URL for sharing
# public_url = get_public_sharing_url(metabase, card_id=123)

def generate_embed_url(metabase, dashboard_id, secret_key, params=None):
    """
    Generate signed embed URL for dashboard
    Requires JWT signing
    """
    import jwt
    import time

    payload = {
        'resource': {'dashboard': dashboard_id},
        'params': params or {},
        'exp': int(time.time()) + 60 * 10  # 10 minutes
    }

    token = jwt.encode(payload, secret_key, algorithm='HS256')

    embed_url = f"{metabase.base_url}/embed/dashboard/{token}"

    return embed_url

# Generate embed URL
# embed_url = generate_embed_url(
#     metabase,
#     dashboard_id=5,
#     secret_key='your_embedding_secret_key',
#     params={'date_filter': '2024-01-01~2024-01-31'}
# )
```

### 6. Automated Report Distribution

```python
def create_pulse(metabase, name, cards, channels, schedule):
    """
    Create Pulse (automated report via email/Slack)
    """
    pulse_data = {
        'name': name,
        'cards': [{'id': card_id, 'include_csv': False, 'include_xls': False}
                 for card_id in cards],
        'channels': channels,
        'skip_if_empty': True,
        'collection_id': None
    }

    # Add schedule
    if schedule['type'] == 'daily':
        pulse_data['schedule_type'] = 'daily'
        pulse_data['schedule_hour'] = schedule['hour']
    elif schedule['type'] == 'weekly':
        pulse_data['schedule_type'] = 'weekly'
        pulse_data['schedule_day'] = schedule['day']
        pulse_data['schedule_hour'] = schedule['hour']

    pulse = metabase._make_request('pulse', method='POST', data=pulse_data)

    print(f"Created pulse: {name}")

    return pulse

# Create daily email report
# pulse = create_pulse(
#     metabase,
#     name='Daily Marketing Metrics',
#     cards=[123, 124, 125],  # Card IDs to include
#     channels=[{
#         'channel_type': 'email',
#         'enabled': True,
#         'recipients': [
#             {'email': 'marketing@company.com'}
#         ]
#     }],
#     schedule={
#         'type': 'daily',
#         'hour': 9  # 9 AM
#     }
# )

def get_pulses(metabase):
    """Get all pulses"""
    pulses = metabase._make_request('pulse')

    if pulses:
        pulses_df = pd.DataFrame([
            {
                'id': p['id'],
                'name': p['name'],
                'schedule_type': p.get('schedule_type'),
                'enabled': not p.get('archived', False)
            }
            for p in pulses
        ])

        print("\nActive Pulses:")
        print(pulses_df)

        return pulses_df

    return None

pulses = get_pulses(metabase)
```

### 7. Database Connections

```python
def get_databases(metabase):
    """Get all database connections"""
    databases = metabase._make_request('database')

    if databases:
        db_df = pd.DataFrame([
            {
                'id': db['id'],
                'name': db['name'],
                'engine': db['engine'],
                'is_sample': db.get('is_sample', False)
            }
            for db in databases
        ])

        print("\nDatabase Connections:")
        print(db_df)

        return db_df

    return None

databases = get_databases(metabase)

def sync_database(metabase, database_id):
    """Trigger database schema sync"""
    result = metabase._make_request(
        f'database/{database_id}/sync_schema',
        method='POST'
    )

    print(f"Database sync triggered for ID {database_id}")

    return result

# Sync database schema
# sync_database(metabase, database_id=1)
```

### 8. Collections and Organization

```python
def get_collections(metabase):
    """Get all collections"""
    collections = metabase._make_request('collection')

    if collections:
        coll_df = pd.DataFrame([
            {
                'id': c['id'],
                'name': c['name'],
                'slug': c['slug'],
                'archived': c.get('archived', False)
            }
            for c in collections
        ])

        print("\nCollections:")
        print(coll_df)

        return coll_df

    return None

def create_collection(metabase, name, description, color='#509EE3'):
    """Create new collection"""
    collection_data = {
        'name': name,
        'description': description,
        'color': color
    }

    collection = metabase._make_request(
        'collection',
        method='POST',
        data=collection_data
    )

    print(f"Created collection: {name} (ID: {collection['id']})")

    return collection

collections = get_collections(metabase)

# Create marketing collection
# marketing_collection = create_collection(
#     metabase,
#     name='Marketing Analytics',
#     description='All marketing dashboards and questions',
#     color='#88BF4D'
# )
```

## Installation

```bash
uv pip install requests pandas pyjwt

# For self-hosted Metabase
docker run -d -p 3000:3000 --name metabase metabase/metabase
```

## Authentication

1. Log in to Metabase
2. Navigate to Settings > Admin
3. Create API credentials or use email/password
4. For embedding, generate embedding secret key in Settings

## Quick Start

```python
import requests

# Metabase credentials
METABASE_URL = 'http://localhost:3000'
EMAIL = 'your_email@company.com'
PASSWORD = 'your_password'

# Authenticate
auth_response = requests.post(
    f'{METABASE_URL}/api/session',
    json={'username': EMAIL, 'password': PASSWORD}
)

session_token = auth_response.json()['id']

# Run a query
headers = {'X-Metabase-Session': session_token}

query_data = {
    'database': 1,
    'native': {
        'query': 'SELECT COUNT(*) as total FROM users'
    },
    'type': 'native'
}

result = requests.post(
    f'{METABASE_URL}/api/dataset',
    headers=headers,
    json=query_data
)

print(result.json())
```

## Key Features

- **Open Source**: Free and self-hosted
- **Visual Query Builder**: No SQL required
- **Native SQL**: Full SQL support for advanced queries
- **Dashboards**: Interactive dashboards with filters
- **Pulses**: Automated email/Slack reports
- **Embedding**: White-label embedding
- **Multi-Database**: Connect to multiple data sources

## References

- [Metabase API Documentation](https://www.metabase.com/docs/latest/api-documentation)
- [Metabase Embedding](https://www.metabase.com/docs/latest/embedding/introduction)
- [Metabase SQL Guide](https://www.metabase.com/learn/sql-questions/sql-best-practices)
- [Metabase GitHub](https://github.com/metabase/metabase)

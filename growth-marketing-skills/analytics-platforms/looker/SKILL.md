---
name: looker
description: "BI and data exploration platform. LookML modeling, embedded analytics, SQL runner, custom dashboards, API access, BigQuery integration."
---

# Looker BI and Data Exploration

## Overview

Looker is a modern business intelligence and data exploration platform that uses a semantic modeling layer (LookML) to define metrics and dimensions. This skill covers using the Looker API, creating dashboards, running queries, and analyzing marketing data through Looker's powerful data modeling capabilities.

## When to Use This Skill

- Building and managing BI dashboards
- Creating reusable data models with LookML
- Running ad-hoc SQL queries on marketing data
- Embedding analytics into applications
- Automating report generation and distribution
- Analyzing data across multiple sources
- Self-service analytics for marketing teams

## Core Capabilities

### 1. Looker API Setup

```python
import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import base64

class LookerAPI:
    def __init__(self, base_url, client_id, client_secret):
        self.base_url = base_url.rstrip('/')
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate and get access token"""
        url = f"{self.base_url}/api/4.0/login"
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
        self.access_token = response.json()['access_token']

    def _make_request(self, endpoint, method='GET', params=None, data=None):
        """Make authenticated request to Looker API"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        url = f"{self.base_url}/api/4.0/{endpoint}"

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

    def run_query(self, model, view, fields, filters=None, limit=500):
        """Run a query and return results"""
        query_data = {
            'model': model,
            'view': view,
            'fields': fields,
            'filters': filters or {},
            'limit': limit
        }

        # Create query
        query = self._make_request('queries', method='POST', data=query_data)
        query_id = query['id']

        # Run query
        result = self._make_request(f'queries/{query_id}/run/json')

        return result

    def get_look(self, look_id):
        """Get a Look (saved query)"""
        return self._make_request(f'looks/{look_id}')

    def run_look(self, look_id):
        """Run a Look and get results"""
        return self._make_request(f'looks/{look_id}/run/json')

    def get_dashboard(self, dashboard_id):
        """Get dashboard details"""
        return self._make_request(f'dashboards/{dashboard_id}')

# Initialize Looker API
looker = LookerAPI(
    base_url='https://your-company.looker.com',
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET'
)

print("Authenticated with Looker API")
```

### 2. Running Marketing Queries

```python
def analyze_campaign_performance(looker, date_from, date_to):
    """
    Analyze marketing campaign performance
    """
    # Run query using Looker's data model
    results = looker.run_query(
        model='marketing',
        view='campaigns',
        fields=[
            'campaigns.name',
            'campaigns.source',
            'campaigns.medium',
            'campaigns.impressions',
            'campaigns.clicks',
            'campaigns.conversions',
            'campaigns.cost',
            'campaigns.revenue'
        ],
        filters={
            'campaigns.date': f'{date_from} to {date_to}'
        },
        limit=1000
    )

    # Convert to DataFrame
    df = pd.DataFrame(results)

    # Calculate metrics
    df['ctr'] = df['campaigns.clicks'] / df['campaigns.impressions'] * 100
    df['cpc'] = df['campaigns.cost'] / df['campaigns.clicks']
    df['conversion_rate'] = df['campaigns.conversions'] / df['campaigns.clicks'] * 100
    df['roas'] = df['campaigns.revenue'] / df['campaigns.cost']

    print("\nCampaign Performance Summary:")
    print(f"Total campaigns: {len(df)}")
    print(f"Total cost: ${df['campaigns.cost'].sum():,.2f}")
    print(f"Total revenue: ${df['campaigns.revenue'].sum():,.2f}")
    print(f"Overall ROAS: {df['campaigns.revenue'].sum() / df['campaigns.cost'].sum():.2f}")

    # Top campaigns by ROAS
    top_campaigns = df.nlargest(10, 'roas')[
        ['campaigns.name', 'campaigns.cost', 'campaigns.revenue', 'roas']
    ]

    print("\nTop 10 Campaigns by ROAS:")
    print(top_campaigns)

    return df

# Analyze last 30 days
campaign_df = analyze_campaign_performance(
    looker,
    date_from=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
    date_to=datetime.now().strftime('%Y-%m-%d')
)

def analyze_user_acquisition(looker, date_from, date_to):
    """Analyze user acquisition by channel"""
    results = looker.run_query(
        model='marketing',
        view='users',
        fields=[
            'users.acquisition_date',
            'users.acquisition_channel',
            'users.count',
            'users.total_ltv',
            'users.avg_ltv'
        ],
        filters={
            'users.acquisition_date': f'{date_from} to {date_to}'
        },
        limit=1000
    )

    df = pd.DataFrame(results)
    df['users.acquisition_date'] = pd.to_datetime(df['users.acquisition_date'])

    # Channel performance
    channel_summary = df.groupby('users.acquisition_channel').agg({
        'users.count': 'sum',
        'users.total_ltv': 'sum',
        'users.avg_ltv': 'mean'
    }).round(2)

    print("\nUser Acquisition by Channel:")
    print(channel_summary)

    # Daily trends
    daily_acquisition = df.groupby('users.acquisition_date')['users.count'].sum()
    print(f"\nAverage daily acquisitions: {daily_acquisition.mean():.0f}")

    return df

acquisition_df = analyze_user_acquisition(
    looker,
    date_from='2024-01-01',
    date_to='2024-01-31'
)
```

### 3. Dashboard Management

```python
def get_dashboard_data(looker, dashboard_id):
    """
    Get all data from a dashboard
    """
    # Get dashboard metadata
    dashboard = looker.get_dashboard(dashboard_id)

    print(f"Dashboard: {dashboard['title']}")
    print(f"Elements: {len(dashboard.get('dashboard_elements', []))}")

    # Run all queries in the dashboard
    dashboard_data = {}

    for element in dashboard.get('dashboard_elements', []):
        if 'query' in element and element['query']:
            query_id = element['query']['id']
            element_title = element.get('title', f"Element {element['id']}")

            try:
                # Run the query
                results = looker._make_request(f'queries/{query_id}/run/json')

                dashboard_data[element_title] = pd.DataFrame(results)

                print(f"\n{element_title}: {len(results)} rows")

            except Exception as e:
                print(f"Error running query for {element_title}: {e}")

    return dashboard_data

# Get marketing dashboard data
dashboard_data = get_dashboard_data(looker, dashboard_id='marketing_overview')

def create_dashboard(looker, title, description, queries):
    """
    Create a new dashboard
    """
    dashboard_data = {
        'title': title,
        'description': description
    }

    # Create dashboard
    dashboard = looker._make_request('dashboards', method='POST', data=dashboard_data)
    dashboard_id = dashboard['id']

    print(f"Created dashboard: {title} (ID: {dashboard_id})")

    # Add elements
    for i, query_config in enumerate(queries):
        # Create query
        query = looker._make_request('queries', method='POST', data=query_config)

        # Create dashboard element
        element_data = {
            'dashboard_id': dashboard_id,
            'query_id': query['id'],
            'title': query_config.get('title', f'Query {i+1}'),
            'type': 'vis',
            'vis_config': query_config.get('vis_config', {})
        }

        looker._make_request('dashboard_elements', method='POST', data=element_data)

    print(f"Added {len(queries)} elements to dashboard")

    return dashboard_id

# Create custom marketing dashboard
queries = [
    {
        'title': 'Daily Revenue',
        'model': 'marketing',
        'view': 'orders',
        'fields': ['orders.created_date', 'orders.total_revenue'],
        'filters': {'orders.created_date': '30 days'},
        'vis_config': {'type': 'looker_line'}
    },
    {
        'title': 'Top Products',
        'model': 'marketing',
        'view': 'products',
        'fields': ['products.name', 'products.total_sales'],
        'sorts': ['products.total_sales desc'],
        'limit': 10,
        'vis_config': {'type': 'looker_bar'}
    }
]

# new_dashboard_id = create_dashboard(
#     looker,
#     title='Marketing Performance',
#     description='Key marketing metrics',
#     queries=queries
# )
```

### 4. SQL Runner

```python
def run_sql_query(looker, connection_name, sql):
    """
    Run custom SQL query using SQL Runner
    """
    query_data = {
        'connection_name': connection_name,
        'sql': sql
    }

    result = looker._make_request('sql_queries', method='POST', data=query_data)
    query_slug = result['slug']

    # Get results
    results = looker._make_request(f'sql_queries/{query_slug}/run/json')

    return pd.DataFrame(results)

# Run custom SQL for marketing analysis
sql_query = """
SELECT
    DATE(created_at) as date,
    utm_source,
    utm_medium,
    utm_campaign,
    COUNT(DISTINCT user_id) as users,
    COUNT(DISTINCT CASE WHEN purchased = true THEN user_id END) as purchasers,
    SUM(revenue) as total_revenue
FROM marketing.events
WHERE created_at >= CURRENT_DATE - 30
GROUP BY 1, 2, 3, 4
ORDER BY total_revenue DESC
"""

marketing_data = run_sql_query(
    looker,
    connection_name='bigquery_marketing',
    sql=sql_query
)

print("\nCustom Marketing Analysis:")
print(marketing_data.head(20))

# Calculate conversion rates
marketing_data['conversion_rate'] = (
    marketing_data['purchasers'] / marketing_data['users'] * 100
)

print("\nTop Performing Campaigns:")
print(marketing_data.nlargest(10, 'total_revenue')[
    ['utm_campaign', 'users', 'conversion_rate', 'total_revenue']
])
```

### 5. Scheduled Reports

```python
def create_scheduled_report(looker, dashboard_id, schedule_config):
    """
    Create scheduled dashboard delivery
    """
    schedule_data = {
        'name': schedule_config['name'],
        'dashboard_id': dashboard_id,
        'crontab': schedule_config['crontab'],  # e.g., '0 9 * * 1' for Monday 9am
        'scheduled_plan_destination': [{
            'format': schedule_config.get('format', 'pdf'),
            'address': schedule_config['email'],
            'type': 'email'
        }]
    }

    schedule = looker._make_request('scheduled_plans', method='POST', data=schedule_data)

    print(f"Created scheduled report: {schedule_config['name']}")
    print(f"Schedule: {schedule_config['crontab']}")
    print(f"Recipient: {schedule_config['email']}")

    return schedule

# Schedule weekly marketing report
# schedule_config = {
#     'name': 'Weekly Marketing Report',
#     'crontab': '0 9 * * 1',  # Every Monday at 9am
#     'email': 'marketing-team@company.com',
#     'format': 'pdf'
# }
#
# scheduled_report = create_scheduled_report(
#     looker,
#     dashboard_id='marketing_overview',
#     schedule_config=schedule_config
# )

def get_scheduled_plans(looker):
    """Get all scheduled plans"""
    plans = looker._make_request('scheduled_plans')

    if plans:
        plans_df = pd.DataFrame([
            {
                'id': plan['id'],
                'name': plan['name'],
                'enabled': plan['enabled'],
                'crontab': plan['crontab'],
                'dashboard_id': plan.get('dashboard_id')
            }
            for plan in plans
        ])

        print("\nScheduled Reports:")
        print(plans_df)

        return plans_df

    return None

scheduled_plans = get_scheduled_plans(looker)
```

### 6. Look (Saved Query) Management

```python
def run_saved_look(looker, look_id):
    """
    Run a saved Look and analyze results
    """
    # Get Look metadata
    look = looker.get_look(look_id)

    print(f"Look: {look['title']}")
    print(f"Description: {look.get('description', 'N/A')}")

    # Run the Look
    results = looker.run_look(look_id)

    df = pd.DataFrame(results)

    print(f"\nResults: {len(df)} rows")
    print(df.head())

    return df

# Run marketing performance Look
# marketing_look = run_saved_look(looker, look_id=123)

def create_look(looker, title, query_config, folder_id=None):
    """
    Create a new Look (saved query)
    """
    # Create query
    query = looker._make_request('queries', method='POST', data=query_config)

    # Create Look
    look_data = {
        'title': title,
        'query_id': query['id'],
        'folder_id': folder_id
    }

    look = looker._make_request('looks', method='POST', data=look_data)

    print(f"Created Look: {title} (ID: {look['id']})")

    return look

# Create Look for daily revenue
query_config = {
    'model': 'marketing',
    'view': 'orders',
    'fields': ['orders.created_date', 'orders.total_revenue', 'orders.count'],
    'filters': {'orders.created_date': '30 days'},
    'sorts': ['orders.created_date desc']
}

# daily_revenue_look = create_look(
#     looker,
#     title='Daily Revenue - Last 30 Days',
#     query_config=query_config
# )
```

### 7. User and Cohort Analysis

```python
def analyze_user_cohorts(looker, cohort_metric='revenue'):
    """
    Analyze user cohorts over time
    """
    results = looker.run_query(
        model='marketing',
        view='user_cohorts',
        fields=[
            'user_cohorts.cohort_month',
            'user_cohorts.months_since_signup',
            'user_cohorts.user_count',
            f'user_cohorts.{cohort_metric}'
        ],
        filters={
            'user_cohorts.cohort_month': '6 months'
        },
        limit=1000
    )

    df = pd.DataFrame(results)

    # Pivot for cohort analysis
    cohort_pivot = df.pivot(
        index='user_cohorts.cohort_month',
        columns='user_cohorts.months_since_signup',
        values=f'user_cohorts.{cohort_metric}'
    )

    print(f"\nCohort Analysis - {cohort_metric.title()}:")
    print(cohort_pivot)

    # Calculate retention rates
    if cohort_metric == 'user_count':
        retention = cohort_pivot.div(cohort_pivot[0], axis=0) * 100
        print("\nRetention Rates (%):")
        print(retention)

    return cohort_pivot

# Analyze revenue cohorts
revenue_cohorts = analyze_user_cohorts(looker, cohort_metric='revenue')

# Analyze user retention
retention_cohorts = analyze_user_cohorts(looker, cohort_metric='user_count')
```

### 8. Data Export

```python
def export_query_results(looker, query_config, format='csv', filename=None):
    """
    Export query results to file
    """
    # Create query
    query = looker._make_request('queries', method='POST', data=query_config)
    query_id = query['id']

    # Get results in specified format
    result = looker._make_request(f'queries/{query_id}/run/{format}')

    # Save to file
    if filename:
        with open(filename, 'w') as f:
            f.write(result)
        print(f"Exported to {filename}")

    return result

# Export marketing data to CSV
query_config = {
    'model': 'marketing',
    'view': 'campaigns',
    'fields': [
        'campaigns.name',
        'campaigns.impressions',
        'campaigns.clicks',
        'campaigns.conversions',
        'campaigns.cost',
        'campaigns.revenue'
    ],
    'filters': {'campaigns.date': '30 days'}
}

# csv_data = export_query_results(
#     looker,
#     query_config,
#     format='csv',
#     filename='campaign_performance.csv'
# )
```

## Installation

```bash
uv pip install requests pandas numpy
```

For LookML development:

```bash
# Install Looker SDK
uv pip install looker-sdk
```

## Authentication

1. Log in to Looker
2. Navigate to Admin > Users > Your Account
3. Click "Edit Keys" under API Keys
4. Generate a new Client ID and Secret
5. Save the credentials securely

## Quick Start

```python
import requests

# Looker API credentials
BASE_URL = 'https://your-company.looker.com'
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'

# Authenticate
auth_response = requests.post(
    f'{BASE_URL}/api/4.0/login',
    data={'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
)

access_token = auth_response.json()['access_token']

# Run a query
headers = {'Authorization': f'Bearer {access_token}'}

query_data = {
    'model': 'marketing',
    'view': 'users',
    'fields': ['users.count', 'users.created_date'],
    'filters': {'users.created_date': '7 days'}
}

query_response = requests.post(
    f'{BASE_URL}/api/4.0/queries',
    headers=headers,
    json=query_data
)

query_id = query_response.json()['id']

# Get results
results = requests.get(
    f'{BASE_URL}/api/4.0/queries/{query_id}/run/json',
    headers=headers
)

print(results.json())
```

## Key Features

- **LookML**: Semantic modeling layer for reusable metrics
- **SQL Runner**: Ad-hoc SQL query interface
- **Embedded Analytics**: Embed dashboards in applications
- **Scheduled Delivery**: Automated report distribution
- **API Access**: Programmatic access to all features
- **Git Integration**: Version control for LookML models
- **Multi-Source**: Query across multiple databases

## References

- [Looker API Documentation](https://cloud.google.com/looker/docs/reference/api-and-integration)
- [Looker Python SDK](https://github.com/looker-open-source/sdk-codegen/tree/main/python)
- [LookML Documentation](https://cloud.google.com/looker/docs/what-is-lookml)
- [Looker Best Practices](https://cloud.google.com/looker/docs/best-practices)

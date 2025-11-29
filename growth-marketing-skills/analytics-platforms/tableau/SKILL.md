---
name: tableau
description: "Data visualization and dashboards. Interactive visualizations, calculated fields, data blending, Tableau Server API, embedded analytics."
---

# Tableau Data Visualization

## Overview

Tableau is a leading data visualization and business intelligence platform that enables users to create interactive dashboards and visual analytics. This skill covers using the Tableau Server/Cloud API, automating report generation, and building marketing analytics dashboards programmatically.

## When to Use This Skill

- Creating interactive data visualizations and dashboards
- Building executive marketing reports
- Automating dashboard updates and refreshes
- Embedding analytics in applications
- Connecting to multiple data sources
- Self-service analytics for marketing teams
- Real-time campaign performance monitoring

## Core Capabilities

### 1. Tableau Server API Setup

```python
import requests
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET
import json

class TableauServerAPI:
    def __init__(self, server_url, site_id=''):
        self.server_url = server_url.rstrip('/')
        self.site_id = site_id
        self.api_version = '3.19'
        self.auth_token = None
        self.site_uuid = None

    def sign_in(self, username, password):
        """Authenticate with Tableau Server"""
        url = f"{self.server_url}/api/{self.api_version}/auth/signin"

        payload = f"""
        <tsRequest>
            <credentials name="{username}" password="{password}">
                <site contentUrl="{self.site_id}" />
            </credentials>
        </tsRequest>
        """

        response = requests.post(url, data=payload)
        response.raise_for_status()

        # Parse XML response
        root = ET.fromstring(response.content)
        self.auth_token = root.find('.//t:credentials', {'t': 'http://tableau.com/api'}).get('token')
        self.site_uuid = root.find('.//t:site', {'t': 'http://tableau.com/api'}).get('id')

        print(f"Authenticated successfully")

    def _make_request(self, endpoint, method='GET', data=None, params=None):
        """Make authenticated request to Tableau API"""
        if not self.auth_token:
            raise Exception("Not authenticated. Call sign_in() first.")

        headers = {
            'X-Tableau-Auth': self.auth_token,
            'Content-Type': 'application/json'
        }

        url = f"{self.server_url}/api/{self.api_version}/sites/{self.site_uuid}/{endpoint}"

        if method == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)

        response.raise_for_status()
        return response.content

    def get_workbooks(self):
        """Get all workbooks"""
        response = self._make_request('workbooks')
        root = ET.fromstring(response)

        workbooks = []
        for wb in root.findall('.//{http://tableau.com/api}workbook'):
            workbooks.append({
                'id': wb.get('id'),
                'name': wb.get('name'),
                'created_at': wb.get('createdAt'),
                'updated_at': wb.get('updatedAt')
            })

        return pd.DataFrame(workbooks)

    def get_views(self, workbook_id=None):
        """Get all views (dashboards/sheets)"""
        endpoint = 'views'
        if workbook_id:
            endpoint = f'workbooks/{workbook_id}/views'

        response = self._make_request(endpoint)
        root = ET.fromstring(response)

        views = []
        for view in root.findall('.//{http://tableau.com/api}view'):
            views.append({
                'id': view.get('id'),
                'name': view.get('name'),
                'workbook_id': view.find('.//{http://tableau.com/api}workbook').get('id')
            })

        return pd.DataFrame(views)

# Initialize Tableau API
tableau = TableauServerAPI(
    server_url='https://tableau.yourcompany.com',
    site_id='marketing'
)

tableau.sign_in(
    username='your_username',
    password='your_password'
)

# Get all workbooks
workbooks = tableau.get_workbooks()
print("\nAvailable Workbooks:")
print(workbooks)
```

### 2. Dashboard Image Export

```python
def export_dashboard_image(tableau, view_id, filename, filters=None):
    """
    Export dashboard as PNG image
    """
    endpoint = f'views/{view_id}/image'

    # Add filters to URL params
    params = {}
    if filters:
        for key, value in filters.items():
            params[f'vf_{key}'] = value

    # Get image
    image_data = tableau._make_request(endpoint, params=params)

    # Save to file
    with open(filename, 'wb') as f:
        f.write(image_data)

    print(f"Dashboard exported to {filename}")

    return filename

# Export marketing dashboard
# dashboard_image = export_dashboard_image(
#     tableau,
#     view_id='marketing_dashboard_view_id',
#     filename='marketing_dashboard.png',
#     filters={'Date Range': 'Last 30 Days'}
# )

def export_dashboard_pdf(tableau, view_id, filename):
    """Export dashboard as PDF"""
    endpoint = f'views/{view_id}/pdf'

    pdf_data = tableau._make_request(endpoint)

    with open(filename, 'wb') as f:
        f.write(pdf_data)

    print(f"PDF exported to {filename}")

    return filename

# Export weekly report
# weekly_report = export_dashboard_pdf(
#     tableau,
#     view_id='weekly_report_view_id',
#     filename='weekly_marketing_report.pdf'
# )
```

### 3. Data Refresh and Extract Management

```python
def refresh_datasource(tableau, datasource_id):
    """
    Trigger refresh of a data source extract
    """
    endpoint = f'datasources/{datasource_id}/refresh'

    response = tableau._make_request(endpoint, method='POST')

    print(f"Data source refresh initiated")

    return response

def get_refresh_tasks(tableau):
    """Get all refresh tasks"""
    response = tableau._make_request('tasks/extractRefreshes')
    root = ET.fromstring(response)

    tasks = []
    for task in root.findall('.//{http://tableau.com/api}extractRefresh'):
        tasks.append({
            'id': task.get('id'),
            'type': task.get('type'),
            'schedule_id': task.find('.//{http://tableau.com/api}schedule').get('id') if task.find('.//{http://tableau.com/api}schedule') is not None else None
        })

    return pd.DataFrame(tasks)

# Get all refresh tasks
refresh_tasks = get_refresh_tasks(tableau)
print("\nScheduled Refresh Tasks:")
print(refresh_tasks)

# Refresh marketing data source
# refresh_datasource(tableau, datasource_id='marketing_data_id')
```

### 4. Querying View Data

```python
def query_view_data(tableau, view_id, max_rows=10000):
    """
    Query data from a Tableau view
    """
    endpoint = f'views/{view_id}/data'

    params = {'maxRows': max_rows}

    # Get CSV data
    csv_data = tableau._make_request(endpoint, params=params)

    # Convert to DataFrame
    from io import StringIO
    df = pd.read_csv(StringIO(csv_data.decode('utf-8')))

    print(f"Retrieved {len(df)} rows from view")

    return df

# Query marketing metrics view
# marketing_data = query_view_data(
#     tableau,
#     view_id='marketing_metrics_view_id'
# )
#
# if marketing_data is not None:
#     print("\nMarketing Metrics:")
#     print(marketing_data.head())
#
#     # Analyze data
#     print(f"\nTotal Revenue: ${marketing_data['Revenue'].sum():,.2f}")
#     print(f"Total Orders: {marketing_data['Orders'].sum():,.0f}")
```

### 5. Workbook Publishing

```python
def publish_workbook(tableau, workbook_file, workbook_name, project_id):
    """
    Publish Tableau workbook to server
    """
    import os

    # Prepare multipart form data
    url = f"{tableau.server_url}/api/{tableau.api_version}/sites/{tableau.site_uuid}/workbooks"

    headers = {
        'X-Tableau-Auth': tableau.auth_token
    }

    # XML payload
    payload = f"""
    <tsRequest>
        <workbook name="{workbook_name}">
            <project id="{project_id}" />
        </workbook>
    </tsRequest>
    """

    files = {
        'request_payload': ('', payload, 'text/xml'),
        'tableau_workbook': (os.path.basename(workbook_file), open(workbook_file, 'rb'), 'application/octet-stream')
    }

    response = requests.post(url, headers=headers, files=files)
    response.raise_for_status()

    print(f"Workbook '{workbook_name}' published successfully")

    return response.content

# Publish updated workbook
# publish_workbook(
#     tableau,
#     workbook_file='marketing_dashboard.twbx',
#     workbook_name='Marketing Dashboard',
#     project_id='marketing_project_id'
# )
```

### 6. Embedded Analytics

```python
def generate_embed_url(tableau, view_id, embed_params=None):
    """
    Generate URL for embedding Tableau view
    Requires Tableau's JavaScript API on frontend
    """
    base_url = f"{tableau.server_url}/trusted/{tableau.auth_token}/views/{view_id}"

    # Add parameters
    if embed_params:
        params = '&'.join([f"{k}={v}" for k, v in embed_params.items()])
        base_url += f"?{params}"

    return base_url

# Generate embed URL with filters
embed_url = generate_embed_url(
    tableau,
    view_id='marketing_dashboard',
    embed_params={
        'Date Range': 'Last 30 Days',
        'Channel': 'Paid Search',
        ':embed': 'yes',
        ':toolbar': 'no'
    }
)

print(f"Embed URL: {embed_url}")

# Frontend HTML example
embed_html = f"""
<div id='tableauViz' style='width:100%; height:800px;'>
    <script type='text/javascript' src='https://tableau.yourcompany.com/javascripts/api/tableau-2.8.0.min.js'></script>
    <script type='text/javascript'>
        var containerDiv = document.getElementById('tableauViz'),
            url = '{embed_url}',
            options = {{
                hideTabs: true,
                hideToolbar: true,
                width: '100%',
                height: '800px'
            }};

        var viz = new tableau.Viz(containerDiv, url, options);
    </script>
</div>
"""
```

### 7. User and Permission Management

```python
def get_users(tableau):
    """Get all users on the site"""
    response = tableau._make_request('users')
    root = ET.fromstring(response)

    users = []
    for user in root.findall('.//{http://tableau.com/api}user'):
        users.append({
            'id': user.get('id'),
            'name': user.get('name'),
            'email': user.get('email'),
            'site_role': user.get('siteRole')
        })

    return pd.DataFrame(users)

def add_user_to_group(tableau, user_id, group_id):
    """Add user to a group"""
    endpoint = f'groups/{group_id}/users'

    payload = f"""
    <tsRequest>
        <user id="{user_id}" />
    </tsRequest>
    """

    response = tableau._make_request(endpoint, method='POST', data=payload)

    print(f"User added to group")

    return response

# Get all users
users = get_users(tableau)
print("\nUsers:")
print(users)
```

### 8. Subscription Management

```python
def create_subscription(tableau, view_id, schedule_id, user_id, subject):
    """
    Create subscription to send dashboard via email
    """
    endpoint = 'subscriptions'

    payload = f"""
    <tsRequest>
        <subscription subject="{subject}">
            <content type="View" id="{view_id}" />
            <schedule id="{schedule_id}" />
            <user id="{user_id}" />
        </subscription>
    </tsRequest>
    """

    response = tableau._make_request(endpoint, method='POST', data=payload)

    print(f"Subscription created: {subject}")

    return response

def get_subscriptions(tableau):
    """Get all subscriptions"""
    response = tableau._make_request('subscriptions')
    root = ET.fromstring(response)

    subscriptions = []
    for sub in root.findall('.//{http://tableau.com/api}subscription'):
        subscriptions.append({
            'id': sub.get('id'),
            'subject': sub.get('subject'),
            'user_id': sub.find('.//{http://tableau.com/api}user').get('id'),
            'schedule_id': sub.find('.//{http://tableau.com/api}schedule').get('id')
        })

    return pd.DataFrame(subscriptions)

# Get all subscriptions
subscriptions = get_subscriptions(tableau)
print("\nActive Subscriptions:")
print(subscriptions)

# Create new subscription
# create_subscription(
#     tableau,
#     view_id='marketing_dashboard_view_id',
#     schedule_id='weekly_schedule_id',
#     user_id='user_id',
#     subject='Weekly Marketing Performance Report'
# )
```

### 9. Tableau Hyper API (Data Loading)

```python
from tableauhyperapi import HyperProcess, Connection, TableDefinition, \
    SqlType, Telemetry, Inserter, CreateMode, TableName

def create_hyper_file(data, filename, table_name='Extract'):
    """
    Create Tableau Hyper file from DataFrame
    """
    # Define table schema
    table_def = TableDefinition(
        table_name=TableName('Extract', table_name),
        columns=[
            TableDefinition.Column('Date', SqlType.date()),
            TableDefinition.Column('Campaign', SqlType.text()),
            TableDefinition.Column('Impressions', SqlType.int()),
            TableDefinition.Column('Clicks', SqlType.int()),
            TableDefinition.Column('Cost', SqlType.double()),
            TableDefinition.Column('Revenue', SqlType.double())
        ]
    )

    with HyperProcess(Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(hyper.endpoint, filename, CreateMode.CREATE_AND_REPLACE) as connection:
            # Create table
            connection.catalog.create_table(table_def)

            # Insert data
            with Inserter(connection, table_def) as inserter:
                for _, row in data.iterrows():
                    inserter.add_row([
                        row['date'],
                        row['campaign'],
                        row['impressions'],
                        row['clicks'],
                        row['cost'],
                        row['revenue']
                    ])

                inserter.execute()

    print(f"Hyper file created: {filename}")

# Create Hyper file from marketing data
# marketing_data = pd.DataFrame({
#     'date': pd.date_range('2024-01-01', periods=30),
#     'campaign': ['Campaign A'] * 30,
#     'impressions': [1000, 1200, 1100, ...],
#     'clicks': [50, 60, 55, ...],
#     'cost': [100, 120, 110, ...],
#     'revenue': [500, 600, 550, ...]
# })
#
# create_hyper_file(marketing_data, 'marketing_data.hyper')
```

### 10. Calculated Field Automation

```python
def create_calculated_field_example():
    """
    Example calculated fields for marketing analytics
    Returns XML/JSON for Tableau workbook
    """
    calculated_fields = {
        'CTR': 'SUM([Clicks]) / SUM([Impressions])',
        'CPC': 'SUM([Cost]) / SUM([Clicks])',
        'Conversion Rate': 'SUM([Conversions]) / SUM([Clicks])',
        'ROAS': 'SUM([Revenue]) / SUM([Cost])',
        'CPA': 'SUM([Cost]) / SUM([Conversions])',
        'Revenue per Click': 'SUM([Revenue]) / SUM([Clicks])'
    }

    print("Marketing Calculated Fields:")
    for name, formula in calculated_fields.items():
        print(f"  {name}: {formula}")

    return calculated_fields

# Get calculated field examples
calc_fields = create_calculated_field_example()
```

## Installation

```bash
# Tableau Server API
uv pip install requests pandas lxml

# Tableau Hyper API (for data extracts)
uv pip install tableauhyperapi

# Tableau Document API (for workbook manipulation)
uv pip install tableaudocumentapi
```

## Authentication

1. Log in to Tableau Server/Cloud
2. Navigate to Settings > Personal Access Tokens (for token-based auth)
   OR use username/password authentication
3. Generate a token with appropriate permissions
4. Use token or credentials for API access

## Quick Start

```python
import requests
import xml.etree.ElementTree as ET

# Tableau Server details
SERVER_URL = 'https://tableau.yourcompany.com'
USERNAME = 'your_username'
PASSWORD = 'your_password'
SITE_ID = 'marketing'

# Sign in
signin_url = f'{SERVER_URL}/api/3.19/auth/signin'
payload = f"""
<tsRequest>
    <credentials name="{USERNAME}" password="{PASSWORD}">
        <site contentUrl="{SITE_ID}" />
    </credentials>
</tsRequest>
"""

response = requests.post(signin_url, data=payload)
root = ET.fromstring(response.content)

auth_token = root.find('.//{http://tableau.com/api}credentials').get('token')
site_id = root.find('.//{http://tableau.com/api}site').get('id')

print(f"Authenticated! Token: {auth_token[:20]}...")

# Get workbooks
headers = {'X-Tableau-Auth': auth_token}
workbooks_url = f'{SERVER_URL}/api/3.19/sites/{site_id}/workbooks'
workbooks = requests.get(workbooks_url, headers=headers)

print(f"Workbooks: {workbooks.status_code}")
```

## Key Features

- **Interactive Dashboards**: Drag-and-drop dashboard creation
- **Data Blending**: Combine data from multiple sources
- **Calculated Fields**: Custom metrics and KPIs
- **Server API**: Automate publishing and refreshes
- **Embedded Analytics**: Embed dashboards in applications
- **Hyper Extracts**: Fast in-memory data engine
- **Mobile Ready**: Responsive dashboards

## References

- [Tableau REST API Documentation](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api.htm)
- [Tableau Hyper API](https://help.tableau.com/current/api/hyper_api/en-us/index.html)
- [Tableau JavaScript API](https://help.tableau.com/current/api/js_api/en-us/JavaScriptAPI/js_api.htm)
- [Tableau Document API](https://tableau.github.io/document-api-python/)

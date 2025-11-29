---
skill_name: fivetran
display_name: Fivetran
description: Automated data integration and ETL for syncing marketing data to warehouses
category: cdp-data
tags: [etl, data-integration, automation, connectors, marketing-data]
complexity: beginner
dependencies: [fivetran-provider-sdk]
---

# Fivetran

## Overview

Fivetran is an automated data integration platform that syncs data from SaaS applications, databases, and files into your data warehouse. For marketing teams, Fivetran eliminates the need to build and maintain custom ETL pipelines for marketing platforms.

Fivetran excels at:
- **Fully Managed Connectors**: 300+ pre-built connectors for marketing platforms
- **Automated Schema Migrations**: Adapt to API changes automatically
- **Incremental Sync**: Efficient syncing of only new/changed data
- **Reliable Data Delivery**: Guaranteed data consistency with retry logic
- **Zero Maintenance**: No infrastructure to manage or code to maintain
- **Marketing Platform Support**: Native connectors for ads, analytics, and CRM

## When to Use

Use Fivetran when you need to:
- **Centralize Marketing Data**: Sync all marketing platforms to one warehouse
- **Zero Maintenance ETL**: Eliminate custom pipeline development and maintenance
- **Reliable Data Pipelines**: Ensure consistent data delivery with automatic retries
- **Fast Implementation**: Set up data pipelines in minutes, not weeks
- **Scale Data Operations**: Handle growing data volumes without infrastructure changes
- **Multi-Platform Analytics**: Combine data from Google Ads, Facebook, Salesforce, etc.
- **Data Warehouse Agnostic**: Support for Snowflake, BigQuery, Redshift, Databricks

## Core Capabilities

### 1. Marketing Platform Connectors

**Available Marketing Connectors**

```python
# Fivetran supports 300+ connectors, key marketing platforms include:

marketing_connectors = {
    # Ad Platforms
    'google_ads': 'Google Ads campaigns, ad groups, keywords, performance',
    'facebook_ads': 'Facebook Ads campaigns, ads, insights, conversions',
    'linkedin_ads': 'LinkedIn Campaign Manager data',
    'tiktok_ads': 'TikTok Ads campaigns and performance',
    'snapchat_ads': 'Snapchat Ads data',
    'twitter_ads': 'Twitter Ads campaigns',
    'pinterest_ads': 'Pinterest Ads performance',
    'amazon_ads': 'Amazon Advertising data',

    # Analytics
    'google_analytics_4': 'GA4 events and user data',
    'google_analytics_360': 'GA360 premium analytics',
    'adobe_analytics': 'Adobe Analytics data',
    'mixpanel': 'Product analytics events',
    'amplitude': 'Behavioral analytics',

    # Marketing Automation
    'hubspot': 'Contacts, deals, campaigns, emails',
    'marketo': 'Leads, programs, campaigns',
    'mailchimp': 'Email campaigns and subscribers',
    'sendgrid': 'Email delivery and engagement',

    # CRM
    'salesforce': 'Accounts, opportunities, contacts',
    'zendesk': 'Support tickets and customer data',

    # Customer Data Platforms
    'segment': 'Event tracking and user profiles',
    'rudderstack': 'CDP events and audiences',

    # eCommerce
    'shopify': 'Orders, products, customers',
    'stripe': 'Payments and subscriptions',
    'amazon_seller_central': 'Sales and inventory',

    # Social Media
    'instagram_business': 'Instagram insights',
    'youtube_analytics': 'Video performance',
    'linkedin_company_pages': 'Company page analytics'
}
```

**Setting Up Connectors (API)**

```python
import requests
import json

class FivetranConnector:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.fivetran.com/v1"
        self.auth = (api_key, api_secret)

    def create_connector(self, group_id, service, config):
        """Create a new Fivetran connector"""

        url = f"{self.base_url}/connectors"

        payload = {
            "group_id": group_id,
            "service": service,
            "config": config
        }

        response = requests.post(
            url,
            auth=self.auth,
            headers={"Content-Type": "application/json"},
            json=payload
        )

        return response.json()

    def sync_connector(self, connector_id):
        """Trigger a manual sync"""

        url = f"{self.base_url}/connectors/{connector_id}/force"

        response = requests.post(url, auth=self.auth)
        return response.json()

    def get_connector_status(self, connector_id):
        """Check connector sync status"""

        url = f"{self.base_url}/connectors/{connector_id}"

        response = requests.get(url, auth=self.auth)
        return response.json()

# Example: Set up Google Ads connector
fivetran = FivetranConnector(
    api_key="your_api_key",
    api_secret="your_api_secret"
)

google_ads_config = {
    "schema": "google_ads_data",
    "customer_id": "1234567890",
    "manager_accounts": ["9876543210"]
}

connector = fivetran.create_connector(
    group_id="your_group_id",
    service="google_ads",
    config=google_ads_config
)

print(f"Created connector: {connector['data']['id']}")

# Trigger sync
fivetran.sync_connector(connector['data']['id'])
```

### 2. Data Ingestion and Syncing

**Automated Sync Configuration**

```python
class FivetranSyncManager:
    def __init__(self, api_key, api_secret):
        self.client = FivetranConnector(api_key, api_secret)

    def setup_marketing_stack(self, group_id, warehouse_config):
        """
        Set up complete marketing data stack

        warehouse_config: {
            'type': 'snowflake',  # or 'bigquery', 'redshift'
            'credentials': {...}
        }
        """

        connectors_to_create = [
            {
                'service': 'google_ads',
                'config': {
                    'schema': 'google_ads',
                    'customer_id': warehouse_config.get('google_ads_customer_id')
                }
            },
            {
                'service': 'facebook_ads',
                'config': {
                    'schema': 'facebook_ads',
                    'account_id': warehouse_config.get('facebook_account_id')
                }
            },
            {
                'service': 'google_analytics_4',
                'config': {
                    'schema': 'ga4',
                    'property_id': warehouse_config.get('ga4_property_id')
                }
            },
            {
                'service': 'hubspot',
                'config': {
                    'schema': 'hubspot'
                }
            },
            {
                'service': 'salesforce',
                'config': {
                    'schema': 'salesforce'
                }
            }
        ]

        created_connectors = []

        for connector_config in connectors_to_create:
            try:
                result = self.client.create_connector(
                    group_id=group_id,
                    service=connector_config['service'],
                    config=connector_config['config']
                )
                created_connectors.append(result['data'])
                print(f"Created {connector_config['service']} connector")
            except Exception as e:
                print(f"Error creating {connector_config['service']}: {e}")

        return created_connectors

    def monitor_syncs(self, connector_ids):
        """Monitor sync status for all connectors"""

        status_report = []

        for connector_id in connector_ids:
            status = self.client.get_connector_status(connector_id)
            connector_data = status['data']

            status_report.append({
                'connector_id': connector_id,
                'schema': connector_data['schema'],
                'service': connector_data['service'],
                'status': connector_data['status']['setup_state'],
                'sync_state': connector_data['status']['sync_state'],
                'succeeded_at': connector_data['succeeded_at'],
                'failed_at': connector_data['failed_at']
            })

        return status_report

# Example usage
manager = FivetranSyncManager(
    api_key="your_api_key",
    api_secret="your_api_secret"
)

# Set up all marketing connectors
warehouse_config = {
    'type': 'snowflake',
    'google_ads_customer_id': '1234567890',
    'facebook_account_id': 'act_123456',
    'ga4_property_id': '123456789'
}

connectors = manager.setup_marketing_stack(
    group_id="your_group_id",
    warehouse_config=warehouse_config
)

# Monitor syncs
connector_ids = [c['id'] for c in connectors]
sync_status = manager.monitor_syncs(connector_ids)

for status in sync_status:
    print(f"{status['service']}: {status['sync_state']}")
```

### 3. Querying Synced Marketing Data

**Standardized Table Schemas**

```sql
-- Fivetran creates standardized schemas for each connector
-- Example: Google Ads tables in Snowflake/BigQuery/Redshift

-- Campaign performance
SELECT
    date,
    campaign_name,
    campaign_id,
    impressions,
    clicks,
    cost_micros / 1000000 as cost,
    conversions,
    conversions_value,
    ROUND(cost_micros / 1000000 / NULLIF(clicks, 0), 2) as cpc,
    ROUND(conversions_value / NULLIF(cost_micros / 1000000, 0), 2) as roas
FROM google_ads.campaign_stats
WHERE date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY cost DESC;

-- Ad group performance
SELECT
    c.campaign_name,
    ag.ad_group_name,
    SUM(ags.impressions) as impressions,
    SUM(ags.clicks) as clicks,
    SUM(ags.cost_micros) / 1000000 as spend,
    SUM(ags.conversions) as conversions
FROM google_ads.ad_group_stats ags
JOIN google_ads.ad_group ag ON ags.ad_group_id = ag.id
JOIN google_ads.campaign c ON ag.campaign_id = c.id
WHERE ags.date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY c.campaign_name, ag.ad_group_name
ORDER BY spend DESC;

-- Facebook Ads performance
SELECT
    date,
    campaign_name,
    adset_name,
    impressions,
    clicks,
    spend,
    actions_value,  -- Purchase value
    ROUND(spend / NULLIF(clicks, 0), 2) as cpc,
    ROUND(actions_value / NULLIF(spend, 0), 2) as roas
FROM facebook_ads.ads_insights
WHERE date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY spend DESC;

-- HubSpot email campaign performance
SELECT
    c.name as campaign_name,
    e.subject,
    e.sent,
    e.delivered,
    e.opens,
    e.clicks,
    ROUND(100.0 * e.delivered / NULLIF(e.sent, 0), 2) as delivery_rate,
    ROUND(100.0 * e.opens / NULLIF(e.delivered, 0), 2) as open_rate,
    ROUND(100.0 * e.clicks / NULLIF(e.delivered, 0), 2) as click_rate
FROM hubspot.email_event e
JOIN hubspot.email_campaign c ON e.campaign_id = c.id
WHERE e.created >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY c.name, e.subject, e.sent, e.delivered, e.opens, e.clicks;
```

### 4. Cross-Platform Marketing Analytics

**Unified Marketing Performance Dashboard**

```sql
-- Combine all ad platforms for unified reporting
WITH google_ads_data AS (
    SELECT
        date,
        'google_ads' as platform,
        campaign_name,
        cost_micros / 1000000 as spend,
        impressions,
        clicks,
        conversions,
        conversions_value as revenue
    FROM google_ads.campaign_stats
    WHERE date >= CURRENT_DATE - INTERVAL '30 days'
),
facebook_ads_data AS (
    SELECT
        date,
        'facebook_ads' as platform,
        campaign_name,
        spend,
        impressions,
        clicks,
        actions as conversions,
        actions_value as revenue
    FROM facebook_ads.ads_insights
    WHERE date >= CURRENT_DATE - INTERVAL '30 days'
        AND action_type = 'purchase'
),
linkedin_ads_data AS (
    SELECT
        date,
        'linkedin_ads' as platform,
        campaign_name,
        cost_in_usd as spend,
        impressions,
        clicks,
        conversions,
        conversion_value_in_local_currency as revenue
    FROM linkedin_ads.ad_analytics_by_campaign
    WHERE date >= CURRENT_DATE - INTERVAL '30 days'
),
all_platforms AS (
    SELECT * FROM google_ads_data
    UNION ALL
    SELECT * FROM facebook_ads_data
    UNION ALL
    SELECT * FROM linkedin_ads_data
)
SELECT
    date,
    platform,
    campaign_name,
    SUM(spend) as total_spend,
    SUM(impressions) as total_impressions,
    SUM(clicks) as total_clicks,
    SUM(conversions) as total_conversions,
    SUM(revenue) as total_revenue,
    ROUND(SUM(spend) / NULLIF(SUM(clicks), 0), 2) as cpc,
    ROUND(100.0 * SUM(clicks) / NULLIF(SUM(impressions), 0), 2) as ctr,
    ROUND(SUM(revenue) / NULLIF(SUM(spend), 0), 2) as roas,
    ROUND(SUM(spend) / NULLIF(SUM(conversions), 0), 2) as cpa
FROM all_platforms
GROUP BY date, platform, campaign_name
ORDER BY date DESC, total_spend DESC;
```

**Customer Journey with Multi-Source Data**

```python
import pandas as pd
from sqlalchemy import create_engine

def analyze_customer_journey(warehouse_conn):
    """
    Analyze complete customer journey using Fivetran-synced data
    from multiple sources
    """

    query = """
    WITH customer_touchpoints AS (
        -- GA4 web interactions
        SELECT
            user_id,
            event_timestamp as timestamp,
            'website' as touchpoint_type,
            event_name,
            traffic_source.source as source,
            traffic_source.medium as medium
        FROM ga4.events_*
        WHERE _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY))

        UNION ALL

        -- Email interactions from HubSpot
        SELECT
            contact_id as user_id,
            created as timestamp,
            'email' as touchpoint_type,
            type as event_name,
            'hubspot' as source,
            'email' as medium
        FROM hubspot.email_event

        UNION ALL

        -- Ad clicks from Google Ads
        SELECT
            user_id,
            click_timestamp as timestamp,
            'paid_ad' as touchpoint_type,
            'ad_click' as event_name,
            'google' as source,
            'cpc' as medium
        FROM google_ads.click_view

        UNION ALL

        -- Sales interactions from Salesforce
        SELECT
            contact_id as user_id,
            created_date as timestamp,
            'sales' as touchpoint_type,
            stage_name as event_name,
            'salesforce' as source,
            'crm' as medium
        FROM salesforce.opportunity
    ),
    customer_conversions AS (
        SELECT
            user_id,
            MIN(close_date) as first_conversion,
            SUM(amount) as total_revenue
        FROM salesforce.opportunity
        WHERE is_won = TRUE
        GROUP BY user_id
    )
    SELECT
        t.user_id,
        t.timestamp,
        t.touchpoint_type,
        t.event_name,
        t.source,
        t.medium,
        c.first_conversion,
        c.total_revenue,
        ROW_NUMBER() OVER (PARTITION BY t.user_id ORDER BY t.timestamp) as touch_number
    FROM customer_touchpoints t
    LEFT JOIN customer_conversions c ON t.user_id = c.user_id
    ORDER BY t.user_id, t.timestamp
    """

    df = pd.read_sql(query, warehouse_conn)
    return df

# Analyze journey
journey_df = analyze_customer_journey(warehouse_connection)
print(f"Analyzed {len(journey_df)} touchpoints across {journey_df['user_id'].nunique()} customers")
```

## Installation and Authentication

### Fivetran API Setup

```python
# Install Fivetran Python SDK (unofficial)
# pip install fivetran-provider-sdk

import requests
from requests.auth import HTTPBasicAuth

class FivetranAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.fivetran.com/v1"
        self.auth = HTTPBasicAuth(api_key, api_secret)

    def get_groups(self):
        """List all groups (destinations)"""
        response = requests.get(
            f"{self.base_url}/groups",
            auth=self.auth
        )
        return response.json()

    def get_connectors(self, group_id):
        """List connectors in a group"""
        response = requests.get(
            f"{self.base_url}/groups/{group_id}/connectors",
            auth=self.auth
        )
        return response.json()

    def get_connector_schema(self, connector_id):
        """Get schema configuration for a connector"""
        response = requests.get(
            f"{self.base_url}/connectors/{connector_id}/schemas",
            auth=self.auth
        )
        return response.json()

# Initialize
fivetran = FivetranAPI(
    api_key="your_api_key",
    api_secret="your_api_secret"
)

# List all groups
groups = fivetran.get_groups()
print(f"Found {len(groups['data']['items'])} destination groups")
```

### Webhook Integration

```python
from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

@app.route('/fivetran-webhook', methods=['POST'])
def fivetran_webhook():
    """
    Receive Fivetran sync completion webhooks
    for triggering downstream processes
    """

    # Verify webhook signature
    signature = request.headers.get('X-Fivetran-Signature')
    body = request.get_data()

    # Validate signature (use your webhook secret)
    webhook_secret = "your_webhook_secret"
    expected_signature = hmac.new(
        webhook_secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if signature != expected_signature:
        return "Invalid signature", 401

    # Process webhook
    data = request.json

    if data['type'] == 'sync_end':
        connector_id = data['connector_id']
        schema = data['schema']
        success = data['success']

        if success:
            print(f"Sync completed for {schema}")
            # Trigger downstream processes (dbt, reverse ETL, etc.)
            trigger_dbt_run(schema)
            trigger_audience_sync(schema)

        else:
            print(f"Sync failed for {schema}")
            send_alert(f"Fivetran sync failed for {schema}")

    return "OK", 200

def trigger_dbt_run(schema):
    """Trigger dbt transformations after Fivetran sync"""
    pass

def trigger_audience_sync(schema):
    """Trigger reverse ETL to sync audiences"""
    pass

def send_alert(message):
    """Send alert for failed syncs"""
    pass
```

## Quick Start

### Complete Setup Workflow

```python
from fivetran_api import FivetranAPI
import os

# 1. Initialize Fivetran
fivetran = FivetranAPI(
    api_key=os.getenv("FIVETRAN_API_KEY"),
    api_secret=os.getenv("FIVETRAN_API_SECRET")
)

# 2. Create destination group (Snowflake)
group_config = {
    "name": "Marketing Data Warehouse",
    "destination": {
        "type": "snowflake",
        "config": {
            "host": "your-account.snowflakecomputing.com",
            "port": 443,
            "database": "marketing_data",
            "auth": "PASSWORD",
            "user": "fivetran_user",
            "password": "your_password"
        }
    }
}

# 3. Set up marketing connectors
connectors = [
    {'service': 'google_ads', 'schema': 'google_ads'},
    {'service': 'facebook_ads', 'schema': 'facebook_ads'},
    {'service': 'google_analytics_4', 'schema': 'ga4'},
    {'service': 'hubspot', 'schema': 'hubspot'},
    {'service': 'salesforce', 'schema': 'salesforce'}
]

for connector in connectors:
    print(f"Setting up {connector['service']}...")
    # Create connector via UI or API

# 4. Monitor sync status
groups = fivetran.get_groups()
for group in groups['data']['items']:
    connectors = fivetran.get_connectors(group['id'])
    for conn in connectors['data']['items']:
        print(f"{conn['schema']}: {conn['status']['sync_state']}")

print("Fivetran setup complete!")
```

## References

- **Official Documentation**: https://fivetran.com/docs
- **API Documentation**: https://fivetran.com/docs/rest-api
- **Connector Documentation**: https://fivetran.com/docs/connectors
- **Schema Information**: https://fivetran.com/docs/schema-information
- **Webhooks**: https://fivetran.com/docs/logs/webhooks
- **Best Practices**: https://fivetran.com/docs/getting-started/fivetran-dashboard/best-practices
- **Pricing Calculator**: https://fivetran.com/pricing
- **dbt Integration**: https://fivetran.com/docs/transformations/dbt
- **Security**: https://fivetran.com/docs/security
- **Support Resources**: https://support.fivetran.com/

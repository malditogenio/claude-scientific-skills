---
skill_name: census
display_name: Census
description: Reverse ETL platform for syncing warehouse data to marketing and sales tools
category: cdp-data
tags: [reverse-etl, data-activation, audience-sync, operational-analytics]
complexity: intermediate
dependencies: [census-api, requests]
---

# Census

## Overview

Census is a Reverse ETL platform that syncs data from your data warehouse to marketing, sales, and business tools. Instead of building custom integrations, Census enables you to activate your warehouse data directly in the tools your teams use every day.

Census excels at:
- **Warehouse-Native**: Use your warehouse as the source of truth
- **No-Code Sync**: Build syncs with SQL and UI, no coding required
- **Real-Time Activation**: Sync audiences and data on demand or schedule
- **200+ Destinations**: Connect to all major marketing and sales tools
- **Audience Hub**: Build and manage audiences in your warehouse
- **Field Mapping**: Flexible mapping between warehouse and destination fields

## When to Use

Use Census when you need to:
- **Activate Warehouse Data**: Sync customer segments from warehouse to marketing tools
- **Reverse ETL**: Send enriched data back to operational systems
- **Audience Management**: Build audiences in warehouse, activate in ad platforms
- **Lead Scoring**: Sync ML-predicted scores to CRM and marketing automation
- **Personalization**: Power personalization engines with warehouse data
- **Customer 360 Activation**: Distribute unified profiles to all business tools
- **Operational Analytics**: Keep business tools in sync with warehouse insights

## Core Capabilities

### 1. Warehouse to Marketing Tool Syncs

**Connecting Data Sources**

```python
import requests
import json

class CensusAPI:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://app.getcensus.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    def create_source(self, source_config):
        """Create warehouse source connection"""

        response = requests.post(
            f"{self.base_url}/sources",
            headers=self.headers,
            json=source_config
        )
        return response.json()

    def create_destination(self, destination_config):
        """Create destination tool connection"""

        response = requests.post(
            f"{self.base_url}/destinations",
            headers=self.headers,
            json=destination_config
        )
        return response.json()

    def create_sync(self, sync_config):
        """Create data sync from warehouse to destination"""

        response = requests.post(
            f"{self.base_url}/syncs",
            headers=self.headers,
            json=sync_config
        )
        return response.json()

    def trigger_sync(self, sync_id):
        """Manually trigger a sync"""

        response = requests.post(
            f"{self.base_url}/syncs/{sync_id}/trigger",
            headers=self.headers
        )
        return response.json()

    def get_sync_status(self, sync_id):
        """Get sync execution status"""

        response = requests.get(
            f"{self.base_url}/syncs/{sync_id}",
            headers=self.headers
        )
        return response.json()

# Example: Connect Snowflake as source
census = CensusAPI(api_token="your_census_token")

snowflake_source = census.create_source({
    "name": "Snowflake Marketing Warehouse",
    "type": "snowflake",
    "credentials": {
        "account": "your-account.snowflakecomputing.com",
        "warehouse": "COMPUTE_WH",
        "database": "MARKETING_DATA",
        "schema": "ANALYTICS",
        "username": "census_user",
        "password": "password"
    }
})

print(f"Created source: {snowflake_source['id']}")
```

### 2. Audience Sync to Ad Platforms

**Sync to Facebook Custom Audiences**

```python
class CensusAudienceSync:
    def __init__(self, api_token):
        self.census = CensusAPI(api_token)

    def sync_to_facebook_custom_audience(self, source_id, audience_query):
        """
        Sync warehouse audience to Facebook Custom Audiences

        audience_query: SQL query that returns users to sync
        """

        # Create Facebook destination
        facebook_dest = self.census.create_destination({
            "name": "Facebook Ads",
            "type": "facebook_custom_audiences",
            "credentials": {
                "access_token": "your_facebook_access_token",
                "ad_account_id": "act_123456"
            }
        })

        # Create sync configuration
        sync_config = {
            "source_id": source_id,
            "destination_id": facebook_dest['id'],
            "source_attributes": {
                "type": "query",
                "query": audience_query
            },
            "mappings": [
                {
                    "from": "email",
                    "to": "email"
                },
                {
                    "from": "phone",
                    "to": "phone"
                },
                {
                    "from": "user_id",
                    "to": "external_id"
                }
            ],
            "operation": "upsert",
            "schedule": {
                "frequency": "daily",
                "hour": 2  # 2 AM UTC
            }
        }

        sync = self.census.create_sync(sync_config)

        # Trigger initial sync
        self.census.trigger_sync(sync['id'])

        return sync

# Example: Sync high-value customers to Facebook
syncer = CensusAudienceSync(api_token="your_token")

high_value_query = """
SELECT
    user_id,
    email,
    phone,
    name
FROM marketing_data.customer_360
WHERE customer_tier = 'high_value'
    AND revenue_90d > 1000
    AND days_since_purchase <= 30
"""

fb_sync = syncer.sync_to_facebook_custom_audience(
    source_id="snowflake_source_id",
    audience_query=high_value_query
)

print(f"Created Facebook sync: {fb_sync['id']}")
```

**Sync to Google Ads Customer Match**

```python
def sync_to_google_customer_match(census_api, source_id, audience_query):
    """Sync audience to Google Ads Customer Match"""

    # Create Google Ads destination
    google_ads_dest = census_api.create_destination({
        "name": "Google Ads",
        "type": "google_ads",
        "credentials": {
            "customer_id": "1234567890",
            "developer_token": "your_developer_token",
            "refresh_token": "your_refresh_token"
        }
    })

    # Create sync
    sync = census_api.create_sync({
        "source_id": source_id,
        "destination_id": google_ads_dest['id'],
        "source_attributes": {
            "type": "query",
            "query": audience_query
        },
        "destination_attributes": {
            "object": "customer_match_user_list",
            "user_list_id": "your_user_list_id"
        },
        "mappings": [
            {"from": "email", "to": "email"},
            {"from": "phone", "to": "phone"},
            {"from": "first_name", "to": "first_name"},
            {"from": "last_name", "to": "last_name"},
            {"from": "country", "to": "country"},
            {"from": "zip_code", "to": "zip_code"}
        ],
        "operation": "mirror",  # Keep destination in sync with source
        "schedule": {
            "frequency": "hourly",
            "minute": 0
        }
    })

    return sync

# Example: Sync cart abandoners
cart_abandoner_query = """
SELECT
    user_id,
    email,
    phone,
    SPLIT_PART(name, ' ', 1) as first_name,
    SPLIT_PART(name, ' ', -1) as last_name,
    country,
    zip_code
FROM marketing_data.audiences.cart_abandoners
WHERE last_cart_add >= CURRENT_DATE - INTERVAL '7 days'
"""

google_sync = sync_to_google_customer_match(
    census,
    "snowflake_source_id",
    cart_abandoner_query
)
```

### 3. Multi-Platform Audience Activation

**Sync to Multiple Platforms Simultaneously**

```python
def activate_audience_multi_platform(census_api, source_id, platforms):
    """
    Activate a single audience across multiple platforms

    platforms: dict of platform configs
    """

    # Base audience query
    base_query = """
    SELECT
        user_id,
        email,
        phone,
        name,
        SPLIT_PART(name, ' ', 1) as first_name,
        SPLIT_PART(name, ' ', -1) as last_name,
        country,
        zip_code,
        customer_tier,
        lifetime_revenue
    FROM marketing_data.customer_360
    WHERE customer_tier = 'high_value'
        AND revenue_90d > 1000
    """

    syncs = []

    # Sync to Facebook
    if 'facebook' in platforms:
        fb_sync = census_api.create_sync({
            "source_id": source_id,
            "destination_id": platforms['facebook']['destination_id'],
            "source_attributes": {"type": "query", "query": base_query},
            "destination_attributes": {
                "object": "custom_audience",
                "audience_id": platforms['facebook']['audience_id']
            },
            "mappings": [
                {"from": "email", "to": "email"},
                {"from": "phone", "to": "phone"}
            ],
            "operation": "mirror",
            "schedule": {"frequency": "daily", "hour": 2}
        })
        syncs.append(('facebook', fb_sync))

    # Sync to Google Ads
    if 'google_ads' in platforms:
        google_sync = census_api.create_sync({
            "source_id": source_id,
            "destination_id": platforms['google_ads']['destination_id'],
            "source_attributes": {"type": "query", "query": base_query},
            "destination_attributes": {
                "object": "customer_match_user_list",
                "user_list_id": platforms['google_ads']['list_id']
            },
            "mappings": [
                {"from": "email", "to": "email"},
                {"from": "phone", "to": "phone"},
                {"from": "first_name", "to": "first_name"},
                {"from": "last_name", "to": "last_name"}
            ],
            "operation": "mirror",
            "schedule": {"frequency": "daily", "hour": 2}
        })
        syncs.append(('google_ads', google_sync))

    # Sync to Braze for email/push
    if 'braze' in platforms:
        braze_sync = census_api.create_sync({
            "source_id": source_id,
            "destination_id": platforms['braze']['destination_id'],
            "source_attributes": {"type": "query", "query": base_query},
            "destination_attributes": {
                "object": "user"
            },
            "mappings": [
                {"from": "user_id", "to": "external_id"},
                {"from": "email", "to": "email"},
                {"from": "customer_tier", "to": "customer_tier"},
                {"from": "lifetime_revenue", "to": "lifetime_value"}
            ],
            "operation": "upsert",
            "schedule": {"frequency": "hourly"}
        })
        syncs.append(('braze', braze_sync))

    # Sync to HubSpot for marketing automation
    if 'hubspot' in platforms:
        hubspot_sync = census_api.create_sync({
            "source_id": source_id,
            "destination_id": platforms['hubspot']['destination_id'],
            "source_attributes": {"type": "query", "query": base_query},
            "destination_attributes": {
                "object": "contact"
            },
            "mappings": [
                {"from": "email", "to": "email"},
                {"from": "customer_tier", "to": "customer_tier"},
                {"from": "lifetime_revenue", "to": "lifetime_value"}
            ],
            "operation": "upsert",
            "schedule": {"frequency": "hourly"}
        })
        syncs.append(('hubspot', hubspot_sync))

    # Trigger all syncs
    for platform, sync in syncs:
        census_api.trigger_sync(sync['id'])
        print(f"Triggered {platform} sync: {sync['id']}")

    return syncs

# Example usage
platforms = {
    'facebook': {
        'destination_id': 'fb_dest_id',
        'audience_id': '23850000000000000'
    },
    'google_ads': {
        'destination_id': 'google_dest_id',
        'list_id': '1234567890'
    },
    'braze': {
        'destination_id': 'braze_dest_id'
    },
    'hubspot': {
        'destination_id': 'hubspot_dest_id'
    }
}

syncs = activate_audience_multi_platform(
    census,
    "snowflake_source_id",
    platforms
)
```

### 4. Dynamic Audience Management

**Create and Sync Multiple Audience Segments**

```python
class CensusAudienceManager:
    def __init__(self, api_token):
        self.census = CensusAPI(api_token)

    def create_audience_segments(self, source_id, destination_configs):
        """
        Create multiple audience segments and sync to destinations

        destination_configs: list of {
            'name': str,
            'query': str,
            'destinations': [...]
        }
        """

        segment_syncs = []

        for segment in destination_configs:
            print(f"Creating segment: {segment['name']}")

            # Create syncs for each destination
            for dest in segment['destinations']:
                sync = self.census.create_sync({
                    "name": f"{segment['name']} -> {dest['platform']}",
                    "source_id": source_id,
                    "destination_id": dest['destination_id'],
                    "source_attributes": {
                        "type": "query",
                        "query": segment['query']
                    },
                    "mappings": dest['mappings'],
                    "operation": dest.get('operation', 'mirror'),
                    "schedule": dest.get('schedule', {
                        "frequency": "daily",
                        "hour": 2
                    })
                })

                segment_syncs.append({
                    'segment': segment['name'],
                    'platform': dest['platform'],
                    'sync_id': sync['id']
                })

        return segment_syncs

# Example: Create multiple audience segments
manager = CensusAudienceManager(api_token="your_token")

audience_segments = [
    {
        'name': 'High Value Customers',
        'query': """
            SELECT user_id, email, phone
            FROM marketing_data.customer_360
            WHERE revenue_90d > 1000
        """,
        'destinations': [
            {
                'platform': 'facebook',
                'destination_id': 'fb_dest_id',
                'mappings': [
                    {'from': 'email', 'to': 'email'},
                    {'from': 'phone', 'to': 'phone'}
                ]
            },
            {
                'platform': 'google_ads',
                'destination_id': 'google_dest_id',
                'mappings': [
                    {'from': 'email', 'to': 'email'}
                ]
            }
        ]
    },
    {
        'name': 'Churn Risk',
        'query': """
            SELECT user_id, email, name, churn_probability
            FROM marketing_data.churn_predictions
            WHERE churn_probability > 0.7
        """,
        'destinations': [
            {
                'platform': 'braze',
                'destination_id': 'braze_dest_id',
                'mappings': [
                    {'from': 'user_id', 'to': 'external_id'},
                    {'from': 'email', 'to': 'email'},
                    {'from': 'churn_probability', 'to': 'churn_risk_score'}
                ],
                'operation': 'upsert'
            }
        ]
    },
    {
        'name': 'High Intent Prospects',
        'query': """
            SELECT user_id, email, predicted_ltv
            FROM marketing_data.ltv_predictions
            WHERE predicted_ltv > 500
                AND total_orders = 0
            ORDER BY predicted_ltv DESC
            LIMIT 10000
        """,
        'destinations': [
            {
                'platform': 'facebook',
                'destination_id': 'fb_dest_id',
                'mappings': [
                    {'from': 'email', 'to': 'email'}
                ]
            },
            {
                'platform': 'salesforce',
                'destination_id': 'sf_dest_id',
                'mappings': [
                    {'from': 'email', 'to': 'Email'},
                    {'from': 'predicted_ltv', 'to': 'Predicted_LTV__c'}
                ],
                'operation': 'upsert'
            }
        ]
    }
]

syncs = manager.create_audience_segments(
    source_id="snowflake_source_id",
    destination_configs=audience_segments
)

print(f"\nCreated {len(syncs)} syncs across {len(audience_segments)} segments")
```

## Installation and Authentication

### Census API Setup

```python
import requests

class CensusClient:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://app.getcensus.com/api/v1"

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def list_sources(self):
        """List all configured sources"""
        response = requests.get(
            f"{self.base_url}/sources",
            headers=self.get_headers()
        )
        return response.json()

    def list_destinations(self):
        """List all configured destinations"""
        response = requests.get(
            f"{self.base_url}/destinations",
            headers=self.get_headers()
        )
        return response.json()

    def list_syncs(self):
        """List all syncs"""
        response = requests.get(
            f"{self.base_url}/syncs",
            headers=self.get_headers()
        )
        return response.json()

# Initialize
census = CensusClient(api_token="your_census_api_token")

# List resources
sources = census.list_sources()
print(f"Sources: {len(sources)}")

destinations = census.list_destinations()
print(f"Destinations: {len(destinations)}")
```

### Webhook Integration

```python
from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

@app.route('/census-webhook', methods=['POST'])
def census_webhook():
    """
    Receive Census sync completion webhooks
    """

    # Verify signature (optional but recommended)
    signature = request.headers.get('X-Census-Signature')
    webhook_secret = "your_webhook_secret"

    # Process webhook payload
    data = request.json

    if data['event_type'] == 'sync.success':
        sync_id = data['sync_id']
        records_processed = data['records_processed']

        print(f"Sync {sync_id} completed: {records_processed} records")

        # Trigger downstream actions
        # e.g., notify team, update dashboard, trigger campaigns

    elif data['event_type'] == 'sync.failed':
        sync_id = data['sync_id']
        error = data['error_message']

        print(f"Sync {sync_id} failed: {error}")
        send_alert(f"Census sync failed: {error}")

    return "OK", 200
```

## Quick Start

### Complete Audience Activation Workflow

```python
from census_api import CensusAPI

# 1. Initialize Census
census = CensusAPI(api_token="your_census_token")

# 2. Create warehouse source (Snowflake)
source = census.create_source({
    "name": "Snowflake Marketing Data",
    "type": "snowflake",
    "credentials": {
        "account": "your-account.snowflakecomputing.com",
        "database": "MARKETING_DATA",
        "schema": "ANALYTICS",
        "username": "census",
        "password": "password"
    }
})

# 3. Create Facebook destination
facebook_dest = census.create_destination({
    "name": "Facebook Ads",
    "type": "facebook_custom_audiences",
    "credentials": {
        "access_token": "your_access_token"
    }
})

# 4. Create sync from warehouse to Facebook
high_value_sync = census.create_sync({
    "name": "High Value Customers -> Facebook",
    "source_id": source['id'],
    "destination_id": facebook_dest['id'],
    "source_attributes": {
        "type": "query",
        "query": """
            SELECT user_id, email, phone
            FROM customer_360
            WHERE revenue_90d > 1000
        """
    },
    "mappings": [
        {"from": "email", "to": "email"},
        {"from": "phone", "to": "phone"}
    ],
    "operation": "mirror",
    "schedule": {"frequency": "daily", "hour": 2}
})

# 5. Trigger sync
census.trigger_sync(high_value_sync['id'])

print("Census audience sync configured!")

# 6. Monitor status
status = census.get_sync_status(high_value_sync['id'])
print(f"Sync status: {status['last_run']['state']}")
```

## References

- **Official Documentation**: https://docs.getcensus.com/
- **API Reference**: https://docs.getcensus.com/basics/api
- **Destination Catalog**: https://docs.getcensus.com/destinations/overview
- **Audience Hub**: https://docs.getcensus.com/basics/audience-hub
- **Sync Configurations**: https://docs.getcensus.com/basics/core-concept#syncs
- **Field Mappings**: https://docs.getcensus.com/basics/core-concept#field-mappings
- **SQL Best Practices**: https://docs.getcensus.com/sources/overview#sql-best-practices
- **Webhooks**: https://docs.getcensus.com/basics/webhooks
- **Security**: https://docs.getcensus.com/misc/security-and-privacy
- **Support**: https://docs.getcensus.com/misc/contact-support

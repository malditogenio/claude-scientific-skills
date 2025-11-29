---
skill_name: hightouch
display_name: Hightouch
description: Data activation platform for syncing warehouse data to marketing tools with visual audience builder
category: cdp-data
tags: [reverse-etl, data-activation, audience-builder, customer-studio]
complexity: intermediate
dependencies: [hightouch-api, requests]
---

# Hightouch

## Overview

Hightouch is a data activation platform that syncs your data warehouse to business applications. With a focus on marketing use cases, Hightouch enables teams to build audiences, sync customer data, and activate insights without engineering support.

Hightouch excels at:
- **Visual Audience Builder**: No-code audience creation with SQL preview
- **Customer Studio**: Build segments with visual interface
- **200+ Destinations**: Sync to all major marketing and sales tools
- **Real-Time Sync**: Activate data with millisecond latency
- **Match Booster**: Improve match rates for ad platform syncs
- **dbt Integration**: Native support for dbt models as sources
- **Warehouse-First**: Leverage your warehouse as the CDP

## When to Use

Use Hightouch when you need to:
- **Visual Audience Building**: Enable marketers to build segments without SQL
- **Data Activation**: Sync warehouse insights to operational tools
- **Customer Studio**: Create sophisticated segments with visual interface
- **Match Rate Optimization**: Improve ad platform audience matching
- **Real-Time Personalization**: Sync data with low latency
- **dbt-Native Workflows**: Activate dbt models directly
- **Marketing Orchestration**: Coordinate campaigns across multiple platforms

## Core Capabilities

### 1. Visual Audience Builder and Customer Studio

**Building Audiences with Customer Studio**

```python
import requests
import json

class HightouchAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.hightouch.io/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def create_model(self, model_config):
        """Create a data model (audience query)"""

        response = requests.post(
            f"{self.base_url}/models",
            headers=self.headers,
            json=model_config
        )
        return response.json()

    def create_destination(self, destination_config):
        """Create destination connection"""

        response = requests.post(
            f"{self.base_url}/destinations",
            headers=self.headers,
            json=destination_config
        )
        return response.json()

    def create_sync(self, sync_config):
        """Create sync from model to destination"""

        response = requests.post(
            f"{self.base_url}/syncs",
            headers=self.headers,
            json=sync_config
        )
        return response.json()

    def trigger_sync(self, sync_id):
        """Trigger sync run"""

        response = requests.post(
            f"{self.base_url}/syncs/{sync_id}/trigger",
            headers=self.headers
        )
        return response.json()

    def get_sync_runs(self, sync_id):
        """Get sync execution history"""

        response = requests.get(
            f"{self.base_url}/syncs/{sync_id}/runs",
            headers=self.headers
        )
        return response.json()

# Example: Create audience model
hightouch = HightouchAPI(api_key="your_api_key")

# Create high-value customer model
high_value_model = hightouch.create_model({
    "name": "High Value Customers",
    "source_id": "snowflake_source_id",
    "is_schema": False,
    "query_type": "custom_sql",
    "custom_sql": """
        SELECT
            user_id,
            email,
            phone,
            name,
            customer_tier,
            lifetime_revenue,
            revenue_90d,
            last_purchase_date
        FROM marketing_data.customer_360
        WHERE revenue_90d > 1000
            AND customer_tier = 'high_value'
            AND days_since_purchase <= 30
    """,
    "primary_key": "user_id"
})

print(f"Created model: {high_value_model['id']}")
```

**Visual Segment Builder (API Representation)**

```python
def create_visual_segment(hightouch_api, source_id):
    """
    Create segment using visual builder conditions
    (API equivalent of UI-built segments)
    """

    segment_model = hightouch_api.create_model({
        "name": "Cart Abandoners - Last 7 Days",
        "source_id": source_id,
        "is_schema": False,
        "query_type": "visual",
        "visual_config": {
            "parent_model_id": "customer_360_model_id",
            "conditions": [
                {
                    "field": "products_viewed_90d",
                    "operator": "greater_than",
                    "value": 2
                },
                {
                    "field": "cart_adds_7d",
                    "operator": "greater_than_or_equal",
                    "value": 1
                },
                {
                    "field": "total_orders",
                    "operator": "equals",
                    "value": 0
                },
                {
                    "field": "last_cart_add",
                    "operator": "within_last",
                    "value": 7,
                    "unit": "days"
                }
            ],
            "logic": "AND"
        },
        "primary_key": "user_id"
    })

    return segment_model

# Create visual segment
cart_abandoner_segment = create_visual_segment(hightouch, "snowflake_source_id")
```

### 2. Multi-Platform Audience Activation

**Sync to Facebook Custom Audiences**

```python
class HightouchAudienceActivation:
    def __init__(self, api_key):
        self.hightouch = HightouchAPI(api_key)

    def activate_to_facebook(self, model_id, facebook_config):
        """Activate audience to Facebook Custom Audiences"""

        # Create Facebook destination if needed
        facebook_dest = self.hightouch.create_destination({
            "name": "Facebook Ads",
            "type": "facebook_custom_audiences",
            "configuration": {
                "access_token": facebook_config['access_token'],
                "ad_account_id": facebook_config['ad_account_id']
            }
        })

        # Create sync configuration
        sync = self.hightouch.create_sync({
            "model_id": model_id,
            "destination_id": facebook_dest['id'],
            "configuration": {
                "mode": "upsert",
                "audience_id": facebook_config.get('custom_audience_id'),
                "create_new_audience": not facebook_config.get('custom_audience_id'),
                "audience_name": facebook_config.get('audience_name', 'Warehouse Audience'),
                "match_keys": ["email", "phone"]
            },
            "mappings": [
                {
                    "model_column": "email",
                    "destination_field": "email"
                },
                {
                    "model_column": "phone",
                    "destination_field": "phone"
                },
                {
                    "model_column": "user_id",
                    "destination_field": "extern_id"
                }
            ],
            "schedule": {
                "type": "interval",
                "interval": "6h"
            }
        })

        # Trigger initial sync
        self.hightouch.trigger_sync(sync['id'])

        return sync

    def activate_to_google_ads(self, model_id, google_config):
        """Activate audience to Google Ads Customer Match"""

        # Create Google Ads destination
        google_dest = self.hightouch.create_destination({
            "name": "Google Ads",
            "type": "google_ads",
            "configuration": {
                "customer_id": google_config['customer_id'],
                "developer_token": google_config['developer_token'],
                "refresh_token": google_config['refresh_token']
            }
        })

        # Create sync with Match Booster enabled
        sync = self.hightouch.create_sync({
            "model_id": model_id,
            "destination_id": google_dest['id'],
            "configuration": {
                "mode": "mirror",
                "user_list_id": google_config.get('user_list_id'),
                "create_new_list": not google_config.get('user_list_id'),
                "list_name": google_config.get('list_name', 'Warehouse Audience'),
                "membership_duration_days": 540,
                "enable_match_booster": True  # Hightouch's match rate optimization
            },
            "mappings": [
                {"model_column": "email", "destination_field": "email"},
                {"model_column": "phone", "destination_field": "phone"},
                {"model_column": "first_name", "destination_field": "first_name"},
                {"model_column": "last_name", "destination_field": "last_name"},
                {"model_column": "country", "destination_field": "country"},
                {"model_column": "zip_code", "destination_field": "zip_code"}
            ],
            "schedule": {
                "type": "interval",
                "interval": "4h"
            }
        })

        self.hightouch.trigger_sync(sync['id'])

        return sync

# Example: Activate high-value customers to multiple platforms
activator = HightouchAudienceActivation(api_key="your_key")

# Activate to Facebook
fb_sync = activator.activate_to_facebook(
    model_id="high_value_model_id",
    facebook_config={
        'access_token': 'fb_token',
        'ad_account_id': 'act_123456',
        'audience_name': 'High Value Customers - Warehouse'
    }
)

# Activate to Google Ads
google_sync = activator.activate_to_google_ads(
    model_id="high_value_model_id",
    google_config={
        'customer_id': '1234567890',
        'developer_token': 'dev_token',
        'refresh_token': 'refresh_token',
        'list_name': 'High Value Customers - Warehouse'
    }
)

print(f"Created Facebook sync: {fb_sync['id']}")
print(f"Created Google Ads sync: {google_sync['id']}")
```

### 3. Marketing Automation and Personalization

**Sync to Braze for Personalization**

```python
def sync_to_braze(hightouch_api, model_id, braze_config):
    """Sync customer attributes to Braze for personalization"""

    # Create Braze destination
    braze_dest = hightouch_api.create_destination({
        "name": "Braze",
        "type": "braze",
        "configuration": {
            "api_url": braze_config['api_url'],
            "api_key": braze_config['api_key']
        }
    })

    # Create sync with rich customer attributes
    sync = hightouch_api.create_sync({
        "model_id": model_id,
        "destination_id": braze_dest['id'],
        "configuration": {
            "mode": "upsert",
            "object": "user"
        },
        "mappings": [
            {"model_column": "user_id", "destination_field": "external_id"},
            {"model_column": "email", "destination_field": "email"},
            {"model_column": "customer_tier", "destination_field": "customer_tier"},
            {"model_column": "lifetime_revenue", "destination_field": "lifetime_value"},
            {"model_column": "revenue_90d", "destination_field": "revenue_90d"},
            {"model_column": "predicted_ltv", "destination_field": "predicted_ltv"},
            {"model_column": "churn_risk_score", "destination_field": "churn_risk"},
            {"model_column": "favorite_category", "destination_field": "favorite_category"},
            {"model_column": "last_purchase_date", "destination_field": "last_purchase_date"}
        ],
        "schedule": {
            "type": "interval",
            "interval": "1h"  # Real-time updates
        }
    })

    return sync

# Sync enriched customer data to Braze
customer_enrichment_query = """
SELECT
    user_id,
    email,
    customer_tier,
    lifetime_revenue,
    revenue_90d,
    predicted_ltv,
    churn_risk_score,
    favorite_category,
    last_purchase_date,
    recommended_products
FROM marketing_data.customer_360_enriched
"""

enrichment_model = hightouch.create_model({
    "name": "Customer Enrichment for Braze",
    "source_id": "snowflake_source_id",
    "query_type": "custom_sql",
    "custom_sql": customer_enrichment_query,
    "primary_key": "user_id"
})

braze_sync = sync_to_braze(
    hightouch,
    enrichment_model['id'],
    {
        'api_url': 'https://rest.iad-01.braze.com',
        'api_key': 'your_braze_api_key'
    }
)
```

**Sync Lead Scores to Salesforce**

```python
def sync_lead_scores_to_salesforce(hightouch_api, model_id):
    """Sync ML-predicted lead scores to Salesforce"""

    # Create Salesforce destination
    salesforce_dest = hightouch_api.create_destination({
        "name": "Salesforce",
        "type": "salesforce",
        "configuration": {
            "username": "salesforce_user@company.com",
            "password": "password",
            "security_token": "security_token",
            "is_sandbox": False
        }
    })

    # Sync lead scoring model results
    sync = hightouch_api.create_sync({
        "model_id": model_id,
        "destination_id": salesforce_dest['id'],
        "configuration": {
            "mode": "upsert",
            "object": "Lead",
            "matching_key": "Email"
        },
        "mappings": [
            {"model_column": "email", "destination_field": "Email"},
            {"model_column": "predicted_ltv", "destination_field": "Predicted_LTV__c"},
            {"model_column": "lead_score", "destination_field": "Lead_Score__c"},
            {"model_column": "conversion_probability", "destination_field": "Conversion_Probability__c"},
            {"model_column": "recommended_action", "destination_field": "Recommended_Action__c"}
        ],
        "schedule": {
            "type": "interval",
            "interval": "2h"
        }
    })

    return sync

# Create lead scoring model
lead_scoring_model = hightouch.create_model({
    "name": "ML Lead Scores",
    "source_id": "snowflake_source_id",
    "query_type": "dbt",  # Use dbt model
    "dbt_model_name": "lead_scoring_predictions",
    "primary_key": "email"
})

sf_sync = sync_lead_scores_to_salesforce(hightouch, lead_scoring_model['id'])
```

### 4. dbt Integration and Real-Time Syncs

**Using dbt Models as Sources**

```python
def create_dbt_powered_sync(hightouch_api, dbt_config):
    """
    Create sync using dbt model as source
    """

    # Create model pointing to dbt model
    dbt_model = hightouch_api.create_model({
        "name": "Customer Segments - dbt",
        "source_id": dbt_config['source_id'],
        "is_schema": False,
        "query_type": "dbt",
        "dbt_model_name": dbt_config['model_name'],  # e.g., "customer_segments"
        "primary_key": "user_id"
    })

    # Create syncs for dbt model
    syncs = []

    for destination in dbt_config['destinations']:
        sync = hightouch_api.create_sync({
            "model_id": dbt_model['id'],
            "destination_id": destination['destination_id'],
            "configuration": destination['config'],
            "mappings": destination['mappings'],
            "schedule": destination.get('schedule', {
                "type": "dbt_cloud",  # Trigger after dbt Cloud run
                "dbt_cloud_job_id": dbt_config['dbt_cloud_job_id']
            })
        })
        syncs.append(sync)

    return dbt_model, syncs

# Example: Sync dbt customer segments model
dbt_config = {
    'source_id': 'snowflake_source_id',
    'model_name': 'customer_segments',  # dbt model name
    'dbt_cloud_job_id': '12345',  # dbt Cloud job ID
    'destinations': [
        {
            'destination_id': 'facebook_dest_id',
            'config': {'mode': 'mirror'},
            'mappings': [
                {'model_column': 'email', 'destination_field': 'email'}
            ]
        },
        {
            'destination_id': 'google_ads_dest_id',
            'config': {'mode': 'mirror'},
            'mappings': [
                {'model_column': 'email', 'destination_field': 'email'}
            ]
        }
    ]
}

dbt_model, syncs = create_dbt_powered_sync(hightouch, dbt_config)
print(f"Created dbt model and {len(syncs)} syncs")
```

**Real-Time Event Streaming**

```python
def setup_realtime_sync(hightouch_api, model_id, destination_id):
    """
    Set up real-time sync using change data capture
    """

    sync = hightouch_api.create_sync({
        "model_id": model_id,
        "destination_id": destination_id,
        "configuration": {
            "mode": "upsert",
            "sync_mode": "live"  # Real-time CDC
        },
        "mappings": [
            {"model_column": "user_id", "destination_field": "user_id"},
            {"model_column": "event_name", "destination_field": "event"},
            {"model_column": "event_properties", "destination_field": "properties"},
            {"model_column": "timestamp", "destination_field": "timestamp"}
        ],
        "schedule": {
            "type": "real_time"  # Continuous sync
        }
    })

    return sync

# Real-time event streaming to analytics tools
realtime_events_model = hightouch.create_model({
    "name": "Real-Time Product Events",
    "source_id": "snowflake_source_id",
    "query_type": "custom_sql",
    "custom_sql": """
        SELECT
            user_id,
            event_name,
            event_properties,
            timestamp
        FROM marketing_data.events_stream
        WHERE event_name IN ('product_viewed', 'add_to_cart', 'checkout_started')
    """,
    "primary_key": "user_id"
})

realtime_sync = setup_realtime_sync(
    hightouch,
    realtime_events_model['id'],
    "segment_dest_id"
)
```

## Installation and Authentication

### Hightouch API Setup

```python
import requests

class HightouchClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.hightouch.io/api/v1"

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def list_sources(self):
        """List all configured sources"""
        response = requests.get(
            f"{self.base_url}/sources",
            headers=self.get_headers()
        )
        return response.json()

    def list_models(self):
        """List all models"""
        response = requests.get(
            f"{self.base_url}/models",
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
hightouch = HightouchClient(api_key="your_hightouch_api_key")

# List resources
sources = hightouch.list_sources()
print(f"Sources: {len(sources['data'])}")

models = hightouch.list_models()
print(f"Models: {len(models['data'])}")
```

### Webhook Configuration

```python
from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

@app.route('/hightouch-webhook', methods=['POST'])
def hightouch_webhook():
    """
    Handle Hightouch sync webhooks
    """

    # Verify webhook signature
    signature = request.headers.get('X-Hightouch-Signature')
    webhook_secret = "your_webhook_secret"

    # Validate signature
    expected_signature = hmac.new(
        webhook_secret.encode(),
        request.get_data(),
        hashlib.sha256
    ).hexdigest()

    if signature != expected_signature:
        return "Invalid signature", 401

    # Process webhook
    data = request.json

    if data['type'] == 'sync.completed':
        sync_id = data['sync_id']
        records_synced = data['records_processed']
        success = data['success']

        if success:
            print(f"Sync {sync_id} completed: {records_synced} records")
            # Trigger next steps
        else:
            print(f"Sync {sync_id} failed: {data['error']}")
            send_alert(f"Hightouch sync failed: {data['error']}")

    return "OK", 200
```

## Quick Start

### Complete Audience Activation Workflow

```python
from hightouch_api import HightouchAPI

# 1. Initialize Hightouch
hightouch = HightouchAPI(api_key="your_api_key")

# 2. Create warehouse source (Snowflake)
source = hightouch.create_source({
    "name": "Snowflake Marketing Warehouse",
    "type": "snowflake",
    "configuration": {
        "account": "your-account.snowflakecomputing.com",
        "database": "MARKETING_DATA",
        "schema": "ANALYTICS",
        "warehouse": "COMPUTE_WH",
        "username": "hightouch",
        "password": "password"
    }
})

# 3. Create audience model
model = hightouch.create_model({
    "name": "High-Value Customers",
    "source_id": source['id'],
    "query_type": "custom_sql",
    "custom_sql": """
        SELECT
            user_id,
            email,
            phone,
            customer_tier,
            lifetime_revenue
        FROM customer_360
        WHERE revenue_90d > 1000
    """,
    "primary_key": "user_id"
})

# 4. Create Facebook destination
facebook_dest = hightouch.create_destination({
    "name": "Facebook Ads",
    "type": "facebook_custom_audiences",
    "configuration": {
        "access_token": "your_fb_token"
    }
})

# 5. Create sync
sync = hightouch.create_sync({
    "model_id": model['id'],
    "destination_id": facebook_dest['id'],
    "configuration": {
        "mode": "mirror",
        "create_new_audience": True,
        "audience_name": "High-Value Customers",
        "enable_match_booster": True
    },
    "mappings": [
        {"model_column": "email", "destination_field": "email"},
        {"model_column": "phone", "destination_field": "phone"}
    ],
    "schedule": {
        "type": "interval",
        "interval": "6h"
    }
})

# 6. Trigger sync
hightouch.trigger_sync(sync['id'])

print("Hightouch audience activation complete!")

# 7. Monitor sync
runs = hightouch.get_sync_runs(sync['id'])
latest_run = runs['data'][0]
print(f"Latest run: {latest_run['status']} - {latest_run['rows_processed']} rows")
```

## References

- **Official Documentation**: https://hightouch.io/docs
- **API Reference**: https://hightouch.io/docs/api-reference
- **Customer Studio**: https://hightouch.io/docs/audiences/schema
- **Destination Catalog**: https://hightouch.io/docs/destinations/overview
- **dbt Integration**: https://hightouch.io/docs/models/dbt
- **Match Booster**: https://hightouch.io/docs/destinations/match-booster
- **Visual Audience Builder**: https://hightouch.io/docs/audiences/visual-segmentation
- **Real-Time Sync**: https://hightouch.io/docs/syncs/live-syncs
- **Security & Privacy**: https://hightouch.io/docs/security/overview
- **Best Practices**: https://hightouch.io/docs/best-practices

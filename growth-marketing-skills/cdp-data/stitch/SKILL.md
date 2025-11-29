---
skill_name: stitch
display_name: Stitch Data
description: Simple, extensible ETL platform for replicating marketing data to warehouses
category: cdp-data
tags: [etl, data-pipeline, singer, replication]
complexity: beginner
dependencies: [stitch-client, singer-python]
---

# Stitch Data

## Overview

Stitch Data is a cloud-based ETL platform (acquired by Talend) that replicates data from SaaS applications, databases, and webhooks into data warehouses. Built on the open-source Singer framework, Stitch provides simple, reliable data pipelines for marketing teams.

Stitch excels at:
- **Simple Setup**: Configure connectors in minutes without coding
- **Singer Protocol**: Extensible with open-source Singer taps
- **Automated Replication**: Set-and-forget data pipelines
- **Incremental Updates**: Efficient syncing of only new/changed data
- **Marketing Platform Support**: 130+ pre-built integrations
- **Transparent Pricing**: Row-based pricing model

## When to Use

Use Stitch when you need to:
- **Quick Setup**: Get data flowing to your warehouse fast
- **Standard Connectors**: Use common marketing platforms (Google Ads, Facebook, HubSpot)
- **Simple Data Pipelines**: Basic replication without complex transformations
- **Singer Ecosystem**: Leverage open-source Singer taps
- **Predictable Costs**: Row-based pricing for budget planning
- **Managed Service**: Avoid infrastructure management
- **Webhook Data**: Capture webhook events from marketing tools

## Core Capabilities

### 1. Marketing Platform Integrations

**Available Marketing Integrations**

```python
# Stitch supports 130+ data sources including:

marketing_integrations = {
    # Advertising
    'google_ads': 'Google Ads campaigns and performance',
    'facebook_ads': 'Facebook Ads insights',
    'linkedin_ads': 'LinkedIn Campaign Manager',
    'bing_ads': 'Microsoft Advertising',
    'adroll': 'AdRoll retargeting platform',

    # Analytics
    'google_analytics': 'Google Analytics reporting',
    'mixpanel': 'Product analytics events',
    'heap': 'Heap analytics',
    'pendo': 'Product analytics',

    # Marketing Automation
    'hubspot': 'CRM and marketing automation',
    'marketo': 'Marketing automation',
    'mailchimp': 'Email marketing',
    'sendgrid': 'Email delivery',
    'iterable': 'Cross-channel marketing',
    'braze': 'Customer engagement platform',

    # CRM & Sales
    'salesforce': 'Sales CRM',
    'zendesk': 'Customer support',
    'intercom': 'Customer messaging',
    'pipedrive': 'Sales CRM',

    # eCommerce
    'shopify': 'eCommerce platform',
    'stripe': 'Payment processing',
    'chargebee': 'Subscription billing',

    # Social Media
    'instagram_business': 'Instagram insights',
    'twitter_ads': 'Twitter advertising',

    # Custom Sources
    'webhook': 'Receive webhook data',
    'http': 'Pull data from any API'
}
```

**Setting Up Integrations (API)**

```python
import requests
import json

class StitchAPI:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.stitchdata.com/v4"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    def list_sources(self):
        """List all configured sources"""
        response = requests.get(
            f"{self.base_url}/sources",
            headers=self.headers
        )
        return response.json()

    def create_source(self, source_type, display_name, properties):
        """Create a new data source"""

        payload = {
            "type": source_type,
            "display_name": display_name,
            "properties": properties
        }

        response = requests.post(
            f"{self.base_url}/sources",
            headers=self.headers,
            json=payload
        )
        return response.json()

    def update_source(self, source_id, properties):
        """Update source configuration"""

        payload = {"properties": properties}

        response = requests.put(
            f"{self.base_url}/sources/{source_id}",
            headers=self.headers,
            json=payload
        )
        return response.json()

    def start_replication(self, source_id):
        """Trigger a replication job"""

        response = requests.post(
            f"{self.base_url}/sources/{source_id}/sync",
            headers=self.headers
        )
        return response.json()

    def get_source_status(self, source_id):
        """Get source replication status"""

        response = requests.get(
            f"{self.base_url}/sources/{source_id}",
            headers=self.headers
        )
        return response.json()

# Example: Set up Google Ads integration
stitch = StitchAPI(api_token="your_api_token")

# Create Google Ads source
google_ads_source = stitch.create_source(
    source_type="platform.google-adwords",
    display_name="Google Ads - Production",
    properties={
        "customer_ids": "1234567890,0987654321",
        "start_date": "2024-01-01T00:00:00Z",
        "oauth_credentials": {
            "developer_token": "your_developer_token",
            "oauth_client_id": "your_client_id",
            "oauth_client_secret": "your_client_secret",
            "refresh_token": "your_refresh_token"
        }
    }
)

print(f"Created source: {google_ads_source}")

# Start replication
stitch.start_replication(google_ads_source["id"])
```

### 2. Data Replication and Syncing

**Configure Replication Schedules**

```python
class StitchReplicationManager:
    def __init__(self, api_token):
        self.stitch = StitchAPI(api_token)

    def setup_marketing_stack(self, destination_config):
        """
        Set up complete marketing data replication stack

        destination_config: {
            'type': 'snowflake',  # or 'bigquery', 'redshift'
            'credentials': {...}
        }
        """

        # Define sources to replicate
        sources_to_create = [
            {
                'type': 'platform.google-adwords',
                'name': 'Google Ads',
                'properties': {
                    'customer_ids': '1234567890',
                    'start_date': '2024-01-01T00:00:00Z'
                }
            },
            {
                'type': 'platform.facebook',
                'name': 'Facebook Ads',
                'properties': {
                    'account_id': 'act_123456',
                    'start_date': '2024-01-01'
                }
            },
            {
                'type': 'platform.hubspot',
                'name': 'HubSpot',
                'properties': {
                    'start_date': '2024-01-01T00:00:00Z'
                }
            },
            {
                'type': 'platform.salesforce',
                'name': 'Salesforce',
                'properties': {
                    'start_date': '2024-01-01T00:00:00Z',
                    'is_sandbox': False
                }
            }
        ]

        created_sources = []

        for source_config in sources_to_create:
            try:
                source = self.stitch.create_source(
                    source_type=source_config['type'],
                    display_name=source_config['name'],
                    properties=source_config['properties']
                )
                created_sources.append(source)
                print(f"Created {source_config['name']}")

                # Configure replication schedule (every 6 hours)
                self.configure_schedule(source['id'], frequency_minutes=360)

            except Exception as e:
                print(f"Error creating {source_config['name']}: {e}")

        return created_sources

    def configure_schedule(self, source_id, frequency_minutes=360):
        """Configure replication schedule"""

        schedule_config = {
            "frequency_in_minutes": frequency_minutes,
            "anchor_time": "2024-01-01T00:00:00Z"
        }

        return self.stitch.update_source(source_id, {
            "frequency_in_minutes": frequency_minutes
        })

    def monitor_replications(self, source_ids):
        """Monitor replication jobs"""

        status_report = []

        for source_id in source_ids:
            status = self.stitch.get_source_status(source_id)

            last_sync = status.get('last_run', {})

            status_report.append({
                'source_id': source_id,
                'name': status['display_name'],
                'type': status['type'],
                'status': last_sync.get('status'),
                'started_at': last_sync.get('started_at'),
                'completed_at': last_sync.get('completed_at'),
                'rows_loaded': last_sync.get('rows_loaded', 0)
            })

        return status_report

# Example usage
manager = StitchReplicationManager(api_token="your_token")

# Set up marketing stack
created_sources = manager.setup_marketing_stack({
    'type': 'snowflake',
    'credentials': {}
})

# Monitor syncs
source_ids = [s['id'] for s in created_sources]
sync_status = manager.monitor_replications(source_ids)

for status in sync_status:
    print(f"{status['name']}: {status['status']} - {status['rows_loaded']} rows")
```

### 3. Custom Data Sources with Singer

**Build Custom Singer Tap**

```python
# Stitch is built on Singer - you can create custom taps
# Example: Custom marketing platform tap

import singer
import requests
from singer import utils, metadata
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema

REQUIRED_CONFIG_KEYS = ["api_key", "start_date"]

class CustomMarketingTap:
    def __init__(self, config, state):
        self.config = config
        self.state = state
        self.api_key = config['api_key']
        self.base_url = "https://api.customplatform.com/v1"

    def get_campaigns(self, start_date):
        """Get campaign data"""
        response = requests.get(
            f"{self.base_url}/campaigns",
            headers={"Authorization": f"Bearer {self.api_key}"},
            params={"start_date": start_date}
        )
        return response.json()

    def get_ad_performance(self, campaign_id, start_date):
        """Get ad performance data"""
        response = requests.get(
            f"{self.base_url}/campaigns/{campaign_id}/performance",
            headers={"Authorization": f"Bearer {self.api_key}"},
            params={"start_date": start_date}
        )
        return response.json()

def discover():
    """Discover available streams and their schemas"""

    # Define campaign schema
    campaign_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "status": {"type": "string"},
            "budget": {"type": "number"},
            "created_at": {"type": "string", "format": "date-time"}
        }
    }

    # Define performance schema
    performance_schema = {
        "type": "object",
        "properties": {
            "campaign_id": {"type": "string"},
            "date": {"type": "string", "format": "date"},
            "impressions": {"type": "integer"},
            "clicks": {"type": "integer"},
            "spend": {"type": "number"},
            "conversions": {"type": "integer"},
            "revenue": {"type": "number"}
        }
    }

    # Create catalog
    streams = []

    campaigns_entry = CatalogEntry(
        tap_stream_id="campaigns",
        stream="campaigns",
        schema=Schema.from_dict(campaign_schema),
        key_properties=["id"],
        metadata=metadata.to_map(metadata.get_standard_metadata(
            schema=campaign_schema,
            key_properties=["id"],
            replication_method="INCREMENTAL",
            valid_replication_keys=["created_at"]
        ))
    )
    streams.append(campaigns_entry)

    performance_entry = CatalogEntry(
        tap_stream_id="ad_performance",
        stream="ad_performance",
        schema=Schema.from_dict(performance_schema),
        key_properties=["campaign_id", "date"],
        metadata=metadata.to_map(metadata.get_standard_metadata(
            schema=performance_schema,
            key_properties=["campaign_id", "date"],
            replication_method="INCREMENTAL",
            valid_replication_keys=["date"]
        ))
    )
    streams.append(performance_entry)

    return Catalog(streams)

def sync(config, state, catalog):
    """Sync data from custom platform"""

    tap = CustomMarketingTap(config, state)

    for stream in catalog.get_selected_streams(state):
        singer.write_schema(
            stream_name=stream.tap_stream_id,
            schema=stream.schema.to_dict(),
            key_properties=stream.key_properties
        )

        if stream.tap_stream_id == "campaigns":
            campaigns = tap.get_campaigns(config['start_date'])
            for campaign in campaigns:
                singer.write_record(
                    stream_name="campaigns",
                    record=campaign
                )

        elif stream.tap_stream_id == "ad_performance":
            campaigns = tap.get_campaigns(config['start_date'])
            for campaign in campaigns:
                performance_data = tap.get_ad_performance(
                    campaign['id'],
                    config['start_date']
                )
                for record in performance_data:
                    singer.write_record(
                        stream_name="ad_performance",
                        record=record
                    )

    return state

# Entry point for Singer tap
@utils.handle_top_exception(logger)
def main():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    catalog = discover() if args.discover else Catalog.from_dict(args.properties)

    if args.discover:
        catalog.dump()
    else:
        sync(args.config, args.state, catalog)
```

### 4. Querying Replicated Data

**Marketing Analytics Queries**

```sql
-- Stitch replicates data to tables in your warehouse
-- Naming convention: stitch.{integration_name}_{table_name}

-- Google Ads performance
SELECT
    date,
    campaign_name,
    campaign_id,
    impressions,
    clicks,
    cost_micros / 1000000 as cost,
    conversions,
    conversions_value
FROM stitch.google_ads_campaign_performance_report
WHERE date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY cost DESC;

-- Facebook Ads insights
SELECT
    date_start as date,
    campaign_name,
    adset_name,
    ad_name,
    impressions,
    clicks,
    spend,
    actions_offsite_conversion_fb_pixel_purchase as purchases,
    action_values_offsite_conversion_fb_pixel_purchase as revenue
FROM stitch.facebook_ads_ads_insights
WHERE date_start >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY spend DESC;

-- HubSpot email performance
SELECT
    c.name as campaign_name,
    COUNT(DISTINCT e.id) as emails_sent,
    COUNT(DISTINCT CASE WHEN e.type = 'OPEN' THEN e.id END) as opens,
    COUNT(DISTINCT CASE WHEN e.type = 'CLICK' THEN e.id END) as clicks,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN e.type = 'OPEN' THEN e.id END) /
        NULLIF(COUNT(DISTINCT e.id), 0), 2) as open_rate,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN e.type = 'CLICK' THEN e.id END) /
        NULLIF(COUNT(DISTINCT e.id), 0), 2) as click_rate
FROM stitch.hubspot_email_events e
JOIN stitch.hubspot_email_campaigns c ON e.campaign_id = c.id
WHERE e.created >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY c.name;

-- Cross-platform campaign performance
WITH all_platforms AS (
    SELECT
        date,
        'google_ads' as platform,
        campaign_name,
        cost_micros / 1000000 as spend,
        impressions,
        clicks,
        conversions as purchases,
        conversions_value as revenue
    FROM stitch.google_ads_campaign_performance_report

    UNION ALL

    SELECT
        date_start as date,
        'facebook_ads' as platform,
        campaign_name,
        spend,
        impressions,
        clicks,
        actions_offsite_conversion_fb_pixel_purchase as purchases,
        action_values_offsite_conversion_fb_pixel_purchase as revenue
    FROM stitch.facebook_ads_ads_insights
)
SELECT
    platform,
    campaign_name,
    SUM(spend) as total_spend,
    SUM(impressions) as total_impressions,
    SUM(clicks) as total_clicks,
    SUM(purchases) as total_purchases,
    SUM(revenue) as total_revenue,
    ROUND(SUM(spend) / NULLIF(SUM(clicks), 0), 2) as avg_cpc,
    ROUND(SUM(revenue) / NULLIF(SUM(spend), 0), 2) as roas
FROM all_platforms
WHERE date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY platform, campaign_name
ORDER BY total_spend DESC;
```

**Python: Analyze Replicated Data**

```python
import pandas as pd
from sqlalchemy import create_engine

def analyze_marketing_roi(warehouse_conn):
    """Analyze marketing ROI across all platforms"""

    query = """
    WITH platform_performance AS (
        SELECT
            date,
            'google_ads' as platform,
            campaign_name,
            cost_micros / 1000000 as spend,
            conversions_value as revenue
        FROM stitch.google_ads_campaign_performance_report
        WHERE date >= CURRENT_DATE - INTERVAL '30 days'

        UNION ALL

        SELECT
            date_start as date,
            'facebook_ads' as platform,
            campaign_name,
            spend,
            action_values_offsite_conversion_fb_pixel_purchase as revenue
        FROM stitch.facebook_ads_ads_insights
        WHERE date_start >= CURRENT_DATE - INTERVAL '30 days'
    )
    SELECT
        platform,
        SUM(spend) as total_spend,
        SUM(revenue) as total_revenue,
        SUM(revenue) - SUM(spend) as profit,
        ROUND(100.0 * (SUM(revenue) - SUM(spend)) / NULLIF(SUM(spend), 0), 2) as roi_percent
    FROM platform_performance
    GROUP BY platform
    ORDER BY roi_percent DESC
    """

    df = pd.read_sql(query, warehouse_conn)

    print("\nMarketing ROI by Platform:")
    print(df)

    return df

# Usage
engine = create_engine('your_warehouse_connection_string')
roi_df = analyze_marketing_roi(engine)
```

## Installation and Authentication

### Stitch API Setup

```python
# Stitch uses API tokens for authentication
# Get your API token from: https://app.stitchdata.com/account/api-keys

import requests

class StitchClient:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.stitchdata.com/v4"

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

# Initialize
stitch = StitchClient(api_token="your_stitch_api_token")
```

### Singer Tap Development

```bash
# Install Singer SDK
pip install singer-python

# Create custom tap
pip install tap-custom-platform

# Run tap
tap-custom-platform --config config.json --catalog catalog.json
```

## Quick Start

### Complete Setup Example

```python
from stitch_api import StitchAPI

# 1. Initialize Stitch
stitch = StitchAPI(api_token="your_api_token")

# 2. List existing sources
sources = stitch.list_sources()
print(f"Existing sources: {len(sources)}")

# 3. Create Google Ads source
google_ads = stitch.create_source(
    source_type="platform.google-adwords",
    display_name="Google Ads Production",
    properties={
        "customer_ids": "1234567890",
        "start_date": "2024-01-01T00:00:00Z"
    }
)

# 4. Create Facebook Ads source
facebook_ads = stitch.create_source(
    source_type="platform.facebook",
    display_name="Facebook Ads",
    properties={
        "account_id": "act_123456",
        "start_date": "2024-01-01"
    }
)

# 5. Start replication
stitch.start_replication(google_ads['id'])
stitch.start_replication(facebook_ads['id'])

print("Stitch replication started!")

# 6. Monitor status
status = stitch.get_source_status(google_ads['id'])
print(f"Google Ads status: {status['last_run']['status']}")
```

## References

- **Official Documentation**: https://www.stitchdata.com/docs/
- **API Reference**: https://www.stitchdata.com/docs/developers/stitch-connect/api
- **Integration Catalog**: https://www.stitchdata.com/integrations/
- **Singer Protocol**: https://github.com/singer-io/getting-started
- **Singer Taps**: https://www.singer.io/#taps
- **Pricing**: https://www.stitchdata.com/pricing/
- **Replication Methods**: https://www.stitchdata.com/docs/replication/replication-methods/
- **Best Practices**: https://www.stitchdata.com/docs/replication/replication-best-practices
- **Support**: https://www.stitchdata.com/contact/support/
- **Status Page**: https://status.stitchdata.com/

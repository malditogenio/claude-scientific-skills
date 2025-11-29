---
skill_name: airbyte
display_name: Airbyte
description: Open-source data integration platform for syncing marketing data with full customization and control
category: cdp-data
tags: [etl, open-source, data-integration, connectors, self-hosted]
complexity: intermediate
dependencies: [airbyte-api, requests]
---

# Airbyte

## Overview

Airbyte is an open-source data integration platform that syncs data from applications, APIs, and databases to data warehouses, lakes, and databases. Unlike proprietary ETL tools, Airbyte gives you full control over your data pipelines with the option to self-host or use Airbyte Cloud.

Airbyte excels at:
- **Open Source**: Full transparency and control over data pipelines
- **Custom Connectors**: Build your own connectors in any language
- **Self-Hosted Option**: Deploy on your infrastructure for data sovereignty
- **300+ Connectors**: Pre-built connectors for marketing platforms
- **Standardized Protocol**: Consistent interface across all connectors
- **Cost-Effective**: Free to use with pay-as-you-go cloud option

## When to Use

Use Airbyte when you need to:
- **Full Data Control**: Self-host your data pipelines for compliance/security
- **Custom Data Sources**: Build connectors for proprietary marketing platforms
- **Cost Optimization**: Reduce ETL costs with open-source infrastructure
- **Flexible Deployment**: Deploy on AWS, GCP, Azure, or Kubernetes
- **API-First Integration**: Sync data from any REST API
- **Data Sovereignty**: Keep data in specific regions/clouds
- **Custom Transformations**: Apply transformations using dbt integration

## Core Capabilities

### 1. Marketing Platform Connections

**Available Marketing Connectors**

```python
# Airbyte supports 300+ connectors including:

marketing_connectors = {
    # Advertising Platforms
    'google-ads': 'Google Ads campaigns, ads, performance',
    'facebook-marketing': 'Facebook Ads insights and campaigns',
    'linkedin-ads': 'LinkedIn Campaign Manager',
    'tiktok-marketing': 'TikTok Ads data',
    'snapchat-marketing': 'Snapchat Ads',
    'pinterest': 'Pinterest Ads',
    'microsoft-advertising': 'Bing Ads (Microsoft Advertising)',

    # Analytics
    'google-analytics-v4': 'Google Analytics 4 data',
    'mixpanel': 'Product analytics events',
    'amplitude': 'Behavioral analytics',
    'heap-analytics': 'Heap product analytics',

    # Marketing Automation
    'hubspot': 'CRM, marketing, and sales data',
    'marketo': 'Marketing automation platform',
    'mailchimp': 'Email marketing campaigns',
    'sendgrid': 'Email delivery data',
    'klaviyo': 'Email and SMS marketing',

    # CRM
    'salesforce': 'Sales CRM data',
    'zendesk-support': 'Customer support tickets',
    'intercom': 'Customer messaging platform',

    # eCommerce
    'shopify': 'eCommerce store data',
    'stripe': 'Payment processing data',
    'woocommerce': 'WordPress eCommerce',

    # Social Media
    'instagram': 'Instagram Business data',
    'youtube-analytics': 'YouTube channel analytics',
    'twitter': 'Twitter analytics'
}
```

**Setting Up Connections (API)**

```python
import requests
import json

class AirbyteAPI:
    def __init__(self, host="localhost", port=8000):
        self.base_url = f"http://{host}:{port}/api/v1"
        # For Airbyte Cloud
        # self.base_url = "https://api.airbyte.com/v1"
        # Add authentication header for cloud

    def create_source(self, workspace_id, source_config):
        """Create a new source connection"""

        url = f"{self.base_url}/sources/create"

        payload = {
            "workspaceId": workspace_id,
            "sourceDefinitionId": source_config["definition_id"],
            "connectionConfiguration": source_config["config"],
            "name": source_config["name"]
        }

        response = requests.post(url, json=payload)
        return response.json()

    def create_destination(self, workspace_id, destination_config):
        """Create a destination (warehouse)"""

        url = f"{self.base_url}/destinations/create"

        payload = {
            "workspaceId": workspace_id,
            "destinationDefinitionId": destination_config["definition_id"],
            "connectionConfiguration": destination_config["config"],
            "name": destination_config["name"]
        }

        response = requests.post(url, json=payload)
        return response.json()

    def create_connection(self, source_id, destination_id, config):
        """Create connection between source and destination"""

        url = f"{self.base_url}/connections/create"

        payload = {
            "sourceId": source_id,
            "destinationId": destination_id,
            "name": config["name"],
            "namespaceDefinition": "customformat",
            "namespaceFormat": config.get("schema", "airbyte"),
            "scheduleType": config.get("schedule_type", "manual"),
            "scheduleData": config.get("schedule_data"),
            "syncCatalog": config.get("sync_catalog")
        }

        response = requests.post(url, json=payload)
        return response.json()

    def trigger_sync(self, connection_id):
        """Manually trigger a connection sync"""

        url = f"{self.base_url}/connections/sync"

        payload = {"connectionId": connection_id}

        response = requests.post(url, json=payload)
        return response.json()

    def get_connection_status(self, connection_id):
        """Get sync status for a connection"""

        url = f"{self.base_url}/connections/get"

        payload = {"connectionId": connection_id}

        response = requests.post(url, json=payload)
        return response.json()

# Example: Set up Google Ads source
airbyte = AirbyteAPI(host="localhost", port=8000)

workspace_id = "your-workspace-id"

# Create Google Ads source
google_ads_source = airbyte.create_source(
    workspace_id=workspace_id,
    source_config={
        "name": "Google Ads Production",
        "definition_id": "google-ads-source-definition-id",
        "config": {
            "credentials": {
                "developer_token": "your-developer-token",
                "client_id": "your-client-id",
                "client_secret": "your-client-secret",
                "refresh_token": "your-refresh-token"
            },
            "customer_id": "1234567890",
            "start_date": "2024-01-01"
        }
    }
)

print(f"Created source: {google_ads_source['sourceId']}")
```

### 2. Custom Connector Development

**Build Custom API Connector (Python)**

```python
# Airbyte supports building connectors with the CDK (Connector Development Kit)
# Example: Custom marketing platform connector

from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpStream
import requests

class CustomMarketingPlatformStream(HttpStream):
    """Stream for custom marketing platform API"""

    url_base = "https://api.customplatform.com/v1/"
    primary_key = "id"

    def __init__(self, api_key: str, **kwargs):
        super().__init__(**kwargs)
        self.api_key = api_key

    def next_page_token(self, response):
        """Handle pagination"""
        data = response.json()
        if data.get("next_page"):
            return {"page": data["next_page"]}
        return None

    def request_params(self, next_page_token=None, **kwargs):
        """Set request parameters"""
        params = {"api_key": self.api_key}
        if next_page_token:
            params.update(next_page_token)
        return params

    def parse_response(self, response, **kwargs):
        """Parse API response"""
        data = response.json()
        for record in data.get("results", []):
            yield record

class CampaignStream(CustomMarketingPlatformStream):
    """Campaign data stream"""

    def path(self, **kwargs):
        return "campaigns"

class AdPerformanceStream(CustomMarketingPlatformStream):
    """Ad performance metrics stream"""

    def path(self, **kwargs):
        return "ads/performance"

    def request_params(self, next_page_token=None, **kwargs):
        params = super().request_params(next_page_token, **kwargs)
        # Add date filter
        params["start_date"] = "2024-01-01"
        params["end_date"] = "2024-12-31"
        return params

class SourceCustomMarketingPlatform(AbstractSource):
    """Airbyte Source for custom marketing platform"""

    def check_connection(self, config):
        """Test the connection"""
        try:
            api_key = config["api_key"]
            response = requests.get(
                "https://api.customplatform.com/v1/status",
                params={"api_key": api_key}
            )
            return response.status_code == 200, None
        except Exception as e:
            return False, str(e)

    def streams(self, config):
        """Return list of available streams"""
        api_key = config["api_key"]
        return [
            CampaignStream(api_key=api_key),
            AdPerformanceStream(api_key=api_key)
        ]
```

### 3. Data Synchronization and Transformations

**Automated Sync with dbt Transformation**

```python
class AirbytePipeline:
    def __init__(self, airbyte_api):
        self.airbyte = airbyte_api

    def setup_marketing_pipeline(self, workspace_id, warehouse_config):
        """
        Set up complete marketing data pipeline with transformations
        """

        # 1. Create destination (Snowflake/BigQuery/Redshift)
        destination = self.airbyte.create_destination(
            workspace_id=workspace_id,
            destination_config={
                "name": "Marketing Warehouse",
                "definition_id": warehouse_config["definition_id"],
                "config": warehouse_config["credentials"]
            }
        )

        destination_id = destination["destinationId"]

        # 2. Create sources for each marketing platform
        sources = []

        marketing_sources = [
            {
                "name": "Google Ads",
                "definition_id": "google-ads-def-id",
                "config": {
                    "customer_id": "1234567890",
                    "start_date": "2024-01-01"
                }
            },
            {
                "name": "Facebook Ads",
                "definition_id": "facebook-marketing-def-id",
                "config": {
                    "account_id": "act_123456",
                    "start_date": "2024-01-01"
                }
            },
            {
                "name": "HubSpot",
                "definition_id": "hubspot-def-id",
                "config": {
                    "start_date": "2024-01-01"
                }
            }
        ]

        for source_config in marketing_sources:
            source = self.airbyte.create_source(workspace_id, source_config)
            sources.append(source)

        # 3. Create connections with sync schedules
        connections = []

        for source in sources:
            connection = self.airbyte.create_connection(
                source_id=source["sourceId"],
                destination_id=destination_id,
                config={
                    "name": f"{source['name']} -> Warehouse",
                    "schema": source["name"].lower().replace(" ", "_"),
                    "schedule_type": "cron",
                    "schedule_data": {
                        "cron": {
                            "cronExpression": "0 */6 * * *",  # Every 6 hours
                            "cronTimeZone": "UTC"
                        }
                    }
                }
            )
            connections.append(connection)

        return {
            "destination": destination,
            "sources": sources,
            "connections": connections
        }

    def monitor_syncs(self, connection_ids):
        """Monitor sync jobs"""

        status_report = []

        for conn_id in connection_ids:
            status = self.airbyte.get_connection_status(conn_id)

            status_report.append({
                "connection_id": conn_id,
                "name": status["name"],
                "status": status["status"],
                "last_sync": status.get("latestSyncJobCreatedAt"),
                "records_synced": status.get("recordsSynced", 0)
            })

        return status_report

# Example usage
pipeline = AirbytePipeline(airbyte)

warehouse_config = {
    "definition_id": "snowflake-destination-id",
    "credentials": {
        "host": "account.snowflakecomputing.com",
        "role": "AIRBYTE_ROLE",
        "warehouse": "COMPUTE_WH",
        "database": "MARKETING_DATA",
        "schema": "RAW_DATA",
        "username": "airbyte_user",
        "password": "password"
    }
}

# Set up pipeline
result = pipeline.setup_marketing_pipeline(
    workspace_id="workspace-id",
    warehouse_config=warehouse_config
)

print(f"Created {len(result['sources'])} sources")
print(f"Created {len(result['connections'])} connections")
```

### 4. Querying Synced Data

**Marketing Analytics Queries**

```sql
-- Airbyte creates tables in your warehouse
-- Naming convention: {schema}_{stream_name}

-- Google Ads campaign performance
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
    ROUND(100.0 * clicks / NULLIF(impressions, 0), 2) as ctr
FROM google_ads_campaign_performance_report
WHERE date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY cost DESC;

-- Facebook Ads insights
SELECT
    date_start as date,
    campaign_name,
    adset_name,
    impressions,
    clicks,
    spend,
    purchase_value,
    purchases,
    ROUND(spend / NULLIF(clicks, 0), 2) as cpc,
    ROUND(purchase_value / NULLIF(spend, 0), 2) as roas
FROM facebook_ads_insights
WHERE date_start >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY spend DESC;

-- HubSpot deals (sales pipeline)
SELECT
    dealname,
    dealstage,
    amount,
    closedate,
    pipeline,
    hs_analytics_source as source,
    hs_analytics_source_data_1 as campaign
FROM hubspot_deals
WHERE closedate >= CURRENT_DATE - INTERVAL '90 days'
    AND dealstage = 'closedwon'
ORDER BY closedate DESC;

-- Cross-platform performance
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
    FROM google_ads_campaign_performance_report

    UNION ALL

    SELECT
        date_start as date,
        'facebook_ads' as platform,
        campaign_name,
        spend,
        impressions,
        clicks,
        purchases,
        purchase_value as revenue
    FROM facebook_ads_insights

    UNION ALL

    SELECT
        day as date,
        'linkedin_ads' as platform,
        campaign_name,
        cost_in_usd as spend,
        impressions,
        clicks,
        external_website_conversions as purchases,
        external_website_post_click_conversions * 100 as revenue  -- Estimate
    FROM linkedin_ads_ad_analytics_by_campaign
)
SELECT
    platform,
    SUM(spend) as total_spend,
    SUM(impressions) as total_impressions,
    SUM(clicks) as total_clicks,
    SUM(purchases) as total_purchases,
    SUM(revenue) as total_revenue,
    ROUND(SUM(spend) / NULLIF(SUM(clicks), 0), 2) as avg_cpc,
    ROUND(SUM(revenue) / NULLIF(SUM(spend), 0), 2) as roas
FROM all_platforms
WHERE date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY platform
ORDER BY total_spend DESC;
```

**Python: Analyze Synced Data**

```python
import pandas as pd
from sqlalchemy import create_engine

def analyze_marketing_performance(warehouse_conn):
    """Analyze marketing performance from Airbyte-synced data"""

    # Get all platform data
    query = """
    WITH platform_performance AS (
        SELECT
            date,
            'google_ads' as platform,
            campaign_name,
            cost_micros / 1000000 as spend,
            conversions as purchases,
            conversions_value as revenue
        FROM google_ads_campaign_performance_report
        WHERE date >= CURRENT_DATE - INTERVAL '30 days'

        UNION ALL

        SELECT
            date_start as date,
            'facebook_ads' as platform,
            campaign_name,
            spend,
            purchases,
            purchase_value as revenue
        FROM facebook_ads_insights
        WHERE date_start >= CURRENT_DATE - INTERVAL '30 days'
    )
    SELECT
        date,
        platform,
        campaign_name,
        spend,
        purchases,
        revenue,
        CASE WHEN spend > 0 THEN revenue / spend ELSE 0 END as roas,
        CASE WHEN purchases > 0 THEN spend / purchases ELSE 0 END as cpa
    FROM platform_performance
    ORDER BY date DESC, spend DESC
    """

    df = pd.read_sql(query, warehouse_conn)

    # Analysis
    summary = df.groupby('platform').agg({
        'spend': 'sum',
        'purchases': 'sum',
        'revenue': 'sum',
        'roas': 'mean',
        'cpa': 'mean'
    }).round(2)

    print("\nPlatform Performance Summary:")
    print(summary)

    return df

# Usage
engine = create_engine('your_warehouse_connection_string')
performance_df = analyze_marketing_performance(engine)
```

## Installation and Deployment

### Self-Hosted Deployment (Docker)

```bash
# Clone Airbyte repository
git clone https://github.com/airbytehq/airbyte.git
cd airbyte

# Start Airbyte with Docker Compose
docker-compose up -d

# Access UI at http://localhost:8000
# Default credentials: airbyte / password
```

### Kubernetes Deployment

```yaml
# airbyte-values.yaml
global:
  database:
    type: external
    host: postgres.example.com
    port: 5432
    database: airbyte
    user: airbyte
    password: password

  storage:
    type: s3
    bucket: airbyte-storage
    region: us-east-1

webapp:
  replicaCount: 2

worker:
  replicaCount: 3
  resources:
    requests:
      memory: "2Gi"
      cpu: "1"
    limits:
      memory: "4Gi"
      cpu: "2"
```

```bash
# Install Airbyte on Kubernetes
helm repo add airbyte https://airbytehq.github.io/helm-charts
helm install airbyte airbyte/airbyte -f airbyte-values.yaml
```

### Python API Client

```bash
pip install airbyte-api
```

```python
from airbyte_api import AirbyteAPI

# For self-hosted
airbyte = AirbyteAPI(
    host="localhost",
    port=8000
)

# For Airbyte Cloud
# airbyte = AirbyteAPI(
#     host="api.airbyte.com",
#     api_key="your-api-key"
# )
```

## Quick Start

### Complete Setup Example

```python
from airbyte_api import AirbyteAPI

# 1. Initialize Airbyte
airbyte = AirbyteAPI(host="localhost", port=8000)

# 2. Get workspace
workspaces = airbyte.list_workspaces()
workspace_id = workspaces[0]["workspaceId"]

# 3. Create Snowflake destination
destination = airbyte.create_destination(
    workspace_id=workspace_id,
    destination_config={
        "name": "Snowflake Marketing Warehouse",
        "definition_id": "snowflake-destination-id",
        "config": {
            "host": "account.snowflakecomputing.com",
            "database": "MARKETING_DATA",
            "schema": "RAW",
            "username": "airbyte",
            "password": "password"
        }
    }
)

# 4. Create Google Ads source
source = airbyte.create_source(
    workspace_id=workspace_id,
    source_config={
        "name": "Google Ads",
        "definition_id": "google-ads-source-id",
        "config": {
            "customer_id": "1234567890",
            "start_date": "2024-01-01"
        }
    }
)

# 5. Create connection
connection = airbyte.create_connection(
    source_id=source["sourceId"],
    destination_id=destination["destinationId"],
    config={
        "name": "Google Ads -> Snowflake",
        "schema": "google_ads",
        "schedule_type": "cron",
        "schedule_data": {
            "cron": {
                "cronExpression": "0 */6 * * *",  # Every 6 hours
                "cronTimeZone": "UTC"
            }
        }
    }
)

# 6. Trigger first sync
airbyte.trigger_sync(connection["connectionId"])

print("Airbyte pipeline set up successfully!")
```

## References

- **Official Documentation**: https://docs.airbyte.com/
- **GitHub Repository**: https://github.com/airbytehq/airbyte
- **Connector Catalog**: https://docs.airbyte.com/integrations/
- **API Reference**: https://airbyte-public-api-docs.s3.us-east-2.amazonaws.com/rapidoc-api-docs.html
- **Connector Development**: https://docs.airbyte.com/connector-development/
- **CDK Documentation**: https://docs.airbyte.com/connector-development/cdk-python/
- **Deploy on Kubernetes**: https://docs.airbyte.com/deploying-airbyte/on-kubernetes/
- **dbt Integration**: https://docs.airbyte.com/operator-guides/transformation-and-normalization/transformations-with-dbt/
- **Community**: https://airbyte.com/community
- **Airbyte Cloud**: https://airbyte.com/airbyte-cloud

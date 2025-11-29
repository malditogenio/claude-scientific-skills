---
skill_name: rudderstack
display_name: RudderStack
description: Open-source Customer Data Platform for event streaming, warehouse-first data collection, and audience activation
category: cdp-data
tags: [cdp, open-source, event-streaming, warehouse-native, customer-data]
complexity: intermediate
dependencies: [rudder-sdk-python, rudder-sdk-js]
---

# RudderStack

## Overview

RudderStack is an open-source, warehouse-first Customer Data Platform that enables you to collect, unify, transform, and activate customer data. Unlike traditional CDPs, RudderStack is built with a warehouse-native architecture, treating your data warehouse as the source of truth.

Key differentiators:
- **Open Source Core**: Self-hosted option with full control over data
- **Warehouse-First Architecture**: Direct data collection into your warehouse
- **Real-Time Event Streaming**: Low-latency data pipeline for immediate activation
- **Privacy-First Design**: GDPR/CCPA compliant with data residency control
- **Developer-Friendly**: Extensive APIs and transformation capabilities

## When to Use

Use RudderStack when you need to:
- **Own Your Data Infrastructure**: Self-host your CDP with complete control
- **Warehouse-Native Analytics**: Collect data directly into Snowflake, BigQuery, or Redshift
- **Real-Time Activation**: Stream events to marketing tools in milliseconds
- **Cost-Effective CDP**: Reduce costs with open-source or cloud pricing
- **Advanced Transformations**: Apply custom data transformations in real-time
- **Multi-Cloud Deployment**: Deploy across AWS, GCP, Azure with data residency
- **Reverse ETL**: Activate warehouse data to marketing and sales tools

## Core Capabilities

### 1. Event Tracking and Data Collection

**JavaScript SDK (Web Tracking)**

```javascript
// Initialize RudderStack
rudderanalytics.load("YOUR_WRITE_KEY", "DATA_PLANE_URL", {
  logLevel: "INFO",
  integrations: {
    All: true,  // Send to all enabled destinations
  },
  // Configure storage
  storage: {
    encryption: {
      version: "v3"
    }
  }
});

// Identify users
rudderanalytics.identify("user_12345", {
  email: "user@example.com",
  name: "Jane Smith",
  plan: "premium",
  company: "Acme Corp",
  signupDate: "2024-01-15",
  ltv: 1500
}, {
  context: {
    campaign: {
      name: "Summer Sale",
      source: "google",
      medium: "cpc"
    }
  }
});

// Track events with rich properties
rudderanalytics.track("Product Purchased", {
  product_id: "prod_abc123",
  product_name: "Premium Subscription",
  revenue: 99.00,
  currency: "USD",
  category: "Subscription",
  // Attribution data
  utm_source: "facebook",
  utm_medium: "cpc",
  utm_campaign: "retargeting_q4",
  // Customer context
  customer_tier: "premium",
  payment_method: "stripe"
}, {
  integrations: {
    "Google Analytics 4": true,
    "Facebook Pixel": true,
    "Google Ads": true
  }
});

// Track page views
rudderanalytics.page("Product", "Pricing Page", {
  path: "/pricing",
  title: "Pricing - Premium Plans",
  url: window.location.href,
  referrer: document.referrer,
  // Custom properties
  experiment_variant: "new_pricing_v2",
  user_intent_score: 0.85
});

// Group users by account (B2B)
rudderanalytics.group("company_123", {
  name: "Acme Corporation",
  industry: "Technology",
  employees: 500,
  plan: "Enterprise",
  arr: 50000
});

// Track eCommerce events
rudderanalytics.track("Order Completed", {
  order_id: "ord_12345",
  total: 299.00,
  revenue: 299.00,
  shipping: 10.00,
  tax: 15.00,
  currency: "USD",
  products: [
    {
      product_id: "prod_1",
      sku: "SKU-001",
      name: "Premium Plan",
      price: 199.00,
      quantity: 1,
      category: "Subscription"
    },
    {
      product_id: "prod_2",
      sku: "SKU-002",
      name: "Add-on Feature",
      price: 100.00,
      quantity: 1,
      category: "Add-ons"
    }
  ]
});
```

**Python SDK (Server-Side Tracking)**

```python
import rudder_analytics as analytics
from datetime import datetime

# Initialize
analytics.write_key = "YOUR_WRITE_KEY"
analytics.data_plane_url = "DATA_PLANE_URL"

# Identify users
analytics.identify(
    user_id="user_12345",
    traits={
        "email": "user@example.com",
        "name": "Jane Smith",
        "plan": "premium",
        "company": "Acme Corp",
        "ltv": 1500,
        "signup_date": "2024-01-15"
    }
)

# Track conversion events
analytics.track(
    user_id="user_12345",
    event="Trial Converted",
    properties={
        "plan": "premium",
        "mrr": 99,
        "trial_start_date": "2024-11-01",
        "trial_end_date": "2024-11-15",
        "conversion_date": datetime.now().isoformat(),
        # Attribution
        "utm_source": "google",
        "utm_medium": "cpc",
        "utm_campaign": "trial_conversion",
        "gclid": "gclid_value"
    }
)

# Track revenue events for attribution
analytics.track(
    user_id="user_12345",
    event="Order Completed",
    properties={
        "order_id": "ord_789",
        "revenue": 299.00,
        "currency": "USD",
        "products": [
            {
                "product_id": "prod_1",
                "name": "Premium Plan",
                "price": 199,
                "quantity": 1
            }
        ],
        # Marketing attribution
        "utm_source": "facebook",
        "utm_medium": "cpc",
        "utm_campaign": "retargeting_q4",
        "fbclid": "fbclid_value"
    }
)

# Batch events for efficiency
def track_batch_events(events_list):
    """Track multiple events efficiently"""
    for event in events_list:
        analytics.track(
            user_id=event['user_id'],
            event=event['event_name'],
            properties=event['properties']
        )

    # Flush to ensure delivery
    analytics.flush()

# Example: Track user journey
user_journey = [
    {
        'user_id': 'user_123',
        'event_name': 'Page Viewed',
        'properties': {'page': 'landing', 'utm_source': 'google'}
    },
    {
        'user_id': 'user_123',
        'event_name': 'Form Submitted',
        'properties': {'form_type': 'contact', 'lead_score': 75}
    },
    {
        'user_id': 'user_123',
        'event_name': 'Trial Started',
        'properties': {'plan': 'premium', 'trial_days': 14}
    }
]

track_batch_events(user_journey)
```

### 2. Warehouse-Native Data Collection

**Direct Warehouse Sync Configuration**

```python
# RudderStack automatically syncs to your warehouse
# Configure warehouse destination in RudderStack UI or via API

import requests
import json

class RudderStackWarehouse:
    def __init__(self, access_token):
        self.access_token = access_token
        self.api_url = "https://api.rudderstack.com/v1"

    def configure_snowflake_destination(self, source_id, config):
        """Configure Snowflake as destination"""

        destination_config = {
            "destinationDefinitionId": "snowflake",
            "name": "Snowflake Production",
            "enabled": True,
            "config": {
                "account": config["account"],
                "warehouse": config["warehouse"],
                "database": config["database"],
                "user": config["user"],
                "password": config["password"],
                "namespace": config.get("namespace", "rudderstack"),
                "syncFrequency": config.get("sync_frequency", "30"),
                "syncStartAt": config.get("sync_start_at", "00:00"),
                # Table names
                "prefix": config.get("table_prefix", ""),
                "useRudderStorage": False
            }
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            f"{self.api_url}/sources/{source_id}/destinations",
            headers=headers,
            json=destination_config
        )

        return response.json()

# Query warehouse data for analytics
def query_rudderstack_warehouse(warehouse_conn):
    """Query RudderStack data in warehouse"""

    # Events are stored in standardized tables
    query = """
    SELECT
        user_id,
        event,
        timestamp,
        context_campaign_source as utm_source,
        context_campaign_medium as utm_medium,
        context_campaign_name as utm_campaign,
        revenue,
        properties
    FROM rudderstack.tracks
    WHERE event IN ('Order Completed', 'Trial Started')
        AND DATE(timestamp) >= CURRENT_DATE - INTERVAL '30 days'
    ORDER BY timestamp DESC
    """

    return pd.read_sql(query, warehouse_conn)
```

**Warehouse-First Analytics**

```sql
-- Query RudderStack data directly in your warehouse
-- All data is in standardized schema

-- User attribution analysis
WITH first_touch AS (
    SELECT
        user_id,
        MIN(timestamp) as first_touch_time,
        FIRST_VALUE(context_campaign_source) OVER (
            PARTITION BY user_id ORDER BY timestamp
        ) as first_touch_source,
        FIRST_VALUE(context_campaign_campaign) OVER (
            PARTITION BY user_id ORDER BY timestamp
        ) as first_touch_campaign
    FROM rudderstack.pages
    WHERE context_campaign_source IS NOT NULL
    GROUP BY user_id
),
conversions AS (
    SELECT
        user_id,
        SUM(revenue) as total_revenue,
        COUNT(*) as conversion_count,
        MIN(timestamp) as first_conversion_date
    FROM rudderstack.tracks
    WHERE event = 'Order Completed'
    GROUP BY user_id
)
SELECT
    ft.first_touch_source,
    ft.first_touch_campaign,
    COUNT(DISTINCT ft.user_id) as total_users,
    COUNT(DISTINCT c.user_id) as converted_users,
    SUM(c.total_revenue) as revenue,
    ROUND(100.0 * COUNT(DISTINCT c.user_id) / COUNT(DISTINCT ft.user_id), 2) as conversion_rate,
    ROUND(SUM(c.total_revenue) / COUNT(DISTINCT ft.user_id), 2) as revenue_per_user
FROM first_touch ft
LEFT JOIN conversions c ON ft.user_id = c.user_id
GROUP BY ft.first_touch_source, ft.first_touch_campaign
ORDER BY revenue DESC;

-- Funnel analysis from warehouse
SELECT
    DATE_TRUNC('week', timestamp) as week,
    COUNT(DISTINCT CASE WHEN event = 'Page Viewed' THEN user_id END) as page_views,
    COUNT(DISTINCT CASE WHEN event = 'Signed Up' THEN user_id END) as signups,
    COUNT(DISTINCT CASE WHEN event = 'Trial Started' THEN user_id END) as trials,
    COUNT(DISTINCT CASE WHEN event = 'Order Completed' THEN user_id END) as conversions,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN event = 'Signed Up' THEN user_id END) /
          NULLIF(COUNT(DISTINCT CASE WHEN event = 'Page Viewed' THEN user_id END), 0), 2) as visit_to_signup_rate,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN event = 'Order Completed' THEN user_id END) /
          NULLIF(COUNT(DISTINCT CASE WHEN event = 'Trial Started' THEN user_id END), 0), 2) as trial_to_paid_rate
FROM rudderstack.tracks
WHERE timestamp >= CURRENT_DATE - INTERVAL '12 weeks'
GROUP BY week
ORDER BY week DESC;
```

### 3. Audience Segmentation with Reverse ETL

**Build Audiences in Warehouse**

```sql
-- Create high-value customer segment in warehouse
CREATE OR REPLACE VIEW marketing.high_value_customers AS
WITH user_metrics AS (
    SELECT
        i.user_id,
        i.email,
        i.name,
        MAX(i.traits_plan) as current_plan,
        SUM(CASE WHEN t.event = 'Order Completed'
            AND t.timestamp > CURRENT_DATE - INTERVAL '90 days'
            THEN t.revenue ELSE 0 END) as revenue_90d,
        COUNT(DISTINCT CASE WHEN t.event = 'Order Completed'
            AND t.timestamp > CURRENT_DATE - INTERVAL '90 days'
            THEN t.id END) as orders_90d,
        MAX(t.timestamp) as last_activity_date
    FROM rudderstack.identifies i
    LEFT JOIN rudderstack.tracks t ON i.user_id = t.user_id
    GROUP BY i.user_id, i.email, i.name
)
SELECT
    user_id,
    email,
    name,
    current_plan,
    revenue_90d,
    orders_90d,
    last_activity_date,
    'high_value' as segment_name
FROM user_metrics
WHERE revenue_90d > 1000
    OR (orders_90d >= 3 AND revenue_90d > 500);

-- Cart abandonment segment
CREATE OR REPLACE VIEW marketing.cart_abandoners AS
WITH cart_adds AS (
    SELECT
        user_id,
        MAX(timestamp) as last_cart_add,
        COUNT(*) as items_added
    FROM rudderstack.tracks
    WHERE event = 'Product Added'
        AND timestamp > CURRENT_DATE - INTERVAL '7 days'
    GROUP BY user_id
),
recent_purchases AS (
    SELECT DISTINCT user_id
    FROM rudderstack.tracks
    WHERE event = 'Order Completed'
        AND timestamp > CURRENT_DATE - INTERVAL '7 days'
)
SELECT
    ca.user_id,
    i.email,
    i.name,
    ca.last_cart_add,
    ca.items_added,
    'cart_abandoner' as segment_name
FROM cart_adds ca
JOIN rudderstack.identifies i ON ca.user_id = i.user_id
WHERE ca.user_id NOT IN (SELECT user_id FROM recent_purchases)
    AND ca.items_added >= 1;
```

**Activate Warehouse Audiences via Reverse ETL**

```python
import rudder_analytics as analytics
import pandas as pd

class RudderStackReverseETL:
    """Activate warehouse segments to marketing tools"""

    def __init__(self, write_key, data_plane_url):
        analytics.write_key = write_key
        analytics.data_plane_url = data_plane_url

    def sync_warehouse_segment_to_destinations(self, warehouse_conn, segment_query, destinations):
        """
        Read segment from warehouse and sync to marketing tools

        destinations: ['facebook_custom_audiences', 'google_ads', 'braze']
        """
        # Get segment from warehouse
        segment_df = pd.read_sql(segment_query, warehouse_conn)

        print(f"Syncing {len(segment_df)} users from warehouse to {len(destinations)} destinations")

        for _, user in segment_df.iterrows():
            # Configure which destinations receive this data
            integrations = {dest: True for dest in destinations}

            # Identify user with segment membership
            analytics.identify(
                user_id=user['user_id'],
                traits={
                    'email': user.get('email'),
                    'name': user.get('name'),
                    'segment': user.get('segment_name'),
                    'segment_updated_at': datetime.now().isoformat(),
                    # Include computed metrics
                    'ltv_90d': user.get('revenue_90d'),
                    'orders_90d': user.get('orders_90d')
                },
                integrations=integrations
            )

        analytics.flush()
        return segment_df

    def sync_to_facebook_custom_audience(self, warehouse_conn):
        """Sync high-value segment to Facebook"""

        query = "SELECT * FROM marketing.high_value_customers"

        return self.sync_warehouse_segment_to_destinations(
            warehouse_conn,
            query,
            ['facebook_custom_audiences']
        )

    def sync_to_google_customer_match(self, warehouse_conn):
        """Sync high-intent users to Google Ads"""

        query = """
        SELECT user_id, email, name, segment_name
        FROM marketing.high_intent_prospects
        """

        return self.sync_warehouse_segment_to_destinations(
            warehouse_conn,
            query,
            ['google_ads']
        )

# Example usage
reverse_etl = RudderStackReverseETL(
    write_key="YOUR_WRITE_KEY",
    data_plane_url="https://your-dataplane.rudderstack.com"
)

# Sync warehouse segment to multiple platforms
segment_query = "SELECT * FROM marketing.high_value_customers LIMIT 10000"
reverse_etl.sync_warehouse_segment_to_destinations(
    warehouse_conn,
    segment_query,
    ['facebook_custom_audiences', 'google_ads', 'braze']
)
```

### 4. Real-Time Event Transformations

**User Transformations (JavaScript)**

```javascript
// Define transformation in RudderStack
// Runs on events before sending to destinations

export async function transformEvent(event, metadata) {
  // Enrich event with computed properties
  if (event.type === 'track' && event.event === 'Product Viewed') {
    // Add user engagement score
    const pageViews = await fetchUserMetric(event.userId, 'page_view_count');
    event.properties.engagement_score = calculateEngagementScore(pageViews);

    // Add customer tier based on LTV
    const ltv = event.traits?.ltv || 0;
    event.properties.customer_tier = ltv > 1000 ? 'high_value' : 'standard';

    // Normalize campaign parameters
    event.properties.utm_source = (event.properties.utm_source || '').toLowerCase();
    event.properties.utm_campaign = (event.properties.utm_campaign || '').toLowerCase();
  }

  // Filter out test users
  if (event.properties?.email?.endsWith('@test.com')) {
    return null;  // Drop event
  }

  return event;
}

function calculateEngagementScore(pageViews) {
  if (pageViews > 50) return 'high';
  if (pageViews > 10) return 'medium';
  return 'low';
}

// PII redaction transformation
export async function transformEvent(event, metadata) {
  // Remove PII before sending to certain destinations
  const nonPIIDestinations = ['Google Analytics 4', 'Mixpanel'];

  if (nonPIIDestinations.includes(metadata.destinationName)) {
    // Hash email
    if (event.traits?.email) {
      event.traits.email_hash = hashEmail(event.traits.email);
      delete event.traits.email;
    }

    // Remove phone
    delete event.traits.phone;
  }

  return event;
}
```

## Installation and Authentication

### JavaScript SDK

```bash
npm install rudder-sdk-js
```

```javascript
import * as rudderanalytics from "rudder-sdk-js";

rudderanalytics.load("YOUR_WRITE_KEY", "DATA_PLANE_URL");
rudderanalytics.ready(() => {
  console.log("RudderStack is ready");
});
```

### Python SDK

```bash
pip install rudder-sdk-python
```

```python
import rudder_analytics as analytics

analytics.write_key = "YOUR_WRITE_KEY"
analytics.data_plane_url = "DATA_PLANE_URL"  # e.g., https://your-dataplane.rudderstack.com
analytics.on_error = lambda error, items: print(f"Error: {error}")
```

### Self-Hosted Deployment (Docker)

```bash
# Clone RudderStack
git clone https://github.com/rudderlabs/rudder-server.git
cd rudder-server

# Set up configuration
cp .env.sample .env
# Edit .env with your warehouse credentials

# Start with Docker Compose
docker-compose up -d

# Access at http://localhost:8080
```

## Quick Start

### Complete Marketing Data Pipeline

```python
import rudder_analytics as analytics
import pandas as pd
from datetime import datetime

# Initialize RudderStack
analytics.write_key = "YOUR_WRITE_KEY"
analytics.data_plane_url = "DATA_PLANE_URL"

# 1. Track user acquisition with attribution
def track_acquisition(user_data, attribution):
    """Track new user with attribution data"""

    # Identify user
    analytics.identify(
        user_id=user_data['user_id'],
        traits={
            'email': user_data['email'],
            'name': user_data['name'],
            'signup_date': datetime.now().isoformat(),
            'plan': 'trial',
            # Store attribution in user profile
            'acquisition_source': attribution.get('utm_source'),
            'acquisition_campaign': attribution.get('utm_campaign')
        }
    )

    # Track signup event
    analytics.track(
        user_id=user_data['user_id'],
        event='Signed Up',
        properties={
            'signup_method': 'email',
            'utm_source': attribution.get('utm_source'),
            'utm_medium': attribution.get('utm_medium'),
            'utm_campaign': attribution.get('utm_campaign'),
            'gclid': attribution.get('gclid'),
            'fbclid': attribution.get('fbclid')
        }
    )

    analytics.flush()

# 2. Build audience in warehouse and activate
def activate_warehouse_audience(warehouse_conn):
    """Query warehouse and sync to ad platforms"""

    # Query high-value segment
    query = """
    SELECT user_id, email, revenue_90d
    FROM marketing.high_value_customers
    WHERE revenue_90d > 1000
    """

    audience_df = pd.read_sql(query, warehouse_conn)

    # Sync to multiple platforms
    for _, user in audience_df.iterrows():
        analytics.identify(
            user_id=user['user_id'],
            traits={
                'email': user['email'],
                'customer_segment': 'high_value',
                'revenue_90d': user['revenue_90d']
            },
            integrations={
                'Facebook Custom Audiences': True,
                'Google Ads': True,
                'Braze': True
            }
        )

    analytics.flush()
    return audience_df

# 3. Track conversions for attribution
def track_conversion(user_id, order_data):
    """Track purchase with complete attribution"""

    analytics.track(
        user_id=user_id,
        event='Order Completed',
        properties={
            'order_id': order_data['order_id'],
            'revenue': order_data['revenue'],
            'currency': 'USD',
            'products': order_data['products'],
            # Attribution
            'utm_source': order_data.get('utm_source'),
            'utm_campaign': order_data.get('utm_campaign'),
            'gclid': order_data.get('gclid')
        }
    )

    analytics.flush()

# Example: Complete workflow
if __name__ == "__main__":
    # Track acquisition
    track_acquisition(
        user_data={'user_id': 'user_789', 'email': 'new@example.com', 'name': 'New User'},
        attribution={'utm_source': 'google', 'utm_medium': 'cpc', 'utm_campaign': 'brand'}
    )

    # Activate warehouse audience (run this periodically)
    # activate_warehouse_audience(your_warehouse_connection)
```

## References

- **Official Documentation**: https://rudderstack.com/docs/
- **Open Source Repository**: https://github.com/rudderlabs/rudder-server
- **Event Spec**: https://rudderstack.com/docs/event-spec/
- **Warehouse Destinations**: https://rudderstack.com/docs/destinations/warehouse-destinations/
- **Reverse ETL**: https://rudderstack.com/docs/sources/reverse-etl/
- **Transformations**: https://rudderstack.com/docs/features/transformations/
- **Python SDK**: https://github.com/rudderlabs/rudder-sdk-python
- **JavaScript SDK**: https://github.com/rudderlabs/rudder-sdk-js
- **Self-Hosting Guide**: https://rudderstack.com/docs/get-started/rudderstack-open-source/
- **Cloud vs Open Source**: https://rudderstack.com/docs/get-started/rudderstack-cloud-vs-open-source/

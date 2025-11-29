---
skill_name: segment
display_name: Segment CDP
description: Customer Data Platform for event tracking, user profiling, and audience synchronization across marketing tools
category: cdp-data
tags: [cdp, analytics, event-tracking, audience-sync, customer-data]
complexity: intermediate
dependencies: [analytics-js, segment-python]
---

# Segment CDP

## Overview

Segment is a leading Customer Data Platform (CDP) that collects, standardizes, and routes customer data from various sources to hundreds of marketing, analytics, and data warehouse tools. It provides a unified API for event tracking, user identification, and audience management.

Segment enables marketing teams to:
- Track customer behavior across web, mobile, and server-side applications
- Build unified customer profiles from multiple touchpoints
- Create and sync audiences to advertising and marketing platforms
- Ensure data consistency across the entire marketing stack

## When to Use

Use Segment when you need to:
- **Centralize Event Tracking**: Implement a single tracking SDK across all platforms
- **Unify Customer Data**: Merge user interactions from multiple sources into unified profiles
- **Sync Audiences to Ad Platforms**: Send computed audiences to Facebook, Google Ads, etc.
- **Enable Marketing Attribution**: Track the complete customer journey across channels
- **Simplify Tool Integration**: Connect to 300+ destinations without custom integration code
- **Build Customer 360 Views**: Combine behavioral, transactional, and demographic data
- **Comply with Privacy Regulations**: Centralized consent management and data governance

## Core Capabilities

### 1. Event Tracking and Data Collection

**Client-Side Tracking (Analytics.js)**

```javascript
// Initialize Segment
analytics.load("YOUR_WRITE_KEY");

// Identify users with traits
analytics.identify("user_12345", {
  email: "user@example.com",
  name: "Jane Smith",
  plan: "premium",
  company: "Acme Corp",
  created_at: "2024-01-15",
  mrr: 99
});

// Track events
analytics.track("Product Purchased", {
  product_id: "prod_abc123",
  product_name: "Premium Plan",
  revenue: 99.00,
  currency: "USD",
  category: "Subscription",
  campaign_id: "summer_sale_2024"
});

// Track page views with properties
analytics.page("Product Page", {
  product_category: "SaaS",
  path: window.location.pathname,
  url: window.location.href
});

// Group users by account/organization
analytics.group("company_123", {
  name: "Acme Corporation",
  industry: "Technology",
  employees: 500,
  plan: "Enterprise"
});
```

**Server-Side Tracking (Python)**

```python
import analytics
from datetime import datetime

# Initialize with your write key
analytics.write_key = "YOUR_WRITE_KEY"

# Identify users
analytics.identify(
    user_id="user_12345",
    traits={
        "email": "user@example.com",
        "name": "Jane Smith",
        "plan": "premium",
        "ltv": 1200,
        "signup_date": "2024-01-15"
    }
)

# Track conversion events
analytics.track(
    user_id="user_12345",
    event="Trial Started",
    properties={
        "plan": "premium",
        "trial_days": 14,
        "source": "google_ads",
        "campaign": "q4_promotion",
        "ad_group": "premium_features"
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
            {"product_id": "prod_1", "price": 199, "quantity": 1},
            {"product_id": "prod_2", "price": 100, "quantity": 1}
        ],
        "utm_source": "facebook",
        "utm_medium": "cpc",
        "utm_campaign": "retargeting_q4"
    }
)

# Batch events for efficiency
analytics.flush()
```

### 2. Audience Segmentation and Computed Traits

**Using Segment Audiences (SQL-based)**

```sql
-- Create high-value customer audience
-- Revenue > $1000 in last 90 days
SELECT
    user_id,
    email,
    SUM(revenue) as total_revenue,
    COUNT(DISTINCT order_id) as order_count,
    MAX(timestamp) as last_purchase_date
FROM tracks
WHERE event = 'Order Completed'
    AND timestamp > CURRENT_DATE - INTERVAL '90 days'
GROUP BY user_id, email
HAVING SUM(revenue) > 1000;

-- Active users who haven't converted
SELECT DISTINCT
    i.user_id,
    i.email,
    i.traits_plan as current_plan
FROM identifies i
WHERE i.timestamp > CURRENT_DATE - INTERVAL '30 days'
    AND i.user_id NOT IN (
        SELECT user_id
        FROM tracks
        WHERE event = 'Subscription Started'
    )
    AND i.traits_plan = 'trial';

-- Cart abandonment audience
SELECT
    user_id,
    email,
    MAX(timestamp) as last_cart_add,
    COUNT(*) as items_in_cart
FROM tracks
WHERE event = 'Product Added'
    AND timestamp > CURRENT_DATE - INTERVAL '7 days'
    AND user_id NOT IN (
        SELECT user_id
        FROM tracks
        WHERE event = 'Order Completed'
        AND timestamp > CURRENT_DATE - INTERVAL '7 days'
    )
GROUP BY user_id, email
HAVING COUNT(*) >= 2;
```

**Computed Traits (Python)**

```python
# Use Segment Profile API to retrieve computed traits
import requests

def get_user_profile(user_id, space_id, access_token):
    """Get complete user profile with computed traits"""
    url = f"https://profiles.segment.com/v1/spaces/{space_id}/collections/users/profiles/user_id:{user_id}/traits"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    profile = response.json()

    # Extract computed traits for marketing decisions
    return {
        "user_id": user_id,
        "ltv": profile.get("traits", {}).get("lifetime_value"),
        "engagement_score": profile.get("traits", {}).get("engagement_score"),
        "churn_risk": profile.get("traits", {}).get("churn_risk_score"),
        "preferred_channel": profile.get("traits", {}).get("preferred_channel"),
        "last_purchase_days": profile.get("traits", {}).get("days_since_last_purchase")
    }

# Use computed traits for audience targeting
def should_target_for_winback(profile):
    """Determine if user should be in winback campaign"""
    return (
        profile["last_purchase_days"] > 60 and
        profile["ltv"] > 500 and
        profile["churn_risk"] > 0.7
    )
```

### 3. Marketing Analytics Queries

**Customer Journey Analysis**

```sql
-- Multi-touch attribution analysis
WITH user_touchpoints AS (
    SELECT
        user_id,
        timestamp,
        properties_utm_source as source,
        properties_utm_medium as medium,
        properties_utm_campaign as campaign,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp) as touch_number
    FROM tracks
    WHERE event IN ('Page Viewed', 'Campaign Clicked')
        AND properties_utm_source IS NOT NULL
),
conversions AS (
    SELECT
        user_id,
        MIN(timestamp) as conversion_date,
        SUM(properties_revenue) as revenue
    FROM tracks
    WHERE event = 'Order Completed'
    GROUP BY user_id
)
SELECT
    t.source,
    t.medium,
    t.campaign,
    COUNT(DISTINCT CASE WHEN t.touch_number = 1 THEN t.user_id END) as first_touch_conversions,
    COUNT(DISTINCT CASE WHEN t.touch_number > 1 THEN t.user_id END) as multi_touch_conversions,
    SUM(c.revenue) as attributed_revenue,
    AVG(c.revenue) as avg_order_value
FROM user_touchpoints t
JOIN conversions c ON t.user_id = c.user_id
WHERE t.timestamp <= c.conversion_date
GROUP BY t.source, t.medium, t.campaign
ORDER BY attributed_revenue DESC;

-- Funnel conversion analysis
SELECT
    DATE_TRUNC('week', timestamp) as week,
    COUNT(DISTINCT CASE WHEN event = 'Signed Up' THEN user_id END) as signups,
    COUNT(DISTINCT CASE WHEN event = 'Trial Started' THEN user_id END) as trials,
    COUNT(DISTINCT CASE WHEN event = 'Subscription Started' THEN user_id END) as conversions,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN event = 'Trial Started' THEN user_id END) /
          NULLIF(COUNT(DISTINCT CASE WHEN event = 'Signed Up' THEN user_id END), 0), 2) as signup_to_trial_rate,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN event = 'Subscription Started' THEN user_id END) /
          NULLIF(COUNT(DISTINCT CASE WHEN event = 'Trial Started' THEN user_id END), 0), 2) as trial_to_paid_rate
FROM tracks
WHERE timestamp >= CURRENT_DATE - INTERVAL '12 weeks'
GROUP BY DATE_TRUNC('week', timestamp)
ORDER BY week DESC;

-- Cohort retention analysis
WITH cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', MIN(timestamp)) as cohort_month
    FROM tracks
    WHERE event = 'Signed Up'
    GROUP BY user_id
),
user_activity AS (
    SELECT DISTINCT
        user_id,
        DATE_TRUNC('month', timestamp) as activity_month
    FROM tracks
    WHERE event IN ('Page Viewed', 'Feature Used', 'Order Completed')
)
SELECT
    c.cohort_month,
    DATEDIFF('month', c.cohort_month, a.activity_month) as months_since_signup,
    COUNT(DISTINCT a.user_id) as active_users,
    COUNT(DISTINCT c.user_id) as cohort_size,
    ROUND(100.0 * COUNT(DISTINCT a.user_id) / COUNT(DISTINCT c.user_id), 2) as retention_rate
FROM cohorts c
LEFT JOIN user_activity a ON c.user_id = a.user_id
GROUP BY c.cohort_month, months_since_signup
ORDER BY c.cohort_month, months_since_signup;
```

**Campaign Performance Analysis**

```python
import pandas as pd
from segment import analytics
import requests

def analyze_campaign_performance(warehouse_connection, campaign_id, date_range):
    """Analyze campaign performance using Segment data"""

    query = f"""
    WITH campaign_users AS (
        SELECT DISTINCT user_id
        FROM tracks
        WHERE event = 'Campaign Clicked'
            AND properties_campaign_id = '{campaign_id}'
            AND timestamp BETWEEN '{date_range[0]}' AND '{date_range[1]}'
    ),
    user_conversions AS (
        SELECT
            t.user_id,
            COUNT(DISTINCT CASE WHEN t.event = 'Trial Started' THEN t.event_id END) as trials,
            COUNT(DISTINCT CASE WHEN t.event = 'Subscription Started' THEN t.event_id END) as conversions,
            SUM(CASE WHEN t.event = 'Order Completed' THEN t.properties_revenue ELSE 0 END) as revenue
        FROM tracks t
        JOIN campaign_users cu ON t.user_id = cu.user_id
        WHERE t.timestamp >= '{date_range[0]}'
        GROUP BY t.user_id
    )
    SELECT
        '{campaign_id}' as campaign_id,
        COUNT(*) as total_users,
        SUM(trials) as total_trials,
        SUM(conversions) as total_conversions,
        SUM(revenue) as total_revenue,
        ROUND(100.0 * SUM(trials) / COUNT(*), 2) as trial_conversion_rate,
        ROUND(100.0 * SUM(conversions) / COUNT(*), 2) as paid_conversion_rate,
        ROUND(SUM(revenue) / NULLIF(SUM(conversions), 0), 2) as avg_revenue_per_conversion
    FROM user_conversions
    """

    df = pd.read_sql(query, warehouse_connection)
    return df
```

### 4. Syncing Audiences to Ad Platforms

**Facebook Ads Audience Sync**

```python
# Segment automatically syncs to Facebook Custom Audiences
# Configure in Segment UI, then track events that trigger sync

analytics.track(
    user_id="user_12345",
    event="Email Subscribed",
    properties={
        "list": "high_intent_prospects",
        "source": "landing_page"
    },
    integrations={
        "Facebook Pixel": True,  # Ensure event goes to Facebook
        "Facebook Custom Audiences": {
            "audience_id": "23850000000000000"  # Your custom audience ID
        }
    }
)

# Track audience membership changes
def sync_audience_to_facebook(audience_name, user_list):
    """Add users to audience and track in Segment"""
    for user in user_list:
        analytics.track(
            user_id=user["user_id"],
            event="Audience Entered",
            properties={
                "audience_name": audience_name,
                "destination": "facebook_custom_audiences",
                "sync_timestamp": datetime.now().isoformat()
            }
        )

    analytics.flush()
```

**Google Ads Customer Match**

```python
# Configure Google Ads destination in Segment
# Use identify calls to sync user data for Customer Match

def sync_to_google_customer_match(users_df):
    """Sync user list to Google Ads via Segment"""

    for _, user in users_df.iterrows():
        analytics.identify(
            user_id=user["user_id"],
            traits={
                "email": user["email"],
                "phone": user["phone"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "country": user["country"],
                "zip_code": user["zip_code"]
            },
            integrations={
                "Google Ads": {
                    "customer_match_user_list_id": "1234567890"
                }
            }
        )

    analytics.flush()
    print(f"Synced {len(users_df)} users to Google Customer Match")

# Track high-value actions for similar audiences
analytics.track(
    user_id="user_12345",
    event="High Value Conversion",
    properties={
        "conversion_value": 500,
        "conversion_label": "premium_signup"
    },
    integrations={
        "Google Ads (Gtag)": True
    }
)
```

**Multi-Platform Audience Sync**

```python
import pandas as pd
from datetime import datetime, timedelta

def sync_audience_multi_platform(audience_query, warehouse_conn, platforms):
    """
    Sync audience to multiple advertising platforms

    platforms: ["facebook", "google_ads", "linkedin", "tiktok"]
    """
    # Get audience from data warehouse
    audience_df = pd.read_sql(audience_query, warehouse_conn)

    print(f"Syncing {len(audience_df)} users to {len(platforms)} platforms")

    for _, user in audience_df.iterrows():
        # Build integration config for each platform
        integrations = {}

        if "facebook" in platforms:
            integrations["Facebook Custom Audiences"] = True
        if "google_ads" in platforms:
            integrations["Google Ads"] = True
        if "linkedin" in platforms:
            integrations["LinkedIn Insight Tag"] = True
        if "tiktok" in platforms:
            integrations["TikTok Pixel"] = True

        # Identify user with traits
        analytics.identify(
            user_id=user["user_id"],
            traits={
                "email": user["email"],
                "audience_segment": user.get("segment_name"),
                "ltv": user.get("lifetime_value"),
                "last_purchase_date": user.get("last_purchase_date")
            },
            integrations=integrations
        )

    analytics.flush()

    # Track the sync operation
    analytics.track(
        user_id="system",
        event="Audience Synced",
        properties={
            "audience_size": len(audience_df),
            "platforms": platforms,
            "sync_timestamp": datetime.now().isoformat()
        }
    )
```

## Installation and Authentication

### Analytics.js (Client-Side)

```html
<!-- Add to your website's <head> -->
<script>
  !function(){var analytics=window.analytics=window.analytics||[];if(!analytics.initialize)if(analytics.invoked)window.console&&console.error&&console.error("Segment snippet included twice.");else{analytics.invoked=!0;analytics.methods=["trackSubmit","trackClick","trackLink","trackForm","pageview","identify","reset","group","track","ready","alias","debug","page","once","off","on","addSourceMiddleware","addIntegrationMiddleware","setAnonymousId","addDestinationMiddleware"];analytics.factory=function(e){return function(){var t=Array.prototype.slice.call(arguments);t.unshift(e);analytics.push(t);return analytics}};for(var e=0;e<analytics.methods.length;e++){var key=analytics.methods[e];analytics[key]=analytics.factory(key)}analytics.load=function(key,e){var t=document.createElement("script");t.type="text/javascript";t.async=!0;t.src="https://cdn.segment.com/analytics.js/v1/" + key + "/analytics.min.js";var n=document.getElementsByTagName("script")[0];n.parentNode.insertBefore(t,n);analytics._loadOptions=e};analytics._writeKey="YOUR_WRITE_KEY";analytics.SNIPPET_VERSION="4.15.3";
  analytics.load("YOUR_WRITE_KEY");
  analytics.page();
  }}();
</script>
```

### Python SDK

```bash
pip install segment-analytics-python
```

```python
import analytics

# Configure with your write key
analytics.write_key = "YOUR_WRITE_KEY"

# Optional: Configure for high-throughput scenarios
analytics.max_queue_size = 100000  # Maximum events in queue
analytics.send = True  # Enable sending
analytics.sync_mode = False  # Async mode for better performance
```

### Node.js SDK

```bash
npm install analytics-node
```

```javascript
const Analytics = require('analytics-node');
const analytics = new Analytics('YOUR_WRITE_KEY', {
  flushAt: 20,  // Flush after 20 events
  flushInterval: 10000  // Flush every 10 seconds
});
```

## Quick Start

### Complete Implementation Example

```python
import analytics
import pandas as pd
from datetime import datetime

# Initialize
analytics.write_key = "YOUR_WRITE_KEY"

# 1. Track user signup with campaign attribution
def track_signup(user_data, utm_params):
    # Identify the user
    analytics.identify(
        user_id=user_data["user_id"],
        traits={
            "email": user_data["email"],
            "name": user_data["name"],
            "created_at": datetime.now().isoformat(),
            "plan": "trial"
        }
    )

    # Track signup event
    analytics.track(
        user_id=user_data["user_id"],
        event="Signed Up",
        properties={
            "utm_source": utm_params.get("utm_source"),
            "utm_medium": utm_params.get("utm_medium"),
            "utm_campaign": utm_params.get("utm_campaign"),
            "signup_method": "email"
        }
    )

    analytics.flush()

# 2. Build and sync high-value audience
def create_high_value_audience(warehouse_conn):
    query = """
    SELECT DISTINCT
        i.user_id,
        i.email,
        SUM(t.properties_revenue) as total_revenue
    FROM identifies i
    JOIN tracks t ON i.user_id = t.user_id
    WHERE t.event = 'Order Completed'
        AND t.timestamp > CURRENT_DATE - INTERVAL '90 days'
    GROUP BY i.user_id, i.email
    HAVING SUM(t.properties_revenue) > 1000
    """

    audience_df = pd.read_sql(query, warehouse_conn)

    # Sync to advertising platforms
    for _, user in audience_df.iterrows():
        analytics.identify(
            user_id=user["user_id"],
            traits={
                "email": user["email"],
                "customer_segment": "high_value",
                "total_revenue_90d": user["total_revenue"]
            },
            integrations={
                "Facebook Custom Audiences": True,
                "Google Ads": True
            }
        )

    analytics.flush()
    return audience_df

# 3. Track conversions for attribution
def track_conversion(user_id, order_data, attribution_data):
    analytics.track(
        user_id=user_id,
        event="Order Completed",
        properties={
            "order_id": order_data["order_id"],
            "revenue": order_data["revenue"],
            "currency": "USD",
            "products": order_data["products"],
            # Attribution parameters
            "utm_source": attribution_data.get("utm_source"),
            "utm_medium": attribution_data.get("utm_medium"),
            "utm_campaign": attribution_data.get("utm_campaign"),
            "gclid": attribution_data.get("gclid"),  # Google Click ID
            "fbclid": attribution_data.get("fbclid")  # Facebook Click ID
        }
    )

    analytics.flush()

# Example usage
if __name__ == "__main__":
    # Track new user signup
    track_signup(
        user_data={"user_id": "user_789", "email": "new@example.com", "name": "New User"},
        utm_params={"utm_source": "google", "utm_medium": "cpc", "utm_campaign": "brand_search"}
    )
```

## References

- **Official Documentation**: https://segment.com/docs/
- **Connections Catalog**: https://segment.com/catalog/
- **Personas Documentation**: https://segment.com/docs/personas/
- **Protocols (Data Quality)**: https://segment.com/docs/protocols/
- **Profile API**: https://segment.com/docs/profiles/profile-api/
- **Python SDK**: https://github.com/segmentio/analytics-python
- **Analytics.js**: https://segment.com/docs/connections/sources/catalog/libraries/website/javascript/
- **Audience Destinations**: https://segment.com/docs/personas/using-personas-data/#send-audiences-to-destinations
- **Best Practices**: https://segment.com/docs/getting-started/implementation-guide/
- **Privacy & GDPR**: https://segment.com/docs/privacy/

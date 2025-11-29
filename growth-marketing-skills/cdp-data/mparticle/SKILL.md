---
skill_name: mparticle
display_name: mParticle CDP
description: Customer data infrastructure platform for collecting, unifying, and activating customer data across marketing tools
category: cdp-data
tags: [cdp, customer-data, data-infrastructure, audience-sync, analytics]
complexity: intermediate
dependencies: [mparticle-sdk]
---

# mParticle CDP

## Overview

mParticle is an enterprise Customer Data Platform focused on data quality, governance, and real-time customer data orchestration. It provides a comprehensive data infrastructure for collecting, transforming, and routing customer data across the marketing technology stack.

mParticle excels at:
- Real-time data collection and validation across all platforms
- Data quality enforcement with schema management
- Identity resolution and customer profile unification
- Audience building and activation across 300+ integrations
- Privacy compliance and consent management

## When to Use

Use mParticle when you need to:
- **Enterprise Data Governance**: Enforce data quality standards and schemas across teams
- **Real-Time Personalization**: Activate customer data in milliseconds for personalized experiences
- **Identity Resolution**: Unify customer identities across devices and platforms
- **Multi-Cloud Architecture**: Route data to different cloud providers and regions
- **Privacy Compliance**: Manage consent and data subject rights (GDPR, CCPA)
- **Advanced Audience Building**: Create sophisticated segments with real-time computation
- **API-First Integration**: Build custom data pipelines with comprehensive APIs

## Core Capabilities

### 1. Event Tracking and Data Collection

**Web Tracking (JavaScript SDK)**

```javascript
// Initialize mParticle
window.mParticle = {
    config: {
        isDevelopmentMode: false,
        identifyRequest: {
            userIdentities: {
                email: 'user@example.com',
                customerid: 'user_12345'
            }
        },
        dataPlan: {
            planId: 'marketing_events_plan',
            planVersion: 2
        }
    }
};

// Load the SDK
(function(t){window.mParticle=window.mParticle||{};window.mParticle.EventType={Unknown:0,Navigation:1,Location:2,Search:3,Transaction:4,UserContent:5,UserPreference:6,Social:7,Other:8};window.mParticle.eCommerce={Cart:{}};window.mParticle.Identity={};window.mParticle.config=window.mParticle.config||{};window.mParticle.config.rq=[];window.mParticle.config.snippetVersion=2.3;window.mParticle.ready=function(t){window.mParticle.config.rq.push(t)};var e=["endSession","logError","logBaseEvent","logEvent","logForm","logLink","logPageView","setSessionAttribute","setAppName","setAppVersion","setOptOut","setPosition","startNewSession","startTrackingLocation","stopTrackingLocation"];var o=["setCurrencyCode","logCheckout"];var i=["identify","login","logout","modify"];e.forEach(function(t){window.mParticle[t]=n(t)});o.forEach(function(t){window.mParticle.eCommerce[t]=n(t,"eCommerce")});i.forEach(function(t){window.mParticle.Identity[t]=n(t,"Identity")});function n(e,o){return function(){if(o){e=o+"."+e}var t=Array.prototype.slice.call(arguments);t.unshift(e);window.mParticle.config.rq.push(t)}}var dpId,dpV,config=window.mParticle.config,env=config.isDevelopmentMode?1:0,dbUrl="?env="+env,dataPlan=window.mParticle.config.dataPlan;dataPlan&&(dpId=dataPlan.planId,dpV=dataPlan.planVersion,dpId&&(dpV&&(dpV<1||dpV>1e3)&&(dpV=null),dbUrl+="&plan_id="+dpId+(dpV?"&plan_version="+dpV:"")));var mp=document.createElement("script");mp.type="text/javascript";mp.async=true;mp.src=("https:"==document.location.protocol?"https://jssdkcdns":"http://jssdkcdn")+".mparticle.com/js/v2/"+t+"/mparticle.js" + dbUrl;var c=document.getElementsByTagName("script")[0];c.parentNode.insertBefore(mp,c)}("YOUR_API_KEY"));

// Identify user
mParticle.Identity.login({
    userIdentities: {
        email: 'customer@example.com',
        customerid: 'cust_12345'
    }
});

// Track custom events
mParticle.logEvent(
    'Product Viewed',
    mParticle.EventType.Navigation,
    {
        'product_id': 'prod_abc123',
        'product_name': 'Premium Plan',
        'product_price': 99.00,
        'product_category': 'Subscription',
        'campaign_id': 'summer_promo'
    }
);

// Track page views with custom attributes
mParticle.logPageView(
    'Product Page',
    {
        'page_category': 'Pricing',
        'user_intent': 'high',
        'ab_test_variant': 'variant_b'
    }
);
```

**Server-Side Tracking (Python SDK)**

```python
from mparticle import AppEvent, SessionStartEvent, SessionEndEvent, Batch
from mparticle import User, UserIdentities, UserAttributes
import mparticle

# Configure the SDK
configuration = mparticle.Configuration()
configuration.api_key = 'YOUR_API_KEY'
configuration.api_secret = 'YOUR_API_SECRET'

api_instance = mparticle.EventsApi(mparticle.ApiClient(configuration))

# Create user identities
user_identities = UserIdentities(
    customer_id='user_12345',
    email='user@example.com'
)

user_attributes = UserAttributes(
    customer_ltv=1500.00,
    acquisition_channel='paid_search',
    subscription_tier='premium'
)

# Track custom event
event = AppEvent(
    event_name='Trial Started',
    custom_event_type='other',
    custom_attributes={
        'trial_length_days': 14,
        'plan_type': 'premium',
        'utm_source': 'google',
        'utm_campaign': 'q4_trial_promo',
        'trial_start_date': '2024-11-29'
    }
)

# Create batch request
batch = Batch(
    environment='production',
    user_identities=user_identities,
    user_attributes=user_attributes,
    events=[event]
)

# Send to mParticle
try:
    api_instance.upload_events(batch)
    print("Event tracked successfully")
except Exception as e:
    print(f"Error tracking event: {e}")

# Track eCommerce transaction
from mparticle import CommerceEvent, Product, ProductAction, TransactionAttributes

def track_purchase(user_id, order_data):
    """Track purchase with full commerce details"""

    products = [
        Product(
            id=item['product_id'],
            name=item['product_name'],
            price=item['price'],
            quantity=item['quantity'],
            category=item.get('category'),
            brand=item.get('brand')
        )
        for item in order_data['items']
    ]

    transaction_attributes = TransactionAttributes(
        transaction_id=order_data['order_id'],
        revenue=order_data['total_revenue'],
        tax=order_data.get('tax', 0),
        shipping=order_data.get('shipping', 0),
        coupon_code=order_data.get('coupon_code')
    )

    product_action = ProductAction(
        action='purchase',
        transaction_id=order_data['order_id'],
        products=products,
        transaction_attributes=transaction_attributes
    )

    commerce_event = CommerceEvent(
        product_action=product_action,
        custom_attributes={
            'payment_method': order_data.get('payment_method'),
            'utm_source': order_data.get('utm_source'),
            'utm_campaign': order_data.get('utm_campaign')
        }
    )

    batch = Batch(
        environment='production',
        user_identities=UserIdentities(customer_id=user_id),
        events=[commerce_event]
    )

    api_instance.upload_events(batch)
```

### 2. Audience Segmentation and Profile Building

**Audience Builder (SQL-Like)**

```python
# Use mParticle Audience API to create and manage audiences
import requests
import json

class mParticleAudience:
    def __init__(self, account_id, workspace_id, bearer_token):
        self.account_id = account_id
        self.workspace_id = workspace_id
        self.bearer_token = bearer_token
        self.base_url = f"https://api.mparticle.com/platform/v2/audiences"

    def create_audience(self, audience_config):
        """Create a new audience with criteria"""

        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "account_id": self.account_id,
            "workspace_id": self.workspace_id,
            "audience_name": audience_config["name"],
            "criteria": audience_config["criteria"],
            "destinations": audience_config.get("destinations", [])
        }

        response = requests.post(
            f"{self.base_url}",
            headers=headers,
            json=payload
        )

        return response.json()

# High-value customer audience
high_value_audience = {
    "name": "High Value Customers - Last 90 Days",
    "criteria": {
        "and": [
            {
                "event": {
                    "event_name": "Order Completed",
                    "attribute_filters": [{
                        "attribute": "revenue",
                        "operator": "greater_than",
                        "value": 1000
                    }],
                    "time_range": {
                        "type": "relative",
                        "days": 90
                    }
                }
            },
            {
                "user_attribute": {
                    "attribute": "subscription_status",
                    "operator": "equals",
                    "value": "active"
                }
            }
        ]
    },
    "destinations": [
        {"type": "facebook_custom_audiences"},
        {"type": "google_ads_customer_match"}
    ]
}

# Cart abandonment audience
cart_abandoners = {
    "name": "Cart Abandoners - Last 7 Days",
    "criteria": {
        "and": [
            {
                "event": {
                    "event_name": "Product Added to Cart",
                    "time_range": {"type": "relative", "days": 7}
                }
            },
            {
                "not": {
                    "event": {
                        "event_name": "Order Completed",
                        "time_range": {"type": "relative", "days": 7}
                    }
                }
            }
        ]
    }
}

# Engaged but not converted
engaged_non_converters = {
    "name": "Engaged Users - No Purchase",
    "criteria": {
        "and": [
            {
                "event": {
                    "event_name": "Session Start",
                    "aggregate": {
                        "type": "count",
                        "operator": "greater_than",
                        "value": 5
                    },
                    "time_range": {"type": "relative", "days": 30}
                }
            },
            {
                "not": {
                    "event": {
                        "event_name": "Order Completed",
                        "time_range": {"type": "relative", "days": 30}
                    }
                }
            },
            {
                "user_attribute": {
                    "attribute": "customer_tier",
                    "operator": "equals",
                    "value": "free"
                }
            }
        ]
    }
}
```

### 3. Marketing Analytics Queries

**User Profile API for Analytics**

```python
import pandas as pd
from datetime import datetime, timedelta

class mParticleAnalytics:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.mparticle.com/v1"

    def get_user_profile(self, user_id):
        """Retrieve complete user profile"""
        import requests
        from requests.auth import HTTPBasicAuth

        url = f"{self.base_url}/users/{user_id}"

        response = requests.get(
            url,
            auth=HTTPBasicAuth(self.api_key, self.api_secret)
        )

        return response.json()

    def analyze_user_journey(self, user_id):
        """Get user's complete journey for attribution"""
        profile = self.get_user_profile(user_id)

        journey = {
            "user_id": user_id,
            "identities": profile.get("user_identities", {}),
            "attributes": profile.get("user_attributes", {}),
            "events": []
        }

        # Extract event history
        for event in profile.get("events", []):
            journey["events"].append({
                "timestamp": event.get("timestamp_unixtime_ms"),
                "event_name": event.get("event_name"),
                "event_type": event.get("event_type"),
                "attributes": event.get("custom_attributes", {}),
                "utm_source": event.get("custom_attributes", {}).get("utm_source"),
                "utm_campaign": event.get("custom_attributes", {}).get("utm_campaign")
            })

        return journey

    def calculate_attribution(self, user_id, conversion_event="Order Completed"):
        """Calculate multi-touch attribution for user"""
        journey = self.analyze_user_journey(user_id)

        # Find conversion event
        conversion = None
        for event in journey["events"]:
            if event["event_name"] == conversion_event:
                conversion = event
                break

        if not conversion:
            return None

        # Get all touchpoints before conversion
        conversion_time = conversion["timestamp"]
        touchpoints = [
            event for event in journey["events"]
            if event["timestamp"] < conversion_time
            and event.get("utm_source")
        ]

        # Attribution models
        attribution = {
            "first_touch": touchpoints[0] if touchpoints else None,
            "last_touch": touchpoints[-1] if touchpoints else None,
            "linear": self._linear_attribution(touchpoints),
            "time_decay": self._time_decay_attribution(touchpoints, conversion_time)
        }

        return attribution

    def _linear_attribution(self, touchpoints):
        """Equal credit to all touchpoints"""
        if not touchpoints:
            return []

        credit_per_touch = 1.0 / len(touchpoints)

        return [
            {
                "source": tp.get("utm_source"),
                "campaign": tp.get("utm_campaign"),
                "credit": credit_per_touch
            }
            for tp in touchpoints
        ]

    def _time_decay_attribution(self, touchpoints, conversion_time, half_life_days=7):
        """More credit to recent touchpoints"""
        import math

        if not touchpoints:
            return []

        # Calculate decay weights
        weights = []
        for tp in touchpoints:
            days_before_conversion = (conversion_time - tp["timestamp"]) / (1000 * 60 * 60 * 24)
            weight = math.exp(-0.693 * days_before_conversion / half_life_days)
            weights.append(weight)

        total_weight = sum(weights)

        return [
            {
                "source": tp.get("utm_source"),
                "campaign": tp.get("utm_campaign"),
                "credit": weight / total_weight,
                "days_before_conversion": (conversion_time - tp["timestamp"]) / (1000 * 60 * 60 * 24)
            }
            for tp, weight in zip(touchpoints, weights)
        ]
```

**Campaign Performance Analysis**

```python
def analyze_campaign_cohorts(api_client, campaign_id, start_date, end_date):
    """Analyze user cohorts by campaign"""

    # This would typically query mParticle's data warehouse output
    # Example using pandas with exported data

    query = f"""
    WITH campaign_users AS (
        SELECT DISTINCT
            mpid,
            MIN(event_timestamp) as first_touch
        FROM events
        WHERE event_name IN ('Page Viewed', 'App Opened')
            AND custom_attributes.utm_campaign = '{campaign_id}'
            AND event_timestamp BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY mpid
    ),
    user_conversions AS (
        SELECT
            cu.mpid,
            cu.first_touch,
            COUNT(CASE WHEN e.event_name = 'Trial Started' THEN 1 END) as trials,
            COUNT(CASE WHEN e.event_name = 'Order Completed' THEN 1 END) as conversions,
            SUM(CASE WHEN e.event_name = 'Order Completed'
                THEN CAST(e.custom_attributes.revenue AS FLOAT64) ELSE 0 END) as revenue
        FROM campaign_users cu
        LEFT JOIN events e ON cu.mpid = e.mpid
            AND e.event_timestamp >= cu.first_touch
        GROUP BY cu.mpid, cu.first_touch
    )
    SELECT
        DATE(first_touch) as acquisition_date,
        COUNT(*) as users_acquired,
        SUM(trials) as total_trials,
        SUM(conversions) as total_conversions,
        SUM(revenue) as total_revenue,
        ROUND(100.0 * SUM(trials) / COUNT(*), 2) as trial_rate,
        ROUND(100.0 * SUM(conversions) / COUNT(*), 2) as conversion_rate,
        ROUND(SUM(revenue) / COUNT(*), 2) as revenue_per_user
    FROM user_conversions
    GROUP BY DATE(first_touch)
    ORDER BY acquisition_date
    """

    # Execute on your data warehouse (BigQuery, Snowflake, etc.)
    return pd.read_sql(query, connection)
```

### 4. Syncing Audiences to Ad Platforms

**Automated Audience Sync**

```python
class mParticleAudienceSync:
    def __init__(self, account_id, bearer_token):
        self.account_id = account_id
        self.bearer_token = bearer_token
        self.api_url = "https://api.mparticle.com/platform/v2"

    def sync_audience_to_facebook(self, audience_id, fb_audience_id):
        """Configure audience sync to Facebook Custom Audiences"""

        config = {
            "audience_id": audience_id,
            "connection": {
                "type": "facebook_custom_audiences",
                "settings": {
                    "custom_audience_id": fb_audience_id,
                    "action": "add_and_remove",  # Sync additions and removals
                    "schema": ["email", "phone", "mobile_advertiser_id"]
                }
            }
        }

        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            f"{self.api_url}/audiences/{audience_id}/connections",
            headers=headers,
            json=config
        )

        return response.json()

    def sync_audience_to_google_ads(self, audience_id, customer_match_list_id):
        """Configure audience sync to Google Ads Customer Match"""

        config = {
            "audience_id": audience_id,
            "connection": {
                "type": "google_ads",
                "settings": {
                    "user_list_id": customer_match_list_id,
                    "match_type": "CRM_ID",
                    "membership_lifespan_days": 540,
                    "upload_key_type": "CONTACT_INFO"
                }
            }
        }

        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            f"{self.api_url}/audiences/{audience_id}/connections",
            headers=headers,
            json=config
        )

        return response.json()

    def sync_to_multiple_platforms(self, audience_id, platform_configs):
        """
        Sync single audience to multiple platforms

        platform_configs = {
            'facebook': {'audience_id': '123456'},
            'google_ads': {'user_list_id': '789012'},
            'linkedin': {'audience_id': '345678'}
        }
        """
        results = {}

        if 'facebook' in platform_configs:
            results['facebook'] = self.sync_audience_to_facebook(
                audience_id,
                platform_configs['facebook']['audience_id']
            )

        if 'google_ads' in platform_configs:
            results['google_ads'] = self.sync_audience_to_google_ads(
                audience_id,
                platform_configs['google_ads']['user_list_id']
            )

        # Add more platforms as needed

        return results

# Example usage
syncer = mParticleAudienceSync(account_id="12345", bearer_token="your_token")

# Sync high-value audience to multiple platforms
syncer.sync_to_multiple_platforms(
    audience_id="aud_high_value_customers",
    platform_configs={
        'facebook': {'audience_id': '23850000000000000'},
        'google_ads': {'user_list_id': '1234567890'}
    }
)
```

**Real-Time Audience Activation**

```python
def activate_real_time_audience(user_event, audience_criteria, destinations):
    """
    Evaluate user against audience criteria in real-time
    and activate to destinations immediately
    """

    # Check if user meets audience criteria
    if evaluate_criteria(user_event, audience_criteria):

        # Send to each destination
        for destination in destinations:
            batch = Batch(
                environment='production',
                user_identities=UserIdentities(
                    customer_id=user_event['user_id'],
                    email=user_event.get('email')
                ),
                user_attributes=UserAttributes(
                    audience_membership=[audience_criteria['name']]
                ),
                events=[
                    AppEvent(
                        event_name='Audience Membership Changed',
                        custom_attributes={
                            'audience_name': audience_criteria['name'],
                            'action': 'added',
                            'destination': destination['type']
                        }
                    )
                ]
            )

            # Send to mParticle (which forwards to destinations)
            api_instance.upload_events(batch)

def evaluate_criteria(user_event, criteria):
    """Simple criteria evaluation"""
    # Implement your criteria logic
    if criteria.get('min_ltv'):
        if user_event.get('ltv', 0) < criteria['min_ltv']:
            return False

    if criteria.get('required_events'):
        # Check event history
        pass

    return True
```

## Installation and Authentication

### JavaScript SDK

```html
<!-- Add to <head> section with your API key -->
<script>
window.mParticle = {
    config: {
        isDevelopmentMode: false,
        identifyRequest: {
            userIdentities: { email: 'user@example.com' }
        }
    }
};
</script>
<script src="https://jssdkcdns.mparticle.com/js/v2/YOUR_API_KEY/mparticle.js"></script>
```

### Python SDK

```bash
pip install mparticle
```

```python
import mparticle
from mparticle import Configuration

# Configure with API credentials
configuration = Configuration()
configuration.api_key = 'YOUR_API_KEY'
configuration.api_secret = 'YOUR_API_SECRET'

# Create API client
api_client = mparticle.ApiClient(configuration)
events_api = mparticle.EventsApi(api_client)
```

### iOS SDK

```bash
pod 'mParticle-Apple-SDK'
```

```swift
import mParticle_Apple_SDK

let options = MParticleOptions(
    key: "YOUR_API_KEY",
    secret: "YOUR_API_SECRET"
)

MParticle.sharedInstance().start(with: options)
```

### Android SDK

```gradle
dependencies {
    implementation 'com.mparticle:android-core:5+'
}
```

```java
MParticleOptions options = MParticleOptions.builder(this)
    .credentials("YOUR_API_KEY", "YOUR_API_SECRET")
    .build();

MParticle.start(options);
```

## Quick Start

### Complete Marketing Implementation

```python
import mparticle
from mparticle import (
    AppEvent, CommerceEvent, Product, ProductAction,
    Batch, User, UserIdentities, UserAttributes
)
from datetime import datetime

# Initialize
configuration = mparticle.Configuration()
configuration.api_key = 'YOUR_API_KEY'
configuration.api_secret = 'YOUR_API_SECRET'
events_api = mparticle.EventsApi(mparticle.ApiClient(configuration))

# 1. Track user acquisition with attribution
def track_user_acquisition(user_data, attribution):
    """Track new user signup with full attribution data"""

    user_identities = UserIdentities(
        customer_id=user_data['user_id'],
        email=user_data['email']
    )

    user_attributes = UserAttributes(
        acquisition_source=attribution.get('utm_source'),
        acquisition_campaign=attribution.get('utm_campaign'),
        first_touch_date=datetime.now().isoformat()
    )

    event = AppEvent(
        event_name='User Signed Up',
        custom_event_type='user_preference',
        custom_attributes={
            'signup_method': user_data.get('signup_method', 'email'),
            'utm_source': attribution.get('utm_source'),
            'utm_medium': attribution.get('utm_medium'),
            'utm_campaign': attribution.get('utm_campaign'),
            'gclid': attribution.get('gclid'),
            'fbclid': attribution.get('fbclid')
        }
    )

    batch = Batch(
        environment='production',
        user_identities=user_identities,
        user_attributes=user_attributes,
        events=[event]
    )

    events_api.upload_events(batch)

# 2. Track conversions for revenue attribution
def track_conversion(user_id, order_data):
    """Track purchase with revenue and attribution"""

    products = [
        Product(
            id=item['id'],
            name=item['name'],
            price=item['price'],
            quantity=item['quantity']
        )
        for item in order_data['items']
    ]

    commerce_event = CommerceEvent(
        product_action=ProductAction(
            action='purchase',
            transaction_id=order_data['order_id'],
            products=products
        ),
        custom_attributes={
            'revenue': order_data['revenue'],
            'utm_source': order_data.get('utm_source'),
            'utm_campaign': order_data.get('utm_campaign')
        }
    )

    batch = Batch(
        environment='production',
        user_identities=UserIdentities(customer_id=user_id),
        events=[commerce_event]
    )

    events_api.upload_events(batch)

# 3. Build and activate audience
from mparticle import mParticleAudienceSync

audience_manager = mParticleAudienceSync(
    account_id="your_account",
    bearer_token="your_token"
)

# Create high-intent audience
high_intent_config = {
    "name": "High Intent Prospects",
    "criteria": {
        "and": [
            {
                "event": {
                    "event_name": "Product Viewed",
                    "aggregate": {"type": "count", "operator": ">=", "value": 3},
                    "time_range": {"type": "relative", "days": 7}
                }
            },
            {
                "not": {
                    "event": {
                        "event_name": "Order Completed",
                        "time_range": {"type": "relative", "days": 30}
                    }
                }
            }
        ]
    }
}

# Sync to ad platforms
audience_id = audience_manager.create_audience(high_intent_config)
audience_manager.sync_to_multiple_platforms(
    audience_id,
    {
        'facebook': {'audience_id': 'fb_aud_123'},
        'google_ads': {'user_list_id': 'goog_list_456'}
    }
)
```

## References

- **Official Documentation**: https://docs.mparticle.com/
- **Platform API**: https://docs.mparticle.com/developers/platform/
- **Events API**: https://docs.mparticle.com/developers/server/http/
- **Python SDK**: https://github.com/mParticle/mparticle-python-sdk
- **Audiences**: https://docs.mparticle.com/guides/platform-guide/audiences/
- **Identity Strategy**: https://docs.mparticle.com/guides/idsync/introduction/
- **Data Planning**: https://docs.mparticle.com/guides/data-master/introduction/
- **Integrations Catalog**: https://docs.mparticle.com/integrations/
- **Privacy & Consent**: https://docs.mparticle.com/guides/consent-management/
- **Best Practices**: https://docs.mparticle.com/guides/getting-started/start-capturing-data/

---
name: pinterest-ads
description: "Pinterest Ads API for visual discovery advertising. Manage promoted pins, shopping ads, video ads, audience targeting, and analytics for e-commerce and inspiration-driven campaigns."
---

# Pinterest Ads

## Overview

Pinterest Ads provides access to a visual discovery platform with over 450 million monthly active users actively searching for inspiration and products. The Pinterest Ads API enables programmatic campaign management, product catalog integration, audience targeting, and comprehensive analytics for e-commerce and brand awareness campaigns.

This skill covers the Pinterest Ads API with Python, enabling automated campaign creation, shopping catalog management, audience targeting, and performance tracking for visual marketing.

## When to Use This Skill

Use this skill when you need to:
- Create and manage Pinterest advertising campaigns programmatically
- Promote pins and products to users with purchase intent
- Leverage visual search and discovery behavior
- Target audiences by interests, keywords, and demographics
- Set up Pinterest Shopping and product catalogs
- Generate performance reports and shopping analytics
- Manage large-scale product feeds and dynamic ads
- Implement conversion tracking for e-commerce
- Create and manage audience lists for remarketing
- Optimize for brand awareness and consideration
- Track product performance and catalog insights

## Core Capabilities

### 1. Campaign Management

**Create Campaign Structure:**
```python
import requests
import json

class PinterestAdsAPI:
    """Pinterest Ads API client."""

    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.pinterest.com/v5"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def create_campaign(self, ad_account_id, name, objective, daily_spend_cap=None,
                       lifetime_spend_cap=None):
        """Create a new campaign."""
        url = f"{self.base_url}/ad_accounts/{ad_account_id}/campaigns"

        data = {
            "name": name,
            "objective_type": objective,
            # AWARENESS, CONSIDERATION, VIDEO_VIEW, WEB_CONVERSIONS,
            # CATALOG_SALES, WEB_SESSIONS, OFFLINE_CONVERSIONS
            "status": "PAUSED",
        }

        if daily_spend_cap:
            data["daily_spend_cap"] = daily_spend_cap  # In micro currency

        if lifetime_spend_cap:
            data["lifetime_spend_cap"] = lifetime_spend_cap

        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def create_ad_group(self, ad_account_id, campaign_id, name, pacing_delivery_type,
                       start_time, bid_in_micro_currency, targeting_spec, optimization_goal):
        """Create an ad group."""
        url = f"{self.base_url}/ad_accounts/{ad_account_id}/ad_groups"

        data = {
            "name": name,
            "campaign_id": campaign_id,
            "pacing_delivery_type": pacing_delivery_type,  # STANDARD, ACCELERATED
            "start_time": int(start_time.timestamp()),
            "bid_in_micro_currency": bid_in_micro_currency,
            "optimization_goal_metadata": {
                "conversion_tag_v3_goal_metadata": {
                    "attribution_windows": {
                        "click_window_days": 30,
                        "view_window_days": 1,
                    }
                }
            },
            "placement_group": "ALL",  # ALL, BROWSE, SEARCH, or specific placements
            "targeting_spec": targeting_spec,
            "billable_event": "CLICKTHROUGH",  # CLICKTHROUGH, IMPRESSION, VIDEO_V_50_MRC
            "optimization_goal": optimization_goal,
            # AWARENESS, ENGAGEMENT, WEB_SESSIONS, WEB_CONVERSIONS, etc.
            "status": "PAUSED",
        }

        response = requests.post(url, headers=self.headers, json=data)
        return response.json()


def build_targeting_spec(interests=None, keywords=None, demographics=None,
                        locations=None, placements=None):
    """Build targeting specification."""
    targeting = {}

    # Interest targeting
    if interests:
        targeting["INTEREST"] = interests  # List of interest IDs

    # Keyword targeting
    if keywords:
        targeting["SEARCH_QUERY"] = [
            {
                "keyword": keyword,
                "match_type": "BROAD"  # BROAD, PHRASE, EXACT
            }
            for keyword in keywords
        ]

    # Demographics
    if demographics:
        if "age_buckets" in demographics:
            targeting["AGE_BUCKET"] = demographics["age_buckets"]
            # ["18-24", "25-34", "35-44", "45-49", "50-54", "55-64", "65+"]

        if "genders" in demographics:
            targeting["GENDER"] = demographics["genders"]  # ["MALE", "FEMALE"]

    # Location targeting
    if locations:
        targeting["GEO"] = locations  # List of location IDs

    # Placement targeting
    if placements:
        targeting["PLACEMENT"] = placements  # ["BROWSE", "SEARCH", "HOME_FEED"]

    return targeting


def create_pin_promotion(api, ad_account_id, ad_group_id, pin_id, creative_type="REGULAR"):
    """Create a promoted pin (ad)."""
    url = f"{api.base_url}/ad_accounts/{ad_account_id}/ads"

    data = {
        "ad_group_id": ad_group_id,
        "creative_type": creative_type,  # REGULAR, VIDEO, SHOPPING, CAROUSEL, IDEA
        "pin_id": pin_id,
        "status": "PAUSED",
        "is_pin_deleted": False,
        "is_removable": False,
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


# Create organic pin first
def create_pin(api, board_id, title, description, link, media_source_url=None,
              media_id=None):
    """Create an organic pin to promote."""
    url = f"{api.base_url}/pins"

    data = {
        "board_id": board_id,
        "title": title,
        "description": description,
        "link": link,
    }

    if media_source_url:
        data["media_source"] = {
            "source_type": "image_url",
            "url": media_source_url
        }
    elif media_id:
        data["media_source"] = {
            "source_type": "image_base64",
            "data": media_id
        }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()
```

**Shopping Ads and Product Catalogs:**
```python
def create_product_group(api, ad_account_id, ad_group_id, feed_id, filters=None):
    """Create a product group for shopping ads."""
    url = f"{api.base_url}/ad_accounts/{ad_account_id}/product_groups"

    data = {
        "ad_group_id": ad_group_id,
        "feed_id": feed_id,
        "name": "Product Group Name",
        "filters": filters or {},  # Product filtering criteria
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def upload_product_catalog(api, ad_account_id, catalog_name, feed_format="TSV",
                          location_url=None):
    """Create and upload product catalog."""
    url = f"{api.base_url}/catalogs"

    # Create catalog
    catalog_data = {
        "name": catalog_name,
        "format": feed_format,  # TSV, CSV, XML
    }

    catalog_response = requests.post(url, headers=api.headers, json=catalog_data)
    catalog_id = catalog_response.json()["id"]

    # Upload feed
    feed_url = f"{api.base_url}/catalogs/{catalog_id}/feeds"
    feed_data = {
        "name": f"{catalog_name} Feed",
        "format": feed_format,
        "location": location_url,  # URL to product feed file
        "default_currency": "USD",
        "default_locale": "en_US",
    }

    feed_response = requests.post(feed_url, headers=api.headers, json=feed_data)
    return catalog_response.json(), feed_response.json()


def create_carousel_pin(api, board_id, title, description, link, carousel_slides):
    """Create a carousel pin for ads."""
    url = f"{api.base_url}/pins"

    data = {
        "board_id": board_id,
        "title": title,
        "description": description,
        "link": link,
        "carousel_slots": carousel_slides,
        # carousel_slides format:
        # [{
        #     "title": "Slide 1",
        #     "description": "Description",
        #     "link": "https://example.com/1",
        #     "image_url": "https://example.com/image1.jpg"
        # }, ...]
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()
```

### 2. Reporting and Analytics

**Campaign Performance Reports:**
```python
import pandas as pd
from datetime import datetime, timedelta

def get_campaign_analytics(api, ad_account_id, campaign_ids, start_date, end_date,
                           granularity="DAY"):
    """Get campaign performance analytics."""
    url = f"{api.base_url}/ad_accounts/{ad_account_id}/campaigns/analytics"

    params = {
        "campaign_ids": campaign_ids,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "granularity": granularity,  # DAY, HOUR, WEEK, MONTH, TOTAL
        "columns": [
            "CAMPAIGN_ID",
            "CAMPAIGN_NAME",
            "SPEND_IN_DOLLAR",
            "IMPRESSION_1",
            "CLICKTHROUGH_1",
            "CTR",
            "CPC_IN_DOLLAR",
            "CPM_IN_DOLLAR",
            "TOTAL_ENGAGEMENT",
            "ENGAGEMENT_RATE",
            "OUTBOUND_CLICK",
            "SAVE_RATE",
            "PIN_CLICK_RATE",
            "TOTAL_CONVERSIONS",
            "CONVERSION_RATE",
            "COST_PER_CONVERSION",
            "TOTAL_CONVERSION_VALUE",
            "ROAS",
        ]
    }

    response = requests.get(url, headers=api.headers, params=params)
    data = response.json()

    results = []
    for item in data:
        results.append({
            'campaign_id': item.get('CAMPAIGN_ID'),
            'campaign_name': item.get('CAMPAIGN_NAME'),
            'date': item.get('DATE'),
            'spend': float(item.get('SPEND_IN_DOLLAR', 0)),
            'impressions': int(item.get('IMPRESSION_1', 0)),
            'clicks': int(item.get('CLICKTHROUGH_1', 0)),
            'ctr': float(item.get('CTR', 0)),
            'cpc': float(item.get('CPC_IN_DOLLAR', 0)),
            'cpm': float(item.get('CPM_IN_DOLLAR', 0)),
            'engagements': int(item.get('TOTAL_ENGAGEMENT', 0)),
            'engagement_rate': float(item.get('ENGAGEMENT_RATE', 0)),
            'outbound_clicks': int(item.get('OUTBOUND_CLICK', 0)),
            'saves': int(item.get('SAVE_RATE', 0)),
            'conversions': int(item.get('TOTAL_CONVERSIONS', 0)),
            'conversion_value': float(item.get('TOTAL_CONVERSION_VALUE', 0)),
            'roas': float(item.get('ROAS', 0)),
        })

    return pd.DataFrame(results)


def get_ad_analytics(api, ad_account_id, ad_ids, start_date, end_date):
    """Get individual ad (promoted pin) performance."""
    url = f"{api.base_url}/ad_accounts/{ad_account_id}/ads/analytics"

    params = {
        "ad_ids": ad_ids,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "columns": [
            "AD_ID",
            "SPEND_IN_DOLLAR",
            "IMPRESSION_1",
            "CLICKTHROUGH_1",
            "SAVE",
            "REPIN_1",
            "OUTBOUND_CLICK",
            "VIDEO_MRC_VIEW",
            "VIDEO_V50_WATCH_TIME",
        ]
    }

    response = requests.get(url, headers=api.headers, params=params)
    return response.json()


def get_audience_insights(api, ad_account_id, ad_group_id):
    """Get audience demographic insights."""
    url = f"{api.base_url}/ad_accounts/{ad_account_id}/ad_groups/{ad_group_id}/targeting_analytics/audience_insights"

    response = requests.get(url, headers=api.headers)
    data = response.json()

    insights = {
        'demographics': data.get('demographics', {}),
        'interests': data.get('interests', []),
        'location': data.get('location', []),
        'devices': data.get('devices', {}),
    }

    return insights
```

### 3. Audience Management

**Custom Audiences:**
```python
def create_customer_list_audience(api, ad_account_id, name, records):
    """Create customer list audience."""
    url = f"{api.base_url}/ad_accounts/{ad_account_id}/customer_lists"

    import hashlib

    # Hash user data
    hashed_records = []
    for record in records:
        hashed_record = {}
        if 'email' in record:
            hashed_record['hashed_email'] = hashlib.sha256(
                record['email'].lower().strip().encode()
            ).hexdigest()
        if 'phone' in record:
            hashed_record['hashed_phone_number'] = hashlib.sha256(
                record['phone'].strip().encode()
            ).hexdigest()
        hashed_records.append(hashed_record)

    data = {
        "name": name,
        "records": hashed_records,
        "list_type": "EMAIL",  # EMAIL, IDFA, MAID, etc.
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def create_visitor_audience(api, ad_account_id, name, tag_id, retention_days=180):
    """Create website visitor audience from Pinterest Tag."""
    url = f"{api.base_url}/ad_accounts/{ad_account_id}/audiences"

    data = {
        "name": name,
        "audience_type": "VISITOR",
        "rule": {
            "event_source": {
                "event_source_id": tag_id
            },
            "retention_days": retention_days,
            "visitor_type": "VISITOR"  # VISITOR, ENGAGER
        },
        "description": "Website visitors in last 180 days"
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def create_engagement_audience(api, ad_account_id, name, engagement_type="PIN_SAVE"):
    """Create engagement audience based on pin interactions."""
    url = f"{api.base_url}/ad_accounts/{ad_account_id}/audiences"

    data = {
        "name": name,
        "audience_type": "ENGAGEMENT",
        "rule": {
            "engagement_type": engagement_type,
            # PIN_SAVE, PIN_CLICK, CLOSEUP, VIDEO_VIEW, etc.
            "engagement_domain": ["pinterest.com"],
            "retention_days": 365,
        }
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def create_actalike_audience(api, ad_account_id, name, source_audience_id, country):
    """Create actalike (lookalike) audience."""
    url = f"{api.base_url}/ad_accounts/{ad_account_id}/audiences"

    data = {
        "name": name,
        "audience_type": "ACTALIKE",
        "rule": {
            "source_audience_id": source_audience_id,
            "country": country,  # "US", "GB", etc.
            "percentage": 1,  # 1-10%
        }
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()
```

### 4. Pinterest Tag and Conversion Tracking

**Set Up Conversion Tracking:**
```python
def create_conversion_tag(api, ad_account_id, name):
    """Create a Pinterest Tag for conversion tracking."""
    url = f"{api.base_url}/ad_accounts/{ad_account_id}/conversion_tags"

    data = {
        "name": name,
        "aem_enabled": False,  # Advanced matching
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def get_tag_code(api, ad_account_id, tag_id):
    """Get Pinterest Tag code snippet."""
    url = f"{api.base_url}/ad_accounts/{ad_account_id}/conversion_tags/{tag_id}"

    response = requests.get(url, headers=api.headers)
    return response.json()


# Server-side event tracking (Conversions API)
def send_conversion_event(api, ad_account_id, tag_id, event_name, user_data,
                         custom_data):
    """Send server-side conversion event."""
    url = f"{api.base_url}/ad_accounts/{ad_account_id}/events"

    import hashlib
    import time

    data = {
        "conversion_tags": [tag_id],
        "data": [{
            "event_name": event_name,  # page_visit, checkout, add_to_cart, etc.
            "action_source": "web",  # web, app, offline
            "event_time": int(time.time()),
            "event_id": f"event_{int(time.time())}",
            "user_data": {
                "em": [hashlib.sha256(user_data.get('email', '').lower().encode()).hexdigest()],
                "ph": [hashlib.sha256(user_data.get('phone', '').encode()).hexdigest()],
                "client_ip_address": user_data.get('ip'),
                "client_user_agent": user_data.get('user_agent'),
            },
            "custom_data": {
                "value": custom_data.get('value'),
                "currency": custom_data.get('currency', 'USD'),
                "content_ids": custom_data.get('content_ids', []),
                "num_items": custom_data.get('num_items'),
                "order_id": custom_data.get('order_id'),
            }
        }]
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()
```

## Installation and Authentication

### Install Required Libraries

```bash
pip install requests pandas
```

### Set Up Authentication

1. **Create Pinterest Business Account** at https://business.pinterest.com/
2. **Create App** in Pinterest Developers Portal
3. **Get App ID and App Secret**
4. **Generate Access Token** using OAuth 2.0 flow
5. **Get Ad Account ID** from Pinterest Ads Manager

### Initialize API Client

```python
import requests

class PinterestAdsAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.pinterest.com/v5"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

# Initialize
api = PinterestAdsAPI(access_token="YOUR_ACCESS_TOKEN")
```

## Quick Start Example

```python
from datetime import datetime, timedelta

# Initialize API
api = PinterestAdsAPI(access_token="YOUR_ACCESS_TOKEN")
ad_account_id = "549755885175"

# Get campaign performance for last 30 days
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

campaign_ids = ["campaign_id_1", "campaign_id_2"]
df = get_campaign_analytics(api, ad_account_id, campaign_ids, start_date, end_date)

# Display results
print(df[['date', 'impressions', 'clicks', 'spend', 'conversions', 'roas']])
print(f"\nTotal Spend: ${df['spend'].sum():.2f}")
print(f"Total Saves: {df['saves'].sum():,}")
print(f"Average Engagement Rate: {df['engagement_rate'].mean():.2%}")
print(f"Total ROAS: {df['roas'].mean():.2f}")
```

## Key Metrics Reference

### Performance Metrics
- **Impressions** - Number of times pin was shown
- **Clicks** - Total clicks on pin
- **Outbound Clicks** - Clicks to destination URL
- **CTR** - Click-through rate
- **CPC** - Cost per click
- **CPM** - Cost per 1,000 impressions
- **Spend** - Total amount spent

### Engagement Metrics
- **Saves** - Number of pin saves
- **Save Rate** - Saves / Impressions
- **Repins** - Repins to other boards
- **Pin Clicks** - Clicks to close-up view
- **Total Engagement** - All engagement actions
- **Engagement Rate** - Engagements / Impressions

### Conversion Metrics
- **Total Conversions** - All conversion events
- **Conversion Rate** - Conversions / Clicks
- **Cost Per Conversion** - Spend / Conversions
- **Conversion Value** - Total value from conversions
- **ROAS** - Return on ad spend (Value / Spend)

### Video Metrics (for video pins)
- **Video Views** - Number of video views
- **Video MRC Views** - Media Rating Council views (50% visible, 2+ seconds)
- **Video V50 Watch Time** - Time watched at 50% completion
- **Video Starts** - Number of video starts

### Shopping Metrics (for catalog ads)
- **Product Impressions** - Product listing views
- **Product Clicks** - Clicks on products
- **Add to Cart** - Products added to cart
- **Checkouts** - Checkout initiations
- **Purchases** - Completed purchases

## Best Practices

1. **Visual Creative**
   - Use high-quality vertical images (2:3 aspect ratio)
   - Keep text overlay minimal (< 20% of image)
   - Use lifestyle imagery showing products in use
   - Test different pin formats (standard, carousel, video)

2. **Targeting Strategy**
   - Combine interest and keyword targeting
   - Target users actively searching for inspiration
   - Use actalike audiences from converters
   - Test broad match keywords first

3. **Shopping Campaigns**
   - Keep product catalog updated daily
   - Use high-quality product images
   - Include detailed product descriptions
   - Optimize for mobile shopping experience

4. **Bidding and Budget**
   - Start with automatic bidding
   - Monitor average CPC benchmarks by industry
   - Use campaign budget optimization
   - Adjust bids based on time-to-conversion

5. **Creative Refresh**
   - Rotate pins every 4-6 weeks
   - Test seasonal and trending themes
   - Use Pinterest Trends tool for inspiration
   - Leverage user-generated content

## Common Use Cases

### E-commerce Product Promotion
```python
def setup_shopping_campaign(api, ad_account_id, catalog_id):
    """Set up shopping catalog campaign."""
    # Create campaign with CATALOG_SALES objective
    # Set up product groups by category
    # Configure dynamic retargeting
    pass
```

### Brand Awareness
```python
def create_awareness_campaign(api, ad_account_id, video_pins):
    """Create brand awareness campaign with video."""
    # Create campaign with AWARENESS objective
    # Upload video pins
    # Target broad interests
    pass
```

### Seasonal Promotion
```python
def create_seasonal_campaign(api, ad_account_id, holiday, products):
    """Create seasonal shopping campaign."""
    # Create themed pins for holiday
    # Target seasonal keywords
    # Set campaign dates for holiday period
    pass
```

## References

- **Official Documentation**: https://developers.pinterest.com/docs/api/v5/
- **Ads API**: https://developers.pinterest.com/docs/ads/
- **Pinterest Tag**: https://help.pinterest.com/en/business/article/track-conversions-with-pinterest-tag
- **Product Catalogs**: https://help.pinterest.com/en/business/article/catalogs-overview
- **Best Practices**: https://business.pinterest.com/en/inspiration/
- **Creative Specs**: https://help.pinterest.com/en/business/article/creative-best-practices
- **Developer Portal**: https://developers.pinterest.com/
- **Support**: https://help.pinterest.com/en/business

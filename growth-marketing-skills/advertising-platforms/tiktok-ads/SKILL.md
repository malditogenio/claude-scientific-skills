---
name: tiktok-ads
description: "TikTok Ads API for short-form video advertising. Manage campaigns, ad groups, ads, creative, audience targeting, and performance analytics on TikTok and TikTok network."
---

# TikTok Ads

## Overview

TikTok Ads provides access to one of the fastest-growing advertising platforms, reaching billions of users with short-form video content. The TikTok Marketing API enables programmatic campaign management, creative optimization, audience targeting, and comprehensive analytics across TikTok and its advertising network.

This skill covers the TikTok Marketing API with Python, enabling automated campaign creation, video ad management, audience targeting, and performance tracking for the Gen Z and Millennial demographics.

## When to Use This Skill

Use this skill when you need to:
- Create and manage TikTok video ad campaigns programmatically
- Automate creative testing for short-form video content
- Target younger demographics (Gen Z, Millennials)
- Manage campaigns across TikTok, TopBuzz, BuzzVideo, and Pangle
- Generate performance reports and video engagement analytics
- Implement TikTok Pixel for conversion tracking
- Create and manage custom and lookalike audiences
- Optimize for app installs and e-commerce conversions
- Manage TikTok Shopping and product catalogs
- Sync audience data for remarketing
- Monitor trending content and hashtag performance

## Core Capabilities

### 1. Campaign Management

**Create Campaign Structure:**
```python
import requests
import json

class TikTokAdsAPI:
    """TikTok Ads API client."""

    def __init__(self, access_token, advertiser_id):
        self.access_token = access_token
        self.advertiser_id = advertiser_id
        self.base_url = "https://business-api.tiktok.com/open_api/v1.3"

    def _make_request(self, endpoint, method="GET", data=None):
        """Make API request."""
        headers = {
            "Access-Token": self.access_token,
            "Content-Type": "application/json",
        }

        url = f"{self.base_url}/{endpoint}/"

        if method == "GET":
            response = requests.get(url, headers=headers, params=data)
        else:
            response = requests.post(url, headers=headers, json=data)

        return response.json()

    def create_campaign(self, campaign_name, budget, budget_mode="BUDGET_MODE_DAY"):
        """Create a new campaign."""
        data = {
            "advertiser_id": self.advertiser_id,
            "campaign_name": campaign_name,
            "objective_type": "CONVERSIONS",  # REACH, TRAFFIC, CONVERSIONS, APP_INSTALL
            "budget": budget,  # In cents
            "budget_mode": budget_mode,  # BUDGET_MODE_DAY, BUDGET_MODE_TOTAL
        }

        return self._make_request("campaign/create", method="POST", data=data)

    def create_ad_group(self, campaign_id, ad_group_name, budget, targeting):
        """Create an ad group with targeting."""
        data = {
            "advertiser_id": self.advertiser_id,
            "campaign_id": campaign_id,
            "ad_group_name": ad_group_name,
            "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
            "placements": ["PLACEMENT_TIKTOK", "PLACEMENT_PANGLE"],
            "budget": budget,
            "budget_mode": "BUDGET_MODE_DAY",
            "schedule_type": "SCHEDULE_START_END",
            "schedule_start_time": "2024-01-01 00:00:00",
            "schedule_end_time": "2024-12-31 23:59:59",
            "optimization_goal": "CONVERT",  # CLICK, CONVERT, REACH, INSTALL
            "billing_event": "CPC",  # CPC, CPM, CPV, OCPC, OCPM
            "bid_type": "BID_TYPE_CUSTOM",
            "bid": 100,  # In cents
            "conversion_id": "YOUR_PIXEL_CONVERSION_ID",
            "targeting": targeting,
        }

        return self._make_request("adgroup/create", method="POST", data=data)

    def build_targeting(self, locations=None, age_groups=None, gender=None, interests=None):
        """Build targeting specification."""
        targeting = {}

        if locations:
            targeting["location_ids"] = locations  # Country/region IDs

        if age_groups:
            targeting["age_groups"] = age_groups  # ["AGE_13_17", "AGE_18_24", "AGE_25_34"]

        if gender:
            targeting["gender"] = gender  # "MALE", "FEMALE", "UNLIMITED"

        if interests:
            targeting["interest_category_ids"] = interests  # Interest category IDs

        # Operating system targeting
        targeting["operating_systems"] = ["ANDROID", "IOS"]

        return targeting


# Example usage
api = TikTokAdsAPI(
    access_token="YOUR_ACCESS_TOKEN",
    advertiser_id="YOUR_ADVERTISER_ID"
)

# Create campaign
campaign = api.create_campaign(
    campaign_name="Summer Campaign 2024",
    budget=5000,  # $50/day
)

# Create ad group with targeting
targeting = api.build_targeting(
    locations=["6252001"],  # US location ID
    age_groups=["AGE_18_24", "AGE_25_34"],
    gender="UNLIMITED",
    interests=["100123", "100456"]  # Interest category IDs
)

ad_group = api.create_ad_group(
    campaign_id=campaign['data']['campaign_id'],
    ad_group_name="Video Ad Group 1",
    budget=2000,  # $20/day
    targeting=targeting
)
```

**Upload Video and Create Ads:**
```python
def upload_video(api, video_path):
    """Upload video creative."""
    # Step 1: Get upload URL
    init_data = {
        "advertiser_id": api.advertiser_id,
        "upload_type": "UPLOAD_BY_FILE",
        "file_name": video_path.split('/')[-1],
    }

    init_response = api._make_request("file/video/ad/init", method="POST", data=init_data)
    upload_url = init_response['data']['upload_url']
    video_id = init_response['data']['video_id']

    # Step 2: Upload video file
    with open(video_path, 'rb') as video_file:
        files = {'video': video_file}
        response = requests.post(upload_url, files=files)

    return video_id


def create_video_ad(api, ad_group_id, video_id, ad_text, landing_page_url):
    """Create a video ad."""
    data = {
        "advertiser_id": api.advertiser_id,
        "ad_group_id": ad_group_id,
        "ad_name": "Video Ad 1",
        "ad_format": "SINGLE_VIDEO",
        "ad_text": ad_text,
        "call_to_action": "SHOP_NOW",  # LEARN_MORE, SHOP_NOW, SIGN_UP, DOWNLOAD
        "landing_page_url": landing_page_url,
        "display_name": "Brand Name",
        "video_id": video_id,
        "tracking_pixel_id": "YOUR_PIXEL_ID",
    }

    return api._make_request("ad/create", method="POST", data=data)


# Spark Ads (using existing TikTok posts)
def create_spark_ad(api, ad_group_id, tiktok_item_id):
    """Create a Spark Ad from existing TikTok post."""
    data = {
        "advertiser_id": api.advertiser_id,
        "ad_group_id": ad_group_id,
        "ad_name": "Spark Ad 1",
        "identity_type": "CUSTOMIZED_USER",
        "identity_id": "YOUR_TIKTOK_ACCOUNT_ID",
        "item_id": tiktok_item_id,  # TikTok post ID
        "call_to_action": "SHOP_NOW",
        "landing_page_url": "https://example.com/product",
    }

    return api._make_request("ad/create", method="POST", data=data)
```

### 2. Reporting and Analytics

**Campaign Performance Reports:**
```python
import pandas as pd
from datetime import datetime, timedelta

def get_campaign_report(api, start_date, end_date, dimensions=None):
    """Get campaign performance report."""
    data = {
        "advertiser_id": api.advertiser_id,
        "service_type": "AUCTION",
        "report_type": "BASIC",
        "data_level": "AUCTION_CAMPAIGN",
        "dimensions": dimensions or ["campaign_id", "stat_time_day"],
        "metrics": [
            "spend",
            "impressions",
            "clicks",
            "ctr",
            "cpc",
            "cpm",
            "conversion",
            "cost_per_conversion",
            "conversion_rate",
            "video_play_actions",
            "video_watched_2s",
            "video_watched_6s",
            "average_video_play",
            "average_video_play_per_user",
        ],
        "start_date": start_date,  # "2024-01-01"
        "end_date": end_date,  # "2024-01-31"
    }

    response = api._make_request("report/integrated/get", method="GET", data=data)

    if response['code'] == 0:
        df = pd.DataFrame(response['data']['list'])
        return df
    else:
        raise Exception(f"API Error: {response['message']}")


def get_ad_group_report(api, start_date, end_date):
    """Get ad group performance report."""
    data = {
        "advertiser_id": api.advertiser_id,
        "service_type": "AUCTION",
        "report_type": "BASIC",
        "data_level": "AUCTION_ADGROUP",
        "dimensions": ["adgroup_id", "stat_time_day"],
        "metrics": [
            "spend",
            "impressions",
            "clicks",
            "ctr",
            "conversion",
            "cost_per_conversion",
            "real_time_conversion",
            "real_time_cost_per_conversion",
        ],
        "start_date": start_date,
        "end_date": end_date,
    }

    response = api._make_request("report/integrated/get", method="GET", data=data)
    return pd.DataFrame(response['data']['list'])


def get_video_performance(api, start_date, end_date):
    """Get video creative performance."""
    data = {
        "advertiser_id": api.advertiser_id,
        "service_type": "AUCTION",
        "report_type": "BASIC",
        "data_level": "AUCTION_AD",
        "dimensions": ["ad_id", "stat_time_day"],
        "metrics": [
            "spend",
            "impressions",
            "clicks",
            "video_play_actions",
            "video_watched_2s",
            "video_watched_6s",
            "video_views_p25",
            "video_views_p50",
            "video_views_p75",
            "video_views_p100",
            "average_video_play",
            "engagement_rate",
            "follows",
            "likes",
            "comments",
            "shares",
        ],
        "start_date": start_date,
        "end_date": end_date,
    }

    response = api._make_request("report/integrated/get", method="GET", data=data)
    return pd.DataFrame(response['data']['list'])


def get_audience_breakdown(api, start_date, end_date, breakdown_dimension="age"):
    """Get performance by audience demographics."""
    data = {
        "advertiser_id": api.advertiser_id,
        "service_type": "AUCTION",
        "report_type": "AUDIENCE",
        "data_level": "AUCTION_CAMPAIGN",
        "dimensions": [breakdown_dimension],  # age, gender, location, platform
        "metrics": [
            "spend",
            "impressions",
            "clicks",
            "ctr",
            "conversion",
        ],
        "start_date": start_date,
        "end_date": end_date,
    }

    response = api._make_request("report/integrated/get", method="GET", data=data)
    return pd.DataFrame(response['data']['list'])
```

### 3. Audience Management

**Custom Audiences:**
```python
def create_custom_audience(api, audience_name, audience_type="CUSTOMER_FILE"):
    """Create a custom audience."""
    data = {
        "advertiser_id": api.advertiser_id,
        "custom_audience_name": audience_name,
        "custom_audience_type": audience_type,  # CUSTOMER_FILE, ENGAGEMENT, WEBSITE
        "retention_days": 180,
    }

    return api._make_request("dmp/custom_audience/create", method="POST", data=data)


def upload_audience_data(api, custom_audience_id, emails=None, phone_numbers=None):
    """Upload customer data to custom audience."""
    import hashlib

    # Hash data with SHA256
    hashed_data = []

    if emails:
        for email in emails:
            hashed_email = hashlib.sha256(email.lower().strip().encode()).hexdigest()
            hashed_data.append({
                "id_type": "EMAIL_SHA256",
                "id": hashed_email,
            })

    if phone_numbers:
        for phone in phone_numbers:
            hashed_phone = hashlib.sha256(phone.strip().encode()).hexdigest()
            hashed_data.append({
                "id_type": "PHONE_SHA256",
                "id": hashed_phone,
            })

    data = {
        "advertiser_id": api.advertiser_id,
        "custom_audience_id": custom_audience_id,
        "user_data": hashed_data,
    }

    return api._make_request("dmp/custom_audience/update", method="POST", data=data)


def create_lookalike_audience(api, custom_audience_id, lookalike_name, location_ids):
    """Create a lookalike audience."""
    data = {
        "advertiser_id": api.advertiser_id,
        "lookalike_name": lookalike_name,
        "custom_audience_id": custom_audience_id,
        "location_ids": location_ids,  # Target location IDs
        "lookalike_type": "SIMILARITY",  # SIMILARITY, REACH, BALANCE
    }

    return api._make_request("dmp/lookalike/create", method="POST", data=data)


def create_website_audience(api, audience_name, pixel_id, retention_days=180):
    """Create website traffic custom audience."""
    data = {
        "advertiser_id": api.advertiser_id,
        "custom_audience_name": audience_name,
        "custom_audience_type": "WEBSITE",
        "pixel_id": pixel_id,
        "retention_days": retention_days,
        "rules": [
            {
                "url_contains": "product",
                "event_type": "PageView",
            }
        ],
    }

    return api._make_request("dmp/custom_audience/create", method="POST", data=data)
```

### 4. TikTok Pixel and Conversion Tracking

**TikTok Pixel Events:**
```python
def create_pixel(api, pixel_name):
    """Create a TikTok Pixel."""
    data = {
        "advertiser_id": api.advertiser_id,
        "pixel_name": pixel_name,
    }

    return api._make_request("pixel/create", method="POST", data=data)


# Server-side event tracking
def send_pixel_event(api, pixel_code, event_name, event_data):
    """Send server-side pixel event."""
    import time

    data = {
        "pixel_code": pixel_code,
        "event": event_name,  # ViewContent, AddToCart, InitiateCheckout, CompletePayment
        "timestamp": int(time.time()),
        "context": {
            "user_agent": event_data.get('user_agent'),
            "ip": event_data.get('ip_address'),
        },
        "properties": {
            "content_type": event_data.get('content_type'),
            "content_id": event_data.get('content_id'),
            "value": event_data.get('value'),
            "currency": event_data.get('currency', 'USD'),
        },
    }

    # Add user identifiers
    if 'email' in event_data:
        import hashlib
        data['context']['email'] = hashlib.sha256(
            event_data['email'].lower().strip().encode()
        ).hexdigest()

    return api._make_request("pixel/track", method="POST", data=data)
```

## Installation and Authentication

### Install Required Libraries

```bash
pip install requests pandas
```

### Set Up Authentication

1. **Create TikTok Business Account** at https://business.tiktok.com/
2. **Create App** in TikTok for Business Developer Portal
3. **Generate Access Token** using OAuth 2.0 flow
4. **Get Advertiser ID** from TikTok Ads Manager

### Initialize API Client

```python
import requests

class TikTokAdsAPI:
    def __init__(self, access_token, advertiser_id):
        self.access_token = access_token
        self.advertiser_id = advertiser_id
        self.base_url = "https://business-api.tiktok.com/open_api/v1.3"

    def _make_request(self, endpoint, method="GET", data=None):
        headers = {
            "Access-Token": self.access_token,
            "Content-Type": "application/json",
        }
        url = f"{self.base_url}/{endpoint}/"

        if method == "GET":
            response = requests.get(url, headers=headers, params=data)
        else:
            response = requests.post(url, headers=headers, json=data)

        return response.json()

# Initialize
api = TikTokAdsAPI(
    access_token="YOUR_ACCESS_TOKEN",
    advertiser_id="YOUR_ADVERTISER_ID"
)
```

## Quick Start Example

```python
from datetime import datetime, timedelta

# Initialize API
api = TikTokAdsAPI(
    access_token="YOUR_ACCESS_TOKEN",
    advertiser_id="YOUR_ADVERTISER_ID"
)

# Get campaign performance for last 7 days
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

report = get_campaign_report(api, start_date, end_date)

# Display results
for _, row in report.iterrows():
    print(f"Campaign: {row.get('campaign_name', 'N/A')}")
    print(f"  Spend: ${float(row.get('spend', 0)):.2f}")
    print(f"  Impressions: {int(row.get('impressions', 0)):,}")
    print(f"  Clicks: {int(row.get('clicks', 0)):,}")
    print(f"  CTR: {float(row.get('ctr', 0)):.2%}")
    print(f"  Conversions: {int(row.get('conversion', 0))}")
    print()
```

## Key Metrics Reference

### Performance Metrics
- **Spend** - Total amount spent
- **Impressions** - Number of ad views
- **Clicks** - Number of clicks
- **CTR** - Click-through rate
- **CPC** - Cost per click
- **CPM** - Cost per 1,000 impressions
- **Reach** - Unique users reached
- **Frequency** - Average impressions per user

### Conversion Metrics
- **Conversion** - Total conversions
- **Cost Per Conversion** - Average cost per conversion
- **Conversion Rate** - Conversions / Clicks
- **Real-Time Conversion** - Conversions in real-time window
- **Value Per Conversion** - Average conversion value

### Video Engagement Metrics
- **Video Play Actions** - Number of video plays
- **Video Watched 2s** - 2-second views
- **Video Watched 6s** - 6-second views
- **Video Views P25/P50/P75/P100** - % completion milestones
- **Average Video Play** - Average watch time
- **Average Video Play Per User** - Average watch time per unique user

### Engagement Metrics
- **Likes** - Number of likes
- **Comments** - Number of comments
- **Shares** - Number of shares
- **Follows** - New followers
- **Engagement Rate** - (Likes + Comments + Shares) / Impressions
- **Profile Visits** - Visits to advertiser profile

## Best Practices

1. **Video Creative Guidelines**
   - Keep videos 9-15 seconds for optimal performance
   - Use vertical format (9:16) for TikTok feed
   - Add captions for sound-off viewing
   - Include hook in first 2 seconds

2. **Targeting Strategy**
   - Start with automatic placement for reach
   - Use age targeting (18-24, 25-34 perform best)
   - Test interest-based and behavioral targeting
   - Create lookalike audiences from converters

3. **Bidding Optimization**
   - Start with automatic bidding
   - Switch to manual bidding after collecting data
   - Use lowest cost bid strategy for conversions
   - Monitor frequency to avoid ad fatigue

4. **Creative Testing**
   - Test 3-5 different video creatives per ad group
   - Use Spark Ads to leverage organic content
   - Refresh creatives every 2-3 weeks
   - Test different CTAs and landing pages

5. **Performance Monitoring**
   - Monitor video completion rates
   - Track engagement metrics (likes, shares, comments)
   - Optimize for 6-second views minimum
   - Use TikTok Pixel for accurate attribution

## Common Use Cases

### App Install Campaigns
```python
def create_app_install_campaign(api, app_id, app_download_url):
    """Create campaign optimized for app installs."""
    # Create campaign with APP_INSTALL objective
    # Set up deep linking
    # Configure app event optimization
    pass
```

### E-commerce Product Ads
```python
def setup_product_catalog_ads(api, catalog_id):
    """Set up dynamic product ads from catalog."""
    # Create product catalog audience
    # Set up dynamic video templates
    # Configure product sets
    pass
```

### Lead Generation
```python
def create_lead_gen_campaign(api, instant_form_id):
    """Create lead generation campaign with instant forms."""
    # Create campaign with LEAD_GENERATION objective
    # Configure instant form
    # Set up lead delivery webhooks
    pass
```

## References

- **Official Documentation**: https://business-api.tiktok.com/portal/docs
- **Marketing API**: https://ads.tiktok.com/marketing_api/docs
- **TikTok Pixel**: https://ads.tiktok.com/help/article?aid=10000357
- **Creative Best Practices**: https://www.tiktok.com/business/en/blog/creative-best-practices
- **Targeting Options**: https://ads.tiktok.com/help/article?aid=9616
- **API Rate Limits**: https://business-api.tiktok.com/portal/docs?id=1739939120946177
- **Developer Portal**: https://developers.tiktok.com/
- **Support**: https://ads.tiktok.com/help/

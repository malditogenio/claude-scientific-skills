---
name: snapchat-ads
description: "Snapchat Ads API for AR and mobile advertising. Manage snap ads, story ads, AR lenses, filters, audience targeting, and analytics for Gen Z and Millennial engagement."
---

# Snapchat Ads

## Overview

Snapchat Ads provides access to a platform reaching over 400 million daily active users, primarily Gen Z and Millennials. The Snapchat Marketing API enables programmatic campaign management, AR lens creation, story ads, and comprehensive analytics for mobile-first and immersive advertising experiences.

This skill covers the Snapchat Marketing API with Python, enabling automated campaign creation, AR advertising, audience targeting, and performance tracking for engagement-focused campaigns.

## When to Use This Skill

Use this skill when you need to:
- Create and manage Snapchat advertising campaigns programmatically
- Target Gen Z and Millennial audiences
- Leverage AR lenses and filters for brand engagement
- Create immersive full-screen mobile ad experiences
- Manage Story Ads and Collection Ads
- Generate performance reports and engagement analytics
- Implement app install and e-commerce campaigns
- Create and manage custom audiences for remarketing
- Optimize for swipe-up actions and engagement
- Track Snap Pixel conversions
- Monitor AR lens usage and engagement

## Core Capabilities

### 1. Campaign Management

**Create Campaign Structure:**
```python
import requests
import json

class SnapchatAdsAPI:
    """Snapchat Ads API client."""

    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://adsapi.snapchat.com/v1"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def create_campaign(self, ad_account_id, name, objective, daily_budget_micro=None,
                       lifetime_budget_micro=None, start_time=None, end_time=None):
        """Create a new campaign."""
        url = f"{self.base_url}/adaccounts/{ad_account_id}/campaigns"

        data = {
            "campaigns": [{
                "name": name,
                "ad_account_id": ad_account_id,
                "status": "PAUSED",
                "objective": objective,
                # AWARENESS, APP_INSTALLS, DRIVE_TRAFFIC, ENGAGEMENT,
                # VIDEO_VIEWS, LEAD_GENERATION, SALES
                "daily_budget_micro": daily_budget_micro,
                "lifetime_budget_micro": lifetime_budget_micro,
                "start_time": start_time,
                "end_time": end_time,
            }]
        }

        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def create_ad_squad(self, ad_account_id, campaign_id, name, type_field,
                       placement_v2, targeting, bid_micro, optimization_goal):
        """Create an ad squad (ad set)."""
        url = f"{self.base_url}/adaccounts/{ad_account_id}/adsquads"

        data = {
            "adsquads": [{
                "name": name,
                "campaign_id": campaign_id,
                "type": type_field,  # SNAP_ADS, STORY_ADS, AR_LENS, COLLECTION_ADS
                "status": "PAUSED",
                "placement_v2": placement_v2,
                # CONTENT: User-generated content
                # FEED: Main feed
                "targeting": targeting,
                "optimization_goal": optimization_goal,
                # IMPRESSIONS, SWIPES, APP_INSTALLS, PIXEL_PURCHASE, etc.
                "bid_micro": bid_micro,
                "billing_event": "IMPRESSION",  # IMPRESSION, SWIPE
                "auto_bid": False,
            }]
        }

        response = requests.post(url, headers=self.headers, json=data)
        return response.json()


def build_targeting(demographics=None, locations=None, devices=None,
                   interests=None, snapchat_audience_segments=None):
    """Build targeting specification."""
    targeting = {}

    # Demographics
    if demographics:
        targeting["demographics"] = []
        if "age_groups" in demographics:
            targeting["demographics"].append({
                "age_groups": demographics["age_groups"]
                # ["13-17", "18-24", "25-34", "35-54", "55+"]
            })
        if "gender" in demographics:
            targeting["demographics"].append({
                "genders": demographics["gender"]  # ["MALE", "FEMALE"]
            })
        if "languages" in demographics:
            targeting["demographics"].append({
                "languages": demographics["languages"]  # ["en", "es", etc.]
            })

    # Location targeting
    if locations:
        targeting["geos"] = [{
            "country_code": loc["country"],
            "region": loc.get("region"),
            "metro": loc.get("metro"),
        } for loc in locations]

    # Device targeting
    if devices:
        targeting["devices"] = {
            "os_types": devices.get("os_types", ["IOS", "ANDROID"]),
            "connection_types": devices.get("connection_types", ["WIFI", "CELL"]),
        }

    # Interest targeting
    if interests:
        targeting["interests"] = interests  # List of interest category IDs

    # Custom audience targeting
    if snapchat_audience_segments:
        targeting["snapchat_audience_segments"] = snapchat_audience_segments

    return targeting


def create_snap_ad(api, ad_account_id, ad_squad_id, name, creative_id,
                  shareable=True, render_type="STATIC"):
    """Create a Snap Ad."""
    url = f"{api.base_url}/adaccounts/{ad_account_id}/ads"

    data = {
        "ads": [{
            "name": name,
            "ad_squad_id": ad_squad_id,
            "creative_id": creative_id,
            "status": "PAUSED",
            "type": "SNAP_AD",
            "shareable": shareable,
            "render_type": render_type,  # STATIC, ADVANCED
        }]
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


# Upload creative
def upload_creative(api, ad_account_id, name, brand_name, headline, call_to_action,
                   top_snap_media_id, shareable=True):
    """Create ad creative."""
    url = f"{api.base_url}/adaccounts/{ad_account_id}/creatives"

    data = {
        "creatives": [{
            "name": name,
            "ad_account_id": ad_account_id,
            "type": "SNAP_AD",
            "brand_name": brand_name,
            "headline": headline,
            "call_to_action": call_to_action,
            # SWIPE_UP, WATCH, INSTALL, SHOP, SIGN_UP, etc.
            "shareable": shareable,
            "top_snap_media_id": top_snap_media_id,
        }]
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def upload_media(api, ad_account_id, media_path, media_type="IMAGE"):
    """Upload media (image or video)."""
    url = f"{api.base_url}/adaccounts/{ad_account_id}/media"

    with open(media_path, 'rb') as media_file:
        files = {
            'file': media_file
        }
        data = {
            "media_type": media_type,  # IMAGE, VIDEO
        }

        # Remove Content-Type header for multipart upload
        headers = {
            "Authorization": api.headers["Authorization"]
        }

        response = requests.post(url, headers=headers, files=files, data=data)
        return response.json()
```

**Story Ads and Collection Ads:**
```python
def create_story_ad(api, ad_account_id, ad_squad_id, name, story_creative_id):
    """Create a Story Ad."""
    url = f"{api.base_url}/adaccounts/{ad_account_id}/ads"

    data = {
        "ads": [{
            "name": name,
            "ad_squad_id": ad_squad_id,
            "creative_id": story_creative_id,
            "status": "PAUSED",
            "type": "STORY_AD",
        }]
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def create_collection_ad(api, ad_account_id, ad_squad_id, name, catalog_id,
                        collection_creative):
    """Create a Collection Ad (shopping ad)."""
    url = f"{api.base_url}/adaccounts/{ad_account_id}/ads"

    data = {
        "ads": [{
            "name": name,
            "ad_squad_id": ad_squad_id,
            "creative_id": collection_creative["creative_id"],
            "status": "PAUSED",
            "type": "COLLECTION_AD",
            "catalog_product_set_id": catalog_id,
        }]
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()
```

### 2. Reporting and Analytics

**Campaign Performance Reports:**
```python
import pandas as pd
from datetime import datetime, timedelta

def get_campaign_stats(api, ad_account_id, campaign_ids, start_time, end_time,
                      granularity="DAY"):
    """Get campaign performance statistics."""
    url = f"{api.base_url}/adaccounts/{ad_account_id}/campaigns/stats"

    params = {
        "ids": ",".join(campaign_ids),
        "granularity": granularity,  # HOUR, DAY, LIFETIME
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "fields": (
            "impressions,swipes,spend,quartile_1,quartile_2,quartile_3,"
            "view_completion,video_views,screen_time_millis,conversion_purchases,"
            "conversion_purchases_value,total_installs,android_installs,ios_installs,"
            "swipe_up_percent,attachment_total_view_time_millis"
        ),
    }

    response = requests.get(url, headers=api.headers, params=params)
    data = response.json()

    results = []
    for campaign in data.get("campaigns", []):
        for stat in campaign.get("stats", []):
            results.append({
                'campaign_id': campaign.get('id'),
                'date': stat.get('start_time'),
                'impressions': int(stat.get('impressions', 0)),
                'swipes': int(stat.get('swipes', 0)),
                'spend': float(stat.get('spend', 0)) / 1_000_000,  # Convert from micro
                'video_views': int(stat.get('video_views', 0)),
                'view_completion': float(stat.get('view_completion', 0)),
                'screen_time_millis': int(stat.get('screen_time_millis', 0)),
                'purchases': int(stat.get('conversion_purchases', 0)),
                'purchase_value': float(stat.get('conversion_purchases_value', 0)),
                'app_installs': int(stat.get('total_installs', 0)),
            })

    df = pd.DataFrame(results)

    # Calculate derived metrics
    if not df.empty:
        df['swipe_rate'] = df['swipes'] / df['impressions'].replace(0, 1)
        df['cost_per_swipe'] = df['spend'] / df['swipes'].replace(0, 1)
        df['cpm'] = (df['spend'] / df['impressions'].replace(0, 1)) * 1000

    return df


def get_ad_squad_stats(api, ad_account_id, ad_squad_ids, start_time, end_time):
    """Get ad squad (ad set) performance."""
    url = f"{api.base_url}/adaccounts/{ad_account_id}/adsquads/stats"

    params = {
        "ids": ",".join(ad_squad_ids),
        "granularity": "DAY",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }

    response = requests.get(url, headers=api.headers, params=params)
    return response.json()


def get_creative_stats(api, ad_account_id, creative_ids, start_time, end_time):
    """Get creative performance statistics."""
    url = f"{api.base_url}/adaccounts/{ad_account_id}/creatives/stats"

    params = {
        "ids": ",".join(creative_ids),
        "granularity": "LIFETIME",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "fields": "impressions,swipes,spend,video_views,shares,saves,view_completion",
    }

    response = requests.get(url, headers=api.headers, params=params)
    return response.json()
```

### 3. Audience Management

**Custom Audiences:**
```python
def create_segment_audience(api, ad_account_id, name, description, retention_days=180):
    """Create a custom audience segment."""
    url = f"{api.base_url}/adaccounts/{ad_account_id}/segments"

    data = {
        "segments": [{
            "name": name,
            "description": description,
            "ad_account_id": ad_account_id,
            "source_type": "FIRST_PARTY",
            "retention_in_days": retention_days,
            "status": "ACTIVE",
        }]
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def upload_user_emails(api, segment_id, emails):
    """Upload email list to audience segment."""
    url = f"{api.base_url}/segments/{segment_id}/users"

    import hashlib

    # Hash emails with SHA256
    hashed_emails = []
    for email in emails:
        hashed = hashlib.sha256(email.lower().strip().encode()).hexdigest()
        hashed_emails.append({
            "schema": ["EMAIL_SHA256"],
            "data": [[hashed]]
        })

    data = {
        "users": hashed_emails
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def create_lookalike_audience(api, ad_account_id, name, source_segment_id,
                              country_code, similarity=0.01):
    """Create a lookalike audience (SAM - Snapchat Audience Match)."""
    url = f"{api.base_url}/adaccounts/{ad_account_id}/segments"

    data = {
        "segments": [{
            "name": name,
            "ad_account_id": ad_account_id,
            "source_type": "LOOKALIKE",
            "seed_segment_id": source_segment_id,
            "country_code": country_code,
            "similarity": similarity,  # 0.01 to 0.10 (1% to 10%)
            "status": "ACTIVE",
        }]
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def create_pixel_audience(api, ad_account_id, name, pixel_id, event_type, retention_days=180):
    """Create audience from Snap Pixel events."""
    url = f"{api.base_url}/adaccounts/{ad_account_id}/segments"

    data = {
        "segments": [{
            "name": name,
            "ad_account_id": ad_account_id,
            "source_type": "PIXEL",
            "pixel_id": pixel_id,
            "event_type": event_type,  # PAGE_VIEW, PURCHASE, ADD_CART, etc.
            "retention_in_days": retention_days,
            "status": "ACTIVE",
        }]
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()
```

### 4. Snap Pixel and Conversion Tracking

**Set Up Conversion Tracking:**
```python
def create_pixel(api, ad_account_id, name):
    """Create a Snap Pixel."""
    url = f"{api.base_url}/adaccounts/{ad_account_id}/pixels"

    data = {
        "pixels": [{
            "name": name,
            "ad_account_id": ad_account_id,
        }]
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def get_pixel_code(api, pixel_id):
    """Get Snap Pixel code snippet."""
    url = f"{api.base_url}/pixels/{pixel_id}"

    response = requests.get(url, headers=api.headers)
    return response.json()


# Conversions API (Server-side tracking)
def send_conversion_event(api, pixel_id, event_type, user_data, custom_data):
    """Send server-side conversion event via Conversions API."""
    url = f"{api.base_url}/pixels/{pixel_id}/events"

    import hashlib
    import time

    event_data = {
        "pixel_id": pixel_id,
        "event_conversion_type": event_type,
        # PAGE_VIEW, PURCHASE, ADD_CART, SIGN_UP, etc.
        "event_tag": "standard",
        "timestamp": int(time.time() * 1000),  # Milliseconds
        "hashed_email": hashlib.sha256(
            user_data.get('email', '').lower().strip().encode()
        ).hexdigest(),
        "hashed_phone_number": hashlib.sha256(
            user_data.get('phone', '').strip().encode()
        ).hexdigest(),
        "hashed_ip_address": hashlib.sha256(
            user_data.get('ip', '').encode()
        ).hexdigest(),
        "user_agent": user_data.get('user_agent'),
        "price": custom_data.get('value'),
        "currency": custom_data.get('currency', 'USD'),
        "transaction_id": custom_data.get('transaction_id'),
        "item_ids": custom_data.get('item_ids', []),
        "number_items": custom_data.get('number_items'),
    }

    data = {"data": [event_data]}

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()
```

## Installation and Authentication

### Install Required Libraries

```bash
pip install requests pandas
```

### Set Up Authentication

1. **Create Snapchat Business Account** at https://business.snapchat.com/
2. **Create App** in Snapchat Marketing API
3. **Get Client ID and Client Secret**
4. **Generate Access Token** using OAuth 2.0 flow
5. **Get Ad Account ID** from Snapchat Ads Manager

### Initialize API Client

```python
import requests

class SnapchatAdsAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://adsapi.snapchat.com/v1"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

# Initialize
api = SnapchatAdsAPI(access_token="YOUR_ACCESS_TOKEN")
```

## Quick Start Example

```python
from datetime import datetime, timedelta

# Initialize API
api = SnapchatAdsAPI(access_token="YOUR_ACCESS_TOKEN")
ad_account_id = "your-ad-account-id"

# Get campaign stats for last 7 days
end_time = datetime.utcnow()
start_time = end_time - timedelta(days=7)

campaign_ids = ["campaign_id_1", "campaign_id_2"]
df = get_campaign_stats(api, ad_account_id, campaign_ids, start_time, end_time)

# Display results
print(df[['date', 'impressions', 'swipes', 'spend', 'video_views']])
print(f"\nTotal Spend: ${df['spend'].sum():.2f}")
print(f"Total Swipes: {df['swipes'].sum():,}")
print(f"Average Swipe Rate: {df['swipe_rate'].mean():.2%}")
```

## Key Metrics Reference

### Performance Metrics
- **Impressions** - Number of times ad was shown
- **Swipes** - Swipe-up actions on ads
- **Swipe Rate** - Swipes / Impressions
- **Spend** - Total amount spent
- **Cost Per Swipe** - Spend / Swipes
- **CPM** - Cost per 1,000 impressions
- **Frequency** - Average impressions per user

### Engagement Metrics
- **Screen Time** - Total time ad was viewed (milliseconds)
- **Attachment View Time** - Time spent viewing attachments
- **Shares** - Number of shares
- **Saves** - Number of saves to camera roll
- **Story Opens** - Opens of Story Ads
- **Story Completions** - Full Story Ad completions

### Video Metrics
- **Video Views** - Total video views (2+ seconds)
- **Quartile 1** - 25% video completion
- **Quartile 2** - 50% video completion
- **Quartile 3** - 75% video completion
- **View Completion** - 100% video completion
- **View Completion Rate** - Completions / Views

### Conversion Metrics
- **Purchases** - Purchase conversions
- **Purchase Value** - Total purchase value
- **App Installs** - Total app installs
- **Android Installs** - Android app installs
- **iOS Installs** - iOS app installs
- **Add to Cart** - Add to cart events
- **Sign Ups** - Registration completions

### AR Lens Metrics
- **Plays** - Number of lens uses
- **Play Time** - Total lens engagement time
- **Shares** - Lens shares to friends
- **Screenshots** - Screenshots taken with lens

## Best Practices

1. **Creative Strategy**
   - Use vertical full-screen format (9:16)
   - Keep videos 3-5 seconds for optimal completion
   - Add sound - 60% of Snapchatters watch with sound on
   - Include branding in first frame

2. **Targeting Strategy**
   - Target 13-34 age range for best reach
   - Use Snap Pixel for behavior-based targeting
   - Create lookalikes from converters
   - Test interest-based targeting

3. **Bidding and Budget**
   - Start with auto-bidding
   - Minimum daily budget: $5/day
   - Use goal-based bidding for conversions
   - Monitor swipe-up costs

4. **AR Lens Strategy**
   - Make lenses fun and shareable
   - Include branded elements naturally
   - Test different AR effects
   - Promote lenses with Snap Ads

5. **Performance Optimization**
   - Refresh creative every 2 weeks
   - Monitor screen time metrics
   - Optimize for swipe-up actions
   - Test different CTAs

## Common Use Cases

### App Install Campaign
```python
def create_app_install_campaign(api, ad_account_id, app_id, app_name):
    """Create campaign optimized for app installs."""
    # Create campaign with APP_INSTALLS objective
    # Configure deep linking
    # Set up app event optimization
    pass
```

### E-commerce Collection Ads
```python
def setup_collection_ads(api, ad_account_id, catalog_id):
    """Set up collection ads for shopping."""
    # Create catalog-based campaign
    # Set up product sets
    # Configure dynamic product ads
    pass
```

### AR Lens Campaign
```python
def create_ar_lens_campaign(api, ad_account_id, lens_id):
    """Create AR lens promotion campaign."""
    # Create campaign with lens objective
    # Set up lens promotion
    # Track lens engagement
    pass
```

## References

- **Official Documentation**: https://marketingapi.snapchat.com/docs/
- **Marketing API**: https://developers.snap.com/api/marketing-api/
- **Snap Pixel**: https://businesshelp.snapchat.com/s/article/pixel-website-install
- **Conversions API**: https://marketingapi.snapchat.com/docs/#conversions-api
- **Creative Specs**: https://forbusiness.snapchat.com/advertising/creative-tools
- **AR Lens Studio**: https://ar.snap.com/lens-studio
- **Best Practices**: https://forbusiness.snapchat.com/inspiration
- **Developer Portal**: https://kit.snapchat.com/
- **Support**: https://businesshelp.snapchat.com/

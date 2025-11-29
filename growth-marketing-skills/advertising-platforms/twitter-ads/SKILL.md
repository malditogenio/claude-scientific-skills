---
name: twitter-ads
description: "Twitter/X Ads API for social advertising. Manage promoted tweets, campaigns, targeting, analytics, and real-time engagement on X platform (formerly Twitter)."
---

# Twitter/X Ads

## Overview

Twitter/X Ads (formerly Twitter Ads) provides advertising on one of the world's largest real-time conversation platforms. The Ads API enables programmatic campaign management, audience targeting, real-time analytics, and engagement tracking for brands looking to participate in trending conversations and cultural moments.

This skill covers the Twitter/X Ads API with Python, enabling automated campaign creation, promoted tweet management, audience targeting, and performance analytics for real-time marketing.

## When to Use This Skill

Use this skill when you need to:
- Create and manage Twitter/X advertising campaigns programmatically
- Promote tweets and trends to targeted audiences
- Leverage real-time events and trending topics
- Target audiences by interests, keywords, and followers
- Generate performance reports and engagement analytics
- Manage large-scale tweet promotion across multiple accounts
- Implement conversion tracking for website events
- Create and manage tailored audiences for remarketing
- Monitor campaign performance in real-time
- Engage with users during live events and cultural moments
- Track brand mentions and competitor activity

## Core Capabilities

### 1. Campaign Management

**Create Campaign Structure:**
```python
import requests
import json
from requests_oauthlib import OAuth1

class TwitterAdsAPI:
    """Twitter/X Ads API client."""

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.auth = OAuth1(
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret
        )
        self.base_url = "https://ads-api.twitter.com/12"

    def create_campaign(self, account_id, name, funding_instrument_id,
                       daily_budget_amount_local_micro, objective):
        """Create a new campaign."""
        url = f"{self.base_url}/accounts/{account_id}/campaigns"

        data = {
            "name": name,
            "funding_instrument_id": funding_instrument_id,
            "daily_budget_amount_local_micro": daily_budget_amount_local_micro,  # In micros
            "objective": objective,
            # TWEET_ENGAGEMENTS, FOLLOWERS, WEBSITE_CLICKS, APP_INSTALLS,
            # VIDEO_VIEWS, REACH, APP_RE_ENGAGEMENTS, AWARENESS
            "status": "PAUSED",
        }

        response = requests.post(url, auth=self.auth, json=data)
        return response.json()

    def create_line_item(self, account_id, campaign_id, name, bid_amount_local_micro,
                        objective, targeting_criteria):
        """Create a line item (ad group)."""
        url = f"{self.base_url}/accounts/{account_id}/line_items"

        data = {
            "campaign_id": campaign_id,
            "name": name,
            "bid_amount_local_micro": bid_amount_local_micro,
            "objective": objective,
            "placements": ["ALL_ON_TWITTER"],
            "automatically_select_bid": False,
            "bid_type": "AUTO",  # AUTO, MAX, TARGET
            "charge_by": "ENGAGEMENT",  # ENGAGEMENT, IMPRESSION, etc.
            "primary_web_event_tag": None,  # For website conversions
            "status": "PAUSED",
            "targeting": targeting_criteria,
        }

        response = requests.post(url, auth=self.auth, json=data)
        return response.json()


def build_targeting_criteria(api, account_id, interests=None, keywords=None,
                            followers_of=None, locations=None, languages=None,
                            gender=None, age_range=None, devices=None):
    """Build targeting criteria for Twitter Ads."""

    targeting_criteria = []

    # Interest targeting
    if interests:
        targeting_criteria.append({
            "targeting_type": "INTEREST",
            "targeting_value": interests  # List of interest IDs
        })

    # Keyword targeting
    if keywords:
        targeting_criteria.append({
            "targeting_type": "KEYWORD",
            "targeting_value": keywords
        })

    # Follower lookalike targeting
    if followers_of:
        targeting_criteria.append({
            "targeting_type": "FOLLOWERS_OF_USER",
            "targeting_value": followers_of  # List of @usernames
        })

    # Location targeting
    if locations:
        targeting_criteria.append({
            "targeting_type": "LOCATION",
            "targeting_value": locations  # Location IDs
        })

    # Language targeting
    if languages:
        targeting_criteria.append({
            "targeting_type": "LANGUAGE",
            "targeting_value": languages  # ["en", "es", etc.]
        })

    # Gender targeting
    if gender:
        targeting_criteria.append({
            "targeting_type": "GENDER",
            "targeting_value": gender  # "1" for male, "2" for female
        })

    # Age range targeting
    if age_range:
        targeting_criteria.append({
            "targeting_type": "AGE",
            "targeting_value": age_range  # ["AGE_13_TO_24", "AGE_25_TO_49", etc.]
        })

    # Device targeting
    if devices:
        targeting_criteria.append({
            "targeting_type": "PLATFORM",
            "targeting_value": devices  # ["0" for desktop, "1" for mobile]
        })

    return targeting_criteria


def create_promoted_tweet(api, account_id, line_item_id, tweet_id):
    """Promote an existing tweet."""
    url = f"{api.base_url}/accounts/{account_id}/promoted_tweets"

    data = {
        "line_item_id": line_item_id,
        "tweet_id": tweet_id,
    }

    response = requests.post(url, auth=api.auth, json=data)
    return response.json()


# Create tweet for promotion
def create_tweet_for_promotion(api, account_id, text, media_ids=None, card_uri=None):
    """Create a tweet to promote (requires Twitter API v2)."""
    # Note: This uses standard Twitter API, not Ads API
    url = "https://api.twitter.com/2/tweets"

    data = {
        "text": text
    }

    if media_ids:
        data["media"] = {"media_ids": media_ids}

    if card_uri:
        data["card_uri"] = card_uri

    response = requests.post(url, auth=api.auth, json=data)
    return response.json()
```

**Twitter Cards for Ads:**
```python
def create_website_card(api, account_id, name, website_title, website_url, image_media_id):
    """Create a website card for promoted tweets."""
    url = f"{api.base_url}/accounts/{account_id}/cards/website"

    data = {
        "name": name,
        "website_title": website_title,
        "website_url": website_url,
        "image_media_id": image_media_id,
    }

    response = requests.post(url, auth=api.auth, json=data)
    return response.json()


def create_video_website_card(api, account_id, name, website_url,
                              video_id, title, description=None):
    """Create a video website card."""
    url = f"{api.base_url}/accounts/{account_id}/cards/video_website"

    data = {
        "name": name,
        "title": title,
        "video_id": video_id,
        "website_url": website_url,
    }

    if description:
        data["description"] = description

    response = requests.post(url, auth=api.auth, json=data)
    return response.json()


def upload_media(api, account_id, media_path, media_type="IMAGE"):
    """Upload media for use in ads."""
    url = f"{api.base_url}/accounts/{account_id}/media_library"

    with open(media_path, 'rb') as media_file:
        files = {
            'media': media_file,
            'media_type': (None, media_type),  # IMAGE or VIDEO
        }

        response = requests.post(url, auth=api.auth, files=files)
        return response.json()
```

### 2. Reporting and Analytics

**Campaign Performance Reports:**
```python
import pandas as pd
from datetime import datetime, timedelta

def get_campaign_stats(api, account_id, campaign_ids, start_time, end_time,
                       granularity="DAY"):
    """Get campaign performance statistics."""
    url = f"{api.base_url}/stats/accounts/{account_id}"

    params = {
        "entity": "CAMPAIGN",
        "entity_ids": ",".join(campaign_ids),
        "start_time": start_time.isoformat() + "Z",
        "end_time": end_time.isoformat() + "Z",
        "granularity": granularity,  # HOUR, DAY, TOTAL
        "metric_groups": "ENGAGEMENT,BILLING,VIDEO,MEDIA,WEB_CONVERSION",
        "placement": "ALL_ON_TWITTER",
    }

    response = requests.get(url, auth=api.auth, params=params)
    data = response.json()

    results = []
    for item in data.get('data', []):
        metrics = item.get('id_data', [{}])[0].get('metrics', {})
        results.append({
            'campaign_id': item.get('id'),
            'date': item.get('id_data', [{}])[0].get('segment', {}).get('start_time'),
            'impressions': int(metrics.get('impressions', [0])[0]),
            'engagements': int(metrics.get('engagements', [0])[0]),
            'clicks': int(metrics.get('clicks', [0])[0]),
            'url_clicks': int(metrics.get('url_clicks', [0])[0]),
            'retweets': int(metrics.get('retweets', [0])[0]),
            'likes': int(metrics.get('likes', [0])[0]),
            'replies': int(metrics.get('replies', [0])[0]),
            'follows': int(metrics.get('follows', [0])[0]),
            'spend': float(metrics.get('billed_charge_local_micro', [0])[0]) / 1_000_000,
            'video_views': int(metrics.get('video_total_views', [0])[0]),
        })

    df = pd.DataFrame(results)

    # Calculate derived metrics
    if not df.empty:
        df['engagement_rate'] = df['engagements'] / df['impressions'].replace(0, 1)
        df['cpe'] = df['spend'] / df['engagements'].replace(0, 1)
        df['cpm'] = (df['spend'] / df['impressions'].replace(0, 1)) * 1000

    return df


def get_tweet_stats(api, account_id, promoted_tweet_ids, start_time, end_time):
    """Get promoted tweet performance."""
    url = f"{api.base_url}/stats/accounts/{account_id}"

    params = {
        "entity": "PROMOTED_TWEET",
        "entity_ids": ",".join(promoted_tweet_ids),
        "start_time": start_time.isoformat() + "Z",
        "end_time": end_time.isoformat() + "Z",
        "granularity": "TOTAL",
        "metric_groups": "ENGAGEMENT,BILLING,VIDEO",
    }

    response = requests.get(url, auth=api.auth, params=params)
    return response.json()


def get_conversion_tracking(api, account_id, campaign_ids, conversion_event):
    """Get conversion tracking data."""
    url = f"{api.base_url}/stats/accounts/{account_id}"

    params = {
        "entity": "CAMPAIGN",
        "entity_ids": ",".join(campaign_ids),
        "metric_groups": "WEB_CONVERSION",
        "segmentation_type": "CONVERSION_TAGS",
    }

    response = requests.get(url, auth=api.auth, params=params)
    return response.json()
```

### 3. Audience Management

**Tailored Audiences:**
```python
def create_tailored_audience(api, account_id, name, audience_type="EMAIL"):
    """Create a tailored audience for remarketing."""
    url = f"{api.base_url}/accounts/{account_id}/tailored_audiences"

    data = {
        "name": name,
        "list_type": audience_type,  # EMAIL, DEVICE_ID, TWITTER_ID, HANDLE, etc.
    }

    response = requests.post(url, auth=api.auth, json=data)
    return response.json()


def upload_audience_data(api, account_id, tailored_audience_id, user_data):
    """Upload user data to tailored audience."""
    import hashlib

    url = f"{api.base_url}/accounts/{account_id}/tailored_audience_changes"

    # Hash emails
    hashed_users = []
    for email in user_data:
        hashed = hashlib.sha256(email.lower().strip().encode()).hexdigest()
        hashed_users.append(hashed)

    data = {
        "tailored_audience_id": tailored_audience_id,
        "operation": "ADD",
        "input_file_path": None,  # For file upload
        "users": hashed_users,  # For direct upload
    }

    response = requests.post(url, auth=api.auth, json=data)
    return response.json()


def create_lookalike_audience(api, account_id, name, source_audience_id, location):
    """Create a lookalike audience."""
    url = f"{api.base_url}/accounts/{account_id}/tailored_audiences"

    data = {
        "name": name,
        "list_type": "LOOKALIKE",
        "lookalike_expansion": 1,  # 1-10 (expansion percentage)
        "lookalike_targeting_type": source_audience_id,
        "locations": location,  # Location IDs
    }

    response = requests.post(url, auth=api.auth, json=data)
    return response.json()


def create_website_audience(api, account_id, name, pixel_id, retention_days=90):
    """Create website traffic audience from Twitter Pixel."""
    url = f"{api.base_url}/accounts/{account_id}/tailored_audiences"

    data = {
        "name": name,
        "list_type": "WEB",
        "web_engagement_type": "CUSTOM_EVENTS",
        "pixel_id": pixel_id,
        "retention_days": retention_days,
    }

    response = requests.post(url, auth=api.auth, json=data)
    return response.json()
```

### 4. Twitter Pixel and Conversion Tracking

**Set Up Conversion Tracking:**
```python
def create_web_event_tag(api, account_id, name):
    """Create a Twitter Pixel (web event tag)."""
    url = f"{api.base_url}/accounts/{account_id}/web_event_tags"

    data = {
        "name": name,
        "click_window": 30,  # Attribution window in days
        "view_through_window": 1,  # View-through attribution window
    }

    response = requests.post(url, auth=api.auth, json=data)
    return response.json()


def get_pixel_code(api, account_id, pixel_id):
    """Get pixel code snippet for website installation."""
    url = f"{api.base_url}/accounts/{account_id}/web_event_tags/{pixel_id}"

    response = requests.get(url, auth=api.auth)
    return response.json()


# Server-side conversion tracking
def track_conversion_event(api, account_id, pixel_id, event_name, conversion_data):
    """Send server-side conversion event."""
    url = f"{api.base_url}/accounts/{account_id}/web_event_tags/{pixel_id}/events"

    data = {
        "conversion_time": conversion_data.get('timestamp'),
        "event_type": event_name,  # PageView, Purchase, AddToCart, etc.
        "identifiers": {
            "hashed_email": conversion_data.get('hashed_email'),
            "hashed_phone_number": conversion_data.get('hashed_phone'),
        },
        "conversion_value": conversion_data.get('value'),
        "currency": conversion_data.get('currency', 'USD'),
    }

    response = requests.post(url, auth=api.auth, json=data)
    return response.json()
```

## Installation and Authentication

### Install Required Libraries

```bash
pip install requests requests-oauthlib pandas
```

### Set Up Authentication

1. **Create Twitter App** at https://developer.twitter.com/en/apps
2. **Apply for Ads API Access** at https://ads.twitter.com/
3. **Get API credentials**:
   - Consumer Key (API Key)
   - Consumer Secret (API Secret)
   - Access Token
   - Access Token Secret
4. **Find Ad Account ID** in Twitter Ads Manager

### Initialize API Client

```python
from requests_oauthlib import OAuth1
import requests

class TwitterAdsAPI:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.auth = OAuth1(
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret
        )
        self.base_url = "https://ads-api.twitter.com/12"

# Initialize
api = TwitterAdsAPI(
    consumer_key="YOUR_CONSUMER_KEY",
    consumer_secret="YOUR_CONSUMER_SECRET",
    access_token="YOUR_ACCESS_TOKEN",
    access_token_secret="YOUR_ACCESS_TOKEN_SECRET"
)
```

## Quick Start Example

```python
from datetime import datetime, timedelta

# Initialize API
api = TwitterAdsAPI(
    consumer_key="YOUR_CONSUMER_KEY",
    consumer_secret="YOUR_CONSUMER_SECRET",
    access_token="YOUR_ACCESS_TOKEN",
    access_token_secret="YOUR_ACCESS_TOKEN_SECRET"
)

account_id = "18ce54d4x5t"

# Get campaign stats for last 7 days
end_time = datetime.utcnow()
start_time = end_time - timedelta(days=7)

campaign_ids = ["campaign_id_1", "campaign_id_2"]
df = get_campaign_stats(api, account_id, campaign_ids, start_time, end_time)

# Display results
print(df[['date', 'impressions', 'engagements', 'clicks', 'spend']])
print(f"\nTotal Spend: ${df['spend'].sum():.2f}")
print(f"Total Engagements: {df['engagements'].sum():,}")
print(f"Average Engagement Rate: {df['engagement_rate'].mean():.2%}")
```

## Key Metrics Reference

### Performance Metrics
- **Impressions** - Number of times ad was shown
- **Engagements** - Total engagements (clicks, retweets, likes, replies, follows)
- **Engagement Rate** - Engagements / Impressions
- **Clicks** - Total clicks on ad
- **URL Clicks** - Clicks on URLs in tweets
- **CPE** - Cost per engagement
- **CPM** - Cost per 1,000 impressions

### Engagement Metrics
- **Retweets** - Number of retweets
- **Likes** - Number of likes
- **Replies** - Number of replies
- **Follows** - New followers gained
- **App Clicks** - Clicks to app store
- **Card Engagements** - Engagements with Twitter Cards
- **Detail Expands** - Tweet detail views
- **Hashtag Clicks** - Clicks on hashtags

### Video Metrics
- **Video Views** - Total video views (2+ seconds)
- **Video Views 25%** - 25% completion
- **Video Views 50%** - 50% completion
- **Video Views 75%** - 75% completion
- **Video Views 100%** - Complete views
- **Video Starts** - Video play starts

### Conversion Metrics
- **Website Conversions** - Tracked conversions
- **Post-Engagement Conversions** - Conversions after engagement
- **Post-View Conversions** - View-through conversions
- **Cost Per Conversion** - Average cost per conversion

## Best Practices

1. **Creative Strategy**
   - Keep tweets concise and engaging
   - Use high-quality images and videos
   - Include clear CTAs
   - Leverage trending topics and hashtags

2. **Targeting Optimization**
   - Use keyword targeting for intent-based campaigns
   - Target followers of competitors and influencers
   - Combine interest and keyword targeting
   - Test different audience segments

3. **Bidding Strategy**
   - Start with automatic bidding
   - Switch to target cost after collecting data
   - Adjust bids based on engagement quality
   - Monitor cost per result metrics

4. **Real-Time Marketing**
   - Participate in trending conversations
   - Monitor live events and cultural moments
   - Use quick turnaround for timely content
   - Leverage Twitter Trends API

5. **Campaign Optimization**
   - Refresh creative weekly to avoid fatigue
   - Exclude converted users from awareness campaigns
   - Use video for higher engagement rates
   - Test different card formats

## Common Use Cases

### Event Promotion
```python
def create_event_campaign(api, account_id, event_hashtag, event_date):
    """Create campaign for event promotion."""
    # Target users interested in event topic
    # Create countdown campaigns
    # Promote event-related content
    pass
```

### App Install Campaign
```python
def create_app_install_campaign(api, account_id, app_id, app_store_url):
    """Create app install campaign."""
    # Set APP_INSTALLS objective
    # Create app card
    # Target mobile users
    pass
```

### Trend Jacking
```python
def create_trending_campaign(api, account_id, trending_topic):
    """Create campaign around trending topic."""
    # Monitor trending hashtags
    # Create relevant content
    # Quick campaign activation
    pass
```

## References

- **Official Documentation**: https://developer.twitter.com/en/docs/twitter-ads-api
- **Ads API Reference**: https://developer.twitter.com/en/docs/twitter-ads-api/campaign-management
- **Authentication**: https://developer.twitter.com/en/docs/authentication/oauth-1-0a
- **Targeting Options**: https://business.twitter.com/en/help/campaign-setup/campaign-targeting.html
- **Twitter Pixel**: https://business.twitter.com/en/help/campaign-measurement-and-analytics/conversion-tracking-for-websites.html
- **Best Practices**: https://business.twitter.com/en/blog
- **Developer Portal**: https://developer.twitter.com/en/portal/dashboard
- **Support**: https://business.twitter.com/en/help.html

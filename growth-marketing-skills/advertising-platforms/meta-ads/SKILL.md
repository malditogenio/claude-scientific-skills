---
name: meta-ads
description: "Meta Ads API for Facebook and Instagram advertising. Manage campaigns, ad sets, ads, audiences, creative, conversion tracking, and performance analytics across Meta platforms."
---

# Meta Ads (Facebook & Instagram)

## Overview

Meta Ads (formerly Facebook Ads) provides advertising across Facebook, Instagram, Messenger, and the Audience Network. The Marketing API enables programmatic campaign management, audience targeting, creative optimization, and comprehensive analytics for the world's largest social media advertising ecosystem.

This skill covers the Meta Marketing API with Python, enabling automated campaign creation, audience management, dynamic creative optimization, and cross-platform performance analysis.

## When to Use This Skill

Use this skill when you need to:
- Create and manage Facebook and Instagram ad campaigns programmatically
- Build and manage custom and lookalike audiences
- Automate creative testing and optimization
- Generate detailed performance reports and insights
- Manage large-scale campaigns across multiple ad accounts
- Implement conversion tracking and attribution
- Create dynamic product ads from product catalogs
- Manage Instagram Shopping and Facebook Shops
- Implement automated bidding strategies
- Sync audience data for remarketing
- Monitor ad spend and ROI across platforms

## Core Capabilities

### 1. Campaign Management

**Create a Campaign Structure:**
```python
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative

# Initialize API
FacebookAdsApi.init(
    access_token='YOUR_ACCESS_TOKEN',
    app_id='YOUR_APP_ID',
    app_secret='YOUR_APP_SECRET'
)

ad_account_id = 'act_123456789'

def create_campaign(ad_account_id, campaign_name, objective):
    """Create a new campaign."""
    from facebook_business.adobjects.adaccount import AdAccount

    account = AdAccount(ad_account_id)

    campaign = Campaign(parent_id=ad_account_id)
    campaign.update({
        Campaign.Field.name: campaign_name,
        Campaign.Field.objective: objective,  # e.g., 'CONVERSIONS', 'LINK_CLICKS', 'REACH'
        Campaign.Field.status: Campaign.Status.paused,
        Campaign.Field.special_ad_categories: [],  # Required for some categories
    })

    campaign.remote_create(params={
        'status': Campaign.Status.paused,
    })

    return campaign


def create_ad_set(campaign_id, ad_set_name, daily_budget, targeting):
    """Create an ad set with targeting."""
    adset = AdSet(parent_id=ad_account_id)

    adset.update({
        AdSet.Field.name: ad_set_name,
        AdSet.Field.campaign_id: campaign_id,
        AdSet.Field.daily_budget: daily_budget,  # In cents: 5000 = $50
        AdSet.Field.billing_event: AdSet.BillingEvent.impressions,
        AdSet.Field.optimization_goal: AdSet.OptimizationGoal.link_clicks,
        AdSet.Field.bid_amount: 150,  # In cents
        AdSet.Field.targeting: targeting,
        AdSet.Field.status: AdSet.Status.paused,
        AdSet.Field.promoted_object: {
            'pixel_id': 'YOUR_PIXEL_ID',
            'custom_event_type': 'PURCHASE'
        },
    })

    adset.remote_create()

    return adset


# Example targeting configuration
def build_targeting(interests=None, age_min=18, age_max=65, genders=None, locations=None):
    """Build a targeting specification."""
    targeting = {
        'geo_locations': locations or {
            'countries': ['US'],
        },
        'age_min': age_min,
        'age_max': age_max,
        'publisher_platforms': ['facebook', 'instagram'],
        'facebook_positions': ['feed', 'right_hand_column'],
        'instagram_positions': ['stream', 'story'],
    }

    if genders:
        targeting['genders'] = genders  # [1] for male, [2] for female

    if interests:
        targeting['flexible_spec'] = [{
            'interests': [{'id': interest_id, 'name': interest_name}
                         for interest_id, interest_name in interests]
        }]

    return targeting


# Create ad with creative
def create_ad_with_creative(ad_set_id, ad_name, image_hash, message, link, cta):
    """Create an ad with image creative."""

    # Create ad creative
    creative = AdCreative(parent_id=ad_account_id)
    creative.update({
        AdCreative.Field.name: f"{ad_name} Creative",
        AdCreative.Field.object_story_spec: {
            'page_id': 'YOUR_PAGE_ID',
            'link_data': {
                'image_hash': image_hash,
                'link': link,
                'message': message,
                'call_to_action': {
                    'type': cta,  # 'LEARN_MORE', 'SHOP_NOW', 'SIGN_UP', etc.
                    'value': {
                        'link': link
                    }
                }
            }
        }
    })
    creative.remote_create()

    # Create ad
    ad = Ad(parent_id=ad_account_id)
    ad.update({
        Ad.Field.name: ad_name,
        Ad.Field.adset_id: ad_set_id,
        Ad.Field.creative: {'creative_id': creative.get_id()},
        Ad.Field.status: Ad.Status.paused,
    })
    ad.remote_create()

    return ad, creative


# Upload image for ad
def upload_image(image_path):
    """Upload an image to use in ads."""
    from facebook_business.adobjects.adimage import AdImage

    image = AdImage(parent_id=ad_account_id)
    image[AdImage.Field.filename] = image_path
    image.remote_create()

    return image[AdImage.Field.hash]
```

**Dynamic Creative Testing:**
```python
def create_dynamic_creative_ad(ad_set_id, ad_name, headlines, descriptions, images, links):
    """Create an ad with dynamic creative optimization."""

    # Build dynamic creative spec
    asset_feed_spec = {
        'images': [{'hash': img_hash} for img_hash in images],
        'bodies': [{'text': desc} for desc in descriptions],
        'titles': [{'text': headline} for headline in headlines],
        'link_urls': [{'website_url': link} for link in links],
        'call_to_action_types': ['SHOP_NOW', 'LEARN_MORE'],
    }

    creative = AdCreative(parent_id=ad_account_id)
    creative.update({
        AdCreative.Field.name: f"{ad_name} Dynamic Creative",
        AdCreative.Field.object_story_spec: {
            'page_id': 'YOUR_PAGE_ID',
        },
        AdCreative.Field.asset_feed_spec: asset_feed_spec,
    })
    creative.remote_create()

    ad = Ad(parent_id=ad_account_id)
    ad.update({
        Ad.Field.name: ad_name,
        Ad.Field.adset_id: ad_set_id,
        Ad.Field.creative: {'creative_id': creative.get_id()},
        Ad.Field.status: Ad.Status.paused,
    })
    ad.remote_create()

    return ad
```

### 2. Reporting and Analytics

**Campaign Performance Report:**
```python
from facebook_business.adobjects.adsinsights import AdsInsights
import pandas as pd

def get_campaign_insights(ad_account_id, date_preset='last_30d'):
    """Get campaign performance metrics."""
    from facebook_business.adobjects.adaccount import AdAccount

    account = AdAccount(ad_account_id)

    params = {
        'level': 'campaign',
        'date_preset': date_preset,  # 'today', 'yesterday', 'last_7d', 'last_30d', etc.
        'time_increment': 1,  # Daily breakdown
    }

    fields = [
        AdsInsights.Field.campaign_id,
        AdsInsights.Field.campaign_name,
        AdsInsights.Field.impressions,
        AdsInsights.Field.clicks,
        AdsInsights.Field.ctr,
        AdsInsights.Field.spend,
        AdsInsights.Field.cpc,
        AdsInsights.Field.cpm,
        AdsInsights.Field.cpp,
        AdsInsights.Field.reach,
        AdsInsights.Field.frequency,
        AdsInsights.Field.actions,  # Conversions
        AdsInsights.Field.cost_per_action_type,
        AdsInsights.Field.action_values,  # Conversion values
        AdsInsights.Field.purchase_roas,
    ]

    insights = account.get_insights(fields=fields, params=params)

    results = []
    for insight in insights:
        row = {
            'campaign_id': insight.get('campaign_id'),
            'campaign_name': insight.get('campaign_name'),
            'date': insight.get('date_start'),
            'impressions': int(insight.get('impressions', 0)),
            'clicks': int(insight.get('clicks', 0)),
            'ctr': float(insight.get('ctr', 0)),
            'spend': float(insight.get('spend', 0)),
            'cpc': float(insight.get('cpc', 0)),
            'cpm': float(insight.get('cpm', 0)),
            'reach': int(insight.get('reach', 0)),
            'frequency': float(insight.get('frequency', 0)),
        }

        # Parse actions (conversions)
        actions = insight.get('actions', [])
        for action in actions:
            action_type = action['action_type']
            row[f'actions_{action_type}'] = int(action['value'])

        results.append(row)

    return pd.DataFrame(results)


def get_ad_creative_report(ad_account_id):
    """Get performance by ad creative."""
    from facebook_business.adobjects.adaccount import AdAccount

    account = AdAccount(ad_account_id)

    params = {
        'level': 'ad',
        'date_preset': 'last_30d',
        'breakdowns': ['age', 'gender'],  # Demographic breakdown
    }

    fields = [
        AdsInsights.Field.ad_id,
        AdsInsights.Field.ad_name,
        AdsInsights.Field.adset_name,
        AdsInsights.Field.campaign_name,
        AdsInsights.Field.impressions,
        AdsInsights.Field.clicks,
        AdsInsights.Field.spend,
        AdsInsights.Field.actions,
        AdsInsights.Field.video_30_sec_watched_actions,
        AdsInsights.Field.video_p25_watched_actions,
        AdsInsights.Field.video_p50_watched_actions,
        AdsInsights.Field.video_p75_watched_actions,
        AdsInsights.Field.video_p100_watched_actions,
    ]

    insights = account.get_insights(fields=fields, params=params)

    return [dict(insight) for insight in insights]


def get_audience_insights(ad_account_id, breakdown='age'):
    """Get audience demographic performance."""
    from facebook_business.adobjects.adaccount import AdAccount

    account = AdAccount(ad_account_id)

    params = {
        'level': 'account',
        'date_preset': 'last_30d',
        'breakdowns': [breakdown],  # 'age', 'gender', 'country', 'region', etc.
    }

    fields = [
        AdsInsights.Field.impressions,
        AdsInsights.Field.clicks,
        AdsInsights.Field.spend,
        AdsInsights.Field.ctr,
        AdsInsights.Field.cpc,
        AdsInsights.Field.actions,
    ]

    insights = account.get_insights(fields=fields, params=params)

    results = []
    for insight in insights:
        results.append({
            breakdown: insight.get(breakdown),
            'impressions': int(insight.get('impressions', 0)),
            'clicks': int(insight.get('clicks', 0)),
            'spend': float(insight.get('spend', 0)),
            'ctr': float(insight.get('ctr', 0)),
            'cpc': float(insight.get('cpc', 0)),
        })

    return pd.DataFrame(results)
```

### 3. Audience Management

**Custom Audiences:**
```python
from facebook_business.adobjects.customaudience import CustomAudience

def create_custom_audience_from_emails(ad_account_id, name, emails):
    """Create a custom audience from email list."""
    import hashlib

    audience = CustomAudience(parent_id=ad_account_id)

    audience.update({
        CustomAudience.Field.name: name,
        CustomAudience.Field.subtype: CustomAudience.Subtype.custom,
        CustomAudience.Field.description: 'Email list upload',
        CustomAudience.Field.customer_file_source: CustomAudience.CustomerFileSource.user_provided_only,
    })

    audience.remote_create()

    # Hash emails with SHA256
    schema = [CustomAudience.Schema.email]
    hashed_users = []

    for email in emails:
        hashed_email = hashlib.sha256(email.lower().strip().encode()).hexdigest()
        hashed_users.append([hashed_email])

    # Add users in batches of 10,000
    batch_size = 10000
    for i in range(0, len(hashed_users), batch_size):
        batch = hashed_users[i:i + batch_size]
        audience.add_users(
            schema=schema,
            users=batch,
        )

    return audience


def create_lookalike_audience(ad_account_id, name, source_audience_id, country, ratio):
    """Create a lookalike audience from a source audience."""
    from facebook_business.adobjects.lookalikaudience import LookalikeAudience

    lookalike = LookalikeAudience(parent_id=ad_account_id)

    lookalike.update({
        LookalikeAudience.Field.name: name,
        LookalikeAudience.Field.origin_audience_id: source_audience_id,
        LookalikeAudience.Field.lookalike_spec: {
            'ratio': ratio,  # 0.01 to 0.20 (1% to 20%)
            'country': country,  # 'US', 'CA', etc.
        },
    })

    lookalike.remote_create()

    return lookalike


def create_website_custom_audience(ad_account_id, pixel_id, name, retention_days=180):
    """Create a website custom audience from pixel events."""

    audience = CustomAudience(parent_id=ad_account_id)

    audience.update({
        CustomAudience.Field.name: name,
        CustomAudience.Field.subtype: CustomAudience.Subtype.website,
        CustomAudience.Field.retention_days: retention_days,
        CustomAudience.Field.rule: {
            'url': {'i_contains': 'product'},  # Visitors to product pages
        },
        CustomAudience.Field.pixel_id: pixel_id,
    })

    audience.remote_create()

    return audience


# Engagement custom audience
def create_engagement_audience(ad_account_id, page_id, name, engagement_type='page'):
    """Create an audience based on engagement with Facebook Page or Instagram."""

    audience = CustomAudience(parent_id=ad_account_id)

    rule_spec = {
        'inclusions': {
            'operator': 'or',
            'rules': [{
                'event_sources': [{
                    'id': page_id,
                    'type': engagement_type,  # 'page', 'video', 'event'
                }],
                'retention_seconds': 15552000,  # 180 days
                'filter': {
                    'operator': 'or',
                    'filters': [{
                        'field': 'event',
                        'operator': 'eq',
                        'value': 'page_engaged',  # or 'video_view', 'page_like'
                    }],
                },
            }],
        },
    }

    audience.update({
        CustomAudience.Field.name: name,
        CustomAudience.Field.subtype: CustomAudience.Subtype.engagement,
        CustomAudience.Field.rule: rule_spec,
    })

    audience.remote_create()

    return audience
```

### 4. Conversion Tracking and Events

**Facebook Pixel Events:**
```python
from facebook_business.adobjects.serverside.event import Event
from facebook_business.adobjects.serverside.event_request import EventRequest
from facebook_business.adobjects.serverside.user_data import UserData
from facebook_business.adobjects.serverside.custom_data import CustomData

def send_conversion_event(pixel_id, access_token, event_name, user_data, custom_data):
    """Send a server-side conversion event."""

    user = UserData(
        email=user_data.get('email'),
        phone=user_data.get('phone'),
        client_ip_address=user_data.get('ip'),
        client_user_agent=user_data.get('user_agent'),
        fbc=user_data.get('fbc'),  # Facebook click ID
        fbp=user_data.get('fbp'),  # Facebook browser ID
    )

    custom = CustomData(
        value=custom_data.get('value'),
        currency=custom_data.get('currency', 'USD'),
        content_ids=custom_data.get('content_ids'),
        content_type=custom_data.get('content_type'),
        content_name=custom_data.get('content_name'),
    )

    event = Event(
        event_name=event_name,  # 'Purchase', 'Lead', 'AddToCart', etc.
        event_time=int(time.time()),
        user_data=user,
        custom_data=custom,
        event_source_url=custom_data.get('source_url'),
        action_source='website',  # or 'app', 'email', 'phone_call'
    )

    event_request = EventRequest(
        events=[event],
        pixel_id=pixel_id,
        access_token=access_token,
    )

    response = event_request.execute()

    return response


# Conversions API for offline events
def upload_offline_conversion(offline_event_set_id, events_data):
    """Upload offline conversions (store purchases, phone orders, etc.)."""
    from facebook_business.adobjects.offlineeventset import OfflineEventSet

    event_set = OfflineEventSet(offline_event_set_id)

    events = []
    for event_data in events_data:
        events.append({
            'event_name': event_data['event_name'],
            'event_time': event_data['event_time'],
            'match_keys': {
                'email': event_data.get('email'),
                'phone': event_data.get('phone'),
            },
            'custom_data': {
                'value': event_data['value'],
                'currency': event_data.get('currency', 'USD'),
            },
        })

    response = event_set.create_event(
        params={'data': events}
    )

    return response
```

## Installation and Authentication

### Install the Facebook Business SDK

```bash
pip install facebook-business
```

### Set Up Authentication

1. **Create a Facebook App** in Meta for Developers
2. **Get App ID and App Secret**
3. **Generate User Access Token** with Marketing API permissions
4. **Get Ad Account ID** from Meta Business Manager

### Initialize API

```python
from facebook_business.api import FacebookAdsApi

# Initialize the API
FacebookAdsApi.init(
    access_token='YOUR_ACCESS_TOKEN',
    app_id='YOUR_APP_ID',
    app_secret='YOUR_APP_SECRET',
)

# Or set up with app token
FacebookAdsApi.init(
    app_id='YOUR_APP_ID',
    app_secret='YOUR_APP_SECRET',
)

# Get long-lived token
from facebook_business.adobjects.user import User
me = User(fbid='me')
my_account = me.get_ad_accounts()[0]
print(f"Ad Account ID: {my_account.get_id()}")
```

## Quick Start Example

```python
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
import pandas as pd

# Initialize
FacebookAdsApi.init(access_token='YOUR_ACCESS_TOKEN')
ad_account_id = 'act_123456789'

# Get account insights
account = AdAccount(ad_account_id)

insights = account.get_insights(
    fields=[
        AdsInsights.Field.campaign_name,
        AdsInsights.Field.impressions,
        AdsInsights.Field.clicks,
        AdsInsights.Field.spend,
        AdsInsights.Field.actions,
    ],
    params={
        'level': 'campaign',
        'date_preset': 'last_7d',
    }
)

# Process results
for insight in insights:
    print(f"Campaign: {insight.get('campaign_name')}")
    print(f"  Impressions: {insight.get('impressions'):,}")
    print(f"  Clicks: {insight.get('clicks'):,}")
    print(f"  Spend: ${float(insight.get('spend')):.2f}")

    # Get conversion actions
    actions = insight.get('actions', [])
    for action in actions:
        if action['action_type'] == 'purchase':
            print(f"  Purchases: {action['value']}")
```

## Key Metrics Reference

### Performance Metrics
- **Impressions** - Ad views
- **Reach** - Unique users who saw ads
- **Frequency** - Average impressions per person
- **Clicks** - Link clicks or ad clicks
- **CTR** - Click-through rate
- **CPC** - Cost per click
- **CPM** - Cost per 1,000 impressions
- **Spend** - Total amount spent

### Conversion Metrics
- **Actions** - Conversion events (purchases, leads, etc.)
- **Cost Per Action** - Average cost per conversion
- **Purchase ROAS** - Return on ad spend for purchases
- **Action Values** - Total value from conversions
- **Conversion Rate** - Conversions / Clicks

### Engagement Metrics (Video/Stories)
- **ThruPlays** - Videos played to completion
- **Video Views** - 3-second video views
- **Video Watched Actions** - 25%, 50%, 75%, 95%, 100% completion
- **Engagement** - Likes, comments, shares
- **Post Reactions** - Reactions to ads

### Attribution Metrics
- **1-Day Click**, **7-Day Click**, **28-Day Click** - Conversions within window
- **1-Day View**, **7-Day View**, **28-Day View** - View-through conversions

## Best Practices

1. **Rate Limits** - Respect API rate limits (200 calls per hour per user)
2. **Batch Requests** - Use batch API for multiple operations
3. **Async Reports** - Use async insights for large date ranges
4. **Test Mode** - Test campaigns before going live
5. **Webhook Integration** - Use webhooks for real-time updates
6. **Error Handling** - Implement retry logic with exponential backoff
7. **Token Management** - Use long-lived tokens and refresh before expiry
8. **Audience Size** - Ensure custom audiences have at least 100 users

## Common Use Cases

### A/B Testing
```python
def create_ab_test_campaigns(ad_account_id, variants):
    """Create multiple campaign variants for testing."""
    # Create campaigns with different targeting/creative
    # Use Campaign Budget Optimization (CBO)
    pass
```

### Dynamic Product Ads
```python
def setup_dynamic_product_ads(catalog_id, product_set_id):
    """Set up dynamic ads from product catalog."""
    # Create catalog-based custom audience
    # Set up dynamic ad template
    pass
```

### Budget Optimization
```python
def optimize_campaign_budgets(ad_account_id, performance_threshold):
    """Reallocate budgets based on performance."""
    # Get campaign performance
    # Increase budgets for high performers
    # Pause underperforming campaigns
    pass
```

## References

- **Official Documentation**: https://developers.facebook.com/docs/marketing-apis
- **Python SDK**: https://github.com/facebook/facebook-python-business-sdk
- **API Reference**: https://developers.facebook.com/docs/marketing-api/reference
- **Pixel Documentation**: https://developers.facebook.com/docs/facebook-pixel
- **Conversions API**: https://developers.facebook.com/docs/marketing-api/conversions-api
- **Best Practices**: https://www.facebook.com/business/help/marketing-api-best-practices
- **Rate Limits**: https://developers.facebook.com/docs/graph-api/overview/rate-limiting
- **Changelog**: https://developers.facebook.com/docs/graph-api/changelog

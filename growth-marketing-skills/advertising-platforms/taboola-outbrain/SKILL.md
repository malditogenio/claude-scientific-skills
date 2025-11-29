---
name: taboola-outbrain
description: "Taboola and Outbrain APIs for native advertising. Manage content recommendation campaigns, sponsored content, audience targeting, and analytics for discovery platforms."
---

# Taboola & Outbrain (Native Advertising)

## Overview

Taboola and Outbrain are the leading native advertising platforms, powering content recommendation widgets on premium publisher sites. Their APIs enable programmatic campaign management, sponsored content promotion, audience targeting, and comprehensive analytics for content discovery and native advertising.

This skill covers both Taboola and Outbrain APIs with Python, enabling automated content promotion, audience targeting, and performance optimization for native advertising campaigns.

## When to Use This Skill

Use this skill when you need to:
- Create and manage native advertising campaigns programmatically
- Promote content on premium publisher networks
- Drive traffic to blog posts, articles, and landing pages
- Target audiences by interests and content affinity
- Generate performance reports and engagement analytics
- Manage large-scale content promotion campaigns
- Implement A/B testing for headlines and images
- Optimize for cost per click (CPC) and conversions
- Track content engagement and time on site
- Manage campaigns across Taboola and Outbrain simultaneously
- Scale content distribution to premium publishers

## Core Capabilities

### 1. Taboola Campaign Management

**Create Taboola Campaign:**
```python
import requests
import json
from datetime import datetime

class TaboolaAPI:
    """Taboola Backstage API client."""

    def __init__(self, client_id, client_secret, account_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.account_id = account_id
        self.base_url = "https://backstage.taboola.com/backstage/api/1.0"
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        """Get OAuth2 access token."""
        url = "https://backstage.taboola.com/backstage/oauth/token"

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }

        response = requests.post(url, data=data)
        return response.json()["access_token"]

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def create_campaign(self, name, branding_text, cpc, daily_cap=None,
                       spending_limit=None, start_date=None):
        """Create a new campaign."""
        url = f"{self.base_url}/{self.account_id}/campaigns"

        data = {
            "name": name,
            "branding_text": branding_text,  # Advertiser name shown in widget
            "cpc": cpc,  # Cost per click
            "daily_cap": daily_cap,
            "spending_limit": spending_limit,
            "spending_limit_model": "ENTIRE",
            "marketing_objective": "DRIVE_WEBSITE_TRAFFIC",
            # DRIVE_WEBSITE_TRAFFIC, BOOST_POST_ENGAGEMENT, DRIVE_CONVERSIONS
            "is_active": False,
        }

        if start_date:
            data["start_date"] = start_date.strftime("%Y-%m-%d %H:%M:%S")

        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def create_campaign_item(self, campaign_id, url, title, description=None,
                            thumbnail_url=None):
        """Create a campaign item (ad unit)."""
        url_endpoint = f"{self.base_url}/{self.account_id}/campaigns/{campaign_id}/items"

        data = {
            "url": url,  # Landing page URL
            "title": title,  # Headline (max 100 chars)
            "type": "ITEM",
            "is_active": False,
        }

        if description:
            data["description"] = description  # Optional description

        if thumbnail_url:
            data["thumbnail_url"] = thumbnail_url

        response = requests.post(url_endpoint, headers=self.headers, json=data)
        return response.json()


def set_targeting(api, campaign_id, targeting_config):
    """Set targeting for campaign."""
    url = f"{api.base_url}/{api.account_id}/campaigns/{campaign_id}/targeting"

    data = {
        "type": "INCLUDE",
        "value": targeting_config
    }

    # Geographic targeting
    if "countries" in targeting_config:
        data["targeting_dimension"] = "GEO"
        data["value"] = targeting_config["countries"]  # ["US", "GB", etc.]

    # Platform targeting
    if "platforms" in targeting_config:
        data["targeting_dimension"] = "PLATFORM"
        data["value"] = targeting_config["platforms"]
        # ["DESK" (desktop), "PHON" (mobile), "TBLT" (tablet)]

    # Operating system targeting
    if "os_families" in targeting_config:
        data["targeting_dimension"] = "OS_FAMILY"
        data["value"] = targeting_config["os_families"]
        # ["IOS", "ANDROID", "WINDOWS", "OSX"]

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def set_publisher_targeting(api, campaign_id, publisher_targeting):
    """Target specific publishers or exclude publishers."""
    url = f"{api.base_url}/{api.account_id}/campaigns/{campaign_id}/targeting"

    data = {
        "targeting_dimension": "PUBLISHER",
        "type": publisher_targeting["type"],  # INCLUDE or EXCLUDE
        "value": publisher_targeting["publisher_ids"]
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


# A/B testing headlines and images
def create_campaign_with_variants(api, campaign_id, url, variants):
    """Create multiple headline/image variants for testing."""
    items = []

    for variant in variants:
        item = api.create_campaign_item(
            campaign_id=campaign_id,
            url=url,
            title=variant["title"],
            thumbnail_url=variant.get("thumbnail_url")
        )
        items.append(item)

    return items
```

### 2. Outbrain Campaign Management

**Create Outbrain Campaign:**
```python
class OutbrainAPI:
    """Outbrain Amplify API client."""

    def __init__(self, username, password, account_id):
        self.username = username
        self.password = password
        self.account_id = account_id
        self.base_url = "https://api.outbrain.com/amplify/v0.1"
        self.access_token = self._login()

    def _login(self):
        """Authenticate and get access token."""
        url = f"{self.base_url}/login"

        data = {
            "username": self.username,
            "password": self.password
        }

        response = requests.post(url, json=data)
        return response.json()["OB-TOKEN-V1"]

    @property
    def headers(self):
        return {
            "OB-TOKEN-V1": self.access_token,
            "Content-Type": "application/json",
        }

    def create_campaign(self, name, budget, cpc=None):
        """Create a new campaign."""
        url = f"{self.base_url}/marketers/{self.account_id}/campaigns"

        data = {
            "name": name,
            "enabled": False,
            "budget": {
                "amount": budget,
                "type": "MONTHLY",
                "shared": False,
                "currency": "USD"
            },
            "targeting": {
                "platform": {
                    "included": ["DESKTOP", "MOBILE", "TABLET"]
                }
            }
        }

        if cpc:
            data["budget"]["cpc"] = cpc

        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def create_promoted_link(self, campaign_id, url, text, images=None):
        """Create a promoted link (ad)."""
        url_endpoint = f"{self.base_url}/marketers/{self.account_id}/campaigns/{campaign_id}/promotedLinks"

        data = {
            "url": url,
            "text": text,  # Headline
            "enabled": False,
            "archived": False,
        }

        if images:
            data["images"] = images
            # [{"url": "https://example.com/image.jpg"}]

        response = requests.post(url_endpoint, headers=self.headers, json=data)
        return response.json()


def set_outbrain_targeting(api, campaign_id, targeting_config):
    """Set targeting for Outbrain campaign."""
    url = f"{api.base_url}/marketers/{api.account_id}/campaigns/{campaign_id}"

    targeting = {}

    # Geographic targeting
    if "countries" in targeting_config:
        targeting["location"] = {
            "type": "INCLUDE",
            "values": [{"type": "COUNTRY", "value": c} for c in targeting_config["countries"]]
        }

    # Interest targeting
    if "interests" in targeting_config:
        targeting["interests"] = {
            "type": "INCLUDE",
            "values": targeting_config["interests"]
        }

    # Device targeting
    if "platforms" in targeting_config:
        targeting["platform"] = {
            "included": targeting_config["platforms"]  # ["DESKTOP", "MOBILE", "TABLET"]
        }

    # Browser targeting
    if "browsers" in targeting_config:
        targeting["browser"] = {
            "included": targeting_config["browsers"]
        }

    data = {
        "targeting": targeting
    }

    response = requests.put(url, headers=api.headers, json=data)
    return response.json()


def set_publisher_exclusions(api, campaign_id, excluded_publishers):
    """Exclude specific publishers."""
    url = f"{api.base_url}/marketers/{api.account_id}/campaigns/{campaign_id}"

    data = {
        "targeting": {
            "publishers": {
                "type": "EXCLUDE",
                "values": excluded_publishers  # List of publisher IDs
            }
        }
    }

    response = requests.put(url, headers=api.headers, json=data)
    return response.json()
```

### 3. Reporting and Analytics

**Taboola Performance Reports:**
```python
import pandas as pd
from datetime import datetime, timedelta

def get_taboola_campaign_report(api, start_date, end_date, dimension="campaign_day"):
    """Get Taboola campaign performance report."""
    url = f"{api.base_url}/{api.account_id}/reports/campaign-summary/dimensions/{dimension}"

    params = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
    }

    response = requests.get(url, headers=api.headers, params=params)
    data = response.json()

    results = []
    for record in data.get("results", []):
        results.append({
            'date': record.get('date'),
            'campaign': record.get('campaign'),
            'impressions': record.get('impressions', 0),
            'clicks': record.get('clicks', 0),
            'ctr': record.get('ctr', 0),
            'cpc': record.get('cpc', 0),
            'spent': record.get('spent', 0),
            'conversions': record.get('actions_num', 0),
            'cpa': record.get('cpa', 0),
            'visible_impressions': record.get('visible_impressions', 0),
            'viewability_rate': record.get('viewability_rate', 0),
        })

    return pd.DataFrame(results)


def get_taboola_top_campaign_content(api, campaign_id, start_date, end_date):
    """Get top performing content items."""
    url = f"{api.base_url}/{api.account_id}/reports/top-campaign-content/dimensions/item_day"

    params = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "campaign": campaign_id,
    }

    response = requests.get(url, headers=api.headers, params=params)
    data = response.json()

    results = []
    for record in data.get("results", []):
        results.append({
            'item_id': record.get('item'),
            'title': record.get('item_title'),
            'url': record.get('item_url'),
            'impressions': record.get('impressions', 0),
            'clicks': record.get('clicks', 0),
            'ctr': record.get('ctr', 0),
            'spent': record.get('spent', 0),
            'conversions': record.get('actions_num', 0),
        })

    return pd.DataFrame(results)


def get_taboola_publisher_performance(api, start_date, end_date):
    """Get performance by publisher."""
    url = f"{api.base_url}/{api.account_id}/reports/top-campaign-content/dimensions/site_day"

    params = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
    }

    response = requests.get(url, headers=api.headers, params=params)
    return response.json()
```

**Outbrain Performance Reports:**
```python
def get_outbrain_campaign_report(api, start_date, end_date):
    """Get Outbrain campaign performance."""
    url = f"{api.base_url}/reports/marketers/{api.account_id}/campaigns"

    params = {
        "from": start_date.strftime("%Y-%m-%d"),
        "to": end_date.strftime("%Y-%m-%d"),
        "breakdown": "daily",
        "includeArchivedCampaigns": False,
    }

    response = requests.get(url, headers=api.headers, params=params)
    data = response.json()

    results = []
    for campaign in data.get("campaigns", []):
        for metric in campaign.get("metrics", []):
            results.append({
                'campaign_id': campaign.get('id'),
                'campaign_name': campaign.get('name'),
                'date': metric.get('fromDate'),
                'impressions': metric.get('impressions', 0),
                'clicks': metric.get('clicks', 0),
                'ctr': metric.get('ctr', 0),
                'spend': metric.get('spend', 0),
                'ecpc': metric.get('ecpc', 0),
                'conversions': metric.get('conversions', 0),
                'cpa': metric.get('cpa', 0),
            })

    return pd.DataFrame(results)


def get_outbrain_promoted_link_report(api, campaign_id, start_date, end_date):
    """Get promoted link (ad) performance."""
    url = f"{api.base_url}/reports/marketers/{api.account_id}/campaigns/{campaign_id}/promotedLinks"

    params = {
        "from": start_date.strftime("%Y-%m-%d"),
        "to": end_date.strftime("%Y-%m-%d"),
        "sort": "spend",
        "limit": 100,
    }

    response = requests.get(url, headers=api.headers, params=params)
    return response.json()


def get_outbrain_publisher_report(api, campaign_id, start_date, end_date):
    """Get performance by publisher."""
    url = f"{api.base_url}/reports/marketers/{api.account_id}/campaigns/{campaign_id}/publishersPerformance"

    params = {
        "from": start_date.strftime("%Y-%m-%d"),
        "to": end_date.strftime("%Y-%m-%d"),
    }

    response = requests.get(url, headers=api.headers, params=params)
    return response.json()
```

### 4. Optimization and Management

**Bid Optimization:**
```python
def optimize_taboola_campaign_bids(api, campaign_id, performance_data,
                                   target_cpa=None, min_cpc=0.10, max_cpc=2.00):
    """Optimize campaign bids based on performance."""
    url = f"{api.base_url}/{api.account_id}/campaigns/{campaign_id}"

    current_cpc = performance_data['cpc']
    actual_cpa = performance_data.get('cpa', 0)

    if target_cpa and actual_cpa > 0:
        # Calculate optimal CPC based on conversion rate
        conversion_rate = performance_data.get('conversions', 0) / performance_data.get('clicks', 1)
        optimal_cpc = target_cpa * conversion_rate

        # Conservative adjustment
        if optimal_cpc > current_cpc:
            new_cpc = min(current_cpc * 1.10, optimal_cpc, max_cpc)
        else:
            new_cpc = max(current_cpc * 0.90, optimal_cpc, min_cpc)

        data = {
            "cpc": round(new_cpc, 2)
        }

        response = requests.patch(url, headers=api.headers, json=data)
        return response.json()

    return {"message": "Insufficient data for optimization"}


def pause_underperforming_items(api, campaign_id, performance_threshold):
    """Pause campaign items below performance threshold."""
    # Get item performance
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    items_df = get_taboola_top_campaign_content(api, campaign_id, start_date, end_date)

    # Identify underperformers
    underperformers = items_df[items_df['ctr'] < performance_threshold]

    for _, item in underperformers.iterrows():
        url = f"{api.base_url}/{api.account_id}/campaigns/{campaign_id}/items/{item['item_id']}"

        data = {
            "is_active": False
        }

        requests.patch(url, headers=api.headers, json=data)

    return underperformers


def block_poor_performing_publishers(api, campaign_id, min_ctr=0.01):
    """Block publishers with poor performance."""
    # Get publisher performance
    end_date = datetime.now()
    start_date = end_date - timedelta(days=14)

    publisher_data = get_taboola_publisher_performance(api, start_date, end_date)

    # Identify poor performers
    poor_publishers = []
    for pub in publisher_data.get("results", []):
        if pub.get('ctr', 0) < min_ctr and pub.get('clicks', 0) > 100:
            poor_publishers.append(pub['site'])

    # Block publishers
    if poor_publishers:
        set_publisher_targeting(api, campaign_id, {
            "type": "EXCLUDE",
            "publisher_ids": poor_publishers
        })

    return poor_publishers
```

## Installation and Authentication

### Install Required Libraries

```bash
pip install requests pandas
```

### Set Up Authentication

**Taboola:**
1. Create account at https://www.taboola.com/
2. Access Backstage (Taboola's management platform)
3. Generate API credentials:
   - Client ID
   - Client Secret
4. Get Account ID from Backstage

**Outbrain:**
1. Create account at https://www.outbrain.com/
2. Access Amplify dashboard
3. Generate API credentials (username and password)
4. Get Marketer ID from dashboard

### Initialize API Clients

```python
# Taboola
taboola_api = TaboolaAPI(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    account_id="YOUR_ACCOUNT_ID"
)

# Outbrain
outbrain_api = OutbrainAPI(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    account_id="YOUR_MARKETER_ID"
)
```

## Quick Start Example

```python
from datetime import datetime, timedelta

# Taboola Example
taboola_api = TaboolaAPI(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    account_id="YOUR_ACCOUNT_ID"
)

# Create campaign
campaign = taboola_api.create_campaign(
    name="Blog Traffic Campaign",
    branding_text="Your Brand",
    cpc=0.25,
    daily_cap=100
)

# Add content
item = taboola_api.create_campaign_item(
    campaign_id=campaign['id'],
    url="https://yourblog.com/article",
    title="10 Ways to Boost Your Marketing",
    thumbnail_url="https://yourblog.com/image.jpg"
)

# Get performance
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

df = get_taboola_campaign_report(taboola_api, start_date, end_date)
print(f"Total Clicks: {df['clicks'].sum():,}")
print(f"Average CTR: {df['ctr'].mean():.2%}")
print(f"Total Spent: ${df['spent'].sum():.2f}")
```

## Key Metrics Reference

### Performance Metrics
- **Impressions** - Number of times content was shown
- **Clicks** - Number of clicks on content
- **CTR** - Click-through rate
- **CPC** - Cost per click
- **Spent** - Total amount spent
- **Visible Impressions** - Viewable impressions
- **Viewability Rate** - Percentage of viewable impressions

### Engagement Metrics
- **Conversions** - Conversion events
- **CPA** - Cost per acquisition
- **Conversion Rate** - Conversions / Clicks
- **Video Completion Rate** - For video content
- **Time on Site** - Average time spent on landing page
- **Bounce Rate** - Percentage of single-page sessions

### Content Performance
- **Top Performing Headlines** - Best CTR by title
- **Top Performing Images** - Best CTR by thumbnail
- **Best Publishers** - Highest performing sites
- **Device Performance** - Desktop vs mobile vs tablet

## Best Practices

1. **Content Strategy**
   - Use curiosity-driven headlines
   - Test multiple headline variations
   - Use high-quality, relevant images
   - Ensure landing pages load quickly
   - Match content to headline promise

2. **Targeting Strategy**
   - Start broad, refine based on data
   - Test different device types
   - Target premium publishers
   - Exclude poor-performing sites
   - Use geographic targeting strategically

3. **Bidding Strategy**
   - Start with platform recommended CPC
   - Adjust based on CTR and conversion data
   - Bid higher for top-performing publishers
   - Set daily budgets to control spend
   - Monitor and adjust frequently

4. **Creative Testing**
   - Test 3-5 headlines per campaign
   - Test different image styles
   - Refresh creative monthly
   - Pause low CTR variants
   - Scale winners

5. **Performance Optimization**
   - Monitor CTR daily
   - Block low-performing publishers
   - Optimize bids by publisher
   - Track engagement metrics
   - Focus on cost per engagement, not just clicks

## Common Use Cases

### Content Distribution
```python
def distribute_blog_content(taboola_api, outbrain_api, article_url, budget):
    """Distribute content across both platforms."""
    # Create campaigns on both platforms
    # Test different headlines
    # Monitor cross-platform performance
    pass
```

### Lead Generation
```python
def create_lead_gen_campaign(api, landing_page_url, lead_magnet):
    """Create campaign for lead generation."""
    # Create campaign with conversion tracking
    # Test headlines focused on value proposition
    # Optimize for cost per lead
    pass
```

### E-commerce Traffic
```python
def drive_product_traffic(api, product_urls, images):
    """Drive traffic to e-commerce products."""
    # Create product-specific campaigns
    # Use product images
    # Track conversion and ROAS
    pass
```

## References

**Taboola:**
- **Official Documentation**: https://developers.taboola.com/backstage-api/reference
- **API Reference**: https://developers.taboola.com/backstage-api/docs
- **Best Practices**: https://help.taboola.com/
- **Creative Specs**: https://help.taboola.com/hc/en-us/articles/115005704987
- **Support**: https://help.taboola.com/

**Outbrain:**
- **Official Documentation**: https://www.outbrain.com/amplify/api
- **API Reference**: https://amplifyv01.docs.apiary.io/
- **Best Practices**: https://www.outbrain.com/blog/
- **Creative Guidelines**: https://www.outbrain.com/help/advertisers/
- **Support**: https://www.outbrain.com/help/

**General:**
- **Native Advertising Institute**: https://nativeadvertisinginstitute.com/
- **IAB Native Ad Guidelines**: https://www.iab.com/guidelines/native-advertising/

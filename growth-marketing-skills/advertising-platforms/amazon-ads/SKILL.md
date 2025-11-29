---
name: amazon-ads
description: "Amazon Ads API for e-commerce advertising. Manage Sponsored Products, Sponsored Brands, Sponsored Display, DSP campaigns, product targeting, and analytics for Amazon marketplace."
---

# Amazon Ads

## Overview

Amazon Ads provides access to one of the world's largest e-commerce platforms with high purchase intent audiences. The Amazon Advertising API enables programmatic management of Sponsored Products, Sponsored Brands, Sponsored Display, and Amazon DSP campaigns, along with comprehensive analytics for marketplace advertising.

This skill covers the Amazon Advertising API with Python, enabling automated campaign creation, product targeting, bid optimization, and performance tracking for e-commerce success on Amazon.

## When to Use This Skill

Use this skill when you need to:
- Create and manage Amazon advertising campaigns programmatically
- Optimize Sponsored Products for product visibility
- Manage Sponsored Brands for brand awareness
- Automate product and keyword targeting
- Generate detailed sales and advertising reports
- Manage large product catalogs at scale
- Implement dynamic bidding strategies
- Track advertising cost of sales (ACoS) and return on ad spend (ROAS)
- Manage Amazon DSP campaigns for programmatic display
- Sync inventory and advertising performance
- Optimize for organic rank and conversions

## Core Capabilities

### 1. Sponsored Products Campaign Management

**Create Sponsored Products Campaign:**
```python
import requests
import json

class AmazonAdsAPI:
    """Amazon Advertising API client."""

    def __init__(self, access_token, client_id, profile_id):
        self.access_token = access_token
        self.client_id = client_id
        self.profile_id = profile_id
        self.base_url = "https://advertising-api.amazon.com"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Amazon-Advertising-API-ClientId": client_id,
            "Amazon-Advertising-API-Scope": profile_id,
            "Content-Type": "application/json",
        }

    def create_sp_campaign(self, name, campaign_type, targeting_type,
                          daily_budget, start_date=None, end_date=None):
        """Create a Sponsored Products campaign."""
        url = f"{self.base_url}/v2/sp/campaigns"

        data = {
            "name": name,
            "campaignType": campaign_type,  # sponsoredProducts
            "targetingType": targeting_type,  # manual, auto
            "state": "paused",
            "dailyBudget": daily_budget,
            "startDate": start_date or datetime.now().strftime("%Y%m%d"),
            "premiumBidAdjustment": True,
            "bidding": {
                "strategy": "legacyForSales",  # legacyForSales, autoForSales, manual
                "adjustments": [{
                    "predicate": "placementTop",
                    "percentage": 50  # Bid adjustment for top of search
                }, {
                    "predicate": "placementProductPage",
                    "percentage": 25  # Bid adjustment for product pages
                }]
            }
        }

        if end_date:
            data["endDate"] = end_date

        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def create_sp_ad_group(self, campaign_id, name, default_bid):
        """Create an ad group for Sponsored Products."""
        url = f"{self.base_url}/v2/sp/adGroups"

        data = {
            "campaignId": campaign_id,
            "name": name,
            "defaultBid": default_bid,
            "state": "enabled"
        }

        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def create_sp_product_ads(self, ad_group_id, sku_list):
        """Create product ads from SKU list."""
        url = f"{self.base_url}/v2/sp/productAds"

        ads = []
        for sku in sku_list:
            ads.append({
                "adGroupId": ad_group_id,
                "sku": sku,
                "state": "enabled"
            })

        response = requests.post(url, headers=self.headers, json=ads)
        return response.json()


# Keyword targeting
def create_sp_keywords(api, ad_group_id, keywords_data):
    """Add keywords to Sponsored Products ad group."""
    url = f"{api.base_url}/v2/sp/keywords"

    keywords = []
    for keyword_text, match_type, bid in keywords_data:
        keywords.append({
            "adGroupId": ad_group_id,
            "keywordText": keyword_text,
            "matchType": match_type,  # exact, phrase, broad
            "bid": bid,
            "state": "enabled"
        })

    response = requests.post(url, headers=api.headers, json=keywords)
    return response.json()


# Product targeting
def create_sp_product_targets(api, ad_group_id, targets):
    """Add product targeting to ad group."""
    url = f"{api.base_url}/v2/sp/targets"

    product_targets = []
    for target_asin, bid in targets:
        product_targets.append({
            "adGroupId": ad_group_id,
            "expressionType": "manual",
            "expression": [{
                "type": "asinCategorySameAs",
                "value": target_asin
            }],
            "bid": bid,
            "state": "enabled"
        })

    response = requests.post(url, headers=api.headers, json=product_targets)
    return response.json()


# Negative keywords
def create_negative_keywords(api, ad_group_id, negative_keywords):
    """Add negative keywords to ad group."""
    url = f"{api.base_url}/v2/sp/negativeKeywords"

    neg_keywords = []
    for keyword_text, match_type in negative_keywords:
        neg_keywords.append({
            "adGroupId": ad_group_id,
            "keywordText": keyword_text,
            "matchType": match_type,  # negativeExact, negativePhrase
            "state": "enabled"
        })

    response = requests.post(url, headers=api.headers, json=neg_keywords)
    return response.json()
```

### 2. Sponsored Brands Campaigns

**Create Sponsored Brands Campaign:**
```python
def create_sb_campaign(api, name, budget, start_date, creative_type="brandVideo"):
    """Create a Sponsored Brands campaign."""
    url = f"{api.base_url}/v2/hsa/campaigns"

    data = {
        "name": name,
        "budget": budget,
        "budgetType": "daily",
        "startDate": start_date,
        "state": "paused",
        "creative": {
            "brandEntityId": "ENTITY123",  # Brand entity ID
            "brandLogoAssetID": "ASSET123",  # Logo asset ID
            "headline": "Shop Our Products",
        }
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def create_sb_ad_group(api, campaign_id, name, keywords):
    """Create Sponsored Brands ad group with keywords."""
    url = f"{api.base_url}/v2/hsa/adGroups"

    data = {
        "campaignId": campaign_id,
        "name": name,
        "state": "enabled"
    }

    response = requests.post(url, headers=api.headers, json=data)
    ad_group_id = response.json().get("adGroupId")

    # Add keywords
    keyword_url = f"{api.base_url}/v2/hsa/keywords"
    keyword_data = []

    for keyword_text, match_type, bid in keywords:
        keyword_data.append({
            "adGroupId": ad_group_id,
            "keywordText": keyword_text,
            "matchType": match_type,
            "bid": bid,
            "state": "enabled"
        })

    requests.post(keyword_url, headers=api.headers, json=keyword_data)

    return response.json()
```

### 3. Sponsored Display Campaigns

**Create Sponsored Display Campaign:**
```python
def create_sd_campaign(api, name, budget, tactic="T00020"):
    """Create a Sponsored Display campaign."""
    url = f"{api.base_url}/sd/campaigns"

    data = {
        "name": name,
        "budget": budget,
        "budgetType": "daily",
        "startDate": datetime.now().strftime("%Y%m%d"),
        "tactic": tactic,  # T00020: Audiences, T00030: Contextual
        "state": "paused",
        "costType": "cpc"
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def create_sd_ad_group(api, campaign_id, name, default_bid, tactic_type="remarketing"):
    """Create Sponsored Display ad group."""
    url = f"{api.base_url}/sd/adGroups"

    data = {
        "campaignId": campaign_id,
        "name": name,
        "defaultBid": default_bid,
        "state": "enabled",
        "tactic": tactic_type  # remarketing, audiences, contextual
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def create_sd_product_ads(api, ad_group_id, asin_list):
    """Create Sponsored Display product ads."""
    url = f"{api.base_url}/sd/productAds"

    ads = []
    for asin in asin_list:
        ads.append({
            "adGroupId": ad_group_id,
            "asin": asin,
            "state": "enabled"
        })

    response = requests.post(url, headers=api.headers, json=ads)
    return response.json()


# Audience targeting for SD
def create_sd_audience_targets(api, ad_group_id, audience_id, bid):
    """Add audience targeting to Sponsored Display ad group."""
    url = f"{api.base_url}/sd/targets"

    data = [{
        "adGroupId": ad_group_id,
        "expressionType": "auto",
        "expression": [{
            "type": "audience",
            "value": audience_id
        }],
        "bid": bid,
        "state": "enabled"
    }]

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()
```

### 4. Reporting and Analytics

**Campaign Performance Reports:**
```python
import pandas as pd
from datetime import datetime, timedelta

def get_sp_campaign_report(api, start_date, end_date, metrics=None):
    """Get Sponsored Products campaign report."""
    url = f"{api.base_url}/v2/sp/campaigns/report"

    data = {
        "reportDate": start_date.strftime("%Y%m%d"),
        "metrics": metrics or [
            "campaignName",
            "campaignId",
            "impressions",
            "clicks",
            "cost",
            "sales7d",
            "orders7d",
            "units7d",
            "attributedConversions7d",
            "attributedSales7d"
        ]
    }

    # Request report
    response = requests.post(url, headers=api.headers, json=data)
    report_id = response.json().get("reportId")

    # Poll for report completion
    import time
    status_url = f"{api.base_url}/v2/reports/{report_id}"

    while True:
        status_response = requests.get(status_url, headers=api.headers)
        status = status_response.json().get("status")

        if status == "SUCCESS":
            download_url = status_response.json().get("location")
            break
        elif status == "FAILURE":
            raise Exception("Report generation failed")

        time.sleep(5)

    # Download report
    report_data = requests.get(download_url, headers=api.headers)

    # Parse JSON report
    import gzip
    import json

    decompressed = gzip.decompress(report_data.content)
    report_json = json.loads(decompressed)

    return pd.DataFrame(report_json)


def get_keyword_report(api, start_date, end_date):
    """Get keyword performance report."""
    url = f"{api.base_url}/v2/sp/keywords/report"

    data = {
        "reportDate": start_date.strftime("%Y%m%d"),
        "metrics": [
            "keywordText",
            "keywordId",
            "matchType",
            "impressions",
            "clicks",
            "cost",
            "ctr",
            "cpc",
            "sales7d",
            "acos7d",
            "roas7d"
        ]
    }

    response = requests.post(url, headers=api.headers, json=data)
    report_id = response.json().get("reportId")

    # Similar polling and download process as above
    # Returns DataFrame with keyword performance
    pass


def get_search_term_report(api, start_date, end_date):
    """Get search term (customer search query) report."""
    url = f"{api.base_url}/v2/sp/targets/report"

    data = {
        "reportDate": start_date.strftime("%Y%m%d"),
        "metrics": [
            "query",
            "impressions",
            "clicks",
            "cost",
            "sales7d",
            "purchases7d"
        ],
        "segment": "query"
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def get_product_performance(api, start_date, end_date):
    """Get advertised product performance."""
    url = f"{api.base_url}/v2/sp/productAds/report"

    data = {
        "reportDate": start_date.strftime("%Y%m%d"),
        "metrics": [
            "asin",
            "sku",
            "impressions",
            "clicks",
            "cost",
            "sales7d",
            "orders7d",
            "units7d",
            "acos7d"
        ]
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()
```

### 5. Bid Optimization

**Automated Bid Management:**
```python
def optimize_keyword_bids(api, performance_data, target_acos=0.25):
    """Optimize keyword bids based on ACoS target."""
    url = f"{api.base_url}/v2/sp/keywords"

    bid_updates = []

    for _, row in performance_data.iterrows():
        keyword_id = row['keywordId']
        current_bid = row['bid']
        acos = row['acos7d']
        clicks = row['clicks']

        # Only adjust if we have enough data
        if clicks < 10:
            continue

        # Calculate new bid
        if acos < target_acos * 0.8:  # Performing well, increase bid
            new_bid = current_bid * 1.15
        elif acos > target_acos * 1.2:  # Poor performance, decrease bid
            new_bid = current_bid * 0.85
        else:
            continue

        # Ensure bid stays within bounds
        new_bid = max(0.02, min(new_bid, 10.00))

        bid_updates.append({
            "keywordId": keyword_id,
            "bid": round(new_bid, 2),
            "state": "enabled"
        })

    # Update bids
    if bid_updates:
        response = requests.put(url, headers=api.headers, json=bid_updates)
        return response.json()

    return {"message": "No bid updates needed"}


def adjust_campaign_budgets(api, campaign_performance, budget_cap):
    """Adjust campaign daily budgets based on performance."""
    url = f"{api.base_url}/v2/sp/campaigns"

    budget_updates = []

    for _, row in campaign_performance.iterrows():
        campaign_id = row['campaignId']
        current_budget = row['dailyBudget']
        spend = row['cost']
        sales = row['sales7d']
        roas = sales / spend if spend > 0 else 0

        # Increase budget for high-performing campaigns
        if roas > 3.0 and spend >= current_budget * 0.9:
            new_budget = min(current_budget * 1.2, budget_cap)
        # Decrease budget for low performers
        elif roas < 1.5:
            new_budget = current_budget * 0.8
        else:
            continue

        budget_updates.append({
            "campaignId": campaign_id,
            "dailyBudget": round(new_budget, 2)
        })

    if budget_updates:
        response = requests.put(url, headers=api.headers, json=budget_updates)
        return response.json()

    return {"message": "No budget updates needed"}
```

## Installation and Authentication

### Install Required Libraries

```bash
pip install requests pandas
```

### Set Up Authentication

1. **Create Amazon Seller or Vendor Account**
2. **Register for Amazon Advertising API** at https://advertising.amazon.com/API/
3. **Create App** and get credentials:
   - Client ID
   - Client Secret
4. **Generate Access Token** using OAuth 2.0 flow with LWA (Login with Amazon)
5. **Get Profile ID** for your advertising account

### Initialize API Client

```python
import requests

class AmazonAdsAPI:
    def __init__(self, access_token, client_id, profile_id):
        self.access_token = access_token
        self.client_id = client_id
        self.profile_id = profile_id
        self.base_url = "https://advertising-api.amazon.com"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Amazon-Advertising-API-ClientId": client_id,
            "Amazon-Advertising-API-Scope": profile_id,
            "Content-Type": "application/json",
        }

# Initialize
api = AmazonAdsAPI(
    access_token="YOUR_ACCESS_TOKEN",
    client_id="YOUR_CLIENT_ID",
    profile_id="YOUR_PROFILE_ID"
)
```

## Quick Start Example

```python
from datetime import datetime, timedelta

# Initialize API
api = AmazonAdsAPI(
    access_token="YOUR_ACCESS_TOKEN",
    client_id="YOUR_CLIENT_ID",
    profile_id="YOUR_PROFILE_ID"
)

# Create Sponsored Products campaign
campaign = api.create_sp_campaign(
    name="Summer Sale Campaign",
    campaign_type="sponsoredProducts",
    targeting_type="manual",
    daily_budget=50.00
)

campaign_id = campaign["campaignId"]

# Create ad group
ad_group = api.create_sp_ad_group(
    campaign_id=campaign_id,
    name="Main Products",
    default_bid=0.75
)

# Get performance report
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()

df = get_sp_campaign_report(api, start_date, end_date)
print(f"Total Sales: ${df['sales7d'].sum():.2f}")
print(f"Average ACoS: {(df['cost'].sum() / df['sales7d'].sum()):.2%}")
```

## Key Metrics Reference

### Performance Metrics
- **Impressions** - Number of times ad was shown
- **Clicks** - Number of clicks
- **CTR** - Click-through rate
- **CPC** - Cost per click
- **Spend** - Total advertising cost

### Sales Metrics
- **Sales (7d/14d/30d)** - Attributed sales within attribution window
- **Orders** - Number of orders attributed to ads
- **Units** - Number of units sold
- **ROAS** - Return on ad spend (Sales / Spend)
- **ACoS** - Advertising cost of sales (Spend / Sales)

### Conversion Metrics
- **Conversion Rate** - Orders / Clicks
- **Detail Page Views** - Product page views from ads
- **Add to Cart** - Products added to cart
- **Subscribe & Save** - Subscription sign-ups

### Organic Impact Metrics
- **Organic Sales** - Non-attributed organic sales
- **Total Sales** - Attributed + Organic sales
- **TACoS** - Total advertising cost of sales (Spend / Total Sales)

## Best Practices

1. **Campaign Structure**
   - Separate campaigns by product category
   - Use single-keyword ad groups for better control
   - Create exact match campaigns for high-performers
   - Implement negative keyword harvesting

2. **Targeting Strategy**
   - Start with automatic campaigns for keyword discovery
   - Graduate high-performers to manual campaigns
   - Use product targeting for competitor ASINs
   - Implement category targeting for broad reach

3. **Bid Management**
   - Target 15-30% ACoS for new products
   - Optimize for profitability, not just ACoS
   - Adjust bids by placement (top of search premium)
   - Use dayparting for optimal timing

4. **Budget Allocation**
   - Allocate more budget to high-ROAS campaigns
   - Ensure budget isn't capping high performers
   - Monitor impression share metrics
   - Reserve budget for peak seasons

5. **Keyword Strategy**
   - Mine search term reports weekly
   - Add negatives to prevent wasted spend
   - Test all match types (exact, phrase, broad)
   - Focus on high-intent commercial keywords

## Common Use Cases

### Keyword Harvesting
```python
def harvest_keywords_from_auto_campaigns(api, auto_campaign_id):
    """Extract performing search terms from auto campaigns."""
    # Get search term report
    # Identify high-performing terms
    # Add to manual campaigns
    # Add negatives for poor performers
    pass
```

### Competitor Targeting
```python
def target_competitor_products(api, ad_group_id, competitor_asins):
    """Target competitor product pages."""
    # Create product targeting for competitor ASINs
    # Set competitive bids
    # Monitor conversion rates
    pass
```

### Seasonal Budget Management
```python
def adjust_budgets_for_season(api, season_multiplier):
    """Scale budgets for seasonal demand."""
    # Identify seasonal campaigns
    # Apply multiplier to budgets
    # Monitor inventory levels
    pass
```

## References

- **Official Documentation**: https://advertising.amazon.com/API/docs/
- **Sponsored Products API**: https://advertising.amazon.com/API/docs/en-us/sponsored-products/
- **Sponsored Brands API**: https://advertising.amazon.com/API/docs/en-us/sponsored-brands/
- **Sponsored Display API**: https://advertising.amazon.com/API/docs/en-us/sponsored-display/
- **Amazon DSP**: https://advertising.amazon.com/solutions/products/amazon-dsp
- **Attribution API**: https://advertising.amazon.com/API/docs/en-us/amazon-attribution/
- **Best Practices**: https://advertising.amazon.com/resources/
- **Developer Portal**: https://developer.amazon.com/
- **Support**: https://advertising.amazon.com/contact-us

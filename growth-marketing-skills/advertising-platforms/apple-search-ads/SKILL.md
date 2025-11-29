---
name: apple-search-ads
description: "Apple Search Ads API for App Store advertising. Manage search campaigns, keyword targeting, creative sets, audience refinement, and analytics for iOS app promotion."
---

# Apple Search Ads

## Overview

Apple Search Ads enables advertising in the App Store search results, reaching users actively searching for apps. The Apple Search Ads API provides programmatic access to create campaigns, manage keywords, optimize bids, and track performance for iOS and iPadOS app promotion.

This skill covers the Apple Search Ads API with Python, enabling automated campaign management, keyword optimization, and performance tracking for app growth and user acquisition.

## When to Use This Skill

Use this skill when you need to:
- Create and manage App Store search advertising campaigns
- Promote iOS, iPadOS, and macOS apps programmatically
- Target users actively searching for apps in the App Store
- Automate keyword bidding and optimization
- Generate detailed app download and conversion reports
- Manage large-scale keyword portfolios
- Implement audience refinement strategies
- Track cost per acquisition (CPA) and lifetime value (LTV)
- A/B test creative sets and custom product pages
- Optimize for app installs and in-app events
- Monitor competitor keyword performance

## Core Capabilities

### 1. Campaign Management

**Create Search Campaign:**
```python
import requests
import json
from datetime import datetime

class AppleSearchAdsAPI:
    """Apple Search Ads API client."""

    def __init__(self, client_id, team_id, key_id, private_key):
        self.client_id = client_id
        self.team_id = team_id
        self.key_id = key_id
        self.private_key = private_key
        self.base_url = "https://api.searchads.apple.com/api/v4"
        self.access_token = self._generate_access_token()

    def _generate_access_token(self):
        """Generate JWT access token for API authentication."""
        import jwt
        import time

        payload = {
            "iss": self.team_id,
            "iat": int(time.time()),
            "exp": int(time.time()) + 86400,  # 24 hours
            "aud": "https://appleid.apple.com",
            "sub": self.client_id
        }

        headers = {
            "alg": "ES256",
            "kid": self.key_id
        }

        token = jwt.encode(payload, self.private_key, algorithm="ES256", headers=headers)
        return token

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-AP-Context": f"orgId={self.org_id}"
        }

    def create_campaign(self, org_id, name, budget_amount, daily_budget_amount,
                       adam_id, countries, billing_event="TAPS"):
        """Create a new campaign."""
        url = f"{self.base_url}/campaigns"

        data = {
            "name": name,
            "budgetAmount": {
                "amount": str(budget_amount),
                "currency": "USD"
            },
            "dailyBudgetAmount": {
                "amount": str(daily_budget_amount),
                "currency": "USD"
            },
            "adamId": adam_id,  # App ID from App Store Connect
            "countriesOrRegions": countries,  # ["US", "GB", etc.]
            "billingEvent": billing_event,  # TAPS (CPC) or IMPRESSIONS (CPM)
            "status": "PAUSED",
            "supplySources": ["APPSTORE_SEARCH_RESULTS"],
            "locInvoiceDetails": {
                "clientName": "Your Company",
                "orderNumber": "ORDER123",
                "buyerName": "Buyer Name",
                "buyerEmail": "buyer@example.com"
            }
        }

        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def create_ad_group(self, campaign_id, name, cpa_goal=None, default_bid_amount=None,
                       start_time=None, end_time=None):
        """Create an ad group."""
        url = f"{self.base_url}/campaigns/{campaign_id}/adgroups"

        data = {
            "name": name,
            "status": "PAUSED",
            "defaultBidAmount": {
                "amount": str(default_bid_amount or "0.50"),
                "currency": "USD"
            },
            "automatedKeywordsOptIn": False,  # Use Search Match
        }

        if cpa_goal:
            data["cpaGoal"] = {
                "amount": str(cpa_goal),
                "currency": "USD"
            }

        if start_time:
            data["startTime"] = start_time.isoformat()

        if end_time:
            data["endTime"] = end_time.isoformat()

        response = requests.post(url, headers=self.headers, json=data)
        return response.json()


def create_keywords(api, campaign_id, ad_group_id, keywords_data):
    """Add keywords to ad group."""
    url = f"{api.base_url}/campaigns/{campaign_id}/adgroups/{ad_group_id}/targetingkeywords"

    keywords = []
    for keyword_text, match_type, bid_amount in keywords_data:
        keywords.append({
            "text": keyword_text,
            "matchType": match_type,  # EXACT, BROAD
            "bidAmount": {
                "amount": str(bid_amount),
                "currency": "USD"
            },
            "status": "ACTIVE"
        })

    response = requests.post(url, headers=api.headers, json=keywords)
    return response.json()


def create_negative_keywords(api, campaign_id, ad_group_id, negative_keywords):
    """Add negative keywords to ad group."""
    url = f"{api.base_url}/campaigns/{campaign_id}/adgroups/{ad_group_id}/negativekeywords"

    neg_keywords = []
    for keyword_text, match_type in negative_keywords:
        neg_keywords.append({
            "text": keyword_text,
            "matchType": match_type,  # EXACT, BROAD
            "status": "ACTIVE"
        })

    response = requests.post(url, headers=api.headers, json=neg_keywords)
    return response.json()


# Search Match (automatic keyword targeting)
def enable_search_match(api, campaign_id, ad_group_id):
    """Enable Search Match for automatic keyword discovery."""
    url = f"{api.base_url}/campaigns/{campaign_id}/adgroups/{ad_group_id}"

    data = {
        "automatedKeywordsOptIn": True
    }

    response = requests.put(url, headers=api.headers, json=data)
    return response.json()
```

**Creative Sets and Custom Product Pages:**
```python
def create_creative_set(api, campaign_id, ad_group_id, name, language_code,
                       asset_links=None):
    """Create a creative set for A/B testing."""
    url = f"{api.base_url}/campaigns/{campaign_id}/adgroups/{ad_group_id}/creativesets"

    data = {
        "name": name,
        "languageCode": language_code,  # "en-US", etc.
        "assetsGenIds": asset_links,  # Asset generation IDs
        "status": "VALID"
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def assign_custom_product_page(api, campaign_id, ad_group_id, creative_set_id,
                               custom_product_page_id):
    """Assign custom product page to creative set."""
    url = f"{api.base_url}/campaigns/{campaign_id}/adgroups/{ad_group_id}/creativesets/{creative_set_id}"

    data = {
        "customProductPageId": custom_product_page_id
    }

    response = requests.put(url, headers=api.headers, json=data)
    return response.json()
```

### 2. Reporting and Analytics

**Campaign Performance Reports:**
```python
import pandas as pd
from datetime import datetime, timedelta

def get_campaign_report(api, org_id, start_date, end_date, granularity="DAILY"):
    """Get campaign performance report."""
    url = f"{api.base_url}/reports/campaigns"

    data = {
        "startTime": start_date.isoformat(),
        "endTime": end_date.isoformat(),
        "granularity": granularity,  # HOURLY, DAILY, MONTHLY, TOTAL
        "selector": {
            "orderBy": [
                {
                    "field": "localSpend",
                    "sortOrder": "DESCENDING"
                }
            ],
            "conditions": [
                {
                    "field": "deleted",
                    "operator": "EQUALS",
                    "values": ["false"]
                }
            ]
        },
        "groupBy": ["countryOrRegion"],
        "returnRowTotals": True,
        "returnRecordsWithNoMetrics": False
    }

    response = requests.post(url, headers=api.headers, json=data)
    report_data = response.json()

    results = []
    for row in report_data.get("data", {}).get("reportingDataResponse", {}).get("row", []):
        metadata = row.get("metadata", {})
        totals = row.get("total", {})

        results.append({
            'campaign_id': metadata.get('campaignId'),
            'campaign_name': metadata.get('campaignName'),
            'country': metadata.get('countryOrRegion'),
            'date': metadata.get('date'),
            'impressions': totals.get('impressions', 0),
            'taps': totals.get('taps', 0),
            'installs': totals.get('installs', 0),
            'new_downloads': totals.get('newDownloads', 0),
            'redownloads': totals.get('redownloads', 0),
            'spend': float(totals.get('localSpend', {}).get('amount', 0)),
            'avg_cpt': float(totals.get('avgCPT', {}).get('amount', 0)),
            'avg_cpa': float(totals.get('avgCPA', {}).get('amount', 0)),
            'ttr': float(totals.get('ttr', 0)),
            'conversion_rate': float(totals.get('conversionRate', 0)),
        })

    return pd.DataFrame(results)


def get_keyword_report(api, org_id, campaign_id, start_date, end_date):
    """Get keyword performance report."""
    url = f"{api.base_url}/reports/campaigns/{campaign_id}/keywords"

    data = {
        "startTime": start_date.isoformat(),
        "endTime": end_date.isoformat(),
        "granularity": "DAILY",
        "selector": {
            "orderBy": [
                {
                    "field": "localSpend",
                    "sortOrder": "DESCENDING"
                }
            ]
        }
    }

    response = requests.post(url, headers=api.headers, json=data)
    report_data = response.json()

    results = []
    for row in report_data.get("data", {}).get("reportingDataResponse", {}).get("row", []):
        metadata = row.get("metadata", {})
        totals = row.get("total", {})

        results.append({
            'keyword_id': metadata.get('keywordId'),
            'keyword': metadata.get('keyword'),
            'match_type': metadata.get('matchType'),
            'bid_amount': float(metadata.get('bidAmount', {}).get('amount', 0)),
            'impressions': totals.get('impressions', 0),
            'taps': totals.get('taps', 0),
            'installs': totals.get('installs', 0),
            'spend': float(totals.get('localSpend', {}).get('amount', 0)),
            'avg_cpa': float(totals.get('avgCPA', {}).get('amount', 0)),
            'ttr': float(totals.get('ttr', 0)),
            'conversion_rate': float(totals.get('conversionRate', 0)),
        })

    return pd.DataFrame(results)


def get_search_terms_report(api, campaign_id, ad_group_id, start_date, end_date):
    """Get search terms that triggered ads."""
    url = f"{api.base_url}/reports/campaigns/{campaign_id}/adgroups/{ad_group_id}/searchterms"

    data = {
        "startTime": start_date.isoformat(),
        "endTime": end_date.isoformat(),
        "granularity": "DAILY",
        "returnRowTotals": True
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def get_creative_set_report(api, campaign_id, start_date, end_date):
    """Get creative set performance for A/B testing."""
    url = f"{api.base_url}/reports/campaigns/{campaign_id}/creativesets"

    data = {
        "startTime": start_date.isoformat(),
        "endTime": end_date.isoformat(),
        "granularity": "TOTAL"
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()
```

### 3. Audience Refinement

**Apply Audience Targeting:**
```python
def set_audience_refinement(api, campaign_id, ad_group_id, demographics=None,
                           device_class=None, app_downloader=None):
    """Apply audience refinement to ad group."""
    url = f"{api.base_url}/campaigns/{campaign_id}/adgroups/{ad_group_id}"

    targeting_dimensions = {}

    # Age targeting
    if demographics and 'age' in demographics:
        targeting_dimensions['age'] = {
            "included": demographics['age']  # ["18-24", "25-34", etc.]
        }

    # Gender targeting
    if demographics and 'gender' in demographics:
        targeting_dimensions['gender'] = {
            "included": demographics['gender']  # ["M", "F"]
        }

    # Device class targeting
    if device_class:
        targeting_dimensions['deviceClass'] = {
            "included": device_class  # ["IPHONE", "IPAD"]
        }

    # App downloader targeting
    if app_downloader:
        targeting_dimensions['appDownloaders'] = {
            "included": app_downloader
            # ["ALL_USERS", "NEW_USERS", "EXISTING_USERS"]
        }

    data = {
        "targetingDimensions": targeting_dimensions
    }

    response = requests.put(url, headers=api.headers, json=data)
    return response.json()


def set_customer_type_targeting(api, campaign_id, ad_group_id, customer_types):
    """Target by customer type (new users, existing users, etc.)."""
    url = f"{api.base_url}/campaigns/{campaign_id}/adgroups/{ad_group_id}"

    data = {
        "targetingDimensions": {
            "customerType": {
                "included": customer_types
                # ["NEW_DOWNLOADERS", "RETURNING_DOWNLOADERS"]
            }
        }
    }

    response = requests.put(url, headers=api.headers, json=data)
    return response.json()
```

### 4. Bid Optimization

**Automated Bid Management:**
```python
def optimize_keyword_bids(api, campaign_id, ad_group_id, performance_data,
                         target_cpa=5.00, min_bid=0.50, max_bid=5.00):
    """Optimize keyword bids based on CPA target."""
    url = f"{api.base_url}/campaigns/{campaign_id}/adgroups/{ad_group_id}/targetingkeywords/bulk"

    bid_updates = []

    for _, row in performance_data.iterrows():
        keyword_id = row['keyword_id']
        current_bid = row['bid_amount']
        avg_cpa = row['avg_cpa']
        installs = row['installs']

        # Only adjust if we have sufficient data
        if installs < 5:
            continue

        # Calculate bid adjustment
        if avg_cpa > 0:
            bid_multiplier = target_cpa / avg_cpa

            # Conservative adjustments
            if bid_multiplier > 1.2:
                new_bid = current_bid * 1.15
            elif bid_multiplier < 0.8:
                new_bid = current_bid * 0.85
            else:
                continue

            # Enforce min/max bounds
            new_bid = max(min_bid, min(new_bid, max_bid))

            bid_updates.append({
                "id": keyword_id,
                "bidAmount": {
                    "amount": f"{new_bid:.2f}",
                    "currency": "USD"
                }
            })

    # Update bids
    if bid_updates:
        response = requests.put(url, headers=api.headers, json=bid_updates)
        return response.json()

    return {"message": "No bid updates needed"}


def adjust_campaign_budget(api, campaign_id, performance_metrics, budget_cap):
    """Adjust campaign budget based on performance."""
    url = f"{api.base_url}/campaigns/{campaign_id}"

    current_budget = performance_metrics['daily_budget']
    avg_cpa = performance_metrics['avg_cpa']
    target_cpa = performance_metrics['target_cpa']
    spend_rate = performance_metrics['spend_rate']

    # Increase budget if performing well and capped
    if avg_cpa < target_cpa * 0.9 and spend_rate > 0.9:
        new_budget = min(current_budget * 1.2, budget_cap)
    # Decrease if not spending efficiently
    elif spend_rate < 0.5:
        new_budget = current_budget * 0.8
    else:
        return {"message": "No budget change needed"}

    data = {
        "dailyBudgetAmount": {
            "amount": f"{new_budget:.2f}",
            "currency": "USD"
        }
    }

    response = requests.put(url, headers=api.headers, json=data)
    return response.json()
```

## Installation and Authentication

### Install Required Libraries

```bash
pip install requests pandas pyjwt cryptography
```

### Set Up Authentication

1. **Create Apple Developer Account** with access to App Store Connect
2. **Generate API Key** in App Store Connect:
   - Go to Users and Access > Keys
   - Create new API key with "App Manager" role
   - Download private key (.p8 file)
   - Note Key ID and Issuer ID
3. **Get Organization ID** from Apple Search Ads Campaign Management
4. **Get App Adam ID** from App Store Connect

### Initialize API Client

```python
import requests

# Read private key from file
with open('path/to/AuthKey.p8', 'r') as key_file:
    private_key = key_file.read()

api = AppleSearchAdsAPI(
    client_id="YOUR_CLIENT_ID",
    team_id="YOUR_TEAM_ID",
    key_id="YOUR_KEY_ID",
    private_key=private_key
)
```

## Quick Start Example

```python
from datetime import datetime, timedelta

# Initialize API
api = AppleSearchAdsAPI(
    client_id="YOUR_CLIENT_ID",
    team_id="YOUR_TEAM_ID",
    key_id="YOUR_KEY_ID",
    private_key=private_key
)

org_id = "YOUR_ORG_ID"

# Get campaign performance for last 30 days
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

df = get_campaign_report(api, org_id, start_date, end_date)

# Display results
print(df[['campaign_name', 'impressions', 'taps', 'installs', 'spend', 'avg_cpa']])
print(f"\nTotal Installs: {df['installs'].sum():,}")
print(f"Total Spend: ${df['spend'].sum():.2f}")
print(f"Average CPA: ${df['avg_cpa'].mean():.2f}")
print(f"Average TTR: {df['ttr'].mean():.2%}")
```

## Key Metrics Reference

### Performance Metrics
- **Impressions** - Number of times ad was shown
- **Taps** - Number of taps on ad
- **TTR (Tap-Through Rate)** - Taps / Impressions
- **Installs** - Total app installs
- **New Downloads** - First-time downloads
- **Redownloads** - Re-installs by previous users
- **Conversion Rate** - Installs / Taps

### Cost Metrics
- **Spend** - Total amount spent
- **CPT (Cost Per Tap)** - Spend / Taps
- **CPA (Cost Per Acquisition)** - Spend / Installs
- **CPM** - Cost per 1,000 impressions
- **LAT On Installs** - Installs with Limit Ad Tracking enabled
- **LAT Off Installs** - Installs with tracking allowed

### Advanced Metrics
- **Post-Install Events** - In-app actions after install
- **Custom Product Page Performance** - Performance by variant
- **Search Match Performance** - Auto-targeted keyword results
- **Keyword Popularity** - Search volume indicator

## Best Practices

1. **Campaign Structure**
   - Separate campaigns by country/region
   - Create themed ad groups by keyword intent
   - Use exact match for brand keywords
   - Broad match for discovery

2. **Keyword Strategy**
   - Start with Search Match for discovery
   - Graduate top performers to exact match
   - Monitor search terms report weekly
   - Add negatives proactively
   - Bid higher on high-intent keywords

3. **Bidding Strategy**
   - Start conservative, raise for winners
   - Target CPA based on user LTV
   - Bid higher on exact match
   - Use max CPT bid caps to control spend
   - Adjust by time of day/week

4. **Creative Optimization**
   - Test multiple creative sets
   - Use custom product pages for A/B testing
   - Refresh screenshots seasonally
   - Highlight key features and benefits
   - Test different value propositions

5. **Audience Refinement**
   - Target new users for acquisition
   - Target existing users for feature adoption
   - Exclude recent installers
   - Test demographic segments
   - Optimize by device class

## Common Use Cases

### Competitor Keyword Targeting
```python
def target_competitor_keywords(api, ad_group_id, competitors, bid_amount):
    """Target competitor app names and brands."""
    # Create exact match keywords for competitor names
    # Set competitive bids
    # Monitor conversion rates
    pass
```

### Seasonal Budget Scaling
```python
def scale_budgets_for_season(api, campaigns, scale_factor):
    """Increase budgets for seasonal demand."""
    # Identify seasonal campaigns
    # Apply scale factor to budgets
    # Monitor performance daily
    pass
```

### ASO Keyword Testing
```python
def test_aso_keywords(api, ad_group_id, keyword_candidates):
    """Test keyword candidates for ASO optimization."""
    # Create low-bid test campaigns
    # Monitor impressions and TTR
    # Use data to inform ASO strategy
    pass
```

## References

- **Official Documentation**: https://developer.apple.com/documentation/apple_search_ads
- **API Reference**: https://developer.apple.com/documentation/apple_search_ads/api_reference
- **Campaign Management**: https://searchads.apple.com/help/
- **Best Practices**: https://searchads.apple.com/best-practices
- **Creative Specs**: https://searchads.apple.com/help/creative-specs
- **App Store Connect**: https://appstoreconnect.apple.com/
- **Support**: https://searchads.apple.com/support

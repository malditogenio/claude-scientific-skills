---
name: criteo
description: "Criteo API for retargeting and commerce media. Manage dynamic product ads, retargeting campaigns, catalog feeds, audience targeting, and performance analytics for e-commerce."
---

# Criteo

## Overview

Criteo is the leading commerce media platform specializing in dynamic retargeting and personalized advertising. The Criteo Marketing API enables programmatic campaign management, product catalog integration, dynamic creative optimization, and comprehensive analytics for e-commerce performance marketing.

This skill covers the Criteo Marketing API with Python, enabling automated retargeting campaigns, product feed management, audience targeting, and ROI optimization for online retailers and e-commerce businesses.

## When to Use This Skill

Use this skill when you need to:
- Create and manage dynamic retargeting campaigns programmatically
- Optimize product catalog advertising at scale
- Target cart abandoners and website visitors
- Manage product feeds and catalog updates
- Generate detailed e-commerce performance reports
- Implement cross-device retargeting strategies
- Optimize for revenue and ROAS
- Create lookalike audiences from purchasers
- Manage campaigns across multiple e-commerce sites
- Track product-level performance
- Implement dynamic creative optimization (DCO)

## Core Capabilities

### 1. Campaign Management

**Create Retargeting Campaign:**
```python
import requests
import json
from datetime import datetime

class CriteoAPI:
    """Criteo Marketing API client."""

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://api.criteo.com/2023-01"
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        """Get OAuth2 access token."""
        url = "https://api.criteo.com/oauth2/token"

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

    def create_campaign(self, advertiser_id, name, budget, bid_type="cpc"):
        """Create a new campaign."""
        url = f"{self.base_url}/marketing-solutions/campaigns"

        data = {
            "data": {
                "type": "Campaign",
                "attributes": {
                    "advertiserId": advertiser_id,
                    "name": name,
                    "budget": budget,
                    "budgetType": "monthly",
                    "bidType": bid_type,  # cpc, cpm
                    "clickAttributionWindow": "30D",
                    "viewAttributionWindow": "1D",
                    "isActive": False,
                }
            }
        }

        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def create_ad_set(self, campaign_id, name, budget, targeting_type="Lower Funnel"):
        """Create an ad set."""
        url = f"{self.base_url}/marketing-solutions/ad-sets"

        data = {
            "data": {
                "type": "AdSet",
                "attributes": {
                    "campaignId": campaign_id,
                    "name": name,
                    "budget": budget,
                    "budgetType": "daily",
                    "targeting": {
                        "targetingType": targeting_type,
                        # "Lower Funnel" (retargeting), "Upper Funnel" (prospecting)
                    },
                    "schedule": {
                        "startDate": datetime.now().isoformat(),
                    },
                    "isActive": False,
                }
            }
        }

        response = requests.post(url, headers=self.headers, json=data)
        return response.json()


def configure_audience_targeting(api, ad_set_id, audience_config):
    """Configure audience targeting for ad set."""
    url = f"{api.base_url}/marketing-solutions/ad-sets/{ad_set_id}/targeting"

    data = {
        "data": {
            "type": "Targeting",
            "attributes": {
                "audiences": audience_config["audiences"],
                # [{
                #     "type": "website_visitors",
                #     "segmentIds": ["segment_123"],
                #     "lookbackWindow": 30
                # }]
                "geoTargeting": audience_config.get("geoTargeting", []),
                "deviceTargeting": audience_config.get("deviceTargeting", {
                    "mobile": True,
                    "desktop": True,
                    "tablet": True
                }),
            }
        }
    }

    response = requests.put(url, headers=api.headers, json=data)
    return response.json()


# Dynamic retargeting with product catalog
def create_product_catalog_campaign(api, advertiser_id, catalog_id, campaign_name):
    """Create campaign using product catalog."""
    # Create campaign
    campaign = api.create_campaign(
        advertiser_id=advertiser_id,
        name=campaign_name,
        budget=10000,
        bid_type="cpc"
    )

    campaign_id = campaign["data"]["id"]

    # Create ad set for catalog products
    ad_set = api.create_ad_set(
        campaign_id=campaign_id,
        name="Dynamic Product Ads",
        budget=500,
        targeting_type="Lower Funnel"
    )

    # Configure product targeting
    url = f"{api.base_url}/marketing-solutions/ad-sets/{ad_set['data']['id']}/catalog-targeting"

    catalog_data = {
        "data": {
            "type": "CatalogTargeting",
            "attributes": {
                "catalogId": catalog_id,
                "productSets": [
                    {
                        "name": "All Products",
                        "filters": []
                    }
                ]
            }
        }
    }

    response = requests.put(url, headers=api.headers, json=catalog_data)
    return campaign, ad_set, response.json()
```

**Bid Management:**
```python
def set_ad_set_bid(api, ad_set_id, bid_amount, bid_type="cpc"):
    """Set bid for ad set."""
    url = f"{api.base_url}/marketing-solutions/ad-sets/{ad_set_id}"

    data = {
        "data": {
            "type": "AdSet",
            "id": ad_set_id,
            "attributes": {
                "bidType": bid_type,
                "bidAmount": bid_amount
            }
        }
    }

    response = requests.patch(url, headers=api.headers, json=data)
    return response.json()


def enable_auto_bidding(api, ad_set_id, target_roas=None, target_cpa=None):
    """Enable automated bidding with performance targets."""
    url = f"{api.base_url}/marketing-solutions/ad-sets/{ad_set_id}"

    bidding_strategy = {
        "type": "automated"
    }

    if target_roas:
        bidding_strategy["targetROAS"] = target_roas

    if target_cpa:
        bidding_strategy["targetCPA"] = target_cpa

    data = {
        "data": {
            "type": "AdSet",
            "id": ad_set_id,
            "attributes": {
                "biddingStrategy": bidding_strategy
            }
        }
    }

    response = requests.patch(url, headers=api.headers, json=data)
    return response.json()
```

### 2. Product Catalog Management

**Upload and Manage Product Feed:**
```python
def create_product_catalog(api, advertiser_id, catalog_name):
    """Create a product catalog."""
    url = f"{api.base_url}/marketing-solutions/catalogs"

    data = {
        "data": {
            "type": "Catalog",
            "attributes": {
                "advertiserId": advertiser_id,
                "name": catalog_name,
                "marketplaceName": "Custom",
            }
        }
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def upload_product_feed(api, catalog_id, feed_url, feed_format="xml"):
    """Upload product feed to catalog."""
    url = f"{api.base_url}/marketing-solutions/catalogs/{catalog_id}/products"

    data = {
        "data": {
            "type": "ProductFeed",
            "attributes": {
                "feedUrl": feed_url,
                "feedFormat": feed_format,  # xml, csv, tsv
                "updateFrequency": "daily",
                "feedType": "full"  # full or incremental
            }
        }
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def get_catalog_status(api, catalog_id):
    """Get catalog processing status."""
    url = f"{api.base_url}/marketing-solutions/catalogs/{catalog_id}/status"

    response = requests.get(url, headers=api.headers)
    return response.json()


def create_product_set(api, catalog_id, product_set_name, filters):
    """Create product set with filters."""
    url = f"{api.base_url}/marketing-solutions/catalogs/{catalog_id}/product-sets"

    data = {
        "data": {
            "type": "ProductSet",
            "attributes": {
                "name": product_set_name,
                "filters": filters
                # [
                #     {"field": "category", "operator": "equals", "value": "Electronics"},
                #     {"field": "price", "operator": "greater_than", "value": 100}
                # ]
            }
        }
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()
```

### 3. Reporting and Analytics

**Campaign Performance Reports:**
```python
import pandas as pd
from datetime import datetime, timedelta

def get_campaign_statistics(api, advertiser_id, start_date, end_date,
                           dimensions=None, metrics=None):
    """Get campaign performance statistics."""
    url = f"{api.base_url}/marketing-solutions/statistics"

    data = {
        "data": {
            "type": "StatisticsReport",
            "attributes": {
                "advertiserId": advertiser_id,
                "startDate": start_date.strftime("%Y-%m-%d"),
                "endDate": end_date.strftime("%Y-%m-%d"),
                "dimensions": dimensions or ["CampaignId", "Date"],
                "metrics": metrics or [
                    "Clicks",
                    "Displays",
                    "Cost",
                    "Sales",
                    "Revenue",
                    "ROAS",
                    "CPC",
                    "CPM",
                    "CTR",
                    "ConversionRate",
                    "SalesPostClick",
                    "SalesPostView",
                ],
                "currency": "USD",
                "format": "json"
            }
        }
    }

    response = requests.post(url, headers=api.headers, json=data)
    report_data = response.json()

    # Convert to DataFrame
    rows = report_data.get("data", {}).get("rows", [])
    return pd.DataFrame(rows)


def get_product_performance(api, advertiser_id, catalog_id, start_date, end_date):
    """Get product-level performance."""
    url = f"{api.base_url}/marketing-solutions/statistics"

    data = {
        "data": {
            "type": "StatisticsReport",
            "attributes": {
                "advertiserId": advertiser_id,
                "catalogId": catalog_id,
                "startDate": start_date.strftime("%Y-%m-%d"),
                "endDate": end_date.strftime("%Y-%m-%d"),
                "dimensions": ["ProductId", "ProductName"],
                "metrics": [
                    "Displays",
                    "Clicks",
                    "Cost",
                    "Sales",
                    "Revenue",
                    "ROAS",
                    "ProductViews",
                    "AddToCart",
                ],
            }
        }
    }

    response = requests.post(url, headers=api.headers, json=data)
    report_data = response.json()

    return pd.DataFrame(report_data.get("data", {}).get("rows", []))


def get_audience_performance(api, advertiser_id, start_date, end_date):
    """Get performance by audience segment."""
    url = f"{api.base_url}/marketing-solutions/statistics"

    data = {
        "data": {
            "type": "StatisticsReport",
            "attributes": {
                "advertiserId": advertiser_id,
                "startDate": start_date.strftime("%Y-%m-%d"),
                "endDate": end_date.strftime("%Y-%m-%d"),
                "dimensions": ["AudienceSegment"],
                "metrics": [
                    "Displays",
                    "Clicks",
                    "Sales",
                    "Revenue",
                    "ROAS",
                    "ConversionRate",
                ],
            }
        }
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()
```

### 4. Audience Management

**Create and Manage Audiences:**
```python
def create_audience_segment(api, advertiser_id, segment_name, segment_type):
    """Create audience segment."""
    url = f"{api.base_url}/marketing-solutions/audiences"

    data = {
        "data": {
            "type": "Audience",
            "attributes": {
                "advertiserId": advertiser_id,
                "name": segment_name,
                "type": segment_type,
                # "website_visitors", "cart_abandoners", "purchasers", "product_viewers"
                "lookbackWindow": 30,  # days
            }
        }
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def create_customer_list_audience(api, advertiser_id, audience_name, emails):
    """Create audience from customer email list."""
    import hashlib

    url = f"{api.base_url}/marketing-solutions/audiences"

    # Hash emails
    hashed_emails = [
        hashlib.sha256(email.lower().strip().encode()).hexdigest()
        for email in emails
    ]

    data = {
        "data": {
            "type": "Audience",
            "attributes": {
                "advertiserId": advertiser_id,
                "name": audience_name,
                "type": "customer_list",
                "identifiers": {
                    "emails": hashed_emails
                }
            }
        }
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def create_lookalike_audience(api, advertiser_id, seed_audience_id,
                             similarity_percentage=1):
    """Create lookalike audience."""
    url = f"{api.base_url}/marketing-solutions/audiences"

    data = {
        "data": {
            "type": "Audience",
            "attributes": {
                "advertiserId": advertiser_id,
                "name": f"Lookalike {similarity_percentage}%",
                "type": "lookalike",
                "seedAudienceId": seed_audience_id,
                "similarityPercentage": similarity_percentage,  # 1-10
            }
        }
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def exclude_converters_audience(api, advertiser_id):
    """Create suppression audience for recent converters."""
    url = f"{api.base_url}/marketing-solutions/audiences"

    data = {
        "data": {
            "type": "Audience",
            "attributes": {
                "advertiserId": advertiser_id,
                "name": "Recent Purchasers - Exclude",
                "type": "purchasers",
                "lookbackWindow": 7,  # Exclude purchases in last 7 days
                "action": "exclude"
            }
        }
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

1. **Create Criteo Account** at https://marketing.criteo.com/
2. **Register for API Access** in Account Settings
3. **Generate API Credentials**:
   - Client ID
   - Client Secret
4. **Get Advertiser ID** from Criteo Management Center

### Initialize API Client

```python
import requests

class CriteoAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://api.criteo.com/2023-01"
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        url = "https://api.criteo.com/oauth2/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        response = requests.post(url, data=data)
        return response.json()["access_token"]

# Initialize
api = CriteoAPI(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
)
```

## Quick Start Example

```python
from datetime import datetime, timedelta

# Initialize API
api = CriteoAPI(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
)

advertiser_id = "YOUR_ADVERTISER_ID"

# Create retargeting campaign
campaign = api.create_campaign(
    advertiser_id=advertiser_id,
    name="Holiday Retargeting 2024",
    budget=50000,
    bid_type="cpc"
)

# Get performance report
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

df = get_campaign_statistics(api, advertiser_id, start_date, end_date)

print(df[['CampaignId', 'Displays', 'Clicks', 'Sales', 'Revenue', 'ROAS']])
print(f"\nTotal Revenue: ${df['Revenue'].sum():.2f}")
print(f"Average ROAS: {df['ROAS'].mean():.2f}x")
print(f"Total Sales: {df['Sales'].sum():.0f}")
```

## Key Metrics Reference

### Performance Metrics
- **Displays** - Number of ad impressions
- **Clicks** - Number of clicks
- **CTR** - Click-through rate
- **CPC** - Cost per click
- **CPM** - Cost per 1,000 impressions
- **Cost** - Total spend

### E-commerce Metrics
- **Sales** - Number of transactions
- **Revenue** - Total sales revenue
- **ROAS** - Return on ad spend (Revenue / Cost)
- **ConversionRate** - Sales / Clicks
- **CPA** - Cost per acquisition (Cost / Sales)
- **AOV** - Average order value (Revenue / Sales)

### Attribution Metrics
- **SalesPostClick** - Sales attributed to clicks
- **SalesPostView** - Sales attributed to views (view-through)
- **RevenuePostClick** - Revenue from click-through conversions
- **RevenuePostView** - Revenue from view-through conversions

### Engagement Metrics
- **ProductViews** - Product page views
- **AddToCart** - Add to cart events
- **CartAbandonment** - Cart abandonment rate
- **VisitsRetargeted** - Website visits from retargeting

## Best Practices

1. **Catalog Management**
   - Update product feed daily
   - Include all required fields (ID, title, price, image, URL)
   - Use product sets for segmentation
   - Monitor feed quality and errors

2. **Audience Strategy**
   - Segment audiences by funnel stage
   - Exclude recent converters
   - Create lookalikes from purchasers
   - Layer behavioral and demographic data

3. **Dynamic Creative**
   - Let Criteo optimize product selection
   - Test different creative formats
   - Use high-quality product images
   - Include pricing and availability

4. **Bid Optimization**
   - Start with CPC bidding
   - Switch to automated bidding after learning period
   - Set ROAS targets based on margin
   - Monitor product-level profitability

5. **Budget Management**
   - Allocate more budget to high-ROAS campaigns
   - Use campaign budget optimization
   - Reserve budget for peak seasons
   - Monitor spend pacing daily

## Common Use Cases

### Cart Abandonment Retargeting
```python
def create_cart_abandonment_campaign(api, advertiser_id, catalog_id):
    """Target users who abandoned shopping carts."""
    # Create audience of cart abandoners
    # Create campaign with urgency messaging
    # Set short attribution window
    pass
```

### Cross-Sell Campaign
```python
def create_cross_sell_campaign(api, advertiser_id, purchaser_segment_id):
    """Show complementary products to recent purchasers."""
    # Create audience of recent purchasers
    # Filter products by category
    # Set up product recommendations
    pass
```

### Seasonal Promotion
```python
def create_seasonal_campaign(api, advertiser_id, product_set_id, promo_dates):
    """Promote seasonal products during peak period."""
    # Create campaign with seasonal budget
    # Target relevant product set
    # Schedule start/end dates
    pass
```

## References

- **Official Documentation**: https://developers.criteo.com/marketing-solutions/docs
- **API Reference**: https://developers.criteo.com/marketing-solutions/reference
- **Product Catalog Specs**: https://help.criteo.com/kb/guide/en/product-feed-specifications
- **Best Practices**: https://www.criteo.com/insights/
- **Commerce Media Platform**: https://www.criteo.com/products/commerce-media-platform/
- **Support**: https://help.criteo.com/
- **Developer Portal**: https://developers.criteo.com/

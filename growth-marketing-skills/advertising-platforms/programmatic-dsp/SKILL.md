---
name: programmatic-dsp
description: "Programmatic advertising and DSP (Demand-Side Platform) APIs. Manage real-time bidding, display campaigns, video ads, audience targeting, and cross-platform media buying."
---

# Programmatic DSP (Demand-Side Platform)

## Overview

Programmatic advertising automates the buying and selling of digital ad inventory through Demand-Side Platforms (DSPs). DSP APIs enable real-time bidding (RTB), automated media buying, audience targeting, and cross-platform campaign management across display, video, mobile, and connected TV.

This skill covers programmatic DSP APIs (including The Trade Desk, DV360, Amazon DSP concepts) with Python, enabling automated bidding, audience management, and performance optimization for large-scale digital advertising.

## When to Use This Skill

Use this skill when you need to:
- Automate programmatic media buying across multiple exchanges
- Manage real-time bidding (RTB) campaigns
- Target audiences across display, video, mobile, and CTV
- Implement data-driven audience targeting and lookalikes
- Generate cross-platform performance reports
- Optimize bids based on viewability and brand safety
- Manage private marketplace (PMP) deals
- Implement frequency capping and sequential messaging
- Track viewability, completion rates, and engagement
- Integrate first-party and third-party data
- Manage large-scale cross-device campaigns

## Core Capabilities

### 1. Campaign Management

**Create Programmatic Campaign (The Trade Desk Pattern):**
```python
import requests
import json
from datetime import datetime

class ProgrammaticDSPAPI:
    """Generic Programmatic DSP API client pattern."""

    def __init__(self, access_token, advertiser_id):
        self.access_token = access_token
        self.advertiser_id = advertiser_id
        self.base_url = "https://api.thetradedesk.com/v3"
        self.headers = {
            "TTD-Auth": access_token,
            "Content-Type": "application/json",
        }

    def create_campaign(self, name, budget, start_date, end_date=None,
                       campaign_type="DISPLAY"):
        """Create a programmatic campaign."""
        url = f"{self.base_url}/campaign"

        data = {
            "AdvertiserId": self.advertiser_id,
            "CampaignName": name,
            "Budget": {
                "Amount": budget,
                "CurrencyCode": "USD"
            },
            "StartDate": start_date.isoformat(),
            "CampaignConversionReportingColumns": [],
            "Description": f"{campaign_type} campaign",
        }

        if end_date:
            data["EndDate"] = end_date.isoformat()

        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def create_ad_group(self, campaign_id, name, base_bid_cpm, daily_budget=None,
                       pacing_mode="PACE_AHEAD"):
        """Create an ad group."""
        url = f"{self.base_url}/adgroup"

        data = {
            "CampaignId": campaign_id,
            "AdGroupName": name,
            "BaseBidCPM": {
                "Amount": base_bid_cpm,
                "CurrencyCode": "USD"
            },
            "PacingMode": pacing_mode,  # PACE_AHEAD, PACE_EVENLY
            "RTBAttributes": {
                "BudgetInImpressions": False,
                "BudgetInDollars": True,
            },
            "IsEnabled": True,
        }

        if daily_budget:
            data["DailyBudget"] = {
                "Amount": daily_budget,
                "CurrencyCode": "USD"
            }

        response = requests.post(url, headers=self.headers, json=data)
        return response.json()


def build_targeting_facets(demographics=None, geography=None, device_types=None,
                          audiences=None, contextual=None, inventory=None):
    """Build targeting facets for programmatic campaigns."""
    facets = []

    # Demographic targeting
    if demographics:
        if 'age_ranges' in demographics:
            facets.append({
                "FacetType": "Age",
                "Include": demographics['age_ranges']  # ["18-24", "25-34", etc.]
            })
        if 'gender' in demographics:
            facets.append({
                "FacetType": "Gender",
                "Include": demographics['gender']  # ["M", "F"]
            })
        if 'household_income' in demographics:
            facets.append({
                "FacetType": "HouseholdIncome",
                "Include": demographics['household_income']
            })

    # Geographic targeting
    if geography:
        facets.append({
            "FacetType": "Geography",
            "Include": geography  # List of geo IDs
        })

    # Device type targeting
    if device_types:
        facets.append({
            "FacetType": "DeviceType",
            "Include": device_types  # ["Desktop", "Mobile", "CTV"]
        })

    # Audience targeting
    if audiences:
        facets.append({
            "FacetType": "ThirdPartyAudienceSegments",
            "Include": audiences  # Audience segment IDs
        })

    # Contextual targeting
    if contextual:
        if 'site_lists' in contextual:
            facets.append({
                "FacetType": "SiteList",
                "Include": contextual['site_lists']
            })
        if 'categories' in contextual:
            facets.append({
                "FacetType": "ContentCategory",
                "Include": contextual['categories']
            })

    # Inventory targeting
    if inventory:
        facets.append({
            "FacetType": "SupplyVendor",
            "Include": inventory  # Supply source IDs
        })

    return facets


def apply_targeting_to_ad_group(api, ad_group_id, targeting_facets):
    """Apply targeting facets to ad group."""
    url = f"{api.base_url}/adgroup/{ad_group_id}/facets"

    data = {
        "AdGroupId": ad_group_id,
        "Facets": targeting_facets
    }

    response = requests.put(url, headers=api.headers, json=data)
    return response.json()


# Creative management
def upload_creative(api, advertiser_id, creative_name, ad_format, asset_url,
                   click_through_url, dimensions):
    """Upload display or video creative."""
    url = f"{api.base_url}/creative"

    data = {
        "AdvertiserId": advertiser_id,
        "CreativeName": creative_name,
        "AdFormat": ad_format,  # "Display", "Video", "Native"
        "HostedCreativeAsset": {
            "Url": asset_url
        },
        "ClickThroughUrl": click_through_url,
        "Dimensions": dimensions,  # {"Height": 250, "Width": 300}
        "CreativeApprovalStatus": "PendingApproval",
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def assign_creative_to_ad_group(api, ad_group_id, creative_id):
    """Assign creative to ad group."""
    url = f"{api.base_url}/adgroup/{ad_group_id}/creatives"

    data = {
        "CreativeIds": [creative_id]
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()
```

**Private Marketplace (PMP) Deals:**
```python
def create_pmp_deal(api, advertiser_id, publisher_name, deal_id, floor_price_cpm):
    """Set up private marketplace deal."""
    url = f"{api.base_url}/deal"

    data = {
        "AdvertiserId": advertiser_id,
        "DealName": f"PMP - {publisher_name}",
        "DealId": deal_id,  # Deal ID from publisher
        "FloorPriceCPM": {
            "Amount": floor_price_cpm,
            "CurrencyCode": "USD"
        },
        "DealType": "PrivateMarketplace",
        "IsEnabled": True,
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def assign_deal_to_ad_group(api, ad_group_id, deal_id):
    """Target specific PMP deal in ad group."""
    url = f"{api.base_url}/adgroup/{ad_group_id}/deals"

    data = {
        "DealIds": [deal_id]
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()
```

### 2. Reporting and Analytics

**Campaign Performance Reports:**
```python
import pandas as pd
from datetime import datetime, timedelta

def get_campaign_performance(api, advertiser_id, start_date, end_date,
                            dimension="Campaign"):
    """Get campaign performance metrics."""
    url = f"{api.base_url}/myreports/reportexecution/query/advertiser"

    query = {
        "AdvertiserId": advertiser_id,
        "ReportScheduleName": "Campaign Performance",
        "ReportDateRange": {
            "StartDate": start_date.isoformat(),
            "EndDate": end_date.isoformat(),
        },
        "Dimensions": [dimension],  # Campaign, AdGroup, Creative, etc.
        "Metrics": [
            "Impressions",
            "Clicks",
            "TotalCost",
            "CTR",
            "Conversions",
            "CPA",
            "ROAS",
            "VideoCompletionRate",
            "Viewability",
            "BrandSafetyScore"
        ],
        "Filters": []
    }

    response = requests.post(url, headers=api.headers, json=query)
    report_execution_id = response.json().get("ReportExecutionId")

    # Poll for completion
    import time
    status_url = f"{api.base_url}/myreports/reportexecution/{report_execution_id}"

    while True:
        status_response = requests.get(status_url, headers=api.headers)
        status = status_response.json().get("ReportExecutionState")

        if status == "Complete":
            download_url = status_response.json().get("ReportDeliveries")[0]["DownloadURL"]
            break
        elif status == "Failed":
            raise Exception("Report generation failed")

        time.sleep(10)

    # Download and parse report
    report_data = requests.get(download_url)
    # Parse CSV/JSON based on format

    return pd.read_csv(pd.io.common.BytesIO(report_data.content))


def get_supply_source_performance(api, advertiser_id, start_date, end_date):
    """Get performance by supply source."""
    query = {
        "AdvertiserId": advertiser_id,
        "ReportScheduleName": "Supply Source Report",
        "ReportDateRange": {
            "StartDate": start_date.isoformat(),
            "EndDate": end_date.isoformat(),
        },
        "Dimensions": ["SupplyVendor"],
        "Metrics": [
            "Impressions",
            "Clicks",
            "TotalCost",
            "Viewability",
            "InvalidTrafficRate",
            "Conversions"
        ]
    }

    # Similar execution pattern as above
    return query


def get_audience_segment_performance(api, advertiser_id, start_date, end_date):
    """Get performance by audience segment."""
    query = {
        "AdvertiserId": advertiser_id,
        "Dimensions": ["AudienceSegment"],
        "Metrics": [
            "Impressions",
            "Clicks",
            "TotalCost",
            "Conversions",
            "CPA",
            "ROAS"
        ],
        "ReportDateRange": {
            "StartDate": start_date.isoformat(),
            "EndDate": end_date.isoformat(),
        }
    }

    return query
```

### 3. Audience Management

**First-Party Data Management:**
```python
def create_first_party_audience(api, advertiser_id, audience_name, data_provider_id):
    """Create first-party data audience."""
    url = f"{api.base_url}/firstpartydatasegment"

    data = {
        "AdvertiserId": advertiser_id,
        "FirstPartyDataSegmentName": audience_name,
        "DataProviderId": data_provider_id,
        "IsEnabled": True,
        "MembershipDurationInDays": 180,
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def upload_audience_data(api, segment_id, user_identifiers):
    """Upload user data to first-party segment."""
    url = f"{api.base_url}/firstpartydatasegment/{segment_id}/users"

    import hashlib

    # Hash identifiers
    hashed_data = []
    for user in user_identifiers:
        hashed_user = {}
        if 'email' in user:
            hashed_user['HashedEmail'] = hashlib.sha256(
                user['email'].lower().strip().encode()
            ).hexdigest()
        if 'phone' in user:
            hashed_user['HashedPhone'] = hashlib.sha256(
                user['phone'].strip().encode()
            ).hexdigest()
        if 'device_id' in user:
            hashed_user['DeviceId'] = user['device_id']

        hashed_data.append(hashed_user)

    data = {
        "Users": hashed_data,
        "Action": "Add"  # Add or Remove
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


def create_lookalike_audience(api, advertiser_id, seed_segment_id, similarity_percentage):
    """Create lookalike audience from seed segment."""
    url = f"{api.base_url}/audienceextension"

    data = {
        "AdvertiserId": advertiser_id,
        "AudienceExtensionName": f"Lookalike {similarity_percentage}%",
        "SeedSegmentId": seed_segment_id,
        "SimilarityPercentage": similarity_percentage,  # 1-10
        "IsEnabled": True,
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()


# Suppression lists
def create_suppression_list(api, advertiser_id, list_name, user_identifiers):
    """Create suppression list to exclude users."""
    url = f"{api.base_url}/universalpixelsuppression"

    data = {
        "AdvertiserId": advertiser_id,
        "SuppressionListName": list_name,
        "Users": user_identifiers,
        "IsEnabled": True,
    }

    response = requests.post(url, headers=api.headers, json=data)
    return response.json()
```

### 4. Bid Optimization and Brand Safety

**Dynamic Bidding Strategies:**
```python
def set_dynamic_bidding(api, ad_group_id, optimization_goal="CPA",
                       target_value=None, max_bid_cpm=None):
    """Configure dynamic bidding for ad group."""
    url = f"{api.base_url}/adgroup/{ad_group_id}/bidding"

    data = {
        "BiddingStrategy": "Optimize",
        "OptimizationGoal": optimization_goal,  # CPA, CPC, ROAS, Viewability
    }

    if target_value:
        data["TargetValue"] = {
            "Amount": target_value,
            "CurrencyCode": "USD"
        }

    if max_bid_cpm:
        data["MaxBidCPM"] = {
            "Amount": max_bid_cpm,
            "CurrencyCode": "USD"
        }

    response = requests.put(url, headers=api.headers, json=data)
    return response.json()


def apply_brand_safety_filters(api, ad_group_id, sensitivity_level="MODERATE"):
    """Apply brand safety and viewability filters."""
    url = f"{api.base_url}/adgroup/{ad_group_id}/filters"

    data = {
        "BrandSafety": {
            "SensitivityLevel": sensitivity_level,  # LOW, MODERATE, HIGH
            "BlockedCategories": [
                "AdultContent",
                "IllegalContent",
                "Violence"
            ]
        },
        "ViewabilityRequirements": {
            "MinimumViewabilityRate": 70,  # Percentage
            "MeasurementVendor": "IAS"  # IAS, MOAT, DoubleVerify
        },
        "InvalidTrafficFilter": {
            "Enabled": True,
            "MaxInvalidTrafficRate": 5  # Percentage
        }
    }

    response = requests.put(url, headers=api.headers, json=data)
    return response.json()


def set_frequency_cap(api, ad_group_id, max_impressions, time_window_hours):
    """Set frequency cap to limit ad exposure."""
    url = f"{api.base_url}/adgroup/{ad_group_id}/frequencycap"

    data = {
        "MaxImpressions": max_impressions,
        "TimeWindowInHours": time_window_hours,
        "IsEnabled": True,
    }

    response = requests.put(url, headers=api.headers, json=data)
    return response.json()


# Contextual targeting
def apply_contextual_targeting(api, ad_group_id, keywords=None, categories=None,
                              site_lists=None):
    """Apply contextual targeting based on page content."""
    url = f"{api.base_url}/adgroup/{ad_group_id}/contextual"

    data = {
        "ContextualTargeting": {}
    }

    if keywords:
        data["ContextualTargeting"]["Keywords"] = {
            "Include": keywords,
            "MatchType": "BROAD"  # EXACT, PHRASE, BROAD
        }

    if categories:
        data["ContextualTargeting"]["ContentCategories"] = {
            "Include": categories
        }

    if site_lists:
        data["ContextualTargeting"]["SiteLists"] = {
            "Include": site_lists
        }

    response = requests.put(url, headers=api.headers, json=data)
    return response.json()
```

## Installation and Authentication

### Install Required Libraries

```bash
pip install requests pandas
```

### Set Up Authentication

**The Trade Desk:**
1. Create account at https://www.thetradedesk.com/
2. Generate API credentials in platform
3. Get Partner ID and Advertiser ID

**Google DV360 (Display & Video 360):**
1. Access via Google Marketing Platform
2. Use OAuth 2.0 for authentication
3. Enable Display & Video 360 API

**Amazon DSP:**
1. Access via Amazon Advertising Console
2. Request API access
3. Generate OAuth credentials

### Initialize API Client

```python
import requests

class ProgrammaticDSPAPI:
    def __init__(self, access_token, advertiser_id):
        self.access_token = access_token
        self.advertiser_id = advertiser_id
        self.base_url = "https://api.dsp-platform.com/v3"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

# Initialize
api = ProgrammaticDSPAPI(
    access_token="YOUR_ACCESS_TOKEN",
    advertiser_id="YOUR_ADVERTISER_ID"
)
```

## Quick Start Example

```python
from datetime import datetime, timedelta

# Initialize API
api = ProgrammaticDSPAPI(
    access_token="YOUR_ACCESS_TOKEN",
    advertiser_id="YOUR_ADVERTISER_ID"
)

# Create campaign
campaign = api.create_campaign(
    name="Q4 Brand Awareness",
    budget=50000,
    start_date=datetime.now(),
    campaign_type="DISPLAY"
)

# Create ad group with targeting
ad_group = api.create_ad_group(
    campaign_id=campaign['CampaignId'],
    name="Tech Enthusiasts",
    base_bid_cpm=5.00,
    daily_budget=500
)

# Get performance report
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

df = get_campaign_performance(api, api.advertiser_id, start_date, end_date)
print(f"Total Impressions: {df['Impressions'].sum():,}")
print(f"Total Spend: ${df['TotalCost'].sum():.2f}")
print(f"Average Viewability: {df['Viewability'].mean():.1f}%")
```

## Key Metrics Reference

### Performance Metrics
- **Impressions** - Number of ad impressions served
- **Clicks** - Number of clicks
- **CTR** - Click-through rate
- **eCPM** - Effective cost per 1,000 impressions
- **Win Rate** - Percentage of auctions won
- **Total Cost** - Total media spend

### Video Metrics
- **Video Starts** - Number of video plays
- **Video Completion Rate** - Percentage of videos watched to end
- **Quartile Completion** - 25%, 50%, 75% completion rates
- **CPCV** - Cost per completed view
- **VTR** - View-through rate

### Quality Metrics
- **Viewability Rate** - Percentage of viewable impressions (MRC standard)
- **Brand Safety Score** - Content appropriateness rating
- **Invalid Traffic Rate** - Percentage of non-human traffic
- **In-Target Rate** - Percentage reaching target audience
- **Fraud Score** - Ad fraud detection score

### Conversion Metrics
- **Conversions** - Total conversion events
- **View-Through Conversions** - Conversions after viewing (no click)
- **Click-Through Conversions** - Conversions after clicking
- **CPA** - Cost per acquisition
- **ROAS** - Return on ad spend
- **Post-View Revenue** - Revenue from view-through conversions

## Best Practices

1. **Campaign Setup**
   - Separate campaigns by objective and channel
   - Use clear naming conventions
   - Set appropriate frequency caps
   - Implement conversion tracking from day one

2. **Audience Strategy**
   - Layer first-party data with third-party segments
   - Create suppression lists for converters
   - Build lookalikes from best performers
   - Test broad vs narrow targeting

3. **Bidding Optimization**
   - Start with moderate CPM bids
   - Enable dynamic bidding after learning period
   - Set max CPM caps to control costs
   - Optimize for quality metrics (viewability, completion)

4. **Brand Safety**
   - Always enable brand safety filters
   - Use third-party verification (IAS, DoubleVerify)
   - Create allowlists for premium inventory
   - Monitor invalid traffic rates

5. **Creative Strategy**
   - Test multiple creative sizes
   - Refresh creative every 2-3 weeks
   - Use dynamic creative optimization (DCO)
   - A/B test messaging and visuals

6. **Inventory Selection**
   - Prioritize private marketplaces for quality
   - Test open exchange for scale
   - Monitor supply source performance
   - Block underperforming domains

## Common Use Cases

### Cross-Device Retargeting
```python
def setup_cross_device_retargeting(api, advertiser_id, website_visitors):
    """Retarget website visitors across devices."""
    # Create audience from website pixels
    # Enable cross-device targeting
    # Set frequency caps per user
    pass
```

### Sequential Messaging Campaign
```python
def create_sequential_campaign(api, message_sequence):
    """Create sequential messaging funnel."""
    # Create ad groups for each message
    # Set up audience progression
    # Implement frequency and recency rules
    pass
```

### CTV + Display Campaign
```python
def create_ctv_display_campaign(api, advertiser_id):
    """Create coordinated CTV and display campaign."""
    # Set up CTV awareness campaign
    # Create display retargeting for CTV viewers
    # Measure incremental reach
    pass
```

## References

- **The Trade Desk API**: https://api.thetradedesk.com/v3/portal
- **Google DV360 API**: https://developers.google.com/display-video
- **Amazon DSP**: https://advertising.amazon.com/API/docs/en-us/dsp
- **IAB Standards**: https://www.iab.com/guidelines/
- **Viewability Standards (MRC)**: https://www.mediaratingcouncil.org/
- **Brand Safety**: https://www.iab.com/guidelines/brand-safety/
- **OpenRTB Protocol**: https://www.iab.com/guidelines/openrtb/
- **Programmatic Best Practices**: https://www.iab.com/guidelines/programmatic/

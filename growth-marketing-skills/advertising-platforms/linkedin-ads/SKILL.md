---
name: linkedin-ads
description: "LinkedIn Ads API for B2B advertising. Manage sponsored content, message ads, dynamic ads, lead gen forms, audience targeting, and analytics for professional network advertising."
---

# LinkedIn Ads

## Overview

LinkedIn Ads is the leading B2B advertising platform, providing access to over 900 million professionals worldwide. The LinkedIn Marketing API enables programmatic campaign management, precise professional targeting, lead generation, and comprehensive analytics for B2B marketing and recruitment.

This skill covers the LinkedIn Marketing API with Python, enabling automated campaign creation, audience targeting by job title/company/industry, lead form management, and performance tracking for B2B campaigns.

## When to Use This Skill

Use this skill when you need to:
- Create and manage B2B advertising campaigns programmatically
- Target audiences by job title, company, industry, and seniority
- Generate leads with LinkedIn Lead Gen Forms
- Manage Sponsored Content, Message Ads, and Dynamic Ads
- Automate account-based marketing (ABM) campaigns
- Generate detailed B2B performance reports
- Manage large-scale recruitment advertising
- Sync CRM data for matched audiences
- Implement conversion tracking for B2B events
- Monitor campaign performance by job function and company size
- Create lookalike audiences from high-value accounts

## Core Capabilities

### 1. Campaign Management

**Create Campaign Structure:**
```python
import requests
import json

class LinkedInAdsAPI:
    """LinkedIn Ads API client."""

    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

    def create_campaign_group(self, account_id, name, total_budget=None):
        """Create a campaign group (formerly campaign)."""
        data = {
            "account": f"urn:li:sponsoredAccount:{account_id}",
            "name": name,
            "status": "PAUSED",
            "type": "SPONSORED_UPDATES",
            "test": False,
        }

        if total_budget:
            data["totalBudget"] = {
                "amount": str(total_budget),
                "currencyCode": "USD"
            }

        response = requests.post(
            f"{self.base_url}/adCampaignGroupsV2",
            headers=self.headers,
            json=data
        )

        return response.json()

    def create_campaign(self, account_id, campaign_group_id, name,
                       objective, daily_budget, targeting_criteria):
        """Create a campaign (formerly ad group)."""
        data = {
            "account": f"urn:li:sponsoredAccount:{account_id}",
            "campaignGroup": campaign_group_id,
            "name": name,
            "type": "SPONSORED_UPDATES",
            "costType": "CPM",  # CPM, CPC
            "objectiveType": objective,  # BRAND_AWARENESS, WEBSITE_VISITS, ENGAGEMENT,
                                         # VIDEO_VIEWS, LEAD_GENERATION, WEBSITE_CONVERSIONS
            "dailyBudget": {
                "amount": str(daily_budget),
                "currencyCode": "USD"
            },
            "unitCost": {
                "amount": "10.00",  # Bid amount
                "currencyCode": "USD"
            },
            "offsiteDeliveryEnabled": False,
            "targetingCriteria": targeting_criteria,
            "status": "PAUSED",
        }

        response = requests.post(
            f"{self.base_url}/adCampaignsV2",
            headers=self.headers,
            json=data
        )

        return response.json()


def build_targeting_criteria(job_titles=None, job_functions=None,
                            industries=None, company_sizes=None,
                            seniority=None, skills=None, locations=None):
    """Build LinkedIn targeting criteria."""
    targeting = {
        "include": {
            "and": []
        }
    }

    # Job title targeting
    if job_titles:
        targeting["include"]["and"].append({
            "or": {
                "urn:li:adTargetingFacet:titles": [
                    f"urn:li:title:{title_id}" for title_id in job_titles
                ]
            }
        })

    # Job function targeting
    if job_functions:
        targeting["include"]["and"].append({
            "or": {
                "urn:li:adTargetingFacet:jobFunctions": [
                    f"urn:li:function:{func_id}" for func_id in job_functions
                ]
            }
        })

    # Industry targeting
    if industries:
        targeting["include"]["and"].append({
            "or": {
                "urn:li:adTargetingFacet:industries": [
                    f"urn:li:industry:{ind_id}" for ind_id in industries
                ]
            }
        })

    # Company size targeting
    if company_sizes:
        targeting["include"]["and"].append({
            "or": {
                "urn:li:adTargetingFacet:companySizes": company_sizes
                # ["A" (1-10), "B" (11-50), "C" (51-200), "D" (201-500),
                #  "E" (501-1000), "F" (1001-5000), "G" (5001-10000), "H" (10001+)]
            }
        })

    # Seniority targeting
    if seniority:
        targeting["include"]["and"].append({
            "or": {
                "urn:li:adTargetingFacet:seniorities": [
                    f"urn:li:seniority:{sen_id}" for sen_id in seniority
                ]
            }
        })

    # Skills targeting
    if skills:
        targeting["include"]["and"].append({
            "or": {
                "urn:li:adTargetingFacet:skills": [
                    f"urn:li:skill:{skill_id}" for skill_id in skills
                ]
            }
        })

    # Location targeting
    if locations:
        targeting["include"]["and"].append({
            "or": {
                "urn:li:adTargetingFacet:locations": [
                    f"urn:li:geo:{loc_id}" for loc_id in locations
                ]
            }
        })

    return targeting


# Create Sponsored Content
def create_sponsored_content(api, account_id, campaign_id, creative_type="SINGLE_IMAGE"):
    """Create sponsored content creative."""

    # Register share (LinkedIn post)
    share_data = {
        "author": f"urn:li:organization:{account_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": "Check out our latest solution for B2B marketers!"
                },
                "shareMediaCategory": "ARTICLE",
                "media": [
                    {
                        "status": "READY",
                        "description": {
                            "text": "Learn how to scale your B2B marketing"
                        },
                        "originalUrl": "https://example.com/article",
                        "title": {
                            "text": "B2B Marketing Guide"
                        }
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    # Create ad creative
    creative_data = {
        "campaign": campaign_id,
        "status": "PAUSED",
        "type": "SPONSORED_STATUS_UPDATE",
        "reference": "SHARE_URN_HERE",  # URN from share creation
        "variables": {
            "clickUri": "https://example.com",
            "data": {
                "com.linkedin.ads.SponsoredUpdateCreativeVariables": {
                    "activity": "SHARE_URN_HERE"
                }
            }
        }
    }

    response = requests.post(
        f"{api.base_url}/adCreativesV2",
        headers=api.headers,
        json=creative_data
    )

    return response.json()
```

**Message Ads (Sponsored InMail):**
```python
def create_message_ad(api, account_id, campaign_id, subject, message_body, cta_text, cta_url):
    """Create a LinkedIn Message Ad (Sponsored InMail)."""

    creative_data = {
        "campaign": campaign_id,
        "status": "PAUSED",
        "type": "SPONSORED_INMAILS",
        "variables": {
            "data": {
                "com.linkedin.ads.SponsoredInMailCreativeVariables": {
                    "sender": f"urn:li:person:SENDER_ID",
                    "subject": subject,
                    "body": message_body,
                    "callToAction": {
                        "text": cta_text,
                        "url": cta_url
                    }
                }
            }
        }
    }

    response = requests.post(
        f"{api.base_url}/adCreativesV2",
        headers=api.headers,
        json=creative_data
    )

    return response.json()
```

### 2. Reporting and Analytics

**Campaign Performance Reports:**
```python
import pandas as pd
from datetime import datetime, timedelta

def get_campaign_analytics(api, account_id, start_date, end_date,
                           time_granularity="DAILY", pivot="CAMPAIGN"):
    """Get campaign performance analytics."""

    params = {
        "q": "analytics",
        "pivot": pivot,  # CAMPAIGN, CREATIVE, ACCOUNT
        "dateRange.start.day": start_date.day,
        "dateRange.start.month": start_date.month,
        "dateRange.start.year": start_date.year,
        "dateRange.end.day": end_date.day,
        "dateRange.end.month": end_date.month,
        "dateRange.end.year": end_date.year,
        "timeGranularity": time_granularity,  # DAILY, MONTHLY, ALL
        "campaigns[0]": f"urn:li:sponsoredCampaign:CAMPAIGN_ID",
        "fields": (
            "dateRange,impressions,clicks,costInUsd,costInLocalCurrency,"
            "landingPageClicks,likes,shares,comments,follows,videoViews,"
            "videoCompletions,videoFirstQuartileCompletions,videoMidpointCompletions,"
            "videoThirdQuartileCompletions,externalWebsiteConversions,"
            "externalWebsitePostClickConversions,externalWebsitePostViewConversions"
        )
    }

    response = requests.get(
        f"{api.base_url}/adAnalyticsV2",
        headers=api.headers,
        params=params
    )

    data = response.json()

    results = []
    for element in data.get('elements', []):
        results.append({
            'date': element.get('dateRange', {}).get('start'),
            'impressions': element.get('impressions', 0),
            'clicks': element.get('clicks', 0),
            'cost': element.get('costInUsd', 0),
            'landing_page_clicks': element.get('landingPageClicks', 0),
            'likes': element.get('likes', 0),
            'shares': element.get('shares', 0),
            'comments': element.get('comments', 0),
            'follows': element.get('follows', 0),
            'video_views': element.get('videoViews', 0),
            'conversions': element.get('externalWebsiteConversions', 0),
        })

    df = pd.DataFrame(results)

    # Calculate derived metrics
    if not df.empty:
        df['ctr'] = df['clicks'] / df['impressions'].replace(0, 1)
        df['cpc'] = df['cost'] / df['clicks'].replace(0, 1)
        df['cpm'] = (df['cost'] / df['impressions'].replace(0, 1)) * 1000
        df['engagement_rate'] = (df['likes'] + df['shares'] + df['comments']) / df['impressions'].replace(0, 1)

    return df


def get_demographic_analytics(api, account_id, dimension="seniority"):
    """Get performance breakdown by demographics."""

    params = {
        "q": "analytics",
        "pivot": f"({dimension.upper()})",
        "dateRange.start.day": 1,
        "dateRange.start.month": 1,
        "dateRange.start.year": 2024,
        "dateRange.end.day": 31,
        "dateRange.end.month": 12,
        "dateRange.end.year": 2024,
        "timeGranularity": "ALL",
        "accounts[0]": f"urn:li:sponsoredAccount:{account_id}",
    }

    response = requests.get(
        f"{api.base_url}/adAnalyticsV2",
        headers=api.headers,
        params=params
    )

    return response.json()


def get_company_analytics(api, account_id):
    """Get performance by company (for ABM campaigns)."""

    params = {
        "q": "analytics",
        "pivot": "COMPANY",
        "dateRange.start.day": 1,
        "dateRange.start.month": 1,
        "dateRange.start.year": 2024,
        "dateRange.end.day": 31,
        "dateRange.end.month": 12,
        "dateRange.end.year": 2024,
        "timeGranularity": "ALL",
        "accounts[0]": f"urn:li:sponsoredAccount:{account_id}",
    }

    response = requests.get(
        f"{api.base_url}/adAnalyticsV2",
        headers=api.headers,
        params=params
    )

    return response.json()
```

### 3. Audience Management

**Matched Audiences:**
```python
def create_matched_audience(api, account_id, audience_name, audience_type="USER_COMPANY"):
    """Create a matched audience for targeting."""

    data = {
        "account": f"urn:li:sponsoredAccount:{account_id}",
        "name": audience_name,
        "type": audience_type,  # USER_COMPANY, USER_EMAIL, USER_CONTACT
    }

    response = requests.post(
        f"{api.base_url}/dmpSegments",
        headers=api.headers,
        json=data
    )

    return response.json()


def upload_company_list(api, segment_id, company_names):
    """Upload list of company names for Account-Based Marketing."""
    import hashlib

    # Hash company names
    hashed_companies = []
    for company in company_names:
        hashed = hashlib.sha256(company.lower().strip().encode()).hexdigest()
        hashed_companies.append(hashed)

    data = {
        "segment": segment_id,
        "userMatchRequest": {
            "companies": hashed_companies
        }
    }

    response = requests.post(
        f"{api.base_url}/dmpSegments/{segment_id}/users",
        headers=api.headers,
        json=data
    )

    return response.json()


def upload_email_list(api, segment_id, emails):
    """Upload email list for matched audience."""
    import hashlib

    # Hash emails with SHA256
    hashed_emails = []
    for email in emails:
        hashed = hashlib.sha256(email.lower().strip().encode()).hexdigest()
        hashed_emails.append(hashed)

    data = {
        "segment": segment_id,
        "userMatchRequest": {
            "emails": hashed_emails
        }
    }

    response = requests.post(
        f"{api.base_url}/dmpSegments/{segment_id}/users",
        headers=api.headers,
        json=data
    )

    return response.json()


def create_lookalike_audience(api, account_id, name, source_segment_id, expansion_size=5):
    """Create a lookalike audience from a matched audience."""

    data = {
        "account": f"urn:li:sponsoredAccount:{account_id}",
        "name": name,
        "type": "LOOKALIKE",
        "lookalikeSpec": {
            "sourceSegment": source_segment_id,
            "expansionSize": expansion_size,  # 1-10 (larger = broader reach)
        }
    }

    response = requests.post(
        f"{api.base_url}/dmpSegments",
        headers=api.headers,
        json=data
    )

    return response.json()


def create_website_retargeting_audience(api, account_id, name, insight_tag_id):
    """Create website retargeting audience using LinkedIn Insight Tag."""

    data = {
        "account": f"urn:li:sponsoredAccount:{account_id}",
        "name": name,
        "type": "WEBSITE_RETARGETING",
        "retargetingRules": [
            {
                "type": "URL",
                "operator": "CONTAINS",
                "value": "/product",
                "lookbackDays": 180
            }
        ],
        "insightTagId": insight_tag_id
    }

    response = requests.post(
        f"{api.base_url}/dmpSegments",
        headers=api.headers,
        json=data
    )

    return response.json()
```

### 4. Lead Gen Forms

**Create and Manage Lead Gen Forms:**
```python
def create_lead_gen_form(api, account_id, form_name, privacy_policy_url):
    """Create a LinkedIn Lead Gen Form."""

    data = {
        "account": f"urn:li:sponsoredAccount:{account_id}",
        "name": form_name,
        "privacyPolicyUrl": privacy_policy_url,
        "locale": {
            "language": "en",
            "country": "US"
        },
        "headline": "Download Our B2B Marketing Guide",
        "description": "Get insights on scaling your B2B marketing strategy",
        "confirmationMessage": "Thank you! We'll send the guide to your email.",
        "callToAction": {
            "label": "DOWNLOAD"  # DOWNLOAD, APPLY, SUBSCRIBE, REGISTER, etc.
        },
        "fields": [
            {
                "type": "FIRST_NAME",
                "required": True
            },
            {
                "type": "LAST_NAME",
                "required": True
            },
            {
                "type": "EMAIL",
                "required": True
            },
            {
                "type": "COMPANY",
                "required": True
            },
            {
                "type": "TITLE",
                "required": False
            },
            {
                "type": "PHONE",
                "required": False
            }
        ]
    }

    response = requests.post(
        f"{api.base_url}/adDirectSponsoredContents",
        headers=api.headers,
        json=data
    )

    return response.json()


def get_lead_gen_form_responses(api, form_id):
    """Retrieve lead form submissions."""

    params = {
        "q": "owner",
        "owner": form_id
    }

    response = requests.get(
        f"{api.base_url}/leadFormResponses",
        headers=api.headers,
        params=params
    )

    data = response.json()

    leads = []
    for element in data.get('elements', []):
        lead_data = {}
        for answer in element.get('answers', []):
            field_name = answer.get('fieldName')
            value = answer.get('answerDetails', {}).get('textAnswer', '')
            lead_data[field_name] = value

        lead_data['submitted_at'] = element.get('submittedAt')
        leads.append(lead_data)

    return pd.DataFrame(leads)
```

## Installation and Authentication

### Install Required Libraries

```bash
pip install requests pandas
```

### Set Up Authentication

1. **Create LinkedIn App** at https://www.linkedin.com/developers/apps
2. **Configure OAuth 2.0** with required scopes:
   - `r_ads` (read ads)
   - `rw_ads` (write ads)
   - `r_ads_reporting` (reporting)
   - `r_organization_social` (for sponsored content)
3. **Get Access Token** via OAuth flow
4. **Find Ad Account ID** in LinkedIn Campaign Manager

### Initialize API Client

```python
import requests

class LinkedInAdsAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

# Initialize
api = LinkedInAdsAPI(access_token="YOUR_ACCESS_TOKEN")
```

## Quick Start Example

```python
from datetime import datetime, timedelta

# Initialize API
api = LinkedInAdsAPI(access_token="YOUR_ACCESS_TOKEN")
account_id = "123456789"

# Get campaign performance for last 30 days
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

df = get_campaign_analytics(api, account_id, start_date, end_date)

# Display results
print(df[['date', 'impressions', 'clicks', 'cost', 'conversions']])
print(f"\nTotal Spend: ${df['cost'].sum():.2f}")
print(f"Total Clicks: {df['clicks'].sum():,}")
print(f"Average CTR: {df['ctr'].mean():.2%}")
print(f"Total Conversions: {df['conversions'].sum():.0f}")
```

## Key Metrics Reference

### Performance Metrics
- **Impressions** - Number of ad views
- **Clicks** - Total clicks on ads
- **Landing Page Clicks** - Clicks to landing page (excludes reactions)
- **CTR** - Click-through rate
- **CPC** - Cost per click
- **CPM** - Cost per 1,000 impressions
- **Spend** - Total amount spent

### Engagement Metrics
- **Likes** - Number of likes on sponsored content
- **Comments** - Number of comments
- **Shares** - Number of shares
- **Follows** - New page/company followers
- **Engagement Rate** - (Likes + Comments + Shares) / Impressions
- **Reactions** - Total social actions

### Conversion Metrics
- **Conversions** - Total conversions tracked
- **Post-Click Conversions** - Conversions from clicks
- **Post-View Conversions** - View-through conversions
- **Cost Per Conversion** - Average cost per conversion
- **Conversion Rate** - Conversions / Clicks

### Video Metrics (for video ads)
- **Video Views** - Total video starts
- **Video Completions** - Videos watched to end
- **Video First Quartile** - 25% completion
- **Video Midpoint** - 50% completion
- **Video Third Quartile** - 75% completion
- **View Rate** - Video views / Impressions

### Lead Gen Metrics
- **Lead Form Opens** - Number of form opens
- **Lead Form Submissions** - Completed submissions
- **Form Completion Rate** - Submissions / Opens
- **Cost Per Lead** - Total spend / Leads

## Best Practices

1. **Professional Targeting**
   - Use job title + job function for precise targeting
   - Target by company size for better budget allocation
   - Use seniority filters for decision-maker targeting
   - Combine targeting criteria with AND logic

2. **Creative Strategy**
   - Keep copy professional and value-focused
   - Use single image ads for thought leadership
   - Carousel ads for product features/case studies
   - Video ads for brand awareness and engagement

3. **Bidding and Budget**
   - Start with maximum delivery bidding
   - Switch to manual bidding after collecting data
   - Minimum daily budget: $10/day per campaign
   - Recommended minimum: $25-$50/day for testing

4. **Lead Generation**
   - Keep forms short (3-5 fields) for higher conversion
   - Always include privacy policy URL
   - Pre-fill fields using LinkedIn profile data
   - Set up automated lead delivery to CRM

5. **Account-Based Marketing**
   - Use matched audiences for target account lists
   - Create separate campaigns per account tier
   - Combine company targeting with job title filters
   - Monitor company-level analytics

6. **Optimization Tips**
   - Rotate creatives every 2-3 weeks to avoid fatigue
   - Test different CTAs and messaging
   - Exclude converted audiences from awareness campaigns
   - Use A/B testing for campaign optimization

## Common Use Cases

### ABM Campaign Setup
```python
def setup_abm_campaign(api, account_id, target_companies, job_titles):
    """Set up account-based marketing campaign."""
    # Create matched audience from company list
    # Build targeting with job titles
    # Create campaign with high-value messaging
    pass
```

### Lead Nurturing
```python
def create_lead_nurture_sequence(api, account_id, form_id):
    """Create retargeting campaign for lead form openers."""
    # Create audience of users who opened form but didn't submit
    # Set up message ads or sponsored content
    # Configure follow-up messaging
    pass
```

### Content Syndication
```python
def promote_content(api, account_id, content_url, target_personas):
    """Promote content to specific professional personas."""
    # Create campaigns for each persona
    # Set up sponsored content with article links
    # Monitor engagement and lead quality
    pass
```

## References

- **Official Documentation**: https://docs.microsoft.com/en-us/linkedin/marketing/
- **Marketing API**: https://docs.microsoft.com/en-us/linkedin/marketing/integrations/ads
- **API Reference**: https://docs.microsoft.com/en-us/linkedin/marketing/integrations/ads/advertising-targeting
- **Lead Gen Forms**: https://docs.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/lead-gen-forms
- **Best Practices**: https://business.linkedin.com/marketing-solutions/ads-guide
- **Targeting Options**: https://business.linkedin.com/marketing-solutions/ad-targeting
- **Developer Portal**: https://www.linkedin.com/developers/
- **Support**: https://www.linkedin.com/help/lms

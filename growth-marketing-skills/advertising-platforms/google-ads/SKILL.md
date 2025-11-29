---
name: google-ads
description: "Google Ads API integration for search, display, video, shopping campaigns. Manage campaigns, ad groups, keywords, bidding, budgets, reporting, audience targeting, and performance analytics."
---

# Google Ads

## Overview

Google Ads (formerly Google AdWords) is the world's largest online advertising platform, offering search ads, display advertising, video ads (YouTube), shopping ads, and app campaigns. The Google Ads API provides programmatic access to create, manage, and optimize advertising campaigns across Google's vast network.

This skill covers the Google Ads API with Python, enabling automated campaign management, performance reporting, bid optimization, and audience targeting at scale.

## When to Use This Skill

Use this skill when you need to:
- Create and manage Google Ads campaigns programmatically
- Automate bid adjustments and budget optimization
- Generate custom performance reports and analytics
- Manage large-scale campaigns across multiple accounts
- Sync campaign data with internal systems
- Implement automated rules and alerts
- Manage keyword lists and negative keywords
- Create and update ad copy at scale
- Implement audience targeting and remarketing lists
- Monitor competitor ads and search terms
- Integrate Google Ads data with data warehouses

## Core Capabilities

### 1. Campaign Management

**Create a Search Campaign:**
```python
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Initialize client
client = GoogleAdsClient.load_from_storage("google-ads.yaml")

customer_id = "1234567890"

def create_search_campaign(client, customer_id):
    """Create a new search campaign."""
    campaign_service = client.get_service("CampaignService")
    campaign_budget_service = client.get_service("CampaignBudgetService")

    # Create campaign budget
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"Budget {uuid.uuid4()}"
    campaign_budget.amount_micros = 50000000  # $50
    campaign_budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD

    budget_response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[campaign_budget_operation]
    )
    budget_resource_name = budget_response.results[0].resource_name

    # Create campaign
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = f"Search Campaign {uuid.uuid4()}"
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.SEARCH
    )
    campaign.status = client.enums.CampaignStatusEnum.PAUSED
    campaign.manual_cpc.enhanced_cpc_enabled = True
    campaign.campaign_budget = budget_resource_name
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = True
    campaign.network_settings.target_content_network = False
    campaign.start_date = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")

    # Set targeting
    campaign.geo_target_type_setting.positive_geo_target_type = (
        client.enums.PositiveGeoTargetTypeEnum.PRESENCE_OR_INTEREST
    )

    campaign_response = campaign_service.mutate_campaigns(
        customer_id=customer_id, operations=[campaign_operation]
    )

    return campaign_response.results[0].resource_name


# Create ad group with keywords
def create_ad_group_with_keywords(client, customer_id, campaign_resource_name):
    """Create an ad group and add keywords."""
    ad_group_service = client.get_service("AdGroupService")
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    # Create ad group
    ad_group_operation = client.get_type("AdGroupOperation")
    ad_group = ad_group_operation.create
    ad_group.name = f"Ad Group {uuid.uuid4()}"
    ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
    ad_group.campaign = campaign_resource_name
    ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    ad_group.cpc_bid_micros = 1000000  # $1.00

    ad_group_response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[ad_group_operation]
    )
    ad_group_resource_name = ad_group_response.results[0].resource_name

    # Add keywords
    keywords = [
        ("data analytics software", "EXACT"),
        ("business intelligence tools", "PHRASE"),
        ("analytics platform", "BROAD"),
    ]

    operations = []
    for keyword_text, match_type in keywords:
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.create
        criterion.ad_group = ad_group_resource_name
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        criterion.keyword.text = keyword_text
        criterion.keyword.match_type = getattr(
            client.enums.KeywordMatchTypeEnum, match_type
        )
        operations.append(operation)

    keyword_response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=operations
    )

    return ad_group_resource_name, keyword_response
```

**Create Responsive Search Ads:**
```python
def create_responsive_search_ad(client, customer_id, ad_group_resource_name):
    """Create a responsive search ad."""
    ad_group_ad_service = client.get_service("AdGroupAdService")

    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.ad_group = ad_group_resource_name
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED

    # Set final URLs
    ad_group_ad.ad.final_urls.append("https://www.example.com")

    # Create responsive search ad
    rsa = ad_group_ad.ad.responsive_search_ad

    # Add headlines (up to 15)
    headline_texts = [
        "Best Analytics Software",
        "Data Insights Platform",
        "Try Free for 30 Days",
        "Trusted by 10,000+ Teams",
    ]
    for text in headline_texts:
        headline = client.get_type("AdTextAsset")
        headline.text = text
        rsa.headlines.append(headline)

    # Add descriptions (up to 4)
    description_texts = [
        "Powerful analytics to drive business growth. Start your free trial today.",
        "Real-time dashboards and automated reporting. No credit card required.",
    ]
    for text in description_texts:
        description = client.get_type("AdTextAsset")
        description.text = text
        rsa.descriptions.append(description)

    response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[ad_group_ad_operation]
    )

    return response.results[0].resource_name
```

### 2. Reporting and Analytics

**Generate Performance Report:**
```python
def get_campaign_performance(client, customer_id, date_range="LAST_30_DAYS"):
    """Get campaign performance metrics."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.average_cpc,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value,
            metrics.cost_per_conversion
        FROM campaign
        WHERE segments.date DURING {date_range}
            AND campaign.status != 'REMOVED'
        ORDER BY metrics.impressions DESC
        LIMIT 100
    """

    response = ga_service.search_stream(customer_id=customer_id, query=query)

    results = []
    for batch in response:
        for row in batch.results:
            results.append({
                "campaign_id": row.campaign.id,
                "campaign_name": row.campaign.name,
                "status": row.campaign.status.name,
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "ctr": row.metrics.ctr,
                "avg_cpc": row.metrics.average_cpc / 1_000_000,  # Convert to dollars
                "cost": row.metrics.cost_micros / 1_000_000,
                "conversions": row.metrics.conversions,
                "conversion_value": row.metrics.conversions_value,
                "cost_per_conversion": row.metrics.cost_per_conversion,
            })

    return pd.DataFrame(results)


# Search term report
def get_search_terms_report(client, customer_id):
    """Get search terms that triggered ads."""
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            campaign.name,
            ad_group.name,
            segments.search_term_match_type,
            segments.search_term,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.cost_micros,
            metrics.conversions
        FROM search_term_view
        WHERE segments.date DURING LAST_30_DAYS
        ORDER BY metrics.impressions DESC
        LIMIT 1000
    """

    response = ga_service.search_stream(customer_id=customer_id, query=query)

    results = []
    for batch in response:
        for row in batch.results:
            results.append({
                "campaign": row.campaign.name,
                "ad_group": row.ad_group.name,
                "search_term": row.segments.search_term,
                "match_type": row.segments.search_term_match_type.name,
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "ctr": row.metrics.ctr,
                "cost": row.metrics.cost_micros / 1_000_000,
                "conversions": row.metrics.conversions,
            })

    return pd.DataFrame(results)


# Keyword performance
def get_keyword_performance(client, customer_id):
    """Get keyword-level performance data."""
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            campaign.name,
            ad_group.name,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.quality_info.quality_score,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.average_cpc,
            metrics.cost_micros,
            metrics.conversions,
            metrics.search_impression_share,
            metrics.search_rank_lost_impression_share
        FROM keyword_view
        WHERE segments.date DURING LAST_30_DAYS
            AND ad_group_criterion.status = 'ENABLED'
        ORDER BY metrics.cost_micros DESC
        LIMIT 500
    """

    response = ga_service.search_stream(customer_id=customer_id, query=query)

    results = []
    for batch in response:
        for row in batch.results:
            results.append({
                "campaign": row.campaign.name,
                "ad_group": row.ad_group.name,
                "keyword": row.ad_group_criterion.keyword.text,
                "match_type": row.ad_group_criterion.keyword.match_type.name,
                "quality_score": row.ad_group_criterion.quality_info.quality_score,
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "ctr": row.metrics.ctr,
                "avg_cpc": row.metrics.average_cpc / 1_000_000,
                "cost": row.metrics.cost_micros / 1_000_000,
                "conversions": row.metrics.conversions,
                "impression_share": row.metrics.search_impression_share,
                "lost_is_rank": row.metrics.search_rank_lost_impression_share,
            })

    return pd.DataFrame(results)
```

### 3. Audience Management

**Create and Manage Remarketing Lists:**
```python
def create_remarketing_list(client, customer_id):
    """Create a remarketing list based on website visitors."""
    user_list_service = client.get_service("UserListService")

    # Create user list operation
    user_list_operation = client.get_type("UserListOperation")
    user_list = user_list_operation.create

    user_list.name = f"Website Visitors - All Pages {uuid.uuid4()}"
    user_list.description = "Remarketing list for all website visitors"
    user_list.membership_life_span = 540  # 540 days (maximum)
    user_list.membership_status = client.enums.UserListMembershipStatusEnum.OPEN

    # Set up rule-based user list
    user_list.rule_based_user_list.prepopulation_status = (
        client.enums.UserListPrepopulationStatusEnum.REQUESTED
    )

    # Define flexible rule for URL contains
    flexible_rule_operation_info = client.get_type(
        "FlexibleRuleOperandInfo"
    )
    flexible_rule_operation_info.rule.rule_item_groups.extend([
        client.get_type("FlexibleRuleItemGroupInfo")
    ])

    rule_item = client.get_type("FlexibleRuleItemInfo")
    rule_item.string_rule_item.operator = (
        client.enums.UserListStringRuleItemOperatorEnum.CONTAINS
    )
    rule_item.string_rule_item.value = "/product"

    user_list.rule_based_user_list.flexible_rule_user_list.inclusive_rule_operator = (
        client.enums.UserListFlexibleRuleOperatorEnum.AND
    )

    response = user_list_service.mutate_user_lists(
        customer_id=customer_id, operations=[user_list_operation]
    )

    return response.results[0].resource_name


def add_audience_to_ad_group(client, customer_id, ad_group_id, user_list_id):
    """Target an ad group with a remarketing list."""
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    operation = client.get_type("AdGroupCriterionOperation")
    criterion = operation.create

    criterion.ad_group = client.get_service("AdGroupService").ad_group_path(
        customer_id, ad_group_id
    )
    criterion.user_list.user_list = user_list_id

    # Set bid modifier for this audience (e.g., bid 20% more)
    criterion.bid_modifier = 1.20

    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=[operation]
    )

    return response.results[0].resource_name


# Customer Match audience upload
def upload_customer_match_list(client, customer_id, emails):
    """Upload customer emails for Customer Match targeting."""
    import hashlib

    offline_user_data_job_service = client.get_service(
        "OfflineUserDataJobService"
    )

    # Create user list first
    user_list_service = client.get_service("UserListService")
    user_list_operation = client.get_type("UserListOperation")
    user_list = user_list_operation.create
    user_list.name = f"Customer Match List {uuid.uuid4()}"
    user_list.crm_based_user_list.upload_key_type = (
        client.enums.CustomerMatchUploadKeyTypeEnum.CONTACT_INFO
    )

    user_list_response = user_list_service.mutate_user_lists(
        customer_id=customer_id, operations=[user_list_operation]
    )
    user_list_resource_name = user_list_response.results[0].resource_name

    # Create offline user data job
    job_operation = client.get_type("OfflineUserDataJobOperation")
    job = job_operation.create
    job.type_ = client.enums.OfflineUserDataJobTypeEnum.CUSTOMER_MATCH_USER_LIST
    job.customer_match_user_list_metadata.user_list = user_list_resource_name

    job_response = offline_user_data_job_service.create_offline_user_data_job(
        customer_id=customer_id, job=job
    )
    job_resource_name = job_response.resource_name

    # Hash and upload emails
    operations = []
    for email in emails:
        operation = client.get_type("OfflineUserDataJobOperation")
        user_data = operation.create

        user_identifier = client.get_type("UserIdentifier")
        # Hash email with SHA256
        user_identifier.hashed_email = hashlib.sha256(
            email.lower().strip().encode()
        ).hexdigest()

        user_data.user_identifiers.append(user_identifier)
        operations.append(operation)

    # Upload in batches of 10,000
    batch_size = 10000
    for i in range(0, len(operations), batch_size):
        batch = operations[i:i + batch_size]
        offline_user_data_job_service.add_offline_user_data_job_operations(
            resource_name=job_resource_name,
            enable_partial_failure=True,
            operations=batch,
        )

    # Run the job
    offline_user_data_job_service.run_offline_user_data_job(
        resource_name=job_resource_name
    )

    return user_list_resource_name
```

### 4. Bid and Budget Optimization

**Automated Bid Adjustments:**
```python
def update_keyword_bids(client, customer_id, bid_adjustments):
    """Update keyword bids based on performance."""
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    operations = []
    for keyword_id, new_bid_micros in bid_adjustments.items():
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.update

        criterion.resource_name = (
            ad_group_criterion_service.ad_group_criterion_path(
                customer_id, keyword_id
            )
        )
        criterion.cpc_bid_micros = new_bid_micros

        # Update only the bid field
        client.copy_from(
            operation.update_mask,
            protobuf_helpers.field_mask(None, criterion._pb),
        )

        operations.append(operation)

    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=operations
    )

    return response


def adjust_campaign_budget(client, customer_id, campaign_id, new_budget_micros):
    """Update campaign budget."""
    campaign_budget_service = client.get_service("CampaignBudgetService")

    # Get current budget resource name
    ga_service = client.get_service("GoogleAdsService")
    query = f"""
        SELECT campaign.campaign_budget
        FROM campaign
        WHERE campaign.id = {campaign_id}
    """
    response = ga_service.search(customer_id=customer_id, query=query)
    budget_resource_name = list(response)[0].campaign.campaign_budget

    # Update budget
    operation = client.get_type("CampaignBudgetOperation")
    budget = operation.update
    budget.resource_name = budget_resource_name
    budget.amount_micros = new_budget_micros

    client.copy_from(
        operation.update_mask,
        protobuf_helpers.field_mask(None, budget._pb),
    )

    response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[operation]
    )

    return response
```

## Installation and Authentication

### Install the Google Ads API Client

```bash
pip install google-ads
```

### Set Up Authentication

1. **Enable the Google Ads API** in your Google Ads account
2. **Create OAuth2 credentials** in Google Cloud Console
3. **Generate refresh token** using OAuth2 flow
4. **Create configuration file** (`google-ads.yaml`):

```yaml
developer_token: YOUR_DEVELOPER_TOKEN
client_id: YOUR_CLIENT_ID
client_secret: YOUR_CLIENT_SECRET
refresh_token: YOUR_REFRESH_TOKEN
login_customer_id: YOUR_LOGIN_CUSTOMER_ID
use_proto_plus: True
```

### Initialize Client

```python
from google.ads.googleads.client import GoogleAdsClient

# Load from YAML file
client = GoogleAdsClient.load_from_storage("google-ads.yaml")

# Or configure programmatically
client = GoogleAdsClient.load_from_dict({
    "developer_token": "YOUR_DEVELOPER_TOKEN",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "refresh_token": "YOUR_REFRESH_TOKEN",
    "login_customer_id": "YOUR_LOGIN_CUSTOMER_ID",
    "use_proto_plus": True,
})
```

## Quick Start Example

```python
from google.ads.googleads.client import GoogleAdsClient
import pandas as pd

# Initialize client
client = GoogleAdsClient.load_from_storage("google-ads.yaml")
customer_id = "1234567890"

# Get campaign performance
ga_service = client.get_service("GoogleAdsService")

query = """
    SELECT
        campaign.id,
        campaign.name,
        metrics.impressions,
        metrics.clicks,
        metrics.ctr,
        metrics.cost_micros,
        metrics.conversions
    FROM campaign
    WHERE segments.date DURING LAST_7_DAYS
    ORDER BY metrics.impressions DESC
"""

response = ga_service.search_stream(customer_id=customer_id, query=query)

# Process results
for batch in response:
    for row in batch.results:
        print(f"Campaign: {row.campaign.name}")
        print(f"  Impressions: {row.metrics.impressions:,}")
        print(f"  Clicks: {row.metrics.clicks:,}")
        print(f"  CTR: {row.metrics.ctr:.2%}")
        print(f"  Cost: ${row.metrics.cost_micros / 1_000_000:,.2f}")
        print(f"  Conversions: {row.metrics.conversions}\n")
```

## Key Metrics Reference

### Performance Metrics
- **Impressions** - Number of times ads were shown
- **Clicks** - Number of clicks on ads
- **CTR (Click-Through Rate)** - Clicks / Impressions
- **CPC (Cost Per Click)** - Total cost / Clicks
- **Conversions** - Number of completed conversion actions
- **Conversion Rate** - Conversions / Clicks
- **Cost Per Conversion** - Total cost / Conversions
- **Conversion Value** - Total value from conversions
- **ROAS (Return on Ad Spend)** - Conversion value / Cost

### Quality & Auction Metrics
- **Quality Score** - 1-10 rating of ad quality and relevance
- **Impression Share** - Percentage of possible impressions received
- **Lost IS (Rank)** - Impressions lost due to low ad rank
- **Lost IS (Budget)** - Impressions lost due to budget constraints
- **Average Position** - Average position of ad on page (deprecated)

### Engagement Metrics
- **Average CPM** - Cost per 1,000 impressions
- **Engagement Rate** - Engagements / Impressions (for video/display)
- **Video Views** - Number of video views
- **View Rate** - Video views / Impressions

### Shopping Metrics (for Shopping campaigns)
- **Product Clicks** - Clicks on product listings
- **Product Impressions** - Product listing impressions
- **Product CTR** - Product clicks / Product impressions

## Best Practices

1. **API Quotas** - Monitor API usage and implement rate limiting
2. **Batch Operations** - Use batch mutations for bulk updates (up to 5,000 operations)
3. **Google Ads Query Language (GAQL)** - Use efficient queries with proper filtering
4. **Error Handling** - Implement retry logic for transient errors
5. **Test in Test Accounts** - Use test/development accounts before production
6. **Version Management** - Stay updated with API versions and migrations
7. **Partial Failure** - Enable partial failure mode for batch operations
8. **Field Masks** - Use field masks to update only specific fields

## Common Use Cases

### Automated Budget Pacing
```python
def check_budget_pacing(client, customer_id):
    """Monitor budget pacing and adjust if needed."""
    # Get current spend vs. budget
    # Calculate expected spend based on days in month
    # Adjust daily budget if over/under pacing
    pass
```

### Smart Bidding Optimization
```python
def optimize_bids_by_performance(client, customer_id):
    """Adjust bids based on conversion performance."""
    # Get keyword performance data
    # Calculate target CPA
    # Adjust bids for keywords above/below target
    pass
```

### Negative Keyword Mining
```python
def find_negative_keywords(client, customer_id, min_cost=10, max_conversions=0):
    """Identify search terms to add as negative keywords."""
    # Get search terms with high cost and no conversions
    # Add to negative keyword lists
    pass
```

## References

- **Official Documentation**: https://developers.google.com/google-ads/api/docs/start
- **Python Client Library**: https://github.com/googleads/google-ads-python
- **API Reference**: https://developers.google.com/google-ads/api/reference/rpc/latest
- **GAQL Guide**: https://developers.google.com/google-ads/api/docs/query/overview
- **Best Practices**: https://developers.google.com/google-ads/api/docs/best-practices
- **Migration Guide**: https://developers.google.com/google-ads/api/docs/migration
- **Rate Limits**: https://developers.google.com/google-ads/api/docs/rate-limits
- **Support Forum**: https://groups.google.com/g/adwords-api

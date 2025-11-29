---
name: salesforce
description: "Salesforce CRM platform. Sales Cloud, Marketing Cloud, lead management, opportunity tracking, campaign attribution, custom objects, Apex, SOQL queries."
---

# Salesforce Integration

## Overview

Salesforce is the world's leading CRM platform, offering Sales Cloud for sales management, Marketing Cloud for marketing automation, and extensive customization capabilities. This skill covers using the Salesforce API to manage leads, track opportunities, analyze pipelines, and integrate with your marketing stack for complete marketing-sales alignment and attribution.

## When to Use This Skill

- Managing leads, contacts, and accounts in CRM
- Tracking sales opportunities and pipeline
- Marketing campaign attribution and ROI
- Lead scoring and qualification
- Sales activity tracking and forecasting
- Custom object creation for vertical-specific workflows
- Integrating marketing automation with sales processes
- Building attribution models across marketing touchpoints
- Syncing customer data between marketing and sales tools

## Core Capabilities

### 1. Lead and Contact Management

```python
from simple_salesforce import Salesforce
import pandas as pd

# Initialize Salesforce connection
sf = Salesforce(
    username='your-email@company.com',
    password='your-password',
    security_token='your-security-token'
)

# Create lead from marketing campaign
def create_lead(lead_data):
    """Create a new lead with marketing attribution."""
    lead = sf.Lead.create({
        'FirstName': lead_data['first_name'],
        'LastName': lead_data['last_name'],
        'Email': lead_data['email'],
        'Company': lead_data['company'],
        'Title': lead_data['title'],
        'LeadSource': lead_data['source'],  # e.g., 'Google Ads', 'LinkedIn'
        'Status': 'Open - Not Contacted',
        'Rating': 'Warm',
        # Marketing attribution fields
        'Campaign__c': lead_data.get('campaign_id'),
        'UTM_Source__c': lead_data.get('utm_source'),
        'UTM_Medium__c': lead_data.get('utm_medium'),
        'UTM_Campaign__c': lead_data.get('utm_campaign'),
        'UTM_Content__c': lead_data.get('utm_content'),
        'First_Touch_Channel__c': lead_data.get('first_touch'),
        'Landing_Page__c': lead_data.get('landing_page')
    })

    return lead['id']

# Example: Create lead from web form
lead_id = create_lead({
    'first_name': 'Sarah',
    'last_name': 'Johnson',
    'email': 'sarah.johnson@techcorp.com',
    'company': 'TechCorp Inc',
    'title': 'VP of Marketing',
    'source': 'Website',
    'campaign_id': 'CAM-2025-Q1',
    'utm_source': 'google',
    'utm_medium': 'cpc',
    'utm_campaign': 'spring-2025-awareness',
    'first_touch': 'Paid Search',
    'landing_page': '/demo-request'
})

print(f"Lead created: {lead_id}")

# Update lead score based on engagement
def update_lead_score(lead_id, score, scoring_factors):
    """Update lead score with detailed breakdown."""
    sf.Lead.update(lead_id, {
        'Lead_Score__c': score,
        'Scoring_Factors__c': scoring_factors,  # JSON string of factors
        'Last_Score_Update__c': datetime.now().isoformat(),
        'Rating': 'Hot' if score >= 80 else 'Warm' if score >= 50 else 'Cold'
    })

# Convert lead to contact/account/opportunity
def convert_lead(lead_id, opportunity_name, amount):
    """Convert qualified lead to contact with opportunity."""
    # Query lead details
    lead = sf.Lead.get(lead_id)

    # Create conversion
    conversion = sf.LeadConvert.create({
        'leadId': lead_id,
        'convertedStatus': 'Qualified',
        'opportunityName': opportunity_name,
        'createOpportunity': True
    })

    # Update opportunity with marketing attribution
    sf.Opportunity.update(conversion['opportunityId'], {
        'Amount': amount,
        'StageName': 'Qualification',
        'LeadSource': lead['LeadSource'],
        'First_Touch_Campaign__c': lead.get('Campaign__c'),
        'Marketing_Attributed_Revenue__c': amount
    })

    return {
        'contact_id': conversion['contactId'],
        'account_id': conversion['accountId'],
        'opportunity_id': conversion['opportunityId']
    }

# Bulk lead enrichment and scoring
def score_and_enrich_leads():
    """Score all open leads based on engagement data."""
    # Query leads with engagement data
    query = """
        SELECT Id, Email, Company, Title, LeadSource,
               Website_Visits__c, Email_Opens__c, Email_Clicks__c,
               Content_Downloads__c, Demo_Requests__c, Lead_Score__c
        FROM Lead
        WHERE Status = 'Open - Not Contacted'
        AND CreatedDate = LAST_N_DAYS:30
    """

    leads = sf.query_all(query)['records']

    for lead in leads:
        # Calculate lead score
        score = 0
        factors = []

        # Engagement scoring
        if lead.get('Website_Visits__c', 0) > 5:
            score += 20
            factors.append('Multiple site visits')

        if lead.get('Email_Opens__c', 0) > 3:
            score += 15
            factors.append('Email engagement')

        if lead.get('Content_Downloads__c', 0) > 0:
            score += 25
            factors.append('Content download')

        if lead.get('Demo_Requests__c', 0) > 0:
            score += 40
            factors.append('Demo request')

        # Firmographic scoring
        if lead.get('Title') and any(title in lead['Title'].lower()
                                     for title in ['vp', 'director', 'ceo', 'cmo']):
            score += 20
            factors.append('Senior title')

        # Update lead
        update_lead_score(
            lead['Id'],
            min(score, 100),
            ', '.join(factors)
        )

    print(f"Scored {len(leads)} leads")
```

### 2. Pipeline Analytics and Forecasting

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Get pipeline snapshot
def get_pipeline_snapshot():
    """Get current pipeline by stage with marketing attribution."""
    query = """
        SELECT Id, Name, StageName, Amount, Probability, CloseDate,
               LeadSource, First_Touch_Campaign__c, Last_Touch_Campaign__c,
               Campaign_Touches__c, Marketing_Attributed_Revenue__c,
               Account.Name, Owner.Name
        FROM Opportunity
        WHERE IsClosed = FALSE
        ORDER BY CloseDate ASC
    """

    opportunities = sf.query_all(query)['records']

    # Convert to DataFrame
    df = pd.DataFrame([{
        'opportunity_id': opp['Id'],
        'opportunity_name': opp['Name'],
        'stage': opp['StageName'],
        'amount': float(opp.get('Amount', 0)),
        'probability': float(opp.get('Probability', 0)),
        'close_date': opp['CloseDate'],
        'lead_source': opp.get('LeadSource'),
        'first_touch_campaign': opp.get('First_Touch_Campaign__c'),
        'last_touch_campaign': opp.get('Last_Touch_Campaign__c'),
        'campaign_touches': opp.get('Campaign_Touches__c', 0),
        'marketing_attributed': float(opp.get('Marketing_Attributed_Revenue__c', 0)),
        'account': opp['Account']['Name'] if opp.get('Account') else None,
        'owner': opp['Owner']['Name'] if opp.get('Owner') else None
    } for opp in opportunities])

    return df

# Pipeline metrics by stage
def analyze_pipeline_by_stage(df):
    """Analyze pipeline velocity and conversion by stage."""
    stage_analysis = df.groupby('stage').agg({
        'opportunity_id': 'count',
        'amount': 'sum',
        'probability': 'mean',
        'marketing_attributed': 'sum'
    }).rename(columns={
        'opportunity_id': 'count',
        'amount': 'total_value',
        'probability': 'avg_probability',
        'marketing_attributed': 'marketing_attributed_value'
    })

    stage_analysis['weighted_value'] = (
        stage_analysis['total_value'] * stage_analysis['avg_probability'] / 100
    )

    stage_analysis['marketing_influence_rate'] = (
        stage_analysis['marketing_attributed_value'] / stage_analysis['total_value'] * 100
    )

    return stage_analysis

# Marketing attribution analysis
def analyze_marketing_attribution(df):
    """Analyze revenue attribution by marketing channel."""
    # First touch attribution
    first_touch = df.groupby('first_touch_campaign').agg({
        'opportunity_id': 'count',
        'amount': 'sum',
        'marketing_attributed': 'sum'
    }).rename(columns={
        'opportunity_id': 'opportunities',
        'amount': 'pipeline_value',
        'marketing_attributed': 'attributed_revenue'
    })

    # Last touch attribution
    last_touch = df.groupby('last_touch_campaign').agg({
        'opportunity_id': 'count',
        'amount': 'sum'
    }).rename(columns={
        'opportunity_id': 'opportunities',
        'amount': 'pipeline_value'
    })

    return {
        'first_touch': first_touch.sort_values('attributed_revenue', ascending=False),
        'last_touch': last_touch.sort_values('pipeline_value', ascending=False)
    }

# Sales velocity calculation
def calculate_sales_velocity():
    """Calculate sales velocity metrics for forecasting."""
    # Last 90 days of closed won opportunities
    query = """
        SELECT Id, CreatedDate, CloseDate, Amount, StageName
        FROM Opportunity
        WHERE IsWon = TRUE
        AND CloseDate = LAST_N_DAYS:90
    """

    won_opps = sf.query_all(query)['records']

    metrics = {
        'total_deals': len(won_opps),
        'total_revenue': sum(float(opp.get('Amount', 0)) for opp in won_opps),
        'average_deal_size': 0,
        'average_sales_cycle_days': 0,
        'win_rate': 0
    }

    if won_opps:
        metrics['average_deal_size'] = metrics['total_revenue'] / metrics['total_deals']

        # Calculate average sales cycle
        cycle_lengths = []
        for opp in won_opps:
            created = datetime.fromisoformat(opp['CreatedDate'].replace('Z', '+00:00'))
            closed = datetime.fromisoformat(opp['CloseDate'])
            cycle_lengths.append((closed - created).days)

        metrics['average_sales_cycle_days'] = np.mean(cycle_lengths)

        # Calculate win rate
        total_closed_query = """
            SELECT COUNT() FROM Opportunity
            WHERE IsClosed = TRUE
            AND CloseDate = LAST_N_DAYS:90
        """
        total_closed = sf.query(total_closed_query)['totalSize']
        metrics['win_rate'] = (metrics['total_deals'] / total_closed * 100) if total_closed > 0 else 0

    # Sales velocity = (Opps * Deal Size * Win Rate) / Sales Cycle Length
    metrics['sales_velocity'] = (
        metrics['total_deals'] *
        metrics['average_deal_size'] *
        (metrics['win_rate'] / 100) /
        max(metrics['average_sales_cycle_days'], 1)
    )

    return metrics

# Example usage
pipeline_df = get_pipeline_snapshot()
stage_metrics = analyze_pipeline_by_stage(pipeline_df)
attribution = analyze_marketing_attribution(pipeline_df)
velocity = calculate_sales_velocity()

print("Pipeline by Stage:")
print(stage_metrics)
print("\nMarketing Attribution (First Touch):")
print(attribution['first_touch'])
print(f"\nSales Velocity: ${velocity['sales_velocity']:,.2f} per day")
```

### 3. Data Enrichment and Lead Routing

```python
import requests

# Enrich lead with external data
def enrich_lead_data(lead_id, email, company_domain):
    """Enrich lead with firmographic data from external sources."""
    # Get lead
    lead = sf.Lead.get(lead_id)

    # Enrichment logic (example with Clearbit)
    enrichment_data = {
        'company_size': None,
        'industry': None,
        'revenue': None,
        'technologies': []
    }

    # Update lead with enriched data
    sf.Lead.update(lead_id, {
        'NumberOfEmployees': enrichment_data.get('company_size'),
        'Industry': enrichment_data.get('industry'),
        'AnnualRevenue': enrichment_data.get('revenue'),
        'Technologies__c': ','.join(enrichment_data.get('technologies', [])),
        'Enrichment_Date__c': datetime.now().isoformat(),
        'Data_Quality_Score__c': calculate_data_quality(lead)
    })

def calculate_data_quality(lead):
    """Calculate data quality score based on field completeness."""
    required_fields = [
        'FirstName', 'LastName', 'Email', 'Company',
        'Title', 'Phone', 'Industry'
    ]

    filled_fields = sum(1 for field in required_fields if lead.get(field))
    return int((filled_fields / len(required_fields)) * 100)

# Intelligent lead routing
def route_lead_to_sales(lead_id):
    """Route lead to appropriate sales rep based on territory and criteria."""
    lead = sf.Lead.get(lead_id)

    # Territory-based routing
    routing_rules = {
        'Enterprise': {
            'criteria': lambda l: l.get('NumberOfEmployees', 0) > 1000,
            'queue': 'Enterprise_Sales_Queue'
        },
        'Mid-Market': {
            'criteria': lambda l: 100 < l.get('NumberOfEmployees', 0) <= 1000,
            'queue': 'Mid_Market_Sales_Queue'
        },
        'SMB': {
            'criteria': lambda l: l.get('NumberOfEmployees', 0) <= 100,
            'queue': 'SMB_Sales_Queue'
        }
    }

    # Apply routing rules
    for segment, rule in routing_rules.items():
        if rule['criteria'](lead):
            # Get queue ID
            queue_query = f"SELECT Id FROM Group WHERE Name = '{rule['queue']}' AND Type = 'Queue'"
            queue = sf.query(queue_query)['records']

            if queue:
                sf.Lead.update(lead_id, {
                    'OwnerId': queue[0]['Id'],
                    'Lead_Routing_Segment__c': segment,
                    'Routed_Date__c': datetime.now().isoformat()
                })

                print(f"Lead routed to {segment} queue")
                return segment

    return None
```

### 4. Sales Activity Tracking and Engagement

```python
# Track sales activities
def log_sales_activity(record_id, activity_type, subject, description):
    """Log sales activity (call, email, meeting) with outcome."""
    task = sf.Task.create({
        'WhoId': record_id,  # Lead or Contact ID
        'Subject': subject,
        'Type': activity_type,  # Call, Email, Meeting
        'Description': description,
        'Status': 'Completed',
        'ActivityDate': datetime.now().date().isoformat(),
        'CallDurationInSeconds': 1800 if activity_type == 'Call' else None
    })

    return task['id']

# Track email engagement
def track_email_engagement(lead_id, email_id, opened=False, clicked=False, link_clicked=None):
    """Track marketing/sales email engagement."""
    lead = sf.Lead.get(lead_id)

    # Increment counters
    current_opens = int(lead.get('Email_Opens__c', 0))
    current_clicks = int(lead.get('Email_Clicks__c', 0))

    updates = {
        'Last_Email_Engagement__c': datetime.now().isoformat()
    }

    if opened:
        updates['Email_Opens__c'] = current_opens + 1
        updates['Last_Email_Open__c'] = datetime.now().isoformat()

    if clicked:
        updates['Email_Clicks__c'] = current_clicks + 1
        updates['Last_Email_Click__c'] = datetime.now().isoformat()
        updates['Last_Clicked_Link__c'] = link_clicked

    sf.Lead.update(lead_id, updates)

    # Re-score lead based on new engagement
    new_score = calculate_engagement_score(lead_id)
    update_lead_score(lead_id, new_score, 'Email engagement')

# Get sales activity summary
def get_activity_summary(owner_id, days=30):
    """Get activity summary for sales rep."""
    query = f"""
        SELECT Type, COUNT(Id) total
        FROM Task
        WHERE OwnerId = '{owner_id}'
        AND CreatedDate = LAST_N_DAYS:{days}
        GROUP BY Type
    """

    activities = sf.query(query)['records']

    summary = {activity['Type']: activity['total'] for activity in activities}

    return summary

# Campaign member tracking for attribution
def add_lead_to_campaign(lead_id, campaign_id, status='Sent'):
    """Add lead to campaign and track for attribution."""
    member = sf.CampaignMember.create({
        'LeadId': lead_id,
        'CampaignId': campaign_id,
        'Status': status
    })

    # Update lead with campaign touch
    lead = sf.Lead.get(lead_id)
    campaign_touches = int(lead.get('Campaign_Touches__c', 0))

    sf.Lead.update(lead_id, {
        'Campaign_Touches__c': campaign_touches + 1,
        'Last_Campaign_Touch__c': campaign_id,
        'Last_Campaign_Date__c': datetime.now().isoformat()
    })

    return member['id']
```

## Installation

```bash
# Install Salesforce Simple-Salesforce library
uv pip install simple-salesforce

# For more advanced features, install Salesforce DX
uv pip install salesforce-python

# Additional libraries for analytics
uv pip install pandas numpy python-dateutil
```

## Authentication

### Using Username/Password/Security Token

```python
from simple_salesforce import Salesforce

sf = Salesforce(
    username='your-email@company.com',
    password='your-password',
    security_token='your-security-token'
)
```

### Using OAuth 2.0 (Recommended for production)

```python
from simple_salesforce import Salesforce

sf = Salesforce(
    instance_url='https://your-instance.salesforce.com',
    session_id='your-session-id'
)

# Or using OAuth flow
from simple_salesforce import SalesforceLogin

session_id, instance = SalesforceLogin(
    username='your-email@company.com',
    password='your-password',
    security_token='your-security-token'
)

sf = Salesforce(instance=instance, session_id=session_id)
```

To get credentials:
1. Go to Setup > My Personal Information > Reset Security Token
2. Copy your security token from email
3. For OAuth apps: Setup > Apps > App Manager > New Connected App

## Quick Start

```python
from simple_salesforce import Salesforce
from datetime import datetime

# Connect to Salesforce
sf = Salesforce(
    username='your-email@company.com',
    password='your-password',
    security_token='your-security-token'
)

# Create a lead with marketing attribution
lead = sf.Lead.create({
    'FirstName': 'John',
    'LastName': 'Doe',
    'Email': 'john.doe@example.com',
    'Company': 'Example Corp',
    'Title': 'Marketing Director',
    'LeadSource': 'Google Ads',
    'Status': 'Open - Not Contacted',
    'UTM_Source__c': 'google',
    'UTM_Medium__c': 'cpc',
    'UTM_Campaign__c': 'brand-awareness-q1',
    'Lead_Score__c': 65
})

print(f"Lead created: {lead['id']}")

# Query high-value leads
high_value_leads = sf.query("""
    SELECT Id, Name, Email, Company, Lead_Score__c, LeadSource
    FROM Lead
    WHERE Lead_Score__c >= 80
    AND Status = 'Open - Not Contacted'
    ORDER BY Lead_Score__c DESC
    LIMIT 10
""")

for lead in high_value_leads['records']:
    print(f"{lead['Name']} - Score: {lead['Lead_Score__c']} - Source: {lead['LeadSource']}")
```

## Key Features Reference

- **Sales Cloud**: Lead/contact/account management, opportunity tracking
- **Marketing Cloud**: Email campaigns, journey builder, attribution
- **Custom Objects**: Vertical-specific data models
- **SOQL**: Salesforce Object Query Language for data retrieval
- **Apex**: Server-side programming for complex business logic
- **Process Builder/Flow**: No-code automation and workflows
- **Reports & Dashboards**: Analytics and visualization
- **AppExchange**: Ecosystem of third-party integrations
- **Salesforce DX**: Development and deployment tools

## References

- [Salesforce API Documentation](https://developer.salesforce.com/docs/apis)
- [Simple Salesforce GitHub](https://github.com/simple-salesforce/simple-salesforce)
- [SOQL Reference Guide](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/)
- [REST API Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/)
- [Marketing Cloud APIs](https://developer.salesforce.com/docs/marketing/marketing-cloud)
- [Trailhead Learning Platform](https://trailhead.salesforce.com/)

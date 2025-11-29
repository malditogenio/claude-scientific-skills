---
name: apollo-io
description: "Apollo.io sales intelligence platform. B2B contact database, prospecting, email sequences, data enrichment, intent signals, outreach automation."
---

# Apollo.io Integration

## Overview

Apollo.io is a comprehensive sales intelligence and engagement platform combining a B2B contact database with prospecting tools, email sequences, and analytics. This skill covers using the Apollo API to find prospects, enrich data, execute outreach campaigns, and track engagement for complete sales and marketing alignment.

## When to Use This Skill

- B2B prospecting and lead generation
- Contact and company data enrichment
- Building targeted prospect lists
- Automated email outreach sequences
- Lead scoring based on engagement
- Intent signal detection and tracking
- Sales and marketing alignment on target accounts
- Account-based marketing (ABM) campaigns
- CRM data enrichment and cleanup

## Core Capabilities

### 1. Prospecting and Lead Generation

```python
import requests
import json
from datetime import datetime
import pandas as pd

# Apollo API configuration
API_KEY = 'your-apollo-api-key'
BASE_URL = 'https://api.apollo.io/v1'

def api_request(endpoint, method='GET', data=None):
    """Make Apollo API request."""
    url = f'{BASE_URL}/{endpoint}'
    headers = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'X-Api-Key': API_KEY
    }

    if method == 'GET':
        response = requests.get(url, headers=headers, params=data)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=data)

    return response.json()

# Search for people (contacts)
def search_people(person_titles=None, company_size=None, industry=None, location=None, keywords=None, page=1):
    """Search Apollo database for contacts matching criteria."""
    search_data = {
        'page': page,
        'per_page': 100,
        'person_titles': person_titles or [],
        'organization_num_employees_ranges': company_size or [],
        'organization_industry_tag_ids': industry or [],
        'person_locations': location or [],
        'q_keywords': keywords
    }

    result = api_request('mixed_people/search', method='POST', data=search_data)
    return result

# Search for companies
def search_companies(industry=None, employee_range=None, revenue_range=None, location=None, technologies=None):
    """Search for companies matching criteria."""
    search_data = {
        'page': 1,
        'per_page': 100,
        'organization_industry_tag_ids': industry or [],
        'organization_num_employees_ranges': employee_range or [],
        'organization_estimated_revenue_ranges': revenue_range or [],
        'organization_locations': location or [],
        'technologies': technologies or []
    }

    result = api_request('mixed_companies/search', method='POST', data=search_data)
    return result

# Example: Find VP of Marketing at tech companies
prospects = search_people(
    person_titles=['VP of Marketing', 'Chief Marketing Officer', 'Head of Marketing'],
    company_size=['11-50', '51-200', '201-500'],
    industry=['5567cd4773696439b10b0000'],  # Software/Technology
    location=['San Francisco, CA', 'New York, NY', 'Austin, TX'],
    keywords='SaaS B2B'
)

print(f"Found {prospects['pagination']['total_entries']} prospects")

# Export prospects to DataFrame
def prospects_to_dataframe(search_results):
    """Convert search results to pandas DataFrame."""
    people = search_results.get('people', [])

    df = pd.DataFrame([{
        'id': person['id'],
        'name': person['name'],
        'title': person['title'],
        'email': person.get('email'),
        'phone': person.get('phone_numbers', [{}])[0].get('raw_number') if person.get('phone_numbers') else None,
        'company': person['organization']['name'] if person.get('organization') else None,
        'company_size': person['organization'].get('estimated_num_employees') if person.get('organization') else None,
        'company_industry': person['organization'].get('industry') if person.get('organization') else None,
        'company_website': person['organization'].get('website_url') if person.get('organization') else None,
        'linkedin_url': person.get('linkedin_url'),
        'seniority': person.get('seniority')
    } for person in people])

    return df

prospects_df = prospects_to_dataframe(prospects)
print(prospects_df.head())
```

### 2. Data Enrichment

```python
# Enrich person by email
def enrich_person(email):
    """Enrich contact data using email address."""
    data = {
        'email': email,
        'reveal_personal_emails': True
    }

    result = api_request('people/match', method='POST', data=data)
    return result.get('person', {})

# Enrich company by domain
def enrich_company(domain):
    """Enrich company data using domain."""
    data = {
        'domain': domain
    }

    result = api_request('organizations/enrich', method='POST', data=data)
    return result.get('organization', {})

# Bulk enrichment
def bulk_enrich_contacts(email_list):
    """Enrich multiple contacts."""
    enriched_data = []

    for email in email_list:
        try:
            person_data = enrich_person(email)

            enriched = {
                'email': email,
                'name': person_data.get('name'),
                'title': person_data.get('title'),
                'company': person_data.get('organization', {}).get('name'),
                'company_size': person_data.get('organization', {}).get('estimated_num_employees'),
                'industry': person_data.get('organization', {}).get('industry'),
                'phone': person_data.get('phone_numbers', [{}])[0].get('raw_number') if person_data.get('phone_numbers') else None,
                'linkedin': person_data.get('linkedin_url'),
                'seniority': person_data.get('seniority'),
                'departments': person_data.get('departments', [])
            }

            enriched_data.append(enriched)

        except Exception as e:
            print(f"Error enriching {email}: {e}")
            enriched_data.append({'email': email, 'error': str(e)})

    return pd.DataFrame(enriched_data)

# Example: Enrich leads from marketing campaign
campaign_emails = ['lead1@company.com', 'lead2@startup.io', 'lead3@enterprise.com']
enriched_df = bulk_enrich_contacts(campaign_emails)

print("Enriched contact data:")
print(enriched_df[['email', 'name', 'title', 'company', 'company_size']])

# Get person intent signals
def get_person_intent(person_id):
    """Get intent signals for a person."""
    # Note: This requires Apollo's intent data access
    result = api_request(f'people/{person_id}')

    person = result.get('person', {})

    intent_signals = {
        'recent_job_change': person.get('employment_history', [{}])[0].get('current', False)
        if person.get('employment_history') else False,
        'hiring': person.get('organization', {}).get('currently_hiring', False),
        'funding_events': person.get('organization', {}).get('funding_events', []),
        'technologies': person.get('organization', {}).get('technologies', []),
        'keywords': person.get('headline_keywords', [])
    }

    return intent_signals
```

### 3. Sales Activity and Outreach

```python
# Add contact to sequence
def add_to_sequence(email, sequence_id, mailbox_id=None):
    """Add contact to email sequence."""
    data = {
        'email': email,
        'sequence_id': sequence_id,
        'mailbox_id': mailbox_id
    }

    result = api_request('emailer_campaigns/add_contact', method='POST', data=data)
    return result

# Create email sequence
def create_sequence(name, steps, schedule=None):
    """Create multi-step email sequence."""
    # Note: Sequences are typically created in Apollo UI
    # This shows the structure for API automation

    sequence_data = {
        'name': name,
        'steps': steps,
        'schedule': schedule or {
            'send_days': [1, 2, 3, 4, 5],  # Monday-Friday
            'send_start_time': '09:00',
            'send_end_time': '17:00',
            'timezone': 'America/Los_Angeles'
        }
    }

    # Example step structure:
    # {
    #     'type': 'email',
    #     'wait_time': 2,  # days
    #     'subject': 'Email subject with {{first_name}}',
    #     'body': 'Email body with personalization',
    #     'template_id': 'template_xxx'
    # }

    return sequence_data

# Track email engagement
def get_email_engagement(email_id):
    """Get email open/click data."""
    result = api_request(f'emailer_messages/{email_id}')

    message = result.get('emailer_message', {})

    engagement = {
        'email_id': email_id,
        'status': message.get('status'),
        'opened': message.get('opened', False),
        'clicked': message.get('clicked', False),
        'replied': message.get('replied', False),
        'bounced': message.get('bounced', False),
        'open_count': message.get('open_count', 0),
        'click_count': message.get('click_count', 0),
        'first_opened_at': message.get('first_opened_at'),
        'first_clicked_at': message.get('first_clicked_at')
    }

    return engagement

# Log activity
def create_task(contact_id, note, due_date=None, task_type='call'):
    """Create follow-up task."""
    data = {
        'contact_id': contact_id,
        'note': note,
        'due_date': due_date or datetime.now().isoformat(),
        'type': task_type,
        'status': 'pending'
    }

    result = api_request('tasks', method='POST', data=data)
    return result

# Get sequence analytics
def get_sequence_performance(sequence_id):
    """Get performance metrics for email sequence."""
    result = api_request(f'emailer_campaigns/{sequence_id}/analytics')

    analytics = result.get('analytics', {})

    metrics = {
        'sequence_id': sequence_id,
        'total_contacts': analytics.get('num_contacted', 0),
        'emails_sent': analytics.get('num_sent', 0),
        'emails_delivered': analytics.get('num_delivered', 0),
        'emails_opened': analytics.get('num_opened', 0),
        'emails_clicked': analytics.get('num_clicked', 0),
        'emails_replied': analytics.get('num_replied', 0),
        'emails_bounced': analytics.get('num_bounced', 0),
        'open_rate': analytics.get('open_rate', 0) * 100,
        'click_rate': analytics.get('click_rate', 0) * 100,
        'reply_rate': analytics.get('reply_rate', 0) * 100,
        'bounce_rate': analytics.get('bounce_rate', 0) * 100
    }

    return metrics
```

### 4. Lead Scoring and Attribution

```python
# Calculate lead score based on Apollo data
def calculate_apollo_lead_score(person_data):
    """Score lead based on firmographic and engagement data."""
    score = 0
    factors = []

    # Email validity
    if person_data.get('email_status') == 'verified':
        score += 15
        factors.append('Verified email')

    # Seniority level
    seniority = person_data.get('seniority', '').lower()
    if 'c_suite' in seniority or 'vp' in seniority:
        score += 25
        factors.append('Senior decision maker')
    elif 'director' in seniority or 'manager' in seniority:
        score += 15
        factors.append('Manager level')

    # Company size (ICP fit)
    if person_data.get('organization'):
        employee_count = person_data['organization'].get('estimated_num_employees', 0)

        if 100 <= employee_count <= 1000:
            score += 20
            factors.append('Ideal company size')
        elif employee_count > 1000:
            score += 15
            factors.append('Enterprise')

    # Industry fit
    target_industries = ['Computer Software', 'Internet', 'Information Technology']
    if person_data.get('organization', {}).get('industry') in target_industries:
        score += 15
        factors.append('Target industry')

    # Technologies used (intent signal)
    if person_data.get('organization', {}).get('technologies'):
        relevant_tech = ['Salesforce', 'HubSpot', 'Google Analytics', 'Marketo']
        used_tech = person_data['organization'].get('technologies', [])

        if any(tech in used_tech for tech in relevant_tech):
            score += 20
            factors.append('Uses relevant tech stack')

    # Recent funding (buying signal)
    if person_data.get('organization', {}).get('latest_funding_stage'):
        score += 10
        factors.append('Recently funded')

    # Email engagement (if available)
    if person_data.get('email_engagement'):
        if person_data['email_engagement'].get('opened'):
            score += 10
            factors.append('Email engagement')
        if person_data['email_engagement'].get('clicked'):
            score += 15
            factors.append('Clicked email link')

    return {
        'score': min(score, 100),
        'factors': factors,
        'grade': 'A' if score >= 80 else 'B' if score >= 60 else 'C' if score >= 40 else 'D'
    }

# Score and prioritize prospect list
def score_prospect_list(prospects_df):
    """Score all prospects in DataFrame."""
    scores = []

    for _, prospect in prospects_df.iterrows():
        # Enrich to get full data
        person_data = enrich_person(prospect['email']) if prospect.get('email') else {}

        scoring_result = calculate_apollo_lead_score(person_data)

        scores.append({
            'email': prospect.get('email'),
            'name': prospect.get('name'),
            'company': prospect.get('company'),
            'score': scoring_result['score'],
            'grade': scoring_result['grade'],
            'factors': ', '.join(scoring_result['factors'])
        })

    scored_df = pd.DataFrame(scores)
    return scored_df.sort_values('score', ascending=False)

# Track attribution and ROI
def analyze_apollo_attribution(sequence_id, crm_won_deals):
    """Analyze contribution of Apollo sequences to closed deals."""
    # Get sequence contacts
    sequence_perf = get_sequence_performance(sequence_id)

    # Match with CRM won deals
    # This assumes you have CRM data with email addresses

    attribution = {
        'sequence_id': sequence_id,
        'total_contacted': sequence_perf['total_contacts'],
        'total_replied': sequence_perf['emails_replied'],
        'deals_influenced': 0,
        'deal_value': 0,
        'roi': 0
    }

    # Calculate deals influenced
    for deal in crm_won_deals:
        # Check if contact was in sequence
        # This is simplified - you'd match by email
        if deal.get('from_apollo_sequence'):
            attribution['deals_influenced'] += 1
            attribution['deal_value'] += deal.get('amount', 0)

    # Calculate ROI
    # Assuming cost per contact
    cost_per_contact = 0.50  # Example cost
    total_cost = attribution['total_contacted'] * cost_per_contact
    attribution['roi'] = (attribution['deal_value'] / total_cost - 1) * 100 if total_cost > 0 else 0

    return attribution
```

## Installation

```bash
# Apollo doesn't have an official Python SDK
# Use requests library for API calls
uv pip install requests pandas python-dateutil
```

## Authentication

```python
import requests

# Apollo uses API key authentication
API_KEY = 'your-apollo-api-key'
BASE_URL = 'https://api.apollo.io/v1'

headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'X-Api-Key': API_KEY
}

# Make request
response = requests.post(
    f'{BASE_URL}/mixed_people/search',
    headers=headers,
    json={'page': 1, 'per_page': 10}
)
```

To get API key:
1. Log into Apollo.io
2. Go to Settings > API
3. Generate API key
4. Copy the key

## Quick Start

```python
import requests

# Configuration
API_KEY = 'your-apollo-api-key'
BASE_URL = 'https://api.apollo.io/v1'

headers = {
    'Content-Type': 'application/json',
    'X-Api-Key': API_KEY
}

# Search for prospects
search_data = {
    'page': 1,
    'per_page': 25,
    'person_titles': ['VP of Marketing', 'CMO'],
    'organization_num_employees_ranges': ['51-200', '201-500'],
    'q_keywords': 'SaaS'
}

response = requests.post(
    f'{BASE_URL}/mixed_people/search',
    headers=headers,
    json=search_data
)

results = response.json()
print(f"Found {results['pagination']['total_entries']} prospects")

# Display first few results
for person in results['people'][:5]:
    print(f"{person['name']} - {person['title']} at {person.get('organization', {}).get('name')}")
    print(f"Email: {person.get('email')}")
    print("---")

# Enrich a contact
enrich_data = {
    'email': 'prospect@company.com',
    'reveal_personal_emails': True
}

enrich_response = requests.post(
    f'{BASE_URL}/people/match',
    headers=headers,
    json=enrich_data
)

enriched = enrich_response.json()
print(f"Enriched data: {enriched.get('person', {}).get('name')}")
```

## Key Features Reference

- **Contact Database**: 275M+ contacts, 73M+ companies
- **Prospecting**: Advanced search with 65+ filters
- **Data Enrichment**: Real-time contact/company enrichment
- **Email Sequences**: Automated multi-step outreach
- **Email Tracking**: Open, click, reply tracking
- **Chrome Extension**: Prospecting from LinkedIn/web
- **Intent Signals**: Job changes, funding, hiring
- **Technology Tracking**: 6000+ technologies tracked
- **CRM Integration**: Salesforce, HubSpot sync
- **API Access**: Full programmatic access

## References

- [Apollo.io API Documentation](https://apolloio.github.io/apollo-api-docs/)
- [API Authentication](https://apolloio.github.io/apollo-api-docs/#authentication)
- [People Search API](https://apolloio.github.io/apollo-api-docs/#people-search)
- [Enrichment API](https://apolloio.github.io/apollo-api-docs/#enrichment)
- [Sequences API](https://apolloio.github.io/apollo-api-docs/#sequences)
- [Rate Limits](https://apolloio.github.io/apollo-api-docs/#rate-limiting)

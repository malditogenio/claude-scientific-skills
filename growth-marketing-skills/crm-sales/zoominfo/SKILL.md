---
name: zoominfo
description: "ZoomInfo B2B contact database. Company/contact data, technographics, intent signals, organizational charts, direct dials, data enrichment, prospecting."
---

# ZoomInfo Integration

## Overview

ZoomInfo is the leading B2B contact database and go-to-market intelligence platform with over 200M contacts and 100M companies. This skill covers using the ZoomInfo API to find prospects, enrich data, identify intent signals, and build targeted account lists for sales and marketing.

## When to Use This Skill

- B2B prospecting and lead generation
- Contact and company data enrichment
- Technographic analysis and targeting
- Intent signal detection and prioritization
- Account-based marketing (ABM) list building
- Organizational chart mapping
- Direct dial and email discovery
- CRM data enrichment and cleanup
- Competitive intelligence gathering

## Core Capabilities

### 1. Contact and Company Search

```python
import requests
import json
from datetime import datetime
import pandas as pd

# ZoomInfo API configuration
API_KEY = 'your-zoominfo-api-key'
BASE_URL = 'https://api.zoominfo.com'

def get_access_token(username, password):
    """Get OAuth access token."""
    url = f'{BASE_URL}/authenticate'

    data = {
        'username': username,
        'password': password
    }

    response = requests.post(url, json=data)
    return response.json().get('jwt')

# Initialize with access token
ACCESS_TOKEN = get_access_token('your-username', 'your-password')

def api_request(endpoint, method='POST', data=None):
    """Make ZoomInfo API request."""
    url = f'{BASE_URL}/{endpoint}'
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=data)

    return response.json()

# Search for contacts
def search_contacts(job_titles=None, company_revenue=None, company_size=None,
                   location=None, industry=None, technologies=None, max_results=100):
    """Search for contacts matching criteria."""
    search_data = {
        'jobTitleSearchRequests': [
            {'jobTitles': job_titles or []}
        ],
        'companySearchRequests': [
            {
                'revenueRange': company_revenue,
                'employeeRange': company_size,
                'companyLocations': location,
                'companyIndustries': industry,
                'technologies': technologies
            }
        ],
        'outputFields': [
            'id', 'firstName', 'lastName', 'email', 'phone', 'directPhone',
            'jobTitle', 'managementLevel', 'companyName', 'companyId',
            'companyRevenue', 'companyEmployeeCount', 'companyIndustry'
        ],
        'page': 1,
        'rpp': max_results  # Results per page
    }

    result = api_request('search/contact', method='POST', data=search_data)
    return result.get('data', [])

# Search for companies
def search_companies(revenue_range=None, employee_range=None, industry=None,
                    location=None, technologies=None, max_results=100):
    """Search for companies matching criteria."""
    search_data = {
        'companySearchRequests': [
            {
                'revenueRange': revenue_range,
                'employeeRange': employee_range,
                'companyIndustries': industry,
                'companyLocations': location,
                'technologies': technologies
            }
        ],
        'outputFields': [
            'id', 'companyName', 'website', 'revenue', 'employeeCount',
            'industry', 'description', 'foundedYear', 'phone',
            'companyStreetAddress', 'companyCity', 'companyState',
            'companyCountry', 'technologies'
        ],
        'page': 1,
        'rpp': max_results
    }

    result = api_request('search/company', method='POST', data=search_data)
    return result.get('data', [])

# Example: Find VP of Marketing at tech companies
contacts = search_contacts(
    job_titles=['VP of Marketing', 'Chief Marketing Officer', 'Head of Marketing'],
    company_revenue={'min': 10000000, 'max': 100000000},  # $10M-$100M
    company_size={'min': 100, 'max': 1000},
    industry=['Computer Software', 'Information Technology'],
    location=['United States'],
    technologies=['Salesforce', 'HubSpot', 'Google Analytics']
)

print(f"Found {len(contacts)} contacts")

# Convert to DataFrame
contacts_df = pd.DataFrame(contacts)
print(contacts_df[['firstName', 'lastName', 'email', 'jobTitle', 'companyName']].head())

# Example: Find SaaS companies with specific tech stack
companies = search_companies(
    employee_range={'min': 50, 'max': 500},
    industry=['Computer Software', 'SaaS'],
    technologies=['AWS', 'Segment', 'Stripe'],
    location=['San Francisco, CA', 'New York, NY', 'Austin, TX']
)

print(f"Found {len(companies)} companies")
```

### 2. Data Enrichment

```python
# Enrich contact by email
def enrich_contact_by_email(email):
    """Enrich contact data using email address."""
    search_data = {
        'emailAddress': email,
        'outputFields': [
            'id', 'firstName', 'lastName', 'email', 'phone', 'directPhone',
            'mobilePhone', 'jobTitle', 'jobFunction', 'managementLevel',
            'companyName', 'companyId', 'companyRevenue', 'companyEmployeeCount',
            'companyIndustry', 'companyDescription', 'linkedInUrl',
            'technologies', 'departmentSize'
        ]
    }

    result = api_request('enrich/contact', method='POST', data=search_data)
    return result.get('data', {})

# Enrich company by domain
def enrich_company_by_domain(domain):
    """Enrich company data using domain."""
    search_data = {
        'website': domain,
        'outputFields': [
            'id', 'companyName', 'website', 'revenue', 'employeeCount',
            'industry', 'subIndustry', 'description', 'foundedYear',
            'phone', 'companyStreetAddress', 'companyCity', 'companyState',
            'companyCountry', 'technologies', 'numberOfLocations',
            'sicCodes', 'naicsCodes', 'ticker', 'ownership'
        ]
    }

    result = api_request('enrich/company', method='POST', data=search_data)
    return result.get('data', {})

# Bulk enrichment
def bulk_enrich_contacts(email_list):
    """Enrich multiple contacts."""
    enriched_data = []

    for email in email_list:
        try:
            contact_data = enrich_contact_by_email(email)

            if contact_data:
                enriched = {
                    'email': email,
                    'name': f"{contact_data.get('firstName', '')} {contact_data.get('lastName', '')}".strip(),
                    'title': contact_data.get('jobTitle'),
                    'management_level': contact_data.get('managementLevel'),
                    'company': contact_data.get('companyName'),
                    'company_size': contact_data.get('companyEmployeeCount'),
                    'company_revenue': contact_data.get('companyRevenue'),
                    'industry': contact_data.get('companyIndustry'),
                    'direct_phone': contact_data.get('directPhone'),
                    'mobile_phone': contact_data.get('mobilePhone'),
                    'linkedin': contact_data.get('linkedInUrl'),
                    'technologies': contact_data.get('technologies', [])
                }

                enriched_data.append(enriched)

        except Exception as e:
            print(f"Error enriching {email}: {e}")
            enriched_data.append({'email': email, 'error': str(e)})

    return pd.DataFrame(enriched_data)

# Get organizational chart
def get_org_chart(company_id, department=None):
    """Get organizational chart for company."""
    search_data = {
        'companyId': company_id,
        'department': department,
        'outputFields': [
            'id', 'firstName', 'lastName', 'jobTitle', 'managementLevel',
            'email', 'directPhone', 'reportsTo'
        ]
    }

    result = api_request('search/contact', method='POST', data=search_data)
    contacts = result.get('data', [])

    # Build org chart structure
    org_chart = []
    for contact in contacts:
        org_chart.append({
            'id': contact.get('id'),
            'name': f"{contact.get('firstName')} {contact.get('lastName')}",
            'title': contact.get('jobTitle'),
            'level': contact.get('managementLevel'),
            'email': contact.get('email'),
            'phone': contact.get('directPhone'),
            'reports_to': contact.get('reportsTo')
        })

    return org_chart
```

### 3. Intent Signals and Technographics

```python
# Get companies with intent signals
def get_intent_companies(topics, intent_strength='strong'):
    """Find companies showing buying intent on specific topics."""
    search_data = {
        'intentSearchRequests': [
            {
                'topics': topics,
                'intentStrength': intent_strength  # 'strong', 'moderate', 'weak'
            }
        ],
        'outputFields': [
            'id', 'companyName', 'website', 'employeeCount', 'revenue',
            'industry', 'intentTopics', 'intentScore', 'technologies'
        ],
        'page': 1,
        'rpp': 100
    }

    result = api_request('search/company', method='POST', data=search_data)
    return result.get('data', [])

# Search by technology usage
def search_by_technology(technologies, employee_range=None):
    """Find companies using specific technologies."""
    search_data = {
        'companySearchRequests': [
            {
                'technologies': technologies,
                'employeeRange': employee_range
            }
        ],
        'outputFields': [
            'id', 'companyName', 'website', 'employeeCount', 'revenue',
            'industry', 'technologies', 'technologyCategories'
        ],
        'page': 1,
        'rpp': 100
    }

    result = api_request('search/company', method='POST', data=search_data)
    return result.get('data', [])

# Technographic analysis
def analyze_technographics(company_id):
    """Get detailed technology stack for company."""
    company_data = api_request(f'company/{company_id}')

    tech_analysis = {
        'company_id': company_id,
        'company_name': company_data.get('companyName'),
        'technologies': company_data.get('technologies', []),
        'technology_categories': {},
        'total_technologies': len(company_data.get('technologies', []))
    }

    # Categorize technologies
    for tech in company_data.get('technologies', []):
        category = tech.get('category', 'Other')
        if category not in tech_analysis['technology_categories']:
            tech_analysis['technology_categories'][category] = []

        tech_analysis['technology_categories'][category].append(tech.get('name'))

    return tech_analysis

# Example: Find companies with CRM intent
intent_companies = get_intent_companies(
    topics=['CRM Software', 'Sales Automation', 'Marketing Automation'],
    intent_strength='strong'
)

print(f"Found {len(intent_companies)} companies with strong CRM intent")

# Find companies using competitor products
competitor_users = search_by_technology(
    technologies=['Competitor CRM', 'Competitor Platform'],
    employee_range={'min': 100, 'max': 1000}
)

print(f"Found {len(competitor_users)} companies using competitor technology")
```

### 4. Lead Scoring and Prioritization

```python
# Calculate lead score based on ZoomInfo data
def calculate_zoominfo_lead_score(contact_data):
    """Score lead based on firmographic and intent data."""
    score = 0
    factors = []

    # Management level scoring
    mgmt_level = contact_data.get('managementLevel', '').lower()
    if 'c-level' in mgmt_level or 'executive' in mgmt_level:
        score += 30
        factors.append('Executive level')
    elif 'vp' in mgmt_level or 'vice president' in mgmt_level:
        score += 25
        factors.append('VP level')
    elif 'director' in mgmt_level:
        score += 20
        factors.append('Director level')
    elif 'manager' in mgmt_level:
        score += 10
        factors.append('Manager level')

    # Company size scoring
    employee_count = contact_data.get('companyEmployeeCount', 0)
    if 100 <= employee_count <= 1000:
        score += 25
        factors.append('Ideal company size')
    elif employee_count > 1000:
        score += 20
        factors.append('Enterprise')
    elif 50 <= employee_count < 100:
        score += 15
        factors.append('Mid-market')

    # Revenue scoring
    revenue = contact_data.get('companyRevenue', 0)
    if revenue > 100000000:  # $100M+
        score += 20
        factors.append('High revenue')
    elif revenue > 10000000:  # $10M+
        score += 15
        factors.append('Good revenue')

    # Technology stack scoring
    target_tech = ['Salesforce', 'HubSpot', 'Marketo', 'Pardot']
    technologies = contact_data.get('technologies', [])

    matching_tech = [tech for tech in technologies if tech in target_tech]
    if matching_tech:
        score += 15
        factors.append(f'Uses {len(matching_tech)} target technologies')

    # Intent signal scoring
    if contact_data.get('intentScore'):
        intent_score = contact_data.get('intentScore', 0)
        if intent_score >= 80:
            score += 20
            factors.append('Strong buying intent')
        elif intent_score >= 60:
            score += 10
            factors.append('Moderate buying intent')

    # Contact quality
    if contact_data.get('directPhone'):
        score += 5
        factors.append('Direct phone available')

    if contact_data.get('email'):
        score += 5
        factors.append('Email available')

    return {
        'score': min(score, 100),
        'grade': 'A' if score >= 80 else 'B' if score >= 60 else 'C' if score >= 40 else 'D',
        'factors': factors
    }

# Build prioritized prospect list
def build_target_account_list(search_criteria, min_score=70):
    """Build and score target account list."""
    # Search for contacts
    contacts = search_contacts(**search_criteria)

    # Score each contact
    scored_contacts = []

    for contact in contacts:
        scoring = calculate_zoominfo_lead_score(contact)

        if scoring['score'] >= min_score:
            scored_contacts.append({
                **contact,
                'lead_score': scoring['score'],
                'lead_grade': scoring['grade'],
                'scoring_factors': ', '.join(scoring['factors'])
            })

    # Sort by score
    scored_df = pd.DataFrame(scored_contacts)

    if not scored_df.empty:
        scored_df = scored_df.sort_values('lead_score', ascending=False)

    return scored_df

# ABM account selection
def select_abm_accounts(industry, min_revenue, min_employees, technologies):
    """Select high-value accounts for ABM campaigns."""
    companies = search_companies(
        revenue_range={'min': min_revenue},
        employee_range={'min': min_employees},
        industry=industry,
        technologies=technologies
    )

    abm_accounts = []

    for company in companies:
        # Get key contacts at each account
        contacts = search_contacts(
            job_titles=['CEO', 'CMO', 'VP of Marketing', 'VP of Sales'],
            company_size={'min': min_employees}
        )

        company_contacts = [c for c in contacts if c.get('companyId') == company.get('id')]

        if company_contacts:
            abm_accounts.append({
                'company_id': company.get('id'),
                'company_name': company.get('companyName'),
                'revenue': company.get('revenue'),
                'employees': company.get('employeeCount'),
                'industry': company.get('industry'),
                'technologies': company.get('technologies', []),
                'key_contacts': len(company_contacts),
                'contacts': company_contacts
            })

    return pd.DataFrame(abm_accounts)
```

## Installation

```bash
# Install requests library
uv pip install requests pandas python-dateutil
```

## Authentication

```python
import requests

# ZoomInfo uses OAuth 2.0 authentication
BASE_URL = 'https://api.zoominfo.com'

# Get access token
def get_token(username, password):
    url = f'{BASE_URL}/authenticate'

    data = {
        'username': username,
        'password': password
    }

    response = requests.post(url, json=data)
    return response.json().get('jwt')

# Use token in requests
ACCESS_TOKEN = get_token('your-username', 'your-password')

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}
```

To get credentials:
1. Contact ZoomInfo to set up API access
2. Receive API username and password
3. Use credentials to get JWT token
4. Token expires after 60 minutes - refresh as needed

## Quick Start

```python
import requests

# Configuration
BASE_URL = 'https://api.zoominfo.com'
USERNAME = 'your-username'
PASSWORD = 'your-password'

# Authenticate
auth_response = requests.post(
    f'{BASE_URL}/authenticate',
    json={'username': USERNAME, 'password': PASSWORD}
)

access_token = auth_response.json().get('jwt')

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Search for contacts
search_data = {
    'jobTitleSearchRequests': [
        {'jobTitles': ['VP of Marketing', 'CMO']}
    ],
    'companySearchRequests': [
        {
            'employeeRange': {'min': 100, 'max': 1000},
            'companyIndustries': ['Computer Software']
        }
    ],
    'outputFields': ['firstName', 'lastName', 'email', 'jobTitle', 'companyName'],
    'page': 1,
    'rpp': 25
}

response = requests.post(
    f'{BASE_URL}/search/contact',
    headers=headers,
    json=search_data
)

contacts = response.json().get('data', [])
print(f"Found {len(contacts)} contacts")

for contact in contacts[:5]:
    print(f"{contact.get('firstName')} {contact.get('lastName')} - {contact.get('jobTitle')} at {contact.get('companyName')}")
```

## Key Features Reference

- **Contact Database**: 200M+ B2B contacts with direct dials
- **Company Database**: 100M+ companies worldwide
- **Technographics**: 35,000+ technologies tracked
- **Intent Data**: Real-time buying signal detection
- **Organizational Charts**: Company hierarchy mapping
- **Scoops**: News and trigger events
- **Data Enrichment**: Real-time contact/company enrichment
- **CRM Integration**: Salesforce, Microsoft Dynamics sync
- **Chrome Extension**: Prospecting while browsing
- **ReachOut**: Email campaign tool

## References

- [ZoomInfo API Documentation](https://api-docs.zoominfo.com/)
- [Authentication](https://api-docs.zoominfo.com/#authentication)
- [Contact Search API](https://api-docs.zoominfo.com/#contact-search)
- [Company Search API](https://api-docs.zoominfo.com/#company-search)
- [Enrichment API](https://api-docs.zoominfo.com/#enrichment)
- [Intent API](https://api-docs.zoominfo.com/#intent)
- [Rate Limits](https://api-docs.zoominfo.com/#rate-limits)

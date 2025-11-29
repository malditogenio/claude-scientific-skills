---
name: clearbit
description: "Clearbit data enrichment platform. Company/person enrichment, lead scoring, website visitor identification (Reveal), form shortening, prospect intelligence."
---

# Clearbit Integration

## Overview

Clearbit is a data enrichment and intelligence platform that provides real-time company and contact data. This skill covers using the Clearbit API for data enrichment, lead scoring, website visitor identification, and prospect intelligence to enhance marketing and sales workflows.

## When to Use This Skill

- Lead and account data enrichment
- Form field reduction and smart forms
- Website visitor identification and tracking
- Lead scoring based on firmographic data
- Account-based marketing (ABM) targeting
- CRM data cleanup and standardization
- Real-time prospect intelligence
- Marketing attribution and segmentation
- Sales intelligence and prospecting

## Core Capabilities

### 1. Company and Person Enrichment

```python
import requests
import json
from datetime import datetime
import pandas as pd

# Clearbit API configuration
API_KEY = 'your-clearbit-api-key'
BASE_URL = 'https://person.clearbit.com/v2'
COMPANY_URL = 'https://company.clearbit.com/v2'

def api_request(url, params=None):
    """Make Clearbit API request."""
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 202:
        # Clearbit is processing the request
        return {'status': 'processing'}
    elif response.status_code == 404:
        return {'error': 'not_found'}
    else:
        return {'error': response.status_code}

# Enrich person by email
def enrich_person(email):
    """Enrich person data using email address."""
    url = f'{BASE_URL}/people/find'
    params = {'email': email}

    result = api_request(url, params)

    if result.get('error'):
        return None

    # Extract relevant data
    enriched = {
        'email': email,
        'name': result.get('name', {}).get('fullName'),
        'first_name': result.get('name', {}).get('givenName'),
        'last_name': result.get('name', {}).get('familyName'),
        'title': result.get('employment', {}).get('title'),
        'seniority': result.get('employment', {}).get('seniority'),
        'role': result.get('employment', {}).get('role'),
        'company': result.get('employment', {}).get('name'),
        'company_domain': result.get('employment', {}).get('domain'),
        'location': result.get('location'),
        'timezone': result.get('timeZone'),
        'bio': result.get('bio'),
        'linkedin': result.get('linkedin', {}).get('handle'),
        'twitter': result.get('twitter', {}).get('handle'),
        'github': result.get('github', {}).get('handle')
    }

    return enriched

# Enrich company by domain
def enrich_company(domain):
    """Enrich company data using domain."""
    url = f'{COMPANY_URL}/companies/find'
    params = {'domain': domain}

    result = api_request(url, params)

    if result.get('error'):
        return None

    # Extract relevant data
    enriched = {
        'domain': domain,
        'name': result.get('name'),
        'legal_name': result.get('legalName'),
        'description': result.get('description'),
        'url': result.get('url'),
        'industry': result.get('category', {}).get('industry'),
        'sector': result.get('category', {}).get('sector'),
        'tags': result.get('tags', []),
        'employees': result.get('metrics', {}).get('employees'),
        'employees_range': result.get('metrics', {}).get('employeesRange'),
        'estimated_revenue': result.get('metrics', {}).get('estimatedAnnualRevenue'),
        'raised': result.get('metrics', {}).get('raised'),
        'founded_year': result.get('foundedYear'),
        'location': result.get('location'),
        'phone': result.get('phone'),
        'technologies': result.get('tech', []),
        'linkedin': result.get('linkedin', {}).get('handle'),
        'twitter': result.get('twitter', {}).get('handle'),
        'facebook': result.get('facebook', {}).get('handle')
    }

    return enriched

# Combined enrichment
def enrich_lead(email):
    """Enrich both person and company data."""
    person = enrich_person(email)

    if not person:
        return None

    # Get company data if domain available
    company_data = None
    if person.get('company_domain'):
        company_data = enrich_company(person['company_domain'])

    enriched_lead = {
        'person': person,
        'company': company_data,
        'enrichment_date': datetime.now().isoformat()
    }

    return enriched_lead

# Bulk enrichment
def bulk_enrich_leads(email_list):
    """Enrich multiple leads."""
    enriched_leads = []

    for email in email_list:
        try:
            enriched = enrich_lead(email)

            if enriched:
                enriched_leads.append(enriched)
            else:
                enriched_leads.append({
                    'person': {'email': email},
                    'company': None,
                    'error': 'not_found'
                })

        except Exception as e:
            print(f"Error enriching {email}: {e}")
            enriched_leads.append({
                'person': {'email': email},
                'company': None,
                'error': str(e)
            })

    return enriched_leads

# Example: Enrich marketing leads
campaign_emails = [
    'john@acme.com',
    'sarah@techstartup.io',
    'mike@enterprise.com'
]

enriched = bulk_enrich_leads(campaign_emails)

for lead in enriched:
    person = lead.get('person', {})
    company = lead.get('company', {})

    print(f"{person.get('name')} - {person.get('title')} at {company.get('name') if company else 'Unknown'}")
    print(f"  Company size: {company.get('employees_range') if company else 'Unknown'}")
    print(f"  Industry: {company.get('industry') if company else 'Unknown'}")
    print("---")
```

### 2. Lead Scoring and Segmentation

```python
# Calculate lead score based on Clearbit data
def calculate_enriched_lead_score(enriched_lead):
    """Score lead based on firmographic and demographic data."""
    score = 0
    factors = []

    person = enriched_lead.get('person', {})
    company = enriched_lead.get('company', {})

    # Seniority scoring
    seniority = person.get('seniority', '').lower()
    if 'executive' in seniority or 'c-level' in seniority:
        score += 30
        factors.append('Executive level')
    elif 'vp' in seniority or 'director' in seniority:
        score += 20
        factors.append('Senior management')
    elif 'manager' in seniority:
        score += 10
        factors.append('Manager level')

    # Role scoring
    role = person.get('role', '').lower()
    if 'engineering' in role or 'technical' in role:
        score += 15
        factors.append('Technical role')
    elif 'product' in role:
        score += 15
        factors.append('Product role')
    elif 'sales' in role or 'marketing' in role:
        score += 20
        factors.append('GTM role')

    # Company size scoring (ICP fit)
    if company:
        employees = company.get('employees', 0)

        if 100 <= employees <= 1000:
            score += 25
            factors.append('Ideal company size')
        elif employees > 1000:
            score += 20
            factors.append('Enterprise')
        elif 50 <= employees < 100:
            score += 15
            factors.append('Mid-market')

        # Industry scoring
        target_industries = ['Software', 'Technology', 'SaaS', 'Cloud Computing']
        industry = company.get('industry', '')

        if any(target in industry for target in target_industries):
            score += 20
            factors.append('Target industry')

        # Technology stack scoring
        target_tech = ['Salesforce', 'HubSpot', 'Google Analytics', 'Segment']
        technologies = company.get('technologies', [])

        matching_tech = [tech for tech in technologies if tech in target_tech]
        if matching_tech:
            score += 15
            factors.append(f'Uses {len(matching_tech)} relevant technologies')

        # Funding/revenue signals
        if company.get('raised') and company['raised'] > 10000000:  # $10M+
            score += 15
            factors.append('Well-funded')

    # Email domain scoring
    email = person.get('email', '')
    if email and not any(domain in email for domain in ['gmail.com', 'yahoo.com', 'hotmail.com']):
        score += 10
        factors.append('Business email')

    return {
        'score': min(score, 100),
        'grade': 'A' if score >= 80 else 'B' if score >= 60 else 'C' if score >= 40 else 'D',
        'factors': factors
    }

# Segment leads based on enriched data
def segment_leads(enriched_leads):
    """Segment leads into categories based on Clearbit data."""
    segments = {
        'enterprise': [],
        'mid_market': [],
        'smb': [],
        'high_priority': [],
        'nurture': []
    }

    for lead in enriched_leads:
        company = lead.get('company', {})
        person = lead.get('person', {})

        if not company:
            segments['nurture'].append(lead)
            continue

        employees = company.get('employees', 0)

        # Size-based segmentation
        if employees > 1000:
            segments['enterprise'].append(lead)
        elif 100 <= employees <= 1000:
            segments['mid_market'].append(lead)
        else:
            segments['smb'].append(lead)

        # Priority segmentation
        scoring = calculate_enriched_lead_score(lead)
        if scoring['score'] >= 70:
            segments['high_priority'].append(lead)

    return segments

# Example usage
enriched_leads = bulk_enrich_leads(campaign_emails)
segments = segment_leads(enriched_leads)

print(f"Enterprise: {len(segments['enterprise'])}")
print(f"Mid-Market: {len(segments['mid_market'])}")
print(f"SMB: {len(segments['smb'])}")
print(f"High Priority: {len(segments['high_priority'])}")
```

### 3. Website Visitor Intelligence (Reveal)

```python
# Note: Clearbit Reveal requires JavaScript integration on your website
# This example shows how to process Reveal data

def process_reveal_visitor(ip_address):
    """Identify company from IP address using Clearbit Reveal."""
    url = f'{COMPANY_URL}/companies/find'
    params = {'ip': ip_address}

    result = api_request(url, params)

    if result.get('error'):
        return None

    visitor_company = {
        'ip_address': ip_address,
        'company_name': result.get('name'),
        'domain': result.get('domain'),
        'industry': result.get('category', {}).get('industry'),
        'employees': result.get('metrics', {}).get('employees'),
        'location': result.get('location'),
        'technologies': result.get('tech', []),
        'identified_at': datetime.now().isoformat()
    }

    return visitor_company

# Analyze website visitor companies
def analyze_visitor_companies(visitor_ips):
    """Analyze companies visiting your website."""
    identified_companies = []

    for ip in visitor_ips:
        company = process_reveal_visitor(ip)

        if company:
            identified_companies.append(company)

    # Convert to DataFrame for analysis
    if identified_companies:
        df = pd.DataFrame(identified_companies)

        # Analyze by industry
        industry_breakdown = df.groupby('industry').size().to_dict()

        # Analyze by company size
        size_breakdown = df.groupby('employees').size().to_dict()

        return {
            'total_companies': len(identified_companies),
            'companies': identified_companies,
            'by_industry': industry_breakdown,
            'by_size': size_breakdown
        }

    return {'total_companies': 0}

# Score and prioritize anonymous visitors
def prioritize_anonymous_visitors(visitor_companies):
    """Score anonymous visitors for sales outreach."""
    scored_visitors = []

    for company in visitor_companies:
        score = 0
        factors = []

        # Company size scoring
        employees = company.get('employees', 0)
        if employees > 1000:
            score += 30
            factors.append('Enterprise')
        elif 100 <= employees <= 1000:
            score += 25
            factors.append('Mid-market')

        # Industry fit
        target_industries = ['Software', 'Technology']
        if any(ind in company.get('industry', '') for ind in target_industries):
            score += 20
            factors.append('Target industry')

        # Technology signals
        target_tech = ['Salesforce', 'HubSpot']
        if any(tech in company.get('technologies', []) for tech in target_tech):
            score += 15
            factors.append('Uses relevant tech')

        scored_visitors.append({
            **company,
            'priority_score': score,
            'scoring_factors': factors
        })

    # Sort by priority score
    return sorted(scored_visitors, key=lambda x: x['priority_score'], reverse=True)
```

### 4. Form Enrichment and Smart Forms

```python
# Simulate form enrichment (typically done client-side)
def enrich_form_submission(email):
    """Enrich form submission with Clearbit data."""
    enriched = enrich_lead(email)

    if not enriched:
        return {'email': email, 'enriched': False}

    person = enriched.get('person', {})
    company = enriched.get('company', {})

    # Return pre-filled form data
    form_data = {
        'email': email,
        'first_name': person.get('first_name', ''),
        'last_name': person.get('last_name', ''),
        'title': person.get('title', ''),
        'company': company.get('name', '') if company else '',
        'company_size': company.get('employees_range', '') if company else '',
        'industry': company.get('industry', '') if company else '',
        'phone': company.get('phone', '') if company else '',
        'enriched': True
    }

    return form_data

# CRM enrichment workflow
def enrich_crm_contacts(crm_contacts_df):
    """Enrich existing CRM contacts with Clearbit data."""
    enriched_contacts = []

    for _, contact in crm_contacts_df.iterrows():
        email = contact.get('email')

        if not email:
            continue

        enriched = enrich_lead(email)

        if enriched:
            person = enriched.get('person', {})
            company = enriched.get('company', {})

            enriched_contact = {
                'crm_id': contact.get('id'),
                'email': email,
                'enriched_title': person.get('title'),
                'enriched_seniority': person.get('seniority'),
                'enriched_company': company.get('name') if company else None,
                'company_size': company.get('employees') if company else None,
                'company_industry': company.get('industry') if company else None,
                'company_technologies': ','.join(company.get('technologies', [])) if company else None,
                'linkedin_url': person.get('linkedin'),
                'data_quality_improved': True
            }

            enriched_contacts.append(enriched_contact)

    return pd.DataFrame(enriched_contacts)
```

## Installation

```bash
# Install requests library
uv pip install requests pandas
```

## Authentication

```python
import requests

# Clearbit uses API key authentication
API_KEY = 'your-clearbit-api-key'

headers = {
    'Authorization': f'Bearer {API_KEY}'
}

# Make request
response = requests.get(
    'https://person.clearbit.com/v2/people/find',
    headers=headers,
    params={'email': 'test@example.com'}
)
```

To get API key:
1. Log into Clearbit
2. Go to Settings > API Keys
3. Copy your Secret API Key
4. Use the key in Authorization header

## Quick Start

```python
import requests

# Configuration
API_KEY = 'your-api-key'
PERSON_URL = 'https://person.clearbit.com/v2'
COMPANY_URL = 'https://company.clearbit.com/v2'

headers = {
    'Authorization': f'Bearer {API_KEY}'
}

# Enrich a person
person_response = requests.get(
    f'{PERSON_URL}/people/find',
    headers=headers,
    params={'email': 'john@acme.com'}
)

if person_response.status_code == 200:
    person = person_response.json()
    print(f"Name: {person.get('name', {}).get('fullName')}")
    print(f"Title: {person.get('employment', {}).get('title')}")
    print(f"Company: {person.get('employment', {}).get('name')}")

# Enrich a company
company_response = requests.get(
    f'{COMPANY_URL}/companies/find',
    headers=headers,
    params={'domain': 'acme.com'}
)

if company_response.status_code == 200:
    company = company_response.json()
    print(f"Company: {company.get('name')}")
    print(f"Employees: {company.get('metrics', {}).get('employees')}")
    print(f"Industry: {company.get('category', {}).get('industry')}")
```

## Key Features Reference

- **Enrichment API**: Person and company data enrichment
- **Reveal**: Website visitor identification by IP
- **Prospector**: Find contacts at target companies
- **Logo API**: Company logo retrieval
- **Risk API**: Email validation and risk scoring
- **Autocomplete**: Company name autocomplete
- **Webhooks**: Real-time enrichment notifications
- **Chrome Extension**: Enrich while browsing
- **Integrations**: Salesforce, HubSpot, Marketo, Segment

## References

- [Clearbit API Documentation](https://clearbit.com/docs)
- [Enrichment API](https://clearbit.com/docs#enrichment-api)
- [Reveal API](https://clearbit.com/docs#reveal-api)
- [Prospector API](https://clearbit.com/docs#prospector-api)
- [Risk API](https://clearbit.com/docs#risk-api)
- [Rate Limits](https://clearbit.com/docs#rate-limiting)
- [Webhooks](https://clearbit.com/docs#webhooks)

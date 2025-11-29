---
name: requests-apis
description: "API integrations for marketing platforms. Connect to Google Analytics, Meta Ads, HubSpot, Stripe, Shopify. Data extraction, automation, webhook handling, rate limiting."
---

# Requests for Marketing API Integrations

## Overview

Requests is the standard HTTP library for Python, essential for integrating with marketing APIs. This skill covers connecting to major marketing platforms (Google Analytics, Meta Ads, HubSpot, Stripe, Shopify), handling authentication, managing rate limits, processing webhooks, and automating data extraction.

## When to Use This Skill

- Extracting data from marketing platforms programmatically
- Automating report generation across multiple tools
- Building custom dashboards with data from various APIs
- Setting up webhook handlers for real-time events
- Creating custom integrations between marketing tools
- Bulk operations on marketing platforms
- Monitoring API health and performance

## Core Capabilities

### 1. Google Analytics 4 API Integration

```python
import requests
import pandas as pd
from datetime import datetime, timedelta

class GoogleAnalytics4API:
    def __init__(self, property_id, access_token):
        self.property_id = property_id
        self.access_token = access_token
        self.base_url = "https://analyticsdata.googleapis.com/v1beta"

    def get_report(self, start_date, end_date, metrics, dimensions):
        """
        Fetch GA4 report data
        """
        url = f"{self.base_url}/properties/{self.property_id}:runReport"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "dateRanges": [{"startDate": start_date, "endDate": end_date}],
            "metrics": [{"name": m} for m in metrics],
            "dimensions": [{"name": d} for d in dimensions]
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        return self._parse_response(response.json())

    def _parse_response(self, data):
        """
        Parse GA4 API response into DataFrame
        """
        rows = []
        for row in data.get('rows', []):
            parsed_row = {}
            for i, dim in enumerate(data['dimensionHeaders']):
                parsed_row[dim['name']] = row['dimensionValues'][i]['value']
            for i, metric in enumerate(data['metricHeaders']):
                parsed_row[metric['name']] = float(row['metricValues'][i]['value'])
            rows.append(parsed_row)

        return pd.DataFrame(rows)

# Usage
ga = GoogleAnalytics4API(
    property_id="123456789",
    access_token="your_access_token"
)

# Get last 30 days of traffic by source
df = ga.get_report(
    start_date="30daysAgo",
    end_date="today",
    metrics=["sessions", "totalUsers", "conversions"],
    dimensions=["sessionSource", "sessionMedium"]
)

print(df.head())
```

### 2. Meta Ads API Integration

```python
import requests
import pandas as pd
from datetime import datetime

class MetaAdsAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com/v18.0"

    def get_campaign_insights(self, account_id, date_start, date_end):
        """
        Fetch campaign performance data from Meta Ads
        """
        url = f"{self.base_url}/act_{account_id}/insights"

        params = {
            'access_token': self.access_token,
            'time_range': {
                'since': date_start,
                'until': date_end
            },
            'level': 'campaign',
            'fields': ','.join([
                'campaign_name',
                'impressions',
                'clicks',
                'spend',
                'conversions',
                'cpc',
                'cpm',
                'ctr',
                'frequency'
            ]),
            'limit': 500
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        return pd.DataFrame(data.get('data', []))

    def get_ad_creative(self, ad_id):
        """
        Fetch ad creative details
        """
        url = f"{self.base_url}/{ad_id}"

        params = {
            'access_token': self.access_token,
            'fields': 'name,creative{title,body,image_url,video_id}'
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()

# Usage
meta = MetaAdsAPI(access_token="your_access_token")

# Get campaign data
campaigns = meta.get_campaign_insights(
    account_id="123456789",
    date_start="2024-01-01",
    date_end="2024-01-31"
)

print(f"Total spend: ${campaigns['spend'].sum():,.2f}")
print(f"Total conversions: {campaigns['conversions'].sum():,.0f}")
```

### 3. HubSpot CRM API Integration

```python
import requests
import pandas as pd
from datetime import datetime

class HubSpotAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.hubapi.com"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def get_contacts(self, limit=100, properties=None):
        """
        Fetch contacts from HubSpot
        """
        url = f"{self.base_url}/crm/v3/objects/contacts"

        params = {"limit": limit}
        if properties:
            params["properties"] = ",".join(properties)

        all_contacts = []
        after = None

        while True:
            if after:
                params["after"] = after

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            data = response.json()
            all_contacts.extend(data.get('results', []))

            # Handle pagination
            paging = data.get('paging', {})
            after = paging.get('next', {}).get('after')

            if not after:
                break

        return pd.DataFrame([c['properties'] for c in all_contacts])

    def create_contact(self, email, firstname, lastname, **custom_properties):
        """
        Create a new contact in HubSpot
        """
        url = f"{self.base_url}/crm/v3/objects/contacts"

        properties = {
            "email": email,
            "firstname": firstname,
            "lastname": lastname,
            **custom_properties
        }

        payload = {"properties": properties}

        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()

        return response.json()

    def get_deals(self, limit=100):
        """
        Fetch deals from HubSpot
        """
        url = f"{self.base_url}/crm/v3/objects/deals"

        params = {
            "limit": limit,
            "properties": "dealname,amount,closedate,dealstage,pipeline"
        }

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        data = response.json()
        return pd.DataFrame([d['properties'] for d in data.get('results', [])])

# Usage
hubspot = HubSpotAPI(api_key="your_api_key")

# Get all contacts
contacts = hubspot.get_contacts(
    properties=["email", "firstname", "lastname", "lifecyclestage"]
)
print(f"Total contacts: {len(contacts)}")

# Create new contact
new_contact = hubspot.create_contact(
    email="john@example.com",
    firstname="John",
    lastname="Doe",
    lifecyclestage="lead"
)
```

### 4. Stripe API Integration

```python
import requests
import pandas as pd

class StripeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.stripe.com/v1"
        self.auth = (api_key, '')

    def get_customers(self, limit=100):
        """
        Fetch customers from Stripe
        """
        url = f"{self.base_url}/customers"

        params = {"limit": limit}

        response = requests.get(url, auth=self.auth, params=params)
        response.raise_for_status()

        data = response.json()
        return pd.DataFrame(data['data'])

    def get_charges(self, start_date=None, end_date=None, limit=100):
        """
        Fetch charges/transactions
        """
        url = f"{self.base_url}/charges"

        params = {"limit": limit}
        if start_date:
            params['created[gte]'] = int(start_date.timestamp())
        if end_date:
            params['created[lte]'] = int(end_date.timestamp())

        all_charges = []
        starting_after = None

        while True:
            if starting_after:
                params['starting_after'] = starting_after

            response = requests.get(url, auth=self.auth, params=params)
            response.raise_for_status()

            data = response.json()
            charges = data['data']

            if not charges:
                break

            all_charges.extend(charges)
            starting_after = charges[-1]['id']

            if not data['has_more']:
                break

        return pd.DataFrame(all_charges)

    def calculate_mrr(self):
        """
        Calculate Monthly Recurring Revenue from subscriptions
        """
        url = f"{self.base_url}/subscriptions"

        params = {"status": "active", "limit": 100}

        response = requests.get(url, auth=self.auth, params=params)
        response.raise_for_status()

        data = response.json()
        subscriptions = data['data']

        total_mrr = sum(
            sub['items']['data'][0]['price']['unit_amount'] / 100
            for sub in subscriptions
            if sub['items']['data']
        )

        return {
            'total_mrr': total_mrr,
            'active_subscriptions': len(subscriptions)
        }

# Usage
stripe = StripeAPI(api_key="sk_test_...")

# Get MRR
mrr_data = stripe.calculate_mrr()
print(f"Monthly Recurring Revenue: ${mrr_data['total_mrr']:,.2f}")
print(f"Active Subscriptions: {mrr_data['active_subscriptions']}")
```

### 5. Rate Limiting and Retry Logic

```python
import requests
import time
from functools import wraps

class RateLimiter:
    """
    Handle API rate limiting with exponential backoff
    """
    def __init__(self, max_retries=5, base_delay=1):
        self.max_retries = max_retries
        self.base_delay = base_delay

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(self.max_retries):
                try:
                    response = func(*args, **kwargs)

                    # Check for rate limiting
                    if response.status_code == 429:
                        retry_after = int(response.headers.get('Retry-After', self.base_delay * (2 ** attempt)))
                        print(f"Rate limited. Retrying after {retry_after}s...")
                        time.sleep(retry_after)
                        continue

                    response.raise_for_status()
                    return response

                except requests.exceptions.RequestException as e:
                    if attempt == self.max_retries - 1:
                        raise
                    delay = self.base_delay * (2 ** attempt)
                    print(f"Request failed. Retrying in {delay}s... ({e})")
                    time.sleep(delay)

            raise Exception(f"Failed after {self.max_retries} retries")

        return wrapper

# Usage
@RateLimiter(max_retries=5, base_delay=2)
def make_api_request(url, headers):
    return requests.get(url, headers=headers)

# This will automatically retry with backoff if rate limited
response = make_api_request(
    "https://api.example.com/data",
    headers={"Authorization": "Bearer token"}
)
```

### 6. Webhook Handler for Real-time Events

```python
import requests
import hmac
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

class WebhookHandler:
    """
    Handle webhooks from marketing platforms
    """
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def verify_signature(self, payload, signature, timestamp):
        """
        Verify webhook signature (Stripe-style)
        """
        signed_payload = f"{timestamp}.{payload}"

        expected_signature = hmac.new(
            self.secret_key.encode(),
            signed_payload.encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)

    def process_event(self, event_type, data):
        """
        Process different webhook events
        """
        if event_type == 'customer.created':
            return self.handle_new_customer(data)
        elif event_type == 'charge.succeeded':
            return self.handle_successful_payment(data)
        elif event_type == 'subscription.cancelled':
            return self.handle_cancellation(data)

    def handle_new_customer(self, data):
        print(f"New customer: {data['email']}")
        # Add to email list, trigger welcome sequence, etc.
        return {"status": "processed"}

    def handle_successful_payment(self, data):
        print(f"Payment received: ${data['amount']/100}")
        # Update analytics, send receipt, etc.
        return {"status": "processed"}

    def handle_cancellation(self, data):
        print(f"Subscription cancelled: {data['customer_id']}")
        # Trigger win-back campaign
        return {"status": "processed"}

# Flask endpoint
webhook_handler = WebhookHandler(secret_key="whsec_...")

@app.route('/webhooks/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.data.decode('utf-8')
    signature = request.headers.get('Stripe-Signature')

    # Verify signature
    timestamp = signature.split(',')[0].split('=')[1]
    sig_hash = signature.split(',')[1].split('=')[1]

    if not webhook_handler.verify_signature(payload, sig_hash, timestamp):
        return jsonify({"error": "Invalid signature"}), 401

    # Process event
    event = request.json
    result = webhook_handler.process_event(event['type'], event['data']['object'])

    return jsonify(result), 200

# Run webhook server
# app.run(port=5000)
```

## Installation

```bash
uv pip install requests pandas flask
```

## Quick Start

```python
import requests

# Simple API call
response = requests.get(
    'https://api.example.com/data',
    headers={'Authorization': 'Bearer YOUR_TOKEN'}
)

# Check status
response.raise_for_status()

# Parse JSON
data = response.json()
print(data)
```

## Best Practices

1. **Use sessions** - Reuse `requests.Session()` for connection pooling
2. **Handle errors** - Always use try/except and check status codes
3. **Respect rate limits** - Implement exponential backoff and retry logic
4. **Secure credentials** - Use environment variables for API keys
5. **Log requests** - Keep audit trail of API calls for debugging
6. **Validate webhooks** - Always verify webhook signatures
7. **Use pagination** - Handle paginated responses properly

## Common Marketing APIs

- **Google Analytics 4**: GA4 Data API
- **Meta Ads**: Graph API
- **Google Ads**: Google Ads API
- **HubSpot**: CRM API
- **Mailchimp**: Marketing API
- **Stripe**: Payments API
- **Shopify**: Admin API
- **Segment**: HTTP Tracking API

## References

- [Requests Documentation](https://requests.readthedocs.io/)
- [Google Analytics Data API](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [Meta Marketing API](https://developers.facebook.com/docs/marketing-apis)
- [HubSpot API](https://developers.hubspot.com/docs/api/overview)
- [Stripe API](https://stripe.com/docs/api)

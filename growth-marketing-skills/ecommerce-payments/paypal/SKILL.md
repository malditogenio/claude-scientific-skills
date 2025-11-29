---
name: paypal
description: "PayPal payment processing and checkout API. Transaction analytics, customer lifetime value, revenue tracking, subscription management, refund analysis."
---

# PayPal Integration

## Overview

PayPal is one of the world's largest payment processors with over 400 million active users. This skill covers using the PayPal REST API to analyze payment transactions, track revenue metrics, manage subscriptions, optimize checkout conversion, and calculate customer lifetime value for data-driven growth.

## When to Use This Skill

- Payment transaction analysis and reporting
- Subscription billing and recurring revenue tracking
- Customer purchase behavior analysis
- Refund and dispute management
- International payment analytics
- Checkout conversion optimization
- Revenue forecasting and reconciliation
- Multi-currency transaction analysis

## Core Capabilities

### 1. Transaction Analysis and Revenue Tracking

```python
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from datetime import datetime, timedelta
import base64

# PayPal API Configuration
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
BASE_URL = "https://api-m.paypal.com"  # Use api-m.sandbox.paypal.com for testing

# Get OAuth access token
def get_access_token():
    """Authenticate with PayPal API"""
    url = f"{BASE_URL}/v1/oauth2/token"

    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(url, auth=auth, headers=headers, data=data)
    return response.json()['access_token']

# Get transaction history
def get_transactions(start_date, end_date, access_token):
    """Fetch transaction data from PayPal"""
    url = f"{BASE_URL}/v1/reporting/transactions"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    params = {
        'start_date': start_date.isoformat() + 'Z',
        'end_date': end_date.isoformat() + 'Z',
        'fields': 'all',
        'page_size': 500
    }

    all_transactions = []
    page = 1

    while True:
        params['page'] = page
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        transactions = data.get('transaction_details', [])

        if not transactions:
            break

        all_transactions.extend(transactions)

        # Check if there are more pages
        if len(transactions) < params['page_size']:
            break

        page += 1

    return all_transactions

# Calculate revenue metrics
def calculate_revenue_metrics(days=30):
    """Comprehensive revenue analysis"""
    access_token = get_access_token()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    transactions = get_transactions(start_date, end_date, access_token)

    transaction_data = []

    for txn in transactions:
        transaction_info = txn.get('transaction_info', {})
        payer_info = txn.get('payer_info', {})

        # Only include completed transactions
        if transaction_info.get('transaction_status') == 'S':  # Success
            amount_info = transaction_info.get('transaction_amount', {})

            transaction_data.append({
                'transaction_id': transaction_info.get('transaction_id'),
                'date': pd.to_datetime(transaction_info.get('transaction_initiation_date')),
                'amount': float(amount_info.get('value', 0)),
                'currency': amount_info.get('currency_code', 'USD'),
                'fee_amount': float(transaction_info.get('fee_amount', {}).get('value', 0)),
                'transaction_status': transaction_info.get('transaction_status'),
                'transaction_type': transaction_info.get('transaction_event_code'),
                'payer_email': payer_info.get('email_address'),
                'payer_name': payer_info.get('payer_name', {}).get('alternate_full_name', ''),
                'country_code': payer_info.get('country_code')
            })

    df = pd.DataFrame(transaction_data)

    if len(df) == 0:
        return {}, df, None

    df['date_only'] = df['date'].dt.date
    df['net_amount'] = df['amount'] - abs(df['fee_amount'])

    # Calculate metrics
    metrics = {
        'total_revenue': df['amount'].sum(),
        'net_revenue': df['net_amount'].sum(),
        'total_fees': abs(df['fee_amount'].sum()),
        'total_transactions': len(df),
        'average_transaction_value': df['amount'].mean(),
        'median_transaction_value': df['amount'].median(),
        'unique_customers': df['payer_email'].nunique(),
        'revenue_per_customer': df.groupby('payer_email')['amount'].sum().mean(),
        'currency_breakdown': df.groupby('currency')['amount'].sum().to_dict(),
        'country_breakdown': df.groupby('country_code')['amount'].sum().to_dict()
    }

    # Daily trends
    daily_stats = df.groupby('date_only').agg({
        'amount': ['sum', 'mean', 'count'],
        'net_amount': 'sum',
        'payer_email': 'nunique'
    })

    return metrics, df, daily_stats

# Analyze payment types
def analyze_payment_methods(days=30):
    """Track payment method distribution"""
    access_token = get_access_token()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    transactions = get_transactions(start_date, end_date, access_token)

    payment_data = []

    for txn in transactions:
        transaction_info = txn.get('transaction_info', {})

        if transaction_info.get('transaction_status') == 'S':
            payment_data.append({
                'transaction_id': transaction_info.get('transaction_id'),
                'amount': float(transaction_info.get('transaction_amount', {}).get('value', 0)),
                'transaction_type': transaction_info.get('transaction_event_code'),
                'payment_tracking_id': transaction_info.get('payment_tracking_id')
            })

    df = pd.DataFrame(payment_data)

    if len(df) == 0:
        return None

    # Analyze by transaction type
    type_stats = df.groupby('transaction_type').agg({
        'amount': ['sum', 'mean', 'count']
    }).round(2)

    type_stats.columns = ['total_revenue', 'avg_transaction', 'transaction_count']
    type_stats['revenue_percent'] = (
        type_stats['total_revenue'] / type_stats['total_revenue'].sum() * 100
    ).round(2)

    return type_stats

# Example usage
metrics, transactions_df, daily_stats = calculate_revenue_metrics(days=30)
if metrics:
    print(f"30-Day PayPal Analytics:")
    print(f"  Total Revenue: ${metrics['total_revenue']:,.2f}")
    print(f"  Net Revenue: ${metrics['net_revenue']:,.2f}")
    print(f"  Total Fees: ${metrics['total_fees']:,.2f}")
    print(f"  Transactions: {metrics['total_transactions']}")
    print(f"  Avg Transaction: ${metrics['average_transaction_value']:,.2f}")
```

### 2. Customer Data and Lifetime Value

```python
# Analyze customer purchase patterns
def calculate_customer_ltv(days=180):
    """Calculate customer lifetime value from PayPal transactions"""
    access_token = get_access_token()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    transactions = get_transactions(start_date, end_date, access_token)

    # Group by customer email
    customer_purchases = {}

    for txn in transactions:
        transaction_info = txn.get('transaction_info', {})
        payer_info = txn.get('payer_info', {})

        if transaction_info.get('transaction_status') == 'S':
            email = payer_info.get('email_address')

            if not email:
                continue

            amount = float(transaction_info.get('transaction_amount', {}).get('value', 0))
            date = pd.to_datetime(transaction_info.get('transaction_initiation_date'))

            if email not in customer_purchases:
                customer_purchases[email] = {
                    'transactions': [],
                    'total_spent': 0,
                    'transaction_count': 0,
                    'name': payer_info.get('payer_name', {}).get('alternate_full_name', ''),
                    'country': payer_info.get('country_code', '')
                }

            customer_purchases[email]['transactions'].append({
                'date': date,
                'amount': amount
            })
            customer_purchases[email]['total_spent'] += amount
            customer_purchases[email]['transaction_count'] += 1

    # Build customer DataFrame
    customer_data = []

    for email, data in customer_purchases.items():
        if data['transaction_count'] > 0:
            transaction_dates = [t['date'] for t in data['transactions']]
            first_purchase = min(transaction_dates)
            last_purchase = max(transaction_dates)

            customer_data.append({
                'email': email,
                'name': data['name'],
                'country': data['country'],
                'total_spent': data['total_spent'],
                'transaction_count': data['transaction_count'],
                'first_purchase': first_purchase,
                'last_purchase': last_purchase
            })

    df = pd.DataFrame(customer_data)

    if len(df) == 0:
        return {}, df

    # Calculate additional metrics
    df['avg_transaction_value'] = df['total_spent'] / df['transaction_count']
    df['customer_lifetime_days'] = (df['last_purchase'] - df['first_purchase']).dt.days
    df['days_since_last_purchase'] = (datetime.now() - df['last_purchase']).dt.days

    # Segment customers
    df['segment'] = pd.qcut(
        df['total_spent'],
        q=4,
        labels=['Low Value', 'Medium Value', 'High Value', 'VIP'],
        duplicates='drop'
    )

    ltv_metrics = {
        'total_customers': len(df),
        'average_ltv': df['total_spent'].mean(),
        'median_ltv': df['total_spent'].median(),
        'top_10_percent_ltv': df.nlargest(int(len(df) * 0.1), 'total_spent')['total_spent'].mean(),
        'repeat_customer_rate': (df['transaction_count'] > 1).sum() / len(df) * 100,
        'avg_transactions_per_customer': df['transaction_count'].mean(),
        'segment_distribution': df['segment'].value_counts().to_dict()
    }

    return ltv_metrics, df

# Geographic customer analysis
def analyze_customer_geography(days=90):
    """Analyze revenue by customer location"""
    access_token = get_access_token()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    transactions = get_transactions(start_date, end_date, access_token)

    geo_data = []

    for txn in transactions:
        transaction_info = txn.get('transaction_info', {})
        payer_info = txn.get('payer_info', {})

        if transaction_info.get('transaction_status') == 'S':
            geo_data.append({
                'country': payer_info.get('country_code', 'Unknown'),
                'amount': float(transaction_info.get('transaction_amount', {}).get('value', 0)),
                'currency': transaction_info.get('transaction_amount', {}).get('currency_code', 'USD')
            })

    df = pd.DataFrame(geo_data)

    if len(df) == 0:
        return None

    # Country performance
    country_stats = df.groupby('country').agg({
        'amount': ['sum', 'mean', 'count']
    }).round(2)

    country_stats.columns = ['total_revenue', 'avg_transaction', 'transaction_count']
    country_stats['revenue_percent'] = (
        country_stats['total_revenue'] / country_stats['total_revenue'].sum() * 100
    ).round(2)

    return country_stats.sort_values('total_revenue', ascending=False)

# Example usage
ltv_metrics, customers_df = calculate_customer_ltv(days=180)
if ltv_metrics:
    print(f"Customer Metrics:")
    print(f"  Total Customers: {ltv_metrics['total_customers']}")
    print(f"  Average LTV: ${ltv_metrics['average_ltv']:,.2f}")
    print(f"  Repeat Rate: {ltv_metrics['repeat_customer_rate']:.1f}%")
```

### 3. Subscription Management and Analytics

```python
# Get subscription plans
def get_subscription_plans(access_token):
    """Fetch billing plans"""
    url = f"{BASE_URL}/v1/billing/plans"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    params = {
        'page_size': 20,
        'page': 1,
        'total_required': True
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json().get('plans', [])

# Get active subscriptions
def get_subscriptions(access_token, plan_id=None):
    """Fetch subscription data"""
    url = f"{BASE_URL}/v1/billing/subscriptions"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    params = {
        'page_size': 20
    }

    if plan_id:
        params['plan_id'] = plan_id

    all_subscriptions = []
    page = 1

    while True:
        params['page'] = page
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        subscriptions = data.get('subscriptions', [])

        if not subscriptions:
            break

        all_subscriptions.extend(subscriptions)
        page += 1

        if len(subscriptions) < params['page_size']:
            break

    return all_subscriptions

# Calculate subscription metrics
def calculate_subscription_metrics():
    """Analyze subscription revenue and churn"""
    access_token = get_access_token()

    # Get all active subscriptions
    subscriptions = get_subscriptions(access_token)

    sub_data = []

    for sub in subscriptions:
        billing_info = sub.get('billing_info', {})
        plan_info = sub.get('plan', {})

        # Calculate monthly recurring revenue
        if billing_info.get('last_payment', {}).get('amount'):
            amount = float(billing_info['last_payment']['amount'].get('value', 0))
            currency = billing_info['last_payment']['amount'].get('currency_code', 'USD')
        else:
            amount = 0
            currency = 'USD'

        sub_data.append({
            'subscription_id': sub.get('id'),
            'status': sub.get('status'),
            'plan_id': plan_info.get('product_id'),
            'amount': amount,
            'currency': currency,
            'subscriber_email': sub.get('subscriber', {}).get('email_address'),
            'created_time': pd.to_datetime(sub.get('create_time')),
            'start_time': pd.to_datetime(sub.get('start_time'))
        })

    df = pd.DataFrame(sub_data)

    if len(df) == 0:
        return {}, df

    # Filter active subscriptions
    active_subs = df[df['status'] == 'ACTIVE']

    metrics = {
        'total_subscriptions': len(df),
        'active_subscriptions': len(active_subs),
        'mrr': active_subs['amount'].sum(),
        'arr': active_subs['amount'].sum() * 12,
        'avg_subscription_value': active_subs['amount'].mean(),
        'status_breakdown': df['status'].value_counts().to_dict()
    }

    return metrics, df

# Example usage
sub_metrics, subs_df = calculate_subscription_metrics()
if sub_metrics:
    print(f"Subscription Metrics:")
    print(f"  Active Subscriptions: {sub_metrics['active_subscriptions']}")
    print(f"  MRR: ${sub_metrics['mrr']:,.2f}")
    print(f"  ARR: ${sub_metrics['arr']:,.2f}")
```

### 4. Refund and Dispute Analytics

```python
# Analyze refunds
def analyze_refunds(days=90):
    """Track refund rates and amounts"""
    access_token = get_access_token()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    transactions = get_transactions(start_date, end_date, access_token)

    refund_data = []

    for txn in transactions:
        transaction_info = txn.get('transaction_info', {})

        # Check for refunds
        if 'refund' in transaction_info.get('transaction_event_code', '').lower():
            refund_data.append({
                'transaction_id': transaction_info.get('transaction_id'),
                'date': pd.to_datetime(transaction_info.get('transaction_initiation_date')),
                'amount': abs(float(transaction_info.get('transaction_amount', {}).get('value', 0))),
                'currency': transaction_info.get('transaction_amount', {}).get('currency_code', 'USD'),
                'transaction_type': transaction_info.get('transaction_event_code')
            })

    if not refund_data:
        return None

    df = pd.DataFrame(refund_data)

    # Get total revenue for refund rate calculation
    metrics, _, _ = calculate_revenue_metrics(days=days)

    refund_metrics = {
        'total_refunds': len(df),
        'total_refund_amount': df['amount'].sum(),
        'avg_refund_amount': df['amount'].mean(),
        'refund_rate': (df['amount'].sum() / metrics.get('total_revenue', 1) * 100) if metrics else 0
    }

    return refund_metrics, df

# Analyze disputes
def get_disputes(access_token, start_date=None):
    """Fetch dispute/chargeback data"""
    url = f"{BASE_URL}/v1/customer/disputes"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    params = {
        'page_size': 50
    }

    if start_date:
        params['start_time'] = start_date.isoformat() + 'Z'

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return []

    return response.json().get('items', [])

def analyze_disputes(days=90):
    """Track dispute rates and resolution"""
    access_token = get_access_token()
    start_date = datetime.now() - timedelta(days=days)

    disputes = get_disputes(access_token, start_date)

    if not disputes:
        return None

    dispute_data = []

    for dispute in disputes:
        dispute_data.append({
            'dispute_id': dispute.get('dispute_id'),
            'reason': dispute.get('reason'),
            'status': dispute.get('status'),
            'amount': float(dispute.get('dispute_amount', {}).get('value', 0)),
            'currency': dispute.get('dispute_amount', {}).get('currency_code', 'USD'),
            'create_time': pd.to_datetime(dispute.get('create_time'))
        })

    df = pd.DataFrame(dispute_data)

    dispute_metrics = {
        'total_disputes': len(df),
        'total_disputed_amount': df['amount'].sum(),
        'dispute_reasons': df['reason'].value_counts().to_dict(),
        'dispute_status': df['status'].value_counts().to_dict()
    }

    return dispute_metrics, df

# Example usage
refund_metrics, refunds_df = analyze_refunds(days=90)
if refund_metrics:
    print(f"Refund Metrics:")
    print(f"  Total Refunds: {refund_metrics['total_refunds']}")
    print(f"  Refund Amount: ${refund_metrics['total_refund_amount']:,.2f}")
    print(f"  Refund Rate: {refund_metrics['refund_rate']:.2f}%")
```

## Installation

```bash
# Install required packages
uv pip install requests pandas python-dateutil
```

## Authentication

### REST API Credentials

1. Go to PayPal Developer Dashboard: https://developer.paypal.com/
2. Create a new app under "My Apps & Credentials"
3. Copy Client ID and Secret
4. Use Sandbox credentials for testing

```python
import requests
from requests.auth import HTTPBasicAuth

CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
BASE_URL = "https://api-m.paypal.com"  # Production
# BASE_URL = "https://api-m.sandbox.paypal.com"  # Sandbox

def get_access_token():
    """Get OAuth 2.0 access token"""
    url = f"{BASE_URL}/v1/oauth2/token"

    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'client_credentials'}

    response = requests.post(url, auth=auth, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Authentication failed: {response.text}")

# Test authentication
access_token = get_access_token()
print(f"Access token obtained: {access_token[:20]}...")
```

## Quick Start

```python
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta

# Configuration
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
BASE_URL = "https://api-m.paypal.com"

# Get access token
def get_access_token():
    url = f"{BASE_URL}/v1/oauth2/token"
    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    data = {'grant_type': 'client_credentials'}

    response = requests.post(url, auth=auth, data=data)
    return response.json()['access_token']

access_token = get_access_token()

# Get recent transactions
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

end_date = datetime.now()
start_date = end_date - timedelta(days=7)

params = {
    'start_date': start_date.isoformat() + 'Z',
    'end_date': end_date.isoformat() + 'Z',
    'fields': 'all',
    'page_size': 10
}

response = requests.get(
    f"{BASE_URL}/v1/reporting/transactions",
    headers=headers,
    params=params
)

transactions = response.json().get('transaction_details', [])
print(f"Recent transactions: {len(transactions)}")

for txn in transactions:
    info = txn.get('transaction_info', {})
    amount = info.get('transaction_amount', {})
    print(f"${amount.get('value', 0)} - {info.get('transaction_status')}")
```

## Key Metrics Reference

### Revenue Metrics
- **Gross Revenue**: Total payment volume
- **Net Revenue**: Revenue after PayPal fees
- **Fee Rate**: Fees / gross revenue (typically 2.9% + $0.30)
- **Average Transaction Value**: Total revenue / transactions

### Customer Metrics
- **Customer Lifetime Value (LTV)**: Total spend per customer
- **Repeat Purchase Rate**: Customers with 2+ transactions
- **Geographic Distribution**: Revenue by country
- **Currency Mix**: Revenue by currency

### Subscription Metrics
- **MRR (Monthly Recurring Revenue)**: Predictable monthly revenue
- **ARR (Annual Recurring Revenue)**: MRR × 12
- **Active Subscribers**: Current active subscriptions
- **Churn Rate**: Canceled / total subscriptions

### Risk Metrics
- **Refund Rate**: Refunds / total revenue
- **Dispute Rate**: Disputes / total transactions
- **Chargeback Rate**: Chargebacks / total transactions
- **Resolution Rate**: Resolved disputes / total disputes

## References

- [PayPal REST API Documentation](https://developer.paypal.com/api/rest/)
- [Transaction Search API](https://developer.paypal.com/docs/api/transaction-search/v1/)
- [Subscriptions API](https://developer.paypal.com/docs/api/subscriptions/v1/)
- [Disputes API](https://developer.paypal.com/docs/api/customer-disputes/v1/)
- [PayPal Developer Dashboard](https://developer.paypal.com/dashboard/)

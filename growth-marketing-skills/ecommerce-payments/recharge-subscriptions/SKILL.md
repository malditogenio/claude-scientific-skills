---
name: recharge-subscriptions
description: "Recharge subscription management API. Track MRR/ARR, churn analysis, customer lifetime value, retention cohorts, subscription analytics, revenue optimization."
---

# Recharge Subscriptions Integration

## Overview

Recharge is a leading subscription management platform for e-commerce, powering subscription billing for thousands of Shopify and BigCommerce stores. This skill covers using the Recharge API to analyze subscription revenue, track customer retention, reduce churn, and optimize pricing strategies for recurring revenue growth.

## When to Use This Skill

- Subscription revenue tracking (MRR, ARR)
- Customer churn analysis and prevention
- Retention cohort analysis
- Subscription lifetime value calculations
- Product subscription performance
- Dunning and payment recovery optimization
- Pricing tier analysis
- Subscription health monitoring

## Core Capabilities

### 1. Subscription Revenue and MRR/ARR Analysis

```python
import requests
import pandas as pd
from datetime import datetime, timedelta

# Recharge API Configuration
API_TOKEN = "your_api_token"
BASE_URL = "https://api.rechargeapps.com"

headers = {
    'X-Recharge-Access-Token': API_TOKEN,
    'Content-Type': 'application/json'
}

# Get subscriptions
def get_subscriptions(status='ACTIVE'):
    """Fetch subscription data"""
    url = f"{BASE_URL}/subscriptions"

    params = {
        'limit': 250,
        'status': status
    }

    all_subscriptions = []
    cursor = None

    while True:
        if cursor:
            params['cursor'] = cursor

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        subscriptions = data.get('subscriptions', [])

        if not subscriptions:
            break

        all_subscriptions.extend(subscriptions)

        # Check for next page
        cursor = data.get('next_cursor')
        if not cursor:
            break

    return all_subscriptions

# Calculate MRR and ARR
def calculate_mrr_arr():
    """Calculate Monthly and Annual Recurring Revenue"""
    subscriptions = get_subscriptions(status='ACTIVE')

    sub_data = []

    for sub in subscriptions:
        # Get subscription price and frequency
        price = float(sub.get('price', 0))
        order_interval_frequency = int(sub.get('order_interval_frequency', 1))
        order_interval_unit = sub.get('order_interval_unit', 'month')

        # Calculate monthly recurring revenue
        if order_interval_unit == 'month':
            mrr = price / order_interval_frequency
        elif order_interval_unit == 'week':
            mrr = price * (4.33 / order_interval_frequency)  # Average weeks per month
        elif order_interval_unit == 'day':
            mrr = price * (30 / order_interval_frequency)
        else:
            mrr = price  # Default to monthly

        sub_data.append({
            'subscription_id': sub['id'],
            'customer_id': sub['customer_id'],
            'status': sub['status'],
            'mrr': mrr,
            'price': price,
            'interval_frequency': order_interval_frequency,
            'interval_unit': order_interval_unit,
            'created_at': pd.to_datetime(sub['created_at']),
            'next_charge_scheduled_at': pd.to_datetime(sub.get('next_charge_scheduled_at')),
            'product_title': sub.get('product_title', 'Unknown')
        })

    df = pd.DataFrame(sub_data)

    if len(df) == 0:
        return {}, df

    metrics = {
        'total_mrr': df['mrr'].sum(),
        'arr': df['mrr'].sum() * 12,
        'total_active_subscriptions': len(df),
        'avg_mrr_per_subscription': df['mrr'].mean(),
        'median_subscription_value': df['mrr'].median(),
        'mrr_by_product': df.groupby('product_title')['mrr'].sum().to_dict(),
        'subscription_count_by_product': df['product_title'].value_counts().to_dict()
    }

    return metrics, df

# MRR movement analysis
def analyze_mrr_movements(months=3):
    """Track MRR expansion, contraction, and churn"""
    # Get active and canceled subscriptions
    active_subs = get_subscriptions(status='ACTIVE')
    canceled_subs = get_subscriptions(status='CANCELLED')

    # Recent cancellations
    cutoff_date = datetime.now() - timedelta(days=30*months)

    recent_cancellations = [
        sub for sub in canceled_subs
        if pd.to_datetime(sub.get('cancelled_at')) >= cutoff_date
    ]

    # Calculate churned MRR
    churned_mrr = 0
    for sub in recent_cancellations:
        price = float(sub.get('price', 0))
        interval = int(sub.get('order_interval_frequency', 1))
        unit = sub.get('order_interval_unit', 'month')

        if unit == 'month':
            mrr = price / interval
        else:
            mrr = price  # Simplified

        churned_mrr += mrr

    # Calculate new MRR
    new_subs = [
        sub for sub in active_subs
        if pd.to_datetime(sub.get('created_at')) >= cutoff_date
    ]

    new_mrr = 0
    for sub in new_subs:
        price = float(sub.get('price', 0))
        interval = int(sub.get('order_interval_frequency', 1))

        new_mrr += price / interval

    metrics = {
        'new_mrr': new_mrr,
        'churned_mrr': churned_mrr,
        'net_mrr_change': new_mrr - churned_mrr,
        'new_subscriptions': len(new_subs),
        'churned_subscriptions': len(recent_cancellations)
    }

    return metrics

# Revenue trends over time
def analyze_revenue_trends(months=12):
    """Track MRR trends over time"""
    # This would require historical data tracking
    # Simplified version using current subscription data

    subscriptions = get_subscriptions(status='ACTIVE')

    # Group by creation month
    sub_data = []
    for sub in subscriptions:
        created_at = pd.to_datetime(sub['created_at'])
        price = float(sub.get('price', 0))
        interval = int(sub.get('order_interval_frequency', 1))

        mrr = price / interval

        sub_data.append({
            'created_month': created_at.to_period('M'),
            'mrr': mrr
        })

    df = pd.DataFrame(sub_data)

    monthly_mrr = df.groupby('created_month')['mrr'].sum()

    return monthly_mrr

# Example usage
mrr_metrics, subs_df = calculate_mrr_arr()
print(f"Subscription Revenue Metrics:")
print(f"  MRR: ${mrr_metrics['total_mrr']:,.2f}")
print(f"  ARR: ${mrr_metrics['arr']:,.2f}")
print(f"  Active Subscriptions: {mrr_metrics['total_active_subscriptions']}")
print(f"  Avg MRR per Subscription: ${mrr_metrics['avg_mrr_per_subscription']:,.2f}")
```

### 2. Customer Churn and Retention Analysis

```python
# Get customers
def get_customers():
    """Fetch customer data"""
    url = f"{BASE_URL}/customers"

    params = {'limit': 250}

    all_customers = []
    cursor = None

    while True:
        if cursor:
            params['cursor'] = cursor

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        customers = data.get('customers', [])

        if not customers:
            break

        all_customers.extend(customers)

        cursor = data.get('next_cursor')
        if not cursor:
            break

    return all_customers

# Calculate churn rate
def calculate_churn_rate(months=6):
    """Analyze subscription churn"""
    # Get canceled subscriptions
    canceled_subs = get_subscriptions(status='CANCELLED')

    # Filter recent cancellations
    start_date = datetime.now() - timedelta(days=30*months)

    churn_data = []

    for sub in canceled_subs:
        canceled_at = sub.get('cancelled_at')

        if canceled_at:
            cancel_date = pd.to_datetime(canceled_at)

            if cancel_date >= start_date:
                created_at = pd.to_datetime(sub['created_at'])

                churn_data.append({
                    'subscription_id': sub['id'],
                    'customer_id': sub['customer_id'],
                    'created_at': created_at,
                    'canceled_at': cancel_date,
                    'lifetime_days': (cancel_date - created_at).days,
                    'cancellation_reason': sub.get('cancellation_reason'),
                    'product_title': sub.get('product_title', 'Unknown')
                })

    df = pd.DataFrame(churn_data)

    if len(df) == 0:
        return {}, df

    df['cancel_month'] = df['canceled_at'].dt.to_period('M')

    # Monthly churn counts
    monthly_churn = df.groupby('cancel_month').agg({
        'subscription_id': 'count'
    }).rename(columns={'subscription_id': 'churned_count'})

    # Get total active subs at start of period
    active_subs = get_subscriptions(status='ACTIVE')
    current_active = len(active_subs)

    # Calculate churn rate
    avg_monthly_churn = len(df) / months
    churn_rate = (avg_monthly_churn / (current_active + avg_monthly_churn)) * 100

    metrics = {
        'total_churned': len(df),
        'avg_monthly_churn': avg_monthly_churn,
        'churn_rate': churn_rate,
        'avg_lifetime_days': df['lifetime_days'].mean(),
        'cancellation_reasons': df['cancellation_reason'].value_counts().to_dict(),
        'churn_by_product': df['product_title'].value_counts().to_dict()
    }

    return metrics, df

# Cohort retention analysis
def cohort_retention_analysis(months=12):
    """Analyze retention by signup cohort"""
    # Get all subscriptions
    active_subs = get_subscriptions(status='ACTIVE')
    canceled_subs = get_subscriptions(status='CANCELLED')

    all_subs = active_subs + canceled_subs

    cohort_data = []

    for sub in all_subs:
        created_at = pd.to_datetime(sub['created_at'])
        canceled_at = pd.to_datetime(sub.get('cancelled_at')) if sub.get('cancelled_at') else None

        cohort_data.append({
            'subscription_id': sub['id'],
            'customer_id': sub['customer_id'],
            'cohort_month': created_at.to_period('M'),
            'status': sub['status'],
            'created_at': created_at,
            'canceled_at': canceled_at
        })

    df = pd.DataFrame(cohort_data)

    # Calculate retention by cohort
    cohort_counts = df.groupby('cohort_month').agg({
        'subscription_id': 'count'
    }).rename(columns={'subscription_id': 'cohort_size'})

    # Active subs by cohort
    active_by_cohort = df[df['status'] == 'ACTIVE'].groupby('cohort_month').agg({
        'subscription_id': 'count'
    }).rename(columns={'subscription_id': 'still_active'})

    cohort_counts = cohort_counts.join(active_by_cohort, how='left').fillna(0)
    cohort_counts['retention_rate'] = (
        cohort_counts['still_active'] / cohort_counts['cohort_size'] * 100
    ).round(2)

    return cohort_counts

# At-risk subscription identification
def identify_at_risk_subscriptions():
    """Find subscriptions at risk of churning"""
    active_subs = get_subscriptions(status='ACTIVE')

    at_risk = []

    for sub in active_subs:
        # Get charge history
        subscription_id = sub['id']

        # Factors indicating risk:
        # 1. Failed payment attempts
        # 2. Long time since last charge
        # 3. Approaching renewal date

        next_charge = pd.to_datetime(sub.get('next_charge_scheduled_at'))
        days_until_renewal = (next_charge - datetime.now()).days

        # Check if payment method is about to expire
        # This would require additional API calls to charges

        at_risk.append({
            'subscription_id': subscription_id,
            'customer_id': sub['customer_id'],
            'product_title': sub.get('product_title'),
            'mrr': float(sub.get('price', 0)),
            'days_until_renewal': days_until_renewal,
            'status': sub['status']
        })

    df = pd.DataFrame(at_risk)

    # Filter for at-risk criteria
    # e.g., renewal in next 7 days
    at_risk_df = df[df['days_until_renewal'] <= 7]

    return at_risk_df

# Example usage
churn_metrics, churn_df = calculate_churn_rate(months=6)
print(f"Churn Analysis:")
print(f"  Total Churned: {churn_metrics['total_churned']}")
print(f"  Monthly Churn Rate: {churn_metrics['churn_rate']:.2f}%")
print(f"  Avg Lifetime: {churn_metrics['avg_lifetime_days']:.0f} days")
```

### 3. Customer Lifetime Value and Analytics

```python
# Calculate customer LTV
def calculate_subscription_ltv():
    """Analyze customer lifetime value from subscriptions"""
    customers = get_customers()

    customer_data = []

    for customer in customers:
        customer_id = customer['id']

        # Get customer's subscriptions
        url = f"{BASE_URL}/subscriptions"
        params = {'customer_id': customer_id, 'limit': 100}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            continue

        subscriptions = response.json().get('subscriptions', [])

        total_value = 0
        active_count = 0
        total_count = len(subscriptions)

        for sub in subscriptions:
            price = float(sub.get('price', 0))
            total_value += price

            if sub['status'] == 'ACTIVE':
                active_count += 1

        if total_count > 0:
            customer_data.append({
                'customer_id': customer_id,
                'email': customer.get('email'),
                'first_name': customer.get('first_name', ''),
                'last_name': customer.get('last_name', ''),
                'created_at': pd.to_datetime(customer['created_at']),
                'total_subscriptions': total_count,
                'active_subscriptions': active_count,
                'total_value': total_value
            })

    df = pd.DataFrame(customer_data)

    if len(df) == 0:
        return {}, df

    # Calculate metrics
    df['avg_subscription_value'] = df['total_value'] / df['total_subscriptions']
    df['customer_lifetime_days'] = (datetime.now() - df['created_at']).dt.days

    # Segment customers
    df['segment'] = pd.qcut(
        df['total_value'],
        q=4,
        labels=['Low Value', 'Medium Value', 'High Value', 'VIP'],
        duplicates='drop'
    )

    ltv_metrics = {
        'total_customers': len(df),
        'average_ltv': df['total_value'].mean(),
        'median_ltv': df['total_value'].median(),
        'top_10_percent_ltv': df.nlargest(int(len(df) * 0.1), 'total_value')['total_value'].mean(),
        'avg_subscriptions_per_customer': df['total_subscriptions'].mean(),
        'active_subscription_rate': df['active_subscriptions'].sum() / df['total_subscriptions'].sum() * 100,
        'segment_distribution': df['segment'].value_counts().to_dict()
    }

    return ltv_metrics, df

# Example usage
ltv_metrics, customers_df = calculate_subscription_ltv()
print(f"Customer LTV Metrics:")
print(f"  Total Customers: {ltv_metrics['total_customers']}")
print(f"  Average LTV: ${ltv_metrics['average_ltv']:,.2f}")
print(f"  Active Sub Rate: {ltv_metrics['active_subscription_rate']:.1f}%")
```

### 4. Product and Pricing Analytics

```python
# Product subscription performance
def analyze_product_performance():
    """Analyze subscription performance by product"""
    subscriptions = get_subscriptions(status='ACTIVE')

    product_data = []

    for sub in subscriptions:
        price = float(sub.get('price', 0))
        interval = int(sub.get('order_interval_frequency', 1))
        mrr = price / interval

        product_data.append({
            'product_title': sub.get('product_title', 'Unknown'),
            'variant_title': sub.get('variant_title', ''),
            'mrr': mrr,
            'price': price,
            'interval_frequency': interval,
            'interval_unit': sub.get('order_interval_unit')
        })

    df = pd.DataFrame(product_data)

    if len(df) == 0:
        return None

    # Product performance
    product_stats = df.groupby('product_title').agg({
        'mrr': ['sum', 'mean', 'count']
    }).round(2)

    product_stats.columns = ['total_mrr', 'avg_mrr', 'subscription_count']
    product_stats['mrr_percent'] = (
        product_stats['total_mrr'] / product_stats['total_mrr'].sum() * 100
    ).round(2)

    return product_stats.sort_values('total_mrr', ascending=False)

# Frequency interval analysis
def analyze_billing_frequencies():
    """Analyze subscription billing intervals"""
    subscriptions = get_subscriptions(status='ACTIVE')

    frequency_data = []

    for sub in subscriptions:
        frequency = int(sub.get('order_interval_frequency', 1))
        unit = sub.get('order_interval_unit', 'month')
        price = float(sub.get('price', 0))

        frequency_data.append({
            'interval': f"{frequency} {unit}",
            'mrr': price / frequency if unit == 'month' else price,
            'price': price
        })

    df = pd.DataFrame(frequency_data)

    if len(df) == 0:
        return None

    frequency_stats = df.groupby('interval').agg({
        'mrr': ['sum', 'count'],
        'price': 'mean'
    }).round(2)

    frequency_stats.columns = ['total_mrr', 'subscription_count', 'avg_price']

    return frequency_stats.sort_values('total_mrr', ascending=False)

# Prepaid vs recurring analysis
def analyze_payment_types():
    """Compare prepaid and recurring subscription models"""
    subscriptions = get_subscriptions(status='ACTIVE')

    # Categorize by billing frequency
    payment_data = []

    for sub in subscriptions:
        interval = int(sub.get('order_interval_frequency', 1))
        unit = sub.get('order_interval_unit', 'month')

        # Longer intervals might indicate prepaid
        if unit == 'month' and interval >= 6:
            payment_type = 'Prepaid/Long-term'
        else:
            payment_type = 'Recurring/Short-term'

        price = float(sub.get('price', 0))

        payment_data.append({
            'payment_type': payment_type,
            'price': price,
            'interval': f"{interval} {unit}"
        })

    df = pd.DataFrame(payment_data)

    if len(df) == 0:
        return None

    type_stats = df.groupby('payment_type').agg({
        'price': ['sum', 'mean', 'count']
    }).round(2)

    type_stats.columns = ['total_revenue', 'avg_price', 'subscription_count']

    return type_stats

# Example usage
product_performance = analyze_product_performance()
if product_performance is not None:
    print("Product Performance:")
    print(product_performance.head(10))

frequency_analysis = analyze_billing_frequencies()
if frequency_analysis is not None:
    print("\nBilling Frequency Analysis:")
    print(frequency_analysis)
```

## Installation

```bash
# Install required packages
uv pip install requests pandas python-dateutil
```

## Authentication

### API Token

1. Log in to Recharge merchant portal
2. Go to Apps > API Tokens
3. Create a new API token with appropriate scopes
4. Copy the token (starts with `sk_`)

```python
import requests

API_TOKEN = "your_api_token"
BASE_URL = "https://api.rechargeapps.com"

headers = {
    'X-Recharge-Access-Token': API_TOKEN,
    'Content-Type': 'application/json'
}

# Test connection
response = requests.get(f"{BASE_URL}/subscriptions", headers=headers, params={'limit': 1})

if response.status_code == 200:
    print("Connected to Recharge API successfully!")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

## Quick Start

```python
import requests
import pandas as pd

# Configuration
API_TOKEN = "your_api_token"
BASE_URL = "https://api.rechargeapps.com"

headers = {
    'X-Recharge-Access-Token': API_TOKEN,
    'Content-Type': 'application/json'
}

# Get active subscriptions
response = requests.get(
    f"{BASE_URL}/subscriptions",
    headers=headers,
    params={'status': 'ACTIVE', 'limit': 10}
)

subscriptions = response.json().get('subscriptions', [])

print(f"Active Subscriptions: {len(subscriptions)}")

total_mrr = 0
for sub in subscriptions:
    price = float(sub.get('price', 0))
    interval = int(sub.get('order_interval_frequency', 1))
    mrr = price / interval

    total_mrr += mrr
    print(f"{sub.get('product_title')}: ${price:.2f} every {interval} months")

print(f"\nTotal MRR: ${total_mrr:,.2f}")
```

## Key Metrics Reference

### Revenue Metrics
- **MRR (Monthly Recurring Revenue)**: Predictable monthly revenue
- **ARR (Annual Recurring Revenue)**: MRR × 12
- **New MRR**: Revenue from new subscriptions
- **Churned MRR**: Revenue lost from cancellations
- **Net MRR Growth**: New MRR - Churned MRR

### Retention Metrics
- **Churn Rate**: Canceled subscriptions / total subscriptions
- **Retention Rate**: (1 - Churn Rate) × 100
- **Customer Retention**: Cohort-based retention over time
- **Logo Churn**: Customer churn (vs revenue churn)

### Customer Metrics
- **Customer Lifetime Value (LTV)**: Total subscription value per customer
- **Average Subscriptions Per Customer**: Total subs / customers
- **Active Subscription Rate**: Active subs / total subs created
- **Customer Acquisition Cost (CAC)**: Marketing spend / new customers

### Product Metrics
- **MRR by Product**: Revenue contribution by product
- **Subscription Count by Product**: Popularity by SKU
- **Average Order Value**: By subscription frequency
- **Billing Frequency Mix**: Monthly, quarterly, annual distribution

## References

- [Recharge API Documentation](https://developer.rechargepayments.com/)
- [Subscriptions API](https://developer.rechargepayments.com/2021-11/subscriptions)
- [Customers API](https://developer.rechargepayments.com/2021-11/customers)
- [Charges API](https://developer.rechargepayments.com/2021-11/charges)
- [Recharge Analytics Guide](https://support.rechargepayments.com/hc/en-us/articles/360008683594)

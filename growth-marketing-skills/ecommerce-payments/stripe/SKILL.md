---
name: stripe
description: "Stripe payment processing and billing API. Track payment transactions, subscriptions, customer lifetime value, revenue analytics, churn analysis, MRR/ARR metrics."
---

# Stripe Integration

## Overview

Stripe is a leading payment processing platform powering millions of businesses worldwide. This skill covers using the Stripe API to analyze payment data, track subscription metrics, calculate customer lifetime value, optimize pricing strategies, and reduce churn through data-driven insights.

## When to Use This Skill

- Payment transaction analysis and reconciliation
- Subscription revenue tracking (MRR, ARR, churn)
- Customer lifetime value calculations
- Revenue cohort analysis
- Failed payment recovery
- Pricing optimization and A/B testing
- Subscription retention and churn analysis
- Revenue forecasting and financial reporting

## Core Capabilities

### 1. Transaction Analysis and Revenue Tracking

```python
import stripe
import pandas as pd
from datetime import datetime, timedelta

# Initialize Stripe
stripe.api_key = "sk_test_your_secret_key"

# Get payment intents (transactions)
def get_payments(days=30, status='succeeded'):
    """Fetch successful payments for analysis"""
    start_date = int((datetime.now() - timedelta(days=days)).timestamp())

    payments = []
    has_more = True
    starting_after = None

    while has_more:
        params = {
            'limit': 100,
            'created': {'gte': start_date}
        }

        if starting_after:
            params['starting_after'] = starting_after

        response = stripe.PaymentIntent.list(**params)

        for payment in response.data:
            if payment.status == status:
                payments.append(payment)

        has_more = response.has_more
        if has_more:
            starting_after = response.data[-1].id

    return payments

# Calculate revenue metrics
def calculate_revenue_metrics(days=30):
    """Comprehensive payment analytics"""
    payments = get_payments(days=days)

    payment_data = []
    for payment in payments:
        payment_data.append({
            'payment_id': payment.id,
            'created': datetime.fromtimestamp(payment.created),
            'amount': payment.amount / 100,  # Convert from cents
            'currency': payment.currency,
            'status': payment.status,
            'customer_id': payment.customer,
            'payment_method': payment.payment_method,
            'description': payment.description,
            'metadata': payment.metadata
        })

    df = pd.DataFrame(payment_data)
    df['date'] = df['created'].dt.date

    # Calculate metrics
    metrics = {
        'total_revenue': df['amount'].sum(),
        'total_transactions': len(df),
        'average_transaction_value': df['amount'].mean(),
        'median_transaction_value': df['amount'].median(),
        'unique_customers': df['customer_id'].nunique(),
        'revenue_per_customer': df.groupby('customer_id')['amount'].sum().mean(),
        'daily_revenue': df.groupby('date')['amount'].sum().to_dict(),
        'currency_breakdown': df.groupby('currency')['amount'].sum().to_dict()
    }

    # Daily trends
    daily_stats = df.groupby('date').agg({
        'amount': ['sum', 'mean', 'count'],
        'customer_id': 'nunique'
    })

    return metrics, df, daily_stats

# Analyze payment methods
def analyze_payment_methods(days=30):
    """Track payment method performance"""
    payments = get_payments(days=days)

    # Get payment method details
    method_data = []

    for payment in payments:
        if payment.payment_method:
            try:
                pm = stripe.PaymentMethod.retrieve(payment.payment_method)
                method_data.append({
                    'payment_id': payment.id,
                    'type': pm.type,
                    'card_brand': pm.card.brand if pm.type == 'card' else None,
                    'amount': payment.amount / 100,
                    'status': payment.status
                })
            except:
                method_data.append({
                    'payment_id': payment.id,
                    'type': 'unknown',
                    'card_brand': None,
                    'amount': payment.amount / 100,
                    'status': payment.status
                })

    df = pd.DataFrame(method_data)

    # Payment method performance
    method_stats = df.groupby('type').agg({
        'amount': ['sum', 'mean', 'count']
    }).round(2)

    method_stats.columns = ['total_revenue', 'avg_transaction', 'transaction_count']
    method_stats['revenue_percent'] = (
        method_stats['total_revenue'] / method_stats['total_revenue'].sum() * 100
    ).round(2)

    return method_stats

# Failed payment analysis
def analyze_failed_payments(days=30):
    """Identify and analyze payment failures"""
    start_date = int((datetime.now() - timedelta(days=days)).timestamp())

    failed_payments = stripe.PaymentIntent.list(
        limit=100,
        created={'gte': start_date}
    )

    failure_data = []

    for payment in failed_payments.auto_paging_iter():
        if payment.status in ['requires_payment_method', 'canceled']:
            charges = payment.charges.data
            failure_reason = None

            if charges:
                failure_reason = charges[0].failure_message

            failure_data.append({
                'payment_id': payment.id,
                'amount': payment.amount / 100,
                'customer_id': payment.customer,
                'failure_reason': failure_reason,
                'created': datetime.fromtimestamp(payment.created)
            })

    if not failure_data:
        return None

    df = pd.DataFrame(failure_data)

    metrics = {
        'total_failed': len(df),
        'failed_revenue': df['amount'].sum(),
        'failure_reasons': df['failure_reason'].value_counts().to_dict()
    }

    return metrics, df

# Example usage
metrics, payments_df, daily_stats = calculate_revenue_metrics(days=30)
print(f"30-Day Payment Analytics:")
print(f"  Total Revenue: ${metrics['total_revenue']:,.2f}")
print(f"  Transactions: {metrics['total_transactions']}")
print(f"  Avg Transaction: ${metrics['average_transaction_value']:,.2f}")
print(f"  Unique Customers: {metrics['unique_customers']}")
```

### 2. Subscription Revenue and MRR/ARR Analysis

```python
# Get active subscriptions
def get_subscriptions(status='active'):
    """Fetch subscription data"""
    subscriptions = []

    params = {
        'limit': 100,
        'status': status
    }

    response = stripe.Subscription.list(**params)

    for sub in response.auto_paging_iter():
        subscriptions.append(sub)

    return subscriptions

# Calculate MRR and ARR
def calculate_mrr_arr():
    """Calculate Monthly Recurring Revenue and Annual Recurring Revenue"""
    subscriptions = get_subscriptions(status='active')

    sub_data = []

    for sub in subscriptions:
        # Get subscription amount
        amount = 0
        for item in sub['items'].data:
            price = item.price
            quantity = item.quantity

            # Convert to monthly amount
            if price.recurring.interval == 'month':
                monthly_amount = (price.unit_amount / 100) * quantity
            elif price.recurring.interval == 'year':
                monthly_amount = (price.unit_amount / 100) * quantity / 12
            elif price.recurring.interval == 'week':
                monthly_amount = (price.unit_amount / 100) * quantity * 4.33
            elif price.recurring.interval == 'day':
                monthly_amount = (price.unit_amount / 100) * quantity * 30
            else:
                monthly_amount = 0

            amount += monthly_amount

        sub_data.append({
            'subscription_id': sub.id,
            'customer_id': sub.customer,
            'status': sub.status,
            'mrr': amount,
            'plan_id': sub['items'].data[0].price.id,
            'created': datetime.fromtimestamp(sub.created),
            'current_period_start': datetime.fromtimestamp(sub.current_period_start),
            'current_period_end': datetime.fromtimestamp(sub.current_period_end)
        })

    df = pd.DataFrame(sub_data)

    metrics = {
        'total_mrr': df['mrr'].sum(),
        'arr': df['mrr'].sum() * 12,
        'total_subscriptions': len(df),
        'avg_mrr_per_customer': df['mrr'].mean(),
        'mrr_by_plan': df.groupby('plan_id')['mrr'].sum().to_dict()
    }

    return metrics, df

# Subscription cohort analysis
def subscription_cohort_analysis(months=12):
    """Analyze subscription retention by cohort"""
    # Get all subscriptions (including canceled)
    all_subs = []

    for status in ['active', 'canceled', 'past_due']:
        subs = get_subscriptions(status=status)
        all_subs.extend(subs)

    cohort_data = []

    for sub in all_subs:
        cohort_data.append({
            'customer_id': sub.customer,
            'subscription_id': sub.id,
            'created': datetime.fromtimestamp(sub.created),
            'status': sub.status,
            'canceled_at': datetime.fromtimestamp(sub.canceled_at) if sub.canceled_at else None
        })

    df = pd.DataFrame(cohort_data)

    # Cohort by signup month
    df['cohort_month'] = df['created'].dt.to_period('M')

    # Create cohort analysis table
    cohort_counts = df.groupby('cohort_month').agg({
        'subscription_id': 'count',
        'customer_id': 'nunique'
    })

    # Calculate retention by month
    active_by_cohort = df[df['status'] == 'active'].groupby('cohort_month')['subscription_id'].count()

    cohort_counts['active_subs'] = active_by_cohort
    cohort_counts['retention_rate'] = (
        cohort_counts['active_subs'] / cohort_counts['subscription_id'] * 100
    ).round(2)

    return cohort_counts

# Churn analysis
def calculate_churn_rate(months=6):
    """Calculate monthly churn rate"""
    start_date = datetime.now() - timedelta(days=30*months)
    start_timestamp = int(start_date.timestamp())

    # Get canceled subscriptions
    canceled_subs = stripe.Subscription.list(
        status='canceled',
        limit=100
    )

    churn_data = []

    for sub in canceled_subs.auto_paging_iter():
        if sub.canceled_at and sub.canceled_at >= start_timestamp:
            churn_data.append({
                'subscription_id': sub.id,
                'customer_id': sub.customer,
                'canceled_at': datetime.fromtimestamp(sub.canceled_at),
                'created_at': datetime.fromtimestamp(sub.created),
                'cancellation_reason': sub.cancellation_details.get('reason') if sub.cancellation_details else None
            })

    df = pd.DataFrame(churn_data)

    if len(df) == 0:
        return None

    df['cancel_month'] = df['canceled_at'].dt.to_period('M')

    # Get total active subs at beginning of each month
    monthly_churn = df.groupby('cancel_month').agg({
        'subscription_id': 'count'
    }).rename(columns={'subscription_id': 'churned_subs'})

    # Calculate churn rate
    # Note: You'd need to track beginning of month sub counts for accurate rate
    monthly_churn['churn_count'] = monthly_churn['churned_subs']

    return monthly_churn

# Revenue expansion and contraction
def analyze_mrr_movements(months=3):
    """Track MRR expansion, contraction, and churn"""
    # This requires tracking subscription changes over time
    # Simplified version using current subscription data

    subscriptions = get_subscriptions(status='active')

    # Get subscription items with quantity changes
    expansion_data = []

    for sub in subscriptions:
        # Check for recent updates
        if sub.created > (datetime.now() - timedelta(days=30*months)).timestamp():
            continue

        for item in sub['items'].data:
            expansion_data.append({
                'subscription_id': sub.id,
                'customer_id': sub.customer,
                'quantity': item.quantity,
                'price': item.price.unit_amount / 100
            })

    df = pd.DataFrame(expansion_data)

    # Track upgrades (quantity increases)
    # This is simplified - real implementation would track historical changes

    return df

# Example usage
mrr_metrics, subs_df = calculate_mrr_arr()
print(f"Subscription Metrics:")
print(f"  MRR: ${mrr_metrics['total_mrr']:,.2f}")
print(f"  ARR: ${mrr_metrics['arr']:,.2f}")
print(f"  Active Subscriptions: {mrr_metrics['total_subscriptions']}")
print(f"  Avg MRR per Customer: ${mrr_metrics['avg_mrr_per_customer']:,.2f}")
```

### 3. Customer Lifetime Value and Analytics

```python
# Get customer data
def get_customers(limit=100):
    """Fetch customer data"""
    customers = []

    response = stripe.Customer.list(limit=limit)

    for customer in response.auto_paging_iter():
        customers.append(customer)

    return customers

# Calculate customer lifetime value
def calculate_customer_ltv():
    """Analyze customer lifetime value from Stripe data"""
    customers = get_customers(limit=500)

    customer_data = []

    for customer in customers:
        # Get customer's payment history
        payments = stripe.PaymentIntent.list(
            customer=customer.id,
            limit=100
        )

        total_spent = 0
        payment_count = 0
        first_payment = None
        last_payment = None

        for payment in payments.auto_paging_iter():
            if payment.status == 'succeeded':
                total_spent += payment.amount / 100
                payment_count += 1

                payment_date = datetime.fromtimestamp(payment.created)

                if first_payment is None or payment_date < first_payment:
                    first_payment = payment_date
                if last_payment is None or payment_date > last_payment:
                    last_payment = payment_date

        # Get subscription data
        subscriptions = stripe.Subscription.list(
            customer=customer.id,
            limit=10
        )

        has_subscription = len(subscriptions.data) > 0

        customer_data.append({
            'customer_id': customer.id,
            'email': customer.email,
            'created': datetime.fromtimestamp(customer.created),
            'total_spent': total_spent,
            'payment_count': payment_count,
            'first_payment': first_payment,
            'last_payment': last_payment,
            'has_subscription': has_subscription,
            'metadata': customer.metadata
        })

    df = pd.DataFrame(customer_data)

    # Remove customers with no payments
    df = df[df['payment_count'] > 0]

    if len(df) == 0:
        return {}, df

    # Calculate additional metrics
    df['avg_transaction_value'] = df['total_spent'] / df['payment_count']
    df['customer_lifetime_days'] = (df['last_payment'] - df['first_payment']).dt.days
    df['days_since_last_payment'] = (datetime.now() - df['last_payment']).dt.days

    # Segment by value
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
        'repeat_customer_rate': (df['payment_count'] > 1).sum() / len(df) * 100,
        'avg_payments_per_customer': df['payment_count'].mean(),
        'subscription_rate': df['has_subscription'].sum() / len(df) * 100,
        'segment_distribution': df['segment'].value_counts().to_dict()
    }

    return ltv_metrics, df

# Customer payment frequency analysis
def analyze_payment_frequency():
    """Analyze customer purchase patterns"""
    customers = get_customers(limit=500)

    frequency_data = []

    for customer in customers:
        payments = stripe.PaymentIntent.list(
            customer=customer.id,
            limit=100
        )

        payment_dates = []
        for payment in payments.auto_paging_iter():
            if payment.status == 'succeeded':
                payment_dates.append(datetime.fromtimestamp(payment.created))

        if len(payment_dates) > 1:
            payment_dates.sort()

            # Calculate average days between purchases
            intervals = [
                (payment_dates[i+1] - payment_dates[i]).days
                for i in range(len(payment_dates)-1)
            ]

            frequency_data.append({
                'customer_id': customer.id,
                'payment_count': len(payment_dates),
                'avg_days_between_purchases': sum(intervals) / len(intervals) if intervals else 0,
                'first_purchase': payment_dates[0],
                'last_purchase': payment_dates[-1]
            })

    df = pd.DataFrame(frequency_data)

    return df

# Revenue by customer segment
def segment_revenue_analysis():
    """Analyze revenue contribution by customer segment"""
    ltv_metrics, customers_df = calculate_customer_ltv()

    if len(customers_df) == 0:
        return None

    segment_revenue = customers_df.groupby('segment').agg({
        'total_spent': ['sum', 'mean', 'count'],
        'payment_count': 'mean'
    }).round(2)

    segment_revenue.columns = ['total_revenue', 'avg_ltv', 'customer_count', 'avg_purchases']
    segment_revenue['revenue_percent'] = (
        segment_revenue['total_revenue'] / segment_revenue['total_revenue'].sum() * 100
    ).round(2)

    return segment_revenue

# Example usage
ltv_metrics, customers_df = calculate_customer_ltv()
print(f"Customer Metrics:")
print(f"  Total Customers: {ltv_metrics['total_customers']}")
print(f"  Average LTV: ${ltv_metrics['average_ltv']:,.2f}")
print(f"  Repeat Rate: {ltv_metrics['repeat_customer_rate']:.1f}%")
print(f"  Subscription Rate: {ltv_metrics['subscription_rate']:.1f}%")
```

### 4. Revenue Optimization and Pricing Analytics

```python
# Analyze pricing tiers
def analyze_pricing_performance():
    """Analyze revenue by price point"""
    products = stripe.Product.list(limit=100)

    pricing_data = []

    for product in products.auto_paging_iter():
        # Get prices for this product
        prices = stripe.Price.list(product=product.id, limit=10)

        for price in prices.data:
            # Get subscriptions on this price
            subscriptions = stripe.Subscription.list(
                price=price.id,
                limit=100
            )

            sub_count = 0
            mrr = 0

            for sub in subscriptions.auto_paging_iter():
                if sub.status == 'active':
                    sub_count += 1

                    for item in sub['items'].data:
                        if item.price.id == price.id:
                            if price.recurring.interval == 'month':
                                mrr += (price.unit_amount / 100) * item.quantity
                            elif price.recurring.interval == 'year':
                                mrr += (price.unit_amount / 100) * item.quantity / 12

            pricing_data.append({
                'product_name': product.name,
                'price_id': price.id,
                'amount': price.unit_amount / 100,
                'currency': price.currency,
                'interval': price.recurring.interval if price.recurring else 'one_time',
                'active_subscriptions': sub_count,
                'mrr': mrr
            })

    df = pd.DataFrame(pricing_data)

    return df.sort_values('mrr', ascending=False)

# Discount and coupon analysis
def analyze_coupon_usage(months=6):
    """Track promotion and discount effectiveness"""
    coupons = stripe.Coupon.list(limit=100)

    coupon_data = []

    for coupon in coupons.auto_paging_iter():
        # Get promotion codes for this coupon
        promo_codes = stripe.PromotionCode.list(
            coupon=coupon.id,
            limit=100
        )

        for promo in promo_codes.data:
            coupon_data.append({
                'coupon_id': coupon.id,
                'code': promo.code,
                'amount_off': coupon.amount_off / 100 if coupon.amount_off else None,
                'percent_off': coupon.percent_off,
                'times_redeemed': promo.times_redeemed,
                'active': promo.active,
                'created': datetime.fromtimestamp(promo.created)
            })

    if not coupon_data:
        return None

    df = pd.DataFrame(coupon_data)

    coupon_performance = df.groupby('code').agg({
        'times_redeemed': 'sum',
        'amount_off': 'first',
        'percent_off': 'first'
    }).sort_values('times_redeemed', ascending=False)

    return coupon_performance

# Revenue recovery from failed payments
def analyze_payment_recovery():
    """Track success rate of payment retry logic"""
    # Get invoices with payment attempts
    invoices = stripe.Invoice.list(
        limit=100,
        status='open'
    )

    recovery_data = []

    for invoice in invoices.auto_paging_iter():
        # Check payment attempts
        if invoice.attempt_count > 1:
            recovery_data.append({
                'invoice_id': invoice.id,
                'customer_id': invoice.customer,
                'amount': invoice.amount_due / 100,
                'attempt_count': invoice.attempt_count,
                'status': invoice.status,
                'created': datetime.fromtimestamp(invoice.created)
            })

    if not recovery_data:
        return None

    df = pd.DataFrame(recovery_data)

    metrics = {
        'total_recovery_attempts': len(df),
        'total_at_risk_revenue': df['amount'].sum(),
        'avg_attempts': df['attempt_count'].mean()
    }

    return metrics, df

# Example usage
pricing_performance = analyze_pricing_performance()
print("Pricing Tier Performance:")
print(pricing_performance.head(10))
```

## Installation

```bash
# Install Stripe Python library
uv pip install stripe

# Additional packages for analytics
uv pip install pandas numpy python-dateutil
```

## Authentication

### API Keys

1. Go to Stripe Dashboard > Developers > API keys
2. Copy your Secret key (starts with `sk_test_` or `sk_live_`)
3. Never commit API keys to version control

```python
import stripe

# Test mode
stripe.api_key = "sk_test_xxxxxxxxxxxxx"

# Production mode
stripe.api_key = "sk_live_xxxxxxxxxxxxx"

# Test connection
try:
    balance = stripe.Balance.retrieve()
    print(f"Available balance: {balance.available[0].amount / 100}")
except stripe.error.AuthenticationError:
    print("Invalid API key")
```

## Quick Start

```python
import stripe
from datetime import datetime, timedelta

# Initialize
stripe.api_key = "sk_test_xxxxx"

# Get recent successful payments
payments = stripe.PaymentIntent.list(
    limit=10,
    created={'gte': int((datetime.now() - timedelta(days=7)).timestamp())}
)

print(f"Recent Payments: {len(payments.data)}")
for payment in payments.data:
    if payment.status == 'succeeded':
        print(f"${payment.amount/100:.2f} - {payment.description}")

# Get active subscriptions
subscriptions = stripe.Subscription.list(
    limit=10,
    status='active'
)

print(f"\nActive Subscriptions: {len(subscriptions.data)}")
for sub in subscriptions.data:
    print(f"Customer: {sub.customer} - ${sub.plan.amount/100:.2f}/{sub.plan.interval}")

# Get customers
customers = stripe.Customer.list(limit=5)

for customer in customers.data:
    print(f"{customer.email}: {customer.invoice_prefix}")
```

## Key Metrics Reference

### Revenue Metrics
- **Gross Revenue**: Total payment volume
- **Net Revenue**: Revenue after refunds and fees
- **MRR (Monthly Recurring Revenue)**: Predictable monthly subscription revenue
- **ARR (Annual Recurring Revenue)**: MRR × 12

### Subscription Metrics
- **Churn Rate**: Canceled subscriptions / total subscriptions
- **Retention Rate**: (1 - Churn Rate) × 100
- **Revenue Churn**: MRR lost from cancellations / total MRR
- **Expansion Revenue**: Upgrades and additional seats

### Customer Metrics
- **Customer Lifetime Value (LTV)**: Total revenue per customer
- **Customer Acquisition Cost (CAC)**: Marketing spend / new customers
- **LTV:CAC Ratio**: Target 3:1 or higher
- **Average Revenue Per User (ARPU)**: Total revenue / customers

### Payment Metrics
- **Success Rate**: Successful payments / total attempts
- **Decline Rate**: Failed payments / total attempts
- **Recovery Rate**: Recovered payments / failed payments
- **Average Transaction Value**: Total revenue / transactions

## References

- [Stripe API Documentation](https://stripe.com/docs/api)
- [Stripe Python Library](https://github.com/stripe/stripe-python)
- [Stripe Billing Documentation](https://stripe.com/docs/billing)
- [Stripe Metrics Guide](https://stripe.com/guides/revenue-recognition-for-saas)
- [Subscription Lifecycle](https://stripe.com/docs/billing/subscriptions/overview)

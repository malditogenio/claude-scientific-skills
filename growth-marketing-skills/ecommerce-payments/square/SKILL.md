---
name: square
description: "Square commerce ecosystem API. Payment processing, point-of-sale, customer analytics, inventory tracking, revenue optimization, omnichannel sales."
---

# Square Integration

## Overview

Square provides a complete commerce ecosystem including payment processing, point-of-sale hardware, and business management tools. This skill covers using the Square API to analyze payment transactions, track customer behavior across channels, optimize inventory, and calculate revenue metrics for omnichannel retail growth.

## When to Use This Skill

- Omnichannel payment and sales analytics
- Customer lifetime value across online and offline
- Inventory management and sell-through analysis
- Point-of-sale transaction tracking
- Multi-location revenue reporting
- Customer engagement and loyalty programs
- Payment processing optimization
- Business intelligence and forecasting

## Core Capabilities

### 1. Payment Transaction and Revenue Analytics

```python
from square.client import Client
import pandas as pd
from datetime import datetime, timedelta

# Initialize Square API client
ACCESS_TOKEN = "your_access_token"
client = Client(
    access_token=ACCESS_TOKEN,
    environment='production'  # or 'sandbox' for testing
)

# Get payments
def get_payments(days=30, location_id=None):
    """Fetch payment transactions"""
    end_at = datetime.now()
    begin_at = end_at - timedelta(days=days)

    # Format dates for Square API (RFC 3339)
    begin_time = begin_at.isoformat() + 'Z'
    end_time = end_at.isoformat() + 'Z'

    payments = []
    cursor = None

    while True:
        body = {
            'begin_time': begin_time,
            'end_time': end_time,
            'sort_order': 'DESC'
        }

        if location_id:
            body['location_id'] = location_id

        if cursor:
            body['cursor'] = cursor

        result = client.payments.list_payments(
            **body
        )

        if result.is_success():
            batch = result.body.get('payments', [])
            payments.extend(batch)

            cursor = result.body.get('cursor')
            if not cursor:
                break
        else:
            print(f"Error: {result.errors}")
            break

    return payments

# Calculate revenue metrics
def calculate_revenue_metrics(days=30, location_id=None):
    """Comprehensive payment analytics"""
    payments = get_payments(days=days, location_id=location_id)

    payment_data = []

    for payment in payments:
        # Only completed payments
        if payment.get('status') == 'COMPLETED':
            amount_money = payment.get('amount_money', {})
            total_money = payment.get('total_money', {})

            payment_data.append({
                'payment_id': payment['id'],
                'created_at': pd.to_datetime(payment['created_at']),
                'amount': float(amount_money.get('amount', 0)) / 100,  # Convert from cents
                'currency': amount_money.get('currency', 'USD'),
                'total_amount': float(total_money.get('amount', 0)) / 100,
                'status': payment.get('status'),
                'source_type': payment.get('source_type'),
                'location_id': payment.get('location_id'),
                'customer_id': payment.get('customer_id'),
                'order_id': payment.get('order_id'),
                'processing_fee': sum([
                    float(fee.get('amount_money', {}).get('amount', 0)) / 100
                    for fee in payment.get('processing_fee', [])
                ]),
                'card_brand': payment.get('card_details', {}).get('card', {}).get('card_brand'),
                'entry_method': payment.get('card_details', {}).get('entry_method')
            })

    df = pd.DataFrame(payment_data)

    if len(df) == 0:
        return {}, df, None

    df['date'] = df['created_at'].dt.date
    df['net_amount'] = df['amount'] - df['processing_fee']

    # Calculate metrics
    metrics = {
        'total_revenue': df['amount'].sum(),
        'net_revenue': df['net_amount'].sum(),
        'total_fees': df['processing_fee'].sum(),
        'total_payments': len(df),
        'average_payment_value': df['amount'].mean(),
        'median_payment_value': df['amount'].median(),
        'unique_customers': df[df['customer_id'].notna()]['customer_id'].nunique(),
        'revenue_per_customer': df[df['customer_id'].notna()].groupby('customer_id')['amount'].sum().mean(),
        'revenue_by_location': df.groupby('location_id')['amount'].sum().to_dict(),
        'revenue_by_card_brand': df.groupby('card_brand')['amount'].sum().to_dict(),
        'payment_method_distribution': df['source_type'].value_counts().to_dict()
    }

    # Daily trends
    daily_stats = df.groupby('date').agg({
        'amount': ['sum', 'mean', 'count'],
        'net_amount': 'sum',
        'customer_id': 'nunique'
    })

    return metrics, df, daily_stats

# Analyze payment methods
def analyze_payment_methods(days=30):
    """Track payment method performance"""
    payments = get_payments(days=days)

    method_data = []

    for payment in payments:
        if payment.get('status') == 'COMPLETED':
            amount = float(payment.get('amount_money', {}).get('amount', 0)) / 100

            method_data.append({
                'source_type': payment.get('source_type'),
                'card_brand': payment.get('card_details', {}).get('card', {}).get('card_brand'),
                'entry_method': payment.get('card_details', {}).get('entry_method'),
                'amount': amount
            })

    df = pd.DataFrame(method_data)

    if len(df) == 0:
        return None

    # Analyze by entry method (in-person vs online)
    entry_stats = df.groupby('entry_method').agg({
        'amount': ['sum', 'mean', 'count']
    }).round(2)

    entry_stats.columns = ['total_revenue', 'avg_transaction', 'transaction_count']
    entry_stats['revenue_percent'] = (
        entry_stats['total_revenue'] / entry_stats['total_revenue'].sum() * 100
    ).round(2)

    return entry_stats

# Example usage
metrics, payments_df, daily_stats = calculate_revenue_metrics(days=30)
if metrics:
    print(f"30-Day Square Analytics:")
    print(f"  Total Revenue: ${metrics['total_revenue']:,.2f}")
    print(f"  Net Revenue: ${metrics['net_revenue']:,.2f}")
    print(f"  Processing Fees: ${metrics['total_fees']:,.2f}")
    print(f"  Payments: {metrics['total_payments']}")
    print(f"  Avg Payment: ${metrics['average_payment_value']:,.2f}")
```

### 2. Customer Data and Lifetime Value

```python
# Get customers
def get_customers():
    """Fetch customer data"""
    customers = []
    cursor = None

    while True:
        body = {}
        if cursor:
            body['cursor'] = cursor

        result = client.customers.list_customers(**body)

        if result.is_success():
            batch = result.body.get('customers', [])
            customers.extend(batch)

            cursor = result.body.get('cursor')
            if not cursor:
                break
        else:
            print(f"Error: {result.errors}")
            break

    return customers

# Calculate customer lifetime value
def calculate_customer_ltv(days=365):
    """Analyze customer lifetime value"""
    customers = get_customers()
    payments = get_payments(days=days)

    # Build customer payment history
    customer_payments = {}

    for payment in payments:
        customer_id = payment.get('customer_id')

        if not customer_id or payment.get('status') != 'COMPLETED':
            continue

        amount = float(payment.get('amount_money', {}).get('amount', 0)) / 100
        date = pd.to_datetime(payment['created_at'])

        if customer_id not in customer_payments:
            customer_payments[customer_id] = {
                'payments': [],
                'total_spent': 0,
                'payment_count': 0
            }

        customer_payments[customer_id]['payments'].append({
            'date': date,
            'amount': amount
        })
        customer_payments[customer_id]['total_spent'] += amount
        customer_payments[customer_id]['payment_count'] += 1

    # Build customer dataframe
    customer_data = []

    for customer in customers:
        customer_id = customer['id']
        payment_data = customer_payments.get(customer_id)

        if not payment_data:
            continue

        payment_dates = [p['date'] for p in payment_data['payments']]
        first_payment = min(payment_dates)
        last_payment = max(payment_dates)

        customer_data.append({
            'customer_id': customer_id,
            'email': customer.get('email_address'),
            'phone': customer.get('phone_number'),
            'created_at': pd.to_datetime(customer.get('created_at')),
            'total_spent': payment_data['total_spent'],
            'payment_count': payment_data['payment_count'],
            'first_payment': first_payment,
            'last_payment': last_payment,
            'reference_id': customer.get('reference_id'),
            'note': customer.get('note')
        })

    df = pd.DataFrame(customer_data)

    if len(df) == 0:
        return {}, df

    # Calculate additional metrics
    df['avg_transaction_value'] = df['total_spent'] / df['payment_count']
    df['customer_lifetime_days'] = (df['last_payment'] - df['first_payment']).dt.days
    df['days_since_last_payment'] = (datetime.now() - df['last_payment']).dt.days

    # RFM Segmentation
    df['recency_score'] = pd.qcut(df['days_since_last_payment'], q=4, labels=[4,3,2,1], duplicates='drop')
    df['frequency_score'] = pd.qcut(df['payment_count'], q=4, labels=[1,2,3,4], duplicates='drop')
    df['monetary_score'] = pd.qcut(df['total_spent'], q=4, labels=[1,2,3,4], duplicates='drop')

    df['rfm_score'] = (
        df['recency_score'].astype(float) +
        df['frequency_score'].astype(float) +
        df['monetary_score'].astype(float)
    )

    # Customer segments
    df['segment'] = pd.cut(
        df['rfm_score'],
        bins=[0, 5, 8, 10, 12],
        labels=['At Risk', 'Potential', 'Loyal', 'Champions']
    )

    ltv_metrics = {
        'total_customers': len(df),
        'average_ltv': df['total_spent'].mean(),
        'median_ltv': df['total_spent'].median(),
        'top_10_percent_ltv': df.nlargest(int(len(df) * 0.1), 'total_spent')['total_spent'].mean(),
        'repeat_customer_rate': (df['payment_count'] > 1).sum() / len(df) * 100,
        'avg_payments_per_customer': df['payment_count'].mean(),
        'segment_distribution': df['segment'].value_counts().to_dict()
    }

    return ltv_metrics, df

# Get customer orders
def get_customer_orders(customer_id):
    """Get detailed order history for a customer"""
    result = client.orders.search_orders(
        body={
            'query': {
                'filter': {
                    'customer_filter': {
                        'customer_ids': [customer_id]
                    }
                }
            }
        }
    )

    if result.is_success():
        return result.body.get('orders', [])
    else:
        return []

# Example usage
ltv_metrics, customers_df = calculate_customer_ltv(days=365)
if ltv_metrics:
    print(f"Customer Metrics:")
    print(f"  Total Customers: {ltv_metrics['total_customers']}")
    print(f"  Average LTV: ${ltv_metrics['average_ltv']:,.2f}")
    print(f"  Repeat Rate: {ltv_metrics['repeat_customer_rate']:.1f}%")
    print(f"\nCustomer Segments:")
    for segment, count in ltv_metrics['segment_distribution'].items():
        print(f"  {segment}: {count} customers")
```

### 3. Inventory and Product Analytics

```python
# Get catalog items
def get_catalog_items():
    """Fetch product catalog"""
    items = []
    cursor = None

    while True:
        body = {
            'types': 'ITEM'
        }

        if cursor:
            body['cursor'] = cursor

        result = client.catalog.list_catalog(**body)

        if result.is_success():
            batch = result.body.get('objects', [])
            items.extend(batch)

            cursor = result.body.get('cursor')
            if not cursor:
                break
        else:
            print(f"Error: {result.errors}")
            break

    return items

# Product performance analysis
def analyze_product_performance(days=90):
    """Analyze product sales and revenue"""
    # Get orders for the period
    end_at = datetime.now()
    begin_at = end_at - timedelta(days=days)

    result = client.orders.search_orders(
        body={
            'query': {
                'filter': {
                    'date_time_filter': {
                        'created_at': {
                            'start_at': begin_at.isoformat() + 'Z',
                            'end_at': end_at.isoformat() + 'Z'
                        }
                    },
                    'state_filter': {
                        'states': ['COMPLETED']
                    }
                }
            },
            'limit': 500
        }
    )

    if not result.is_success():
        return None

    orders = result.body.get('orders', [])

    product_sales = {}

    for order in orders:
        line_items = order.get('line_items', [])

        for item in line_items:
            catalog_object_id = item.get('catalog_object_id')
            name = item.get('name', 'Unknown')

            if catalog_object_id not in product_sales:
                product_sales[catalog_object_id] = {
                    'name': name,
                    'quantity_sold': 0,
                    'revenue': 0,
                    'orders': 0
                }

            quantity = float(item.get('quantity', 1))
            amount = float(item.get('total_money', {}).get('amount', 0)) / 100

            product_sales[catalog_object_id]['quantity_sold'] += quantity
            product_sales[catalog_object_id]['revenue'] += amount
            product_sales[catalog_object_id]['orders'] += 1

    df = pd.DataFrame.from_dict(product_sales, orient='index')

    if len(df) == 0:
        return None

    df = df.sort_values('revenue', ascending=False)
    df['avg_price'] = df['revenue'] / df['quantity_sold']
    df['revenue_percent'] = (df['revenue'] / df['revenue'].sum() * 100).round(2)

    return df

# Get inventory counts
def get_inventory_counts(location_id):
    """Check inventory levels"""
    # Get catalog items
    items = get_catalog_items()

    inventory_data = []

    for item in items:
        item_data = item.get('item_data', {})
        variations = item_data.get('variations', [])

        for variation in variations:
            variation_id = variation['id']

            # Get inventory count
            result = client.inventory.retrieve_inventory_count(
                catalog_object_id=variation_id,
                location_ids=location_id
            )

            if result.is_success():
                counts = result.body.get('counts', [])

                for count in counts:
                    inventory_data.append({
                        'item_name': item_data.get('name'),
                        'variation_id': variation_id,
                        'variation_name': variation.get('item_variation_data', {}).get('name'),
                        'quantity': float(count.get('quantity', 0)),
                        'location_id': count.get('location_id'),
                        'state': count.get('state')
                    })

    df = pd.DataFrame(inventory_data)

    return df

# Example usage
product_performance = analyze_product_performance(days=90)
if product_performance is not None:
    print("Top 10 Products by Revenue:")
    print(product_performance.head(10)[['name', 'quantity_sold', 'revenue', 'revenue_percent']])
```

### 4. Multi-Location and Omnichannel Analytics

```python
# Get locations
def get_locations():
    """Fetch all business locations"""
    result = client.locations.list_locations()

    if result.is_success():
        return result.body.get('locations', [])
    else:
        return []

# Compare location performance
def compare_location_performance(days=30):
    """Analyze revenue by location"""
    locations = get_locations()
    location_stats = []

    for location in locations:
        location_id = location['id']
        location_name = location.get('name', 'Unknown')

        # Get payments for this location
        metrics, _, _ = calculate_revenue_metrics(days=days, location_id=location_id)

        if metrics:
            location_stats.append({
                'location_id': location_id,
                'location_name': location_name,
                'address': location.get('address', {}).get('locality', ''),
                'total_revenue': metrics.get('total_revenue', 0),
                'total_payments': metrics.get('total_payments', 0),
                'avg_payment': metrics.get('average_payment_value', 0),
                'unique_customers': metrics.get('unique_customers', 0)
            })

    df = pd.DataFrame(location_stats)

    if len(df) == 0:
        return None

    df = df.sort_values('total_revenue', ascending=False)
    df['revenue_percent'] = (df['total_revenue'] / df['total_revenue'].sum() * 100).round(2)

    return df

# Online vs in-person sales
def analyze_channel_performance(days=30):
    """Compare online and in-person sales"""
    payments = get_payments(days=days)

    channel_data = []

    for payment in payments:
        if payment.get('status') == 'COMPLETED':
            entry_method = payment.get('card_details', {}).get('entry_method', 'UNKNOWN')

            # Categorize as online or in-person
            if entry_method in ['KEYED', 'ON_FILE', 'EMV']:
                channel = 'In-Person'
            elif entry_method in ['CONTACTLESS', 'CHIP', 'SWIPED']:
                channel = 'In-Person'
            else:
                channel = 'Online'

            amount = float(payment.get('amount_money', {}).get('amount', 0)) / 100

            channel_data.append({
                'channel': channel,
                'entry_method': entry_method,
                'amount': amount
            })

    df = pd.DataFrame(channel_data)

    if len(df) == 0:
        return None

    channel_stats = df.groupby('channel').agg({
        'amount': ['sum', 'mean', 'count']
    }).round(2)

    channel_stats.columns = ['total_revenue', 'avg_transaction', 'transaction_count']
    channel_stats['revenue_percent'] = (
        channel_stats['total_revenue'] / channel_stats['total_revenue'].sum() * 100
    ).round(2)

    return channel_stats

# Example usage
location_performance = compare_location_performance(days=30)
if location_performance is not None:
    print("Location Performance:")
    print(location_performance)

channel_performance = analyze_channel_performance(days=30)
if channel_performance is not None:
    print("\nChannel Performance:")
    print(channel_performance)
```

## Installation

```bash
# Install Square Python SDK
uv pip install squareup

# Additional packages for analytics
uv pip install pandas python-dateutil
```

## Authentication

### Access Token

1. Go to Square Developer Dashboard: https://developer.squareup.com/
2. Create a new application
3. Copy the Access Token from the Credentials tab
4. Use Sandbox token for testing

```python
from square.client import Client

# Production
ACCESS_TOKEN = "your_production_access_token"
client = Client(
    access_token=ACCESS_TOKEN,
    environment='production'
)

# Sandbox (for testing)
SANDBOX_TOKEN = "your_sandbox_access_token"
sandbox_client = Client(
    access_token=SANDBOX_TOKEN,
    environment='sandbox'
)

# Test connection
result = client.locations.list_locations()

if result.is_success():
    locations = result.body.get('locations', [])
    print(f"Connected! Found {len(locations)} locations")
else:
    print(f"Error: {result.errors}")
```

## Quick Start

```python
from square.client import Client
from datetime import datetime, timedelta

# Initialize
ACCESS_TOKEN = "your_access_token"
client = Client(access_token=ACCESS_TOKEN, environment='production')

# Get recent payments
end_at = datetime.now()
begin_at = end_at - timedelta(days=7)

result = client.payments.list_payments(
    begin_time=begin_at.isoformat() + 'Z',
    end_time=end_at.isoformat() + 'Z',
    sort_order='DESC'
)

if result.is_success():
    payments = result.body.get('payments', [])
    print(f"Recent Payments: {len(payments)}")

    for payment in payments[:5]:
        amount = float(payment['amount_money']['amount']) / 100
        print(f"${amount:.2f} - {payment['status']}")

# Get customers
result = client.customers.list_customers()

if result.is_success():
    customers = result.body.get('customers', [])
    print(f"\nTotal Customers: {len(customers)}")
```

## Key Metrics Reference

### Revenue Metrics
- **Gross Revenue**: Total payment volume
- **Net Revenue**: Revenue after processing fees
- **Average Transaction Value**: Total revenue / transactions
- **Revenue Per Location**: Sales by store location

### Customer Metrics
- **Customer Lifetime Value (LTV)**: Total customer spend
- **RFM Score**: Recency + Frequency + Monetary
- **Repeat Customer Rate**: Customers with 2+ purchases
- **Customer Segments**: Champions, Loyal, Potential, At Risk

### Product Metrics
- **Units Sold**: Quantity sold by product
- **Revenue Per Product**: Sales by SKU
- **Inventory Turnover**: Sales / average inventory
- **Product Mix**: Revenue distribution by category

### Channel Metrics
- **Online vs In-Person**: Revenue by channel
- **Location Performance**: Sales by store
- **Payment Method Mix**: Card, cash, digital wallet
- **Entry Method**: Chip, contactless, keyed, swiped

## References

- [Square API Documentation](https://developer.squareup.com/docs)
- [Square Python SDK](https://github.com/square/square-python-sdk)
- [Payments API](https://developer.squareup.com/reference/square/payments-api)
- [Customers API](https://developer.squareup.com/reference/square/customers-api)
- [Catalog API](https://developer.squareup.com/reference/square/catalog-api)
- [Orders API](https://developer.squareup.com/reference/square/orders-api)

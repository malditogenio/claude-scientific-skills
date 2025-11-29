---
name: shopify
description: "Shopify e-commerce platform API integration. Access store data, orders, customers, products, inventory. Analyze sales trends, customer lifetime value, cohort analysis, revenue optimization."
---

# Shopify Integration

## Overview

Shopify is a leading e-commerce platform powering over 4 million stores worldwide. This skill covers using the Shopify Admin API and Storefront API to analyze customer behavior, track revenue metrics, optimize product performance, and build data-driven marketing campaigns.

## When to Use This Skill

- Analyzing customer purchase behavior and LTV
- Tracking order trends and revenue metrics
- Customer segmentation for targeted marketing
- Product performance analysis and optimization
- Inventory management and forecasting
- Cohort analysis and retention metrics
- Abandoned cart recovery campaigns
- Subscription and recurring revenue tracking

## Core Capabilities

### 1. Order Management and Analytics

```python
import shopify
import pandas as pd
from datetime import datetime, timedelta

# Initialize Shopify session
shop_url = "your-store.myshopify.com"
api_version = "2024-01"
access_token = "your-access-token"

session = shopify.Session(shop_url, api_version, access_token)
shopify.ShopifyResource.activate_session(session)

# Get orders with detailed analysis
def get_orders(start_date=None, status='any', limit=250):
    """Fetch orders for analysis"""
    params = {
        'status': status,
        'limit': limit,
        'fields': 'id,order_number,created_at,total_price,subtotal_price,customer,line_items,financial_status'
    }

    if start_date:
        params['created_at_min'] = start_date.isoformat()

    orders = shopify.Order.find(**params)
    return orders

# Calculate revenue metrics
def calculate_revenue_metrics(days=30):
    """Calculate key revenue metrics"""
    start_date = datetime.now() - timedelta(days=days)
    orders = get_orders(start_date=start_date, status='any')

    order_data = []
    for order in orders:
        order_data.append({
            'order_id': order.id,
            'order_number': order.order_number,
            'created_at': order.created_at,
            'total_price': float(order.total_price),
            'subtotal_price': float(order.subtotal_price),
            'customer_id': order.customer.id if order.customer else None,
            'financial_status': order.financial_status,
            'items_count': len(order.line_items)
        })

    df = pd.DataFrame(order_data)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['date'] = df['created_at'].dt.date

    # Calculate metrics
    metrics = {
        'total_revenue': df['total_price'].sum(),
        'total_orders': len(df),
        'average_order_value': df['total_price'].mean(),
        'unique_customers': df['customer_id'].nunique(),
        'revenue_per_customer': df.groupby('customer_id')['total_price'].sum().mean(),
        'daily_revenue': df.groupby('date')['total_price'].sum().to_dict()
    }

    return metrics, df

# Get revenue trends
def analyze_revenue_trends(months=6):
    """Analyze monthly revenue trends"""
    start_date = datetime.now() - timedelta(days=30*months)
    orders = get_orders(start_date=start_date)

    order_data = []
    for order in orders:
        order_data.append({
            'date': pd.to_datetime(order.created_at),
            'revenue': float(order.total_price),
            'order_id': order.id
        })

    df = pd.DataFrame(order_data)
    df['month'] = df['date'].dt.to_period('M')

    monthly_stats = df.groupby('month').agg({
        'revenue': ['sum', 'mean', 'count'],
        'order_id': 'nunique'
    }).round(2)

    # Calculate month-over-month growth
    monthly_revenue = df.groupby('month')['revenue'].sum()
    mom_growth = monthly_revenue.pct_change() * 100

    return monthly_stats, mom_growth

# Example usage
metrics, orders_df = calculate_revenue_metrics(days=30)
print(f"Total Revenue: ${metrics['total_revenue']:,.2f}")
print(f"Average Order Value: ${metrics['average_order_value']:,.2f}")
print(f"Orders: {metrics['total_orders']}")
print(f"Unique Customers: {metrics['unique_customers']}")
```

### 2. Customer Data and Lifetime Value

```python
# Customer lifetime value analysis
def calculate_customer_ltv(lookback_days=365):
    """Calculate customer lifetime value metrics"""
    start_date = datetime.now() - timedelta(days=lookback_days)
    orders = get_orders(start_date=start_date, status='any')

    customer_data = {}

    for order in orders:
        if not order.customer:
            continue

        customer_id = order.customer.id

        if customer_id not in customer_data:
            customer_data[customer_id] = {
                'email': order.customer.email,
                'first_order_date': order.created_at,
                'last_order_date': order.created_at,
                'total_spent': 0,
                'order_count': 0,
                'orders': []
            }

        customer_data[customer_id]['total_spent'] += float(order.total_price)
        customer_data[customer_id]['order_count'] += 1
        customer_data[customer_id]['orders'].append({
            'date': order.created_at,
            'amount': float(order.total_price)
        })

        # Update date range
        if order.created_at < customer_data[customer_id]['first_order_date']:
            customer_data[customer_id]['first_order_date'] = order.created_at
        if order.created_at > customer_data[customer_id]['last_order_date']:
            customer_data[customer_id]['last_order_date'] = order.created_at

    # Calculate LTV metrics
    df = pd.DataFrame.from_dict(customer_data, orient='index')
    df['first_order_date'] = pd.to_datetime(df['first_order_date'])
    df['last_order_date'] = pd.to_datetime(df['last_order_date'])
    df['customer_lifetime_days'] = (df['last_order_date'] - df['first_order_date']).dt.days
    df['avg_order_value'] = df['total_spent'] / df['order_count']

    # Segment customers by value
    df['segment'] = pd.qcut(df['total_spent'], q=4, labels=['Bronze', 'Silver', 'Gold', 'Platinum'])

    ltv_metrics = {
        'average_ltv': df['total_spent'].mean(),
        'median_ltv': df['total_spent'].median(),
        'top_10_percent_ltv': df.nlargest(int(len(df) * 0.1), 'total_spent')['total_spent'].mean(),
        'repeat_customer_rate': (df['order_count'] > 1).sum() / len(df) * 100,
        'avg_orders_per_customer': df['order_count'].mean(),
        'segment_distribution': df['segment'].value_counts().to_dict()
    }

    return ltv_metrics, df

# Get high-value customer segments
def get_vip_customers(min_spent=1000, min_orders=3):
    """Identify VIP customers for targeted marketing"""
    customers = shopify.Customer.find(limit=250)

    vip_customers = []

    for customer in customers:
        total_spent = float(customer.total_spent) if hasattr(customer, 'total_spent') else 0
        orders_count = int(customer.orders_count) if hasattr(customer, 'orders_count') else 0

        if total_spent >= min_spent and orders_count >= min_orders:
            vip_customers.append({
                'id': customer.id,
                'email': customer.email,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'total_spent': total_spent,
                'orders_count': orders_count,
                'created_at': customer.created_at,
                'tags': customer.tags
            })

    return pd.DataFrame(vip_customers)

# Customer cohort analysis
def cohort_analysis(months=12):
    """Analyze customer cohorts and retention"""
    start_date = datetime.now() - timedelta(days=30*months)
    orders = get_orders(start_date=start_date)

    cohort_data = []

    for order in orders:
        if order.customer:
            cohort_data.append({
                'customer_id': order.customer.id,
                'order_date': pd.to_datetime(order.created_at),
                'revenue': float(order.total_price)
            })

    df = pd.DataFrame(cohort_data)

    # Determine cohort month (first purchase month)
    df['cohort_month'] = df.groupby('customer_id')['order_date'].transform('min').dt.to_period('M')
    df['order_month'] = df['order_date'].dt.to_period('M')

    # Calculate months since first purchase
    df['cohort_age'] = (df['order_month'] - df['cohort_month']).apply(lambda x: x.n)

    # Cohort analysis table
    cohort_pivot = df.groupby(['cohort_month', 'cohort_age'])['customer_id'].nunique().unstack(fill_value=0)

    # Calculate retention rates
    cohort_size = cohort_pivot.iloc[:, 0]
    retention = cohort_pivot.divide(cohort_size, axis=0) * 100

    return retention.round(1)

# Example usage
ltv_metrics, customer_df = calculate_customer_ltv(lookback_days=365)
print(f"Average LTV: ${ltv_metrics['average_ltv']:,.2f}")
print(f"Repeat Customer Rate: {ltv_metrics['repeat_customer_rate']:.1f}%")
print(f"\nCustomer Segments:")
for segment, count in ltv_metrics['segment_distribution'].items():
    print(f"  {segment}: {count} customers")

vip_customers = get_vip_customers(min_spent=1000, min_orders=3)
print(f"\nVIP Customers: {len(vip_customers)}")
```

### 3. Product Management and Performance

```python
# Product performance analysis
def analyze_product_performance(days=90):
    """Analyze product sales and performance"""
    start_date = datetime.now() - timedelta(days=days)
    orders = get_orders(start_date=start_date)

    product_sales = {}

    for order in orders:
        for item in order.line_items:
            product_id = item.product_id

            if product_id not in product_sales:
                product_sales[product_id] = {
                    'name': item.name,
                    'sku': item.sku,
                    'quantity_sold': 0,
                    'revenue': 0,
                    'orders': 0
                }

            product_sales[product_id]['quantity_sold'] += item.quantity
            product_sales[product_id]['revenue'] += float(item.price) * item.quantity
            product_sales[product_id]['orders'] += 1

    df = pd.DataFrame.from_dict(product_sales, orient='index')
    df = df.sort_values('revenue', ascending=False)
    df['avg_price'] = df['revenue'] / df['quantity_sold']
    df['revenue_percent'] = (df['revenue'] / df['revenue'].sum() * 100).round(2)

    return df

# Get inventory levels
def get_inventory_status(location_id=None):
    """Monitor inventory levels for restocking"""
    products = shopify.Product.find(limit=250)

    inventory_data = []

    for product in products:
        for variant in product.variants:
            inventory_data.append({
                'product_id': product.id,
                'product_title': product.title,
                'variant_id': variant.id,
                'variant_title': variant.title,
                'sku': variant.sku,
                'price': float(variant.price),
                'inventory_quantity': variant.inventory_quantity,
                'inventory_policy': variant.inventory_policy
            })

    df = pd.DataFrame(inventory_data)

    # Flag low stock items
    df['stock_status'] = df['inventory_quantity'].apply(
        lambda x: 'Out of Stock' if x <= 0 else 'Low Stock' if x < 10 else 'In Stock'
    )

    return df

# Product recommendation analysis
def analyze_product_associations(min_support=0.01):
    """Find products frequently bought together"""
    from itertools import combinations

    orders = get_orders(status='any', limit=250)

    # Build transaction data
    transactions = []
    for order in orders:
        products = [item.product_id for item in order.line_items]
        if len(products) > 1:
            transactions.append(products)

    # Count product pairs
    pair_counts = {}
    for transaction in transactions:
        for pair in combinations(set(transaction), 2):
            pair = tuple(sorted(pair))
            pair_counts[pair] = pair_counts.get(pair, 0) + 1

    # Calculate support
    total_transactions = len(transactions)
    associations = []

    for (prod_a, prod_b), count in pair_counts.items():
        support = count / total_transactions
        if support >= min_support:
            associations.append({
                'product_a': prod_a,
                'product_b': prod_b,
                'co_purchases': count,
                'support': support
            })

    return pd.DataFrame(associations).sort_values('support', ascending=False)

# Example usage
product_performance = analyze_product_performance(days=90)
print("Top 10 Products by Revenue:")
print(product_performance.head(10)[['name', 'quantity_sold', 'revenue', 'revenue_percent']])

inventory = get_inventory_status()
low_stock = inventory[inventory['stock_status'] != 'In Stock']
print(f"\nLow/Out of Stock Items: {len(low_stock)}")
```

### 4. Marketing Campaign Analytics

```python
# Abandoned cart recovery
def analyze_abandoned_carts(days=7):
    """Analyze abandoned checkouts for recovery campaigns"""
    start_date = datetime.now() - timedelta(days=days)

    checkouts = shopify.Checkout.find(
        created_at_min=start_date.isoformat(),
        status='open',
        limit=250
    )

    abandoned_data = []

    for checkout in checkouts:
        if checkout.email:
            abandoned_data.append({
                'checkout_id': checkout.id,
                'email': checkout.email,
                'created_at': checkout.created_at,
                'abandoned_value': float(checkout.total_price),
                'line_items_count': len(checkout.line_items),
                'customer_id': checkout.customer_id
            })

    df = pd.DataFrame(abandoned_data)

    metrics = {
        'total_abandoned': len(df),
        'total_value': df['abandoned_value'].sum(),
        'avg_cart_value': df['abandoned_value'].mean(),
        'recovery_potential': df['abandoned_value'].sum()
    }

    return metrics, df

# Discount code performance
def analyze_discount_codes(days=90):
    """Analyze discount code usage and effectiveness"""
    start_date = datetime.now() - timedelta(days=days)
    orders = get_orders(start_date=start_date)

    discount_data = []

    for order in orders:
        if hasattr(order, 'discount_codes') and order.discount_codes:
            for discount in order.discount_codes:
                discount_data.append({
                    'code': discount.code,
                    'amount': float(discount.amount),
                    'order_value': float(order.total_price),
                    'order_date': order.created_at
                })

    if not discount_data:
        return None

    df = pd.DataFrame(discount_data)

    performance = df.groupby('code').agg({
        'amount': ['sum', 'count', 'mean'],
        'order_value': 'sum'
    }).round(2)

    performance.columns = ['total_discount', 'usage_count', 'avg_discount', 'revenue_generated']
    performance['roi'] = (performance['revenue_generated'] / performance['total_discount']).round(2)

    return performance.sort_values('usage_count', ascending=False)

# Customer acquisition source analysis
def analyze_traffic_sources(days=30):
    """Analyze order sources for attribution"""
    start_date = datetime.now() - timedelta(days=days)
    orders = get_orders(start_date=start_date)

    source_data = []

    for order in orders:
        source = 'Direct'
        if hasattr(order, 'source_name'):
            source = order.source_name or 'Direct'

        source_data.append({
            'source': source,
            'revenue': float(order.total_price),
            'order_id': order.id
        })

    df = pd.DataFrame(source_data)

    source_performance = df.groupby('source').agg({
        'revenue': 'sum',
        'order_id': 'count'
    }).rename(columns={'order_id': 'orders'})

    source_performance['avg_order_value'] = (
        source_performance['revenue'] / source_performance['orders']
    ).round(2)

    source_performance['revenue_percent'] = (
        source_performance['revenue'] / source_performance['revenue'].sum() * 100
    ).round(2)

    return source_performance.sort_values('revenue', ascending=False)

# Example usage
abandoned_metrics, abandoned_carts = analyze_abandoned_carts(days=7)
print(f"Abandoned Carts (7 days):")
print(f"  Total: {abandoned_metrics['total_abandoned']}")
print(f"  Potential Revenue: ${abandoned_metrics['recovery_potential']:,.2f}")
print(f"  Average Cart Value: ${abandoned_metrics['avg_cart_value']:,.2f}")

traffic_sources = analyze_traffic_sources(days=30)
print(f"\nTop Traffic Sources:")
print(traffic_sources)
```

## Installation

```bash
# Install Shopify Python library
uv pip install ShopifyAPI

# Additional packages for analytics
uv pip install pandas numpy python-dateutil
```

## Authentication

### Private App Access Token (Recommended for Internal Tools)

1. In Shopify Admin, go to Settings > Apps and sales channels > Develop apps
2. Create a new app and configure Admin API scopes
3. Install the app and copy the Admin API access token

```python
import shopify

shop_url = "your-store.myshopify.com"
api_version = "2024-01"
access_token = "shpat_xxxxx"

session = shopify.Session(shop_url, api_version, access_token)
shopify.ShopifyResource.activate_session(session)
```

### OAuth (For Public Apps)

```python
# OAuth flow for public apps
import shopify

API_KEY = 'your-api-key'
API_SECRET = 'your-api-secret'
SCOPES = ['read_products', 'read_orders', 'read_customers']

# Generate authorization URL
shop_url = "store.myshopify.com"
redirect_uri = "https://yourapp.com/callback"

permission_url = shopify.Session(shop_url, api_version).create_permission_url(
    SCOPES, redirect_uri
)

# After user approves, exchange code for token
# (handle in your callback endpoint)
```

## Quick Start

```python
import shopify
from datetime import datetime, timedelta

# Initialize connection
shop_url = "your-store.myshopify.com"
api_version = "2024-01"
access_token = "shpat_xxxxx"

session = shopify.Session(shop_url, api_version, access_token)
shopify.ShopifyResource.activate_session(session)

# Get recent orders
orders = shopify.Order.find(
    limit=10,
    status='any',
    created_at_min=(datetime.now() - timedelta(days=7)).isoformat()
)

print(f"Orders in last 7 days: {len(orders)}")

for order in orders:
    print(f"Order #{order.order_number}: ${order.total_price}")

# Get product information
products = shopify.Product.find(limit=5)

for product in products:
    print(f"{product.title}: {len(product.variants)} variants")

# Get customer data
customers = shopify.Customer.find(limit=10)

for customer in customers:
    print(f"{customer.email}: {customer.orders_count} orders, ${customer.total_spent} spent")
```

## Key Metrics Reference

### Revenue Metrics
- **Total Revenue**: Sum of all order totals
- **Average Order Value (AOV)**: Total revenue / number of orders
- **Revenue Per Customer**: Total revenue / unique customers
- **Monthly Recurring Revenue (MRR)**: For subscription products

### Customer Metrics
- **Customer Lifetime Value (LTV)**: Total spend per customer over lifetime
- **Repeat Customer Rate**: Customers with 2+ orders / total customers
- **Customer Acquisition Cost (CAC)**: Marketing spend / new customers
- **Cohort Retention**: Percentage of customers who return each month

### Product Metrics
- **Units Sold**: Total quantity of products sold
- **Revenue Per Product**: Total revenue by product
- **Inventory Turnover**: Units sold / average inventory
- **Product Attach Rate**: Secondary products per order

### Conversion Metrics
- **Cart Abandonment Rate**: Abandoned carts / total carts
- **Checkout Conversion Rate**: Orders / checkouts initiated
- **Add to Cart Rate**: Products added / product views

## References

- [Shopify Admin API Documentation](https://shopify.dev/docs/api/admin-rest)
- [Shopify GraphQL API](https://shopify.dev/docs/api/admin-graphql)
- [ShopifyAPI Python Library](https://github.com/Shopify/shopify_python_api)
- [Shopify Analytics Guide](https://help.shopify.com/en/manual/reports-and-analytics)
- [Shopify App Development](https://shopify.dev/docs/apps)

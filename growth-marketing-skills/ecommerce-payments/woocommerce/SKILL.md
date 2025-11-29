---
name: woocommerce
description: "WooCommerce WordPress e-commerce plugin REST API integration. Access orders, products, customers, analytics. Track sales performance, customer behavior, revenue optimization."
---

# WooCommerce Integration

## Overview

WooCommerce is the most popular e-commerce plugin for WordPress, powering over 5 million online stores. This skill covers using the WooCommerce REST API to analyze sales data, track customer behavior, optimize product performance, and build marketing automation workflows.

## When to Use This Skill

- Analyzing sales trends and revenue metrics
- Customer segmentation and behavioral analysis
- Product performance tracking and optimization
- Order fulfillment and inventory management
- Marketing campaign attribution and ROI
- Customer lifetime value calculations
- Abandoned cart analysis
- Multi-channel sales tracking

## Core Capabilities

### 1. Order Management and Analytics

```python
from woocommerce import API
import pandas as pd
from datetime import datetime, timedelta

# Initialize WooCommerce API
wcapi = API(
    url="https://yourstore.com",
    consumer_key="ck_xxxxx",
    consumer_secret="cs_xxxxx",
    version="wc/v3",
    timeout=30
)

# Get orders with analytics
def get_orders(start_date=None, status='any', per_page=100):
    """Fetch orders for analysis"""
    params = {
        'per_page': per_page,
        'status': status,
        'orderby': 'date',
        'order': 'desc'
    }

    if start_date:
        params['after'] = start_date.isoformat()

    orders = wcapi.get("orders", params=params).json()
    return orders

# Calculate revenue metrics
def calculate_revenue_metrics(days=30):
    """Comprehensive revenue analysis"""
    start_date = datetime.now() - timedelta(days=days)
    orders = get_orders(start_date=start_date, status='completed')

    order_data = []
    for order in orders:
        order_data.append({
            'order_id': order['id'],
            'order_number': order['number'],
            'date_created': pd.to_datetime(order['date_created']),
            'total': float(order['total']),
            'subtotal': float(order.get('cart_subtotal', 0)),
            'shipping': float(order.get('shipping_total', 0)),
            'tax': float(order.get('total_tax', 0)),
            'discount': float(order.get('discount_total', 0)),
            'customer_id': order.get('customer_id', 0),
            'payment_method': order.get('payment_method', 'unknown'),
            'items_count': len(order.get('line_items', []))
        })

    df = pd.DataFrame(order_data)
    df['date'] = df['date_created'].dt.date

    # Calculate comprehensive metrics
    metrics = {
        'total_revenue': df['total'].sum(),
        'gross_revenue': df['subtotal'].sum(),
        'total_orders': len(df),
        'average_order_value': df['total'].mean(),
        'median_order_value': df['total'].median(),
        'total_shipping': df['shipping'].sum(),
        'total_tax': df['tax'].sum(),
        'total_discounts': df['discount'].sum(),
        'unique_customers': df[df['customer_id'] > 0]['customer_id'].nunique(),
        'daily_revenue': df.groupby('date')['total'].sum().to_dict(),
        'payment_method_breakdown': df.groupby('payment_method')['total'].sum().to_dict()
    }

    # Revenue trends
    daily_stats = df.groupby('date').agg({
        'total': ['sum', 'mean', 'count'],
        'customer_id': 'nunique'
    })

    return metrics, df, daily_stats

# Sales by hour analysis
def analyze_sales_by_hour(days=30):
    """Find peak sales hours for campaign timing"""
    start_date = datetime.now() - timedelta(days=days)
    orders = get_orders(start_date=start_date, status='completed')

    hourly_data = []
    for order in orders:
        date_created = pd.to_datetime(order['date_created'])
        hourly_data.append({
            'hour': date_created.hour,
            'day_of_week': date_created.day_name(),
            'revenue': float(order['total'])
        })

    df = pd.DataFrame(hourly_data)

    # Hour of day analysis
    hourly_revenue = df.groupby('hour').agg({
        'revenue': ['sum', 'count', 'mean']
    }).round(2)

    # Day of week analysis
    daily_revenue = df.groupby('day_of_week').agg({
        'revenue': ['sum', 'count', 'mean']
    }).round(2)

    return hourly_revenue, daily_revenue

# Example usage
metrics, orders_df, daily_stats = calculate_revenue_metrics(days=30)
print(f"30-Day Performance:")
print(f"  Total Revenue: ${metrics['total_revenue']:,.2f}")
print(f"  Orders: {metrics['total_orders']}")
print(f"  AOV: ${metrics['average_order_value']:,.2f}")
print(f"  Unique Customers: {metrics['unique_customers']}")
print(f"  Total Discounts: ${metrics['total_discounts']:,.2f}")
```

### 2. Customer Data and Lifetime Value

```python
# Customer lifetime value analysis
def calculate_customer_ltv(min_orders=1):
    """Calculate and segment customers by LTV"""
    # Get all customers
    customers = []
    page = 1
    per_page = 100

    while True:
        response = wcapi.get("customers", params={
            'per_page': per_page,
            'page': page
        }).json()

        if not response:
            break

        customers.extend(response)
        page += 1

        if len(response) < per_page:
            break

    customer_data = []

    for customer in customers:
        if customer.get('orders_count', 0) >= min_orders:
            customer_data.append({
                'customer_id': customer['id'],
                'email': customer['email'],
                'first_name': customer.get('first_name', ''),
                'last_name': customer.get('last_name', ''),
                'date_created': pd.to_datetime(customer['date_created']),
                'orders_count': customer.get('orders_count', 0),
                'total_spent': float(customer.get('total_spent', 0)),
                'avatar_url': customer.get('avatar_url', '')
            })

    df = pd.DataFrame(customer_data)

    # Calculate additional metrics
    df['avg_order_value'] = df['total_spent'] / df['orders_count']
    df['days_since_signup'] = (datetime.now() - df['date_created']).dt.days
    df['monthly_value'] = (df['total_spent'] / df['days_since_signup'] * 30).fillna(0)

    # Segment customers
    df['segment'] = pd.cut(
        df['total_spent'],
        bins=[0, 100, 500, 1000, float('inf')],
        labels=['Low Value', 'Medium Value', 'High Value', 'VIP']
    )

    # RFM analysis
    current_date = datetime.now()

    ltv_metrics = {
        'total_customers': len(df),
        'average_ltv': df['total_spent'].mean(),
        'median_ltv': df['total_spent'].median(),
        'top_10_percent_ltv': df.nlargest(int(len(df) * 0.1), 'total_spent')['total_spent'].mean(),
        'repeat_rate': (df['orders_count'] > 1).sum() / len(df) * 100,
        'avg_orders_per_customer': df['orders_count'].mean(),
        'segment_distribution': df['segment'].value_counts().to_dict(),
        'total_customer_value': df['total_spent'].sum()
    }

    return ltv_metrics, df

# Get customer purchase history
def get_customer_purchase_history(customer_id):
    """Detailed purchase history for individual customer"""
    orders = wcapi.get("orders", params={
        'customer': customer_id,
        'per_page': 100
    }).json()

    purchase_history = []

    for order in orders:
        purchase_history.append({
            'order_id': order['id'],
            'date': pd.to_datetime(order['date_created']),
            'status': order['status'],
            'total': float(order['total']),
            'items': [
                {
                    'name': item['name'],
                    'quantity': item['quantity'],
                    'price': float(item['price'])
                }
                for item in order.get('line_items', [])
            ]
        })

    df = pd.DataFrame(purchase_history)

    # Calculate metrics
    if len(df) > 0:
        metrics = {
            'total_orders': len(df),
            'total_spent': df['total'].sum(),
            'avg_order_value': df['total'].mean(),
            'first_purchase': df['date'].min(),
            'last_purchase': df['date'].max(),
            'purchase_frequency_days': (df['date'].max() - df['date'].min()).days / max(len(df) - 1, 1)
        }
    else:
        metrics = {}

    return metrics, df

# Customer segmentation for targeting
def segment_customers_for_campaigns():
    """Create customer segments for targeted marketing"""
    ltv_metrics, customers_df = calculate_customer_ltv(min_orders=1)

    segments = {
        'vip_customers': customers_df[
            (customers_df['total_spent'] > 1000) &
            (customers_df['orders_count'] >= 5)
        ],
        'at_risk_customers': customers_df[
            (customers_df['total_spent'] > 500) &
            (customers_df['days_since_signup'] > 90) &
            (customers_df['orders_count'] == 1)
        ],
        'new_customers': customers_df[
            customers_df['days_since_signup'] <= 30
        ],
        'frequent_buyers': customers_df[
            (customers_df['orders_count'] >= 5) &
            (customers_df['monthly_value'] > 50)
        ]
    }

    # Export segments for email campaigns
    segment_summary = {
        name: {
            'count': len(segment),
            'total_value': segment['total_spent'].sum(),
            'avg_ltv': segment['total_spent'].mean()
        }
        for name, segment in segments.items()
    }

    return segments, segment_summary

# Example usage
ltv_metrics, customers_df = calculate_customer_ltv()
print(f"Customer Metrics:")
print(f"  Total Customers: {ltv_metrics['total_customers']}")
print(f"  Average LTV: ${ltv_metrics['average_ltv']:,.2f}")
print(f"  Repeat Rate: {ltv_metrics['repeat_rate']:.1f}%")

segments, summary = segment_customers_for_campaigns()
print(f"\nCustomer Segments:")
for name, stats in summary.items():
    print(f"  {name}: {stats['count']} customers, ${stats['total_value']:,.2f} total value")
```

### 3. Product Management and Performance

```python
# Product performance analysis
def analyze_product_performance(days=90):
    """Comprehensive product analytics"""
    start_date = datetime.now() - timedelta(days=days)
    orders = get_orders(start_date=start_date, status='completed')

    product_sales = {}

    for order in orders:
        for item in order.get('line_items', []):
            product_id = item['product_id']

            if product_id not in product_sales:
                product_sales[product_id] = {
                    'name': item['name'],
                    'sku': item.get('sku', 'N/A'),
                    'quantity_sold': 0,
                    'revenue': 0,
                    'orders': 0,
                    'total_cost': 0
                }

            qty = item['quantity']
            price = float(item['price'])
            total = float(item['total'])

            product_sales[product_id]['quantity_sold'] += qty
            product_sales[product_id]['revenue'] += total
            product_sales[product_id]['orders'] += 1

    df = pd.DataFrame.from_dict(product_sales, orient='index')
    df = df.sort_values('revenue', ascending=False)

    df['avg_price'] = df['revenue'] / df['quantity_sold']
    df['avg_quantity_per_order'] = df['quantity_sold'] / df['orders']
    df['revenue_percent'] = (df['revenue'] / df['revenue'].sum() * 100).round(2)

    # ABC analysis
    df['cumulative_revenue_percent'] = df['revenue_percent'].cumsum()
    df['abc_category'] = df['cumulative_revenue_percent'].apply(
        lambda x: 'A' if x <= 80 else 'B' if x <= 95 else 'C'
    )

    return df

# Get product inventory and stock levels
def get_product_inventory():
    """Monitor product inventory for restocking"""
    products = []
    page = 1
    per_page = 100

    while True:
        response = wcapi.get("products", params={
            'per_page': per_page,
            'page': page,
            'status': 'publish'
        }).json()

        if not response:
            break

        products.extend(response)
        page += 1

        if len(response) < per_page:
            break

    inventory_data = []

    for product in products:
        inventory_data.append({
            'product_id': product['id'],
            'name': product['name'],
            'sku': product.get('sku', ''),
            'price': float(product.get('price', 0)),
            'regular_price': float(product.get('regular_price', 0)),
            'stock_quantity': product.get('stock_quantity'),
            'stock_status': product.get('stock_status', 'instock'),
            'manage_stock': product.get('manage_stock', False),
            'categories': ', '.join([cat['name'] for cat in product.get('categories', [])]),
            'total_sales': product.get('total_sales', 0)
        })

    df = pd.DataFrame(inventory_data)

    # Flag items needing attention
    df['needs_restock'] = (
        (df['stock_quantity'].notna()) &
        (df['stock_quantity'] < 10) &
        (df['stock_quantity'] > 0)
    )
    df['out_of_stock'] = df['stock_status'] == 'outofstock'

    return df

# Product category performance
def analyze_category_performance(days=90):
    """Analyze sales by product category"""
    start_date = datetime.now() - timedelta(days=days)
    orders = get_orders(start_date=start_date, status='completed')

    # Get product categories
    products_response = wcapi.get("products", params={'per_page': 100}).json()
    product_categories = {
        p['id']: ', '.join([cat['name'] for cat in p.get('categories', [])])
        for p in products_response
    }

    category_sales = {}

    for order in orders:
        for item in order.get('line_items', []):
            categories = product_categories.get(item['product_id'], 'Uncategorized')

            for category in categories.split(', '):
                if category not in category_sales:
                    category_sales[category] = {
                        'revenue': 0,
                        'quantity': 0,
                        'orders': 0
                    }

                category_sales[category]['revenue'] += float(item['total'])
                category_sales[category]['quantity'] += item['quantity']
                category_sales[category]['orders'] += 1

    df = pd.DataFrame.from_dict(category_sales, orient='index')
    df = df.sort_values('revenue', ascending=False)
    df['avg_order_value'] = df['revenue'] / df['orders']

    return df

# Example usage
product_performance = analyze_product_performance(days=90)
print("Top 10 Products by Revenue:")
print(product_performance.head(10)[['name', 'quantity_sold', 'revenue', 'revenue_percent']])

inventory = get_product_inventory()
print(f"\nInventory Status:")
print(f"  Low Stock Items: {inventory['needs_restock'].sum()}")
print(f"  Out of Stock: {inventory['out_of_stock'].sum()}")
```

### 4. Marketing Campaign Analytics

```python
# Coupon performance analysis
def analyze_coupon_performance(days=90):
    """Analyze discount coupon effectiveness"""
    start_date = datetime.now() - timedelta(days=days)
    orders = get_orders(start_date=start_date, status='completed')

    coupon_data = []

    for order in orders:
        coupons = order.get('coupon_lines', [])
        if coupons:
            for coupon in coupons:
                coupon_data.append({
                    'code': coupon.get('code', ''),
                    'discount': float(coupon.get('discount', 0)),
                    'order_total': float(order['total']),
                    'order_subtotal': float(order.get('cart_subtotal', 0)),
                    'order_date': pd.to_datetime(order['date_created'])
                })

    if not coupon_data:
        return None

    df = pd.DataFrame(coupon_data)

    # Calculate coupon performance
    performance = df.groupby('code').agg({
        'discount': ['sum', 'mean', 'count'],
        'order_total': 'sum',
        'order_subtotal': 'sum'
    }).round(2)

    performance.columns = ['total_discount', 'avg_discount', 'usage_count', 'revenue', 'gross_revenue']
    performance['discount_rate'] = (
        performance['total_discount'] / performance['gross_revenue'] * 100
    ).round(2)
    performance['revenue_per_use'] = (performance['revenue'] / performance['usage_count']).round(2)

    return performance.sort_values('usage_count', ascending=False)

# Cart abandonment analysis
def analyze_cart_abandonment():
    """Estimate cart abandonment rate"""
    # Note: WooCommerce doesn't track abandoned carts by default
    # This requires WooCommerce Recover Abandoned Cart plugin or similar

    # Get completed orders
    completed = get_orders(status='completed', per_page=100)

    # Get pending/failed orders (proxy for abandonment)
    pending = get_orders(status='pending', per_page=100)
    failed = get_orders(status='failed', per_page=100)

    abandoned_orders = pending + failed

    completed_revenue = sum(float(o['total']) for o in completed)
    abandoned_revenue = sum(float(o['total']) for o in abandoned_orders)

    metrics = {
        'completed_orders': len(completed),
        'abandoned_carts': len(abandoned_orders),
        'abandonment_rate': len(abandoned_orders) / (len(completed) + len(abandoned_orders)) * 100,
        'potential_recovery': abandoned_revenue,
        'completed_revenue': completed_revenue
    }

    # List high-value abandoned carts
    abandoned_df = pd.DataFrame([
        {
            'order_id': o['id'],
            'customer_email': o.get('billing', {}).get('email', ''),
            'total': float(o['total']),
            'date': pd.to_datetime(o['date_created'])
        }
        for o in abandoned_orders
    ]).sort_values('total', ascending=False)

    return metrics, abandoned_df

# Marketing attribution
def analyze_utm_sources(days=30):
    """Analyze order sources via UTM parameters"""
    start_date = datetime.now() - timedelta(days=days)
    orders = get_orders(start_date=start_date, status='completed')

    # Extract UTM data from order meta
    source_data = []

    for order in orders:
        meta_data = {m['key']: m['value'] for m in order.get('meta_data', [])}

        source_data.append({
            'order_id': order['id'],
            'revenue': float(order['total']),
            'utm_source': meta_data.get('utm_source', 'direct'),
            'utm_medium': meta_data.get('utm_medium', 'none'),
            'utm_campaign': meta_data.get('utm_campaign', 'none')
        })

    df = pd.DataFrame(source_data)

    # Attribution analysis
    source_performance = df.groupby(['utm_source', 'utm_medium', 'utm_campaign']).agg({
        'revenue': 'sum',
        'order_id': 'count'
    }).rename(columns={'order_id': 'orders'}).sort_values('revenue', ascending=False)

    source_performance['avg_order_value'] = (
        source_performance['revenue'] / source_performance['orders']
    ).round(2)

    return source_performance

# Example usage
coupon_performance = analyze_coupon_performance(days=90)
if coupon_performance is not None:
    print("Coupon Performance:")
    print(coupon_performance.head(10))

abandonment_metrics, abandoned_carts = analyze_cart_abandonment()
print(f"\nCart Abandonment:")
print(f"  Rate: {abandonment_metrics['abandonment_rate']:.1f}%")
print(f"  Potential Recovery: ${abandonment_metrics['potential_recovery']:,.2f}")
```

## Installation

```bash
# Install WooCommerce Python library
uv pip install woocommerce

# Additional packages for analytics
uv pip install pandas numpy python-dateutil requests
```

## Authentication

### REST API Credentials

1. In WordPress Admin, go to WooCommerce > Settings > Advanced > REST API
2. Click "Add key"
3. Set Description, User, and Permissions (Read/Write)
4. Copy Consumer Key and Consumer Secret

```python
from woocommerce import API

wcapi = API(
    url="https://yourstore.com",
    consumer_key="ck_xxxxxxxxxxxxx",
    consumer_secret="cs_xxxxxxxxxxxxx",
    version="wc/v3",
    timeout=30
)

# Test connection
response = wcapi.get("products")
print(f"Status: {response.status_code}")
```

### Authentication Methods

```python
# Standard authentication
wcapi = API(
    url="https://example.com",
    consumer_key="ck_xxxxx",
    consumer_secret="cs_xxxxx",
    version="wc/v3"
)

# With query string auth (for non-HTTPS)
wcapi = API(
    url="http://example.com",
    consumer_key="ck_xxxxx",
    consumer_secret="cs_xxxxx",
    version="wc/v3",
    query_string_auth=True
)
```

## Quick Start

```python
from woocommerce import API
import pandas as pd

# Initialize API
wcapi = API(
    url="https://yourstore.com",
    consumer_key="ck_xxxxx",
    consumer_secret="cs_xxxxx",
    version="wc/v3"
)

# Get recent orders
orders = wcapi.get("orders", params={'per_page': 10}).json()

print(f"Recent Orders: {len(orders)}")
for order in orders:
    print(f"Order #{order['number']}: ${order['total']} - {order['status']}")

# Get products
products = wcapi.get("products", params={'per_page': 5}).json()

for product in products:
    print(f"{product['name']}: ${product['price']} - Stock: {product.get('stock_quantity', 'N/A')}")

# Get customers
customers = wcapi.get("customers", params={'per_page': 5}).json()

for customer in customers:
    print(f"{customer['email']}: {customer['orders_count']} orders, ${customer['total_spent']} spent")
```

## Key Metrics Reference

### Revenue Metrics
- **Gross Revenue**: Sum of all order subtotals (before discounts/shipping)
- **Net Revenue**: Total revenue after discounts
- **Average Order Value (AOV)**: Total revenue / orders
- **Revenue Per Customer**: Total revenue / unique customers

### Customer Metrics
- **Customer Lifetime Value (LTV)**: Total spend per customer
- **Repeat Purchase Rate**: Customers with 2+ orders / total
- **Average Orders Per Customer**: Total orders / unique customers
- **Customer Retention Rate**: Returning customers / total customers

### Product Metrics
- **Units Sold**: Total quantity sold
- **Revenue Per Product**: Sales by product
- **Sell-Through Rate**: Units sold / units available
- **ABC Classification**: A (80% revenue), B (15%), C (5%)

### Marketing Metrics
- **Coupon Redemption Rate**: Coupons used / coupons created
- **Discount Impact**: Revenue with discounts / total revenue
- **Cart Abandonment Rate**: Abandoned carts / total carts
- **Attribution Revenue**: Revenue by traffic source

## References

- [WooCommerce REST API Documentation](https://woocommerce.github.io/woocommerce-rest-api-docs/)
- [WooCommerce Python Client](https://github.com/woocommerce/wc-api-python)
- [WooCommerce Analytics](https://woocommerce.com/document/woocommerce-analytics/)
- [WooCommerce Reports API](https://woocommerce.github.io/woocommerce-rest-api-docs/#reports)
- [WooCommerce Webhooks](https://woocommerce.github.io/woocommerce-rest-api-docs/#webhooks)

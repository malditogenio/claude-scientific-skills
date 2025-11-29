---
name: bigcommerce
description: "BigCommerce e-commerce platform API. Access store orders, customers, products, analytics. Track sales metrics, customer lifetime value, revenue optimization, marketing attribution."
---

# BigCommerce Integration

## Overview

BigCommerce is a leading SaaS e-commerce platform serving mid-market and enterprise retailers. This skill covers using the BigCommerce API to analyze store performance, track customer behavior, optimize product catalogs, and execute data-driven marketing strategies for revenue growth.

## When to Use This Skill

- E-commerce store analytics and KPI tracking
- Customer lifetime value and segmentation analysis
- Product performance and inventory optimization
- Order management and fulfillment tracking
- Marketing attribution and campaign ROI
- Multi-channel sales analytics
- Abandoned cart recovery campaigns
- Subscription revenue tracking

## Core Capabilities

### 1. Order Management and Analytics

```python
import requests
import pandas as pd
from datetime import datetime, timedelta

# BigCommerce API Configuration
STORE_HASH = "your_store_hash"
ACCESS_TOKEN = "your_access_token"
API_VERSION = "v2"
BASE_URL = f"https://api.bigcommerce.com/stores/{STORE_HASH}/{API_VERSION}"

headers = {
    'X-Auth-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Get orders with filtering
def get_orders(min_date_created=None, status_id=None, limit=250):
    """Fetch orders from BigCommerce"""
    url = f"{BASE_URL}/orders"

    params = {
        'limit': limit,
        'sort': 'date_created:desc'
    }

    if min_date_created:
        params['min_date_created'] = min_date_created.strftime('%a, %d %b %Y %H:%M:%S %z')

    if status_id:
        params['status_id'] = status_id

    all_orders = []
    page = 1

    while True:
        params['page'] = page
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            break

        orders = response.json()

        if not orders:
            break

        all_orders.extend(orders)

        if len(orders) < limit:
            break

        page += 1

    return all_orders

# Calculate revenue metrics
def calculate_revenue_metrics(days=30):
    """Comprehensive revenue analysis"""
    min_date = datetime.now() - timedelta(days=days)
    orders = get_orders(min_date_created=min_date)

    order_data = []
    for order in orders:
        order_data.append({
            'order_id': order['id'],
            'date_created': pd.to_datetime(order['date_created']),
            'status': order['status'],
            'status_id': order['status_id'],
            'subtotal_ex_tax': float(order['subtotal_ex_tax']),
            'subtotal_inc_tax': float(order['subtotal_inc_tax']),
            'total_ex_tax': float(order['total_ex_tax']),
            'total_inc_tax': float(order['total_inc_tax']),
            'shipping_cost_ex_tax': float(order['shipping_cost_ex_tax']),
            'discount_amount': float(order['discount_amount']),
            'coupon_discount': float(order['coupon_discount']),
            'customer_id': order.get('customer_id', 0),
            'items_total': order['items_total'],
            'payment_method': order.get('payment_method', 'unknown')
        })

    df = pd.DataFrame(order_data)
    df['date'] = df['date_created'].dt.date

    # Calculate metrics
    metrics = {
        'total_revenue': df['total_inc_tax'].sum(),
        'gross_revenue': df['subtotal_inc_tax'].sum(),
        'net_revenue': df['total_inc_tax'].sum() - df['discount_amount'].sum(),
        'total_orders': len(df),
        'average_order_value': df['total_inc_tax'].mean(),
        'median_order_value': df['total_inc_tax'].median(),
        'total_shipping': df['shipping_cost_ex_tax'].sum(),
        'total_discounts': df['discount_amount'].sum(),
        'coupon_discounts': df['coupon_discount'].sum(),
        'unique_customers': df[df['customer_id'] > 0]['customer_id'].nunique(),
        'avg_items_per_order': df['items_total'].mean(),
        'orders_by_status': df['status'].value_counts().to_dict(),
        'payment_method_distribution': df['payment_method'].value_counts().to_dict()
    }

    # Daily trends
    daily_stats = df.groupby('date').agg({
        'total_inc_tax': ['sum', 'mean', 'count'],
        'customer_id': 'nunique'
    })

    return metrics, df, daily_stats

# Get order products for detailed analysis
def get_order_products(order_id):
    """Get products for a specific order"""
    url = f"{BASE_URL}/orders/{order_id}/products"

    response = requests.get(url, headers=headers)
    return response.json()

# Revenue trends and forecasting
def analyze_revenue_trends(months=6):
    """Analyze monthly revenue trends and growth"""
    min_date = datetime.now() - timedelta(days=30*months)
    orders = get_orders(min_date_created=min_date)

    order_data = []
    for order in orders:
        order_data.append({
            'date': pd.to_datetime(order['date_created']),
            'revenue': float(order['total_inc_tax'])
        })

    df = pd.DataFrame(order_data)
    df['month'] = df['date'].dt.to_period('M')

    monthly_stats = df.groupby('month').agg({
        'revenue': ['sum', 'mean', 'count']
    }).round(2)

    monthly_stats.columns = ['total_revenue', 'avg_order_value', 'order_count']

    # Calculate month-over-month growth
    monthly_stats['mom_growth'] = monthly_stats['total_revenue'].pct_change() * 100

    return monthly_stats

# Example usage
metrics, orders_df, daily_stats = calculate_revenue_metrics(days=30)
print(f"30-Day Performance:")
print(f"  Total Revenue: ${metrics['total_revenue']:,.2f}")
print(f"  Net Revenue: ${metrics['net_revenue']:,.2f}")
print(f"  Orders: {metrics['total_orders']}")
print(f"  AOV: ${metrics['average_order_value']:,.2f}")
print(f"  Unique Customers: {metrics['unique_customers']}")
```

### 2. Customer Data and Lifetime Value

```python
# Get customers
def get_customers(limit=250):
    """Fetch customer data from BigCommerce"""
    url = f"{BASE_URL}/customers"

    params = {
        'limit': limit,
        'sort': 'date_created:desc'
    }

    all_customers = []
    page = 1

    while True:
        params['page'] = page
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            break

        customers = response.json()

        if not customers:
            break

        all_customers.extend(customers)

        if len(customers) < limit:
            break

        page += 1

    return all_customers

# Calculate customer lifetime value
def calculate_customer_ltv(lookback_days=365):
    """Analyze customer lifetime value and segments"""
    customers = get_customers()

    # Get orders
    min_date = datetime.now() - timedelta(days=lookback_days)
    orders = get_orders(min_date_created=min_date)

    # Build customer metrics
    customer_orders = {}

    for order in orders:
        customer_id = order.get('customer_id', 0)
        if customer_id == 0:
            continue

        if customer_id not in customer_orders:
            customer_orders[customer_id] = {
                'orders': [],
                'total_spent': 0,
                'order_count': 0
            }

        customer_orders[customer_id]['orders'].append({
            'date': pd.to_datetime(order['date_created']),
            'amount': float(order['total_inc_tax'])
        })
        customer_orders[customer_id]['total_spent'] += float(order['total_inc_tax'])
        customer_orders[customer_id]['order_count'] += 1

    # Build customer dataframe
    customer_data = []

    for customer in customers:
        customer_id = customer['id']
        order_data = customer_orders.get(customer_id, {
            'orders': [],
            'total_spent': 0,
            'order_count': 0
        })

        if order_data['order_count'] > 0:
            order_dates = [o['date'] for o in order_data['orders']]
            first_order = min(order_dates)
            last_order = max(order_dates)

            customer_data.append({
                'customer_id': customer_id,
                'email': customer['email'],
                'first_name': customer.get('first_name', ''),
                'last_name': customer.get('last_name', ''),
                'date_created': pd.to_datetime(customer['date_created']),
                'total_spent': order_data['total_spent'],
                'order_count': order_data['order_count'],
                'first_order_date': first_order,
                'last_order_date': last_order
            })

    df = pd.DataFrame(customer_data)

    if len(df) == 0:
        return {}, df

    # Calculate additional metrics
    df['avg_order_value'] = df['total_spent'] / df['order_count']
    df['customer_lifetime_days'] = (df['last_order_date'] - df['first_order_date']).dt.days
    df['days_since_last_order'] = (datetime.now() - df['last_order_date']).dt.days

    # RFM Segmentation
    df['recency_score'] = pd.qcut(df['days_since_last_order'], q=4, labels=[4,3,2,1], duplicates='drop')
    df['frequency_score'] = pd.qcut(df['order_count'], q=4, labels=[1,2,3,4], duplicates='drop')
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
        'repeat_rate': (df['order_count'] > 1).sum() / len(df) * 100,
        'avg_orders_per_customer': df['order_count'].mean(),
        'segment_distribution': df['segment'].value_counts().to_dict()
    }

    return ltv_metrics, df

# Customer address analysis
def get_customer_addresses(customer_id):
    """Get customer shipping addresses"""
    url = f"{BASE_URL}/customers/{customer_id}/addresses"

    response = requests.get(url, headers=headers)
    return response.json()

# Geographic customer distribution
def analyze_customer_geography():
    """Analyze customer distribution by location"""
    customers = get_customers()

    geo_data = []

    for customer in customers:
        # Get addresses for geographic analysis
        addresses = get_customer_addresses(customer['id'])

        for address in addresses:
            geo_data.append({
                'customer_id': customer['id'],
                'country': address.get('country', 'Unknown'),
                'state': address.get('state', 'Unknown'),
                'city': address.get('city', 'Unknown'),
                'zip': address.get('zip', '')
            })

    if not geo_data:
        return None

    df = pd.DataFrame(geo_data)

    # Geographic distribution
    country_dist = df.groupby('country').agg({
        'customer_id': 'nunique'
    }).rename(columns={'customer_id': 'customer_count'}).sort_values('customer_count', ascending=False)

    state_dist = df.groupby(['country', 'state']).agg({
        'customer_id': 'nunique'
    }).rename(columns={'customer_id': 'customer_count'}).sort_values('customer_count', ascending=False)

    return country_dist, state_dist

# Example usage
ltv_metrics, customers_df = calculate_customer_ltv(lookback_days=365)
print(f"Customer Metrics:")
print(f"  Total Customers: {ltv_metrics['total_customers']}")
print(f"  Average LTV: ${ltv_metrics['average_ltv']:,.2f}")
print(f"  Repeat Rate: {ltv_metrics['repeat_rate']:.1f}%")
print(f"\nCustomer Segments:")
for segment, count in ltv_metrics['segment_distribution'].items():
    print(f"  {segment}: {count} customers")
```

### 3. Product Management and Performance

```python
# Get products
def get_products(limit=250):
    """Fetch product catalog"""
    url = f"{BASE_URL}/products"

    params = {
        'limit': limit
    }

    all_products = []
    page = 1

    while True:
        params['page'] = page
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            break

        products = response.json()

        if not products:
            break

        all_products.extend(products)

        if len(products) < limit:
            break

        page += 1

    return all_products

# Product performance analysis
def analyze_product_performance(days=90):
    """Analyze product sales and revenue"""
    min_date = datetime.now() - timedelta(days=days)
    orders = get_orders(min_date_created=min_date)

    product_sales = {}

    for order in orders:
        # Get order products
        order_products = get_order_products(order['id'])

        for item in order_products:
            product_id = item['product_id']

            if product_id not in product_sales:
                product_sales[product_id] = {
                    'name': item['name'],
                    'sku': item.get('sku', ''),
                    'quantity_sold': 0,
                    'revenue': 0,
                    'orders': 0
                }

            product_sales[product_id]['quantity_sold'] += item['quantity']
            product_sales[product_id]['revenue'] += float(item['total_inc_tax'])
            product_sales[product_id]['orders'] += 1

    df = pd.DataFrame.from_dict(product_sales, orient='index')
    df = df.sort_values('revenue', ascending=False)

    df['avg_price'] = df['revenue'] / df['quantity_sold']
    df['avg_quantity_per_order'] = df['quantity_sold'] / df['orders']
    df['revenue_percent'] = (df['revenue'] / df['revenue'].sum() * 100).round(2)

    # Pareto analysis (80/20 rule)
    df['cumulative_revenue_percent'] = df['revenue_percent'].cumsum()

    return df

# Get product inventory
def get_product_inventory():
    """Check inventory levels"""
    products = get_products()

    inventory_data = []

    for product in products:
        inventory_data.append({
            'product_id': product['id'],
            'name': product['name'],
            'sku': product['sku'],
            'price': float(product['price']),
            'sale_price': float(product.get('sale_price', 0)),
            'inventory_level': product.get('inventory_level', 0),
            'inventory_warning_level': product.get('inventory_warning_level', 0),
            'is_visible': product.get('is_visible', False),
            'total_sold': product.get('total_sold', 0)
        })

    df = pd.DataFrame(inventory_data)

    # Flag items needing attention
    df['low_stock'] = (
        (df['inventory_level'] > 0) &
        (df['inventory_level'] <= df['inventory_warning_level'])
    )
    df['out_of_stock'] = df['inventory_level'] == 0

    return df

# Product category performance
def analyze_category_performance(days=90):
    """Analyze sales by category"""
    # Get products with categories
    products = get_products()

    product_categories = {}
    for product in products:
        product_categories[product['id']] = product.get('categories', [])

    # Get orders
    min_date = datetime.now() - timedelta(days=days)
    orders = get_orders(min_date_created=min_date)

    category_sales = {}

    for order in orders:
        order_products = get_order_products(order['id'])

        for item in order_products:
            categories = product_categories.get(item['product_id'], [])

            for category_id in categories:
                if category_id not in category_sales:
                    category_sales[category_id] = {
                        'revenue': 0,
                        'quantity': 0,
                        'orders': 0
                    }

                category_sales[category_id]['revenue'] += float(item['total_inc_tax'])
                category_sales[category_id]['quantity'] += item['quantity']
                category_sales[category_id]['orders'] += 1

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
print(f"  Low Stock: {inventory['low_stock'].sum()}")
print(f"  Out of Stock: {inventory['out_of_stock'].sum()}")
```

### 4. Marketing Campaign Analytics

```python
# Analyze coupon usage
def analyze_coupon_performance(days=90):
    """Track coupon code effectiveness"""
    min_date = datetime.now() - timedelta(days=days)
    orders = get_orders(min_date_created=min_date)

    coupon_data = []

    for order in orders:
        if float(order['coupon_discount']) > 0:
            # Get coupon details from order
            url = f"{BASE_URL}/orders/{order['id']}/coupons"
            response = requests.get(url, headers=headers)
            coupons = response.json()

            for coupon in coupons:
                coupon_data.append({
                    'code': coupon.get('code', 'Unknown'),
                    'discount': float(coupon.get('discount', 0)),
                    'order_total': float(order['total_inc_tax']),
                    'subtotal': float(order['subtotal_inc_tax']),
                    'order_date': pd.to_datetime(order['date_created'])
                })

    if not coupon_data:
        return None

    df = pd.DataFrame(coupon_data)

    performance = df.groupby('code').agg({
        'discount': ['sum', 'mean', 'count'],
        'order_total': 'sum',
        'subtotal': 'sum'
    }).round(2)

    performance.columns = ['total_discount', 'avg_discount', 'usage_count', 'revenue', 'gross_revenue']
    performance['discount_rate'] = (
        performance['total_discount'] / performance['gross_revenue'] * 100
    ).round(2)
    performance['roi'] = (performance['revenue'] / performance['total_discount']).round(2)

    return performance.sort_values('usage_count', ascending=False)

# Abandoned cart analysis (using BigCommerce V3 API)
def analyze_abandoned_carts():
    """Analyze abandoned carts for recovery"""
    # Note: Requires V3 API
    v3_url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/carts"

    params = {
        'include': 'line_items.physical_items.options'
    }

    response = requests.get(v3_url, headers=headers, params=params)
    carts = response.json().get('data', [])

    abandoned_data = []

    for cart in carts:
        # Check if cart is abandoned (no recent orders)
        customer_id = cart.get('customer_id')
        email = cart.get('email')

        abandoned_data.append({
            'cart_id': cart['id'],
            'customer_id': customer_id,
            'email': email,
            'cart_value': float(cart.get('cart_amount', 0)),
            'currency': cart.get('currency', {}).get('code', 'USD'),
            'created_time': pd.to_datetime(cart.get('created_time')),
            'updated_time': pd.to_datetime(cart.get('updated_time')),
            'items_count': len(cart.get('line_items', {}).get('physical_items', []))
        })

    if not abandoned_data:
        return None

    df = pd.DataFrame(abandoned_data)
    df['days_abandoned'] = (datetime.now() - df['updated_time']).dt.days

    metrics = {
        'total_abandoned': len(df),
        'total_value': df['cart_value'].sum(),
        'avg_cart_value': df['cart_value'].mean(),
        'recovery_potential': df[df['days_abandoned'] <= 7]['cart_value'].sum()
    }

    return metrics, df

# Channel attribution
def analyze_sales_channels(days=30):
    """Analyze order source attribution"""
    min_date = datetime.now() - timedelta(days=days)
    orders = get_orders(min_date_created=min_date)

    channel_data = []

    for order in orders:
        # BigCommerce tracks order source
        channel_data.append({
            'channel_id': order.get('order_source', 'direct'),
            'revenue': float(order['total_inc_tax']),
            'order_id': order['id']
        })

    df = pd.DataFrame(channel_data)

    channel_performance = df.groupby('channel_id').agg({
        'revenue': 'sum',
        'order_id': 'count'
    }).rename(columns={'order_id': 'orders'})

    channel_performance['avg_order_value'] = (
        channel_performance['revenue'] / channel_performance['orders']
    ).round(2)

    channel_performance['revenue_percent'] = (
        channel_performance['revenue'] / channel_performance['revenue'].sum() * 100
    ).round(2)

    return channel_performance.sort_values('revenue', ascending=False)

# Example usage
coupon_performance = analyze_coupon_performance(days=90)
if coupon_performance is not None:
    print("Coupon Performance:")
    print(coupon_performance.head(10))

abandoned_metrics, abandoned_carts = analyze_abandoned_carts()
if abandoned_metrics:
    print(f"\nAbandoned Carts:")
    print(f"  Total: {abandoned_metrics['total_abandoned']}")
    print(f"  Potential Value: ${abandoned_metrics['total_value']:,.2f}")
```

## Installation

```bash
# Install required packages
uv pip install requests pandas python-dateutil pytz
```

## Authentication

### API Credentials

1. In BigCommerce Control Panel, go to Advanced Settings > API Accounts
2. Create API Account
3. Set OAuth Scopes (Orders, Products, Customers, etc.)
4. Copy Store Hash, Client ID, Access Token

```python
import requests

# API Configuration
STORE_HASH = "abc123xyz"
ACCESS_TOKEN = "your_access_token"
BASE_URL = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v2"

headers = {
    'X-Auth-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Test connection
response = requests.get(f"{BASE_URL}/store", headers=headers)
print(f"Store Info: {response.json()}")
```

## Quick Start

```python
import requests
import pandas as pd

# Configuration
STORE_HASH = "your_store_hash"
ACCESS_TOKEN = "your_access_token"
BASE_URL = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v2"

headers = {
    'X-Auth-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

# Get recent orders
response = requests.get(
    f"{BASE_URL}/orders",
    headers=headers,
    params={'limit': 10, 'sort': 'date_created:desc'}
)

orders = response.json()

print(f"Recent Orders: {len(orders)}")
for order in orders:
    print(f"Order #{order['id']}: ${order['total_inc_tax']} - {order['status']}")

# Get products
response = requests.get(
    f"{BASE_URL}/products",
    headers=headers,
    params={'limit': 5}
)

products = response.json()

for product in products:
    print(f"{product['name']}: ${product['price']}")
```

## Key Metrics Reference

### Revenue Metrics
- **Total Revenue**: Sum of all order totals (inc tax)
- **Gross Revenue**: Revenue before discounts
- **Net Revenue**: Revenue after all discounts
- **Average Order Value (AOV)**: Total revenue / orders

### Customer Metrics
- **Customer Lifetime Value (LTV)**: Total customer spend
- **RFM Score**: Recency + Frequency + Monetary
- **Repeat Purchase Rate**: Customers with 2+ orders
- **Customer Segments**: Champions, Loyal, Potential, At Risk

### Product Metrics
- **Revenue Per Product**: Sales by SKU
- **Units Sold**: Quantity sold by product
- **Sell-Through Rate**: Sold / available inventory
- **Low Stock Alert**: Below warning level

### Marketing Metrics
- **Coupon ROI**: Revenue generated / discount given
- **Abandoned Cart Rate**: Abandoned / total carts
- **Cart Recovery Value**: Potential revenue from abandoned carts
- **Channel Attribution**: Revenue by traffic source

## References

- [BigCommerce API Documentation](https://developer.bigcommerce.com/api-docs)
- [Orders API Reference](https://developer.bigcommerce.com/api-reference/store-management/orders)
- [Customers API Reference](https://developer.bigcommerce.com/api-reference/store-management/customers-v2)
- [Products API Reference](https://developer.bigcommerce.com/api-reference/store-management/catalog/products)
- [BigCommerce API Authentication](https://developer.bigcommerce.com/api-docs/getting-started/authentication)

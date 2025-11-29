---
name: magento
description: "Magento/Adobe Commerce GraphQL and REST API integration. Enterprise e-commerce platform for orders, customers, catalog management, analytics, revenue optimization."
---

# Magento/Adobe Commerce Integration

## Overview

Magento (Adobe Commerce) is an enterprise-grade e-commerce platform powering large-scale online stores. This skill covers using both the GraphQL and REST APIs to analyze sales data, manage customer relationships, optimize product catalogs, and drive revenue growth through data-driven marketing strategies.

## When to Use This Skill

- Enterprise e-commerce analytics and reporting
- Multi-store and multi-channel sales tracking
- Advanced customer segmentation and personalization
- Complex product catalog management
- B2B and B2C order management
- Customer lifetime value optimization
- Marketing attribution and campaign ROI
- Inventory management across warehouses

## Core Capabilities

### 1. Order Management and Analytics

```python
import requests
import pandas as pd
from datetime import datetime, timedelta
import json

# Magento API Configuration
BASE_URL = "https://yourstore.com/rest/V1"
ADMIN_TOKEN = "your-admin-token"

headers = {
    'Authorization': f'Bearer {ADMIN_TOKEN}',
    'Content-Type': 'application/json'
}

# Get orders with search criteria
def get_orders(start_date=None, status=None, page_size=100):
    """Fetch orders using REST API"""
    url = f"{BASE_URL}/orders"

    search_criteria = []

    if start_date:
        search_criteria.append({
            'field': 'created_at',
            'value': start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'condition_type': 'gteq'
        })

    if status:
        search_criteria.append({
            'field': 'status',
            'value': status,
            'condition_type': 'eq'
        })

    params = {
        'searchCriteria[pageSize]': page_size,
        'searchCriteria[currentPage]': 1
    }

    # Add filter groups
    for idx, criteria in enumerate(search_criteria):
        params[f'searchCriteria[filter_groups][0][filters][{idx}][field]'] = criteria['field']
        params[f'searchCriteria[filter_groups][0][filters][{idx}][value]'] = criteria['value']
        params[f'searchCriteria[filter_groups][0][filters][{idx}][condition_type]'] = criteria['condition_type']

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Calculate revenue metrics
def calculate_revenue_metrics(days=30):
    """Comprehensive revenue analysis"""
    start_date = datetime.now() - timedelta(days=days)
    result = get_orders(start_date=start_date)

    orders = result.get('items', [])

    order_data = []
    for order in orders:
        order_data.append({
            'order_id': order['entity_id'],
            'increment_id': order['increment_id'],
            'created_at': pd.to_datetime(order['created_at']),
            'status': order['status'],
            'state': order['state'],
            'grand_total': float(order['grand_total']),
            'subtotal': float(order['subtotal']),
            'tax_amount': float(order.get('tax_amount', 0)),
            'shipping_amount': float(order.get('shipping_amount', 0)),
            'discount_amount': abs(float(order.get('discount_amount', 0))),
            'customer_id': order.get('customer_id'),
            'customer_email': order.get('customer_email'),
            'items_count': len(order.get('items', [])),
            'store_id': order.get('store_id')
        })

    df = pd.DataFrame(order_data)
    df['date'] = df['created_at'].dt.date

    # Calculate comprehensive metrics
    metrics = {
        'total_revenue': df['grand_total'].sum(),
        'gross_revenue': df['subtotal'].sum(),
        'net_revenue': df['grand_total'].sum() - df['discount_amount'].sum(),
        'total_orders': len(df),
        'average_order_value': df['grand_total'].mean(),
        'median_order_value': df['grand_total'].median(),
        'total_tax': df['tax_amount'].sum(),
        'total_shipping': df['shipping_amount'].sum(),
        'total_discounts': df['discount_amount'].sum(),
        'unique_customers': df['customer_id'].nunique(),
        'orders_by_status': df['status'].value_counts().to_dict(),
        'revenue_by_store': df.groupby('store_id')['grand_total'].sum().to_dict()
    }

    # Daily trends
    daily_stats = df.groupby('date').agg({
        'grand_total': ['sum', 'mean', 'count'],
        'customer_id': 'nunique'
    })

    return metrics, df, daily_stats

# Using GraphQL for complex queries
def get_orders_graphql(days=30):
    """Fetch orders using GraphQL for more efficient queries"""
    graphql_url = f"{BASE_URL.replace('/rest/V1', '')}/graphql"

    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    query = """
    query {
        customer {
            orders(filter: {created_at: {from: "%s"}}) {
                items {
                    order_number
                    created_at
                    grand_total
                    status
                    items {
                        product_name
                        quantity_ordered
                        product_sale_price {
                            value
                        }
                    }
                    total {
                        grand_total {
                            value
                            currency
                        }
                        subtotal {
                            value
                        }
                        taxes {
                            amount {
                                value
                            }
                        }
                    }
                }
            }
        }
    }
    """ % start_date

    response = requests.post(
        graphql_url,
        json={'query': query},
        headers={'Authorization': f'Bearer {ADMIN_TOKEN}'}
    )

    return response.json()

# Sales by payment method
def analyze_payment_methods(days=30):
    """Analyze revenue by payment method"""
    start_date = datetime.now() - timedelta(days=days)
    result = get_orders(start_date=start_date)

    payment_data = []

    for order in result.get('items', []):
        payment = order.get('payment', {})
        payment_data.append({
            'method': payment.get('method', 'unknown'),
            'revenue': float(order['grand_total']),
            'order_id': order['entity_id']
        })

    df = pd.DataFrame(payment_data)

    payment_stats = df.groupby('method').agg({
        'revenue': ['sum', 'mean', 'count']
    }).round(2)

    payment_stats.columns = ['total_revenue', 'avg_order_value', 'order_count']
    payment_stats['revenue_percent'] = (
        payment_stats['total_revenue'] / payment_stats['total_revenue'].sum() * 100
    ).round(2)

    return payment_stats.sort_values('total_revenue', ascending=False)

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
# Get customer data
def get_customers(page_size=100):
    """Fetch customer data with orders"""
    url = f"{BASE_URL}/customers/search"

    params = {
        'searchCriteria[pageSize]': page_size,
        'searchCriteria[currentPage]': 1
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Calculate customer lifetime value
def calculate_customer_ltv():
    """Calculate LTV and segment customers"""
    customers_result = get_customers(page_size=250)
    customers = customers_result.get('items', [])

    customer_data = []

    for customer in customers:
        # Get customer's orders
        order_result = get_orders()
        customer_orders = [
            o for o in order_result.get('items', [])
            if o.get('customer_id') == customer['id']
        ]

        if customer_orders:
            total_spent = sum(float(o['grand_total']) for o in customer_orders)
            order_count = len(customer_orders)

            first_order = min(customer_orders, key=lambda x: x['created_at'])
            last_order = max(customer_orders, key=lambda x: x['created_at'])

            customer_data.append({
                'customer_id': customer['id'],
                'email': customer['email'],
                'firstname': customer.get('firstname', ''),
                'lastname': customer.get('lastname', ''),
                'created_at': pd.to_datetime(customer['created_at']),
                'total_spent': total_spent,
                'order_count': order_count,
                'first_order_date': pd.to_datetime(first_order['created_at']),
                'last_order_date': pd.to_datetime(last_order['created_at']),
                'group_id': customer.get('group_id', 1),
                'store_id': customer.get('store_id', 1)
            })

    df = pd.DataFrame(customer_data)

    # Calculate additional metrics
    df['avg_order_value'] = df['total_spent'] / df['order_count']
    df['customer_lifetime_days'] = (df['last_order_date'] - df['first_order_date']).dt.days
    df['days_since_last_order'] = (datetime.now() - df['last_order_date']).dt.days

    # RFM Segmentation
    df['recency_score'] = pd.qcut(df['days_since_last_order'], q=5, labels=[5,4,3,2,1], duplicates='drop')
    df['frequency_score'] = pd.qcut(df['order_count'], q=5, labels=[1,2,3,4,5], duplicates='drop')
    df['monetary_score'] = pd.qcut(df['total_spent'], q=5, labels=[1,2,3,4,5], duplicates='drop')

    df['rfm_score'] = (
        df['recency_score'].astype(int) +
        df['frequency_score'].astype(int) +
        df['monetary_score'].astype(int)
    )

    # Segment labels
    df['segment'] = df['rfm_score'].apply(lambda x:
        'Champions' if x >= 13 else
        'Loyal Customers' if x >= 10 else
        'Potential Loyalists' if x >= 7 else
        'At Risk' if x >= 4 else
        'Lost'
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

# Customer cohort analysis
def cohort_analysis_magento(months=12):
    """Analyze customer retention by cohort"""
    start_date = datetime.now() - timedelta(days=30*months)
    result = get_orders(start_date=start_date)

    orders = result.get('items', [])

    cohort_data = []
    for order in orders:
        if order.get('customer_id'):
            cohort_data.append({
                'customer_id': order['customer_id'],
                'order_date': pd.to_datetime(order['created_at']),
                'revenue': float(order['grand_total'])
            })

    df = pd.DataFrame(cohort_data)

    # Cohort analysis
    df['cohort_month'] = df.groupby('customer_id')['order_date'].transform('min').dt.to_period('M')
    df['order_month'] = df['order_date'].dt.to_period('M')
    df['cohort_age'] = (df['order_month'] - df['cohort_month']).apply(lambda x: x.n)

    # Create cohort table
    cohort_counts = df.groupby(['cohort_month', 'cohort_age'])['customer_id'].nunique().unstack(fill_value=0)

    # Calculate retention rates
    cohort_size = cohort_counts.iloc[:, 0]
    retention = cohort_counts.divide(cohort_size, axis=0) * 100

    return retention.round(1)

# Example usage
ltv_metrics, customers_df = calculate_customer_ltv()
print(f"Customer Metrics:")
print(f"  Average LTV: ${ltv_metrics['average_ltv']:,.2f}")
print(f"  Repeat Rate: {ltv_metrics['repeat_rate']:.1f}%")
print(f"\nCustomer Segments:")
for segment, count in ltv_metrics['segment_distribution'].items():
    print(f"  {segment}: {count} customers")
```

### 3. Product Management and Catalog Analytics

```python
# Get product data
def get_products(page_size=100):
    """Fetch product catalog"""
    url = f"{BASE_URL}/products"

    params = {
        'searchCriteria[pageSize]': page_size,
        'searchCriteria[currentPage]': 1
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Product performance analysis
def analyze_product_performance(days=90):
    """Analyze product sales and profitability"""
    start_date = datetime.now() - timedelta(days=days)
    result = get_orders(start_date=start_date, status='complete')

    product_sales = {}

    for order in result.get('items', []):
        for item in order.get('items', []):
            if item.get('product_type') == 'simple':
                product_id = item['product_id']

                if product_id not in product_sales:
                    product_sales[product_id] = {
                        'sku': item.get('sku', ''),
                        'name': item.get('name', ''),
                        'quantity_sold': 0,
                        'revenue': 0,
                        'cost': 0,
                        'orders': set()
                    }

                qty = item.get('qty_ordered', 0)
                price = float(item.get('price', 0))
                row_total = float(item.get('row_total', 0))

                product_sales[product_id]['quantity_sold'] += qty
                product_sales[product_id]['revenue'] += row_total
                product_sales[product_id]['orders'].add(order['entity_id'])

    # Convert to DataFrame
    df_data = []
    for product_id, data in product_sales.items():
        df_data.append({
            'product_id': product_id,
            'sku': data['sku'],
            'name': data['name'],
            'quantity_sold': data['quantity_sold'],
            'revenue': data['revenue'],
            'order_count': len(data['orders'])
        })

    df = pd.DataFrame(df_data)
    df = df.sort_values('revenue', ascending=False)

    df['avg_price'] = df['revenue'] / df['quantity_sold']
    df['revenue_percent'] = (df['revenue'] / df['revenue'].sum() * 100).round(2)
    df['avg_units_per_order'] = df['quantity_sold'] / df['order_count']

    # ABC analysis
    df['cumulative_revenue_percent'] = df['revenue_percent'].cumsum()
    df['abc_category'] = df['cumulative_revenue_percent'].apply(
        lambda x: 'A' if x <= 80 else 'B' if x <= 95 else 'C'
    )

    return df

# Get inventory levels
def get_inventory_status():
    """Check stock levels across all products"""
    products_result = get_products(page_size=250)
    products = products_result.get('items', [])

    inventory_data = []

    for product in products:
        if product.get('type_id') == 'simple':
            # Get stock item
            stock_item = product.get('extension_attributes', {}).get('stock_item', {})

            inventory_data.append({
                'product_id': product['id'],
                'sku': product['sku'],
                'name': product['name'],
                'price': float(product.get('price', 0)),
                'qty': stock_item.get('qty', 0),
                'is_in_stock': stock_item.get('is_in_stock', False),
                'min_qty': stock_item.get('min_qty', 0),
                'notify_stock_qty': stock_item.get('notify_stock_qty', 0)
            })

    df = pd.DataFrame(inventory_data)

    # Flag items needing attention
    df['needs_restock'] = (df['qty'] < df['notify_stock_qty']) & (df['qty'] > 0)
    df['out_of_stock'] = ~df['is_in_stock']

    return df

# Category performance
def analyze_category_performance(days=90):
    """Analyze sales by product category"""
    products_result = get_products(page_size=250)
    products = products_result.get('items', [])

    # Map products to categories
    product_categories = {}
    for product in products:
        category_ids = product.get('custom_attributes', [])
        category_names = []

        for attr in category_ids:
            if attr.get('attribute_code') == 'category_ids':
                category_names = attr.get('value', [])

        product_categories[product['id']] = ', '.join(map(str, category_names)) if category_names else 'Uncategorized'

    # Get order items
    start_date = datetime.now() - timedelta(days=days)
    result = get_orders(start_date=start_date, status='complete')

    category_sales = {}

    for order in result.get('items', []):
        for item in order.get('items', []):
            categories = product_categories.get(item['product_id'], 'Uncategorized')

            if categories not in category_sales:
                category_sales[categories] = {
                    'revenue': 0,
                    'quantity': 0,
                    'orders': set()
                }

            category_sales[categories]['revenue'] += float(item.get('row_total', 0))
            category_sales[categories]['quantity'] += item.get('qty_ordered', 0)
            category_sales[categories]['orders'].add(order['entity_id'])

    df_data = []
    for category, data in category_sales.items():
        df_data.append({
            'category': category,
            'revenue': data['revenue'],
            'quantity': data['quantity'],
            'order_count': len(data['orders'])
        })

    df = pd.DataFrame(df_data).sort_values('revenue', ascending=False)
    df['avg_order_value'] = df['revenue'] / df['order_count']

    return df

# Example usage
product_performance = analyze_product_performance(days=90)
print("Top 10 Products:")
print(product_performance.head(10)[['name', 'quantity_sold', 'revenue', 'abc_category']])

inventory = get_inventory_status()
print(f"\nInventory Alerts:")
print(f"  Need Restocking: {inventory['needs_restock'].sum()}")
print(f"  Out of Stock: {inventory['out_of_stock'].sum()}")
```

### 4. Marketing and Campaign Analytics

```python
# Analyze coupon usage
def analyze_coupon_performance(days=90):
    """Track coupon code effectiveness"""
    start_date = datetime.now() - timedelta(days=days)
    result = get_orders(start_date=start_date)

    coupon_data = []

    for order in result.get('items', []):
        coupon_code = order.get('coupon_code')
        if coupon_code:
            coupon_data.append({
                'code': coupon_code,
                'discount': abs(float(order.get('discount_amount', 0))),
                'order_total': float(order['grand_total']),
                'subtotal': float(order['subtotal']),
                'order_date': pd.to_datetime(order['created_at'])
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

# Customer acquisition analysis
def analyze_customer_acquisition(months=6):
    """Track new customer acquisition trends"""
    start_date = datetime.now() - timedelta(days=30*months)

    customers_result = get_customers(page_size=500)
    customers = customers_result.get('items', [])

    new_customers = [
        c for c in customers
        if pd.to_datetime(c['created_at']) >= start_date
    ]

    acquisition_data = []
    for customer in new_customers:
        acquisition_data.append({
            'customer_id': customer['id'],
            'signup_date': pd.to_datetime(customer['created_at']),
            'email': customer['email'],
            'store_id': customer.get('store_id', 1)
        })

    df = pd.DataFrame(acquisition_data)
    df['month'] = df['signup_date'].dt.to_period('M')

    monthly_acquisition = df.groupby('month').agg({
        'customer_id': 'count',
        'store_id': 'nunique'
    }).rename(columns={'customer_id': 'new_customers'})

    return monthly_acquisition

# Multi-store performance comparison
def compare_store_performance(days=30):
    """Compare performance across multiple stores"""
    start_date = datetime.now() - timedelta(days=days)
    result = get_orders(start_date=start_date)

    store_data = []

    for order in result.get('items', []):
        store_data.append({
            'store_id': order.get('store_id', 1),
            'revenue': float(order['grand_total']),
            'order_id': order['entity_id'],
            'customer_id': order.get('customer_id')
        })

    df = pd.DataFrame(store_data)

    store_performance = df.groupby('store_id').agg({
        'revenue': 'sum',
        'order_id': 'count',
        'customer_id': 'nunique'
    }).rename(columns={'order_id': 'orders', 'customer_id': 'unique_customers'})

    store_performance['aov'] = (
        store_performance['revenue'] / store_performance['orders']
    ).round(2)
    store_performance['revenue_percent'] = (
        store_performance['revenue'] / store_performance['revenue'].sum() * 100
    ).round(2)

    return store_performance.sort_values('revenue', ascending=False)

# Example usage
coupon_performance = analyze_coupon_performance(days=90)
if coupon_performance is not None:
    print("Top Performing Coupons:")
    print(coupon_performance.head(10))

store_comparison = compare_store_performance(days=30)
print("\nStore Performance Comparison:")
print(store_comparison)
```

## Installation

```bash
# Install required packages
uv pip install requests pandas python-dateutil

# For GraphQL queries (optional)
uv pip install gql aiohttp
```

## Authentication

### Admin Token (REST API)

1. In Magento Admin, go to System > Integrations
2. Add New Integration
3. Set Name, Your Password, and API permissions
4. Activate and copy the Access Token

```python
import requests

BASE_URL = "https://yourstore.com/rest/V1"
ADMIN_TOKEN = "your_admin_token_here"

headers = {
    'Authorization': f'Bearer {ADMIN_TOKEN}',
    'Content-Type': 'application/json'
}

# Test connection
response = requests.get(f"{BASE_URL}/products?searchCriteria[pageSize]=1", headers=headers)
print(f"Status: {response.status_code}")
```

### Customer Token (For customer-specific operations)

```python
def get_customer_token(username, password):
    """Authenticate customer and get token"""
    url = f"{BASE_URL}/integration/customer/token"

    payload = {
        'username': username,
        'password': password
    }

    response = requests.post(url, json=payload)
    return response.json()

customer_token = get_customer_token('customer@example.com', 'password')
```

## Quick Start

```python
import requests
import pandas as pd

# Configuration
BASE_URL = "https://yourstore.com/rest/V1"
ADMIN_TOKEN = "your_token"

headers = {
    'Authorization': f'Bearer {ADMIN_TOKEN}',
    'Content-Type': 'application/json'
}

# Get recent orders
response = requests.get(
    f"{BASE_URL}/orders",
    headers=headers,
    params={'searchCriteria[pageSize]': 10}
)

orders = response.json()['items']

print(f"Recent Orders: {len(orders)}")
for order in orders[:5]:
    print(f"Order #{order['increment_id']}: ${order['grand_total']} - {order['status']}")

# Get products
response = requests.get(
    f"{BASE_URL}/products",
    headers=headers,
    params={'searchCriteria[pageSize]': 5}
)

products = response.json()['items']

for product in products:
    print(f"{product['name']}: ${product.get('price', 'N/A')}")
```

## Key Metrics Reference

### Revenue Metrics
- **Grand Total**: Final order amount including tax and shipping
- **Subtotal**: Order total before tax/shipping
- **Net Revenue**: Revenue after discounts
- **Average Order Value (AOV)**: Total revenue / orders

### Customer Metrics
- **Customer Lifetime Value (LTV)**: Total customer spend
- **RFM Score**: Recency + Frequency + Monetary combined score
- **Customer Segments**: Champions, Loyal, At Risk, Lost
- **Retention Rate**: Cohort-based customer retention

### Product Metrics
- **ABC Classification**: A (top 80%), B (next 15%), C (bottom 5%)
- **Units Sold**: Total quantity sold
- **Revenue Per SKU**: Sales by product
- **Stock Status**: In stock, low stock, out of stock

### Store Metrics
- **Multi-Store Revenue**: Revenue by store view
- **Store AOV**: Average order value by store
- **Store Contribution**: Revenue percentage by store

## References

- [Magento REST API Documentation](https://adobe-commerce.redoc.ly/2.4.6-admin/tag/orders)
- [Magento GraphQL API](https://developer.adobe.com/commerce/webapi/graphql/)
- [Magento API Authentication](https://developer.adobe.com/commerce/webapi/get-started/authentication/)
- [Adobe Commerce Developer Docs](https://developer.adobe.com/commerce/docs/)
- [Magento API Best Practices](https://developer.adobe.com/commerce/webapi/get-started/best-practices/)

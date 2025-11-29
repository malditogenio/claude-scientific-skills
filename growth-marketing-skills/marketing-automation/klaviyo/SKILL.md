---
name: klaviyo
description: "Klaviyo e-commerce email and SMS marketing platform. Customer data, segmentation, behavioral triggers, flows, campaigns, analytics, Shopify integration."
---

# Klaviyo Integration

## Overview

Klaviyo is an e-commerce-focused email and SMS marketing platform with powerful segmentation and automation capabilities. This skill covers using the Klaviyo API for customer data management, campaign creation, behavioral tracking, and analytics.

## When to Use This Skill

- E-commerce email and SMS marketing
- Customer behavior tracking and segmentation
- Abandoned cart recovery
- Product recommendation emails
- Customer lifecycle campaigns
- Revenue attribution and analytics
- Integration with Shopify, WooCommerce, Magento
- Personalized customer journeys

## Core Capabilities

### 1. Profile and Event Tracking

```python
import requests
import json
from datetime import datetime

# Klaviyo API configuration
PRIVATE_API_KEY = 'your-private-api-key'
PUBLIC_API_KEY = 'your-public-api-key'
BASE_URL = 'https://a.klaviyo.com/api'

headers = {
    'Authorization': f'Klaviyo-API-Key {PRIVATE_API_KEY}',
    'revision': '2024-10-15',
    'Content-Type': 'application/json'
}

# Create or update profile
def create_or_update_profile(email, properties):
    url = f'{BASE_URL}/profiles/'

    data = {
        'data': {
            'type': 'profile',
            'attributes': {
                'email': email,
                'properties': properties
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Track custom event
def track_event(email, event_name, properties=None, profile_properties=None):
    url = f'{BASE_URL}/events/'

    data = {
        'data': {
            'type': 'event',
            'attributes': {
                'profile': {
                    'data': {
                        'type': 'profile',
                        'attributes': {
                            'email': email,
                            'properties': profile_properties or {}
                        }
                    }
                },
                'metric': {
                    'data': {
                        'type': 'metric',
                        'attributes': {
                            'name': event_name
                        }
                    }
                },
                'properties': properties or {},
                'time': datetime.now().isoformat()
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example: Track product view
profile = create_or_update_profile(
    'customer@example.com',
    {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'total_orders': 5,
        'total_spent': 499.95
    }
)

# Track event
event = track_event(
    'customer@example.com',
    'Viewed Product',
    properties={
        'product_name': 'Premium Widget',
        'product_id': 'SKU-12345',
        'price': 99.99,
        'category': 'Electronics'
    }
)

print(f"Event tracked: {event}")

# Track e-commerce events
def track_placed_order(email, order_data):
    return track_event(
        email,
        'Placed Order',
        properties={
            'order_id': order_data['order_id'],
            'total': order_data['total'],
            'items': order_data['items'],
            'categories': order_data['categories']
        }
    )

def track_started_checkout(email, cart_data):
    return track_event(
        email,
        'Started Checkout',
        properties={
            'cart_total': cart_data['total'],
            'items': cart_data['items'],
            'checkout_url': cart_data['checkout_url']
        }
    )
```

### 2. List and Segment Management

```python
# Get all lists
def get_lists():
    url = f'{BASE_URL}/lists/'

    response = requests.get(url, headers=headers)
    return response.json()

# Create list
def create_list(list_name):
    url = f'{BASE_URL}/lists/'

    data = {
        'data': {
            'type': 'list',
            'attributes': {
                'name': list_name
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Add profile to list
def add_profile_to_list(list_id, profile_id):
    url = f'{BASE_URL}/lists/{list_id}/relationships/profiles/'

    data = {
        'data': [
            {
                'type': 'profile',
                'id': profile_id
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 204

# Create segment
def create_segment(name, definition):
    url = f'{BASE_URL}/segments/'

    data = {
        'data': {
            'type': 'segment',
            'attributes': {
                'name': name,
                'definition': definition
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example: Create high-value customer segment
high_value_segment = create_segment(
    'High Value Customers',
    {
        'type': 'profile-property',
        'property': 'total_spent',
        'operator': 'greater-than',
        'value': 500
    }
)

# Get segment profiles
def get_segment_profiles(segment_id):
    url = f'{BASE_URL}/segments/{segment_id}/profiles/'

    all_profiles = []
    params = {'page[size]': 100}

    while True:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        all_profiles.extend(data.get('data', []))

        next_page = data.get('links', {}).get('next')
        if not next_page:
            break

        url = next_page

    return all_profiles
```

### 3. Campaign Management

```python
# Create campaign
def create_campaign(name, subject, from_email, from_name, list_ids, template_id):
    url = f'{BASE_URL}/campaigns/'

    data = {
        'data': {
            'type': 'campaign',
            'attributes': {
                'name': name,
                'audiences': {
                    'included': [{'type': 'list', 'id': list_id} for list_id in list_ids]
                },
                'send_strategy': {
                    'method': 'immediate'
                },
                'campaign_messages': {
                    'data': [
                        {
                            'type': 'campaign-message',
                            'attributes': {
                                'channel': 'email',
                                'label': 'Email 1',
                                'content': {
                                    'subject': subject,
                                    'from_email': from_email,
                                    'from_name': from_name,
                                    'template_id': template_id
                                }
                            }
                        }
                    ]
                }
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Send campaign
def send_campaign(campaign_id):
    url = f'{BASE_URL}/campaigns/{campaign_id}/send/'

    response = requests.post(url, headers=headers)
    return response.json()

# Get campaign analytics
def get_campaign_analytics(campaign_id):
    url = f'{BASE_URL}/campaigns/{campaign_id}/'

    params = {
        'fields[campaign]': 'name,status,archived,audiences,send_strategy,send_time,created_at,updated_at',
        'include': 'campaign-messages'
    }

    response = requests.get(url, headers=headers, params=params)
    campaign_data = response.json()

    # Get message stats
    stats_url = f'{BASE_URL}/campaign-messages/{campaign_data["data"]["id"]}/stats/'
    stats_response = requests.get(stats_url, headers=headers)

    return {
        'campaign': campaign_data,
        'stats': stats_response.json()
    }

# Example usage
campaign = create_campaign(
    name='Summer Sale 2025',
    subject='50% Off Summer Collection',
    from_email='sales@example.com',
    from_name='Your Store',
    list_ids=['LIST_ID_1', 'LIST_ID_2'],
    template_id='TEMPLATE_ID'
)

print(f"Campaign created: {campaign['data']['id']}")
```

### 4. Flow (Automation) Management

```python
# Get all flows
def get_flows():
    url = f'{BASE_URL}/flows/'

    response = requests.get(url, headers=headers)
    return response.json()

# Get flow details
def get_flow(flow_id):
    url = f'{BASE_URL}/flows/{flow_id}/'

    params = {
        'include': 'flow-actions'
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Trigger flow for profile
def trigger_flow(flow_id, email, properties=None):
    # This typically happens automatically based on triggers
    # But you can manually enroll via profile updates
    return create_or_update_profile(email, properties or {})

# Get flow analytics
def get_flow_analytics(flow_id, start_date, end_date):
    url = f'{BASE_URL}/flows/{flow_id}/relationships/flow-actions/'

    response = requests.get(url, headers=headers)
    flow_actions = response.json()

    analytics = []
    for action in flow_actions.get('data', []):
        action_id = action['id']
        stats_url = f'{BASE_URL}/flow-actions/{action_id}/flow-message/'

        stats_response = requests.get(stats_url, headers=headers)
        analytics.append(stats_response.json())

    return analytics

# Example: Monitor abandoned cart flow
flows = get_flows()

for flow in flows.get('data', []):
    if 'abandoned' in flow['attributes']['name'].lower():
        flow_details = get_flow(flow['id'])
        print(f"Abandoned Cart Flow: {flow['attributes']['name']}")
        print(f"  Status: {flow['attributes']['status']}")
        print(f"  Actions: {len(flow_details.get('included', []))}")
```

### 5. Product and Catalog Sync

```python
# Create catalog item (product)
def create_catalog_item(catalog_type, external_id, title, price, url, image_url, metadata=None):
    url_endpoint = f'{BASE_URL}/catalog-items/'

    data = {
        'data': {
            'type': 'catalog-item',
            'attributes': {
                'external_id': external_id,
                'catalog_type': catalog_type,
                'title': title,
                'price': price,
                'url': url,
                'image_full_url': image_url,
                'custom_metadata': metadata or {}
            }
        }
    }

    response = requests.post(url_endpoint, headers=headers, json=data)
    return response.json()

# Update catalog item
def update_catalog_item(item_id, updates):
    url_endpoint = f'{BASE_URL}/catalog-items/{item_id}/'

    data = {
        'data': {
            'type': 'catalog-item',
            'id': item_id,
            'attributes': updates
        }
    }

    response = requests.patch(url_endpoint, headers=headers, json=data)
    return response.json()

# Sync product catalog
def sync_product_catalog(products):
    results = []

    for product in products:
        result = create_catalog_item(
            catalog_type='$default',
            external_id=product['sku'],
            title=product['name'],
            price=product['price'],
            url=product['url'],
            image_url=product['image'],
            metadata={
                'category': product.get('category'),
                'brand': product.get('brand'),
                'inventory': product.get('stock')
            }
        )
        results.append(result)

    return results

# Example: Sync products
products_to_sync = [
    {
        'sku': 'WIDGET-001',
        'name': 'Premium Widget',
        'price': 99.99,
        'url': 'https://store.com/widget-001',
        'image': 'https://store.com/images/widget.jpg',
        'category': 'Electronics',
        'brand': 'TechCo',
        'stock': 150
    }
]

sync_results = sync_product_catalog(products_to_sync)
print(f"Synced {len(sync_results)} products")
```

### 6. Metrics and Analytics

```python
import pandas as pd
from datetime import timedelta

# Get metric aggregate
def get_metric_aggregate(metric_id, start_date, end_date):
    url = f'{BASE_URL}/metric-aggregates/'

    params = {
        'filter': f'equals(metric_id,"{metric_id}")',
        'page[size]': 100
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Get all metrics
def get_metrics():
    url = f'{BASE_URL}/metrics/'

    response = requests.get(url, headers=headers)
    return response.json()

# Calculate revenue attribution
def get_revenue_attribution(days=30):
    metrics = get_metrics()

    revenue_data = []

    for metric in metrics.get('data', []):
        metric_name = metric['attributes']['name']

        if 'placed order' in metric_name.lower():
            # Get events for this metric
            events_url = f'{BASE_URL}/events/'
            params = {
                'filter': f'equals(metric_id,"{metric["id"]}")',
                'page[size]': 100
            }

            response = requests.get(events_url, headers=headers, params=params)
            events = response.json()

            total_revenue = sum(
                float(event['attributes'].get('properties', {}).get('total', 0))
                for event in events.get('data', [])
            )

            revenue_data.append({
                'metric': metric_name,
                'revenue': total_revenue,
                'event_count': len(events.get('data', []))
            })

    df = pd.DataFrame(revenue_data)
    return df

# Get campaign performance comparison
def compare_campaigns():
    url = f'{BASE_URL}/campaigns/'

    response = requests.get(url, headers=headers)
    campaigns = response.json()

    performance_data = []

    for campaign in campaigns.get('data', []):
        campaign_id = campaign['id']
        analytics = get_campaign_analytics(campaign_id)

        stats = analytics.get('stats', {}).get('data', {}).get('attributes', {})

        performance_data.append({
            'campaign_name': campaign['attributes']['name'],
            'send_time': campaign['attributes'].get('send_time'),
            'recipients': stats.get('recipients', 0),
            'opens': stats.get('opens', 0),
            'clicks': stats.get('clicks', 0),
            'open_rate': stats.get('open_rate', 0),
            'click_rate': stats.get('click_rate', 0)
        })

    df = pd.DataFrame(performance_data)
    return df.sort_values('send_time', ascending=False)

# Example usage
revenue_report = get_revenue_attribution(30)
print("Revenue Attribution (Last 30 Days):")
print(revenue_report)

campaign_comparison = compare_campaigns()
print("\nCampaign Performance:")
print(campaign_comparison.head(10))
```

## Installation

```python
uv pip install requests pandas
```

## Authentication

Get your API keys from Klaviyo:
1. Log in to Klaviyo
2. Go to Account > Settings > API Keys
3. Create a Private API Key (for server-side operations)
4. Note your Public API Key (for client-side tracking)

```python
headers = {
    'Authorization': f'Klaviyo-API-Key {PRIVATE_API_KEY}',
    'revision': '2024-10-15',  # API version
    'Content-Type': 'application/json'
}
```

## Quick Start

```python
import requests

PRIVATE_API_KEY = 'your-private-api-key'
BASE_URL = 'https://a.klaviyo.com/api'

headers = {
    'Authorization': f'Klaviyo-API-Key {PRIVATE_API_KEY}',
    'revision': '2024-10-15',
    'Content-Type': 'application/json'
}

# Create profile
profile_data = {
    'data': {
        'type': 'profile',
        'attributes': {
            'email': 'customer@example.com',
            'properties': {
                'first_name': 'John',
                'last_name': 'Smith'
            }
        }
    }
}

response = requests.post(
    f'{BASE_URL}/profiles/',
    headers=headers,
    json=profile_data
)

profile = response.json()
print(f"Profile created: {profile['data']['id']}")
```

## Key Features Reference

- **Profiles**: Customer data, properties, custom fields
- **Events**: Behavioral tracking, e-commerce events
- **Lists**: Static contact lists
- **Segments**: Dynamic audience targeting
- **Campaigns**: One-time email/SMS sends
- **Flows**: Automated triggered messages
- **Templates**: Email/SMS message templates
- **Metrics**: Event definitions and aggregates
- **Catalogs**: Product and content synchronization

## References

- [Klaviyo API Documentation](https://developers.klaviyo.com/en/reference/api_overview)
- [API Changelog](https://developers.klaviyo.com/en/docs/changelog_)
- [E-commerce Integration Guide](https://developers.klaviyo.com/en/docs/integrate_with_a_klaviyo-supported_ecommerce_platform)
- [Event Tracking Guide](https://developers.klaviyo.com/en/docs/guide_to_event_tracking)

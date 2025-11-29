---
name: yotpo
description: "Yotpo reviews, ratings, loyalty, and UGC platform API. Track review volume, sentiment analysis, loyalty program performance, customer engagement, social proof optimization."
---

# Yotpo Integration

## Overview

Yotpo is a comprehensive e-commerce marketing platform providing reviews, ratings, loyalty programs, referrals, and user-generated content (UGC) solutions. This skill covers using the Yotpo API to analyze review performance, track customer sentiment, optimize loyalty programs, and leverage social proof for revenue growth.

## When to Use This Skill

- Product review and rating analytics
- Customer sentiment analysis
- Loyalty program performance tracking
- Referral program optimization
- User-generated content (UGC) management
- Review request campaign effectiveness
- Social proof and conversion optimization
- Customer advocacy measurement

## Core Capabilities

### 1. Review and Rating Analytics

```python
import requests
import pandas as pd
from datetime import datetime, timedelta

# Yotpo API Configuration
APP_KEY = "your_app_key"
SECRET_KEY = "your_secret_key"
BASE_URL = "https://api.yotpo.com/v1"

# Get OAuth token
def get_access_token():
    """Authenticate with Yotpo API"""
    url = f"{BASE_URL}/oauth/token"

    data = {
        'client_id': APP_KEY,
        'client_secret': SECRET_KEY,
        'grant_type': 'client_credentials'
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Authentication failed: {response.text}")

# Get reviews
def get_reviews(page=1, count=100):
    """Fetch product reviews"""
    url = f"{BASE_URL}/apps/{APP_KEY}/reviews"

    params = {
        'page': page,
        'count': count
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# Get all reviews
def get_all_reviews():
    """Fetch all reviews with pagination"""
    all_reviews = []
    page = 1

    while True:
        data = get_reviews(page=page, count=100)

        if not data or 'reviews' not in data:
            break

        reviews = data['reviews']

        if not reviews:
            break

        all_reviews.extend(reviews)

        # Check if there are more pages
        pagination = data.get('pagination', {})
        if page >= pagination.get('total_pages', 1):
            break

        page += 1

    return all_reviews

# Calculate review metrics
def calculate_review_metrics():
    """Comprehensive review analytics"""
    reviews = get_all_reviews()

    review_data = []

    for review in reviews:
        review_data.append({
            'review_id': review['id'],
            'product_id': review.get('product_id'),
            'sku': review.get('sku'),
            'product_title': review.get('product_title', 'Unknown'),
            'score': review.get('score', 0),
            'created_at': pd.to_datetime(review.get('created_at')),
            'verified_buyer': review.get('verified_buyer', False),
            'sentiment': review.get('sentiment'),
            'content': review.get('content', ''),
            'title': review.get('title', ''),
            'votes_up': review.get('votes_up', 0),
            'votes_down': review.get('votes_down', 0),
            'published': review.get('published', False)
        })

    df = pd.DataFrame(review_data)

    if len(df) == 0:
        return {}, df

    # Filter published reviews
    published = df[df['published'] == True]

    # Calculate metrics
    metrics = {
        'total_reviews': len(published),
        'average_rating': published['score'].mean(),
        'rating_distribution': published['score'].value_counts().sort_index().to_dict(),
        'verified_buyer_rate': (published['verified_buyer'].sum() / len(published) * 100) if len(published) > 0 else 0,
        'reviews_with_content': len(published[published['content'].str.len() > 0]),
        'avg_helpful_votes': published['votes_up'].mean(),
        'sentiment_distribution': published['sentiment'].value_counts().to_dict() if 'sentiment' in published.columns else {},
        'unique_products_reviewed': published['product_id'].nunique()
    }

    return metrics, df

# Product-level review analysis
def analyze_product_reviews():
    """Analyze reviews by product"""
    reviews = get_all_reviews()

    product_reviews = {}

    for review in reviews:
        if not review.get('published'):
            continue

        product_id = review.get('product_id')
        sku = review.get('sku', 'unknown')
        product_title = review.get('product_title', 'Unknown')

        if product_id not in product_reviews:
            product_reviews[product_id] = {
                'sku': sku,
                'product_title': product_title,
                'review_count': 0,
                'total_score': 0,
                'scores': []
            }

        product_reviews[product_id]['review_count'] += 1
        product_reviews[product_id]['total_score'] += review.get('score', 0)
        product_reviews[product_id]['scores'].append(review.get('score', 0))

    # Build dataframe
    product_data = []

    for product_id, data in product_reviews.items():
        avg_rating = data['total_score'] / data['review_count'] if data['review_count'] > 0 else 0

        product_data.append({
            'product_id': product_id,
            'sku': data['sku'],
            'product_title': data['product_title'],
            'review_count': data['review_count'],
            'average_rating': avg_rating
        })

    df = pd.DataFrame(product_data)
    df = df.sort_values('review_count', ascending=False)

    return df

# Review trends over time
def analyze_review_trends(months=12):
    """Track review volume and ratings over time"""
    reviews = get_all_reviews()

    review_data = []

    for review in reviews:
        if review.get('published'):
            review_data.append({
                'created_at': pd.to_datetime(review.get('created_at')),
                'score': review.get('score', 0)
            })

    df = pd.DataFrame(review_data)

    if len(df) == 0:
        return None

    # Filter to recent months
    cutoff_date = datetime.now() - timedelta(days=30*months)
    df = df[df['created_at'] >= cutoff_date]

    df['month'] = df['created_at'].dt.to_period('M')

    # Monthly aggregation
    monthly_stats = df.groupby('month').agg({
        'score': ['count', 'mean']
    }).round(2)

    monthly_stats.columns = ['review_count', 'avg_rating']

    return monthly_stats

# Example usage
metrics, reviews_df = calculate_review_metrics()
print(f"Review Metrics:")
print(f"  Total Reviews: {metrics['total_reviews']}")
print(f"  Average Rating: {metrics['average_rating']:.2f}")
print(f"  Verified Buyer Rate: {metrics['verified_buyer_rate']:.1f}%")
print(f"  Reviews with Content: {metrics['reviews_with_content']}")
```

### 2. Customer Sentiment and Engagement

```python
# Sentiment analysis
def analyze_review_sentiment():
    """Analyze customer sentiment from reviews"""
    reviews = get_all_reviews()

    sentiment_data = []

    for review in reviews:
        if not review.get('published'):
            continue

        score = review.get('score', 0)
        content = review.get('content', '')
        title = review.get('title', '')

        # Categorize sentiment based on score
        if score >= 4:
            sentiment = 'Positive'
        elif score >= 3:
            sentiment = 'Neutral'
        else:
            sentiment = 'Negative'

        sentiment_data.append({
            'review_id': review['id'],
            'score': score,
            'sentiment': sentiment,
            'content_length': len(content),
            'has_title': len(title) > 0,
            'votes_up': review.get('votes_up', 0),
            'created_at': pd.to_datetime(review.get('created_at'))
        })

    df = pd.DataFrame(sentiment_data)

    if len(df) == 0:
        return None

    # Sentiment distribution
    sentiment_dist = df['sentiment'].value_counts()
    sentiment_pct = (sentiment_dist / len(df) * 100).round(2)

    # Engagement by sentiment
    engagement = df.groupby('sentiment').agg({
        'votes_up': 'mean',
        'content_length': 'mean'
    }).round(2)

    return sentiment_dist, sentiment_pct, engagement, df

# Top and bottom rated products
def get_product_sentiment_rankings():
    """Identify best and worst reviewed products"""
    product_reviews = analyze_product_reviews()

    if len(product_reviews) == 0:
        return None, None

    # Filter products with minimum reviews (e.g., 5+)
    qualified = product_reviews[product_reviews['review_count'] >= 5]

    top_rated = qualified.nlargest(10, 'average_rating')
    bottom_rated = qualified.nsmallest(10, 'average_rating')

    return top_rated, bottom_rated

# Review response rate
def analyze_review_responses():
    """Track merchant response to reviews"""
    reviews = get_all_reviews()

    response_data = []

    for review in reviews:
        # Check if review has a response
        has_response = review.get('public_response') is not None

        response_data.append({
            'review_id': review['id'],
            'score': review.get('score', 0),
            'has_response': has_response,
            'created_at': pd.to_datetime(review.get('created_at'))
        })

    df = pd.DataFrame(response_data)

    if len(df) == 0:
        return None

    # Response rate overall
    response_rate = (df['has_response'].sum() / len(df) * 100)

    # Response rate by score
    response_by_score = df.groupby('score')['has_response'].apply(
        lambda x: (x.sum() / len(x) * 100)
    ).round(2)

    metrics = {
        'overall_response_rate': response_rate,
        'response_by_score': response_by_score.to_dict(),
        'total_reviews': len(df),
        'responded_reviews': df['has_response'].sum()
    }

    return metrics, df

# Example usage
sentiment_dist, sentiment_pct, engagement, sentiment_df = analyze_review_sentiment()
print(f"Sentiment Distribution:")
for sentiment, count in sentiment_dist.items():
    pct = sentiment_pct[sentiment]
    print(f"  {sentiment}: {count} ({pct}%)")
```

### 3. Loyalty Program Analytics

```python
# Get loyalty data
def get_loyalty_customers(access_token):
    """Fetch loyalty program members"""
    url = f"{BASE_URL}/apps/{APP_KEY}/loyalty/customers"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    params = {
        'page': 1,
        'per_page': 100
    }

    all_customers = []
    page = 1

    while True:
        params['page'] = page
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        customers = data.get('customers', [])

        if not customers:
            break

        all_customers.extend(customers)
        page += 1

        # Check if more pages
        if len(customers) < params['per_page']:
            break

    return all_customers

# Calculate loyalty metrics
def calculate_loyalty_metrics():
    """Analyze loyalty program performance"""
    access_token = get_access_token()
    customers = get_loyalty_customers(access_token)

    loyalty_data = []

    for customer in customers:
        loyalty_data.append({
            'customer_id': customer.get('id'),
            'email': customer.get('email'),
            'points_balance': customer.get('points_balance', 0),
            'points_earned': customer.get('points_earned', 0),
            'points_redeemed': customer.get('points_redeemed', 0),
            'tier': customer.get('tier', {}).get('name', 'Standard'),
            'created_at': pd.to_datetime(customer.get('created_at')),
            'last_activity': pd.to_datetime(customer.get('last_activity_at'))
        })

    df = pd.DataFrame(loyalty_data)

    if len(df) == 0:
        return {}, df

    # Calculate metrics
    metrics = {
        'total_members': len(df),
        'total_points_issued': df['points_earned'].sum(),
        'total_points_redeemed': df['points_redeemed'].sum(),
        'redemption_rate': (df['points_redeemed'].sum() / df['points_earned'].sum() * 100) if df['points_earned'].sum() > 0 else 0,
        'avg_points_balance': df['points_balance'].mean(),
        'active_members': len(df[df['points_balance'] > 0]),
        'tier_distribution': df['tier'].value_counts().to_dict()
    }

    return metrics, df

# Loyalty engagement analysis
def analyze_loyalty_engagement(days=90):
    """Track loyalty program engagement"""
    access_token = get_access_token()
    customers = get_loyalty_customers(access_token)

    cutoff_date = datetime.now() - timedelta(days=days)

    engagement_data = []

    for customer in customers:
        last_activity = pd.to_datetime(customer.get('last_activity_at'))
        is_active = last_activity >= cutoff_date if last_activity else False

        engagement_data.append({
            'customer_id': customer.get('id'),
            'points_earned': customer.get('points_earned', 0),
            'points_redeemed': customer.get('points_redeemed', 0),
            'is_active': is_active,
            'days_since_activity': (datetime.now() - last_activity).days if last_activity else None
        })

    df = pd.DataFrame(engagement_data)

    if len(df) == 0:
        return None

    # Engagement metrics
    engagement_rate = (df['is_active'].sum() / len(df) * 100)

    metrics = {
        'engagement_rate': engagement_rate,
        'active_members': df['is_active'].sum(),
        'inactive_members': (~df['is_active']).sum(),
        'avg_days_since_activity': df['days_since_activity'].mean()
    }

    return metrics, df

# VIP tier analysis
def analyze_loyalty_tiers():
    """Analyze performance by loyalty tier"""
    access_token = get_access_token()
    customers = get_loyalty_customers(access_token)

    tier_data = []

    for customer in customers:
        tier_data.append({
            'tier': customer.get('tier', {}).get('name', 'Standard'),
            'points_earned': customer.get('points_earned', 0),
            'points_redeemed': customer.get('points_redeemed', 0),
            'points_balance': customer.get('points_balance', 0)
        })

    df = pd.DataFrame(tier_data)

    if len(df) == 0:
        return None

    # Tier performance
    tier_stats = df.groupby('tier').agg({
        'points_earned': ['sum', 'mean', 'count'],
        'points_redeemed': ['sum', 'mean'],
        'points_balance': 'mean'
    }).round(2)

    tier_stats.columns = [
        'total_earned', 'avg_earned', 'member_count',
        'total_redeemed', 'avg_redeemed', 'avg_balance'
    ]

    return tier_stats

# Example usage
loyalty_metrics, loyalty_df = calculate_loyalty_metrics()
if loyalty_metrics:
    print(f"Loyalty Program Metrics:")
    print(f"  Total Members: {loyalty_metrics['total_members']}")
    print(f"  Points Issued: {loyalty_metrics['total_points_issued']:,.0f}")
    print(f"  Redemption Rate: {loyalty_metrics['redemption_rate']:.1f}%")
    print(f"  Active Members: {loyalty_metrics['active_members']}")
```

### 4. UGC and Social Proof Analytics

```python
# Get bottom line (aggregate stats)
def get_bottom_line(product_id=None):
    """Get aggregate review statistics"""
    if product_id:
        url = f"{BASE_URL}/apps/{APP_KEY}/bottom_lines/{product_id}"
    else:
        url = f"{BASE_URL}/apps/{APP_KEY}/bottom_line"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# Analyze review impact on conversion
def analyze_review_conversion_impact():
    """Calculate how reviews impact purchase decisions"""
    # Get overall stats
    bottom_line = get_bottom_line()

    if not bottom_line:
        return None

    stats = bottom_line.get('response', {}).get('bottomline', {})

    metrics = {
        'total_reviews': stats.get('total_reviews', 0),
        'average_score': stats.get('average_score', 0),
        'star_distribution': stats.get('star_distribution', {}),
        'products_count': stats.get('products_count', 0)
    }

    return metrics

# Get photos (UGC)
def get_review_photos():
    """Fetch user-generated photo content"""
    url = f"{BASE_URL}/apps/{APP_KEY}/albums/album_id/images"

    # Note: Requires album ID from Yotpo dashboard
    # This is a simplified version

    reviews = get_all_reviews()

    photos_data = []

    for review in reviews:
        if review.get('images'):
            for image in review.get('images', []):
                photos_data.append({
                    'review_id': review['id'],
                    'product_id': review.get('product_id'),
                    'image_url': image.get('original_url'),
                    'score': review.get('score'),
                    'created_at': pd.to_datetime(review.get('created_at'))
                })

    df = pd.DataFrame(photos_data)

    if len(df) == 0:
        return None

    metrics = {
        'total_photos': len(df),
        'reviews_with_photos': df['review_id'].nunique(),
        'photo_rate': None,  # Would need total reviews
        'avg_rating_with_photos': df['score'].mean()
    }

    return metrics, df

# Social sharing analysis
def analyze_social_sharing():
    """Track social media sharing of reviews"""
    reviews = get_all_reviews()

    sharing_data = []

    for review in reviews:
        # Check for social shares
        shares = review.get('social_shares', {})

        sharing_data.append({
            'review_id': review['id'],
            'score': review.get('score', 0),
            'facebook_shares': shares.get('facebook', 0),
            'twitter_shares': shares.get('twitter', 0),
            'total_shares': sum(shares.values()) if shares else 0
        })

    df = pd.DataFrame(sharing_data)

    if len(df) == 0:
        return None

    # Sharing metrics
    metrics = {
        'total_shares': df['total_shares'].sum(),
        'reviews_shared': len(df[df['total_shares'] > 0]),
        'share_rate': (len(df[df['total_shares'] > 0]) / len(df) * 100),
        'avg_shares_per_review': df['total_shares'].mean()
    }

    return metrics, df

# Review request performance
def analyze_review_requests():
    """Track effectiveness of review request campaigns"""
    # This would require campaign data from Yotpo
    # Simplified version using review creation dates

    reviews = get_all_reviews()

    # Group by week
    review_data = []

    for review in reviews:
        review_data.append({
            'created_at': pd.to_datetime(review.get('created_at')),
            'verified_buyer': review.get('verified_buyer', False)
        })

    df = pd.DataFrame(review_data)

    if len(df) == 0:
        return None

    df['week'] = df['created_at'].dt.to_period('W')

    # Weekly review volume
    weekly_reviews = df.groupby('week').agg({
        'created_at': 'count',
        'verified_buyer': 'sum'
    }).rename(columns={'created_at': 'total_reviews', 'verified_buyer': 'verified_reviews'})

    weekly_reviews['verification_rate'] = (
        weekly_reviews['verified_reviews'] / weekly_reviews['total_reviews'] * 100
    ).round(2)

    return weekly_reviews

# Example usage
conversion_metrics = analyze_review_conversion_impact()
if conversion_metrics:
    print(f"Review Conversion Impact:")
    print(f"  Total Reviews: {conversion_metrics['total_reviews']}")
    print(f"  Average Score: {conversion_metrics['average_score']:.2f}")
    print(f"  Products Reviewed: {conversion_metrics['products_count']}")
```

## Installation

```bash
# Install required packages
uv pip install requests pandas python-dateutil
```

## Authentication

### API Credentials

1. Log in to Yotpo dashboard
2. Go to Settings > Store Settings > General Settings
3. Find your App Key and Secret Key
4. Use OAuth for authenticated requests

```python
import requests

APP_KEY = "your_app_key"
SECRET_KEY = "your_secret_key"
BASE_URL = "https://api.yotpo.com/v1"

# Get access token
def get_access_token():
    url = f"{BASE_URL}/oauth/token"

    data = {
        'client_id': APP_KEY,
        'client_secret': SECRET_KEY,
        'grant_type': 'client_credentials'
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Auth failed: {response.text}")

# Test connection
access_token = get_access_token()
print(f"Access token: {access_token[:20]}...")
```

## Quick Start

```python
import requests

APP_KEY = "your_app_key"
SECRET_KEY = "your_secret_key"
BASE_URL = "https://api.yotpo.com/v1"

# Get reviews
response = requests.get(
    f"{BASE_URL}/apps/{APP_KEY}/reviews",
    params={'page': 1, 'count': 10}
)

if response.status_code == 200:
    data = response.json()
    reviews = data.get('reviews', [])

    print(f"Recent Reviews: {len(reviews)}")

    for review in reviews:
        print(f"{review.get('score')} stars - {review.get('product_title')}")
        print(f"  {review.get('content', '')[:100]}...")

# Get bottom line stats
response = requests.get(f"{BASE_URL}/apps/{APP_KEY}/bottom_line")

if response.status_code == 200:
    stats = response.json()['response']['bottomline']
    print(f"\nOverall Stats:")
    print(f"  Total Reviews: {stats.get('total_reviews')}")
    print(f"  Average Score: {stats.get('average_score'):.2f}")
```

## Key Metrics Reference

### Review Metrics
- **Total Reviews**: All published reviews
- **Average Rating**: Mean star rating (1-5)
- **Rating Distribution**: Count by star rating
- **Verified Buyer Rate**: Verified purchases / total reviews

### Engagement Metrics
- **Review Response Rate**: Merchant responses / total reviews
- **Helpful Votes**: Average votes per review
- **Photo Attachment Rate**: Reviews with photos / total
- **Social Shares**: Reviews shared on social media

### Loyalty Metrics
- **Total Members**: Loyalty program enrollments
- **Redemption Rate**: Points redeemed / points issued
- **Engagement Rate**: Active members / total members
- **Tier Distribution**: Members by VIP tier

### Conversion Metrics
- **Review Conversion Impact**: Sales lift from reviews
- **UGC Performance**: Engagement with user photos
- **Referral Conversion Rate**: Referral program success
- **Social Proof ROI**: Revenue attributed to reviews

## References

- [Yotpo API Documentation](https://apidocs.yotpo.com/reference)
- [Reviews API](https://apidocs.yotpo.com/reference/retrieve-all-reviews)
- [Loyalty API](https://apidocs.yotpo.com/reference/loyalty-api-overview)
- [Bottom Line API](https://apidocs.yotpo.com/reference/retrieve-the-bottom-line)
- [Yotpo Analytics Guide](https://support.yotpo.com/docs/analytics-overview)

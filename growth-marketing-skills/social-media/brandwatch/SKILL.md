---
name: brandwatch
description: "Social listening and analytics platform. Brand monitoring, sentiment analysis, trend detection, competitive intelligence, crisis management, influencer identification."
---

# Brandwatch Integration

## Overview

Brandwatch is an enterprise social listening and analytics platform that monitors billions of online conversations to provide insights about brands, markets, and trends. This skill covers using the Brandwatch API for social listening, sentiment analysis, competitive intelligence, crisis detection, influencer identification, and generating actionable insights from social data.

## When to Use This Skill

- Brand monitoring and reputation management
- Social listening and sentiment analysis
- Competitive intelligence and market research
- Crisis detection and response
- Trend identification and analysis
- Influencer discovery and tracking
- Consumer insights and audience research
- Campaign performance analysis
- Market segmentation and targeting

## Core Capabilities

### 1. Query and Project Management

```python
import requests
import json
from datetime import datetime, timedelta

# Brandwatch API configuration
ACCESS_TOKEN = 'your-brandwatch-access-token'
BASE_URL = 'https://api.brandwatch.com'

# Headers for all requests
def get_headers():
    return {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

# Get projects
def get_projects():
    """Get all Brandwatch projects"""
    url = f'{BASE_URL}/projects'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Get project details
def get_project(project_id):
    """Get specific project details"""
    url = f'{BASE_URL}/projects/{project_id}'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Create query
def create_query(project_id, name, query_string, language='en'):
    """
    Create a social listening query

    Args:
        project_id: Brandwatch project ID
        name: Query name
        query_string: Boolean search query
        language: Language code (e.g., 'en', 'es', 'fr')
    """
    url = f'{BASE_URL}/projects/{project_id}/queries'

    query_data = {
        'name': name,
        'query': query_string,
        'language': language
    }

    response = requests.post(url, headers=get_headers(), json=query_data)
    return response.json()

# Get queries
def get_queries(project_id):
    """Get all queries in a project"""
    url = f'{BASE_URL}/projects/{project_id}/queries'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Update query
def update_query(project_id, query_id, query_string=None, name=None):
    """Update an existing query"""
    url = f'{BASE_URL}/projects/{project_id}/queries/{query_id}'

    update_data = {}
    if query_string:
        update_data['query'] = query_string
    if name:
        update_data['name'] = name

    response = requests.patch(url, headers=get_headers(), json=update_data)
    return response.json()

# Example: Create brand monitoring query
project_id = 12345

brand_query = create_query(
    project_id=project_id,
    name='Brand Mentions',
    query_string='("YourBrand" OR @YourBrand OR #YourBrand) AND NOT spam',
    language='en'
)

print(f"Query created: {brand_query['id']}")
```

### 2. Mention Retrieval and Analysis

```python
# Get mentions
def get_mentions(project_id, query_id, start_date=None, end_date=None,
                page_size=1000, sentiment=None):
    """
    Retrieve social mentions

    Args:
        project_id: Project ID
        query_id: Query ID
        start_date: Start date for mentions
        end_date: End date for mentions
        page_size: Results per page (max 5000)
        sentiment: Filter by 'positive', 'negative', 'neutral'
    """
    url = f'{BASE_URL}/projects/{project_id}/data/mentions'

    params = {
        'queryId': query_id,
        'pageSize': page_size
    }

    if start_date:
        params['startDate'] = start_date.strftime('%Y-%m-%dT%H:%M:%S')
    if end_date:
        params['endDate'] = end_date.strftime('%Y-%m-%dT%H:%M:%S')
    if sentiment:
        params['sentiment'] = sentiment

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Get mention volume
def get_mention_volume(project_id, query_id, start_date, end_date, interval='day'):
    """
    Get mention volume over time

    Args:
        project_id: Project ID
        query_id: Query ID
        start_date: Start date
        end_date: End date
        interval: 'hour', 'day', 'week', or 'month'
    """
    url = f'{BASE_URL}/projects/{project_id}/data/volume/queries/{query_id}'

    params = {
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d'),
        'interval': interval
    }

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Search mentions by keyword
def search_mentions(project_id, keywords, start_date, end_date, max_results=1000):
    """
    Search mentions containing specific keywords

    Args:
        project_id: Project ID
        keywords: List of keywords to search
        start_date: Start date
        end_date: End date
        max_results: Maximum results to return
    """
    url = f'{BASE_URL}/projects/{project_id}/data/mentions/search'

    search_data = {
        'keywords': keywords,
        'startDate': start_date.isoformat(),
        'endDate': end_date.isoformat(),
        'maxResults': max_results
    }

    response = requests.post(url, headers=get_headers(), json=search_data)
    return response.json()

# Example: Get last 7 days of brand mentions
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

mentions = get_mentions(
    project_id=project_id,
    query_id=brand_query['id'],
    start_date=start_date,
    end_date=end_date
)

print(f"Found {len(mentions.get('results', []))} mentions")
```

### 3. Sentiment Analysis

```python
import pandas as pd

# Get sentiment breakdown
def get_sentiment_analysis(project_id, query_id, start_date, end_date):
    """
    Analyze sentiment distribution

    Args:
        project_id: Project ID
        query_id: Query ID
        start_date: Start date
        end_date: End date
    """
    url = f'{BASE_URL}/projects/{project_id}/data/sentiment/queries/{query_id}'

    params = {
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d')
    }

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Get sentiment over time
def get_sentiment_trend(project_id, query_id, start_date, end_date, interval='day'):
    """
    Track sentiment changes over time

    Args:
        project_id: Project ID
        query_id: Query ID
        start_date: Start date
        end_date: End date
        interval: Time interval for aggregation
    """
    url = f'{BASE_URL}/projects/{project_id}/data/sentiment/timeseries'

    params = {
        'queryId': query_id,
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d'),
        'interval': interval
    }

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Analyze negative mentions
def analyze_negative_mentions(project_id, query_id, days=7):
    """
    Deep dive into negative sentiment

    Returns: Negative mentions with context
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    negative_mentions = get_mentions(
        project_id=project_id,
        query_id=query_id,
        start_date=start_date,
        end_date=end_date,
        sentiment='negative'
    )

    # Analyze common themes in negative mentions
    negative_data = []

    for mention in negative_mentions.get('results', []):
        negative_data.append({
            'date': mention.get('date'),
            'author': mention.get('author'),
            'text': mention.get('title'),
            'source': mention.get('domain'),
            'reach': mention.get('impressions', 0)
        })

    df = pd.DataFrame(negative_data)

    analysis = {
        'total_negative': len(df),
        'avg_reach': df['reach'].mean() if len(df) > 0 else 0,
        'top_sources': df['source'].value_counts().head(5).to_dict(),
        'recent_mentions': negative_data[:10]
    }

    return analysis

# Sentiment comparison
def compare_sentiment(project_id, query_ids, start_date, end_date):
    """
    Compare sentiment across multiple queries (e.g., your brand vs competitors)

    Args:
        project_id: Project ID
        query_ids: List of query IDs to compare
        start_date: Start date
        end_date: End date
    """
    comparison = []

    for query_id in query_ids:
        sentiment_data = get_sentiment_analysis(
            project_id, query_id, start_date, end_date
        )

        comparison.append({
            'query_id': query_id,
            'query_name': sentiment_data.get('queryName'),
            'positive': sentiment_data.get('positive', 0),
            'neutral': sentiment_data.get('neutral', 0),
            'negative': sentiment_data.get('negative', 0),
            'net_sentiment': sentiment_data.get('netSentiment', 0)
        })

    return pd.DataFrame(comparison)

# Example: Sentiment analysis
sentiment = get_sentiment_analysis(
    project_id=project_id,
    query_id=brand_query['id'],
    start_date=start_date,
    end_date=end_date
)

print(f"Sentiment breakdown:")
print(f"  Positive: {sentiment.get('positive', 0)}%")
print(f"  Neutral: {sentiment.get('neutral', 0)}%")
print(f"  Negative: {sentiment.get('negative', 0)}%")
print(f"  Net Sentiment: {sentiment.get('netSentiment', 0)}")
```

### 4. Topic and Theme Analysis

```python
# Get topics
def get_topics(project_id, query_id, start_date, end_date, limit=20):
    """
    Extract main topics from conversations

    Args:
        project_id: Project ID
        query_id: Query ID
        start_date: Start date
        end_date: End date
        limit: Number of topics to return
    """
    url = f'{BASE_URL}/projects/{project_id}/data/topics'

    params = {
        'queryId': query_id,
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d'),
        'limit': limit
    }

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Get trending topics
def get_trending_topics(project_id, query_id, hours=24):
    """
    Identify trending topics in recent conversations

    Args:
        project_id: Project ID
        query_id: Query ID
        hours: Time window for trending analysis
    """
    url = f'{BASE_URL}/projects/{project_id}/data/topics/trending'

    end_date = datetime.now()
    start_date = end_date - timedelta(hours=hours)

    params = {
        'queryId': query_id,
        'startDate': start_date.isoformat(),
        'endDate': end_date.isoformat()
    }

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Get word cloud data
def get_word_cloud(project_id, query_id, start_date, end_date, limit=100):
    """
    Get most frequently mentioned words

    Args:
        project_id: Project ID
        query_id: Query ID
        start_date: Start date
        end_date: End date
        limit: Number of words to return
    """
    url = f'{BASE_URL}/projects/{project_id}/data/words'

    params = {
        'queryId': query_id,
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d'),
        'limit': limit
    }

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Analyze themes
def analyze_themes(project_id, query_id, days=30):
    """
    Identify main conversation themes

    Returns: Theme analysis with volume and sentiment
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    topics = get_topics(project_id, query_id, start_date, end_date, limit=50)

    theme_data = []

    for topic in topics.get('results', []):
        theme_data.append({
            'theme': topic.get('name'),
            'volume': topic.get('volume', 0),
            'sentiment': topic.get('sentiment', 0),
            'growth': topic.get('growth', 0),
            'reach': topic.get('reach', 0)
        })

    df = pd.DataFrame(theme_data)

    return df.sort_values('volume', ascending=False)

# Example: Topic analysis
topics = get_topics(
    project_id=project_id,
    query_id=brand_query['id'],
    start_date=start_date,
    end_date=end_date
)

print("Top conversation topics:")
for topic in topics.get('results', [])[:10]:
    print(f"  - {topic['name']}: {topic['volume']:,} mentions")
```

### 5. Influencer Identification

```python
# Get top authors
def get_top_authors(project_id, query_id, start_date, end_date, limit=50):
    """
    Identify top authors/influencers

    Args:
        project_id: Project ID
        query_id: Query ID
        start_date: Start date
        end_date: End date
        limit: Number of authors to return
    """
    url = f'{BASE_URL}/projects/{project_id}/data/authors'

    params = {
        'queryId': query_id,
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d'),
        'limit': limit,
        'orderBy': 'reach'  # or 'volume', 'engagement'
    }

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Analyze influencer impact
def analyze_influencers(project_id, query_id, days=30, min_followers=10000):
    """
    Identify and analyze influencers discussing your brand

    Args:
        project_id: Project ID
        query_id: Query ID
        days: Days to analyze
        min_followers: Minimum follower count to be considered influencer
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    authors = get_top_authors(project_id, query_id, start_date, end_date, limit=100)

    influencer_data = []

    for author in authors.get('results', []):
        followers = author.get('followers', 0)

        if followers >= min_followers:
            influencer_data.append({
                'username': author.get('username'),
                'name': author.get('name'),
                'followers': followers,
                'mentions': author.get('mentions', 0),
                'reach': author.get('reach', 0),
                'engagement': author.get('engagement', 0),
                'sentiment': author.get('sentiment', 0),
                'location': author.get('location', 'Unknown')
            })

    df = pd.DataFrame(influencer_data)

    return df.sort_values('reach', ascending=False)

# Get author profile
def get_author_profile(project_id, author_id):
    """Get detailed author/influencer profile"""
    url = f'{BASE_URL}/projects/{project_id}/data/authors/{author_id}'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Example: Identify influencers
influencers = analyze_influencers(
    project_id=project_id,
    query_id=brand_query['id'],
    days=30,
    min_followers=50000
)

print(f"Found {len(influencers)} influencers")
print("\nTop 5 Influencers by Reach:")
print(influencers[['username', 'followers', 'reach', 'sentiment']].head())
```

### 6. Crisis Detection and Monitoring

```python
# Monitor for crisis signals
def detect_crisis_signals(project_id, query_id, threshold_multiplier=3):
    """
    Detect unusual spikes in mentions or negative sentiment

    Args:
        project_id: Project ID
        query_id: Query ID
        threshold_multiplier: How many standard deviations above normal to alert
    """
    # Get last 30 days for baseline
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    volume_data = get_mention_volume(
        project_id, query_id, start_date, end_date, interval='hour'
    )

    # Calculate baseline statistics
    volumes = [point.get('value', 0) for point in volume_data.get('results', [])]

    if not volumes:
        return {'alert': False, 'message': 'No data available'}

    import numpy as np
    mean_volume = np.mean(volumes)
    std_volume = np.std(volumes)

    # Check last hour
    latest_volume = volumes[-1] if volumes else 0
    threshold = mean_volume + (threshold_multiplier * std_volume)

    # Get sentiment for last 24 hours
    recent_start = end_date - timedelta(hours=24)
    sentiment = get_sentiment_analysis(project_id, query_id, recent_start, end_date)

    negative_pct = sentiment.get('negative', 0)

    # Crisis conditions
    volume_spike = latest_volume > threshold
    high_negativity = negative_pct > 60  # More than 60% negative

    crisis_detected = volume_spike or high_negativity

    return {
        'alert': crisis_detected,
        'volume_spike': volume_spike,
        'high_negativity': high_negativity,
        'current_volume': latest_volume,
        'threshold': threshold,
        'negative_percentage': negative_pct,
        'message': 'Crisis detected!' if crisis_detected else 'No crisis detected'
    }

# Get crisis mentions
def get_crisis_mentions(project_id, query_id, hours=24):
    """
    Get recent high-impact negative mentions for crisis response

    Args:
        project_id: Project ID
        query_id: Query ID
        hours: Hours to look back
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(hours=hours)

    # Get negative mentions sorted by reach
    mentions = get_mentions(
        project_id=project_id,
        query_id=query_id,
        start_date=start_date,
        end_date=end_date,
        sentiment='negative'
    )

    # Sort by reach/impact
    sorted_mentions = sorted(
        mentions.get('results', []),
        key=lambda x: x.get('impressions', 0),
        reverse=True
    )

    return sorted_mentions[:20]  # Top 20 by reach

# Real-time monitoring
def monitor_brand_health(project_id, query_id):
    """
    Real-time brand health monitoring

    Returns: Comprehensive health score
    """
    # Last 24 hours
    end_date = datetime.now()
    start_date = end_date - timedelta(hours=24)

    # Get metrics
    mentions = get_mentions(project_id, query_id, start_date, end_date)
    sentiment = get_sentiment_analysis(project_id, query_id, start_date, end_date)
    crisis_check = detect_crisis_signals(project_id, query_id)

    # Calculate health score (0-100)
    net_sentiment = sentiment.get('netSentiment', 0)
    negative_pct = sentiment.get('negative', 0)

    health_score = max(0, min(100, 50 + net_sentiment - (negative_pct / 2)))

    return {
        'health_score': health_score,
        'mention_count': len(mentions.get('results', [])),
        'net_sentiment': net_sentiment,
        'negative_percentage': negative_pct,
        'crisis_alert': crisis_check['alert'],
        'status': 'Critical' if health_score < 40 else 'Warning' if health_score < 60 else 'Healthy'
    }

# Example: Crisis monitoring
crisis_status = detect_crisis_signals(project_id, brand_query['id'])

if crisis_status['alert']:
    print("⚠️ CRISIS ALERT!")
    print(f"  Current volume: {crisis_status['current_volume']}")
    print(f"  Negative sentiment: {crisis_status['negative_percentage']:.1f}%")

    # Get crisis mentions for response
    crisis_mentions = get_crisis_mentions(project_id, brand_query['id'], hours=24)
    print(f"\n  Top crisis mentions to address: {len(crisis_mentions)}")
```

### 7. Competitive Intelligence

```python
# Compare brands
def compare_competitors(project_id, brand_queries, start_date, end_date):
    """
    Compare your brand against competitors

    Args:
        project_id: Project ID
        brand_queries: Dict of brand_name: query_id
        start_date: Start date
        end_date: End date
    """
    comparison_data = []

    for brand_name, query_id in brand_queries.items():
        # Get volume
        volume = get_mention_volume(project_id, query_id, start_date, end_date)
        total_volume = sum(point.get('value', 0) for point in volume.get('results', []))

        # Get sentiment
        sentiment = get_sentiment_analysis(project_id, query_id, start_date, end_date)

        # Get top topics
        topics = get_topics(project_id, query_id, start_date, end_date, limit=5)
        top_topics = [t.get('name') for t in topics.get('results', [])[:3]]

        comparison_data.append({
            'brand': brand_name,
            'volume': total_volume,
            'net_sentiment': sentiment.get('netSentiment', 0),
            'positive_pct': sentiment.get('positive', 0),
            'negative_pct': sentiment.get('negative', 0),
            'top_topics': ', '.join(top_topics)
        })

    df = pd.DataFrame(comparison_data)
    return df.sort_values('volume', ascending=False)

# Example: Competitive analysis
competitor_queries = {
    'Your Brand': brand_query['id'],
    'Competitor A': 67890,
    'Competitor B': 11111
}

competitive_analysis = compare_competitors(
    project_id=project_id,
    brand_queries=competitor_queries,
    start_date=start_date,
    end_date=end_date
)

print("Competitive Analysis:")
print(competitive_analysis)
```

## Installation

```bash
# Using requests for REST API
uv pip install requests pandas numpy

# Optional: For advanced analytics
uv pip install scikit-learn matplotlib seaborn
```

## Authentication

Brandwatch uses OAuth 2.0 authentication:

```python
import requests

# OAuth credentials
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
USERNAME = 'your-username'
PASSWORD = 'your-password'

# Get access token
def get_access_token():
    url = 'https://api.brandwatch.com/oauth/token'

    data = {
        'grant_type': 'api-password',
        'username': USERNAME,
        'password': PASSWORD,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(url, data=data)
    token_data = response.json()

    return token_data['access_token']

# Use token in requests
ACCESS_TOKEN = get_access_token()

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}
```

## Quick Start

```python
import requests
from datetime import datetime, timedelta

# Get access token and configure
ACCESS_TOKEN = 'your-brandwatch-access-token'
BASE_URL = 'https://api.brandwatch.com'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

# 1. Get your projects
response = requests.get(f'{BASE_URL}/projects', headers=headers)
projects = response.json()

project_id = projects['results'][0]['id']
print(f"Using project: {projects['results'][0]['name']}")

# 2. Create a brand monitoring query
query_data = {
    'name': 'Brand Monitoring',
    'query': '("YourBrand" OR @YourBrand) AND NOT spam',
    'language': 'en'
}

response = requests.post(
    f'{BASE_URL}/projects/{project_id}/queries',
    headers=headers,
    json=query_data
)

query = response.json()
print(f"Query created: {query['id']}")

# 3. Get recent mentions
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

response = requests.get(
    f'{BASE_URL}/projects/{project_id}/data/mentions',
    headers=headers,
    params={
        'queryId': query['id'],
        'startDate': start_date.strftime('%Y-%m-%dT%H:%M:%S'),
        'endDate': end_date.strftime('%Y-%m-%dT%H:%M:%S')
    }
)

mentions = response.json()
print(f"\nFound {len(mentions.get('results', []))} mentions in last 7 days")
```

## Key Metrics

### Volume Metrics
- **Mention Volume**: Total mentions over time
- **Share of Voice**: Your mentions vs. competitors
- **Reach**: Total potential audience reached
- **Impressions**: Total times content was seen

### Sentiment Metrics
- **Net Sentiment**: (Positive % - Negative %) score
- **Sentiment Distribution**: Positive/Neutral/Negative breakdown
- **Sentiment Trend**: Changes over time
- **Emotion Analysis**: Joy, anger, fear, sadness, surprise

### Engagement Metrics
- **Engagement Rate**: Interactions per mention
- **Amplification**: Shares and retweets
- **Author Influence**: Reach and follower counts
- **Conversation Threads**: Discussion depth

### Crisis Indicators
- **Volume Spikes**: Unusual increases in mentions
- **Negative Sentiment Spikes**: Sudden negativity increases
- **Reach of Negative Content**: Impact of negative mentions
- **Response Time**: Time to address issues

## Best Practices

1. **Set Up Comprehensive Queries**: Include brand variations, common misspellings, hashtags
2. **Monitor Continuously**: Check sentiment and volume daily
3. **Set Up Alerts**: Configure alerts for crisis signals
4. **Track Competitors**: Benchmark against 3-5 main competitors
5. **Identify Influencers**: Build relationships with positive influencers
6. **Respond Quickly**: Address negative mentions within 1 hour
7. **Analyze Trends**: Review weekly/monthly to identify patterns
8. **Segment Audiences**: Understand different audience segments

## References

- [Brandwatch API Documentation](https://developers.brandwatch.com/docs)
- [Authentication Guide](https://developers.brandwatch.com/docs/authentication)
- [Query Language](https://developers.brandwatch.com/docs/query-language)
- [Sentiment Analysis](https://developers.brandwatch.com/docs/sentiment)
- [Crisis Management Guide](https://www.brandwatch.com/crisis-management/)
- [Brandwatch Academy](https://www.brandwatch.com/academy/)
- [API Rate Limits](https://developers.brandwatch.com/docs/rate-limits)

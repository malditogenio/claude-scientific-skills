---
name: mention
description: "Media monitoring and social listening platform. Real-time alerts, brand monitoring, competitor tracking, influencer discovery, sentiment analysis, multi-source monitoring."
---

# Mention Integration

## Overview

Mention is a real-time media monitoring and social listening platform that tracks brand mentions across social media, news sites, blogs, forums, and the web. This skill covers using the Mention API for real-time brand monitoring, competitive intelligence, influencer identification, sentiment tracking, and generating alerts for important mentions across multiple sources.

## When to Use This Skill

- Real-time brand and keyword monitoring
- Social media mention tracking
- News and blog monitoring
- Forum and review site tracking
- Competitive intelligence gathering
- Influencer identification and outreach
- Crisis detection and management
- PR and media relations tracking
- Customer feedback monitoring
- Market research and trend analysis

## Core Capabilities

### 1. Alert and Account Management

```python
import requests
import json
from datetime import datetime, timedelta

# Mention API configuration
ACCESS_TOKEN = 'your-mention-access-token'
ACCOUNT_ID = 'your-account-id'
BASE_URL = 'https://api.mention.com/api/v2'

# Headers for all requests
def get_headers():
    return {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

# Get account information
def get_account():
    """Get account details and limits"""
    url = f'{BASE_URL}/accounts/{ACCOUNT_ID}'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Get all alerts
def get_alerts():
    """Get all monitoring alerts for the account"""
    url = f'{BASE_URL}/accounts/{ACCOUNT_ID}/alerts'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Get specific alert
def get_alert(alert_id):
    """Get details for a specific alert"""
    url = f'{BASE_URL}/accounts/{ACCOUNT_ID}/alerts/{alert_id}'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Create alert
def create_alert(name, keywords, languages=['en'], sources=None, excluded_keywords=None):
    """
    Create a new monitoring alert

    Args:
        name: Alert name
        keywords: List of keywords to monitor
        languages: List of language codes
        sources: List of sources to monitor (twitter, web, news, blogs, forums, etc.)
        excluded_keywords: Keywords to exclude
    """
    url = f'{BASE_URL}/accounts/{ACCOUNT_ID}/alerts'

    alert_data = {
        'name': name,
        'primary_keyword': keywords[0] if keywords else '',
        'query': {
            'type': 'boolean',
            'included_keywords': keywords,
            'excluded_keywords': excluded_keywords or []
        },
        'languages': languages
    }

    if sources:
        alert_data['sources'] = sources

    response = requests.post(url, headers=get_headers(), json=alert_data)
    return response.json()

# Update alert
def update_alert(alert_id, name=None, keywords=None, excluded_keywords=None):
    """Update an existing alert"""
    url = f'{BASE_URL}/accounts/{ACCOUNT_ID}/alerts/{alert_id}'

    update_data = {}

    if name:
        update_data['name'] = name
    if keywords:
        update_data['query'] = {
            'type': 'boolean',
            'included_keywords': keywords,
            'excluded_keywords': excluded_keywords or []
        }

    response = requests.put(url, headers=get_headers(), json=update_data)
    return response.json()

# Delete alert
def delete_alert(alert_id):
    """Delete an alert"""
    url = f'{BASE_URL}/accounts/{ACCOUNT_ID}/alerts/{alert_id}'

    response = requests.delete(url, headers=get_headers())
    return response.status_code == 204

# Example: Create brand monitoring alert
brand_alert = create_alert(
    name='Brand Mentions',
    keywords=['YourBrand', '@YourBrand', '#YourBrand', 'Your Company Name'],
    excluded_keywords=['spam', 'bot', 'fake'],
    languages=['en'],
    sources=['twitter', 'facebook', 'instagram', 'web', 'news', 'blogs']
)

print(f"Alert created: {brand_alert['alert']['id']}")
print(f"Monitoring keywords: {brand_alert['alert']['query']['included_keywords']}")
```

### 2. Mention Retrieval and Management

```python
# Get mentions for an alert
def get_mentions(alert_id, limit=20, offset=0, sort='published_at',
                sources=None, tone=None, unread_only=False):
    """
    Retrieve mentions for a specific alert

    Args:
        alert_id: Alert ID
        limit: Number of mentions to retrieve
        offset: Pagination offset
        sort: Sort by 'published_at', 'reach', or 'engagement'
        sources: Filter by sources (twitter, web, news, etc.)
        tone: Filter by sentiment ('positive', 'neutral', 'negative')
        unread_only: Only return unread mentions
    """
    url = f'{BASE_URL}/accounts/{ACCOUNT_ID}/alerts/{alert_id}/mentions'

    params = {
        'limit': limit,
        'offset': offset,
        'sort': sort
    }

    if sources:
        params['sources'] = ','.join(sources)
    if tone:
        params['tone'] = tone
    if unread_only:
        params['unread'] = 'true'

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Get mention by ID
def get_mention(alert_id, mention_id):
    """Get details for a specific mention"""
    url = f'{BASE_URL}/accounts/{ACCOUNT_ID}/alerts/{alert_id}/mentions/{mention_id}'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Mark mention as read
def mark_as_read(alert_id, mention_id):
    """Mark a mention as read"""
    url = f'{BASE_URL}/accounts/{ACCOUNT_ID}/alerts/{alert_id}/mentions/{mention_id}'

    update_data = {'read': True}

    response = requests.put(url, headers=get_headers(), json=update_data)
    return response.json()

# Add tag to mention
def tag_mention(alert_id, mention_id, tags):
    """
    Add tags to a mention for organization

    Args:
        alert_id: Alert ID
        mention_id: Mention ID
        tags: List of tag names
    """
    url = f'{BASE_URL}/accounts/{ACCOUNT_ID}/alerts/{alert_id}/mentions/{mention_id}/tags'

    tag_data = {'tags': tags}

    response = requests.post(url, headers=get_headers(), json=tag_data)
    return response.json()

# Mark as favorite
def favorite_mention(alert_id, mention_id):
    """Mark mention as favorite/important"""
    url = f'{BASE_URL}/accounts/{ACCOUNT_ID}/alerts/{alert_id}/mentions/{mention_id}'

    update_data = {'favorite': True}

    response = requests.put(url, headers=get_headers(), json=update_data)
    return response.json()

# Archive mention
def archive_mention(alert_id, mention_id):
    """Archive a mention"""
    url = f'{BASE_URL}/accounts/{ACCOUNT_ID}/alerts/{alert_id}/mentions/{mention_id}'

    update_data = {'archived': True}

    response = requests.put(url, headers=get_headers(), json=update_data)
    return response.json()

# Example: Get and process mentions
mentions = get_mentions(
    alert_id=brand_alert['alert']['id'],
    limit=50,
    sort='published_at',
    unread_only=True
)

print(f"Unread mentions: {mentions['total']}")

for mention in mentions['mentions']:
    print(f"\n{mention['title']}")
    print(f"  Source: {mention['source_name']} ({mention['source_type']})")
    print(f"  Author: {mention['author_name']}")
    print(f"  Reach: {mention.get('reach', 0):,}")
    print(f"  Tone: {mention.get('tone', 'neutral')}")
```

### 3. Real-time Monitoring and Alerts

```python
# Get recent mentions (real-time)
def get_recent_mentions(alert_id, since_datetime=None, limit=50):
    """
    Get mentions since a specific time (for real-time monitoring)

    Args:
        alert_id: Alert ID
        since_datetime: Get mentions since this datetime
        limit: Maximum mentions to return
    """
    url = f'{BASE_URL}/accounts/{ACCOUNT_ID}/alerts/{alert_id}/mentions'

    params = {
        'limit': limit,
        'sort': 'published_at'
    }

    if since_datetime:
        params['since_id'] = since_datetime.isoformat()

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Monitor for high-impact mentions
def monitor_high_impact_mentions(alert_id, min_reach=10000):
    """
    Monitor for mentions with high reach

    Args:
        alert_id: Alert ID
        min_reach: Minimum reach threshold
    """
    mentions = get_mentions(alert_id, limit=100, sort='reach')

    high_impact = [
        m for m in mentions.get('mentions', [])
        if m.get('reach', 0) >= min_reach
    ]

    return high_impact

# Check for crisis signals
def check_crisis_signals(alert_id, hours=24, volume_threshold=50, negative_threshold=60):
    """
    Check for potential crisis situations

    Args:
        alert_id: Alert ID
        hours: Time window to check
        volume_threshold: Mention volume to trigger alert
        negative_threshold: Percentage of negative mentions to trigger alert
    """
    since_time = datetime.now() - timedelta(hours=hours)

    mentions = get_recent_mentions(alert_id, since_datetime=since_time, limit=1000)

    total_mentions = len(mentions.get('mentions', []))

    if total_mentions == 0:
        return {'crisis': False, 'message': 'No mentions in time period'}

    negative_count = sum(
        1 for m in mentions.get('mentions', [])
        if m.get('tone') == 'negative'
    )

    negative_percentage = (negative_count / total_mentions) * 100

    volume_crisis = total_mentions > volume_threshold
    sentiment_crisis = negative_percentage > negative_threshold

    crisis = volume_crisis and sentiment_crisis

    return {
        'crisis': crisis,
        'total_mentions': total_mentions,
        'negative_count': negative_count,
        'negative_percentage': negative_percentage,
        'volume_threshold_exceeded': volume_crisis,
        'sentiment_threshold_exceeded': sentiment_crisis,
        'message': 'Crisis detected!' if crisis else 'No crisis detected'
    }

# Example: Real-time crisis monitoring
crisis_status = check_crisis_signals(
    alert_id=brand_alert['alert']['id'],
    hours=24,
    volume_threshold=100,
    negative_threshold=50
)

if crisis_status['crisis']:
    print("⚠️ CRISIS ALERT!")
    print(f"  Total mentions (24h): {crisis_status['total_mentions']}")
    print(f"  Negative: {crisis_status['negative_percentage']:.1f}%")

    # Get high-impact negative mentions for immediate response
    high_impact = monitor_high_impact_mentions(
        alert_id=brand_alert['alert']['id'],
        min_reach=50000
    )

    print(f"\n  High-impact mentions requiring attention: {len(high_impact)}")
```

### 4. Sentiment Analysis

```python
import pandas as pd

# Get sentiment breakdown
def get_sentiment_breakdown(alert_id, days=30):
    """
    Analyze sentiment distribution

    Args:
        alert_id: Alert ID
        days: Number of days to analyze
    """
    since_time = datetime.now() - timedelta(days=days)

    mentions = get_recent_mentions(alert_id, since_datetime=since_time, limit=1000)

    sentiment_counts = {
        'positive': 0,
        'neutral': 0,
        'negative': 0
    }

    for mention in mentions.get('mentions', []):
        tone = mention.get('tone', 'neutral')
        sentiment_counts[tone] = sentiment_counts.get(tone, 0) + 1

    total = sum(sentiment_counts.values())

    sentiment_analysis = {
        'total_mentions': total,
        'counts': sentiment_counts,
        'percentages': {
            tone: (count / total * 100) if total > 0 else 0
            for tone, count in sentiment_counts.items()
        },
        'net_sentiment': (
            sentiment_counts['positive'] - sentiment_counts['negative']
        ) / total * 100 if total > 0 else 0
    }

    return sentiment_analysis

# Track sentiment over time
def track_sentiment_trend(alert_id, days=30, interval='day'):
    """
    Track how sentiment changes over time

    Args:
        alert_id: Alert ID
        days: Number of days to analyze
        interval: 'day' or 'hour'
    """
    since_time = datetime.now() - timedelta(days=days)

    mentions = get_recent_mentions(alert_id, since_datetime=since_time, limit=5000)

    # Group by time interval
    trend_data = []

    for mention in mentions.get('mentions', []):
        published_at = datetime.fromisoformat(mention['published_at'].replace('Z', '+00:00'))
        tone = mention.get('tone', 'neutral')

        if interval == 'day':
            period = published_at.date()
        else:
            period = published_at.replace(minute=0, second=0, microsecond=0)

        trend_data.append({
            'period': period,
            'tone': tone,
            'reach': mention.get('reach', 0)
        })

    df = pd.DataFrame(trend_data)

    # Aggregate by period
    sentiment_trend = df.groupby(['period', 'tone']).size().unstack(fill_value=0)

    return sentiment_trend

# Identify sentiment drivers
def identify_sentiment_drivers(alert_id, sentiment='negative', days=7):
    """
    Identify what's driving positive or negative sentiment

    Args:
        alert_id: Alert ID
        sentiment: 'positive' or 'negative'
        days: Days to analyze
    """
    since_time = datetime.now() - timedelta(days=days)

    mentions = get_mentions(
        alert_id=alert_id,
        limit=500,
        tone=sentiment
    )

    # Extract common themes
    themes = {}

    for mention in mentions.get('mentions', []):
        title = mention.get('title', '').lower()
        description = mention.get('description', '').lower()

        # Simple keyword extraction (in production, use NLP)
        text = f"{title} {description}"

        # Count word frequency
        words = text.split()
        for word in words:
            if len(word) > 4:  # Filter short words
                themes[word] = themes.get(word, 0) + 1

    # Sort by frequency
    sorted_themes = sorted(themes.items(), key=lambda x: x[1], reverse=True)

    return sorted_themes[:20]  # Top 20 themes

# Example: Sentiment analysis
sentiment = get_sentiment_breakdown(
    alert_id=brand_alert['alert']['id'],
    days=30
)

print("30-Day Sentiment Analysis:")
print(f"  Total Mentions: {sentiment['total_mentions']}")
print(f"  Positive: {sentiment['percentages']['positive']:.1f}%")
print(f"  Neutral: {sentiment['percentages']['neutral']:.1f}%")
print(f"  Negative: {sentiment['percentages']['negative']:.1f}%")
print(f"  Net Sentiment: {sentiment['net_sentiment']:.1f}")

if sentiment['percentages']['negative'] > 30:
    print("\nAnalyzing negative sentiment drivers...")
    drivers = identify_sentiment_drivers(alert_id=brand_alert['alert']['id'])
    print("Top negative themes:")
    for theme, count in drivers[:5]:
        print(f"  - {theme}: {count} mentions")
```

### 5. Source and Channel Analysis

```python
# Get mentions by source
def get_mentions_by_source(alert_id, days=30):
    """
    Analyze which sources mention your brand most

    Args:
        alert_id: Alert ID
        days: Days to analyze
    """
    since_time = datetime.now() - timedelta(days=days)

    mentions = get_recent_mentions(alert_id, since_datetime=since_time, limit=5000)

    source_data = {}

    for mention in mentions.get('mentions', []):
        source_type = mention.get('source_type', 'unknown')
        source_name = mention.get('source_name', 'unknown')

        key = f"{source_type}:{source_name}"

        if key not in source_data:
            source_data[key] = {
                'count': 0,
                'reach': 0,
                'engagement': 0
            }

        source_data[key]['count'] += 1
        source_data[key]['reach'] += mention.get('reach', 0)

    # Convert to DataFrame
    source_list = []
    for key, data in source_data.items():
        source_type, source_name = key.split(':', 1)
        source_list.append({
            'source_type': source_type,
            'source_name': source_name,
            'mentions': data['count'],
            'total_reach': data['reach'],
            'avg_reach': data['reach'] / data['count'] if data['count'] > 0 else 0
        })

    df = pd.DataFrame(source_list)
    return df.sort_values('mentions', ascending=False)

# Get top news sources
def get_top_news_sources(alert_id, days=30, limit=20):
    """Get top news sites mentioning your brand"""
    mentions = get_mentions(
        alert_id=alert_id,
        limit=1000,
        sources=['news']
    )

    news_sources = {}

    for mention in mentions.get('mentions', []):
        source = mention.get('source_name', 'Unknown')

        if source not in news_sources:
            news_sources[source] = {
                'count': 0,
                'reach': 0,
                'tone': {'positive': 0, 'neutral': 0, 'negative': 0}
            }

        news_sources[source]['count'] += 1
        news_sources[source]['reach'] += mention.get('reach', 0)

        tone = mention.get('tone', 'neutral')
        news_sources[source]['tone'][tone] += 1

    # Convert to list and sort
    source_list = [
        {
            'source': source,
            'mentions': data['count'],
            'total_reach': data['reach'],
            'sentiment': max(data['tone'], key=data['tone'].get)
        }
        for source, data in news_sources.items()
    ]

    return sorted(source_list, key=lambda x: x['mentions'], reverse=True)[:limit]

# Example: Source analysis
source_analysis = get_mentions_by_source(
    alert_id=brand_alert['alert']['id'],
    days=30
)

print("Top Sources (30 days):")
print(source_analysis.head(10))

print("\nTop News Sources:")
news_sources = get_top_news_sources(alert_id=brand_alert['alert']['id'])
for source in news_sources[:5]:
    print(f"  {source['source']}: {source['mentions']} mentions ({source['sentiment']} sentiment)")
```

### 6. Influencer and Author Analysis

```python
# Get top authors
def get_top_authors(alert_id, days=30, min_reach=1000, limit=50):
    """
    Identify influential authors mentioning your brand

    Args:
        alert_id: Alert ID
        days: Days to analyze
        min_reach: Minimum author reach
        limit: Number of authors to return
    """
    since_time = datetime.now() - timedelta(days=days)

    mentions = get_recent_mentions(alert_id, since_datetime=since_time, limit=5000)

    author_data = {}

    for mention in mentions.get('mentions', []):
        author_name = mention.get('author_name', 'Unknown')
        author_reach = mention.get('author_influence', {}).get('reach', 0)

        if author_reach < min_reach:
            continue

        if author_name not in author_data:
            author_data[author_name] = {
                'mentions': 0,
                'reach': author_reach,
                'tone': {'positive': 0, 'neutral': 0, 'negative': 0},
                'sources': set()
            }

        author_data[author_name]['mentions'] += 1

        tone = mention.get('tone', 'neutral')
        author_data[author_name]['tone'][tone] += 1

        author_data[author_name]['sources'].add(mention.get('source_type', 'unknown'))

    # Convert to list
    author_list = []
    for author, data in author_data.items():
        dominant_tone = max(data['tone'], key=data['tone'].get)

        author_list.append({
            'author': author,
            'reach': data['reach'],
            'mentions': data['mentions'],
            'sentiment': dominant_tone,
            'sources': ', '.join(data['sources'])
        })

    df = pd.DataFrame(author_list)
    return df.sort_values('reach', ascending=False).head(limit)

# Find potential brand advocates
def find_brand_advocates(alert_id, days=30, min_positive_mentions=3):
    """
    Identify potential brand advocates (positive mentions)

    Args:
        alert_id: Alert ID
        days: Days to analyze
        min_positive_mentions: Minimum positive mentions to be considered advocate
    """
    since_time = datetime.now() - timedelta(days=days)

    mentions = get_mentions(alert_id=alert_id, limit=5000, tone='positive')

    advocates = {}

    for mention in mentions.get('mentions', []):
        author_name = mention.get('author_name')
        author_reach = mention.get('author_influence', {}).get('reach', 0)

        if not author_name:
            continue

        if author_name not in advocates:
            advocates[author_name] = {
                'positive_mentions': 0,
                'reach': author_reach,
                'contact': mention.get('author_url', '')
            }

        advocates[author_name]['positive_mentions'] += 1

    # Filter by minimum mentions
    advocate_list = [
        {
            'author': author,
            'positive_mentions': data['positive_mentions'],
            'reach': data['reach'],
            'contact': data['contact']
        }
        for author, data in advocates.items()
        if data['positive_mentions'] >= min_positive_mentions
    ]

    df = pd.DataFrame(advocate_list)
    return df.sort_values('reach', ascending=False) if len(df) > 0 else df

# Example: Influencer analysis
influencers = get_top_authors(
    alert_id=brand_alert['alert']['id'],
    days=30,
    min_reach=10000
)

print("Top Influencers (30 days):")
print(influencers[['author', 'reach', 'mentions', 'sentiment']].head(10))

advocates = find_brand_advocates(
    alert_id=brand_alert['alert']['id'],
    days=30,
    min_positive_mentions=3
)

print(f"\nFound {len(advocates)} potential brand advocates")
```

### 7. Competitive Analysis

```python
# Compare multiple alerts (brands)
def compare_brands(alert_ids, alert_names, days=30):
    """
    Compare mention volume and sentiment across multiple brands

    Args:
        alert_ids: List of alert IDs
        alert_names: List of brand names (same order as alert_ids)
        days: Days to analyze
    """
    comparison_data = []

    for alert_id, name in zip(alert_ids, alert_names):
        sentiment = get_sentiment_breakdown(alert_id, days=days)

        comparison_data.append({
            'brand': name,
            'mentions': sentiment['total_mentions'],
            'positive_pct': sentiment['percentages']['positive'],
            'neutral_pct': sentiment['percentages']['neutral'],
            'negative_pct': sentiment['percentages']['negative'],
            'net_sentiment': sentiment['net_sentiment']
        })

    df = pd.DataFrame(comparison_data)
    return df.sort_values('mentions', ascending=False)

# Share of voice analysis
def calculate_share_of_voice(alert_ids, alert_names, days=30):
    """
    Calculate share of voice for each brand

    Args:
        alert_ids: List of alert IDs
        alert_names: List of brand names
        days: Days to analyze
    """
    total_mentions = 0
    brand_mentions = {}

    for alert_id, name in zip(alert_ids, alert_names):
        sentiment = get_sentiment_breakdown(alert_id, days=days)
        mentions = sentiment['total_mentions']

        brand_mentions[name] = mentions
        total_mentions += mentions

    share_of_voice = {
        brand: (mentions / total_mentions * 100) if total_mentions > 0 else 0
        for brand, mentions in brand_mentions.items()
    }

    return share_of_voice

# Example: Competitive analysis
competitor_alerts = {
    'Your Brand': brand_alert['alert']['id'],
    'Competitor A': 'competitor_a_alert_id',
    'Competitor B': 'competitor_b_alert_id'
}

comparison = compare_brands(
    alert_ids=list(competitor_alerts.values()),
    alert_names=list(competitor_alerts.keys()),
    days=30
)

print("Competitive Analysis (30 days):")
print(comparison)

sov = calculate_share_of_voice(
    alert_ids=list(competitor_alerts.values()),
    alert_names=list(competitor_alerts.keys()),
    days=30
)

print("\nShare of Voice:")
for brand, percentage in sov.items():
    print(f"  {brand}: {percentage:.1f}%")
```

## Installation

```bash
# Using requests for REST API
uv pip install requests pandas

# Optional: For NLP and advanced analysis
uv pip install nltk textblob
```

## Authentication

Mention uses OAuth 2.0 or API token authentication:

### API Token (Simpler)

```python
ACCESS_TOKEN = 'your-mention-api-token'
ACCOUNT_ID = 'your-account-id'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}
```

### OAuth 2.0 (Production)

```python
import requests

CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'

# Get access token
def get_access_token(authorization_code):
    url = 'https://api.mention.com/oauth/token'

    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(url, data=data)
    return response.json()['access_token']
```

## Quick Start

```python
import requests
from datetime import datetime, timedelta

# Configure API
ACCESS_TOKEN = 'your-mention-api-token'
ACCOUNT_ID = 'your-account-id'
BASE_URL = 'https://api.mention.com/api/v2'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

# 1. Create a brand monitoring alert
alert_data = {
    'name': 'My Brand',
    'primary_keyword': 'YourBrand',
    'query': {
        'type': 'boolean',
        'included_keywords': ['YourBrand', '@YourBrand', '#YourBrand'],
        'excluded_keywords': ['spam']
    },
    'languages': ['en']
}

response = requests.post(
    f'{BASE_URL}/accounts/{ACCOUNT_ID}/alerts',
    headers=headers,
    json=alert_data
)

alert = response.json()
alert_id = alert['alert']['id']
print(f"Alert created: {alert_id}")

# 2. Get recent mentions
response = requests.get(
    f'{BASE_URL}/accounts/{ACCOUNT_ID}/alerts/{alert_id}/mentions',
    headers=headers,
    params={'limit': 20, 'unread': 'true'}
)

mentions = response.json()
print(f"\nUnread mentions: {mentions['total']}")

# 3. Process mentions
for mention in mentions['mentions'][:5]:
    print(f"\n{mention['title']}")
    print(f"  Source: {mention['source_name']}")
    print(f"  Sentiment: {mention.get('tone', 'neutral')}")
    print(f"  Reach: {mention.get('reach', 0):,}")
```

## Key Metrics

### Mention Metrics
- **Mention Volume**: Total mentions over time
- **Reach**: Potential audience size
- **Engagement**: Likes, shares, comments
- **Source Distribution**: Where mentions occur

### Sentiment Metrics
- **Tone**: Positive, neutral, negative classification
- **Net Sentiment**: (Positive - Negative) / Total
- **Sentiment Trend**: Changes over time
- **Sentiment by Source**: Sentiment variation across channels

### Author Metrics
- **Author Reach**: Follower/subscriber count
- **Author Influence**: Overall influence score
- **Top Authors**: Most frequent mentioners
- **Brand Advocates**: Authors with positive mentions

### Competitive Metrics
- **Share of Voice**: Your mentions vs. competitors
- **Sentiment Comparison**: Comparative sentiment analysis
- **Source Analysis**: Where competitors are mentioned

## Best Practices

1. **Comprehensive Keywords**: Include brand variations, common misspellings, hashtags
2. **Exclude Noise**: Filter spam, bots, and irrelevant content
3. **Real-Time Monitoring**: Check mentions hourly during business hours
4. **Prioritize by Reach**: Address high-reach mentions first
5. **Quick Response**: Respond to mentions within 1 hour
6. **Track Sentiment**: Monitor for negative sentiment spikes
7. **Identify Influencers**: Build relationships with frequent positive mentioners
8. **Competitive Intelligence**: Track 3-5 main competitors consistently

## References

- [Mention API Documentation](https://dev.mention.com/current/)
- [Authentication Guide](https://dev.mention.com/current/authentication/)
- [Alerts API](https://dev.mention.com/current/alerts/)
- [Mentions API](https://dev.mention.com/current/mentions/)
- [Mention Help Center](https://help.mention.com/)
- [Best Practices Guide](https://mention.com/en/blog/social-media-monitoring-best-practices/)
- [API Rate Limits](https://dev.mention.com/current/rate-limiting/)

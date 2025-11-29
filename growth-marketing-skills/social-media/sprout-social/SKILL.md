---
name: sprout-social
description: "Social media management and analytics. Publishing, engagement, listening, analytics, team collaboration, customer care, competitive analysis."
---

# Sprout Social Integration

## Overview

Sprout Social is an enterprise-grade social media management and analytics platform that provides deep insights, advanced publishing capabilities, and robust team collaboration features. This skill covers using the Sprout Social API for content publishing, social listening, analytics reporting, customer care, and competitive intelligence across all major social networks.

## When to Use This Skill

- Enterprise social media management across teams
- Advanced social analytics and reporting
- Social customer care and response management
- Social listening and sentiment analysis
- Competitive social media analysis
- Influencer identification and tracking
- Cross-platform publishing and scheduling
- Team collaboration and workflow management

## Core Capabilities

### 1. Profile Management

```python
import requests
import json
from datetime import datetime, timedelta

# Sprout Social API configuration
ACCESS_TOKEN = 'your-sprout-social-access-token'
BASE_URL = 'https://api.sproutsocial.com/v1'

# Headers for all requests
def get_headers():
    return {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

# Get customer profiles (social accounts)
def get_customer_profiles():
    url = f'{BASE_URL}/customer_profiles'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Get specific profile details
def get_profile(profile_id):
    url = f'{BASE_URL}/customer_profiles/{profile_id}'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Get profile analytics summary
def get_profile_summary(profile_id):
    url = f'{BASE_URL}/analytics/profiles/{profile_id}/summary'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Example usage
profiles = get_customer_profiles()

print("Connected social profiles:")
for profile in profiles.get('data', []):
    print(f"  - {profile['network_type']}: {profile['customer_name']}")
    print(f"    ID: {profile['id']}")
    print(f"    Followers: {profile.get('follower_count', 'N/A')}")
```

### 2. Publishing and Scheduling

```python
# Create a post
def create_post(profile_ids, text, send_time=None, media_urls=None, link_url=None):
    """
    Create and schedule a social media post

    Args:
        profile_ids: List of Sprout customer profile IDs
        text: Post content
        send_time: datetime for scheduled post (None for immediate)
        media_urls: List of image/video URLs
        link_url: URL to attach to post
    """
    url = f'{BASE_URL}/publishing/posts'

    post_data = {
        'content': text,
        'customer_profile_ids': profile_ids
    }

    # Schedule or publish now
    if send_time:
        post_data['send_time'] = send_time.isoformat()
        post_data['send_status'] = 'SCHEDULED'
    else:
        post_data['send_status'] = 'SEND_NOW'

    # Add media attachments
    if media_urls:
        post_data['media_urls'] = media_urls

    # Add link
    if link_url:
        post_data['link_url'] = link_url

    response = requests.post(url, headers=get_headers(), json=post_data)
    return response.json()

# Schedule post with optimal timing
def schedule_with_optimal_time(profile_ids, text, target_date=None):
    """
    Schedule post using Sprout's optimal send time feature

    Args:
        profile_ids: List of profile IDs
        text: Post content
        target_date: Target date (will use optimal time on that date)
    """
    # Get optimal send times for profiles
    optimal_times = get_optimal_send_times(profile_ids)

    # Use the best time
    if optimal_times and target_date:
        best_time = optimal_times[0]
        send_time = target_date.replace(
            hour=best_time['hour'],
            minute=best_time['minute']
        )
    else:
        send_time = None

    return create_post(profile_ids, text, send_time=send_time)

# Get optimal send times
def get_optimal_send_times(profile_ids):
    """Get recommended posting times based on audience engagement"""
    url = f'{BASE_URL}/analytics/optimal_send_times'

    params = {'customer_profile_ids': ','.join(map(str, profile_ids))}

    response = requests.get(url, headers=get_headers(), params=params)
    data = response.json()

    return data.get('optimal_times', [])

# Bulk schedule posts
def bulk_schedule_posts(posts_data):
    """
    Schedule multiple posts at once

    posts_data format: [
        {
            'profile_ids': [123, 456],
            'text': 'Post content',
            'send_time': datetime_obj,
            'media_urls': ['url1', 'url2']
        },
        ...
    ]
    """
    results = []

    for post in posts_data:
        result = create_post(
            profile_ids=post['profile_ids'],
            text=post['text'],
            send_time=post.get('send_time'),
            media_urls=post.get('media_urls'),
            link_url=post.get('link_url')
        )
        results.append(result)

    return results

# Example: Schedule a post
tomorrow_10am = datetime.now() + timedelta(days=1)
tomorrow_10am = tomorrow_10am.replace(hour=10, minute=0, second=0)

post = create_post(
    profile_ids=[123, 456],  # Twitter and LinkedIn
    text='Excited to share our Q1 results! 📊 Record growth across all metrics. #BusinessUpdate',
    send_time=tomorrow_10am,
    link_url='https://example.com/q1-results'
)

print(f"Post scheduled: {post['id']}")
```

### 3. Post Management

```python
# Get scheduled posts
def get_scheduled_posts(profile_ids=None, start_date=None, end_date=None):
    url = f'{BASE_URL}/publishing/posts'

    params = {'send_status': 'SCHEDULED'}

    if profile_ids:
        params['customer_profile_ids'] = ','.join(map(str, profile_ids))
    if start_date:
        params['start_date'] = start_date.isoformat()
    if end_date:
        params['end_date'] = end_date.isoformat()

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Get sent posts
def get_sent_posts(profile_ids, days=30):
    url = f'{BASE_URL}/publishing/posts'

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    params = {
        'send_status': 'SENT',
        'customer_profile_ids': ','.join(map(str, profile_ids)),
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat()
    }

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Update scheduled post
def update_post(post_id, text=None, send_time=None):
    url = f'{BASE_URL}/publishing/posts/{post_id}'

    update_data = {}

    if text:
        update_data['content'] = text
    if send_time:
        update_data['send_time'] = send_time.isoformat()

    response = requests.patch(url, headers=get_headers(), json=update_data)
    return response.json()

# Delete post
def delete_post(post_id):
    url = f'{BASE_URL}/publishing/posts/{post_id}'

    response = requests.delete(url, headers=get_headers())
    return response.status_code == 204

# Get post details with analytics
def get_post_details(post_id):
    url = f'{BASE_URL}/publishing/posts/{post_id}'

    response = requests.get(url, headers=get_headers())
    return response.json()
```

### 4. Social Listening and Monitoring

```python
# Search social mentions
def search_mentions(keywords, networks=None, start_date=None, limit=100):
    """
    Search for mentions of keywords across social networks

    Args:
        keywords: List of keywords/hashtags to search
        networks: List of networks to search (twitter, facebook, etc.)
        start_date: Start date for search
        limit: Maximum results to return
    """
    url = f'{BASE_URL}/listening/messages'

    params = {
        'query': ' OR '.join(keywords),
        'limit': limit
    }

    if networks:
        params['networks'] = ','.join(networks)
    if start_date:
        params['start_date'] = start_date.isoformat()

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Get brand mentions
def get_brand_mentions(brand_terms, days=7):
    """Track all mentions of your brand"""
    start_date = datetime.now() - timedelta(days=days)

    mentions = search_mentions(
        keywords=brand_terms,
        start_date=start_date,
        limit=500
    )

    return mentions.get('data', [])

# Analyze sentiment
def analyze_sentiment(messages):
    """
    Analyze sentiment of social messages

    Returns: Sentiment breakdown and trends
    """
    sentiment_counts = {
        'positive': 0,
        'neutral': 0,
        'negative': 0
    }

    for message in messages:
        sentiment = message.get('sentiment', 'neutral')
        sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1

    total = sum(sentiment_counts.values())

    sentiment_analysis = {
        'total_messages': total,
        'counts': sentiment_counts,
        'percentages': {
            sentiment: (count / total * 100) if total > 0 else 0
            for sentiment, count in sentiment_counts.items()
        }
    }

    return sentiment_analysis

# Monitor competitors
def monitor_competitors(competitor_handles, days=30):
    """
    Track competitor social media activity

    Args:
        competitor_handles: List of competitor social handles
        days: Days of history to analyze
    """
    competitor_data = []

    for handle in competitor_handles:
        mentions = search_mentions(
            keywords=[handle],
            start_date=datetime.now() - timedelta(days=days)
        )

        activity_data = {
            'handle': handle,
            'total_posts': len(mentions.get('data', [])),
            'engagement': sum(
                msg.get('engagement_count', 0)
                for msg in mentions.get('data', [])
            ),
            'sentiment': analyze_sentiment(mentions.get('data', []))
        }

        competitor_data.append(activity_data)

    return competitor_data

# Example: Monitor brand and competitors
brand_mentions = get_brand_mentions(
    brand_terms=['@YourBrand', '#YourBrand', 'Your Company'],
    days=7
)

print(f"Brand mentions in last 7 days: {len(brand_mentions)}")

sentiment = analyze_sentiment(brand_mentions)
print(f"Sentiment breakdown:")
for sent, pct in sentiment['percentages'].items():
    print(f"  {sent}: {pct:.1f}%")
```

### 5. Analytics and Reporting

```python
import pandas as pd

# Get profile analytics
def get_profile_analytics(profile_id, start_date, end_date, metrics=None):
    """
    Get detailed analytics for a social profile

    Args:
        profile_id: Sprout customer profile ID
        start_date: Start date for analytics
        end_date: End date for analytics
        metrics: List of metrics to retrieve
    """
    url = f'{BASE_URL}/analytics/profiles/{profile_id}'

    params = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }

    if metrics:
        params['metrics'] = ','.join(metrics)

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Get post performance analytics
def get_post_analytics(post_ids):
    """Get engagement metrics for specific posts"""
    analytics = []

    for post_id in post_ids:
        url = f'{BASE_URL}/analytics/posts/{post_id}'
        response = requests.get(url, headers=get_headers())
        analytics.append(response.json())

    return analytics

# Generate engagement report
def generate_engagement_report(profile_ids, days=30):
    """
    Generate comprehensive engagement report

    Returns: DataFrame with engagement metrics
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    report_data = []

    for profile_id in profile_ids:
        analytics = get_profile_analytics(profile_id, start_date, end_date)

        metrics = analytics.get('metrics', {})

        report_data.append({
            'profile_id': profile_id,
            'profile_name': analytics.get('profile_name'),
            'network': analytics.get('network_type'),
            'posts': metrics.get('posts_sent', 0),
            'impressions': metrics.get('impressions', 0),
            'engagements': metrics.get('engagements', 0),
            'engagement_rate': metrics.get('engagement_rate', 0),
            'clicks': metrics.get('link_clicks', 0),
            'followers_gained': metrics.get('followers_gained', 0),
            'followers_lost': metrics.get('followers_lost', 0),
            'net_follower_growth': metrics.get('net_follower_growth', 0)
        })

    df = pd.DataFrame(report_data)
    return df

# Get competitive benchmarks
def get_competitive_benchmarks(profile_ids, competitor_ids, days=30):
    """
    Compare your performance against competitors

    Returns: Comparative analytics
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Get your analytics
    your_analytics = []
    for pid in profile_ids:
        analytics = get_profile_analytics(pid, start_date, end_date)
        your_analytics.append(analytics)

    # Get competitor analytics
    competitor_analytics = []
    for cid in competitor_ids:
        analytics = get_profile_analytics(cid, start_date, end_date)
        competitor_analytics.append(analytics)

    # Calculate benchmarks
    comparison = {
        'your_avg_engagement_rate': sum(
            a.get('metrics', {}).get('engagement_rate', 0)
            for a in your_analytics
        ) / len(your_analytics) if your_analytics else 0,
        'competitor_avg_engagement_rate': sum(
            a.get('metrics', {}).get('engagement_rate', 0)
            for a in competitor_analytics
        ) / len(competitor_analytics) if competitor_analytics else 0,
        'your_total_followers': sum(
            a.get('metrics', {}).get('followers', 0)
            for a in your_analytics
        ),
        'competitor_avg_followers': sum(
            a.get('metrics', {}).get('followers', 0)
            for a in competitor_analytics
        ) / len(competitor_analytics) if competitor_analytics else 0
    }

    return comparison

# Example: Generate monthly report
report = generate_engagement_report(
    profile_ids=[123, 456, 789],
    days=30
)

print("30-Day Social Media Report:")
print(report)

print(f"\nSummary:")
print(f"Total Posts: {report['posts'].sum()}")
print(f"Total Impressions: {report['impressions'].sum():,}")
print(f"Avg Engagement Rate: {report['engagement_rate'].mean():.2f}%")
print(f"Net Follower Growth: {report['net_follower_growth'].sum():,}")
```

### 6. Customer Care and Response Management

```python
# Get inbound messages
def get_inbound_messages(profile_ids, start_date=None, limit=100):
    """Get messages requiring response"""
    url = f'{BASE_URL}/messages/inbound'

    params = {
        'customer_profile_ids': ','.join(map(str, profile_ids)),
        'limit': limit
    }

    if start_date:
        params['start_date'] = start_date.isoformat()

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Reply to message
def reply_to_message(message_id, reply_text):
    """Send a reply to an inbound message"""
    url = f'{BASE_URL}/messages/{message_id}/reply'

    reply_data = {'content': reply_text}

    response = requests.post(url, headers=get_headers(), json=reply_data)
    return response.json()

# Tag message
def tag_message(message_id, tags):
    """Add tags to message for organization"""
    url = f'{BASE_URL}/messages/{message_id}/tags'

    tag_data = {'tags': tags}

    response = requests.post(url, headers=get_headers(), json=tag_data)
    return response.json()

# Assign message to team member
def assign_message(message_id, user_id):
    """Assign message to team member for response"""
    url = f'{BASE_URL}/messages/{message_id}/assign'

    assignment_data = {'user_id': user_id}

    response = requests.post(url, headers=get_headers(), json=assignment_data)
    return response.json()

# Calculate response metrics
def calculate_response_metrics(profile_ids, days=30):
    """
    Calculate customer care response metrics

    Returns: Response time, resolution rate, etc.
    """
    start_date = datetime.now() - timedelta(days=days)
    messages = get_inbound_messages(profile_ids, start_date=start_date)

    total_messages = len(messages.get('data', []))
    responded = sum(
        1 for msg in messages.get('data', [])
        if msg.get('response_status') == 'RESPONDED'
    )

    response_times = [
        msg.get('response_time_minutes', 0)
        for msg in messages.get('data', [])
        if msg.get('response_time_minutes')
    ]

    metrics = {
        'total_messages': total_messages,
        'responded': responded,
        'response_rate': (responded / total_messages * 100) if total_messages > 0 else 0,
        'avg_response_time': sum(response_times) / len(response_times) if response_times else 0,
        'pending': total_messages - responded
    }

    return metrics

# Example: Customer care dashboard
care_metrics = calculate_response_metrics(
    profile_ids=[123, 456],
    days=7
)

print("Customer Care Metrics (7 days):")
print(f"  Total Messages: {care_metrics['total_messages']}")
print(f"  Response Rate: {care_metrics['response_rate']:.1f}%")
print(f"  Avg Response Time: {care_metrics['avg_response_time']:.0f} minutes")
print(f"  Pending Responses: {care_metrics['pending']}")
```

## Installation

```bash
# Using requests for REST API
uv pip install requests pandas

# Optional: For advanced analytics and visualization
uv pip install matplotlib seaborn plotly
```

## Authentication

Sprout Social uses OAuth 2.0 for API authentication:

```python
import requests

CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
REDIRECT_URI = 'https://your-app.com/callback'

# Step 1: Get authorization URL
auth_url = (
    f'https://sproutsocial.com/oauth/authorize'
    f'?client_id={CLIENT_ID}'
    f'&redirect_uri={REDIRECT_URI}'
    f'&response_type=code'
)

# Step 2: Exchange authorization code for access token
def get_access_token(authorization_code):
    url = 'https://api.sproutsocial.com/oauth/token'

    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(url, data=data)
    token_data = response.json()

    return {
        'access_token': token_data['access_token'],
        'refresh_token': token_data.get('refresh_token'),
        'expires_in': token_data['expires_in']
    }

# Step 3: Refresh token when expired
def refresh_token(refresh_token):
    url = 'https://api.sproutsocial.com/oauth/token'

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(url, data=data)
    return response.json()
```

## Quick Start

```python
import requests
from datetime import datetime, timedelta

# Configure API
ACCESS_TOKEN = 'your-sprout-social-access-token'
BASE_URL = 'https://api.sproutsocial.com/v1'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

# 1. Get your social profiles
response = requests.get(f'{BASE_URL}/customer_profiles', headers=headers)
profiles = response.json()

print("Your social profiles:")
for profile in profiles.get('data', []):
    print(f"  - {profile['network_type']}: {profile['customer_name']}")

# 2. Schedule a post
profile_id = profiles['data'][0]['id']
tomorrow = datetime.now() + timedelta(days=1)

post_data = {
    'content': 'Hello from Sprout Social API! 🌱',
    'customer_profile_ids': [profile_id],
    'send_time': tomorrow.isoformat(),
    'send_status': 'SCHEDULED'
}

response = requests.post(
    f'{BASE_URL}/publishing/posts',
    headers=headers,
    json=post_data
)

if response.status_code == 201:
    post = response.json()
    print(f"\nPost scheduled successfully!")
    print(f"Post ID: {post['id']}")

# 3. Get analytics
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

response = requests.get(
    f'{BASE_URL}/analytics/profiles/{profile_id}',
    headers=headers,
    params={
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }
)

analytics = response.json()
print(f"\n30-Day Analytics:")
print(f"  Posts: {analytics['metrics'].get('posts_sent', 0)}")
print(f"  Engagement Rate: {analytics['metrics'].get('engagement_rate', 0):.2f}%")
```

## Key Metrics

### Engagement Metrics
- **Impressions**: Times content was displayed
- **Reach**: Unique users who saw content
- **Engagements**: Total interactions (likes, comments, shares, clicks)
- **Engagement Rate**: (Engagements / Impressions) × 100
- **Clicks**: Link clicks and profile clicks

### Audience Metrics
- **Follower Count**: Total followers
- **Follower Growth**: Net change in followers
- **Audience Demographics**: Age, gender, location breakdown
- **Audience Activity**: When followers are most active

### Performance Metrics
- **Post Performance**: Individual post analytics
- **Best Performing Content**: Top posts by engagement
- **Optimal Send Times**: Best times to post
- **Response Time**: Average time to respond to messages
- **Response Rate**: Percentage of messages responded to

## Best Practices

1. **Data-Driven Posting**: Use optimal send times based on audience activity
2. **Consistent Publishing**: Maintain regular posting schedule
3. **Social Listening**: Monitor brand mentions and industry trends daily
4. **Quick Responses**: Respond to customer messages within 1 hour
5. **Competitive Intelligence**: Track competitor performance monthly
6. **Team Collaboration**: Use assignments and tags for workflow management
7. **Regular Reporting**: Review analytics weekly, report monthly
8. **Sentiment Monitoring**: Track brand sentiment to identify issues early

## References

- [Sprout Social API Documentation](https://api.sproutsocial.com/docs/)
- [Authentication Guide](https://api.sproutsocial.com/docs/authentication)
- [Publishing API](https://api.sproutsocial.com/docs/publishing)
- [Analytics API](https://api.sproutsocial.com/docs/analytics)
- [Listening API](https://api.sproutsocial.com/docs/listening)
- [Messages API](https://api.sproutsocial.com/docs/messages)
- [Sprout Social Help Docs](https://support.sproutsocial.com/)

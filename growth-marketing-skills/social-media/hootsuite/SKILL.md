---
name: hootsuite
description: "Social media management platform. Schedule posts, monitor conversations, team collaboration, analytics dashboards, social listening, multi-account management."
---

# Hootsuite Integration

## Overview

Hootsuite is a comprehensive social media management platform that enables scheduling, monitoring, and analyzing social media content across multiple networks. This skill covers using the Hootsuite API to manage posts, monitor social conversations, collaborate with teams, and generate analytics reports across platforms including Twitter, Facebook, Instagram, LinkedIn, and YouTube.

## When to Use This Skill

- Managing multiple social media accounts from one platform
- Scheduling and publishing content across networks
- Monitoring brand mentions and social conversations
- Team collaboration on social media content
- Social media analytics and reporting
- Social listening and sentiment analysis
- Managing social media campaigns
- Responding to messages and comments centrally

## Core Capabilities

### 1. Profile and Account Management

```python
import requests
import json

# Hootsuite API configuration
ACCESS_TOKEN = 'your-hootsuite-access-token'
BASE_URL = 'https://platform.hootsuite.com/v1'

# Headers for all requests
def get_headers():
    return {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

# Get organization information
def get_organization():
    url = f'{BASE_URL}/me'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Get social media profiles
def get_social_profiles():
    url = f'{BASE_URL}/socialProfiles'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Get specific social profile
def get_profile(profile_id):
    url = f'{BASE_URL}/socialProfiles/{profile_id}'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Example usage
org = get_organization()
print(f"Organization: {org.get('fullName', 'N/A')}")

profiles = get_social_profiles()
print(f"\nConnected social profiles:")
for profile in profiles.get('data', []):
    print(f"  - {profile['type']}: {profile.get('socialNetworkUsername', 'N/A')}")
    print(f"    ID: {profile['id']}")
```

### 2. Message Scheduling and Publishing

```python
from datetime import datetime, timedelta

# Create a scheduled message
def create_scheduled_message(profile_id, text, scheduled_time=None, media_urls=None):
    url = f'{BASE_URL}/messages'

    # Build message data
    message_data = {
        'text': text,
        'socialProfileIds': [profile_id]
    }

    # Add scheduled time if provided
    if scheduled_time:
        message_data['scheduledSendTime'] = scheduled_time.isoformat()

    # Add media attachments
    if media_urls:
        message_data['media'] = [
            {'url': url} for url in media_urls
        ]

    response = requests.post(
        url,
        headers=get_headers(),
        json=message_data
    )

    return response.json()

# Publish message immediately
def publish_now(profile_ids, text, media_urls=None):
    """Publish message immediately to specified profiles"""
    message_data = {
        'text': text,
        'socialProfileIds': profile_ids
    }

    if media_urls:
        message_data['media'] = [
            {'url': url} for url in media_urls
        ]

    url = f'{BASE_URL}/messages'
    response = requests.post(url, headers=get_headers(), json=message_data)

    return response.json()

# Schedule to multiple profiles
def schedule_multi_platform(profile_ids, text, scheduled_time, tags=None):
    """
    Schedule same content to multiple social profiles

    Args:
        profile_ids: List of Hootsuite social profile IDs
        text: Message content
        scheduled_time: datetime object
        tags: List of tag IDs for organization
    """
    message_data = {
        'text': text,
        'socialProfileIds': profile_ids,
        'scheduledSendTime': scheduled_time.isoformat()
    }

    if tags:
        message_data['tags'] = tags

    url = f'{BASE_URL}/messages'
    response = requests.post(url, headers=get_headers(), json=message_data)

    if response.status_code == 201:
        result = response.json()
        print(f"Message scheduled for {scheduled_time}")
        print(f"Message ID: {result.get('id')}")
        return result
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Example: Schedule a post for tomorrow
tomorrow = datetime.now() + timedelta(days=1)
tomorrow = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)

message = create_scheduled_message(
    profile_id='twitter_profile_id',
    text='Excited to announce our latest feature! 🚀 #ProductUpdate',
    scheduled_time=tomorrow,
    media_urls=['https://example.com/image.jpg']
)

print(f"Scheduled message: {message}")
```

### 3. Message Management

```python
# Get scheduled messages
def get_scheduled_messages(start_time=None, end_time=None, limit=50):
    url = f'{BASE_URL}/messages'

    params = {
        'state': 'SCHEDULED',
        'limit': limit
    }

    if start_time:
        params['startTime'] = start_time.isoformat()
    if end_time:
        params['endTime'] = end_time.isoformat()

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Get sent messages
def get_sent_messages(limit=50):
    url = f'{BASE_URL}/messages'

    params = {
        'state': 'SENT',
        'limit': limit
    }

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Update scheduled message
def update_message(message_id, text=None, scheduled_time=None):
    url = f'{BASE_URL}/messages/{message_id}'

    update_data = {}

    if text:
        update_data['text'] = text
    if scheduled_time:
        update_data['scheduledSendTime'] = scheduled_time.isoformat()

    response = requests.put(url, headers=get_headers(), json=update_data)
    return response.json()

# Delete scheduled message
def delete_message(message_id):
    url = f'{BASE_URL}/messages/{message_id}'

    response = requests.delete(url, headers=get_headers())
    return response.status_code == 204

# Get message details
def get_message(message_id):
    url = f'{BASE_URL}/messages/{message_id}'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Example: Manage scheduled messages
scheduled = get_scheduled_messages(limit=10)

print(f"Scheduled messages: {len(scheduled.get('data', []))}")
for msg in scheduled.get('data', []):
    print(f"  - {msg['text'][:50]}...")
    print(f"    Scheduled: {msg.get('scheduledSendTime')}")
    print(f"    ID: {msg['id']}")
```

### 4. Social Listening and Monitoring

```python
# Create a stream for monitoring
def create_stream(name, profile_ids, keywords=None):
    """
    Create a monitoring stream for specific keywords or profiles

    Args:
        name: Stream name
        profile_ids: List of social profile IDs to monitor
        keywords: List of keywords/hashtags to track
    """
    url = f'{BASE_URL}/streams'

    stream_data = {
        'name': name,
        'socialProfileIds': profile_ids
    }

    if keywords:
        stream_data['keywords'] = keywords

    response = requests.post(url, headers=get_headers(), json=stream_data)
    return response.json()

# Get streams
def get_streams():
    url = f'{BASE_URL}/streams'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Get messages from stream
def get_stream_messages(stream_id, limit=50):
    url = f'{BASE_URL}/streams/{stream_id}/messages'

    params = {'limit': limit}

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Monitor brand mentions
def monitor_brand_mentions(brand_keywords, profile_ids):
    """
    Monitor mentions of brand keywords across social profiles

    Returns: List of messages mentioning the brand
    """
    mentions = []

    for keyword in brand_keywords:
        stream = create_stream(
            name=f'Brand Monitor - {keyword}',
            profile_ids=profile_ids,
            keywords=[keyword]
        )

        if stream.get('id'):
            messages = get_stream_messages(stream['id'])
            mentions.extend(messages.get('data', []))

    return mentions

# Example: Monitor brand mentions
brand_mentions = monitor_brand_mentions(
    brand_keywords=['@YourBrand', '#YourBrand', 'Your Company Name'],
    profile_ids=['twitter_profile_id', 'facebook_profile_id']
)

print(f"Found {len(brand_mentions)} brand mentions")
```

### 5. Analytics and Reporting

```python
import pandas as pd

# Get message statistics
def get_message_stats(message_id):
    url = f'{BASE_URL}/messages/{message_id}/statistics'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Get profile analytics
def get_profile_analytics(profile_id, start_date, end_date):
    url = f'{BASE_URL}/socialProfiles/{profile_id}/analytics'

    params = {
        'startDate': start_date.isoformat(),
        'endDate': end_date.isoformat()
    }

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Analyze message performance
def analyze_message_performance(messages):
    """
    Analyze performance metrics for a list of messages

    Returns: DataFrame with engagement metrics
    """
    performance_data = []

    for message in messages:
        stats = get_message_stats(message['id'])

        performance_data.append({
            'message_id': message['id'],
            'text': message['text'],
            'sent_time': message.get('sentTime'),
            'impressions': stats.get('impressions', 0),
            'clicks': stats.get('clicks', 0),
            'likes': stats.get('likes', 0),
            'shares': stats.get('shares', 0),
            'comments': stats.get('comments', 0),
            'engagement_rate': calculate_engagement_rate(stats)
        })

    df = pd.DataFrame(performance_data)
    return df

def calculate_engagement_rate(stats):
    """Calculate engagement rate from statistics"""
    impressions = stats.get('impressions', 0)
    if impressions == 0:
        return 0

    engagements = (
        stats.get('likes', 0) +
        stats.get('comments', 0) +
        stats.get('shares', 0) +
        stats.get('clicks', 0)
    )

    return (engagements / impressions) * 100

# Generate comprehensive report
def generate_social_report(profile_ids, days=30):
    """
    Generate comprehensive social media performance report

    Args:
        profile_ids: List of social profile IDs
        days: Number of days to analyze
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    report = {
        'period': f'{start_date.date()} to {end_date.date()}',
        'profiles': []
    }

    for profile_id in profile_ids:
        analytics = get_profile_analytics(profile_id, start_date, end_date)

        profile_report = {
            'profile_id': profile_id,
            'total_posts': analytics.get('totalPosts', 0),
            'total_impressions': analytics.get('totalImpressions', 0),
            'total_engagement': analytics.get('totalEngagement', 0),
            'follower_growth': analytics.get('followerGrowth', 0),
            'avg_engagement_rate': analytics.get('avgEngagementRate', 0)
        }

        report['profiles'].append(profile_report)

    return report

# Example: Generate monthly report
report = generate_social_report(
    profile_ids=['twitter_id', 'linkedin_id', 'facebook_id'],
    days=30
)

print(f"Social Media Report: {report['period']}")
for profile in report['profiles']:
    print(f"\nProfile {profile['profile_id']}:")
    print(f"  Posts: {profile['total_posts']}")
    print(f"  Impressions: {profile['total_impressions']:,}")
    print(f"  Engagement Rate: {profile['avg_engagement_rate']:.2f}%")
```

### 6. Team Collaboration

```python
# Get team members
def get_team_members():
    url = f'{BASE_URL}/members'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Assign message to team member
def assign_message(message_id, member_id):
    url = f'{BASE_URL}/messages/{message_id}/assignments'

    assignment_data = {'memberId': member_id}

    response = requests.post(url, headers=get_headers(), json=assignment_data)
    return response.json()

# Add approval workflow
def submit_for_approval(message_id, approver_id):
    """Submit message for approval before publishing"""
    url = f'{BASE_URL}/messages/{message_id}/approvals'

    approval_data = {
        'approverId': approver_id,
        'required': True
    }

    response = requests.post(url, headers=get_headers(), json=approval_data)
    return response.json()

# Approve message
def approve_message(message_id):
    url = f'{BASE_URL}/messages/{message_id}/approve'

    response = requests.post(url, headers=get_headers())
    return response.json()

# Reject message with feedback
def reject_message(message_id, feedback):
    url = f'{BASE_URL}/messages/{message_id}/reject'

    rejection_data = {'feedback': feedback}

    response = requests.post(url, headers=get_headers(), json=rejection_data)
    return response.json()

# Example: Team workflow
team = get_team_members()
print(f"Team members: {len(team.get('data', []))}")

for member in team.get('data', []):
    print(f"  - {member['fullName']} ({member['role']})")
```

## Installation

```bash
# Using requests for REST API
uv pip install requests pandas

# Optional: For advanced analytics
uv pip install matplotlib seaborn
```

## Authentication

Hootsuite uses OAuth 2.0 for authentication:

### Getting an Access Token

1. **Create a Hootsuite App:**
   - Go to https://platform.hootsuite.com/
   - Navigate to "My Apps"
   - Create a new app

2. **OAuth 2.0 Flow:**

```python
import requests
from urllib.parse import urlencode

CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
REDIRECT_URI = 'https://your-app.com/callback'

# Step 1: Generate authorization URL
def get_auth_url():
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': 'offline'  # For refresh tokens
    }

    base_url = 'https://platform.hootsuite.com/oauth2/auth'
    return f"{base_url}?{urlencode(params)}"

# Step 2: Exchange authorization code for access token
def get_access_token(authorization_code):
    url = 'https://platform.hootsuite.com/oauth2/token'

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

# Step 3: Refresh access token
def refresh_access_token(refresh_token):
    url = 'https://platform.hootsuite.com/oauth2/token'

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
ACCESS_TOKEN = 'your-hootsuite-access-token'
BASE_URL = 'https://platform.hootsuite.com/v1'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

# 1. Get your social profiles
response = requests.get(f'{BASE_URL}/socialProfiles', headers=headers)
profiles = response.json()

print("Your connected profiles:")
for profile in profiles.get('data', []):
    print(f"  - {profile['type']}: {profile.get('socialNetworkUsername')}")
    print(f"    ID: {profile['id']}")

# 2. Schedule a message
profile_id = profiles['data'][0]['id']  # Use first profile
tomorrow = datetime.now() + timedelta(days=1)

message_data = {
    'text': 'Hello from the Hootsuite API! 👋',
    'socialProfileIds': [profile_id],
    'scheduledSendTime': tomorrow.isoformat()
}

response = requests.post(
    f'{BASE_URL}/messages',
    headers=headers,
    json=message_data
)

if response.status_code == 201:
    message = response.json()
    print(f"\nMessage scheduled successfully!")
    print(f"Message ID: {message['id']}")
    print(f"Scheduled for: {message['scheduledSendTime']}")

# 3. Get scheduled messages
response = requests.get(
    f'{BASE_URL}/messages',
    headers=headers,
    params={'state': 'SCHEDULED'}
)

scheduled = response.json()
print(f"\nYou have {len(scheduled.get('data', []))} scheduled messages")
```

## Key Metrics

### Message Performance
- **Impressions**: Number of times content was displayed
- **Clicks**: Link clicks and profile clicks
- **Engagement**: Likes, comments, shares, retweets
- **Engagement Rate**: (Engagements / Impressions) × 100
- **Click-Through Rate**: (Clicks / Impressions) × 100

### Profile Metrics
- **Follower Growth**: Net change in followers
- **Follower Count**: Total followers per profile
- **Post Frequency**: Average posts per day/week
- **Response Time**: Average time to respond to messages

### Team Metrics
- **Messages Pending Approval**: Content awaiting review
- **Response Rate**: Percentage of messages responded to
- **Team Activity**: Posts published per team member
- **Approval Turnaround**: Time from submission to approval

## Best Practices

1. **Content Calendar**: Plan content 1-2 weeks in advance
2. **Consistent Scheduling**: Post at consistent times when audience is active
3. **Approval Workflows**: Implement review process for brand consistency
4. **Social Listening**: Monitor brand mentions and industry conversations
5. **Response Management**: Respond to messages within 1 hour during business hours
6. **Team Collaboration**: Use assignments to distribute workload
7. **Analytics Review**: Review metrics weekly to optimize strategy
8. **Cross-Platform Optimization**: Tailor content for each platform's best practices

## References

- [Hootsuite Platform API Documentation](https://platform.hootsuite.com/docs)
- [Authentication Guide](https://platform.hootsuite.com/docs/authentication)
- [Messages API](https://platform.hootsuite.com/docs/api/messages)
- [Social Profiles API](https://platform.hootsuite.com/docs/api/social-profiles)
- [Analytics API](https://platform.hootsuite.com/docs/api/analytics)
- [Streams API](https://platform.hootsuite.com/docs/api/streams)
- [Hootsuite Help Center](https://help.hootsuite.com/)

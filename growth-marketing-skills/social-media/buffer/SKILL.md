---
name: buffer
description: "Social media scheduling and analytics API. Schedule posts, manage queues, track engagement metrics, cross-platform publishing, optimal timing analysis."
---

# Buffer Integration

## Overview

Buffer is a social media management platform that simplifies scheduling, publishing, and analyzing content across multiple social networks. This skill covers using the Buffer API to schedule posts, manage content queues, analyze engagement metrics, and optimize posting times across platforms like Twitter, Facebook, LinkedIn, Instagram, and Pinterest.

## When to Use This Skill

- Scheduling social media posts across multiple platforms
- Managing content calendars and posting queues
- Analyzing post performance and engagement metrics
- Optimizing posting times based on audience activity
- Bulk uploading and scheduling content
- Cross-platform social media campaigns
- Tracking team collaboration on social content
- Generating social media analytics reports

## Core Capabilities

### 1. Profile Management

```python
import requests
import json

# Buffer API configuration
ACCESS_TOKEN = 'your-buffer-access-token'
BASE_URL = 'https://api.bufferapp.com/1'

# Get all connected profiles
def get_profiles():
    url = f'{BASE_URL}/profiles.json'

    params = {'access_token': ACCESS_TOKEN}

    response = requests.get(url, params=params)
    return response.json()

# Get specific profile details
def get_profile(profile_id):
    url = f'{BASE_URL}/profiles/{profile_id}.json'

    params = {'access_token': ACCESS_TOKEN}

    response = requests.get(url, params=params)
    return response.json()

# Example usage
profiles = get_profiles()

for profile in profiles:
    print(f"Profile: {profile['formatted_service']} - @{profile['service_username']}")
    print(f"  ID: {profile['id']}")
    print(f"  Timezone: {profile['timezone']}")
    print(f"  Followers: {profile.get('followers_count', 'N/A')}")
```

### 2. Post Scheduling

```python
from datetime import datetime, timedelta

# Create a scheduled post
def create_post(profile_ids, text, scheduled_at=None, media=None, shorten=True):
    url = f'{BASE_URL}/updates/create.json'

    data = {
        'access_token': ACCESS_TOKEN,
        'profile_ids[]': profile_ids,
        'text': text,
        'shorten': shorten
    }

    # Add scheduled time if provided
    if scheduled_at:
        data['scheduled_at'] = int(scheduled_at.timestamp())
    else:
        data['now'] = True

    # Add media attachments
    if media:
        if isinstance(media, dict):
            if 'photo' in media:
                data['media[photo]'] = media['photo']
            if 'link' in media:
                data['media[link]'] = media['link']
            if 'description' in media:
                data['media[description]'] = media['description']

    response = requests.post(url, data=data)
    return response.json()

# Schedule post to multiple profiles
def schedule_multi_platform_post(profile_ids, content, post_time):
    """
    Schedule a post across multiple social media profiles

    Args:
        profile_ids: List of Buffer profile IDs
        content: Post text content
        post_time: datetime object for scheduled time
    """
    result = create_post(
        profile_ids=profile_ids,
        text=content,
        scheduled_at=post_time
    )

    if result.get('success'):
        print(f"Post scheduled for {post_time}")
        for update in result.get('updates', []):
            print(f"  - Update ID: {update['id']}")

    return result

# Add post to queue (using optimal timing)
def add_to_queue(profile_ids, text, top=False):
    """Add post to profile queue at next available slot"""
    url = f'{BASE_URL}/updates/create.json'

    data = {
        'access_token': ACCESS_TOKEN,
        'profile_ids[]': profile_ids,
        'text': text,
        'top': top  # True to add to top of queue
    }

    response = requests.post(url, data=data)
    return response.json()

# Example: Schedule a post for tomorrow at 2 PM
tomorrow_2pm = datetime.now() + timedelta(days=1)
tomorrow_2pm = tomorrow_2pm.replace(hour=14, minute=0, second=0)

post_result = create_post(
    profile_ids=['twitter_profile_id', 'linkedin_profile_id'],
    text='Excited to share our latest product update! 🚀 #ProductLaunch',
    scheduled_at=tomorrow_2pm,
    media={'link': 'https://example.com/product-update'}
)

print(f"Post scheduled: {post_result}")
```

### 3. Post Management

```python
# Get pending posts in queue
def get_pending_posts(profile_id):
    url = f'{BASE_URL}/profiles/{profile_id}/updates/pending.json'

    params = {'access_token': ACCESS_TOKEN}

    response = requests.get(url, params=params)
    return response.json()

# Get sent posts
def get_sent_posts(profile_id, page=1, count=30):
    url = f'{BASE_URL}/profiles/{profile_id}/updates/sent.json'

    params = {
        'access_token': ACCESS_TOKEN,
        'page': page,
        'count': count
    }

    response = requests.get(url, params=params)
    return response.json()

# Update a scheduled post
def update_post(update_id, text=None, scheduled_at=None):
    url = f'{BASE_URL}/updates/{update_id}/update.json'

    data = {'access_token': ACCESS_TOKEN}

    if text:
        data['text'] = text

    if scheduled_at:
        data['scheduled_at'] = int(scheduled_at.timestamp())

    response = requests.post(url, data=data)
    return response.json()

# Delete a scheduled post
def delete_post(update_id):
    url = f'{BASE_URL}/updates/{update_id}/destroy.json'

    data = {'access_token': ACCESS_TOKEN}

    response = requests.post(url, data=data)
    return response.json()

# Reorder posts in queue
def move_to_top(update_id):
    url = f'{BASE_URL}/updates/{update_id}/move_to_top.json'

    data = {'access_token': ACCESS_TOKEN}

    response = requests.post(url, data=data)
    return response.json()

# Example: Get and manage pending posts
profile_id = 'your_profile_id'
pending = get_pending_posts(profile_id)

print(f"Pending posts: {len(pending.get('updates', []))}")

for post in pending.get('updates', [])[:5]:
    print(f"  - {post['text'][:50]}... (ID: {post['id']})")
    print(f"    Scheduled: {post['scheduled_at']}")
```

### 4. Analytics and Engagement Metrics

```python
import pandas as pd

# Get post statistics
def get_post_stats(update_id):
    url = f'{BASE_URL}/updates/{update_id}.json'

    params = {'access_token': ACCESS_TOKEN}

    response = requests.get(url, params=params)
    return response.json()

# Analyze post performance
def analyze_post_performance(profile_id, days=30):
    """
    Analyze performance of sent posts

    Returns engagement metrics and best performing content
    """
    sent_posts = get_sent_posts(profile_id, count=100)

    performance_data = []

    for post in sent_posts.get('updates', []):
        stats = post.get('statistics', {})

        performance_data.append({
            'id': post['id'],
            'text': post['text'],
            'sent_at': post.get('sent_at'),
            'clicks': stats.get('clicks', 0),
            'reach': stats.get('reach', 0),
            'shares': stats.get('shares', 0),
            'comments': stats.get('comments', 0),
            'likes': stats.get('likes', 0),
            'engagement_rate': calculate_engagement_rate(stats)
        })

    df = pd.DataFrame(performance_data)
    return df

def calculate_engagement_rate(stats):
    """Calculate engagement rate from post statistics"""
    reach = stats.get('reach', 0)
    if reach == 0:
        return 0

    engagements = (
        stats.get('likes', 0) +
        stats.get('comments', 0) +
        stats.get('shares', 0) +
        stats.get('clicks', 0)
    )

    return (engagements / reach) * 100

# Generate performance report
def generate_performance_report(profile_id):
    df = analyze_post_performance(profile_id)

    report = {
        'total_posts': len(df),
        'avg_clicks': df['clicks'].mean(),
        'avg_reach': df['reach'].mean(),
        'avg_engagement_rate': df['engagement_rate'].mean(),
        'best_performing': df.nlargest(5, 'engagement_rate')[
            ['text', 'engagement_rate', 'likes', 'shares']
        ].to_dict('records')
    }

    return report

# Example usage
report = generate_performance_report('your_profile_id')

print(f"Performance Report:")
print(f"  Total Posts: {report['total_posts']}")
print(f"  Avg Reach: {report['avg_reach']:.0f}")
print(f"  Avg Clicks: {report['avg_clicks']:.0f}")
print(f"  Avg Engagement Rate: {report['avg_engagement_rate']:.2f}%")

print(f"\nTop Performing Posts:")
for i, post in enumerate(report['best_performing'], 1):
    print(f"{i}. {post['text'][:60]}...")
    print(f"   Engagement: {post['engagement_rate']:.2f}% | Likes: {post['likes']} | Shares: {post['shares']}")
```

### 5. Optimal Posting Times

```python
# Get optimal posting schedule
def get_posting_schedule(profile_id):
    url = f'{BASE_URL}/profiles/{profile_id}/schedules.json'

    params = {'access_token': ACCESS_TOKEN}

    response = requests.get(url, params=params)
    return response.json()

# Update posting schedule
def update_posting_schedule(profile_id, schedule):
    """
    Update when Buffer should post from queue

    schedule format: {
        'days': ['mon', 'tue', 'wed', 'thu', 'fri'],
        'times': ['09:00', '12:00', '15:00', '18:00']
    }
    """
    url = f'{BASE_URL}/profiles/{profile_id}/schedules/update.json'

    data = {
        'access_token': ACCESS_TOKEN,
        'schedules[]': []
    }

    for day in schedule['days']:
        for time in schedule['times']:
            data['schedules[]'].append(f"{day} at {time}")

    response = requests.post(url, data=data)
    return response.json()

# Get suggested posting times based on audience engagement
def suggest_optimal_times(profile_id):
    """
    Analyze past post performance to suggest optimal posting times
    """
    sent_posts = get_sent_posts(profile_id, count=200)

    # Group by hour and day of week
    performance_by_time = {}

    for post in sent_posts.get('updates', []):
        sent_time = datetime.fromtimestamp(post.get('sent_at', 0))
        hour = sent_time.hour
        day = sent_time.strftime('%a').lower()

        key = f"{day}_{hour:02d}"

        if key not in performance_by_time:
            performance_by_time[key] = {'posts': 0, 'total_engagement': 0}

        stats = post.get('statistics', {})
        engagement = (
            stats.get('likes', 0) +
            stats.get('comments', 0) +
            stats.get('shares', 0)
        )

        performance_by_time[key]['posts'] += 1
        performance_by_time[key]['total_engagement'] += engagement

    # Calculate average engagement per time slot
    for key in performance_by_time:
        posts = performance_by_time[key]['posts']
        if posts > 0:
            performance_by_time[key]['avg_engagement'] = (
                performance_by_time[key]['total_engagement'] / posts
            )

    # Sort by average engagement
    sorted_times = sorted(
        performance_by_time.items(),
        key=lambda x: x[1].get('avg_engagement', 0),
        reverse=True
    )

    # Return top 10 time slots
    return sorted_times[:10]

# Example usage
optimal_times = suggest_optimal_times('your_profile_id')

print("Suggested optimal posting times:")
for time_slot, metrics in optimal_times:
    day, hour = time_slot.split('_')
    print(f"  {day.upper()} at {hour}:00 - Avg Engagement: {metrics.get('avg_engagement', 0):.1f}")
```

### 6. Bulk Content Scheduling

```python
import csv
from datetime import datetime, timedelta

# Bulk schedule posts from CSV
def bulk_schedule_from_csv(csv_file, profile_ids):
    """
    Schedule posts from CSV file

    CSV format: date,time,text,link
    """
    scheduled_posts = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Parse date and time
            post_datetime = datetime.strptime(
                f"{row['date']} {row['time']}",
                "%Y-%m-%d %H:%M"
            )

            # Prepare media if link provided
            media = None
            if row.get('link'):
                media = {'link': row['link']}

            # Schedule post
            result = create_post(
                profile_ids=profile_ids,
                text=row['text'],
                scheduled_at=post_datetime,
                media=media
            )

            scheduled_posts.append(result)

    return scheduled_posts

# Generate content calendar
def create_content_calendar(profile_ids, start_date, num_days, posts_per_day=3):
    """
    Create a content calendar template
    """
    calendar = []

    post_times = ['09:00', '13:00', '17:00']  # Default posting times

    for day in range(num_days):
        post_date = start_date + timedelta(days=day)

        for i in range(posts_per_day):
            calendar.append({
                'date': post_date.strftime('%Y-%m-%d'),
                'time': post_times[i % len(post_times)],
                'text': f'[Add content for {post_date.strftime("%B %d")}]',
                'link': '',
                'scheduled': False
            })

    return calendar

# Example: Bulk schedule posts
# bulk_result = bulk_schedule_from_csv('content_calendar.csv', ['profile_id_1', 'profile_id_2'])
# print(f"Scheduled {len(bulk_result)} posts")
```

## Installation

```bash
# Using requests for REST API
uv pip install requests pandas

# Optional: For CSV handling and date manipulation
uv pip install python-dateutil
```

## Authentication

Buffer uses OAuth 2.0 for authentication:

### Getting an Access Token

1. **Create a Buffer App:**
   - Go to https://buffer.com/developers/apps
   - Click "Create an App"
   - Fill in app details

2. **Get Access Token:**
   - For personal use, use the Access Token provided in your app settings
   - For production apps, implement OAuth 2.0 flow

```python
# Simple authentication with access token
ACCESS_TOKEN = 'your-buffer-access-token'

# Use in all API requests
params = {'access_token': ACCESS_TOKEN}
```

### OAuth 2.0 Flow (for production apps)

```python
import requests
from flask import Flask, request, redirect

CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
REDIRECT_URI = 'https://your-app.com/callback'

# Step 1: Redirect user to Buffer authorization
auth_url = f'https://bufferapp.com/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code'

# Step 2: Exchange authorization code for access token
def get_access_token(code):
    url = 'https://api.bufferapp.com/1/oauth2/token.json'

    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code,
        'grant_type': 'authorization_code'
    }

    response = requests.post(url, data=data)
    return response.json()['access_token']
```

## Quick Start

```python
import requests
from datetime import datetime, timedelta

# Configure API
ACCESS_TOKEN = 'your-buffer-access-token'
BASE_URL = 'https://api.bufferapp.com/1'

# 1. Get your profiles
response = requests.get(
    f'{BASE_URL}/profiles.json',
    params={'access_token': ACCESS_TOKEN}
)
profiles = response.json()

print("Your connected profiles:")
for profile in profiles:
    print(f"  - {profile['service']}: @{profile['service_username']} (ID: {profile['id']})")

# 2. Schedule a post
profile_id = profiles[0]['id']  # Use first profile

tomorrow = datetime.now() + timedelta(days=1, hours=2)

post_data = {
    'access_token': ACCESS_TOKEN,
    'profile_ids[]': [profile_id],
    'text': 'Hello from the Buffer API! 👋',
    'scheduled_at': int(tomorrow.timestamp())
}

response = requests.post(
    f'{BASE_URL}/updates/create.json',
    data=post_data
)

result = response.json()
if result.get('success'):
    print(f"\nPost scheduled successfully for {tomorrow}")
    print(f"Update ID: {result['updates'][0]['id']}")

# 3. Check pending posts
response = requests.get(
    f'{BASE_URL}/profiles/{profile_id}/updates/pending.json',
    params={'access_token': ACCESS_TOKEN}
)

pending = response.json()
print(f"\nYou have {len(pending.get('updates', []))} pending posts")
```

## Key Metrics

### Post Performance Metrics
- **Clicks**: Link clicks on posts
- **Reach**: Total unique users who saw the post
- **Impressions**: Total times post was displayed
- **Engagement**: Likes, comments, shares, retweets
- **Engagement Rate**: (Total engagements / Reach) × 100

### Queue Metrics
- **Queue Size**: Number of scheduled posts
- **Average Post Frequency**: Posts per day/week
- **Optimal Times**: Best performing posting times
- **Coverage**: Distribution across days/times

### Profile Metrics
- **Follower Growth**: Change in follower count
- **Profile Reach**: Total audience size
- **Cross-Platform Performance**: Comparison across networks

## Best Practices

1. **Consistent Scheduling**: Maintain regular posting schedule for better engagement
2. **Optimal Timing**: Use analytics to identify when your audience is most active
3. **Content Diversity**: Mix content types (links, images, videos, text)
4. **Queue Management**: Keep 3-7 days of content queued at all times
5. **Performance Tracking**: Monitor metrics weekly to refine strategy
6. **Platform Optimization**: Tailor content format for each social platform
7. **Link Shortening**: Use Buffer's link shortening for tracking
8. **Team Collaboration**: Use Buffer's team features for content approval workflows

## References

- [Buffer API Documentation](https://buffer.com/developers/api)
- [Authentication Guide](https://buffer.com/developers/api/oauth)
- [Rate Limits](https://buffer.com/developers/api#ratelimiting)
- [Buffer Publishing API](https://buffer.com/developers/api/posts)
- [Analytics API](https://buffer.com/developers/api/analytics)
- [Buffer Help Center](https://support.buffer.com/)

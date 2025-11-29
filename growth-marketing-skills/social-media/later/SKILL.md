---
name: later
description: "Visual content scheduler for Instagram, Pinterest, TikTok, Facebook, Twitter. Visual planning, media library, hashtag suggestions, analytics, linkinbio."
---

# Later Integration

## Overview

Later is a visual-first social media scheduling platform optimized for Instagram, Pinterest, TikTok, Facebook, and Twitter. This skill covers using the Later API for visual content planning, media management, hashtag optimization, Instagram-specific features like link in bio, and visual analytics for image and video-heavy social strategies.

## When to Use This Skill

- Visual content planning and scheduling (especially Instagram)
- Managing visual content calendars
- Instagram Stories and Reels scheduling
- Pinterest pin scheduling
- TikTok video scheduling
- Hashtag research and optimization
- Link in bio management for Instagram
- Visual analytics and performance tracking
- User-generated content management
- Influencer content scheduling

## Core Capabilities

### 1. Media Library Management

```python
import requests
import json
from datetime import datetime, timedelta

# Later API configuration
API_KEY = 'your-later-api-key'
BASE_URL = 'https://api.later.com/api/v1'

# Headers for all requests
def get_headers():
    return {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }

# Upload media to library
def upload_media(file_path, caption=None, tags=None):
    """
    Upload image or video to Later media library

    Args:
        file_path: Path to media file
        caption: Optional caption for media
        tags: Optional list of tags
    """
    url = f'{BASE_URL}/media'

    files = {'file': open(file_path, 'rb')}

    data = {}
    if caption:
        data['caption'] = caption
    if tags:
        data['tags'] = ','.join(tags)

    # Upload without Content-Type header for multipart
    headers = {'X-API-Key': API_KEY}

    response = requests.post(url, headers=headers, files=files, data=data)
    return response.json()

# Get media from library
def get_media_library(folder_id=None, tags=None, limit=50):
    """
    Retrieve media from your Later library

    Args:
        folder_id: Filter by folder
        tags: Filter by tags
        limit: Number of items to return
    """
    url = f'{BASE_URL}/media'

    params = {'limit': limit}

    if folder_id:
        params['folder_id'] = folder_id
    if tags:
        params['tags'] = ','.join(tags)

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Search media by tags
def search_media(search_query, media_type=None):
    """
    Search media library

    Args:
        search_query: Search text
        media_type: Filter by 'image' or 'video'
    """
    url = f'{BASE_URL}/media/search'

    params = {'query': search_query}

    if media_type:
        params['type'] = media_type

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Create media folder
def create_folder(name, parent_folder_id=None):
    """Create folder to organize media"""
    url = f'{BASE_URL}/media/folders'

    folder_data = {'name': name}

    if parent_folder_id:
        folder_data['parent_id'] = parent_folder_id

    response = requests.post(url, headers=get_headers(), json=folder_data)
    return response.json()

# Example: Upload and organize media
media = upload_media(
    file_path='/path/to/image.jpg',
    caption='Product launch photo',
    tags=['product', 'launch', 'instagram']
)

print(f"Media uploaded: {media['id']}")
print(f"Preview URL: {media['preview_url']}")
```

### 2. Visual Content Scheduling

```python
# Get social profiles
def get_profiles():
    """Get all connected social media profiles"""
    url = f'{BASE_URL}/profiles'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Schedule Instagram post
def schedule_instagram_post(profile_id, media_id, caption, scheduled_time,
                            first_comment=None, location=None, hashtags=None):
    """
    Schedule an Instagram feed post

    Args:
        profile_id: Later profile ID
        media_id: ID of media from library
        caption: Post caption
        scheduled_time: datetime for scheduling
        first_comment: Optional first comment (good for hashtags)
        location: Optional location tag
        hashtags: List of hashtags (can go in caption or first_comment)
    """
    url = f'{BASE_URL}/posts'

    post_data = {
        'profile_id': profile_id,
        'media_id': media_id,
        'caption': caption,
        'scheduled_at': scheduled_time.isoformat(),
        'post_type': 'feed'
    }

    if first_comment:
        post_data['first_comment'] = first_comment

    if location:
        post_data['location'] = location

    if hashtags:
        post_data['hashtags'] = hashtags

    response = requests.post(url, headers=get_headers(), json=post_data)
    return response.json()

# Schedule Instagram Story
def schedule_instagram_story(profile_id, media_id, scheduled_time,
                             link_url=None, link_text=None):
    """
    Schedule an Instagram Story

    Args:
        profile_id: Later profile ID
        media_id: ID of media from library
        scheduled_time: datetime for scheduling
        link_url: Swipe-up link (requires 10k+ followers)
        link_text: Link sticker text
    """
    url = f'{BASE_URL}/posts'

    story_data = {
        'profile_id': profile_id,
        'media_id': media_id,
        'scheduled_at': scheduled_time.isoformat(),
        'post_type': 'story'
    }

    if link_url:
        story_data['link'] = {
            'url': link_url,
            'text': link_text or 'Swipe Up'
        }

    response = requests.post(url, headers=get_headers(), json=story_data)
    return response.json()

# Schedule Instagram Reel
def schedule_instagram_reel(profile_id, video_id, caption, scheduled_time,
                            cover_image_id=None, share_to_feed=True):
    """
    Schedule an Instagram Reel

    Args:
        profile_id: Later profile ID
        video_id: ID of video from library
        caption: Reel caption
        scheduled_time: datetime for scheduling
        cover_image_id: Optional custom cover image
        share_to_feed: Whether to share to main feed
    """
    url = f'{BASE_URL}/posts'

    reel_data = {
        'profile_id': profile_id,
        'media_id': video_id,
        'caption': caption,
        'scheduled_at': scheduled_time.isoformat(),
        'post_type': 'reel',
        'share_to_feed': share_to_feed
    }

    if cover_image_id:
        reel_data['cover_image_id'] = cover_image_id

    response = requests.post(url, headers=get_headers(), json=reel_data)
    return response.json()

# Schedule Pinterest Pin
def schedule_pinterest_pin(profile_id, media_id, title, description,
                          scheduled_time, board_id, link_url=None):
    """
    Schedule a Pinterest Pin

    Args:
        profile_id: Later profile ID
        media_id: ID of media from library
        title: Pin title
        description: Pin description
        scheduled_time: datetime for scheduling
        board_id: Pinterest board ID
        link_url: Destination URL for pin
    """
    url = f'{BASE_URL}/posts'

    pin_data = {
        'profile_id': profile_id,
        'media_id': media_id,
        'title': title,
        'description': description,
        'scheduled_at': scheduled_time.isoformat(),
        'post_type': 'pin',
        'board_id': board_id
    }

    if link_url:
        pin_data['link'] = link_url

    response = requests.post(url, headers=get_headers(), json=pin_data)
    return response.json()

# Schedule TikTok video
def schedule_tiktok_video(profile_id, video_id, caption, scheduled_time,
                         privacy='PUBLIC', allow_comments=True):
    """
    Schedule a TikTok video

    Args:
        profile_id: Later profile ID
        video_id: ID of video from library
        caption: Video caption
        scheduled_time: datetime for scheduling
        privacy: 'PUBLIC', 'FRIENDS', or 'PRIVATE'
        allow_comments: Whether to allow comments
    """
    url = f'{BASE_URL}/posts'

    tiktok_data = {
        'profile_id': profile_id,
        'media_id': video_id,
        'caption': caption,
        'scheduled_at': scheduled_time.isoformat(),
        'post_type': 'tiktok',
        'privacy': privacy,
        'allow_comments': allow_comments
    }

    response = requests.post(url, headers=get_headers(), json=tiktok_data)
    return response.json()

# Example: Schedule Instagram post for optimal time
tomorrow_9am = datetime.now() + timedelta(days=1)
tomorrow_9am = tomorrow_9am.replace(hour=9, minute=0, second=0)

post = schedule_instagram_post(
    profile_id='instagram_profile_id',
    media_id='media_123',
    caption='New product alert! 🎉 Check out our latest collection.',
    scheduled_time=tomorrow_9am,
    first_comment='#newproduct #fashion #style #shopping #instafashion',
    location='New York, NY'
)

print(f"Instagram post scheduled: {post['id']}")
```

### 3. Visual Calendar Management

```python
# Get calendar view
def get_calendar(profile_id, start_date, end_date):
    """
    Get visual calendar of scheduled posts

    Args:
        profile_id: Later profile ID
        start_date: Start date for calendar
        end_date: End date for calendar
    """
    url = f'{BASE_URL}/calendar'

    params = {
        'profile_id': profile_id,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Get scheduled posts
def get_scheduled_posts(profile_id, start_date=None, end_date=None):
    """Get all scheduled posts for a profile"""
    url = f'{BASE_URL}/posts'

    params = {
        'profile_id': profile_id,
        'status': 'scheduled'
    }

    if start_date:
        params['start_date'] = start_date.strftime('%Y-%m-%d')
    if end_date:
        params['end_date'] = end_date.strftime('%Y-%m-%d')

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Update scheduled post
def update_post(post_id, caption=None, scheduled_time=None, hashtags=None):
    """Update a scheduled post"""
    url = f'{BASE_URL}/posts/{post_id}'

    update_data = {}

    if caption:
        update_data['caption'] = caption
    if scheduled_time:
        update_data['scheduled_at'] = scheduled_time.isoformat()
    if hashtags:
        update_data['hashtags'] = hashtags

    response = requests.patch(url, headers=get_headers(), json=update_data)
    return response.json()

# Delete scheduled post
def delete_post(post_id):
    """Delete a scheduled post"""
    url = f'{BASE_URL}/posts/{post_id}'

    response = requests.delete(url, headers=get_headers())
    return response.status_code == 204

# Bulk schedule posts
def bulk_schedule(profile_id, posts_data):
    """
    Bulk schedule multiple posts

    posts_data format: [
        {
            'media_id': 'media_123',
            'caption': 'Post content',
            'scheduled_time': datetime_obj,
            'post_type': 'feed'
        },
        ...
    ]
    """
    url = f'{BASE_URL}/posts/bulk'

    bulk_data = {
        'profile_id': profile_id,
        'posts': posts_data
    }

    response = requests.post(url, headers=get_headers(), json=bulk_data)
    return response.json()
```

### 4. Hashtag Optimization

```python
# Get hashtag suggestions
def get_hashtag_suggestions(caption_text, platform='instagram', limit=30):
    """
    Get AI-powered hashtag suggestions

    Args:
        caption_text: Post caption to analyze
        platform: 'instagram', 'tiktok', or 'twitter'
        limit: Number of suggestions to return
    """
    url = f'{BASE_URL}/hashtags/suggestions'

    params = {
        'text': caption_text,
        'platform': platform,
        'limit': limit
    }

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Search hashtags
def search_hashtags(query, platform='instagram'):
    """
    Search for hashtags and get their metrics

    Args:
        query: Hashtag to search (without #)
        platform: Social platform
    """
    url = f'{BASE_URL}/hashtags/search'

    params = {
        'query': query,
        'platform': platform
    }

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Get hashtag analytics
def get_hashtag_analytics(hashtags, profile_id, days=30):
    """
    Analyze performance of specific hashtags

    Args:
        hashtags: List of hashtags to analyze
        profile_id: Profile ID
        days: Days of history to analyze
    """
    url = f'{BASE_URL}/analytics/hashtags'

    params = {
        'hashtags': ','.join(hashtags),
        'profile_id': profile_id,
        'days': days
    }

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Create hashtag groups
def create_hashtag_group(name, hashtags):
    """
    Save frequently used hashtag combinations

    Args:
        name: Group name
        hashtags: List of hashtags
    """
    url = f'{BASE_URL}/hashtags/groups'

    group_data = {
        'name': name,
        'hashtags': hashtags
    }

    response = requests.post(url, headers=get_headers(), json=group_data)
    return response.json()

# Get saved hashtag groups
def get_hashtag_groups():
    """Retrieve all saved hashtag groups"""
    url = f'{BASE_URL}/hashtags/groups'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Example: Optimize hashtags for a post
caption = "New summer collection is here! Fresh styles and vibrant colors."

suggestions = get_hashtag_suggestions(caption, platform='instagram', limit=30)

print("Suggested hashtags:")
for tag in suggestions.get('hashtags', []):
    print(f"  #{tag['tag']} - {tag['usage_count']:,} posts")

# Create hashtag group for later use
fashion_group = create_hashtag_group(
    name='Fashion Posts',
    hashtags=[
        'fashion', 'style', 'ootd', 'fashionblogger', 'instafashion',
        'fashionista', 'styleinspo', 'fashiongram', 'outfitoftheday'
    ]
)
```

### 5. Link in Bio (Linkin.bio)

```python
# Create linkin.bio link
def create_linkinbio_link(profile_id, title, url, image_url=None):
    """
    Create a link for Instagram link in bio

    Args:
        profile_id: Instagram profile ID
        title: Link title
        url: Destination URL
        image_url: Optional thumbnail image
    """
    linkinbio_url = f'{BASE_URL}/linkinbio/links'

    link_data = {
        'profile_id': profile_id,
        'title': title,
        'url': url
    }

    if image_url:
        link_data['image_url'] = image_url

    response = requests.post(linkinbio_url, headers=get_headers(), json=link_data)
    return response.json()

# Get linkin.bio page
def get_linkinbio_page(profile_id):
    """Get all links on linkin.bio page"""
    url = f'{BASE_URL}/linkinbio/pages/{profile_id}'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Update link order
def update_link_order(profile_id, link_ids):
    """
    Reorder links on linkin.bio page

    Args:
        profile_id: Instagram profile ID
        link_ids: List of link IDs in desired order
    """
    url = f'{BASE_URL}/linkinbio/pages/{profile_id}/order'

    order_data = {'link_ids': link_ids}

    response = requests.put(url, headers=get_headers(), json=order_data)
    return response.json()

# Get link analytics
def get_link_analytics(link_id, days=30):
    """
    Get click analytics for linkin.bio link

    Args:
        link_id: Link ID
        days: Days of analytics
    """
    url = f'{BASE_URL}/linkinbio/links/{link_id}/analytics'

    params = {'days': days}

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Auto-update linkin.bio with latest post
def auto_update_linkinbio(profile_id, post_url, post_image_url):
    """Automatically add latest Instagram post to linkin.bio"""
    link = create_linkinbio_link(
        profile_id=profile_id,
        title='Latest Post',
        url=post_url,
        image_url=post_image_url
    )

    # Move to top of page
    page = get_linkinbio_page(profile_id)
    link_ids = [link['id']] + [l['id'] for l in page.get('links', []) if l['id'] != link['id']]

    update_link_order(profile_id, link_ids)

    return link
```

### 6. Analytics and Insights

```python
import pandas as pd

# Get post analytics
def get_post_analytics(post_id):
    """Get detailed analytics for a published post"""
    url = f'{BASE_URL}/analytics/posts/{post_id}'

    response = requests.get(url, headers=get_headers())
    return response.json()

# Get profile analytics
def get_profile_analytics(profile_id, start_date, end_date):
    """
    Get profile-level analytics

    Args:
        profile_id: Profile ID
        start_date: Start date
        end_date: End date
    """
    url = f'{BASE_URL}/analytics/profiles/{profile_id}'

    params = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Analyze best performing content
def analyze_best_content(profile_id, days=30, metric='engagement'):
    """
    Find best performing content

    Args:
        profile_id: Profile ID
        days: Days to analyze
        metric: 'engagement', 'likes', 'comments', or 'saves'
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    analytics = get_profile_analytics(profile_id, start_date, end_date)

    posts = analytics.get('posts', [])

    # Sort by metric
    sorted_posts = sorted(
        posts,
        key=lambda x: x.get(metric, 0),
        reverse=True
    )

    return sorted_posts[:10]  # Top 10

# Get optimal posting times
def get_optimal_posting_times(profile_id, days=90):
    """
    Analyze when your audience is most engaged

    Returns: Best times to post
    """
    url = f'{BASE_URL}/analytics/optimal-times'

    params = {
        'profile_id': profile_id,
        'days': days
    }

    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()

# Generate visual analytics report
def generate_visual_report(profile_id, days=30):
    """
    Generate comprehensive visual content report

    Returns: DataFrame with visual content metrics
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    analytics = get_profile_analytics(profile_id, start_date, end_date)

    report_data = []

    for post in analytics.get('posts', []):
        report_data.append({
            'post_id': post['id'],
            'type': post['post_type'],
            'published_at': post['published_at'],
            'likes': post.get('likes', 0),
            'comments': post.get('comments', 0),
            'saves': post.get('saves', 0),
            'shares': post.get('shares', 0),
            'reach': post.get('reach', 0),
            'engagement_rate': post.get('engagement_rate', 0)
        })

    df = pd.DataFrame(report_data)

    summary = {
        'total_posts': len(df),
        'avg_engagement_rate': df['engagement_rate'].mean(),
        'total_likes': df['likes'].sum(),
        'total_comments': df['comments'].sum(),
        'total_saves': df['saves'].sum(),
        'best_performing_type': df.groupby('type')['engagement_rate'].mean().idxmax()
    }

    return df, summary

# Example: Generate monthly report
df, summary = generate_visual_report('instagram_profile_id', days=30)

print("30-Day Visual Content Report:")
print(f"  Total Posts: {summary['total_posts']}")
print(f"  Avg Engagement Rate: {summary['avg_engagement_rate']:.2f}%")
print(f"  Total Saves: {summary['total_saves']:,}")
print(f"  Best Content Type: {summary['best_performing_type']}")

print("\nTop 5 Posts:")
print(df.nlargest(5, 'engagement_rate')[['type', 'likes', 'saves', 'engagement_rate']])
```

## Installation

```bash
# Using requests for REST API
uv pip install requests pandas Pillow

# Optional: For image processing
uv pip install pillow opencv-python
```

## Authentication

Later uses API Key authentication:

### Getting an API Key

1. **Access Later Settings:**
   - Log in to Later
   - Go to Settings > API
   - Generate new API key

2. **Use API Key in requests:**

```python
API_KEY = 'your-later-api-key'

headers = {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

# Use in all requests
response = requests.get(url, headers=headers)
```

## Quick Start

```python
import requests
from datetime import datetime, timedelta

# Configure API
API_KEY = 'your-later-api-key'
BASE_URL = 'https://api.later.com/api/v1'

headers = {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

# 1. Get your profiles
response = requests.get(f'{BASE_URL}/profiles', headers=headers)
profiles = response.json()

print("Your profiles:")
for profile in profiles.get('data', []):
    print(f"  - {profile['platform']}: @{profile['username']}")

# 2. Upload media
files = {'file': open('image.jpg', 'rb')}
headers_upload = {'X-API-Key': API_KEY}

response = requests.post(
    f'{BASE_URL}/media',
    headers=headers_upload,
    files=files,
    data={'caption': 'Product photo'}
)

media = response.json()
print(f"\nMedia uploaded: {media['id']}")

# 3. Schedule Instagram post
profile_id = profiles['data'][0]['id']
tomorrow = datetime.now() + timedelta(days=1)

post_data = {
    'profile_id': profile_id,
    'media_id': media['id'],
    'caption': 'Check out our new product! 🎉 #newproduct',
    'scheduled_at': tomorrow.isoformat(),
    'post_type': 'feed'
}

response = requests.post(
    f'{BASE_URL}/posts',
    headers=headers,
    json=post_data
)

if response.status_code == 201:
    post = response.json()
    print(f"\nPost scheduled successfully!")
    print(f"Post ID: {post['id']}")
```

## Key Metrics

### Visual Content Metrics
- **Engagement Rate**: (Likes + Comments + Saves) / Reach × 100
- **Saves**: Number of times content was saved (high-value metric)
- **Shares**: Content shared to Stories or direct messages
- **Reach**: Unique accounts reached
- **Impressions**: Total times content was viewed

### Instagram-Specific Metrics
- **Profile Visits**: Visits from your posts
- **Follower Growth**: Net follower change
- **Story Completion Rate**: % who watched full story
- **Story Exits**: When people leave your story
- **Link Clicks**: Linkin.bio and story link clicks

### Content Type Performance
- **Feed Posts**: Standard grid posts
- **Stories**: 24-hour ephemeral content
- **Reels**: Short-form video
- **Carousel**: Multi-image posts
- **Video**: IGTV and video posts

## Best Practices

1. **Visual Consistency**: Maintain consistent aesthetic and brand colors
2. **Optimal Posting Times**: Post when your audience is most active (use analytics)
3. **Hashtag Strategy**: Use 20-30 hashtags via first comment
4. **Story Engagement**: Post stories 3-7 times daily for maximum engagement
5. **Reels Strategy**: Post Reels 3-5x per week for maximum reach
6. **User-Generated Content**: Feature customer photos to build community
7. **Linkin.bio**: Update regularly with latest content and offers
8. **Content Mix**: 70% value, 20% engagement, 10% promotional

## References

- [Later API Documentation](https://developer.later.com/docs)
- [Later Media Library Guide](https://later.com/blog/media-library/)
- [Instagram Best Times to Post](https://later.com/blog/best-time-to-post-on-instagram/)
- [Hashtag Strategy Guide](https://later.com/blog/instagram-hashtags/)
- [Linkin.bio Setup](https://later.com/linkinbio/)
- [Later Analytics Guide](https://later.com/blog/instagram-analytics/)
- [Later Help Center](https://help.later.com/)

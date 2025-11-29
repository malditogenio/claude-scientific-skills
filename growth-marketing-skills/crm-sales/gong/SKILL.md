---
name: gong
description: "Gong revenue intelligence platform. Call recording, conversation analytics, deal intelligence, coaching insights, pipeline forecasting, win/loss analysis."
---

# Gong Integration

## Overview

Gong is a revenue intelligence platform that captures and analyzes customer interactions to provide insights into deals, coaching opportunities, and market intelligence. This skill covers using the Gong API to access call data, analyze conversations, track deal health, and derive insights for sales and marketing alignment.

## When to Use This Skill

- Sales call recording and transcription
- Conversation analytics and intelligence
- Deal health scoring and risk assessment
- Competitive intelligence gathering
- Sales coaching and performance improvement
- Win/loss analysis and pattern detection
- Product feedback and market insights
- Marketing message testing and validation
- Customer objection analysis

## Core Capabilities

### 1. Call and Meeting Data Access

```python
import requests
import json
from datetime import datetime, timedelta
import pandas as pd

# Gong API configuration
API_KEY = 'your-gong-api-key'
API_SECRET = 'your-gong-api-secret'
BASE_URL = 'https://api.gong.io/v2'

import base64

def get_auth_header():
    """Generate Basic Auth header."""
    credentials = f'{API_KEY}:{API_SECRET}'
    encoded = base64.b64encode(credentials.encode()).decode()
    return f'Basic {encoded}'

def api_request(endpoint, method='GET', data=None, params=None):
    """Make Gong API request."""
    url = f'{BASE_URL}/{endpoint}'
    headers = {
        'Authorization': get_auth_header(),
        'Content-Type': 'application/json'
    }

    if method == 'GET':
        response = requests.get(url, headers=headers, params=params)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=data)

    return response.json()

# Get calls
def get_calls(from_date=None, to_date=None, workspace_id=None):
    """Get calls within date range."""
    if not from_date:
        from_date = (datetime.now() - timedelta(days=30)).isoformat() + 'Z'

    if not to_date:
        to_date = datetime.now().isoformat() + 'Z'

    request_data = {
        'filter': {
            'fromDateTime': from_date,
            'toDateTime': to_date,
            'workspaceId': workspace_id
        }
    }

    result = api_request('calls', method='POST', data=request_data)
    return result.get('calls', [])

# Get call details
def get_call_details(call_id):
    """Get detailed information for specific call."""
    result = api_request(f'calls/{call_id}')
    return result.get('call', {})

# Get call transcript
def get_call_transcript(call_id):
    """Get transcript for call."""
    result = api_request(f'calls/transcript', method='POST', data={'callId': call_id})
    return result.get('transcript', {})

# Download call recording
def get_call_recording_url(call_id):
    """Get URL to download call recording."""
    result = api_request(f'calls/{call_id}/media')
    return result.get('audioUrl')

# Example: Get recent calls and transcripts
recent_calls = get_calls(from_date=(datetime.now() - timedelta(days=7)).isoformat() + 'Z')

print(f"Found {len(recent_calls)} calls in last 7 days")

# Get transcript for first call
if recent_calls:
    first_call = recent_calls[0]
    call_id = first_call['id']

    details = get_call_details(call_id)
    transcript = get_call_transcript(call_id)

    print(f"Call: {details.get('title')}")
    print(f"Duration: {details.get('duration')} seconds")
    print(f"Participants: {len(details.get('parties', []))}")
```

### 2. Conversation Analytics and Insights

```python
# Analyze conversation topics and keywords
def analyze_call_topics(call_id):
    """Extract topics and keywords from call."""
    transcript = get_call_transcript(call_id)

    # Gong provides topic tracking
    details = get_call_details(call_id)

    topics = {
        'call_id': call_id,
        'tracked_topics': details.get('topics', []),
        'keywords_mentioned': details.get('keywords', []),
        'questions_asked': details.get('questions', []),
        'action_items': details.get('actionItems', []),
        'next_steps': details.get('nextSteps', [])
    }

    return topics

# Get conversation metrics
def get_conversation_metrics(call_id):
    """Get talk-to-listen ratio and other metrics."""
    details = get_call_details(call_id)

    # Extract metrics from call
    metrics = {
        'call_id': call_id,
        'duration_seconds': details.get('duration', 0),
        'talk_to_listen_ratio': details.get('stats', {}).get('talkListenRatio'),
        'speaker_stats': []
    }

    # Get stats per participant
    for party in details.get('parties', []):
        speaker_stats = {
            'name': party.get('name'),
            'email': party.get('emailAddress'),
            'talk_time': party.get('speakingTime'),
            'monologues': party.get('longestMonologue'),
            'interactivity': party.get('interactivity')
        }
        metrics['speaker_stats'].append(speaker_stats)

    return metrics

# Analyze competitive mentions
def analyze_competitive_intelligence(calls_df):
    """Analyze competitor mentions across calls."""
    competitors = ['Competitor A', 'Competitor B', 'Competitor C']

    competitive_data = []

    for _, call in calls_df.iterrows():
        call_id = call['id']
        transcript = get_call_transcript(call_id)

        # Search transcript for competitor mentions
        mentions = {}
        transcript_text = ' '.join([
            turn.get('text', '') for turn in transcript.get('turns', [])
        ]).lower()

        for competitor in competitors:
            mentions[competitor] = transcript_text.count(competitor.lower())

        if sum(mentions.values()) > 0:
            competitive_data.append({
                'call_id': call_id,
                'date': call.get('started'),
                'competitor_mentions': mentions,
                'total_mentions': sum(mentions.values())
            })

    return pd.DataFrame(competitive_data)

# Extract customer objections
def extract_objections(call_id):
    """Identify common objections in call."""
    transcript = get_call_transcript(call_id)
    details = get_call_details(call_id)

    # Common objection patterns
    objection_patterns = [
        'too expensive', 'price', 'cost', 'budget',
        'not the right time', 'timing',
        'need to think', 'need more time',
        'already using', 'current solution',
        'not interested', 'no need'
    ]

    objections_found = []
    transcript_text = ' '.join([
        turn.get('text', '') for turn in transcript.get('turns', [])
    ]).lower()

    for pattern in objection_patterns:
        if pattern in transcript_text:
            objections_found.append(pattern)

    return {
        'call_id': call_id,
        'objections': objections_found,
        'objection_count': len(objections_found),
        'tagged_topics': details.get('topics', [])
    }

# Sentiment analysis from Gong data
def get_call_sentiment(call_id):
    """Get sentiment and engagement from call."""
    details = get_call_details(call_id)

    sentiment = {
        'call_id': call_id,
        'overall_sentiment': details.get('stats', {}).get('sentiment'),
        'engagement_level': details.get('stats', {}).get('engagementLevel'),
        'customer_interest': details.get('stats', {}).get('interestLevel'),
        'next_steps_defined': len(details.get('nextSteps', [])) > 0
    }

    return sentiment
```

### 3. Deal Intelligence and Pipeline Analytics

```python
# Get calls for specific deal
def get_deal_calls(crm_deal_id):
    """Get all calls associated with a deal."""
    request_data = {
        'filter': {
            'crmObjectIds': [crm_deal_id]
        }
    }

    result = api_request('calls', method='POST', data=request_data)
    return result.get('calls', [])

# Analyze deal health
def analyze_deal_health(crm_deal_id):
    """Analyze deal health based on conversation data."""
    calls = get_deal_calls(crm_deal_id)

    if not calls:
        return {'status': 'No calls found'}

    # Analyze all calls for the deal
    metrics = {
        'deal_id': crm_deal_id,
        'total_calls': len(calls),
        'total_duration': sum(c.get('duration', 0) for c in calls),
        'stakeholders_engaged': len(set(
            party.get('emailAddress')
            for call in calls
            for party in call.get('parties', [])
            if party.get('emailAddress')
        )),
        'recent_activity': max(
            (datetime.fromisoformat(c.get('started', '').replace('Z', '+00:00'))
             for c in calls),
            default=None
        ),
        'objections_count': 0,
        'positive_signals': 0,
        'risk_factors': []
    }

    # Analyze each call
    for call in calls:
        call_id = call['id']

        # Get sentiment
        sentiment = get_call_sentiment(call_id)
        if sentiment.get('overall_sentiment') == 'positive':
            metrics['positive_signals'] += 1

        # Check for objections
        objections = extract_objections(call_id)
        metrics['objections_count'] += objections['objection_count']

        # Check for next steps
        if not sentiment.get('next_steps_defined'):
            metrics['risk_factors'].append(f"Call {call_id}: No next steps defined")

    # Calculate health score
    health_score = 50  # Base score

    # Adjust based on factors
    health_score += min(metrics['total_calls'] * 5, 20)  # More calls = better
    health_score += min(metrics['stakeholders_engaged'] * 10, 30)  # More stakeholders = better
    health_score -= metrics['objections_count'] * 5  # Objections reduce score
    health_score += metrics['positive_signals'] * 10  # Positive sentiment helps
    health_score -= len(metrics['risk_factors']) * 10  # Risk factors reduce score

    # Days since last activity
    if metrics['recent_activity']:
        days_since = (datetime.now(metrics['recent_activity'].tzinfo) - metrics['recent_activity']).days
        if days_since > 14:
            health_score -= 20
            metrics['risk_factors'].append(f"No activity in {days_since} days")

    metrics['health_score'] = max(0, min(100, health_score))
    metrics['health_grade'] = (
        'A' if metrics['health_score'] >= 80 else
        'B' if metrics['health_score'] >= 60 else
        'C' if metrics['health_score'] >= 40 else
        'D'
    )

    return metrics

# Win/loss analysis
def analyze_win_loss_patterns(won_deals, lost_deals):
    """Compare conversation patterns between won and lost deals."""
    won_analysis = []
    lost_analysis = []

    # Analyze won deals
    for deal_id in won_deals:
        health = analyze_deal_health(deal_id)
        won_analysis.append(health)

    # Analyze lost deals
    for deal_id in lost_deals:
        health = analyze_deal_health(deal_id)
        lost_analysis.append(health)

    won_df = pd.DataFrame(won_analysis)
    lost_df = pd.DataFrame(lost_analysis)

    comparison = {
        'won_deals': {
            'avg_calls': won_df['total_calls'].mean() if not won_df.empty else 0,
            'avg_stakeholders': won_df['stakeholders_engaged'].mean() if not won_df.empty else 0,
            'avg_objections': won_df['objections_count'].mean() if not won_df.empty else 0,
            'avg_health_score': won_df['health_score'].mean() if not won_df.empty else 0
        },
        'lost_deals': {
            'avg_calls': lost_df['total_calls'].mean() if not lost_df.empty else 0,
            'avg_stakeholders': lost_df['stakeholders_engaged'].mean() if not lost_df.empty else 0,
            'avg_objections': lost_df['objections_count'].mean() if not lost_df.empty else 0,
            'avg_health_score': lost_df['health_score'].mean() if not lost_df.empty else 0
        }
    }

    # Identify key differences
    comparison['insights'] = []

    if comparison['won_deals']['avg_calls'] > comparison['lost_deals']['avg_calls'] * 1.2:
        comparison['insights'].append(
            f"Won deals had {comparison['won_deals']['avg_calls']:.1f} calls vs "
            f"{comparison['lost_deals']['avg_calls']:.1f} for lost deals"
        )

    if comparison['won_deals']['avg_stakeholders'] > comparison['lost_deals']['avg_stakeholders'] * 1.2:
        comparison['insights'].append(
            f"Won deals engaged {comparison['won_deals']['avg_stakeholders']:.1f} stakeholders vs "
            f"{comparison['lost_deals']['avg_stakeholders']:.1f} for lost deals"
        )

    return comparison
```

### 4. Sales Coaching and Performance

```python
# Get user (rep) statistics
def get_rep_performance(user_id, from_date=None):
    """Get performance metrics for sales rep."""
    if not from_date:
        from_date = (datetime.now() - timedelta(days=30)).isoformat() + 'Z'

    # Get calls for user
    request_data = {
        'filter': {
            'fromDateTime': from_date,
            'primaryUserId': user_id
        }
    }

    calls = api_request('calls', method='POST', data=request_data).get('calls', [])

    if not calls:
        return {'user_id': user_id, 'calls': 0}

    # Analyze calls
    total_calls = len(calls)
    total_duration = sum(c.get('duration', 0) for c in calls)

    # Get detailed metrics
    talk_ratios = []
    engagement_scores = []

    for call in calls[:50]:  # Limit to avoid rate limits
        metrics = get_conversation_metrics(call['id'])
        if metrics.get('talk_to_listen_ratio'):
            talk_ratios.append(metrics['talk_to_listen_ratio'])

        sentiment = get_call_sentiment(call['id'])
        if sentiment.get('engagement_level'):
            engagement_scores.append(sentiment['engagement_level'])

    performance = {
        'user_id': user_id,
        'total_calls': total_calls,
        'total_duration_minutes': total_duration / 60,
        'avg_call_duration': total_duration / total_calls if total_calls > 0 else 0,
        'avg_talk_to_listen_ratio': sum(talk_ratios) / len(talk_ratios) if talk_ratios else None,
        'avg_engagement': sum(engagement_scores) / len(engagement_scores) if engagement_scores else None
    }

    # Coaching recommendations
    performance['coaching_tips'] = []

    if performance.get('avg_talk_to_listen_ratio', 0) > 0.65:
        performance['coaching_tips'].append(
            "Talk ratio is high - practice active listening and asking more questions"
        )

    if performance.get('avg_call_duration', 0) < 900:  # Less than 15 minutes
        performance['coaching_tips'].append(
            "Calls are short - work on building deeper conversations"
        )

    return performance

# Identify best practices from top performers
def identify_best_practices(top_performer_ids):
    """Analyze top performers to identify best practices."""
    best_practices = {
        'call_patterns': [],
        'talk_strategies': [],
        'engagement_tactics': []
    }

    for user_id in top_performer_ids:
        perf = get_rep_performance(user_id)

        # Extract patterns
        if perf.get('avg_talk_to_listen_ratio'):
            best_practices['talk_strategies'].append({
                'user_id': user_id,
                'talk_ratio': perf['avg_talk_to_listen_ratio'],
                'avg_duration': perf['avg_call_duration']
            })

    # Analyze patterns
    talk_df = pd.DataFrame(best_practices['talk_strategies'])

    if not talk_df.empty:
        best_practices['recommendations'] = {
            'ideal_talk_ratio': talk_df['talk_ratio'].median(),
            'ideal_call_length': talk_df['avg_duration'].median()
        }

    return best_practices
```

## Installation

```bash
# Gong doesn't have an official Python SDK
# Use requests library for API calls
uv pip install requests pandas python-dateutil
```

## Authentication

```python
import requests
import base64

# Gong uses Basic Auth with API Key and Secret
API_KEY = 'your-api-key'
API_SECRET = 'your-api-secret'

# Encode credentials
credentials = f'{API_KEY}:{API_SECRET}'
encoded = base64.b64encode(credentials.encode()).decode()

headers = {
    'Authorization': f'Basic {encoded}',
    'Content-Type': 'application/json'
}

# Make request
response = requests.post(
    'https://api.gong.io/v2/calls',
    headers=headers,
    json={'filter': {}}
)
```

To get API credentials:
1. Log into Gong
2. Go to Settings > API
3. Create API credentials
4. Copy API Key and API Secret

## Quick Start

```python
import requests
import base64
from datetime import datetime, timedelta

# Configuration
API_KEY = 'your-api-key'
API_SECRET = 'your-api-secret'
BASE_URL = 'https://api.gong.io/v2'

# Setup authentication
credentials = f'{API_KEY}:{API_SECRET}'
encoded = base64.b64encode(credentials.encode()).decode()

headers = {
    'Authorization': f'Basic {encoded}',
    'Content-Type': 'application/json'
}

# Get recent calls
from_date = (datetime.now() - timedelta(days=7)).isoformat() + 'Z'
to_date = datetime.now().isoformat() + 'Z'

request_data = {
    'filter': {
        'fromDateTime': from_date,
        'toDateTime': to_date
    }
}

response = requests.post(
    f'{BASE_URL}/calls',
    headers=headers,
    json=request_data
)

calls = response.json().get('calls', [])
print(f"Found {len(calls)} calls in last 7 days")

# Get details for first call
if calls:
    call_id = calls[0]['id']

    details_response = requests.get(
        f'{BASE_URL}/calls/{call_id}',
        headers=headers
    )

    call_details = details_response.json().get('call', {})
    print(f"Call: {call_details.get('title')}")
    print(f"Duration: {call_details.get('duration')} seconds")
```

## Key Features Reference

- **Call Recording**: Automatic recording of calls and meetings
- **Transcription**: AI-powered speech-to-text
- **Conversation Intelligence**: Topic tracking, keyword detection
- **Deal Intelligence**: Deal health scoring and risk alerts
- **Coaching**: Performance analytics and coaching insights
- **Competitive Intelligence**: Track competitor mentions
- **Market Intelligence**: Product feedback and trends
- **Integrations**: Salesforce, HubSpot, Outreach, SalesLoft
- **Analytics**: Win/loss analysis, forecasting
- **Mobile Apps**: iOS and Android

## References

- [Gong API Documentation](https://help.gong.io/hc/en-us/sections/360007814638-Public-API)
- [API Reference](https://us-66463.api.gong.io/documentation)
- [Authentication Guide](https://help.gong.io/hc/en-us/articles/360052002512-API-Authentication)
- [Calls API](https://us-66463.api.gong.io/documentation#tag/Calls)
- [Users API](https://us-66463.api.gong.io/documentation#tag/Users)
- [Rate Limits](https://help.gong.io/hc/en-us/articles/360052002892-API-Rate-Limits)

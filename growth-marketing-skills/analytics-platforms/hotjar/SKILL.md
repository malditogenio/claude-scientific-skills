---
name: hotjar
description: "Behavior analytics and user feedback. Heatmaps, session recordings, surveys, feedback widgets, conversion funnels, form analysis."
---

# Hotjar Behavior Analytics

## Overview

Hotjar is a behavior analytics and user feedback platform that helps understand how users interact with your website through heatmaps, session recordings, surveys, and feedback widgets. This skill covers API access for retrieving analytics data, analyzing user behavior patterns, and leveraging feedback for optimization.

## When to Use This Skill

- Understanding user behavior through visual heatmaps
- Watching session recordings to identify UX issues
- Collecting user feedback with surveys and polls
- Analyzing form completion and abandonment
- Identifying conversion funnel drop-offs
- Gathering qualitative insights from users
- A/B testing validation through behavior observation

## Core Capabilities

### 1. Hotjar API Setup

```python
import requests
import pandas as pd
from datetime import datetime, timedelta
import json

class HotjarAnalytics:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.hotjar.com/v1"
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, endpoint, method='GET', params=None, data=None):
        """Make authenticated request to Hotjar API"""
        url = f"{self.base_url}/{endpoint}"

        if method == 'GET':
            response = requests.get(url, headers=self.headers, params=params)
        else:
            response = requests.post(url, headers=self.headers, json=data)

        response.raise_for_status()
        return response.json()

    def get_sites(self):
        """Get all sites"""
        return self._make_request('sites')

    def get_heatmaps(self, site_id):
        """Get all heatmaps for a site"""
        return self._make_request(f'sites/{site_id}/heatmaps')

    def get_recordings(self, site_id, filters=None):
        """Get session recordings"""
        params = filters or {}
        return self._make_request(f'sites/{site_id}/recordings', params=params)

    def get_feedback(self, site_id):
        """Get feedback responses"""
        return self._make_request(f'sites/{site_id}/feedback')

# Initialize Hotjar client
hotjar = HotjarAnalytics(api_key='YOUR_API_KEY')

# Get all sites
sites = hotjar.get_sites()
print(f"Sites: {sites}")

if sites and 'sites' in sites:
    site_id = sites['sites'][0]['id']
    print(f"Using site ID: {site_id}")
```

### 2. Heatmap Data Analysis

```python
def analyze_heatmap_data(hotjar, site_id, page_url):
    """
    Analyze heatmap click data for a page
    """
    heatmaps = hotjar.get_heatmaps(site_id)

    # Find heatmap for specific page
    page_heatmap = None
    if 'heatmaps' in heatmaps:
        for hm in heatmaps['heatmaps']:
            if hm['page_url'] == page_url:
                page_heatmap = hm
                break

    if page_heatmap:
        heatmap_id = page_heatmap['id']

        # Get detailed heatmap data
        heatmap_data = hotjar._make_request(
            f'sites/{site_id}/heatmaps/{heatmap_id}'
        )

        if 'clicks' in heatmap_data:
            # Process click data
            clicks = []
            for click in heatmap_data['clicks']:
                clicks.append({
                    'x': click['x'],
                    'y': click['y'],
                    'count': click['count'],
                    'element': click.get('element', 'unknown')
                })

            clicks_df = pd.DataFrame(clicks)

            # Top clicked elements
            top_elements = clicks_df.groupby('element')['count'].sum().sort_values(ascending=False)

            print(f"\nHeatmap Analysis for {page_url}")
            print(f"Total clicks: {clicks_df['count'].sum():,}")
            print("\nTop 10 Clicked Elements:")
            print(top_elements.head(10))

            return clicks_df

    return None

# Analyze homepage heatmap
heatmap_analysis = analyze_heatmap_data(
    hotjar,
    site_id='your_site_id',
    page_url='https://yoursite.com/'
)

# Analyze scroll depth
def analyze_scroll_heatmap(hotjar, site_id, page_url):
    """Analyze how far users scroll on a page"""
    heatmaps = hotjar.get_heatmaps(site_id)

    for hm in heatmaps.get('heatmaps', []):
        if hm['page_url'] == page_url:
            heatmap_id = hm['id']
            scroll_data = hotjar._make_request(
                f'sites/{site_id}/heatmaps/{heatmap_id}/scroll'
            )

            if 'scroll_depth' in scroll_data:
                scroll_df = pd.DataFrame(scroll_data['scroll_depth'])

                print(f"\nScroll Depth Analysis for {page_url}")
                print(f"Average scroll depth: {scroll_df['percentage'].mean():.1f}%")
                print(f"Users reaching 25%: {(scroll_df['percentage'] >= 25).sum()}")
                print(f"Users reaching 50%: {(scroll_df['percentage'] >= 50).sum()}")
                print(f"Users reaching 75%: {(scroll_df['percentage'] >= 75).sum()}")
                print(f"Users reaching 100%: {(scroll_df['percentage'] >= 100).sum()}")

                return scroll_df

    return None

scroll_analysis = analyze_scroll_heatmap(
    hotjar,
    site_id='your_site_id',
    page_url='https://yoursite.com/blog/article'
)
```

### 3. Session Recording Analysis

```python
def get_filtered_recordings(hotjar, site_id, filters):
    """
    Get recordings with specific filters
    """
    recordings = hotjar.get_recordings(site_id, filters)

    if 'recordings' in recordings:
        rec_data = []
        for rec in recordings['recordings']:
            rec_data.append({
                'id': rec['id'],
                'created': rec['created_at'],
                'duration': rec['duration'],
                'device': rec['device_type'],
                'browser': rec['browser'],
                'country': rec.get('country', 'Unknown'),
                'url': rec['start_url'],
                'user_id': rec.get('user_id')
            })

        rec_df = pd.DataFrame(rec_data)

        print(f"\nFound {len(rec_df)} recordings")
        print(f"Average duration: {rec_df['duration'].mean():.0f} seconds")
        print(f"\nDevice breakdown:")
        print(rec_df['device'].value_counts())

        return rec_df

    return None

# Get recordings with rage clicks (frustrated users)
rage_click_recordings = get_filtered_recordings(
    hotjar,
    site_id='your_site_id',
    filters={
        'has_rage_click': True,
        'date_from': (datetime.now() - timedelta(days=7)).isoformat(),
        'limit': 100
    }
)

# Get recordings from specific funnel step
funnel_recordings = get_filtered_recordings(
    hotjar,
    site_id='your_site_id',
    filters={
        'page_url': '/checkout',
        'date_from': (datetime.now() - timedelta(days=30)).isoformat(),
        'min_duration': 30,  # At least 30 seconds
        'limit': 50
    }
)

# Analyze recording patterns
def analyze_recording_patterns(recordings_df):
    """Identify patterns in session recordings"""
    if recordings_df is None or recordings_df.empty:
        return None

    # Duration analysis
    duration_bins = [0, 30, 60, 120, 300, float('inf')]
    duration_labels = ['0-30s', '30-60s', '1-2m', '2-5m', '5m+']
    recordings_df['duration_bucket'] = pd.cut(
        recordings_df['duration'],
        bins=duration_bins,
        labels=duration_labels
    )

    print("\nSession Duration Distribution:")
    print(recordings_df['duration_bucket'].value_counts().sort_index())

    # Country analysis
    print("\nTop Countries:")
    print(recordings_df['country'].value_counts().head(10))

    # Device & Browser
    print("\nBrowser Distribution:")
    print(recordings_df['browser'].value_counts())

    return recordings_df

if rage_click_recordings is not None:
    analyze_recording_patterns(rage_click_recordings)
```

### 4. Survey and Feedback Analysis

```python
def get_survey_responses(hotjar, site_id, survey_id=None):
    """Get survey responses"""
    endpoint = f'sites/{site_id}/surveys'
    if survey_id:
        endpoint += f'/{survey_id}/responses'

    responses = hotjar._make_request(endpoint)

    if 'responses' in responses:
        survey_data = []
        for resp in responses['responses']:
            survey_data.append({
                'response_id': resp['id'],
                'created': resp['created_at'],
                'question': resp['question'],
                'answer': resp['answer'],
                'page_url': resp.get('page_url'),
                'device': resp.get('device_type'),
                'country': resp.get('country')
            })

        survey_df = pd.DataFrame(survey_data)

        print(f"\nTotal survey responses: {len(survey_df)}")

        return survey_df

    return None

def analyze_survey_sentiment(survey_df):
    """Analyze survey responses for sentiment and themes"""
    if survey_df is None or survey_df.empty:
        return None

    # For NPS-style questions (0-10 scale)
    if survey_df['answer'].dtype in ['int64', 'float64']:
        promoters = (survey_df['answer'] >= 9).sum()
        passives = ((survey_df['answer'] >= 7) & (survey_df['answer'] <= 8)).sum()
        detractors = (survey_df['answer'] <= 6).sum()

        nps = ((promoters - detractors) / len(survey_df)) * 100

        print(f"\nNPS Analysis:")
        print(f"  Promoters (9-10): {promoters} ({promoters/len(survey_df)*100:.1f}%)")
        print(f"  Passives (7-8): {passives} ({passives/len(survey_df)*100:.1f}%)")
        print(f"  Detractors (0-6): {detractors} ({detractors/len(survey_df)*100:.1f}%)")
        print(f"  NPS Score: {nps:.1f}")

    # For text responses
    else:
        # Most common responses
        print("\nMost Common Responses:")
        print(survey_df['answer'].value_counts().head(10))

        # Simple keyword analysis
        all_text = ' '.join(survey_df['answer'].astype(str).str.lower())
        words = all_text.split()
        from collections import Counter
        word_freq = Counter(words)

        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        filtered_words = {w: c for w, c in word_freq.items()
                         if w not in stop_words and len(w) > 3}

        print("\nTop Keywords:")
        for word, count in sorted(filtered_words.items(),
                                 key=lambda x: x[1], reverse=True)[:20]:
            print(f"  {word}: {count}")

    return survey_df

# Get NPS survey responses
nps_responses = get_survey_responses(
    hotjar,
    site_id='your_site_id',
    survey_id='your_survey_id'
)

if nps_responses is not None:
    analyze_survey_sentiment(nps_responses)

# Analyze feedback by page
def analyze_feedback_by_page(survey_df):
    """Analyze survey responses by page URL"""
    if survey_df is None or 'page_url' not in survey_df.columns:
        return None

    page_scores = survey_df.groupby('page_url').agg({
        'answer': ['count', 'mean'],
        'response_id': 'count'
    }).round(2)

    page_scores.columns = ['responses', 'avg_score', 'total']
    page_scores = page_scores.sort_values('avg_score', ascending=False)

    print("\nFeedback by Page:")
    print(page_scores.head(20))

    return page_scores

if nps_responses is not None:
    page_feedback = analyze_feedback_by_page(nps_responses)
```

### 5. Form Analysis

```python
def analyze_form_performance(hotjar, site_id):
    """
    Analyze form completion and abandonment
    """
    forms = hotjar._make_request(f'sites/{site_id}/forms')

    if 'forms' in forms:
        form_data = []
        for form in forms['forms']:
            form_id = form['id']

            # Get form analytics
            form_stats = hotjar._make_request(
                f'sites/{site_id}/forms/{form_id}/analytics'
            )

            if 'analytics' in form_stats:
                stats = form_stats['analytics']
                form_data.append({
                    'form_name': form['name'],
                    'page_url': form['page_url'],
                    'views': stats['views'],
                    'starts': stats['starts'],
                    'submissions': stats['submissions'],
                    'start_rate': stats['starts'] / stats['views'] * 100 if stats['views'] > 0 else 0,
                    'completion_rate': stats['submissions'] / stats['starts'] * 100 if stats['starts'] > 0 else 0,
                    'avg_time': stats.get('avg_completion_time', 0)
                })

        forms_df = pd.DataFrame(form_data)

        print("\nForm Performance Analysis:")
        print(forms_df.sort_values('completion_rate', ascending=False))

        # Identify problematic forms
        low_completion = forms_df[forms_df['completion_rate'] < 50]
        if not low_completion.empty:
            print("\nForms with Low Completion (<50%):")
            print(low_completion[['form_name', 'completion_rate', 'submissions']])

        return forms_df

    return None

def analyze_form_fields(hotjar, site_id, form_id):
    """Analyze individual form field performance"""
    field_data = hotjar._make_request(
        f'sites/{site_id}/forms/{form_id}/fields'
    )

    if 'fields' in field_data:
        fields = []
        for field in field_data['fields']:
            fields.append({
                'field_name': field['name'],
                'field_type': field['type'],
                'interactions': field['interactions'],
                'drops': field['drops'],
                'drop_rate': field['drops'] / field['interactions'] * 100 if field['interactions'] > 0 else 0,
                'avg_hesitation': field.get('avg_hesitation_time', 0)
            })

        fields_df = pd.DataFrame(fields)

        print(f"\nForm Field Analysis:")
        print(fields_df.sort_values('drop_rate', ascending=False))

        # Identify problematic fields
        problem_fields = fields_df[fields_df['drop_rate'] > 20]
        if not problem_fields.empty:
            print("\nProblematic Fields (>20% drop rate):")
            print(problem_fields[['field_name', 'drop_rate', 'avg_hesitation']])

        return fields_df

    return None

# Analyze all forms
forms_analysis = analyze_form_performance(hotjar, 'your_site_id')

# Analyze specific form fields
if forms_analysis is not None and not forms_analysis.empty:
    # Get the form with lowest completion rate
    worst_form = forms_analysis.loc[forms_analysis['completion_rate'].idxmin()]
    print(f"\nAnalyzing fields for: {worst_form['form_name']}")

    # Note: You would need the form_id here
    # field_analysis = analyze_form_fields(hotjar, 'your_site_id', 'form_id')
```

### 6. Funnel and Conversion Analysis

```python
def create_conversion_funnel(hotjar, site_id, funnel_pages):
    """
    Create conversion funnel from Hotjar data
    """
    funnel_stats = []

    for i, page in enumerate(funnel_pages):
        # Get heatmap/recording data for page
        page_data = hotjar._make_request(
            f'sites/{site_id}/pages/analytics',
            params={'page_url': page}
        )

        if 'analytics' in page_data:
            stats = page_data['analytics']
            funnel_stats.append({
                'step': i + 1,
                'page': page,
                'visitors': stats.get('visitors', 0),
                'avg_time': stats.get('avg_time_on_page', 0)
            })

    funnel_df = pd.DataFrame(funnel_stats)

    # Calculate conversion rates
    funnel_df['conversion_rate'] = (
        funnel_df['visitors'] / funnel_df['visitors'].iloc[0] * 100
        if not funnel_df.empty else 0
    )

    funnel_df['drop_off'] = 100 - funnel_df['conversion_rate']

    print("\nConversion Funnel Analysis:")
    print(funnel_df)

    # Identify biggest drop-off
    if len(funnel_df) > 1:
        funnel_df['step_drop'] = funnel_df['conversion_rate'].diff().abs()
        biggest_drop = funnel_df.loc[funnel_df['step_drop'].idxmax()]
        print(f"\nBiggest drop-off at step {biggest_drop['step']}: {biggest_drop['page']}")

    return funnel_df

# Define funnel
funnel_pages = [
    'https://yoursite.com/',
    'https://yoursite.com/pricing',
    'https://yoursite.com/signup',
    'https://yoursite.com/onboarding',
    'https://yoursite.com/dashboard'
]

funnel = create_conversion_funnel(hotjar, 'your_site_id', funnel_pages)
```

### 7. Incoming Feedback Widget Analysis

```python
def analyze_incoming_feedback(hotjar, site_id):
    """
    Analyze incoming feedback from widgets
    """
    feedback = hotjar.get_feedback(site_id)

    if 'feedback' in feedback:
        feedback_data = []
        for item in feedback['feedback']:
            feedback_data.append({
                'id': item['id'],
                'created': item['created_at'],
                'emotion': item.get('emotion'),  # happy, neutral, sad
                'comment': item.get('comment', ''),
                'page_url': item['page_url'],
                'device': item.get('device_type'),
                'browser': item.get('browser')
            })

        feedback_df = pd.DataFrame(feedback_data)

        print(f"\nIncoming Feedback Analysis:")
        print(f"Total feedback items: {len(feedback_df)}")

        # Emotion breakdown
        if 'emotion' in feedback_df.columns:
            print("\nEmotion Distribution:")
            print(feedback_df['emotion'].value_counts())

            # Calculate satisfaction score
            emotion_scores = {'happy': 1, 'neutral': 0, 'sad': -1}
            feedback_df['score'] = feedback_df['emotion'].map(emotion_scores)
            avg_score = feedback_df['score'].mean()
            print(f"\nAverage satisfaction score: {avg_score:.2f}")

        # Feedback by page
        print("\nFeedback by Page:")
        page_feedback = feedback_df.groupby('page_url').agg({
            'id': 'count',
            'emotion': lambda x: x.value_counts().index[0] if len(x) > 0 else None
        })
        page_feedback.columns = ['count', 'top_emotion']
        print(page_feedback.sort_values('count', ascending=False).head(10))

        return feedback_df

    return None

feedback_analysis = analyze_incoming_feedback(hotjar, 'your_site_id')
```

## Installation

```bash
uv pip install requests pandas numpy
```

Hotjar tracking script (add to website):

```html
<!-- Hotjar Tracking Code -->
<script>
    (function(h,o,t,j,a,r){
        h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
        h._hjSettings={hjid:YOUR_HOTJAR_ID,hjsv:6};
        a=o.getElementsByTagName('head')[0];
        r=o.createElement('script');r.async=1;
        r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
        a.appendChild(r);
    })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
</script>
```

## Authentication

1. Sign up at https://www.hotjar.com
2. Navigate to Account Settings > API
3. Generate a Personal API Token
4. Copy the token for use in API requests

## Quick Start

```python
import requests

# Hotjar API credentials
API_KEY = 'your_api_key'
SITE_ID = 'your_site_id'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Get heatmaps
response = requests.get(
    f'https://api.hotjar.com/v1/sites/{SITE_ID}/heatmaps',
    headers=headers
)

heatmaps = response.json()
print(f"Heatmaps: {len(heatmaps.get('heatmaps', []))}")

# Get recordings
response = requests.get(
    f'https://api.hotjar.com/v1/sites/{SITE_ID}/recordings',
    headers=headers,
    params={'limit': 10}
)

recordings = response.json()
print(f"Recordings: {len(recordings.get('recordings', []))}")
```

## Key Features

- **Heatmaps**: Click, move, and scroll heatmaps
- **Session Recordings**: Watch real user sessions
- **Conversion Funnels**: Identify drop-off points
- **Form Analysis**: Field-level abandonment tracking
- **Feedback Polls**: On-site surveys and NPS
- **Incoming Feedback**: Widget for user comments
- **Rage Click Detection**: Identify frustrated users

## References

- [Hotjar API Documentation](https://help.hotjar.com/hc/en-us/sections/4410331327515-API)
- [Hotjar JavaScript API](https://help.hotjar.com/hc/en-us/articles/115011639927)
- [Heatmaps Guide](https://www.hotjar.com/heatmaps/)
- [Session Recordings Guide](https://www.hotjar.com/session-recordings/)
- [Surveys & Feedback](https://www.hotjar.com/surveys/)

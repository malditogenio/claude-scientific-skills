---
name: google-search-console
description: "SEO performance data. Search queries, rankings, click-through rates, impressions, indexing status, Core Web Vitals, mobile usability."
---

# Google Search Console

## Overview

Google Search Console provides data about your site's organic search performance, including search queries, rankings, click-through rates, and technical SEO issues. This skill covers accessing Search Console data via API, analyzing search performance, and optimizing for organic visibility.

## When to Use This Skill

- Analyzing organic search traffic and rankings
- Identifying top-performing keywords
- Monitoring click-through rates and impressions
- Tracking page indexing status
- Analyzing Core Web Vitals and page experience
- Identifying SEO issues and opportunities
- Competitive keyword research

## Core Capabilities

### 1. Search Console API Setup

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, timedelta

class SearchConsoleAPI:
    def __init__(self, service_account_file):
        self.credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=['https://www.googleapis.com/auth/webmasters.readonly']
        )
        self.service = build('searchconsole', 'v1', credentials=self.credentials)

    def list_sites(self):
        """List all sites/properties"""
        sites = self.service.sites().list().execute()
        return sites.get('siteEntry', [])

    def query_search_analytics(self, site_url, start_date, end_date,
                               dimensions=None, filters=None, row_limit=1000):
        """
        Query search analytics data

        dimensions: List of dimensions (query, page, country, device, date)
        filters: List of filter objects
        """
        request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': dimensions or ['query'],
            'rowLimit': row_limit
        }

        if filters:
            request['dimensionFilterGroups'] = filters

        response = self.service.searchanalytics().query(
            siteUrl=site_url,
            body=request
        ).execute()

        return response.get('rows', [])

# Initialize Search Console API
gsc = SearchConsoleAPI(service_account_file='service-account.json')

# List all sites
sites = gsc.list_sites()
print("Search Console Properties:")
for site in sites:
    print(f"  {site['siteUrl']} - {site['permissionLevel']}")
```

### 2. Search Query Analysis

```python
def analyze_search_queries(gsc, site_url, days=30):
    """
    Analyze top search queries
    """
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    # Get query data
    rows = gsc.query_search_analytics(
        site_url=site_url,
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d'),
        dimensions=['query'],
        row_limit=1000
    )

    # Convert to DataFrame
    query_data = []
    for row in rows:
        query_data.append({
            'query': row['keys'][0],
            'clicks': row['clicks'],
            'impressions': row['impressions'],
            'ctr': row['ctr'] * 100,
            'position': row['position']
        })

    df = pd.DataFrame(query_data)

    print(f"\nSearch Query Analysis (Last {days} days):")
    print(f"Total queries: {len(df)}")
    print(f"Total clicks: {df['clicks'].sum():,.0f}")
    print(f"Total impressions: {df['impressions'].sum():,.0f}")
    print(f"Average CTR: {df['ctr'].mean():.2f}%")
    print(f"Average position: {df['position'].mean():.1f}")

    # Top queries by clicks
    print("\nTop 20 Queries by Clicks:")
    print(df.nlargest(20, 'clicks')[['query', 'clicks', 'ctr', 'position']])

    # Low CTR opportunities (high impressions, low CTR)
    low_ctr = df[(df['impressions'] > 100) & (df['ctr'] < 2)]
    if not low_ctr.empty:
        print("\nLow CTR Opportunities (>100 impressions, <2% CTR):")
        print(low_ctr.nlargest(10, 'impressions')[
            ['query', 'impressions', 'ctr', 'position']
        ])

    return df

# Analyze queries
query_df = analyze_search_queries(
    gsc,
    site_url='https://yoursite.com/',
    days=30
)

def analyze_query_trends(gsc, site_url, query, days=90):
    """Analyze trend for specific query"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    rows = gsc.query_search_analytics(
        site_url=site_url,
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d'),
        dimensions=['date'],
        filters=[{
            'filters': [{
                'dimension': 'query',
                'operator': 'equals',
                'expression': query
            }]
        }]
    )

    trend_data = []
    for row in rows:
        trend_data.append({
            'date': row['keys'][0],
            'clicks': row['clicks'],
            'impressions': row['impressions'],
            'ctr': row['ctr'] * 100,
            'position': row['position']
        })

    trend_df = pd.DataFrame(trend_data)
    trend_df['date'] = pd.to_datetime(trend_df['date'])
    trend_df = trend_df.sort_values('date')

    print(f"\nTrend Analysis for '{query}':")
    print(f"Date range: {trend_df['date'].min()} to {trend_df['date'].max()}")
    print(f"Average position: {trend_df['position'].mean():.1f}")
    print(f"Total clicks: {trend_df['clicks'].sum():,.0f}")

    return trend_df

# Analyze specific query trend
# query_trend = analyze_query_trends(
#     gsc,
#     site_url='https://yoursite.com/',
#     query='your target keyword',
#     days=90
# )
```

### 3. Page Performance Analysis

```python
def analyze_page_performance(gsc, site_url, days=30):
    """
    Analyze performance by page
    """
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    rows = gsc.query_search_analytics(
        site_url=site_url,
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d'),
        dimensions=['page'],
        row_limit=1000
    )

    page_data = []
    for row in rows:
        page_data.append({
            'page': row['keys'][0],
            'clicks': row['clicks'],
            'impressions': row['impressions'],
            'ctr': row['ctr'] * 100,
            'position': row['position']
        })

    df = pd.DataFrame(page_data)

    print(f"\nPage Performance Analysis:")
    print(f"Total pages: {len(df)}")

    # Top pages
    print("\nTop 20 Pages by Clicks:")
    print(df.nlargest(20, 'clicks')[['page', 'clicks', 'ctr', 'position']])

    # Pages with declining performance (high position, low CTR)
    declining = df[(df['position'] < 10) & (df['ctr'] < 5)]
    if not declining.empty:
        print("\nPages Needing Optimization (Position <10, CTR <5%):")
        print(declining[['page', 'position', 'ctr', 'clicks']])

    return df

page_df = analyze_page_performance(
    gsc,
    site_url='https://yoursite.com/',
    days=30
)

def get_page_queries(gsc, site_url, page_url, days=30):
    """Get queries driving traffic to specific page"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    rows = gsc.query_search_analytics(
        site_url=site_url,
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d'),
        dimensions=['query'],
        filters=[{
            'filters': [{
                'dimension': 'page',
                'operator': 'equals',
                'expression': page_url
            }]
        }],
        row_limit=100
    )

    query_data = []
    for row in rows:
        query_data.append({
            'query': row['keys'][0],
            'clicks': row['clicks'],
            'impressions': row['impressions'],
            'ctr': row['ctr'] * 100,
            'position': row['position']
        })

    df = pd.DataFrame(query_data)

    print(f"\nQueries for {page_url}:")
    print(df.head(20))

    return df

# Get queries for specific page
# page_queries = get_page_queries(
#     gsc,
#     site_url='https://yoursite.com/',
#     page_url='https://yoursite.com/blog/post-title'
# )
```

### 4. Device and Country Analysis

```python
def analyze_by_device(gsc, site_url, days=30):
    """Analyze performance by device type"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    rows = gsc.query_search_analytics(
        site_url=site_url,
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d'),
        dimensions=['device']
    )

    device_data = []
    for row in rows:
        device_data.append({
            'device': row['keys'][0],
            'clicks': row['clicks'],
            'impressions': row['impressions'],
            'ctr': row['ctr'] * 100,
            'position': row['position']
        })

    df = pd.DataFrame(device_data)

    print("\nPerformance by Device:")
    print(df)

    # Calculate device distribution
    df['click_share'] = df['clicks'] / df['clicks'].sum() * 100

    print("\nClick Distribution:")
    for _, row in df.iterrows():
        print(f"  {row['device']}: {row['click_share']:.1f}%")

    return df

device_df = analyze_by_device(gsc, site_url='https://yoursite.com/')

def analyze_by_country(gsc, site_url, days=30, top_n=20):
    """Analyze performance by country"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    rows = gsc.query_search_analytics(
        site_url=site_url,
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d'),
        dimensions=['country'],
        row_limit=top_n
    )

    country_data = []
    for row in rows:
        country_data.append({
            'country': row['keys'][0],
            'clicks': row['clicks'],
            'impressions': row['impressions'],
            'ctr': row['ctr'] * 100,
            'position': row['position']
        })

    df = pd.DataFrame(country_data)

    print(f"\nTop {top_n} Countries by Clicks:")
    print(df)

    return df

country_df = analyze_by_country(gsc, site_url='https://yoursite.com/')
```

### 5. Keyword Opportunity Analysis

```python
def find_keyword_opportunities(gsc, site_url, days=30):
    """
    Find keyword opportunities:
    - High impressions, low clicks (improve CTR)
    - Position 11-20 (potential quick wins)
    - High CTR, low position (create more content)
    """
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    rows = gsc.query_search_analytics(
        site_url=site_url,
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d'),
        dimensions=['query'],
        row_limit=1000
    )

    query_data = []
    for row in rows:
        query_data.append({
            'query': row['keys'][0],
            'clicks': row['clicks'],
            'impressions': row['impressions'],
            'ctr': row['ctr'] * 100,
            'position': row['position']
        })

    df = pd.DataFrame(query_data)

    print("\n=== KEYWORD OPPORTUNITIES ===")

    # Opportunity 1: High impressions, low CTR
    high_imp_low_ctr = df[
        (df['impressions'] > 500) & (df['ctr'] < 2)
    ].nlargest(15, 'impressions')

    if not high_imp_low_ctr.empty:
        print("\n1. Improve CTR (>500 impressions, <2% CTR):")
        print(high_imp_low_ctr[['query', 'impressions', 'ctr', 'position']])

    # Opportunity 2: Position 11-20 (quick wins)
    quick_wins = df[
        (df['position'] >= 11) & (df['position'] <= 20) & (df['impressions'] > 100)
    ].nlargest(15, 'impressions')

    if not quick_wins.empty:
        print("\n2. Quick Wins (Position 11-20, >100 impressions):")
        print(quick_wins[['query', 'position', 'impressions', 'clicks']])

    # Opportunity 3: High CTR, poor position
    high_ctr_low_pos = df[
        (df['ctr'] > 5) & (df['position'] > 15)
    ].nlargest(15, 'ctr')

    if not high_ctr_low_pos.empty:
        print("\n3. High Intent Keywords (>5% CTR, Position >15):")
        print(high_ctr_low_pos[['query', 'ctr', 'position', 'impressions']])

    return {
        'improve_ctr': high_imp_low_ctr,
        'quick_wins': quick_wins,
        'high_intent': high_ctr_low_pos
    }

opportunities = find_keyword_opportunities(
    gsc,
    site_url='https://yoursite.com/',
    days=30
)
```

### 6. Competitive Analysis

```python
def compare_query_positions(gsc, site_url, competitor_queries, days=30):
    """
    Track positions for competitive queries
    """
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    results = []

    for query in competitor_queries:
        rows = gsc.query_search_analytics(
            site_url=site_url,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            dimensions=['query'],
            filters=[{
                'filters': [{
                    'dimension': 'query',
                    'operator': 'equals',
                    'expression': query
                }]
            }]
        )

        if rows:
            row = rows[0]
            results.append({
                'query': query,
                'clicks': row['clicks'],
                'impressions': row['impressions'],
                'ctr': row['ctr'] * 100,
                'position': row['position']
            })
        else:
            results.append({
                'query': query,
                'clicks': 0,
                'impressions': 0,
                'ctr': 0,
                'position': None
            })

    df = pd.DataFrame(results)

    print("\nCompetitive Query Tracking:")
    print(df)

    # Identify gaps
    not_ranking = df[df['position'].isna()]
    if not not_ranking.empty:
        print("\nNot Ranking For:")
        print(not_ranking['query'].tolist())

    return df

# Track competitive keywords
competitive_queries = [
    'best marketing analytics tools',
    'marketing automation software',
    'customer data platform'
]

# competitive_positions = compare_query_positions(
#     gsc,
#     site_url='https://yoursite.com/',
#     competitor_queries=competitive_queries
# )
```

### 7. Indexing and Coverage Analysis

```python
def get_index_coverage(gsc, site_url):
    """
    Note: This requires the Google Search Console Inspect URL API
    Currently in beta - alternative is to use Search Console UI
    """
    # Get sitemap information
    sitemaps = gsc.service.sitemaps().list(siteUrl=site_url).execute()

    if 'sitemap' in sitemaps:
        print("\nSitemaps:")
        for sitemap in sitemaps['sitemap']:
            print(f"  Path: {sitemap['path']}")
            print(f"  Last Submitted: {sitemap.get('lastSubmitted', 'N/A')}")
            print(f"  Last Downloaded: {sitemap.get('lastDownloaded', 'N/A')}")

            if 'contents' in sitemap:
                for content in sitemap['contents']:
                    print(f"    Type: {content['type']}")
                    print(f"    Submitted: {content.get('submitted', 'N/A')}")
                    print(f"    Indexed: {content.get('indexed', 'N/A')}")

    return sitemaps

# Get indexing status
# indexing_status = get_index_coverage(gsc, 'https://yoursite.com/')
```

### 8. Date Comparison Analysis

```python
def compare_periods(gsc, site_url, current_days=30, comparison_days=30):
    """
    Compare current period vs previous period
    """
    end_date = datetime.now().date()
    current_start = end_date - timedelta(days=current_days)

    comparison_end = current_start - timedelta(days=1)
    comparison_start = comparison_end - timedelta(days=comparison_days)

    # Get current period data
    current_rows = gsc.query_search_analytics(
        site_url=site_url,
        start_date=current_start.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d'),
        dimensions=['query'],
        row_limit=1000
    )

    current_df = pd.DataFrame([
        {
            'query': r['keys'][0],
            'clicks': r['clicks'],
            'impressions': r['impressions'],
            'ctr': r['ctr'],
            'position': r['position']
        }
        for r in current_rows
    ])

    # Get comparison period data
    comparison_rows = gsc.query_search_analytics(
        site_url=site_url,
        start_date=comparison_start.strftime('%Y-%m-%d'),
        end_date=comparison_end.strftime('%Y-%m-%d'),
        dimensions=['query'],
        row_limit=1000
    )

    comparison_df = pd.DataFrame([
        {
            'query': r['keys'][0],
            'clicks': r['clicks'],
            'impressions': r['impressions'],
            'ctr': r['ctr'],
            'position': r['position']
        }
        for r in comparison_rows
    ])

    # Calculate totals
    print(f"\nPeriod Comparison:")
    print(f"Current ({current_start} to {end_date}):")
    print(f"  Total Clicks: {current_df['clicks'].sum():,.0f}")
    print(f"  Total Impressions: {current_df['impressions'].sum():,.0f}")

    print(f"\nPrevious ({comparison_start} to {comparison_end}):")
    print(f"  Total Clicks: {comparison_df['clicks'].sum():,.0f}")
    print(f"  Total Impressions: {comparison_df['impressions'].sum():,.0f}")

    # Calculate changes
    click_change = (current_df['clicks'].sum() - comparison_df['clicks'].sum()) / comparison_df['clicks'].sum() * 100
    imp_change = (current_df['impressions'].sum() - comparison_df['impressions'].sum()) / comparison_df['impressions'].sum() * 100

    print(f"\nChanges:")
    print(f"  Clicks: {click_change:+.1f}%")
    print(f"  Impressions: {imp_change:+.1f}%")

    return current_df, comparison_df

# Compare periods
# current, previous = compare_periods(gsc, 'https://yoursite.com/')
```

## Installation

```bash
uv pip install google-api-python-client google-auth pandas
```

## Authentication

1. Create a service account in Google Cloud Console
2. Enable the Google Search Console API
3. Add the service account email as a user in Search Console (with at least "Restricted" permission)
4. Download the service account JSON key

## Quick Start

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Authenticate
credentials = service_account.Credentials.from_service_account_file(
    'service-account.json',
    scopes=['https://www.googleapis.com/auth/webmasters.readonly']
)

service = build('searchconsole', 'v1', credentials=credentials)

# List sites
sites = service.sites().list().execute()
print(f"Sites: {sites}")

# Query search data
site_url = 'https://yoursite.com/'
end_date = datetime.now().date()
start_date = end_date - timedelta(days=7)

request = {
    'startDate': start_date.strftime('%Y-%m-%d'),
    'endDate': end_date.strftime('%Y-%m-%d'),
    'dimensions': ['query'],
    'rowLimit': 10
}

response = service.searchanalytics().query(
    siteUrl=site_url,
    body=request
).execute()

print(f"Top queries: {response.get('rows', [])}")
```

## Key Metrics

- **Clicks**: Number of clicks from search results
- **Impressions**: Number of times page appeared in search
- **CTR**: Click-through rate (clicks/impressions)
- **Position**: Average position in search results
- **Coverage**: Pages indexed vs total pages

## References

- [Search Console API Documentation](https://developers.google.com/webmaster-tools/search-console-api-original)
- [Search Analytics API](https://developers.google.com/webmaster-tools/search-console-api-original/v3/searchanalytics)
- [URL Inspection API](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect)

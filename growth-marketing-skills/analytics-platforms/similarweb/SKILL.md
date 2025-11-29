---
name: similarweb
description: "Competitive intelligence platform. Traffic analysis, market share, audience insights, competitor benchmarking, referral sources, keyword analysis."
---

# SimilarWeb Competitive Intelligence

## Overview

SimilarWeb is a competitive intelligence platform that provides insights into website traffic, audience behavior, and market trends. This skill covers using the SimilarWeb API to analyze competitors, track market share, identify traffic sources, and discover growth opportunities.

## When to Use This Skill

- Competitive analysis and benchmarking
- Market research and sizing
- Identifying traffic sources and strategies
- Audience overlap analysis
- Keyword and SEO competitive research
- Partnership and advertising opportunities
- Industry trend analysis

## Core Capabilities

### 1. SimilarWeb API Setup

```python
import requests
import pandas as pd
from datetime import datetime, timedelta
import json

class SimilarWebAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.similarweb.com"
        self.headers = {
            'api-key': api_key,
            'Content-Type': 'application/json'
        }

    def _make_request(self, endpoint, params=None):
        """Make authenticated request to SimilarWeb API"""
        url = f"{self.base_url}/{endpoint}"

        params = params or {}
        params['api_key'] = self.api_key

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()

    def get_website_overview(self, domain, start_date, end_date, country='world',
                            main_domain_only=False):
        """Get overall website metrics"""
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'country': country,
            'main_domain_only': str(main_domain_only).lower()
        }

        return self._make_request(
            f'v1/website/{domain}/total-traffic-and-engagement/visits',
            params=params
        )

    def get_traffic_sources(self, domain, start_date, end_date, country='world'):
        """Get traffic source breakdown"""
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'country': country
        }

        return self._make_request(
            f'v1/website/{domain}/traffic-sources/overview',
            params=params
        )

    def get_referrals(self, domain, start_date, end_date, country='world'):
        """Get top referring websites"""
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'country': country
        }

        return self._make_request(
            f'v1/website/{domain}/referrals',
            params=params
        )

    def get_organic_keywords(self, domain, start_date, end_date, country='world'):
        """Get top organic search keywords"""
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'country': country
        }

        return self._make_request(
            f'v1/website/{domain}/organic-keywords',
            params=params
        )

# Initialize SimilarWeb API
similarweb = SimilarWebAPI(api_key='YOUR_API_KEY')

# Date range for analysis
end_date = datetime.now().strftime('%Y-%m')
start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m')
```

### 2. Website Traffic Analysis

```python
def analyze_website_traffic(similarweb, domain, months=3):
    """
    Analyze website traffic metrics
    """
    end_date = datetime.now().strftime('%Y-%m')
    start_date = (datetime.now() - timedelta(days=months*30)).strftime('%Y-%m')

    # Get traffic overview
    traffic = similarweb.get_website_overview(
        domain=domain,
        start_date=start_date,
        end_date=end_date
    )

    if 'visits' in traffic:
        visits_data = []
        for visit in traffic['visits']:
            visits_data.append({
                'date': visit['date'],
                'visits': visit['visits']
            })

        visits_df = pd.DataFrame(visits_data)
        visits_df['date'] = pd.to_datetime(visits_df['date'])

        print(f"\nTraffic Analysis for {domain}:")
        print(f"Period: {start_date} to {end_date}")
        print(f"Total visits: {visits_df['visits'].sum():,.0f}")
        print(f"Average monthly visits: {visits_df['visits'].mean():,.0f}")

        # Traffic trend
        if len(visits_df) > 1:
            first_month = visits_df.iloc[0]['visits']
            last_month = visits_df.iloc[-1]['visits']
            growth = (last_month - first_month) / first_month * 100

            print(f"\nGrowth: {growth:+.1f}%")

        print("\nMonthly Visits:")
        print(visits_df)

        return visits_df

    return None

# Analyze competitor traffic
competitor_traffic = analyze_website_traffic(
    similarweb,
    domain='competitor.com',
    months=6
)

def compare_websites(similarweb, domains, months=3):
    """Compare multiple websites"""
    end_date = datetime.now().strftime('%Y-%m')
    start_date = (datetime.now() - timedelta(days=months*30)).strftime('%Y-%m')

    comparison_data = []

    for domain in domains:
        try:
            traffic = similarweb.get_website_overview(
                domain=domain,
                start_date=start_date,
                end_date=end_date
            )

            if 'visits' in traffic:
                total_visits = sum(v['visits'] for v in traffic['visits'])
                avg_visits = total_visits / len(traffic['visits'])

                comparison_data.append({
                    'domain': domain,
                    'total_visits': total_visits,
                    'avg_monthly_visits': avg_visits
                })

        except Exception as e:
            print(f"Error fetching data for {domain}: {e}")

    comparison_df = pd.DataFrame(comparison_data)
    comparison_df = comparison_df.sort_values('total_visits', ascending=False)

    print("\nWebsite Comparison:")
    print(comparison_df)

    return comparison_df

# Compare competitors
competitors = ['yoursite.com', 'competitor1.com', 'competitor2.com']
comparison = compare_websites(similarweb, competitors, months=3)
```

### 3. Traffic Source Analysis

```python
def analyze_traffic_sources(similarweb, domain):
    """
    Analyze where traffic comes from
    """
    end_date = datetime.now().strftime('%Y-%m')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m')

    sources = similarweb.get_traffic_sources(
        domain=domain,
        start_date=start_date,
        end_date=end_date
    )

    if 'overview' in sources:
        overview = sources['overview']

        source_breakdown = {
            'Direct': overview.get('direct', 0) * 100,
            'Email': overview.get('mail', 0) * 100,
            'Referrals': overview.get('referrals', 0) * 100,
            'Social': overview.get('social', 0) * 100,
            'Organic Search': overview.get('search', 0) * 100,
            'Paid Search': overview.get('paid_search', 0) * 100,
            'Display Ads': overview.get('display_ads', 0) * 100
        }

        print(f"\nTraffic Sources for {domain}:")
        for source, percentage in sorted(source_breakdown.items(),
                                        key=lambda x: x[1], reverse=True):
            if percentage > 0:
                print(f"  {source}: {percentage:.2f}%")

        return pd.DataFrame([source_breakdown])

    return None

# Analyze traffic sources
traffic_sources = analyze_traffic_sources(similarweb, 'competitor.com')

def compare_traffic_sources(similarweb, domains):
    """Compare traffic source mix across competitors"""
    all_sources = []

    for domain in domains:
        try:
            end_date = datetime.now().strftime('%Y-%m')
            start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m')

            sources = similarweb.get_traffic_sources(
                domain=domain,
                start_date=start_date,
                end_date=end_date
            )

            if 'overview' in sources:
                overview = sources['overview']
                all_sources.append({
                    'domain': domain,
                    'direct': overview.get('direct', 0) * 100,
                    'search': overview.get('search', 0) * 100,
                    'social': overview.get('social', 0) * 100,
                    'paid': overview.get('paid_search', 0) * 100,
                    'referrals': overview.get('referrals', 0) * 100
                })

        except Exception as e:
            print(f"Error for {domain}: {e}")

    sources_df = pd.DataFrame(all_sources)

    print("\nTraffic Source Comparison:")
    print(sources_df)

    return sources_df

# Compare traffic sources
source_comparison = compare_traffic_sources(
    similarweb,
    ['yoursite.com', 'competitor1.com', 'competitor2.com']
)
```

### 4. Referral Analysis

```python
def analyze_referrals(similarweb, domain):
    """
    Analyze top referring websites
    """
    end_date = datetime.now().strftime('%Y-%m')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m')

    referrals = similarweb.get_referrals(
        domain=domain,
        start_date=start_date,
        end_date=end_date
    )

    if 'referrals' in referrals:
        referral_data = []
        for ref in referrals['referrals']:
            referral_data.append({
                'referring_site': ref['domain'],
                'share': ref['share'] * 100,
                'change': ref.get('change', 0)
            })

        referrals_df = pd.DataFrame(referral_data)
        referrals_df = referrals_df.sort_values('share', ascending=False)

        print(f"\nTop Referring Websites for {domain}:")
        print(referrals_df.head(20))

        # Identify partnership opportunities
        high_value_referrals = referrals_df[referrals_df['share'] > 1]
        print(f"\nHigh-Value Referral Sources (>1% of traffic):")
        print(high_value_referrals)

        return referrals_df

    return None

# Analyze referrals
referral_analysis = analyze_referrals(similarweb, 'competitor.com')

def find_shared_referrals(similarweb, domains):
    """Find websites that refer traffic to multiple competitors"""
    all_referrals = {}

    for domain in domains:
        try:
            end_date = datetime.now().strftime('%Y-%m')
            start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m')

            referrals = similarweb.get_referrals(
                domain=domain,
                start_date=start_date,
                end_date=end_date
            )

            if 'referrals' in referrals:
                for ref in referrals['referrals'][:50]:  # Top 50
                    ref_domain = ref['domain']
                    if ref_domain not in all_referrals:
                        all_referrals[ref_domain] = []
                    all_referrals[ref_domain].append(domain)

        except Exception as e:
            print(f"Error for {domain}: {e}")

    # Find shared referrals
    shared = {k: v for k, v in all_referrals.items() if len(v) > 1}

    print("\nShared Referral Sources:")
    for referral, targets in sorted(shared.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {referral} → {', '.join(targets)}")

    return shared

# Find partnership opportunities
shared_referrals = find_shared_referrals(
    similarweb,
    ['competitor1.com', 'competitor2.com', 'competitor3.com']
)
```

### 5. Keyword Analysis

```python
def analyze_organic_keywords(similarweb, domain):
    """
    Analyze organic search keywords
    """
    end_date = datetime.now().strftime('%Y-%m')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m')

    keywords = similarweb.get_organic_keywords(
        domain=domain,
        start_date=start_date,
        end_date=end_date
    )

    if 'keywords' in keywords:
        keyword_data = []
        for kw in keywords['keywords']:
            keyword_data.append({
                'keyword': kw['keyword'],
                'position': kw.get('position'),
                'volume': kw.get('volume', 0),
                'share': kw.get('share', 0) * 100
            })

        keywords_df = pd.DataFrame(keyword_data)
        keywords_df = keywords_df.sort_values('share', ascending=False)

        print(f"\nTop Organic Keywords for {domain}:")
        print(keywords_df.head(20))

        # High-value keywords
        high_volume = keywords_df[keywords_df['volume'] > 1000]
        print(f"\nHigh-Volume Keywords (>1000 searches/mo):")
        print(high_volume.head(10))

        return keywords_df

    return None

# Analyze keywords
keyword_analysis = analyze_organic_keywords(similarweb, 'competitor.com')

def find_keyword_gaps(similarweb, your_domain, competitor_domains):
    """Find keywords competitors rank for but you don't"""
    # Get your keywords
    your_keywords = analyze_organic_keywords(similarweb, your_domain)

    if your_keywords is None:
        return None

    your_kw_set = set(your_keywords['keyword'].str.lower())

    # Get competitor keywords
    gaps = []

    for competitor in competitor_domains:
        try:
            comp_keywords = analyze_organic_keywords(similarweb, competitor)

            if comp_keywords is not None:
                # Find keywords they have that you don't
                comp_kw_set = set(comp_keywords['keyword'].str.lower())
                unique_to_comp = comp_kw_set - your_kw_set

                for kw in unique_to_comp:
                    kw_row = comp_keywords[comp_keywords['keyword'].str.lower() == kw].iloc[0]
                    gaps.append({
                        'keyword': kw,
                        'competitor': competitor,
                        'volume': kw_row.get('volume', 0),
                        'position': kw_row.get('position')
                    })

        except Exception as e:
            print(f"Error analyzing {competitor}: {e}")

    gaps_df = pd.DataFrame(gaps)
    gaps_df = gaps_df.sort_values('volume', ascending=False)

    print("\nKeyword Gaps (Competitors rank, you don't):")
    print(gaps_df.head(30))

    return gaps_df

# Find keyword opportunities
# keyword_gaps = find_keyword_gaps(
#     similarweb,
#     your_domain='yoursite.com',
#     competitor_domains=['competitor1.com', 'competitor2.com']
# )
```

### 6. Audience Analysis

```python
def analyze_audience_interests(similarweb, domain):
    """
    Analyze audience interests and demographics
    """
    end_date = datetime.now().strftime('%Y-%m')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m')

    # Get audience interests
    try:
        interests = similarweb._make_request(
            f'v1/website/{domain}/audience-interests',
            params={
                'start_date': start_date,
                'end_date': end_date
            }
        )

        if 'categories' in interests:
            print(f"\nAudience Interests for {domain}:")
            for category in interests['categories'][:10]:
                print(f"  {category['name']}: {category['affinity']:.2f}x affinity")

        return interests

    except Exception as e:
        print(f"Error getting audience interests: {e}")
        return None

# Analyze audience
# audience = analyze_audience_interests(similarweb, 'competitor.com')

def get_similar_sites(similarweb, domain):
    """Find similar websites"""
    try:
        similar = similarweb._make_request(
            f'v1/website/{domain}/similar-sites/similarsites'
        )

        if 'similar_sites' in similar:
            similar_data = []
            for site in similar['similar_sites']:
                similar_data.append({
                    'domain': site['domain'],
                    'score': site['score']
                })

            similar_df = pd.DataFrame(similar_data)

            print(f"\nSimilar Websites to {domain}:")
            print(similar_df)

            return similar_df

    except Exception as e:
        print(f"Error getting similar sites: {e}")

    return None

# Find similar sites
# similar_sites = get_similar_sites(similarweb, 'yoursite.com')
```

### 7. Market Analysis

```python
def analyze_market_share(similarweb, domains, industry='All'):
    """
    Calculate market share among competitors
    """
    end_date = datetime.now().strftime('%Y-%m')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m')

    market_data = []

    for domain in domains:
        try:
            traffic = similarweb.get_website_overview(
                domain=domain,
                start_date=start_date,
                end_date=end_date
            )

            if 'visits' in traffic:
                total_visits = sum(v['visits'] for v in traffic['visits'])
                market_data.append({
                    'domain': domain,
                    'visits': total_visits
                })

        except Exception as e:
            print(f"Error for {domain}: {e}")

    market_df = pd.DataFrame(market_data)
    total_market = market_df['visits'].sum()
    market_df['market_share'] = market_df['visits'] / total_market * 100
    market_df = market_df.sort_values('market_share', ascending=False)

    print(f"\n{industry} Market Share Analysis:")
    for _, row in market_df.iterrows():
        print(f"  {row['domain']}: {row['market_share']:.1f}% ({row['visits']:,.0f} visits)")

    return market_df

# Analyze market share
market_players = [
    'yoursite.com',
    'competitor1.com',
    'competitor2.com',
    'competitor3.com'
]

market_share = analyze_market_share(
    similarweb,
    domains=market_players,
    industry='Marketing Analytics'
)
```

### 8. Competitive Monitoring Dashboard

```python
def create_competitive_report(similarweb, your_domain, competitors):
    """
    Generate comprehensive competitive intelligence report
    """
    report = {
        'generated_at': datetime.now().isoformat(),
        'your_domain': your_domain,
        'competitors': competitors
    }

    print(f"\n{'='*60}")
    print(f"COMPETITIVE INTELLIGENCE REPORT")
    print(f"Generated: {report['generated_at']}")
    print(f"{'='*60}")

    # 1. Traffic comparison
    print("\n1. TRAFFIC COMPARISON")
    traffic_comp = compare_websites(similarweb, [your_domain] + competitors)
    report['traffic'] = traffic_comp.to_dict('records')

    # 2. Traffic sources
    print("\n2. TRAFFIC SOURCE MIX")
    source_comp = compare_traffic_sources(similarweb, [your_domain] + competitors)
    report['sources'] = source_comp.to_dict('records')

    # 3. Market share
    print("\n3. MARKET SHARE")
    market = analyze_market_share(similarweb, [your_domain] + competitors)
    report['market_share'] = market.to_dict('records')

    # 4. Top referrals for each competitor
    print("\n4. TOP REFERRAL SOURCES")
    for domain in competitors[:3]:  # Limit to top 3 competitors
        print(f"\n  {domain}:")
        refs = analyze_referrals(similarweb, domain)
        if refs is not None:
            print(refs.head(5))

    return report

# Generate full competitive report
# competitive_report = create_competitive_report(
#     similarweb,
#     your_domain='yoursite.com',
#     competitors=['competitor1.com', 'competitor2.com', 'competitor3.com']
# )
```

## Installation

```bash
uv pip install requests pandas numpy
```

## Authentication

1. Sign up for SimilarWeb API access
2. Subscribe to an API plan (Developer, Business, or Enterprise)
3. Get your API key from the dashboard
4. Use the API key in requests

## Quick Start

```python
import requests

# SimilarWeb API credentials
API_KEY = 'your_api_key'
DOMAIN = 'example.com'

# Get website overview
url = f'https://api.similarweb.com/v1/website/{DOMAIN}/total-traffic-and-engagement/visits'

params = {
    'api_key': API_KEY,
    'start_date': '2024-01',
    'end_date': '2024-03',
    'country': 'world',
    'main_domain_only': 'false'
}

response = requests.get(url, params=params)
data = response.json()

print(f"Traffic data: {data}")
```

## Key Metrics

- **Visits**: Total website visits
- **Unique Visitors**: Distinct visitors
- **Pages per Visit**: Average pages viewed
- **Bounce Rate**: Single-page sessions
- **Avg Visit Duration**: Time spent on site
- **Traffic Sources**: Direct, search, social, referral breakdown
- **Market Share**: Share of total industry traffic

## References

- [SimilarWeb API Documentation](https://developers.similarweb.com/)
- [Digital Data API](https://developers.similarweb.com/digital-data-api)
- [Website Analysis API](https://developers.similarweb.com/website-analysis-api)
- [Keyword Analysis API](https://developers.similarweb.com/keyword-analysis-api)

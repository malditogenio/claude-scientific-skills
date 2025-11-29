---
name: social-listening
description: "Social listening methodology for brand monitoring, sentiment tracking, competitive intelligence, crisis management, trend detection, and consumer insights."
---

# Social Listening Methodology

## Overview

Social listening is the strategic practice of monitoring, analyzing, and responding to conversations about your brand, industry, and competitors across social media and the web. This skill provides comprehensive methodology, best practices, and frameworks for implementing effective social listening programs that drive business decisions, protect brand reputation, and identify growth opportunities.

## When to Use This Skill

- Building a social listening strategy from scratch
- Brand reputation monitoring and management
- Crisis detection and response planning
- Competitive intelligence gathering
- Market research and consumer insights
- Product development and feedback analysis
- Influencer identification and relationship building
- Trend detection and market analysis
- Customer service and support optimization
- Campaign performance measurement

## Core Concepts

### Social Listening vs. Social Monitoring

**Social Monitoring** (Reactive):
- Tracking direct brand mentions
- Responding to customer inquiries
- Counting metrics (likes, shares, comments)
- Day-to-day management

**Social Listening** (Proactive):
- Analyzing broader conversations and themes
- Understanding sentiment and context
- Identifying trends and opportunities
- Strategic insights and decision-making

### The Social Listening Framework

```
Data Collection → Analysis → Insights → Action → Measurement
       ↑                                              ↓
       └──────────────────────────────────────────────┘
                    (Continuous Loop)
```

## Core Capabilities

### 1. Setting Up a Social Listening Program

#### Define Objectives

```python
# Example: Social Listening Objectives Framework

objectives_framework = {
    'brand_health': {
        'primary_goal': 'Monitor brand reputation and sentiment',
        'key_metrics': [
            'sentiment_score',
            'share_of_voice',
            'mention_volume',
            'net_promoter_score'
        ],
        'success_criteria': 'Maintain 70%+ positive sentiment'
    },

    'crisis_management': {
        'primary_goal': 'Early detection and response to issues',
        'key_metrics': [
            'negative_sentiment_spikes',
            'mention_volume_anomalies',
            'response_time',
            'issue_resolution_rate'
        ],
        'success_criteria': 'Detect issues within 1 hour, respond within 2 hours'
    },

    'competitive_intelligence': {
        'primary_goal': 'Track competitor activities and market positioning',
        'key_metrics': [
            'competitive_share_of_voice',
            'feature_comparisons',
            'pricing_discussions',
            'customer_switching_intent'
        ],
        'success_criteria': 'Maintain top 3 share of voice in category'
    },

    'product_development': {
        'primary_goal': 'Gather product feedback and feature requests',
        'key_metrics': [
            'feature_request_frequency',
            'pain_point_mentions',
            'satisfaction_scores',
            'use_case_diversity'
        ],
        'success_criteria': 'Identify 10+ validated feature requests per quarter'
    },

    'customer_insights': {
        'primary_goal': 'Understand customer needs and behaviors',
        'key_metrics': [
            'audience_demographics',
            'purchase_intent_signals',
            'usage_patterns',
            'pain_points'
        ],
        'success_criteria': 'Generate 5+ actionable insights per month'
    }
}

# Set your objectives
def define_listening_objectives(business_goals):
    """
    Align social listening objectives with business goals

    Args:
        business_goals: List of primary business objectives

    Returns: Structured listening objectives
    """
    listening_objectives = []

    for goal in business_goals:
        if 'brand awareness' in goal.lower():
            listening_objectives.append(objectives_framework['brand_health'])
        elif 'risk management' in goal.lower():
            listening_objectives.append(objectives_framework['crisis_management'])
        elif 'market position' in goal.lower():
            listening_objectives.append(objectives_framework['competitive_intelligence'])
        elif 'product' in goal.lower():
            listening_objectives.append(objectives_framework['product_development'])
        elif 'customer' in goal.lower():
            listening_objectives.append(objectives_framework['customer_insights'])

    return listening_objectives
```

#### Build Your Query Strategy

```python
# Example: Comprehensive Query Building

class QueryBuilder:
    """Build effective social listening queries"""

    def __init__(self, brand_name):
        self.brand_name = brand_name
        self.queries = {}

    def build_brand_query(self, variations=None, exclude_terms=None):
        """
        Build comprehensive brand monitoring query

        Args:
            variations: List of brand name variations
            exclude_terms: Terms to exclude (spam, unrelated)
        """
        # Brand name variations
        brand_terms = [self.brand_name]

        if variations:
            brand_terms.extend(variations)

        # Social handles
        social_handles = [
            f'@{self.brand_name}',
            f'#{self.brand_name}',
            f'#{self.brand_name.replace(" ", "")}'
        ]

        # Combine all terms
        all_terms = brand_terms + social_handles

        # Exclusions
        exclusions = exclude_terms or ['spam', 'bot', 'fake', 'scam']

        query = {
            'name': 'Brand Mentions',
            'included': all_terms,
            'excluded': exclusions,
            'boolean': self._build_boolean(all_terms, exclusions)
        }

        self.queries['brand'] = query
        return query

    def build_competitor_query(self, competitors):
        """
        Build competitor monitoring queries

        Args:
            competitors: List of competitor names
        """
        competitor_queries = {}

        for competitor in competitors:
            query = {
                'name': f'Competitor: {competitor}',
                'included': [competitor, f'@{competitor}', f'#{competitor}'],
                'excluded': ['spam', 'bot'],
                'boolean': self._build_boolean(
                    [competitor, f'@{competitor}'],
                    ['spam', 'bot']
                )
            }

            competitor_queries[competitor] = query

        self.queries['competitors'] = competitor_queries
        return competitor_queries

    def build_industry_query(self, keywords, trends=None):
        """
        Build industry and trend monitoring query

        Args:
            keywords: Industry keywords
            trends: Emerging trends to track
        """
        industry_terms = keywords

        if trends:
            industry_terms.extend(trends)

        query = {
            'name': 'Industry Conversations',
            'included': industry_terms,
            'excluded': ['spam', 'advertisement'],
            'boolean': self._build_boolean(industry_terms, ['spam'])
        }

        self.queries['industry'] = query
        return query

    def build_product_feedback_query(self, product_keywords):
        """
        Build product feedback and feature request query

        Args:
            product_keywords: Product-related terms
        """
        feedback_terms = [
            f'{self.brand_name} AND (feature OR request OR need)',
            f'{self.brand_name} AND (bug OR issue OR problem)',
            f'{self.brand_name} AND (love OR hate OR wish)',
            f'{self.brand_name} AND (review OR rating OR experience)'
        ]

        query = {
            'name': 'Product Feedback',
            'included': feedback_terms,
            'excluded': ['spam'],
            'boolean': ' OR '.join(f'({term})' for term in feedback_terms)
        }

        self.queries['feedback'] = query
        return query

    def build_crisis_query(self):
        """Build crisis detection query"""
        crisis_terms = [
            f'{self.brand_name} AND (outage OR down OR not working)',
            f'{self.brand_name} AND (breach OR hack OR security)',
            f'{self.brand_name} AND (lawsuit OR legal OR court)',
            f'{self.brand_name} AND (recall OR dangerous OR unsafe)',
            f'{self.brand_name} AND (boycott OR protest OR scandal)'
        ]

        query = {
            'name': 'Crisis Detection',
            'included': crisis_terms,
            'excluded': [],
            'boolean': ' OR '.join(f'({term})' for term in crisis_terms)
        }

        self.queries['crisis'] = query
        return query

    def _build_boolean(self, included, excluded):
        """Build boolean search string"""
        include_str = ' OR '.join(f'"{term}"' for term in included)
        exclude_str = ' AND NOT '.join(f'"{term}"' for term in excluded) if excluded else ''

        boolean = f'({include_str})'
        if exclude_str:
            boolean += f' AND NOT ({exclude_str})'

        return boolean

# Example usage
builder = QueryBuilder('YourBrand')

# Build queries
brand_query = builder.build_brand_query(
    variations=['Your Brand', 'YourBrand', 'Your Co'],
    exclude_terms=['spam', 'bot', 'fake']
)

competitor_queries = builder.build_competitor_query(
    competitors=['Competitor A', 'Competitor B', 'Competitor C']
)

industry_query = builder.build_industry_query(
    keywords=['industry keyword', 'category term', 'market segment'],
    trends=['emerging trend 1', 'emerging trend 2']
)

feedback_query = builder.build_product_feedback_query(
    product_keywords=['product', 'feature', 'service']
)

crisis_query = builder.build_crisis_query()

print("Queries built:")
for query_type, query in builder.queries.items():
    print(f"  {query_type}: {query['name']}")
```

### 2. Data Collection Strategy

```python
import pandas as pd
from datetime import datetime, timedelta

class DataCollectionStrategy:
    """Strategy for collecting social listening data"""

    def __init__(self):
        self.sources = {}
        self.collection_schedule = {}

    def define_sources(self):
        """Define which sources to monitor"""
        self.sources = {
            'social_media': {
                'platforms': ['twitter', 'facebook', 'instagram', 'linkedin', 'tiktok'],
                'priority': 'high',
                'frequency': 'real-time',
                'use_cases': ['brand mentions', 'customer service', 'engagement']
            },

            'news_media': {
                'platforms': ['news sites', 'press releases', 'trade publications'],
                'priority': 'high',
                'frequency': 'hourly',
                'use_cases': ['brand reputation', 'crisis detection', 'PR tracking']
            },

            'blogs_forums': {
                'platforms': ['blogs', 'reddit', 'forums', 'discussion boards'],
                'priority': 'medium',
                'frequency': 'daily',
                'use_cases': ['product feedback', 'community insights', 'technical discussions']
            },

            'review_sites': {
                'platforms': ['trustpilot', 'g2', 'capterra', 'yelp', 'google reviews'],
                'priority': 'high',
                'frequency': 'daily',
                'use_cases': ['product feedback', 'customer satisfaction', 'competitive analysis']
            },

            'video_platforms': {
                'platforms': ['youtube', 'vimeo', 'twitch'],
                'priority': 'medium',
                'frequency': 'daily',
                'use_cases': ['brand mentions', 'influencer content', 'tutorials']
            },

            'podcasts': {
                'platforms': ['podcast directories', 'audio platforms'],
                'priority': 'low',
                'frequency': 'weekly',
                'use_cases': ['thought leadership', 'brand mentions', 'industry trends']
            }
        }

        return self.sources

    def set_collection_frequency(self, objectives):
        """
        Set data collection frequency based on objectives

        Args:
            objectives: List of listening objectives
        """
        frequency_map = {
            'crisis_management': 'real-time',  # Every 5-15 minutes
            'customer_service': 'real-time',   # Every 5-15 minutes
            'brand_health': 'hourly',          # Every hour
            'competitive_intelligence': 'daily',  # Once per day
            'market_research': 'daily',        # Once per day
            'trend_analysis': 'weekly'         # Once per week
        }

        for objective in objectives:
            objective_type = objective.get('type', 'brand_health')
            frequency = frequency_map.get(objective_type, 'daily')

            self.collection_schedule[objective_type] = {
                'frequency': frequency,
                'last_collected': None,
                'next_collection': datetime.now()
            }

        return self.collection_schedule

# Example usage
strategy = DataCollectionStrategy()
sources = strategy.define_sources()

print("Data Sources:")
for source_type, config in sources.items():
    print(f"\n{source_type}:")
    print(f"  Platforms: {', '.join(config['platforms'])}")
    print(f"  Priority: {config['priority']}")
    print(f"  Frequency: {config['frequency']}")
```

### 3. Sentiment Analysis Framework

```python
class SentimentAnalyzer:
    """Framework for analyzing sentiment in social listening"""

    def __init__(self):
        self.sentiment_categories = {
            'positive': {
                'keywords': ['love', 'great', 'excellent', 'amazing', 'fantastic', 'best'],
                'score_range': (60, 100)
            },
            'neutral': {
                'keywords': ['okay', 'fine', 'acceptable', 'average'],
                'score_range': (40, 60)
            },
            'negative': {
                'keywords': ['hate', 'terrible', 'awful', 'worst', 'bad', 'disappointed'],
                'score_range': (0, 40)
            }
        }

    def analyze_sentiment_trends(self, mentions_df):
        """
        Analyze sentiment trends over time

        Args:
            mentions_df: DataFrame with columns ['date', 'sentiment', 'text']

        Returns: Sentiment trend analysis
        """
        # Group by date and sentiment
        daily_sentiment = mentions_df.groupby([
            mentions_df['date'].dt.date,
            'sentiment'
        ]).size().unstack(fill_value=0)

        # Calculate daily percentages
        daily_total = daily_sentiment.sum(axis=1)
        daily_pct = daily_sentiment.div(daily_total, axis=0) * 100

        # Calculate net sentiment score
        daily_pct['net_sentiment'] = (
            daily_pct.get('positive', 0) - daily_pct.get('negative', 0)
        )

        return daily_pct

    def identify_sentiment_drivers(self, mentions_df, sentiment='negative'):
        """
        Identify what's driving specific sentiment

        Args:
            mentions_df: DataFrame with mention data
            sentiment: 'positive', 'neutral', or 'negative'

        Returns: Common themes driving the sentiment
        """
        # Filter by sentiment
        sentiment_mentions = mentions_df[mentions_df['sentiment'] == sentiment]

        # Extract common themes (simplified - use NLP in production)
        word_frequency = {}

        for text in sentiment_mentions['text']:
            words = str(text).lower().split()
            for word in words:
                if len(word) > 4:  # Filter short words
                    word_frequency[word] = word_frequency.get(word, 0) + 1

        # Sort by frequency
        sorted_themes = sorted(
            word_frequency.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_themes[:20]

    def calculate_sentiment_health_score(self, mentions_df, weights=None):
        """
        Calculate overall sentiment health score (0-100)

        Args:
            mentions_df: DataFrame with sentiment data
            weights: Custom weights for each sentiment

        Returns: Health score and breakdown
        """
        if weights is None:
            weights = {
                'positive': 1.0,
                'neutral': 0.5,
                'negative': -1.0
            }

        sentiment_counts = mentions_df['sentiment'].value_counts()
        total = len(mentions_df)

        if total == 0:
            return {'score': 50, 'breakdown': {}, 'status': 'No Data'}

        # Calculate weighted score
        weighted_score = 0
        breakdown = {}

        for sentiment, weight in weights.items():
            count = sentiment_counts.get(sentiment, 0)
            percentage = (count / total) * 100

            breakdown[sentiment] = {
                'count': count,
                'percentage': percentage
            }

            weighted_score += (percentage * weight)

        # Normalize to 0-100 scale
        health_score = max(0, min(100, 50 + weighted_score))

        # Determine status
        if health_score >= 70:
            status = 'Healthy'
        elif health_score >= 50:
            status = 'Neutral'
        elif health_score >= 30:
            status = 'At Risk'
        else:
            status = 'Critical'

        return {
            'score': health_score,
            'breakdown': breakdown,
            'status': status
        }

# Example usage
analyzer = SentimentAnalyzer()

# Sample data
sample_data = pd.DataFrame({
    'date': pd.date_range('2025-01-01', periods=30),
    'sentiment': ['positive'] * 18 + ['neutral'] * 7 + ['negative'] * 5,
    'text': ['sample text'] * 30
})

health_score = analyzer.calculate_sentiment_health_score(sample_data)
print(f"Sentiment Health Score: {health_score['score']:.1f} ({health_score['status']})")
```

### 4. Crisis Detection and Management

```python
import numpy as np

class CrisisDetector:
    """Framework for detecting and managing crises"""

    def __init__(self, baseline_days=30):
        self.baseline_days = baseline_days
        self.alert_thresholds = {
            'volume_spike': 3.0,      # 3x standard deviation
            'negative_spike': 2.5,     # 2.5x standard deviation
            'negative_threshold': 60,  # 60% negative sentiment
            'high_reach': 100000       # High-reach negative mention
        }

    def detect_anomalies(self, historical_data, current_data):
        """
        Detect anomalies in mention volume and sentiment

        Args:
            historical_data: DataFrame with historical mentions
            current_data: DataFrame with recent mentions (last 24h)

        Returns: Anomaly detection results
        """
        # Calculate baseline statistics
        baseline_volume = len(historical_data) / self.baseline_days

        baseline_negative = (
            (historical_data['sentiment'] == 'negative').sum() /
            len(historical_data) * 100
        )

        # Calculate current statistics
        current_volume = len(current_data)

        current_negative = (
            (current_data['sentiment'] == 'negative').sum() /
            len(current_data) * 100 if len(current_data) > 0 else 0
        )

        # Detect anomalies
        volume_anomaly = current_volume > (baseline_volume * self.alert_thresholds['volume_spike'])

        negative_anomaly = current_negative > (
            baseline_negative + self.alert_thresholds['negative_spike'] * 10
        )

        critical_negative = current_negative > self.alert_thresholds['negative_threshold']

        # Detect high-reach negative mentions
        high_reach_negative = []
        if 'reach' in current_data.columns:
            high_reach_negative = current_data[
                (current_data['sentiment'] == 'negative') &
                (current_data['reach'] > self.alert_thresholds['high_reach'])
            ]

        return {
            'crisis_detected': volume_anomaly or negative_anomaly or critical_negative,
            'volume_anomaly': volume_anomaly,
            'negative_anomaly': negative_anomaly,
            'critical_negative': critical_negative,
            'baseline_volume': baseline_volume,
            'current_volume': current_volume,
            'baseline_negative_pct': baseline_negative,
            'current_negative_pct': current_negative,
            'high_reach_negative_count': len(high_reach_negative),
            'severity': self._calculate_severity(
                volume_anomaly, negative_anomaly, critical_negative
            )
        }

    def _calculate_severity(self, volume_anomaly, negative_anomaly, critical_negative):
        """Calculate crisis severity level"""
        severity_score = 0

        if volume_anomaly:
            severity_score += 3
        if negative_anomaly:
            severity_score += 3
        if critical_negative:
            severity_score += 4

        if severity_score >= 7:
            return 'CRITICAL'
        elif severity_score >= 5:
            return 'HIGH'
        elif severity_score >= 3:
            return 'MEDIUM'
        else:
            return 'LOW'

    def create_crisis_response_plan(self, crisis_type):
        """
        Generate crisis response template

        Args:
            crisis_type: Type of crisis detected

        Returns: Response plan template
        """
        response_plans = {
            'product_issue': {
                'immediate_actions': [
                    '1. Acknowledge the issue publicly within 1 hour',
                    '2. Activate technical team to investigate',
                    '3. Prepare holding statement for customers',
                    '4. Monitor social mentions every 15 minutes'
                ],
                'stakeholders': ['Product Team', 'Engineering', 'Customer Support', 'PR'],
                'communication_channels': ['Twitter', 'Status Page', 'Email'],
                'response_time_sla': '1 hour'
            },

            'security_breach': {
                'immediate_actions': [
                    '1. Activate security incident response team',
                    '2. Issue security advisory within 2 hours',
                    '3. Prepare FAQ for customers',
                    '4. Coordinate with legal team',
                    '5. Monitor for misinformation'
                ],
                'stakeholders': ['Security Team', 'Legal', 'PR', 'Executive Team'],
                'communication_channels': ['Website', 'Email', 'Social Media'],
                'response_time_sla': '30 minutes'
            },

            'negative_pr': {
                'immediate_actions': [
                    '1. Gather all facts and context',
                    '2. Prepare official statement',
                    '3. Identify key messages',
                    '4. Respond to high-reach mentions',
                    '5. Brief executive team'
                ],
                'stakeholders': ['PR Team', 'Legal', 'Executive Team'],
                'communication_channels': ['Press Release', 'Social Media', 'Media Outreach'],
                'response_time_sla': '2 hours'
            },

            'customer_service': {
                'immediate_actions': [
                    '1. Scale up support team capacity',
                    '2. Prepare response templates',
                    '3. Update help documentation',
                    '4. Monitor resolution metrics',
                    '5. Respond to all mentions within SLA'
                ],
                'stakeholders': ['Customer Support', 'Product Team'],
                'communication_channels': ['Social Media', 'Support Portal', 'Email'],
                'response_time_sla': '1 hour'
            }
        }

        return response_plans.get(crisis_type, response_plans['customer_service'])

# Example usage
detector = CrisisDetector(baseline_days=30)

# Sample historical data
historical = pd.DataFrame({
    'date': pd.date_range('2024-12-01', periods=30),
    'sentiment': ['positive'] * 18 + ['neutral'] * 8 + ['negative'] * 4,
    'reach': np.random.randint(100, 10000, 30)
})

# Sample current data (crisis scenario)
current = pd.DataFrame({
    'date': pd.date_range('2025-01-01', periods=100, freq='H'),
    'sentiment': ['negative'] * 70 + ['neutral'] * 20 + ['positive'] * 10,
    'reach': np.random.randint(1000, 200000, 100)
})

crisis_status = detector.detect_anomalies(historical, current)

print(f"Crisis Detection Results:")
print(f"  Crisis Detected: {crisis_status['crisis_detected']}")
print(f"  Severity: {crisis_status['severity']}")
print(f"  Current Volume: {crisis_status['current_volume']} (Baseline: {crisis_status['baseline_volume']:.1f})")
print(f"  Negative Sentiment: {crisis_status['current_negative_pct']:.1f}% (Baseline: {crisis_status['baseline_negative_pct']:.1f}%)")

if crisis_status['crisis_detected']:
    response_plan = detector.create_crisis_response_plan('product_issue')
    print(f"\nImmediate Actions:")
    for action in response_plan['immediate_actions']:
        print(f"  {action}")
```

### 5. Competitive Intelligence Framework

```python
class CompetitiveIntelligence:
    """Framework for gathering competitive intelligence"""

    def __init__(self, your_brand, competitors):
        self.your_brand = your_brand
        self.competitors = competitors

    def calculate_share_of_voice(self, mention_counts):
        """
        Calculate share of voice

        Args:
            mention_counts: Dict of {brand: mention_count}

        Returns: Share of voice percentages
        """
        total_mentions = sum(mention_counts.values())

        if total_mentions == 0:
            return {brand: 0 for brand in mention_counts.keys()}

        sov = {
            brand: (count / total_mentions * 100)
            for brand, count in mention_counts.items()
        }

        return sov

    def competitive_sentiment_analysis(self, brand_sentiment_data):
        """
        Compare sentiment across competitors

        Args:
            brand_sentiment_data: Dict of {brand: {'positive': x, 'neutral': y, 'negative': z}}

        Returns: Comparative sentiment analysis
        """
        comparison = []

        for brand, sentiment in brand_sentiment_data.items():
            total = sum(sentiment.values())

            if total == 0:
                continue

            net_sentiment = (
                (sentiment['positive'] - sentiment['negative']) / total * 100
            )

            comparison.append({
                'brand': brand,
                'positive_pct': sentiment['positive'] / total * 100,
                'neutral_pct': sentiment['neutral'] / total * 100,
                'negative_pct': sentiment['negative'] / total * 100,
                'net_sentiment': net_sentiment
            })

        df = pd.DataFrame(comparison)
        return df.sort_values('net_sentiment', ascending=False)

    def identify_competitive_gaps(self, feature_mentions):
        """
        Identify features competitors have that you don't

        Args:
            feature_mentions: Dict of {competitor: [features_mentioned]}

        Returns: Feature gap analysis
        """
        # Get all competitor features
        competitor_features = set()
        for features in feature_mentions.values():
            if features:
                competitor_features.update(features)

        # Your features
        your_features = set(feature_mentions.get(self.your_brand, []))

        # Gaps
        feature_gaps = competitor_features - your_features

        # Most mentioned gaps
        gap_frequency = {}
        for competitor, features in feature_mentions.items():
            if competitor == self.your_brand:
                continue

            for feature in features:
                if feature in feature_gaps:
                    gap_frequency[feature] = gap_frequency.get(feature, 0) + 1

        sorted_gaps = sorted(
            gap_frequency.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return {
            'feature_gaps': list(feature_gaps),
            'most_mentioned_gaps': sorted_gaps,
            'gap_count': len(feature_gaps)
        }

    def track_competitive_campaigns(self, campaign_mentions):
        """
        Track competitor marketing campaigns

        Args:
            campaign_mentions: List of campaign-related mentions

        Returns: Campaign analysis
        """
        campaigns = {}

        for mention in campaign_mentions:
            competitor = mention.get('competitor')
            campaign_id = mention.get('campaign_id', 'unknown')

            if campaign_id not in campaigns:
                campaigns[campaign_id] = {
                    'competitor': competitor,
                    'mentions': 0,
                    'reach': 0,
                    'engagement': 0,
                    'sentiment': {'positive': 0, 'neutral': 0, 'negative': 0}
                }

            campaigns[campaign_id]['mentions'] += 1
            campaigns[campaign_id]['reach'] += mention.get('reach', 0)
            campaigns[campaign_id]['engagement'] += mention.get('engagement', 0)

            sentiment = mention.get('sentiment', 'neutral')
            campaigns[campaign_id]['sentiment'][sentiment] += 1

        return campaigns

# Example usage
competitors = ['Competitor A', 'Competitor B', 'Competitor C']
intelligence = CompetitiveIntelligence('YourBrand', competitors)

# Share of Voice
mention_counts = {
    'YourBrand': 1200,
    'Competitor A': 1500,
    'Competitor B': 900,
    'Competitor C': 600
}

sov = intelligence.calculate_share_of_voice(mention_counts)
print("Share of Voice:")
for brand, percentage in sorted(sov.items(), key=lambda x: x[1], reverse=True):
    print(f"  {brand}: {percentage:.1f}%")

# Sentiment Comparison
sentiment_data = {
    'YourBrand': {'positive': 700, 'neutral': 350, 'negative': 150},
    'Competitor A': {'positive': 800, 'neutral': 500, 'negative': 200},
    'Competitor B': {'positive': 400, 'neutral': 350, 'negative': 150},
    'Competitor C': {'positive': 250, 'neutral': 250, 'negative': 100}
}

sentiment_comparison = intelligence.competitive_sentiment_analysis(sentiment_data)
print("\nSentiment Comparison:")
print(sentiment_comparison)
```

### 6. Actionable Insights Generation

```python
class InsightsGenerator:
    """Generate actionable insights from social listening data"""

    def __init__(self):
        self.insight_types = [
            'product_improvement',
            'content_opportunity',
            'customer_service',
            'competitive_positioning',
            'crisis_prevention'
        ]

    def generate_insights(self, listening_data):
        """
        Generate actionable insights from listening data

        Args:
            listening_data: Dict containing various listening metrics

        Returns: List of actionable insights
        """
        insights = []

        # Product Insights
        if 'feature_requests' in listening_data:
            top_requests = listening_data['feature_requests'][:5]
            if top_requests:
                insights.append({
                    'type': 'product_improvement',
                    'priority': 'high',
                    'insight': f"Top feature request: {top_requests[0]['feature']}",
                    'data': f"{top_requests[0]['count']} mentions",
                    'action': f"Evaluate adding '{top_requests[0]['feature']}' to product roadmap",
                    'stakeholders': ['Product Team', 'Engineering'],
                    'timeline': '30 days'
                })

        # Content Opportunities
        if 'trending_topics' in listening_data:
            trending = listening_data['trending_topics'][:3]
            if trending:
                insights.append({
                    'type': 'content_opportunity',
                    'priority': 'medium',
                    'insight': f"Trending topic: {trending[0]['topic']}",
                    'data': f"{trending[0]['volume']} mentions in 24h",
                    'action': f"Create content addressing '{trending[0]['topic']}'",
                    'stakeholders': ['Content Team', 'Marketing'],
                    'timeline': '7 days'
                })

        # Customer Service
        if 'common_issues' in listening_data:
            issues = listening_data['common_issues'][:3]
            if issues:
                insights.append({
                    'type': 'customer_service',
                    'priority': 'high',
                    'insight': f"Recurring issue: {issues[0]['issue']}",
                    'data': f"{issues[0]['count']} mentions",
                    'action': f"Create help documentation for '{issues[0]['issue']}'",
                    'stakeholders': ['Support Team', 'Product Team'],
                    'timeline': '14 days'
                })

        # Competitive Positioning
        if 'competitive_gaps' in listening_data:
            gaps = listening_data['competitive_gaps']
            if gaps:
                insights.append({
                    'type': 'competitive_positioning',
                    'priority': 'medium',
                    'insight': f"Feature gap identified: {gaps[0]['feature']}",
                    'data': f"{gaps[0]['competitor_count']} competitors have this",
                    'action': f"Evaluate competitive positioning on '{gaps[0]['feature']}'",
                    'stakeholders': ['Product Team', 'Marketing'],
                    'timeline': '60 days'
                })

        # Crisis Prevention
        if 'negative_trends' in listening_data:
            trends = listening_data['negative_trends']
            if trends and trends[0]['growth_rate'] > 50:
                insights.append({
                    'type': 'crisis_prevention',
                    'priority': 'critical',
                    'insight': f"Negative sentiment increasing: {trends[0]['theme']}",
                    'data': f"{trends[0]['growth_rate']}% increase",
                    'action': f"Investigate and address '{trends[0]['theme']}' immediately",
                    'stakeholders': ['PR Team', 'Executive Team', 'Product Team'],
                    'timeline': '24 hours'
                })

        return insights

    def prioritize_insights(self, insights):
        """
        Prioritize insights by urgency and impact

        Args:
            insights: List of insights

        Returns: Prioritized insights
        """
        priority_scores = {
            'critical': 4,
            'high': 3,
            'medium': 2,
            'low': 1
        }

        # Sort by priority
        sorted_insights = sorted(
            insights,
            key=lambda x: priority_scores.get(x['priority'], 0),
            reverse=True
        )

        return sorted_insights

    def create_action_plan(self, insights):
        """
        Create action plan from insights

        Args:
            insights: List of prioritized insights

        Returns: Structured action plan
        """
        action_plan = {
            'immediate': [],  # 24-48 hours
            'short_term': [],  # 1-4 weeks
            'long_term': []    # 1-3 months
        }

        for insight in insights:
            timeline = insight.get('timeline', '30 days')

            action_item = {
                'insight': insight['insight'],
                'action': insight['action'],
                'stakeholders': insight['stakeholders'],
                'priority': insight['priority'],
                'data': insight['data']
            }

            if 'hour' in timeline or 'day' in timeline:
                days = int(''.join(filter(str.isdigit, timeline))) if any(c.isdigit() for c in timeline) else 1
                if days <= 2:
                    action_plan['immediate'].append(action_item)
                else:
                    action_plan['short_term'].append(action_item)
            elif 'week' in timeline:
                action_plan['short_term'].append(action_item)
            else:
                action_plan['long_term'].append(action_item)

        return action_plan

# Example usage
generator = InsightsGenerator()

sample_listening_data = {
    'feature_requests': [
        {'feature': 'Dark mode', 'count': 145},
        {'feature': 'Mobile app', 'count': 98},
        {'feature': 'API access', 'count': 76}
    ],
    'trending_topics': [
        {'topic': 'AI integration', 'volume': 234},
        {'topic': 'Security features', 'volume': 187}
    ],
    'common_issues': [
        {'issue': 'Slow loading times', 'count': 67},
        {'issue': 'Login problems', 'count': 45}
    ],
    'negative_trends': [
        {'theme': 'Customer support response time', 'growth_rate': 65}
    ]
}

insights = generator.generate_insights(sample_listening_data)
prioritized = generator.prioritize_insights(insights)
action_plan = generator.create_action_plan(prioritized)

print("Prioritized Insights:")
for insight in prioritized:
    print(f"\n[{insight['priority'].upper()}] {insight['insight']}")
    print(f"  Action: {insight['action']}")
    print(f"  Stakeholders: {', '.join(insight['stakeholders'])}")
```

## Best Practices

### 1. Query Building
- **Be Comprehensive**: Include brand variations, misspellings, acronyms
- **Use Boolean Logic**: Combine keywords effectively with AND, OR, NOT
- **Exclude Noise**: Filter spam, bots, irrelevant content
- **Test and Refine**: Regularly review and optimize queries
- **Monitor Variations**: Track @mentions, #hashtags, URL mentions

### 2. Data Collection
- **Multi-Source**: Monitor social media, news, blogs, forums, reviews
- **Real-Time Critical**: Use real-time monitoring for crisis and customer service
- **Historical Context**: Maintain 6-12 months of historical data
- **Data Quality**: Validate and clean data regularly
- **Deduplication**: Remove duplicate mentions

### 3. Analysis
- **Context Matters**: Don't rely solely on automated sentiment
- **Segment Data**: Analyze by source, geography, audience segment
- **Track Trends**: Monitor changes over time, not just snapshots
- **Competitive Context**: Always benchmark against competitors
- **Multiple Metrics**: Use volume, sentiment, reach, engagement together

### 4. Response
- **Speed**: Respond to customer inquiries within 1 hour
- **Personalization**: Tailor responses to individual situations
- **Transparency**: Be honest about issues and timelines
- **Escalation Path**: Have clear escalation for crisis situations
- **Follow Up**: Close the loop on all interactions

### 5. Reporting
- **Actionable**: Focus on insights that drive decisions
- **Visual**: Use charts and dashboards for clarity
- **Regular Cadence**: Daily monitoring, weekly reports, monthly deep dives
- **Stakeholder-Specific**: Customize reports for different audiences
- **ROI Tracking**: Measure impact of insights on business metrics

## Key Metrics

### Volume Metrics
- Total mention volume
- Volume trend (growing/declining)
- Share of voice vs. competitors
- Source distribution

### Sentiment Metrics
- Net sentiment score
- Sentiment distribution (positive/neutral/negative)
- Sentiment trend over time
- Sentiment by source/topic

### Engagement Metrics
- Reach (potential audience)
- Engagement rate
- Influencer participation
- Viral coefficient

### Business Impact Metrics
- Response time
- Issue resolution rate
- Customer satisfaction impact
- Product roadmap influence
- Crisis prevention/mitigation

## Tools and Technologies

### Social Listening Platforms
- **Enterprise**: Brandwatch, Sprout Social, Talkwalker
- **Mid-Market**: Mention, Hootsuite, Sprinklr
- **Social-Specific**: Buffer (scheduling focus), Later (visual focus)

### Complementary Tools
- **Sentiment Analysis**: IBM Watson, Google NLP, AWS Comprehend
- **Data Visualization**: Tableau, Looker, Google Data Studio
- **Alert Management**: PagerDuty, Slack, Email notifications

## Implementation Checklist

- [ ] Define business objectives
- [ ] Build comprehensive query set
- [ ] Select monitoring sources
- [ ] Set up data collection
- [ ] Configure alert thresholds
- [ ] Create response workflows
- [ ] Assign team roles and responsibilities
- [ ] Set up reporting dashboards
- [ ] Train team on tools and processes
- [ ] Establish escalation procedures
- [ ] Schedule regular reviews
- [ ] Measure and optimize

## References

- [Social Listening Best Practices](https://sproutsocial.com/insights/social-listening/)
- [Building Boolean Queries](https://boolean-builder.com/)
- [Sentiment Analysis Guide](https://monkeylearn.com/sentiment-analysis/)
- [Crisis Management Framework](https://www.crisiscommunications.com/)
- [Competitive Intelligence](https://www.competitiveintelligence.com/)
- [ROI of Social Listening](https://www.forrester.com/social-listening/)

---
name: nltk-sentiment
description: "Sentiment analysis for marketing. Customer review analysis, social media sentiment, brand monitoring, NPS analysis, voice of customer insights."
---

# NLTK for Marketing Sentiment Analysis

## Overview

NLTK provides natural language processing tools for analyzing customer feedback, reviews, social media, and other text data. This skill covers sentiment analysis, topic extraction, and customer voice insights.

## When to Use This Skill

- Analyzing customer reviews and feedback
- Social media sentiment monitoring
- NPS verbatim analysis
- Brand mention sentiment
- Support ticket categorization
- Voice of customer insights

## Core Capabilities

### 1. Basic Sentiment Analysis with VADER

```python
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

# Download VADER lexicon
nltk.download('vader_lexicon')

# Initialize analyzer
sia = SentimentIntensityAnalyzer()

# Sample reviews
reviews = [
    "This product is amazing! Best purchase I've ever made.",
    "Terrible customer service. Will never buy again.",
    "It's okay, nothing special but works as expected.",
    "Love the quality! Shipping was fast too. Highly recommend!",
    "The product broke after one week. Very disappointed."
]

# Analyze sentiment
results = []
for review in reviews:
    scores = sia.polarity_scores(review)
    results.append({
        'review': review[:50] + '...' if len(review) > 50 else review,
        'positive': scores['pos'],
        'negative': scores['neg'],
        'neutral': scores['neu'],
        'compound': scores['compound'],
        'sentiment': 'Positive' if scores['compound'] > 0.05
                     else 'Negative' if scores['compound'] < -0.05
                     else 'Neutral'
    })

df = pd.DataFrame(results)
print(df)
```

### 2. Batch Review Analysis

```python
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Load reviews
reviews_df = pd.read_csv('customer_reviews.csv')
sia = SentimentIntensityAnalyzer()

# Analyze all reviews
def analyze_sentiment(text):
    if pd.isna(text):
        return pd.Series({'compound': 0, 'sentiment': 'Unknown'})

    scores = sia.polarity_scores(str(text))
    sentiment = 'Positive' if scores['compound'] > 0.05 \
                else 'Negative' if scores['compound'] < -0.05 \
                else 'Neutral'
    return pd.Series({
        'compound': scores['compound'],
        'sentiment': sentiment
    })

# Apply to dataframe
reviews_df[['compound', 'sentiment']] = reviews_df['review_text'].apply(analyze_sentiment)

# Summary statistics
print("Sentiment Distribution:")
print(reviews_df['sentiment'].value_counts(normalize=True))

# Average sentiment by product
product_sentiment = reviews_df.groupby('product_id').agg({
    'compound': 'mean',
    'review_text': 'count'
}).rename(columns={'review_text': 'review_count'})

print("\nProduct Sentiment Scores:")
print(product_sentiment.sort_values('compound', ascending=False).head(10))
```

### 3. NPS Verbatim Analysis

```python
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import nltk

nltk.download('punkt')
nltk.download('stopwords')

# Load NPS responses
nps_df = pd.read_csv('nps_responses.csv')
sia = SentimentIntensityAnalyzer()

# Categorize by NPS score
nps_df['nps_category'] = pd.cut(
    nps_df['nps_score'],
    bins=[-1, 6, 8, 10],
    labels=['Detractor', 'Passive', 'Promoter']
)

# Analyze sentiment in verbatims
nps_df['verbatim_sentiment'] = nps_df['verbatim'].apply(
    lambda x: sia.polarity_scores(str(x))['compound'] if pd.notna(x) else 0
)

# Extract common themes by category
stop_words = set(stopwords.words('english'))

def extract_keywords(texts, n=10):
    all_words = []
    for text in texts.dropna():
        tokens = word_tokenize(str(text).lower())
        words = [w for w in tokens if w.isalpha() and w not in stop_words and len(w) > 2]
        all_words.extend(words)
    return Counter(all_words).most_common(n)

for category in ['Detractor', 'Passive', 'Promoter']:
    subset = nps_df[nps_df['nps_category'] == category]['verbatim']
    keywords = extract_keywords(subset)
    print(f"\n{category} Top Keywords:")
    for word, count in keywords:
        print(f"  {word}: {count}")
```

### 4. Social Media Sentiment Tracking

```python
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime

# Load social mentions
mentions_df = pd.read_csv('social_mentions.csv', parse_dates=['timestamp'])
sia = SentimentIntensityAnalyzer()

# Analyze sentiment
mentions_df['sentiment_score'] = mentions_df['text'].apply(
    lambda x: sia.polarity_scores(str(x))['compound']
)

mentions_df['sentiment'] = mentions_df['sentiment_score'].apply(
    lambda x: 'Positive' if x > 0.05 else 'Negative' if x < -0.05 else 'Neutral'
)

# Daily sentiment trend
daily_sentiment = mentions_df.set_index('timestamp').resample('D').agg({
    'sentiment_score': 'mean',
    'text': 'count'
}).rename(columns={'text': 'mention_count'})

print("Daily Sentiment Trend:")
print(daily_sentiment.tail(14))

# Sentiment by platform
platform_sentiment = mentions_df.groupby('platform').agg({
    'sentiment_score': 'mean',
    'text': 'count'
})
print("\nSentiment by Platform:")
print(platform_sentiment)

# Alert on negative sentiment spikes
negative_mentions = mentions_df[mentions_df['sentiment_score'] < -0.5]
print(f"\nHighly Negative Mentions: {len(negative_mentions)}")
```

### 5. Aspect-Based Sentiment Analysis

```python
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

nltk.download('punkt')
sia = SentimentIntensityAnalyzer()

# Define aspects to analyze
aspects = {
    'price': ['price', 'cost', 'expensive', 'cheap', 'value', 'money', 'affordable'],
    'quality': ['quality', 'durable', 'material', 'sturdy', 'flimsy', 'build'],
    'shipping': ['shipping', 'delivery', 'arrived', 'package', 'fast', 'slow'],
    'service': ['service', 'support', 'help', 'customer', 'response', 'team'],
    'product': ['product', 'item', 'works', 'function', 'feature', 'use']
}

def extract_aspect_sentiment(text, aspects):
    """Extract sentiment for each aspect mentioned in text"""
    text_lower = text.lower()
    sentences = nltk.sent_tokenize(text)
    aspect_sentiments = {}

    for aspect, keywords in aspects.items():
        relevant_sentences = []
        for sentence in sentences:
            if any(kw in sentence.lower() for kw in keywords):
                relevant_sentences.append(sentence)

        if relevant_sentences:
            combined = ' '.join(relevant_sentences)
            score = sia.polarity_scores(combined)['compound']
            aspect_sentiments[aspect] = score

    return aspect_sentiments

# Analyze reviews
reviews = [
    "Great product quality but the price is too high. Shipping was super fast!",
    "Terrible customer service. Had to wait 2 weeks for a response. Product works fine though.",
    "Best value for money! Quality is amazing and delivery was quick."
]

for review in reviews:
    print(f"\nReview: {review[:60]}...")
    aspects_found = extract_aspect_sentiment(review, aspects)
    for aspect, score in aspects_found.items():
        sentiment = 'Positive' if score > 0.05 else 'Negative' if score < -0.05 else 'Neutral'
        print(f"  {aspect}: {score:.2f} ({sentiment})")
```

### 6. Competitive Brand Sentiment

```python
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Load mentions with brand tags
mentions_df = pd.read_csv('brand_mentions.csv', parse_dates=['date'])
sia = SentimentIntensityAnalyzer()

# Analyze sentiment
mentions_df['sentiment_score'] = mentions_df['text'].apply(
    lambda x: sia.polarity_scores(str(x))['compound']
)

# Brand comparison
brand_comparison = mentions_df.groupby('brand').agg({
    'sentiment_score': ['mean', 'std'],
    'text': 'count'
})
brand_comparison.columns = ['avg_sentiment', 'sentiment_std', 'mention_count']
brand_comparison = brand_comparison.sort_values('avg_sentiment', ascending=False)

print("Brand Sentiment Comparison:")
print(brand_comparison)

# Share of voice with sentiment
total_mentions = len(mentions_df)
brand_comparison['share_of_voice'] = brand_comparison['mention_count'] / total_mentions * 100

# Net sentiment score (% positive - % negative)
for brand in mentions_df['brand'].unique():
    brand_data = mentions_df[mentions_df['brand'] == brand]
    positive = (brand_data['sentiment_score'] > 0.05).sum()
    negative = (brand_data['sentiment_score'] < -0.05).sum()
    total = len(brand_data)
    net_sentiment = (positive - negative) / total * 100
    print(f"{brand}: Net Sentiment = {net_sentiment:.1f}%")
```

## Installation

```bash
uv pip install nltk pandas
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')"
```

## Quick Start

```python
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

text = "I love this product! It's exactly what I needed."
scores = sia.polarity_scores(text)
print(scores)
# {'neg': 0.0, 'neu': 0.408, 'pos': 0.592, 'compound': 0.8398}
```

## Best Practices

1. **Preprocess text** - Clean HTML, normalize text before analysis
2. **Handle negations** - VADER handles negations, but verify for domain-specific cases
3. **Calibrate thresholds** - Adjust sentiment thresholds based on your domain
4. **Combine with volume** - Sentiment alone isn't enough; track volume too
5. **Manual validation** - Sample and validate automated sentiment scores

## References

- [NLTK Documentation](https://www.nltk.org/)
- [VADER Paper](https://ojs.aaai.org/index.php/ICWSM/article/view/14550)

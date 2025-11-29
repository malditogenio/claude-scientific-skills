---
name: spacy-nlp
description: "NLP for marketing content analysis. Sentiment analysis, entity extraction, keyword extraction, content categorization, customer feedback analysis, brand mention tracking."
---

# spaCy for Marketing NLP

## Overview

spaCy is an industrial-strength NLP library perfect for processing marketing content at scale. This skill covers using spaCy for sentiment analysis, entity extraction from customer feedback, keyword extraction, content categorization, brand monitoring, and automated content tagging.

## When to Use This Skill

- Analyzing customer feedback and reviews at scale
- Extracting insights from support tickets and emails
- Categorizing marketing content automatically
- Identifying brand mentions and competitor references
- Extracting product features from customer feedback
- Processing survey responses and open-ended questions
- Analyzing social media mentions and comments

## Core Capabilities

### 1. Customer Feedback Analysis

```python
import spacy
from collections import Counter
import pandas as pd

# Load spaCy model
nlp = spacy.load("en_core_web_lg")

def analyze_feedback(feedback_list):
    """
    Extract insights from customer feedback
    """
    results = []

    for text in feedback_list:
        doc = nlp(text)

        # Extract entities (products, features, brands)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        # Extract key noun phrases
        noun_chunks = [chunk.text for chunk in doc.noun_chunks]

        # Get sentiment-bearing adjectives
        adjectives = [token.text for token in doc if token.pos_ == 'ADJ']

        results.append({
            'text': text,
            'entities': entities,
            'noun_phrases': noun_chunks,
            'adjectives': adjectives,
            'tokens': len(doc),
            'sentences': len(list(doc.sents))
        })

    return pd.DataFrame(results)

# Example usage
reviews = [
    "The new iPhone has an amazing camera but the battery life is disappointing",
    "Switched to Android after 10 years. Samsung Galaxy is much faster",
    "Apple's customer service was incredibly helpful with my MacBook issue",
]

feedback_df = analyze_feedback(reviews)
print(feedback_df)
```

### 2. Entity Extraction for Brand Monitoring

```python
import spacy
from collections import Counter

nlp = spacy.load("en_core_web_lg")

def extract_brands_and_products(texts):
    """
    Extract brand mentions, products, and competitors from text
    """
    all_orgs = []
    all_products = []
    all_money = []

    for text in texts:
        doc = nlp(text)

        for ent in doc.ents:
            if ent.label_ == 'ORG':
                all_orgs.append(ent.text)
            elif ent.label_ == 'PRODUCT':
                all_products.append(ent.text)
            elif ent.label_ == 'MONEY':
                all_money.append(ent.text)

    return {
        'brand_mentions': Counter(all_orgs).most_common(20),
        'product_mentions': Counter(all_products).most_common(20),
        'pricing_mentions': Counter(all_money).most_common(10)
    }

# Analyze social media mentions
social_posts = [
    "Just bought the new Tesla Model 3 for $45,000 - best purchase ever!",
    "Nike shoes are overpriced. Adidas has better quality for the price",
    "Amazon Prime is worth every penny of $139/year",
]

mentions = extract_brands_and_products(social_posts)
print("\nTop Brand Mentions:")
for brand, count in mentions['brand_mentions']:
    print(f"  {brand}: {count}")
```

### 3. Sentiment Analysis with Context

```python
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

# Load model and add sentiment component
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe('spacytextblob')

def analyze_sentiment_detailed(texts):
    """
    Perform detailed sentiment analysis on marketing content
    """
    results = []

    for text in texts:
        doc = nlp(text)

        # Overall sentiment
        overall_sentiment = doc._.polarity
        subjectivity = doc._.subjectivity

        # Sentence-level sentiment
        sentences_sentiment = []
        for sent in doc.sents:
            sentences_sentiment.append({
                'sentence': sent.text,
                'polarity': sent._.polarity,
                'subjectivity': sent._.subjectivity
            })

        # Classify overall sentiment
        if overall_sentiment > 0.2:
            label = 'Positive'
        elif overall_sentiment < -0.2:
            label = 'Negative'
        else:
            label = 'Neutral'

        results.append({
            'text': text,
            'polarity': overall_sentiment,
            'subjectivity': subjectivity,
            'sentiment_label': label,
            'sentences': sentences_sentiment
        })

    return results

# Analyze customer reviews
reviews = [
    "This product exceeded my expectations! Fast shipping and great quality.",
    "Terrible customer service. Waited 2 hours on hold and got no help.",
    "It's okay. Does what it says but nothing special.",
]

sentiment_results = analyze_sentiment_detailed(reviews)
for result in sentiment_results:
    print(f"\nText: {result['text']}")
    print(f"Sentiment: {result['sentiment_label']} (score: {result['polarity']:.2f})")
```

### 4. Keyword and Feature Extraction

```python
import spacy
from collections import Counter
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_lg")

def extract_product_features(reviews):
    """
    Extract product features and attributes mentioned in reviews
    """
    # Common feature patterns
    matcher = Matcher(nlp.vocab)

    # Pattern: ADJ + NOUN (e.g., "fast shipping", "great quality")
    pattern1 = [{"POS": "ADJ"}, {"POS": "NOUN"}]
    # Pattern: ADV + ADJ (e.g., "very good", "extremely fast")
    pattern2 = [{"POS": "ADV"}, {"POS": "ADJ"}]
    # Pattern: NOUN + NOUN (e.g., "battery life", "customer service")
    pattern3 = [{"POS": "NOUN"}, {"POS": "NOUN"}]

    matcher.add("FEATURE", [pattern1, pattern2, pattern3])

    all_features = []
    feature_sentiments = {}

    for review in reviews:
        doc = nlp(review)
        matches = matcher(doc)

        for match_id, start, end in matches:
            feature = doc[start:end].text.lower()
            all_features.append(feature)

            # Get surrounding context for sentiment
            sent = doc[start:end].sent
            feature_sentiments[feature] = sent._.polarity if hasattr(sent._, 'polarity') else 0

    # Count and rank features
    feature_counts = Counter(all_features)

    return {
        'top_features': feature_counts.most_common(20),
        'feature_sentiment': feature_sentiments
    }

# Extract features from reviews
customer_reviews = [
    "Fast shipping and excellent customer service made this a great purchase",
    "Battery life is amazing but the screen quality could be better",
    "Great value for money. The build quality exceeded expectations",
]

features = extract_product_features(customer_reviews)
print("\nMost Mentioned Features:")
for feature, count in features['top_features']:
    sentiment = features['feature_sentiment'].get(feature, 0)
    print(f"  {feature}: {count} mentions (sentiment: {sentiment:.2f})")
```

### 5. Content Categorization

```python
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd

nlp = spacy.load("en_core_web_lg")

def preprocess_for_classification(texts):
    """
    Preprocess text for content categorization
    """
    processed = []

    for text in texts:
        doc = nlp(text)

        # Remove stopwords and lemmatize
        tokens = [token.lemma_.lower() for token in doc
                 if not token.is_stop and not token.is_punct and token.is_alpha]

        processed.append(' '.join(tokens))

    return processed

# Train content classifier
training_data = pd.DataFrame({
    'text': [
        "New product launch announcement with special discount",
        "How to use our software: step by step tutorial",
        "Customer success story with 10x ROI",
        "Industry trends and market analysis for 2024",
        "Webinar registration for next week's event",
    ],
    'category': ['Product', 'Educational', 'Case Study', 'Thought Leadership', 'Event']
})

# Preprocess and train
X_train = preprocess_for_classification(training_data['text'])
y_train = training_data['category']

vectorizer = TfidfVectorizer(max_features=100)
X_train_vec = vectorizer.fit_transform(X_train)

classifier = MultinomialNB()
classifier.fit(X_train_vec, y_train)

# Categorize new content
new_content = [
    "Join our upcoming conference on digital marketing",
    "See how Company X increased revenue by 50%",
]

X_new = preprocess_for_classification(new_content)
X_new_vec = vectorizer.transform(X_new)
predictions = classifier.predict(X_new_vec)

print("\nContent Categorization:")
for text, category in zip(new_content, predictions):
    print(f"  '{text}' -> {category}")
```

### 6. Multi-Language Support for Global Marketing

```python
import spacy

def analyze_multilingual_content(texts, languages):
    """
    Analyze marketing content in multiple languages
    """
    # Load models for different languages
    models = {
        'en': spacy.load('en_core_web_lg'),
        'es': spacy.load('es_core_news_lg'),
        'de': spacy.load('de_core_news_lg'),
        'fr': spacy.load('fr_core_news_lg'),
    }

    results = []

    for text, lang in zip(texts, languages):
        if lang in models:
            nlp = models[lang]
            doc = nlp(text)

            entities = [(ent.text, ent.label_) for ent in doc.ents]
            keywords = [chunk.text for chunk in doc.noun_chunks]

            results.append({
                'language': lang,
                'text': text,
                'entities': entities,
                'keywords': keywords[:5]
            })

    return results

# Analyze global campaigns
global_content = [
    ("Our new product launches next week with amazing features", 'en'),
    ("Nuestro nuevo producto se lanza la próxima semana", 'es'),
    ("Unser neues Produkt startet nächste Woche", 'de'),
]

multilingual_results = analyze_multilingual_content(
    [text for text, _ in global_content],
    [lang for _, lang in global_content]
)

for result in multilingual_results:
    print(f"\n{result['language'].upper()}: {result['text']}")
    print(f"  Keywords: {', '.join(result['keywords'][:3])}")
```

## Installation

```bash
# Install spaCy
uv pip install spacy spacytextblob

# Download English model (large)
python -m spacy download en_core_web_lg

# Optional: Download other language models
python -m spacy download es_core_news_lg  # Spanish
python -m spacy download de_core_news_lg  # German
python -m spacy download fr_core_news_lg  # French
```

## Quick Start

```python
import spacy

# Load model
nlp = spacy.load("en_core_web_lg")

# Analyze text
text = "Apple's new iPhone 15 Pro is getting great reviews"
doc = nlp(text)

# Extract entities
for ent in doc.ents:
    print(f"{ent.text}: {ent.label_}")

# Output:
# Apple: ORG
# iPhone 15 Pro: PRODUCT
```

## Best Practices

1. **Choose the right model** - Use `lg` (large) models for better accuracy in production
2. **Batch processing** - Use `nlp.pipe()` for processing large volumes efficiently
3. **Custom entities** - Train custom NER models for industry-specific terms
4. **Disable unused components** - Speed up processing by disabling unneeded pipeline components
5. **Combine with sentiment** - Use spacytextblob or other sentiment libraries
6. **Cache results** - Store processed documents to avoid reprocessing

## References

- [spaCy Documentation](https://spacy.io/)
- [spaCy 101](https://spacy.io/usage/spacy-101)
- [Linguistic Features](https://spacy.io/usage/linguistic-features)
- [spacytextblob](https://github.com/SamEdwardes/spacytextblob)

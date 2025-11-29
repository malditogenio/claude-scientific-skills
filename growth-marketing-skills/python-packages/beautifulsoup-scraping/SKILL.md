---
name: beautifulsoup-scraping
description: "Web scraping for competitive intelligence. Competitor pricing, product monitoring, review analysis, SEO data extraction, market research, trend monitoring."
---

# BeautifulSoup for Marketing Web Scraping

## Overview

BeautifulSoup is a powerful HTML parsing library perfect for extracting marketing intelligence from websites. This skill covers scraping competitor pricing, monitoring product listings, analyzing reviews, extracting SEO metadata, tracking market trends, and gathering competitive intelligence.

## When to Use This Skill

- Monitoring competitor pricing and promotions
- Tracking competitor product launches and updates
- Scraping customer reviews from e-commerce sites
- Extracting SEO metadata and keywords from competitor sites
- Gathering market research data from public websites
- Monitoring brand mentions and sentiment online
- Tracking social media metrics and engagement

## Core Capabilities

### 1. Competitor Pricing Monitor

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

class CompetitorPriceMonitor:
    """
    Monitor competitor pricing across e-commerce sites
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_product_price(self, url, price_selector, name_selector):
        """
        Scrape product price and name from competitor site
        """
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract product name
        name_elem = soup.select_one(name_selector)
        product_name = name_elem.text.strip() if name_elem else "Unknown"

        # Extract price
        price_elem = soup.select_one(price_selector)
        if price_elem:
            price_text = price_elem.text.strip()
            # Clean price: "$99.99" -> 99.99
            price = float(price_text.replace('$', '').replace(',', ''))
        else:
            price = None

        return {
            'product_name': product_name,
            'price': price,
            'url': url,
            'timestamp': datetime.now(),
            'currency': 'USD'
        }

    def monitor_competitors(self, competitor_urls):
        """
        Monitor multiple competitor products
        """
        results = []

        for comp_data in competitor_urls:
            try:
                price_data = self.scrape_product_price(
                    url=comp_data['url'],
                    price_selector=comp_data['price_selector'],
                    name_selector=comp_data['name_selector']
                )
                price_data['competitor'] = comp_data['competitor']
                results.append(price_data)
            except Exception as e:
                print(f"Error scraping {comp_data['url']}: {e}")

        return pd.DataFrame(results)

# Usage
monitor = CompetitorPriceMonitor()

competitors = [
    {
        'competitor': 'Amazon',
        'url': 'https://www.amazon.com/dp/B08N5WRWNW',
        'price_selector': '.a-price-whole',
        'name_selector': '#productTitle'
    },
    {
        'competitor': 'BestBuy',
        'url': 'https://www.bestbuy.com/site/product/12345',
        'price_selector': '.priceView-customer-price span',
        'name_selector': '.sku-title h1'
    }
]

# Get current prices
price_df = monitor.monitor_competitors(competitors)
print(price_df)

# Calculate price differences
avg_price = price_df['price'].mean()
price_df['vs_avg'] = ((price_df['price'] - avg_price) / avg_price * 100).round(2)
print("\nPrice Analysis:")
print(price_df[['competitor', 'price', 'vs_avg']])
```

### 2. Product Review Scraper

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class ReviewScraper:
    """
    Scrape product reviews for sentiment and feature analysis
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_amazon_reviews(self, product_url, max_pages=5):
        """
        Scrape Amazon product reviews
        """
        reviews = []

        for page in range(1, max_pages + 1):
            # Construct review page URL
            asin = product_url.split('/dp/')[1].split('/')[0]
            review_url = f"https://www.amazon.com/product-reviews/{asin}?pageNumber={page}"

            response = requests.get(review_url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all review containers
            review_divs = soup.find_all('div', {'data-hook': 'review'})

            for review_div in review_divs:
                # Extract review data
                title_elem = review_div.find('a', {'data-hook': 'review-title'})
                title = title_elem.text.strip() if title_elem else ""

                rating_elem = review_div.find('i', {'data-hook': 'review-star-rating'})
                rating = None
                if rating_elem:
                    rating_text = rating_elem.text.strip()
                    rating = float(rating_text.split(' ')[0])

                body_elem = review_div.find('span', {'data-hook': 'review-body'})
                body = body_elem.text.strip() if body_elem else ""

                date_elem = review_div.find('span', {'data-hook': 'review-date'})
                date = date_elem.text.strip() if date_elem else ""

                verified_elem = review_div.find('span', {'data-hook': 'avp-badge'})
                verified = verified_elem is not None

                reviews.append({
                    'title': title,
                    'rating': rating,
                    'body': body,
                    'date': date,
                    'verified': verified
                })

            # Be respectful - add delay between requests
            time.sleep(2)

        return pd.DataFrame(reviews)

    def analyze_reviews(self, reviews_df):
        """
        Analyze review sentiment and extract insights
        """
        # Rating distribution
        rating_dist = reviews_df['rating'].value_counts().sort_index()

        # Average rating
        avg_rating = reviews_df['rating'].mean()

        # Verified vs unverified
        verified_pct = (reviews_df['verified'].sum() / len(reviews_df)) * 100

        # Common words in positive vs negative reviews
        positive_reviews = reviews_df[reviews_df['rating'] >= 4]['body'].str.cat(sep=' ')
        negative_reviews = reviews_df[reviews_df['rating'] <= 2]['body'].str.cat(sep=' ')

        return {
            'avg_rating': avg_rating,
            'total_reviews': len(reviews_df),
            'verified_percentage': verified_pct,
            'rating_distribution': rating_dist.to_dict()
        }

# Usage
scraper = ReviewScraper()

# Scrape reviews
reviews = scraper.scrape_amazon_reviews(
    'https://www.amazon.com/dp/B08N5WRWNW',
    max_pages=3
)

# Analyze
analysis = scraper.analyze_reviews(reviews)
print(f"Average Rating: {analysis['avg_rating']:.2f}/5.0")
print(f"Total Reviews: {analysis['total_reviews']}")
print(f"Verified: {analysis['verified_percentage']:.1f}%")
```

### 3. SEO Metadata Extractor

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

class SEOMetadataExtractor:
    """
    Extract SEO metadata from competitor websites
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def extract_metadata(self, url):
        """
        Extract comprehensive SEO metadata
        """
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        metadata = {
            'url': url,
            'title': None,
            'meta_description': None,
            'meta_keywords': None,
            'h1_tags': [],
            'h2_tags': [],
            'canonical_url': None,
            'og_title': None,
            'og_description': None,
            'og_image': None,
            'twitter_card': None,
            'total_links': 0,
            'internal_links': 0,
            'external_links': 0,
            'images_count': 0,
            'images_with_alt': 0
        }

        # Title tag
        title = soup.find('title')
        metadata['title'] = title.text.strip() if title else None

        # Meta tags
        meta_desc = soup.find('meta', {'name': 'description'})
        metadata['meta_description'] = meta_desc.get('content', '') if meta_desc else None

        meta_keywords = soup.find('meta', {'name': 'keywords'})
        metadata['meta_keywords'] = meta_keywords.get('content', '') if meta_keywords else None

        # Heading tags
        metadata['h1_tags'] = [h1.text.strip() for h1 in soup.find_all('h1')]
        metadata['h2_tags'] = [h2.text.strip() for h2 in soup.find_all('h2')]

        # Canonical URL
        canonical = soup.find('link', {'rel': 'canonical'})
        metadata['canonical_url'] = canonical.get('href', '') if canonical else None

        # Open Graph tags
        og_title = soup.find('meta', {'property': 'og:title'})
        metadata['og_title'] = og_title.get('content', '') if og_title else None

        og_desc = soup.find('meta', {'property': 'og:description'})
        metadata['og_description'] = og_desc.get('content', '') if og_desc else None

        og_image = soup.find('meta', {'property': 'og:image'})
        metadata['og_image'] = og_image.get('content', '') if og_image else None

        # Twitter Card
        twitter_card = soup.find('meta', {'name': 'twitter:card'})
        metadata['twitter_card'] = twitter_card.get('content', '') if twitter_card else None

        # Links analysis
        all_links = soup.find_all('a', href=True)
        metadata['total_links'] = len(all_links)

        domain = url.split('/')[2]
        for link in all_links:
            if domain in link['href'] or link['href'].startswith('/'):
                metadata['internal_links'] += 1
            else:
                metadata['external_links'] += 1

        # Images analysis
        images = soup.find_all('img')
        metadata['images_count'] = len(images)
        metadata['images_with_alt'] = sum(1 for img in images if img.get('alt'))

        return metadata

    def analyze_competitors_seo(self, competitor_urls):
        """
        Analyze SEO for multiple competitors
        """
        results = []

        for url in competitor_urls:
            try:
                metadata = self.extract_metadata(url)
                results.append(metadata)
                time.sleep(1)  # Be respectful
            except Exception as e:
                print(f"Error analyzing {url}: {e}")

        return pd.DataFrame(results)

# Usage
seo = SEOMetadataExtractor()

competitors = [
    'https://www.competitor1.com/product',
    'https://www.competitor2.com/product',
    'https://www.competitor3.com/product'
]

seo_data = seo.analyze_competitors_seo(competitors)
print("\nSEO Comparison:")
print(seo_data[['url', 'title', 'meta_description', 'h1_tags', 'total_links']])
```

### 4. Social Media Metrics Scraper

```python
import requests
from bs4 import BeautifulSoup
import json

class SocialMediaScraper:
    """
    Scrape public social media metrics
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_linkedin_company(self, company_url):
        """
        Scrape public LinkedIn company data
        """
        response = requests.get(company_url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        data = {
            'url': company_url,
            'company_name': None,
            'followers': None,
            'employees': None,
            'industry': None
        }

        # Company name
        name_elem = soup.find('h1', {'class': 'org-top-card-summary__title'})
        if name_elem:
            data['company_name'] = name_elem.text.strip()

        # Followers (look for text containing "followers")
        followers_elem = soup.find('div', text=lambda t: t and 'followers' in t.lower())
        if followers_elem:
            followers_text = followers_elem.text.strip()
            # Extract number from text like "1,234 followers"
            data['followers'] = followers_text.split(' ')[0].replace(',', '')

        return data

    def get_facebook_share_count(self, url):
        """
        Get Facebook share count for a URL
        """
        api_url = f"https://graph.facebook.com/?id={url}"

        response = requests.get(api_url)
        data = response.json()

        return {
            'url': url,
            'facebook_shares': data.get('share', {}).get('share_count', 0)
        }

# Usage
social = SocialMediaScraper()

# Get LinkedIn company data
linkedin_data = social.scrape_linkedin_company(
    'https://www.linkedin.com/company/example-company'
)
print(linkedin_data)
```

### 5. Competitor Content Monitor

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import hashlib

class ContentMonitor:
    """
    Monitor competitor blog posts and content updates
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_blog_posts(self, blog_url, article_selector, title_selector, date_selector):
        """
        Scrape blog posts from competitor blogs
        """
        response = requests.get(blog_url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = []
        article_elements = soup.select(article_selector)

        for article in article_elements:
            title_elem = article.select_one(title_selector)
            title = title_elem.text.strip() if title_elem else "No title"

            link_elem = article.find('a', href=True)
            link = link_elem['href'] if link_elem else ""

            # Make relative URLs absolute
            if link.startswith('/'):
                domain = '/'.join(blog_url.split('/')[:3])
                link = domain + link

            date_elem = article.select_one(date_selector)
            date = date_elem.text.strip() if date_elem else "Unknown"

            # Generate content hash for change detection
            content_hash = hashlib.md5(title.encode()).hexdigest()

            articles.append({
                'title': title,
                'url': link,
                'date': date,
                'content_hash': content_hash,
                'scraped_at': datetime.now()
            })

        return pd.DataFrame(articles)

    def detect_new_content(self, current_articles, previous_articles):
        """
        Detect new blog posts since last check
        """
        if previous_articles is None or len(previous_articles) == 0:
            return current_articles

        previous_hashes = set(previous_articles['content_hash'])
        current_hashes = set(current_articles['content_hash'])

        new_hashes = current_hashes - previous_hashes
        new_articles = current_articles[current_articles['content_hash'].isin(new_hashes)]

        return new_articles

# Usage
monitor = ContentMonitor()

# Scrape competitor blog
articles = monitor.scrape_blog_posts(
    blog_url='https://competitor.com/blog',
    article_selector='article.post',
    title_selector='h2.post-title',
    date_selector='time.post-date'
)

print(f"\nFound {len(articles)} articles")
print(articles[['title', 'date']].head())
```

### 6. Market Research Data Collector

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

class MarketResearchScraper:
    """
    Collect market research data from public sources
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_product_listings(self, search_url, max_results=50):
        """
        Scrape product listings for market analysis
        """
        response = requests.get(search_url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        products = []

        # This is site-specific - adjust selectors for your target
        product_cards = soup.find_all('div', {'class': 'product-card'})[:max_results]

        for card in product_cards:
            title = card.find('h3', {'class': 'product-title'})
            price = card.find('span', {'class': 'product-price'})
            rating = card.find('span', {'class': 'product-rating'})
            reviews = card.find('span', {'class': 'review-count'})

            products.append({
                'title': title.text.strip() if title else None,
                'price': price.text.strip() if price else None,
                'rating': rating.text.strip() if rating else None,
                'review_count': reviews.text.strip() if reviews else None
            })

        return pd.DataFrame(products)

# Usage
research = MarketResearchScraper()

# Scrape product data
products = research.scrape_product_listings(
    'https://example.com/search?q=wireless+headphones',
    max_results=100
)

# Analyze market
print("\nMarket Analysis:")
print(f"Total products: {len(products)}")
print(f"Price range: {products['price'].min()} - {products['price'].max()}")
```

## Installation

```bash
uv pip install beautifulsoup4 requests pandas lxml
```

## Quick Start

```python
import requests
from bs4 import BeautifulSoup

# Fetch webpage
url = 'https://example.com'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract title
title = soup.find('title').text
print(f"Page title: {title}")

# Find all links
links = soup.find_all('a')
for link in links:
    print(link.get('href'))
```

## Best Practices

1. **Respect robots.txt** - Always check and follow site's robots.txt
2. **Add delays** - Use time.sleep() between requests to avoid overwhelming servers
3. **Handle errors** - Use try/except to handle network and parsing errors
4. **User agents** - Set realistic User-Agent headers
5. **Check ToS** - Review website terms of service before scraping
6. **Cache results** - Store scraped data to avoid repeated requests
7. **Monitor changes** - Websites change structure - monitor your scrapers

## Legal Considerations

- Only scrape publicly available data
- Respect copyright and intellectual property
- Follow website terms of service
- Don't overwhelm servers with requests
- Consider using official APIs when available

## References

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Library](https://requests.readthedocs.io/)
- [Web Scraping Best Practices](https://www.scrapehero.com/web-scraping-best-practices/)

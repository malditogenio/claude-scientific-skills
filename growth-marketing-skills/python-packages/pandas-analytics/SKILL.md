---
name: pandas-analytics
description: "Data manipulation and analysis for marketing. DataFrame operations, time series, aggregations, pivot tables, customer analytics, cohort analysis, RFM scoring."
---

# Pandas for Marketing Analytics

## Overview

pandas is the foundational data manipulation library for marketing analytics. This skill covers using pandas for customer data analysis, campaign performance tracking, cohort analysis, RFM segmentation, and all types of marketing data transformations.

## When to Use This Skill

- Analyzing customer transaction data and purchase history
- Creating cohort analysis and retention tables
- Building RFM (Recency, Frequency, Monetary) segments
- Processing campaign performance data
- Aggregating metrics by time periods, segments, or channels
- Merging data from multiple marketing sources
- Cleaning and preparing data for ML models

## Core Capabilities

### 1. Customer Analytics

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load customer transaction data
df = pd.read_csv('transactions.csv', parse_dates=['order_date'])

# Calculate customer-level metrics
customer_metrics = df.groupby('customer_id').agg({
    'order_id': 'count',           # Frequency
    'revenue': ['sum', 'mean'],     # Monetary
    'order_date': ['min', 'max']    # First/Last purchase
}).reset_index()

customer_metrics.columns = ['customer_id', 'order_count', 'total_revenue',
                            'avg_order_value', 'first_purchase', 'last_purchase']

# Calculate customer lifetime
customer_metrics['customer_lifetime_days'] = (
    customer_metrics['last_purchase'] - customer_metrics['first_purchase']
).dt.days
```

### 2. RFM Segmentation

```python
# Calculate RFM scores
reference_date = df['order_date'].max() + timedelta(days=1)

rfm = df.groupby('customer_id').agg({
    'order_date': lambda x: (reference_date - x.max()).days,  # Recency
    'order_id': 'count',                                       # Frequency
    'revenue': 'sum'                                           # Monetary
}).reset_index()

rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']

# Create RFM scores (1-5 scale)
rfm['r_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])
rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
rfm['m_score'] = pd.qcut(rfm['monetary'].rank(method='first'), 5, labels=[1,2,3,4,5])

# Combined RFM score
rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)

# Segment mapping
def rfm_segment(row):
    if row['r_score'] >= 4 and row['f_score'] >= 4:
        return 'Champions'
    elif row['r_score'] >= 3 and row['f_score'] >= 3:
        return 'Loyal Customers'
    elif row['r_score'] >= 4 and row['f_score'] <= 2:
        return 'New Customers'
    elif row['r_score'] <= 2 and row['f_score'] >= 4:
        return 'At Risk'
    elif row['r_score'] <= 2 and row['f_score'] <= 2:
        return 'Lost'
    else:
        return 'Others'

rfm['segment'] = rfm.apply(rfm_segment, axis=1)
```

### 3. Cohort Analysis

```python
# Create cohort analysis
df['order_month'] = df['order_date'].dt.to_period('M')
df['cohort'] = df.groupby('customer_id')['order_date'].transform('min').dt.to_period('M')

# Calculate cohort index (months since first purchase)
df['cohort_index'] = (df['order_month'] - df['cohort']).apply(lambda x: x.n)

# Create cohort table
cohort_data = df.groupby(['cohort', 'cohort_index'])['customer_id'].nunique().reset_index()
cohort_table = cohort_data.pivot(index='cohort', columns='cohort_index', values='customer_id')

# Calculate retention rates
cohort_sizes = cohort_table.iloc[:, 0]
retention_table = cohort_table.divide(cohort_sizes, axis=0) * 100
```

### 4. Campaign Performance Analysis

```python
# Analyze campaign performance over time
campaigns = pd.read_csv('campaigns.csv', parse_dates=['send_date'])

# Calculate daily metrics
daily_metrics = campaigns.groupby(['campaign_id', 'send_date']).agg({
    'impressions': 'sum',
    'clicks': 'sum',
    'conversions': 'sum',
    'spend': 'sum',
    'revenue': 'sum'
}).reset_index()

# Calculate rates
daily_metrics['ctr'] = daily_metrics['clicks'] / daily_metrics['impressions'] * 100
daily_metrics['conversion_rate'] = daily_metrics['conversions'] / daily_metrics['clicks'] * 100
daily_metrics['roas'] = daily_metrics['revenue'] / daily_metrics['spend']
daily_metrics['cpa'] = daily_metrics['spend'] / daily_metrics['conversions']

# Rolling averages
daily_metrics['roas_7d_avg'] = daily_metrics.groupby('campaign_id')['roas'].transform(
    lambda x: x.rolling(7, min_periods=1).mean()
)
```

### 5. Time Series Analysis

```python
# Resample to different frequencies
daily_revenue = df.set_index('order_date').resample('D')['revenue'].sum()
weekly_revenue = df.set_index('order_date').resample('W')['revenue'].sum()
monthly_revenue = df.set_index('order_date').resample('M')['revenue'].sum()

# Year-over-year comparison
df['year'] = df['order_date'].dt.year
df['week'] = df['order_date'].dt.isocalendar().week

yoy_comparison = df.groupby(['year', 'week'])['revenue'].sum().unstack(0)
yoy_comparison['yoy_growth'] = (
    (yoy_comparison[2024] - yoy_comparison[2023]) / yoy_comparison[2023] * 100
)
```

### 6. Multi-Source Data Merging

```python
# Merge data from multiple marketing platforms
ga_data = pd.read_csv('google_analytics.csv')
ads_data = pd.read_csv('meta_ads.csv')
crm_data = pd.read_csv('hubspot.csv')

# Merge on common keys
combined = ga_data.merge(
    ads_data,
    left_on='utm_campaign',
    right_on='campaign_name',
    how='left'
)

combined = combined.merge(
    crm_data,
    on='email',
    how='left'
)

# Handle duplicates and missing values
combined = combined.drop_duplicates(subset=['session_id'])
combined['revenue'].fillna(0, inplace=True)
```

## Installation

```bash
uv pip install pandas numpy
```

## Quick Start

```python
import pandas as pd

# Load your marketing data
df = pd.read_csv('marketing_data.csv')

# Quick summary statistics
print(df.describe())
print(df.info())

# Group by channel and calculate metrics
channel_performance = df.groupby('channel').agg({
    'sessions': 'sum',
    'conversions': 'sum',
    'revenue': 'sum'
})
channel_performance['conversion_rate'] = (
    channel_performance['conversions'] / channel_performance['sessions'] * 100
)

print(channel_performance.sort_values('revenue', ascending=False))
```

## Best Practices

1. **Use appropriate dtypes** - Convert dates with `parse_dates`, use `category` for low-cardinality strings
2. **Chain operations** - Use method chaining for cleaner code
3. **Avoid loops** - Use vectorized operations for performance
4. **Handle missing data** - Always check for and handle NaN values appropriately
5. **Memory management** - Use `chunksize` for large files, downcasting for numeric types

## References

- [pandas Documentation](https://pandas.pydata.org/docs/)
- [10 Minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)

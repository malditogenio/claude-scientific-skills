---
name: csv-data
description: "CSV data toolkit for marketing analytics. Import platform exports, clean campaign data, merge sources, analyze performance, for data-driven marketing optimization."
license: Proprietary. LICENSE.txt has complete terms
---

# CSV Data Processing for Marketing

## Overview

Import, clean, analyze, and export CSV data from marketing platforms. Process campaign exports, consolidate multi-source data, perform analytics, and prepare data for visualization and reporting. Apply this skill for marketing data operations and campaign optimization.

## When to Use

- **Platform Data Export**: Process CSV exports from Google Ads, Facebook Ads, etc.
- **Data Consolidation**: Merge data from multiple marketing platforms
- **Campaign Analysis**: Analyze performance metrics and identify trends
- **Data Cleaning**: Standardize and validate marketing data
- **Attribution Modeling**: Process multi-touch attribution data
- **Bulk Operations**: Prepare CSV files for platform bulk uploads
- **Reporting Automation**: Generate regular performance reports

## Installation

```bash
# Core data processing
uv pip install pandas numpy

# For advanced analytics
uv pip install scipy scikit-learn

# For date handling
uv pip install python-dateutil

# For data validation
uv pip install pandera
```

## Core Capabilities

### 1. Importing and Cleaning Platform Data

Import CSV exports from marketing platforms and standardize the data:

```python
import pandas as pd
import numpy as np
from datetime import datetime

def import_google_ads_data(csv_file):
    """Import and clean Google Ads CSV export"""

    # Read CSV, handling Google Ads format quirks
    df = pd.read_csv(csv_file, skiprows=2)  # Skip header rows

    # Remove summary rows (often at bottom)
    df = df[df['Campaign'].notna()]
    df = df[df['Campaign'] != 'Total']

    # Clean currency columns
    if 'Cost' in df.columns:
        df['Cost'] = df['Cost'].str.replace('$', '').str.replace(',', '')
        df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')

    # Clean percentage columns
    if 'CTR' in df.columns:
        df['CTR'] = df['CTR'].str.replace('%', '')
        df['CTR'] = pd.to_numeric(df['CTR'], errors='coerce')

    # Clean number columns
    numeric_cols = ['Impressions', 'Clicks', 'Conversions']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].str.replace(',', '') if df[col].dtype == 'object' else df[col]
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Parse dates
    if 'Day' in df.columns:
        df['Day'] = pd.to_datetime(df['Day'])

    # Add platform identifier
    df['platform'] = 'Google Ads'

    return df

def import_facebook_ads_data(csv_file):
    """Import and clean Facebook Ads CSV export"""

    df = pd.read_csv(csv_file)

    # Rename columns to standard format
    column_mapping = {
        'Campaign name': 'Campaign',
        'Amount spent (USD)': 'Cost',
        'Link clicks': 'Clicks',
        'Results': 'Conversions',
        'Reporting starts': 'Date'
    }

    df = df.rename(columns=column_mapping)

    # Clean cost column
    if 'Cost' in df.columns:
        df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')

    # Parse dates
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])

    # Calculate CTR if not present
    if 'Impressions' in df.columns and 'Clicks' in df.columns:
        df['CTR'] = (df['Clicks'] / df['Impressions'] * 100).round(2)

    df['platform'] = 'Facebook Ads'

    return df

# Import from multiple platforms
google_data = import_google_ads_data('google_ads_export.csv')
facebook_data = import_facebook_ads_data('facebook_ads_export.csv')

# Save cleaned data
google_data.to_csv('google_ads_clean.csv', index=False)
facebook_data.to_csv('facebook_ads_clean.csv', index=False)
```

### 2. Consolidating Multi-Platform Data

Merge data from different marketing platforms into a unified dataset:

```python
def consolidate_marketing_data(file_paths):
    """Consolidate data from multiple marketing platforms"""

    all_data = []

    for platform, file_path in file_paths.items():
        if platform == 'google_ads':
            df = import_google_ads_data(file_path)
        elif platform == 'facebook_ads':
            df = import_facebook_ads_data(file_path)
        elif platform == 'linkedin_ads':
            df = pd.read_csv(file_path)
            df['platform'] = 'LinkedIn Ads'
        else:
            df = pd.read_csv(file_path)

        all_data.append(df)

    # Combine all platforms
    consolidated = pd.concat(all_data, ignore_index=True)

    # Standardize column names
    consolidated.columns = consolidated.columns.str.lower().str.replace(' ', '_')

    # Calculate unified metrics
    if 'clicks' in consolidated.columns and 'impressions' in consolidated.columns:
        consolidated['ctr'] = (consolidated['clicks'] / consolidated['impressions'] * 100).round(2)

    if 'cost' in consolidated.columns and 'clicks' in consolidated.columns:
        consolidated['cpc'] = (consolidated['cost'] / consolidated['clicks']).round(2)

    if 'cost' in consolidated.columns and 'conversions' in consolidated.columns:
        consolidated['cpa'] = (consolidated['cost'] / consolidated['conversions']).round(2)

    if 'revenue' in consolidated.columns and 'cost' in consolidated.columns:
        consolidated['roas'] = (consolidated['revenue'] / consolidated['cost']).round(2)

    return consolidated

# Consolidate data
platforms = {
    'google_ads': 'google_ads_nov.csv',
    'facebook_ads': 'facebook_ads_nov.csv',
    'linkedin_ads': 'linkedin_ads_nov.csv'
}

consolidated_data = consolidate_marketing_data(platforms)
consolidated_data.to_csv('all_platforms_consolidated.csv', index=False)

# Summary by platform
platform_summary = consolidated_data.groupby('platform').agg({
    'impressions': 'sum',
    'clicks': 'sum',
    'conversions': 'sum',
    'cost': 'sum'
}).round(2)

print(platform_summary)
```

### 3. Campaign Performance Analysis

Analyze campaign data to identify top performers and optimization opportunities:

```python
def analyze_campaign_performance(df):
    """Analyze campaign performance and identify insights"""

    # Calculate key metrics by campaign
    campaign_metrics = df.groupby('campaign').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'cost': 'sum',
        'revenue': 'sum'
    }).reset_index()

    # Calculate derived metrics
    campaign_metrics['ctr'] = (campaign_metrics['clicks'] / campaign_metrics['impressions'] * 100).round(2)
    campaign_metrics['cvr'] = (campaign_metrics['conversions'] / campaign_metrics['clicks'] * 100).round(2)
    campaign_metrics['cpc'] = (campaign_metrics['cost'] / campaign_metrics['clicks']).round(2)
    campaign_metrics['cpa'] = (campaign_metrics['cost'] / campaign_metrics['conversions']).round(2)
    campaign_metrics['roas'] = (campaign_metrics['revenue'] / campaign_metrics['cost']).round(2)

    # Identify top performers
    top_roas = campaign_metrics.nlargest(5, 'roas')[['campaign', 'roas', 'cost', 'revenue']]
    top_conversions = campaign_metrics.nlargest(5, 'conversions')[['campaign', 'conversions', 'cpa']]

    # Identify underperformers (high spend, low ROAS)
    high_spend = campaign_metrics[campaign_metrics['cost'] > campaign_metrics['cost'].quantile(0.75)]
    underperformers = high_spend[high_spend['roas'] < 2.0][['campaign', 'cost', 'roas']]

    # Identify optimization opportunities
    # High CTR but low CVR = landing page issue
    optimization_opps = campaign_metrics[
        (campaign_metrics['ctr'] > campaign_metrics['ctr'].median()) &
        (campaign_metrics['cvr'] < campaign_metrics['cvr'].median())
    ][['campaign', 'ctr', 'cvr']]

    results = {
        'all_campaigns': campaign_metrics,
        'top_roas': top_roas,
        'top_conversions': top_conversions,
        'underperformers': underperformers,
        'optimization_opportunities': optimization_opps
    }

    return results

# Analyze performance
analysis = analyze_campaign_performance(consolidated_data)

# Save results
analysis['all_campaigns'].to_csv('campaign_performance_analysis.csv', index=False)
analysis['top_roas'].to_csv('top_performing_campaigns.csv', index=False)
analysis['optimization_opportunities'].to_csv('optimization_opportunities.csv', index=False)

# Print summary
print("Top 5 Campaigns by ROAS:")
print(analysis['top_roas'])
print("\nOptimization Opportunities:")
print(analysis['optimization_opportunities'])
```

### 4. Time Series Analysis and Trends

Analyze performance trends over time:

```python
def analyze_time_trends(df, date_column='date'):
    """Analyze performance trends over time"""

    # Ensure date column is datetime
    df[date_column] = pd.to_datetime(df[date_column])

    # Daily trends
    daily_metrics = df.groupby(date_column).agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'cost': 'sum',
        'revenue': 'sum'
    }).reset_index()

    # Calculate daily metrics
    daily_metrics['ctr'] = (daily_metrics['clicks'] / daily_metrics['impressions'] * 100).round(2)
    daily_metrics['roas'] = (daily_metrics['revenue'] / daily_metrics['cost']).round(2)

    # Add moving averages for trend analysis
    daily_metrics['conversions_7day_avg'] = daily_metrics['conversions'].rolling(window=7).mean().round(2)
    daily_metrics['roas_7day_avg'] = daily_metrics['roas'].rolling(window=7).mean().round(2)

    # Week-over-week comparison
    daily_metrics['week'] = daily_metrics[date_column].dt.isocalendar().week
    weekly_metrics = daily_metrics.groupby('week').agg({
        'conversions': 'sum',
        'cost': 'sum',
        'revenue': 'sum'
    })

    weekly_metrics['wow_conversion_change'] = weekly_metrics['conversions'].pct_change() * 100
    weekly_metrics['wow_revenue_change'] = weekly_metrics['revenue'].pct_change() * 100

    # Day of week analysis
    daily_metrics['day_of_week'] = daily_metrics[date_column].dt.day_name()
    dow_performance = daily_metrics.groupby('day_of_week').agg({
        'conversions': 'mean',
        'cost': 'mean',
        'roas': 'mean'
    }).round(2)

    results = {
        'daily': daily_metrics,
        'weekly': weekly_metrics,
        'day_of_week': dow_performance
    }

    return results

# Analyze trends
trends = analyze_time_trends(consolidated_data)

# Save results
trends['daily'].to_csv('daily_performance_trends.csv', index=False)
trends['weekly'].to_csv('weekly_performance.csv', index=False)
trends['day_of_week'].to_csv('day_of_week_analysis.csv', index=False)

print("Day of Week Performance:")
print(trends['day_of_week'])
```

### 5. Data Validation and Quality Checks

Validate marketing data for completeness and accuracy:

```python
def validate_marketing_data(df):
    """Validate marketing data quality"""

    issues = []

    # Check for missing critical columns
    required_columns = ['campaign', 'impressions', 'clicks', 'cost']
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        issues.append(f"Missing required columns: {missing_cols}")

    # Check for null values
    null_counts = df[required_columns].isnull().sum()
    if null_counts.any():
        issues.append(f"Null values found:\n{null_counts[null_counts > 0]}")

    # Check for negative values
    numeric_cols = ['impressions', 'clicks', 'cost', 'conversions']
    for col in numeric_cols:
        if col in df.columns:
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                issues.append(f"{col} has {negative_count} negative values")

    # Check for impossible CTR (>100%)
    if 'ctr' in df.columns:
        high_ctr = (df['ctr'] > 100).sum()
        if high_ctr > 0:
            issues.append(f"{high_ctr} rows have CTR > 100%")

    # Check for clicks > impressions
    if 'clicks' in df.columns and 'impressions' in df.columns:
        invalid_clicks = (df['clicks'] > df['impressions']).sum()
        if invalid_clicks > 0:
            issues.append(f"{invalid_clicks} rows have clicks > impressions")

    # Check for conversions > clicks
    if 'conversions' in df.columns and 'clicks' in df.columns:
        invalid_conversions = (df['conversions'] > df['clicks']).sum()
        if invalid_conversions > 0:
            issues.append(f"{invalid_conversions} rows have conversions > clicks")

    # Check for duplicate rows
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        issues.append(f"{duplicates} duplicate rows found")

    # Data quality score
    total_checks = 7
    failed_checks = len(issues)
    quality_score = ((total_checks - failed_checks) / total_checks * 100)

    validation_result = {
        'quality_score': quality_score,
        'issues': issues,
        'total_rows': len(df),
        'total_columns': len(df.columns)
    }

    return validation_result

# Validate data
validation = validate_marketing_data(consolidated_data)

print(f"Data Quality Score: {validation['quality_score']:.1f}%")
print(f"Total Rows: {validation['total_rows']:,}")

if validation['issues']:
    print("\nData Quality Issues:")
    for issue in validation['issues']:
        print(f"  - {issue}")
else:
    print("\nNo data quality issues found!")
```

### 6. Preparing Bulk Upload Files

Format data for platform bulk uploads:

```python
def prepare_google_ads_upload(campaigns_df):
    """Prepare Google Ads Editor bulk upload CSV"""

    # Select and rename columns for Google Ads format
    upload_df = campaigns_df[['campaign', 'ad_group', 'keyword', 'max_cpc', 'final_url']].copy()

    upload_df.columns = ['Campaign', 'Ad group', 'Keyword', 'Max CPC', 'Final URL']

    # Add required columns
    upload_df['Match type'] = 'Exact'
    upload_df['Status'] = 'Enabled'
    upload_df['Labels'] = ''

    # Format CPC (no currency symbol)
    upload_df['Max CPC'] = upload_df['Max CPC'].round(2)

    # Reorder columns for Google Ads Editor
    column_order = ['Campaign', 'Ad group', 'Keyword', 'Match type',
                   'Max CPC', 'Final URL', 'Status', 'Labels']
    upload_df = upload_df[column_order]

    return upload_df

def prepare_facebook_ads_upload(campaigns_df):
    """Prepare Facebook Ads bulk upload CSV"""

    upload_df = campaigns_df[[
        'campaign_name', 'ad_set_name', 'ad_name',
        'daily_budget', 'lifetime_budget',
        'start_date', 'end_date'
    ]].copy()

    # Rename for Facebook format
    upload_df.columns = [
        'Campaign Name', 'Ad Set Name', 'Ad Name',
        'Daily Budget', 'Lifetime Budget',
        'Start Date', 'End Date'
    ]

    # Add Facebook-specific columns
    upload_df['Status'] = 'ACTIVE'
    upload_df['Optimization Goal'] = 'CONVERSIONS'
    upload_df['Bid Strategy'] = 'LOWEST_COST_WITH_BID_CAP'

    # Format dates
    upload_df['Start Date'] = pd.to_datetime(upload_df['Start Date']).dt.strftime('%Y-%m-%d')
    upload_df['End Date'] = pd.to_datetime(upload_df['End Date']).dt.strftime('%Y-%m-%d')

    return upload_df

# Prepare uploads
# google_upload = prepare_google_ads_upload(campaign_data)
# google_upload.to_csv('google_ads_bulk_upload.csv', index=False)

# facebook_upload = prepare_facebook_ads_upload(campaign_data)
# facebook_upload.to_csv('facebook_ads_bulk_upload.csv', index=False)
```

### 7. Attribution Data Processing

Process multi-touch attribution data:

```python
def process_attribution_data(attribution_df):
    """Process multi-touch attribution data"""

    # Parse user journey
    attribution_df['touchpoints'] = attribution_df['touchpoint_sequence'].str.split(',')
    attribution_df['touchpoint_count'] = attribution_df['touchpoints'].apply(len)

    # First touch attribution
    attribution_df['first_touch'] = attribution_df['touchpoints'].apply(lambda x: x[0] if x else None)

    # Last touch attribution
    attribution_df['last_touch'] = attribution_df['touchpoints'].apply(lambda x: x[-1] if x else None)

    # Calculate attribution by channel
    # First touch
    first_touch_attribution = attribution_df.groupby('first_touch').agg({
        'conversion_value': 'sum',
        'user_id': 'count'
    }).rename(columns={'user_id': 'conversions'})

    # Last touch
    last_touch_attribution = attribution_df.groupby('last_touch').agg({
        'conversion_value': 'sum',
        'user_id': 'count'
    }).rename(columns={'user_id': 'conversions'})

    # Linear attribution (equal credit to all touchpoints)
    linear_attribution = {}
    for _, row in attribution_df.iterrows():
        touchpoints = row['touchpoints']
        value = row['conversion_value']
        credit_per_touchpoint = value / len(touchpoints)

        for touchpoint in touchpoints:
            if touchpoint not in linear_attribution:
                linear_attribution[touchpoint] = {'value': 0, 'conversions': 0}
            linear_attribution[touchpoint]['value'] += credit_per_touchpoint
            linear_attribution[touchpoint]['conversions'] += 1 / len(touchpoints)

    linear_df = pd.DataFrame(linear_attribution).T

    results = {
        'first_touch': first_touch_attribution,
        'last_touch': last_touch_attribution,
        'linear': linear_df
    }

    return results

# Example attribution data
attribution_data = pd.DataFrame({
    'user_id': range(1, 6),
    'touchpoint_sequence': [
        'Paid Search,Email,Direct',
        'Social,Display,Social',
        'Paid Search,Direct',
        'Email,Social,Email,Direct',
        'Display,Paid Search,Direct'
    ],
    'conversion_value': [150, 200, 120, 180, 160]
})

# Process attribution
attribution_results = process_attribution_data(attribution_data)

print("First Touch Attribution:")
print(attribution_results['first_touch'])
print("\nLast Touch Attribution:")
print(attribution_results['last_touch'])
print("\nLinear Attribution:")
print(attribution_results['linear'])
```

## Quick Start

### Read and Analyze CSV

```python
import pandas as pd

# Read CSV
df = pd.read_csv('campaign_data.csv')

# Basic info
print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")

# Summary statistics
print(df.describe())

# Group by campaign
campaign_summary = df.groupby('campaign')['conversions'].sum()
print(campaign_summary)
```

### Clean and Export Data

```python
# Remove duplicates
df = df.drop_duplicates()

# Fill missing values
df['conversions'].fillna(0, inplace=True)

# Calculate metrics
df['ctr'] = (df['clicks'] / df['impressions'] * 100).round(2)
df['cpc'] = (df['cost'] / df['clicks']).round(2)

# Export clean data
df.to_csv('cleaned_campaign_data.csv', index=False)
```

### Merge Multiple Files

```python
# Read multiple CSVs
files = ['jan.csv', 'feb.csv', 'mar.csv']
dfs = [pd.read_csv(f) for f in files]

# Concatenate
combined = pd.concat(dfs, ignore_index=True)

# Save merged data
combined.to_csv('q1_combined.csv', index=False)
```

## Best Practices

### Data Import

1. **Encoding**: Specify encoding when reading CSVs
   ```python
   df = pd.read_csv('file.csv', encoding='utf-8')
   ```

2. **Data Types**: Specify column types to avoid inference issues
   ```python
   df = pd.read_csv('file.csv', dtype={'campaign_id': str, 'cost': float})
   ```

3. **Date Parsing**: Parse dates during import
   ```python
   df = pd.read_csv('file.csv', parse_dates=['date', 'start_date'])
   ```

### Data Cleaning

1. **Remove Whitespace**: Clean string columns
   ```python
   df['campaign'] = df['campaign'].str.strip()
   ```

2. **Standardize Cases**: Consistent casing
   ```python
   df['platform'] = df['platform'].str.lower()
   ```

3. **Handle Missing Data**: Choose appropriate strategy
   ```python
   # Fill with 0 for metrics
   df['conversions'].fillna(0, inplace=True)

   # Drop rows with critical missing data
   df.dropna(subset=['campaign', 'date'], inplace=True)
   ```

### Performance Optimization

```python
# For large files, use chunks
chunk_size = 10000
chunks = []

for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    # Process each chunk
    processed = process_chunk(chunk)
    chunks.append(processed)

result = pd.concat(chunks)

# Use efficient data types
df['campaign_id'] = df['campaign_id'].astype('category')
df['impressions'] = pd.to_numeric(df['impressions'], downcast='integer')
```

## References

### Libraries

- **pandas**: Data manipulation and analysis
  - [Documentation](https://pandas.pydata.org/docs/)
  - Essential for CSV processing

- **numpy**: Numerical computing
  - [Documentation](https://numpy.org/doc/)
  - Used with pandas for calculations

- **scipy**: Statistical analysis
  - [Documentation](https://scipy.org/)
  - For advanced analytics

- **pandera**: Data validation
  - [Documentation](https://pandera.readthedocs.io/)
  - Schema validation for data quality

### Common Data Quality Issues

1. **Encoding Problems**: Use UTF-8 or detect encoding
2. **Inconsistent Delimiters**: Verify CSV uses commas
3. **Quote Characters**: Handle quoted fields correctly
4. **Header Rows**: Skip or handle platform-specific headers
5. **Summary Rows**: Remove total/summary rows from exports
6. **Date Formats**: Standardize date formatting
7. **Currency Symbols**: Remove before converting to numeric

### Marketing Data Standards

1. **Column Naming**: Use lowercase with underscores (snake_case)
2. **Date Format**: YYYY-MM-DD (ISO 8601)
3. **Currency**: Store as numeric without symbols
4. **Percentages**: Store as decimal (0.15 not 15%)
5. **Platform IDs**: Keep as strings to preserve leading zeros
6. **Campaign Names**: Consistent naming conventions across platforms

### Useful Pandas Operations

```python
# Filter data
recent_campaigns = df[df['date'] > '2024-01-01']
high_performers = df[df['roas'] > 3.0]

# Sort data
top_campaigns = df.sort_values('conversions', ascending=False).head(10)

# Pivot tables
pivot = df.pivot_table(
    values='conversions',
    index='campaign',
    columns='platform',
    aggfunc='sum'
)

# Group and aggregate
summary = df.groupby(['platform', 'campaign']).agg({
    'impressions': 'sum',
    'clicks': 'sum',
    'cost': 'sum',
    'conversions': 'sum'
})

# Calculate percentages
df['conversion_rate'] = (df['conversions'] / df['clicks'] * 100).round(2)

# Create date-based columns
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.day_name()
df['quarter'] = df['date'].dt.quarter
```

---
name: cohort-analysis
description: Analyze customer behavior over time using cohort analysis. Track retention curves, customer lifecycle patterns, and cohort performance metrics. Build cohort tables, visualize retention heatmaps, calculate cohort LTV, and identify temporal trends in user behavior for growth marketing insights.
---

# Cohort Analysis

## Overview

Cohort analysis groups customers by shared characteristics or time periods to understand how behavior changes over time. This methodology is essential for measuring retention, identifying product-market fit, and tracking the impact of product changes on different user groups.

**Key Capabilities:**
- Time-based cohort construction (acquisition date)
- Behavior-based cohort segmentation
- Retention curve analysis and visualization
- Cohort lifetime value (LTV) calculation
- Engagement and activity cohorts
- Cohort comparison and trend analysis
- Churn rate calculation by cohort

## When to Use This Skill

Use this skill when:
- Measuring user retention over time
- Understanding how product changes affect different user groups
- Calculating lifetime value by acquisition period
- Identifying when users typically churn
- Comparing performance across acquisition channels
- Tracking the impact of onboarding improvements
- Analyzing seasonal or temporal patterns in user behavior

## Core Capabilities

### 1. Building Cohort Tables

Create cohort analysis from user activity data.

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_cohort_table(
    df: pd.DataFrame,
    user_col: str = 'user_id',
    date_col: str = 'activity_date',
    cohort_col: str = 'cohort_date'
) -> pd.DataFrame:
    """
    Create cohort analysis table from user activity data.

    Parameters:
    -----------
    df : DataFrame with columns for user_id, activity_date, and cohort_date
    user_col : Name of user identifier column
    date_col : Name of activity date column
    cohort_col : Name of cohort date column (e.g., signup date)

    Returns:
    --------
    DataFrame : Cohort table with retention percentages
    """
    # Ensure dates are datetime
    df[date_col] = pd.to_datetime(df[date_col])
    df[cohort_col] = pd.to_datetime(df[cohort_col])

    # Create cohort periods (e.g., month of signup)
    df['cohort_period'] = df[cohort_col].dt.to_period('M')

    # Create activity periods
    df['activity_period'] = df[date_col].dt.to_period('M')

    # Calculate periods since cohort
    df['periods_since_cohort'] = (
        df['activity_period'] - df['cohort_period']
    ).apply(lambda x: x.n)

    # Group by cohort and period
    cohort_data = df.groupby(['cohort_period', 'periods_since_cohort'])[user_col].nunique()
    cohort_data = cohort_data.reset_index()

    # Pivot to create cohort table
    cohort_table = cohort_data.pivot(
        index='cohort_period',
        columns='periods_since_cohort',
        values=user_col
    )

    # Calculate retention percentages
    cohort_size = cohort_table.iloc[:, 0]
    retention_table = cohort_table.divide(cohort_size, axis=0) * 100

    return retention_table

# Example: Create sample data
np.random.seed(42)

# Generate user cohorts
n_users = 10000
cohort_dates = pd.date_range('2023-01-01', '2023-12-01', freq='D')

users = []
for user_id in range(n_users):
    cohort_date = np.random.choice(cohort_dates)
    users.append({
        'user_id': user_id,
        'cohort_date': cohort_date
    })

users_df = pd.DataFrame(users)

# Generate activity data (with declining retention)
activities = []
for _, user in users_df.iterrows():
    current_date = user['cohort_date']
    end_date = pd.Timestamp('2024-06-01')

    # Simulate retention decay
    months_active = 0
    while current_date <= end_date:
        # Probability of activity declines each month
        retention_rate = 0.95 ** months_active

        if np.random.random() < retention_rate:
            activities.append({
                'user_id': user['user_id'],
                'activity_date': current_date,
                'cohort_date': user['cohort_date']
            })

        current_date += timedelta(days=30)
        months_active += 1

activity_df = pd.DataFrame(activities)

# Create cohort table
retention_table = create_cohort_table(activity_df)

print("Cohort Retention Table (%):")
print(retention_table.round(1))
```

### 2. Retention Curve Visualization

Visualize retention curves for different cohorts.

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_retention_curves(
    retention_table: pd.DataFrame,
    n_cohorts: int = 6,
    title: str = "Retention Curves by Cohort"
) -> plt.Figure:
    """
    Plot retention curves for recent cohorts.

    Parameters:
    -----------
    retention_table : DataFrame from create_cohort_table
    n_cohorts : Number of recent cohorts to display
    title : Plot title
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # Select recent cohorts
    recent_cohorts = retention_table.tail(n_cohorts)

    # Plot each cohort
    for cohort in recent_cohorts.index:
        cohort_data = recent_cohorts.loc[cohort].dropna()
        ax.plot(
            cohort_data.index,
            cohort_data.values,
            marker='o',
            label=str(cohort),
            linewidth=2
        )

    ax.set_xlabel('Months Since Cohort Start', fontsize=12)
    ax.set_ylabel('Retention Rate (%)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(title='Cohort', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 105)

    plt.tight_layout()
    return fig

# Example: Plot retention curves
fig = plot_retention_curves(retention_table, n_cohorts=6)
plt.savefig('retention_curves.png', dpi=300, bbox_inches='tight')
print("Retention curves saved to: retention_curves.png")
```

### 3. Cohort Heatmap

Create a heatmap showing retention patterns.

```python
def plot_cohort_heatmap(
    retention_table: pd.DataFrame,
    cmap: str = 'RdYlGn',
    title: str = "Cohort Retention Heatmap"
) -> plt.Figure:
    """
    Create heatmap visualization of cohort retention.

    Parameters:
    -----------
    retention_table : DataFrame from create_cohort_table
    cmap : Color map for heatmap
    title : Plot title
    """
    fig, ax = plt.subplots(figsize=(14, 8))

    # Create heatmap
    sns.heatmap(
        retention_table,
        annot=True,
        fmt='.1f',
        cmap=cmap,
        center=50,
        vmin=0,
        vmax=100,
        cbar_kws={'label': 'Retention Rate (%)'},
        ax=ax
    )

    ax.set_xlabel('Months Since Cohort Start', fontsize=12)
    ax.set_ylabel('Cohort Period', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')

    plt.tight_layout()
    return fig

# Example: Create heatmap
fig = plot_cohort_heatmap(retention_table)
plt.savefig('cohort_heatmap.png', dpi=300, bbox_inches='tight')
print("Cohort heatmap saved to: cohort_heatmap.png")
```

### 4. Cohort Lifetime Value (LTV)

Calculate cumulative revenue by cohort.

```python
def calculate_cohort_ltv(
    df: pd.DataFrame,
    user_col: str = 'user_id',
    date_col: str = 'transaction_date',
    cohort_col: str = 'cohort_date',
    revenue_col: str = 'revenue'
) -> pd.DataFrame:
    """
    Calculate cumulative LTV by cohort over time.

    Parameters:
    -----------
    df : DataFrame with user transactions
    user_col : User identifier column
    date_col : Transaction date column
    cohort_col : User cohort date column
    revenue_col : Revenue amount column

    Returns:
    --------
    DataFrame : Cumulative LTV by cohort and period
    """
    # Ensure dates are datetime
    df[date_col] = pd.to_datetime(df[date_col])
    df[cohort_col] = pd.to_datetime(df[cohort_col])

    # Create periods
    df['cohort_period'] = df[cohort_col].dt.to_period('M')
    df['transaction_period'] = df[date_col].dt.to_period('M')

    # Calculate periods since cohort
    df['periods_since_cohort'] = (
        df['transaction_period'] - df['cohort_period']
    ).apply(lambda x: x.n)

    # Group by cohort and period
    ltv_data = df.groupby(['cohort_period', 'periods_since_cohort'])[revenue_col].sum()
    ltv_data = ltv_data.reset_index()

    # Pivot to create LTV table
    ltv_table = ltv_data.pivot(
        index='cohort_period',
        columns='periods_since_cohort',
        values=revenue_col
    )

    # Calculate cumulative LTV
    cumulative_ltv = ltv_table.cumsum(axis=1)

    # Get cohort sizes
    cohort_sizes = df.groupby('cohort_period')[user_col].nunique()

    # Calculate per-user LTV
    ltv_per_user = cumulative_ltv.div(cohort_sizes, axis=0)

    return ltv_per_user

# Example: Generate revenue data
np.random.seed(42)
transactions = []

for _, activity in activity_df.sample(5000).iterrows():
    # Simulate revenue with some probability
    if np.random.random() < 0.3:
        transactions.append({
            'user_id': activity['user_id'],
            'transaction_date': activity['activity_date'],
            'cohort_date': activity['cohort_date'],
            'revenue': np.random.gamma(2, 15)  # Average ~$30
        })

transaction_df = pd.DataFrame(transactions)

# Calculate cohort LTV
ltv_table = calculate_cohort_ltv(transaction_df)

print("\nCohort LTV (Cumulative $ per User):")
print(ltv_table.round(2).head(10))
```

### 5. Cohort Metrics Summary

Calculate key metrics for each cohort.

```python
def calculate_cohort_metrics(
    retention_table: pd.DataFrame,
    ltv_table: pd.DataFrame = None,
    periods: list = [1, 3, 6, 12]
) -> pd.DataFrame:
    """
    Calculate summary metrics for each cohort.

    Parameters:
    -----------
    retention_table : Retention percentages by cohort
    ltv_table : LTV by cohort (optional)
    periods : Which periods to calculate metrics for

    Returns:
    --------
    DataFrame with cohort metrics
    """
    metrics = []

    for cohort in retention_table.index:
        cohort_metrics = {'cohort': str(cohort)}

        # Retention metrics
        for period in periods:
            if period in retention_table.columns:
                cohort_metrics[f'retention_m{period}'] = retention_table.loc[cohort, period]

        # LTV metrics
        if ltv_table is not None:
            for period in periods:
                if period in ltv_table.columns:
                    cohort_metrics[f'ltv_m{period}'] = ltv_table.loc[cohort, period]

            # Total LTV (last available period)
            cohort_metrics['ltv_total'] = ltv_table.loc[cohort].dropna().iloc[-1]

        metrics.append(cohort_metrics)

    return pd.DataFrame(metrics)

# Example: Calculate metrics
cohort_metrics = calculate_cohort_metrics(
    retention_table,
    ltv_table,
    periods=[1, 3, 6, 12]
)

print("\nCohort Metrics Summary:")
print(cohort_metrics.head(10).to_string(index=False))
```

### 6. Behavioral Cohorts

Create cohorts based on user behavior, not just time.

```python
def create_behavioral_cohorts(
    df: pd.DataFrame,
    user_col: str = 'user_id',
    feature_cols: list = None,
    n_clusters: int = 4
) -> pd.DataFrame:
    """
    Create cohorts based on user behavior patterns.

    Parameters:
    -----------
    df : DataFrame with user features
    user_col : User identifier column
    feature_cols : List of columns to use for clustering
    n_clusters : Number of cohorts to create

    Returns:
    --------
    DataFrame with user-cohort assignments
    """
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans

    # Prepare features
    X = df[feature_cols].values

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Cluster users
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['behavior_cohort'] = kmeans.fit_predict(X_scaled)

    # Calculate cohort statistics
    cohort_summary = df.groupby('behavior_cohort')[feature_cols].mean()

    return df, cohort_summary

# Example: Create behavioral cohorts
# First, create user feature summary
user_features = activity_df.groupby('user_id').agg({
    'activity_date': ['count', 'min', 'max']
}).reset_index()

user_features.columns = ['user_id', 'activity_count', 'first_activity', 'last_activity']
user_features['days_active'] = (
    user_features['last_activity'] - user_features['first_activity']
).dt.days

# Add revenue if available
user_revenue = transaction_df.groupby('user_id')['revenue'].sum().reset_index()
user_features = user_features.merge(user_revenue, on='user_id', how='left')
user_features['revenue'] = user_features['revenue'].fillna(0)

# Create behavioral cohorts
users_with_cohorts, cohort_profiles = create_behavioral_cohorts(
    user_features,
    feature_cols=['activity_count', 'days_active', 'revenue'],
    n_clusters=4
)

print("\nBehavioral Cohort Profiles:")
print(cohort_profiles.round(2))

print("\nCohort Sizes:")
print(users_with_cohorts['behavior_cohort'].value_counts().sort_index())
```

### 7. Cohort Comparison Analysis

Compare cohorts to identify trends and changes.

```python
def analyze_cohort_trends(
    retention_table: pd.DataFrame,
    window_size: int = 3
) -> dict:
    """
    Analyze trends across cohorts.

    Parameters:
    -----------
    retention_table : Retention percentages by cohort
    window_size : Number of cohorts to average for trend

    Returns:
    --------
    dict with trend analysis
    """
    results = {
        'improving_retention': {},
        'declining_retention': {},
        'stable_cohorts': []
    }

    # Analyze each period
    for period in retention_table.columns[1:7]:  # First 6 months
        if period not in retention_table.columns:
            continue

        period_data = retention_table[period].dropna()

        if len(period_data) < window_size:
            continue

        # Calculate rolling average
        rolling_avg = period_data.rolling(window=window_size).mean()

        # Compare recent vs older cohorts
        recent_avg = rolling_avg.iloc[-window_size:].mean()
        older_avg = rolling_avg.iloc[:window_size].mean()

        change = recent_avg - older_avg
        pct_change = (change / older_avg * 100) if older_avg > 0 else 0

        period_name = f"Month {period}"

        if pct_change > 5:  # 5% improvement threshold
            results['improving_retention'][period_name] = {
                'change': change,
                'pct_change': pct_change,
                'recent_avg': recent_avg,
                'older_avg': older_avg
            }
        elif pct_change < -5:  # 5% decline threshold
            results['declining_retention'][period_name] = {
                'change': change,
                'pct_change': pct_change,
                'recent_avg': recent_avg,
                'older_avg': older_avg
            }

    return results

# Example: Analyze trends
trends = analyze_cohort_trends(retention_table, window_size=3)

print("\nRetention Trend Analysis:")
if trends['improving_retention']:
    print("\nImproving Retention Periods:")
    for period, data in trends['improving_retention'].items():
        print(f"  {period}: {data['pct_change']:.1f}% improvement "
              f"({data['older_avg']:.1f}% -> {data['recent_avg']:.1f}%)")

if trends['declining_retention']:
    print("\nDeclining Retention Periods:")
    for period, data in trends['declining_retention'].items():
        print(f"  {period}: {data['pct_change']:.1f}% decline "
              f"({data['older_avg']:.1f}% -> {data['recent_avg']:.1f}%)")
```

## Best Practices

### 1. Cohort Definition
- **Time-based cohorts**: Group by signup month/week for temporal analysis
- **Behavior-based cohorts**: Group by acquisition channel, first action, or feature usage
- **Attribute-based cohorts**: Group by demographics, plan type, or user segment
- **Ensure sufficient size**: Each cohort should have enough users for statistical significance

### 2. Analysis Period Selection
- **Match business cycle**: Weekly cohorts for fast-moving products, monthly for others
- **Consider product lifecycle**: How long until value is realized?
- **Account for seasonality**: Compare same periods year-over-year
- **Allow maturation**: Give cohorts enough time to show patterns

### 3. Retention Metrics
- **Day 1, Day 7, Day 30**: Common checkpoints for initial engagement
- **Month 1, 3, 6, 12**: Standard periods for subscription products
- **Define "retained"**: Active usage, login, or transaction?
- **Track both absolute and relative**: Number of users and percentage

### 4. Common Pitfalls to Avoid
- **Incomplete cohorts**: Don't compare immature cohorts to mature ones
- **Selection bias**: Early adopters may behave differently
- **Confounding factors**: Product changes affect different cohorts differently
- **Small sample sizes**: Particularly for recent or niche cohorts

### 5. Advanced Techniques
- **Cohort-based forecasting**: Predict future behavior from retention curves
- **Retention drivers**: Identify which actions correlate with better retention
- **Cohort triangulation**: Use multiple cohort definitions to validate findings
- **Micro-cohorts**: Create very specific cohorts to test hypotheses

## References

### Methodology
- Amplitude. "The Comprehensive Guide to Cohort Analysis"
- Mixpanel. "Retention Reports: Understand User Engagement"
- Lenny Rachitsky. "How to Measure and Improve Retention"

### Tools and Libraries
- **pandas**: DataFrame operations for cohort analysis
- **matplotlib/seaborn**: Visualization
- **lifelines**: Survival analysis for retention

### Industry Benchmarks
- Median D1 retention: 25-40% (mobile apps)
- Median M1 retention: 15-25% (SaaS)
- Good retention: >20% at Month 6 for consumer, >80% for B2B SaaS

### Additional Resources
- Reforge. "Retention & Engagement"
- Brian Balfour. "Why Product Market Fit Isn't Enough"
- Casey Winters. "Selecting the Right Retention Metric"

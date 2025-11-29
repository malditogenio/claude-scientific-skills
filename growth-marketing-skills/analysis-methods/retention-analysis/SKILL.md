---
name: retention-analysis
description: Analyze customer retention patterns and measure retention metrics. Calculate retention rates, survival curves, and churn cohorts. Build retention curves, identify retention drivers, optimize retention strategies, and measure the impact of retention initiatives on customer lifetime value.
---

# Retention Analysis

## Overview

Retention analysis measures how many customers continue using a product or service over time. Strong retention is the foundation of sustainable growth, as it's more cost-effective to retain existing customers than acquire new ones. This skill covers comprehensive retention measurement and optimization.

**Key Capabilities:**
- Retention rate calculation (classic, rolling, unbounded)
- Survival analysis and retention curves
- N-day and N-week retention metrics
- Retention cohort analysis
- Churn rate calculation and forecasting
- Retention driver identification
- Retention initiative impact measurement

## When to Use This Skill

Use this skill when:
- Measuring product stickiness and engagement
- Evaluating product-market fit
- Identifying when users typically churn
- Optimizing onboarding and engagement strategies
- Comparing retention across segments or cohorts
- Forecasting future active users
- Measuring impact of retention initiatives

## Core Capabilities

### 1. Classic Retention Calculation

Calculate standard retention metrics.

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_retention_rate(
    df: pd.DataFrame,
    user_col: str = 'user_id',
    date_col: str = 'activity_date',
    cohort_col: str = 'cohort_date',
    period: str = 'M',
    retention_type: str = 'classic'
) -> pd.DataFrame:
    """
    Calculate retention rate by cohort.

    Parameters:
    -----------
    df : DataFrame with user activity
    user_col : User identifier column
    date_col : Activity date column
    cohort_col : User cohort date column
    period : Time period ('D', 'W', 'M', 'Q')
    retention_type : 'classic', 'rolling', or 'unbounded'
        - classic: Active in specific period only
        - rolling: Active in period or any later period
        - unbounded: Active at any point after period start

    Returns:
    --------
    DataFrame with retention rates
    """
    # Ensure dates are datetime
    df[date_col] = pd.to_datetime(df[date_col])
    df[cohort_col] = pd.to_datetime(df[cohort_col])

    # Create period columns
    df['cohort_period'] = df[cohort_col].dt.to_period(period)
    df['activity_period'] = df[date_col].dt.to_period(period)

    # Calculate periods since cohort
    df['periods_since_cohort'] = (
        df['activity_period'] - df['cohort_period']
    ).apply(lambda x: x.n)

    if retention_type == 'classic':
        # Classic retention: active in specific period
        retention_data = df.groupby(
            ['cohort_period', 'periods_since_cohort']
        )[user_col].nunique().reset_index()

    elif retention_type == 'rolling':
        # Rolling retention: active in period N or later
        retention_data = []
        for cohort in df['cohort_period'].unique():
            cohort_users = df[df['cohort_period'] == cohort]

            for period_n in range(0, 24):  # Up to 24 periods
                # Users active in period N or later
                active_users = cohort_users[
                    cohort_users['periods_since_cohort'] >= period_n
                ][user_col].nunique()

                retention_data.append({
                    'cohort_period': cohort,
                    'periods_since_cohort': period_n,
                    user_col: active_users
                })

        retention_data = pd.DataFrame(retention_data)

    else:  # unbounded
        # Unbounded retention: ever active after period N
        retention_data = []
        for cohort in df['cohort_period'].unique():
            cohort_users = df[df['cohort_period'] == cohort]

            for period_n in range(0, 24):
                # Users who were active at period N or later
                active_users = cohort_users[
                    cohort_users['periods_since_cohort'] >= period_n
                ][user_col].nunique()

                retention_data.append({
                    'cohort_period': cohort,
                    'periods_since_cohort': period_n,
                    user_col: active_users
                })

        retention_data = pd.DataFrame(retention_data)

    # Pivot to create retention table
    retention_table = retention_data.pivot(
        index='cohort_period',
        columns='periods_since_cohort',
        values=user_col
    )

    # Calculate retention percentages
    cohort_sizes = retention_table.iloc[:, 0]
    retention_pct = retention_table.div(cohort_sizes, axis=0) * 100

    return retention_pct

# Example: Generate sample activity data
np.random.seed(42)

# Create user cohorts
n_users = 5000
users = []

for user_id in range(n_users):
    cohort_date = pd.Timestamp('2023-01-01') + pd.Timedelta(
        days=np.random.randint(0, 365)
    )

    users.append({
        'user_id': user_id,
        'cohort_date': cohort_date
    })

users_df = pd.DataFrame(users)

# Generate activity with retention decay
activities = []

for _, user in users_df.iterrows():
    current_date = user['cohort_date']
    end_date = pd.Timestamp('2024-06-01')

    month = 0
    while current_date <= end_date:
        # Retention rate decays over time
        retention_probability = 0.95 ** month  # 5% monthly churn

        if np.random.random() < retention_probability:
            # User is active this month
            # Generate 1-10 activities in the month
            n_activities = np.random.randint(1, 11)

            for _ in range(n_activities):
                activity_date = current_date + pd.Timedelta(
                    days=np.random.randint(0, 30)
                )

                if activity_date <= end_date:
                    activities.append({
                        'user_id': user['user_id'],
                        'activity_date': activity_date,
                        'cohort_date': user['cohort_date']
                    })

        current_date += pd.DateOffset(months=1)
        month += 1

activities_df = pd.DataFrame(activities)

# Calculate classic retention
classic_retention = calculate_retention_rate(
    activities_df,
    period='M',
    retention_type='classic'
)

print("Classic Retention Rates (%):")
print(classic_retention.iloc[:6, :12].round(1))  # First 6 cohorts, 12 months
```

### 2. N-Day Retention

Calculate day-specific retention metrics (D1, D7, D30).

```python
def calculate_n_day_retention(
    df: pd.DataFrame,
    user_col: str = 'user_id',
    date_col: str = 'activity_date',
    cohort_col: str = 'cohort_date',
    days: list = [1, 7, 14, 30, 60, 90]
) -> pd.DataFrame:
    """
    Calculate N-day retention rates.

    Parameters:
    -----------
    df : DataFrame with user activity
    user_col : User identifier column
    date_col : Activity date column
    cohort_col : User cohort date column
    days : List of days to calculate retention for

    Returns:
    --------
    DataFrame with N-day retention rates
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df[cohort_col] = pd.to_datetime(df[cohort_col])

    # Calculate days since cohort
    df['days_since_cohort'] = (df[date_col] - df[cohort_col]).dt.days

    retention_results = []

    # Get unique users and their cohort dates
    user_cohorts = df.groupby(user_col)[cohort_col].first()
    total_users = len(user_cohorts)

    for day_n in days:
        # Users active on day N (within ±1 day window for flexibility)
        active_on_day_n = df[
            (df['days_since_cohort'] >= day_n - 1) &
            (df['days_since_cohort'] <= day_n + 1)
        ][user_col].nunique()

        retention_rate = active_on_day_n / total_users * 100

        retention_results.append({
            'day': f'D{day_n}',
            'day_number': day_n,
            'active_users': active_on_day_n,
            'total_users': total_users,
            'retention_rate': retention_rate
        })

    return pd.DataFrame(retention_results)

# Example: Calculate N-day retention
n_day_retention = calculate_n_day_retention(
    activities_df,
    days=[1, 7, 14, 30, 60, 90, 180, 365]
)

print("\nN-Day Retention:")
print(n_day_retention.to_string(index=False))
```

### 3. Survival Analysis

Use survival curves to model retention over time.

```python
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

def perform_survival_analysis(
    df: pd.DataFrame,
    user_col: str = 'user_id',
    cohort_col: str = 'cohort_date',
    last_activity_col: str = 'last_activity_date',
    reference_date: pd.Timestamp = None
) -> tuple:
    """
    Perform survival analysis on customer retention.

    Parameters:
    -----------
    df : DataFrame with user cohort and activity data
    user_col : User identifier column
    cohort_col : User cohort date column
    last_activity_col : Last activity date column
    reference_date : Reference date for censoring

    Returns:
    --------
    tuple: (KaplanMeierFitter, survival data DataFrame)
    """
    if reference_date is None:
        reference_date = pd.Timestamp.now()

    # Calculate survival time (days from cohort to last activity or censoring)
    df = df.copy()
    df[cohort_col] = pd.to_datetime(df[cohort_col])
    df[last_activity_col] = pd.to_datetime(df[last_activity_col])

    df['survival_time'] = (df[last_activity_col] - df[cohort_col]).dt.days

    # Event indicator (1 if churned, 0 if censored/still active)
    # User is censored if last activity is very recent
    df['churned'] = (
        (reference_date - df[last_activity_col]).dt.days > 30
    ).astype(int)

    # Fit Kaplan-Meier survival curve
    kmf = KaplanMeierFitter()
    kmf.fit(
        durations=df['survival_time'],
        event_observed=df['churned'],
        label='Overall Retention'
    )

    return kmf, df

def plot_survival_curve(
    kmf: KaplanMeierFitter,
    title: str = "Customer Survival Curve"
) -> plt.Figure:
    """
    Plot Kaplan-Meier survival curve.
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    kmf.plot_survival_function(ax=ax, linewidth=2)

    ax.set_xlabel('Days Since Cohort Start', fontsize=12)
    ax.set_ylabel('Survival Probability (Retention Rate)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.05)

    # Add reference lines
    for retention_level in [0.75, 0.50, 0.25]:
        ax.axhline(
            retention_level,
            color='red',
            linestyle='--',
            alpha=0.3,
            linewidth=1
        )

    plt.tight_layout()
    return fig

# Example: Perform survival analysis
# Prepare data with last activity
user_last_activity = activities_df.groupby('user_id').agg({
    'activity_date': 'max',
    'cohort_date': 'first'
}).reset_index()

user_last_activity.columns = ['user_id', 'last_activity_date', 'cohort_date']

kmf_model, survival_data = perform_survival_analysis(
    user_last_activity,
    reference_date=pd.Timestamp('2024-06-01')
)

print("\nSurvival Analysis Summary:")
print(f"Median Survival Time: {kmf_model.median_survival_time_:.0f} days")
print(f"Retention at Day 30: {kmf_model.survival_function_at_times(30).values[0]:.1%}")
print(f"Retention at Day 90: {kmf_model.survival_function_at_times(90).values[0]:.1%}")
print(f"Retention at Day 180: {kmf_model.survival_function_at_times(180).values[0]:.1%}")

# Plot survival curve
fig = plot_survival_curve(kmf_model)
plt.savefig('survival_curve.png', dpi=300, bbox_inches='tight')
print("\nSurvival curve saved to: survival_curve.png")
```

### 4. Retention Curve Analysis

Analyze and visualize retention curves.

```python
def analyze_retention_curves(
    retention_table: pd.DataFrame,
    key_periods: list = [1, 3, 6, 12]
) -> dict:
    """
    Analyze retention curve characteristics.

    Parameters:
    -----------
    retention_table : Retention table from calculate_retention_rate
    key_periods : Key periods to analyze

    Returns:
    --------
    dict with retention metrics
    """
    metrics = {}

    # Overall retention at key periods
    for period in key_periods:
        if period in retention_table.columns:
            avg_retention = retention_table[period].mean()
            metrics[f'avg_retention_m{period}'] = avg_retention

    # Retention curve shape (decay rate)
    # Calculate average decline per period
    first_period_retention = retention_table.iloc[:, 0].mean()
    last_period_retention = retention_table.iloc[:, -1].mean()

    n_periods = len(retention_table.columns)
    avg_decline_per_period = (first_period_retention - last_period_retention) / n_periods

    metrics['avg_decline_per_period'] = avg_decline_per_period

    # Calculate "flattening" - when retention stabilizes
    # Find when month-over-month decline drops below 2%
    retention_changes = retention_table.diff(axis=1)
    avg_changes = retention_changes.mean()

    flattening_period = None
    for i, change in enumerate(avg_changes[1:], 1):
        if abs(change) < 2:  # Less than 2% change
            flattening_period = i
            break

    metrics['flattening_period'] = flattening_period

    return metrics

# Example: Analyze retention curves
retention_metrics = analyze_retention_curves(classic_retention)

print("\nRetention Curve Analysis:")
for metric, value in retention_metrics.items():
    if 'avg_retention' in metric:
        print(f"{metric}: {value:.1f}%")
    elif 'decline' in metric:
        print(f"{metric}: {value:.2f}%")
    else:
        print(f"{metric}: {value}")
```

### 5. Retention Driver Analysis

Identify factors that influence retention.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

def analyze_retention_drivers(
    user_features_df: pd.DataFrame,
    feature_cols: list,
    retention_col: str = 'retained',
    retention_period_days: int = 30
) -> pd.DataFrame:
    """
    Identify features that drive retention.

    Parameters:
    -----------
    user_features_df : DataFrame with user features and retention status
    feature_cols : List of feature columns
    retention_col : Column indicating if user was retained
    retention_period_days : Days used to define retention

    Returns:
    --------
    DataFrame with feature importance
    """
    # Prepare data
    X = user_features_df[feature_cols].values
    y = user_features_df[retention_col].values

    # Handle missing values
    X = np.nan_to_num(X)

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train random forest
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

    rf_model.fit(X_scaled, y)

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)

    # Calculate correlation with retention
    correlations = []
    for feature in feature_cols:
        corr = user_features_df[[feature, retention_col]].corr().iloc[0, 1]
        correlations.append(corr)

    feature_importance['correlation'] = correlations

    print(f"\nRetention Drivers (Day {retention_period_days}):")
    print(feature_importance.head(10).to_string(index=False))

    return feature_importance, rf_model

# Example: Create user features and analyze drivers
# Create feature set
user_features = activities_df.groupby('user_id').agg({
    'activity_date': ['count', 'min', 'max'],
    'cohort_date': 'first'
}).reset_index()

user_features.columns = [
    'user_id', 'activity_count', 'first_activity', 'last_activity', 'cohort_date'
]

# Calculate features
user_features['days_active'] = (
    user_features['last_activity'] - user_features['first_activity']
).dt.days

user_features['days_since_signup'] = (
    user_features['last_activity'] - user_features['cohort_date']
).dt.days

user_features['avg_activities_per_day'] = (
    user_features['activity_count'] / (user_features['days_active'] + 1)
)

# Define retention (active in last 30 days)
reference_date = pd.Timestamp('2024-06-01')
user_features['days_since_last_activity'] = (
    reference_date - user_features['last_activity']
).dt.days

user_features['retained_30d'] = (
    user_features['days_since_last_activity'] <= 30
).astype(int)

# Analyze drivers
feature_cols = ['activity_count', 'days_active', 'avg_activities_per_day', 'days_since_signup']

retention_drivers, driver_model = analyze_retention_drivers(
    user_features,
    feature_cols=feature_cols,
    retention_col='retained_30d'
)
```

### 6. Retention by Segment

Compare retention across different user segments.

```python
def compare_retention_by_segment(
    df: pd.DataFrame,
    segment_col: str,
    user_col: str = 'user_id',
    date_col: str = 'activity_date',
    cohort_col: str = 'cohort_date',
    period: str = 'M'
) -> dict:
    """
    Compare retention rates across segments.

    Parameters:
    -----------
    df : DataFrame with activity and segment data
    segment_col : Column with segment labels
    Other parameters same as calculate_retention_rate

    Returns:
    --------
    dict with retention tables for each segment
    """
    segments = {}

    for segment in df[segment_col].unique():
        segment_df = df[df[segment_col] == segment]

        retention_table = calculate_retention_rate(
            segment_df,
            user_col=user_col,
            date_col=date_col,
            cohort_col=cohort_col,
            period=period
        )

        segments[segment] = retention_table

    return segments

# Example: Compare retention by segment
# Add random segments to activity data
np.random.seed(42)
user_segments = {
    user_id: np.random.choice(['Premium', 'Free', 'Trial'])
    for user_id in activities_df['user_id'].unique()
}

activities_df['segment'] = activities_df['user_id'].map(user_segments)

# Compare retention
segment_retention = compare_retention_by_segment(
    activities_df,
    segment_col='segment'
)

print("\n\nRetention by Segment (Month 1, 3, 6):")
for segment, retention_table in segment_retention.items():
    print(f"\n{segment}:")
    months_to_show = [1, 3, 6]
    avg_retention = {
        f"M{m}": retention_table[m].mean()
        for m in months_to_show
        if m in retention_table.columns
    }
    print(f"  {avg_retention}")
```

## Best Practices

### 1. Retention Metrics Selection
- **Classic retention**: Best for understanding period-specific engagement
- **Rolling retention**: Better for products with irregular usage patterns
- **N-day retention**: Standard for mobile apps and games
- **Survival analysis**: For understanding customer lifetime

### 2. Time Windows
- **Consumer products**: D1, D7, D30 retention
- **SaaS**: M1, M3, M6, M12 retention
- **Enterprise**: Q1, Q2, Q4 retention
- **Match to usage cycle**: Align periods with natural product usage

### 3. Cohort Selection
- **Acquisition cohorts**: When users signed up
- **Feature cohorts**: When users adopted a feature
- **Behavior cohorts**: Based on actions taken
- **Geographic/demographic**: For segmented analysis

### 4. Common Pitfalls to Avoid
- **Incomplete cohorts**: Don't compare immature cohorts
- **Survivor bias**: Include all users, not just active ones
- **Irregular usage**: Some products aren't used daily/weekly
- **Definition changes**: Keep retention definition consistent

### 5. Improvement Strategies
- **Onboarding optimization**: First-week experience is critical
- **Activation improvements**: Get users to "aha moment" faster
- **Engagement loops**: Build habits through notifications, emails
- **Value delivery**: Continuously demonstrate product value

## References

### Methodology
- Amplitude. "The Complete Guide to Retention Analysis"
- Lenny Rachitsky. "How to Measure and Improve Retention"
- Brian Balfour. "Retention Has Three Faces"

### Tools and Libraries
- **pandas**: Data manipulation
- **lifelines**: Survival analysis
- **matplotlib/seaborn**: Visualization

### Industry Benchmarks
- **Mobile Apps D1**: 25-40% (games), 35-60% (utilities)
- **SaaS M1**: 40-60%, M6: 30-50%
- **E-commerce**: 20-30% annual retention
- **Social Networks**: D1: 40-50%, D30: 20-30%

### Additional Resources
- Mixpanel. "Retention Analysis: The Complete Guide"
- Reforge. "Retention + Engagement Deep Dive"
- Casey Winters. "Unpacking Retention"

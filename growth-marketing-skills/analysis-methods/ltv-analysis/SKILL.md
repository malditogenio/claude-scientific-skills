---
name: ltv-analysis
description: Calculate and predict customer lifetime value (LTV/CLV) using historical, cohort-based, and predictive approaches. Implement simple average, cohort, and probabilistic LTV models. Segment customers by value, optimize LTV:CAC ratios, and forecast future customer value for growth strategy and marketing ROI optimization.
---

# Lifetime Value (LTV) Analysis

## Overview

Customer Lifetime Value (LTV or CLV) represents the total revenue a business can expect from a single customer over their entire relationship. LTV analysis is crucial for determining how much to spend on customer acquisition, retention strategies, and overall business unit economics.

**Key Capabilities:**
- Historical LTV calculation
- Cohort-based LTV analysis
- Predictive LTV modeling
- LTV segmentation
- LTV:CAC ratio analysis
- Probabilistic models (BG/NBD, Pareto/NBD)
- LTV forecasting and sensitivity analysis

## When to Use This Skill

Use this skill when:
- Determining customer acquisition budgets
- Evaluating marketing channel ROI
- Identifying high-value customer segments
- Optimizing pricing and product strategy
- Making retention investment decisions
- Forecasting revenue from customer base
- Calculating business valuation metrics

## Core Capabilities

### 1. Historical LTV Calculation

Calculate realized LTV from historical customer data.

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_historical_ltv(
    transactions_df: pd.DataFrame,
    customer_col: str = 'customer_id',
    date_col: str = 'transaction_date',
    revenue_col: str = 'revenue',
    cohort_col: str = 'cohort_date'
) -> pd.DataFrame:
    """
    Calculate historical LTV for customers.

    Parameters:
    -----------
    transactions_df : DataFrame with transaction history
    customer_col : Customer identifier column
    date_col : Transaction date column
    revenue_col : Revenue column
    cohort_col : Customer cohort/signup date column

    Returns:
    --------
    DataFrame with customer LTV metrics
    """
    # Ensure dates are datetime
    transactions_df[date_col] = pd.to_datetime(transactions_df[date_col])
    transactions_df[cohort_col] = pd.to_datetime(transactions_df[cohort_col])

    # Calculate customer-level metrics
    customer_ltv = transactions_df.groupby(customer_col).agg({
        revenue_col: ['sum', 'mean', 'count'],
        date_col: ['min', 'max'],
        cohort_col: 'first'
    })

    customer_ltv.columns = [
        'total_revenue', 'avg_transaction_value', 'transaction_count',
        'first_purchase', 'last_purchase', 'cohort_date'
    ]

    # Calculate customer lifetime (days)
    customer_ltv['customer_lifetime_days'] = (
        customer_ltv['last_purchase'] - customer_ltv['first_purchase']
    ).dt.days

    # Calculate age (days since first purchase)
    reference_date = transactions_df[date_col].max()
    customer_ltv['customer_age_days'] = (
        reference_date - customer_ltv['first_purchase']
    ).dt.days

    # LTV = total revenue (for historical calculation)
    customer_ltv['historical_ltv'] = customer_ltv['total_revenue']

    # Average revenue per day (while active)
    customer_ltv['revenue_per_day'] = (
        customer_ltv['total_revenue'] /
        (customer_ltv['customer_lifetime_days'] + 1)  # +1 to avoid division by zero
    )

    return customer_ltv.reset_index()

# Example: Generate sample customer transaction data
np.random.seed(42)

# Generate cohorts and transactions
n_customers = 1000
transactions = []

for customer_id in range(n_customers):
    # Cohort date (when customer signed up)
    cohort_date = pd.Timestamp('2023-01-01') + pd.Timedelta(
        days=np.random.randint(0, 365)
    )

    # Customer lifetime (some customers are more valuable)
    customer_type = np.random.choice(['high_value', 'medium_value', 'low_value'],
                                    p=[0.2, 0.5, 0.3])

    if customer_type == 'high_value':
        n_transactions = np.random.randint(15, 50)
        avg_value = 150
        lifetime_months = np.random.randint(12, 24)
    elif customer_type == 'medium_value':
        n_transactions = np.random.randint(5, 20)
        avg_value = 75
        lifetime_months = np.random.randint(6, 18)
    else:  # low_value
        n_transactions = np.random.randint(1, 8)
        avg_value = 40
        lifetime_months = np.random.randint(1, 12)

    # Generate transactions over the customer lifetime
    for i in range(n_transactions):
        trans_date = cohort_date + pd.Timedelta(
            days=np.random.randint(0, lifetime_months * 30)
        )

        # Make sure transaction is before today
        if trans_date <= pd.Timestamp('2024-06-01'):
            revenue = np.random.gamma(2, avg_value / 2)

            transactions.append({
                'customer_id': customer_id,
                'transaction_date': trans_date,
                'revenue': revenue,
                'cohort_date': cohort_date
            })

transactions_df = pd.DataFrame(transactions)

# Calculate historical LTV
historical_ltv = calculate_historical_ltv(transactions_df)

print("Historical LTV Summary:")
print(historical_ltv[['customer_id', 'total_revenue', 'transaction_count',
                      'customer_lifetime_days', 'historical_ltv']].describe())

print(f"\nAverage LTV: ${historical_ltv['historical_ltv'].mean():.2f}")
print(f"Median LTV: ${historical_ltv['historical_ltv'].median():.2f}")
```

### 2. Cohort-Based LTV

Calculate average LTV by cohort over time.

```python
def calculate_cohort_ltv(
    transactions_df: pd.DataFrame,
    customer_col: str = 'customer_id',
    date_col: str = 'transaction_date',
    revenue_col: str = 'revenue',
    cohort_col: str = 'cohort_date',
    period: str = 'M'  # 'M' for month, 'Q' for quarter
) -> pd.DataFrame:
    """
    Calculate cumulative LTV by cohort over time.

    Parameters:
    -----------
    transactions_df : DataFrame with transactions
    customer_col, date_col, revenue_col, cohort_col : Column names
    period : Time period for cohort grouping ('M', 'Q', 'Y')

    Returns:
    --------
    DataFrame with cumulative LTV by cohort and period
    """
    df = transactions_df.copy()

    # Ensure dates are datetime
    df[date_col] = pd.to_datetime(df[date_col])
    df[cohort_col] = pd.to_datetime(df[cohort_col])

    # Create period columns
    df['cohort_period'] = df[cohort_col].dt.to_period(period)
    df['transaction_period'] = df[date_col].dt.to_period(period)

    # Calculate periods since cohort
    df['periods_since_cohort'] = (
        df['transaction_period'] - df['cohort_period']
    ).apply(lambda x: x.n)

    # Group by cohort and period
    cohort_data = df.groupby(['cohort_period', 'periods_since_cohort']).agg({
        revenue_col: 'sum',
        customer_col: 'nunique'
    }).reset_index()

    cohort_data.columns = [
        'cohort_period', 'periods_since_cohort', 'revenue', 'customers'
    ]

    # Get cohort sizes
    cohort_sizes = df.groupby('cohort_period')[customer_col].nunique()

    # Calculate LTV per customer
    cohort_data['ltv_per_customer'] = (
        cohort_data['revenue'] / cohort_data['customers']
    )

    # Pivot to create cohort table
    cohort_ltv = cohort_data.pivot(
        index='cohort_period',
        columns='periods_since_cohort',
        values='ltv_per_customer'
    )

    # Calculate cumulative LTV
    cumulative_ltv = cohort_ltv.cumsum(axis=1)

    return cumulative_ltv

# Example: Calculate cohort LTV
cohort_ltv = calculate_cohort_ltv(
    transactions_df,
    period='M'
)

print("\nCohort LTV (Cumulative $ per Customer):")
print(cohort_ltv.iloc[:10, :12].round(2))  # First 10 cohorts, first 12 months
```

### 3. Predictive LTV - Simple Model

Predict future LTV based on early behavior.

```python
def predict_ltv_simple(
    customer_features: pd.DataFrame,
    early_period_months: int = 3
) -> pd.DataFrame:
    """
    Predict LTV based on early customer behavior.

    Uses revenue in first N months to predict lifetime value.

    Parameters:
    -----------
    customer_features : DataFrame with customer metrics
    early_period_months : Months of data to use for prediction

    Returns:
    --------
    DataFrame with predicted LTV
    """
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, r2_score

    # Filter to customers with enough history
    mature_customers = customer_features[
        customer_features['customer_age_days'] >= early_period_months * 30 * 2
    ].copy()

    # Calculate early revenue (first N months)
    # This would require transaction-level data; simplified here
    # Assume we have 'revenue_first_3m' feature

    # For simulation, create proxy features
    mature_customers['revenue_first_3m'] = (
        mature_customers['total_revenue'] *
        np.random.uniform(0.2, 0.4, len(mature_customers))
    )

    mature_customers['transactions_first_3m'] = (
        mature_customers['transaction_count'] *
        np.random.uniform(0.2, 0.5, len(mature_customers))
    )

    # Features for prediction
    feature_cols = ['revenue_first_3m', 'transactions_first_3m']
    target_col = 'historical_ltv'

    X = mature_customers[feature_cols].values
    y = mature_customers[target_col].values

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Evaluate
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\nPredictive LTV Model Performance:")
    print(f"Mean Absolute Error: ${mae:.2f}")
    print(f"R² Score: {r2:.3f}")

    # Feature importance
    importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\nFeature Importance:")
    print(importance)

    # Add predictions to dataframe
    mature_customers['predicted_ltv'] = model.predict(
        mature_customers[feature_cols].values
    )

    return mature_customers, model

# Example: Predict LTV
ltv_predictions, ltv_model = predict_ltv_simple(historical_ltv)

print("\nLTV Predictions Sample:")
print(ltv_predictions[['customer_id', 'historical_ltv', 'predicted_ltv']].head(10))
```

### 4. LTV:CAC Ratio Analysis

Calculate the ratio of lifetime value to customer acquisition cost.

```python
def calculate_ltv_cac_ratio(
    ltv_df: pd.DataFrame,
    cac_df: pd.DataFrame,
    ltv_col: str = 'historical_ltv',
    cac_col: str = 'cac',
    cohort_col: str = 'cohort_period'
) -> pd.DataFrame:
    """
    Calculate LTV:CAC ratio by cohort or channel.

    Parameters:
    -----------
    ltv_df : DataFrame with customer LTV
    cac_df : DataFrame with customer acquisition cost
    ltv_col : LTV column name
    cac_col : CAC column name
    cohort_col : Cohort identifier column

    Returns:
    --------
    DataFrame with LTV:CAC analysis
    """
    # Merge LTV and CAC data
    analysis = ltv_df.merge(cac_df, on='customer_id', how='inner')

    # Calculate ratio
    analysis['ltv_cac_ratio'] = analysis[ltv_col] / analysis[cac_col]

    # Payback period (months to recover CAC)
    # Simplified: assumes even revenue distribution
    analysis['payback_months'] = (
        analysis[cac_col] / (analysis[ltv_col] / analysis['customer_lifetime_days'] * 30)
    )

    # Summary by cohort
    cohort_summary = analysis.groupby(cohort_col).agg({
        ltv_col: 'mean',
        cac_col: 'mean',
        'ltv_cac_ratio': 'mean',
        'payback_months': 'mean',
        'customer_id': 'count'
    }).reset_index()

    cohort_summary.columns = [
        cohort_col, 'avg_ltv', 'avg_cac', 'ltv_cac_ratio',
        'payback_months', 'customers'
    ]

    return analysis, cohort_summary

# Example: Generate CAC data and calculate ratio
np.random.seed(42)

# Simulate CAC by channel
cac_data = []
for customer_id in historical_ltv['customer_id']:
    channel = np.random.choice(
        ['Paid Search', 'Social', 'Organic', 'Referral'],
        p=[0.3, 0.3, 0.2, 0.2]
    )

    # Different CAC by channel
    if channel == 'Paid Search':
        cac = np.random.normal(80, 20)
    elif channel == 'Social':
        cac = np.random.normal(60, 15)
    elif channel == 'Organic':
        cac = np.random.normal(20, 5)
    else:  # Referral
        cac = np.random.normal(15, 5)

    cac_data.append({
        'customer_id': customer_id,
        'channel': channel,
        'cac': max(5, cac)  # Ensure positive CAC
    })

cac_df = pd.DataFrame(cac_data)

# Add cohort period to historical_ltv
historical_ltv['cohort_period'] = pd.to_datetime(
    historical_ltv['cohort_date']
).dt.to_period('M')

# Calculate LTV:CAC
ltv_cac_analysis, cohort_ltv_cac = calculate_ltv_cac_ratio(
    historical_ltv,
    cac_df,
    cohort_col='cohort_period'
)

print("\nLTV:CAC Ratio by Cohort (Recent 6 months):")
print(cohort_ltv_cac.tail(6).to_string(index=False))

# By channel
channel_ltv_cac = ltv_cac_analysis.groupby('channel').agg({
    'historical_ltv': 'mean',
    'cac': 'mean',
    'ltv_cac_ratio': 'mean',
    'payback_months': 'mean'
}).round(2)

print("\nLTV:CAC by Channel:")
print(channel_ltv_cac)
```

### 5. Probabilistic LTV Models

Implement advanced probabilistic models for LTV prediction.

```python
def calculate_contractual_ltv(
    avg_revenue_per_period: float,
    churn_rate_per_period: float,
    discount_rate: float = 0.01,
    periods: int = 60
) -> dict:
    """
    Calculate LTV for contractual business (subscriptions).

    Uses geometric series formula for LTV with churn.

    Parameters:
    -----------
    avg_revenue_per_period : Average revenue per customer per period
    churn_rate_per_period : Churn rate (e.g., 0.05 for 5% monthly churn)
    discount_rate : Discount rate per period (e.g., 0.01 for 1% monthly)
    periods : Number of periods to calculate

    Returns:
    --------
    dict with LTV metrics
    """
    # Retention rate
    retention_rate = 1 - churn_rate_per_period

    # Simple LTV formula (no discounting)
    simple_ltv = avg_revenue_per_period / churn_rate_per_period

    # Discounted LTV (with time value of money)
    # LTV = ARPU * [retention / (1 + discount - retention)]
    discounted_ltv = avg_revenue_per_period * (
        retention_rate / (1 + discount_rate - retention_rate)
    )

    # Calculate period-by-period
    period_values = []
    cumulative_ltv = 0

    for period in range(1, periods + 1):
        # Probability customer is still active
        survival_prob = retention_rate ** period

        # Discounted value
        period_value = (
            avg_revenue_per_period *
            survival_prob /
            ((1 + discount_rate) ** period)
        )

        cumulative_ltv += period_value

        period_values.append({
            'period': period,
            'survival_probability': survival_prob,
            'period_value': period_value,
            'cumulative_ltv': cumulative_ltv
        })

    return {
        'simple_ltv': simple_ltv,
        'discounted_ltv': discounted_ltv,
        'avg_customer_lifetime_periods': 1 / churn_rate_per_period,
        'period_details': pd.DataFrame(period_values)
    }

# Example: Calculate contractual LTV
contractual_ltv = calculate_contractual_ltv(
    avg_revenue_per_period=50,  # $50/month
    churn_rate_per_period=0.05,  # 5% monthly churn
    discount_rate=0.01,  # 1% monthly discount rate
    periods=60
)

print("\nContractual LTV Analysis:")
print(f"Simple LTV: ${contractual_ltv['simple_ltv']:.2f}")
print(f"Discounted LTV: ${contractual_ltv['discounted_ltv']:.2f}")
print(f"Average Customer Lifetime: {contractual_ltv['avg_customer_lifetime_periods']:.1f} periods")

print("\nLTV Accumulation Over Time:")
print(contractual_ltv['period_details'].iloc[::6].to_string(index=False))  # Every 6 months
```

### 6. LTV Segmentation

Segment customers by lifetime value.

```python
import matplotlib.pyplot as plt
import seaborn as sns

def segment_by_ltv(
    ltv_df: pd.DataFrame,
    ltv_col: str = 'historical_ltv',
    n_segments: int = 4,
    method: str = 'quantile'
) -> pd.DataFrame:
    """
    Segment customers by LTV.

    Parameters:
    -----------
    ltv_df : DataFrame with customer LTV
    ltv_col : LTV column name
    n_segments : Number of segments to create
    method : 'quantile' or 'kmeans'

    Returns:
    --------
    DataFrame with LTV segments
    """
    df = ltv_df.copy()

    if method == 'quantile':
        # Segment by quantiles
        df['ltv_segment'] = pd.qcut(
            df[ltv_col],
            q=n_segments,
            labels=[f'Tier {i+1}' for i in range(n_segments)]
        )

    else:  # kmeans
        from sklearn.cluster import KMeans

        X = df[[ltv_col]].values
        kmeans = KMeans(n_clusters=n_segments, random_state=42)
        df['ltv_segment'] = kmeans.fit_predict(X)

        # Rename clusters by average LTV
        segment_means = df.groupby('ltv_segment')[ltv_col].mean().sort_values()
        segment_map = {
            old: f'Tier {i+1}'
            for i, old in enumerate(segment_means.index)
        }
        df['ltv_segment'] = df['ltv_segment'].map(segment_map)

    # Segment profiles
    segment_profiles = df.groupby('ltv_segment').agg({
        'customer_id': 'count',
        ltv_col: ['mean', 'median', 'sum'],
        'transaction_count': 'mean',
        'customer_lifetime_days': 'mean'
    }).round(2)

    print("\nLTV Segment Profiles:")
    print(segment_profiles)

    return df, segment_profiles

# Example: Segment customers by LTV
ltv_segmented, segment_profiles = segment_by_ltv(
    historical_ltv,
    ltv_col='historical_ltv',
    n_segments=4,
    method='quantile'
)

# Visualize LTV distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histogram
axes[0].hist(historical_ltv['historical_ltv'], bins=50, edgecolor='black', alpha=0.7)
axes[0].axvline(
    historical_ltv['historical_ltv'].mean(),
    color='red',
    linestyle='--',
    linewidth=2,
    label='Mean'
)
axes[0].axvline(
    historical_ltv['historical_ltv'].median(),
    color='green',
    linestyle='--',
    linewidth=2,
    label='Median'
)
axes[0].set_xlabel('LTV ($)', fontsize=12)
axes[0].set_ylabel('Number of Customers', fontsize=12)
axes[0].set_title('LTV Distribution', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Box plot by segment
ltv_segmented.boxplot(
    column='historical_ltv',
    by='ltv_segment',
    ax=axes[1]
)
axes[1].set_xlabel('LTV Segment', fontsize=12)
axes[1].set_ylabel('LTV ($)', fontsize=12)
axes[1].set_title('LTV by Segment', fontsize=14, fontweight='bold')
plt.suptitle('')  # Remove default title

plt.tight_layout()
plt.savefig('ltv_distribution.png', dpi=300, bbox_inches='tight')
print("\nLTV distribution saved to: ltv_distribution.png")
```

## Best Practices

### 1. LTV Calculation Methods
- **Historical**: For mature businesses with stable cohorts
- **Predictive**: For younger businesses or forward planning
- **Contractual vs. Non-contractual**: Different formulas needed
- **Include all revenue**: Subscriptions, upsells, cross-sells

### 2. Time Horizons
- **Short-term LTV**: 12-24 months for planning
- **Long-term LTV**: 3-5 years for valuation
- **Infinite horizon**: For stable subscription businesses
- **Cohort maturity**: Wait for cohorts to mature before finalizing

### 3. Discounting
- **Always discount**: Money today > money tomorrow
- **Use appropriate rate**: WACC or opportunity cost
- **Sensitivity analysis**: Test different discount rates
- **Compare to industry**: Benchmark against similar businesses

### 4. Common Pitfalls to Avoid
- **Survivorship bias**: Include churned customers in calculations
- **Ignoring costs**: LTV should be gross margin, not just revenue
- **Assuming linearity**: Customer value may accelerate or decelerate
- **Over-optimism**: Be conservative with retention assumptions

### 5. Using LTV for Decisions
- **LTV:CAC ratio > 3**: Healthy unit economics
- **Payback < 12 months**: Good for most businesses
- **Segment-specific**: Different LTV by channel, product, segment
- **Dynamic**: Update regularly as business evolves

## References

### Methodology
- Fader, P. S., & Hardie, B. G. (2009). "Probability Models for Customer-Base Analysis"
- Gupta, S., et al. (2006). "Modeling Customer Lifetime Value"
- Berger, P. D., & Nasr, N. I. (1998). "Customer Lifetime Value: Marketing Models and Applications"

### Tools and Libraries
- **pandas**: Data manipulation
- **sklearn**: Predictive modeling
- **lifetimes**: Python library for probabilistic CLV models

### Industry Benchmarks
- **SaaS**: LTV:CAC of 3-5x, payback < 12 months
- **E-commerce**: LTV:CAC of 3x, payback < 6 months
- **Subscription**: Average lifetime 18-36 months
- **B2B**: LTV typically $10K-$1M+

### Additional Resources
- [Lifetimes Library Documentation](https://github.com/CamDavidsonPilon/lifetimes)
- ProfitWell. "The Complete Guide to SaaS LTV"
- Shopify. "How to Calculate Customer Lifetime Value"
- David Skok. "SaaS Metrics 2.0"

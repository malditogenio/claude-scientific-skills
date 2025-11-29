---
name: cac-optimization
description: Calculate and optimize Customer Acquisition Cost (CAC) across marketing channels. Analyze CAC trends, payback periods, and channel efficiency. Optimize marketing spend allocation, identify high-ROI channels, and improve unit economics through data-driven CAC reduction strategies.
---

# CAC Optimization

## Overview

Customer Acquisition Cost (CAC) represents the total cost of acquiring a new customer, including marketing and sales expenses. Optimizing CAC is essential for profitable growth, as it directly impacts unit economics, marketing ROI, and business sustainability.

**Key Capabilities:**
- CAC calculation by channel, campaign, and cohort
- Payback period analysis
- Channel efficiency comparison
- Marketing mix optimization
- CAC trend analysis
- Blended vs. organic CAC
- Budget allocation optimization

## When to Use This Skill

Use this skill when:
- Optimizing marketing budget allocation
- Evaluating channel performance and ROI
- Identifying cost-effective acquisition strategies
- Planning growth budgets
- Improving unit economics (LTV:CAC ratio)
- Comparing acquisition efficiency across time periods
- Making strategic decisions about scaling channels

## Core Capabilities

### 1. Basic CAC Calculation

Calculate customer acquisition cost overall and by channel.

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_cac(
    marketing_spend_df: pd.DataFrame,
    customers_acquired_df: pd.DataFrame,
    spend_col: str = 'spend',
    customers_col: str = 'customers_acquired',
    date_col: str = 'date',
    channel_col: str = 'channel',
    period: str = 'M'
) -> pd.DataFrame:
    """
    Calculate Customer Acquisition Cost (CAC).

    Parameters:
    -----------
    marketing_spend_df : DataFrame with marketing spend by channel and period
    customers_acquired_df : DataFrame with customers acquired
    spend_col : Marketing spend column
    customers_col : Customers acquired column
    date_col : Date column
    channel_col : Channel column
    period : Time period for aggregation ('D', 'W', 'M', 'Q')

    Returns:
    --------
    DataFrame with CAC metrics
    """
    # Ensure dates are datetime
    marketing_spend_df[date_col] = pd.to_datetime(marketing_spend_df[date_col])
    customers_acquired_df[date_col] = pd.to_datetime(customers_acquired_df[date_col])

    # Create period columns
    marketing_spend_df['period'] = marketing_spend_df[date_col].dt.to_period(period)
    customers_acquired_df['period'] = customers_acquired_df[date_col].dt.to_period(period)

    # Aggregate spend
    spend_agg = marketing_spend_df.groupby(['period', channel_col])[spend_col].sum().reset_index()

    # Aggregate customers
    customers_agg = customers_acquired_df.groupby(
        ['period', channel_col]
    )[customers_col].sum().reset_index()

    # Merge and calculate CAC
    cac_df = spend_agg.merge(
        customers_agg,
        on=['period', channel_col],
        how='outer'
    ).fillna(0)

    cac_df['cac'] = cac_df[spend_col] / cac_df[customers_col]
    cac_df['cac'] = cac_df['cac'].replace([np.inf, -np.inf], np.nan)

    return cac_df

# Example: Generate sample marketing data
np.random.seed(42)

# Generate marketing spend data
channels = ['Paid Search', 'Social Media', 'Display', 'Content', 'Email', 'Referral']
dates = pd.date_range('2023-01-01', '2024-06-01', freq='D')

marketing_spend = []
for date in dates:
    for channel in channels:
        # Different spend levels by channel
        if channel == 'Paid Search':
            daily_spend = np.random.normal(2000, 300)
        elif channel == 'Social Media':
            daily_spend = np.random.normal(1500, 250)
        elif channel == 'Display':
            daily_spend = np.random.normal(1000, 200)
        elif channel == 'Content':
            daily_spend = np.random.normal(500, 100)
        elif channel == 'Email':
            daily_spend = np.random.normal(200, 50)
        else:  # Referral
            daily_spend = np.random.normal(100, 30)

        marketing_spend.append({
            'date': date,
            'channel': channel,
            'spend': max(0, daily_spend)
        })

marketing_spend_df = pd.DataFrame(marketing_spend)

# Generate customers acquired (with different conversion efficiencies)
customers_acquired = []
for _, row in marketing_spend_df.iterrows():
    # Conversion efficiency varies by channel
    if row['channel'] == 'Paid Search':
        conversion_rate = 0.025  # 2.5% of spend converts to customer
    elif row['channel'] == 'Social Media':
        conversion_rate = 0.02
    elif row['channel'] == 'Display':
        conversion_rate = 0.015
    elif row['channel'] == 'Content':
        conversion_rate = 0.04  # More efficient
    elif row['channel'] == 'Email':
        conversion_rate = 0.05  # Very efficient
    else:  # Referral
        conversion_rate = 0.08  # Most efficient

    # Customers acquired (with some randomness)
    customers = np.random.poisson(row['spend'] * conversion_rate / 80)  # ~$80 CAC

    customers_acquired.append({
        'date': row['date'],
        'channel': row['channel'],
        'customers_acquired': customers
    })

customers_acquired_df = pd.DataFrame(customers_acquired)

# Calculate CAC
cac_data = calculate_cac(
    marketing_spend_df,
    customers_acquired_df,
    period='M'
)

print("CAC by Channel and Period (Last 6 months):")
recent_cac = cac_data[cac_data['period'] >= cac_data['period'].max() - 5]
print(recent_cac.to_string(index=False))

# Overall CAC by channel
channel_cac = cac_data.groupby('channel').agg({
    'spend': 'sum',
    'customers_acquired': 'sum',
    'cac': 'mean'
}).reset_index()

channel_cac['overall_cac'] = channel_cac['spend'] / channel_cac['customers_acquired']

print("\nOverall CAC by Channel:")
print(channel_cac[['channel', 'spend', 'customers_acquired', 'overall_cac']].sort_values(
    'overall_cac'
).to_string(index=False))
```

### 2. Blended vs. Organic CAC

Separate paid acquisition costs from organic growth.

```python
def calculate_blended_organic_cac(
    total_spend: float,
    total_customers: int,
    organic_customers: int
) -> dict:
    """
    Calculate blended CAC and true paid CAC.

    Parameters:
    -----------
    total_spend : Total marketing spend
    total_customers : Total customers acquired
    organic_customers : Customers acquired organically (no direct cost)

    Returns:
    --------
    dict with CAC metrics
    """
    # Blended CAC (includes organic)
    blended_cac = total_spend / total_customers

    # Paid customers
    paid_customers = total_customers - organic_customers

    # Paid CAC (only paid acquisition)
    paid_cac = total_spend / paid_customers if paid_customers > 0 else np.inf

    # Organic percentage
    organic_pct = organic_customers / total_customers * 100

    return {
        'total_spend': total_spend,
        'total_customers': total_customers,
        'paid_customers': paid_customers,
        'organic_customers': organic_customers,
        'blended_cac': blended_cac,
        'paid_cac': paid_cac,
        'organic_percentage': organic_pct
    }

# Example: Calculate blended vs organic CAC
# Assume referral and content are partially organic
organic_channels = ['Referral', 'Content']

monthly_cac = cac_data.copy()
monthly_cac['is_organic'] = monthly_cac['channel'].isin(organic_channels)

by_period = monthly_cac.groupby('period').agg({
    'spend': 'sum',
    'customers_acquired': 'sum'
}).reset_index()

organic_by_period = monthly_cac[monthly_cac['is_organic']].groupby('period').agg({
    'customers_acquired': 'sum'
}).reset_index()

organic_by_period.columns = ['period', 'organic_customers']

by_period = by_period.merge(organic_by_period, on='period', how='left')
by_period['organic_customers'] = by_period['organic_customers'].fillna(0)

# Calculate both CAC types
for _, row in by_period.tail(6).iterrows():
    cac_metrics = calculate_blended_organic_cac(
        row['spend'],
        row['customers_acquired'],
        row['organic_customers']
    )

    print(f"\nPeriod: {row['period']}")
    print(f"  Blended CAC: ${cac_metrics['blended_cac']:.2f}")
    print(f"  Paid CAC: ${cac_metrics['paid_cac']:.2f}")
    print(f"  Organic %: {cac_metrics['organic_percentage']:.1f}%")
```

### 3. CAC Payback Period

Calculate how long it takes to recover acquisition costs.

```python
def calculate_payback_period(
    cac: float,
    monthly_revenue_per_customer: float,
    gross_margin: float = 0.80
) -> dict:
    """
    Calculate CAC payback period.

    Parameters:
    -----------
    cac : Customer acquisition cost
    monthly_revenue_per_customer : Average monthly revenue per customer
    gross_margin : Gross margin percentage (default 80%)

    Returns:
    --------
    dict with payback metrics
    """
    # Monthly gross profit per customer
    monthly_gross_profit = monthly_revenue_per_customer * gross_margin

    # Payback period in months
    payback_months = cac / monthly_gross_profit if monthly_gross_profit > 0 else np.inf

    # Annual payback
    payback_years = payback_months / 12

    return {
        'cac': cac,
        'monthly_revenue': monthly_revenue_per_customer,
        'monthly_gross_profit': monthly_gross_profit,
        'gross_margin': gross_margin,
        'payback_months': payback_months,
        'payback_years': payback_years
    }

# Example: Calculate payback by channel
# Assume average monthly revenue varies by customer source
channel_revenue = {
    'Paid Search': 75,
    'Social Media': 65,
    'Display': 60,
    'Content': 80,
    'Email': 70,
    'Referral': 85
}

payback_analysis = []

for _, row in channel_cac.iterrows():
    channel = row['channel']
    monthly_rev = channel_revenue.get(channel, 70)

    payback = calculate_payback_period(
        row['overall_cac'],
        monthly_rev,
        gross_margin=0.80
    )

    payback['channel'] = channel
    payback_analysis.append(payback)

payback_df = pd.DataFrame(payback_analysis)

print("\nPayback Period Analysis by Channel:")
print(payback_df[['channel', 'cac', 'monthly_revenue', 'payback_months']].sort_values(
    'payback_months'
).to_string(index=False))
```

### 4. CAC Trend Analysis

Analyze how CAC changes over time.

```python
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_cac_trends(
    cac_df: pd.DataFrame,
    period_col: str = 'period',
    channel_col: str = 'channel',
    cac_col: str = 'cac'
) -> dict:
    """
    Analyze CAC trends over time.

    Parameters:
    -----------
    cac_df : DataFrame with CAC data
    period_col : Period column
    channel_col : Channel column
    cac_col : CAC column

    Returns:
    --------
    dict with trend analysis
    """
    trends = {}

    for channel in cac_df[channel_col].unique():
        channel_data = cac_df[cac_df[channel_col] == channel].sort_values(period_col)

        if len(channel_data) < 2:
            continue

        # Calculate trend (linear regression slope)
        x = np.arange(len(channel_data))
        y = channel_data[cac_col].values

        # Remove NaN values
        mask = ~np.isnan(y)
        if mask.sum() < 2:
            continue

        x_clean = x[mask]
        y_clean = y[mask]

        # Calculate slope
        slope = np.polyfit(x_clean, y_clean, 1)[0]

        # Calculate percentage change
        first_value = y_clean[0]
        last_value = y_clean[-1]
        pct_change = (last_value - first_value) / first_value * 100 if first_value > 0 else 0

        trends[channel] = {
            'slope': slope,
            'pct_change': pct_change,
            'first_cac': first_value,
            'last_cac': last_value,
            'avg_cac': np.mean(y_clean),
            'trend': 'Increasing' if slope > 0 else 'Decreasing'
        }

    return trends

def plot_cac_trends(
    cac_df: pd.DataFrame,
    title: str = "CAC Trends by Channel"
) -> plt.Figure:
    """
    Visualize CAC trends over time.
    """
    fig, ax = plt.subplots(figsize=(14, 7))

    for channel in cac_df['channel'].unique():
        channel_data = cac_df[cac_df['channel'] == channel].sort_values('period')

        # Convert period to string for plotting
        x = channel_data['period'].astype(str)
        y = channel_data['cac']

        ax.plot(x, y, marker='o', linewidth=2, label=channel, alpha=0.7)

    ax.set_xlabel('Period', fontsize=12)
    ax.set_ylabel('CAC ($)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')

    # Show every 3rd label to avoid crowding
    ax.set_xticks(ax.get_xticks()[::3])

    plt.tight_layout()
    return fig

# Example: Analyze trends
cac_trends = analyze_cac_trends(cac_data)

print("\nCAC Trend Analysis:")
for channel, metrics in cac_trends.items():
    print(f"\n{channel}:")
    print(f"  First CAC: ${metrics['first_cac']:.2f}")
    print(f"  Last CAC: ${metrics['last_cac']:.2f}")
    print(f"  Change: {metrics['pct_change']:+.1f}%")
    print(f"  Trend: {metrics['trend']}")

# Plot trends
fig = plot_cac_trends(cac_data)
plt.savefig('cac_trends.png', dpi=300, bbox_inches='tight')
print("\nCAC trends chart saved to: cac_trends.png")
```

### 5. Marketing Mix Optimization

Optimize budget allocation across channels to minimize CAC.

```python
from scipy.optimize import minimize

def optimize_marketing_mix(
    channel_cac: pd.DataFrame,
    total_budget: float,
    min_spend_pct: float = 0.05,
    max_spend_pct: float = 0.50
) -> dict:
    """
    Optimize marketing budget allocation to maximize customer acquisition.

    Parameters:
    -----------
    channel_cac : DataFrame with channel CAC data
    total_budget : Total marketing budget
    min_spend_pct : Minimum spend percentage per channel
    max_spend_pct : Maximum spend percentage per channel

    Returns:
    --------
    dict with optimal allocation
    """
    channels = channel_cac['channel'].tolist()
    cac_values = channel_cac['overall_cac'].values

    n_channels = len(channels)

    # Objective: maximize customers (minimize total CAC spend)
    def objective(allocation):
        # allocation is array of budget percentages
        customers_acquired = sum(
            (allocation[i] * total_budget) / cac_values[i]
            for i in range(n_channels)
        )
        return -customers_acquired  # Negative because we minimize

    # Constraints
    constraints = [
        # Sum of allocations must equal 1
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    ]

    # Bounds (min and max spend per channel)
    bounds = [(min_spend_pct, max_spend_pct) for _ in range(n_channels)]

    # Initial guess (equal allocation)
    x0 = np.array([1/n_channels] * n_channels)

    # Optimize
    result = minimize(
        objective,
        x0,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    # Calculate results
    optimal_allocation = result.x
    optimal_spend = optimal_allocation * total_budget
    optimal_customers = [
        spend / cac for spend, cac in zip(optimal_spend, cac_values)
    ]

    return {
        'channels': channels,
        'optimal_allocation_pct': optimal_allocation * 100,
        'optimal_spend': optimal_spend,
        'expected_customers': optimal_customers,
        'total_customers': sum(optimal_customers),
        'blended_cac': total_budget / sum(optimal_customers)
    }

# Example: Optimize marketing mix
total_monthly_budget = 150000  # $150K monthly budget

optimal_mix = optimize_marketing_mix(
    channel_cac,
    total_budget=total_monthly_budget,
    min_spend_pct=0.05,
    max_spend_pct=0.40
)

print("\nOptimized Marketing Mix:")
print(f"Total Budget: ${total_monthly_budget:,.0f}")
print(f"Expected Customers: {optimal_mix['total_customers']:.0f}")
print(f"Blended CAC: ${optimal_mix['blended_cac']:.2f}\n")

for i, channel in enumerate(optimal_mix['channels']):
    print(f"{channel}:")
    print(f"  Allocation: {optimal_mix['optimal_allocation_pct'][i]:.1f}%")
    print(f"  Spend: ${optimal_mix['optimal_spend'][i]:,.0f}")
    print(f"  Expected Customers: {optimal_mix['expected_customers'][i]:.0f}")
```

### 6. Channel Efficiency Metrics

Calculate comprehensive efficiency metrics for each channel.

```python
def calculate_channel_efficiency(
    cac_df: pd.DataFrame,
    ltv_df: pd.DataFrame = None,
    payback_df: pd.DataFrame = None
) -> pd.DataFrame:
    """
    Calculate comprehensive efficiency metrics by channel.

    Parameters:
    -----------
    cac_df : DataFrame with CAC by channel
    ltv_df : DataFrame with LTV by channel (optional)
    payback_df : DataFrame with payback period by channel (optional)

    Returns:
    --------
    DataFrame with efficiency metrics
    """
    efficiency = cac_df.groupby('channel').agg({
        'spend': 'sum',
        'customers_acquired': 'sum',
        'cac': 'mean'
    }).reset_index()

    efficiency['overall_cac'] = efficiency['spend'] / efficiency['customers_acquired']

    # Add LTV if available
    if ltv_df is not None:
        efficiency = efficiency.merge(ltv_df, on='channel', how='left')
        efficiency['ltv_cac_ratio'] = efficiency['ltv'] / efficiency['overall_cac']

    # Add payback if available
    if payback_df is not None:
        efficiency = efficiency.merge(payback_df[['channel', 'payback_months']], on='channel', how='left')

    # Calculate efficiency score (lower CAC = higher score)
    min_cac = efficiency['overall_cac'].min()
    efficiency['efficiency_score'] = min_cac / efficiency['overall_cac'] * 100

    # Rank channels
    efficiency = efficiency.sort_values('efficiency_score', ascending=False)
    efficiency['rank'] = range(1, len(efficiency) + 1)

    return efficiency

# Example: Calculate channel efficiency
channel_efficiency = calculate_channel_efficiency(
    cac_data,
    payback_df=payback_df
)

print("\nChannel Efficiency Ranking:")
print(channel_efficiency[['rank', 'channel', 'overall_cac', 'customers_acquired',
                          'payback_months', 'efficiency_score']].to_string(index=False))
```

### 7. CAC Sensitivity Analysis

Analyze how CAC changes with different assumptions.

```python
def cac_sensitivity_analysis(
    base_cac: float,
    base_conversion_rate: float,
    conversion_rate_changes: list = None
) -> pd.DataFrame:
    """
    Perform sensitivity analysis on CAC.

    Parameters:
    -----------
    base_cac : Current CAC
    base_conversion_rate : Current conversion rate
    conversion_rate_changes : List of conversion rate multipliers

    Returns:
    --------
    DataFrame with sensitivity results
    """
    if conversion_rate_changes is None:
        conversion_rate_changes = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5]

    results = []

    for multiplier in conversion_rate_changes:
        new_conversion_rate = base_conversion_rate * multiplier
        new_cac = base_cac / multiplier

        pct_change_conversion = (multiplier - 1) * 100
        pct_change_cac = (new_cac - base_cac) / base_cac * 100

        results.append({
            'conversion_rate_change': f"{pct_change_conversion:+.0f}%",
            'new_conversion_rate': new_conversion_rate,
            'new_cac': new_cac,
            'cac_change': f"{pct_change_cac:+.0f}%"
        })

    return pd.DataFrame(results)

# Example: Sensitivity analysis
sensitivity = cac_sensitivity_analysis(
    base_cac=80,
    base_conversion_rate=0.025
)

print("\nCAC Sensitivity Analysis:")
print(sensitivity.to_string(index=False))
```

## Best Practices

### 1. CAC Calculation
- **Include all costs**: Marketing spend, sales salaries, tools, agencies
- **Match time periods**: Align spend with when customers were acquired
- **Account for lag**: Customer acquisition may lag spend by days/weeks
- **Fully-loaded vs. marketing-only**: Be consistent in what you include

### 2. Channel Attribution
- **Use proper attribution**: First-touch, last-touch, or multi-touch
- **Track organic separately**: Don't inflate CAC with organic customers
- **Consider assisted conversions**: Channels work together
- **Account for brand building**: Some channels have indirect effects

### 3. Optimization
- **Focus on efficiency**: Lowest CAC isn't always best (consider LTV)
- **Test and iterate**: Continuously experiment with channels
- **Scale what works**: Double down on efficient channels
- **Diversify risk**: Don't rely on single channel

### 4. Common Pitfalls to Avoid
- **Ignoring fixed costs**: Salaries, tools, overhead matter
- **Short-term thinking**: Some channels take time to optimize
- **Comparing unlike periods**: Seasonality affects CAC
- **Forgetting churn**: High churn makes CAC less meaningful

### 5. Target Benchmarks
- **LTV:CAC ratio > 3**: Healthy unit economics
- **Payback period < 12 months**: For most businesses
- **CAC trend**: Should decrease or stay flat as you optimize
- **Blended vs paid**: Track both for full picture

## References

### Methodology
- Skok, D. "SaaS Metrics 2.0 - A Guide to Measuring and Improving What Matters"
- Ellis, S. "Startup Growth Engines"
- Maurya, A. "Scaling Lean"

### Tools and Libraries
- **pandas**: Data manipulation
- **scipy**: Optimization
- **numpy**: Numerical calculations

### Industry Benchmarks
- **SaaS**: $100-$500 CAC (varies by ACV)
- **E-commerce**: $10-$50 CAC
- **Mobile Apps**: $0.50-$5 CAC
- **B2B Enterprise**: $1,000-$10,000+ CAC

### Additional Resources
- ProfitWell. "SaaS CAC Benchmarks"
- HubSpot. "How to Calculate and Reduce CAC"
- FirstRound. "The CAC Ratio: A Framework for Evaluating Channel Efficiency"

---
name: attribution-modeling
description: Build multi-touch attribution (MTA) models to assign conversion credit across marketing touchpoints. Implement first-touch, last-touch, linear, time-decay, position-based, and algorithmic attribution models. Analyze channel effectiveness, optimize marketing spend, and understand customer journey impact.
---

# Attribution Modeling

## Overview

Attribution modeling assigns credit for conversions to marketing touchpoints along the customer journey. This is crucial for understanding which channels drive value and optimizing marketing budget allocation across channels.

**Key Capabilities:**
- Multi-touch attribution (MTA) model implementation
- First-touch, last-touch, and linear attribution
- Time-decay and position-based models
- Data-driven algorithmic attribution
- Channel ROI and effectiveness analysis
- Customer journey mapping
- Attribution comparison and validation

## When to Use This Skill

Use this skill when:
- Allocating marketing budget across channels
- Understanding which touchpoints drive conversions
- Comparing effectiveness of different marketing channels
- Analyzing customer journey complexity
- Optimizing marketing mix
- Evaluating campaign performance
- Justifying marketing spend to stakeholders

## Core Capabilities

### 1. Data Preparation for Attribution

Structure touchpoint data for attribution analysis.

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict

def prepare_attribution_data(
    touchpoints_df: pd.DataFrame,
    conversions_df: pd.DataFrame,
    user_col: str = 'user_id',
    touchpoint_date_col: str = 'touchpoint_date',
    conversion_date_col: str = 'conversion_date',
    channel_col: str = 'channel',
    revenue_col: str = 'revenue',
    lookback_days: int = 30
) -> pd.DataFrame:
    """
    Prepare attribution data by joining touchpoints with conversions.

    Parameters:
    -----------
    touchpoints_df : DataFrame with marketing touchpoints
    conversions_df : DataFrame with conversions
    user_col : User identifier column
    touchpoint_date_col : Date of touchpoint
    conversion_date_col : Date of conversion
    channel_col : Marketing channel column
    revenue_col : Revenue/value column
    lookback_days : Days before conversion to consider touchpoints

    Returns:
    --------
    DataFrame with attribution-ready data
    """
    # Ensure dates are datetime
    touchpoints_df[touchpoint_date_col] = pd.to_datetime(touchpoints_df[touchpoint_date_col])
    conversions_df[conversion_date_col] = pd.to_datetime(conversions_df[conversion_date_col])

    # Join touchpoints with conversions
    attribution_data = []

    for _, conversion in conversions_df.iterrows():
        user = conversion[user_col]
        conv_date = conversion[conversion_date_col]
        revenue = conversion[revenue_col]

        # Get touchpoints for this user within lookback window
        user_touchpoints = touchpoints_df[
            (touchpoints_df[user_col] == user) &
            (touchpoints_df[touchpoint_date_col] <= conv_date) &
            (touchpoints_df[touchpoint_date_col] >= conv_date - pd.Timedelta(days=lookback_days))
        ].copy()

        if len(user_touchpoints) > 0:
            # Sort by date
            user_touchpoints = user_touchpoints.sort_values(touchpoint_date_col)

            # Add conversion info
            user_touchpoints['conversion_date'] = conv_date
            user_touchpoints['revenue'] = revenue
            user_touchpoints['days_to_conversion'] = (
                conv_date - user_touchpoints[touchpoint_date_col]
            ).dt.days
            user_touchpoints['touchpoint_position'] = range(1, len(user_touchpoints) + 1)
            user_touchpoints['total_touchpoints'] = len(user_touchpoints)

            attribution_data.append(user_touchpoints)

    return pd.concat(attribution_data, ignore_index=True) if attribution_data else pd.DataFrame()

# Example: Generate sample attribution data
np.random.seed(42)

# Define channels
channels = ['Paid Search', 'Organic Search', 'Social Media', 'Email', 'Display', 'Direct']

# Generate touchpoints
n_users = 1000
touchpoints = []

for user_id in range(n_users):
    # Each user has 1-10 touchpoints
    n_touchpoints = np.random.randint(1, 11)

    start_date = pd.Timestamp('2024-01-01') + pd.Timedelta(days=np.random.randint(0, 60))

    for i in range(n_touchpoints):
        touchpoint_date = start_date + pd.Timedelta(days=i * np.random.randint(1, 5))
        channel = np.random.choice(channels)

        touchpoints.append({
            'user_id': user_id,
            'touchpoint_date': touchpoint_date,
            'channel': channel,
            'campaign': f"{channel}_Campaign_{np.random.randint(1, 4)}"
        })

touchpoints_df = pd.DataFrame(touchpoints)

# Generate conversions (30% of users convert)
converters = np.random.choice(range(n_users), size=int(n_users * 0.3), replace=False)

conversions = []
for user_id in converters:
    # Conversion happens after last touchpoint
    user_touchpoints = touchpoints_df[touchpoints_df['user_id'] == user_id]
    last_touchpoint = user_touchpoints['touchpoint_date'].max()

    conversion_date = last_touchpoint + pd.Timedelta(days=np.random.randint(1, 7))
    revenue = np.random.gamma(2, 50)  # Average ~$100

    conversions.append({
        'user_id': user_id,
        'conversion_date': conversion_date,
        'revenue': revenue
    })

conversions_df = pd.DataFrame(conversions)

# Prepare attribution data
attribution_df = prepare_attribution_data(
    touchpoints_df,
    conversions_df,
    lookback_days=30
)

print("Attribution Data Sample:")
print(attribution_df.head(10))
```

### 2. First-Touch Attribution

Assign 100% credit to the first touchpoint.

```python
def first_touch_attribution(
    attribution_df: pd.DataFrame,
    channel_col: str = 'channel',
    revenue_col: str = 'revenue',
    user_col: str = 'user_id',
    conversion_date_col: str = 'conversion_date'
) -> pd.DataFrame:
    """
    Calculate first-touch attribution.

    Returns:
    --------
    DataFrame with attributed revenue by channel
    """
    # Get first touchpoint for each conversion
    first_touch = attribution_df.sort_values('touchpoint_position').groupby(
        [user_col, conversion_date_col]
    ).first().reset_index()

    # Sum revenue by channel
    channel_attribution = first_touch.groupby(channel_col)[revenue_col].agg([
        ('conversions', 'count'),
        ('attributed_revenue', 'sum'),
        ('avg_revenue', 'mean')
    ]).reset_index()

    channel_attribution['attribution_model'] = 'First Touch'

    return channel_attribution

# Example: Calculate first-touch attribution
first_touch_results = first_touch_attribution(attribution_df)

print("\nFirst-Touch Attribution:")
print(first_touch_results.sort_values('attributed_revenue', ascending=False))
```

### 3. Last-Touch Attribution

Assign 100% credit to the last touchpoint.

```python
def last_touch_attribution(
    attribution_df: pd.DataFrame,
    channel_col: str = 'channel',
    revenue_col: str = 'revenue',
    user_col: str = 'user_id',
    conversion_date_col: str = 'conversion_date'
) -> pd.DataFrame:
    """
    Calculate last-touch attribution.
    """
    # Get last touchpoint for each conversion
    last_touch = attribution_df.sort_values('touchpoint_position').groupby(
        [user_col, conversion_date_col]
    ).last().reset_index()

    # Sum revenue by channel
    channel_attribution = last_touch.groupby(channel_col)[revenue_col].agg([
        ('conversions', 'count'),
        ('attributed_revenue', 'sum'),
        ('avg_revenue', 'mean')
    ]).reset_index()

    channel_attribution['attribution_model'] = 'Last Touch'

    return channel_attribution

# Example: Calculate last-touch attribution
last_touch_results = last_touch_attribution(attribution_df)

print("\nLast-Touch Attribution:")
print(last_touch_results.sort_values('attributed_revenue', ascending=False))
```

### 4. Linear Attribution

Distribute credit equally across all touchpoints.

```python
def linear_attribution(
    attribution_df: pd.DataFrame,
    channel_col: str = 'channel',
    revenue_col: str = 'revenue'
) -> pd.DataFrame:
    """
    Calculate linear attribution (equal credit to all touchpoints).
    """
    # Calculate attribution weight (1 / number of touchpoints)
    attribution_df['attribution_weight'] = 1 / attribution_df['total_touchpoints']
    attribution_df['attributed_revenue'] = (
        attribution_df[revenue_col] * attribution_df['attribution_weight']
    )

    # Sum by channel
    channel_attribution = attribution_df.groupby(channel_col).agg({
        'attributed_revenue': 'sum',
        'user_id': 'nunique',  # Unique users influenced
        revenue_col: 'count'  # Total touchpoints
    }).reset_index()

    channel_attribution.columns = [
        channel_col, 'attributed_revenue', 'users_influenced', 'total_touchpoints'
    ]
    channel_attribution['attribution_model'] = 'Linear'

    return channel_attribution

# Example: Calculate linear attribution
linear_results = linear_attribution(attribution_df)

print("\nLinear Attribution:")
print(linear_results.sort_values('attributed_revenue', ascending=False))
```

### 5. Time-Decay Attribution

Give more credit to touchpoints closer to conversion.

```python
def time_decay_attribution(
    attribution_df: pd.DataFrame,
    channel_col: str = 'channel',
    revenue_col: str = 'revenue',
    half_life_days: int = 7
) -> pd.DataFrame:
    """
    Calculate time-decay attribution with exponential decay.

    Parameters:
    -----------
    attribution_df : Attribution data
    channel_col : Channel column name
    revenue_col : Revenue column name
    half_life_days : Number of days for weight to halve

    Returns:
    --------
    DataFrame with attributed revenue by channel
    """
    # Calculate time-decay weight
    # Weight = 2^(-days_to_conversion / half_life)
    attribution_df = attribution_df.copy()
    attribution_df['time_weight'] = 2 ** (
        -attribution_df['days_to_conversion'] / half_life_days
    )

    # Normalize weights for each conversion
    def normalize_weights(group):
        group['attribution_weight'] = group['time_weight'] / group['time_weight'].sum()
        return group

    attribution_df = attribution_df.groupby(
        ['user_id', 'conversion_date']
    ).apply(normalize_weights).reset_index(drop=True)

    # Calculate attributed revenue
    attribution_df['attributed_revenue'] = (
        attribution_df[revenue_col] * attribution_df['attribution_weight']
    )

    # Sum by channel
    channel_attribution = attribution_df.groupby(channel_col).agg({
        'attributed_revenue': 'sum',
        'user_id': 'nunique',
        revenue_col: 'count'
    }).reset_index()

    channel_attribution.columns = [
        channel_col, 'attributed_revenue', 'users_influenced', 'total_touchpoints'
    ]
    channel_attribution['attribution_model'] = 'Time Decay'

    return channel_attribution

# Example: Calculate time-decay attribution
time_decay_results = time_decay_attribution(attribution_df, half_life_days=7)

print("\nTime-Decay Attribution:")
print(time_decay_results.sort_values('attributed_revenue', ascending=False))
```

### 6. Position-Based (U-Shaped) Attribution

Give more credit to first and last touch (e.g., 40-20-40).

```python
def position_based_attribution(
    attribution_df: pd.DataFrame,
    channel_col: str = 'channel',
    revenue_col: str = 'revenue',
    first_touch_weight: float = 0.4,
    last_touch_weight: float = 0.4
) -> pd.DataFrame:
    """
    Calculate position-based attribution.

    Parameters:
    -----------
    attribution_df : Attribution data
    channel_col : Channel column name
    revenue_col : Revenue column name
    first_touch_weight : Weight for first touch (e.g., 0.4 for 40%)
    last_touch_weight : Weight for last touch (e.g., 0.4 for 40%)

    Middle touchpoints share remaining weight equally.
    """
    attribution_df = attribution_df.copy()

    def assign_position_weights(group):
        n = len(group)

        if n == 1:
            # Single touchpoint gets 100%
            group['attribution_weight'] = 1.0
        elif n == 2:
            # Two touchpoints: split first/last weights
            group['attribution_weight'] = [first_touch_weight, last_touch_weight]
        else:
            # Multiple touchpoints
            middle_weight = 1 - first_touch_weight - last_touch_weight
            per_middle = middle_weight / (n - 2) if n > 2 else 0

            weights = [first_touch_weight]
            weights.extend([per_middle] * (n - 2))
            weights.append(last_touch_weight)

            group['attribution_weight'] = weights

        return group

    attribution_df = attribution_df.sort_values('touchpoint_position').groupby(
        ['user_id', 'conversion_date']
    ).apply(assign_position_weights).reset_index(drop=True)

    # Calculate attributed revenue
    attribution_df['attributed_revenue'] = (
        attribution_df[revenue_col] * attribution_df['attribution_weight']
    )

    # Sum by channel
    channel_attribution = attribution_df.groupby(channel_col).agg({
        'attributed_revenue': 'sum',
        'user_id': 'nunique',
        revenue_col: 'count'
    }).reset_index()

    channel_attribution.columns = [
        channel_col, 'attributed_revenue', 'users_influenced', 'total_touchpoints'
    ]
    channel_attribution['attribution_model'] = 'Position-Based'

    return channel_attribution

# Example: Calculate position-based attribution
position_based_results = position_based_attribution(
    attribution_df,
    first_touch_weight=0.4,
    last_touch_weight=0.4
)

print("\nPosition-Based Attribution (40-20-40):")
print(position_based_results.sort_values('attributed_revenue', ascending=False))
```

### 7. Data-Driven Attribution (Markov Chains)

Use probabilistic approach based on actual customer journeys.

```python
from collections import defaultdict
from itertools import combinations

def markov_chain_attribution(
    attribution_df: pd.DataFrame,
    channel_col: str = 'channel',
    revenue_col: str = 'revenue',
    user_col: str = 'user_id',
    conversion_date_col: str = 'conversion_date'
) -> pd.DataFrame:
    """
    Calculate attribution using Markov chains.

    This measures the "removal effect" - how much conversion probability
    drops when a channel is removed from the journey.
    """
    # Build customer journeys
    journeys = attribution_df.sort_values('touchpoint_position').groupby(
        [user_col, conversion_date_col]
    ).agg({
        channel_col: list,
        revenue_col: 'first'
    }).reset_index()

    # Calculate transition probabilities
    transitions = defaultdict(lambda: defaultdict(int))
    start_channels = defaultdict(int)

    for _, row in journeys.iterrows():
        path = row[channel_col]

        # Start transitions
        start_channels[path[0]] += 1

        # Channel transitions
        for i in range(len(path) - 1):
            transitions[path[i]][path[i+1]] += 1

        # Last channel to conversion
        transitions[path[-1]]['(conversion)'] += 1

    # Convert to probabilities
    transition_probs = {}
    for source in transitions:
        total = sum(transitions[source].values())
        transition_probs[source] = {
            target: count / total
            for target, count in transitions[source].items()
        }

    # Calculate removal effect for each channel
    channels = attribution_df[channel_col].unique()
    total_conversions = len(journeys)

    removal_effects = {}

    for channel in channels:
        # Calculate conversion probability without this channel
        # This is a simplified version; full implementation would simulate all paths
        conversions_with = journeys[
            journeys[channel_col].apply(lambda x: channel in x)
        ][revenue_col].sum()

        conversions_without = journeys[
            journeys[channel_col].apply(lambda x: channel not in x)
        ][revenue_col].sum()

        # Removal effect
        removal_effect = conversions_with / (conversions_with + conversions_without)
        removal_effects[channel] = removal_effect

    # Normalize removal effects to sum to total revenue
    total_removal = sum(removal_effects.values())
    total_revenue = journeys[revenue_col].sum()

    channel_attribution = []
    for channel, effect in removal_effects.items():
        attributed_rev = (effect / total_removal) * total_revenue

        channel_attribution.append({
            channel_col: channel,
            'attributed_revenue': attributed_rev,
            'removal_effect': effect
        })

    result_df = pd.DataFrame(channel_attribution)
    result_df['attribution_model'] = 'Markov Chain'

    return result_df

# Example: Calculate Markov chain attribution
markov_results = markov_chain_attribution(attribution_df)

print("\nMarkov Chain Attribution:")
print(markov_results.sort_values('attributed_revenue', ascending=False))
```

### 8. Attribution Model Comparison

Compare different attribution models side-by-side.

```python
import matplotlib.pyplot as plt
import seaborn as sns

def compare_attribution_models(
    attribution_df: pd.DataFrame,
    models_to_compare: List[str] = None
) -> pd.DataFrame:
    """
    Run multiple attribution models and compare results.

    Parameters:
    -----------
    attribution_df : Attribution data
    models_to_compare : List of model names to include

    Returns:
    --------
    DataFrame with comparison across models
    """
    if models_to_compare is None:
        models_to_compare = [
            'first_touch', 'last_touch', 'linear',
            'time_decay', 'position_based'
        ]

    results = []

    # Calculate each model
    if 'first_touch' in models_to_compare:
        ft = first_touch_attribution(attribution_df)
        results.append(ft)

    if 'last_touch' in models_to_compare:
        lt = last_touch_attribution(attribution_df)
        results.append(lt)

    if 'linear' in models_to_compare:
        lin = linear_attribution(attribution_df)
        results.append(lin)

    if 'time_decay' in models_to_compare:
        td = time_decay_attribution(attribution_df)
        results.append(td)

    if 'position_based' in models_to_compare:
        pb = position_based_attribution(attribution_df)
        results.append(pb)

    # Combine results
    combined = pd.concat(results, ignore_index=True)

    return combined

def plot_attribution_comparison(
    comparison_df: pd.DataFrame,
    channel_col: str = 'channel'
) -> plt.Figure:
    """
    Visualize attribution model comparison.
    """
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Plot 1: Attributed revenue by channel and model
    pivot_data = comparison_df.pivot(
        index=channel_col,
        columns='attribution_model',
        values='attributed_revenue'
    )

    pivot_data.plot(kind='bar', ax=axes[0], width=0.8)
    axes[0].set_xlabel('Channel', fontsize=12)
    axes[0].set_ylabel('Attributed Revenue ($)', fontsize=12)
    axes[0].set_title('Attributed Revenue by Model', fontsize=14, fontweight='bold')
    axes[0].legend(title='Attribution Model', bbox_to_anchor=(1.05, 1), loc='upper left')
    axes[0].grid(axis='y', alpha=0.3)
    axes[0].tick_params(axis='x', rotation=45)

    # Plot 2: Revenue share by model
    ax2 = axes[1]
    models = comparison_df['attribution_model'].unique()
    width = 0.8 / len(models)
    x = np.arange(len(comparison_df[channel_col].unique()))

    for i, model in enumerate(models):
        model_data = comparison_df[comparison_df['attribution_model'] == model]
        total_revenue = model_data['attributed_revenue'].sum()
        model_data['revenue_share'] = (
            model_data['attributed_revenue'] / total_revenue * 100
        )

        offset = (i - len(models)/2 + 0.5) * width
        ax2.bar(
            x + offset,
            model_data['revenue_share'],
            width,
            label=model,
            alpha=0.8
        )

    ax2.set_xlabel('Channel', fontsize=12)
    ax2.set_ylabel('Revenue Share (%)', fontsize=12)
    ax2.set_title('Revenue Share by Model', fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(comparison_df[channel_col].unique(), rotation=45, ha='right')
    ax2.legend(title='Attribution Model')
    ax2.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig

# Example: Compare models
comparison = compare_attribution_models(attribution_df)

print("\nAttribution Model Comparison:")
print(comparison.pivot(
    index='channel',
    columns='attribution_model',
    values='attributed_revenue'
).round(2))

# Plot comparison
fig = plot_attribution_comparison(comparison)
plt.savefig('attribution_comparison.png', dpi=300, bbox_inches='tight')
print("\nComparison chart saved to: attribution_comparison.png")
```

## Best Practices

### 1. Model Selection
- **First/Last Touch**: Simple but biased; good for initial analysis
- **Linear**: Fair but may over-credit low-value touches
- **Time Decay**: Good when recent touches are more important
- **Position-Based**: Balances acquisition and conversion credit
- **Data-Driven**: Most accurate but requires significant data

### 2. Data Requirements
- **Sufficient volume**: Need 100+ conversions for reliable results
- **Complete tracking**: Must track all touchpoints consistently
- **Proper lookback window**: 7-90 days depending on sales cycle
- **Clean data**: Remove bots, internal traffic, duplicates

### 3. Implementation
- **Start simple**: Begin with first/last touch, add complexity
- **Validate results**: Compare with known channel performance
- **Update regularly**: Attribution degrades as behavior changes
- **Consider offline**: Phone calls, store visits matter

### 4. Common Pitfalls to Avoid
- **View-through attribution**: Overvaluing display impressions
- **Double counting**: Ensure events counted once per model
- **Ignoring indirect value**: Assist touches matter
- **Over-attribution**: Can't attribute more than 100%

### 5. Advanced Considerations
- **Multi-conversion attribution**: Users may convert multiple times
- **Cross-device tracking**: Mobile and desktop journeys
- **Offline integration**: Connect online and offline touchpoints
- **Incrementality testing**: Use experiments to validate

## References

### Methodology
- Dalessandro, B., et al. (2012). "Causally Motivated Attribution for Online Advertising"
- Shao, X., & Li, L. (2011). "Data-driven Multi-touch Attribution Models"
- Google. "Data-Driven Attribution Methodology"

### Tools and Libraries
- **pandas**: Data manipulation
- **networkx**: For Markov chain implementations
- **sklearn**: For algorithmic attribution models

### Industry Standards
- **B2C E-commerce**: 7-14 day lookback, position-based
- **B2B SaaS**: 30-90 day lookback, linear or data-driven
- **Mobile Apps**: 7 day lookback, last-touch or time-decay

### Additional Resources
- Google Analytics. "Attribution Modeling"
- Facebook. "Attribution Settings"
- Avinash Kaushik. "Multi-Channel Attribution Modeling: The Good, Bad and Ugly"

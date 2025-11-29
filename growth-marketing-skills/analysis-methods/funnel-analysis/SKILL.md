---
name: funnel-analysis
description: Analyze conversion funnels and user journeys to identify drop-off points and optimization opportunities. Build multi-step funnels, calculate conversion rates, visualize drop-offs, perform time-to-convert analysis, and segment funnels by user attributes for data-driven conversion optimization.
---

# Funnel Analysis

## Overview

Funnel analysis tracks users through sequential steps toward a conversion goal, identifying where users drop off and which steps have the biggest impact on overall conversion. This is essential for optimizing onboarding, checkout processes, and any multi-step user journey.

**Key Capabilities:**
- Multi-step funnel construction
- Conversion rate calculation at each step
- Drop-off analysis and bottleneck identification
- Time-to-convert analysis
- Segmented funnel comparison
- Alternative path analysis
- Funnel visualization and reporting

## When to Use This Skill

Use this skill when:
- Optimizing signup or onboarding flows
- Analyzing checkout abandonment
- Understanding trial-to-paid conversion
- Identifying friction points in user journeys
- Comparing funnel performance across segments
- Measuring the impact of funnel optimizations
- Analyzing time spent in each funnel step

## Core Capabilities

### 1. Building Conversion Funnels

Create a funnel from sequential event data.

```python
import pandas as pd
import numpy as np
from typing import List, Dict

def build_funnel(
    df: pd.DataFrame,
    user_col: str = 'user_id',
    event_col: str = 'event_name',
    timestamp_col: str = 'timestamp',
    funnel_steps: List[str] = None,
    time_window: int = None
) -> pd.DataFrame:
    """
    Build conversion funnel from event data.

    Parameters:
    -----------
    df : DataFrame with user events
    user_col : User identifier column
    event_col : Event name column
    timestamp_col : Event timestamp column
    funnel_steps : Ordered list of events in the funnel
    time_window : Maximum days between first and last step (optional)

    Returns:
    --------
    DataFrame with funnel metrics
    """
    # Ensure timestamp is datetime
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])

    # Filter to funnel events
    funnel_df = df[df[event_col].isin(funnel_steps)].copy()

    # Get first occurrence of each event for each user
    user_events = funnel_df.sort_values([user_col, timestamp_col]).groupby(
        [user_col, event_col]
    )[timestamp_col].first().reset_index()

    # Pivot to get one row per user
    user_funnel = user_events.pivot(
        index=user_col,
        columns=event_col,
        values=timestamp_col
    )

    # Calculate funnel metrics
    funnel_metrics = []
    total_users = len(df[user_col].unique())

    for i, step in enumerate(funnel_steps):
        # Users who completed this step
        completed = user_funnel[step].notna()

        if i == 0:
            # First step: count all users who started
            step_users = completed.sum()
            conversion_from_start = step_users / total_users * 100
            conversion_from_previous = 100.0
            drop_off = 100 - conversion_from_previous
        else:
            # Subsequent steps: must have completed previous step
            previous_step = funnel_steps[i-1]
            eligible = user_funnel[previous_step].notna()

            step_users = (completed & eligible).sum()
            previous_users = eligible.sum()

            conversion_from_start = step_users / total_users * 100
            conversion_from_previous = (
                step_users / previous_users * 100 if previous_users > 0 else 0
            )
            drop_off = 100 - conversion_from_previous

        funnel_metrics.append({
            'step': i + 1,
            'step_name': step,
            'users': step_users,
            'conversion_from_start': conversion_from_start,
            'conversion_from_previous': conversion_from_previous,
            'drop_off_rate': drop_off
        })

    return pd.DataFrame(funnel_metrics)

# Example: Generate sample funnel data
np.random.seed(42)

events = []
n_users = 10000

# Define funnel steps
funnel_steps = [
    'visit_homepage',
    'view_product',
    'add_to_cart',
    'checkout',
    'purchase'
]

# Simulate user journeys with decreasing conversion at each step
for user_id in range(n_users):
    timestamp = pd.Timestamp('2024-01-01') + pd.Timedelta(days=np.random.randint(0, 90))

    # Each user starts at homepage
    events.append({
        'user_id': user_id,
        'event_name': 'visit_homepage',
        'timestamp': timestamp
    })

    # Simulate drop-off at each step
    conversion_rates = [0.7, 0.5, 0.6, 0.8]  # Rates for subsequent steps

    current_timestamp = timestamp
    for i, (step, rate) in enumerate(zip(funnel_steps[1:], conversion_rates)):
        if np.random.random() < rate:
            # User continues to next step
            current_timestamp += pd.Timedelta(minutes=np.random.randint(1, 60))
            events.append({
                'user_id': user_id,
                'event_name': step,
                'timestamp': current_timestamp
            })
        else:
            # User drops off
            break

events_df = pd.DataFrame(events)

# Build funnel
funnel = build_funnel(
    events_df,
    funnel_steps=funnel_steps
)

print("Conversion Funnel Analysis:")
print(funnel.to_string(index=False))
```

### 2. Funnel Visualization

Visualize the funnel with drop-off rates.

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_funnel(
    funnel_df: pd.DataFrame,
    title: str = "Conversion Funnel"
) -> plt.Figure:
    """
    Create funnel visualization.

    Parameters:
    -----------
    funnel_df : DataFrame from build_funnel function
    title : Plot title
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Plot 1: Funnel bars
    colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(funnel_df)))

    bars = ax1.barh(
        funnel_df['step_name'],
        funnel_df['users'],
        color=colors
    )

    # Add value labels
    for i, (bar, row) in enumerate(zip(bars, funnel_df.itertuples())):
        width = bar.get_width()
        ax1.text(
            width, bar.get_y() + bar.get_height()/2,
            f' {int(row.users):,} ({row.conversion_from_start:.1f}%)',
            va='center', fontsize=10, fontweight='bold'
        )

    ax1.set_xlabel('Number of Users', fontsize=12)
    ax1.set_title(f'{title} - User Counts', fontsize=14, fontweight='bold')
    ax1.invert_yaxis()
    ax1.grid(axis='x', alpha=0.3)

    # Plot 2: Conversion rates
    x = range(len(funnel_df))

    # Overall conversion from start
    ax2.plot(
        x, funnel_df['conversion_from_start'],
        marker='o', linewidth=3, markersize=10,
        label='From Start', color='#2ecc71'
    )

    # Step-by-step conversion
    ax2.plot(
        x, funnel_df['conversion_from_previous'],
        marker='s', linewidth=3, markersize=10,
        label='From Previous Step', color='#3498db'
    )

    ax2.set_xlabel('Funnel Step', fontsize=12)
    ax2.set_ylabel('Conversion Rate (%)', fontsize=12)
    ax2.set_title(f'{title} - Conversion Rates', fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(funnel_df['step_name'], rotation=45, ha='right')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 105)

    plt.tight_layout()
    return fig

# Example: Plot funnel
fig = plot_funnel(funnel, title="E-commerce Purchase Funnel")
plt.savefig('funnel_analysis.png', dpi=300, bbox_inches='tight')
print("\nFunnel visualization saved to: funnel_analysis.png")
```

### 3. Time-to-Convert Analysis

Analyze how long users take to complete the funnel.

```python
def analyze_time_to_convert(
    df: pd.DataFrame,
    user_col: str = 'user_id',
    event_col: str = 'event_name',
    timestamp_col: str = 'timestamp',
    start_event: str = None,
    end_event: str = None
) -> pd.DataFrame:
    """
    Analyze time between funnel start and completion.

    Parameters:
    -----------
    df : DataFrame with user events
    user_col : User identifier column
    event_col : Event name column
    timestamp_col : Event timestamp column
    start_event : First event in funnel
    end_event : Last event in funnel (conversion)

    Returns:
    --------
    DataFrame with time-to-convert statistics
    """
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])

    # Get start times
    start_times = df[df[event_col] == start_event].groupby(
        user_col
    )[timestamp_col].min()

    # Get end times
    end_times = df[df[event_col] == end_event].groupby(
        user_col
    )[timestamp_col].min()

    # Calculate time to convert
    time_to_convert = pd.DataFrame({
        'start_time': start_times,
        'end_time': end_times
    }).dropna()

    time_to_convert['time_to_convert_hours'] = (
        time_to_convert['end_time'] - time_to_convert['start_time']
    ).dt.total_seconds() / 3600

    time_to_convert['time_to_convert_days'] = (
        time_to_convert['time_to_convert_hours'] / 24
    )

    # Calculate statistics
    stats = {
        'total_converters': len(time_to_convert),
        'mean_hours': time_to_convert['time_to_convert_hours'].mean(),
        'median_hours': time_to_convert['time_to_convert_hours'].median(),
        'p25_hours': time_to_convert['time_to_convert_hours'].quantile(0.25),
        'p75_hours': time_to_convert['time_to_convert_hours'].quantile(0.75),
        'p90_hours': time_to_convert['time_to_convert_hours'].quantile(0.90),
    }

    print("\nTime to Convert Statistics:")
    print(f"Total Converters: {stats['total_converters']:,}")
    print(f"Mean Time: {stats['mean_hours']:.1f} hours ({stats['mean_hours']/24:.1f} days)")
    print(f"Median Time: {stats['median_hours']:.1f} hours ({stats['median_hours']/24:.1f} days)")
    print(f"25th Percentile: {stats['p25_hours']:.1f} hours")
    print(f"75th Percentile: {stats['p75_hours']:.1f} hours")
    print(f"90th Percentile: {stats['p90_hours']:.1f} hours")

    return time_to_convert, stats

# Example: Analyze time to convert
time_data, stats = analyze_time_to_convert(
    events_df,
    start_event='visit_homepage',
    end_event='purchase'
)

# Plot distribution
fig, ax = plt.subplots(figsize=(12, 6))
ax.hist(
    time_data['time_to_convert_hours'],
    bins=50,
    edgecolor='black',
    alpha=0.7
)
ax.axvline(
    stats['median_hours'],
    color='red',
    linestyle='--',
    linewidth=2,
    label=f"Median: {stats['median_hours']:.1f}h"
)
ax.set_xlabel('Time to Convert (hours)', fontsize=12)
ax.set_ylabel('Number of Users', fontsize=12)
ax.set_title('Distribution of Time to Convert', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('time_to_convert.png', dpi=300, bbox_inches='tight')
```

### 4. Segmented Funnel Analysis

Compare funnel performance across different segments.

```python
def segment_funnel_analysis(
    df: pd.DataFrame,
    segment_col: str,
    user_col: str = 'user_id',
    event_col: str = 'event_name',
    timestamp_col: str = 'timestamp',
    funnel_steps: List[str] = None
) -> Dict[str, pd.DataFrame]:
    """
    Build funnels for different user segments.

    Parameters:
    -----------
    df : DataFrame with user events and segment information
    segment_col : Column containing segment labels
    Other parameters same as build_funnel

    Returns:
    --------
    dict : Funnel DataFrames for each segment
    """
    funnels = {}

    for segment in df[segment_col].unique():
        segment_df = df[df[segment_col] == segment]
        funnel = build_funnel(
            segment_df,
            user_col=user_col,
            event_col=event_col,
            timestamp_col=timestamp_col,
            funnel_steps=funnel_steps
        )
        funnel['segment'] = segment
        funnels[segment] = funnel

    # Combine all funnels
    combined = pd.concat(funnels.values(), ignore_index=True)

    return funnels, combined

def plot_segmented_funnels(
    combined_df: pd.DataFrame,
    title: str = "Funnel by Segment"
) -> plt.Figure:
    """
    Plot funnel comparison across segments.
    """
    fig, ax = plt.subplots(figsize=(14, 7))

    segments = combined_df['segment'].unique()
    x = np.arange(len(combined_df['step_name'].unique()))
    width = 0.8 / len(segments)

    for i, segment in enumerate(segments):
        segment_data = combined_df[combined_df['segment'] == segment]
        offset = (i - len(segments)/2 + 0.5) * width

        bars = ax.bar(
            x + offset,
            segment_data['conversion_from_start'],
            width,
            label=segment,
            alpha=0.8
        )

    ax.set_xlabel('Funnel Step', fontsize=12)
    ax.set_ylabel('Conversion Rate from Start (%)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(combined_df['step_name'].unique(), rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig

# Example: Add segments to data
np.random.seed(42)
events_df['device_type'] = np.random.choice(
    ['mobile', 'desktop', 'tablet'],
    size=len(events_df),
    p=[0.6, 0.3, 0.1]
)

# Analyze by segment
segment_funnels, combined_funnel = segment_funnel_analysis(
    events_df,
    segment_col='device_type',
    funnel_steps=funnel_steps
)

print("\n\nSegmented Funnel Analysis:")
print(combined_funnel.to_string(index=False))

# Plot segmented funnels
fig = plot_segmented_funnels(combined_funnel, title="Conversion Funnel by Device Type")
plt.savefig('segmented_funnel.png', dpi=300, bbox_inches='tight')
```

### 5. Funnel Optimization Impact

Calculate the impact of improving specific funnel steps.

```python
def calculate_optimization_impact(
    funnel_df: pd.DataFrame,
    improvements: Dict[str, float]
) -> pd.DataFrame:
    """
    Calculate impact of improving conversion at specific steps.

    Parameters:
    -----------
    funnel_df : DataFrame from build_funnel
    improvements : dict mapping step_name to improvement (e.g., 0.05 for 5% increase)

    Returns:
    --------
    DataFrame showing projected impact
    """
    results = []

    # Current overall conversion
    current_overall = funnel_df.iloc[-1]['conversion_from_start']

    for step_name, improvement in improvements.items():
        # Create copy of funnel
        projected_funnel = funnel_df.copy()

        # Find the step
        step_idx = projected_funnel[
            projected_funnel['step_name'] == step_name
        ].index[0]

        # Calculate new conversion rates
        for i in range(step_idx, len(projected_funnel)):
            if i == step_idx:
                # Improve this step
                current_rate = projected_funnel.loc[i, 'conversion_from_previous']
                new_rate = min(100, current_rate * (1 + improvement))
                projected_funnel.loc[i, 'conversion_from_previous'] = new_rate

            # Recalculate downstream conversions
            if i == 0:
                projected_funnel.loc[i, 'conversion_from_start'] = 100
            else:
                prev_conversion = projected_funnel.loc[i-1, 'conversion_from_start']
                step_conversion = projected_funnel.loc[i, 'conversion_from_previous']
                projected_funnel.loc[i, 'conversion_from_start'] = (
                    prev_conversion * step_conversion / 100
                )

        # New overall conversion
        new_overall = projected_funnel.iloc[-1]['conversion_from_start']

        # Calculate impact
        absolute_increase = new_overall - current_overall
        relative_increase = (new_overall - current_overall) / current_overall

        # Additional conversions
        total_users = funnel_df.iloc[0]['users']
        additional_conversions = (absolute_increase / 100) * total_users

        results.append({
            'step_improved': step_name,
            'improvement': f"{improvement*100:.0f}%",
            'current_overall_cr': current_overall,
            'new_overall_cr': new_overall,
            'absolute_increase': absolute_increase,
            'relative_increase': relative_increase,
            'additional_conversions': additional_conversions
        })

    return pd.DataFrame(results)

# Example: Calculate impact of improvements
improvements = {
    'view_product': 0.10,  # 10% improvement
    'add_to_cart': 0.10,
    'checkout': 0.10,
    'purchase': 0.05
}

impact_analysis = calculate_optimization_impact(funnel, improvements)

print("\n\nFunnel Optimization Impact Analysis:")
for _, row in impact_analysis.iterrows():
    print(f"\nImproving '{row['step_improved']}' by {row['improvement']}:")
    print(f"  Overall CR: {row['current_overall_cr']:.2f}% → {row['new_overall_cr']:.2f}%")
    print(f"  Relative Increase: {row['relative_increase']:.2%}")
    print(f"  Additional Conversions: {row['additional_conversions']:.0f}")

# Find best opportunity
best_opportunity = impact_analysis.loc[
    impact_analysis['additional_conversions'].idxmax()
]
print(f"\nBest Optimization Opportunity: {best_opportunity['step_improved']}")
print(f"  Would add {best_opportunity['additional_conversions']:.0f} conversions")
```

### 6. Funnel Drop-off Analysis

Identify users who drop off at each step and analyze their characteristics.

```python
def analyze_dropoff_users(
    df: pd.DataFrame,
    user_col: str = 'user_id',
    event_col: str = 'event_name',
    funnel_steps: List[str] = None,
    user_attributes: pd.DataFrame = None
) -> Dict[str, pd.DataFrame]:
    """
    Identify and characterize users who drop off at each step.

    Parameters:
    -----------
    df : DataFrame with user events
    user_col, event_col : Column names
    funnel_steps : Ordered list of funnel events
    user_attributes : DataFrame with user characteristics

    Returns:
    --------
    dict : Drop-off users for each step
    """
    # Get users who completed each step
    user_events = df[df[event_col].isin(funnel_steps)].groupby(
        [user_col, event_col]
    ).size().reset_index(name='count')

    user_steps = user_events.pivot(
        index=user_col,
        columns=event_col,
        values='count'
    ).fillna(0)

    dropoff_analysis = {}

    for i, step in enumerate(funnel_steps[:-1]):
        next_step = funnel_steps[i + 1]

        # Users who completed this step but not next
        completed_current = user_steps[step] > 0
        didnt_complete_next = user_steps[next_step] == 0

        dropoff_users = user_steps[completed_current & didnt_complete_next].index

        dropoff_info = {
            'step': step,
            'next_step': next_step,
            'dropoff_count': len(dropoff_users),
            'dropoff_users': dropoff_users.tolist()
        }

        if user_attributes is not None:
            # Analyze characteristics of drop-off users
            dropoff_chars = user_attributes[
                user_attributes[user_col].isin(dropoff_users)
            ]
            dropoff_info['characteristics'] = dropoff_chars

        dropoff_analysis[step] = dropoff_info

    return dropoff_analysis

# Example: Analyze drop-offs
dropoff_data = analyze_dropoff_users(
    events_df,
    funnel_steps=funnel_steps
)

print("\n\nDrop-off Analysis:")
for step, info in dropoff_data.items():
    print(f"\nUsers who dropped off after '{step}':")
    print(f"  Count: {info['dropoff_count']:,}")
    print(f"  Did not proceed to: {info['next_step']}")
```

## Best Practices

### 1. Funnel Design
- **Define clear steps**: Each step should be a meaningful action
- **Order matters**: Steps must be sequential and logical
- **Not too many steps**: 3-7 steps is ideal for analysis
- **Include alternative paths**: Users may skip steps

### 2. Measurement
- **Time windows**: Set realistic timeframes for completion
- **Unique vs. repeat events**: Count first occurrence or all?
- **Strict vs. flexible order**: Must steps be in exact order?
- **Partial completion**: Track and analyze incomplete journeys

### 3. Analysis
- **Identify biggest drops**: Focus on steps with largest drop-off
- **Calculate impact**: Which improvements matter most?
- **Segment analysis**: Different users may behave differently
- **Time-based trends**: Is the funnel improving or degrading?

### 4. Common Pitfalls to Avoid
- **Survivor bias**: Don't only analyze converters
- **Selection effects**: Early steps may filter specific user types
- **Confounding factors**: External events can affect funnel performance
- **Over-optimization**: Don't sacrifice user experience for conversion

### 5. Advanced Techniques
- **Multi-path funnels**: Users may take different routes
- **Recursive funnels**: Users may retry steps
- **Event sequences**: Analyze order and timing of events
- **Predictive modeling**: Identify likely converters early

## References

### Methodology
- Amplitude. "The Essential Guide to Funnel Analysis"
- Mixpanel. "Funnel Analysis Best Practices"
- Google Analytics. "Goal Funnels and Conversion Tracking"

### Tools and Libraries
- **pandas**: Data manipulation for funnel construction
- **matplotlib/seaborn**: Visualization
- **plotly**: Interactive funnel charts

### Industry Benchmarks
- E-commerce cart abandonment: 60-80%
- SaaS trial-to-paid: 15-25%
- Mobile app onboarding completion: 20-40%
- Lead-to-customer (B2B): 5-20%

### Additional Resources
- Reforge. "Conversion Optimization"
- CXL. "Funnel Analysis: The Complete Guide"
- Heap. "Understanding Conversion Funnels"

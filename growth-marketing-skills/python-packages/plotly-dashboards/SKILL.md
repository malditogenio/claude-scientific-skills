---
name: plotly-dashboards
description: "Interactive marketing dashboards and visualizations. Funnel charts, time series, heatmaps, cohort visualizations, campaign performance charts, ROAS tracking."
---

# Plotly for Marketing Dashboards

## Overview

Plotly enables creation of interactive, publication-quality visualizations for marketing analytics. This skill covers building marketing dashboards, funnel visualizations, cohort heatmaps, campaign performance charts, and real-time metrics displays.

## When to Use This Skill

- Creating interactive marketing dashboards
- Visualizing conversion funnels
- Building cohort retention heatmaps
- Displaying campaign performance over time
- Creating executive reports with drill-down capabilities
- Building real-time metrics visualizations

## Core Capabilities

### 1. Conversion Funnel Visualization

```python
import plotly.graph_objects as go

# Funnel data
stages = ['Website Visits', 'Product Views', 'Add to Cart', 'Checkout Started', 'Purchase']
values = [10000, 4500, 2100, 1200, 450]

fig = go.Figure(go.Funnel(
    y=stages,
    x=values,
    textposition="inside",
    textinfo="value+percent initial+percent previous",
    marker=dict(
        color=["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099"]
    )
))

fig.update_layout(
    title="E-commerce Conversion Funnel",
    font=dict(size=14)
)
fig.show()
```

### 2. Cohort Retention Heatmap

```python
import plotly.express as px
import pandas as pd
import numpy as np

# Sample cohort retention data
cohorts = ['Jan 2024', 'Feb 2024', 'Mar 2024', 'Apr 2024', 'May 2024']
months = ['Month 0', 'Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5']

retention_data = np.array([
    [100, 45, 32, 28, 25, 22],
    [100, 48, 35, 30, 27, np.nan],
    [100, 42, 30, 26, np.nan, np.nan],
    [100, 50, 38, np.nan, np.nan, np.nan],
    [100, 46, np.nan, np.nan, np.nan, np.nan]
])

fig = px.imshow(
    retention_data,
    labels=dict(x="Cohort Age", y="Cohort", color="Retention %"),
    x=months,
    y=cohorts,
    color_continuous_scale='Blues',
    text_auto='.1f'
)

fig.update_layout(
    title="Customer Retention by Cohort",
    xaxis_title="Months Since Acquisition",
    yaxis_title="Acquisition Cohort"
)
fig.show()
```

### 3. Campaign Performance Dashboard

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Create multi-chart dashboard
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Daily Revenue', 'ROAS by Channel',
                   'Conversion Rate Trend', 'Spend Distribution'),
    specs=[[{"type": "scatter"}, {"type": "bar"}],
           [{"type": "scatter"}, {"type": "pie"}]]
)

# Chart 1: Daily Revenue
dates = pd.date_range('2024-01-01', periods=30, freq='D')
revenue = [45000 + np.random.randn()*5000 for _ in range(30)]
fig.add_trace(
    go.Scatter(x=dates, y=revenue, mode='lines+markers', name='Revenue'),
    row=1, col=1
)

# Chart 2: ROAS by Channel
channels = ['Meta', 'Google', 'TikTok', 'Email', 'Organic']
roas = [3.2, 4.1, 2.8, 8.5, 12.0]
fig.add_trace(
    go.Bar(x=channels, y=roas, name='ROAS', marker_color='steelblue'),
    row=1, col=2
)

# Chart 3: Conversion Rate
conv_rate = [2.1 + np.random.randn()*0.3 for _ in range(30)]
fig.add_trace(
    go.Scatter(x=dates, y=conv_rate, mode='lines', name='Conv Rate %',
               line=dict(color='green')),
    row=2, col=1
)

# Chart 4: Spend Distribution
spend = [25000, 35000, 15000, 5000, 0]
fig.add_trace(
    go.Pie(labels=channels, values=spend, name='Spend'),
    row=2, col=2
)

fig.update_layout(height=800, title_text="Marketing Performance Dashboard")
fig.show()
```

### 4. Time Series with Annotations

```python
import plotly.graph_objects as go
import pandas as pd

# Revenue with campaign annotations
dates = pd.date_range('2024-01-01', periods=90, freq='D')
revenue = [50000 + i*100 + np.random.randn()*3000 for i in range(90)]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=dates, y=revenue,
    mode='lines',
    name='Daily Revenue',
    line=dict(color='#2E86AB', width=2)
))

# Add campaign annotations
campaigns = [
    ('2024-01-15', 'Email Campaign Launch'),
    ('2024-02-01', 'Meta Ads Scale'),
    ('2024-02-20', 'Flash Sale'),
    ('2024-03-10', 'New Product Launch')
]

for date, label in campaigns:
    fig.add_vline(x=date, line_dash="dash", line_color="gray")
    fig.add_annotation(x=date, y=max(revenue)*1.05, text=label,
                       showarrow=False, textangle=-45)

fig.update_layout(
    title="Revenue Trend with Campaign Events",
    xaxis_title="Date",
    yaxis_title="Revenue ($)"
)
fig.show()
```

### 5. Channel Attribution Sankey Diagram

```python
import plotly.graph_objects as go

# Attribution flow data
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=["Paid Social", "Paid Search", "Organic", "Email",
               "First Touch", "Multi-Touch", "Last Touch",
               "Conversion"],
        color=["#3366cc", "#dc3912", "#ff9900", "#109618",
               "#990099", "#0099c6", "#dd4477", "#66aa00"]
    ),
    link=dict(
        source=[0, 0, 1, 1, 2, 2, 3, 3, 4, 5, 6],
        target=[4, 5, 5, 6, 4, 5, 5, 6, 7, 7, 7],
        value=[300, 200, 250, 150, 180, 120, 100, 80, 480, 570, 230]
    )
)])

fig.update_layout(title_text="Marketing Attribution Flow", font_size=12)
fig.show()
```

### 6. A/B Test Results Visualization

```python
import plotly.graph_objects as go
import numpy as np

# A/B test results with confidence intervals
variants = ['Control', 'Variant A', 'Variant B', 'Variant C']
conversion_rates = [3.2, 3.8, 4.1, 3.5]
ci_lower = [2.9, 3.4, 3.7, 3.1]
ci_upper = [3.5, 4.2, 4.5, 3.9]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=variants,
    y=conversion_rates,
    error_y=dict(
        type='data',
        symmetric=False,
        array=[u - c for u, c in zip(ci_upper, conversion_rates)],
        arrayminus=[c - l for l, c in zip(ci_lower, conversion_rates)]
    ),
    marker_color=['gray', 'steelblue', 'green', 'steelblue']
))

# Add baseline reference
fig.add_hline(y=conversion_rates[0], line_dash="dash",
              annotation_text="Control Baseline")

fig.update_layout(
    title="A/B Test Results: Conversion Rate by Variant",
    xaxis_title="Variant",
    yaxis_title="Conversion Rate (%)",
    yaxis=dict(range=[0, 5])
)
fig.show()
```

## Installation

```bash
uv pip install plotly pandas numpy
```

## Quick Start

```python
import plotly.express as px
import pandas as pd

# Quick visualization
df = pd.read_csv('marketing_data.csv')

# Scatter plot of spend vs revenue by channel
fig = px.scatter(df, x='spend', y='revenue', color='channel',
                 size='conversions', hover_data=['campaign_name'],
                 title='Campaign Performance: Spend vs Revenue')
fig.show()
```

## References

- [Plotly Python Documentation](https://plotly.com/python/)
- [Plotly Express](https://plotly.com/python/plotly-express/)

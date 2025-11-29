---
name: streamlit-dashboards
description: "Interactive marketing dashboards. Real-time metrics, KPI tracking, campaign monitoring, executive reports, customer analytics, multi-page apps, data exploration."
---

# Streamlit for Marketing Dashboards

## Overview

Streamlit enables rapid development of interactive data apps and dashboards for marketing teams. This skill covers building real-time marketing dashboards, KPI trackers, campaign monitors, customer analytics apps, executive reports, and interactive data exploration tools.

## When to Use This Skill

- Building real-time marketing performance dashboards
- Creating interactive reports for executives
- Developing self-service analytics tools for marketing teams
- Prototyping data apps quickly
- Building campaign monitoring tools
- Creating customer segmentation explorers
- Developing A/B test analysis dashboards
- Building attribution model visualizations

## Core Capabilities

### 1. Real-Time Marketing Dashboard

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configure page
st.set_page_config(
    page_title="Marketing Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Marketing Performance Dashboard")
st.markdown("Real-time marketing metrics and campaign performance")

# Sidebar filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Date Range",
    value=(datetime.now() - timedelta(days=30), datetime.now())
)
channel_filter = st.sidebar.multiselect(
    "Channels",
    options=["Meta", "Google", "TikTok", "Email", "Organic"],
    default=["Meta", "Google", "Email"]
)

# Load data (simulated)
@st.cache_data
def load_marketing_data():
    return pd.DataFrame({
        'date': pd.date_range(start='2024-01-01', periods=90, freq='D'),
        'channel': ['Meta', 'Google', 'TikTok'] * 30,
        'impressions': [10000 + i*100 for i in range(90)],
        'clicks': [500 + i*5 for i in range(90)],
        'conversions': [50 + i for i in range(90)],
        'spend': [1000 + i*10 for i in range(90)],
        'revenue': [5000 + i*50 for i in range(90)]
    })

df = load_marketing_data()

# Filter data
df_filtered = df[df['channel'].isin(channel_filter)]

# Key metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_spend = df_filtered['spend'].sum()
    st.metric(
        label="Total Spend",
        value=f"${total_spend:,.0f}",
        delta=f"{((total_spend / df_filtered['spend'].sum() - 1) * 100):.1f}%"
    )

with col2:
    total_revenue = df_filtered['revenue'].sum()
    st.metric(
        label="Total Revenue",
        value=f"${total_revenue:,.0f}",
        delta=f"{((total_revenue / df_filtered['revenue'].sum() - 1) * 100):.1f}%"
    )

with col3:
    roas = total_revenue / total_spend if total_spend > 0 else 0
    st.metric(
        label="ROAS",
        value=f"{roas:.2f}x",
        delta=f"{((roas / 3.5 - 1) * 100):.1f}%"
    )

with col4:
    conversions = df_filtered['conversions'].sum()
    st.metric(
        label="Conversions",
        value=f"{conversions:,.0f}",
        delta=f"{((conversions / df_filtered['conversions'].sum() - 1) * 100):.1f}%"
    )

# Charts
st.subheader("Performance Trends")

col1, col2 = st.columns(2)

with col1:
    # Revenue over time
    fig_revenue = px.line(
        df_filtered,
        x='date',
        y='revenue',
        color='channel',
        title='Revenue by Channel Over Time'
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

with col2:
    # ROAS by channel
    channel_metrics = df_filtered.groupby('channel').agg({
        'spend': 'sum',
        'revenue': 'sum'
    }).reset_index()
    channel_metrics['roas'] = channel_metrics['revenue'] / channel_metrics['spend']

    fig_roas = px.bar(
        channel_metrics,
        x='channel',
        y='roas',
        title='ROAS by Channel',
        color='roas',
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig_roas, use_container_width=True)

# Conversion funnel
st.subheader("Conversion Funnel")
funnel_data = df_filtered.agg({
    'impressions': 'sum',
    'clicks': 'sum',
    'conversions': 'sum'
})

fig_funnel = go.Figure(go.Funnel(
    y=['Impressions', 'Clicks', 'Conversions'],
    x=[funnel_data['impressions'], funnel_data['clicks'], funnel_data['conversions']],
    textinfo="value+percent initial"
))
st.plotly_chart(fig_funnel, use_container_width=True)

# Data table
if st.checkbox("Show Raw Data"):
    st.dataframe(df_filtered)
```

### 2. Campaign Performance Analyzer

```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🎯 Campaign Performance Analyzer")

# File upload
uploaded_file = st.file_uploader("Upload Campaign Data (CSV)", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Campaign selector
    campaigns = df['campaign_name'].unique()
    selected_campaign = st.selectbox("Select Campaign", campaigns)

    # Filter to selected campaign
    campaign_data = df[df['campaign_name'] == selected_campaign]

    # Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Impressions", f"{campaign_data['impressions'].sum():,.0f}")

    with col2:
        ctr = (campaign_data['clicks'].sum() / campaign_data['impressions'].sum()) * 100
        st.metric("CTR", f"{ctr:.2f}%")

    with col3:
        cpa = campaign_data['spend'].sum() / campaign_data['conversions'].sum()
        st.metric("CPA", f"${cpa:.2f}")

    # Performance over time
    st.subheader("Daily Performance")
    fig = px.line(
        campaign_data,
        x='date',
        y=['impressions', 'clicks', 'conversions'],
        title=f"Performance Trends - {selected_campaign}"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Ad creative breakdown
    st.subheader("Ad Creative Performance")
    creative_perf = campaign_data.groupby('ad_creative').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'spend': 'sum'
    }).reset_index()

    creative_perf['ctr'] = (creative_perf['clicks'] / creative_perf['impressions']) * 100
    creative_perf['conversion_rate'] = (creative_perf['conversions'] / creative_perf['clicks']) * 100

    st.dataframe(
        creative_perf.style.format({
            'impressions': '{:,.0f}',
            'clicks': '{:,.0f}',
            'conversions': '{:,.0f}',
            'spend': '${:,.2f}',
            'ctr': '{:.2f}%',
            'conversion_rate': '{:.2f}%'
        }),
        use_container_width=True
    )
```

### 3. Customer Segmentation Explorer

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("👥 Customer Segmentation Explorer")

# Load customer data
@st.cache_data
def load_customer_data():
    return pd.DataFrame({
        'customer_id': range(1000),
        'recency': [i % 365 for i in range(1000)],
        'frequency': [(i % 20) + 1 for i in range(1000)],
        'monetary': [(i % 50) * 100 + 500 for i in range(1000)],
        'segment': ['Champions', 'Loyal', 'At Risk', 'Lost', 'New'] * 200
    })

df = load_customer_data()

# Segment selector
st.sidebar.header("Filters")
selected_segments = st.sidebar.multiselect(
    "Customer Segments",
    options=df['segment'].unique(),
    default=df['segment'].unique()
)

# Filter data
df_filtered = df[df['segment'].isin(selected_segments)]

# Segment overview
st.subheader("Segment Overview")
segment_summary = df_filtered.groupby('segment').agg({
    'customer_id': 'count',
    'monetary': 'sum',
    'frequency': 'mean'
}).reset_index()
segment_summary.columns = ['Segment', 'Customers', 'Total Revenue', 'Avg Frequency']

col1, col2 = st.columns(2)

with col1:
    # Segment distribution
    fig_dist = px.pie(
        segment_summary,
        values='Customers',
        names='Segment',
        title='Customer Distribution by Segment'
    )
    st.plotly_chart(fig_dist, use_container_width=True)

with col2:
    # Revenue by segment
    fig_revenue = px.bar(
        segment_summary,
        x='Segment',
        y='Total Revenue',
        title='Revenue by Customer Segment',
        color='Total Revenue',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

# RFM Analysis
st.subheader("RFM Analysis")
fig_rfm = px.scatter_3d(
    df_filtered,
    x='recency',
    y='frequency',
    z='monetary',
    color='segment',
    title='3D RFM Segmentation',
    labels={'recency': 'Recency (days)', 'frequency': 'Frequency', 'monetary': 'Monetary ($)'}
)
st.plotly_chart(fig_rfm, use_container_width=True)

# Segment details
st.subheader("Segment Details")
selected_segment_detail = st.selectbox("Select Segment for Details", selected_segments)
segment_data = df_filtered[df_filtered['segment'] == selected_segment_detail]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Customers", f"{len(segment_data):,}")
with col2:
    st.metric("Avg Monetary", f"${segment_data['monetary'].mean():,.2f}")
with col3:
    st.metric("Avg Frequency", f"{segment_data['frequency'].mean():.1f}")

# Show customer list
if st.checkbox("Show Customer List"):
    st.dataframe(segment_data)
```

### 4. A/B Test Results Dashboard

```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scipy import stats

st.title("🧪 A/B Test Results Dashboard")

# Test configuration
st.sidebar.header("Test Configuration")
test_name = st.sidebar.text_input("Test Name", "Homepage CTA Button Color")
alpha = st.sidebar.slider("Significance Level (α)", 0.01, 0.10, 0.05, 0.01)

# Input data
col1, col2 = st.columns(2)

with col1:
    st.subheader("Control (A)")
    control_visitors = st.number_input("Visitors (Control)", value=10000, step=100)
    control_conversions = st.number_input("Conversions (Control)", value=250, step=10)
    control_rate = (control_conversions / control_visitors) * 100 if control_visitors > 0 else 0

with col2:
    st.subheader("Variant (B)")
    variant_visitors = st.number_input("Visitors (Variant)", value=10000, step=100)
    variant_conversions = st.number_input("Conversions (Variant)", value=310, step=10)
    variant_rate = (variant_conversions / variant_visitors) * 100 if variant_visitors > 0 else 0

# Calculate statistical significance
if st.button("Calculate Results"):
    # Chi-square test
    observed = [[control_conversions, control_visitors - control_conversions],
               [variant_conversions, variant_visitors - variant_conversions]]

    chi2, p_value, dof, expected = stats.chi2_contingency(observed)

    # Results
    st.subheader("Test Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Control Conversion Rate", f"{control_rate:.2f}%")

    with col2:
        st.metric("Variant Conversion Rate", f"{variant_rate:.2f}%")

    with col3:
        lift = ((variant_rate - control_rate) / control_rate) * 100 if control_rate > 0 else 0
        st.metric("Lift", f"{lift:+.2f}%")

    # Statistical significance
    st.subheader("Statistical Significance")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("P-Value", f"{p_value:.4f}")

    with col2:
        is_significant = p_value < alpha
        if is_significant:
            st.success(f"✅ Result is statistically significant (p < {alpha})")
        else:
            st.warning(f"⚠️ Result is NOT statistically significant (p ≥ {alpha})")

    # Visualization
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Control',
        x=['Conversion Rate'],
        y=[control_rate],
        error_y=dict(
            type='data',
            array=[0.5],  # Simplified confidence interval
            visible=True
        ),
        marker_color='steelblue'
    ))

    fig.add_trace(go.Bar(
        name='Variant',
        x=['Conversion Rate'],
        y=[variant_rate],
        error_y=dict(
            type='data',
            array=[0.5],
            visible=True
        ),
        marker_color='green' if is_significant else 'orange'
    ))

    fig.update_layout(
        title='Conversion Rate Comparison',
        yaxis_title='Conversion Rate (%)',
        barmode='group'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Recommendation
    st.subheader("Recommendation")
    if is_significant and lift > 0:
        st.success(f"🚀 **Implement Variant B** - Statistically significant improvement of {lift:.2f}%")
    elif is_significant and lift < 0:
        st.error(f"❌ **Keep Control A** - Variant B performs significantly worse ({lift:.2f}%)")
    else:
        st.info("⏸️ **Continue Testing** - No statistically significant difference detected yet")
```

### 5. Attribution Model Dashboard

```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("📈 Marketing Attribution Dashboard")

# Sample customer journey data
@st.cache_data
def load_journey_data():
    return pd.DataFrame({
        'customer_id': [1, 1, 1, 2, 2, 3, 3, 3, 3],
        'touchpoint': ['Paid Search', 'Email', 'Direct', 'Social', 'Email', 'Organic', 'Email', 'Paid Search', 'Direct'],
        'timestamp': pd.date_range('2024-01-01', periods=9, freq='D'),
        'converted': [0, 0, 1, 0, 1, 0, 0, 0, 1]
    })

df = load_journey_data()

# Attribution model selector
st.sidebar.header("Attribution Settings")
model = st.sidebar.selectbox(
    "Attribution Model",
    ["First Touch", "Last Touch", "Linear", "Time Decay", "U-Shaped"]
)

def calculate_attribution(journeys, model='last_touch'):
    """
    Calculate attribution based on selected model
    """
    attribution = {}

    for customer_id in journeys['customer_id'].unique():
        customer_journey = journeys[journeys['customer_id'] == customer_id]
        converted = customer_journey['converted'].iloc[-1] == 1

        if converted:
            touchpoints = customer_journey['touchpoint'].tolist()
            n = len(touchpoints)

            if model == 'First Touch':
                weights = [1] + [0] * (n - 1)
            elif model == 'Last Touch':
                weights = [0] * (n - 1) + [1]
            elif model == 'Linear':
                weights = [1/n] * n
            elif model == 'Time Decay':
                weights = [2**i for i in range(n)]
                total = sum(weights)
                weights = [w/total for w in weights]
            elif model == 'U-Shaped':
                if n == 1:
                    weights = [1]
                elif n == 2:
                    weights = [0.5, 0.5]
                else:
                    weights = [0.4] + [0.2/(n-2)] * (n-2) + [0.4]

            for touchpoint, weight in zip(touchpoints, weights):
                attribution[touchpoint] = attribution.get(touchpoint, 0) + weight

    return attribution

# Calculate attribution
attribution_scores = calculate_attribution(df, model)
attribution_df = pd.DataFrame(list(attribution_scores.items()), columns=['Channel', 'Conversions'])
attribution_df = attribution_df.sort_values('Conversions', ascending=False)

# Display results
st.subheader(f"{model} Attribution")

col1, col2 = st.columns(2)

with col1:
    # Attribution chart
    fig = go.Figure(data=[
        go.Bar(x=attribution_df['Channel'], y=attribution_df['Conversions'])
    ])
    fig.update_layout(
        title=f'Conversions by Channel ({model})',
        xaxis_title='Channel',
        yaxis_title='Attributed Conversions'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Pie chart
    fig_pie = go.Figure(data=[
        go.Pie(labels=attribution_df['Channel'], values=attribution_df['Conversions'])
    ])
    fig_pie.update_layout(title='Attribution Distribution')
    st.plotly_chart(fig_pie, use_container_width=True)

# Show attribution table
st.subheader("Attribution Breakdown")
st.dataframe(attribution_df.style.format({'Conversions': '{:.2f}'}), use_container_width=True)

# Customer journeys
st.subheader("Sample Customer Journeys")
if st.checkbox("Show Customer Journeys"):
    for customer_id in df['customer_id'].unique():
        journey = df[df['customer_id'] == customer_id]
        converted = journey['converted'].iloc[-1] == 1
        status = "✅ Converted" if converted else "❌ Not Converted"

        with st.expander(f"Customer {customer_id} - {status}"):
            st.write(" → ".join(journey['touchpoint'].tolist()))
            st.dataframe(journey)
```

### 6. Multi-Page App with Navigation

```python
import streamlit as st

# Configure page
st.set_page_config(
    page_title="Marketing Hub",
    page_icon="📊",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("Marketing Hub")
page = st.sidebar.radio(
    "Navigate to:",
    ["Dashboard", "Campaigns", "Customers", "Analytics", "Settings"]
)

# Page routing
if page == "Dashboard":
    st.title("📊 Marketing Dashboard")
    st.write("Overview of all marketing metrics")
    # Dashboard content here

elif page == "Campaigns":
    st.title("🎯 Campaign Management")
    st.write("Manage and monitor campaigns")
    # Campaign content here

elif page == "Customers":
    st.title("👥 Customer Analytics")
    st.write("Customer segmentation and analysis")
    # Customer content here

elif page == "Analytics":
    st.title("📈 Advanced Analytics")
    st.write("Deep-dive analytics and reports")
    # Analytics content here

elif page == "Settings":
    st.title("⚙️ Settings")
    st.write("Configure dashboard settings")
    # Settings content here
```

## Installation

```bash
uv pip install streamlit pandas plotly scipy numpy
```

## Quick Start

```python
import streamlit as st
import pandas as pd

# Create simple dashboard
st.title("My Marketing Dashboard")

# Add widgets
name = st.text_input("Campaign Name")
budget = st.slider("Budget", 0, 10000, 5000)

# Display data
df = pd.DataFrame({'metric': ['impressions', 'clicks'], 'value': [10000, 500]})
st.dataframe(df)

# Run with: streamlit run dashboard.py
```

## Running Streamlit Apps

```bash
# Run app
streamlit run your_app.py

# Run on specific port
streamlit run your_app.py --server.port 8080

# Run with auto-reload
streamlit run your_app.py --server.runOnSave true
```

## Best Practices

1. **Use caching** - Cache data loading with `@st.cache_data`
2. **Session state** - Store user state with `st.session_state`
3. **Layout** - Use columns and containers for better organization
4. **Performance** - Minimize reruns, use callbacks
5. **Mobile-friendly** - Design works on different screen sizes
6. **Error handling** - Add try/except blocks for data loading
7. **Documentation** - Add helpful text and tooltips

## Advanced Features

- **Authentication** - Add login with streamlit-authenticator
- **Database integration** - Connect to SQL, MongoDB, etc.
- **Real-time updates** - Use `st.experimental_rerun()`
- **File downloads** - Export data as CSV/Excel
- **Sharing** - Deploy to Streamlit Cloud for free

## References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [Streamlit Components](https://streamlit.io/components)
- [Streamlit Cloud](https://streamlit.io/cloud)

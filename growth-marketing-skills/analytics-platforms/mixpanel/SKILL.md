---
name: mixpanel
description: "Mixpanel product analytics. User behavior tracking, funnel analysis, retention analysis, cohort analysis, A/B test analysis, API integration."
---

# Mixpanel Product Analytics

## Overview

Mixpanel is a product analytics platform for tracking user behavior and product engagement. This skill covers event tracking, funnel analysis, retention, cohorts, and accessing data via the Mixpanel API.

## When to Use This Skill

- Analyzing user behavior and engagement
- Building conversion funnels
- Measuring feature adoption
- Retention and cohort analysis
- User segmentation
- A/B test analysis in product

## Core Capabilities

### 1. Mixpanel API Setup

```python
import requests
import pandas as pd
from datetime import datetime, timedelta
import json

class MixpanelClient:
    def __init__(self, project_id, service_account, service_secret):
        self.project_id = project_id
        self.auth = (service_account, service_secret)
        self.base_url = "https://mixpanel.com/api/2.0"

    def query(self, endpoint, params):
        response = requests.get(
            f"{self.base_url}/{endpoint}",
            auth=self.auth,
            params=params
        )
        response.raise_for_status()
        return response.json()

    def jql_query(self, script):
        """Execute a JQL query"""
        response = requests.post(
            f"{self.base_url}/jql",
            auth=self.auth,
            data={"script": script}
        )
        response.raise_for_status()
        return response.json()

# Initialize client
client = MixpanelClient(
    project_id="YOUR_PROJECT_ID",
    service_account="YOUR_SERVICE_ACCOUNT",
    service_secret="YOUR_SERVICE_SECRET"
)
```

### 2. Event Analytics

```python
# Get event data using JQL
script = """
function main() {
    return Events({
        from_date: "2024-01-01",
        to_date: "2024-01-31",
        event_selectors: [
            {event: "Page View"},
            {event: "Sign Up"},
            {event: "Purchase"}
        ]
    })
    .groupByUser(["event"])
    .reduce(mixpanel.reducer.count());
}
"""

results = client.jql_query(script)

# Process results
df = pd.DataFrame(results)
print("Event Counts by User:")
print(df.head())

# Event trends over time
script = """
function main() {
    return Events({
        from_date: "2024-01-01",
        to_date: "2024-01-31"
    })
    .groupBy(["name"], mixpanel.reducer.count())
    .sortDesc("value");
}
"""

event_counts = client.jql_query(script)
df = pd.DataFrame(event_counts)
print("\nTop Events:")
print(df.head(20))
```

### 3. Funnel Analysis

```python
# Define and analyze funnel
script = """
function main() {
    return Events({
        from_date: "2024-01-01",
        to_date: "2024-01-31"
    })
    .funnel([
        {event: "Page View"},
        {event: "View Product"},
        {event: "Add to Cart"},
        {event: "Begin Checkout"},
        {event: "Purchase"}
    ], {
        conversion_window_days: 7,
        count_type: "unique"
    });
}
"""

funnel_results = client.jql_query(script)

# Process funnel results
stages = ["Page View", "View Product", "Add to Cart", "Begin Checkout", "Purchase"]
print("\nConversion Funnel:")
for i, (stage, data) in enumerate(zip(stages, funnel_results)):
    count = data.get('count', 0)
    if i > 0:
        prev_count = funnel_results[i-1].get('count', 1)
        rate = count / prev_count * 100 if prev_count > 0 else 0
        print(f"  {stage}: {count:,} ({rate:.1f}% conversion)")
    else:
        print(f"  {stage}: {count:,}")

# Overall conversion rate
if funnel_results:
    overall = funnel_results[-1].get('count', 0) / funnel_results[0].get('count', 1) * 100
    print(f"\nOverall Conversion: {overall:.2f}%")
```

### 4. Retention Analysis

```python
# Retention cohort analysis
script = """
function main() {
    return Events({
        from_date: "2024-01-01",
        to_date: "2024-03-31"
    })
    .retention({
        born_event: "Sign Up",
        return_event: "Login",
        retention_window: "day",
        retention_periods: [1, 7, 14, 30, 60, 90]
    });
}
"""

retention_results = client.jql_query(script)

# Process retention data
print("\nRetention Rates:")
for period, data in retention_results.items():
    retained = data.get('retained', 0)
    total = data.get('total', 1)
    rate = retained / total * 100 if total > 0 else 0
    print(f"  Day {period}: {rate:.1f}% ({retained:,} / {total:,})")

# Weekly cohort retention
script = """
function main() {
    return Events({
        from_date: "2024-01-01",
        to_date: "2024-03-31"
    })
    .groupByUser([
        mixpanel.numeric_bucket("time", mixpanel.weekly_buckets)
    ])
    .filter(function(row) {
        return row.key[0] !== undefined;
    })
    .retention({
        born_event: "Sign Up",
        return_event: "Any Event",
        retention_window: "week",
        group_by: "cohort"
    });
}
"""

cohort_retention = client.jql_query(script)
df = pd.DataFrame(cohort_retention)
print("\nCohort Retention Table:")
print(df)
```

### 5. User Segmentation

```python
# Segment users by behavior
script = """
function main() {
    return People()
    .filter(function(user) {
        return user.properties.$last_seen !== undefined;
    })
    .groupBy(
        [
            mixpanel.numeric_bucket("properties.total_purchases",
                [0, 1, 5, 10, 50, 100])
        ],
        mixpanel.reducer.count()
    );
}
"""

segments = client.jql_query(script)

# Power users analysis
script = """
function main() {
    return Events({
        from_date: "2024-01-01",
        to_date: "2024-01-31"
    })
    .groupByUser(mixpanel.reducer.count())
    .filter(function(row) {
        return row.value > 50;  // Power users: 50+ events
    })
    .reduce(mixpanel.reducer.count());
}
"""

power_users = client.jql_query(script)
print(f"\nPower Users (50+ events): {power_users}")

# Feature adoption
script = """
function main() {
    return Events({
        from_date: "2024-01-01",
        to_date: "2024-01-31",
        event_selectors: [{event: "Feature Used"}]
    })
    .groupBy(["properties.feature_name"], mixpanel.reducer.count())
    .sortDesc("value");
}
"""

feature_adoption = client.jql_query(script)
df = pd.DataFrame(feature_adoption)
print("\nFeature Adoption:")
print(df.head(10))
```

### 6. Export Raw Data

```python
# Export raw events for analysis
def export_events(client, from_date, to_date, event=None):
    """Export raw event data from Mixpanel"""
    params = {
        "from_date": from_date,
        "to_date": to_date
    }
    if event:
        params["event"] = json.dumps([event])

    # Use data export API
    response = requests.get(
        "https://data.mixpanel.com/api/2.0/export",
        auth=client.auth,
        params=params,
        stream=True
    )

    events = []
    for line in response.iter_lines():
        if line:
            events.append(json.loads(line))

    return pd.DataFrame(events)

# Export purchases
purchases_df = export_events(client, "2024-01-01", "2024-01-31", "Purchase")
print(f"\nExported {len(purchases_df)} purchase events")
print(purchases_df.head())

# Analyze exported data
if 'properties' in purchases_df.columns:
    purchases_df = pd.concat([
        purchases_df.drop(['properties'], axis=1),
        pd.json_normalize(purchases_df['properties'])
    ], axis=1)

    # Revenue analysis
    total_revenue = purchases_df['revenue'].sum()
    avg_order = purchases_df['revenue'].mean()
    print(f"\nTotal Revenue: ${total_revenue:,.2f}")
    print(f"Average Order Value: ${avg_order:.2f}")
```

### 7. A/B Test Analysis

```python
# Analyze experiment results
script = """
function main() {
    return Events({
        from_date: "2024-01-15",
        to_date: "2024-02-15",
        event_selectors: [{event: "Experiment Viewed"}]
    })
    .filter(function(e) {
        return e.properties.experiment_name === "checkout_redesign";
    })
    .groupBy(["properties.variant"], [
        mixpanel.reducer.count(),
        mixpanel.reducer.numeric("properties.converted"),
        mixpanel.reducer.sum("properties.revenue")
    ]);
}
"""

experiment_results = client.jql_query(script)

# Calculate test metrics
for variant_data in experiment_results:
    variant = variant_data['key'][0]
    participants = variant_data['value'][0]
    conversions = variant_data['value'][1]
    revenue = variant_data['value'][2]

    conv_rate = conversions / participants * 100 if participants > 0 else 0
    arpu = revenue / participants if participants > 0 else 0

    print(f"\nVariant: {variant}")
    print(f"  Participants: {participants:,}")
    print(f"  Conversions: {conversions:,} ({conv_rate:.2f}%)")
    print(f"  Revenue: ${revenue:,.2f}")
    print(f"  ARPU: ${arpu:.2f}")
```

## Installation

```bash
uv pip install requests pandas
```

## Authentication

1. Go to Mixpanel Project Settings → Service Accounts
2. Create a new service account with appropriate permissions
3. Note down the service account username and secret

## Quick Start

```python
import requests

# Quick event query
response = requests.get(
    "https://mixpanel.com/api/2.0/events/top",
    auth=("service_account", "secret"),
    params={
        "type": "general",
        "limit": 10
    }
)

print(response.json())
```

## Key Concepts

- **Events**: User actions tracked with properties
- **User Profiles**: Persistent user data and attributes
- **Funnels**: Ordered sequence of events measuring conversion
- **Retention**: Returning user behavior over time
- **Cohorts**: Groups of users segmented by behavior

## References

- [Mixpanel API Reference](https://developer.mixpanel.com/reference)
- [JQL Query Language](https://developer.mixpanel.com/docs/jql-overview)
- [Data Export API](https://developer.mixpanel.com/reference/raw-data-export)

---
name: prophet-forecasting
description: "Time series forecasting for marketing. Revenue forecasting, demand prediction, seasonality modeling, campaign impact analysis, growth projections."
---

# Prophet for Marketing Forecasting

## Overview

Prophet is Facebook's time series forecasting library, ideal for marketing metrics with strong seasonal patterns and holiday effects. This skill covers revenue forecasting, demand prediction, campaign impact quantification, and growth projections.

## When to Use This Skill

- Forecasting revenue and sales
- Predicting traffic and conversion trends
- Modeling seasonality in marketing metrics
- Quantifying campaign lift and impact
- Budget planning and goal setting
- Demand forecasting for inventory

## Core Capabilities

### 1. Revenue Forecasting

```python
from prophet import Prophet
import pandas as pd

# Prepare data (Prophet requires 'ds' and 'y' columns)
df = pd.read_csv('daily_revenue.csv')
df = df.rename(columns={'date': 'ds', 'revenue': 'y'})

# Initialize and fit model
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    seasonality_mode='multiplicative'  # Good for growing businesses
)

model.fit(df)

# Create future dataframe
future = model.make_future_dataframe(periods=90)  # 90 days ahead

# Forecast
forecast = model.predict(future)

# View forecast
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30))

# Plot
fig1 = model.plot(forecast)
fig2 = model.plot_components(forecast)
```

### 2. Adding Holiday Effects

```python
from prophet import Prophet
import pandas as pd

# Define marketing holidays and events
holidays = pd.DataFrame({
    'holiday': [
        'black_friday', 'cyber_monday', 'christmas_sale',
        'new_year_sale', 'valentines', 'summer_sale',
        'prime_day', 'labor_day_sale', 'memorial_day_sale'
    ] * 3,  # Repeat for multiple years
    'ds': pd.to_datetime([
        # 2022
        '2022-11-25', '2022-11-28', '2022-12-20',
        '2022-01-01', '2022-02-14', '2022-07-01',
        '2022-07-12', '2022-09-05', '2022-05-30',
        # 2023
        '2023-11-24', '2023-11-27', '2023-12-20',
        '2023-01-01', '2023-02-14', '2023-07-01',
        '2023-07-11', '2023-09-04', '2023-05-29',
        # 2024
        '2024-11-29', '2024-12-02', '2024-12-20',
        '2024-01-01', '2024-02-14', '2024-07-01',
        '2024-07-16', '2024-09-02', '2024-05-27'
    ]),
    'lower_window': [-1] * 27,  # Effect starts 1 day before
    'upper_window': [1] * 27    # Effect lasts 1 day after
})

# Initialize model with holidays
model = Prophet(
    holidays=holidays,
    yearly_seasonality=True,
    weekly_seasonality=True
)

model.fit(df)
forecast = model.predict(future)

# See holiday effects
print(forecast[['ds', 'black_friday', 'cyber_monday', 'christmas_sale']].dropna())
```

### 3. Campaign Impact Modeling with Regressors

```python
from prophet import Prophet
import pandas as pd

# Add campaign indicators as regressors
df['meta_campaign'] = (df['ds'] >= '2024-01-15') & (df['ds'] <= '2024-02-15')
df['meta_campaign'] = df['meta_campaign'].astype(int)

df['email_blast'] = df['ds'].isin(['2024-01-20', '2024-02-01', '2024-02-15'])
df['email_blast'] = df['email_blast'].astype(int)

df['tv_campaign'] = (df['ds'] >= '2024-02-01') & (df['ds'] <= '2024-03-01')
df['tv_campaign'] = df['tv_campaign'].astype(int)

# Initialize model with regressors
model = Prophet()
model.add_regressor('meta_campaign')
model.add_regressor('email_blast')
model.add_regressor('tv_campaign')

model.fit(df)

# For forecasting, need to specify future regressor values
future = model.make_future_dataframe(periods=30)
future['meta_campaign'] = 0  # No campaign planned
future['email_blast'] = future['ds'].isin(['2024-03-01', '2024-03-15']).astype(int)
future['tv_campaign'] = 0

forecast = model.predict(future)

# Extract campaign effects
campaign_effects = model.params['beta']
print("Campaign Effects:")
for name, effect in zip(['meta_campaign', 'email_blast', 'tv_campaign'],
                        campaign_effects[0]):
    print(f"  {name}: {effect:.2f}")
```

### 4. Multiple Metrics Forecasting

```python
from prophet import Prophet
import pandas as pd

# Forecast multiple metrics
metrics = ['revenue', 'sessions', 'conversions', 'new_customers']
forecasts = {}

for metric in metrics:
    # Prepare data
    metric_df = df[['date', metric]].copy()
    metric_df.columns = ['ds', 'y']

    # Fit model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        changepoint_prior_scale=0.05  # Less flexible for stability
    )
    model.fit(metric_df)

    # Forecast
    future = model.make_future_dataframe(periods=90)
    forecast = model.predict(future)

    forecasts[metric] = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    print(f"\n{metric.upper()} - Next 30 Days:")
    print(f"  Predicted Total: {forecast['yhat'].tail(30).sum():,.0f}")
    print(f"  Lower Bound: {forecast['yhat_lower'].tail(30).sum():,.0f}")
    print(f"  Upper Bound: {forecast['yhat_upper'].tail(30).sum():,.0f}")
```

### 5. Trend Changepoint Detection

```python
from prophet import Prophet
import pandas as pd

# Detect trend changes (e.g., from growth initiatives)
model = Prophet(
    changepoint_prior_scale=0.1,  # More sensitive to changes
    n_changepoints=25  # Number of potential changepoints
)

model.fit(df)
forecast = model.predict(future)

# Get changepoint dates
changepoints = model.changepoints
print("Detected Trend Changepoints:")
for cp in changepoints:
    print(f"  {cp.strftime('%Y-%m-%d')}")

# Visualize
from prophet.plot import add_changepoints_to_plot
fig = model.plot(forecast)
add_changepoints_to_plot(fig.gca(), model, forecast)
```

### 6. Cross-Validation and Accuracy

```python
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics

# Fit model
model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
model.fit(df)

# Cross-validation
# - Initial training period: 365 days
# - Forecast horizon: 30 days
# - Between cutoffs: 30 days
df_cv = cross_validation(
    model,
    initial='365 days',
    period='30 days',
    horizon='30 days'
)

# Calculate performance metrics
metrics = performance_metrics(df_cv)
print("\nForecast Accuracy Metrics:")
print(f"  MAPE: {metrics['mape'].mean():.2%}")
print(f"  MAE: {metrics['mae'].mean():,.2f}")
print(f"  RMSE: {metrics['rmse'].mean():,.2f}")

# Plot accuracy by horizon
from prophet.plot import plot_cross_validation_metric
fig = plot_cross_validation_metric(df_cv, metric='mape')
```

## Installation

```bash
uv pip install prophet pandas
```

## Quick Start

```python
from prophet import Prophet
import pandas as pd

# Load data
df = pd.read_csv('metrics.csv')
df = df.rename(columns={'date': 'ds', 'revenue': 'y'})

# Fit and forecast
model = Prophet()
model.fit(df)

future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Plot
model.plot(forecast)
model.plot_components(forecast)
```

## Best Practices

1. **Data preparation** - Prophet handles missing data, but ensure dates are continuous
2. **Seasonality mode** - Use 'multiplicative' for metrics that scale with the trend
3. **Changepoint sensitivity** - Lower `changepoint_prior_scale` for more stable forecasts
4. **Validation** - Always use cross-validation to assess forecast accuracy
5. **Uncertainty intervals** - Report prediction intervals, not just point estimates

## References

- [Prophet Documentation](https://facebook.github.io/prophet/)
- [Prophet Paper](https://peerj.com/preprints/3190/)

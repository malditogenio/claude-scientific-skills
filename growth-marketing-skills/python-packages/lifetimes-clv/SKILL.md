---
name: lifetimes-clv
description: "Customer Lifetime Value modeling. BG/NBD models, Gamma-Gamma value models, CLV prediction, customer probability analysis, cohort value forecasting."
---

# Lifetimes for CLV Modeling

## Overview

The lifetimes library provides probabilistic models for Customer Lifetime Value (CLV) prediction. This skill covers BG/NBD models for purchase frequency, Gamma-Gamma models for monetary value, and combining them for CLV forecasting.

## When to Use This Skill

- Predicting customer lifetime value
- Modeling purchase frequency patterns
- Estimating probability of customer being alive
- Forecasting future transactions
- Segmenting customers by predicted value
- Optimizing customer acquisition costs

## Core Capabilities

### 1. Prepare RFM Data

```python
import pandas as pd
from lifetimes.utils import summary_data_from_transaction_data

# Load transaction data
transactions = pd.read_csv('transactions.csv', parse_dates=['order_date'])

# Create RFM summary
summary = summary_data_from_transaction_data(
    transactions,
    customer_id_col='customer_id',
    datetime_col='order_date',
    monetary_value_col='revenue',
    observation_period_end='2024-03-01'
)

print(summary.head())
# Columns: frequency, recency, T, monetary_value
# frequency: number of repeat purchases
# recency: time between first and last purchase
# T: age of customer (time since first purchase)
# monetary_value: average order value of repeat purchases
```

### 2. BG/NBD Model for Purchase Frequency

```python
from lifetimes import BetaGeoFitter

# Fit BG/NBD model
bgf = BetaGeoFitter(penalizer_coef=0.001)
bgf.fit(
    summary['frequency'],
    summary['recency'],
    summary['T']
)

# Print model parameters
print("BG/NBD Model Parameters:")
print(f"  r: {bgf.params_['r']:.4f}")
print(f"  alpha: {bgf.params_['alpha']:.4f}")
print(f"  a: {bgf.params_['a']:.4f}")
print(f"  b: {bgf.params_['b']:.4f}")

# Predict future purchases for each customer
t = 90  # next 90 days
summary['predicted_purchases_90d'] = bgf.conditional_expected_number_of_purchases_up_to_time(
    t,
    summary['frequency'],
    summary['recency'],
    summary['T']
)

print("\nTop 10 customers by predicted purchases:")
print(summary.nlargest(10, 'predicted_purchases_90d')[['frequency', 'recency', 'T', 'predicted_purchases_90d']])
```

### 3. Probability of Being Alive

```python
# Calculate probability that each customer is still active
summary['prob_alive'] = bgf.conditional_probability_alive(
    summary['frequency'],
    summary['recency'],
    summary['T']
)

# Identify at-risk customers (low probability of being alive)
at_risk = summary[summary['prob_alive'] < 0.3]
print(f"\nCustomers at risk of churning: {len(at_risk)}")
print(at_risk.head())

# Visualize probability matrix
from lifetimes.plotting import plot_probability_alive_matrix
import matplotlib.pyplot as plt

plot_probability_alive_matrix(bgf)
plt.title('Probability of Being Alive by Frequency and Recency')
plt.show()
```

### 4. Gamma-Gamma Model for Monetary Value

```python
from lifetimes import GammaGammaFitter

# Filter customers with repeat purchases (required for Gamma-Gamma)
returning_customers = summary[summary['frequency'] > 0]

# Fit Gamma-Gamma model
ggf = GammaGammaFitter(penalizer_coef=0.001)
ggf.fit(
    returning_customers['frequency'],
    returning_customers['monetary_value']
)

# Print model parameters
print("Gamma-Gamma Model Parameters:")
print(f"  p: {ggf.params_['p']:.4f}")
print(f"  q: {ggf.params_['q']:.4f}")
print(f"  v: {ggf.params_['v']:.4f}")

# Predict expected average order value
returning_customers['predicted_aov'] = ggf.conditional_expected_average_profit(
    returning_customers['frequency'],
    returning_customers['monetary_value']
)

print("\nActual vs Predicted AOV:")
print(f"  Mean Actual: ${returning_customers['monetary_value'].mean():.2f}")
print(f"  Mean Predicted: ${returning_customers['predicted_aov'].mean():.2f}")
```

### 5. Customer Lifetime Value Calculation

```python
# Calculate CLV for all returning customers
clv = ggf.customer_lifetime_value(
    bgf,  # BG/NBD model
    returning_customers['frequency'],
    returning_customers['recency'],
    returning_customers['T'],
    returning_customers['monetary_value'],
    time=12,  # 12 months
    discount_rate=0.01  # monthly discount rate
)

returning_customers['clv_12m'] = clv

print("\nCLV Distribution:")
print(returning_customers['clv_12m'].describe())

# Segment by CLV
returning_customers['clv_segment'] = pd.qcut(
    returning_customers['clv_12m'],
    5,
    labels=['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond']
)

# Segment summary
clv_summary = returning_customers.groupby('clv_segment').agg({
    'clv_12m': ['mean', 'sum'],
    'frequency': 'mean',
    'monetary_value': 'mean'
}).round(2)

print("\nCLV by Segment:")
print(clv_summary)
```

### 6. Cohort-Level CLV Forecasting

```python
# Add cohort information
transactions['cohort'] = transactions.groupby('customer_id')['order_date'].transform('min').dt.to_period('M')

# Calculate CLV by cohort
cohort_clv = returning_customers.groupby('cohort').agg({
    'clv_12m': ['mean', 'sum', 'count']
}).round(2)

cohort_clv.columns = ['avg_clv', 'total_clv', 'customer_count']

print("\nCLV by Acquisition Cohort:")
print(cohort_clv)

# Calculate expected revenue from cohort
monthly_cohort_value = cohort_clv['total_clv'] / 12
print("\nExpected Monthly Revenue by Cohort:")
print(monthly_cohort_value)
```

### 7. Model Validation

```python
from lifetimes.plotting import plot_calibration_purchases_vs_holdout_purchases
from lifetimes.utils import calibration_and_holdout_data

# Split data into calibration and holdout periods
summary_cal_holdout = calibration_and_holdout_data(
    transactions,
    customer_id_col='customer_id',
    datetime_col='order_date',
    calibration_period_end='2023-12-31',
    observation_period_end='2024-03-01'
)

# Fit model on calibration data
bgf_cal = BetaGeoFitter(penalizer_coef=0.001)
bgf_cal.fit(
    summary_cal_holdout['frequency_cal'],
    summary_cal_holdout['recency_cal'],
    summary_cal_holdout['T_cal']
)

# Compare predicted vs actual holdout purchases
plot_calibration_purchases_vs_holdout_purchases(
    bgf_cal,
    summary_cal_holdout
)
plt.title('Model Validation: Predicted vs Actual Holdout Purchases')
plt.show()
```

## Installation

```bash
uv pip install lifetimes pandas matplotlib
```

## Quick Start

```python
from lifetimes import BetaGeoFitter, GammaGammaFitter
from lifetimes.utils import summary_data_from_transaction_data
import pandas as pd

# Load and prepare data
transactions = pd.read_csv('transactions.csv', parse_dates=['date'])
summary = summary_data_from_transaction_data(
    transactions, 'customer_id', 'date', 'revenue'
)

# Fit models
bgf = BetaGeoFitter().fit(summary['frequency'], summary['recency'], summary['T'])
ggf = GammaGammaFitter().fit(summary['frequency'], summary['monetary_value'])

# Calculate CLV
summary['clv'] = ggf.customer_lifetime_value(
    bgf, summary['frequency'], summary['recency'],
    summary['T'], summary['monetary_value'], time=12
)

print(summary.nlargest(10, 'clv'))
```

## Best Practices

1. **Minimum data** - Need at least 6 months of transaction data
2. **Repeat customers** - Gamma-Gamma model requires customers with frequency > 0
3. **Penalizer** - Use small penalizer (0.001) to prevent overfitting
4. **Validation** - Always validate with holdout data
5. **Discount rate** - Use appropriate discount rate for your business

## References

- [Lifetimes Documentation](https://lifetimes.readthedocs.io/)
- [BG/NBD Model Paper](https://www.brucehardie.com/papers/018/fader_et_al_mksc_05.pdf)

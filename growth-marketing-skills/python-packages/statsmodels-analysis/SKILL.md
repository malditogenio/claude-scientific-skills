---
name: statsmodels-analysis
description: "Statistical analysis for marketing. Regression analysis, A/B test significance, time series decomposition, causal inference, marketing mix modeling."
---

# Statsmodels for Marketing Analysis

## Overview

statsmodels provides statistical modeling tools essential for rigorous marketing analysis. This skill covers hypothesis testing, regression analysis, time series decomposition, and marketing mix modeling.

## When to Use This Skill

- A/B test statistical analysis
- Regression for understanding drivers
- Time series decomposition
- Marketing mix modeling (MMM)
- Causal inference analysis
- Experimental design and power analysis

## Core Capabilities

### 1. A/B Test Statistical Analysis

```python
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.proportion import proportions_ztest, proportion_confint
from statsmodels.stats.power import TTestIndPower

# Conversion rate test
control_visitors = 10000
control_conversions = 320
variant_visitors = 10000
variant_conversions = 380

# Two-proportion z-test
count = np.array([control_conversions, variant_conversions])
nobs = np.array([control_visitors, variant_visitors])

stat, pvalue = proportions_ztest(count, nobs, alternative='two-sided')

# Confidence intervals
ci_control = proportion_confint(control_conversions, control_visitors, alpha=0.05)
ci_variant = proportion_confint(variant_conversions, variant_visitors, alpha=0.05)

print("A/B Test Results:")
print(f"  Control: {control_conversions/control_visitors:.2%} [{ci_control[0]:.2%}, {ci_control[1]:.2%}]")
print(f"  Variant: {variant_conversions/variant_visitors:.2%} [{ci_variant[0]:.2%}, {ci_variant[1]:.2%}]")
print(f"  Relative Lift: {(variant_conversions/variant_visitors)/(control_conversions/control_visitors) - 1:.1%}")
print(f"  P-value: {pvalue:.4f}")
print(f"  Significant: {'Yes' if pvalue < 0.05 else 'No'}")
```

### 2. Sample Size Calculation

```python
from statsmodels.stats.power import TTestIndPower, NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

# Parameters
baseline_rate = 0.03  # 3% conversion rate
minimum_detectable_effect = 0.15  # 15% relative lift
alpha = 0.05  # Significance level
power = 0.80  # Statistical power

# Calculate effect size
target_rate = baseline_rate * (1 + minimum_detectable_effect)
effect_size = proportion_effectsize(baseline_rate, target_rate)

# Calculate sample size per group
analysis = NormalIndPower()
sample_size = analysis.solve_power(
    effect_size=effect_size,
    alpha=alpha,
    power=power,
    ratio=1.0,  # Equal groups
    alternative='two-sided'
)

print(f"Sample Size Calculation:")
print(f"  Baseline: {baseline_rate:.1%}")
print(f"  Target: {target_rate:.1%}")
print(f"  MDE: {minimum_detectable_effect:.0%}")
print(f"  Required per group: {int(np.ceil(sample_size)):,}")
print(f"  Total required: {int(np.ceil(sample_size * 2)):,}")
```

### 3. Regression for Marketing Drivers

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Marketing performance data
df = pd.read_csv('marketing_data.csv')

# OLS regression with formula API
model = smf.ols(
    'revenue ~ spend_meta + spend_google + spend_email + price_discount + is_weekend',
    data=df
).fit()

print(model.summary())

# Extract key insights
print("\nKey Drivers of Revenue:")
for var, coef, pval in zip(model.params.index[1:], model.params[1:], model.pvalues[1:]):
    significance = "***" if pval < 0.001 else "**" if pval < 0.01 else "*" if pval < 0.05 else ""
    print(f"  {var}: {coef:.2f} {significance}")
```

### 4. Marketing Mix Modeling (MMM)

```python
import statsmodels.api as sm
import numpy as np

# Adstock transformation (carryover effect)
def adstock(series, decay_rate=0.5):
    """Apply adstock transformation to capture carryover effects"""
    adstocked = np.zeros(len(series))
    adstocked[0] = series[0]
    for i in range(1, len(series)):
        adstocked[i] = series[i] + decay_rate * adstocked[i-1]
    return adstocked

# Saturation transformation (diminishing returns)
def saturation(series, alpha=0.5):
    """Apply saturation curve"""
    return 1 - np.exp(-alpha * series)

# Prepare MMM features
df['tv_adstock'] = adstock(df['tv_spend'], decay_rate=0.7)
df['digital_adstock'] = adstock(df['digital_spend'], decay_rate=0.3)
df['tv_saturated'] = saturation(df['tv_adstock'], alpha=0.0001)
df['digital_saturated'] = saturation(df['digital_adstock'], alpha=0.001)

# Add control variables
X = df[['tv_saturated', 'digital_saturated', 'price', 'seasonality_index']]
X = sm.add_constant(X)
y = df['sales']

# Fit model
mmm_model = sm.OLS(y, X).fit()
print(mmm_model.summary())

# Calculate channel contribution
df['tv_contribution'] = mmm_model.params['tv_saturated'] * df['tv_saturated']
df['digital_contribution'] = mmm_model.params['digital_saturated'] * df['digital_saturated']

print("\nChannel Contribution:")
print(f"  TV: {df['tv_contribution'].sum() / df['sales'].sum():.1%}")
print(f"  Digital: {df['digital_contribution'].sum() / df['sales'].sum():.1%}")
```

### 5. Time Series Decomposition

```python
from statsmodels.tsa.seasonal import seasonal_decompose

# Decompose time series
df = pd.read_csv('daily_revenue.csv', parse_dates=['date'], index_col='date')

# Multiplicative decomposition (good for revenue)
decomposition = seasonal_decompose(
    df['revenue'],
    model='multiplicative',
    period=7  # Weekly seasonality
)

# Extract components
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# Plot
decomposition.plot()

# Identify anomalies from residuals
residual_std = residual.std()
anomalies = df[abs(residual) > 2 * residual_std]
print(f"\nAnomalies detected: {len(anomalies)}")
print(anomalies)
```

### 6. Causal Impact Analysis

```python
import statsmodels.api as sm
from statsmodels.tsa.statespace.structural import UnobservedComponents

# Pre/post intervention analysis
df = pd.read_csv('campaign_impact.csv', parse_dates=['date'], index_col='date')

# Split pre and post intervention
intervention_date = '2024-02-01'
pre = df[df.index < intervention_date]
post = df[df.index >= intervention_date]

# Fit model on pre-period with control series
pre_X = sm.add_constant(pre[['control_market', 'seasonality']])
pre_y = pre['treatment_market']

model = sm.OLS(pre_y, pre_X).fit()

# Predict counterfactual for post-period
post_X = sm.add_constant(post[['control_market', 'seasonality']])
counterfactual = model.predict(post_X)

# Calculate causal impact
actual = post['treatment_market']
impact = actual - counterfactual

print("Causal Impact Analysis:")
print(f"  Pre-period R²: {model.rsquared:.3f}")
print(f"  Post-period actual: {actual.sum():,.0f}")
print(f"  Counterfactual: {counterfactual.sum():,.0f}")
print(f"  Estimated impact: {impact.sum():,.0f}")
print(f"  Relative lift: {impact.sum() / counterfactual.sum():.1%}")
```

## Installation

```bash
uv pip install statsmodels pandas numpy scipy
```

## Quick Start

```python
import statsmodels.api as sm
import pandas as pd

# Quick regression
df = pd.read_csv('data.csv')
X = sm.add_constant(df[['feature1', 'feature2']])
y = df['target']

model = sm.OLS(y, X).fit()
print(model.summary())
```

## References

- [statsmodels Documentation](https://www.statsmodels.org/)
- [Statistical Tests in statsmodels](https://www.statsmodels.org/stable/stats.html)

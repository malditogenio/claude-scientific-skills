---
name: pymc-bayesian
description: "Bayesian analysis for marketing. Bayesian A/B testing, probabilistic CLV models, hierarchical models for campaigns, marketing mix modeling with uncertainty."
---

# PyMC for Bayesian Marketing Analysis

## Overview

PyMC enables Bayesian statistical modeling for marketing analytics. This skill covers Bayesian A/B testing, probabilistic CLV models, hierarchical campaign analysis, and marketing mix modeling with proper uncertainty quantification.

## When to Use This Skill

- Bayesian A/B testing with credible intervals
- Early stopping decisions in experiments
- Hierarchical models across campaigns/segments
- Probabilistic lifetime value models
- Marketing mix modeling with uncertainty
- Small sample size analysis

## Core Capabilities

### 1. Bayesian A/B Testing

```python
import pymc as pm
import numpy as np
import arviz as az

# A/B test data
control_visitors = 5000
control_conversions = 150
variant_visitors = 5000
variant_conversions = 185

with pm.Model() as ab_model:
    # Priors (uninformative)
    p_control = pm.Beta('p_control', alpha=1, beta=1)
    p_variant = pm.Beta('p_variant', alpha=1, beta=1)

    # Likelihoods
    obs_control = pm.Binomial('obs_control', n=control_visitors,
                               p=p_control, observed=control_conversions)
    obs_variant = pm.Binomial('obs_variant', n=variant_visitors,
                               p=p_variant, observed=variant_conversions)

    # Derived quantities
    lift = pm.Deterministic('lift', (p_variant - p_control) / p_control)
    prob_variant_better = pm.Deterministic('prob_variant_better',
                                            pm.math.gt(p_variant, p_control))

    # Sample
    trace = pm.sample(2000, tune=1000, return_inferencedata=True)

# Results
summary = az.summary(trace, var_names=['p_control', 'p_variant', 'lift'])
print(summary)

# Probability that variant is better
prob_better = trace.posterior['prob_variant_better'].mean().values
print(f"\nProbability variant is better: {prob_better:.1%}")

# Expected lift
lift_samples = trace.posterior['lift'].values.flatten()
print(f"Expected lift: {np.mean(lift_samples):.1%}")
print(f"95% Credible Interval: [{np.percentile(lift_samples, 2.5):.1%}, {np.percentile(lift_samples, 97.5):.1%}]")
```

### 2. Revenue A/B Test (Continuous Outcome)

```python
import pymc as pm
import numpy as np

# Revenue per user data
control_revenue = np.random.lognormal(3, 1, 1000)  # Example data
variant_revenue = np.random.lognormal(3.1, 1, 1000)

with pm.Model() as revenue_model:
    # Priors for log-normal parameters
    mu_control = pm.Normal('mu_control', mu=3, sigma=1)
    mu_variant = pm.Normal('mu_variant', mu=3, sigma=1)
    sigma = pm.HalfNormal('sigma', sigma=1)

    # Likelihoods
    obs_control = pm.LogNormal('obs_control', mu=mu_control, sigma=sigma,
                                observed=control_revenue)
    obs_variant = pm.LogNormal('obs_variant', mu=mu_variant, sigma=sigma,
                                observed=variant_revenue)

    # Expected revenue (mean of lognormal)
    mean_control = pm.Deterministic('mean_control',
                                     pm.math.exp(mu_control + sigma**2/2))
    mean_variant = pm.Deterministic('mean_variant',
                                     pm.math.exp(mu_variant + sigma**2/2))

    # Revenue lift
    revenue_lift = pm.Deterministic('revenue_lift',
                                     (mean_variant - mean_control) / mean_control)

    trace = pm.sample(2000, tune=1000, return_inferencedata=True)

# Analyze results
lift_samples = trace.posterior['revenue_lift'].values.flatten()
print(f"Revenue Lift: {np.mean(lift_samples):.1%}")
print(f"Probability of positive lift: {(lift_samples > 0).mean():.1%}")
```

### 3. Hierarchical Campaign Model

```python
import pymc as pm
import pandas as pd
import numpy as np

# Campaign data: multiple campaigns, each with conversion data
campaigns = pd.DataFrame({
    'campaign_id': range(10),
    'impressions': [50000, 30000, 80000, 20000, 60000,
                    40000, 70000, 25000, 55000, 45000],
    'conversions': [250, 180, 320, 80, 300, 160, 280, 100, 220, 200]
})

with pm.Model() as hierarchical_model:
    # Hyperpriors (population-level)
    mu_alpha = pm.Normal('mu_alpha', mu=0, sigma=1)
    sigma_alpha = pm.HalfNormal('sigma_alpha', sigma=1)

    # Campaign-level conversion rates (logit scale)
    alpha = pm.Normal('alpha', mu=mu_alpha, sigma=sigma_alpha,
                      shape=len(campaigns))

    # Convert to probability
    p = pm.Deterministic('p', pm.math.invlogit(alpha))

    # Likelihood
    conversions = pm.Binomial('conversions',
                               n=campaigns['impressions'].values,
                               p=p,
                               observed=campaigns['conversions'].values)

    trace = pm.sample(2000, tune=1000, return_inferencedata=True)

# Campaign-level estimates with shrinkage
p_samples = trace.posterior['p'].values.reshape(-1, len(campaigns))
for i, campaign_id in enumerate(campaigns['campaign_id']):
    raw_rate = campaigns.iloc[i]['conversions'] / campaigns.iloc[i]['impressions']
    posterior_mean = p_samples[:, i].mean()
    print(f"Campaign {campaign_id}: Raw={raw_rate:.3%}, Posterior={posterior_mean:.3%}")
```

### 4. Bayesian Marketing Mix Model

```python
import pymc as pm
import numpy as np
import pandas as pd

# Weekly marketing data
df = pd.read_csv('weekly_marketing.csv')

# Adstock transformation
def adstock(x, decay):
    result = np.zeros_like(x)
    result[0] = x[0]
    for i in range(1, len(x)):
        result[i] = x[i] + decay * result[i-1]
    return result

with pm.Model() as mmm_model:
    # Priors for adstock decay rates
    decay_tv = pm.Beta('decay_tv', alpha=2, beta=2)
    decay_digital = pm.Beta('decay_digital', alpha=2, beta=2)

    # Apply adstock (using PyTensor operations)
    # Note: In practice, you might precompute for different decay values
    tv_adstock = pm.Deterministic('tv_adstock',
        pm.math.cumsum(df['tv_spend'].values * (1-decay_tv)))
    digital_adstock = pm.Deterministic('digital_adstock',
        pm.math.cumsum(df['digital_spend'].values * (1-decay_digital)))

    # Channel coefficients
    beta_tv = pm.HalfNormal('beta_tv', sigma=1)
    beta_digital = pm.HalfNormal('beta_digital', sigma=1)
    beta_base = pm.Normal('beta_base', mu=df['sales'].mean(), sigma=1000)

    # Expected sales
    mu = beta_base + beta_tv * tv_adstock + beta_digital * digital_adstock

    # Likelihood
    sigma = pm.HalfNormal('sigma', sigma=1000)
    sales = pm.Normal('sales', mu=mu, sigma=sigma,
                       observed=df['sales'].values)

    trace = pm.sample(2000, tune=1000, return_inferencedata=True)

# Channel contribution with uncertainty
print(az.summary(trace, var_names=['beta_tv', 'beta_digital', 'decay_tv', 'decay_digital']))
```

### 5. Sequential Testing (Early Stopping)

```python
import pymc as pm
import numpy as np

def bayesian_stopping_decision(control_n, control_conv, variant_n, variant_conv,
                                threshold=0.95, rope=(-0.01, 0.01)):
    """
    Decide whether to stop A/B test early based on Bayesian criteria.

    Args:
        threshold: Probability threshold for decision
        rope: Region of Practical Equivalence for lift
    """
    with pm.Model():
        p_control = pm.Beta('p_control', alpha=1+control_conv,
                            beta=1+control_n-control_conv)
        p_variant = pm.Beta('p_variant', alpha=1+variant_conv,
                            beta=1+variant_n-variant_conv)

        lift = pm.Deterministic('lift', (p_variant - p_control) / p_control)

        trace = pm.sample(5000, tune=1000, return_inferencedata=True,
                         progressbar=False)

    lift_samples = trace.posterior['lift'].values.flatten()

    prob_variant_wins = (lift_samples > rope[1]).mean()
    prob_control_wins = (lift_samples < rope[0]).mean()
    prob_inconclusive = 1 - prob_variant_wins - prob_control_wins

    decision = None
    if prob_variant_wins > threshold:
        decision = "VARIANT WINS - Stop test"
    elif prob_control_wins > threshold:
        decision = "CONTROL WINS - Stop test"
    else:
        decision = "CONTINUE - Need more data"

    return {
        'decision': decision,
        'prob_variant_wins': prob_variant_wins,
        'prob_control_wins': prob_control_wins,
        'expected_lift': np.mean(lift_samples),
        'lift_ci': (np.percentile(lift_samples, 2.5), np.percentile(lift_samples, 97.5))
    }

# Example usage
result = bayesian_stopping_decision(3000, 90, 3000, 120)
print(result)
```

## Installation

```bash
uv pip install pymc arviz numpy pandas
```

## Quick Start

```python
import pymc as pm
import arviz as az

# Simple Bayesian A/B test
with pm.Model() as model:
    p_a = pm.Beta('p_a', 1, 1)
    p_b = pm.Beta('p_b', 1, 1)

    obs_a = pm.Binomial('obs_a', n=1000, p=p_a, observed=35)
    obs_b = pm.Binomial('obs_b', n=1000, p=p_b, observed=45)

    diff = pm.Deterministic('diff', p_b - p_a)
    trace = pm.sample(2000)

print(az.summary(trace, var_names=['p_a', 'p_b', 'diff']))
```

## Best Practices

1. **Choose appropriate priors** - Use domain knowledge to inform priors
2. **Check convergence** - Use r_hat and ESS diagnostics
3. **Visualize posteriors** - Use az.plot_posterior() for insights
4. **Consider ROPE** - Define practical significance, not just statistical
5. **Document assumptions** - Clearly state model assumptions

## References

- [PyMC Documentation](https://www.pymc.io/)
- [Bayesian Methods for Hackers](https://camdavidsonpilon.github.io/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/)

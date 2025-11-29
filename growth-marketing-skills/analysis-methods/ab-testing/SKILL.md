---
name: ab-testing
description: Design, implement, and analyze A/B tests and multivariate experiments. Calculate sample sizes, run statistical significance tests (t-tests, chi-square, ANOVA), perform Bayesian analysis, and handle multiple comparison corrections. Includes power analysis, sequential testing, and practical significance evaluation for growth marketing experiments.
---

# A/B Testing and Experiment Design

## Overview

A/B testing (split testing) is the fundamental methodology for making data-driven decisions in growth marketing. This skill covers the complete experimental workflow from design through analysis, including statistical rigor, practical significance assessment, and common pitfalls.

**Key Capabilities:**
- Experimental design and sample size calculation
- Statistical significance testing (frequentist and Bayesian)
- Power analysis and minimum detectable effect
- Multiple comparison corrections
- Sequential testing and early stopping
- Segmented analysis and heterogeneous treatment effects
- Practical significance and business impact assessment

## When to Use This Skill

Use this skill when:
- Designing new A/B tests or multivariate experiments
- Calculating required sample sizes for experiments
- Analyzing test results for statistical significance
- Evaluating conversion rate changes, revenue impacts, or engagement metrics
- Testing new features, pricing changes, landing pages, or marketing messages
- Performing power analysis to determine test feasibility
- Running segmented analysis to identify differential effects

## Core Capabilities

### 1. Sample Size Calculation

Determine the required sample size before running an experiment.

```python
import numpy as np
import pandas as pd
from scipy import stats
from typing import Tuple

def calculate_sample_size(
    baseline_rate: float,
    minimum_detectable_effect: float,
    alpha: float = 0.05,
    power: float = 0.80,
    two_sided: bool = True
) -> int:
    """
    Calculate required sample size per variant for A/B test.

    Parameters:
    -----------
    baseline_rate : float
        Current conversion rate (e.g., 0.10 for 10%)
    minimum_detectable_effect : float
        Minimum relative change to detect (e.g., 0.10 for 10% improvement)
    alpha : float
        Significance level (Type I error rate)
    power : float
        Statistical power (1 - Type II error rate)
    two_sided : bool
        Whether to run a two-sided test

    Returns:
    --------
    int : Required sample size per variant
    """
    # Calculate effect size (Cohen's h for proportions)
    p1 = baseline_rate
    p2 = baseline_rate * (1 + minimum_detectable_effect)

    # Cohen's h
    effect_size = 2 * (np.arcsin(np.sqrt(p2)) - np.arcsin(np.sqrt(p1)))

    # Z-scores for alpha and beta
    if two_sided:
        z_alpha = stats.norm.ppf(1 - alpha / 2)
    else:
        z_alpha = stats.norm.ppf(1 - alpha)

    z_beta = stats.norm.ppf(power)

    # Sample size calculation
    n = ((z_alpha + z_beta) / effect_size) ** 2

    return int(np.ceil(n))

# Example: Calculate sample size for conversion rate test
baseline_cr = 0.05  # 5% current conversion rate
mde = 0.10  # Want to detect 10% relative improvement (5% -> 5.5%)

sample_size = calculate_sample_size(
    baseline_rate=baseline_cr,
    minimum_detectable_effect=mde,
    alpha=0.05,
    power=0.80
)

print(f"Required sample size per variant: {sample_size:,}")
print(f"Total sample size needed: {sample_size * 2:,}")
print(f"To detect: {baseline_cr:.1%} -> {baseline_cr * (1 + mde):.1%}")
```

### 2. Two-Sample Proportion Test (Conversion Rates)

Test whether two conversion rates are significantly different.

```python
def ab_test_proportions(
    conversions_a: int,
    visitors_a: int,
    conversions_b: int,
    visitors_b: int,
    alpha: float = 0.05
) -> dict:
    """
    Perform two-proportion z-test for A/B test.

    Returns:
    --------
    dict with keys:
        - conversion_rate_a, conversion_rate_b
        - lift (relative improvement)
        - p_value
        - significant (bool)
        - confidence_interval (95% CI for lift)
    """
    # Conversion rates
    cr_a = conversions_a / visitors_a
    cr_b = conversions_b / visitors_b

    # Pooled proportion
    pooled_p = (conversions_a + conversions_b) / (visitors_a + visitors_b)

    # Standard error
    se = np.sqrt(pooled_p * (1 - pooled_p) * (1/visitors_a + 1/visitors_b))

    # Z-statistic
    z_stat = (cr_b - cr_a) / se

    # Two-sided p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    # Lift calculation
    lift = (cr_b - cr_a) / cr_a if cr_a > 0 else np.inf

    # Confidence interval for difference
    z_crit = stats.norm.ppf(1 - alpha/2)
    se_diff = np.sqrt(cr_a*(1-cr_a)/visitors_a + cr_b*(1-cr_b)/visitors_b)
    ci_lower = (cr_b - cr_a) - z_crit * se_diff
    ci_upper = (cr_b - cr_a) + z_crit * se_diff

    # Convert to lift CI
    lift_ci_lower = ci_lower / cr_a if cr_a > 0 else -np.inf
    lift_ci_upper = ci_upper / cr_a if cr_a > 0 else np.inf

    return {
        'conversion_rate_a': cr_a,
        'conversion_rate_b': cr_b,
        'absolute_lift': cr_b - cr_a,
        'relative_lift': lift,
        'z_statistic': z_stat,
        'p_value': p_value,
        'significant': p_value < alpha,
        'confidence_interval': (lift_ci_lower, lift_ci_upper),
        'sample_size_a': visitors_a,
        'sample_size_b': visitors_b
    }

# Example: Analyze A/B test results
results = ab_test_proportions(
    conversions_a=550,
    visitors_a=10000,
    conversions_b=605,
    visitors_b=10000,
    alpha=0.05
)

print(f"Control (A): {results['conversion_rate_a']:.2%} conversion rate")
print(f"Variant (B): {results['conversion_rate_b']:.2%} conversion rate")
print(f"Relative Lift: {results['relative_lift']:.2%}")
print(f"P-value: {results['p_value']:.4f}")
print(f"Significant: {results['significant']}")
print(f"95% CI for lift: [{results['confidence_interval'][0]:.2%}, "
      f"{results['confidence_interval'][1]:.2%}]")
```

### 3. Continuous Metric Testing (Revenue, Time on Site)

Test differences in continuous metrics like revenue or engagement time.

```python
def ab_test_continuous(
    values_a: np.ndarray,
    values_b: np.ndarray,
    alpha: float = 0.05
) -> dict:
    """
    Perform t-test for continuous metrics in A/B test.
    Uses Welch's t-test (unequal variances).
    """
    mean_a = np.mean(values_a)
    mean_b = np.mean(values_b)
    std_a = np.std(values_a, ddof=1)
    std_b = np.std(values_b, ddof=1)
    n_a = len(values_a)
    n_b = len(values_b)

    # Welch's t-test
    t_stat, p_value = stats.ttest_ind(values_a, values_b, equal_var=False)

    # Effect size (Cohen's d)
    pooled_std = np.sqrt(((n_a - 1) * std_a**2 + (n_b - 1) * std_b**2) / (n_a + n_b - 2))
    cohens_d = (mean_b - mean_a) / pooled_std

    # Confidence interval for difference
    se_diff = np.sqrt(std_a**2/n_a + std_b**2/n_b)
    df = (std_a**2/n_a + std_b**2/n_b)**2 / \
         ((std_a**2/n_a)**2/(n_a-1) + (std_b**2/n_b)**2/(n_b-1))
    t_crit = stats.t.ppf(1 - alpha/2, df)
    ci_lower = (mean_b - mean_a) - t_crit * se_diff
    ci_upper = (mean_b - mean_a) + t_crit * se_diff

    lift = (mean_b - mean_a) / mean_a if mean_a != 0 else np.inf

    return {
        'mean_a': mean_a,
        'mean_b': mean_b,
        'std_a': std_a,
        'std_b': std_b,
        'absolute_lift': mean_b - mean_a,
        'relative_lift': lift,
        't_statistic': t_stat,
        'p_value': p_value,
        'significant': p_value < alpha,
        'cohens_d': cohens_d,
        'confidence_interval': (ci_lower, ci_upper),
        'sample_size_a': n_a,
        'sample_size_b': n_b
    }

# Example: Test revenue per user
np.random.seed(42)
revenue_control = np.random.gamma(2, 15, 5000)  # Control group revenue
revenue_variant = np.random.gamma(2, 16, 5000)  # Variant group revenue

results = ab_test_continuous(revenue_control, revenue_variant)

print(f"Control mean: ${results['mean_a']:.2f}")
print(f"Variant mean: ${results['mean_b']:.2f}")
print(f"Lift: {results['relative_lift']:.2%}")
print(f"P-value: {results['p_value']:.4f}")
print(f"Effect size (Cohen's d): {results['cohens_d']:.3f}")
print(f"Significant: {results['significant']}")
```

### 4. Bayesian A/B Test Analysis

Bayesian approach for more intuitive probability statements.

```python
def bayesian_ab_test(
    conversions_a: int,
    visitors_a: int,
    conversions_b: int,
    visitors_b: int,
    n_simulations: int = 100000
) -> dict:
    """
    Bayesian A/B test using Beta-Binomial conjugate prior.

    Returns probability that B is better than A.
    """
    # Beta posterior parameters (uniform prior: Beta(1,1))
    alpha_a = conversions_a + 1
    beta_a = visitors_a - conversions_a + 1

    alpha_b = conversions_b + 1
    beta_b = visitors_b - conversions_b + 1

    # Sample from posterior distributions
    samples_a = np.random.beta(alpha_a, beta_a, n_simulations)
    samples_b = np.random.beta(alpha_b, beta_b, n_simulations)

    # Probability that B > A
    prob_b_better = np.mean(samples_b > samples_a)

    # Expected lift
    expected_lift = np.mean((samples_b - samples_a) / samples_a)

    # Credible interval for lift
    lift_samples = (samples_b - samples_a) / samples_a
    ci_lower, ci_upper = np.percentile(lift_samples, [2.5, 97.5])

    return {
        'conversion_rate_a': conversions_a / visitors_a,
        'conversion_rate_b': conversions_b / visitors_b,
        'prob_b_better': prob_b_better,
        'expected_lift': expected_lift,
        'credible_interval': (ci_lower, ci_upper),
        'posterior_a': (alpha_a, beta_a),
        'posterior_b': (alpha_b, beta_b)
    }

# Example: Bayesian analysis
results = bayesian_ab_test(
    conversions_a=550,
    visitors_a=10000,
    conversions_b=605,
    visitors_b=10000
)

print(f"Control: {results['conversion_rate_a']:.2%}")
print(f"Variant: {results['conversion_rate_b']:.2%}")
print(f"Probability B is better than A: {results['prob_b_better']:.2%}")
print(f"Expected lift: {results['expected_lift']:.2%}")
print(f"95% Credible interval: [{results['credible_interval'][0]:.2%}, "
      f"{results['credible_interval'][1]:.2%}]")
```

### 5. Multiple Comparison Correction

When testing multiple variants or metrics, correct for multiple comparisons.

```python
from statsmodels.stats.multitest import multipletests

def multivariate_test_correction(
    p_values: list,
    method: str = 'bonferroni',
    alpha: float = 0.05
) -> dict:
    """
    Apply multiple comparison correction.

    Parameters:
    -----------
    p_values : list of float
        P-values from multiple tests
    method : str
        Correction method: 'bonferroni', 'holm', 'fdr_bh' (Benjamini-Hochberg)
    alpha : float
        Family-wise error rate or FDR threshold

    Returns:
    --------
    dict with corrected p-values and significance
    """
    rejected, corrected_p, alpha_sidak, alpha_bonf = multipletests(
        p_values, alpha=alpha, method=method
    )

    return {
        'original_p_values': p_values,
        'corrected_p_values': corrected_p.tolist(),
        'significant': rejected.tolist(),
        'method': method,
        'alpha': alpha
    }

# Example: Testing 5 different variants
variants = ['V1', 'V2', 'V3', 'V4', 'V5']
p_values = [0.03, 0.12, 0.008, 0.45, 0.02]

# Bonferroni correction
bonf_results = multivariate_test_correction(p_values, method='bonferroni')

# Benjamini-Hochberg FDR
fdr_results = multivariate_test_correction(p_values, method='fdr_bh')

print("Bonferroni Correction:")
for variant, p_orig, p_corr, sig in zip(
    variants,
    bonf_results['original_p_values'],
    bonf_results['corrected_p_values'],
    bonf_results['significant']
):
    print(f"  {variant}: p={p_orig:.4f} -> {p_corr:.4f}, sig={sig}")

print("\nBenjamini-Hochberg FDR:")
for variant, p_orig, p_corr, sig in zip(
    variants,
    fdr_results['original_p_values'],
    fdr_results['corrected_p_values'],
    fdr_results['significant']
):
    print(f"  {variant}: p={p_orig:.4f} -> {p_corr:.4f}, sig={sig}")
```

### 6. Sequential Testing and Early Stopping

Implement sequential testing to monitor experiments over time.

```python
def sequential_test(
    conversions_a_cumsum: np.ndarray,
    visitors_a_cumsum: np.ndarray,
    conversions_b_cumsum: np.ndarray,
    visitors_b_cumsum: np.ndarray,
    alpha: float = 0.05,
    spending_function: str = 'obrien_fleming'
) -> pd.DataFrame:
    """
    Sequential testing with alpha spending.

    Parameters:
    -----------
    *_cumsum : arrays of cumulative counts over time
    spending_function : 'obrien_fleming' or 'pocock'

    Returns:
    --------
    DataFrame with p-values and adjusted thresholds over time
    """
    n_looks = len(conversions_a_cumsum)
    results = []

    for i in range(n_looks):
        # Run test at this point
        test_result = ab_test_proportions(
            conversions_a_cumsum[i],
            visitors_a_cumsum[i],
            conversions_b_cumsum[i],
            visitors_b_cumsum[i]
        )

        # Alpha spending (O'Brien-Fleming approximation)
        if spending_function == 'obrien_fleming':
            # Adjusted alpha at look i
            t = (i + 1) / n_looks  # Information fraction
            alpha_i = 2 * (1 - stats.norm.cdf(stats.norm.ppf(1 - alpha/2) / np.sqrt(t)))
        else:  # Pocock
            alpha_i = alpha * np.log(1 + (np.e - 1) * (i + 1) / n_looks)

        results.append({
            'look': i + 1,
            'visitors_a': visitors_a_cumsum[i],
            'visitors_b': visitors_b_cumsum[i],
            'cr_a': test_result['conversion_rate_a'],
            'cr_b': test_result['conversion_rate_b'],
            'p_value': test_result['p_value'],
            'alpha_threshold': alpha_i,
            'significant': test_result['p_value'] < alpha_i
        })

    return pd.DataFrame(results)

# Example: Simulate sequential testing
np.random.seed(42)
n_days = 14
daily_visitors = 1000

# Simulate cumulative data
visitors_a_cum = np.arange(1, n_days + 1) * daily_visitors
visitors_b_cum = np.arange(1, n_days + 1) * daily_visitors

conversions_a_cum = np.random.binomial(visitors_a_cum, 0.05)
conversions_b_cum = np.random.binomial(visitors_b_cum, 0.055)

seq_results = sequential_test(
    conversions_a_cum,
    visitors_a_cum,
    conversions_b_cum,
    visitors_b_cum,
    spending_function='obrien_fleming'
)

print("\nSequential Test Results:")
print(seq_results.to_string(index=False))
```

### 7. Complete A/B Test Report

Generate a comprehensive analysis report.

```python
import matplotlib.pyplot as plt
import seaborn as sns

def generate_ab_test_report(
    conversions_a: int,
    visitors_a: int,
    conversions_b: int,
    visitors_b: int,
    metric_name: str = "Conversion Rate",
    variant_names: tuple = ("Control", "Variant")
) -> None:
    """
    Generate comprehensive A/B test report with visualizations.
    """
    # Run both frequentist and Bayesian analysis
    freq_results = ab_test_proportions(conversions_a, visitors_a,
                                       conversions_b, visitors_b)
    bayes_results = bayesian_ab_test(conversions_a, visitors_a,
                                     conversions_b, visitors_b)

    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Conversion rates comparison
    ax1 = axes[0, 0]
    variants = [variant_names[0], variant_names[1]]
    rates = [freq_results['conversion_rate_a'], freq_results['conversion_rate_b']]
    bars = ax1.bar(variants, rates, color=['#1f77b4', '#ff7f0e'])
    ax1.set_ylabel(metric_name)
    ax1.set_title(f'{metric_name} by Variant')

    # Add value labels
    for bar, rate in zip(bars, rates):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{rate:.2%}', ha='center', va='bottom')

    # 2. Statistical significance
    ax2 = axes[0, 1]
    ax2.axis('off')

    report_text = f"""
    FREQUENTIST ANALYSIS
    {'='*40}
    Control: {freq_results['conversion_rate_a']:.3%}
    Variant: {freq_results['conversion_rate_b']:.3%}
    Lift: {freq_results['relative_lift']:.2%}

    P-value: {freq_results['p_value']:.4f}
    Significant: {freq_results['significant']} (α=0.05)
    95% CI: [{freq_results['confidence_interval'][0]:.2%},
             {freq_results['confidence_interval'][1]:.2%}]

    BAYESIAN ANALYSIS
    {'='*40}
    P(Variant > Control): {bayes_results['prob_b_better']:.2%}
    Expected Lift: {bayes_results['expected_lift']:.2%}
    95% Credible Interval:
        [{bayes_results['credible_interval'][0]:.2%},
         {bayes_results['credible_interval'][1]:.2%}]
    """

    ax2.text(0, 0.5, report_text, fontfamily='monospace',
             verticalalignment='center', fontsize=9)

    # 3. Posterior distributions (Bayesian)
    ax3 = axes[1, 0]
    alpha_a, beta_a = bayes_results['posterior_a']
    alpha_b, beta_b = bayes_results['posterior_b']

    x = np.linspace(0, 0.1, 1000)
    posterior_a = stats.beta.pdf(x, alpha_a, beta_a)
    posterior_b = stats.beta.pdf(x, alpha_b, beta_b)

    ax3.plot(x, posterior_a, label=variant_names[0], linewidth=2)
    ax3.plot(x, posterior_b, label=variant_names[1], linewidth=2)
    ax3.fill_between(x, posterior_a, alpha=0.3)
    ax3.fill_between(x, posterior_b, alpha=0.3)
    ax3.set_xlabel(metric_name)
    ax3.set_ylabel('Probability Density')
    ax3.set_title('Posterior Distributions')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. Lift distribution
    ax4 = axes[1, 1]
    n_sim = 100000
    samples_a = np.random.beta(alpha_a, beta_a, n_sim)
    samples_b = np.random.beta(alpha_b, beta_b, n_sim)
    lift_dist = (samples_b - samples_a) / samples_a

    ax4.hist(lift_dist, bins=100, alpha=0.7, edgecolor='black')
    ax4.axvline(0, color='red', linestyle='--', linewidth=2, label='No Effect')
    ax4.axvline(np.median(lift_dist), color='green', linestyle='--',
                linewidth=2, label=f'Median: {np.median(lift_dist):.2%}')
    ax4.set_xlabel('Relative Lift')
    ax4.set_ylabel('Frequency')
    ax4.set_title('Distribution of Lift')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('ab_test_report.png', dpi=300, bbox_inches='tight')
    print("Report saved to: ab_test_report.png")

    return fig

# Example: Generate full report
fig = generate_ab_test_report(
    conversions_a=550,
    visitors_a=10000,
    conversions_b=605,
    visitors_b=10000,
    metric_name="Conversion Rate",
    variant_names=("Control", "New Design")
)
```

## Best Practices

### 1. Experimental Design
- **Define success metrics before starting**: Primary and secondary metrics
- **Calculate sample size upfront**: Don't peek at results before reaching target
- **Randomize properly**: Ensure random assignment to avoid selection bias
- **Run for full weeks**: Account for day-of-week effects
- **Avoid novelty effects**: Run long enough for users to adapt

### 2. Statistical Rigor
- **Pre-register hypotheses**: Decide on metrics and analysis plan beforehand
- **Use appropriate tests**: Proportions vs. continuous metrics
- **Correct for multiple comparisons**: When testing multiple variants/metrics
- **Check assumptions**: Normality, independence, equal variance
- **Report confidence intervals**: Not just p-values

### 3. Practical Significance
- **Don't confuse statistical and practical significance**: Small effects can be significant with large samples
- **Consider business impact**: Is the lift worth implementation cost?
- **Calculate expected value**: Lift × volume × value per conversion
- **Account for long-term effects**: Short-term wins may have long-term costs

### 4. Common Pitfalls to Avoid
- **Peeking**: Looking at results repeatedly increases false positive rate
- **Small sample sizes**: Underpowered tests lead to missed effects
- **Ignoring segments**: Average effects may hide important heterogeneity
- **Selection bias**: Users self-selecting into variants
- **Novelty effects**: Short-term changes that don't persist
- **Simpson's paradox**: Segment effects opposite to aggregate

### 5. Advanced Considerations
- **Segmented analysis**: Test for heterogeneous treatment effects
- **Long-term effects**: Consider lifetime value, not just immediate conversion
- **Network effects**: Account for interference between users
- **CUPED/variance reduction**: Use pre-experiment data to reduce variance
- **Bayesian methods**: For continuous monitoring and intuitive interpretation

## References

### Statistical Methods
- Kohavi, R., Tang, D., & Xu, Y. (2020). *Trustworthy Online Controlled Experiments*
- VanderPlas, J. (2014). "Frequentism and Bayesianism: A Python-driven Primer"
- Deng, A., Xu, Y., Kohavi, R., & Walker, T. (2013). "Improving the Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data"

### Tools and Libraries
- **SciPy**: Statistical tests and distributions
- **statsmodels**: Advanced statistical models and corrections
- **pymc**: Bayesian modeling
- **abracadabra**: A/B testing library for Python

### Online Resources
- [Evan Miller's A/B Testing Tools](https://www.evanmiller.org/ab-testing/)
- [Optimizely Stats Engine](https://www.optimizely.com/optimization-glossary/statistical-significance/)
- [GrowthBook Documentation](https://docs.growthbook.io/statistics)

### Industry Standards
- ISO 3534-1:2006 - Statistics vocabulary
- American Statistical Association: "P-Values and Statistical Significance: What Everyone Should Know"

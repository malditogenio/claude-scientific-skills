---
name: pricing-optimization
description: Optimize pricing strategy through price elasticity analysis, willingness-to-pay studies, and A/B testing. Calculate optimal price points, analyze price sensitivity, segment pricing strategies, measure revenue impact, and implement data-driven pricing decisions for revenue maximization.
---

# Pricing Optimization

## Overview

Pricing optimization uses data analysis to determine the optimal price points that maximize revenue, profit, or customer acquisition. Understanding price elasticity, customer willingness-to-pay, and competitive dynamics enables evidence-based pricing decisions rather than gut feel.

**Key Capabilities:**
- Price elasticity calculation
- Willingness-to-pay (WTP) analysis
- Van Westendorp Price Sensitivity Meter
- Revenue optimization modeling
- Price testing and A/B experiments
- Price discrimination and segmentation
- Competitive pricing analysis

## When to Use This Skill

Use this skill when:
- Setting initial pricing for new products
- Optimizing existing pricing tiers
- Evaluating price increase impacts
- Designing promotional discounts
- Creating price segmentation strategies
- Measuring price sensitivity
- Maximizing revenue or profit

## Core Capabilities

### 1. Price Elasticity Calculation

Measure how demand changes with price.

```python
import pandas as pd
import numpy as np
from scipy import stats

def calculate_price_elasticity(
    price_data: pd.DataFrame,
    price_col: str = 'price',
    quantity_col: str = 'quantity_sold',
    method: str = 'log-log'
) -> dict:
    """
    Calculate price elasticity of demand.

    Elasticity = % change in quantity / % change in price

    Parameters:
    -----------
    price_data : DataFrame with price and quantity data
    price_col : Price column
    quantity_col : Quantity sold column
    method : 'log-log' (constant elasticity) or 'point' (point elasticity)

    Returns:
    --------
    dict with elasticity metrics
    """
    # Ensure data is sorted by price
    df = price_data.sort_values(price_col).copy()

    if method == 'log-log':
        # Log-log regression for constant elasticity
        # ln(Q) = a + b*ln(P)
        # Elasticity = b

        log_price = np.log(df[price_col])
        log_quantity = np.log(df[quantity_col])

        # Linear regression on logs
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            log_price, log_quantity
        )

        elasticity = slope
        r_squared = r_value ** 2

        return {
            'elasticity': elasticity,
            'r_squared': r_squared,
            'p_value': p_value,
            'method': 'log-log',
            'interpretation': (
                'Elastic (sensitive)' if elasticity < -1
                else 'Inelastic (not sensitive)' if elasticity > -1
                else 'Unit elastic'
            )
        }

    else:  # point elasticity
        # Calculate elasticity at each point
        df['pct_change_price'] = df[price_col].pct_change()
        df['pct_change_quantity'] = df[quantity_col].pct_change()

        df['point_elasticity'] = (
            df['pct_change_quantity'] / df['pct_change_price']
        )

        # Average elasticity
        avg_elasticity = df['point_elasticity'].mean()

        return {
            'elasticity': avg_elasticity,
            'method': 'point',
            'elasticity_by_price': df[[price_col, 'point_elasticity']].to_dict('records')
        }

# Example: Generate pricing data
np.random.seed(42)

# Simulate demand curve: Q = 1000 - 5*P + noise
prices = np.arange(50, 200, 10)
pricing_data = []

for price in prices:
    # Demand decreases with price (elasticity of about -1.5)
    base_quantity = 1000 * (price / 100) ** -1.5
    quantity = base_quantity + np.random.normal(0, base_quantity * 0.1)

    pricing_data.append({
        'price': price,
        'quantity_sold': max(0, quantity)
    })

pricing_df = pd.DataFrame(pricing_data)

# Calculate elasticity
elasticity_results = calculate_price_elasticity(pricing_df)

print("Price Elasticity Analysis:")
print(f"Elasticity: {elasticity_results['elasticity']:.2f}")
print(f"R-squared: {elasticity_results.get('r_squared', 'N/A')}")
print(f"Interpretation: {elasticity_results.get('interpretation', 'N/A')}")

if elasticity_results['elasticity'] < -1:
    print("\n→ Elastic demand: Lowering price increases total revenue")
else:
    print("\n→ Inelastic demand: Raising price increases total revenue")
```

### 2. Revenue Optimization

Find the revenue-maximizing price point.

```python
def optimize_price_for_revenue(
    price_range: tuple,
    demand_function,
    cost_per_unit: float = 0,
    n_points: int = 100
) -> dict:
    """
    Find optimal price to maximize revenue or profit.

    Parameters:
    -----------
    price_range : (min_price, max_price) tuple
    demand_function : Function that takes price and returns quantity
    cost_per_unit : Variable cost per unit (for profit optimization)
    n_points : Number of price points to evaluate

    Returns:
    --------
    dict with optimal price and metrics
    """
    prices = np.linspace(price_range[0], price_range[1], n_points)

    results = []

    for price in prices:
        quantity = demand_function(price)
        revenue = price * quantity
        cost = cost_per_unit * quantity
        profit = revenue - cost

        results.append({
            'price': price,
            'quantity': quantity,
            'revenue': revenue,
            'profit': profit
        })

    results_df = pd.DataFrame(results)

    # Find optimal prices
    optimal_revenue_idx = results_df['revenue'].idxmax()
    optimal_profit_idx = results_df['profit'].idxmax()

    optimal_revenue = results_df.loc[optimal_revenue_idx]
    optimal_profit = results_df.loc[optimal_profit_idx]

    return {
        'optimal_price_revenue': optimal_revenue['price'],
        'optimal_quantity_revenue': optimal_revenue['quantity'],
        'max_revenue': optimal_revenue['revenue'],
        'optimal_price_profit': optimal_profit['price'],
        'optimal_quantity_profit': optimal_profit['quantity'],
        'max_profit': optimal_profit['profit'],
        'price_quantity_curve': results_df
    }

# Example: Optimize price
# Define demand function based on elasticity
def demand_function(price, base_demand=1000, base_price=100, elasticity=-1.5):
    return base_demand * (price / base_price) ** elasticity

optimization_results = optimize_price_for_revenue(
    price_range=(50, 200),
    demand_function=demand_function,
    cost_per_unit=30,
    n_points=150
)

print("\n\nPrice Optimization Results:")
print(f"Optimal price (revenue): ${optimization_results['optimal_price_revenue']:.2f}")
print(f"Expected quantity: {optimization_results['optimal_quantity_revenue']:.0f}")
print(f"Expected revenue: ${optimization_results['max_revenue']:,.0f}")

print(f"\nOptimal price (profit): ${optimization_results['optimal_price_profit']:.2f}")
print(f"Expected quantity: {optimization_results['optimal_quantity_profit']:.0f}")
print(f"Expected profit: ${optimization_results['max_profit']:,.0f}")
```

### 3. Van Westendorp Price Sensitivity Meter

Survey-based method to find acceptable price ranges.

```python
def van_westendorp_analysis(
    survey_df: pd.DataFrame,
    too_cheap_col: str = 'too_cheap',
    cheap_col: str = 'cheap',
    expensive_col: str = 'expensive',
    too_expensive_col: str = 'too_expensive'
) -> dict:
    """
    Analyze Van Westendorp Price Sensitivity Meter data.

    Survey asks 4 questions:
    1. At what price would this be too cheap (suspicious quality)?
    2. At what price would this be a bargain?
    3. At what price would this start to seem expensive?
    4. At what price would this be too expensive?

    Parameters:
    -----------
    survey_df : DataFrame with survey responses
    too_cheap_col, cheap_col, expensive_col, too_expensive_col : Column names

    Returns:
    --------
    dict with optimal price range
    """
    # Create price points for analysis
    all_prices = pd.concat([
        survey_df[too_cheap_col],
        survey_df[cheap_col],
        survey_df[expensive_col],
        survey_df[too_expensive_col]
    ])

    price_points = np.linspace(all_prices.min(), all_prices.max(), 200)

    # Calculate cumulative percentages
    analysis_data = []

    for price in price_points:
        # % who say it's too cheap at this price
        pct_too_cheap = (survey_df[too_cheap_col] >= price).mean() * 100

        # % who say it's not a bargain (too expensive) at this price
        pct_not_cheap = (survey_df[cheap_col] < price).mean() * 100

        # % who say it's expensive at this price
        pct_expensive = (survey_df[expensive_col] <= price).mean() * 100

        # % who say it's not too expensive at this price
        pct_not_too_expensive = (survey_df[too_expensive_col] > price).mean() * 100

        analysis_data.append({
            'price': price,
            'too_cheap': pct_too_cheap,
            'not_bargain': pct_not_cheap,
            'expensive': pct_expensive,
            'not_too_expensive': pct_not_too_expensive
        })

    analysis_df = pd.DataFrame(analysis_data)

    # Find key price points
    # Point of Marginal Cheapness: too_cheap = expensive
    pmc_idx = (analysis_df['too_cheap'] - analysis_df['expensive']).abs().idxmin()
    pmc = analysis_df.loc[pmc_idx, 'price']

    # Point of Marginal Expensiveness: not_bargain = not_too_expensive
    pme_idx = (analysis_df['not_bargain'] - analysis_df['not_too_expensive']).abs().idxmin()
    pme = analysis_df.loc[pme_idx, 'price']

    # Optimal Price Point: not_bargain = expensive
    opp_idx = (analysis_df['not_bargain'] - analysis_df['expensive']).abs().idxmin()
    opp = analysis_df.loc[opp_idx, 'price']

    # Indifference Price Point: too_cheap = too_expensive (inverted)
    analysis_df['too_expensive_pct'] = 100 - analysis_df['not_too_expensive']
    ipp_idx = (analysis_df['too_cheap'] - analysis_df['too_expensive_pct']).abs().idxmin()
    ipp = analysis_df.loc[ipp_idx, 'price']

    return {
        'point_of_marginal_cheapness': pmc,
        'point_of_marginal_expensiveness': pme,
        'optimal_price_point': opp,
        'indifference_price_point': ipp,
        'acceptable_price_range': (pmc, pme),
        'analysis_data': analysis_df
    }

# Example: Generate Van Westendorp survey data
np.random.seed(42)
n_respondents = 500

survey_data = []

for _ in range(n_respondents):
    # Generate responses with some correlation
    base_value = np.random.normal(100, 30)

    too_cheap = max(10, base_value * np.random.uniform(0.3, 0.6))
    cheap = max(too_cheap, base_value * np.random.uniform(0.7, 0.9))
    expensive = max(cheap, base_value * np.random.uniform(1.1, 1.3))
    too_expensive = max(expensive, base_value * np.random.uniform(1.4, 2.0))

    survey_data.append({
        'too_cheap': too_cheap,
        'cheap': cheap,
        'expensive': expensive,
        'too_expensive': too_expensive
    })

survey_df = pd.DataFrame(survey_data)

# Analyze
vw_results = van_westendorp_analysis(survey_df)

print("\n\nVan Westendorp Price Sensitivity Analysis:")
print(f"Point of Marginal Cheapness: ${vw_results['point_of_marginal_cheapness']:.2f}")
print(f"Optimal Price Point: ${vw_results['optimal_price_point']:.2f}")
print(f"Indifference Price Point: ${vw_results['indifference_price_point']:.2f}")
print(f"Point of Marginal Expensiveness: ${vw_results['point_of_marginal_expensiveness']:.2f}")
print(f"\nAcceptable Price Range: ${vw_results['acceptable_price_range'][0]:.2f} - "
      f"${vw_results['acceptable_price_range'][1]:.2f}")
```

### 4. Price Testing Framework

Design and analyze price experiments.

```python
def analyze_price_test(
    test_df: pd.DataFrame,
    price_col: str = 'price',
    conversion_col: str = 'converted',
    revenue_col: str = 'revenue'
) -> pd.DataFrame:
    """
    Analyze A/B test results for different price points.

    Parameters:
    -----------
    test_df : DataFrame with test data
    price_col : Price variant column
    conversion_col : Conversion indicator (0/1)
    revenue_col : Revenue column

    Returns:
    --------
    DataFrame with test results by price
    """
    # Aggregate by price variant
    results = test_df.groupby(price_col).agg({
        conversion_col: ['count', 'sum', 'mean'],
        revenue_col: ['sum', 'mean']
    }).reset_index()

    results.columns = [
        'price', 'visitors', 'conversions', 'conversion_rate',
        'total_revenue', 'revenue_per_visitor'
    ]

    # Calculate confidence intervals for conversion rate
    from scipy import stats

    for idx, row in results.iterrows():
        n = row['visitors']
        p = row['conversion_rate']

        # Wilson score interval
        z = 1.96  # 95% confidence
        denominator = 1 + z**2/n
        centre_adjusted_probability = p + z**2 / (2*n)
        adjusted_standard_deviation = np.sqrt((p*(1 - p) + z**2 / (4*n)) / n)

        lower_bound = (centre_adjusted_probability - z * adjusted_standard_deviation) / denominator
        upper_bound = (centre_adjusted_probability + z * adjusted_standard_deviation) / denominator

        results.loc[idx, 'conversion_rate_ci_lower'] = lower_bound
        results.loc[idx, 'conversion_rate_ci_upper'] = upper_bound

    # Calculate statistical significance vs. lowest price
    base_price = results['price'].min()
    base_row = results[results['price'] == base_price].iloc[0]

    for idx, row in results[results['price'] != base_price].iterrows():
        # Two-proportion z-test
        n1, p1 = base_row['visitors'], base_row['conversion_rate']
        n2, p2 = row['visitors'], row['conversion_rate']

        pooled_p = (n1*p1 + n2*p2) / (n1 + n2)
        se = np.sqrt(pooled_p * (1 - pooled_p) * (1/n1 + 1/n2))
        z_stat = (p2 - p1) / se if se > 0 else 0
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

        results.loc[idx, 'p_value_vs_base'] = p_value
        results.loc[idx, 'significant'] = p_value < 0.05

    return results

# Example: Generate price test data
np.random.seed(42)

price_variants = [49, 79, 99, 129]
test_data = []

for price in price_variants:
    # Higher price = lower conversion but higher revenue per customer
    base_conversion_rate = 0.10 * (100 / price) ** 0.5
    n_visitors = 1000

    for _ in range(n_visitors):
        converted = np.random.random() < base_conversion_rate
        revenue = price if converted else 0

        test_data.append({
            'price': price,
            'converted': int(converted),
            'revenue': revenue
        })

test_df = pd.DataFrame(test_data)

# Analyze test
price_test_results = analyze_price_test(test_df)

print("\n\nPrice Test Results:")
print(price_test_results[['price', 'visitors', 'conversions', 'conversion_rate',
                          'revenue_per_visitor', 'p_value_vs_base']].to_string(index=False))

# Find best price
best_price_idx = price_test_results['revenue_per_visitor'].idxmax()
best_price = price_test_results.loc[best_price_idx]

print(f"\nBest Price Point: ${best_price['price']:.0f}")
print(f"  Conversion Rate: {best_price['conversion_rate']:.2%}")
print(f"  Revenue per Visitor: ${best_price['revenue_per_visitor']:.2f}")
```

### 5. Price Discrimination Analysis

Analyze pricing by customer segment.

```python
def analyze_price_discrimination(
    customer_df: pd.DataFrame,
    segment_col: str = 'segment',
    wtp_col: str = 'willingness_to_pay',
    price_col: str = 'price_paid'
) -> dict:
    """
    Analyze price discrimination opportunity across segments.

    Parameters:
    -----------
    customer_df : DataFrame with customer data
    segment_col : Customer segment column
    wtp_col : Willingness-to-pay column
    price_col : Price paid column

    Returns:
    --------
    dict with discrimination analysis
    """
    # Aggregate by segment
    segment_analysis = customer_df.groupby(segment_col).agg({
        wtp_col: ['mean', 'median', 'std'],
        price_col: 'mean',
        'customer_id': 'count'
    }).reset_index()

    segment_analysis.columns = [
        'segment', 'avg_wtp', 'median_wtp', 'std_wtp',
        'avg_price_paid', 'customers'
    ]

    # Calculate consumer surplus (WTP - Price Paid)
    segment_analysis['consumer_surplus'] = (
        segment_analysis['avg_wtp'] - segment_analysis['avg_price_paid']
    )

    # Calculate potential revenue gain from perfect price discrimination
    segment_analysis['potential_revenue_gain'] = (
        segment_analysis['consumer_surplus'] * segment_analysis['customers']
    )

    # Total potential gain
    total_potential = segment_analysis['potential_revenue_gain'].sum()
    current_revenue = (segment_analysis['avg_price_paid'] *
                      segment_analysis['customers']).sum()

    potential_lift = total_potential / current_revenue * 100 if current_revenue > 0 else 0

    return {
        'segment_analysis': segment_analysis,
        'total_potential_revenue_gain': total_potential,
        'current_revenue': current_revenue,
        'potential_revenue_lift_pct': potential_lift
    }

# Example: Analyze price discrimination opportunity
np.random.seed(42)

segments = ['Enterprise', 'SMB', 'Individual']
segment_data = []

for segment in segments:
    if segment == 'Enterprise':
        n_customers = 200
        avg_wtp = 500
        current_price = 350
    elif segment == 'SMB':
        n_customers = 500
        avg_wtp = 200
        current_price = 150
    else:  # Individual
        n_customers = 1000
        avg_wtp = 80
        current_price = 79

    for i in range(n_customers):
        wtp = np.random.normal(avg_wtp, avg_wtp * 0.3)

        segment_data.append({
            'customer_id': f"{segment}_{i}",
            'segment': segment,
            'willingness_to_pay': max(0, wtp),
            'price_paid': current_price
        })

segment_df = pd.DataFrame(segment_data)

# Analyze discrimination opportunity
discrimination_analysis = analyze_price_discrimination(segment_df)

print("\n\nPrice Discrimination Analysis:")
print(discrimination_analysis['segment_analysis'].to_string(index=False))
print(f"\nTotal Potential Revenue Gain: ${discrimination_analysis['total_potential_revenue_gain']:,.0f}")
print(f"Potential Revenue Lift: {discrimination_analysis['potential_revenue_lift_pct']:.1f}%")
```

### 6. Competitive Pricing Analysis

Analyze pricing relative to competitors.

```python
def analyze_competitive_pricing(
    your_price: float,
    competitor_prices: list,
    your_features: int,
    competitor_features: list
) -> dict:
    """
    Analyze your pricing position relative to competitors.

    Parameters:
    -----------
    your_price : Your product price
    competitor_prices : List of competitor prices
    your_features : Your feature count/score
    competitor_features : List of competitor feature counts

    Returns:
    --------
    dict with competitive analysis
    """
    # Price positioning
    avg_competitor_price = np.mean(competitor_prices)
    price_premium = (your_price - avg_competitor_price) / avg_competitor_price * 100

    # Value positioning (price per feature)
    your_price_per_feature = your_price / your_features if your_features > 0 else 0

    competitor_price_per_feature = [
        price / features if features > 0 else 0
        for price, features in zip(competitor_prices, competitor_features)
    ]

    avg_competitor_price_per_feature = np.mean(competitor_price_per_feature)

    value_premium = (
        (your_price_per_feature - avg_competitor_price_per_feature) /
        avg_competitor_price_per_feature * 100
        if avg_competitor_price_per_feature > 0 else 0
    )

    # Positioning
    if your_price > avg_competitor_price * 1.2:
        price_position = "Premium"
    elif your_price < avg_competitor_price * 0.8:
        price_position = "Budget"
    else:
        price_position = "Market"

    if your_price_per_feature < avg_competitor_price_per_feature * 0.9:
        value_position = "Best Value"
    elif your_price_per_feature > avg_competitor_price_per_feature * 1.1:
        value_position = "Premium Value"
    else:
        value_position = "Market Value"

    return {
        'your_price': your_price,
        'avg_competitor_price': avg_competitor_price,
        'price_premium_pct': price_premium,
        'price_position': price_position,
        'your_price_per_feature': your_price_per_feature,
        'avg_competitor_price_per_feature': avg_competitor_price_per_feature,
        'value_premium_pct': value_premium,
        'value_position': value_position
    }

# Example: Analyze competitive positioning
competitive_analysis = analyze_competitive_pricing(
    your_price=99,
    competitor_prices=[79, 89, 119, 129, 149],
    your_features=25,
    competitor_features=[20, 22, 30, 28, 35]
)

print("\n\nCompetitive Pricing Analysis:")
print(f"Your Price: ${competitive_analysis['your_price']:.0f}")
print(f"Average Competitor Price: ${competitive_analysis['avg_competitor_price']:.0f}")
print(f"Price Premium: {competitive_analysis['price_premium_pct']:+.1f}%")
print(f"Price Position: {competitive_analysis['price_position']}")

print(f"\nYour Price per Feature: ${competitive_analysis['your_price_per_feature']:.2f}")
print(f"Avg Competitor Price per Feature: ${competitive_analysis['avg_competitor_price_per_feature']:.2f}")
print(f"Value Premium: {competitive_analysis['value_premium_pct']:+.1f}%")
print(f"Value Position: {competitive_analysis['value_position']}")
```

## Best Practices

### 1. Pricing Research Methods
- **Van Westendorp**: Quick survey-based acceptable price range
- **Conjoint Analysis**: Trade-off between price and features
- **Price Testing**: A/B test actual purchase behavior
- **Elasticity Studies**: Analyze historical price-demand relationship

### 2. Setting Prices
- **Value-based**: Price based on customer value, not cost
- **Competitive**: Understand competitive landscape
- **Psychological**: Use charm pricing ($99 vs $100)
- **Anchoring**: Show higher-priced option first

### 3. Price Testing
- **Test meaningful differences**: At least 10-20% price difference
- **Sufficient sample size**: Need statistical power
- **Control for seasonality**: Test during comparable periods
- **Measure long-term**: Price affects LTV, not just initial conversion

### 4. Common Pitfalls to Avoid
- **Racing to bottom**: Competing only on price
- **Ignoring segments**: Different customers have different WTP
- **Cost-plus pricing**: Doesn't reflect value
- **Fear of raising prices**: Often underestimate customer value perception

### 5. Dynamic Pricing
- **Time-based**: Different prices by time of day/season
- **Demand-based**: Surge pricing when demand is high
- **Personalized**: Different prices by segment (carefully)
- **Promotional**: Strategic discounts for acquisition/activation

## References

### Methodology
- Nagle, T. T., & Holden, R. K. (2002). "The Strategy and Tactics of Pricing"
- Dolan, R. J., & Simon, H. (1996). "Power Pricing"
- Van Westendorp, P. (1976). "Price Sensitivity Meter"

### Tools and Libraries
- **pandas**: Data analysis
- **scipy**: Statistical tests
- **numpy**: Numerical calculations

### Industry Benchmarks
- **SaaS**: 10-20% annual price increases typical
- **E-commerce**: -1.5 to -2.0 elasticity common
- **Freemium**: 2-5% conversion rates
- **Price Testing**: Minimum 15% difference to detect

### Additional Resources
- ProfitWell. "The SaaS Pricing Strategy Guide"
- PriceIntelligently. "The Complete Guide to SaaS Pricing Models"
- Simon-Kucher. "Pricing Best Practices"

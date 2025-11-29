---
name: market-basket-analysis
description: Discover product associations and cross-sell opportunities using market basket analysis. Implement association rule mining (Apriori algorithm), calculate support, confidence, and lift metrics. Identify product bundles, optimize product placement, and create data-driven cross-sell recommendations.
---

# Market Basket Analysis

## Overview

Market Basket Analysis (MBA) identifies products that are frequently purchased together, revealing hidden patterns in customer purchasing behavior. This technique uses association rule mining to discover relationships between items, enabling cross-sell recommendations, product bundling, and optimized product placement.

**Key Capabilities:**
- Association rule mining (Apriori algorithm)
- Support, confidence, and lift calculation
- Product affinity analysis
- Cross-sell recommendation generation
- Product bundle identification
- Sequential pattern analysis
- Recommendation system optimization

## When to Use This Skill

Use this skill when:
- Identifying cross-sell opportunities
- Creating product bundles
- Optimizing product placement
- Building recommendation engines
- Analyzing purchase patterns
- Designing promotional bundles
- Planning inventory based on co-purchase patterns

## Core Capabilities

### 1. Basic Market Basket Analysis

Prepare transaction data and calculate basic metrics.

```python
import pandas as pd
import numpy as np
from collections import defaultdict
from itertools import combinations

def prepare_transaction_data(
    df: pd.DataFrame,
    transaction_col: str = 'transaction_id',
    item_col: str = 'product_id'
) -> list:
    """
    Prepare transaction data for market basket analysis.

    Parameters:
    -----------
    df : DataFrame with transaction-level data
    transaction_col : Transaction identifier column
    item_col : Item/product column

    Returns:
    --------
    list of transactions (each transaction is a list of items)
    """
    transactions = df.groupby(transaction_col)[item_col].apply(list).tolist()
    return transactions

def calculate_support(
    transactions: list,
    itemset: set,
    total_transactions: int = None
) -> float:
    """
    Calculate support for an itemset.

    Support = # transactions containing itemset / total transactions

    Parameters:
    -----------
    transactions : List of transactions
    itemset : Set of items to check
    total_transactions : Total number of transactions

    Returns:
    --------
    float: Support value (0 to 1)
    """
    if total_transactions is None:
        total_transactions = len(transactions)

    # Count transactions containing all items in itemset
    count = sum(1 for transaction in transactions if itemset.issubset(set(transaction)))

    support = count / total_transactions if total_transactions > 0 else 0

    return support

# Example: Generate sample transaction data
np.random.seed(42)

# Product catalog
products = [
    'Laptop', 'Mouse', 'Keyboard', 'Monitor', 'USB Cable',
    'HDMI Cable', 'Laptop Bag', 'Webcam', 'Headphones',
    'External HD', 'Mouse Pad', 'Desk Lamp'
]

# Product associations (some products are more likely to be bought together)
associations = {
    'Laptop': ['Mouse', 'Laptop Bag', 'USB Cable'],
    'Monitor': ['HDMI Cable', 'Desk Lamp'],
    'Mouse': ['Mouse Pad', 'Keyboard'],
    'Webcam': ['Headphones'],
}

# Generate transactions
n_transactions = 1000
transactions_data = []

for transaction_id in range(n_transactions):
    # Random number of items per transaction (1-5)
    n_items = np.random.randint(1, 6)

    # Start with random product
    items = [np.random.choice(products)]

    # Add associated products with some probability
    for _ in range(n_items - 1):
        if items[-1] in associations and np.random.random() < 0.7:
            # Add associated product
            associated = np.random.choice(associations[items[-1]])
            if associated not in items:
                items.append(associated)
        else:
            # Add random product
            random_product = np.random.choice(products)
            if random_product not in items:
                items.append(random_product)

    # Add items to transaction data
    for item in items:
        transactions_data.append({
            'transaction_id': transaction_id,
            'product_id': item
        })

transactions_df = pd.DataFrame(transactions_data)

print("Sample Transactions:")
print(transactions_df.head(20))

# Prepare transaction list
transactions_list = prepare_transaction_data(transactions_df)

print(f"\nTotal Transactions: {len(transactions_list)}")
print(f"Average items per transaction: {len(transactions_data) / len(transactions_list):.1f}")

# Calculate support for some itemsets
example_itemsets = [
    {'Laptop'},
    {'Laptop', 'Mouse'},
    {'Laptop', 'Mouse', 'Laptop Bag'}
]

print("\nItemset Support:")
for itemset in example_itemsets:
    support = calculate_support(transactions_list, itemset)
    print(f"  {itemset}: {support:.3f} ({support*100:.1f}%)")
```

### 2. Association Rule Mining (Apriori Algorithm)

Find frequent itemsets and generate association rules.

```python
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

def find_association_rules(
    transactions: list,
    min_support: float = 0.01,
    min_confidence: float = 0.3,
    min_lift: float = 1.0,
    max_length: int = 3
) -> pd.DataFrame:
    """
    Find association rules using Apriori algorithm.

    Parameters:
    -----------
    transactions : List of transactions
    min_support : Minimum support threshold
    min_confidence : Minimum confidence threshold
    min_lift : Minimum lift threshold
    max_length : Maximum itemset size

    Returns:
    --------
    DataFrame with association rules
    """
    # Encode transactions as binary matrix
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

    # Find frequent itemsets
    frequent_itemsets = apriori(
        df_encoded,
        min_support=min_support,
        use_colnames=True,
        max_len=max_length
    )

    if len(frequent_itemsets) == 0:
        print("No frequent itemsets found. Try lowering min_support.")
        return pd.DataFrame()

    # Generate association rules
    rules = association_rules(
        frequent_itemsets,
        metric="confidence",
        min_threshold=min_confidence
    )

    # Filter by lift
    rules = rules[rules['lift'] >= min_lift]

    # Sort by lift
    rules = rules.sort_values('lift', ascending=False)

    return rules

# Example: Find association rules
rules = find_association_rules(
    transactions_list,
    min_support=0.02,  # 2% of transactions
    min_confidence=0.3,  # 30% confidence
    min_lift=1.2,  # 20% lift over random
    max_length=3
)

print("\nTop Association Rules:")
if len(rules) > 0:
    print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(20).to_string(index=False))
else:
    print("No rules found with current thresholds.")
```

### 3. Cross-Sell Recommendations

Generate product recommendations based on basket analysis.

```python
def generate_cross_sell_recommendations(
    rules_df: pd.DataFrame,
    product: str,
    top_n: int = 5,
    min_confidence: float = 0.3
) -> pd.DataFrame:
    """
    Generate cross-sell recommendations for a product.

    Parameters:
    -----------
    rules_df : DataFrame with association rules
    product : Product to get recommendations for
    top_n : Number of recommendations
    min_confidence : Minimum confidence threshold

    Returns:
    --------
    DataFrame with recommendations
    """
    # Filter rules where product is in antecedents
    product_rules = rules_df[
        rules_df['antecedents'].apply(lambda x: product in x) &
        (rules_df['confidence'] >= min_confidence)
    ].copy()

    if len(product_rules) == 0:
        return pd.DataFrame()

    # Extract recommended products
    recommendations = []

    for _, rule in product_rules.iterrows():
        consequents = list(rule['consequents'])

        for rec_product in consequents:
            recommendations.append({
                'recommended_product': rec_product,
                'confidence': rule['confidence'],
                'lift': rule['lift'],
                'support': rule['support']
            })

    recommendations_df = pd.DataFrame(recommendations)

    # Aggregate (product might appear in multiple rules)
    recommendations_agg = recommendations_df.groupby('recommended_product').agg({
        'confidence': 'mean',
        'lift': 'mean',
        'support': 'mean'
    }).reset_index()

    # Sort by lift and confidence
    recommendations_agg['score'] = (
        recommendations_agg['lift'] * recommendations_agg['confidence']
    )

    recommendations_agg = recommendations_agg.sort_values('score', ascending=False).head(top_n)

    return recommendations_agg

# Example: Get recommendations for specific products
for product in ['Laptop', 'Mouse', 'Monitor']:
    print(f"\nCross-sell recommendations for {product}:")
    recommendations = generate_cross_sell_recommendations(rules, product, top_n=5)

    if len(recommendations) > 0:
        print(recommendations.to_string(index=False))
    else:
        print("  No recommendations found")
```

### 4. Product Affinity Matrix

Create a matrix showing affinity between all products.

```python
def create_affinity_matrix(
    transactions: list,
    products: list = None
) -> pd.DataFrame:
    """
    Create product affinity matrix.

    Affinity = P(A and B) / (P(A) * P(B))
    = Lift of rule A -> B

    Parameters:
    -----------
    transactions : List of transactions
    products : List of products to analyze (None = all products)

    Returns:
    --------
    DataFrame: Affinity matrix
    """
    # Get all unique products if not specified
    if products is None:
        products = list(set([item for transaction in transactions for item in transaction]))

    n_transactions = len(transactions)

    # Calculate support for each product
    product_support = {}
    for product in products:
        support = calculate_support(transactions, {product}, n_transactions)
        product_support[product] = support

    # Calculate affinity matrix
    affinity_matrix = pd.DataFrame(index=products, columns=products, dtype=float)

    for prod_a in products:
        for prod_b in products:
            if prod_a == prod_b:
                affinity_matrix.loc[prod_a, prod_b] = 1.0
            else:
                # Calculate joint support
                joint_support = calculate_support(
                    transactions,
                    {prod_a, prod_b},
                    n_transactions
                )

                # Calculate affinity (lift)
                expected_support = product_support[prod_a] * product_support[prod_b]

                if expected_support > 0:
                    affinity = joint_support / expected_support
                else:
                    affinity = 0

                affinity_matrix.loc[prod_a, prod_b] = affinity

    return affinity_matrix.astype(float)

# Example: Create affinity matrix
top_products = transactions_df['product_id'].value_counts().head(8).index.tolist()
affinity_matrix = create_affinity_matrix(transactions_list, top_products)

print("\n\nProduct Affinity Matrix (Lift):")
print(affinity_matrix.round(2))

# Visualize affinity matrix
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(10, 8))

sns.heatmap(
    affinity_matrix,
    annot=True,
    fmt='.2f',
    cmap='RdYlGn',
    center=1.0,
    vmin=0,
    vmax=3,
    ax=ax,
    cbar_kws={'label': 'Affinity (Lift)'}
)

ax.set_title('Product Affinity Matrix', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('affinity_matrix.png', dpi=300, bbox_inches='tight')
print("\nAffinity matrix visualization saved to: affinity_matrix.png")
```

### 5. Product Bundle Recommendations

Identify optimal product bundles.

```python
def identify_product_bundles(
    rules_df: pd.DataFrame,
    min_items: int = 2,
    max_items: int = 4,
    min_support: float = 0.02,
    min_lift: float = 1.5
) -> pd.DataFrame:
    """
    Identify product bundles based on association rules.

    Parameters:
    -----------
    rules_df : DataFrame with association rules
    min_items : Minimum items in bundle
    max_items : Maximum items in bundle
    min_support : Minimum support threshold
    min_lift : Minimum lift threshold

    Returns:
    --------
    DataFrame with bundle recommendations
    """
    bundles = []

    for _, rule in rules_df.iterrows():
        # Combine antecedents and consequents to form bundle
        bundle = set(rule['antecedents']) | set(rule['consequents'])

        if min_items <= len(bundle) <= max_items:
            if rule['support'] >= min_support and rule['lift'] >= min_lift:
                bundles.append({
                    'bundle': frozenset(bundle),
                    'bundle_items': ', '.join(sorted(bundle)),
                    'support': rule['support'],
                    'confidence': rule['confidence'],
                    'lift': rule['lift'],
                    'bundle_size': len(bundle)
                })

    bundles_df = pd.DataFrame(bundles)

    if len(bundles_df) == 0:
        return pd.DataFrame()

    # Remove duplicate bundles
    bundles_df = bundles_df.drop_duplicates(subset=['bundle'])

    # Calculate bundle score
    bundles_df['bundle_score'] = (
        bundles_df['support'] * bundles_df['lift'] * bundles_df['confidence']
    )

    # Sort by score
    bundles_df = bundles_df.sort_values('bundle_score', ascending=False)

    return bundles_df[['bundle_items', 'bundle_size', 'support', 'lift',
                       'confidence', 'bundle_score']]

# Example: Identify bundles
bundles = identify_product_bundles(
    rules,
    min_items=2,
    max_items=3,
    min_support=0.02,
    min_lift=1.3
)

print("\n\nTop Product Bundles:")
if len(bundles) > 0:
    print(bundles.head(15).to_string(index=False))
else:
    print("No bundles found with current criteria")
```

### 6. Sequential Pattern Analysis

Analyze sequences of purchases over time.

```python
def analyze_sequential_patterns(
    df: pd.DataFrame,
    customer_col: str = 'customer_id',
    product_col: str = 'product_id',
    date_col: str = 'purchase_date',
    time_window_days: int = 30
) -> pd.DataFrame:
    """
    Analyze sequential purchase patterns.

    Find products commonly purchased after another product.

    Parameters:
    -----------
    df : DataFrame with purchase history
    customer_col : Customer identifier
    product_col : Product column
    date_col : Purchase date column
    time_window_days : Time window for sequences

    Returns:
    --------
    DataFrame with sequential patterns
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    # Sort by customer and date
    df = df.sort_values([customer_col, date_col])

    # Find sequential purchases
    sequences = []

    for customer in df[customer_col].unique():
        customer_purchases = df[df[customer_col] == customer]

        for i in range(len(customer_purchases) - 1):
            current_purchase = customer_purchases.iloc[i]
            next_purchase = customer_purchases.iloc[i + 1]

            days_between = (
                next_purchase[date_col] - current_purchase[date_col]
            ).days

            if 0 < days_between <= time_window_days:
                sequences.append({
                    'first_product': current_purchase[product_col],
                    'next_product': next_purchase[product_col],
                    'days_between': days_between
                })

    sequences_df = pd.DataFrame(sequences)

    if len(sequences_df) == 0:
        return pd.DataFrame()

    # Aggregate sequential patterns
    pattern_analysis = sequences_df.groupby(
        ['first_product', 'next_product']
    ).agg({
        'days_between': ['count', 'mean', 'median']
    }).reset_index()

    pattern_analysis.columns = [
        'first_product', 'next_product', 'frequency',
        'avg_days', 'median_days'
    ]

    # Sort by frequency
    pattern_analysis = pattern_analysis.sort_values('frequency', ascending=False)

    return pattern_analysis

# Example: Generate sequential purchase data
np.random.seed(42)

sequential_data = []
n_customers = 200

for customer_id in range(n_customers):
    # Number of purchases per customer
    n_purchases = np.random.randint(2, 10)

    start_date = pd.Timestamp('2024-01-01') + pd.Timedelta(
        days=np.random.randint(0, 60)
    )

    # First purchase
    first_product = np.random.choice(products)
    sequential_data.append({
        'customer_id': customer_id,
        'product_id': first_product,
        'purchase_date': start_date
    })

    current_date = start_date
    previous_product = first_product

    # Subsequent purchases (with associations)
    for _ in range(n_purchases - 1):
        # Days until next purchase
        days_until_next = np.random.gamma(2, 7)  # Average ~2 weeks
        current_date += pd.Timedelta(days=days_until_next)

        # Next product (potentially related)
        if previous_product in associations and np.random.random() < 0.5:
            next_product = np.random.choice(associations[previous_product])
        else:
            next_product = np.random.choice(products)

        sequential_data.append({
            'customer_id': customer_id,
            'product_id': next_product,
            'purchase_date': current_date
        })

        previous_product = next_product

sequential_df = pd.DataFrame(sequential_data)

# Analyze sequential patterns
sequential_patterns = analyze_sequential_patterns(
    sequential_df,
    time_window_days=30
)

print("\n\nTop Sequential Purchase Patterns:")
if len(sequential_patterns) > 0:
    print(sequential_patterns.head(15).to_string(index=False))
else:
    print("No sequential patterns found")
```

### 7. Recommendation Performance Analysis

Evaluate recommendation effectiveness.

```python
def evaluate_recommendation_performance(
    actual_purchases: pd.DataFrame,
    recommendations: pd.DataFrame,
    customer_col: str = 'customer_id',
    product_col: str = 'product_id',
    recommended_col: str = 'recommended_product'
) -> dict:
    """
    Evaluate how well recommendations match actual purchases.

    Parameters:
    -----------
    actual_purchases : DataFrame with actual customer purchases
    recommendations : DataFrame with recommendations made
    customer_col : Customer identifier
    product_col : Product column in actual purchases
    recommended_col : Recommended product column

    Returns:
    --------
    dict with evaluation metrics
    """
    # Get unique customer-product combinations
    actual_set = set(
        actual_purchases[[customer_col, product_col]].itertuples(index=False, name=None)
    )

    recommended_set = set(
        recommendations[[customer_col, recommended_col]].itertuples(index=False, name=None)
    )

    # Calculate metrics
    true_positives = len(actual_set & recommended_set)
    false_positives = len(recommended_set - actual_set)
    false_negatives = len(actual_set - recommended_set)

    # Precision: % of recommendations that were purchased
    precision = (
        true_positives / (true_positives + false_positives)
        if (true_positives + false_positives) > 0 else 0
    )

    # Recall: % of purchases that were recommended
    recall = (
        true_positives / (true_positives + false_negatives)
        if (true_positives + false_negatives) > 0 else 0
    )

    # F1 score
    f1_score = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0 else 0
    )

    return {
        'true_positives': true_positives,
        'false_positives': false_positives,
        'false_negatives': false_negatives,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'total_recommendations': len(recommended_set),
        'total_purchases': len(actual_set)
    }

print("\n\nRecommendation System Performance Metrics:")
print("(Metrics would be calculated with actual holdout test set)")
print("Precision: % of recommendations that were actually purchased")
print("Recall: % of purchases that were recommended")
print("F1 Score: Harmonic mean of precision and recall")
```

## Best Practices

### 1. Metric Selection
- **Support**: Frequency of itemset (higher = more common)
- **Confidence**: P(B|A) - probability of B given A
- **Lift**: How much more likely than random (>1 = positive association)
- **Use all three**: Balance frequency, accuracy, and strength

### 2. Threshold Setting
- **Support**: 0.5-5% for retail, 0.1-1% for rare items
- **Confidence**: 30-70% depending on use case
- **Lift**: >1.2 for meaningful associations
- **Adjust based on**: Industry, product catalog size, business goals

### 3. Implementation
- **Start simple**: Single itemsets, then pairs, then larger
- **Filter noise**: Remove too common or too rare items
- **Consider context**: Time of year, customer segment, channel
- **Validate**: Test recommendations with holdout data

### 4. Common Pitfalls to Avoid
- **Too low support**: Generates too many rules, many spurious
- **Ignoring lift**: High confidence doesn't mean strong association
- **Static recommendations**: Update regularly as patterns change
- **One-size-fits-all**: Segment customers for personalized recommendations

### 5. Business Applications
- **Cross-sell**: "Customers who bought X also bought Y"
- **Bundling**: Create product packages
- **Store layout**: Place related products nearby
- **Promotions**: Discount bundles of associated products
- **Inventory**: Stock complementary products together

## References

### Methodology
- Agrawal, R., & Srikant, R. (1994). "Fast Algorithms for Mining Association Rules"
- Han, J., Pei, J., & Yin, Y. (2000). "Mining Frequent Patterns without Candidate Generation"
- Berry, M. J., & Linoff, G. S. (2004). "Data Mining Techniques"

### Tools and Libraries
- **mlxtend**: Apriori algorithm implementation
- **pandas**: Data manipulation
- **numpy**: Numerical operations

### Industry Benchmarks
- **Retail**: Typical lift values 1.2-3.0 for strong associations
- **E-commerce**: 3-5% support threshold common
- **Grocery**: 10-30% confidence for cross-sell
- **Recommendation CTR**: 2-5% typical for product recommendations

### Additional Resources
- [MLxtend Association Rules](http://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/)
- Coursera. "Mining Massive Datasets"
- Kaggle. "Market Basket Analysis Tutorials"

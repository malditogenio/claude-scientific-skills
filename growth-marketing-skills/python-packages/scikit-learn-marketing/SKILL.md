---
name: scikit-learn-marketing
description: "Machine learning for marketing. Customer segmentation, churn prediction, propensity modeling, CLV prediction, recommendation systems, lead scoring."
---

# Scikit-learn for Marketing ML

## Overview

scikit-learn provides essential machine learning tools for marketing analytics. This skill covers customer segmentation, churn prediction, propensity scoring, lead prioritization, and other ML applications in marketing contexts.

## When to Use This Skill

- Building customer segmentation models
- Predicting customer churn
- Creating propensity-to-buy models
- Lead scoring and prioritization
- Customer lifetime value prediction
- Product recommendation systems
- Campaign response modeling

## Core Capabilities

### 1. Customer Segmentation with K-Means

```python
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# Prepare customer features
customers = pd.read_csv('customers.csv')
features = customers[['recency', 'frequency', 'monetary',
                       'avg_order_value', 'customer_lifetime_days']]

# Scale features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Find optimal number of clusters
silhouette_scores = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(features_scaled)
    score = silhouette_score(features_scaled, labels)
    silhouette_scores.append(score)
    print(f"K={k}: Silhouette Score = {score:.3f}")

# Fit final model
optimal_k = 5
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
customers['segment'] = kmeans.fit_predict(features_scaled)

# Analyze segments
segment_profile = customers.groupby('segment').agg({
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': 'mean',
    'customer_id': 'count'
}).rename(columns={'customer_id': 'count'})

print(segment_profile)
```

### 2. Churn Prediction Model

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder

# Prepare data
df = pd.read_csv('customer_data.csv')

# Feature engineering
features = ['days_since_last_purchase', 'total_orders', 'avg_order_value',
            'total_revenue', 'support_tickets', 'email_opens_30d',
            'app_sessions_30d', 'discount_usage_rate']

X = df[features]
y = df['churned']  # 1 = churned, 0 = active

# Handle missing values
X = X.fillna(X.median())

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
model = GradientBoostingClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("Classification Report:")
print(classification_report(y_test, y_pred))
print(f"ROC AUC: {roc_auc_score(y_test, y_proba):.3f}")

# Feature importance
importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
print("\nFeature Importance:")
print(importance)

# Score all customers
df['churn_probability'] = model.predict_proba(X)[:, 1]
df['churn_risk'] = pd.qcut(df['churn_probability'], 5,
                            labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
```

### 3. Propensity to Purchase Model

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Features for propensity model
numeric_features = ['page_views', 'time_on_site', 'email_clicks',
                    'previous_purchases', 'cart_abandons', 'days_since_signup']
categorical_features = ['traffic_source', 'device_type', 'customer_segment']

# Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Full pipeline
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(max_iter=1000, class_weight='balanced'))
])

# Train
X = df[numeric_features + categorical_features]
y = df['converted']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

# Score visitors
df['purchase_propensity'] = pipeline.predict_proba(X)[:, 1]

# Prioritize for targeting
high_propensity = df[df['purchase_propensity'] > 0.7]
```

### 4. Lead Scoring

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

# Lead features
lead_features = ['company_size', 'industry_score', 'website_visits',
                 'content_downloads', 'email_engagement', 'demo_requested',
                 'budget_indicated', 'decision_timeline_score']

X = leads_df[lead_features]
y = leads_df['converted_to_customer']

# Hyperparameter tuning
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 7],
    'min_samples_split': [2, 5, 10]
}

rf = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='roc_auc')
grid_search.fit(X, y)

print(f"Best parameters: {grid_search.best_params_}")
print(f"Best ROC AUC: {grid_search.best_score_:.3f}")

# Score leads
best_model = grid_search.best_estimator_
leads_df['lead_score'] = best_model.predict_proba(X)[:, 1] * 100

# Categorize leads
leads_df['lead_grade'] = pd.cut(
    leads_df['lead_score'],
    bins=[0, 25, 50, 75, 100],
    labels=['D', 'C', 'B', 'A']
)
```

### 5. Customer Lifetime Value Prediction

```python
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score

# CLV features (from first X days of customer activity)
clv_features = ['first_order_value', 'orders_first_30d', 'revenue_first_30d',
                'products_purchased_first_30d', 'avg_days_between_orders',
                'referral_source_score', 'email_engaged', 'app_user']

X = early_customers[clv_features]
y = early_customers['ltv_365']  # Actual LTV after 365 days

# Train regression model
model = GradientBoostingRegressor(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    random_state=42
)

# Cross-validation
cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
print(f"Cross-validation R²: {cv_scores.mean():.3f} (+/- {cv_scores.std()*2:.3f})")

model.fit(X, y)

# Predict CLV for new customers
new_customers['predicted_ltv'] = model.predict(new_customers[clv_features])

# Segment by predicted value
new_customers['value_tier'] = pd.qcut(
    new_customers['predicted_ltv'],
    4,
    labels=['Bronze', 'Silver', 'Gold', 'Platinum']
)
```

### 6. Market Basket Analysis (Association Rules)

```python
from sklearn.preprocessing import MultiLabelBinarizer
import itertools

# Prepare transaction data
transactions = df.groupby('order_id')['product_id'].apply(list).tolist()

# Create binary matrix
mlb = MultiLabelBinarizer()
basket = pd.DataFrame(
    mlb.fit_transform(transactions),
    columns=mlb.classes_
)

# Calculate support
support = basket.mean()

# Find frequent itemsets (simplified)
def get_frequent_pairs(basket, min_support=0.01):
    pairs = []
    products = basket.columns.tolist()

    for p1, p2 in itertools.combinations(products, 2):
        pair_support = (basket[p1] & basket[p2]).mean()
        if pair_support >= min_support:
            pairs.append({
                'product_1': p1,
                'product_2': p2,
                'support': pair_support,
                'lift': pair_support / (support[p1] * support[p2])
            })

    return pd.DataFrame(pairs).sort_values('lift', ascending=False)

frequent_pairs = get_frequent_pairs(basket)
print(frequent_pairs.head(20))
```

## Installation

```bash
uv pip install scikit-learn pandas numpy
```

## Quick Start

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

# Load data
df = pd.read_csv('customer_data.csv')

# Prepare features and target
X = df[['feature1', 'feature2', 'feature3']]
y = df['target']

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Score
print(f"Accuracy: {model.score(X_test, y_test):.3f}")
```

## Best Practices

1. **Handle imbalanced data** - Use class_weight='balanced' or SMOTE
2. **Feature scaling** - Always scale features for distance-based algorithms
3. **Cross-validation** - Use k-fold CV to evaluate model performance
4. **Feature importance** - Understand which features drive predictions
5. **Monitor for drift** - Retrain models as customer behavior changes

## References

- [scikit-learn Documentation](https://scikit-learn.org/stable/)
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)

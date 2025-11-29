---
name: churn-prediction
description: Build predictive models to identify customers at risk of churning. Use logistic regression, random forests, and gradient boosting to predict churn probability. Perform feature engineering, calculate churn risk scores, identify at-risk customers, and design retention interventions based on churn drivers.
---

# Churn Prediction

## Overview

Churn prediction uses machine learning to identify customers likely to stop using a product or service. By predicting churn before it happens, companies can proactively intervene with targeted retention efforts, improving customer lifetime value and reducing acquisition costs.

**Key Capabilities:**
- Churn probability prediction
- Feature engineering for churn models
- Logistic regression, random forest, and gradient boosting models
- Feature importance analysis
- At-risk customer identification
- Churn driver analysis
- Model evaluation and calibration

## When to Use This Skill

Use this skill when:
- Identifying customers at risk of churning
- Prioritizing retention efforts
- Understanding what drives churn
- Designing targeted retention campaigns
- Calculating customer health scores
- Optimizing resource allocation for customer success
- Measuring the impact of retention initiatives

## Core Capabilities

### 1. Feature Engineering for Churn

Create predictive features from customer data.

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def engineer_churn_features(
    transactions_df: pd.DataFrame,
    events_df: pd.DataFrame,
    support_df: pd.DataFrame = None,
    reference_date: pd.Timestamp = None,
    observation_period_days: int = 90,
    churn_definition_days: int = 30
) -> pd.DataFrame:
    """
    Engineer features for churn prediction.

    Parameters:
    -----------
    transactions_df : DataFrame with transaction history
    events_df : DataFrame with usage events
    support_df : DataFrame with support interactions (optional)
    reference_date : Date to calculate features from
    observation_period_days : Days to observe features
    churn_definition_days : Days of inactivity to define churn

    Returns:
    --------
    DataFrame with engineered features and churn label
    """
    if reference_date is None:
        reference_date = pd.Timestamp.now()

    observation_start = reference_date - pd.Timedelta(days=observation_period_days)
    churn_end = reference_date + pd.Timedelta(days=churn_definition_days)

    # Transaction features
    trans_features = transactions_df[
        (transactions_df['transaction_date'] >= observation_start) &
        (transactions_df['transaction_date'] < reference_date)
    ].groupby('customer_id').agg({
        'transaction_date': ['count', 'min', 'max'],
        'revenue': ['sum', 'mean', 'std']
    })

    trans_features.columns = [
        'transaction_count', 'first_transaction', 'last_transaction',
        'total_revenue', 'avg_transaction_value', 'std_transaction_value'
    ]

    # Recency (days since last transaction)
    trans_features['days_since_last_transaction'] = (
        reference_date - trans_features['last_transaction']
    ).dt.days

    # Frequency (transactions per day)
    trans_features['transaction_frequency'] = (
        trans_features['transaction_count'] / observation_period_days
    )

    # Transaction trend (recent vs. early)
    mid_point = observation_start + pd.Timedelta(days=observation_period_days / 2)

    recent_trans = transactions_df[
        (transactions_df['transaction_date'] >= mid_point) &
        (transactions_df['transaction_date'] < reference_date)
    ].groupby('customer_id').size()

    early_trans = transactions_df[
        (transactions_df['transaction_date'] >= observation_start) &
        (transactions_df['transaction_date'] < mid_point)
    ].groupby('customer_id').size()

    trans_features['transaction_trend'] = (
        recent_trans - early_trans
    ).fillna(0)

    # Event/usage features
    event_features = events_df[
        (events_df['event_date'] >= observation_start) &
        (events_df['event_date'] < reference_date)
    ].groupby('customer_id').agg({
        'event_date': ['count', 'nunique'],
        'event_type': lambda x: x.nunique()
    })

    event_features.columns = [
        'total_events', 'days_active', 'unique_event_types'
    ]

    event_features['events_per_day'] = (
        event_features['total_events'] / observation_period_days
    )

    # Support features (if available)
    if support_df is not None:
        support_features = support_df[
            (support_df['support_date'] >= observation_start) &
            (support_df['support_date'] < reference_date)
        ].groupby('customer_id').agg({
            'support_date': 'count',
            'issue_type': lambda x: x.mode()[0] if len(x) > 0 else 'none'
        })

        support_features.columns = ['support_tickets', 'most_common_issue']

        # Combine features
        features = trans_features.join(event_features, how='outer').join(
            support_features, how='left'
        )
    else:
        features = trans_features.join(event_features, how='outer')

    # Fill missing values
    features = features.fillna(0)

    # Calculate churn label
    # Customer churned if no activity after reference_date
    future_activity = events_df[
        (events_df['event_date'] >= reference_date) &
        (events_df['event_date'] < churn_end)
    ]['customer_id'].unique()

    features['churned'] = ~features.index.isin(future_activity)
    features['churned'] = features['churned'].astype(int)

    return features.reset_index()

# Example: Generate sample data for churn prediction
np.random.seed(42)

n_customers = 1000
reference_date = pd.Timestamp('2024-05-01')

# Generate transactions
transactions = []
for customer_id in range(n_customers):
    # Simulate different customer types
    will_churn = np.random.random() < 0.25  # 25% churn rate

    if will_churn:
        # Declining activity before churn
        n_trans = np.random.randint(2, 10)
        last_trans_days_ago = np.random.randint(20, 60)
    else:
        # Consistent activity
        n_trans = np.random.randint(5, 20)
        last_trans_days_ago = np.random.randint(1, 15)

    for i in range(n_trans):
        trans_date = reference_date - pd.Timedelta(
            days=last_trans_days_ago + i * np.random.randint(1, 10)
        )

        if trans_date >= reference_date - pd.Timedelta(days=90):
            transactions.append({
                'customer_id': customer_id,
                'transaction_date': trans_date,
                'revenue': np.random.gamma(2, 30)
            })

transactions_df = pd.DataFrame(transactions)

# Generate events
events = []
for customer_id in range(n_customers):
    will_churn = customer_id in transactions_df[
        transactions_df['transaction_date'] < reference_date - pd.Timedelta(days=20)
    ]['customer_id'].unique()

    if will_churn:
        n_events = np.random.randint(10, 50)
        last_event_days_ago = np.random.randint(15, 50)
    else:
        n_events = np.random.randint(30, 100)
        last_event_days_ago = np.random.randint(1, 10)

    for i in range(n_events):
        event_date = reference_date - pd.Timedelta(
            days=last_event_days_ago + i * np.random.random() * 2
        )

        if event_date >= reference_date - pd.Timedelta(days=90):
            events.append({
                'customer_id': customer_id,
                'event_date': event_date,
                'event_type': np.random.choice(['login', 'feature_use', 'view_content'])
            })

# Add future events for non-churners
for customer_id in range(n_customers):
    will_churn = customer_id in transactions_df[
        transactions_df['transaction_date'] < reference_date - pd.Timedelta(days=20)
    ]['customer_id'].unique()

    if not will_churn:
        # Add future activity
        for _ in range(np.random.randint(5, 15)):
            event_date = reference_date + pd.Timedelta(days=np.random.randint(1, 30))
            events.append({
                'customer_id': customer_id,
                'event_date': event_date,
                'event_type': np.random.choice(['login', 'feature_use', 'view_content'])
            })

events_df = pd.DataFrame(events)

# Engineer features
churn_data = engineer_churn_features(
    transactions_df,
    events_df,
    reference_date=reference_date,
    observation_period_days=90,
    churn_definition_days=30
)

print("Churn Data Sample:")
print(churn_data.head())
print(f"\nChurn Rate: {churn_data['churned'].mean():.2%}")
```

### 2. Logistic Regression for Churn

Build a simple, interpretable churn prediction model.

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, roc_curve
)
import matplotlib.pyplot as plt

def train_logistic_churn_model(
    df: pd.DataFrame,
    feature_cols: list,
    target_col: str = 'churned',
    test_size: float = 0.3
) -> tuple:
    """
    Train logistic regression model for churn prediction.

    Parameters:
    -----------
    df : DataFrame with features and target
    feature_cols : List of feature columns
    target_col : Target column name
    test_size : Proportion of data for testing

    Returns:
    --------
    tuple: (model, scaler, X_test, y_test, y_pred_proba)
    """
    # Prepare data
    X = df[feature_cols].values
    y = df[target_col].values

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train model
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train_scaled, y_train)

    # Predict
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

    # Evaluate
    print("Logistic Regression Churn Model Results:")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Retained', 'Churned']))

    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)

    auc_score = roc_auc_score(y_test, y_pred_proba)
    print(f"\nROC AUC Score: {auc_score:.3f}")

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'coefficient': model.coef_[0],
        'abs_coefficient': np.abs(model.coef_[0])
    }).sort_values('abs_coefficient', ascending=False)

    print("\nTop 10 Most Important Features:")
    print(feature_importance.head(10).to_string(index=False))

    return model, scaler, X_test_scaled, y_test, y_pred_proba, feature_importance

# Example: Train logistic regression model
feature_cols = [
    'transaction_count', 'days_since_last_transaction', 'total_revenue',
    'avg_transaction_value', 'transaction_frequency', 'transaction_trend',
    'total_events', 'days_active', 'unique_event_types', 'events_per_day'
]

lr_model, scaler, X_test, y_test, y_pred_proba, feature_imp = train_logistic_churn_model(
    churn_data,
    feature_cols=feature_cols
)
```

### 3. Random Forest for Churn

Build a more powerful ensemble model.

```python
from sklearn.ensemble import RandomForestClassifier

def train_random_forest_churn_model(
    df: pd.DataFrame,
    feature_cols: list,
    target_col: str = 'churned',
    test_size: float = 0.3,
    n_estimators: int = 100
) -> tuple:
    """
    Train random forest model for churn prediction.
    """
    # Prepare data
    X = df[feature_cols].values
    y = df[target_col].values

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )

    # Train model
    rf_model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=10,
        min_samples_split=20,
        min_samples_leaf=10,
        random_state=42,
        n_jobs=-1
    )

    rf_model.fit(X_train, y_train)

    # Predict
    y_pred = rf_model.predict(X_test)
    y_pred_proba = rf_model.predict_proba(X_test)[:, 1]

    # Evaluate
    print("Random Forest Churn Model Results:")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Retained', 'Churned']))

    auc_score = roc_auc_score(y_test, y_pred_proba)
    print(f"\nROC AUC Score: {auc_score:.3f}")

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\nTop 10 Most Important Features:")
    print(feature_importance.head(10).to_string(index=False))

    return rf_model, X_test, y_test, y_pred_proba, feature_importance

# Example: Train random forest model
rf_model, X_test_rf, y_test_rf, y_pred_proba_rf, rf_feature_imp = train_random_forest_churn_model(
    churn_data,
    feature_cols=feature_cols,
    n_estimators=100
)
```

### 4. ROC Curve and Model Comparison

Visualize and compare model performance.

```python
def plot_roc_curves(
    models_dict: dict,
    title: str = "ROC Curves - Churn Prediction"
) -> plt.Figure:
    """
    Plot ROC curves for multiple models.

    Parameters:
    -----------
    models_dict : dict with format {'Model Name': (y_test, y_pred_proba)}
    title : Plot title

    Returns:
    --------
    matplotlib Figure
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    for model_name, (y_true, y_proba) in models_dict.items():
        fpr, tpr, _ = roc_curve(y_true, y_proba)
        auc_score = roc_auc_score(y_true, y_proba)

        ax.plot(
            fpr, tpr,
            linewidth=2,
            label=f'{model_name} (AUC = {auc_score:.3f})'
        )

    # Plot diagonal
    ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random Classifier')

    ax.set_xlabel('False Positive Rate', fontsize=12)
    ax.set_ylabel('True Positive Rate', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

# Example: Compare models
models_comparison = {
    'Logistic Regression': (y_test, y_pred_proba),
    'Random Forest': (y_test_rf, y_pred_proba_rf)
}

fig = plot_roc_curves(models_comparison)
plt.savefig('churn_roc_curves.png', dpi=300, bbox_inches='tight')
print("\nROC curves saved to: churn_roc_curves.png")
```

### 5. Identify At-Risk Customers

Score all customers and identify those at highest risk.

```python
def identify_at_risk_customers(
    df: pd.DataFrame,
    model,
    scaler,
    feature_cols: list,
    risk_threshold: float = 0.7,
    top_n: int = 100
) -> pd.DataFrame:
    """
    Identify customers at high risk of churning.

    Parameters:
    -----------
    df : DataFrame with customer features
    model : Trained churn prediction model
    scaler : Fitted scaler (None for tree-based models)
    feature_cols : List of feature columns
    risk_threshold : Probability threshold for high risk
    top_n : Number of highest-risk customers to return

    Returns:
    --------
    DataFrame with churn risk scores
    """
    # Prepare features
    X = df[feature_cols].values

    # Scale if needed
    if scaler is not None:
        X = scaler.transform(X)

    # Predict churn probability
    churn_proba = model.predict_proba(X)[:, 1]

    # Create results dataframe
    results = df.copy()
    results['churn_probability'] = churn_proba
    results['risk_level'] = pd.cut(
        churn_proba,
        bins=[0, 0.3, 0.7, 1.0],
        labels=['Low Risk', 'Medium Risk', 'High Risk']
    )

    # Sort by risk
    results = results.sort_values('churn_probability', ascending=False)

    # High risk customers
    high_risk = results[results['churn_probability'] >= risk_threshold]

    print(f"\nAt-Risk Customer Summary:")
    print(f"Total Customers: {len(results):,}")
    print(f"High Risk (>={risk_threshold:.0%}): {len(high_risk):,} ({len(high_risk)/len(results):.1%})")
    print(f"\nRisk Level Distribution:")
    print(results['risk_level'].value_counts())

    # Top at-risk customers
    top_risk = results.head(top_n)

    return results, top_risk

# Example: Identify at-risk customers
all_customers_scored, top_at_risk = identify_at_risk_customers(
    churn_data,
    rf_model,
    scaler=None,  # Random forest doesn't need scaling
    feature_cols=feature_cols,
    risk_threshold=0.7,
    top_n=50
)

print("\nTop 10 At-Risk Customers:")
print(top_at_risk[['customer_id', 'churn_probability', 'days_since_last_transaction',
                    'transaction_count', 'total_events']].head(10).to_string(index=False))
```

### 6. Churn Driver Analysis

Understand what drives churn for different customer segments.

```python
def analyze_churn_drivers(
    df: pd.DataFrame,
    feature_importance: pd.DataFrame,
    churned_col: str = 'churned',
    top_n_features: int = 5
) -> pd.DataFrame:
    """
    Analyze differences between churned and retained customers.

    Parameters:
    -----------
    df : DataFrame with customer features and churn labels
    feature_importance : DataFrame with feature importance scores
    churned_col : Column indicating churn
    top_n_features : Number of top features to analyze

    Returns:
    --------
    DataFrame with driver analysis
    """
    top_features = feature_importance.head(top_n_features)['feature'].tolist()

    analysis = []

    for feature in top_features:
        churned_mean = df[df[churned_col] == 1][feature].mean()
        retained_mean = df[df[churned_col] == 0][feature].mean()

        difference = churned_mean - retained_mean
        pct_difference = (difference / retained_mean * 100) if retained_mean != 0 else 0

        analysis.append({
            'feature': feature,
            'churned_avg': churned_mean,
            'retained_avg': retained_mean,
            'difference': difference,
            'pct_difference': pct_difference
        })

    return pd.DataFrame(analysis)

# Example: Analyze churn drivers
churn_drivers = analyze_churn_drivers(
    churn_data,
    rf_feature_imp,
    top_n_features=10
)

print("\nChurn Driver Analysis:")
print(churn_drivers.round(2).to_string(index=False))

# Visualize drivers
fig, ax = plt.subplots(figsize=(12, 6))

features = churn_drivers['feature']
x = np.arange(len(features))
width = 0.35

ax.bar(x - width/2, churn_drivers['churned_avg'], width, label='Churned', alpha=0.8)
ax.bar(x + width/2, churn_drivers['retained_avg'], width, label='Retained', alpha=0.8)

ax.set_xlabel('Feature', fontsize=12)
ax.set_ylabel('Average Value', fontsize=12)
ax.set_title('Churn Drivers: Churned vs Retained Customers', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(features, rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('churn_drivers.png', dpi=300, bbox_inches='tight')
print("\nChurn drivers visualization saved to: churn_drivers.png")
```

### 7. Retention Strategy Targeting

Recommend retention strategies based on churn risk profiles.

```python
def recommend_retention_strategies(
    at_risk_df: pd.DataFrame,
    churn_drivers: pd.DataFrame
) -> pd.DataFrame:
    """
    Recommend retention strategies for at-risk customers.

    Parameters:
    -----------
    at_risk_df : DataFrame with at-risk customers
    churn_drivers : DataFrame with churn driver analysis

    Returns:
    --------
    DataFrame with retention recommendations
    """
    recommendations = []

    for _, customer in at_risk_df.head(100).iterrows():
        # Determine primary churn driver
        if customer['days_since_last_transaction'] > 20:
            strategy = 'Re-engagement Campaign'
            action = 'Send personalized email with special offer'
        elif customer['transaction_count'] < 5:
            strategy = 'Onboarding Improvement'
            action = 'Assign customer success manager'
        elif customer['total_events'] < customer['total_events'].quantile(0.25):
            strategy = 'Engagement Campaign'
            action = 'Feature education and training'
        elif customer['avg_transaction_value'] < 50:
            strategy = 'Value Demonstration'
            action = 'Show ROI and upsell opportunities'
        else:
            strategy = 'General Retention'
            action = 'Check-in call from account manager'

        recommendations.append({
            'customer_id': customer['customer_id'],
            'churn_probability': customer['churn_probability'],
            'recommended_strategy': strategy,
            'recommended_action': action,
            'priority': 'High' if customer['churn_probability'] > 0.8 else 'Medium'
        })

    return pd.DataFrame(recommendations)

# Example: Generate retention recommendations
retention_strategies = recommend_retention_strategies(
    all_customers_scored,
    churn_drivers
)

print("\nRetention Strategy Recommendations (Top 10):")
print(retention_strategies.head(10).to_string(index=False))

# Strategy distribution
print("\nStrategy Distribution:")
print(retention_strategies['recommended_strategy'].value_counts())
```

## Best Practices

### 1. Data and Features
- **Behavioral data is key**: Usage patterns predict churn better than demographics
- **Recency matters most**: Days since last activity is often the top predictor
- **Trends over snapshots**: Declining activity is more predictive than current level
- **Domain knowledge**: Include features specific to your business

### 2. Model Selection
- **Start simple**: Logistic regression for interpretability
- **Tree-based for performance**: Random Forest or XGBoost for accuracy
- **Calibrate probabilities**: Ensure predicted probabilities are realistic
- **Regular retraining**: Customer behavior changes over time

### 3. Defining Churn
- **Clear definition**: What constitutes churn in your business?
- **Appropriate window**: Match to your product usage cycle
- **Consider partial churn**: Reduced usage vs. complete abandonment
- **Contractual vs. non-contractual**: Different approaches needed

### 4. Common Pitfalls to Avoid
- **Class imbalance**: Churn is often rare; use appropriate techniques
- **Data leakage**: Don't include post-churn data in features
- **Overfitting**: Regularize models, use cross-validation
- **Ignoring timing**: Predict churn early enough to intervene

### 5. Actionability
- **Score all customers**: Not just those who churned
- **Segment interventions**: Different strategies for different churn drivers
- **Test retention campaigns**: A/B test retention offers
- **Measure impact**: Track if interventions reduce churn

## References

### Methodology
- Neslin, S. A., et al. (2006). "Defection Detection: Measuring and Understanding Churn"
- Verbeke, W., et al. (2012). "New insights into churn prediction in the telecommunication sector"
- Risselada, H., et al. (2010). "Staying Power of Churn Prediction Models"

### Tools and Libraries
- **sklearn**: Logistic regression, random forest, model evaluation
- **xgboost**: Gradient boosting for churn prediction
- **imbalanced-learn**: Handle class imbalance

### Industry Benchmarks
- **SaaS Monthly Churn**: 3-8% (depends on segment)
- **E-commerce Annual Churn**: 20-40%
- **Subscription Services**: 5-10% monthly
- **Mobile Apps (D30)**: 60-80% churn

### Additional Resources
- ProfitWell. "SaaS Churn Rate Benchmarks"
- Recurly. "Churn Rate Best Practices"
- CustomerGauge. "Reducing Churn with Predictive Analytics"

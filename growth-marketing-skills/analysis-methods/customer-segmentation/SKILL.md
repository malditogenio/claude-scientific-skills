---
name: customer-segmentation
description: Segment customers using RFM analysis, behavioral clustering, and demographic segmentation. Apply K-means, hierarchical clustering, and DBSCAN algorithms. Build customer personas, identify high-value segments, and create actionable marketing segments for targeted campaigns and personalization.
---

# Customer Segmentation

## Overview

Customer segmentation groups customers by shared characteristics to enable targeted marketing, personalized experiences, and optimized resource allocation. Effective segmentation reveals distinct customer groups with different needs, behaviors, and value.

**Key Capabilities:**
- RFM (Recency, Frequency, Monetary) analysis
- K-means and hierarchical clustering
- Behavioral segmentation
- Demographic and firmographic segmentation
- Customer lifetime value segmentation
- Persona development
- Segment profiling and visualization

## When to Use This Skill

Use this skill when:
- Creating targeted marketing campaigns
- Personalizing product recommendations
- Identifying high-value customer segments
- Developing customer personas
- Optimizing pricing strategies
- Allocating sales and support resources
- Understanding customer diversity

## Core Capabilities

### 1. RFM (Recency, Frequency, Monetary) Analysis

Classic segmentation based on purchase behavior.

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_rfm(
    df: pd.DataFrame,
    customer_col: str = 'customer_id',
    date_col: str = 'purchase_date',
    revenue_col: str = 'revenue',
    reference_date: pd.Timestamp = None
) -> pd.DataFrame:
    """
    Calculate RFM metrics for each customer.

    Parameters:
    -----------
    df : DataFrame with transaction data
    customer_col : Customer identifier column
    date_col : Transaction date column
    revenue_col : Revenue/value column
    reference_date : Date to calculate recency from (default: max date in data)

    Returns:
    --------
    DataFrame with RFM scores
    """
    # Ensure date is datetime
    df[date_col] = pd.to_datetime(df[date_col])

    if reference_date is None:
        reference_date = df[date_col].max()

    # Calculate RFM metrics
    rfm = df.groupby(customer_col).agg({
        date_col: lambda x: (reference_date - x.max()).days,  # Recency
        customer_col: 'count',  # Frequency
        revenue_col: 'sum'  # Monetary
    }).reset_index()

    rfm.columns = [customer_col, 'recency', 'frequency', 'monetary']

    return rfm

def assign_rfm_scores(
    rfm_df: pd.DataFrame,
    n_bins: int = 5
) -> pd.DataFrame:
    """
    Assign RFM scores (1-5, where 5 is best).

    Parameters:
    -----------
    rfm_df : DataFrame from calculate_rfm
    n_bins : Number of bins for scoring (default: 5)

    Returns:
    --------
    DataFrame with RFM scores and segments
    """
    rfm_scored = rfm_df.copy()

    # Create quintiles (5 bins)
    # For Recency: lower is better, so reverse
    rfm_scored['r_score'] = pd.qcut(
        rfm_scored['recency'],
        q=n_bins,
        labels=range(n_bins, 0, -1),
        duplicates='drop'
    )

    # For Frequency: higher is better
    rfm_scored['f_score'] = pd.qcut(
        rfm_scored['frequency'],
        q=n_bins,
        labels=range(1, n_bins + 1),
        duplicates='drop'
    )

    # For Monetary: higher is better
    rfm_scored['m_score'] = pd.qcut(
        rfm_scored['monetary'],
        q=n_bins,
        labels=range(1, n_bins + 1),
        duplicates='drop'
    )

    # Convert to int
    rfm_scored['r_score'] = rfm_scored['r_score'].astype(int)
    rfm_scored['f_score'] = rfm_scored['f_score'].astype(int)
    rfm_scored['m_score'] = rfm_scored['m_score'].astype(int)

    # Combined RFM score
    rfm_scored['rfm_score'] = (
        rfm_scored['r_score'].astype(str) +
        rfm_scored['f_score'].astype(str) +
        rfm_scored['m_score'].astype(str)
    )

    # Overall score (simple average)
    rfm_scored['rfm_total'] = (
        rfm_scored['r_score'] +
        rfm_scored['f_score'] +
        rfm_scored['m_score']
    ) / 3

    return rfm_scored

def create_rfm_segments(rfm_scored: pd.DataFrame) -> pd.DataFrame:
    """
    Create named segments from RFM scores.

    Segment definitions:
    - Champions: R=5, F=5, M=5
    - Loyal Customers: R=4-5, F=4-5, M=3-5
    - Potential Loyalists: R=4-5, F=2-3, M=2-3
    - New Customers: R=5, F=1, M=1-2
    - At Risk: R=2-3, F=3-5, M=3-5
    - Can't Lose: R=1-2, F=4-5, M=4-5
    - Hibernating: R=1-2, F=1-2, M=1-2
    - Others
    """
    rfm_segmented = rfm_scored.copy()

    def assign_segment(row):
        r, f, m = row['r_score'], row['f_score'], row['m_score']

        if r >= 5 and f >= 5 and m >= 5:
            return 'Champions'
        elif r >= 4 and f >= 4 and m >= 3:
            return 'Loyal Customers'
        elif r >= 4 and f >= 2 and m >= 2 and f <= 3:
            return 'Potential Loyalists'
        elif r >= 5 and f == 1:
            return 'New Customers'
        elif r <= 3 and r >= 2 and f >= 3 and m >= 3:
            return 'At Risk'
        elif r <= 2 and f >= 4 and m >= 4:
            return "Can't Lose Them"
        elif r <= 2 and f <= 2:
            return 'Hibernating'
        else:
            return 'Others'

    rfm_segmented['segment'] = rfm_segmented.apply(assign_segment, axis=1)

    return rfm_segmented

# Example: Generate sample transaction data
np.random.seed(42)

# Generate transactions
n_customers = 1000
transactions = []

for customer_id in range(n_customers):
    # Different customer patterns
    customer_type = np.random.choice(['champion', 'at_risk', 'new', 'hibernating'])

    if customer_type == 'champion':
        # Recent, frequent, high-value
        n_transactions = np.random.randint(10, 30)
        days_ago = np.random.randint(1, 30)
        avg_value = 150
    elif customer_type == 'at_risk':
        # Not recent, but was frequent
        n_transactions = np.random.randint(8, 15)
        days_ago = np.random.randint(60, 150)
        avg_value = 100
    elif customer_type == 'new':
        # Very recent, few transactions
        n_transactions = np.random.randint(1, 3)
        days_ago = np.random.randint(1, 15)
        avg_value = 80
    else:  # hibernating
        # Old, few transactions
        n_transactions = np.random.randint(1, 5)
        days_ago = np.random.randint(150, 365)
        avg_value = 60

    last_purchase = pd.Timestamp('2024-06-01') - pd.Timedelta(days=days_ago)

    for _ in range(n_transactions):
        purchase_date = last_purchase - pd.Timedelta(
            days=np.random.randint(0, min(days_ago, 90))
        )
        revenue = np.random.gamma(2, avg_value / 2)

        transactions.append({
            'customer_id': customer_id,
            'purchase_date': purchase_date,
            'revenue': revenue
        })

transactions_df = pd.DataFrame(transactions)

# Calculate RFM
rfm = calculate_rfm(
    transactions_df,
    reference_date=pd.Timestamp('2024-06-01')
)

# Score RFM
rfm_scored = assign_rfm_scores(rfm)

# Create segments
rfm_segmented = create_rfm_segments(rfm_scored)

print("RFM Segmentation Summary:")
print(rfm_segmented['segment'].value_counts().sort_values(ascending=False))

print("\nSegment Profiles:")
segment_profiles = rfm_segmented.groupby('segment').agg({
    'customer_id': 'count',
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': 'mean'
}).round(2)
segment_profiles.columns = ['customers', 'avg_recency_days', 'avg_frequency', 'avg_revenue']
print(segment_profiles.sort_values('customers', ascending=False))
```

### 2. K-Means Clustering

Use machine learning to discover customer segments.

```python
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns

def perform_kmeans_segmentation(
    df: pd.DataFrame,
    feature_cols: list,
    n_clusters: int = 4,
    customer_col: str = 'customer_id'
) -> tuple:
    """
    Perform K-means clustering on customer features.

    Parameters:
    -----------
    df : DataFrame with customer features
    feature_cols : List of columns to use for clustering
    n_clusters : Number of clusters to create
    customer_col : Customer identifier column

    Returns:
    --------
    tuple: (DataFrame with cluster assignments, KMeans model, StandardScaler)
    """
    # Prepare features
    X = df[feature_cols].values

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Fit K-means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    # Add clusters to dataframe
    df_clustered = df.copy()
    df_clustered['cluster'] = clusters

    # Calculate silhouette score
    silhouette_avg = silhouette_score(X_scaled, clusters)
    print(f"\nSilhouette Score: {silhouette_avg:.3f}")

    return df_clustered, kmeans, scaler

def find_optimal_clusters(
    df: pd.DataFrame,
    feature_cols: list,
    max_clusters: int = 10
) -> plt.Figure:
    """
    Use elbow method and silhouette analysis to find optimal number of clusters.

    Parameters:
    -----------
    df : DataFrame with customer features
    feature_cols : List of columns to use for clustering
    max_clusters : Maximum number of clusters to test

    Returns:
    --------
    matplotlib Figure with elbow and silhouette plots
    """
    X = df[feature_cols].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    inertias = []
    silhouette_scores = []
    K_range = range(2, max_clusters + 1)

    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)

        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))

    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Elbow plot
    ax1.plot(K_range, inertias, marker='o', linewidth=2, markersize=8)
    ax1.set_xlabel('Number of Clusters', fontsize=12)
    ax1.set_ylabel('Inertia (Within-Cluster Sum of Squares)', fontsize=12)
    ax1.set_title('Elbow Method', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # Silhouette plot
    ax2.plot(K_range, silhouette_scores, marker='o', linewidth=2, markersize=8, color='green')
    ax2.set_xlabel('Number of Clusters', fontsize=12)
    ax2.set_ylabel('Silhouette Score', fontsize=12)
    ax2.set_title('Silhouette Analysis', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

# Example: Create customer feature matrix from RFM
customer_features = rfm_segmented[[
    'customer_id', 'recency', 'frequency', 'monetary'
]].copy()

# Find optimal number of clusters
fig = find_optimal_clusters(
    customer_features,
    feature_cols=['recency', 'frequency', 'monetary'],
    max_clusters=10
)
plt.savefig('cluster_optimization.png', dpi=300, bbox_inches='tight')
print("Cluster optimization plot saved to: cluster_optimization.png")

# Perform K-means with optimal k
customers_clustered, kmeans_model, scaler = perform_kmeans_segmentation(
    customer_features,
    feature_cols=['recency', 'frequency', 'monetary'],
    n_clusters=4
)

print("\nCluster Sizes:")
print(customers_clustered['cluster'].value_counts().sort_index())

print("\nCluster Profiles:")
cluster_profiles = customers_clustered.groupby('cluster')[
    ['recency', 'frequency', 'monetary']
].mean().round(2)
print(cluster_profiles)
```

### 3. Hierarchical Clustering

Build a dendrogram to visualize hierarchical customer relationships.

```python
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.preprocessing import StandardScaler

def hierarchical_segmentation(
    df: pd.DataFrame,
    feature_cols: list,
    n_clusters: int = 4,
    method: str = 'ward'
) -> pd.DataFrame:
    """
    Perform hierarchical clustering.

    Parameters:
    -----------
    df : DataFrame with customer features
    feature_cols : List of columns to use for clustering
    n_clusters : Number of clusters to create
    method : Linkage method ('ward', 'complete', 'average', 'single')

    Returns:
    --------
    DataFrame with cluster assignments
    """
    # Prepare and scale features
    X = df[feature_cols].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Perform hierarchical clustering
    linkage_matrix = linkage(X_scaled, method=method)

    # Assign clusters
    clusters = fcluster(linkage_matrix, n_clusters, criterion='maxclust')

    df_clustered = df.copy()
    df_clustered['cluster'] = clusters - 1  # Make 0-indexed

    return df_clustered, linkage_matrix

def plot_dendrogram(
    linkage_matrix,
    max_display: int = 30,
    title: str = "Hierarchical Clustering Dendrogram"
) -> plt.Figure:
    """
    Plot dendrogram for hierarchical clustering.
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    dendrogram(
        linkage_matrix,
        truncate_mode='lastp',
        p=max_display,
        ax=ax
    )

    ax.set_xlabel('Cluster Size', fontsize=12)
    ax.set_ylabel('Distance', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')

    plt.tight_layout()
    return fig

# Example: Hierarchical clustering
hierarchical_result, linkage_mat = hierarchical_segmentation(
    customer_features,
    feature_cols=['recency', 'frequency', 'monetary'],
    n_clusters=4,
    method='ward'
)

# Plot dendrogram
fig = plot_dendrogram(linkage_mat)
plt.savefig('dendrogram.png', dpi=300, bbox_inches='tight')
print("\nDendrogram saved to: dendrogram.png")
```

### 4. Behavioral Segmentation

Segment based on user behavior patterns.

```python
def create_behavioral_segments(
    events_df: pd.DataFrame,
    user_col: str = 'user_id',
    event_col: str = 'event_type',
    date_col: str = 'event_date'
) -> pd.DataFrame:
    """
    Create segments based on user behavior patterns.

    Parameters:
    -----------
    events_df : DataFrame with user events
    user_col : User identifier column
    event_col : Event type column
    date_col : Event date column

    Returns:
    --------
    DataFrame with behavioral features
    """
    # Calculate behavioral metrics
    user_behavior = events_df.groupby(user_col).agg({
        event_col: 'count',  # Total events
        date_col: ['min', 'max', 'nunique']  # First, last, days active
    }).reset_index()

    user_behavior.columns = [
        user_col, 'total_events', 'first_event', 'last_event', 'days_active'
    ]

    # Calculate event type distribution
    event_distribution = events_df.groupby([user_col, event_col]).size().unstack(
        fill_value=0
    )

    # Combine
    user_behavior = user_behavior.merge(
        event_distribution,
        left_on=user_col,
        right_index=True,
        how='left'
    )

    # Calculate engagement score
    user_behavior['engagement_score'] = (
        user_behavior['total_events'] *
        user_behavior['days_active']
    )

    # Calculate feature usage diversity (entropy)
    event_cols = event_distribution.columns
    user_behavior['feature_diversity'] = 0

    for col in event_cols:
        if col in user_behavior.columns:
            prop = user_behavior[col] / user_behavior['total_events']
            # Entropy calculation (avoiding log(0))
            user_behavior['feature_diversity'] -= prop * np.log(prop + 1e-10)

    return user_behavior

# Example: Generate behavioral data
np.random.seed(42)
event_types = ['page_view', 'feature_use', 'purchase', 'support_contact', 'settings_change']

events = []
for user_id in range(500):
    # Different user types
    user_type = np.random.choice(['power_user', 'casual', 'explorer'])

    if user_type == 'power_user':
        n_events = np.random.randint(50, 200)
        event_probs = [0.3, 0.4, 0.2, 0.05, 0.05]
    elif user_type == 'casual':
        n_events = np.random.randint(5, 30)
        event_probs = [0.7, 0.1, 0.15, 0.03, 0.02]
    else:  # explorer
        n_events = np.random.randint(20, 60)
        event_probs = [0.25, 0.25, 0.15, 0.15, 0.2]

    start_date = pd.Timestamp('2024-01-01')

    for _ in range(n_events):
        event_date = start_date + pd.Timedelta(days=np.random.randint(0, 180))
        event_type = np.random.choice(event_types, p=event_probs)

        events.append({
            'user_id': user_id,
            'event_type': event_type,
            'event_date': event_date
        })

events_df = pd.DataFrame(events)

# Create behavioral segments
behavioral_features = create_behavioral_segments(events_df)

print("\nBehavioral Features Sample:")
print(behavioral_features.head())

# Cluster on behavioral features
behavior_cols = ['total_events', 'days_active', 'engagement_score', 'feature_diversity']
behavioral_segments, _, _ = perform_kmeans_segmentation(
    behavioral_features,
    feature_cols=behavior_cols,
    n_clusters=3
)

print("\nBehavioral Segment Profiles:")
segment_profiles = behavioral_segments.groupby('cluster')[behavior_cols].mean().round(2)
print(segment_profiles)
```

### 5. Segment Visualization

Visualize customer segments in 2D/3D space.

```python
from sklearn.decomposition import PCA

def visualize_segments(
    df: pd.DataFrame,
    feature_cols: list,
    cluster_col: str = 'cluster',
    method: str = 'pca',
    title: str = "Customer Segments"
) -> plt.Figure:
    """
    Visualize customer segments using dimensionality reduction.

    Parameters:
    -----------
    df : DataFrame with features and cluster assignments
    feature_cols : List of feature columns
    cluster_col : Column with cluster labels
    method : Dimensionality reduction method ('pca' or 'tsne')
    title : Plot title

    Returns:
    --------
    matplotlib Figure
    """
    # Prepare features
    X = df[feature_cols].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Reduce to 2D
    if method == 'pca':
        from sklearn.decomposition import PCA
        reducer = PCA(n_components=2, random_state=42)
        X_2d = reducer.fit_transform(X_scaled)
        x_label = f'PC1 ({reducer.explained_variance_ratio_[0]:.1%})'
        y_label = f'PC2 ({reducer.explained_variance_ratio_[1]:.1%})'
    else:  # t-SNE
        from sklearn.manifold import TSNE
        reducer = TSNE(n_components=2, random_state=42)
        X_2d = reducer.fit_transform(X_scaled)
        x_label = 't-SNE 1'
        y_label = 't-SNE 2'

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot each cluster
    clusters = df[cluster_col].unique()
    colors = plt.cm.tab10(np.linspace(0, 1, len(clusters)))

    for i, cluster in enumerate(sorted(clusters)):
        mask = df[cluster_col] == cluster
        ax.scatter(
            X_2d[mask, 0],
            X_2d[mask, 1],
            c=[colors[i]],
            label=f'Segment {cluster}',
            alpha=0.6,
            s=50
        )

    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

# Example: Visualize RFM segments
fig = visualize_segments(
    customers_clustered,
    feature_cols=['recency', 'frequency', 'monetary'],
    cluster_col='cluster',
    method='pca',
    title='Customer Segments (RFM Features)'
)
plt.savefig('segment_visualization.png', dpi=300, bbox_inches='tight')
print("\nSegment visualization saved to: segment_visualization.png")
```

### 6. Segment Profiling and Comparison

Create detailed profiles for each segment.

```python
def profile_segments(
    df: pd.DataFrame,
    cluster_col: str = 'cluster',
    metric_cols: list = None
) -> pd.DataFrame:
    """
    Create detailed profiles for each segment.

    Parameters:
    -----------
    df : DataFrame with cluster assignments and metrics
    cluster_col : Column with cluster labels
    metric_cols : List of columns to profile

    Returns:
    --------
    DataFrame with segment profiles
    """
    profiles = []

    for cluster in sorted(df[cluster_col].unique()):
        cluster_data = df[df[cluster_col] == cluster]

        profile = {
            'segment': cluster,
            'size': len(cluster_data),
            'pct_of_total': len(cluster_data) / len(df) * 100
        }

        # Calculate statistics for each metric
        for col in metric_cols:
            profile[f'{col}_mean'] = cluster_data[col].mean()
            profile[f'{col}_median'] = cluster_data[col].median()
            profile[f'{col}_std'] = cluster_data[col].std()

        profiles.append(profile)

    return pd.DataFrame(profiles)

# Example: Profile segments
segment_profiles = profile_segments(
    customers_clustered,
    cluster_col='cluster',
    metric_cols=['recency', 'frequency', 'monetary']
)

print("\nDetailed Segment Profiles:")
print(segment_profiles.to_string(index=False))

# Name segments based on characteristics
def name_segments(profiles_df: pd.DataFrame) -> dict:
    """
    Assign descriptive names to segments based on their characteristics.
    """
    segment_names = {}

    for _, row in profiles_df.iterrows():
        segment = row['segment']

        # High value, frequent, recent
        if (row['monetary_mean'] > profiles_df['monetary_mean'].quantile(0.75) and
            row['frequency_mean'] > profiles_df['frequency_mean'].quantile(0.75) and
            row['recency_mean'] < profiles_df['recency_mean'].quantile(0.25)):
            segment_names[segment] = 'VIP Champions'

        # High value but not recent
        elif (row['monetary_mean'] > profiles_df['monetary_mean'].quantile(0.75) and
              row['recency_mean'] > profiles_df['recency_mean'].quantile(0.75)):
            segment_names[segment] = 'At Risk High Value'

        # Recent but low value
        elif (row['recency_mean'] < profiles_df['recency_mean'].quantile(0.25) and
              row['monetary_mean'] < profiles_df['monetary_mean'].quantile(0.25)):
            segment_names[segment] = 'New/Low Value'

        # Default
        else:
            segment_names[segment] = f'Segment {segment}'

    return segment_names

segment_names = name_segments(segment_profiles)
print("\nSegment Names:")
for segment, name in segment_names.items():
    print(f"  Segment {segment}: {name}")
```

## Best Practices

### 1. Feature Selection
- **Choose relevant features**: Select features that predict behavior
- **Scale features**: Normalize to prevent dominance by large-scale features
- **Avoid redundancy**: Remove highly correlated features
- **Include temporal**: Recency matters as much as frequency

### 2. Number of Segments
- **Not too many**: 3-7 segments are typically actionable
- **Not too few**: Must capture meaningful differences
- **Use validation**: Silhouette score, elbow method, business judgment
- **Consider actionability**: Can you target each segment differently?

### 3. Validation
- **Business validation**: Do segments make sense?
- **Stability**: Are segments stable over time?
- **Actionability**: Can you act on the differences?
- **Predictive power**: Do segments predict future behavior?

### 4. Common Pitfalls to Avoid
- **Over-segmentation**: Too many segments to action
- **Trivial segments**: Segments without meaningful differences
- **Ignoring size**: Some segments may be too small
- **Static segments**: Must update as behavior changes

### 5. Advanced Techniques
- **Ensemble clustering**: Combine multiple methods
- **Temporal segmentation**: How segments evolve over time
- **Predictive segmentation**: Forward-looking behavior
- **Multi-dimensional**: Combine RFM with demographics and behavior

## References

### Methodology
- Arthur, D., & Vassilvitskii, S. (2007). "k-means++: The advantages of careful seeding"
- Hughes, A. M. (1994). "Strategic Database Marketing"
- Wedel, M., & Kamakura, W. A. (2000). "Market Segmentation: Conceptual and Methodological Foundations"

### Tools and Libraries
- **sklearn**: K-means, hierarchical clustering, PCA
- **scipy**: Hierarchical clustering, dendrograms
- **pandas**: Data manipulation

### Industry Standards
- **B2C**: RFM, behavioral, demographic
- **B2B**: Firmographic, usage-based, revenue-based
- **E-commerce**: Product affinity, browsing behavior
- **SaaS**: Feature usage, engagement level

### Additional Resources
- Optimove. "The Complete Guide to Customer Segmentation"
- CleverTap. "Behavioral Segmentation Guide"
- Kissmetrics. "Customer Segmentation Best Practices"

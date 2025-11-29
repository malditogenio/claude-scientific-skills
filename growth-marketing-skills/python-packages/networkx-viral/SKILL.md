---
name: networkx-viral
description: "Viral growth analysis and network effects. Referral mapping, influencer identification, customer network analysis, viral coefficient calculation, network centrality metrics."
---

# NetworkX for Viral Growth Analysis

## Overview

NetworkX is a powerful library for analyzing social networks and viral growth patterns. This skill covers using NetworkX for referral program analysis, identifying key influencers, measuring network effects, calculating viral coefficients, and visualizing customer acquisition networks.

## When to Use This Skill

- Analyzing referral program performance and viral loops
- Identifying power users and influencers in your customer base
- Mapping customer acquisition networks
- Calculating viral coefficient and K-factor
- Understanding network effects in product growth
- Detecting communities and clusters in your user base
- Measuring social influence and information spread

## Core Capabilities

### 1. Referral Network Analysis

```python
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Create referral network from customer data
df = pd.read_csv('referrals.csv')  # columns: referrer_id, referred_id, signup_date, converted

# Build directed graph
G = nx.DiGraph()

for _, row in df.iterrows():
    G.add_edge(row['referrer_id'], row['referred_id'],
               date=row['signup_date'],
               converted=row['converted'])

# Basic network statistics
print(f"Total users in network: {G.number_of_nodes()}")
print(f"Total referrals: {G.number_of_edges()}")
print(f"Network density: {nx.density(G):.4f}")

# Find top referrers
out_degrees = dict(G.out_degree())
top_referrers = sorted(out_degrees.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Referrers:")
for user_id, referrals in top_referrers:
    print(f"  User {user_id}: {referrals} referrals")
```

### 2. Viral Coefficient Calculation

```python
import networkx as nx
import numpy as np

def calculate_viral_coefficient(G, conversion_data):
    """
    Calculate K-factor (viral coefficient) for the referral network
    K > 1 means exponential growth, K < 1 means growth will plateau
    """
    # Get users who made referrals
    referrers = [node for node in G.nodes() if G.out_degree(node) > 0]

    # Calculate average invites sent per user
    total_invites = G.number_of_edges()
    avg_invites = total_invites / len(referrers) if referrers else 0

    # Calculate conversion rate
    converted_edges = sum(1 for _, _, data in G.edges(data=True) if data.get('converted', False))
    conversion_rate = converted_edges / total_invites if total_invites > 0 else 0

    # K-factor = (avg invites per user) × (conversion rate)
    k_factor = avg_invites * conversion_rate

    return {
        'k_factor': k_factor,
        'avg_invites_per_user': avg_invites,
        'conversion_rate': conversion_rate,
        'total_referrers': len(referrers),
        'total_conversions': converted_edges
    }

# Calculate viral metrics
metrics = calculate_viral_coefficient(G, df)
print("\nViral Growth Metrics:")
print(f"  K-Factor: {metrics['k_factor']:.3f}")
print(f"  Avg Invites/User: {metrics['avg_invites_per_user']:.2f}")
print(f"  Conversion Rate: {metrics['conversion_rate']:.2%}")

if metrics['k_factor'] > 1:
    print("  Status: VIRAL GROWTH! 🚀")
else:
    print(f"  Status: Need {1/metrics['conversion_rate']:.1f} invites/user for viral growth")
```

### 3. Influencer Identification

```python
import networkx as nx
import pandas as pd

def identify_influencers(G, top_n=20):
    """
    Identify key influencers using multiple centrality metrics
    """
    # PageRank - measures overall influence
    pagerank = nx.pagerank(G)

    # Betweenness centrality - measures bridge nodes
    betweenness = nx.betweenness_centrality(G)

    # Out-degree centrality - direct referrals
    out_degree = dict(G.out_degree())

    # Combine metrics
    influencers = pd.DataFrame({
        'user_id': list(G.nodes()),
        'pagerank': [pagerank.get(node, 0) for node in G.nodes()],
        'betweenness': [betweenness.get(node, 0) for node in G.nodes()],
        'referrals': [out_degree.get(node, 0) for node in G.nodes()]
    })

    # Calculate composite influence score
    influencers['influence_score'] = (
        influencers['pagerank'] * 0.4 +
        influencers['betweenness'] * 0.3 +
        (influencers['referrals'] / influencers['referrals'].max()) * 0.3
    )

    return influencers.nlargest(top_n, 'influence_score')

# Find influencers
influencers = identify_influencers(G, top_n=20)
print("\nTop 20 Influencers:")
print(influencers.to_string(index=False))
```

### 4. Referral Chain Analysis

```python
import networkx as nx

def analyze_referral_chains(G, source_node):
    """
    Analyze the complete referral chain starting from a source user
    """
    # Find all descendants (people referred by this user and their referrals)
    descendants = nx.descendants(G, source_node)

    # Create subgraph of this referral tree
    subgraph = G.subgraph([source_node] + list(descendants))

    # Calculate tree metrics
    total_network = len(descendants)
    max_depth = 0

    if descendants:
        # Find longest path from source
        for node in descendants:
            try:
                depth = nx.shortest_path_length(G, source_node, node)
                max_depth = max(max_depth, depth)
            except nx.NetworkXNoPath:
                pass

    # Calculate network value
    direct_referrals = G.out_degree(source_node)

    return {
        'source_user': source_node,
        'total_network_size': total_network,
        'direct_referrals': direct_referrals,
        'max_chain_depth': max_depth,
        'network_generations': max_depth,
        'subgraph': subgraph
    }

# Analyze top referrer's network
top_user = top_referrers[0][0]
chain = analyze_referral_chains(G, top_user)

print(f"\nReferral Chain Analysis for User {top_user}:")
print(f"  Total Network Size: {chain['total_network_size']} users")
print(f"  Direct Referrals: {chain['direct_referrals']}")
print(f"  Max Chain Depth: {chain['max_chain_depth']} generations")
```

### 5. Community Detection

```python
import networkx as nx
from networkx.algorithms import community

def detect_communities(G):
    """
    Detect communities/clusters in the referral network
    """
    # Convert to undirected for community detection
    G_undirected = G.to_undirected()

    # Use Louvain method for community detection
    communities = community.greedy_modularity_communities(G_undirected)

    # Analyze communities
    community_stats = []
    for i, comm in enumerate(communities):
        subgraph = G.subgraph(comm)
        community_stats.append({
            'community_id': i,
            'size': len(comm),
            'edges': subgraph.number_of_edges(),
            'density': nx.density(subgraph),
            'avg_degree': sum(dict(subgraph.degree()).values()) / len(comm)
        })

    return pd.DataFrame(community_stats).sort_values('size', ascending=False)

# Detect and analyze communities
communities_df = detect_communities(G)
print("\nCustomer Communities:")
print(communities_df.to_string(index=False))
```

### 6. Network Visualization

```python
import networkx as nx
import matplotlib.pyplot as plt

def visualize_referral_network(G, top_n=50, output_file='referral_network.png'):
    """
    Visualize the referral network focusing on most active users
    """
    # Get top nodes by degree
    degrees = dict(G.degree())
    top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_node_ids = [node for node, _ in top_nodes]

    # Create subgraph
    subgraph = G.subgraph(top_node_ids)

    # Calculate layout
    pos = nx.spring_layout(subgraph, k=0.5, iterations=50)

    # Node sizes based on out-degree
    node_sizes = [G.out_degree(node) * 100 + 100 for node in subgraph.nodes()]

    # Node colors based on PageRank
    pagerank = nx.pagerank(subgraph)
    node_colors = [pagerank[node] for node in subgraph.nodes()]

    # Draw network
    plt.figure(figsize=(16, 12))
    nx.draw_networkx_nodes(subgraph, pos,
                          node_size=node_sizes,
                          node_color=node_colors,
                          cmap='YlOrRd',
                          alpha=0.7)
    nx.draw_networkx_edges(subgraph, pos,
                          alpha=0.2,
                          arrows=True,
                          arrowsize=10)

    # Add labels for top 10 nodes
    top_10_nodes = top_node_ids[:10]
    labels = {node: f"User {node}" for node in top_10_nodes}
    nx.draw_networkx_labels(subgraph, pos, labels, font_size=8)

    plt.title(f"Referral Network - Top {top_n} Most Connected Users", fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Network visualization saved to {output_file}")

visualize_referral_network(G, top_n=50)
```

## Installation

```bash
uv pip install networkx pandas matplotlib numpy
```

## Quick Start

```python
import networkx as nx
import pandas as pd

# Load referral data
df = pd.read_csv('referrals.csv')

# Create network
G = nx.DiGraph()
for _, row in df.iterrows():
    G.add_edge(row['referrer_id'], row['referred_id'])

# Quick analysis
print(f"Users: {G.number_of_nodes()}")
print(f"Referrals: {G.number_of_edges()}")

# Top referrers
top_5 = sorted(G.out_degree(), key=lambda x: x[1], reverse=True)[:5]
print("\nTop 5 Referrers:")
for user, count in top_5:
    print(f"  User {user}: {count} referrals")
```

## Best Practices

1. **Track conversions** - Always include conversion status in edge attributes
2. **Time-based analysis** - Include timestamps to analyze viral growth over time
3. **Multi-generation tracking** - Track referral depth to understand compounding effects
4. **A/B test incentives** - Compare K-factors across different referral reward structures
5. **Monitor churn** - Include user lifecycle status in node attributes
6. **Detect fraud** - Use graph patterns to identify suspicious referral behavior

## References

- [NetworkX Documentation](https://networkx.org/documentation/stable/)
- [Graph Theory Basics](https://networkx.org/documentation/stable/tutorial.html)
- [Viral Growth Metrics](https://www.reforge.com/blog/viral-growth)

---
skill_name: databricks
display_name: Databricks
description: Unified analytics platform for marketing data lakehouse, ML-powered attribution, and real-time personalization
category: cdp-data
tags: [data-lakehouse, analytics, ml, spark, marketing-analytics]
complexity: advanced
dependencies: [databricks-sql-connector, pyspark, mlflow]
---

# Databricks

## Overview

Databricks is a unified data analytics platform built on Apache Spark that combines data warehousing, data engineering, and machine learning capabilities. For marketing teams, Databricks enables advanced analytics, real-time personalization, and ML-powered customer insights at massive scale.

Databricks excels at:
- **Lakehouse Architecture**: Combine data lake flexibility with warehouse performance
- **Real-Time Analytics**: Process streaming events for instant personalization
- **ML at Scale**: Build and deploy ML models for attribution, LTV, and propensity
- **Unified Customer Data**: Process billions of events from all marketing channels
- **Collaborative Analytics**: Notebooks for data scientists and marketing analysts
- **Delta Lake**: ACID transactions and time travel for marketing data

## When to Use

Use Databricks when you need to:
- **Advanced ML Models**: Build sophisticated attribution, propensity, and LTV models
- **Real-Time Personalization**: Process streaming events for immediate activation
- **Massive Scale Analytics**: Handle petabytes of marketing data
- **Unified Data Platform**: Combine batch and streaming analytics
- **Collaborative Data Science**: Enable data teams to work together on marketing insights
- **Feature Engineering**: Build complex features for ML models
- **Multi-Cloud Strategy**: Deploy on AWS, Azure, or GCP

## Core Capabilities

### 1. Marketing Data Lakehouse Setup

**Create Delta Tables for Marketing Data**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Initialize Spark session
spark = SparkSession.builder \
    .appName("MarketingDataLakehouse") \
    .getOrCreate()

# Create database for marketing data
spark.sql("CREATE DATABASE IF NOT EXISTS marketing_data")
spark.sql("USE marketing_data")

# Create Delta table for events (CDP data)
events_schema = StructType([
    StructField("event_id", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("anonymous_id", StringType(), True),
    StructField("event_name", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("properties", MapType(StringType(), StringType()), True),
    StructField("utm_source", StringType(), True),
    StructField("utm_medium", StringType(), True),
    StructField("utm_campaign", StringType(), True),
    StructField("revenue", DoubleType(), True)
])

# Read from S3/ADLS/GCS and write to Delta
events_df = spark.read \
    .format("json") \
    .schema(events_schema) \
    .load("s3://your-bucket/segment-events/")

events_df.write \
    .format("delta") \
    .mode("overwrite") \
    .partitionBy("date") \
    .option("overwriteSchema", "true") \
    .saveAsTable("marketing_data.events")

# Create Delta table for user profiles
spark.sql("""
CREATE TABLE IF NOT EXISTS marketing_data.user_profiles (
    user_id STRING,
    email STRING,
    name STRING,
    traits MAP<STRING, STRING>,
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
USING DELTA
PARTITIONED BY (DATE(created_at))
""")

# Create Delta table for ad platform data
spark.sql("""
CREATE TABLE IF NOT EXISTS marketing_data.ad_performance (
    date DATE,
    platform STRING,
    campaign_id STRING,
    campaign_name STRING,
    ad_id STRING,
    ad_name STRING,
    impressions BIGINT,
    clicks BIGINT,
    spend DOUBLE,
    conversions BIGINT,
    conversion_value DOUBLE,
    loaded_at TIMESTAMP
)
USING DELTA
PARTITIONED BY (date, platform)
""")
```

**Streaming Event Ingestion**

```python
from pyspark.sql.functions import from_json, col, current_timestamp

# Read streaming events from Kafka/Kinesis/Event Hubs
streaming_events = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "your-kafka-servers") \
    .option("subscribe", "marketing-events") \
    .load()

# Parse JSON events
event_schema = StructType([
    StructField("user_id", StringType()),
    StructField("event_name", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("properties", MapType(StringType(), StringType())),
    StructField("utm_source", StringType()),
    StructField("utm_campaign", StringType())
])

parsed_events = streaming_events \
    .select(from_json(col("value").cast("string"), event_schema).alias("data")) \
    .select("data.*") \
    .withColumn("processed_at", current_timestamp())

# Write to Delta table with streaming
query = parsed_events.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/checkpoints/marketing-events") \
    .table("marketing_data.events_stream")

query.awaitTermination()
```

### 2. Customer 360 with Delta Lake

**Build Unified Customer Profiles**

```python
# Customer 360 using Delta Lake
from delta.tables import DeltaTable
from pyspark.sql.window import Window

def build_customer_360():
    """Build comprehensive customer 360 view"""

    # User profile base
    user_profiles = spark.table("marketing_data.user_profiles")

    # Behavior metrics (last 90 days)
    behavior_metrics = spark.sql("""
    SELECT
        user_id,
        COUNT(DISTINCT DATE(timestamp)) as active_days_90d,
        COUNT(DISTINCT CASE WHEN event_name = 'page_view' THEN event_id END) as page_views_90d,
        COUNT(DISTINCT CASE WHEN event_name LIKE '%product%' THEN event_id END) as product_interactions_90d,
        MAX(timestamp) as last_activity_date
    FROM marketing_data.events
    WHERE timestamp >= date_sub(current_date(), 90)
    GROUP BY user_id
    """)

    # Revenue metrics
    revenue_metrics = spark.sql("""
    SELECT
        user_id,
        COUNT(DISTINCT CASE WHEN event_name = 'order_completed'
            THEN properties['order_id'] END) as total_orders,
        SUM(CASE WHEN event_name = 'order_completed' THEN revenue ELSE 0 END) as lifetime_revenue,
        SUM(CASE WHEN event_name = 'order_completed'
            AND timestamp >= date_sub(current_date(), 90)
            THEN revenue ELSE 0 END) as revenue_90d,
        MAX(CASE WHEN event_name = 'order_completed' THEN timestamp END) as last_purchase_date,
        MIN(CASE WHEN event_name = 'order_completed' THEN timestamp END) as first_purchase_date
    FROM marketing_data.events
    GROUP BY user_id
    """)

    # Attribution (first and last touch)
    window_spec_first = Window.partitionBy("user_id").orderBy("timestamp")
    window_spec_last = Window.partitionBy("user_id").orderBy(col("timestamp").desc())

    attribution = spark.table("marketing_data.events") \
        .filter(col("utm_source").isNotNull()) \
        .select(
            "user_id",
            first("utm_source").over(window_spec_first).alias("first_touch_source"),
            first("utm_campaign").over(window_spec_first).alias("first_touch_campaign"),
            first("utm_source").over(window_spec_last).alias("last_touch_source"),
            first("utm_campaign").over(window_spec_last).alias("last_touch_campaign")
        ) \
        .distinct()

    # Join all metrics
    customer_360 = user_profiles \
        .join(behavior_metrics, "user_id", "left") \
        .join(revenue_metrics, "user_id", "left") \
        .join(attribution, "user_id", "left") \
        .withColumn("days_since_purchase",
                    datediff(current_date(), col("last_purchase_date"))) \
        .withColumn("customer_tier",
                    when(col("revenue_90d") > 1000, "high_value")
                    .when(col("revenue_90d") > 500, "medium_value")
                    .when(col("total_orders") > 0, "low_value")
                    .otherwise("prospect")) \
        .withColumn("engagement_level",
                    when(col("active_days_90d") >= 20, "highly_engaged")
                    .when(col("active_days_90d") >= 10, "engaged")
                    .when(col("active_days_90d") >= 3, "casual")
                    .otherwise("inactive"))

    # Write to Delta table
    customer_360.write \
        .format("delta") \
        .mode("overwrite") \
        .option("overwriteSchema", "true") \
        .saveAsTable("marketing_data.customer_360")

    return customer_360

# Build customer 360
customer_360_df = build_customer_360()
customer_360_df.show(10)
```

**Audience Segmentation with Delta**

```sql
-- Using Databricks SQL

-- High-value customers
CREATE OR REPLACE TABLE marketing_data.audience_high_value
USING DELTA
AS
SELECT
    user_id,
    email,
    name,
    lifetime_revenue,
    revenue_90d,
    'high_value_customers' as audience_name,
    current_timestamp() as created_at
FROM marketing_data.customer_360
WHERE revenue_90d > 1000
    AND days_since_purchase <= 90;

-- Cart abandoners (last 7 days)
CREATE OR REPLACE TABLE marketing_data.audience_cart_abandoners
USING DELTA
AS
WITH recent_cart_adds AS (
    SELECT
        user_id,
        MAX(timestamp) as last_cart_add,
        COUNT(DISTINCT properties['product_id']) as products_in_cart
    FROM marketing_data.events
    WHERE event_name IN ('product_added', 'cart_updated')
        AND timestamp >= date_sub(current_date(), 7)
    GROUP BY user_id
),
recent_purchases AS (
    SELECT DISTINCT user_id
    FROM marketing_data.events
    WHERE event_name = 'order_completed'
        AND timestamp >= date_sub(current_date(), 7)
)
SELECT
    c.user_id,
    p.email,
    p.name,
    c.last_cart_add,
    c.products_in_cart,
    'cart_abandoner' as audience_name,
    current_timestamp() as created_at
FROM recent_cart_adds c
JOIN marketing_data.user_profiles p ON c.user_id = p.user_id
WHERE c.user_id NOT IN (SELECT user_id FROM recent_purchases);
```

### 3. ML-Powered Marketing Analytics

**Customer Lifetime Value Prediction**

```python
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import GBTRegressor
from pyspark.ml import Pipeline
import mlflow
import mlflow.spark

# Prepare training data
training_data = spark.sql("""
SELECT
    user_id,
    active_days_90d,
    page_views_90d,
    product_interactions_90d,
    total_orders,
    days_since_purchase,
    lifetime_revenue as label
FROM marketing_data.customer_360
WHERE lifetime_revenue > 0
    AND lifetime_revenue < 10000  -- Remove outliers
""")

# Split data
train_df, test_df = training_data.randomSplit([0.8, 0.2], seed=42)

# Feature engineering
feature_cols = [
    'active_days_90d',
    'page_views_90d',
    'product_interactions_90d',
    'total_orders',
    'days_since_purchase'
]

assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")

# Build model
gbt = GBTRegressor(
    featuresCol="features",
    labelCol="label",
    maxDepth=5,
    maxIter=100
)

pipeline = Pipeline(stages=[assembler, gbt])

# Train with MLflow tracking
with mlflow.start_run(run_name="ltv_prediction"):
    # Log parameters
    mlflow.log_param("max_depth", 5)
    mlflow.log_param("max_iter", 100)

    # Train model
    model = pipeline.fit(train_df)

    # Evaluate
    predictions = model.transform(test_df)
    from pyspark.ml.evaluation import RegressionEvaluator

    evaluator = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="rmse")
    rmse = evaluator.evaluate(predictions)

    mlflow.log_metric("rmse", rmse)
    mlflow.spark.log_model(model, "ltv_model")

    print(f"RMSE: {rmse}")

# Predict LTV for prospects
prospect_data = spark.sql("""
SELECT
    user_id,
    email,
    active_days_90d,
    page_views_90d,
    product_interactions_90d,
    total_orders,
    days_since_purchase
FROM marketing_data.customer_360
WHERE total_orders = 0
""")

ltv_predictions = model.transform(prospect_data) \
    .select("user_id", "email", col("prediction").alias("predicted_ltv")) \
    .orderBy(col("predicted_ltv").desc())

# Save predictions
ltv_predictions.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("marketing_data.ltv_predictions")

ltv_predictions.show(20)
```

**Churn Prediction Model**

```python
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator

# Prepare churn training data
churn_data = spark.sql("""
SELECT
    user_id,
    active_days_90d,
    page_views_90d,
    days_since_purchase,
    lifetime_revenue,
    CASE WHEN days_since_purchase > 90 THEN 1 ELSE 0 END as churned
FROM marketing_data.customer_360
WHERE total_orders > 0
""")

train_df, test_df = churn_data.randomSplit([0.8, 0.2], seed=42)

# Build churn model
churn_features = [
    'active_days_90d',
    'page_views_90d',
    'days_since_purchase',
    'lifetime_revenue'
]

assembler = VectorAssembler(inputCols=churn_features, outputCol="features")

rf = RandomForestClassifier(
    featuresCol="features",
    labelCol="churned",
    numTrees=100,
    maxDepth=5
)

pipeline = Pipeline(stages=[assembler, rf])

# Train with MLflow
with mlflow.start_run(run_name="churn_prediction"):
    mlflow.log_param("num_trees", 100)
    mlflow.log_param("max_depth", 5)

    model = pipeline.fit(train_df)

    predictions = model.transform(test_df)

    evaluator = BinaryClassificationEvaluator(labelCol="churned", metricName="areaUnderROC")
    auc = evaluator.evaluate(predictions)

    mlflow.log_metric("auc", auc)
    mlflow.spark.log_model(model, "churn_model")

    print(f"AUC: {auc}")

# Identify churn risk customers
active_customers = spark.sql("""
SELECT
    user_id,
    email,
    active_days_90d,
    page_views_90d,
    days_since_purchase,
    lifetime_revenue
FROM marketing_data.customer_360
WHERE total_orders > 0
    AND days_since_purchase <= 90
""")

churn_predictions = model.transform(active_customers)

# Get churn probability
churn_risk = churn_predictions \
    .select(
        "user_id",
        "email",
        "lifetime_revenue",
        col("probability").getItem(1).alias("churn_probability")
    ) \
    .filter(col("churn_probability") > 0.7) \
    .orderBy(col("churn_probability").desc())

# Save churn risk audience
churn_risk.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("marketing_data.audience_churn_risk")

churn_risk.show(20)
```

### 4. Advanced Attribution Modeling

**Multi-Touch Attribution with Spark SQL**

```sql
-- Multi-touch attribution using Databricks SQL
CREATE OR REPLACE TABLE marketing_data.attribution_analysis
USING DELTA
AS
WITH touchpoints AS (
    SELECT
        user_id,
        timestamp,
        utm_source,
        utm_medium,
        utm_campaign,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp) as touch_number,
        COUNT(*) OVER (PARTITION BY user_id) as total_touches
    FROM marketing_data.events
    WHERE utm_source IS NOT NULL
),
conversions AS (
    SELECT
        user_id,
        properties['order_id'] as order_id,
        timestamp as conversion_time,
        revenue
    FROM marketing_data.events
    WHERE event_name = 'order_completed'
),
attributed_touches AS (
    SELECT
        t.user_id,
        c.order_id,
        c.revenue,
        t.utm_source,
        t.utm_medium,
        t.utm_campaign,
        t.touch_number,
        t.total_touches,
        datediff(c.conversion_time, t.timestamp) as days_to_conversion,
        -- Attribution weights
        CASE WHEN t.touch_number = 1 THEN 1.0 ELSE 0 END as first_touch_weight,
        CASE WHEN t.touch_number = t.total_touches THEN 1.0 ELSE 0 END as last_touch_weight,
        1.0 / t.total_touches as linear_weight,
        POW(0.5, datediff(c.conversion_time, t.timestamp) / 7.0) as time_decay_base
    FROM touchpoints t
    JOIN conversions c ON t.user_id = c.user_id
    WHERE t.timestamp <= c.conversion_time
),
time_decay_normalized AS (
    SELECT
        *,
        time_decay_base / SUM(time_decay_base) OVER (PARTITION BY order_id) as time_decay_weight
    FROM attributed_touches
)
SELECT
    utm_source,
    utm_medium,
    utm_campaign,
    COUNT(DISTINCT order_id) as total_conversions,
    SUM(revenue * first_touch_weight) as first_touch_revenue,
    SUM(revenue * last_touch_weight) as last_touch_revenue,
    SUM(revenue * linear_weight) as linear_revenue,
    SUM(revenue * time_decay_weight) as time_decay_revenue,
    AVG(days_to_conversion) as avg_days_to_conversion
FROM time_decay_normalized
GROUP BY utm_source, utm_medium, utm_campaign
ORDER BY time_decay_revenue DESC;
```

**Markov Chain Attribution (Python)**

```python
from pyspark.sql.functions import collect_list, array_join

def markov_chain_attribution():
    """Advanced Markov Chain attribution model"""

    # Build user paths
    user_paths = spark.sql("""
    WITH user_touchpoints AS (
        SELECT
            user_id,
            utm_source,
            timestamp,
            CASE WHEN event_name = 'order_completed' THEN 1 ELSE 0 END as converted
        FROM marketing_data.events
        WHERE utm_source IS NOT NULL
    ),
    ordered_paths AS (
        SELECT
            user_id,
            collect_list(utm_source) OVER (
                PARTITION BY user_id ORDER BY timestamp
                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            ) as path,
            MAX(converted) as converted
        FROM user_touchpoints
    )
    SELECT DISTINCT
        user_id,
        array_join(path, ' > ') as path_string,
        converted
    FROM ordered_paths
    """)

    # Calculate transition probabilities
    # This is a simplified version - full Markov chain would require
    # more complex probability calculations

    conversion_paths = user_paths.filter(col("converted") == 1)
    non_conversion_paths = user_paths.filter(col("converted") == 0)

    # Channel removal effect
    channels = spark.sql("""
    SELECT DISTINCT utm_source
    FROM marketing_data.events
    WHERE utm_source IS NOT NULL
    """).collect()

    removal_effects = []
    for row in channels:
        channel = row['utm_source']

        # Calculate conversions with and without channel
        with_channel = conversion_paths.filter(col("path_string").contains(channel)).count()
        total_conversions = conversion_paths.count()

        removal_effect = with_channel / total_conversions if total_conversions > 0 else 0
        removal_effects.append((channel, removal_effect))

    # Create attribution weights
    removal_df = spark.createDataFrame(removal_effects, ["channel", "removal_effect"])

    total_effect = removal_df.agg({"removal_effect": "sum"}).collect()[0][0]

    markov_attribution = removal_df.withColumn(
        "attribution_weight",
        col("removal_effect") / total_effect
    )

    return markov_attribution

markov_results = markov_chain_attribution()
markov_results.show()
```

## Installation and Authentication

### Databricks SQL Connector

```bash
pip install databricks-sql-connector
```

```python
from databricks import sql
import os

# Connect to Databricks
connection = sql.connect(
    server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
    http_path=os.getenv("DATABRICKS_HTTP_PATH"),
    access_token=os.getenv("DATABRICKS_TOKEN")
)

cursor = connection.cursor()
cursor.execute("SELECT * FROM marketing_data.customer_360 LIMIT 10")
result = cursor.fetchall()

for row in result:
    print(row)

cursor.close()
connection.close()
```

### PySpark with Databricks

```python
# In Databricks notebook
from pyspark.sql import SparkSession

# Spark is automatically initialized in Databricks
df = spark.table("marketing_data.customer_360")
df.show()
```

## Quick Start

### Complete Marketing Analytics Workflow

```python
# In Databricks notebook
from pyspark.sql.functions import *
import mlflow

# 1. Load and prepare marketing data
events_df = spark.table("marketing_data.events")

# 2. Build customer 360
customer_360 = build_customer_360()

# 3. Create high-value audience
high_value = customer_360 \
    .filter(col("revenue_90d") > 1000) \
    .select("user_id", "email", "lifetime_revenue")

print(f"High-value customers: {high_value.count()}")
high_value.show(10)

# 4. Train LTV prediction model
# (See ML-Powered Marketing Analytics section)

# 5. Run attribution analysis
attribution_df = spark.table("marketing_data.attribution_analysis")

print("\nTop Channels by Time-Decay Attribution:")
attribution_df \
    .orderBy(col("time_decay_revenue").desc()) \
    .show(10)

# 6. Export audience for activation
high_value.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("marketing_data.audiences.high_value_export")
```

## References

- **Official Documentation**: https://docs.databricks.com/
- **Delta Lake**: https://docs.databricks.com/delta/
- **Databricks SQL**: https://docs.databricks.com/sql/
- **MLflow**: https://www.mlflow.org/docs/latest/index.html
- **PySpark**: https://spark.apache.org/docs/latest/api/python/
- **Python Connector**: https://docs.databricks.com/dev-tools/python-sql-connector.html
- **Machine Learning**: https://docs.databricks.com/machine-learning/
- **Feature Store**: https://docs.databricks.com/machine-learning/feature-store/
- **Best Practices**: https://docs.databricks.com/best-practices/
- **Lakehouse Platform**: https://www.databricks.com/product/data-lakehouse

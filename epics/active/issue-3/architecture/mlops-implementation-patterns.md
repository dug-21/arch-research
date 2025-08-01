# MLOps Implementation Patterns for Payment Systems - 2025 Standards

## Executive Summary

This document provides production-ready implementation patterns to achieve MLOps maturity level 4 (85% target) from the current level 1 (25%). These patterns focus on automated pipelines, feature stores, model governance, and continuous deployment for payment fraud detection and risk scoring models.

## Table of Contents

1. [MLOps Platform Architecture](#mlops-platform-architecture)
2. [Automated Training Pipelines](#automated-training-pipelines)
3. [Feature Store Implementation](#feature-store-implementation)
4. [Model Registry and Versioning](#model-registry-and-versioning)
5. [A/B Testing Framework](#ab-testing-framework)
6. [Model Monitoring and Observability](#model-monitoring-and-observability)
7. [Automated Retraining](#automated-retraining)
8. [CI/CD for ML Models](#cicd-for-ml-models)
9. [Production Deployment Patterns](#production-deployment-patterns)
10. [Cost Optimization](#cost-optimization)

## 1. MLOps Platform Architecture

### Infrastructure Stack

```yaml
# mlops-platform/infrastructure/terraform/main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

# EKS Cluster for MLOps
module "eks_mlops" {
  source = "./modules/eks"
  
  cluster_name = "payment-mlops-cluster"
  cluster_version = "1.28"
  
  node_groups = {
    ml_training = {
      instance_types = ["p3.8xlarge", "p3.16xlarge"]
      min_size = 0
      max_size = 10
      desired_size = 2
      
      labels = {
        workload = "ml-training"
      }
      
      taints = [{
        key    = "nvidia.com/gpu"
        value  = "true"
        effect = "NO_SCHEDULE"
      }]
    }
    
    ml_inference = {
      instance_types = ["g4dn.xlarge", "g4dn.2xlarge"]
      min_size = 3
      max_size = 20
      desired_size = 5
      
      labels = {
        workload = "ml-inference"
      }
    }
  }
}
```

### Kubeflow Installation

```bash
#!/bin/bash
# install-kubeflow.sh

# Install Kubeflow on EKS
export CLUSTER_NAME=payment-mlops-cluster
export AWS_REGION=us-east-1

# Install Kustomize
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
sudo mv kustomize /usr/local/bin/

# Clone Kubeflow manifests
git clone https://github.com/kubeflow/manifests.git
cd manifests

# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Install Istio for Kubeflow
kustomize build common/istio-1-17/istio-crds/base | kubectl apply -f -
kustomize build common/istio-1-17/istio-namespace/base | kubectl apply -f -
kustomize build common/istio-1-17/istio-install/base | kubectl apply -f -

# Install Kubeflow
while ! kustomize build example | kubectl apply -f -; do echo "Retrying..."; sleep 10; done

# Configure GPU support
kubectl apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: gpu-operator-config
  namespace: gpu-operator
data:
  gpu-feature-discovery: "true"
  cuda-toolkit: "11.8"
  driver-version: "525.60.13"
EOF
```

## 2. Automated Training Pipelines

### Kubeflow Pipeline for Fraud Detection

```python
# pipelines/fraud_detection_pipeline.py
from kfp import dsl, compiler
from kfp.dsl import component, Input, Output, Dataset, Model, Metrics
import kfp.components as comp

@component(
    base_image="python:3.9",
    packages_to_install=["pandas", "numpy", "scikit-learn", "feast", "mlflow"]
)
def extract_features(
    start_date: str,
    end_date: str,
    feature_repo: str,
    output_dataset: Output[Dataset]
):
    """Extract features from Feast feature store"""
    import pandas as pd
    from feast import FeatureStore
    from datetime import datetime
    
    # Initialize feature store
    fs = FeatureStore(repo_path=feature_repo)
    
    # Define feature service
    feature_service = fs.get_feature_service("fraud_detection_features")
    
    # Create entity dataframe
    entity_df = pd.DataFrame({
        "transaction_id": fs.get_entity("transaction").join_keys,
        "event_timestamp": pd.date_range(
            start=start_date, 
            end=end_date, 
            freq='1min'
        )
    })
    
    # Retrieve features
    training_df = fs.get_historical_features(
        entity_df=entity_df,
        features=feature_service,
    ).to_df()
    
    # Save dataset
    training_df.to_parquet(output_dataset.path)
    
    # Log metadata
    output_dataset.metadata["row_count"] = len(training_df)
    output_dataset.metadata["feature_count"] = len(training_df.columns)
    output_dataset.metadata["date_range"] = f"{start_date} to {end_date}"

@component(
    base_image="python:3.9",
    packages_to_install=["pandas", "numpy", "xgboost", "scikit-learn", "mlflow"]
)
def train_fraud_model(
    training_data: Input[Dataset],
    hyperparameters: dict,
    output_model: Output[Model],
    metrics: Output[Metrics]
):
    """Train XGBoost fraud detection model"""
    import pandas as pd
    import xgboost as xgb
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import roc_auc_score, precision_recall_curve
    import mlflow
    import mlflow.xgboost
    
    # Load data
    df = pd.read_parquet(training_data.path)
    
    # Prepare features and target
    feature_cols = [col for col in df.columns if col not in ['is_fraud', 'transaction_id', 'event_timestamp']]
    X = df[feature_cols]
    y = df['is_fraud']
    
    # Split data
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Create DMatrix
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_val, label=y_val)
    
    # Set up MLflow
    mlflow.set_tracking_uri("http://mlflow-service:5000")
    mlflow.set_experiment("payment-fraud-detection")
    
    with mlflow.start_run():
        # Log hyperparameters
        mlflow.log_params(hyperparameters)
        
        # Train model
        evallist = [(dtrain, 'train'), (dval, 'val')]
        
        model = xgb.train(
            hyperparameters,
            dtrain,
            num_boost_round=1000,
            evals=evallist,
            early_stopping_rounds=50,
            verbose_eval=100
        )
        
        # Make predictions
        y_pred = model.predict(dval)
        
        # Calculate metrics
        auc_score = roc_auc_score(y_val, y_pred)
        precision, recall, _ = precision_recall_curve(y_val, y_pred)
        
        # Log metrics
        mlflow.log_metric("auc", auc_score)
        mlflow.log_metric("precision_at_1_percent_fpr", precision[int(0.01 * len(precision))])
        
        metrics.log_metric("auc", auc_score)
        metrics.log_metric("val_samples", len(y_val))
        
        # Log model
        mlflow.xgboost.log_model(
            model, 
            "model",
            registered_model_name="payment-fraud-detector"
        )
        
        # Save model artifact
        model.save_model(output_model.path)
        
        # Save metadata
        output_model.metadata["framework"] = "xgboost"
        output_model.metadata["auc"] = auc_score
        output_model.metadata["feature_count"] = len(feature_cols)
        output_model.metadata["training_samples"] = len(y_train)

@component(
    base_image="python:3.9",
    packages_to_install=["mlflow", "evidently", "pandas", "numpy"]
)
def validate_model(
    model: Input[Model],
    validation_data: Input[Dataset],
    baseline_metrics: dict,
    deploy_decision: Output[str]
):
    """Validate model against baseline metrics"""
    import pandas as pd
    import xgboost as xgb
    from sklearn.metrics import roc_auc_score, precision_score, recall_score
    import json
    
    # Load model and data
    model_obj = xgb.Booster()
    model_obj.load_model(model.path)
    
    df = pd.read_parquet(validation_data.path)
    
    # Prepare data
    feature_cols = [col for col in df.columns if col not in ['is_fraud', 'transaction_id', 'event_timestamp']]
    X_val = df[feature_cols]
    y_val = df['is_fraud']
    
    dval = xgb.DMatrix(X_val)
    y_pred = model_obj.predict(dval)
    
    # Calculate metrics
    current_metrics = {
        "auc": roc_auc_score(y_val, y_pred),
        "precision": precision_score(y_val, (y_pred > 0.5).astype(int)),
        "recall": recall_score(y_val, (y_pred > 0.5).astype(int))
    }
    
    # Compare with baseline
    deploy = True
    reasons = []
    
    for metric, value in current_metrics.items():
        if metric in baseline_metrics:
            if value < baseline_metrics[metric] * 0.95:  # 5% degradation threshold
                deploy = False
                reasons.append(f"{metric} degraded: {value:.4f} < {baseline_metrics[metric] * 0.95:.4f}")
    
    # Write decision
    decision = {
        "deploy": deploy,
        "current_metrics": current_metrics,
        "baseline_metrics": baseline_metrics,
        "reasons": reasons
    }
    
    with open(deploy_decision.path, 'w') as f:
        json.dump(decision, f)

@dsl.pipeline(
    name="Payment Fraud Detection Training Pipeline",
    description="End-to-end ML pipeline for fraud detection"
)
def fraud_detection_pipeline(
    start_date: str = "2024-01-01",
    end_date: str = "2024-12-31",
    feature_repo: str = "s3://payment-mlops/feature-store",
    hyperparameters: dict = {
        "objective": "binary:logistic",
        "max_depth": 6,
        "eta": 0.3,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "scale_pos_weight": 10  # Handle class imbalance
    },
    baseline_metrics: dict = {
        "auc": 0.95,
        "precision": 0.85,
        "recall": 0.80
    }
):
    # Extract features
    feature_extraction = extract_features(
        start_date=start_date,
        end_date=end_date,
        feature_repo=feature_repo
    )
    
    # Train model
    model_training = train_fraud_model(
        training_data=feature_extraction.outputs["output_dataset"],
        hyperparameters=hyperparameters
    )
    
    # Validate model
    model_validation = validate_model(
        model=model_training.outputs["output_model"],
        validation_data=feature_extraction.outputs["output_dataset"],
        baseline_metrics=baseline_metrics
    )
    
    # Conditional deployment
    with dsl.Condition(model_validation.outputs["deploy_decision"] == "true"):
        deploy_op = comp.load_component_from_file("components/deploy_model.yaml")
        deploy_op(
            model=model_training.outputs["output_model"],
            deployment_name="fraud-detector-prod"
        )

# Compile pipeline
compiler.Compiler().compile(
    pipeline_func=fraud_detection_pipeline,
    package_path="fraud_detection_pipeline.yaml"
)
```

## 3. Feature Store Implementation

### Feast Configuration

```yaml
# feature_store/feature_store.yaml
project: payment_fraud_detection
registry: s3://payment-mlops/feast/registry.db
provider: aws
online_store:
  type: dynamodb
  region: us-east-1
offline_store:
  type: athena
  region: us-east-1
  database: payment_features
  s3_staging_location: s3://payment-mlops/feast/staging
```

### Feature Definitions

```python
# feature_store/features/transaction_features.py
from datetime import timedelta
from feast import Entity, Feature, FeatureView, FileSource, ValueType
from feast.types import Float32, Float64, Int64, String

# Define entities
transaction = Entity(
    name="transaction",
    value_type=ValueType.STRING,
    description="Transaction ID",
    join_keys=["transaction_id"]
)

user = Entity(
    name="user",
    value_type=ValueType.STRING,
    description="User ID",
    join_keys=["user_id"]
)

merchant = Entity(
    name="merchant",
    value_type=ValueType.STRING,
    description="Merchant ID",
    join_keys=["merchant_id"]
)

# Define data sources
transaction_source = FileSource(
    name="transaction_source",
    path="s3://payment-data/transactions/*.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

user_profile_source = FileSource(
    name="user_profile_source",
    path="s3://payment-data/user_profiles/*.parquet",
    timestamp_field="event_timestamp",
)

# Transaction features
transaction_features = FeatureView(
    name="transaction_features",
    entities=[transaction],
    ttl=timedelta(days=365),
    schema=[
        Feature("amount", Float64),
        Feature("currency", String),
        Feature("merchant_category", String),
        Feature("channel", String),
        Feature("country_code", String),
        Feature("time_of_day", Int64),
        Feature("day_of_week", Int64),
        Feature("is_weekend", Int64),
        Feature("device_type", String),
        Feature("ip_country", String),
    ],
    online=True,
    source=transaction_source,
    tags={"team": "fraud-detection"},
)

# User aggregated features
user_stats = FeatureView(
    name="user_transaction_stats",
    entities=[user],
    ttl=timedelta(days=30),
    schema=[
        Feature("transaction_count_1d", Int64),
        Feature("transaction_count_7d", Int64),
        Feature("transaction_count_30d", Int64),
        Feature("avg_transaction_amount_1d", Float64),
        Feature("avg_transaction_amount_7d", Float64),
        Feature("avg_transaction_amount_30d", Float64),
        Feature("unique_merchants_1d", Int64),
        Feature("unique_merchants_7d", Int64),
        Feature("failed_transactions_1d", Int64),
        Feature("max_transaction_1d", Float64),
        Feature("velocity_score", Float32),
    ],
    online=True,
    source=user_profile_source,
    tags={"team": "fraud-detection"},
)

# Merchant risk features
merchant_risk = FeatureView(
    name="merchant_risk_features",
    entities=[merchant],
    ttl=timedelta(days=90),
    schema=[
        Feature("chargeback_rate", Float32),
        Feature("fraud_rate", Float32),
        Feature("avg_transaction_amount", Float64),
        Feature("transaction_volume_30d", Int64),
        Feature("risk_score", Float32),
        Feature("merchant_tenure_days", Int64),
        Feature("country_risk_score", Float32),
    ],
    online=True,
    source=FileSource(
        path="s3://payment-data/merchant_profiles/*.parquet",
        timestamp_field="event_timestamp",
    ),
    tags={"team": "fraud-detection", "pii": "false"},
)
```

### Feature Engineering Pipeline

```python
# feature_store/pipelines/feature_engineering.py
import pandas as pd
import numpy as np
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.window import Window
from datetime import datetime, timedelta

class FeatureEngineeringPipeline:
    def __init__(self, spark: SparkSession):
        self.spark = spark
        
    def compute_user_velocity_features(self, transactions_df):
        """Compute user velocity features for fraud detection"""
        
        # Define time windows
        windows = {
            "1h": Window.partitionBy("user_id").orderBy(F.col("event_timestamp").cast("long"))
                        .rangeBetween(-3600, 0),
            "24h": Window.partitionBy("user_id").orderBy(F.col("event_timestamp").cast("long"))
                         .rangeBetween(-86400, 0),
            "7d": Window.partitionBy("user_id").orderBy(F.col("event_timestamp").cast("long"))
                        .rangeBetween(-604800, 0),
        }
        
        # Calculate velocity features
        velocity_df = transactions_df
        
        for window_name, window_spec in windows.items():
            velocity_df = velocity_df.withColumn(
                f"transaction_count_{window_name}",
                F.count("transaction_id").over(window_spec)
            ).withColumn(
                f"unique_merchants_{window_name}",
                F.size(F.collect_set("merchant_id").over(window_spec))
            ).withColumn(
                f"total_amount_{window_name}",
                F.sum("amount").over(window_spec)
            ).withColumn(
                f"unique_countries_{window_name}",
                F.size(F.collect_set("country_code").over(window_spec))
            )
        
        # Calculate velocity change ratios
        velocity_df = velocity_df.withColumn(
            "velocity_ratio_1h_24h",
            F.when(F.col("transaction_count_24h") > 0,
                   F.col("transaction_count_1h") * 24 / F.col("transaction_count_24h"))
            .otherwise(0)
        ).withColumn(
            "amount_velocity_1h_7d",
            F.when(F.col("total_amount_7d") > 0,
                   F.col("total_amount_1h") * 168 / F.col("total_amount_7d"))
            .otherwise(0)
        )
        
        # Flag suspicious velocity patterns
        velocity_df = velocity_df.withColumn(
            "high_velocity_flag",
            F.when(
                (F.col("transaction_count_1h") > 10) |
                (F.col("velocity_ratio_1h_24h") > 5) |
                (F.col("unique_countries_1h") > 3),
                1
            ).otherwise(0)
        )
        
        return velocity_df
    
    def compute_merchant_risk_features(self, transactions_df):
        """Compute merchant risk features"""
        
        # Calculate merchant statistics
        merchant_stats = transactions_df.groupBy("merchant_id").agg(
            F.count("transaction_id").alias("total_transactions"),
            F.sum(F.when(F.col("is_fraud") == 1, 1).otherwise(0)).alias("fraud_count"),
            F.sum(F.when(F.col("is_chargeback") == 1, 1).otherwise(0)).alias("chargeback_count"),
            F.avg("amount").alias("avg_transaction_amount"),
            F.stddev("amount").alias("stddev_transaction_amount"),
            F.min("event_timestamp").alias("first_transaction_date"),
            F.max("event_timestamp").alias("last_transaction_date")
        )
        
        # Calculate rates
        merchant_stats = merchant_stats.withColumn(
            "fraud_rate",
            F.col("fraud_count") / F.col("total_transactions")
        ).withColumn(
            "chargeback_rate",
            F.col("chargeback_count") / F.col("total_transactions")
        ).withColumn(
            "merchant_tenure_days",
            F.datediff(F.current_date(), F.col("first_transaction_date"))
        )
        
        # Calculate risk score
        merchant_stats = merchant_stats.withColumn(
            "risk_score",
            (
                F.col("fraud_rate") * 0.5 +
                F.col("chargeback_rate") * 0.3 +
                F.when(F.col("merchant_tenure_days") < 30, 0.2).otherwise(0)
            )
        )
        
        return merchant_stats
    
    def compute_device_fingerprint_features(self, device_df):
        """Compute device fingerprinting features"""
        
        device_features = device_df.withColumn(
            "device_age_hours",
            (F.current_timestamp().cast("long") - F.col("first_seen").cast("long")) / 3600
        ).withColumn(
            "is_new_device",
            F.when(F.col("device_age_hours") < 24, 1).otherwise(0)
        ).withColumn(
            "device_transaction_velocity",
            F.col("transaction_count_24h") / F.greatest(F.col("device_age_hours") / 24, F.lit(1))
        )
        
        # Compute device sharing indicators
        window_spec = Window.partitionBy("device_fingerprint").orderBy("event_timestamp")
        
        device_features = device_features.withColumn(
            "unique_users_per_device",
            F.size(F.collect_set("user_id").over(window_spec))
        ).withColumn(
            "device_sharing_flag",
            F.when(F.col("unique_users_per_device") > 3, 1).otherwise(0)
        )
        
        return device_features
    
    def create_feature_dataset(self, start_date: str, end_date: str):
        """Create complete feature dataset for training"""
        
        # Load raw data
        transactions_df = self.spark.read.parquet(
            f"s3://payment-data/transactions/date_range={start_date}_{end_date}"
        )
        
        device_df = self.spark.read.parquet(
            "s3://payment-data/device_fingerprints/latest"
        )
        
        # Compute features
        velocity_features = self.compute_user_velocity_features(transactions_df)
        merchant_features = self.compute_merchant_risk_features(transactions_df)
        device_features = self.compute_device_fingerprint_features(device_df)
        
        # Join all features
        feature_dataset = velocity_features.join(
            merchant_features,
            on="merchant_id",
            how="left"
        ).join(
            device_features,
            on=["device_fingerprint", "event_timestamp"],
            how="left"
        )
        
        # Write to feature store
        output_path = f"s3://payment-mlops/feature-store/training_datasets/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        feature_dataset.write.mode("overwrite").parquet(output_path)
        
        return output_path
```

## 4. Model Registry and Versioning

### MLflow Model Registry Configuration

```python
# model_registry/mlflow_config.py
import mlflow
from mlflow.tracking import MlflowClient
from mlflow.models.signature import infer_signature
import pandas as pd
import json

class PaymentModelRegistry:
    def __init__(self, tracking_uri: str = "http://mlflow-service:5000"):
        self.tracking_uri = tracking_uri
        mlflow.set_tracking_uri(tracking_uri)
        self.client = MlflowClient()
        
    def register_model(self, model, model_name: str, features_df: pd.DataFrame, tags: dict = None):
        """Register a new model version with comprehensive metadata"""
        
        # Infer model signature
        signature = infer_signature(features_df, model.predict(features_df))
        
        # Start MLflow run
        with mlflow.start_run() as run:
            # Log model
            mlflow.sklearn.log_model(
                model,
                artifact_path="model",
                signature=signature,
                registered_model_name=model_name,
                await_registration_for=120
            )
            
            # Log feature importance
            if hasattr(model, 'feature_importances_'):
                feature_importance = pd.DataFrame({
                    'feature': features_df.columns,
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False)
                
                mlflow.log_table(feature_importance, "feature_importance.json")
            
            # Log model metadata
            mlflow.log_param("model_type", type(model).__name__)
            mlflow.log_param("n_features", len(features_df.columns))
            mlflow.log_param("feature_names", json.dumps(list(features_df.columns)))
            
            # Log tags
            if tags:
                mlflow.set_tags(tags)
            
            # Get the latest version
            model_version = self.client.get_latest_versions(
                name=model_name,
                stages=["None"]
            )[0]
            
            return model_version
    
    def promote_model(self, model_name: str, version: str, stage: str = "Staging"):
        """Promote model to different stages with validation"""
        
        # Get current model in production
        try:
            prod_versions = self.client.get_latest_versions(
                name=model_name,
                stages=["Production"]
            )
            current_prod = prod_versions[0] if prod_versions else None
        except:
            current_prod = None
        
        # Transition new model to staging
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage,
            archive_existing_versions=False
        )
        
        # Add deployment metadata
        self.client.set_model_version_tag(
            name=model_name,
            version=version,
            key="deployment_timestamp",
            value=str(pd.Timestamp.now())
        )
        
        if current_prod:
            self.client.set_model_version_tag(
                name=model_name,
                version=version,
                key="replaced_version",
                value=current_prod.version
            )
        
        return {
            "model_name": model_name,
            "version": version,
            "stage": stage,
            "previous_production": current_prod.version if current_prod else None
        }
    
    def create_model_alias(self, model_name: str, alias: str, version: str):
        """Create model alias for easy reference"""
        self.client.set_registered_model_alias(
            name=model_name,
            alias=alias,
            version=version
        )
        
    def get_model_lineage(self, model_name: str, version: str):
        """Get complete model lineage including data and code"""
        
        model_version = self.client.get_model_version(
            name=model_name,
            version=version
        )
        
        run = self.client.get_run(model_version.run_id)
        
        lineage = {
            "model_name": model_name,
            "version": version,
            "run_id": model_version.run_id,
            "creation_timestamp": model_version.creation_timestamp,
            "training_data": run.data.params.get("training_data_path"),
            "git_commit": run.data.tags.get("mlflow.source.git.commit"),
            "source_code": run.data.tags.get("mlflow.source.name"),
            "metrics": run.data.metrics,
            "parameters": run.data.params,
            "tags": run.data.tags
        }
        
        return lineage
```

### Model Deployment Configuration

```yaml
# model_registry/deployment_config.yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: fraud-detector
  namespace: payment-mlops
spec:
  protocol: v2
  name: fraud-detector
  predictors:
  - name: default
    replicas: 3
    componentSpecs:
    - spec:
        containers:
        - name: model
          image: payment-mlops/fraud-detector:latest
          env:
          - name: MODEL_NAME
            value: payment-fraud-detector
          - name: MODEL_VERSION
            value: "latest"
          - name: MLFLOW_TRACKING_URI
            value: http://mlflow-service:5000
          resources:
            requests:
              memory: "2Gi"
              cpu: "1"
            limits:
              memory: "4Gi"
              cpu: "2"
              nvidia.com/gpu: "1"
    graph:
      name: model
      type: MODEL
      implementation: MLFLOW_SERVER
      modelUri: mlflow:payment-fraud-detector/Production
      envSecretRefName: mlflow-secret
    
    # Canary deployment configuration
    canaryTraffic: 5
    
    # Scaling configuration
    hpa:
      minReplicas: 3
      maxReplicas: 20
      metrics:
      - type: Resource
        resource:
          name: cpu
          targetAverageUtilization: 70
      - type: Resource
        resource:
          name: memory
          targetAverageUtilization: 80
      - type: Pods
        pods:
          metric:
            name: inference_requests_per_second
          targetAverageValue: "100"
```

## 5. A/B Testing Framework

### A/B Test Controller

```python
# ab_testing/ab_test_controller.py
import numpy as np
from typing import Dict, List, Tuple
import redis
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
import hashlib

@dataclass
class ABTestConfig:
    test_id: str
    model_a: str  # Control model
    model_b: str  # Treatment model
    traffic_split: float  # Percentage for model B
    success_metrics: Dict[str, float]  # Target metrics
    min_sample_size: int
    max_duration_days: int
    
class ABTestController:
    def __init__(self, redis_host: str = "redis-service", redis_port: int = 6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.model_cache = {}
        
    def create_ab_test(self, config: ABTestConfig) -> str:
        """Create a new A/B test"""
        test_data = {
            "test_id": config.test_id,
            "model_a": config.model_a,
            "model_b": config.model_b,
            "traffic_split": config.traffic_split,
            "success_metrics": config.success_metrics,
            "min_sample_size": config.min_sample_size,
            "max_duration_days": config.max_duration_days,
            "start_time": datetime.now().isoformat(),
            "status": "active",
            "metrics": {
                "model_a": {"count": 0, "fraud_caught": 0, "false_positives": 0},
                "model_b": {"count": 0, "fraud_caught": 0, "false_positives": 0}
            }
        }
        
        self.redis_client.set(
            f"ab_test:{config.test_id}",
            json.dumps(test_data),
            ex=timedelta(days=config.max_duration_days).total_seconds()
        )
        
        return config.test_id
    
    def route_request(self, test_id: str, transaction_id: str) -> str:
        """Route request to appropriate model based on A/B test configuration"""
        test_data = self._get_test_data(test_id)
        
        if not test_data or test_data["status"] != "active":
            return "default"  # Fallback to default model
        
        # Use consistent hashing for sticky routing
        hash_value = int(hashlib.md5(transaction_id.encode()).hexdigest(), 16)
        threshold = int(test_data["traffic_split"] * (2**128))
        
        return test_data["model_b"] if hash_value < threshold else test_data["model_a"]
    
    def record_prediction(self, test_id: str, model_version: str, 
                         prediction: float, actual: bool = None):
        """Record prediction results for analysis"""
        test_data = self._get_test_data(test_id)
        
        if not test_data:
            return
        
        # Determine which model was used
        model_key = "model_a" if model_version == test_data["model_a"] else "model_b"
        
        # Update metrics
        test_data["metrics"][model_key]["count"] += 1
        
        if actual is not None:
            if actual and prediction > 0.5:
                test_data["metrics"][model_key]["fraud_caught"] += 1
            elif not actual and prediction > 0.5:
                test_data["metrics"][model_key]["false_positives"] += 1
        
        # Save updated data
        self.redis_client.set(
            f"ab_test:{test_id}",
            json.dumps(test_data)
        )
        
        # Check if test should be concluded
        self._check_test_completion(test_id, test_data)
    
    def _check_test_completion(self, test_id: str, test_data: dict):
        """Check if A/B test should be concluded"""
        total_samples = sum(m["count"] for m in test_data["metrics"].values())
        
        # Check sample size
        if total_samples >= test_data["min_sample_size"]:
            # Calculate statistical significance
            if self._is_statistically_significant(test_data):
                self._conclude_test(test_id, test_data)
        
        # Check duration
        start_time = datetime.fromisoformat(test_data["start_time"])
        if datetime.now() - start_time > timedelta(days=test_data["max_duration_days"]):
            self._conclude_test(test_id, test_data)
    
    def _is_statistically_significant(self, test_data: dict) -> bool:
        """Check if results are statistically significant using Chi-squared test"""
        from scipy.stats import chi2_contingency
        
        # Create contingency table
        a_metrics = test_data["metrics"]["model_a"]
        b_metrics = test_data["metrics"]["model_b"]
        
        if a_metrics["count"] == 0 or b_metrics["count"] == 0:
            return False
        
        table = [
            [a_metrics["fraud_caught"], a_metrics["count"] - a_metrics["fraud_caught"]],
            [b_metrics["fraud_caught"], b_metrics["count"] - b_metrics["fraud_caught"]]
        ]
        
        _, p_value, _, _ = chi2_contingency(table)
        
        return p_value < 0.05  # 95% confidence level
    
    def _conclude_test(self, test_id: str, test_data: dict):
        """Conclude A/B test and determine winner"""
        test_data["status"] = "completed"
        test_data["end_time"] = datetime.now().isoformat()
        
        # Calculate performance metrics
        a_metrics = test_data["metrics"]["model_a"]
        b_metrics = test_data["metrics"]["model_b"]
        
        a_precision = (a_metrics["fraud_caught"] / 
                      max(a_metrics["fraud_caught"] + a_metrics["false_positives"], 1))
        b_precision = (b_metrics["fraud_caught"] / 
                      max(b_metrics["fraud_caught"] + b_metrics["false_positives"], 1))
        
        # Determine winner
        if b_precision > a_precision * 1.05:  # 5% improvement threshold
            test_data["winner"] = "model_b"
            test_data["recommendation"] = f"Deploy {test_data['model_b']}"
        else:
            test_data["winner"] = "model_a"
            test_data["recommendation"] = f"Keep {test_data['model_a']}"
        
        # Save final results
        self.redis_client.set(
            f"ab_test:{test_id}:results",
            json.dumps(test_data)
        )
        
        # Notify deployment system
        self._notify_deployment_system(test_data)
    
    def _get_test_data(self, test_id: str) -> dict:
        """Retrieve test data from Redis"""
        data = self.redis_client.get(f"ab_test:{test_id}")
        return json.loads(data) if data else None
    
    def _notify_deployment_system(self, test_data: dict):
        """Notify deployment system of test results"""
        # Publish to deployment queue
        self.redis_client.publish(
            "deployment_decisions",
            json.dumps({
                "test_id": test_data["test_id"],
                "winner": test_data["winner"],
                "recommendation": test_data["recommendation"],
                "metrics": test_data["metrics"]
            })
        )
```

### A/B Test Integration

```python
# ab_testing/integration.py
from fastapi import FastAPI, Request
from typing import Dict
import asyncio
import httpx

app = FastAPI()
ab_controller = ABTestController()

@app.post("/predict")
async def predict(request: Request, transaction_data: Dict):
    """Prediction endpoint with A/B testing"""
    
    # Extract transaction ID
    transaction_id = transaction_data.get("transaction_id")
    
    # Check for active A/B tests
    active_test_id = await get_active_test()
    
    if active_test_id:
        # Route to appropriate model
        model_version = ab_controller.route_request(active_test_id, transaction_id)
        
        # Make prediction using selected model
        prediction = await make_prediction(model_version, transaction_data)
        
        # Record for A/B test analysis (async)
        asyncio.create_task(
            record_ab_result(active_test_id, model_version, prediction, transaction_id)
        )
    else:
        # Use production model
        prediction = await make_prediction("production", transaction_data)
    
    return {
        "transaction_id": transaction_id,
        "fraud_score": prediction,
        "model_version": model_version if active_test_id else "production"
    }

async def make_prediction(model_version: str, transaction_data: Dict) -> float:
    """Make prediction using specified model version"""
    
    # Call model serving endpoint
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://model-serving/{model_version}/predict",
            json=transaction_data,
            timeout=0.1  # 100ms timeout for low latency
        )
        
    return response.json()["fraud_score"]

async def record_ab_result(test_id: str, model_version: str, 
                          prediction: float, transaction_id: str):
    """Record A/B test results asynchronously"""
    
    # Wait for actual outcome (from payment processing)
    actual_outcome = await wait_for_outcome(transaction_id, timeout=300)  # 5 min timeout
    
    if actual_outcome is not None:
        ab_controller.record_prediction(
            test_id=test_id,
            model_version=model_version,
            prediction=prediction,
            actual=actual_outcome
        )
```

## 6. Model Monitoring and Observability

### Monitoring Stack Configuration

```yaml
# monitoring/prometheus-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: payment-mlops
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    rule_files:
      - /etc/prometheus/rules/*.yml
    
    scrape_configs:
      - job_name: 'ml-models'
        kubernetes_sd_configs:
          - role: pod
            namespaces:
              names:
                - payment-mlops
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
            action: replace
            target_label: __metrics_path__
            regex: (.+)
    
      - job_name: 'model-metrics'
        static_configs:
          - targets:
              - 'fraud-detector-service:9090'
              - 'risk-scorer-service:9090'
              - 'transaction-classifier-service:9090'
        metric_relabel_configs:
          - source_labels: [__name__]
            regex: 'model_.*'
            action: keep

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-rules
  namespace: payment-mlops
data:
  model-alerts.yml: |
    groups:
      - name: model_performance
        interval: 30s
        rules:
          - alert: ModelAccuracyDegraded
            expr: |
              rate(model_predictions_correct_total[5m]) / 
              rate(model_predictions_total[5m]) < 0.90
            for: 10m
            labels:
              severity: critical
              team: ml-platform
            annotations:
              summary: "Model accuracy below threshold"
              description: "Model {{ $labels.model_name }} accuracy is {{ $value }}"
          
          - alert: PredictionLatencyHigh
            expr: |
              histogram_quantile(0.99, 
                rate(model_prediction_duration_seconds_bucket[5m])
              ) > 0.1
            for: 5m
            labels:
              severity: warning
              team: ml-platform
            annotations:
              summary: "High prediction latency"
              description: "P99 latency is {{ $value }}s for {{ $labels.model_name }}"
          
          - alert: DataDriftDetected
            expr: |
              model_feature_drift_score > 0.3
            for: 30m
            labels:
              severity: warning
              team: ml-platform
            annotations:
              summary: "Data drift detected"
              description: "Feature {{ $labels.feature_name }} drift score is {{ $value }}"
```

### Custom Monitoring Library

```python
# monitoring/model_monitoring.py
from prometheus_client import Counter, Histogram, Gauge, Summary
import numpy as np
from typing import Dict, List, Optional
import pandas as pd
from scipy import stats
import json
import logging

# Prometheus metrics
prediction_counter = Counter(
    'model_predictions_total',
    'Total number of predictions',
    ['model_name', 'model_version', 'prediction_class']
)

prediction_latency = Histogram(
    'model_prediction_duration_seconds',
    'Prediction latency',
    ['model_name', 'model_version'],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
)

feature_drift_gauge = Gauge(
    'model_feature_drift_score',
    'Feature drift score',
    ['model_name', 'feature_name']
)

model_accuracy_gauge = Gauge(
    'model_accuracy_score',
    'Model accuracy score',
    ['model_name', 'model_version']
)

class ModelMonitor:
    def __init__(self, model_name: str, model_version: str, 
                 reference_data: pd.DataFrame):
        self.model_name = model_name
        self.model_version = model_version
        self.reference_data = reference_data
        self.reference_stats = self._compute_reference_stats()
        self.prediction_buffer = []
        self.logger = logging.getLogger(__name__)
        
    def _compute_reference_stats(self) -> Dict:
        """Compute reference statistics for drift detection"""
        stats = {}
        
        for column in self.reference_data.columns:
            if self.reference_data[column].dtype in ['float64', 'int64']:
                stats[column] = {
                    'mean': self.reference_data[column].mean(),
                    'std': self.reference_data[column].std(),
                    'min': self.reference_data[column].min(),
                    'max': self.reference_data[column].max(),
                    'quantiles': self.reference_data[column].quantile([0.25, 0.5, 0.75]).to_dict()
                }
            else:
                stats[column] = {
                    'categories': self.reference_data[column].value_counts().to_dict()
                }
        
        return stats
    
    def monitor_prediction(self, features: Dict, prediction: float, 
                          actual: Optional[bool] = None,
                          latency: float = None):
        """Monitor individual prediction"""
        
        # Record prediction metrics
        prediction_class = "fraud" if prediction > 0.5 else "legitimate"
        prediction_counter.labels(
            model_name=self.model_name,
            model_version=self.model_version,
            prediction_class=prediction_class
        ).inc()
        
        # Record latency
        if latency:
            prediction_latency.labels(
                model_name=self.model_name,
                model_version=self.model_version
            ).observe(latency)
        
        # Add to buffer for batch analysis
        self.prediction_buffer.append({
            'features': features,
            'prediction': prediction,
            'actual': actual,
            'timestamp': pd.Timestamp.now()
        })
        
        # Perform batch analysis every 100 predictions
        if len(self.prediction_buffer) >= 100:
            self._analyze_batch()
    
    def _analyze_batch(self):
        """Analyze batch of predictions for drift and performance"""
        
        # Convert buffer to DataFrame
        df = pd.DataFrame(self.prediction_buffer)
        features_df = pd.json_normalize(df['features'])
        
        # Check for data drift
        drift_scores = self._calculate_drift(features_df)
        
        for feature, score in drift_scores.items():
            feature_drift_gauge.labels(
                model_name=self.model_name,
                feature_name=feature
            ).set(score)
            
            if score > 0.3:
                self.logger.warning(
                    f"Data drift detected for feature {feature}: {score:.3f}"
                )
        
        # Calculate accuracy if we have actuals
        actuals = df['actual'].dropna()
        if len(actuals) > 0:
            predictions = df.loc[actuals.index, 'prediction'] > 0.5
            accuracy = (predictions == actuals).mean()
            
            model_accuracy_gauge.labels(
                model_name=self.model_name,
                model_version=self.model_version
            ).set(accuracy)
        
        # Clear buffer
        self.prediction_buffer = []
    
    def _calculate_drift(self, current_data: pd.DataFrame) -> Dict[str, float]:
        """Calculate drift scores for each feature"""
        drift_scores = {}
        
        for column in current_data.columns:
            if column not in self.reference_stats:
                continue
            
            if current_data[column].dtype in ['float64', 'int64']:
                # Use Kolmogorov-Smirnov test for numerical features
                _, p_value = stats.ks_2samp(
                    self.reference_data[column],
                    current_data[column]
                )
                drift_scores[column] = 1 - p_value
            else:
                # Use chi-squared test for categorical features
                ref_counts = self.reference_stats[column]['categories']
                curr_counts = current_data[column].value_counts()
                
                # Align categories
                all_categories = set(ref_counts.keys()) | set(curr_counts.keys())
                ref_freq = [ref_counts.get(cat, 0) for cat in all_categories]
                curr_freq = [curr_counts.get(cat, 0) for cat in all_categories]
                
                if sum(curr_freq) > 0:
                    _, p_value = stats.chisquare(curr_freq, ref_freq)
                    drift_scores[column] = 1 - p_value
                else:
                    drift_scores[column] = 0
        
        return drift_scores
    
    def generate_monitoring_report(self) -> Dict:
        """Generate comprehensive monitoring report"""
        
        # Get current metric values
        report = {
            'model_name': self.model_name,
            'model_version': self.model_version,
            'timestamp': pd.Timestamp.now().isoformat(),
            'metrics': {
                'total_predictions': len(self.prediction_buffer),
                'drift_alerts': [],
                'performance_metrics': {},
                'latency_stats': {}
            }
        }
        
        # Add drift information
        for feature in self.reference_stats:
            drift_score = feature_drift_gauge.labels(
                model_name=self.model_name,
                feature_name=feature
            )._value.get()
            
            if drift_score and drift_score > 0.3:
                report['metrics']['drift_alerts'].append({
                    'feature': feature,
                    'drift_score': drift_score,
                    'severity': 'high' if drift_score > 0.5 else 'medium'
                })
        
        return report
```

### Grafana Dashboard Configuration

```json
{
  "dashboard": {
    "title": "Payment ML Models Monitoring",
    "panels": [
      {
        "title": "Model Prediction Rate",
        "targets": [
          {
            "expr": "rate(model_predictions_total[5m])",
            "legendFormat": "{{ model_name }} - {{ model_version }}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Prediction Latency P99",
        "targets": [
          {
            "expr": "histogram_quantile(0.99, rate(model_prediction_duration_seconds_bucket[5m]))",
            "legendFormat": "{{ model_name }}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Feature Drift Scores",
        "targets": [
          {
            "expr": "model_feature_drift_score",
            "legendFormat": "{{ feature_name }}"
          }
        ],
        "type": "heatmap"
      },
      {
        "title": "Model Accuracy",
        "targets": [
          {
            "expr": "model_accuracy_score",
            "legendFormat": "{{ model_name }} v{{ model_version }}"
          }
        ],
        "type": "gauge",
        "options": {
          "min": 0,
          "max": 1,
          "thresholds": {
            "steps": [
              {"value": 0, "color": "red"},
              {"value": 0.9, "color": "yellow"},
              {"value": 0.95, "color": "green"}
            ]
          }
        }
      }
    ]
  }
}
```

## 7. Automated Retraining

### Retraining Pipeline

```python
# retraining/automated_retraining.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor
from datetime import datetime, timedelta
import json

default_args = {
    'owner': 'ml-platform',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'fraud_model_retraining',
    default_args=default_args,
    description='Automated retraining pipeline for fraud detection model',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    catchup=False
)

def check_retraining_criteria(**context):
    """Check if model needs retraining"""
    from monitoring.model_monitoring import ModelMonitor
    import mlflow
    
    # Get current production model metrics
    client = mlflow.tracking.MlflowClient()
    model_name = "payment-fraud-detector"
    production_model = client.get_latest_versions(model_name, stages=["Production"])[0]
    
    # Check performance metrics
    metrics = {
        'accuracy': float(production_model.tags.get('accuracy', 1.0)),
        'data_drift': float(production_model.tags.get('max_drift_score', 0)),
        'days_since_training': (datetime.now() - datetime.fromtimestamp(
            production_model.creation_timestamp/1000)).days
    }
    
    # Retraining criteria
    needs_retraining = (
        metrics['accuracy'] < 0.92 or
        metrics['data_drift'] > 0.4 or
        metrics['days_since_training'] > 30
    )
    
    context['task_instance'].xcom_push(
        key='needs_retraining',
        value=needs_retraining
    )
    context['task_instance'].xcom_push(
        key='retraining_reason',
        value=metrics
    )
    
    return needs_retraining

# Check retraining criteria
check_criteria = PythonOperator(
    task_id='check_retraining_criteria',
    python_callable=check_retraining_criteria,
    dag=dag
)

# Prepare training data
prepare_data = KubernetesPodOperator(
    task_id='prepare_training_data',
    name='prepare-training-data',
    namespace='payment-mlops',
    image='payment-mlops/feature-engineering:latest',
    cmds=['python'],
    arguments=[
        'prepare_training_data.py',
        '--start-date', '{{ ds }}',
        '--end-date', '{{ tomorrow_ds }}',
        '--output-path', 's3://payment-mlops/training-data/{{ ds }}'
    ],
    get_logs=True,
    is_delete_operator_pod=True,
    dag=dag
)

# Feature engineering with Spark
feature_engineering = KubernetesPodOperator(
    task_id='feature_engineering',
    name='feature-engineering-spark',
    namespace='payment-mlops',
    image='payment-mlops/spark-feature-engineering:latest',
    cmds=['spark-submit'],
    arguments=[
        '--master', 'k8s://https://kubernetes.default.svc:443',
        '--deploy-mode', 'cluster',
        '--name', 'feature-engineering-{{ ds }}',
        '--conf', 'spark.kubernetes.namespace=payment-mlops',
        '--conf', 'spark.kubernetes.driver.request.cores=2',
        '--conf', 'spark.kubernetes.executor.request.cores=4',
        '--conf', 'spark.kubernetes.executor.instances=5',
        '--conf', 'spark.kubernetes.container.image=payment-mlops/spark:3.4.0',
        's3://payment-mlops/jobs/feature_engineering.py',
        '--input-path', 's3://payment-mlops/training-data/{{ ds }}',
        '--output-path', 's3://payment-mlops/features/{{ ds }}'
    ],
    do_xcom_push=True,
    dag=dag
)

# Train model
train_model = KubernetesPodOperator(
    task_id='train_fraud_model',
    name='train-fraud-model',
    namespace='payment-mlops',
    image='payment-mlops/model-training:latest',
    cmds=['python'],
    arguments=[
        'train_model.py',
        '--features-path', 's3://payment-mlops/features/{{ ds }}',
        '--model-name', 'payment-fraud-detector',
        '--experiment-name', 'automated-retraining',
        '--hyperparameter-tuning', 'true'
    ],
    resources={
        'request_memory': '8Gi',
        'request_cpu': '4',
        'limit_memory': '16Gi',
        'limit_cpu': '8',
        'limit_gpu': '1'
    },
    node_selector={'workload': 'ml-training'},
    tolerations=[{
        'key': 'nvidia.com/gpu',
        'operator': 'Equal',
        'value': 'true',
        'effect': 'NoSchedule'
    }],
    get_logs=True,
    is_delete_operator_pod=True,
    dag=dag
)

# Validate model
validate_model = KubernetesPodOperator(
    task_id='validate_model',
    name='validate-model',
    namespace='payment-mlops',
    image='payment-mlops/model-validation:latest',
    cmds=['python'],
    arguments=[
        'validate_model.py',
        '--model-name', 'payment-fraud-detector',
        '--validation-dataset', 's3://payment-mlops/validation-data/latest',
        '--baseline-metrics-file', 's3://payment-mlops/baselines/fraud-detector.json'
    ],
    dag=dag
)

# Deploy to staging
deploy_staging = KubernetesPodOperator(
    task_id='deploy_to_staging',
    name='deploy-staging',
    namespace='payment-mlops',
    image='payment-mlops/model-deployment:latest',
    cmds=['python'],
    arguments=[
        'deploy_model.py',
        '--model-name', 'payment-fraud-detector',
        '--stage', 'staging',
        '--namespace', 'payment-staging',
        '--replicas', '2'
    ],
    dag=dag
)

# Run integration tests
integration_tests = KubernetesPodOperator(
    task_id='run_integration_tests',
    name='integration-tests',
    namespace='payment-mlops',
    image='payment-mlops/integration-tests:latest',
    cmds=['pytest'],
    arguments=[
        'tests/integration/',
        '--model-endpoint', 'http://fraud-detector.payment-staging:8080',
        '--junitxml=/tmp/test-results.xml'
    ],
    dag=dag
)

# Create A/B test
create_ab_test = PythonOperator(
    task_id='create_ab_test',
    python_callable=lambda **context: create_ab_test_config(context),
    dag=dag
)

def create_ab_test_config(context):
    """Create A/B test configuration"""
    from ab_testing.ab_test_controller import ABTestController, ABTestConfig
    
    controller = ABTestController()
    
    # Get model versions
    ti = context['task_instance']
    new_model_version = ti.xcom_pull(task_ids='train_fraud_model', key='model_version')
    
    config = ABTestConfig(
        test_id=f"fraud-model-{context['ds']}",
        model_a="production",
        model_b=new_model_version,
        traffic_split=0.05,  # 5% initial traffic
        success_metrics={
            "precision": 0.85,
            "recall": 0.80,
            "f1_score": 0.82
        },
        min_sample_size=10000,
        max_duration_days=7
    )
    
    test_id = controller.create_ab_test(config)
    ti.xcom_push(key='ab_test_id', value=test_id)

# Monitor A/B test
monitor_ab_test = PythonOperator(
    task_id='monitor_ab_test',
    python_callable=lambda **context: monitor_test_progress(context),
    dag=dag,
    trigger_rule='none_failed_or_skipped'
)

# Set up task dependencies
check_criteria >> prepare_data >> feature_engineering >> train_model
train_model >> validate_model >> deploy_staging >> integration_tests
integration_tests >> create_ab_test >> monitor_ab_test
```

### Hyperparameter Tuning

```python
# retraining/hyperparameter_tuning.py
import optuna
from optuna.integration import MLflowCallback
import xgboost as xgb
from sklearn.model_selection import cross_val_score
import numpy as np
import mlflow

class HyperparameterTuner:
    def __init__(self, X_train, y_train, model_name: str):
        self.X_train = X_train
        self.y_train = y_train
        self.model_name = model_name
        
    def objective(self, trial):
        """Optuna objective function for hyperparameter tuning"""
        
        # Suggest hyperparameters
        params = {
            'objective': 'binary:logistic',
            'eval_metric': 'auc',
            'max_depth': trial.suggest_int('max_depth', 3, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
            'subsample': trial.suggest_float('subsample', 0.6, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
            'gamma': trial.suggest_float('gamma', 0, 5),
            'reg_alpha': trial.suggest_float('reg_alpha', 0, 2),
            'reg_lambda': trial.suggest_float('reg_lambda', 0, 2),
            'scale_pos_weight': trial.suggest_float('scale_pos_weight', 1, 20),
            'use_label_encoder': False
        }
        
        # Create model
        model = xgb.XGBClassifier(**params, random_state=42)
        
        # Cross-validation
        scores = cross_val_score(
            model, self.X_train, self.y_train,
            cv=5, scoring='roc_auc', n_jobs=-1
        )
        
        return scores.mean()
    
    def tune(self, n_trials: int = 100):
        """Run hyperparameter tuning"""
        
        # Set up MLflow
        mlflow.set_experiment(f"{self.model_name}-hyperparameter-tuning")
        mlflc = MLflowCallback(
            tracking_uri=mlflow.get_tracking_uri(),
            metric_name="auc"
        )
        
        # Create study
        study = optuna.create_study(
            study_name=f"{self.model_name}-tuning",
            direction='maximize',
            storage='postgresql://optuna:password@postgres:5432/optuna',
            load_if_exists=True
        )
        
        # Optimize
        study.optimize(
            self.objective,
            n_trials=n_trials,
            callbacks=[mlflc],
            n_jobs=4
        )
        
        # Log best parameters
        with mlflow.start_run():
            mlflow.log_params(study.best_params)
            mlflow.log_metric("best_auc", study.best_value)
            
            # Train final model with best parameters
            best_model = xgb.XGBClassifier(
                **study.best_params,
                objective='binary:logistic',
                eval_metric='auc',
                use_label_encoder=False,
                random_state=42
            )
            
            best_model.fit(self.X_train, self.y_train)
            
            # Log model
            mlflow.xgboost.log_model(
                best_model,
                "model",
                registered_model_name=self.model_name
            )
            
        return study.best_params, best_model
```

## 8. CI/CD for ML Models

### GitLab CI/CD Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - train
  - validate
  - deploy

variables:
  DOCKER_REGISTRY: payment-mlops.azurecr.io
  MODEL_NAME: payment-fraud-detector
  MLFLOW_TRACKING_URI: http://mlflow.payment-mlops.svc.cluster.local:5000

# Test stage
unit-tests:
  stage: test
  image: python:3.9
  before_script:
    - pip install -r requirements-test.txt
  script:
    - pytest tests/unit/ -v --cov=src --cov-report=xml
    - python -m coverage report
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

data-validation:
  stage: test
  image: python:3.9
  script:
    - pip install great_expectations pandas
    - python scripts/validate_data.py --dataset $CI_COMMIT_SHA
  only:
    - merge_requests

# Build stage
build-training-image:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $DOCKER_REGISTRY/model-training:$CI_COMMIT_SHA -f docker/Dockerfile.training .
    - docker push $DOCKER_REGISTRY/model-training:$CI_COMMIT_SHA
  only:
    - main
    - develop

build-serving-image:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $DOCKER_REGISTRY/model-serving:$CI_COMMIT_SHA -f docker/Dockerfile.serving .
    - docker push $DOCKER_REGISTRY/model-serving:$CI_COMMIT_SHA
  only:
    - main
    - develop

# Train stage
train-model:
  stage: train
  image: $DOCKER_REGISTRY/model-training:$CI_COMMIT_SHA
  script:
    - |
      python train_model.py \
        --data-path s3://payment-mlops/training-data/latest \
        --model-name $MODEL_NAME \
        --git-commit $CI_COMMIT_SHA \
        --hyperparameter-tuning true
  artifacts:
    paths:
      - models/
      - metrics/
    expire_in: 30 days
  only:
    - main
    - develop

# Validate stage
validate-model:
  stage: validate
  image: $DOCKER_REGISTRY/model-training:$CI_COMMIT_SHA
  dependencies:
    - train-model
  script:
    - |
      python validate_model.py \
        --model-path models/model.pkl \
        --validation-data s3://payment-mlops/validation-data/latest \
        --baseline-metrics baselines/metrics.json
  artifacts:
    reports:
      junit: validation-report.xml

security-scan:
  stage: validate
  image: python:3.9
  script:
    - pip install bandit safety
    - bandit -r src/ -f json -o bandit-report.json
    - safety check --json > safety-report.json
  artifacts:
    paths:
      - bandit-report.json
      - safety-report.json

# Deploy stage
deploy-staging:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - |
      kubectl apply -f - <<EOF
      apiVersion: machinelearning.seldon.io/v1
      kind: SeldonDeployment
      metadata:
        name: $MODEL_NAME-staging
        namespace: payment-staging
      spec:
        name: $MODEL_NAME
        predictors:
        - graph:
            implementation: MLFLOW_SERVER
            modelUri: mlflow:$MODEL_NAME/Staging
            name: classifier
          name: default
          replicas: 2
      EOF
  environment:
    name: staging
    url: https://staging.payment-mlops.com
  only:
    - develop

deploy-production:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - |
      # Create A/B test deployment
      kubectl apply -f kubernetes/ab-deployment.yaml
      
      # Wait for rollout
      kubectl rollout status deployment/$MODEL_NAME-production -n payment-production
      
      # Run smoke tests
      python scripts/smoke_tests.py --endpoint https://api.payments.com/v1/predict
  environment:
    name: production
    url: https://api.payments.com
  when: manual
  only:
    - main
```

### Model Serving Dockerfile

```dockerfile
# docker/Dockerfile.serving
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements-serving.txt .
RUN pip install --no-cache-dir -r requirements-serving.txt

# Copy model serving code
COPY src/serving/ ./serving/
COPY src/monitoring/ ./monitoring/
COPY src/utils/ ./utils/

# Create non-root user
RUN useradd -m -u 1000 model-server && \
    chown -R model-server:model-server /app

USER model-server

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV MODEL_NAME=payment-fraud-detector
ENV MLFLOW_TRACKING_URI=http://mlflow:5000

# Expose ports
EXPOSE 8080 9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Run the server
CMD ["uvicorn", "serving.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]
```

## 9. Production Deployment Patterns

### Blue-Green Deployment

```yaml
# kubernetes/blue-green-deployment.yaml
apiVersion: v1
kind: Service
metadata:
  name: fraud-detector-service
  namespace: payment-production
spec:
  selector:
    app: fraud-detector
    version: active
  ports:
    - port: 80
      targetPort: 8080
      name: http
    - port: 9090
      targetPort: 9090
      name: metrics

---
# Blue deployment (current production)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fraud-detector-blue
  namespace: payment-production
  labels:
    app: fraud-detector
    version: blue
spec:
  replicas: 10
  selector:
    matchLabels:
      app: fraud-detector
      version: blue
  template:
    metadata:
      labels:
        app: fraud-detector
        version: blue
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: model-server
        image: payment-mlops.azurecr.io/fraud-detector:v2.0.1
        ports:
        - containerPort: 8080
          name: http
        - containerPort: 9090
          name: metrics
        env:
        - name: MODEL_VERSION
          value: "v2.0.1"
        - name: MLFLOW_TRACKING_URI
          valueFrom:
            secretKeyRef:
              name: mlflow-secret
              key: tracking-uri
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 20
          periodSeconds: 5

---
# Green deployment (new version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fraud-detector-green
  namespace: payment-production
  labels:
    app: fraud-detector
    version: green
spec:
  replicas: 10
  selector:
    matchLabels:
      app: fraud-detector
      version: green
  template:
    metadata:
      labels:
        app: fraud-detector
        version: green
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: model-server
        image: payment-mlops.azurecr.io/fraud-detector:v2.1.0
        ports:
        - containerPort: 8080
          name: http
        - containerPort: 9090
          name: metrics
        env:
        - name: MODEL_VERSION
          value: "v2.1.0"
        - name: MLFLOW_TRACKING_URI
          valueFrom:
            secretKeyRef:
              name: mlflow-secret
              key: tracking-uri
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 20
          periodSeconds: 5
```

### Traffic Switching Script

```python
# deployment/switch_traffic.py
import kubernetes
from kubernetes import client, config
import time
import requests
from typing import Dict
import logging

class BlueGreenDeployer:
    def __init__(self, namespace: str = "payment-production"):
        config.load_incluster_config()  # Use in-cluster config
        self.v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        self.namespace = namespace
        self.logger = logging.getLogger(__name__)
        
    def get_current_version(self) -> str:
        """Get currently active version (blue or green)"""
        service = self.v1.read_namespaced_service(
            name="fraud-detector-service",
            namespace=self.namespace
        )
        return service.spec.selector.get('version', 'blue')
    
    def validate_deployment(self, version: str) -> bool:
        """Validate deployment health before switching"""
        deployment_name = f"fraud-detector-{version}"
        
        # Check deployment status
        deployment = self.apps_v1.read_namespaced_deployment(
            name=deployment_name,
            namespace=self.namespace
        )
        
        if deployment.status.ready_replicas != deployment.spec.replicas:
            self.logger.error(f"Deployment {deployment_name} not fully ready")
            return False
        
        # Check endpoint health
        pods = self.v1.list_namespaced_pod(
            namespace=self.namespace,
            label_selector=f"app=fraud-detector,version={version}"
        )
        
        for pod in pods.items:
            if not self._check_pod_health(pod):
                return False
        
        return True
    
    def _check_pod_health(self, pod) -> bool:
        """Check individual pod health"""
        pod_ip = pod.status.pod_ip
        
        try:
            # Check health endpoint
            response = requests.get(
                f"http://{pod_ip}:8080/health",
                timeout=5
            )
            
            if response.status_code != 200:
                self.logger.error(f"Pod {pod.metadata.name} health check failed")
                return False
            
            # Check model loaded
            response = requests.get(
                f"http://{pod_ip}:8080/model/info",
                timeout=5
            )
            
            model_info = response.json()
            if not model_info.get('model_loaded'):
                self.logger.error(f"Pod {pod.metadata.name} model not loaded")
                return False
                
        except Exception as e:
            self.logger.error(f"Pod {pod.metadata.name} health check error: {e}")
            return False
        
        return True
    
    def switch_traffic(self, to_version: str, validation_period: int = 60):
        """Switch traffic to new version with validation"""
        
        current_version = self.get_current_version()
        
        if current_version == to_version:
            self.logger.info(f"Already on version {to_version}")
            return True
        
        # Validate new deployment
        if not self.validate_deployment(to_version):
            self.logger.error(f"Validation failed for {to_version}")
            return False
        
        # Update service selector
        service = self.v1.read_namespaced_service(
            name="fraud-detector-service",
            namespace=self.namespace
        )
        
        service.spec.selector['version'] = to_version
        
        self.v1.patch_namespaced_service(
            name="fraud-detector-service",
            namespace=self.namespace,
            body=service
        )
        
        self.logger.info(f"Switched traffic from {current_version} to {to_version}")
        
        # Monitor for validation period
        time.sleep(validation_period)
        
        # Check metrics
        if self._check_error_rates(to_version):
            self.logger.info("Deployment successful")
            
            # Scale down old version
            self._scale_deployment(f"fraud-detector-{current_version}", 0)
            
            return True
        else:
            self.logger.error("High error rate detected, rolling back")
            service.spec.selector['version'] = current_version
            self.v1.patch_namespaced_service(
                name="fraud-detector-service",
                namespace=self.namespace,
                body=service
            )
            return False
    
    def _check_error_rates(self, version: str) -> bool:
        """Check error rates from Prometheus"""
        # Query Prometheus for error rates
        query = f'rate(model_predictions_errors_total{{version="{version}"}}[5m])'
        
        # Simplified - in production, use proper Prometheus client
        # This is a placeholder for actual implementation
        error_rate = 0.001  # Mock value
        
        return error_rate < 0.01  # 1% error rate threshold
    
    def _scale_deployment(self, deployment_name: str, replicas: int):
        """Scale deployment to specified replicas"""
        body = {
            'spec': {
                'replicas': replicas
            }
        }
        
        self.apps_v1.patch_namespaced_deployment_scale(
            name=deployment_name,
            namespace=self.namespace,
            body=body
        )

# Usage
if __name__ == "__main__":
    deployer = BlueGreenDeployer()
    
    # Switch to green
    success = deployer.switch_traffic("green", validation_period=300)
    
    if success:
        print("Successfully deployed new version")
    else:
        print("Deployment failed, rolled back")
```

## 10. Cost Optimization

### Cost Tracking Implementation

```python
# cost_optimization/cost_tracker.py
import boto3
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List
import json

class MLOpsCostTracker:
    def __init__(self):
        self.ce_client = boto3.client('ce', region_name='us-east-1')
        self.cloudwatch = boto3.client('cloudwatch')
        
    def get_ml_costs(self, start_date: str, end_date: str) -> Dict:
        """Get ML-related costs from AWS Cost Explorer"""
        
        response = self.ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['BlendedCost', 'UsageQuantity'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                {'Type': 'TAG', 'Key': 'Environment'},
                {'Type': 'TAG', 'Key': 'Team'}
            ],
            Filter={
                'Tags': {
                    'Key': 'Project',
                    'Values': ['payment-mlops']
                }
            }
        )
        
        # Parse costs
        costs = {
            'total': 0,
            'by_service': {},
            'by_environment': {},
            'ml_specific': {
                'training': 0,
                'inference': 0,
                'storage': 0,
                'data_transfer': 0
            }
        }
        
        for result in response['ResultsByTime']:
            for group in result['Groups']:
                cost = float(group['Metrics']['BlendedCost']['Amount'])
                service = group['Keys'][0]
                
                costs['total'] += cost
                costs['by_service'][service] = costs['by_service'].get(service, 0) + cost
                
                # Categorize ML costs
                if 'SageMaker' in service or 'EC2' in service:
                    if 'training' in group['Keys'][2].lower():
                        costs['ml_specific']['training'] += cost
                    else:
                        costs['ml_specific']['inference'] += cost
                elif 'S3' in service:
                    costs['ml_specific']['storage'] += cost
                elif 'DataTransfer' in service:
                    costs['ml_specific']['data_transfer'] += cost
        
        return costs
    
    def calculate_cost_per_prediction(self) -> float:
        """Calculate cost per prediction"""
        
        # Get yesterday's costs
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')
        
        costs = self.get_ml_costs(yesterday, today)
        
        # Get prediction count from CloudWatch
        response = self.cloudwatch.get_metric_statistics(
            Namespace='PaymentMLOps',
            MetricName='PredictionCount',
            Dimensions=[
                {'Name': 'ModelName', 'Value': 'fraud-detector'}
            ],
            StartTime=datetime.now() - timedelta(days=1),
            EndTime=datetime.now(),
            Period=86400,
            Statistics=['Sum']
        )
        
        prediction_count = sum(point['Sum'] for point in response['Datapoints'])
        
        if prediction_count > 0:
            return costs['ml_specific']['inference'] / prediction_count
        return 0
    
    def optimize_instance_types(self) -> List[Dict]:
        """Recommend optimal instance types based on usage"""
        
        recommendations = []
        
        # Get current instance usage
        ec2 = boto3.client('ec2')
        
        instances = ec2.describe_instances(
            Filters=[
                {'Name': 'tag:Project', 'Values': ['payment-mlops']},
                {'Name': 'instance-state-name', 'Values': ['running']}
            ]
        )
        
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                
                # Get CPU utilization
                cpu_response = self.cloudwatch.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='CPUUtilization',
                    Dimensions=[
                        {'Name': 'InstanceId', 'Value': instance_id}
                    ],
                    StartTime=datetime.now() - timedelta(days=7),
                    EndTime=datetime.now(),
                    Period=3600,
                    Statistics=['Average']
                )
                
                avg_cpu = sum(point['Average'] for point in cpu_response['Datapoints']) / len(cpu_response['Datapoints'])
                
                # Recommend downsizing if underutilized
                if avg_cpu < 20:
                    current_cost = self._get_instance_cost(instance_type)
                    recommended_type = self._recommend_smaller_instance(instance_type)
                    new_cost = self._get_instance_cost(recommended_type)
                    
                    recommendations.append({
                        'instance_id': instance_id,
                        'current_type': instance_type,
                        'recommended_type': recommended_type,
                        'current_cost_hourly': current_cost,
                        'new_cost_hourly': new_cost,
                        'monthly_savings': (current_cost - new_cost) * 24 * 30,
                        'reason': f'Low CPU utilization: {avg_cpu:.1f}%'
                    })
        
        return recommendations
    
    def _get_instance_cost(self, instance_type: str) -> float:
        """Get hourly cost for instance type"""
        # Simplified - in production, use AWS Pricing API
        costs = {
            'ml.m5.xlarge': 0.23,
            'ml.m5.2xlarge': 0.46,
            'ml.p3.2xlarge': 3.06,
            'ml.g4dn.xlarge': 0.526,
            # Add more instance types
        }
        return costs.get(instance_type, 0)
    
    def _recommend_smaller_instance(self, current_type: str) -> str:
        """Recommend smaller instance type"""
        downsizing_map = {
            'ml.m5.2xlarge': 'ml.m5.xlarge',
            'ml.m5.4xlarge': 'ml.m5.2xlarge',
            'ml.p3.2xlarge': 'ml.g4dn.xlarge',
            # Add more mappings
        }
        return downsizing_map.get(current_type, current_type)
    
    def create_cost_dashboard(self):
        """Create cost optimization dashboard"""
        
        # Get last 30 days of costs
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        daily_costs = []
        
        for i in range(30):
            date = start_date + timedelta(days=i)
            costs = self.get_ml_costs(
                date.strftime('%Y-%m-%d'),
                (date + timedelta(days=1)).strftime('%Y-%m-%d')
            )
            
            daily_costs.append({
                'date': date,
                'total_cost': costs['total'],
                'training_cost': costs['ml_specific']['training'],
                'inference_cost': costs['ml_specific']['inference'],
                'storage_cost': costs['ml_specific']['storage']
            })
        
        # Create DataFrame
        df = pd.DataFrame(daily_costs)
        
        # Calculate metrics
        metrics = {
            'average_daily_cost': df['total_cost'].mean(),
            'total_monthly_cost': df['total_cost'].sum(),
            'cost_trend': 'increasing' if df['total_cost'].iloc[-7:].mean() > df['total_cost'].iloc[:7].mean() else 'decreasing',
            'highest_cost_component': max(costs['ml_specific'].items(), key=lambda x: x[1])[0],
            'cost_per_prediction': self.calculate_cost_per_prediction(),
            'optimization_opportunities': len(self.optimize_instance_types())
        }
        
        return {
            'daily_costs': df.to_dict('records'),
            'metrics': metrics,
            'recommendations': self.optimize_instance_types()
        }
```

### Spot Instance Management

```python
# cost_optimization/spot_instance_manager.py
import boto3
from kubernetes import client, config
import time
import logging

class SpotInstanceManager:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        config.load_incluster_config()
        self.k8s_v1 = client.CoreV1Api()
        self.logger = logging.getLogger(__name__)
        
    def request_spot_instances(self, instance_config: Dict) -> List[str]:
        """Request spot instances for ML training"""
        
        # Calculate bid price (80% of on-demand price)
        on_demand_price = self._get_on_demand_price(instance_config['instance_type'])
        max_price = str(on_demand_price * 0.8)
        
        # Create launch template
        launch_template = {
            'LaunchTemplateName': f"ml-training-{int(time.time())}",
            'LaunchTemplateData': {
                'ImageId': instance_config['ami_id'],
                'InstanceType': instance_config['instance_type'],
                'KeyName': instance_config.get('key_name'),
                'SecurityGroupIds': instance_config['security_groups'],
                'UserData': self._generate_user_data(instance_config),
                'BlockDeviceMappings': [
                    {
                        'DeviceName': '/dev/xvda',
                        'Ebs': {
                            'VolumeSize': instance_config.get('volume_size', 100),
                            'VolumeType': 'gp3',
                            'DeleteOnTermination': True
                        }
                    }
                ],
                'TagSpecifications': [
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {'Key': 'Name', 'Value': 'ml-training-spot'},
                            {'Key': 'Project', 'Value': 'payment-mlops'},
                            {'Key': 'Type', 'Value': 'spot-training'},
                            {'Key': 'ManagedBy', 'Value': 'mlops-platform'}
                        ]
                    }
                ]
            }
        }
        
        # Create launch template
        template_response = self.ec2.create_launch_template(**launch_template)
        template_id = template_response['LaunchTemplate']['LaunchTemplateId']
        
        # Request spot instances
        spot_request = {
            'SpotPrice': max_price,
            'InstanceCount': instance_config['count'],
            'Type': 'persistent',
            'LaunchSpecification': {
                'LaunchTemplate': {
                    'LaunchTemplateId': template_id,
                    'Version': '$Latest'
                }
            },
            'InstanceInterruptionBehavior': 'stop'
        }
        
        response = self.ec2.request_spot_instances(**spot_request)
        
        # Wait for fulfillment
        request_ids = [req['SpotInstanceRequestId'] for req in response['SpotInstanceRequests']]
        instance_ids = self._wait_for_fulfillment(request_ids)
        
        # Join instances to Kubernetes cluster
        self._join_k8s_cluster(instance_ids)
        
        return instance_ids
    
    def _generate_user_data(self, config: Dict) -> str:
        """Generate user data script for spot instances"""
        
        user_data = f"""#!/bin/bash
        # Install Docker
        apt-get update
        apt-get install -y docker.io
        
        # Install NVIDIA Docker for GPU instances
        if [[ "{config['instance_type']}" == p3* ]] || [[ "{config['instance_type']}" == g4* ]]; then
            distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
            curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -
            curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list
            apt-get update && apt-get install -y nvidia-docker2
            systemctl restart docker
        fi
        
        # Install Kubernetes components
        curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
        echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list
        apt-get update
        apt-get install -y kubelet kubeadm kubectl
        
        # Join cluster
        {config.get('join_command', '')}
        
        # Label node for ML workloads
        kubectl label node $(hostname) workload=ml-training-spot
        kubectl label node $(hostname) node.kubernetes.io/instance-type={config['instance_type']}
        
        # Setup termination handler
        cat > /usr/local/bin/spot-termination-handler.sh << 'EOF'
#!/bin/bash
while true; do
            if curl -s http://169.254.169.254/latest/meta-data/spot/termination-time | grep -q .; then
                echo "Spot instance termination notice detected"
                kubectl drain $(hostname) --ignore-daemonsets --delete-emptydir-data
                kubectl delete node $(hostname)
                break
            fi
            sleep 5
        done
        EOF
        
        chmod +x /usr/local/bin/spot-termination-handler.sh
        nohup /usr/local/bin/spot-termination-handler.sh &
        """
        
        return user_data
    
    def handle_spot_interruption(self, instance_id: str):
        """Handle spot instance interruption gracefully"""
        
        # Get node name
        node_name = self._get_node_name(instance_id)
        
        if node_name:
            # Cordon node to prevent new pods
            self.k8s_v1.patch_node(
                node_name,
                {'spec': {'unschedulable': True}}
            )
            
            # Get running pods
            pods = self.k8s_v1.list_pod_for_all_namespaces(
                field_selector=f"spec.nodeName={node_name}"
            )
            
            # Save training checkpoints
            for pod in pods.items:
                if 'ml-training' in pod.metadata.labels.get('job-type', ''):
                    self._save_training_checkpoint(pod)
            
            # Drain node
            self._drain_node(node_name)
            
            # Remove node from cluster
            self.k8s_v1.delete_node(node_name)
    
    def _save_training_checkpoint(self, pod):
        """Save training checkpoint before termination"""
        
        namespace = pod.metadata.namespace
        pod_name = pod.metadata.name
        
        # Execute checkpoint command in pod
        exec_command = [
            '/bin/sh',
            '-c',
            'kill -USR1 $(pgrep python)'  # Send signal to save checkpoint
        ]
        
        resp = stream(
            self.k8s_v1.connect_get_namespaced_pod_exec,
            pod_name,
            namespace,
            command=exec_command,
            stderr=True,
            stdin=False,
            stdout=True,
            tty=False
        )
        
        self.logger.info(f"Checkpoint saved for pod {pod_name}")
```

## Implementation Timeline

### Phase 1: Foundation (Month 1-2)
1. Set up Kubeflow on EKS
2. Implement Feast feature store
3. Create basic training pipeline
4. Set up MLflow tracking

### Phase 2: Automation (Month 2-3)
1. Implement automated retraining
2. Create A/B testing framework
3. Set up monitoring stack
4. Implement CI/CD pipelines

### Phase 3: Production (Month 3-4)
1. Deploy blue-green deployment
2. Implement cost optimization
3. Set up comprehensive monitoring
4. Create operational runbooks

## Success Metrics

| Metric | Current (25%) | Target (85%) | Measurement |
|--------|---------------|--------------|-------------|
| Model deployment frequency | Monthly | Daily | Deployments/day |
| Model training automation | Manual | Fully automated | % automated |
| Feature engineering time | 2 weeks | 2 hours | Time to production |
| Model monitoring coverage | Basic | Comprehensive | % metrics tracked |
| Experimentation velocity | 1/month | 10+/week | Experiments/week |
| Model rollback time | Hours | Minutes | MTTR |
| Cost per prediction | Unknown | <$0.001 | $/prediction |

## Conclusion

These MLOps implementation patterns provide a comprehensive foundation for achieving 85% maturity in machine learning operations for payment systems. The focus on automation, monitoring, and cost optimization ensures sustainable and scalable ML operations that meet 2025 industry standards.
# Cloud-Native Excellence Guide for Payment Systems - 2025 Standards

## Executive Summary

This guide provides production-ready implementation patterns to achieve Cloud-Native excellence (95% target) from the current level (60%). It focuses on GitOps workflows, Policy as Code, infrastructure automation, and cloud-native patterns required for modern payment systems.

## Table of Contents

1. [GitOps Implementation](#gitops-implementation)
2. [Policy as Code Framework](#policy-as-code-framework)
3. [Infrastructure as Code](#infrastructure-as-code)
4. [Service Mesh Excellence](#service-mesh-excellence)
5. [Observability Stack](#observability-stack)
6. [Progressive Delivery](#progressive-delivery)
7. [Multi-Cloud Architecture](#multi-cloud-architecture)
8. [Disaster Recovery Automation](#disaster-recovery-automation)
9. [Security Automation](#security-automation)
10. [Cost Governance](#cost-governance)

## 1. GitOps Implementation

### Repository Structure

```bash
# GitOps repository structure
payment-platform-gitops/
├── clusters/
│   ├── production/
│   │   ├── us-east-1/
│   │   │   ├── kustomization.yaml
│   │   │   ├── infrastructure/
│   │   │   ├── namespaces/
│   │   │   ├── helm-releases/
│   │   │   └── policies/
│   │   ├── eu-west-1/
│   │   └── ap-southeast-1/
│   ├── staging/
│   └── development/
├── infrastructure/
│   ├── terraform/
│   │   ├── modules/
│   │   ├── environments/
│   │   └── backend.tf
│   ├── crossplane/
│   │   ├── compositions/
│   │   └── providers/
│   └── pulumi/
├── applications/
│   ├── base/
│   │   ├── payment-gateway/
│   │   ├── fraud-detector/
│   │   ├── transaction-processor/
│   │   └── settlement-engine/
│   └── overlays/
│       ├── production/
│       ├── staging/
│       └── development/
├── platform/
│   ├── observability/
│   ├── service-mesh/
│   ├── security/
│   └── networking/
└── policies/
    ├── security/
    ├── compliance/
    ├── resource-limits/
    └── network/
```

### ArgoCD Configuration

```yaml
# argocd/argocd-cm.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  # Enable automated sync
  application.instanceLabelKey: argocd.argoproj.io/instance
  
  # Repository credentials
  repositories: |
    - url: https://github.com/payment-platform/gitops
      passwordSecret:
        name: github-secret
        key: password
      usernameSecret:
        name: github-secret
        key: username
    
  # Plugin configuration for advanced deployments
  configManagementPlugins: |
    - name: kustomized-helm
      init:
        command: ["/bin/sh", "-c"]
        args: ["helm dependency build"]
      generate:
        command: ["/bin/sh", "-c"]
        args: ["helm template $ARGOCD_APP_NAME . --include-crds | kustomize build"]
    
    - name: vault-secrets
      generate:
        command: ["sh", "-c"]
        args: ["vault-k8s-sync generate $ARGOCD_APP_NAME"]
  
  # Resource customizations
  resource.customizations: |
    argoproj.io/Rollout:
      health.lua: |
        hs = {}
        if obj.status ~= nil then
          if obj.status.phase == "Healthy" then
            hs.status = "Healthy"
          else
            hs.status = "Progressing"
          end
          hs.message = obj.status.message
        end
        return hs

---
# Application of Applications Pattern
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payment-platform
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: platform
  source:
    repoURL: https://github.com/payment-platform/gitops
    targetRevision: HEAD
    path: clusters/production/us-east-1
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  revisionHistoryLimit: 10
```

### Production Application Deployment

```yaml
# applications/production/payment-gateway.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payment-gateway-prod
  namespace: argocd
  annotations:
    notifications.argoproj.io/subscribe.on-sync-succeeded.slack: payments-team
    notifications.argoproj.io/subscribe.on-sync-failed.slack: payments-oncall
spec:
  project: payment-services
  source:
    repoURL: https://github.com/payment-platform/gitops
    path: applications/base/payment-gateway
    targetRevision: HEAD
    kustomize:
      images:
        - payment-platform/payment-gateway:v2.5.0
      patchesStrategicMerge:
        - |-
          apiVersion: apps/v1
          kind: Deployment
          metadata:
            name: payment-gateway
          spec:
            replicas: 20
            template:
              spec:
                containers:
                - name: payment-gateway
                  resources:
                    requests:
                      memory: "4Gi"
                      cpu: "2"
                    limits:
                      memory: "8Gi"
                      cpu: "4"
                  env:
                  - name: ENVIRONMENT
                    value: production
                  - name: LOG_LEVEL
                    value: info
                  - name: ENABLE_PROFILING
                    value: "true"
  destination:
    server: https://kubernetes.default.svc
    namespace: payment-system
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - PrunePropagationPolicy=foreground
    - Replace=false
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  # Health checks
  ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
    - /spec/replicas
  - group: autoscaling
    kind: HorizontalPodAutoscaler
    jsonPointers:
    - /spec/minReplicas
    - /spec/maxReplicas
```

### Automated Rollback Configuration

```yaml
# argocd/rollback-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rollback-config
  namespace: argocd
data:
  rollback.sh: |
    #!/bin/bash
    set -e
    
    APP_NAME=$1
    NAMESPACE=$2
    
    # Get current revision
    CURRENT_REVISION=$(argocd app get $APP_NAME -o json | jq -r .status.sync.revision)
    
    # Get previous successful revision
    PREVIOUS_REVISION=$(argocd app history $APP_NAME -o json | \
      jq -r '.[] | select(.deployedAt != null) | select(.revision != "'$CURRENT_REVISION'") | .revision' | \
      head -1)
    
    if [ -z "$PREVIOUS_REVISION" ]; then
      echo "No previous revision found"
      exit 1
    fi
    
    echo "Rolling back $APP_NAME from $CURRENT_REVISION to $PREVIOUS_REVISION"
    
    # Perform rollback
    argocd app rollback $APP_NAME $PREVIOUS_REVISION
    
    # Wait for sync
    argocd app wait $APP_NAME --health --timeout 300
    
    # Verify health
    kubectl rollout status deployment -n $NAMESPACE -l app=$APP_NAME
    
    # Send notification
    curl -X POST $SLACK_WEBHOOK_URL \
      -H 'Content-Type: application/json' \
      -d '{
        "text": "🔄 Rollback completed for '$APP_NAME' to revision '$PREVIOUS_REVISION'"
      }'

---
apiVersion: batch/v1
kind: Job
metadata:
  name: automated-rollback
  namespace: argocd
spec:
  template:
    spec:
      serviceAccountName: argocd-rollback
      containers:
      - name: rollback
        image: argoproj/argocd:v2.8.0
        command: ["/bin/bash"]
        args:
          - -c
          - |
            # Monitor application health
            while true; do
              APPS=$(argocd app list -o json | jq -r '.[] | select(.status.health.status == "Degraded") | .metadata.name')
              
              for app in $APPS; do
                echo "Detected degraded application: $app"
                
                # Check if it's a recent deployment (within 10 minutes)
                LAST_SYNC=$(argocd app get $app -o json | jq -r .status.operationState.finishedAt)
                LAST_SYNC_EPOCH=$(date -d "$LAST_SYNC" +%s)
                CURRENT_EPOCH=$(date +%s)
                DIFF=$((CURRENT_EPOCH - LAST_SYNC_EPOCH))
                
                if [ $DIFF -lt 600 ]; then
                  echo "Recent deployment detected, initiating rollback"
                  /scripts/rollback.sh $app payment-system
                fi
              done
              
              sleep 30
            done
        volumeMounts:
        - name: scripts
          mountPath: /scripts
        env:
        - name: SLACK_WEBHOOK_URL
          valueFrom:
            secretKeyRef:
              name: slack-secret
              key: webhook-url
      volumes:
      - name: scripts
        configMap:
          name: argocd-rollback-config
          defaultMode: 0755
```

## 2. Policy as Code Framework

### Open Policy Agent (OPA) Implementation

```yaml
# policies/opa/deployment-policies.rego
package kubernetes.admission

import future.keywords.contains
import future.keywords.if
import future.keywords.in

# Deny deployments without resource limits
deny[msg] {
    input.request.kind.kind == "Deployment"
    container := input.request.object.spec.template.spec.containers[_]
    not container.resources.limits.memory
    msg := sprintf("Container %v is missing memory limits", [container.name])
}

deny[msg] {
    input.request.kind.kind == "Deployment"
    container := input.request.object.spec.template.spec.containers[_]
    not container.resources.limits.cpu
    msg := sprintf("Container %v is missing CPU limits", [container.name])
}

# Enforce PCI compliance labels
deny[msg] {
    input.request.kind.kind in ["Deployment", "StatefulSet", "DaemonSet"]
    input.request.namespace == "payment-system"
    not input.request.object.metadata.labels["pci-compliance"]
    msg := "Payment system workloads must have pci-compliance label"
}

# Require encryption for PVCs
deny[msg] {
    input.request.kind.kind == "PersistentVolumeClaim"
    input.request.namespace == "payment-system"
    not input.request.object.spec.storageClassName == "encrypted-gp3"
    msg := "Payment system PVCs must use encrypted storage class"
}

# Enforce network policies
deny[msg] {
    input.request.kind.kind == "Deployment"
    input.request.namespace == "payment-system"
    not has_network_policy
    msg := "Payment system deployments must have associated NetworkPolicy"
}

has_network_policy {
    # Check if NetworkPolicy exists for this deployment
    np := data.kubernetes.networkpolicies[input.request.namespace][_]
    np.spec.podSelector.matchLabels.app == input.request.object.metadata.labels.app
}

# Enforce image signing
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not verified_image(container.image)
    msg := sprintf("Image %v is not signed by trusted authority", [container.image])
}

verified_image(image) {
    # Check against Cosign/Notary signatures
    signatures := data.image_signatures[image]
    signatures.verified == true
    signatures.signer in ["payment-platform-ci", "security-team"]
}

# Rate limiting for payment APIs
deny[msg] {
    input.request.kind.kind == "Ingress"
    input.request.object.metadata.annotations["kubernetes.io/ingress.class"] == "nginx"
    contains(input.request.object.spec.rules[_].host, "api.payments.com")
    not input.request.object.metadata.annotations["nginx.ingress.kubernetes.io/limit-rps"]
    msg := "Payment API ingresses must have rate limiting configured"
}

# Enforce mTLS for service-to-service
deny[msg] {
    input.request.kind.kind == "Service"
    input.request.namespace == "payment-system"
    input.request.object.metadata.labels["security.istio.io/tlsMode"] != "STRICT"
    msg := "Payment services must enforce STRICT mTLS"
}
```

### Kyverno Policy Examples

```yaml
# policies/kyverno/payment-policies.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: payment-system-policies
spec:
  validationFailureAction: enforce
  background: true
  rules:
    # Auto-inject sidecar containers
    - name: inject-security-sidecar
      match:
        any:
        - resources:
            kinds:
            - Deployment
            - StatefulSet
            namespaces:
            - payment-system
      mutate:
        patchStrategicMerge:
          spec:
            template:
              spec:
                containers:
                - name: security-sidecar
                  image: payment-platform/security-sidecar:latest
                  args:
                  - --mode=enforce
                  - --log-level=info
                  resources:
                    requests:
                      memory: "128Mi"
                      cpu: "100m"
                    limits:
                      memory: "256Mi"
                      cpu: "200m"
                  securityContext:
                    readOnlyRootFilesystem: true
                    runAsNonRoot: true
                    runAsUser: 1000
    
    # Enforce pod security standards
    - name: disallow-privileged
      match:
        any:
        - resources:
            kinds:
            - Pod
      validate:
        message: "Privileged containers are not allowed in payment system"
        pattern:
          spec:
            =(securityContext):
              =(privileged): "false"
            containers:
            - =(securityContext):
                =(privileged): "false"
    
    # Auto-generate NetworkPolicies
    - name: generate-network-policy
      match:
        any:
        - resources:
            kinds:
            - Deployment
            - StatefulSet
            namespaces:
            - payment-system
      generate:
        kind: NetworkPolicy
        name: "{{request.object.metadata.name}}-netpol"
        namespace: "{{request.object.metadata.namespace}}"
        data:
          spec:
            podSelector:
              matchLabels:
                app: "{{request.object.metadata.labels.app}}"
            policyTypes:
            - Ingress
            - Egress
            ingress:
            - from:
              - namespaceSelector:
                  matchLabels:
                    name: payment-system
              - podSelector:
                  matchLabels:
                    authorized: "true"
            egress:
            - to:
              - namespaceSelector:
                  matchLabels:
                    name: payment-system
            - to:
              - namespaceSelector:
                  matchLabels:
                    name: kube-system
                podSelector:
                  matchLabels:
                    k8s-app: kube-dns
              ports:
              - protocol: UDP
                port: 53
    
    # Enforce resource quotas
    - name: enforce-resource-limits
      match:
        any:
        - resources:
            kinds:
            - Deployment
            - StatefulSet
            namespaces:
            - payment-system
      validate:
        message: "Resource limits are required for payment workloads"
        pattern:
          spec:
            template:
              spec:
                containers:
                - name: "*"
                  resources:
                    limits:
                      memory: "?*"
                      cpu: "?*"
                    requests:
                      memory: "?*"
                      cpu: "?*"

---
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: payment-compliance-policies
spec:
  validationFailureAction: enforce
  background: false
  rules:
    # PCI DSS compliance
    - name: pci-encryption-in-transit
      match:
        any:
        - resources:
            kinds:
            - Service
            namespaces:
            - payment-system
      validate:
        message: "Services must use TLS for PCI compliance"
        pattern:
          metadata:
            annotations:
              service.beta.kubernetes.io/aws-load-balancer-ssl-cert: "?*"
    
    # Data residency compliance
    - name: enforce-data-residency
      match:
        any:
        - resources:
            kinds:
            - PersistentVolumeClaim
            namespaces:
            - payment-system
      validate:
        message: "Storage must be in compliant regions"
        pattern:
          spec:
            storageClassName: "encrypted-gp3-{{request.object.metadata.labels.region}}"
    
    # Audit logging requirement
    - name: require-audit-logging
      match:
        any:
        - resources:
            kinds:
            - Deployment
            namespaces:
            - payment-system
      mutate:
        patchStrategicMerge:
          metadata:
            annotations:
              fluentbit.io/parser: payment-audit
              audit.payments.com/enabled: "true"
```

### Falco Security Rules

```yaml
# policies/falco/payment-rules.yaml
- rule: Unauthorized Payment API Access
  desc: Detect unauthorized access to payment processing APIs
  condition: >
    spawned_process and container and
    (proc.name in (curl, wget, nc, ncat) and
     (proc.args contains "payment-api" or
      proc.args contains "transaction-processor" or
      proc.args contains "settlement-engine"))
  output: >
    Unauthorized payment API access attempt
    (user=%user.name container=%container.id image=%container.image.repository
     proc=%proc.cmdline connection=%fd.name)
  priority: CRITICAL
  tags: [payment, security, compliance]

- rule: Payment Data Exfiltration Attempt
  desc: Detect attempts to exfiltrate payment data
  condition: >
    open_write and container and
    (fd.name contains "/payment-data/" or
     fd.name contains "/transaction-logs/" or
     fd.name contains "/card-vault/") and
    (proc.name in (scp, rsync, sftp) or
     (proc.name = curl and proc.args contains "-X POST"))
  output: >
    Potential payment data exfiltration
    (user=%user.name file=%fd.name container=%container.id command=%proc.cmdline)
  priority: CRITICAL
  tags: [payment, data-loss, compliance]

- rule: Suspicious Database Access Pattern
  desc: Detect unusual database access patterns in payment system
  condition: >
    spawned_process and container and
    container.image.repository contains "payment" and
    proc.name in (psql, mysql, mongosh) and
    (proc.args contains "DELETE" or
     proc.args contains "DROP" or
     proc.args contains "TRUNCATE" or
     proc.args contains "--dump")
  output: >
    Suspicious database operation in payment system
    (user=%user.name container=%container.id operation=%proc.cmdline)
  priority: WARNING
  tags: [payment, database, security]

- rule: Payment Service Configuration Change
  desc: Detect unauthorized configuration changes
  condition: >
    open_write and container and
    container.image.repository contains "payment" and
    (fd.name pmatch "/etc/payment/*" or
     fd.name pmatch "/config/*" or
     fd.name contains "application.yaml")
  output: >
    Payment service configuration modified
    (user=%user.name file=%fd.name container=%container.id)
  priority: WARNING
  tags: [payment, configuration, compliance]

- rule: Cryptographic Key Access
  desc: Monitor access to cryptographic keys
  condition: >
    open_read and container and
    (fd.name contains "/keys/" or
     fd.name contains ".pem" or
     fd.name contains ".key" or
     fd.name contains "wallet.dat")
  output: >
    Cryptographic key accessed
    (user=%user.name file=%fd.name container=%container.id process=%proc.name)
  priority: INFO
  tags: [payment, crypto, security]
```

## 3. Infrastructure as Code

### Terraform Module for Payment Infrastructure

```hcl
# infrastructure/terraform/modules/payment-cluster/main.tf
terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = var.cluster_name
  cluster_version = var.kubernetes_version

  vpc_id     = var.vpc_id
  subnet_ids = var.private_subnet_ids

  # Encryption
  cluster_encryption_config = [{
    provider_key_arn = aws_kms_key.eks.arn
    resources        = ["secrets"]
  }]

  # Security groups
  cluster_security_group_additional_rules = {
    ingress_nodes_ephemeral_ports_tcp = {
      description                = "Nodes on ephemeral ports"
      protocol                   = "tcp"
      from_port                  = 1025
      to_port                    = 65535
      type                       = "ingress"
      source_node_security_group = true
    }
  }

  # Node groups
  eks_managed_node_groups = {
    # System nodes
    system = {
      name = "${var.cluster_name}-system"
      
      instance_types = ["m6i.xlarge"]
      
      min_size     = 3
      max_size     = 6
      desired_size = 3

      taints = [{
        key    = "CriticalAddonsOnly"
        value  = "true"
        effect = "NO_SCHEDULE"
      }]

      labels = {
        role = "system"
      }
    }

    # Payment processing nodes
    payment_processing = {
      name = "${var.cluster_name}-payment"
      
      instance_types = ["m6i.2xlarge", "m6i.4xlarge"]
      
      min_size     = 5
      max_size     = 50
      desired_size = 10

      labels = {
        role     = "payment-processing"
        workload = "critical"
      }

      block_device_mappings = {
        xvda = {
          device_name = "/dev/xvda"
          ebs = {
            volume_size           = 200
            volume_type           = "gp3"
            iops                  = 16000
            throughput            = 1000
            encrypted             = true
            delete_on_termination = true
          }
        }
      }
    }

    # ML inference nodes
    ml_inference = {
      name = "${var.cluster_name}-ml"
      
      instance_types = ["g4dn.xlarge", "g4dn.2xlarge"]
      
      min_size     = 2
      max_size     = 20
      desired_size = 5

      labels = {
        role     = "ml-inference"
        workload = "gpu"
      }

      taints = [{
        key    = "nvidia.com/gpu"
        value  = "true"
        effect = "NO_SCHEDULE"
      }]
    }
  }

  # IRSA roles
  enable_irsa = true

  # Add-ons
  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
      configuration_values = jsonencode({
        enableNetworkPolicy = "true"
        env = {
          ENABLE_PREFIX_DELEGATION = "true"
          WARM_PREFIX_TARGET       = "1"
        }
      })
    }
    aws-ebs-csi-driver = {
      most_recent = true
      service_account_role_arn = module.ebs_csi_irsa_role.iam_role_arn
    }
  }

  tags = merge(var.tags, {
    Environment = var.environment
    Compliance  = "PCI-DSS"
  })
}

# KMS key for encryption
resource "aws_kms_key" "eks" {
  description             = "EKS cluster encryption key"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  tags = var.tags
}

# IRSA for EBS CSI Driver
module "ebs_csi_irsa_role" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "~> 5.0"

  role_name = "${var.cluster_name}-ebs-csi"

  attach_ebs_csi_policy = true

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:ebs-csi-controller-sa"]
    }
  }
}

# VPC endpoints for private cluster
resource "aws_vpc_endpoint" "s3" {
  vpc_id       = var.vpc_id
  service_name = "com.amazonaws.${var.region}.s3"
  
  tags = merge(var.tags, {
    Name = "${var.cluster_name}-s3-endpoint"
  })
}

resource "aws_vpc_endpoint" "ecr_api" {
  vpc_id              = var.vpc_id
  service_name        = "com.amazonaws.${var.region}.ecr.api"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = var.private_subnet_ids
  security_group_ids  = [aws_security_group.vpc_endpoints.id]
  
  private_dns_enabled = true
  
  tags = merge(var.tags, {
    Name = "${var.cluster_name}-ecr-api-endpoint"
  })
}

# Security group for VPC endpoints
resource "aws_security_group" "vpc_endpoints" {
  name_prefix = "${var.cluster_name}-vpc-endpoints"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = var.tags
}
```

### Crossplane Compositions

```yaml
# infrastructure/crossplane/compositions/payment-database.yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: payment-database
  labels:
    provider: aws
    service: rds
spec:
  writeConnectionSecretsToNamespace: crossplane-system
  compositeTypeRef:
    apiVersion: payment.io/v1alpha1
    kind: PaymentDatabase
  
  resources:
    # RDS Instance
    - name: rds-instance
      base:
        apiVersion: rds.aws.crossplane.io/v1alpha1
        kind: DBInstance
        spec:
          forProvider:
            region: us-east-1
            engine: postgres
            engineVersion: "15.4"
            instanceClass: db.r6i.2xlarge
            allocatedStorage: 500
            storageType: gp3
            storageEncrypted: true
            multiAZ: true
            deletionProtection: true
            
            dbSubnetGroupNameSelector:
              matchControllerRef: true
            
            vpcSecurityGroupIDSelector:
              matchControllerRef: true
            
            masterUsername: dbadmin
            autoMinorVersionUpgrade: false
            backupRetentionPeriod: 30
            preferredBackupWindow: "03:00-04:00"
            preferredMaintenanceWindow: "sun:04:00-sun:05:00"
            
            enablePerformanceInsights: true
            performanceInsightsRetentionPeriod: 7
            
            enableCloudwatchLogsExports:
              - postgresql
      
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.region
        
        - type: FromCompositeFieldPath
          fromFieldPath: spec.instanceClass
          toFieldPath: spec.forProvider.instanceClass
        
        - type: FromCompositeFieldPath
          fromFieldPath: spec.storageSize
          toFieldPath: spec.forProvider.allocatedStorage
        
        - type: FromCompositeFieldPath
          fromFieldPath: metadata.uid
          toFieldPath: spec.writeConnectionSecretToRef.name
          transforms:
            - type: string
              string:
                fmt: "%s-rds-connection"
    
    # DB Subnet Group
    - name: db-subnet-group
      base:
        apiVersion: rds.aws.crossplane.io/v1alpha1
        kind: DBSubnetGroup
        spec:
          forProvider:
            region: us-east-1
            description: Payment database subnet group
            subnetIDSelector:
              matchLabels:
                type: private
                service: database
            tags:
              - key: Environment
                value: production
              - key: Service
                value: payment-database
      
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.region
    
    # Security Group
    - name: security-group
      base:
        apiVersion: ec2.aws.crossplane.io/v1beta1
        kind: SecurityGroup
        spec:
          forProvider:
            region: us-east-1
            vpcIdSelector:
              matchLabels:
                name: payment-vpc
            description: Security group for payment database
            ingress:
              - ipProtocol: tcp
                fromPort: 5432
                toPort: 5432
                ipRanges:
                  - cidrIp: 10.0.0.0/8
                    description: Allow from private network
      
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.region
    
    # Parameter Group
    - name: parameter-group
      base:
        apiVersion: rds.aws.crossplane.io/v1alpha1
        kind: DBParameterGroup
        spec:
          forProvider:
            region: us-east-1
            dbParameterGroupFamily: postgres15
            description: Payment database parameters
            parameters:
              - parameterName: shared_preload_libraries
                parameterValue: pg_stat_statements,pgaudit
              - parameterName: log_statement
                parameterValue: all
              - parameterName: log_min_duration_statement
                parameterValue: "1000"
              - parameterName: pgaudit.log
                parameterValue: "DDL,ROLE,FUNCTION"
      
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.region

---
# XRD Definition
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: paymentdatabases.payment.io
spec:
  group: payment.io
  names:
    kind: PaymentDatabase
    plural: paymentdatabases
  versions:
  - name: v1alpha1
    served: true
    referenceable: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              region:
                type: string
                description: AWS region for the database
              instanceClass:
                type: string
                description: RDS instance class
                default: db.r6i.xlarge
              storageSize:
                type: integer
                description: Storage size in GB
                default: 100
              highAvailability:
                type: boolean
                description: Enable Multi-AZ deployment
                default: true
            required:
              - region
```

### Pulumi Implementation

```typescript
// infrastructure/pulumi/payment-infrastructure.ts
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as k8s from "@pulumi/kubernetes";
import * as random from "@pulumi/random";

interface PaymentInfrastructureArgs {
    environment: string;
    region: string;
    vpcCidr: string;
    availabilityZones: string[];
    enableDnsHostnames?: boolean;
    enableDnsSupport?: boolean;
}

export class PaymentInfrastructure extends pulumi.ComponentResource {
    public readonly vpc: aws.ec2.Vpc;
    public readonly cluster: aws.eks.Cluster;
    public readonly nodeGroups: aws.eks.NodeGroup[];
    
    constructor(name: string, args: PaymentInfrastructureArgs, opts?: pulumi.ComponentResourceOptions) {
        super("payment:infrastructure:PaymentInfrastructure", name, {}, opts);
        
        // Create VPC with proper tagging for EKS
        this.vpc = new aws.ec2.Vpc(`${name}-vpc`, {
            cidrBlock: args.vpcCidr,
            enableDnsHostnames: args.enableDnsHostnames ?? true,
            enableDnsSupport: args.enableDnsSupport ?? true,
            tags: {
                Name: `${name}-vpc`,
                Environment: args.environment,
                "kubernetes.io/cluster/payment-cluster": "shared",
            },
        }, { parent: this });
        
        // Create subnets
        const publicSubnets: aws.ec2.Subnet[] = [];
        const privateSubnets: aws.ec2.Subnet[] = [];
        const databaseSubnets: aws.ec2.Subnet[] = [];
        
        for (let i = 0; i < args.availabilityZones.length; i++) {
            const az = args.availabilityZones[i];
            
            // Public subnet
            publicSubnets.push(new aws.ec2.Subnet(`${name}-public-${i}`, {
                vpcId: this.vpc.id,
                cidrBlock: `10.0.${i * 10}.0/24`,
                availabilityZone: az,
                mapPublicIpOnLaunch: true,
                tags: {
                    Name: `${name}-public-${i}`,
                    "kubernetes.io/role/elb": "1",
                    "kubernetes.io/cluster/payment-cluster": "shared",
                },
            }, { parent: this }));
            
            // Private subnet
            privateSubnets.push(new aws.ec2.Subnet(`${name}-private-${i}`, {
                vpcId: this.vpc.id,
                cidrBlock: `10.0.${i * 10 + 1}.0/24`,
                availabilityZone: az,
                tags: {
                    Name: `${name}-private-${i}`,
                    "kubernetes.io/role/internal-elb": "1",
                    "kubernetes.io/cluster/payment-cluster": "shared",
                },
            }, { parent: this }));
            
            // Database subnet
            databaseSubnets.push(new aws.ec2.Subnet(`${name}-database-${i}`, {
                vpcId: this.vpc.id,
                cidrBlock: `10.0.${i * 10 + 2}.0/24`,
                availabilityZone: az,
                tags: {
                    Name: `${name}-database-${i}`,
                    Type: "database",
                },
            }, { parent: this }));
        }
        
        // Internet Gateway
        const internetGateway = new aws.ec2.InternetGateway(`${name}-igw`, {
            vpcId: this.vpc.id,
            tags: {
                Name: `${name}-igw`,
            },
        }, { parent: this });
        
        // NAT Gateways for high availability
        const natGateways: aws.ec2.NatGateway[] = [];
        for (let i = 0; i < publicSubnets.length; i++) {
            const eip = new aws.ec2.Eip(`${name}-nat-eip-${i}`, {
                vpc: true,
                tags: {
                    Name: `${name}-nat-eip-${i}`,
                },
            }, { parent: this });
            
            natGateways.push(new aws.ec2.NatGateway(`${name}-nat-${i}`, {
                subnetId: publicSubnets[i].id,
                allocationId: eip.id,
                tags: {
                    Name: `${name}-nat-${i}`,
                },
            }, { parent: this }));
        }
        
        // Route tables
        const publicRouteTable = new aws.ec2.RouteTable(`${name}-public-rt`, {
            vpcId: this.vpc.id,
            routes: [{
                cidrBlock: "0.0.0.0/0",
                gatewayId: internetGateway.id,
            }],
            tags: {
                Name: `${name}-public-rt`,
            },
        }, { parent: this });
        
        // Associate public subnets with public route table
        publicSubnets.forEach((subnet, i) => {
            new aws.ec2.RouteTableAssociation(`${name}-public-rta-${i}`, {
                subnetId: subnet.id,
                routeTableId: publicRouteTable.id,
            }, { parent: this });
        });
        
        // Private route tables (one per AZ for HA)
        privateSubnets.forEach((subnet, i) => {
            const privateRouteTable = new aws.ec2.RouteTable(`${name}-private-rt-${i}`, {
                vpcId: this.vpc.id,
                routes: [{
                    cidrBlock: "0.0.0.0/0",
                    natGatewayId: natGateways[i].id,
                }],
                tags: {
                    Name: `${name}-private-rt-${i}`,
                },
            }, { parent: this });
            
            new aws.ec2.RouteTableAssociation(`${name}-private-rta-${i}`, {
                subnetId: subnet.id,
                routeTableId: privateRouteTable.id,
            }, { parent: this });
        });
        
        // EKS Cluster
        const eksRole = new aws.iam.Role(`${name}-eks-role`, {
            assumeRolePolicy: aws.iam.assumeRolePolicyForPrincipal({
                Service: "eks.amazonaws.com",
            }),
            managedPolicyArns: [
                "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy",
                "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController",
            ],
            tags: {
                Name: `${name}-eks-role`,
            },
        }, { parent: this });
        
        // KMS key for EKS encryption
        const eksKmsKey = new aws.kms.Key(`${name}-eks-key`, {
            description: "EKS cluster encryption key",
            enableKeyRotation: true,
            tags: {
                Name: `${name}-eks-key`,
            },
        }, { parent: this });
        
        this.cluster = new aws.eks.Cluster(`${name}-cluster`, {
            roleArn: eksRole.arn,
            vpcConfig: {
                subnetIds: [...publicSubnets, ...privateSubnets].map(s => s.id),
                endpointPrivateAccess: true,
                endpointPublicAccess: true,
                publicAccessCidrs: ["0.0.0.0/0"], // Restrict in production
            },
            encryptionConfig: {
                provider: {
                    keyArn: eksKmsKey.arn,
                },
                resources: ["secrets"],
            },
            enabledClusterLogTypes: [
                "api",
                "audit",
                "authenticator",
                "controllerManager",
                "scheduler",
            ],
            tags: {
                Name: `${name}-cluster`,
                Environment: args.environment,
            },
        }, { parent: this });
        
        // Node group IAM role
        const nodeGroupRole = new aws.iam.Role(`${name}-nodegroup-role`, {
            assumeRolePolicy: aws.iam.assumeRolePolicyForPrincipal({
                Service: "ec2.amazonaws.com",
            }),
            managedPolicyArns: [
                "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
                "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",
                "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
                "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore",
            ],
            tags: {
                Name: `${name}-nodegroup-role`,
            },
        }, { parent: this });
        
        // Node groups
        this.nodeGroups = [];
        
        // System node group
        this.nodeGroups.push(new aws.eks.NodeGroup(`${name}-system-nodes`, {
            clusterName: this.cluster.name,
            nodeRoleArn: nodeGroupRole.arn,
            subnetIds: privateSubnets.map(s => s.id),
            scalingConfig: {
                desiredSize: 3,
                maxSize: 6,
                minSize: 3,
            },
            instanceTypes: ["m6i.large"],
            labels: {
                role: "system",
                workload: "critical",
            },
            taints: [{
                effect: "NO_SCHEDULE",
                key: "CriticalAddonsOnly",
                value: "true",
            }],
            tags: {
                Name: `${name}-system-nodes`,
            },
        }, { parent: this }));
        
        // Payment processing nodes
        this.nodeGroups.push(new aws.eks.NodeGroup(`${name}-payment-nodes`, {
            clusterName: this.cluster.name,
            nodeRoleArn: nodeGroupRole.arn,
            subnetIds: privateSubnets.map(s => s.id),
            scalingConfig: {
                desiredSize: 10,
                maxSize: 50,
                minSize: 5,
            },
            instanceTypes: ["m6i.2xlarge", "m6i.4xlarge"],
            capacityType: "ON_DEMAND",
            labels: {
                role: "payment-processing",
                workload: "critical",
            },
            tags: {
                Name: `${name}-payment-nodes`,
            },
        }, { parent: this }));
        
        // ML inference nodes (with GPU)
        this.nodeGroups.push(new aws.eks.NodeGroup(`${name}-ml-nodes`, {
            clusterName: this.cluster.name,
            nodeRoleArn: nodeGroupRole.arn,
            subnetIds: privateSubnets.map(s => s.id),
            scalingConfig: {
                desiredSize: 3,
                maxSize: 10,
                minSize: 1,
            },
            instanceTypes: ["g4dn.xlarge"],
            amiType: "AL2_x86_64_GPU",
            labels: {
                role: "ml-inference",
                workload: "gpu",
            },
            taints: [{
                effect: "NO_SCHEDULE",
                key: "nvidia.com/gpu",
                value: "true",
            }],
            tags: {
                Name: `${name}-ml-nodes`,
            },
        }, { parent: this }));
        
        // Register outputs
        this.registerOutputs({
            vpcId: this.vpc.id,
            clusterEndpoint: this.cluster.endpoint,
            clusterName: this.cluster.name,
        });
    }
}

// Deployment
const paymentInfra = new PaymentInfrastructure("payment-prod", {
    environment: "production",
    region: "us-east-1",
    vpcCidr: "10.0.0.0/16",
    availabilityZones: ["us-east-1a", "us-east-1b", "us-east-1c"],
});

export const clusterName = paymentInfra.cluster.name;
export const clusterEndpoint = paymentInfra.cluster.endpoint;
```

## 4. Service Mesh Excellence

### Istio Configuration

```yaml
# service-mesh/istio/control-plane.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: payment-platform-istio
spec:
  profile: production
  
  meshConfig:
    accessLogFile: /dev/stdout
    accessLogFormat: |
      [%START_TIME%] "%REQ(:METHOD)% %REQ(X-ENVOY-ORIGINAL-PATH?:PATH)% %PROTOCOL%" %RESPONSE_CODE% %RESPONSE_FLAGS% %RESPONSE_CODE_DETAILS% %CONNECTION_TERMINATION_DETAILS% "%UPSTREAM_TRANSPORT_FAILURE_REASON%" %BYTES_RECEIVED% %BYTES_SENT% %DURATION% %RESP(X-ENVOY-UPSTREAM-SERVICE-TIME)% "%REQ(X-FORWARDED-FOR)%" "%REQ(USER-AGENT)%" "%REQ(X-REQUEST-ID)%" "%REQ(:AUTHORITY)%" "%UPSTREAM_HOST%" %DOWNSTREAM_REMOTE_ADDRESS% %DOWNSTREAM_LOCAL_ADDRESS% %DOWNSTREAM_LOCAL_URI_SAN% %ROUTE_NAME%
    
    defaultConfig:
      proxyStatsMatcher:
        inclusionRegexps:
        - ".*outlier_detection.*"
        - ".*circuit_breakers.*"
        - ".*upstream_rq_retry.*"
        - ".*upstream_rq_pending.*"
        - ".*payment.*"
      
      # Enable distributed tracing
      tracing:
        sampling: 100.0
        custom_tags:
          environment:
            literal:
              value: "production"
          service.version:
            environment:
              name: SERVICE_VERSION
      
      # Outlier detection defaults
      outlierDetection:
        consecutiveErrors: 5
        interval: 30s
        baseEjectionTime: 30s
        maxEjectionPercent: 50
    
    # mTLS configuration
    defaultProviders:
      metrics:
      - prometheus
      tracing:
      - jaeger
    
    extensionProviders:
    - name: prometheus
      prometheus:
        configOverride:
          inboundSidecar:
            disable_host_header_fallback: true
          outboundSidecar:
            disable_host_header_fallback: true
    
    - name: jaeger
      jaeger:
        service: jaeger-collector.istio-system.svc.cluster.local
        port: 14268
        maxTagLength: 256
    
    # Enable mTLS by default
    mtls:
      mode: STRICT
  
  components:
    pilot:
      k8s:
        resources:
          requests:
            cpu: 1000m
            memory: 2Gi
          limits:
            cpu: 2000m
            memory: 4Gi
        
        hpaSpec:
          minReplicas: 2
          maxReplicas: 5
          metrics:
          - type: Resource
            resource:
              name: cpu
              targetAverageUtilization: 60
        
        nodeSelector:
          role: system
        
        tolerations:
        - key: CriticalAddonsOnly
          operator: Exists
          effect: NoSchedule
    
    ingressGateways:
    - name: istio-ingressgateway
      enabled: true
      k8s:
        resources:
          requests:
            cpu: 1000m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 2Gi
        
        hpaSpec:
          minReplicas: 3
          maxReplicas: 10
        
        service:
          type: LoadBalancer
          loadBalancerIP: ""
          loadBalancerSourceRanges: []
          ports:
          - port: 15021
            targetPort: 15021
            name: status-port
          - port: 80
            targetPort: 8080
            name: http2
          - port: 443
            targetPort: 8443
            name: https
          - port: 31400
            targetPort: 31400
            name: tcp
            
        serviceAnnotations:
          service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
          service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
          service.beta.kubernetes.io/aws-load-balancer-backend-protocol: "tcp"
          service.beta.kubernetes.io/aws-load-balancer-proxy-protocol: "*"
    
    egressGateways:
    - name: istio-egressgateway
      enabled: true
      k8s:
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi
  
  values:
    global:
      proxy:
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 200m
            memory: 256Mi
      
      # Enable auto mTLS
      mtls:
        enabled: true
        auto: true
```

### Payment Service Mesh Policies

```yaml
# service-mesh/istio/payment-policies.yaml
# Strict mTLS for payment namespace
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: payment-mtls
  namespace: payment-system
spec:
  mtls:
    mode: STRICT

---
# Authorization policy for payment services
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: payment-authz
  namespace: payment-system
spec:
  action: ALLOW
  rules:
  - from:
    - source:
        namespaces: ["payment-system", "payment-gateway"]
    to:
    - operation:
        methods: ["GET", "POST", "PUT", "DELETE"]
  - from:
    - source:
        principals: ["cluster.local/ns/istio-system/sa/istio-ingressgateway-service-account"]
    to:
    - operation:
        paths: ["/api/v1/*", "/health", "/metrics"]

---
# Rate limiting for payment APIs
apiVersion: networking.istio.io/v1beta1
kind: EnvoyFilter
metadata:
  name: payment-rate-limit
  namespace: payment-system
spec:
  configPatches:
  - applyTo: HTTP_FILTER
    match:
      context: SIDECAR_INBOUND
      listener:
        filterChain:
          filter:
            name: "envoy.filters.network.http_connection_manager"
    patch:
      operation: INSERT_BEFORE
      value:
        name: envoy.filters.http.local_ratelimit
        typed_config:
          "@type": type.googleapis.com/udpa.type.v1.TypedStruct
          type_url: type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
          value:
            stat_prefix: payment_rate_limiter
            token_bucket:
              max_tokens: 1000
              tokens_per_fill: 100
              fill_interval: 1s
            filter_enabled:
              runtime_key: local_rate_limit_enabled
              default_value:
                numerator: 100
                denominator: HUNDRED
            filter_enforced:
              runtime_key: local_rate_limit_enforced
              default_value:
                numerator: 100
                denominator: HUNDRED

---
# Circuit breaker for payment services
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: payment-circuit-breaker
  namespace: payment-system
spec:
  host: "*.payment-system.svc.cluster.local"
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: DO_NOT_UPGRADE
        http1MaxPendingRequests: 100
        http2MaxRequests: 100
        maxRequestsPerConnection: 1
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 30
      splitExternalLocalOriginErrors: true
    retryPolicy:
      attempts: 3
      perTryTimeout: 5s
      retryOn: "5xx,reset,connect-failure,refused-stream"
      retryRemoteLocalities: true

---
# Virtual service for canary deployments
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: payment-gateway
  namespace: payment-system
spec:
  hosts:
  - payment-gateway
  http:
  - match:
    - headers:
        x-canary:
          exact: "true"
    route:
    - destination:
        host: payment-gateway
        subset: canary
      weight: 100
  - route:
    - destination:
        host: payment-gateway
        subset: stable
      weight: 95
    - destination:
        host: payment-gateway
        subset: canary
      weight: 5

---
# Destination rules for subsets
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: payment-gateway
  namespace: payment-system
spec:
  host: payment-gateway
  subsets:
  - name: stable
    labels:
      version: stable
  - name: canary
    labels:
      version: canary
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL
```

## 5. Observability Stack

### Prometheus Configuration

```yaml
# observability/prometheus/values.yaml
prometheus:
  prometheusSpec:
    retention: 30d
    retentionSize: "100GB"
    
    resources:
      requests:
        cpu: 2
        memory: 8Gi
      limits:
        cpu: 4
        memory: 16Gi
    
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: gp3-encrypted
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 500Gi
    
    # Service monitors for payment services
    serviceMonitorSelector:
      matchLabels:
        prometheus: payment-platform
    
    # Pod monitors for payment pods
    podMonitorSelector:
      matchLabels:
        prometheus: payment-platform
    
    # Additional scrape configs
    additionalScrapeConfigs:
    - job_name: 'payment-services'
      kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
          - payment-system
          - payment-gateway
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
    
    # Recording rules
    additionalPrometheusRulesMap:
      payment-rules:
        groups:
        - name: payment_performance
          interval: 30s
          rules:
          - record: payment:request_rate
            expr: |
              sum by (service, method) (
                rate(http_server_requests_seconds_count{namespace="payment-system"}[5m])
              )
          
          - record: payment:error_rate
            expr: |
              sum by (service, method) (
                rate(http_server_requests_seconds_count{namespace="payment-system",status=~"5.."}[5m])
              ) / 
              sum by (service, method) (
                rate(http_server_requests_seconds_count{namespace="payment-system"}[5m])
              )
          
          - record: payment:latency_p99
            expr: |
              histogram_quantile(0.99,
                sum by (service, method, le) (
                  rate(http_server_requests_seconds_bucket{namespace="payment-system"}[5m])
                )
              )
```

### Grafana Dashboards

```json
{
  "dashboard": {
    "title": "Payment System Overview",
    "panels": [
      {
        "title": "Transaction Volume",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
        "targets": [
          {
            "expr": "sum(rate(payment_transactions_total[5m])) by (type)",
            "legendFormat": "{{ type }}"
          }
        ],
        "type": "graph",
        "yaxes": [{"format": "ops", "label": "Transactions/sec"}]
      },
      {
        "title": "Transaction Success Rate",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
        "targets": [
          {
            "expr": "sum(rate(payment_transactions_total{status=\"success\"}[5m])) / sum(rate(payment_transactions_total[5m])) * 100"
          }
        ],
        "type": "gauge",
        "options": {
          "min": 0,
          "max": 100,
          "thresholds": {
            "steps": [
              {"value": 0, "color": "red"},
              {"value": 95, "color": "yellow"},
              {"value": 99, "color": "green"}
            ]
          }
        }
      },
      {
        "title": "API Latency (P99)",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
        "targets": [
          {
            "expr": "payment:latency_p99",
            "legendFormat": "{{ service }} - {{ method }}"
          }
        ],
        "type": "graph",
        "yaxes": [{"format": "s", "label": "Latency"}]
      },
      {
        "title": "Error Rate by Service",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8},
        "targets": [
          {
            "expr": "payment:error_rate * 100",
            "legendFormat": "{{ service }}"
          }
        ],
        "type": "graph",
        "yaxes": [{"format": "percent", "label": "Error Rate"}]
      },
      {
        "title": "Fraud Detection Performance",
        "gridPos": {"h": 8, "w": 24, "x": 0, "y": 16},
        "targets": [
          {
            "expr": "rate(fraud_detections_total[5m])",
            "legendFormat": "Detections"
          },
          {
            "expr": "rate(fraud_false_positives_total[5m])",
            "legendFormat": "False Positives"
          }
        ],
        "type": "graph"
      }
    ],
    "refresh": "5s",
    "time": {"from": "now-1h", "to": "now"},
    "timepicker": {
      "refresh_intervals": ["5s", "10s", "30s", "1m", "5m"]
    }
  }
}
```

### Distributed Tracing with Jaeger

```yaml
# observability/jaeger/production-config.yaml
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: payment-platform
  namespace: observability
spec:
  strategy: production
  
  ingress:
    enabled: true
    annotations:
      nginx.ingress.kubernetes.io/ssl-redirect: "true"
    hosts:
    - jaeger.payments.internal
  
  storage:
    type: elasticsearch
    options:
      es:
        server-urls: https://elasticsearch.observability.svc:9200
        tls:
          enabled: true
          ca-cert: /es-certs/ca.crt
        index-prefix: payment-traces
        tags-as-fields:
          all: true
        
    esIndexCleaner:
      enabled: true
      numberOfDays: 7
      schedule: "0 0 * * *"
    
    dependencies:
      enabled: true
      schedule: "0 */6 * * *"
  
  collector:
    replicas: 3
    maxReplicas: 10
    
    resources:
      requests:
        cpu: 500m
        memory: 1Gi
      limits:
        cpu: 1
        memory: 2Gi
    
    options:
      collector:
        queue-size: 5000
        num-workers: 100
      
      kafka:
        producer:
          topic: payment-traces
          brokers: kafka-bootstrap.kafka:9092
          encoding: protobuf
          required-acks: 1
    
    autoscale: true
    
    nodeSelector:
      workload: monitoring
  
  query:
    replicas: 2
    
    resources:
      requests:
        cpu: 250m
        memory: 512Mi
      limits:
        cpu: 500m
        memory: 1Gi
    
    options:
      query:
        base-path: /jaeger
        
    serviceMonitor:
      enabled: true
      labels:
        prometheus: payment-platform
  
  agent:
    strategy: DaemonSet
    
    hostNetwork: true
    
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 200m
        memory: 256Mi
    
    options:
      reporter:
        grpc:
          host-port: jaeger-collector.observability.svc:14250
      processor:
        jaeger-compact:
          server-queue-size: 1000
```

## 6. Progressive Delivery

### Flagger Configuration

```yaml
# progressive-delivery/flagger/payment-canary.yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: payment-gateway
  namespace: payment-system
spec:
  # Target reference
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: payment-gateway
  
  # Progressive delivery configuration
  progressDeadlineSeconds: 600
  
  # HPA reference
  autoscalerRef:
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    name: payment-gateway
  
  # Service configuration
  service:
    port: 8080
    targetPort: 8080
    gateways:
    - public-gateway.istio-system.svc.cluster.local
    hosts:
    - api.payments.com
    
    # Traffic management
    trafficPolicy:
      tls:
        mode: ISTIO_MUTUAL
    
    # Retry policy
    retries:
      attempts: 3
      perTryTimeout: 5s
      retryOn: "gateway-error,connect-failure,refused-stream"
  
  # Analysis configuration
  analysis:
    # Promotion interval
    interval: 1m
    
    # Max number of failed checks
    threshold: 5
    
    # Max traffic percentage
    maxWeight: 50
    
    # Canary increment step
    stepWeight: 5
    
    # Metrics to evaluate
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 30s
    
    - name: fraud-detection-accuracy
      templateRef:
        name: fraud-detection-accuracy
        namespace: payment-system
      thresholdRange:
        min: 95
    
    # Load testing
    webhooks:
    - name: load-test
      type: pre-rollout
      url: http://flagger-loadtester.payment-system/
      timeout: 5m
      metadata:
        cmd: "hey -z 2m -q 100 -c 10 -m POST -d '{\"amount\":100}' http://payment-gateway-canary.payment-system:8080/api/v1/transaction"
    
    - name: acceptance-test
      type: pre-rollout
      url: http://flagger-loadtester.payment-system/
      timeout: 3m
      metadata:
        type: bash
        cmd: "curl -X POST http://payment-gateway-canary.payment-system:8080/api/v1/test | grep 'success'"
    
    # Alerts
    alerts:
    - name: "payment-gateway deployment"
      severity: info
      providerRef:
        name: slack
        namespace: flagger-system

---
# Custom metric template
apiVersion: flagger.app/v1beta1
kind: MetricTemplate
metadata:
  name: fraud-detection-accuracy
  namespace: payment-system
spec:
  provider:
    type: prometheus
    address: http://prometheus.observability:9090
  query: |
    (
      sum(
        rate(
          fraud_detections_correct_total{
            namespace="{{ namespace }}",
            deployment=~"{{ target }}"
          }[{{ interval }}]
        )
      ) / 
      sum(
        rate(
          fraud_detections_total{
            namespace="{{ namespace }}",
            deployment=~"{{ target }}"
          }[{{ interval }}]
        )
      )
    ) * 100

---
# Alert provider
apiVersion: v1
kind: Secret
metadata:
  name: slack
  namespace: flagger-system
stringData:
  address: https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK

---
apiVersion: flagger.app/v1beta1
kind: AlertProvider
metadata:
  name: slack
  namespace: flagger-system
spec:
  type: slack
  secretRef:
    name: slack
  channel: payment-deployments
```

### Blue-Green Deployment with Flagger

```yaml
# progressive-delivery/flagger/blue-green.yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: settlement-engine
  namespace: payment-system
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: settlement-engine
  
  # Blue-green specific configuration
  skipAnalysis: false
  
  service:
    port: 8080
    targetPort: 8080
    portDiscovery: true
  
  # Blue-green analysis
  analysis:
    interval: 1m
    threshold: 3
    iterations: 10
    
    # Switch all traffic at once
    canaryAnalysis:
      maxWeight: 0
      stepWeight: 0
    
    # Promote to blue-green
    blueGreen:
      # Pre-promotion active service label
      activeService: settlement-engine-active
      
      # Preview service
      previewService: settlement-engine-preview
      
      # Scale down old version after promotion
      scaleDownDelaySeconds: 300
      
      # Anti-affinity to spread blue/green
      antiAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
          topologyKey: kubernetes.io/hostname
    
    metrics:
    - name: settlement-accuracy
      templateRef:
        name: settlement-accuracy-metric
      thresholdRange:
        min: 99.9
    
    - name: reconciliation-success
      query: |
        sum(
          rate(
            settlement_reconciliation_success_total{
              namespace="{{ namespace }}",
              pod=~"{{ target }}-[0-9a-zA-Z]+(-[0-9a-zA-Z]+)"
            }[{{ interval }}]
          )
        ) / 
        sum(
          rate(
            settlement_reconciliation_total{
              namespace="{{ namespace }}",
              pod=~"{{ target }}-[0-9a-zA-Z]+(-[0-9a-zA-Z]+)"
            }[{{ interval }}]
          )
        ) * 100
      thresholdRange:
        min: 100
```

## 7. Multi-Cloud Architecture

### Crossplane Multi-Cloud Composition

```yaml
# multi-cloud/crossplane/multi-cloud-database.yaml
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: multicloudatabases.payment.io
spec:
  group: payment.io
  names:
    kind: MultiCloudDatabase
    plural: multicloudatabases
  versions:
  - name: v1alpha1
    served: true
    referenceable: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              providers:
                type: array
                items:
                  type: string
                  enum: ["aws", "gcp", "azure"]
              primaryRegion:
                type: string
              replicaRegions:
                type: array
                items:
                  type: string
              size:
                type: string
                enum: ["small", "medium", "large", "xlarge"]

---
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: multicloud-database-composition
spec:
  compositeTypeRef:
    apiVersion: payment.io/v1alpha1
    kind: MultiCloudDatabase
  
  patchSets:
  - name: common-fields
    patches:
    - type: FromCompositeFieldPath
      fromFieldPath: metadata.labels
      toFieldPath: metadata.labels
    - type: FromCompositeFieldPath
      fromFieldPath: metadata.annotations
      toFieldPath: metadata.annotations
  
  resources:
  # AWS RDS Instance
  - name: aws-primary
    base:
      apiVersion: database.aws.crossplane.io/v1beta1
      kind: RDSInstance
      spec:
        forProvider:
          engine: postgres
          engineVersion: "15"
          dbInstanceClass: db.r6i.xlarge
          allocatedStorage: 100
          storageEncrypted: true
          multiAZ: true
    
    patches:
    - type: PatchSet
      patchSetName: common-fields
    
    - type: FromCompositeFieldPath
      fromFieldPath: spec.primaryRegion
      toFieldPath: spec.forProvider.region
      transforms:
      - type: map
        map:
          us: us-east-1
          eu: eu-west-1
          asia: ap-southeast-1
    
    - type: FromCompositeFieldPath
      fromFieldPath: spec.size
      toFieldPath: spec.forProvider.dbInstanceClass
      transforms:
      - type: map
        map:
          small: db.r6i.large
          medium: db.r6i.xlarge
          large: db.r6i.2xlarge
          xlarge: db.r6i.4xlarge
  
  # GCP Cloud SQL Instance
  - name: gcp-replica
    base:
      apiVersion: database.gcp.crossplane.io/v1beta1
      kind: CloudSQLInstance
      spec:
        forProvider:
          databaseVersion: POSTGRES_15
          settings:
            tier: db-standard-4
            diskSize: 100
            diskType: PD_SSD
            availabilityType: REGIONAL
            backupConfiguration:
              enabled: true
              startTime: "03:00"
            ipConfiguration:
              requireSsl: true
              privateNetwork: projects/payment-platform/global/networks/payment-vpc
    
    patches:
    - type: PatchSet
      patchSetName: common-fields
    
    - type: FromCompositeFieldPath
      fromFieldPath: spec.replicaRegions[0]
      toFieldPath: spec.forProvider.region
      transforms:
      - type: map
        map:
          us: us-central1
          eu: europe-west1
          asia: asia-southeast1
    
    - type: FromCompositeFieldPath
      fromFieldPath: spec.size
      toFieldPath: spec.forProvider.settings.tier
      transforms:
      - type: map
        map:
          small: db-standard-2
          medium: db-standard-4
          large: db-standard-8
          xlarge: db-standard-16
  
  # Azure Database for PostgreSQL
  - name: azure-replica
    base:
      apiVersion: database.azure.crossplane.io/v1beta1
      kind: PostgreSQLServer
      spec:
        forProvider:
          location: East US
          version: "15"
          sslEnforcement: Enabled
          sku:
            tier: GeneralPurpose
            capacity: 4
            family: Gen5
          storageProfile:
            storageMB: 102400
            backupRetentionDays: 30
            geoRedundantBackup: Enabled
    
    patches:
    - type: PatchSet
      patchSetName: common-fields
    
    - type: FromCompositeFieldPath
      fromFieldPath: spec.replicaRegions[1]
      toFieldPath: spec.forProvider.location
      transforms:
      - type: map
        map:
          us: East US
          eu: West Europe
          asia: Southeast Asia
    
    - type: FromCompositeFieldPath
      fromFieldPath: spec.size
      toFieldPath: spec.forProvider.sku.capacity
      transforms:
      - type: map
        map:
          small: 2
          medium: 4
          large: 8
          xlarge: 16
```

### Multi-Cloud Service Mesh

```yaml
# multi-cloud/consul/mesh-gateway.yaml
apiVersion: consul.hashicorp.com/v1alpha1
kind: Mesh
metadata:
  name: payment-mesh
  namespace: consul
spec:
  mtls:
    enabled: true
  
  transparentProxy:
    enabled: true
  
  http:
    sanitizeXForwardedClientCert: true

---
apiVersion: consul.hashicorp.com/v1alpha1
kind: MeshGateway
metadata:
  name: aws-gateway
  namespace: consul
spec:
  replicas: 3
  
  serviceType: LoadBalancer
  
  wanAddress:
    source: Service
    port: 443
    static: ""
  
  consul:
    datacenter: aws-us-east-1

---
apiVersion: consul.hashicorp.com/v1alpha1
kind: MeshGateway
metadata:
  name: gcp-gateway
  namespace: consul
spec:
  replicas: 3
  
  serviceType: LoadBalancer
  
  wanAddress:
    source: Service
    port: 443
    static: ""
  
  consul:
    datacenter: gcp-us-central1

---
# Service configuration for multi-cloud
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceDefaults
metadata:
  name: payment-gateway
  namespace: payment-system
spec:
  protocol: http
  
  meshGateway:
    mode: local
  
  expose:
    checks: true
    paths:
    - path: /health
      localPathPort: 8080
      listenerPort: 21500
  
  upstreamConfig:
    defaults:
      connectTimeoutMs: 5000
      protocol: http
      meshGateway:
        mode: remote

---
# Cross-datacenter service resolver
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceResolver
metadata:
  name: payment-processor
  namespace: payment-system
spec:
  redirect:
    service: payment-processor
    datacenter: aws-us-east-1
  
  failover:
    "*":
      datacenters:
      - gcp-us-central1
      - azure-east-us
  
  connectTimeout: 5s
```

## 8. Disaster Recovery Automation

### Velero Backup Configuration

```yaml
# disaster-recovery/velero/backup-schedule.yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: payment-system-backup
  namespace: velero
spec:
  schedule: "0 */6 * * *"  # Every 6 hours
  
  template:
    includedNamespaces:
    - payment-system
    - payment-gateway
    - payment-data
    
    excludedResources:
    - events
    - events.events.k8s.io
    
    labelSelector:
      matchLabels:
        backup: "true"
    
    hooks:
      resources:
      - name: payment-db-backup
        includedNamespaces:
        - payment-data
        labelSelector:
          matchLabels:
            app: payment-database
        pre:
        - exec:
            container: postgres
            command:
            - /bin/bash
            - -c
            - |
              PGPASSWORD=$POSTGRES_PASSWORD pg_dump \
                -h localhost \
                -U postgres \
                -d payments \
                --no-owner \
                --clean \
                --if-exists \
                > /backup/payments-$(date +%Y%m%d%H%M%S).sql
            onError: Fail
            timeout: 30m
    
    storageLocation: aws-s3-backup
    
    volumeSnapshotLocations:
    - aws-ebs-snapshots
    
    ttl: 720h  # 30 days

---
# Backup storage location
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: aws-s3-backup
  namespace: velero
spec:
  provider: aws
  
  objectStorage:
    bucket: payment-platform-backups
    prefix: velero
  
  config:
    region: us-east-1
    s3ForcePathStyle: "false"
    serverSideEncryption: AES256
    
  credential:
    name: aws-credentials
    key: cloud-credentials

---
# Volume snapshot location
apiVersion: velero.io/v1
kind: VolumeSnapshotLocation
metadata:
  name: aws-ebs-snapshots
  namespace: velero
spec:
  provider: aws
  
  config:
    region: us-east-1
  
  credential:
    name: aws-credentials
    key: cloud-credentials
```

### Disaster Recovery Runbook

```bash
#!/bin/bash
# disaster-recovery/scripts/dr-failover.sh

set -euo pipefail

# Configuration
PRIMARY_REGION="us-east-1"
DR_REGION="us-west-2"
NAMESPACE="payment-system"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    for cmd in kubectl velero aws argocd; do
        if ! command -v $cmd &> /dev/null; then
            error "$cmd is not installed"
            exit 1
        fi
    done
    
    # Check cluster connectivity
    if ! kubectl cluster-info &> /dev/null; then
        error "Cannot connect to Kubernetes cluster"
        exit 1
    fi
}

# Backup primary region
backup_primary() {
    log "Creating backup of primary region..."
    
    velero backup create dr-failover-$(date +%Y%m%d%H%M%S) \
        --include-namespaces $NAMESPACE \
        --wait
    
    if [ $? -eq 0 ]; then
        log "Backup completed successfully"
    else
        error "Backup failed"
        exit 1
    fi
}

# Scale down primary
scale_down_primary() {
    log "Scaling down primary region workloads..."
    
    kubectl config use-context $PRIMARY_REGION
    
    # Get all deployments
    deployments=$(kubectl get deployments -n $NAMESPACE -o name)
    
    for deployment in $deployments; do
        log "Scaling down $deployment"
        kubectl scale $deployment -n $NAMESPACE --replicas=0
    done
    
    # Wait for pods to terminate
    kubectl wait --for=delete pod -n $NAMESPACE --all --timeout=300s
}

# Restore in DR region
restore_dr_region() {
    log "Restoring in DR region..."
    
    kubectl config use-context $DR_REGION
    
    # Get latest backup
    latest_backup=$(velero backup get -o json | jq -r '.items | sort_by(.metadata.creationTimestamp) | last | .metadata.name')
    
    log "Restoring from backup: $latest_backup"
    
    velero restore create --from-backup $latest_backup \
        --include-namespaces $NAMESPACE \
        --wait
    
    if [ $? -eq 0 ]; then
        log "Restore completed successfully"
    else
        error "Restore failed"
        exit 1
    fi
}

# Update DNS
update_dns() {
    log "Updating DNS records..."
    
    # Get DR load balancer endpoint
    dr_endpoint=$(kubectl get svc -n istio-system istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
    
    # Update Route53
    cat > /tmp/dns-update.json <<EOF
{
    "Changes": [{
        "Action": "UPSERT",
        "ResourceRecordSet": {
            "Name": "api.payments.com",
            "Type": "CNAME",
            "TTL": 60,
            "ResourceRecords": [{
                "Value": "$dr_endpoint"
            }]
        }
    }]
}
EOF
    
    aws route53 change-resource-record-sets \
        --hosted-zone-id $HOSTED_ZONE_ID \
        --change-batch file:///tmp/dns-update.json
    
    log "DNS updated to point to DR region"
}

# Verify DR site
verify_dr_site() {
    log "Verifying DR site health..."
    
    kubectl config use-context $DR_REGION
    
    # Check deployments
    unhealthy=$(kubectl get deployments -n $NAMESPACE -o json | \
        jq -r '.items[] | select(.status.readyReplicas != .spec.replicas) | .metadata.name')
    
    if [ -n "$unhealthy" ]; then
        error "Unhealthy deployments found: $unhealthy"
        return 1
    fi
    
    # Check services
    services=$(kubectl get svc -n $NAMESPACE -o name)
    for svc in $services; do
        if ! kubectl get endpoints ${svc#*/} -n $NAMESPACE -o json | jq -e '.subsets[0].addresses[0]' &> /dev/null; then
            error "Service ${svc#*/} has no endpoints"
            return 1
        fi
    done
    
    log "All services healthy in DR region"
    return 0
}

# Update ArgoCD
update_argocd() {
    log "Updating ArgoCD applications..."
    
    apps=$(argocd app list -o json | jq -r '.[] | select(.spec.destination.namespace == "'$NAMESPACE'") | .metadata.name')
    
    for app in $apps; do
        log "Updating $app to use DR cluster"
        argocd app set $app --dest-server https://k8s-dr.payments.internal:6443
        argocd app sync $app
    done
}

# Main execution
main() {
    log "Starting disaster recovery failover process..."
    
    check_prerequisites
    
    # Confirm failover
    echo -e "${YELLOW}This will failover from $PRIMARY_REGION to $DR_REGION${NC}"
    read -p "Are you sure you want to proceed? (yes/no): " confirm
    
    if [ "$confirm" != "yes" ]; then
        log "Failover cancelled"
        exit 0
    fi
    
    # Execute failover
    backup_primary
    scale_down_primary
    restore_dr_region
    update_dns
    
    # Verify
    if verify_dr_site; then
        update_argocd
        log "Disaster recovery failover completed successfully!"
        log "Services are now running in $DR_REGION"
    else
        error "Verification failed. Manual intervention required."
        exit 1
    fi
}

# Run main function
main "$@"
```

## 9. Security Automation

### Falco Custom Rules

```yaml
# security/falco/custom-rules.yaml
customRules:
  payment-security-rules.yaml: |-
    - list: payment_binaries
      items: [payment-gateway, fraud-detector, transaction-processor, settlement-engine]
    
    - list: allowed_payment_files
      items: [/etc/payment/*, /var/lib/payment/*, /tmp/payment-processing/*]
    
    - list: payment_sensitive_files
      items: [/etc/payment/keys/*, /etc/payment/certs/*, /vault/secrets/*]
    
    - macro: payment_container
      condition: (container.image.repository contains "payment")
    
    - rule: Unauthorized Payment Binary Execution
      desc: Detect execution of payment binaries by unauthorized users
      condition: >
        spawned_process and payment_container and
        proc.name in (payment_binaries) and
        not user.name in (payment, root)
      output: >
        Unauthorized payment binary execution
        (user=%user.name command=%proc.cmdline container=%container.id)
      priority: CRITICAL
      tags: [payment, security, mitre_execution]
    
    - rule: Payment Configuration Access
      desc: Detect unauthorized access to payment configuration
      condition: >
        open_read and payment_container and
        fd.name pmatch (payment_sensitive_files) and
        not proc.name in (payment-gateway, vault)
      output: >
        Unauthorized payment config access
        (user=%user.name file=%fd.name process=%proc.name container=%container.id)
      priority: WARNING
      tags: [payment, configuration, mitre_discovery]
    
    - rule: Payment Data Exfiltration
      desc: Detect potential payment data exfiltration
      condition: >
        (open_read or open_write) and payment_container and
        fd.name contains "payment" and
        (proc.name in (nc, ncat, socat) or
         (proc.name = curl and proc.args contains "-X POST"))
      output: >
        Potential payment data exfiltration
        (user=%user.name file=%fd.name command=%proc.cmdline container=%container.id)
      priority: CRITICAL
      tags: [payment, data_loss, mitre_exfiltration]
    
    - rule: Suspicious Database Query
      desc: Detect suspicious database queries in payment system
      condition: >
        spawned_process and payment_container and
        proc.name in (psql, mysql, mongo) and
        (proc.args contains "DELETE FROM" or
         proc.args contains "DROP TABLE" or
         proc.args contains "'; --")
      output: >
        Suspicious database query in payment system
        (user=%user.name query=%proc.cmdline container=%container.id)
      priority: WARNING
      tags: [payment, database, mitre_impact]
```

### Security Scanning Pipeline

```yaml
# security/scanning/security-pipeline.yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: payment-security-scan
  namespace: payment-security
spec:
  params:
  - name: image-url
    type: string
    description: Image to scan
  - name: severity-threshold
    type: string
    default: "CRITICAL"
  
  workspaces:
  - name: shared-workspace
  - name: docker-credentials
  
  tasks:
  # Container image scanning
  - name: trivy-scan
    taskRef:
      name: trivy-scanner
    params:
    - name: IMAGE
      value: $(params.image-url)
    - name: SEVERITY
      value: $(params.severity-threshold)
    workspaces:
    - name: manifest-dir
      workspace: shared-workspace
  
  # SAST scanning
  - name: sonarqube-scan
    taskRef:
      name: sonarqube-scanner
    runAfter:
    - trivy-scan
    params:
    - name: PROJECT_KEY
      value: payment-platform
    workspaces:
    - name: source
      workspace: shared-workspace
  
  # Secret scanning
  - name: trufflehog-scan
    taskRef:
      name: trufflehog-scanner
    runAfter:
    - trivy-scan
    params:
    - name: REPO_PATH
      value: /workspace/source
    workspaces:
    - name: source
      workspace: shared-workspace
  
  # License compliance
  - name: license-scan
    taskRef:
      name: license-scanner
    runAfter:
    - trivy-scan
    workspaces:
    - name: source
      workspace: shared-workspace
  
  # OWASP dependency check
  - name: dependency-check
    taskRef:
      name: owasp-dependency-check
    runAfter:
    - sonarqube-scan
    params:
    - name: PROJECT_NAME
      value: payment-platform
    workspaces:
    - name: source
      workspace: shared-workspace
  
  # Policy validation
  - name: policy-check
    taskRef:
      name: opa-policy-check
    runAfter:
    - dependency-check
    params:
    - name: POLICY_PATH
      value: /policies/security
    workspaces:
    - name: source
      workspace: shared-workspace
  
  # Generate security report
  - name: generate-report
    taskRef:
      name: security-report-generator
    runAfter:
    - policy-check
    params:
    - name: SCAN_RESULTS
      value: $(tasks.trivy-scan.results.scan-results)
    workspaces:
    - name: reports
      workspace: shared-workspace

---
# Trivy scanner task
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: trivy-scanner
spec:
  params:
  - name: IMAGE
    type: string
  - name: SEVERITY
    type: string
    default: "CRITICAL,HIGH"
  
  workspaces:
  - name: manifest-dir
  
  results:
  - name: scan-results
    description: The scan results
  
  steps:
  - name: trivy-scan
    image: aquasec/trivy:latest
    script: |
      #!/bin/bash
      set -e
      
      echo "Scanning image: $(params.IMAGE)"
      
      # Run Trivy scan
      trivy image \
        --severity $(params.SEVERITY) \
        --no-progress \
        --format json \
        --output /tmp/scan-results.json \
        $(params.IMAGE)
      
      # Check for vulnerabilities
      CRITICAL=$(jq '.Results[].Vulnerabilities | map(select(.Severity == "CRITICAL")) | length' /tmp/scan-results.json | awk '{s+=$1} END {print s}')
      HIGH=$(jq '.Results[].Vulnerabilities | map(select(.Severity == "HIGH")) | length' /tmp/scan-results.json | awk '{s+=$1} END {print s}')
      
      echo "Found $CRITICAL CRITICAL and $HIGH HIGH vulnerabilities"
      
      if [ "$CRITICAL" -gt 0 ]; then
        echo "CRITICAL vulnerabilities found!"
        exit 1
      fi
      
      # Save results
      cp /tmp/scan-results.json $(workspaces.manifest-dir.path)/
      echo -n "/tmp/scan-results.json" > $(results.scan-results.path)
```

## 10. Cost Governance

### FinOps Dashboard

```yaml
# cost-governance/kubecost/values.yaml
kubecost:
  productConfigs:
    clusterName: payment-production
    currencyCode: USD
    azureBillingRegion: US
    
    # Prometheus integration
    prometheus:
      fqdn: http://prometheus-server.observability.svc.cluster.local
      enabled: true
    
    # Cloud billing integration
    cloudIntegration:
      enabled: true
      awsSpotDataRegion: us-east-1
      awsSpotDataBucket: s3://payment-platform-spot-data
      awsSpotDataPrefix: payment-cluster
    
    # Alerts configuration
    alerts:
      enabled: true
      alertConfigs:
        budgetAlert:
          enabled: true
          threshold: 10000  # $10,000 monthly budget
        
        efficiencyAlert:
          enabled: true
          threshold: 0.7  # 70% efficiency threshold
        
        spendChangeAlert:
          enabled: true
          threshold: 1.2  # 20% increase threshold
    
    # Recommendations
    recommendations:
      enabled: true
      
  # Grafana dashboards
  grafana:
    enabled: true
    domainName: cost.payments.internal
    
    dashboards:
      enabled: true
      
  # Cost model configuration
  costModel:
    enabled: true
    
    # CPU cost per hour
    cpuCostPerHour: 0.031
    
    # Memory cost per GB hour
    memoryGostPerGBHour: 0.004
    
    # Storage cost per GB hour
    storageCostPerGBHour: 0.00013
    
    # Network cost per GB
    networkCostPerGB: 0.12

---
# Cost allocation by namespace
apiVersion: v1
kind: ConfigMap
metadata:
  name: kubecost-allocation
  namespace: kubecost
data:
  allocation.yaml: |
    namespaceAllocation:
      payment-system:
        team: payment-platform
        environment: production
        costCenter: CC-1001
        budget: 5000
      
      payment-gateway:
        team: api-team
        environment: production
        costCenter: CC-1002
        budget: 3000
      
      fraud-detection:
        team: ml-team
        environment: production
        costCenter: CC-1003
        budget: 2000
    
    labelAllocation:
      app:
        payment-gateway: CC-1002
        fraud-detector: CC-1003
        transaction-processor: CC-1001
        settlement-engine: CC-1001
    
    annotations:
      cost-center: true
      team: true
      environment: true
```

### Cost Optimization Policies

```yaml
# cost-governance/policies/cost-policies.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: cost-optimization-policies
spec:
  validationFailureAction: enforce
  background: true
  rules:
    # Require resource requests/limits
    - name: require-pod-resources
      match:
        any:
        - resources:
            kinds:
            - Pod
            namespaces:
            - payment-*
      validate:
        message: "Resource requests and limits are required for cost tracking"
        pattern:
          spec:
            containers:
            - name: "*"
              resources:
                requests:
                  memory: "?*"
                  cpu: "?*"
                limits:
                  memory: "?*"
                  cpu: "?*"
    
    # Enforce node selectors for cost optimization
    - name: enforce-spot-instances
      match:
        any:
        - resources:
            kinds:
            - Deployment
            - StatefulSet
            namespaces:
            - payment-system
            selector:
              matchLabels:
                workload-type: batch
      mutate:
        patchStrategicMerge:
          spec:
            template:
              spec:
                nodeSelector:
                  node.kubernetes.io/instance-type: spot
                tolerations:
                - key: spot
                  operator: Equal
                  value: "true"
                  effect: NoSchedule
    
    # Enforce PVC size limits
    - name: limit-pvc-size
      match:
        any:
        - resources:
            kinds:
            - PersistentVolumeClaim
            namespaces:
            - payment-*
      validate:
        message: "PVC size must not exceed 1Ti without approval"
        deny:
          conditions:
          - key: "{{ request.object.spec.resources.requests.storage }}"
            operator: GreaterThan
            value: "1Ti"
          - key: "{{ request.object.metadata.annotations.\"cost-approved\" || '' }}"
            operator: NotEquals
            value: "true"

---
# Goldilocks VPA recommendations
apiVersion: v1
kind: ConfigMap
metadata:
  name: goldilocks-config
  namespace: goldilocks
data:
  config.yaml: |
    # Enable VPA for all payment namespaces
    namespaces:
      payment-system:
        enabled: true
        labels:
          goldilocks.fairwinds.com/enabled: "true"
      
      payment-gateway:
        enabled: true
        labels:
          goldilocks.fairwinds.com/enabled: "true"
    
    # Dashboard configuration
    dashboard:
      enabled: true
      basePath: /goldilocks
      
    # Exclude certain workloads
    excludes:
      - name: "fluent-bit-*"
      - name: "node-exporter-*"
```

## Implementation Timeline

### Phase 1: Foundation (Month 1-2)
1. GitOps repository setup
2. ArgoCD deployment and configuration
3. Policy as Code framework
4. Basic observability stack

### Phase 2: Automation (Month 2-3)
1. Progressive delivery implementation
2. Security automation
3. Disaster recovery automation
4. Multi-cloud foundations

### Phase 3: Excellence (Month 3-4)
1. Advanced service mesh features
2. Cost governance implementation
3. Full multi-cloud deployment
4. Performance optimization

## Success Metrics

| Metric | Current (60%) | Target (95%) | Measurement |
|--------|---------------|--------------|-------------|
| GitOps adoption | Manual deploys | 100% GitOps | % automated deployments |
| Policy compliance | Basic | Comprehensive | Policy violations/day |
| Deployment frequency | Weekly | Multiple daily | Deployments/day |
| MTTR | 4 hours | <15 minutes | Incident recovery time |
| Security scanning | Manual | 100% automated | % images scanned |
| Cost visibility | Limited | Real-time | Cost tracking accuracy |
| Multi-cloud ready | Single cloud | 3+ clouds | Cloud provider count |

## Conclusion

This Cloud-Native Excellence Guide provides comprehensive patterns for achieving 95% cloud-native maturity. The focus on GitOps, Policy as Code, automation, and observability ensures a robust, scalable, and maintainable payment platform that meets 2025 industry standards.
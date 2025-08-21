# Azure Enterprise Deployment Guide

## Overview

This comprehensive guide provides step-by-step instructions for deploying Azure enterprise architectures using Infrastructure as Code (IaC) with Terraform, Bicep, and Azure DevOps.

## Prerequisites

### Required Tools
```bash
# Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Terraform
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Azure PowerShell
sudo apt-get update
sudo apt-get install -y wget apt-transport-https software-properties-common
wget -q https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt-get update
sudo apt-get install -y powershell

# Bicep CLI
az bicep install
```

### Azure Subscription Setup
```bash
# Login to Azure
az login

# Set default subscription
az account set --subscription "your-subscription-id"

# Create service principal for automation
az ad sp create-for-rbac --name "terraform-sp" --role="Contributor" --scopes="/subscriptions/your-subscription-id"
```

## Deployment Methods

### Method 1: Terraform Deployment

#### 1.1 Backend Configuration

Create a storage account for Terraform state:

```bash
# Create resource group for Terraform state
az group create --name "terraform-state-rg" --location "East US"

# Create storage account
az storage account create \
  --name "terraformstate$(date +%s)" \
  --resource-group "terraform-state-rg" \
  --location "East US" \
  --sku "Standard_LRS" \
  --kind "StorageV2"

# Create container
az storage container create \
  --name "tfstate" \
  --account-name "your-storage-account-name"
```

Create `backend.tf`:

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "your-storage-account-name"
    container_name      = "tfstate"
    key                 = "enterprise.terraform.tfstate"
  }
}
```

#### 1.2 Variables Configuration

Create `terraform.tfvars`:

```hcl
# Environment configuration
environment   = "prod"
location      = "East US"
organization  = "contoso"

# Network configuration
hub_address_space           = ["10.0.0.0/16"]
prod_spoke_address_space    = ["10.1.0.0/16"]
dev_spoke_address_space     = ["10.2.0.0/16"]
shared_address_space        = ["10.3.0.0/16"]

# AKS configuration
kubernetes_version = "1.28"
aks_node_count    = 3
aks_vm_size       = "Standard_D4s_v3"

# Database configuration
sql_admin_username = "sqladmin"
sql_sku_name      = "S2"
sql_max_size_gb   = 100

# Monitoring configuration
log_retention_days = 90
```

#### 1.3 Deployment Steps

```bash
# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Plan deployment
terraform plan -var-file="terraform.tfvars" -out="tfplan"

# Apply changes
terraform apply "tfplan"

# Verify deployment
terraform show
```

### Method 2: Bicep Deployment

#### 2.1 Parameter Files

Create `main.parameters.json`:

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "namePrefix": {
      "value": "microservices"
    },
    "location": {
      "value": "East US"
    },
    "environment": {
      "value": "prod"
    },
    "aksAdminPublicKey": {
      "value": "ssh-rsa AAAAB3NzaC1yc2E..."
    }
  }
}
```

#### 2.2 Deployment Commands

```bash
# Create resource group
az group create --name "microservices-prod-rg" --location "East US"

# Validate template
az deployment group validate \
  --resource-group "microservices-prod-rg" \
  --template-file "bicep-microservices-architecture.bicep" \
  --parameters "@main.parameters.json"

# Deploy template
az deployment group create \
  --resource-group "microservices-prod-rg" \
  --template-file "bicep-microservices-architecture.bicep" \
  --parameters "@main.parameters.json" \
  --name "microservices-deployment"

# Monitor deployment
az deployment group show \
  --resource-group "microservices-prod-rg" \
  --name "microservices-deployment"
```

### Method 3: ARM Template Deployment

Create ARM template deployment script:

```bash
#!/bin/bash

# Configuration
RESOURCE_GROUP="enterprise-arm-rg"
LOCATION="East US"
TEMPLATE_FILE="azuredeploy.json"
PARAMETERS_FILE="azuredeploy.parameters.json"
DEPLOYMENT_NAME="enterprise-deployment-$(date +%Y%m%d-%H%M%S)"

# Create resource group
echo "Creating resource group..."
az group create --name $RESOURCE_GROUP --location "$LOCATION"

# Validate template
echo "Validating ARM template..."
az deployment group validate \
  --resource-group $RESOURCE_GROUP \
  --template-file $TEMPLATE_FILE \
  --parameters @$PARAMETERS_FILE

if [ $? -eq 0 ]; then
    echo "Template validation successful"
    
    # Deploy template
    echo "Deploying ARM template..."
    az deployment group create \
      --resource-group $RESOURCE_GROUP \
      --template-file $TEMPLATE_FILE \
      --parameters @$PARAMETERS_FILE \
      --name $DEPLOYMENT_NAME \
      --verbose
      
    if [ $? -eq 0 ]; then
        echo "Deployment completed successfully"
        
        # Get deployment outputs
        az deployment group show \
          --resource-group $RESOURCE_GROUP \
          --name $DEPLOYMENT_NAME \
          --query properties.outputs
    else
        echo "Deployment failed"
        exit 1
    fi
else
    echo "Template validation failed"
    exit 1
fi
```

## Post-Deployment Configuration

### 1. AKS Cluster Setup

```bash
# Get AKS credentials
az aks get-credentials --resource-group "microservices-prod-rg" --name "microservices-prod-aks"

# Install kubectl
az aks install-cli

# Verify cluster connection
kubectl get nodes

# Install Helm
curl https://get.helm.sh/helm-v3.13.0-linux-amd64.tar.gz | tar xz
sudo mv linux-amd64/helm /usr/local/bin/helm

# Add required Helm repositories
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo add jetstack https://charts.jetstack.io
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

### 2. Install Core Components

#### Cert-Manager for SSL Certificates

```bash
# Create namespace
kubectl create namespace cert-manager

# Install cert-manager
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --version v1.13.0 \
  --set installCRDs=true

# Create ClusterIssuer for Let's Encrypt
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@yourdomain.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: azure/application-gateway
EOF
```

#### Monitoring Stack

```bash
# Create monitoring namespace
kubectl create namespace monitoring

# Install Prometheus and Grafana
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=50Gi \
  --set grafana.persistence.enabled=true \
  --set grafana.persistence.size=10Gi
```

### 3. Configure Azure Key Vault CSI Driver

```bash
# Install Azure Key Vault CSI Driver
helm repo add csi-secrets-store-provider-azure https://azure.github.io/secrets-store-csi-driver-provider-azure/charts
helm install csi-secrets-store-provider-azure csi-secrets-store-provider-azure/csi-secrets-store-provider-azure \
  --namespace kube-system

# Enable workload identity
az aks update --resource-group "microservices-prod-rg" --name "microservices-prod-aks" --enable-workload-identity

# Create managed identity
az identity create --name "microservices-workload-identity" --resource-group "microservices-prod-rg"

# Get identity details
CLIENT_ID=$(az identity show --name "microservices-workload-identity" --resource-group "microservices-prod-rg" --query clientId -o tsv)
IDENTITY_OBJECT_ID=$(az identity show --name "microservices-workload-identity" --resource-group "microservices-prod-rg" --query principalId -o tsv)

# Grant permissions to Key Vault
az keyvault set-policy --name "microservices-prod-kv" --object-id $IDENTITY_OBJECT_ID --secret-permissions get list
```

## Security Hardening

### 1. Network Security

```bash
# Create Network Security Groups
az network nsg create \
  --resource-group "microservices-prod-rg" \
  --name "microservices-nsg"

# Add security rules
az network nsg rule create \
  --resource-group "microservices-prod-rg" \
  --nsg-name "microservices-nsg" \
  --name "AllowHTTPS" \
  --priority 100 \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes "*" \
  --destination-port-ranges 443

# Enable Azure Firewall
az network firewall create \
  --name "microservices-firewall" \
  --resource-group "microservices-prod-rg" \
  --location "East US"
```

### 2. Identity and Access Management

```bash
# Create Azure AD groups
az ad group create --display-name "AKS-Admins" --mail-nickname "aks-admins"
az ad group create --display-name "AKS-Developers" --mail-nickname "aks-developers"

# Enable RBAC on AKS
az aks update \
  --resource-group "microservices-prod-rg" \
  --name "microservices-prod-aks" \
  --enable-aad \
  --aad-admin-group-object-ids $(az ad group show --group "AKS-Admins" --query objectId -o tsv)
```

### 3. Azure Policy Implementation

```bash
# Assign Azure Policy initiatives
az policy assignment create \
  --name "aks-security-baseline" \
  --scope "/subscriptions/your-subscription-id/resourceGroups/microservices-prod-rg" \
  --policy-set-definition "/providers/Microsoft.Authorization/policySetDefinitions/a8640138-9b0a-4a28-b8cb-1666c838647d"
```

## Monitoring and Alerting Setup

### 1. Azure Monitor Configuration

```bash
# Create Log Analytics workspace (if not created by deployment)
az monitor log-analytics workspace create \
  --resource-group "microservices-prod-rg" \
  --workspace-name "microservices-logs"

# Enable Container Insights
az aks enable-addons \
  --resource-group "microservices-prod-rg" \
  --name "microservices-prod-aks" \
  --addons monitoring \
  --workspace-resource-id "/subscriptions/your-subscription-id/resourceGroups/microservices-prod-rg/providers/Microsoft.OperationalInsights/workspaces/microservices-logs"
```

### 2. Alert Rules Configuration

```bash
# Create action group for notifications
az monitor action-group create \
  --name "microservices-alerts" \
  --resource-group "microservices-prod-rg" \
  --short-name "msalerts" \
  --email-receivers name="admin" email-address="admin@yourdomain.com"

# Create metric alert for high CPU usage
az monitor metrics alert create \
  --name "AKS-HighCPU" \
  --resource-group "microservices-prod-rg" \
  --scopes "/subscriptions/your-subscription-id/resourceGroups/microservices-prod-rg/providers/Microsoft.ContainerService/managedClusters/microservices-prod-aks" \
  --condition "avg Percentage CPU > 80" \
  --action-groups "/subscriptions/your-subscription-id/resourceGroups/microservices-prod-rg/providers/Microsoft.Insights/actionGroups/microservices-alerts"
```

## Backup and Disaster Recovery

### 1. Database Backup Configuration

```bash
# Configure automated backups for Azure SQL
az sql db update \
  --resource-group "microservices-prod-rg" \
  --server "microservices-sql-server" \
  --name "microservices-db" \
  --backup-storage-redundancy "Geo"

# Create long-term retention policy
az sql db ltr-policy set \
  --resource-group "microservices-prod-rg" \
  --server "microservices-sql-server" \
  --database "microservices-db" \
  --weekly-retention "P12W" \
  --monthly-retention "P12M" \
  --yearly-retention "P10Y" \
  --week-of-year 1
```

### 2. Storage Account Backup

```bash
# Enable blob versioning and soft delete
az storage account blob-service-properties update \
  --account-name "microservicesstorage" \
  --resource-group "microservices-prod-rg" \
  --enable-versioning true \
  --enable-delete-retention true \
  --delete-retention-days 30
```

## Troubleshooting Common Issues

### 1. Deployment Failures

```bash
# Check deployment status
az deployment group show \
  --resource-group "microservices-prod-rg" \
  --name "microservices-deployment" \
  --query properties.provisioningState

# Get deployment errors
az deployment group show \
  --resource-group "microservices-prod-rg" \
  --name "microservices-deployment" \
  --query properties.error
```

### 2. AKS Connectivity Issues

```bash
# Check AKS cluster health
az aks show --resource-group "microservices-prod-rg" --name "microservices-prod-aks" --query provisioningState

# Get cluster credentials again
az aks get-credentials --resource-group "microservices-prod-rg" --name "microservices-prod-aks" --overwrite-existing

# Check node status
kubectl get nodes -o wide
kubectl describe nodes
```

### 3. Certificate Issues

```bash
# Check cert-manager logs
kubectl logs -n cert-manager deployment/cert-manager

# Check certificate status
kubectl get certificates --all-namespaces
kubectl describe certificate your-certificate-name -n your-namespace
```

## Performance Optimization

### 1. AKS Optimization

```bash
# Enable cluster autoscaler
az aks update \
  --resource-group "microservices-prod-rg" \
  --name "microservices-prod-aks" \
  --enable-cluster-autoscaler \
  --min-count 1 \
  --max-count 10

# Configure node pools for different workloads
az aks nodepool add \
  --resource-group "microservices-prod-rg" \
  --cluster-name "microservices-prod-aks" \
  --name "computepool" \
  --node-count 2 \
  --node-vm-size "Standard_D8s_v3" \
  --mode User \
  --labels workload=compute-intensive
```

### 2. Database Performance

```bash
# Scale database if needed
az sql db update \
  --resource-group "microservices-prod-rg" \
  --server "microservices-sql-server" \
  --name "microservices-db" \
  --service-objective "S4"
```

This deployment guide provides a comprehensive approach to deploying and managing enterprise Azure architectures with proper security, monitoring, and operational practices.
# Azure Enterprise Infrastructure as Code - Terraform
# This template creates a complete hub-and-spoke architecture for enterprise deployments

terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.0"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
    key_vault {
      purge_soft_delete_on_destroy = true
    }
  }
}

# Variables
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "prod"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "East US"
}

variable "organization" {
  description = "Organization name"
  type        = string
  default     = "contoso"
}

variable "admin_username" {
  description = "Administrator username for VMs"
  type        = string
  default     = "azureadmin"
}

# Local values
locals {
  common_tags = {
    Environment   = var.environment
    Organization  = var.organization
    ManagedBy     = "Terraform"
    CostCenter    = "IT"
    Project       = "Azure-Enterprise-Architecture"
  }
  
  resource_prefix = "${var.organization}-${var.environment}"
}

# Resource Groups
resource "azurerm_resource_group" "hub" {
  name     = "${local.resource_prefix}-hub-rg"
  location = var.location
  tags     = local.common_tags
}

resource "azurerm_resource_group" "prod_spoke" {
  name     = "${local.resource_prefix}-prod-spoke-rg"
  location = var.location
  tags     = local.common_tags
}

resource "azurerm_resource_group" "dev_spoke" {
  name     = "${local.resource_prefix}-dev-spoke-rg"
  location = var.location
  tags     = local.common_tags
}

resource "azurerm_resource_group" "shared" {
  name     = "${local.resource_prefix}-shared-rg"
  location = var.location
  tags     = local.common_tags
}

resource "azurerm_resource_group" "data" {
  name     = "${local.resource_prefix}-data-rg"
  location = var.location
  tags     = local.common_tags
}

# Hub Virtual Network
resource "azurerm_virtual_network" "hub" {
  name                = "${local.resource_prefix}-hub-vnet"
  location            = azurerm_resource_group.hub.location
  resource_group_name = azurerm_resource_group.hub.name
  address_space       = ["10.0.0.0/16"]
  tags                = local.common_tags
}

resource "azurerm_subnet" "gateway" {
  name                 = "GatewaySubnet"
  resource_group_name  = azurerm_resource_group.hub.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_subnet" "firewall" {
  name                 = "AzureFirewallSubnet"
  resource_group_name  = azurerm_resource_group.hub.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_subnet" "bastion" {
  name                 = "AzureBastionSubnet"
  resource_group_name  = azurerm_resource_group.hub.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.0.3.0/24"]
}

# Production Spoke Virtual Network
resource "azurerm_virtual_network" "prod_spoke" {
  name                = "${local.resource_prefix}-prod-vnet"
  location            = azurerm_resource_group.prod_spoke.location
  resource_group_name = azurerm_resource_group.prod_spoke.name
  address_space       = ["10.1.0.0/16"]
  tags                = local.common_tags
}

resource "azurerm_subnet" "prod_web" {
  name                 = "${local.resource_prefix}-prod-web-subnet"
  resource_group_name  = azurerm_resource_group.prod_spoke.name
  virtual_network_name = azurerm_virtual_network.prod_spoke.name
  address_prefixes     = ["10.1.1.0/24"]
}

resource "azurerm_subnet" "prod_app" {
  name                 = "${local.resource_prefix}-prod-app-subnet"
  resource_group_name  = azurerm_resource_group.prod_spoke.name
  virtual_network_name = azurerm_virtual_network.prod_spoke.name
  address_prefixes     = ["10.1.2.0/24"]
}

resource "azurerm_subnet" "prod_data" {
  name                 = "${local.resource_prefix}-prod-data-subnet"
  resource_group_name  = azurerm_resource_group.prod_spoke.name
  virtual_network_name = azurerm_virtual_network.prod_spoke.name
  address_prefixes     = ["10.1.3.0/24"]
  
  delegation {
    name = "delegation"
    service_delegation {
      name    = "Microsoft.Sql/managedInstances"
      actions = ["Microsoft.Network/virtualNetworks/subnets/join/action", "Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action", "Microsoft.Network/virtualNetworks/subnets/unprepareNetworkPolicies/action"]
    }
  }
}

# Development Spoke Virtual Network
resource "azurerm_virtual_network" "dev_spoke" {
  name                = "${local.resource_prefix}-dev-vnet"
  location            = azurerm_resource_group.dev_spoke.location
  resource_group_name = azurerm_resource_group.dev_spoke.name
  address_space       = ["10.2.0.0/16"]
  tags                = local.common_tags
}

resource "azurerm_subnet" "dev_apps" {
  name                 = "${local.resource_prefix}-dev-apps-subnet"
  resource_group_name  = azurerm_resource_group.dev_spoke.name
  virtual_network_name = azurerm_virtual_network.dev_spoke.name
  address_prefixes     = ["10.2.1.0/24"]
}

# VNet Peering - Hub to Prod Spoke
resource "azurerm_virtual_network_peering" "hub_to_prod" {
  name                      = "hub-to-prod-peering"
  resource_group_name       = azurerm_resource_group.hub.name
  virtual_network_name      = azurerm_virtual_network.hub.name
  remote_virtual_network_id = azurerm_virtual_network.prod_spoke.id
  allow_forwarded_traffic   = true
  allow_gateway_transit     = true
}

resource "azurerm_virtual_network_peering" "prod_to_hub" {
  name                      = "prod-to-hub-peering"
  resource_group_name       = azurerm_resource_group.prod_spoke.name
  virtual_network_name      = azurerm_virtual_network.prod_spoke.name
  remote_virtual_network_id = azurerm_virtual_network.hub.id
  allow_forwarded_traffic   = true
  use_remote_gateways       = true
  depends_on               = [azurerm_virtual_network_gateway.hub]
}

# VNet Peering - Hub to Dev Spoke
resource "azurerm_virtual_network_peering" "hub_to_dev" {
  name                      = "hub-to-dev-peering"
  resource_group_name       = azurerm_resource_group.hub.name
  virtual_network_name      = azurerm_virtual_network.hub.name
  remote_virtual_network_id = azurerm_virtual_network.dev_spoke.id
  allow_forwarded_traffic   = true
  allow_gateway_transit     = true
}

resource "azurerm_virtual_network_peering" "dev_to_hub" {
  name                      = "dev-to-hub-peering"
  resource_group_name       = azurerm_resource_group.dev_spoke.name
  virtual_network_name      = azurerm_virtual_network.dev_spoke.name
  remote_virtual_network_id = azurerm_virtual_network.hub.id
  allow_forwarded_traffic   = true
  use_remote_gateways       = true
  depends_on               = [azurerm_virtual_network_gateway.hub]
}

# Public IP for VPN Gateway
resource "azurerm_public_ip" "gateway" {
  name                = "${local.resource_prefix}-gateway-pip"
  location            = azurerm_resource_group.hub.location
  resource_group_name = azurerm_resource_group.hub.name
  allocation_method   = "Static"
  sku                 = "Standard"
  tags                = local.common_tags
}

# VPN Gateway
resource "azurerm_virtual_network_gateway" "hub" {
  name                = "${local.resource_prefix}-hub-gateway"
  location            = azurerm_resource_group.hub.location
  resource_group_name = azurerm_resource_group.hub.name
  type                = "Vpn"
  vpn_type            = "RouteBased"
  active_active       = false
  enable_bgp          = false
  sku                 = "VpnGw2"
  tags                = local.common_tags

  ip_configuration {
    name                          = "vnetGatewayConfig"
    public_ip_address_id          = azurerm_public_ip.gateway.id
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.gateway.id
  }
}

# Public IP for Azure Firewall
resource "azurerm_public_ip" "firewall" {
  name                = "${local.resource_prefix}-firewall-pip"
  location            = azurerm_resource_group.hub.location
  resource_group_name = azurerm_resource_group.hub.name
  allocation_method   = "Static"
  sku                 = "Standard"
  tags                = local.common_tags
}

# Azure Firewall
resource "azurerm_firewall" "hub" {
  name                = "${local.resource_prefix}-hub-firewall"
  location            = azurerm_resource_group.hub.location
  resource_group_name = azurerm_resource_group.hub.name
  sku_name            = "AZFW_VNet"
  sku_tier            = "Standard"
  tags                = local.common_tags

  ip_configuration {
    name                 = "configuration"
    subnet_id            = azurerm_subnet.firewall.id
    public_ip_address_id = azurerm_public_ip.firewall.id
  }
}

# Azure Firewall Network Rules
resource "azurerm_firewall_network_rule_collection" "hub" {
  name                = "allow-internal"
  azure_firewall_name = azurerm_firewall.hub.name
  resource_group_name = azurerm_resource_group.hub.name
  priority            = 100
  action              = "Allow"

  rule {
    name = "allow-internal-traffic"
    source_addresses = [
      "10.0.0.0/8"
    ]
    destination_ports = ["*"]
    destination_addresses = [
      "10.0.0.0/8"
    ]
    protocols = ["Any"]
  }
}

# Key Vault for secrets management
data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "shared" {
  name                        = "${var.organization}-${var.environment}-kv"
  location                    = azurerm_resource_group.shared.location
  resource_group_name         = azurerm_resource_group.shared.name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false
  sku_name                    = "standard"
  tags                        = local.common_tags

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    key_permissions = [
      "Get", "List", "Update", "Create", "Import", "Delete", "Recover", "Backup", "Restore"
    ]

    secret_permissions = [
      "Get", "List", "Set", "Delete", "Recover", "Backup", "Restore"
    ]

    storage_permissions = [
      "Get", "List", "Update", "Delete", "Set"
    ]
  }
}

# Log Analytics Workspace for monitoring
resource "azurerm_log_analytics_workspace" "shared" {
  name                = "${local.resource_prefix}-logs"
  location            = azurerm_resource_group.shared.location
  resource_group_name = azurerm_resource_group.shared.name
  sku                 = "PerGB2018"
  retention_in_days   = 90
  tags                = local.common_tags
}

# Application Insights
resource "azurerm_application_insights" "shared" {
  name                = "${local.resource_prefix}-appinsights"
  location            = azurerm_resource_group.shared.location
  resource_group_name = azurerm_resource_group.shared.name
  workspace_id        = azurerm_log_analytics_workspace.shared.id
  application_type    = "web"
  tags                = local.common_tags
}

# Azure SQL Database
resource "azurerm_mssql_server" "prod" {
  name                         = "${local.resource_prefix}-sql-server"
  resource_group_name          = azurerm_resource_group.prod_spoke.name
  location                     = azurerm_resource_group.prod_spoke.location
  version                      = "12.0"
  administrator_login          = var.admin_username
  administrator_login_password = random_password.sql_admin_password.result
  minimum_tls_version          = "1.2"
  tags                         = local.common_tags

  azuread_administrator {
    login_username = var.admin_username
    object_id      = data.azurerm_client_config.current.object_id
  }
}

resource "azurerm_mssql_database" "prod" {
  name           = "${local.resource_prefix}-db"
  server_id      = azurerm_mssql_server.prod.id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  license_type   = "LicenseIncluded"
  max_size_gb    = 100
  sku_name       = "S2"
  zone_redundant = false
  tags           = local.common_tags
}

# Random password for SQL admin
resource "random_password" "sql_admin_password" {
  length  = 16
  special = true
}

# Store SQL admin password in Key Vault
resource "azurerm_key_vault_secret" "sql_admin_password" {
  name         = "sql-admin-password"
  value        = random_password.sql_admin_password.result
  key_vault_id = azurerm_key_vault.shared.id
  depends_on   = [azurerm_key_vault.shared]
}

# Container Registry
resource "azurerm_container_registry" "shared" {
  name                = "${var.organization}${var.environment}acr"
  resource_group_name = azurerm_resource_group.shared.name
  location            = azurerm_resource_group.shared.location
  sku                 = "Premium"
  admin_enabled       = false
  tags                = local.common_tags

  georeplications {
    location = "West US"
    zone_redundancy_enabled = false
  }
}

# Azure Kubernetes Service
resource "azurerm_kubernetes_cluster" "prod" {
  name                = "${local.resource_prefix}-aks"
  location            = azurerm_resource_group.prod_spoke.location
  resource_group_name = azurerm_resource_group.prod_spoke.name
  dns_prefix          = "${local.resource_prefix}-aks"
  kubernetes_version  = "1.27"
  tags                = local.common_tags

  default_node_pool {
    name                = "default"
    node_count          = 3
    vm_size             = "Standard_D2s_v3"
    type                = "VirtualMachineScaleSets"
    zones               = ["1", "2", "3"]
    vnet_subnet_id      = azurerm_subnet.prod_app.id
    enable_auto_scaling = true
    min_count           = 1
    max_count           = 10
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
    network_policy    = "azure"
  }

  azure_policy_enabled = true
  oms_agent {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.shared.id
  }
}

# Role assignment for AKS to pull images from ACR
resource "azurerm_role_assignment" "aks_acr_pull" {
  scope                = azurerm_container_registry.shared.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.prod.kubelet_identity[0].object_id
}

# Outputs
output "resource_group_names" {
  description = "Names of created resource groups"
  value = {
    hub        = azurerm_resource_group.hub.name
    prod_spoke = azurerm_resource_group.prod_spoke.name
    dev_spoke  = azurerm_resource_group.dev_spoke.name
    shared     = azurerm_resource_group.shared.name
    data       = azurerm_resource_group.data.name
  }
}

output "virtual_network_names" {
  description = "Names of created virtual networks"
  value = {
    hub        = azurerm_virtual_network.hub.name
    prod_spoke = azurerm_virtual_network.prod_spoke.name
    dev_spoke  = azurerm_virtual_network.dev_spoke.name
  }
}

output "key_vault_name" {
  description = "Name of the Key Vault"
  value       = azurerm_key_vault.shared.name
}

output "aks_cluster_name" {
  description = "Name of the AKS cluster"
  value       = azurerm_kubernetes_cluster.prod.name
}

output "container_registry_name" {
  description = "Name of the Container Registry"
  value       = azurerm_container_registry.shared.name
}

output "sql_server_name" {
  description = "Name of the SQL Server"
  value       = azurerm_mssql_server.prod.name
}

output "log_analytics_workspace_name" {
  description = "Name of the Log Analytics workspace"
  value       = azurerm_log_analytics_workspace.shared.name
}
// Azure Bicep template for Microservices Architecture
// This template creates a complete microservices platform using Azure Kubernetes Service

@description('The name prefix for all resources')
param namePrefix string = 'microservices'

@description('The location where resources will be deployed')
param location string = resourceGroup().location

@description('The environment (dev, test, prod)')
@allowed(['dev', 'test', 'prod'])
param environment string = 'dev'

@description('The AKS cluster admin username')
param aksAdminUsername string = 'aksadmin'

@description('The AKS cluster admin SSH public key')
param aksAdminPublicKey string

// Variables
var resourcePrefix = '${namePrefix}-${environment}'
var tags = {
  Environment: environment
  Application: 'Microservices'
  ManagedBy: 'Bicep'
  CostCenter: 'Engineering'
}

// Virtual Network
resource vnet 'Microsoft.Network/virtualNetworks@2023-05-01' = {
  name: '${resourcePrefix}-vnet'
  location: location
  tags: tags
  properties: {
    addressSpace: {
      addressPrefixes: ['10.0.0.0/16']
    }
    subnets: [
      {
        name: 'aks-subnet'
        properties: {
          addressPrefix: '10.0.1.0/24'
          privateEndpointNetworkPolicies: 'Disabled'
          privateLinkServiceNetworkPolicies: 'Enabled'
        }
      }
      {
        name: 'app-gateway-subnet'
        properties: {
          addressPrefix: '10.0.2.0/24'
        }
      }
      {
        name: 'private-endpoint-subnet'
        properties: {
          addressPrefix: '10.0.3.0/24'
          privateEndpointNetworkPolicies: 'Disabled'
        }
      }
    ]
  }
}

// Network Security Group for AKS
resource aksNsg 'Microsoft.Network/networkSecurityGroups@2023-05-01' = {
  name: '${resourcePrefix}-aks-nsg'
  location: location
  tags: tags
  properties: {
    securityRules: [
      {
        name: 'AllowHTTPS'
        properties: {
          protocol: 'Tcp'
          sourcePortRange: '*'
          destinationPortRange: '443'
          sourceAddressPrefix: '*'
          destinationAddressPrefix: '*'
          access: 'Allow'
          priority: 1000
          direction: 'Inbound'
        }
      }
      {
        name: 'AllowHTTP'
        properties: {
          protocol: 'Tcp'
          sourcePortRange: '*'
          destinationPortRange: '80'
          sourceAddressPrefix: '*'
          destinationAddressPrefix: '*'
          access: 'Allow'
          priority: 1010
          direction: 'Inbound'
        }
      }
    ]
  }
}

// Log Analytics Workspace
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${resourcePrefix}-logs'
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 90
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
  }
}

// Application Insights
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${resourcePrefix}-appinsights'
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

// Azure Container Registry
resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: replace('${resourcePrefix}acr', '-', '')
  location: location
  tags: tags
  sku: {
    name: 'Premium'
  }
  properties: {
    adminUserEnabled: false
    networkRuleSet: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
    policies: {
      quarantinePolicy: {
        status: 'enabled'
      }
      trustPolicy: {
        type: 'Notary'
        status: 'enabled'
      }
      retentionPolicy: {
        days: 30
        status: 'enabled'
      }
      exportPolicy: {
        status: 'enabled'
      }
    }
    encryption: {
      status: 'disabled'
    }
    dataEndpointEnabled: false
    publicNetworkAccess: 'Enabled'
  }
}

// Azure Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: '${resourcePrefix}-kv'
  location: location
  tags: tags
  properties: {
    enabledForDeployment: false
    enabledForTemplateDeployment: true
    enabledForDiskEncryption: false
    tenantId: subscription().tenantId
    accessPolicies: []
    sku: {
      name: 'standard'
      family: 'A'
    }
    networkAcls: {
      defaultAction: 'Allow'
      bypass: 'AzureServices'
    }
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    enablePurgeProtection: false
  }
}

// Azure Kubernetes Service
resource aks 'Microsoft.ContainerService/managedClusters@2023-10-01' = {
  name: '${resourcePrefix}-aks'
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    dnsPrefix: '${resourcePrefix}-aks'
    kubernetesVersion: '1.28'
    enableRBAC: true
    
    // Default node pool
    agentPoolProfiles: [
      {
        name: 'default'
        count: 3
        vmSize: 'Standard_D4s_v3'
        osType: 'Linux'
        mode: 'System'
        type: 'VirtualMachineScaleSets'
        enableAutoScaling: true
        minCount: 1
        maxCount: 10
        vnetSubnetID: '${vnet.id}/subnets/aks-subnet'
        availabilityZones: ['1', '2', '3']
        maxPods: 110
        osDiskSizeGB: 100
        osDiskType: 'Managed'
      }
    ]

    // Linux profile
    linuxProfile: {
      adminUsername: aksAdminUsername
      ssh: {
        publicKeys: [
          {
            keyData: aksAdminPublicKey
          }
        ]
      }
    }

    // Network profile
    networkProfile: {
      networkPlugin: 'azure'
      networkPolicy: 'azure'
      loadBalancerSku: 'standard'
      serviceCidr: '172.16.0.0/16'
      dnsServiceIP: '172.16.0.10'
    }

    // API server access profile
    apiServerAccessProfile: {
      enablePrivateCluster: false
    }

    // Add-ons
    addonProfiles: {
      omsagent: {
        enabled: true
        config: {
          logAnalyticsWorkspaceResourceID: logAnalytics.id
        }
      }
      azurepolicy: {
        enabled: true
      }
      ingressApplicationGateway: {
        enabled: true
        config: {
          applicationGatewayName: '${resourcePrefix}-appgw'
          subnetCIDR: '10.0.2.0/24'
        }
      }
    }

    // Auto-scaler profile
    autoScalerProfile: {
      'balance-similar-node-groups': 'false'
      expander: 'random'
      'max-empty-bulk-delete': '10'
      'max-graceful-termination-sec': '600'
      'max-node-provision-time': '15m'
      'max-total-unready-percentage': '45'
      'new-pod-scale-up-delay': '0s'
      'ok-total-unready-count': '3'
      'scale-down-delay-after-add': '10m'
      'scale-down-delay-after-delete': '10s'
      'scale-down-delay-after-failure': '3m'
      'scale-down-unneeded-time': '10m'
      'scale-down-unready-time': '20m'
      'scale-down-utilization-threshold': '0.5'
      'skip-nodes-with-local-storage': 'false'
      'skip-nodes-with-system-pods': 'true'
    }
  }
}

// Additional node pool for user workloads
resource userNodePool 'Microsoft.ContainerService/managedClusters/agentPools@2023-10-01' = {
  parent: aks
  name: 'userpool'
  properties: {
    count: 2
    vmSize: 'Standard_D8s_v3'
    osType: 'Linux'
    mode: 'User'
    type: 'VirtualMachineScaleSets'
    enableAutoScaling: true
    minCount: 0
    maxCount: 20
    vnetSubnetID: '${vnet.id}/subnets/aks-subnet'
    availabilityZones: ['1', '2', '3']
    maxPods: 110
    osDiskSizeGB: 100
    osDiskType: 'Managed'
    nodeLabels: {
      'node-type': 'user-workload'
    }
    nodeTaints: [
      'workload=user:NoSchedule'
    ]
  }
}

// Role assignment for AKS to pull images from ACR
resource acrPullRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: acr
  name: guid(resourceGroup().id, aks.id, 'acrPull')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d') // AcrPull
    principalId: aks.properties.identityProfile.kubeletidentity.objectId
    principalType: 'ServicePrincipal'
  }
}

// Cosmos DB for microservices data
resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2023-11-15' = {
  name: '${resourcePrefix}-cosmos'
  location: location
  tags: tags
  kind: 'GlobalDocumentDB'
  properties: {
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
    databaseAccountOfferType: 'Standard'
    enableAutomaticFailover: false
    enableMultipleWriteLocations: false
    capabilities: [
      {
        name: 'EnableServerless'
      }
    ]
    backupPolicy: {
      type: 'Periodic'
      periodicModeProperties: {
        backupIntervalInMinutes: 240
        backupRetentionIntervalInHours: 8
        backupStorageRedundancy: 'Local'
      }
    }
  }
}

// Cosmos DB database for orders
resource ordersDatabase 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2023-11-15' = {
  parent: cosmosAccount
  name: 'orders'
  properties: {
    resource: {
      id: 'orders'
    }
  }
}

// Cosmos DB container for orders
resource ordersContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2023-11-15' = {
  parent: ordersDatabase
  name: 'orders'
  properties: {
    resource: {
      id: 'orders'
      partitionKey: {
        paths: ['/customerId']
        kind: 'Hash'
      }
    }
  }
}

// Service Bus namespace for messaging
resource serviceBus 'Microsoft.ServiceBus/namespaces@2021-11-01' = {
  name: '${resourcePrefix}-sb'
  location: location
  tags: tags
  sku: {
    name: 'Standard'
    tier: 'Standard'
  }
  properties: {
    minimumTlsVersion: '1.2'
  }
}

// Service Bus queue for order processing
resource orderQueue 'Microsoft.ServiceBus/namespaces/queues@2021-11-01' = {
  parent: serviceBus
  name: 'order-processing'
  properties: {
    maxSizeInMegabytes: 1024
    defaultMessageTimeToLive: 'P14D'
    lockDuration: 'PT1M'
    maxDeliveryCount: 10
    duplicateDetectionHistoryTimeWindow: 'PT10M'
    enablePartitioning: false
    enableExpress: false
  }
}

// Service Bus topic for events
resource eventTopic 'Microsoft.ServiceBus/namespaces/topics@2021-11-01' = {
  parent: serviceBus
  name: 'events'
  properties: {
    maxSizeInMegabytes: 1024
    defaultMessageTimeToLive: 'P14D'
    duplicateDetectionHistoryTimeWindow: 'PT10M'
    enablePartitioning: false
    enableExpress: false
  }
}

// Service Bus subscription for order events
resource orderEventSubscription 'Microsoft.ServiceBus/namespaces/topics/subscriptions@2021-11-01' = {
  parent: eventTopic
  name: 'order-service'
  properties: {
    maxDeliveryCount: 10
    lockDuration: 'PT1M'
    defaultMessageTimeToLive: 'P14D'
  }
}

// Redis Cache for session state and caching
resource redisCache 'Microsoft.Cache/redis@2023-08-01' = {
  name: '${resourcePrefix}-redis'
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'Premium'
      family: 'P'
      capacity: 1
    }
    minimumTlsVersion: '1.2'
    redisConfiguration: {
      'maxmemory-policy': 'allkeys-lru'
    }
    enableNonSslPort: false
    publicNetworkAccess: 'Enabled'
  }
}

// API Management instance
resource apiManagement 'Microsoft.ApiManagement/service@2023-05-01-preview' = {
  name: '${resourcePrefix}-apim'
  location: location
  tags: tags
  sku: {
    name: 'Developer'
    capacity: 1
  }
  properties: {
    publisherName: 'Microservices Team'
    publisherEmail: 'admin@example.com'
    customProperties: {
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Protocols.Tls10': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Protocols.Tls11': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Protocols.Ssl30': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Backend.Protocols.Tls10': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Backend.Protocols.Tls11': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Backend.Protocols.Ssl30': 'false'
    }
  }
}

// Store sensitive values in Key Vault
resource cosmosConnectionString 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'cosmos-connection-string'
  properties: {
    value: cosmosAccount.listConnectionStrings().connectionStrings[0].connectionString
  }
}

resource serviceBusConnectionString 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'servicebus-connection-string'
  properties: {
    value: listKeys('${serviceBus.id}/AuthorizationRules/RootManageSharedAccessKey', serviceBus.apiVersion).primaryConnectionString
  }
}

resource redisConnectionString 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'redis-connection-string'
  properties: {
    value: '${redisCache.properties.hostName}:${redisCache.properties.sslPort},password=${listKeys(redisCache.id, redisCache.apiVersion).primaryKey},ssl=True,abortConnect=False'
  }
}

// Outputs
output resourceGroupName string = resourceGroup().name
output aksClusterName string = aks.name
output aksClusterFqdn string = aks.properties.fqdn
output acrName string = acr.name
output keyVaultName string = keyVault.name
output cosmosAccountName string = cosmosAccount.name
output serviceBusName string = serviceBus.name
output redisCacheName string = redisCache.name
output apiManagementName string = apiManagement.name
output logAnalyticsWorkspaceName string = logAnalytics.name
output applicationInsightsName string = appInsights.name

// Output connection strings (for reference, actual values stored in Key Vault)
output keyVaultSecrets object = {
  cosmosConnectionString: 'cosmos-connection-string'
  serviceBusConnectionString: 'servicebus-connection-string'
  redisConnectionString: 'redis-connection-string'
}
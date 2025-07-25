# Technical Infrastructure: E-Commerce Platform

## System Architecture Overview

### C4 Model - Level 1: System Context

```mermaid
graph TB
    subgraph External
        Customer[Customer<br/>Web/Mobile]
        Admin[Admin Users<br/>Internal]
        Email[Email Service<br/>SendGrid]
        Payment[Payment Gateway<br/>Stripe]
        CDN[CDN<br/>CloudFlare]
        Analytics[Analytics<br/>Google Analytics]
    end
    
    subgraph "E-Commerce Platform"
        System[E-Commerce System]
    end
    
    Customer -->|Browse, Order| System
    Admin -->|Manage| System
    System -->|Send emails| Email
    System -->|Process payments| Payment
    System -->|Static assets| CDN
    System -->|Track events| Analytics
```

### C4 Model - Level 2: Container Diagram

```mermaid
graph TB
    subgraph "Web Tier"
        UI[React SPA<br/>TypeScript]
        Mobile[Mobile Apps<br/>React Native]
    end
    
    subgraph "API Tier"
        Gateway[API Gateway<br/>Kong]
        GraphQL[GraphQL Server<br/>Apollo]
        REST[REST APIs<br/>Node.js]
    end
    
    subgraph "Service Tier"
        Auth[Auth Service<br/>JWT/OAuth2]
        Catalog[Catalog Service<br/>Node.js]
        Order[Order Service<br/>Node.js]
        Inventory[Inventory Service<br/>Go]
        User[User Service<br/>Node.js]
    end
    
    subgraph "Data Tier"
        PG[(PostgreSQL<br/>Users, Orders)]
        Mongo[(MongoDB<br/>Catalog)]
        Redis[(Redis<br/>Cache, Sessions)]
        Elastic[(Elasticsearch<br/>Search, Logs)]
    end
    
    subgraph "Infrastructure"
        Queue[RabbitMQ<br/>Message Queue]
        Storage[S3<br/>Object Storage]
    end
    
    UI --> Gateway
    Mobile --> Gateway
    Gateway --> GraphQL
    Gateway --> REST
    GraphQL --> Auth
    GraphQL --> Catalog
    GraphQL --> Order
    REST --> Auth
    REST --> User
    Order --> Queue
    Inventory --> Queue
    
    Auth --> Redis
    User --> PG
    Order --> PG
    Catalog --> Mongo
    Inventory --> PG
    Order --> Storage
```

## Infrastructure Architecture

### AWS Cloud Architecture

```python
# Diagram as Code using Python diagrams library
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import ECS, Lambda
from diagrams.aws.database import RDS, ElastiCache, DocumentDB
from diagrams.aws.network import ELB, CloudFront, Route53
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.analytics import Elasticsearch
from diagrams.aws.security import WAF

with Diagram("E-Commerce AWS Infrastructure", show=False):
    dns = Route53("DNS")
    cdn = CloudFront("CDN")
    waf = WAF("WAF")
    
    with Cluster("VPC"):
        with Cluster("Public Subnet"):
            alb = ELB("Application LB")
        
        with Cluster("Private Subnet - Web Tier"):
            web = ECS("Web Containers")
        
        with Cluster("Private Subnet - App Tier"):
            api = ECS("API Containers")
            workers = Lambda("Background Jobs")
        
        with Cluster("Private Subnet - Data Tier"):
            db_primary = RDS("PostgreSQL Primary")
            db_replica = RDS("PostgreSQL Replica")
            cache = ElastiCache("Redis Cluster")
            nosql = DocumentDB("MongoDB")
            search = Elasticsearch("Search Cluster")
    
    with Cluster("Storage"):
        static_assets = S3("Static Assets")
        user_uploads = S3("User Uploads")
        backups = S3("Backups")
    
    with Cluster("Integration"):
        queue = SQS("Job Queue")
        events = SNS("Event Bus")
    
    # Connections
    dns >> cdn >> waf >> alb
    alb >> web >> api
    api >> cache
    api >> db_primary
    db_primary - Edge(style="dashed") - db_replica
    api >> nosql
    api >> search
    api >> queue >> workers
    api >> events
    web >> static_assets
    api >> user_uploads
```

### Network Architecture

```mermaid
graph TB
    subgraph Internet
        Users[Users]
        CloudFlare[CloudFlare CDN]
    end
    
    subgraph "AWS Region: us-east-1"
        subgraph "VPC: 10.0.0.0/16"
            subgraph "Public Subnets"
                subgraph "us-east-1a: 10.0.1.0/24"
                    ALB1[ALB Instance 1]
                    NAT1[NAT Gateway 1]
                end
                subgraph "us-east-1b: 10.0.2.0/24"
                    ALB2[ALB Instance 2]
                    NAT2[NAT Gateway 2]
                end
            end
            
            subgraph "Private Subnets - Web"
                subgraph "us-east-1a: 10.0.11.0/24"
                    Web1[Web Servers]
                end
                subgraph "us-east-1b: 10.0.12.0/24"
                    Web2[Web Servers]
                end
            end
            
            subgraph "Private Subnets - App"
                subgraph "us-east-1a: 10.0.21.0/24"
                    App1[App Servers]
                end
                subgraph "us-east-1b: 10.0.22.0/24"
                    App2[App Servers]
                end
            end
            
            subgraph "Private Subnets - Data"
                subgraph "us-east-1a: 10.0.31.0/24"
                    DB1[RDS Primary]
                    Cache1[Redis Primary]
                end
                subgraph "us-east-1b: 10.0.32.0/24"
                    DB2[RDS Standby]
                    Cache2[Redis Replica]
                end
            end
        end
    end
    
    Users --> CloudFlare
    CloudFlare --> ALB1
    CloudFlare --> ALB2
    ALB1 --> Web1
    ALB2 --> Web2
    Web1 --> App1
    Web2 --> App2
    App1 --> DB1
    App2 --> DB1
    App1 --> Cache1
```

## Technology Stack

### Application Stack
| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Frontend | React | 18.2.0 | SPA framework |
| Mobile | React Native | 0.72.0 | Cross-platform mobile |
| API Gateway | Kong | 3.4.0 | API management |
| GraphQL | Apollo Server | 4.9.0 | GraphQL server |
| Backend | Node.js | 20.10.0 | JavaScript runtime |
| Framework | Express | 4.18.0 | Web framework |
| Language | TypeScript | 5.3.0 | Type safety |

### Data Stack
| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Primary DB | PostgreSQL | 15.4 | Relational data |
| NoSQL DB | MongoDB | 7.0 | Document store |
| Cache | Redis | 7.2 | Caching & sessions |
| Search | Elasticsearch | 8.11 | Full-text search |
| Queue | RabbitMQ | 3.12 | Message broker |

### Infrastructure Stack
| Component | Technology | Purpose |
|-----------|------------|---------|
| Cloud | AWS | Cloud provider |
| Containers | Docker | Containerization |
| Orchestration | ECS Fargate | Container orchestration |
| CI/CD | GitHub Actions | Automation |
| IaC | Terraform | Infrastructure as Code |
| Monitoring | Datadog | Observability |

## Deployment Architecture

### Container Deployment

```yaml
# docker-compose.yml for local development
version: '3.8'

services:
  web:
    build: ./web
    ports:
      - "3000:3000"
    environment:
      - API_URL=http://api:4000
    depends_on:
      - api

  api:
    build: ./api
    ports:
      - "4000:4000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=db
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
  labels:
    app: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: myregistry/api:latest
        ports:
        - containerPort: 4000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: redis-config
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 4000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 4000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Security Architecture

### Security Layers

```mermaid
graph TB
    subgraph "External Protection"
        DDoS[DDoS Protection<br/>CloudFlare]
        WAF[Web Application Firewall<br/>AWS WAF]
        CDN[CDN Security<br/>CloudFlare]
    end
    
    subgraph "Network Security"
        VPC[VPC Isolation]
        SG[Security Groups]
        NACL[Network ACLs]
        TLS[TLS 1.3]
    end
    
    subgraph "Application Security"
        Auth[Authentication<br/>JWT/OAuth2]
        AuthZ[Authorization<br/>RBAC]
        Input[Input Validation]
        CSRF[CSRF Protection]
    end
    
    subgraph "Data Security"
        Encrypt[Encryption at Rest<br/>AES-256]
        Transit[Encryption in Transit<br/>TLS]
        PII[PII Protection]
        Backup[Backup Encryption]
    end
    
    DDoS --> WAF --> CDN
    CDN --> VPC
    VPC --> SG --> NACL
    TLS --> Auth --> AuthZ
    Input --> CSRF
    Encrypt --> Transit --> PII --> Backup
```

### Security Controls

| Layer | Control | Implementation |
|-------|---------|----------------|
| Network | Firewall | AWS Security Groups |
| Network | DDoS Protection | CloudFlare |
| Application | Authentication | JWT with refresh tokens |
| Application | Authorization | Role-based (RBAC) |
| Application | Rate Limiting | Kong API Gateway |
| Data | Encryption at Rest | AWS KMS |
| Data | Encryption in Transit | TLS 1.3 |
| Data | PII Protection | Field-level encryption |
| Compliance | PCI DSS | Tokenization |
| Compliance | GDPR | Data anonymization |

## Monitoring & Observability

### Monitoring Stack

```mermaid
graph LR
    subgraph "Data Sources"
        Apps[Applications]
        Infra[Infrastructure]
        Network[Network]
        Security[Security]
    end
    
    subgraph "Collection"
        Agent[Datadog Agent]
        APM[APM Agent]
        Logs[Log Forwarder]
    end
    
    subgraph "Storage & Processing"
        Metrics[(Metrics Store)]
        Traces[(Trace Store)]
        LogStore[(Log Store)]
    end
    
    subgraph "Visualization"
        Dash[Dashboards]
        Alert[Alerts]
        Report[Reports]
    end
    
    Apps --> APM --> Traces
    Infra --> Agent --> Metrics
    Network --> Agent --> Metrics
    Security --> Logs --> LogStore
    
    Metrics --> Dash
    Traces --> Dash
    LogStore --> Dash
    
    Dash --> Alert
    Dash --> Report
```

### Key Metrics

| Category | Metric | Target | Alert Threshold |
|----------|--------|--------|-----------------|
| Availability | Uptime | 99.9% | < 99.5% |
| Performance | API Response Time | < 200ms | > 500ms |
| Performance | Page Load Time | < 2s | > 3s |
| Capacity | CPU Utilization | < 70% | > 85% |
| Capacity | Memory Usage | < 80% | > 90% |
| Error Rate | 5xx Errors | < 0.1% | > 0.5% |
| Business | Orders/Hour | > 100 | < 50 |

## Disaster Recovery

### Backup Strategy

```mermaid
graph TB
    subgraph "Production"
        ProdDB[(Production DB)]
        ProdFiles[File Storage]
        ProdConfig[Configuration]
    end
    
    subgraph "Backup Schedule"
        Hourly[Hourly Snapshots<br/>Retention: 24h]
        Daily[Daily Backups<br/>Retention: 7d]
        Weekly[Weekly Backups<br/>Retention: 4w]
        Monthly[Monthly Backups<br/>Retention: 12m]
    end
    
    subgraph "Backup Storage"
        S3Primary[S3 Primary Region]
        S3Secondary[S3 DR Region]
        Glacier[Glacier Archive]
    end
    
    ProdDB --> Hourly --> S3Primary
    ProdDB --> Daily --> S3Primary
    ProdDB --> Weekly --> S3Secondary
    ProdDB --> Monthly --> Glacier
    
    ProdFiles --> Daily --> S3Primary
    ProdFiles --> Weekly --> S3Secondary
    
    ProdConfig --> Daily --> S3Primary
```

### RTO/RPO Targets

| System Component | RTO | RPO | Strategy |
|-----------------|-----|-----|----------|
| Database | 1 hour | 15 minutes | Multi-AZ with automated failover |
| Application | 30 minutes | 0 minutes | Stateless with auto-scaling |
| File Storage | 2 hours | 1 hour | Cross-region replication |
| Full System | 4 hours | 1 hour | Automated DR runbook |

## Capacity Planning

### Current Usage

```mermaid
graph TB
    subgraph "Daily Pattern"
        Morning[6AM-12PM<br/>60% capacity]
        Peak[12PM-8PM<br/>95% capacity]
        Evening[8PM-12AM<br/>70% capacity]
        Night[12AM-6AM<br/>30% capacity]
    end
    
    Morning --> Peak
    Peak --> Evening
    Evening --> Night
    Night --> Morning
```

### Growth Projections

| Metric | Current | 6 Months | 12 Months | Scale Strategy |
|--------|---------|----------|-----------|----------------|
| Daily Users | 50K | 75K | 120K | Auto-scaling |
| Orders/Day | 5K | 8K | 15K | Database sharding |
| Data Volume | 2TB | 3.5TB | 6TB | Archival strategy |
| API Calls/Day | 10M | 18M | 35M | Caching optimization |

## Cost Optimization

### Resource Allocation

```mermaid
pie title Monthly AWS Costs ($10,000)
    "Compute (ECS)" : 3500
    "Database (RDS)" : 2000
    "Storage (S3)" : 1000
    "Network (CloudFront)" : 1500
    "Monitoring" : 500
    "Other" : 1500
```

### Optimization Strategies

1. **Compute Optimization**
   - Use Spot instances for batch processing
   - Right-size instances based on metrics
   - Implement auto-scaling policies

2. **Storage Optimization**
   - Lifecycle policies for S3
   - Compress old logs
   - Use Glacier for archives

3. **Database Optimization**
   - Read replicas for reporting
   - Connection pooling
   - Query optimization

## Infrastructure as Code

### Terraform Configuration

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# VPC Configuration
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "ecommerce-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = true
  
  tags = {
    Environment = "production"
    Project     = "ecommerce"
  }
}

# RDS Configuration
resource "aws_db_instance" "postgres" {
  identifier = "ecommerce-db"
  
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.r6g.large"
  
  allocated_storage     = 100
  max_allocated_storage = 1000
  storage_encrypted     = true
  
  db_name  = "ecommerce"
  username = "dbadmin"
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  multi_az               = true
  deletion_protection    = true
  
  tags = {
    Environment = "production"
    Project     = "ecommerce"
  }
}
```

## Appendices

### A. Service Endpoints

| Service | Internal Endpoint | External Endpoint |
|---------|------------------|-------------------|
| Web App | http://web.internal:3000 | https://app.example.com |
| API Gateway | http://gateway.internal:8000 | https://api.example.com |
| GraphQL | http://graphql.internal:4000 | https://api.example.com/graphql |
| Admin | http://admin.internal:3001 | https://admin.example.com |

### B. Configuration Management

All environment-specific configurations stored in:
- AWS Systems Manager Parameter Store
- Encrypted with KMS
- Accessed via IAM roles
- Audited through CloudTrail

### C. Runbooks

1. [Deployment Runbook](./runbooks/deployment.md)
2. [Incident Response Runbook](./runbooks/incident-response.md)
3. [Scaling Runbook](./runbooks/scaling.md)
4. [Disaster Recovery Runbook](./runbooks/disaster-recovery.md)
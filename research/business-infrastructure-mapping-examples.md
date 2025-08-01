# Business to Infrastructure Mapping Examples

## Visual Mapping Patterns for ArchiMate-C4 Integration

### Example 1: E-Commerce Platform Business-to-Infrastructure Mapping

#### Business Capability View (ArchiMate)

```mermaid
graph TB
    subgraph Business Layer
        BA[Customer<br/>Business Actor]
        BR[Online Shopper<br/>Business Role]
        BS[E-Commerce<br/>Business Service]
        BP1[Order Fulfillment<br/>Business Process]
        BP2[Customer Support<br/>Business Process]
        BC1[Product Catalog<br/>Management]
        BC2[Order Processing]
        BC3[Payment Processing]
        BC4[Inventory Management]
    end
    
    BA --> BR
    BR --> BS
    BS --> BP1
    BS --> BP2
    BP1 --> BC1
    BP1 --> BC2
    BP1 --> BC3
    BP1 --> BC4
```

#### Application Component Mapping (C4 Level 2 - Containers)

```mermaid
graph TB
    subgraph External
        U[User]
        PS[Payment Service<br/>External]
        SS[Shipping Service<br/>External]
    end
    
    subgraph E-Commerce System
        WA[Web Application<br/>React/TypeScript]
        AG[API Gateway<br/>Kong]
        
        subgraph Core Services
            PCS[Product Catalog Service<br/>Java/Spring Boot]
            OMS[Order Management Service<br/>Node.js/Express]
            IMS[Inventory Service<br/>Python/FastAPI]
            CMS[Customer Service<br/>Java/Spring Boot]
        end
        
        subgraph Data Stores
            PDB[(Product DB<br/>PostgreSQL)]
            ODB[(Order DB<br/>PostgreSQL)]
            IDB[(Inventory DB<br/>MongoDB)]
            CDB[(Customer DB<br/>PostgreSQL)]
            RC[(Redis Cache)]
        end
        
        MB[Message Broker<br/>Kafka]
    end
    
    U --> WA
    WA --> AG
    AG --> PCS
    AG --> OMS
    AG --> CMS
    OMS --> IMS
    OMS --> PS
    OMS --> SS
    
    PCS --> PDB
    OMS --> ODB
    IMS --> IDB
    CMS --> CDB
    
    OMS --> MB
    IMS --> MB
    PCS --> RC
```

#### Traceability Matrix

| Business Capability | Business Process | Application Service | Microservice | Technology Stack |
|-------------------|------------------|-------------------|--------------|------------------|
| Product Catalog Management | Browse Products | Product Search API | product-catalog-service | Java/Spring Boot, PostgreSQL, ElasticSearch |
| Order Processing | Order Fulfillment | Order Management API | order-management-service | Node.js, PostgreSQL, Redis |
| Payment Processing | Payment Validation | Payment Gateway API | payment-service (external) | 3rd Party Integration |
| Inventory Management | Stock Control | Inventory API | inventory-service | Python/FastAPI, MongoDB |
| Customer Support | Issue Resolution | Support API | customer-service | Java/Spring Boot, PostgreSQL |

### Example 2: Banking System Domain Mapping

#### Value Stream to Service Mapping

```mermaid
graph LR
    subgraph Value Streams
        VS1[Account Opening]
        VS2[Loan Processing]
        VS3[Payment Processing]
        VS4[Fraud Detection]
    end
    
    subgraph Business Domains
        BD1[Customer Domain]
        BD2[Account Domain]
        BD3[Lending Domain]
        BD4[Payment Domain]
        BD5[Risk Domain]
    end
    
    subgraph Microservices
        MS1[customer-service]
        MS2[account-service]
        MS3[kyc-service]
        MS4[loan-service]
        MS5[credit-scoring-service]
        MS6[payment-service]
        MS7[fraud-detection-service]
    end
    
    VS1 --> BD1
    VS1 --> BD2
    VS2 --> BD3
    VS2 --> BD5
    VS3 --> BD4
    VS4 --> BD5
    
    BD1 --> MS1
    BD1 --> MS3
    BD2 --> MS2
    BD3 --> MS4
    BD3 --> MS5
    BD4 --> MS6
    BD5 --> MS7
```

#### Cross-Functional Team Structure

```mermaid
graph TB
    subgraph Platform Teams
        PT1[API Platform Team]
        PT2[Data Platform Team]
        PT3[Security Platform Team]
        PT4[DevOps Platform Team]
    end
    
    subgraph Domain Teams
        subgraph Customer Domain Team
            CDT1[Product Owner]
            CDT2[Tech Lead]
            CDT3[3 Backend Devs]
            CDT4[2 Frontend Devs]
            CDT5[1 QA Engineer]
            CDT6[1 DevOps Engineer]
        end
        
        subgraph Payment Domain Team
            PDT1[Product Owner]
            PDT2[Tech Lead]
            PDT3[4 Backend Devs]
            PDT4[1 Frontend Dev]
            PDT5[2 QA Engineers]
            PDT6[1 DevOps Engineer]
        end
    end
    
    subgraph Services Owned
        CS[customer-service]
        KS[kyc-service]
        PS[payment-service]
        FS[fraud-detection-service]
    end
    
    Customer Domain Team --> CS
    Customer Domain Team --> KS
    Payment Domain Team --> PS
    Payment Domain Team --> FS
    
    Platform Teams -.-> Domain Teams
```

### Example 3: Event-Driven Architecture Pattern

#### Business Event Flow

```mermaid
graph TB
    subgraph Business Events
        BE1[Customer Registered]
        BE2[Order Placed]
        BE3[Payment Received]
        BE4[Inventory Updated]
        BE5[Order Shipped]
    end
    
    subgraph Event Streams
        ES1[customer-events]
        ES2[order-events]
        ES3[payment-events]
        ES4[inventory-events]
        ES5[shipping-events]
    end
    
    subgraph Services
        S1[Customer Service]
        S2[Order Service]
        S3[Payment Service]
        S4[Inventory Service]
        S5[Shipping Service]
        S6[Notification Service]
        S7[Analytics Service]
    end
    
    BE1 --> ES1
    BE2 --> ES2
    BE3 --> ES3
    BE4 --> ES4
    BE5 --> ES5
    
    S1 --> ES1
    S2 --> ES2
    S3 --> ES3
    S4 --> ES4
    S5 --> ES5
    
    ES1 --> S6
    ES2 --> S4
    ES2 --> S6
    ES3 --> S2
    ES3 --> S7
    ES4 --> S2
    ES5 --> S6
```

#### Integration Architecture

```mermaid
graph TB
    subgraph Synchronous Layer
        AG[API Gateway]
        SR[Service Registry<br/>Consul]
        CB[Circuit Breaker<br/>Hystrix]
    end
    
    subgraph Asynchronous Layer
        KB[Kafka Broker]
        SC[Schema Registry]
        KS[Kafka Streams]
    end
    
    subgraph Data Layer
        OD[Operational Data<br/>PostgreSQL]
        AD[Analytical Data<br/>Data Lake]
        CD[Cache Data<br/>Redis]
    end
    
    subgraph Services
        MS1[Microservice 1]
        MS2[Microservice 2]
        MS3[Microservice 3]
    end
    
    MS1 --> AG
    MS2 --> AG
    MS3 --> AG
    
    AG --> SR
    AG --> CB
    
    MS1 --> KB
    MS2 --> KB
    MS3 --> KB
    
    KB --> KS
    KB --> SC
    
    MS1 --> OD
    MS2 --> OD
    MS3 --> CD
    
    KS --> AD
```

### Example 4: Technology Stack Alignment

#### Business to Technology Mapping

```yaml
Business_Domain: Customer_Experience
  Business_Capabilities:
    - Customer_Onboarding:
        Services:
          - registration-service
          - kyc-service
          - document-service
        Technology:
          Frontend: React, TypeScript, Next.js
          Backend: Node.js, Express, GraphQL
          Database: PostgreSQL, S3
          Infrastructure: AWS ECS, ALB
          
    - Customer_Profile_Management:
        Services:
          - profile-service
          - preferences-service
          - notification-service
        Technology:
          Frontend: React Native (Mobile)
          Backend: Java, Spring Boot
          Database: DynamoDB, ElasticSearch
          Infrastructure: AWS Lambda, API Gateway
          
    - Customer_Support:
        Services:
          - ticketing-service
          - chat-service
          - knowledge-base-service
        Technology:
          Frontend: Vue.js, Tailwind CSS
          Backend: Python, FastAPI
          Database: MongoDB, Redis
          Infrastructure: Kubernetes, Istio
```

#### Infrastructure Topology

```mermaid
graph TB
    subgraph AWS Cloud
        subgraph Region US-East-1
            subgraph VPC
                subgraph Public Subnet
                    ALB[Application<br/>Load Balancer]
                    NAT[NAT Gateway]
                end
                
                subgraph Private Subnet A
                    ECS1[ECS Cluster 1<br/>Customer Services]
                    RDS1[(RDS<br/>PostgreSQL)]
                end
                
                subgraph Private Subnet B
                    ECS2[ECS Cluster 2<br/>Order Services]
                    DDB[(DynamoDB)]
                end
                
                subgraph Private Subnet C
                    EKS[EKS Cluster<br/>Analytics Services]
                    ES[(ElasticSearch)]
                end
            end
        end
        
        subgraph Managed Services
            S3[S3 Buckets]
            SQS[SQS Queues]
            SNS[SNS Topics]
            CW[CloudWatch]
        end
    end
    
    Internet --> ALB
    ALB --> ECS1
    ALB --> ECS2
    ALB --> EKS
    ECS1 --> RDS1
    ECS2 --> DDB
    EKS --> ES
    ECS1 --> NAT
    ECS2 --> NAT
    NAT --> Internet
```

### Example 5: Data Flow Architecture

#### Master Data Management Pattern

```mermaid
graph LR
    subgraph Source Systems
        CRM[CRM System]
        ERP[ERP System]
        WEB[Web Platform]
        MOB[Mobile App]
    end
    
    subgraph Integration Layer
        CDC[Change Data<br/>Capture]
        ETL[ETL Pipeline]
        API[API Gateway]
    end
    
    subgraph Master Data Hub
        MDM[Master Data<br/>Management]
        GR[Golden Record]
        DQ[Data Quality]
        DS[Data Steward UI]
    end
    
    subgraph Consumers
        AS[Analytics Service]
        RS[Reporting Service]
        MS[Microservices]
        DW[Data Warehouse]
    end
    
    CRM --> CDC
    ERP --> ETL
    WEB --> API
    MOB --> API
    
    CDC --> MDM
    ETL --> MDM
    API --> MDM
    
    MDM --> GR
    MDM --> DQ
    DQ --> DS
    
    GR --> AS
    GR --> RS
    GR --> MS
    GR --> DW
```

## Implementation Patterns

### Pattern 1: Strangler Fig Migration

```mermaid
graph TB
    subgraph Phase 1 - Initial State
        M1[Monolith]
        DB1[(Monolith DB)]
        U1[Users] --> M1
        M1 --> DB1
    end
    
    subgraph Phase 2 - First Service Extraction
        M2[Monolith]
        MS1[Customer Service]
        DB2[(Monolith DB)]
        DB3[(Customer DB)]
        AG1[API Gateway]
        U2[Users] --> AG1
        AG1 --> M2
        AG1 --> MS1
        M2 --> DB2
        MS1 --> DB3
    end
    
    subgraph Phase 3 - Multiple Services
        M3[Reduced Monolith]
        MS2[Customer Service]
        MS3[Order Service]
        MS4[Inventory Service]
        DB4[(Legacy DB)]
        DB5[(Customer DB)]
        DB6[(Order DB)]
        DB7[(Inventory DB)]
        AG2[API Gateway]
        U3[Users] --> AG2
        AG2 --> M3
        AG2 --> MS2
        AG2 --> MS3
        AG2 --> MS4
        M3 --> DB4
        MS2 --> DB5
        MS3 --> DB6
        MS4 --> DB7
    end
```

### Pattern 2: CQRS Implementation

```mermaid
graph TB
    subgraph Write Side
        CMD[Commands]
        WM[Write Model]
        ES[Event Store]
        EP[Event Publisher]
    end
    
    subgraph Read Side
        Q[Queries]
        RM1[Read Model 1<br/>Customer View]
        RM2[Read Model 2<br/>Order View]
        RM3[Read Model 3<br/>Analytics View]
        RDB1[(Customer<br/>Read DB)]
        RDB2[(Order<br/>Read DB)]
        RDB3[(Analytics<br/>Read DB)]
    end
    
    subgraph Event Processing
        EB[Event Bus]
        P1[Projection 1]
        P2[Projection 2]
        P3[Projection 3]
    end
    
    CMD --> WM
    WM --> ES
    ES --> EP
    EP --> EB
    
    EB --> P1
    EB --> P2
    EB --> P3
    
    P1 --> RDB1
    P2 --> RDB2
    P3 --> RDB3
    
    Q --> RM1
    Q --> RM2
    Q --> RM3
    
    RM1 --> RDB1
    RM2 --> RDB2
    RM3 --> RDB3
```

## Governance and Compliance Mapping

### Service Ownership Matrix

| Service | Business Owner | Technical Owner | Domain Team | SLA | Compliance |
|---------|---------------|-----------------|-------------|-----|------------|
| customer-service | VP Customer Experience | Tech Lead - Customer | Customer Domain Team | 99.9% | GDPR, CCPA |
| payment-service | CFO | Tech Lead - Payments | Payment Domain Team | 99.99% | PCI-DSS |
| order-service | VP Operations | Tech Lead - Commerce | Commerce Domain Team | 99.9% | SOX |
| inventory-service | VP Supply Chain | Tech Lead - Inventory | Supply Chain Team | 99.5% | ISO 27001 |

### Architecture Decision Records (ADR) Template

```markdown
# ADR-001: Microservice Decomposition Strategy

## Status
Accepted

## Context
Need to decompose monolithic e-commerce platform into microservices

## Decision
Use business capability mapping with bounded contexts from DDD

## Consequences
- Clear service boundaries aligned with business
- Each team owns specific business capabilities
- Requires investment in service mesh and monitoring
- Initial complexity increase, long-term maintainability improvement
```

## Monitoring and Observability

### Service Dependency Dashboard

```mermaid
graph TB
    subgraph Service Health
        SH1[customer-service<br/>✅ Healthy<br/>Latency: 45ms]
        SH2[order-service<br/>⚠️ Degraded<br/>Latency: 250ms]
        SH3[payment-service<br/>✅ Healthy<br/>Latency: 120ms]
        SH4[inventory-service<br/>❌ Down<br/>Latency: N/A]
    end
    
    subgraph Dependencies
        SH1 --> SH2
        SH2 --> SH3
        SH2 --> SH4
    end
    
    subgraph Metrics
        M1[Request Rate: 1.2K/s]
        M2[Error Rate: 0.05%]
        M3[Avg Latency: 105ms]
        M4[Active Connections: 3,421]
    end
```

This comprehensive set of examples demonstrates how to effectively map business capabilities to technical infrastructure using ArchiMate and C4 models, following patterns successfully implemented by leading technology companies.
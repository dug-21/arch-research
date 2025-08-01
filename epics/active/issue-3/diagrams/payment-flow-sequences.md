# Payment System Flow Diagrams

## 1. Standard Payment Authorization Flow

```mermaid
sequenceDiagram
    participant M as Merchant
    participant PG as Payment Gateway
    participant PE as Processing Engine
    participant RD as Risk Detection
    participant P as Processor/Bank
    participant TV as Token Vault
    
    M->>PG: Payment Request (Card Details)
    PG->>PG: Validate Request
    PG->>TV: Tokenize Card Data
    TV-->>PG: Token Generated
    
    PG->>PE: Process Transaction (Token)
    PE->>RD: Risk Assessment
    RD->>RD: ML Scoring + Rules
    RD-->>PE: Risk Score
    
    alt Low Risk
        PE->>P: Authorization Request
        P-->>PE: Authorization Response
        PE-->>PG: Success Response
        PG-->>M: Payment Approved
    else High Risk
        PE-->>PG: Declined (Risk)
        PG-->>M: Payment Declined
    end
```

## 2. Settlement and Reconciliation Flow

```mermaid
sequenceDiagram
    participant PE as Processing Engine
    participant SQ as Settlement Queue
    participant BP as Batch Processor
    participant SC as Settlement Calculator
    participant FG as File Generator
    participant B as Bank/Processor
    participant RE as Reconciliation Engine
    
    Note over PE,SQ: End of Day Process
    PE->>SQ: Queue Authorized Transactions
    
    SQ->>BP: Trigger Batch Processing
    BP->>BP: Apply Cut-off Rules
    BP->>SC: Calculate Net Positions
    
    SC->>SC: Group by Merchant
    SC->>SC: Apply Fees & Reserves
    SC->>FG: Settlement Records
    
    FG->>FG: Generate Settlement Files
    FG->>B: Send Settlement Files
    
    B-->>RE: Confirmation Files
    RE->>RE: Match Transactions
    RE->>RE: Identify Exceptions
    
    alt Matched
        RE-->>BP: Settlement Complete
    else Exception
        RE-->>BP: Investigation Required
    end
```

## 3. Tokenization and Security Flow

```mermaid
flowchart TB
    subgraph "Tokenization Process"
        CD[Card Data] --> TV{Token Vault}
        TV --> |New Card| TG[Token Generator]
        TV --> |Existing| TL[Token Lookup]
        TG --> HSM[Hardware Security Module]
        HSM --> ET[Encrypted Token]
        TL --> ET
        ET --> SD[Secure Database]
    end
    
    subgraph "De-tokenization Process"
        RT[Request with Token] --> VA[Validate Access]
        VA --> |Authorized| TV2{Token Vault}
        VA --> |Unauthorized| DENY[Access Denied]
        TV2 --> DT[Decrypt Token]
        DT --> HSM2[HSM Decryption]
        HSM2 --> PAN[Card Number]
    end
    
    subgraph "Security Layers"
        NI[Network Isolation]
        AC[Access Control]
        AL[Audit Logging]
        KR[Key Rotation]
    end
```

## 4. Fraud Detection Decision Flow

```mermaid
flowchart TB
    T[Transaction] --> FE[Feature Extraction]
    
    FE --> ML[ML Models]
    FE --> RE[Rule Engine]
    FE --> VC[Velocity Checks]
    FE --> BA[Behavioral Analysis]
    
    ML --> |Score: 0-100| AS[Aggregation Service]
    RE --> |Pass/Fail + Score| AS
    VC --> |Velocity Score| AS
    BA --> |Anomaly Score| AS
    
    AS --> FS{Final Score}
    
    FS --> |Score < 30| APPROVE[Auto Approve]
    FS --> |30 <= Score < 70| REVIEW[Manual Review]
    FS --> |Score >= 70| DECLINE[Auto Decline]
    
    REVIEW --> CM[Case Management]
    CM --> |Investigate| DECISION[Human Decision]
```

## 5. Microservices Communication Flow

```mermaid
graph TB
    subgraph "API Gateway Layer"
        AG[API Gateway]
    end
    
    subgraph "Service Mesh"
        AG --> LB[Load Balancer]
        LB --> PS[Payment Service]
        LB --> AS[Auth Service]
        LB --> FS[Fraud Service]
        LB --> SS[Settlement Service]
        
        PS <--> MQ[Message Queue]
        AS <--> MQ
        FS <--> MQ
        SS <--> MQ
    end
    
    subgraph "Data Layer"
        PS --> PDB[(Payment DB)]
        AS --> ADB[(Auth DB)]
        FS --> FDB[(Fraud DB)]
        SS --> SDB[(Settlement DB)]
        
        MQ --> EL[Event Log]
        EL --> ES[(Event Store)]
    end
    
    subgraph "External Services"
        PS --> P1[Processor 1]
        PS --> P2[Processor 2]
        FS --> ML[ML Platform]
        SS --> BK[Bank APIs]
    end
```

## 6. Payment Retry and Failover Flow

```mermaid
stateDiagram-v2
    [*] --> InitialRequest
    InitialRequest --> Validation
    
    Validation --> Authorized: Valid
    Validation --> Rejected: Invalid
    
    Authorized --> Processing
    Processing --> PrimaryProcessor
    
    PrimaryProcessor --> Success: Approved
    PrimaryProcessor --> SoftDecline: Retry Eligible
    PrimaryProcessor --> HardDecline: Not Retryable
    PrimaryProcessor --> Timeout: No Response
    
    SoftDecline --> RetryLogic
    Timeout --> RetryLogic
    
    RetryLogic --> SecondaryProcessor: Failover
    SecondaryProcessor --> Success: Approved
    SecondaryProcessor --> Failed: All Attempts Failed
    
    Success --> Captured
    Captured --> Settled
    Settled --> [*]
    
    Failed --> [*]
    HardDecline --> [*]
    Rejected --> [*]
```

## 7. Event-Driven Architecture Flow

```mermaid
graph LR
    subgraph "Event Producers"
        PE[Payment Engine] --> |Payment Events| EB{Event Bus}
        RD[Risk Detection] --> |Risk Events| EB
        SS[Settlement Service] --> |Settlement Events| EB
    end
    
    subgraph "Event Bus (Kafka)"
        EB --> T1[payment.authorized]
        EB --> T2[payment.captured]
        EB --> T3[risk.flagged]
        EB --> T4[settlement.completed]
    end
    
    subgraph "Event Consumers"
        T1 --> NS[Notification Service]
        T1 --> RS[Reporting Service]
        T2 --> IS[Inventory Service]
        T3 --> CM[Case Management]
        T4 --> AS[Accounting Service]
    end
    
    subgraph "Event Storage"
        EB --> ES[(Event Store)]
        ES --> AN[Analytics]
        ES --> AU[Audit Trail]
    end
```

## 8. Multi-Currency Processing Flow

```mermaid
flowchart TB
    TR[Transaction Request] --> CD{Currency Detection}
    
    CD --> |Same Currency| DP[Direct Processing]
    CD --> |Different Currency| FX[FX Service]
    
    FX --> RQ[Rate Quote]
    RQ --> |Current Rates| RP[Rate Provider]
    RP --> CC[Currency Conversion]
    
    CC --> MF[Markup & Fees]
    MF --> CT[Converted Transaction]
    
    DP --> PE[Processing Engine]
    CT --> PE
    
    PE --> AR[Authorization Request]
    AR --> |Original Currency| P1[Processor]
    
    P1 --> |Response| RC[Response Conversion]
    RC --> |Display Currency| MR[Merchant Response]
    
    subgraph "Settlement"
        PE --> SC[Settlement Calculation]
        SC --> |By Currency| CB[Currency Buckets]
        CB --> SF[Settlement Files]
    end
```

## 9. PCI Compliance Architecture

```mermaid
graph TB
    subgraph "Cardholder Data Environment (CDE)"
        style CDE fill:#ff9999
        TV[Token Vault]
        HSM[Hardware Security Module]
        SDB[(Secure Database)]
    end
    
    subgraph "DMZ"
        style DMZ fill:#ffcc99
        WAF[Web Application Firewall]
        AG[API Gateway]
        TLS[TLS Termination]
    end
    
    subgraph "Application Zone"
        style Application Zone fill:#99ccff
        PS[Payment Service]
        AS[Auth Service]
        RE[Reporting Service]
    end
    
    subgraph "External"
        M[Merchants]
        P[Processors]
    end
    
    M --> WAF
    WAF --> AG
    AG --> TLS
    TLS --> PS
    
    PS -.->|Tokens Only| TV
    PS --> P
    
    AS -.->|No Card Data| PS
    RE -.->|No Card Data| PS
    
    TV <--> HSM
    HSM <--> SDB
```

## 10. High Availability Architecture

```mermaid
graph TB
    subgraph "Region 1 (Primary)"
        LB1[Load Balancer]
        PG1[Payment Gateway 1]
        PG2[Payment Gateway 2]
        DB1[(Primary DB)]
        C1[Cache Layer]
    end
    
    subgraph "Region 2 (Secondary)"
        LB2[Load Balancer]
        PG3[Payment Gateway 3]
        PG4[Payment Gateway 4]
        DB2[(Replica DB)]
        C2[Cache Layer]
    end
    
    subgraph "Global Services"
        GSLB[Global Load Balancer]
        MQ[Message Queue Cluster]
        MS[Monitoring Service]
    end
    
    GSLB --> LB1
    GSLB --> LB2
    
    LB1 --> PG1
    LB1 --> PG2
    LB2 --> PG3
    LB2 --> PG4
    
    PG1 --> DB1
    PG2 --> DB1
    PG3 --> DB2
    PG4 --> DB2
    
    DB1 -.->|Replication| DB2
    
    PG1 --> C1
    PG2 --> C1
    PG3 --> C2
    PG4 --> C2
    
    PG1 --> MQ
    PG2 --> MQ
    PG3 --> MQ
    PG4 --> MQ
    
    MS --> PG1
    MS --> PG2
    MS --> PG3
    MS --> PG4
```

## Usage Notes

These diagrams illustrate the key architectural flows in a modern payment system:

1. **Authorization Flow**: Shows the real-time payment processing path
2. **Settlement Flow**: Demonstrates end-of-day batch processing
3. **Tokenization**: Illustrates security token management
4. **Fraud Detection**: Details the risk assessment decision tree
5. **Microservices**: Shows service communication patterns
6. **Retry Logic**: Demonstrates failover and retry strategies
7. **Event Architecture**: Illustrates event-driven patterns
8. **Multi-Currency**: Shows FX handling flows
9. **PCI Compliance**: Demonstrates secure architecture zones
10. **High Availability**: Shows redundancy and failover design

Each diagram can be rendered using Mermaid-compatible tools or documentation platforms.
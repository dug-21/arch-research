# Payment Flow Diagram Templates

## Card Payment Authorization Flow

```mermaid
sequenceDiagram
    participant C as Customer
    participant M as Merchant
    participant G as Payment Gateway
    participant P as Payment Processor
    participant N as Card Network
    participant I as Issuing Bank
    
    C->>M: Provide Card Details
    M->>G: Submit Payment Request
    G->>G: Tokenize Card Data
    G->>P: Forward Authorization
    P->>N: Route to Network
    N->>I: Authorization Request
    
    Note over I: Validate Card<br/>Check Balance<br/>Fraud Screening
    
    alt Approved
        I-->>N: Approval Code
        N-->>P: Approved
        P-->>G: Success Response
        G-->>M: Payment Approved
        M-->>C: Order Confirmed
    else Declined
        I-->>N: Decline Code
        N-->>P: Declined
        P-->>G: Failure Response
        G-->>M: Payment Failed
        M-->>C: Payment Declined
    end
```

## E-commerce Checkout Flow

```mermaid
flowchart TB
    Start([Customer Checkout]) --> Cart[Review Cart]
    Cart --> Shipping[Enter Shipping Info]
    Shipping --> Payment[Select Payment Method]
    
    Payment --> CardPay{Card Payment?}
    Payment --> AltPay{Alternative Payment?}
    
    CardPay -->|Yes| CardForm[Card Details Form]
    CardForm --> Validate[Validate Input]
    Validate --> ThreeDS{3DS Required?}
    
    ThreeDS -->|Yes| Challenge[3DS Challenge]
    ThreeDS -->|No| Auth[Direct Authorization]
    Challenge --> Auth
    
    AltPay -->|Yes| Redirect[Redirect to Provider]
    Redirect --> ExtAuth[External Authorization]
    ExtAuth --> Return[Return to Merchant]
    
    Auth --> Result{Authorized?}
    Return --> Result
    
    Result -->|Success| Confirm[Order Confirmation]
    Result -->|Failure| Retry[Retry Payment]
    
    Confirm --> Email[Send Confirmation Email]
    Email --> End([Order Complete])
    
    Retry --> Payment
    
    style Start fill:#90EE90
    style End fill:#90EE90
    style Result fill:#FFE4B5
```

## Settlement and Reconciliation Flow

```mermaid
graph LR
    subgraph "Day 0 - Transaction"
        T1[Transaction 1] --> Cap1[Capture]
        T2[Transaction 2] --> Cap2[Capture]
        T3[Transaction 3] --> Cap3[Capture]
    end
    
    subgraph "End of Day"
        Cap1 --> Batch[Batch Creation]
        Cap2 --> Batch
        Cap3 --> Batch
        Batch --> Submit[Submit to Processor]
    end
    
    subgraph "Day 1 - Processing"
        Submit --> Clear[Clearing]
        Clear --> NetCalc[Net Calculation]
        NetCalc --> SettleFile[Settlement File]
    end
    
    subgraph "Day 2 - Settlement"
        SettleFile --> BankTrans[Bank Transfer]
        BankTrans --> Deposit[Merchant Account]
        Deposit --> Recon[Reconciliation]
    end
    
    Recon --> Match{All Match?}
    Match -->|Yes| Complete[✓ Complete]
    Match -->|No| Investigate[Investigation]
    Investigate --> Resolve[Resolution]
    Resolve --> Complete
```

## Refund Process Flow

```mermaid
stateDiagram-v2
    [*] --> Original: Original Transaction
    Original --> RefundRequest: Customer Request
    
    RefundRequest --> Validation: Validate Request
    
    Validation --> ValidRefund: Valid
    Validation --> InvalidRefund: Invalid
    
    InvalidRefund --> Rejected: Reject Request
    Rejected --> [*]
    
    ValidRefund --> PartialCheck: Check Type
    
    PartialCheck --> FullRefund: Full Amount
    PartialCheck --> PartialRefund: Partial Amount
    
    FullRefund --> ProcessFull: Process Full Refund
    PartialRefund --> ProcessPartial: Process Partial Refund
    
    ProcessFull --> IssuerCredit: Credit to Issuer
    ProcessPartial --> IssuerCredit
    
    IssuerCredit --> CustomerAccount: Credit Customer
    CustomerAccount --> Notification: Notify Customer
    
    Notification --> UpdateRecords: Update Systems
    UpdateRecords --> [*]
    
    note right of Validation
        Check:
        - Time limits
        - Previous refunds
        - Transaction status
    end note
    
    note right of IssuerCredit
        Timeline:
        3-5 business days
    end note
```

## Chargeback Lifecycle

```mermaid
flowchart TD
    Start([Transaction]) --> Dispute[Customer Disputes]
    Dispute --> CB[Chargeback Initiated]
    
    CB --> Notify[Merchant Notification]
    Notify --> Review{Review Chargeback}
    
    Review -->|Accept| Accept[Accept Liability]
    Review -->|Fight| Represent[Compile Evidence]
    
    Accept --> Debit[Funds Debited]
    Debit --> Close1[Case Closed]
    
    Represent --> Submit[Submit Response]
    Submit --> IssuerReview[Issuer Reviews]
    
    IssuerReview --> Decision{Issuer Decision}
    
    Decision -->|Merchant Wins| Win[Chargeback Reversed]
    Decision -->|Merchant Loses| Lose[Chargeback Upheld]
    
    Win --> Close2[Case Closed - Win]
    Lose --> PreArb{Pre-Arbitration?}
    
    PreArb -->|No| Debit2[Funds Debited]
    PreArb -->|Yes| PreArbSubmit[Submit Pre-Arb]
    
    Debit2 --> Close3[Case Closed - Loss]
    
    PreArbSubmit --> PreArbReview[Network Review]
    PreArbReview --> PreArbDecision{Decision}
    
    PreArbDecision -->|Win| PreArbWin[Win Pre-Arb]
    PreArbDecision -->|Lose| Arbitration[Full Arbitration]
    
    PreArbWin --> Close4[Case Closed - Win]
    Arbitration --> ArbDecision{Final Decision}
    
    ArbDecision -->|Win| FinalWin[Win + Fees Returned]
    ArbDecision -->|Lose| FinalLose[Lose + Pay Fees]
    
    FinalWin --> Close5[Case Closed - Final Win]
    FinalLose --> Close6[Case Closed - Final Loss]
    
    style Start fill:#90EE90
    style Close1 fill:#FFB6C1
    style Close2 fill:#90EE90
    style Close3 fill:#FFB6C1
    style Close4 fill:#90EE90
    style Close5 fill:#90EE90
    style Close6 fill:#FFB6C1
```

## Multi-Party Payment Flow (Marketplace)

```mermaid
sequenceDiagram
    participant B as Buyer
    participant MP as Marketplace
    participant PSP as Payment Service Provider
    participant S1 as Seller 1
    participant S2 as Seller 2
    participant Bank as Banks
    
    B->>MP: Place Order ($100)
    Note over MP: Order contains:<br/>Item A from Seller 1: $60<br/>Item B from Seller 2: $40
    
    MP->>PSP: Process Payment $100
    PSP->>Bank: Authorize $100
    Bank-->>PSP: Approved
    PSP-->>MP: Payment Success
    
    MP->>B: Order Confirmed
    
    Note over MP: Hold funds for<br/>order fulfillment
    
    S1->>MP: Ship Item A
    S2->>MP: Ship Item B
    
    MP->>PSP: Split Disbursement Request
    
    PSP->>PSP: Calculate Splits
    Note over PSP: Seller 1: $60 - fees = $57<br/>Seller 2: $40 - fees = $38<br/>Marketplace: $5 commission
    
    PSP->>Bank: Transfer $57 to Seller 1
    PSP->>Bank: Transfer $38 to Seller 2
    PSP->>Bank: Transfer $5 to Marketplace
    
    Bank-->>S1: Funds Received
    Bank-->>S2: Funds Received
    Bank-->>MP: Commission Received
```

## KYC/AML Workflow

```mermaid
flowchart TB
    Start([New Customer]) --> Initial[Initial Data Collection]
    Initial --> RiskAssess{Risk Assessment}
    
    RiskAssess -->|Low Risk| BasicKYC[Basic KYC]
    RiskAssess -->|Medium Risk| StandardKYC[Standard KYC]
    RiskAssess -->|High Risk| EnhancedKYC[Enhanced KYC]
    
    BasicKYC --> IDVerify[ID Verification]
    StandardKYC --> IDVerify
    EnhancedKYC --> IDVerify
    
    IDVerify --> AddressVerify[Address Verification]
    
    StandardKYC --> SourceFunds[Source of Funds Check]
    EnhancedKYC --> SourceFunds
    EnhancedKYC --> BeneficialOwner[Beneficial Ownership]
    
    AddressVerify --> Screening[Sanctions Screening]
    SourceFunds --> Screening
    BeneficialOwner --> Screening
    
    Screening --> PEPCheck[PEP Screening]
    PEPCheck --> Review{Compliance Review}
    
    Review -->|Approved| Onboard[Account Opening]
    Review -->|More Info| Additional[Request Additional Info]
    Review -->|Declined| Reject[Reject Application]
    
    Additional --> Review
    
    Onboard --> Monitor[Ongoing Monitoring]
    Monitor --> Alert{Suspicious Activity?}
    
    Alert -->|Yes| SAR[File SAR]
    Alert -->|No| Continue[Continue Monitoring]
    
    SAR --> Investigation[Investigation]
    Continue --> Monitor
    
    style Start fill:#90EE90
    style Onboard fill:#90EE90
    style Reject fill:#FFB6C1
```

## Real-time Payment Network Flow

```mermaid
sequenceDiagram
    participant S as Sender
    participant SB as Sender Bank
    participant RTP as RTP Network
    participant RB as Receiver Bank
    participant R as Receiver
    
    S->>SB: Initiate Payment
    
    SB->>SB: Validate Account
    SB->>SB: Check Balance
    SB->>SB: Fraud Check
    
    SB->>RTP: Payment Message
    Note over RTP: Real-time<br/>Processing<br/>(< 2 seconds)
    
    RTP->>RB: Route Payment
    
    RB->>RB: Validate Receiver
    RB->>RB: Compliance Check
    
    alt Success
        RB->>R: Credit Account
        RB-->>RTP: Confirmation
        RTP-->>SB: Success Status
        SB->>S: Payment Complete
        
        Note over S,R: End-to-end: < 10 seconds
    else Failure
        RB-->>RTP: Rejection
        RTP-->>SB: Failed Status
        SB->>S: Payment Failed
    end
    
    opt Payment Request
        R->>RB: Request Payment
        RB->>RTP: Request Message
        RTP->>SB: Payment Request
        SB->>S: Approve Request?
    end
```

## Subscription Billing Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Trial: Customer Signs Up
    
    Trial --> TrialEnd: Trial Period
    
    TrialEnd --> Convert: Convert to Paid
    TrialEnd --> Cancelled: Cancel
    
    Convert --> Active: First Payment
    
    Active --> Billing: Recurring Billing
    
    Billing --> Success: Payment Success
    Billing --> Failed: Payment Failed
    
    Success --> Active: Continue Service
    
    Failed --> Retry: Retry Logic
    
    Retry --> Success2: Retry Success
    Retry --> Dunning: Max Retries
    
    Success2 --> Active
    
    Dunning --> Recovered: Payment Recovered
    Dunning --> Suspended: Suspend Service
    
    Recovered --> Active
    
    Suspended --> Reactivated: Payment Made
    Suspended --> Churned: No Payment
    
    Reactivated --> Active
    
    Active --> Upgrade: Plan Change Up
    Active --> Downgrade: Plan Change Down
    Active --> Pause: Pause Subscription
    Active --> Cancel: Cancel Subscription
    
    Upgrade --> Active
    Downgrade --> Active
    Pause --> Paused
    
    Paused --> Resume: Resume Service
    Paused --> Expire: Max Pause Time
    
    Resume --> Active
    Expire --> Churned
    
    Cancel --> Churned
    Cancelled --> [*]
    Churned --> [*]
    
    note right of Failed
        Reasons:
        - Insufficient funds
        - Card expired
        - Card declined
    end note
    
    note right of Dunning
        Email sequences
        In-app notifications
        Grace period
    end note
```

## Fraud Detection Flow

```mermaid
flowchart TB
    Trans([Transaction]) --> RealTime{Real-time Checks}
    
    RealTime --> Velocity[Velocity Rules]
    RealTime --> Geo[Geo-location Check]
    RealTime --> Device[Device Fingerprint]
    RealTime --> ML[ML Risk Score]
    
    Velocity --> Score1[Risk Score +X]
    Geo --> Score2[Risk Score +Y]
    Device --> Score3[Risk Score +Z]
    ML --> Score4[Risk Score +W]
    
    Score1 --> Aggregate[Aggregate Score]
    Score2 --> Aggregate
    Score3 --> Aggregate
    Score4 --> Aggregate
    
    Aggregate --> Threshold{Risk Threshold}
    
    Threshold -->|Low| Approve[Auto-Approve]
    Threshold -->|Medium| Review[Manual Review]
    Threshold -->|High| Decline[Auto-Decline]
    
    Review --> Analyst[Fraud Analyst]
    
    Analyst --> Investigation[Investigate]
    Investigation --> Decision{Analyst Decision}
    
    Decision -->|Legitimate| Approve2[Approve]
    Decision -->|Fraudulent| Decline2[Decline]
    
    Approve --> Process[Process Transaction]
    Approve2 --> Process
    
    Decline --> Block[Block Transaction]
    Decline2 --> Block
    
    Process --> Monitor[Post-Transaction Monitor]
    Block --> Blacklist[Update Blacklists]
    
    Monitor --> Chargeback{Chargeback?}
    Chargeback -->|Yes| UpdateML[Update ML Model]
    Chargeback -->|No| Success[Success]
    
    Blacklist --> UpdateML
    UpdateML --> Improve[Improve Detection]
    
    style Trans fill:#90EE90
    style Approve fill:#90EE90
    style Approve2 fill:#90EE90
    style Success fill:#90EE90
    style Decline fill:#FFB6C1
    style Decline2 fill:#FFB6C1
    style Block fill:#FFB6C1
```

## Usage Notes

These diagram templates can be customized for specific implementations by:

1. **Adding specific system names** - Replace generic terms with actual system/vendor names
2. **Including timing information** - Add specific SLAs or processing times
3. **Adding error paths** - Include timeout, retry, and failure scenarios
4. **Incorporating business rules** - Add decision logic specific to your implementation
5. **Showing data elements** - Include specific fields or data passed between systems

To use these diagrams:
- Copy the Mermaid code into any Markdown file
- Modify the flow to match your specific process
- Add or remove steps as needed
- Use consistent color coding for status (green=success, red=failure, yellow=pending)
- Include notes for complex business logic or important details
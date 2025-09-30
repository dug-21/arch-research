# Integrated AP2+ACP Trusted Agentic Commerce Architecture

**Document Date:** September 30, 2025
**Architect:** Hive Mind Systems Architect
**Status:** Complete
**Version:** 1.0

---

## Executive Summary

This document proposes an integrated architecture combining **Google's Agent Payments Protocol (AP2)** and **Stripe/OpenAI's Agentic Commerce Protocol (ACP)** to create a comprehensive **Trusted Agentic Commerce Stack**. Rather than competing, these protocols serve complementary roles in the agent commerce ecosystem, with AP2 providing payment authorization infrastructure and ACP handling merchant-agent commerce interactions.

### Key Findings

- **AP2** focuses on **payment authorization and accountability** across payment networks
- **ACP** focuses on **merchant-agent interactions and order management**
- Together they create a **complete commerce flow** from product discovery to payment settlement
- Integration requires **clear architectural boundaries** and **well-defined interfaces**
- Combined implementation provides **defense-in-depth security** and **cross-protocol auditability**

---

## 1. Protocol Comparison and Complementarity

### 1.1 Core Focus Areas

| Aspect | AP2 (Google) | ACP (Stripe/OpenAI) |
|--------|--------------|---------------------|
| **Primary Focus** | Payment authorization & network integration | Merchant-agent commerce interactions |
| **Launched** | September 16, 2025 | September 29, 2025 |
| **Key Stakeholders** | Payment networks (Visa, Mastercard, PayPal) | Merchants, AI platforms, payment processors |
| **Main Problem Solved** | Verifiable user intent for payments | Seamless agent-merchant commerce |
| **Scope** | Payment initiation to settlement | Product discovery to order placement |
| **Architecture Extension** | Extends A2A protocol | Can use MCP or RESTful interfaces |
| **Control Emphasis** | Payment network security | Merchant control and relationships |

### 1.2 Complementary Strengths

**AP2 Strengths:**
- ✅ Cryptographic mandate system (Intent, Cart, Payment)
- ✅ Payment network integration (60+ partners)
- ✅ Multi-payment method support (cards, crypto, bank transfers)
- ✅ Non-repudiation and audit trails
- ✅ Global payment standards alignment

**ACP Strengths:**
- ✅ Merchant-centric design (maintains merchant of record)
- ✅ Shared Payment Token (SPT) for secure credentials
- ✅ Commerce backend flexibility (any platform)
- ✅ Native integration with ChatGPT and Shopify/Etsy
- ✅ Open source with Apache 2.0 license

### 1.3 Why Integration Makes Sense

The protocols operate at **different layers** of the commerce stack:

```
User Intent & Discovery
         ↓
    ACP Layer ← Product catalog, search, recommendations
         ↓
 Order Management ← Cart building, merchant interactions
         ↓
    AP2 Layer ← Payment authorization, mandate creation
         ↓
Payment Processing ← Settlement, reconciliation
```

**Integration Benefits:**
1. **Complete Flow:** Discovery (ACP) → Authorization (AP2) → Settlement (both)
2. **Best of Both:** Merchant control (ACP) + Payment security (AP2)
3. **Broader Reach:** ACP merchants + AP2 payment networks
4. **Layered Security:** Two independent verification systems
5. **Flexible Deployment:** Use one or both depending on needs

---

## 2. Proposed Integrated Architecture

### 2.1 Architectural Layering

The Trusted Agentic Commerce Stack has **five distinct layers**:

```
┌─────────────────────────────────────────────────────────┐
│  Layer 5: User Interface & Agent Interaction            │
│  • ChatGPT, Google Assistant, Custom AI Agents          │
│  • Natural language intent capture                      │
│  • User preference management                           │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 4: Commerce Discovery & Negotiation (ACP)        │
│  • Product catalog access via ACP                       │
│  • Merchant communication (REST/MCP)                    │
│  • Order building and cart management                   │
│  • Merchant-agent negotiation                           │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 3: Payment Authorization (AP2)                   │
│  • Intent Mandate creation                              │
│  • Cart Mandate signing                                 │
│  • Payment Mandate generation                           │
│  • Cryptographic authorization chain                    │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 2: Payment Credential Management                 │
│  • ACP: Shared Payment Token (SPT) issuance             │
│  • AP2: Tokenized payment method references             │
│  • Credential Provider integration                      │
│  • Secure key management                                │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 1: Payment Network & Settlement                  │
│  • Card network processing (Visa, Mastercard)           │
│  • Stripe payment processing                            │
│  • Cryptocurrency settlement                            │
│  • Bank transfer execution                              │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Component Architecture

#### Core Components

**1. Agent Orchestrator**
- **Role:** Coordinates commerce flow across protocols
- **Responsibilities:**
  - User intent interpretation
  - Protocol routing decisions
  - Cross-protocol state management
  - Error handling and rollback
- **Interfaces:**
  - User conversation API
  - ACP client interface
  - AP2 mandate management
  - Analytics and logging

**2. Commerce Interface Layer (ACP)**
- **Role:** Handles merchant interactions
- **Responsibilities:**
  - Product search via ACP
  - Catalog browsing
  - Merchant-agent negotiation
  - Order construction
- **Interfaces:**
  - ACP REST API client
  - MCP server connector (optional)
  - Merchant adapter layer
  - Inventory sync

**3. Payment Authorization Layer (AP2)**
- **Role:** Creates verifiable payment authorization
- **Responsibilities:**
  - Intent Mandate generation
  - User approval collection
  - Cart Mandate cryptographic signing
  - Payment Mandate creation
- **Interfaces:**
  - AP2 protocol library
  - Hardware signing module (HSM/TEE)
  - Credential Provider API
  - Payment network interfaces

**4. Token Management Service**
- **Role:** Manages payment credentials securely
- **Responsibilities:**
  - ACP SPT issuance and lifecycle
  - AP2 tokenized payment references
  - Token-to-mandate binding
  - PCI compliance controls
- **Interfaces:**
  - Stripe Token Service (for ACP)
  - AP2 Credential Provider
  - Secure key vault
  - Audit logging

**5. Settlement Coordinator**
- **Role:** Executes payment and fulfillment
- **Responsibilities:**
  - Payment execution via Stripe or card networks
  - Order fulfillment notification
  - Reconciliation tracking
  - Dispute management
- **Interfaces:**
  - Stripe API (for ACP)
  - AP2 payment network APIs
  - Merchant fulfillment webhook
  - Accounting system

---

## 3. Integration Points and Interfaces

### 3.1 ACP-to-AP2 Integration Points

**Integration Point 1: Cart Finalization**
```
ACP Order Building → AP2 Cart Mandate Creation

Flow:
1. Agent builds cart using ACP merchant API
2. ACP returns finalized cart details (items, prices, merchant)
3. Agent creates AP2 Cart Mandate with identical details
4. User cryptographically signs Cart Mandate
5. Cart Mandate reference stored in ACP order metadata
```

**Integration Point 2: Payment Credential Binding**
```
ACP Shared Payment Token → AP2 Payment Mandate

Flow:
1. Stripe issues SPT scoped to merchant and cart total (ACP)
2. Agent references SPT in AP2 Payment Mandate
3. AP2 Payment Mandate includes SPT token ID
4. Payment Mandate sent to payment network
5. Network validates both SPT and mandate before authorization
```

**Integration Point 3: Merchant Settlement**
```
AP2 Payment Authorization → ACP Order Fulfillment

Flow:
1. AP2 Payment Mandate approved by payment network
2. Settlement instruction sent to Stripe (if using ACP)
3. Stripe charges SPT with AP2 mandate reference
4. ACP merchant receives order fulfillment notification
5. Merchant ships/delivers with full audit trail
```

### 3.2 Data Flow Mapping

**User Intent → Payment Settlement:**

```
┌──────────────┐
│ User Request │ "Buy running shoes under $150"
└──────┬───────┘
       ↓
┌──────────────────────┐
│ Agent Orchestrator   │ Parses intent, routes to ACP
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ ACP Product Search   │ Queries merchant catalogs
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ ACP Cart Building    │ Adds selected items to cart
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ AP2 Intent Mandate   │ Captures authorization context
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ User Approval        │ Reviews and approves purchase
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ AP2 Cart Mandate     │ Cryptographic signature
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ ACP SPT Issuance     │ Stripe creates payment token
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ AP2 Payment Mandate  │ References SPT, sent to network
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ Payment Processing   │ Stripe/Network settles payment
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ ACP Order Fulfillment│ Merchant receives order
└──────────────────────┘
```

---

## 4. Security Architecture

### 4.1 Trust Zones

**Zone 1: User Device (Highest Trust)**
- User intent input
- Cryptographic signing operations (AP2 mandates)
- Biometric authentication
- Secure enclave for private keys

**Zone 2: Agent Platform (High Trust)**
- Agent orchestration logic
- ACP merchant communication
- AP2 mandate construction (unsigned)
- Analytics and monitoring

**Zone 3: Commerce Layer (Medium-High Trust)**
- ACP merchant APIs
- Product catalog access
- Order management
- Inventory systems

**Zone 4: Payment Processing (Medium Trust)**
- Token generation (ACP SPT)
- AP2 Credential Provider
- Payment network communication
- Settlement execution

**Zone 5: External Networks (Lower Trust)**
- Merchant websites
- Third-party APIs
- Public internet
- Analytics services

### 4.2 Security Boundaries

**Boundary 1: User → Agent**
- **Threat:** Agent acting beyond authorized scope
- **Control:** AP2 Intent Mandate limits agent authority
- **Verification:** User signs Cart Mandate before payment

**Boundary 2: Agent → Merchant (via ACP)**
- **Threat:** Malicious merchant overcharging or fraud
- **Control:** ACP maintains merchant of record, Stripe fraud detection
- **Verification:** Cart Mandate matches ACP order exactly

**Boundary 3: Agent → Payment Network (via AP2)**
- **Threat:** Unauthorized payment initiation
- **Control:** Payment Mandate requires valid Intent and Cart Mandates
- **Verification:** Cryptographic signature chain validation

**Boundary 4: Token Management**
- **Threat:** Token theft or misuse
- **Control:** ACP SPT scoped to specific merchant and amount
- **Verification:** AP2 mandate references must match SPT constraints

**Boundary 5: Settlement**
- **Threat:** Payment without delivery or double-charging
- **Control:** Idempotent payment execution, fulfillment webhooks
- **Verification:** Reconciliation between AP2 mandates and ACP orders

### 4.3 Cryptographic Architecture

**AP2 Cryptographic Chain:**
```
User Private Key (Device TEE/HSM)
         ↓
   Intent Mandate Signature
         ↓
    Cart Mandate Signature ← User approval event
         ↓
   Payment Mandate (includes Intent + Cart)
         ↓
Payment Network Validation (non-repudiation)
```

**ACP Token Security:**
```
Stripe Master Key
         ↓
Shared Payment Token (SPT) Generation
    • Scoped to merchant ID
    • Scoped to cart total amount
    • Time-limited validity
    • Single-use constraint
         ↓
Token Redemption (validated by Stripe)
```

**Integrated Security:**
```
AP2 Mandate Chain + ACP SPT = Dual Verification

Payment executes ONLY if:
✅ Valid AP2 Intent Mandate exists
✅ Valid AP2 Cart Mandate signed by user
✅ Valid AP2 Payment Mandate references Intent + Cart
✅ Valid ACP SPT issued by Stripe
✅ SPT constraints match Cart Mandate details
✅ Payment network approves transaction
```

---

## 5. Transaction Flow Scenarios

### 5.1 Scenario 1: Human-Present ChatGPT Purchase

**Use Case:** User shopping in ChatGPT for Etsy products

**Flow:**

1. **Discovery Phase (ACP)**
   ```
   User: "Find handmade leather wallets under $50"
   ↓
   ChatGPT Agent → ACP Etsy Integration
   ↓
   ACP returns product catalog (5 wallet options)
   ↓
   ChatGPT displays options to user
   ```

2. **Selection Phase (ACP + AP2 Intent)**
   ```
   User: "Show me the brown one with brass hardware"
   ↓
   ChatGPT → ACP product details request
   ↓
   AP2 Intent Mandate created:
     • User ID: user@example.com
     • Max Price: $50
     • Category: leather wallets
     • Session: chat-xyz-123
   ```

3. **Checkout Phase (ACP + AP2 Cart)**
   ```
   User: "Buy it"
   ↓
   ACP builds cart:
     • Product: Leather Wallet #AB123
     • Price: $42.00
     • Merchant: Etsy Seller "LeatherCraft"
     • Shipping: $5.00
     • Total: $47.00
   ↓
   AP2 Cart Mandate:
     • References Intent Mandate
     • Contains exact ACP cart details
     • Presented to user for signing
   ↓
   User signs Cart Mandate (fingerprint/FaceID)
   ```

4. **Payment Phase (ACP SPT + AP2 Payment)**
   ```
   Stripe issues SPT:
     • Merchant: Etsy Seller "LeatherCraft"
     • Amount: $47.00
     • Validity: 15 minutes
     • Token: spt_abc123xyz
   ↓
   AP2 Payment Mandate:
     • References Intent Mandate ID
     • References Cart Mandate ID
     • Includes SPT token: spt_abc123xyz
     • Sent to payment network
   ↓
   Payment network validates:
     ✅ Mandate chain complete
     ✅ SPT valid and scoped correctly
     ✅ Fraud checks pass
   ↓
   Payment authorized
   ```

5. **Settlement & Fulfillment (ACP)**
   ```
   Stripe charges SPT → $47.00 to user's card
   ↓
   ACP order fulfillment notification → Etsy
   ↓
   Etsy merchant receives order with full audit trail:
     • ACP order ID
     • AP2 Cart Mandate reference
     • Stripe payment confirmation
   ↓
   Merchant ships wallet
   ↓
   User receives confirmation in ChatGPT
   ```

### 5.2 Scenario 2: Autonomous Agent Purchase (Human-Not-Present)

**Use Case:** Agent monitoring price drops for concert tickets

**Flow:**

1. **Authorization Setup (AP2 Intent)**
   ```
   User: "Buy Taylor Swift tickets when price drops below $100"
   ↓
   Agent creates forward-looking AP2 Intent Mandate:
     • User ID: user@example.com
     • Product: Taylor Swift Concert - Aug 15
     • Max Price: $100
     • Vendor: Approved ticket platforms
     • Validity: 30 days
     • Autonomous: true
   ↓
   User signs Intent Mandate (gives agent authority)
   ```

2. **Monitoring Phase (ACP)**
   ```
   Agent continuously polls:
     • Ticketmaster (via ACP)
     • StubHub (via ACP)
     • SeatGeek (via ACP)
   ↓
   Checks inventory and pricing every 5 minutes
   ```

3. **Trigger Event (ACP)**
   ```
   Day 12: SeatGeek drops price to $95
   ↓
   Agent detects condition met:
     ✅ Product available: Taylor Swift Aug 15
     ✅ Price: $95 (under $100 limit)
     ✅ Merchant: SeatGeek (approved)
   ↓
   Agent initiates autonomous purchase flow
   ```

4. **Autonomous Checkout (ACP + AP2)**
   ```
   ACP cart building:
     • Product: 2 tickets, Section 104, Row F
     • Price: $95 each = $190
     • Merchant: SeatGeek
     • Fees: $25
     • Total: $215
   ↓
   WAIT! Total $215 exceeds Intent Mandate ($100)
   ↓
   Agent adjusts to 1 ticket:
     • Product: 1 ticket, Section 104, Row F
     • Price: $95
     • Fees: $12.50
     • Total: $107.50
   ↓
   STILL exceeds $100!
   ↓
   Agent finds alternative:
     • Product: 1 ticket, Section 201, Row A
     • Price: $85
     • Fees: $11.00
     • Total: $96.00 ✅
   ↓
   AP2 Cart Mandate (auto-generated):
     • References Intent Mandate
     • Contains final cart: $96.00 total
     • No user signature required (Intent authorizes)
   ```

5. **Autonomous Payment (ACP + AP2)**
   ```
   Stripe issues SPT:
     • Merchant: SeatGeek
     • Amount: $96.00
     • Token: spt_auto456
   ↓
   AP2 Payment Mandate:
     • References Intent Mandate (autonomous flag)
     • References auto-generated Cart Mandate
     • Includes SPT: spt_auto456
   ↓
   Payment network validates:
     ✅ Intent Mandate authorizes autonomous action
     ✅ Cart within Intent constraints
     ✅ SPT valid
   ↓
   Payment authorized and settled
   ```

6. **Post-Purchase Notification**
   ```
   ACP order fulfillment → SeatGeek
   ↓
   Agent sends notification to user:
     "✅ Purchased Taylor Swift ticket for $96!
      Section 201, Row A, Aug 15 at 7pm
      Receipt and tickets sent to your email."
   ↓
   User receives full audit trail:
     • Original Intent Mandate (signed by user)
     • Auto-generated Cart Mandate
     • Payment Mandate
     • Stripe receipt
     • ACP order confirmation
   ```

### 5.3 Scenario 3: Multi-Merchant Purchase

**Use Case:** Agent coordinating trip (flights + hotel + car rental)

**Flow:**

1. **Discovery (ACP Multi-Merchant)**
   ```
   User: "Plan weekend trip to NYC, budget $1000"
   ↓
   AP2 Intent Mandate:
     • Budget: $1000 total
     • Category: Travel
     • Merchants: Any approved travel vendors
   ↓
   Agent queries multiple ACP merchants:
     • United Airlines (via ACP)
     • Marriott Hotels (via ACP)
     • Hertz Rental Cars (via ACP)
   ```

2. **Optimization**
   ```
   Agent finds optimal bundle:
     • Flight: United $350
     • Hotel: Marriott $480 (2 nights)
     • Car: Hertz $150 (2 days)
     • Total: $980 (under $1000 ✅)
   ```

3. **Sequential Checkout (3 separate flows)**

   **Purchase 1: Flight**
   ```
   ACP cart: United flight $350
   ↓
   AP2 Cart Mandate #1 (references Intent)
   ↓
   ACP SPT #1: United, $350
   ↓
   AP2 Payment Mandate #1
   ↓
   Payment settled via Stripe
   ```

   **Purchase 2: Hotel**
   ```
   ACP cart: Marriott hotel $480
   ↓
   AP2 Cart Mandate #2 (references Intent)
   ↓
   ACP SPT #2: Marriott, $480
   ↓
   AP2 Payment Mandate #2
   ↓
   Payment settled via Stripe
   ```

   **Purchase 3: Car**
   ```
   ACP cart: Hertz rental $150
   ↓
   AP2 Cart Mandate #3 (references Intent)
   ↓
   ACP SPT #3: Hertz, $150
   ↓
   AP2 Payment Mandate #3
   ↓
   Payment settled via Stripe
   ```

4. **Rollback Handling (If hotel fails)**
   ```
   If Marriott booking fails after flight purchased:
   ↓
   Agent checks Intent Mandate remaining budget:
     • Total budget: $1000
     • Spent: $350 (flight)
     • Remaining: $650
   ↓
   Agent finds alternative hotel under $500
   ↓
   Creates new Cart Mandate referencing Intent
   ↓
   Attempts payment again
   ↓
   If all merchants fail, agent notifies user:
     "Unable to complete full trip.
      Flight booked ($350), but hotels unavailable.
      Would you like to cancel flight?"
   ```

---

## 6. Integration Challenges and Solutions

### 6.1 Challenge: Dual Protocol Complexity

**Problem:**
- Merchants must implement both ACP and AP2
- Different data models and APIs
- Increased integration effort
- Potential inconsistencies

**Solutions:**

**Solution 1: Protocol Adapter Layer**
```
Create middleware that bridges ACP ↔ AP2:
┌─────────────────┐
│  Agent          │
└────┬────────────┘
     ↓
┌─────────────────┐
│ Adapter Layer   │ ← Single integration point
│  • ACP Client   │
│  • AP2 Client   │
│  • Data Mapper  │
└────┬────────────┘
     ↓
┌─────────────────┐
│ Payment Systems │
└─────────────────┘
```

**Solution 2: Platform-as-a-Service**
```
Offer managed service handling both protocols:
• Shopify Plugin (ACP+AP2)
• WooCommerce Plugin (ACP+AP2)
• Stripe App Store Integration
• Google Cloud Managed Service
```

**Solution 3: Standardized Data Models**
```json
{
  "unified_cart": {
    "acp_order": {
      "merchant": "ShopifyMerchant",
      "items": [...],
      "total": 125.00
    },
    "ap2_cart_mandate": {
      "intent_reference": "intent_abc123",
      "cart_hash": "sha256...",
      "signature": "..."
    }
  }
}
```

### 6.2 Challenge: Payment Credential Management

**Problem:**
- ACP uses Shared Payment Tokens (SPT)
- AP2 uses tokenized payment references
- Need to bind tokens to mandates
- Risk of token leakage or misuse

**Solutions:**

**Solution 1: Token Binding Protocol**
```
Create cryptographic binding:
SPT Creation:
  • Stripe generates SPT
  • SPT metadata includes AP2 Cart Mandate hash
  • SPT can only be redeemed with matching mandate

Validation:
  1. Agent submits payment with SPT + AP2 mandate
  2. Stripe validates SPT metadata matches mandate
  3. Payment network validates AP2 signature chain
  4. Both must pass for authorization
```

**Solution 2: Unified Token Service**
```
Single service managing both token types:
┌────────────────────────┐
│ Unified Token Manager  │
│  • Issues ACP SPT      │
│  • Issues AP2 tokens   │
│  • Binds tokens        │
│  • Validates scope     │
└────────────────────────┘
```

**Solution 3: Token Attestation**
```
Add attestation metadata:
{
  "spt_token": "spt_abc123",
  "attestation": {
    "ap2_cart_mandate_id": "cart_xyz789",
    "ap2_intent_mandate_id": "intent_def456",
    "binding_signature": "...",
    "issued_at": "2025-09-30T12:00:00Z",
    "expires_at": "2025-09-30T12:15:00Z"
  }
}
```

### 6.3 Challenge: Merchant Reconciliation

**Problem:**
- Two separate order systems (ACP order, AP2 mandate)
- Need to reconcile fulfillment with payments
- Dispute resolution requires both contexts
- Accounting complexity

**Solutions:**

**Solution 1: Universal Order ID**
```
Generate shared identifier linking both systems:
┌──────────────────┐
│ Universal ID Gen │
└────┬─────────────┘
     ↓
Universal Order ID: UO-2025-09-30-ABC123
     ↓
┌─────────────────────────────────────┐
│ ACP Order: acp_order_xyz789         │
│  • universal_id: UO-2025-09-30-ABC123│
│  • merchant: ShopifyStore           │
│  • total: $125.00                   │
└─────────────────────────────────────┘
     ↓
┌─────────────────────────────────────┐
│ AP2 Cart Mandate: cart_mand_456     │
│  • universal_id: UO-2025-09-30-ABC123│
│  • intent_ref: intent_abc           │
│  • total: $125.00                   │
└─────────────────────────────────────┘
```

**Solution 2: Reconciliation Service**
```
Automated matching and verification:
┌───────────────────────────┐
│ Reconciliation Engine     │
│  1. Match ACP ↔ AP2       │
│  2. Verify amounts match  │
│  3. Check fulfillment     │
│  4. Flag discrepancies    │
│  5. Generate reports      │
└───────────────────────────┘
```

**Solution 3: Unified Audit Trail**
```
Single ledger recording all events:
Timeline for UO-2025-09-30-ABC123:
├─ T+0ms: User intent captured
├─ T+15s: ACP product search
├─ T+42s: ACP cart finalized
├─ T+45s: AP2 Intent Mandate created
├─ T+47s: AP2 Cart Mandate signed
├─ T+50s: ACP SPT issued
├─ T+52s: AP2 Payment Mandate sent
├─ T+55s: Payment authorized
├─ T+58s: ACP order fulfilled
└─ T+120s: Merchant shipped
```

### 6.4 Challenge: Error Handling and Rollback

**Problem:**
- Multi-step flow with multiple failure points
- ACP order might succeed, AP2 payment fail (or vice versa)
- Need consistent state across protocols
- User experience degradation

**Solutions:**

**Solution 1: Two-Phase Commit Protocol**
```
Phase 1: Prepare (both protocols)
  ACP: Reserve inventory, prepare order
  AP2: Validate mandates, prepare payment
  Both respond: READY or ABORT

Phase 2: Commit (if both ready)
  ACP: Finalize order
  AP2: Execute payment
  If either fails, rollback both

Rollback:
  ACP: Release inventory, cancel order
  AP2: Void authorization
  User: Notified with error details
```

**Solution 2: Saga Pattern**
```
Compensating transactions for failures:

Success Path:
1. ACP create order → (order_id)
2. AP2 create mandate → (mandate_id)
3. ACP issue SPT → (spt_token)
4. AP2 execute payment → (payment_id)
5. ACP confirm fulfillment → (confirmed)

Failure at Step 4 (payment fails):
  Compensation:
  4-C. Notify user of payment failure
  3-C. Void SPT (Stripe invalidates token)
  2-C. Mark AP2 mandate as failed
  1-C. Cancel ACP order, release inventory
```

**Solution 3: Idempotent Operations**
```
All operations support retry without side effects:
• ACP order creation: idempotency key
• AP2 mandate creation: unique mandate ID
• Payment execution: idempotent with same key
• Fulfillment: check-then-act pattern

Example:
POST /acp/orders
{
  "idempotency_key": "uo-abc123-order",
  "cart": {...}
}
→ Returns same order ID if called multiple times
```

---

## 7. PCI-DSS Compliance in Integrated Architecture

### 7.1 Compliance Scope

**With ACP Only:**
- Scope: Stripe payment processing (PCI Level 1 Service Provider)
- Merchant responsibility: Minimal (using Stripe-hosted checkout)
- QSA assessment: SAQ A (if fully outsourced)

**With AP2 Only:**
- Scope: Agent systems handling mandates
- Merchant responsibility: Moderate (mandate validation, token handling)
- QSA assessment: SAQ A-EP or full ROC (depending on integration)

**With Integrated ACP+AP2:**
- Scope: Both agent systems AND payment processing
- Merchant responsibility: Higher (dual protocol compliance)
- QSA assessment: Likely full ROC for Level 1-2 merchants

### 7.2 Tokenization Architecture (PCI Req 3)

**Recommended Approach: Dual Tokenization**

```
Layer 1: ACP Shared Payment Token (SPT)
  • User's payment credential → Stripe SPT
  • Agent receives SPT, NEVER sees PAN
  • SPT scoped to merchant and amount

Layer 2: AP2 Tokenized Reference
  • SPT reference → AP2 Payment Mandate
  • Mandate contains token ID, not token itself
  • Payment network validates both

Result: Zero CHD exposure in agent systems ✅
```

**Data Flow:**
```
User's Card (PAN 1234-5678-9012-3456)
            ↓
Stripe Tokenization: spt_abc123xyz
            ↓
Agent receives: { "token": "spt_abc123xyz" }
            ↓
AP2 Mandate includes: { "payment_ref": "spt_abc123xyz" }
            ↓
Payment Network receives mandate + SPT validation
            ↓
Stripe detokenizes → processes actual PAN
```

**PCI Benefit:** Agent systems are OUT OF SCOPE for PCI-DSS if they only handle tokens.

### 7.3 Logging and Monitoring (PCI Req 10)

**Unified Audit Trail Requirements:**

```json
{
  "unified_transaction_log": {
    "transaction_id": "UO-2025-09-30-ABC123",
    "timestamp": "2025-09-30T14:23:15Z",
    "user_id": "user@example.com",
    "agent_id": "chatgpt-agent-42",

    "acp_events": [
      {
        "event": "product_search",
        "timestamp": "2025-09-30T14:23:15Z",
        "merchant": "ShopifyStore",
        "query": "running shoes"
      },
      {
        "event": "cart_created",
        "timestamp": "2025-09-30T14:24:30Z",
        "order_id": "acp_order_xyz789",
        "total": 125.00
      },
      {
        "event": "spt_issued",
        "timestamp": "2025-09-30T14:25:10Z",
        "token": "spt_***xyz" // masked
      }
    ],

    "ap2_events": [
      {
        "event": "intent_mandate_created",
        "timestamp": "2025-09-30T14:24:00Z",
        "mandate_id": "intent_abc123",
        "max_amount": 150.00
      },
      {
        "event": "cart_mandate_signed",
        "timestamp": "2025-09-30T14:25:00Z",
        "mandate_id": "cart_def456",
        "signature": "sig_***" // truncated
      },
      {
        "event": "payment_authorized",
        "timestamp": "2025-09-30T14:25:15Z",
        "payment_mandate_id": "pay_ghi789",
        "amount": 125.00,
        "network_response": "APPROVED"
      }
    ],

    "reconciliation": {
      "acp_order_total": 125.00,
      "ap2_mandate_total": 125.00,
      "amounts_match": true,
      "status": "COMPLETE"
    }
  }
}
```

**PCI Compliance Checklist:**
- ✅ All payment events logged with timestamps
- ✅ Agent actions linked to user identity
- ✅ Token references masked (show last 3 chars only)
- ✅ Signatures truncated (not full values)
- ✅ Audit trail immutable (append-only log)
- ✅ Log retention: 1 year minimum
- ✅ Tamper detection enabled (log hashing)

### 7.4 Vendor Management (PCI Req 12.8)

**Service Provider Assessment:**

| Vendor | Role | PCI Compliance Required | AOC Needed |
|--------|------|------------------------|------------|
| **Stripe** | ACP payment processor | ✅ Yes (Level 1 SP) | ✅ Yes |
| **Google** | AP2 protocol provider | ⚠️ Depends on implementation | Maybe |
| **OpenAI** | ChatGPT agent platform | ⚠️ Depends on integration | Maybe |
| **Shopify** | ACP merchant platform | ✅ Yes (Level 1 SP) | ✅ Yes |
| **Payment Networks** | AP2 settlement | ✅ Yes (PCI Card Brands) | N/A (inherent) |

**Required Documentation:**
1. Stripe: PCI-DSS AOC (Level 1 Service Provider)
2. Shopify: PCI-DSS AOC (Level 1 Service Provider)
3. Agent Platform: Security assessment (if handling tokens)
4. AP2 Library: Security review (open source audit)
5. Shared Responsibility Matrix (who handles what controls)

---

## 8. Deployment Models

### 8.1 Model 1: Full Stack Integration (Enterprise)

**Description:** Large enterprise implementing both protocols natively

**Architecture:**
```
┌──────────────────────────────────────────┐
│  Enterprise Agent Platform               │
│  • Custom AI agents                      │
│  • Full ACP integration                  │
│  • Full AP2 integration                  │
│  • PCI-compliant infrastructure          │
└──────────────────────────────────────────┘
            ↓                    ↓
    ┌───────────────┐     ┌─────────────┐
    │ ACP Merchants │     │ AP2 Payment │
    │ (via Stripe)  │     │  Networks   │
    └───────────────┘     └─────────────┘
```

**Pros:**
- ✅ Maximum control and customization
- ✅ Optimized for specific use cases
- ✅ Direct integration with payment networks
- ✅ Full data ownership

**Cons:**
- ❌ High implementation cost ($500K-$2M)
- ❌ Complex PCI compliance (full ROC)
- ❌ Ongoing maintenance burden
- ❌ Requires specialized expertise

**Best For:**
- Large e-commerce platforms (Amazon, Walmart)
- Payment processors building agent services
- Enterprises with existing PCI infrastructure

### 8.2 Model 2: Platform-as-a-Service (Mid-Market)

**Description:** Use managed platform handling both protocols

**Architecture:**
```
┌──────────────────────────────────────────┐
│  Merchant's Agent (ChatGPT, Custom)      │
└──────────────────┬───────────────────────┘
                   ↓
┌──────────────────────────────────────────┐
│  Managed Commerce Platform               │
│  • Shopify + ACP Plugin                  │
│  • Stripe + AP2 Adapter                  │
│  • PCI-compliant by default              │
│  • Unified merchant dashboard            │
└──────────────────────────────────────────┘
            ↓                    ↓
    ┌───────────────┐     ┌─────────────┐
    │ ACP Network   │     │ AP2 Network │
    └───────────────┘     └─────────────┘
```

**Pros:**
- ✅ Lower implementation cost ($50K-$200K)
- ✅ Simplified PCI compliance (leverage platform AOC)
- ✅ Faster time to market (weeks vs months)
- ✅ Managed updates and security

**Cons:**
- ⚠️ Less customization flexibility
- ⚠️ Platform fees (2-3% of transactions)
- ⚠️ Dependency on platform roadmap
- ⚠️ Shared responsibility model requires understanding

**Best For:**
- Mid-market retailers ($10M-$500M revenue)
- Shopify/WooCommerce merchants
- Companies without PCI expertise
- Rapid prototyping and pilots

### 8.3 Model 3: Agent-Centric (AI Platform)

**Description:** AI platform (ChatGPT, Anthropic) handles integration

**Architecture:**
```
┌──────────────────────────────────────────┐
│  AI Platform (ChatGPT, Claude)           │
│  • Built-in ACP support                  │
│  • Built-in AP2 support                  │
│  • User payment credential management    │
│  • Merchant discovery                    │
└──────────────────┬───────────────────────┘
                   ↓
         ┌─────────┴─────────┐
         ↓                   ↓
┌────────────────┐   ┌──────────────┐
│ ACP Merchants  │   │ AP2 Payments │
│ (Etsy, Shopify)│   │ (Stripe, Visa)│
└────────────────┘   └──────────────┘
```

**Pros:**
- ✅ Zero implementation cost for merchants
- ✅ Instant reach to millions of users
- ✅ PCI compliance handled by platform
- ✅ Best user experience

**Cons:**
- ⚠️ Merchant must integrate with platform
- ⚠️ Platform controls user relationship
- ⚠️ Higher platform fees (potentially)
- ⚠️ Limited customization

**Best For:**
- Small merchants (<$10M revenue)
- Marketplaces (Etsy, eBay)
- Digital goods sellers
- Consumer-facing brands

### 8.4 Model 4: Hybrid (Recommended for Most)

**Description:** Combine platform services with custom logic

**Architecture:**
```
┌──────────────────────────────────────────┐
│  Custom Agent Logic                      │
│  • Business rules                        │
│  • User preference management            │
│  • Analytics and optimization            │
└──────────────────┬───────────────────────┘
                   ↓
┌──────────────────────────────────────────┐
│  Managed Commerce Layer                  │
│  • Stripe for ACP payment processing     │
│  • Google Cloud for AP2 mandate handling │
│  • Shopify for merchant integration      │
└──────────────────┬───────────────────────┘
                   ↓
         ┌─────────┴─────────┐
         ↓                   ↓
┌────────────────┐   ┌──────────────┐
│ ACP Merchants  │   │ AP2 Networks │
└────────────────┘   └──────────────┘
```

**Pros:**
- ✅ Balance of control and simplicity
- ✅ Moderate cost ($100K-$500K)
- ✅ Customizable where needed
- ✅ Leverage platform PCI compliance

**Cons:**
- ⚠️ Integration complexity
- ⚠️ Shared responsibility for compliance
- ⚠️ Need to coordinate multiple vendors

**Best For:**
- Most enterprise and mid-market companies
- Companies with some technical capability
- Those needing customization with compliance simplicity
- Growing businesses scaling up

---

## 9. Recommendations

### 9.1 For Protocol Governance

**Recommendation 1: Establish Joint Working Group**
- Create "ACP+AP2 Integration Task Force"
- Members: Google, Stripe, OpenAI, payment networks, merchants
- Goal: Define standard integration patterns
- Publish joint specification by Q2 2026

**Recommendation 2: Develop Reference Implementation**
- Open-source integration library (GitHub)
- Supports common platforms (Shopify, WooCommerce)
- Includes PCI-compliant architecture patterns
- Community-driven development

**Recommendation 3: Certification Program**
- "ACP+AP2 Certified Platform" badge
- Security assessment criteria
- Compliance validation
- Annual recertification

### 9.2 For Merchants

**Recommendation 1: Start with Platform-as-a-Service**
- Use Shopify + Stripe managed integration
- Pilot with limited product catalog
- Measure ROI before full rollout
- Leverage platform PCI compliance

**Recommendation 2: Implement Tokenization-First**
- Never expose agents to CHD (cardholder data)
- Use ACP SPT for all payment credentials
- Reference tokens in AP2 mandates
- Reduces PCI scope significantly

**Recommendation 3: Unified Monitoring Dashboard**
- Single view of ACP and AP2 transactions
- Real-time reconciliation alerts
- Fraud detection across both protocols
- Compliance reporting

**Recommendation 4: Progressive Rollout**
```
Phase 1 (Months 1-3): Pilot
  • Single product category
  • Limited user group
  • Human-present only
  • Measure and learn

Phase 2 (Months 4-6): Expand
  • Full catalog
  • Broader user base
  • Add autonomous purchasing
  • Optimize based on data

Phase 3 (Months 7-12): Scale
  • Multi-merchant integration
  • Advanced features
  • Full automation
  • Continuous optimization
```

### 9.3 For Payment Processors

**Recommendation 1: Native Integration Support**
- Build ACP+AP2 support into core platform
- Provide unified API for both protocols
- Handle cross-protocol reconciliation
- Offer managed PCI compliance

**Recommendation 2: Enhanced Fraud Detection**
- Analyze patterns across both protocols
- Flag inconsistencies between ACP orders and AP2 mandates
- Real-time risk scoring
- Adaptive authentication based on agent behavior

**Recommendation 3: Merchant Enablement**
- Developer documentation and SDKs
- Pre-built integrations for major platforms
- Training and certification programs
- Dedicated support team

### 9.4 For AI Platform Providers

**Recommendation 1: Built-in Integration**
- Native ACP+AP2 support in agent framework
- Transparent protocol selection
- Automatic fallback and retry logic
- User-friendly payment management

**Recommendation 2: User Control and Transparency**
- Clear visualization of Intent Mandates
- Easy approval flow for Cart Mandates
- Detailed transaction history
- One-click cancellation and refunds

**Recommendation 3: Security-First Design**
- Hardware-backed signing (TEE/Secure Enclave)
- Biometric authentication
- Anomaly detection
- Proactive fraud alerts

---

## 10. Future Evolution

### 10.1 Short-Term (2025-2026)

**Q4 2025:**
- ✅ ACP launches in ChatGPT with Etsy
- ✅ AP2 pilot programs begin
- ✅ First integrated implementations (likely Google/Stripe collaboration)
- ✅ PCI SSC publishes initial guidance

**Q1-Q2 2026:**
- 📈 Shopify merchants adopt ACP+AP2 integration
- 📈 Payment networks enable AP2 support
- 📈 Managed platform providers launch offerings
- 📈 First ROC assessments completed

**Q3-Q4 2026:**
- 🚀 Mainstream adoption begins
- 🚀 Multi-merchant autonomous purchases
- 🚀 Cross-border support enabled
- 🚀 Mobile wallet integration

### 10.2 Medium-Term (2027-2028)

**Enhanced Features:**
- **Intelligent Negotiation:** Agents negotiate prices using both protocols
- **Predictive Purchasing:** Agents anticipate needs and proactively buy
- **Social Commerce:** Group purchasing via multi-user mandates
- **Subscription Management:** Agents optimize recurring purchases

**Technical Advances:**
- **Zero-Knowledge Proofs:** Enhanced privacy in mandates
- **Blockchain Settlement:** AP2 mandates on distributed ledger
- **Quantum-Safe Crypto:** Future-proof cryptographic signatures
- **Federated Learning:** Fraud detection without data sharing

**Regulatory:**
- **Global Standards:** ISO/IEC standards for agent commerce
- **Consumer Protection:** Specific regulations for autonomous purchases
- **PCI-DSS v5.0:** Native agent payment requirements
- **AML/KYC:** Agent-specific compliance frameworks

### 10.3 Long-Term Vision (2029-2030)

**The Autonomous Commerce Ecosystem:**

```
┌─────────────────────────────────────────────┐
│  Autonomous Agent Economy                   │
│  • Agents negotiate agent-to-agent          │
│  • Self-optimizing supply chains            │
│  • Dynamic pricing based on real-time data  │
│  • Personalized micro-services marketplace  │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Universal Commerce Protocol (ACP+AP2)      │
│  • Single standard across all platforms     │
│  • Global interoperability                  │
│  • Multi-currency support                   │
│  • Real-time settlement                     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Decentralized Trust Infrastructure         │
│  • Distributed mandate validation           │
│  • Peer-to-peer payment networks            │
│  • Smart contract enforcement               │
│  • Zero-trust architecture by default       │
└─────────────────────────────────────────────┘
```

**Potential Disruptions:**
- **Death of Traditional Checkout:** All purchases via conversational agents
- **Merchant Disintermediation:** Direct manufacturer-to-consumer via agents
- **Dynamic Personalization:** Every price, product, and service customized
- **Agentic Marketplaces:** Agents buying and selling on behalf of users
- **Post-App Economy:** No more dedicated shopping apps, only agents

---

## 11. Conclusion

### Key Insights

1. **Protocols are Complementary, Not Competitive**
   - ACP excels at merchant-agent commerce interactions
   - AP2 excels at payment authorization and accountability
   - Together they create a complete trusted commerce stack

2. **Integration is Feasible and Beneficial**
   - Clear architectural boundaries enable integration
   - Layered design provides defense-in-depth security
   - Dual verification reduces fraud and disputes

3. **PCI Compliance is Critical**
   - Tokenization-first architecture reduces scope
   - Unified audit trail satisfies requirements
   - Managed platform approach simplifies compliance

4. **Multiple Deployment Models Serve Different Needs**
   - Enterprises: Full stack integration
   - Mid-market: Platform-as-a-service
   - Small merchants: Agent-centric approach
   - Most companies: Hybrid model

5. **Future is Bright for Agentic Commerce**
   - Technology foundation is strong
   - Industry collaboration is active
   - User demand is growing
   - Regulatory frameworks are evolving

### Strategic Recommendations

**For the Industry:**
- ✅ Establish joint working group (Google, Stripe, OpenAI, payment networks)
- ✅ Publish reference implementation by Q2 2026
- ✅ Create certification program for compliant platforms
- ✅ Engage with PCI SSC and regulators proactively

**For Merchants:**
- ✅ Start with managed platform integration
- ✅ Implement tokenization-first architecture
- ✅ Pilot with limited scope, then scale
- ✅ Budget for PCI compliance from day one

**For Technology Providers:**
- ✅ Build native ACP+AP2 support into platforms
- ✅ Offer managed compliance services
- ✅ Provide unified developer experience
- ✅ Invest in security and fraud detection

**For Regulators:**
- ✅ Provide clear guidance for autonomous purchases
- ✅ Update PCI-DSS for agent-specific scenarios
- ✅ Harmonize international standards
- ✅ Balance innovation with consumer protection

### Final Thought

The convergence of **AP2** and **ACP** represents a pivotal moment in the evolution of commerce. By combining Google's payment authorization framework with Stripe/OpenAI's merchant interaction protocol, the industry has the opportunity to create a **truly open, secure, and interoperable foundation for the agent economy**.

Success requires:
- 🤝 **Collaboration** between protocol developers
- 🔒 **Security** as a foundational principle
- 📊 **Standards** that enable innovation
- 🧪 **Experimentation** to learn and improve
- 🌍 **Global perspective** on commerce transformation

The **Trusted Agentic Commerce Stack** is not just a technical architecture—it's a vision for how humans, agents, merchants, and payment networks can work together to create a more efficient, personalized, and secure commerce experience for everyone.

---

## Appendix A: Sequence Diagrams

### A.1 Human-Present Purchase Flow

```
User          ChatGPT       ACP           AP2          Stripe       Payment
                Agent      Merchant     Protocol                   Network
  |              |            |            |             |            |
  |--"Buy shoes"→|            |            |             |            |
  |              |--Search--->|            |             |            |
  |              |<--Results--|            |             |            |
  |              |            |            |             |            |
  |←-Show options─|            |            |             |            |
  |--Select one-→|            |             |            |            |
  |              |--Cart req-→|            |             |            |
  |              |<-Cart data-|            |             |            |
  |              |            |--Intent-->|             |            |
  |              |            |  Mandate  |             |            |
  |              |            |           |             |            |
  |←--Review cart--------------|           |             |            |
  |--Approve----→|            |           |             |            |
  |              |            |--Cart---->|             |            |
  |              |            | Mandate   |             |            |
  |←--Sign req----------------------------→| (User      |            |
  |--Signature--------------------------------→ signs)   |            |
  |              |            |           |             |            |
  |              |            |--SPT req-→|             |            |
  |              |            |<--SPT-----|             |            |
  |              |            |           |             |            |
  |              |            |-Payment-->|             |            |
  |              |            | Mandate   |--Validate-→|            |
  |              |            |           |<-Approved--|            |
  |              |            |           |             |            |
  |              |            |<-Fulfill--|             |            |
  |←--Confirmation-----------|             |            |            |
```

### A.2 Autonomous Purchase Flow

```
User      Agent       ACP        AP2       Stripe     Payment
                   Merchant   Protocol              Network
  |          |         |          |          |          |
  |-Intent->|         |          |          |          |
  | "Buy tickets <$100"|         |          |          |
  |          |-Intent  |          |          |          |
  |          | Mandate---------→|          |          |
  |          | (signed by user)|          |          |
  |          |         |         |          |          |
  | [Time passes - agent monitors]         |          |
  |          |         |         |          |          |
  |          |-Poll-->|         |          |          |
  |          |<-Price: $95------|          |          |
  |          |         |         |          |          |
  |          | [Conditions met!]|          |          |
  |          |         |         |          |          |
  |          |-Build cart-----→|          |          |
  |          |<-Cart details---|          |          |
  |          |         |         |          |          |
  |          |-Auto Cart------→|          |          |
  |          | Mandate (refs Intent)      |          |
  |          |         |         |          |          |
  |          |-SPT req------→|  |          |          |
  |          |<-SPT token----|  |          |          |
  |          |         |         |          |          |
  |          |-Payment------→|  |--Validate----→|     |
  |          | Mandate+SPT   |  |<-Approved-----|     |
  |          |         |         |          |          |
  |          |<-Fulfilled----|  |          |          |
  |-Notify→|         |         |          |          |
  | "Purchased!"      |         |          |          |
```

### A.3 Error Handling and Rollback

```
Agent      ACP        AP2       Stripe    Payment
         Merchant   Protocol             Network
  |          |          |          |          |
  |-Cart req-→|          |          |          |
  |<-Cart----|          |          |          |
  |          |          |          |          |
  |-Intent------------→|          |          |
  |-Cart-------------→|          |          |
  |          |          |          |          |
  |-SPT req-------→|   |          |          |
  |<-SPT---------|   |          |          |
  |          |          |          |          |
  |-Payment---------→|  |-Auth req------→|  |
  |          |          |  |<-DECLINED--|  |
  |          |          |  |          |     |
  | [PAYMENT FAILED]     |          |     |
  |          |          |  |          |     |
  |-Void SPT------→|   |  |          |     |
  |<-Voided------|   |  |          |     |
  |          |          |  |          |     |
  |-Cancel order-→|     |  |          |     |
  |<-Canceled----|     |  |          |     |
  |          |          |  |          |     |
  |-Mark mandate as failed-→|        |     |
  |          |          |  |          |     |
  |-Notify user of failure   |        |     |
```

---

## Appendix B: Data Schema Examples

### B.1 Unified Transaction Record

```json
{
  "transaction": {
    "universal_id": "UO-2025-09-30-ABC123",
    "status": "completed",
    "created_at": "2025-09-30T14:23:15Z",
    "completed_at": "2025-09-30T14:25:20Z",

    "user": {
      "id": "user_xyz789",
      "email": "user@example.com",
      "verification_status": "verified"
    },

    "agent": {
      "id": "chatgpt_agent_42",
      "platform": "OpenAI ChatGPT",
      "version": "4.5"
    },

    "acp_order": {
      "order_id": "acp_order_abc123",
      "merchant": {
        "id": "shopify_merchant_123",
        "name": "ShopifyStore",
        "platform": "Shopify"
      },
      "items": [
        {
          "sku": "SHOE-RUN-001",
          "name": "Running Shoes - Blue",
          "quantity": 1,
          "unit_price": 120.00,
          "total": 120.00
        }
      ],
      "subtotal": 120.00,
      "shipping": 5.00,
      "tax": 0.00,
      "total": 125.00,
      "currency": "USD"
    },

    "ap2_mandates": {
      "intent_mandate": {
        "id": "intent_def456",
        "created_at": "2025-09-30T14:23:20Z",
        "user_signature": "sig_user_intent_...",
        "constraints": {
          "max_amount": 150.00,
          "currency": "USD",
          "category": "footwear",
          "approved_merchants": ["shopify_merchant_123"]
        }
      },

      "cart_mandate": {
        "id": "cart_ghi789",
        "created_at": "2025-09-30T14:25:00Z",
        "intent_reference": "intent_def456",
        "user_signature": "sig_user_cart_...",
        "cart_hash": "sha256:a1b2c3...",
        "total": 125.00,
        "currency": "USD"
      },

      "payment_mandate": {
        "id": "payment_jkl012",
        "created_at": "2025-09-30T14:25:10Z",
        "intent_reference": "intent_def456",
        "cart_reference": "cart_ghi789",
        "payment_token_reference": "spt_mno345",
        "amount": 125.00,
        "currency": "USD",
        "network_response": {
          "code": "APPROVED",
          "timestamp": "2025-09-30T14:25:15Z",
          "authorization_id": "auth_pqr678"
        }
      }
    },

    "payment_credential": {
      "type": "shared_payment_token",
      "spt_id": "spt_mno345",
      "issued_by": "Stripe",
      "issued_at": "2025-09-30T14:25:08Z",
      "scope": {
        "merchant_id": "shopify_merchant_123",
        "max_amount": 125.00,
        "currency": "USD",
        "single_use": true
      },
      "status": "redeemed",
      "redeemed_at": "2025-09-30T14:25:15Z"
    },

    "reconciliation": {
      "acp_total": 125.00,
      "ap2_total": 125.00,
      "amounts_match": true,
      "merchant_match": true,
      "status": "reconciled"
    },

    "audit_trail": [
      {
        "timestamp": "2025-09-30T14:23:15Z",
        "event": "user_intent_captured",
        "actor": "user_xyz789"
      },
      {
        "timestamp": "2025-09-30T14:23:18Z",
        "event": "acp_product_search",
        "actor": "chatgpt_agent_42",
        "query": "running shoes blue"
      },
      {
        "timestamp": "2025-09-30T14:24:30Z",
        "event": "acp_cart_created",
        "actor": "chatgpt_agent_42",
        "order_id": "acp_order_abc123"
      },
      {
        "timestamp": "2025-09-30T14:24:45Z",
        "event": "ap2_intent_mandate_created",
        "actor": "chatgpt_agent_42",
        "mandate_id": "intent_def456"
      },
      {
        "timestamp": "2025-09-30T14:25:00Z",
        "event": "ap2_cart_mandate_signed",
        "actor": "user_xyz789",
        "mandate_id": "cart_ghi789"
      },
      {
        "timestamp": "2025-09-30T14:25:08Z",
        "event": "spt_issued",
        "actor": "stripe",
        "token_id": "spt_mno345"
      },
      {
        "timestamp": "2025-09-30T14:25:10Z",
        "event": "ap2_payment_mandate_created",
        "actor": "chatgpt_agent_42",
        "mandate_id": "payment_jkl012"
      },
      {
        "timestamp": "2025-09-30T14:25:15Z",
        "event": "payment_authorized",
        "actor": "payment_network",
        "authorization_id": "auth_pqr678"
      },
      {
        "timestamp": "2025-09-30T14:25:18Z",
        "event": "acp_order_fulfilled",
        "actor": "shopify_merchant_123"
      },
      {
        "timestamp": "2025-09-30T14:25:20Z",
        "event": "transaction_completed",
        "actor": "system"
      }
    ]
  }
}
```

### B.2 Token Binding Schema

```json
{
  "token_binding": {
    "binding_id": "bind_xyz123",
    "created_at": "2025-09-30T14:25:08Z",

    "acp_token": {
      "spt_id": "spt_mno345",
      "issuer": "Stripe",
      "scope": {
        "merchant_id": "shopify_merchant_123",
        "max_amount": 125.00,
        "currency": "USD"
      }
    },

    "ap2_mandate": {
      "cart_mandate_id": "cart_ghi789",
      "cart_hash": "sha256:a1b2c3...",
      "total": 125.00,
      "currency": "USD"
    },

    "binding_attestation": {
      "spt_matches_mandate": true,
      "amount_matches": true,
      "merchant_matches": true,
      "signature": "sig_binding_...",
      "timestamp": "2025-09-30T14:25:08Z"
    },

    "validation_rules": {
      "spt_can_only_be_used_with_mandate": "cart_ghi789",
      "mandate_can_only_use_token": "spt_mno345",
      "both_must_be_present_for_payment": true
    }
  }
}
```

---

## Document Control

**Version:** 1.0
**Date:** September 30, 2025
**Author:** Hive Mind Systems Architect
**Review Status:** Complete
**Next Review:** December 31, 2025

**Change Log:**
- v1.0 (2025-09-30): Initial comprehensive architecture document

**Related Documents:**
- `/epics/active/a2p/research/ap2-protocol-overview.md`
- `/epics/active/a2p/research/a2p-protocol.md`
- `/epics/active/a2p/analysis/pci-dss-standards-analysis.md`
- `/epics/active/a2p/EXECUTIVE-SUMMARY.md`

---

*This architecture document provides a comprehensive framework for integrating Google's AP2 and Stripe/OpenAI's ACP protocols to create a trusted agentic commerce stack. Implementation should follow PCI-DSS requirements and industry best practices.*
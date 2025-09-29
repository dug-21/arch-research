# AP2 Protocol - Quick Reference Guide

**Last Updated**: September 29, 2025

---

## What is AP2?

**Agent Payments Protocol (AP2)** - An open protocol by Google for secure AI agent payments.

**Important**: It's "AP2" (Agent Payments Protocol), not "A2P" (Application-to-Person messaging).

---

## The 3-Minute Overview

### Purpose
Enable AI agents to make payments on behalf of users with verifiable authorization.

### Three Core Challenges Solved
1. **Authorization** - Prove agent has permission
2. **Authenticity** - Ensure transaction reflects user intent
3. **Accountability** - Clear responsibility for transactions

### How It Works
Uses cryptographically signed digital contracts called **Mandates**:

- **Intent Mandate** - Authorizes agent with rules (price limits, timing)
- **Cart Mandate** - User approves specific purchase
- **Payment Mandate** - Signals AI involvement to payment networks

---

## Key Features

✅ **Open Source** - Public GitHub repository
✅ **Privacy-First** - Protects user data
✅ **Payment Agnostic** - Cards, crypto, bank transfers
✅ **Cryptographic Security** - Tamper-proof authorization
✅ **Global Support** - 60+ partners including Mastercard, PayPal, Coinbase

---

## Two Transaction Modes

### Human-Present
1. User interacts with agent
2. Agent finds products
3. User reviews and signs cart
4. Transaction executes

### Human-Not-Present
1. User sets rules upfront (budget, timing)
2. Agent monitors conditions
3. Auto-executes when conditions met
4. Full audit trail maintained

---

## Use Cases

### Consumer
- Automated purchases (concert tickets, deals)
- Price monitoring and optimal buying
- Recurring transactions (groceries)
- Complex bookings (travel, events)

### Enterprise
- Procurement automation
- Software licensing management
- Cloud marketplace integration
- Business process automation

---

## Technology Stack

**Built on**: Agent2Agent (A2A) + Model Context Protocol (MCP)

**Supports**:
- Credit/debit cards
- Cryptocurrencies & stablecoins
- Real-time bank transfers (future)

**Security**:
- Hardware-backed cryptographic keys
- Non-repudiable audit trails
- PSD2 & GDPR considerations

---

## Key Partners (60+)

**Payments**: Mastercard, Visa, American Express, PayPal, Adyen

**Crypto**: Coinbase, MetaMask, Ethereum Foundation

**Tech**: Salesforce, Shopify, Cloudflare, Etsy

---

## Resources

**Official Site**: https://ap2-protocol.org/

**Specification**: https://ap2-protocol.org/specification/

**Announcement**: https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol

**GitHub**: Public repository (search for "ap2-protocol")

---

## Status & Timeline

**Launch**: September 2025
**Current Version**: V0.1
**Status**: Open development, seeking community feedback

**Roadmap**:
- V1.x: Expanded payment methods
- Future: Complex multi-merchant transactions

---

## Implementation Quick Start

1. Review specification at ap2-protocol.org
2. Access GitHub reference implementations
3. Integrate with A2A/MCP protocols
4. Test with supported payment methods
5. Deploy with mandate verification

---

## Key Technical Terms

**VDC** - Verifiable Digital Credential
**Intent Mandate** - Authorization with conditions
**Cart Mandate** - Explicit purchase approval
**Payment Mandate** - Network notification
**CP** - Credential Provider
**MPP** - Merchant Payment Processor

---

## Security Principles

1. **Verifiable Intent** - Cryptographic proof required
2. **Privacy by Design** - Minimal data exposure
3. **Audit Trail** - Complete transaction history
4. **User Control** - Users maintain authority
5. **Accountability** - Clear responsibility chain

---

## Why AP2 Matters

🎯 **Foundation for AI Commerce** - Enables autonomous agent economy
🔐 **Trust Infrastructure** - Verifiable transactions reduce fraud
🌐 **Universal Standard** - Prevents ecosystem fragmentation
🚀 **Industry Backed** - 60+ major partners at launch
📈 **Future-Proof** - Designed for evolution

---

**For More Details**: See comprehensive research document at `/epics/active/a2p/research/a2p-protocol.md`
# Payment System Integration Strategies

## Executive Summary

This document outlines comprehensive integration strategies for payment systems, covering third-party payment processors, banking systems, merchant platforms, and regulatory compliance interfaces. Each strategy includes implementation patterns, best practices, and real-world examples.

## Table of Contents

1. [Integration Architecture Overview](#integration-architecture-overview)
2. [Payment Processor Integration](#payment-processor-integration)
3. [Banking System Integration](#banking-system-integration)
4. [Merchant Platform Integration](#merchant-platform-integration)
5. [Regulatory Compliance Integration](#regulatory-compliance-integration)
6. [Integration Patterns](#integration-patterns)
7. [Security Considerations](#security-considerations)
8. [Testing Strategies](#testing-strategies)

## Integration Architecture Overview

### Core Principles

1. **Abstraction**: Hide provider-specific details
2. **Resilience**: Handle failures gracefully
3. **Flexibility**: Support multiple providers
4. **Security**: Protect sensitive data
5. **Observability**: Monitor all integrations

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Integration Layer                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Adapter   │  │   Adapter   │  │   Adapter   │  ...   │
│  │   Pattern   │  │   Pattern   │  │   Pattern   │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                 │                 │                │
├─────────┴─────────────────┴─────────────────┴──────────────┤
│                  Orchestration Layer                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Routing   │  │   Retry     │  │  Fallback   │        │
│  │   Logic     │  │   Logic     │  │   Logic     │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│                  External Systems                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Payment   │  │   Banking   │  │  Merchant   │        │
│  │  Processors │  │   Systems   │  │  Platforms  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## Payment Processor Integration

### Major Payment Processors

#### Stripe Integration

```typescript
// Stripe adapter implementation
import Stripe from 'stripe';
import { PaymentAdapter, PaymentRequest, PaymentResponse } from './types';

export class StripeAdapter implements PaymentAdapter {
  private stripe: Stripe;
  private webhookSecret: string;
  
  constructor(config: StripeConfig) {
    this.stripe = new Stripe(config.secretKey, {
      apiVersion: '2023-10-16',
      typescript: true,
      maxNetworkRetries: 3,
      timeout: 30000, // 30 seconds
    });
    this.webhookSecret = config.webhookSecret;
  }
  
  async createPayment(request: PaymentRequest): Promise<PaymentResponse> {
    try {
      // Create payment intent
      const paymentIntent = await this.stripe.paymentIntents.create({
        amount: request.amount,
        currency: request.currency,
        payment_method: request.paymentMethodId,
        confirmation_method: 'manual',
        capture_method: request.capture ? 'automatic' : 'manual',
        metadata: {
          order_id: request.orderId,
          customer_id: request.customerId,
          merchant_reference: request.merchantReference,
        },
        idempotency_key: request.idempotencyKey,
      });
      
      // Confirm payment intent
      const confirmed = await this.stripe.paymentIntents.confirm(
        paymentIntent.id,
        { payment_method: request.paymentMethodId }
      );
      
      return {
        id: confirmed.id,
        status: this.mapStatus(confirmed.status),
        amount: confirmed.amount,
        currency: confirmed.currency,
        processorResponse: confirmed,
      };
    } catch (error) {
      throw this.handleStripeError(error);
    }
  }
  
  async capturePayment(paymentId: string, amount?: number): Promise<PaymentResponse> {
    const captured = await this.stripe.paymentIntents.capture(paymentId, {
      amount_to_capture: amount,
    });
    
    return {
      id: captured.id,
      status: 'captured',
      amount: captured.amount_received,
      currency: captured.currency,
      processorResponse: captured,
    };
  }
  
  async refundPayment(paymentId: string, amount?: number, reason?: string): Promise<RefundResponse> {
    const refund = await this.stripe.refunds.create({
      payment_intent: paymentId,
      amount: amount,
      reason: this.mapRefundReason(reason),
      metadata: {
        internal_reason: reason,
      },
    });
    
    return {
      id: refund.id,
      status: refund.status,
      amount: refund.amount,
      currency: refund.currency,
      processorResponse: refund,
    };
  }
  
  async verifyWebhook(payload: string, signature: string): Promise<any> {
    try {
      return this.stripe.webhooks.constructEvent(
        payload,
        signature,
        this.webhookSecret
      );
    } catch (err) {
      throw new WebhookVerificationError('Invalid webhook signature');
    }
  }
  
  private mapStatus(stripeStatus: string): PaymentStatus {
    const statusMap: Record<string, PaymentStatus> = {
      'requires_payment_method': 'pending',
      'requires_confirmation': 'pending',
      'requires_action': 'requires_action',
      'processing': 'processing',
      'requires_capture': 'authorized',
      'canceled': 'cancelled',
      'succeeded': 'completed',
    };
    
    return statusMap[stripeStatus] || 'unknown';
  }
  
  private handleStripeError(error: any): Error {
    if (error.type === 'StripeCardError') {
      return new PaymentDeclinedError(error.message, error.code);
    } else if (error.type === 'StripeRateLimitError') {
      return new RateLimitError('Rate limit exceeded');
    } else if (error.type === 'StripeConnectionError') {
      return new ConnectionError('Network error');
    }
    
    return new PaymentProcessingError(error.message);
  }
}
```

#### PayPal/Braintree Integration

```java
@Component
public class BraintreeAdapter implements PaymentAdapter {
    
    private final BraintreeGateway gateway;
    private final MeterRegistry metrics;
    private final CircuitBreaker circuitBreaker;
    
    public BraintreeAdapter(BraintreeConfig config, MeterRegistry metrics) {
        this.gateway = new BraintreeGateway(
            config.getEnvironment(),
            config.getMerchantId(),
            config.getPublicKey(),
            config.getPrivateKey()
        );
        this.metrics = metrics;
        this.circuitBreaker = CircuitBreaker.ofDefaults("braintree");
    }
    
    @Override
    public PaymentResponse createPayment(PaymentRequest request) {
        return circuitBreaker.executeSupplier(() -> {
            Timer.Sample sample = Timer.start(metrics);
            try {
                TransactionRequest txRequest = new TransactionRequest()
                    .amount(request.getAmount())
                    .paymentMethodNonce(request.getNonce())
                    .orderId(request.getOrderId())
                    .customerId(request.getCustomerId())
                    .merchantAccountId(request.getMerchantAccountId())
                    .options()
                        .submitForSettlement(!request.isAuthOnly())
                        .done();
                
                Result<Transaction> result = gateway.transaction().sale(txRequest);
                
                if (result.isSuccess()) {
                    Transaction transaction = result.getTarget();
                    return PaymentResponse.builder()
                        .id(transaction.getId())
                        .status(mapStatus(transaction.getStatus()))
                        .amount(transaction.getAmount())
                        .currency(transaction.getCurrencyIsoCode())
                        .processorResponse(transaction)
                        .build();
                } else {
                    throw new PaymentProcessingException(
                        result.getMessage(),
                        result.getErrors().getAllDeepValidationErrors()
                    );
                }
            } finally {
                sample.stop(metrics.timer("braintree.transaction.duration"));
            }
        });
    }
    
    @Override
    public WebhookResponse parseWebhook(String signature, String payload) {
        WebhookNotification notification = gateway.webhookNotification()
            .parse(signature, payload);
        
        return WebhookResponse.builder()
            .eventType(notification.getKind().toString())
            .timestamp(notification.getTimestamp().getTime())
            .data(notification)
            .build();
    }
}
```

#### Square Integration

```python
from square import Client
from square.models import CreatePaymentRequest, Money
from typing import Optional
import asyncio
from dataclasses import dataclass

@dataclass
class SquareConfig:
    access_token: str
    environment: str
    location_id: str
    webhook_signature_key: str

class SquareAdapter(PaymentAdapter):
    def __init__(self, config: SquareConfig):
        self.client = Client(
            access_token=config.access_token,
            environment=config.environment
        )
        self.location_id = config.location_id
        self.webhook_key = config.webhook_signature_key
        
    async def create_payment(self, request: PaymentRequest) -> PaymentResponse:
        try:
            # Build payment request
            square_request = CreatePaymentRequest(
                source_id=request.source_id,
                idempotency_key=request.idempotency_key,
                amount_money=Money(
                    amount=request.amount,
                    currency=request.currency
                ),
                order_id=request.order_id,
                customer_id=request.customer_id,
                location_id=self.location_id,
                reference_id=request.merchant_reference,
                note=request.description,
                autocomplete=not request.auth_only
            )
            
            # Execute payment
            result = self.client.payments.create_payment(square_request)
            
            if result.is_success():
                payment = result.body['payment']
                return PaymentResponse(
                    id=payment['id'],
                    status=self._map_status(payment['status']),
                    amount=payment['amount_money']['amount'],
                    currency=payment['amount_money']['currency'],
                    processor_response=payment
                )
            else:
                raise PaymentProcessingError(
                    f"Square payment failed: {result.errors}"
                )
                
        except Exception as e:
            logger.error(f"Square payment error: {e}")
            raise self._handle_square_error(e)
    
    async def create_customer(self, customer_data: dict) -> dict:
        """Create customer profile for recurring payments"""
        result = self.client.customers.create_customer(
            body={
                "given_name": customer_data.get('first_name'),
                "family_name": customer_data.get('last_name'),
                "email_address": customer_data.get('email'),
                "phone_number": customer_data.get('phone'),
                "reference_id": customer_data.get('external_id'),
                "note": "Created via payment integration"
            }
        )
        
        if result.is_success():
            return result.body['customer']
        else:
            raise CustomerCreationError(f"Failed to create customer: {result.errors}")
    
    def verify_webhook(self, signature: str, body: str) -> bool:
        """Verify Square webhook signature"""
        import hmac
        import hashlib
        import base64
        
        # Square webhook verification
        computed_signature = base64.b64encode(
            hmac.new(
                self.webhook_key.encode('utf-8'),
                body.encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode('utf-8')
        
        return hmac.compare_digest(computed_signature, signature)
```

### Multi-Provider Orchestration

```go
package payment

import (
    "context"
    "fmt"
    "sync"
    "time"
)

type ProviderOrchestrator struct {
    providers     map[string]PaymentProvider
    routingRules  RoutingStrategy
    metrics       MetricsCollector
    circuitBreaker CircuitBreaker
}

// Route payment to optimal provider
func (o *ProviderOrchestrator) ProcessPayment(
    ctx context.Context,
    request PaymentRequest,
) (*PaymentResponse, error) {
    // Select provider based on routing rules
    providerID := o.routingRules.SelectProvider(request)
    
    // Try primary provider
    provider, exists := o.providers[providerID]
    if !exists {
        return nil, fmt.Errorf("provider %s not found", providerID)
    }
    
    // Check circuit breaker
    if !o.circuitBreaker.IsAvailable(providerID) {
        // Fallback to secondary provider
        providerID = o.routingRules.GetFallbackProvider(providerID)
        provider = o.providers[providerID]
    }
    
    // Process with timeout
    ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
    defer cancel()
    
    start := time.Now()
    response, err := provider.ProcessPayment(ctx, request)
    duration := time.Since(start)
    
    // Record metrics
    o.metrics.RecordPayment(providerID, request, response, err, duration)
    
    if err != nil {
        // Try fallback if available
        if fallback := o.routingRules.GetFallbackProvider(providerID); fallback != "" {
            return o.providers[fallback].ProcessPayment(ctx, request)
        }
        return nil, err
    }
    
    return response, nil
}

// Load balancing across providers
type LoadBalancedRouter struct {
    providers []string
    weights   map[string]int
    counter   uint64
    mu        sync.RWMutex
}

func (r *LoadBalancedRouter) SelectProvider(request PaymentRequest) string {
    r.mu.RLock()
    defer r.mu.RUnlock()
    
    // Special routing rules
    if request.Amount > 10000 { // High-value transactions
        return "stripe" // Most reliable for large amounts
    }
    
    if request.Currency == "BTC" {
        return "coinbase" // Crypto specialist
    }
    
    if request.PaymentMethod == "paypal" {
        return "braintree" // PayPal owned
    }
    
    // Weighted round-robin for others
    totalWeight := 0
    for _, weight := range r.weights {
        totalWeight += weight
    }
    
    target := atomic.AddUint64(&r.counter, 1) % uint64(totalWeight)
    current := uint64(0)
    
    for provider, weight := range r.weights {
        current += uint64(weight)
        if target < current {
            return provider
        }
    }
    
    return r.providers[0] // Default fallback
}
```

## Banking System Integration

### ACH Integration

```python
# Modern Treasury integration for ACH
from modern_treasury import ModernTreasuryClient
from datetime import datetime, timedelta
import asyncio

class ACHIntegration:
    def __init__(self, api_key: str, organization_id: str):
        self.client = ModernTreasuryClient(
            api_key=api_key,
            organization_id=organization_id
        )
        self.originating_account_id = self._get_originating_account()
        
    async def create_ach_payment(
        self,
        amount: int,
        direction: str,  # 'debit' or 'credit'
        account_number: str,
        routing_number: str,
        account_type: str,  # 'checking' or 'savings'
        customer_name: str,
        reference: str
    ) -> dict:
        """Create ACH payment order"""
        
        # Create counterparty
        counterparty = await self.client.counterparties.create(
            name=customer_name,
            accounts=[{
                "account_type": "checking",
                "routing_details": [{
                    "routing_number_type": "aba",
                    "routing_number": routing_number
                }],
                "account_details": [{
                    "account_number": account_number
                }]
            }]
        )
        
        # Create payment order
        payment_order = await self.client.payment_orders.create(
            type="ach",
            amount=amount,
            direction=direction,
            currency="USD",
            originating_account_id=self.originating_account_id,
            receiving_account_id=counterparty.accounts[0].id,
            accounting_category_id=self._get_accounting_category(direction),
            metadata={
                "reference": reference,
                "customer_name": customer_name
            },
            effective_date=datetime.now().date(),
            priority="normal",
            fallback_type="check",  # Mail check if ACH fails
            charge_bearer="shared"
        )
        
        return {
            "id": payment_order.id,
            "status": payment_order.status,
            "amount": payment_order.amount,
            "reference": reference,
            "expected_settlement": payment_order.effective_date
        }
    
    async def create_batch_ach(self, transactions: List[ACHTransaction]) -> dict:
        """Create batch ACH file"""
        
        # Group by effective date and direction
        batches = self._group_transactions(transactions)
        
        results = []
        for batch_key, batch_transactions in batches.items():
            effective_date, direction = batch_key
            
            # Create bulk payment order
            bulk_request = {
                "payments": [
                    {
                        "type": "ach",
                        "amount": txn.amount,
                        "direction": direction,
                        "counterparty_id": await self._get_or_create_counterparty(txn),
                        "metadata": {
                            "reference": txn.reference,
                            "batch_id": batch_key
                        }
                    }
                    for txn in batch_transactions
                ],
                "effective_date": effective_date,
                "metadata": {
                    "batch_type": "scheduled_payments",
                    "total_count": len(batch_transactions),
                    "total_amount": sum(t.amount for t in batch_transactions)
                }
            }
            
            bulk_result = await self.client.bulk_requests.create(
                resource_type="payment_order",
                resources=bulk_request
            )
            
            results.append({
                "batch_id": bulk_result.id,
                "status": bulk_result.status,
                "count": len(batch_transactions),
                "total_amount": sum(t.amount for t in batch_transactions),
                "effective_date": effective_date
            })
        
        return {
            "batches": results,
            "total_transactions": sum(r["count"] for r in results),
            "total_amount": sum(r["total_amount"] for r in results)
        }
    
    async def handle_return(self, return_data: dict) -> dict:
        """Handle ACH returns"""
        return_code = return_data.get("return_code")
        
        # Map return codes to actions
        return_actions = {
            "R01": "insufficient_funds",
            "R02": "account_closed",
            "R03": "no_account",
            "R04": "invalid_account",
            "R05": "unauthorized_debit",
            "R07": "authorization_revoked",
            "R08": "payment_stopped",
            "R09": "uncollected_funds",
            "R10": "customer_advises_unauthorized",
            "R29": "corporate_customer_advises_not_authorized"
        }
        
        action = return_actions.get(return_code, "manual_review")
        
        # Update payment status
        await self._update_payment_status(
            payment_id=return_data["payment_id"],
            status="returned",
            return_code=return_code,
            return_reason=return_data.get("return_reason"),
            action_required=action
        )
        
        # Trigger appropriate workflow
        if action == "insufficient_funds":
            await self._schedule_retry(return_data["payment_id"], days=3)
        elif action in ["unauthorized_debit", "authorization_revoked"]:
            await self._flag_for_review(return_data["payment_id"], "compliance")
        
        return {
            "payment_id": return_data["payment_id"],
            "return_code": return_code,
            "action": action,
            "resolution": "pending"
        }
```

### Wire Transfer Integration

```java
@Service
public class WireTransferService {
    
    private final SWIFTClient swiftClient;
    private final FedwireClient fedwireClient;
    private final ComplianceService complianceService;
    private final AuditService auditService;
    
    public WireTransferResponse initiateWireTransfer(WireTransferRequest request) {
        // Compliance checks
        ComplianceResult complianceCheck = complianceService.screenTransfer(request);
        if (!complianceCheck.isApproved()) {
            throw new ComplianceException("Transfer blocked: " + complianceCheck.getReason());
        }
        
        // Route to appropriate network
        WireTransferResponse response;
        if (request.isInternational()) {
            response = processSWIFTTransfer(request);
        } else {
            response = processFedwireTransfer(request);
        }
        
        // Audit trail
        auditService.logWireTransfer(request, response);
        
        return response;
    }
    
    private WireTransferResponse processSWIFTTransfer(WireTransferRequest request) {
        // Build MT103 message
        MT103Message mt103 = MT103Message.builder()
            .messageType("103")
            .sender(request.getSender())
            .receiver(request.getReceiver())
            .transactionReference(generateReference())
            .currencyAmount(request.getAmount())
            .orderingCustomer(request.getOrderingCustomer())
            .beneficiaryCustomer(request.getBeneficiaryCustomer())
            .remittanceInformation(request.getRemittanceInfo())
            .chargesCode("SHA") // Shared charges
            .build();
        
        // Add intermediary bank if needed
        if (request.hasIntermediaryBank()) {
            mt103.setIntermediaryInstitution(request.getIntermediaryBank());
        }
        
        // Send via SWIFT
        SWIFTResponse swiftResponse = swiftClient.sendMessage(mt103);
        
        return WireTransferResponse.builder()
            .transferId(swiftResponse.getUetr()) // Unique End-to-end Transaction Reference
            .status("sent")
            .network("SWIFT")
            .estimatedCompletion(calculateSWIFTCompletion(request))
            .trackingUrl(generateTrackingUrl(swiftResponse.getUetr()))
            .build();
    }
    
    private WireTransferResponse processFedwireTransfer(WireTransferRequest request) {
        // Build Fedwire message
        FedwireMessage message = FedwireMessage.builder()
            .imad(generateIMAD()) // Input Message Accountability Data
            .amount(request.getAmount())
            .senderABA(request.getSenderRoutingNumber())
            .receiverABA(request.getReceiverRoutingNumber())
            .beneficiaryAccount(request.getBeneficiaryAccount())
            .originatorToBeneficiary(request.getRemittanceInfo())
            .build();
        
        // Send via Fedwire
        FedwireResponse fedResponse = fedwireClient.sendTransfer(message);
        
        return WireTransferResponse.builder()
            .transferId(fedResponse.getImad())
            .status("completed")
            .network("Fedwire")
            .completionTime(Instant.now())
            .confirmationNumber(fedResponse.getConfirmation())
            .build();
    }
}
```

### Open Banking Integration

```typescript
// Plaid integration for account verification and balance checks
import { PlaidApi, PlaidEnvironments, Configuration } from 'plaid';

export class OpenBankingService {
  private plaidClient: PlaidApi;
  
  constructor(config: OpenBankingConfig) {
    const configuration = new Configuration({
      basePath: PlaidEnvironments[config.environment],
      baseOptions: {
        headers: {
          'PLAID-CLIENT-ID': config.clientId,
          'PLAID-SECRET': config.secret,
        },
      },
    });
    
    this.plaidClient = new PlaidApi(configuration);
  }
  
  async verifyBankAccount(publicToken: string): Promise<BankAccountVerification> {
    // Exchange public token for access token
    const { data: { access_token } } = await this.plaidClient.itemPublicTokenExchange({
      public_token: publicToken,
    });
    
    // Get account details
    const { data: { accounts } } = await this.plaidClient.accountsGet({
      access_token,
    });
    
    // Get identity verification
    const { data: { identity } } = await this.plaidClient.identityGet({
      access_token,
    });
    
    // Get balance for verification
    const { data: { accounts: balances } } = await this.plaidClient.accountsBalanceGet({
      access_token,
    });
    
    return {
      verified: true,
      accounts: accounts.map(account => ({
        id: account.account_id,
        name: account.name,
        type: account.type,
        subtype: account.subtype,
        mask: account.mask,
        balance: {
          available: balances.find(b => b.account_id === account.account_id)?.balances.available,
          current: balances.find(b => b.account_id === account.account_id)?.balances.current,
        },
        identity: identity.identity.find(i => i.account_id === account.account_id),
      })),
      access_token,
    };
  }
  
  async initiateACHTransfer(
    accessToken: string,
    accountId: string,
    amount: number,
    direction: 'debit' | 'credit'
  ): Promise<TransferResponse> {
    // Create transfer
    const { data: transfer } = await this.plaidClient.transferCreate({
      access_token: accessToken,
      account_id: accountId,
      amount: amount.toString(),
      currency: 'USD',
      direction,
      description: `Payment ${direction}`,
      ach_class: 'web',
      user: {
        email_address: 'customer@example.com',
      },
      metadata: {
        order_id: generateOrderId(),
      },
    });
    
    // Get transfer status
    const { data: { transfer: status } } = await this.plaidClient.transferGet({
      transfer_id: transfer.transfer.id,
    });
    
    return {
      id: transfer.transfer.id,
      status: status.status,
      amount: parseFloat(status.amount),
      direction: status.direction,
      created: status.created,
      expected_settlement: status.expected_sweep_settlement_schedule,
    };
  }
}
```

## Merchant Platform Integration

### E-commerce Platform Integration

```python
# Shopify integration
import shopify
from typing import List, Dict, Optional
import hmac
import hashlib

class ShopifyIntegration:
    def __init__(self, shop_domain: str, api_key: str, api_secret: str):
        self.shop_domain = shop_domain
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = self._create_session()
        
    def _create_session(self):
        session = shopify.Session(
            self.shop_domain,
            self.api_key,
            self.api_secret
        )
        shopify.ShopifyResource.activate_session(session)
        return session
    
    async def create_payment_gateway(self) -> Dict:
        """Register as payment gateway"""
        gateway_config = {
            "payment_gateway": {
                "name": "Custom Payment Gateway",
                "provider_id": "custom_gateway",
                "enabled": True,
                "supports_network_tokenization": True,
                "supported_payment_methods": [
                    "credit_card",
                    "debit_card",
                    "digital_wallet"
                ],
                "configuration": {
                    "api_endpoint": "https://api.payment.com",
                    "test_mode": False,
                    "supported_currencies": ["USD", "EUR", "GBP"],
                    "supported_countries": ["US", "CA", "GB", "EU"]
                }
            }
        }
        
        return await self._api_call("POST", "/admin/api/2023-10/payment_gateways.json", gateway_config)
    
    async def process_checkout_payment(self, checkout_token: str, payment_data: Dict) -> Dict:
        """Process payment for Shopify checkout"""
        
        # Get checkout details
        checkout = await self._get_checkout(checkout_token)
        
        # Create payment session
        payment_session = {
            "payment_session": {
                "amount": checkout["total_price"],
                "currency": checkout["currency"],
                "test": self._is_test_mode(),
                "kind": "sale",
                "gateway": "custom_gateway",
                "payment_details": {
                    "credit_card_number": payment_data["card_number"],
                    "credit_card_verification_value": payment_data["cvv"],
                    "credit_card_name": payment_data["cardholder_name"],
                    "credit_card_month": payment_data["exp_month"],
                    "credit_card_year": payment_data["exp_year"]
                }
            }
        }
        
        # Process payment
        result = await self._api_call(
            "POST",
            f"/admin/api/2023-10/checkouts/{checkout_token}/payments.json",
            payment_session
        )
        
        # Complete checkout if payment successful
        if result["payment"]["status"] == "success":
            order = await self._complete_checkout(checkout_token)
            return {
                "success": True,
                "order_id": order["id"],
                "payment_id": result["payment"]["id"],
                "amount": result["payment"]["amount"]
            }
        
        return {
            "success": False,
            "error": result["payment"]["error_message"]
        }
    
    def verify_webhook(self, data: bytes, hmac_header: str) -> bool:
        """Verify Shopify webhook signature"""
        calculated_hmac = hmac.new(
            self.api_secret.encode('utf-8'),
            data,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(calculated_hmac, hmac_header)
    
    async def handle_webhook(self, topic: str, data: Dict) -> None:
        """Process Shopify webhooks"""
        handlers = {
            "orders/create": self._handle_order_created,
            "orders/updated": self._handle_order_updated,
            "orders/cancelled": self._handle_order_cancelled,
            "refunds/create": self._handle_refund_created,
        }
        
        handler = handlers.get(topic)
        if handler:
            await handler(data)
```

### POS System Integration

```java
// Square POS integration
@RestController
@RequestMapping("/api/pos")
public class POSIntegrationController {
    
    private final SquareClient squareClient;
    private final PaymentService paymentService;
    private final WebSocketService webSocketService;
    
    @PostMapping("/terminals/{terminalId}/checkout")
    public ResponseEntity<TerminalCheckoutResponse> createTerminalCheckout(
        @PathVariable String terminalId,
        @RequestBody TerminalCheckoutRequest request
    ) {
        // Create terminal checkout
        TerminalCheckout checkout = TerminalCheckout.builder()
            .amountMoney(Money.builder()
                .amount(request.getAmount())
                .currency("USD")
                .build())
            .referenceId(request.getReferenceId())
            .note(request.getDescription())
            .deviceOptions(DeviceCheckoutOptions.builder()
                .deviceId(terminalId)
                .skipReceiptScreen(false)
                .tipSettings(TipSettings.builder()
                    .allowTipping(true)
                    .separateTipScreen(true)
                    .customTipField(false)
                    .build())
                .build())
            .paymentOptions(PaymentOptions.builder()
                .autocomplete(true)
                .acceptPartialAuthorization(false)
                .build())
            .build();
        
        CreateTerminalCheckoutResponse response = squareClient.getTerminalApi()
            .createTerminalCheckout(checkout)
            .execute();
        
        if (response.getErrors() != null) {
            throw new POSException("Failed to create checkout: " + response.getErrors());
        }
        
        // Set up webhook for status updates
        scheduleStatusPolling(response.getCheckout().getId());
        
        return ResponseEntity.ok(TerminalCheckoutResponse.builder()
            .checkoutId(response.getCheckout().getId())
            .status("PENDING")
            .deviceId(terminalId)
            .amount(request.getAmount())
            .build());
    }
    
    @PostMapping("/terminals/{terminalId}/refund")
    public ResponseEntity<TerminalRefundResponse> createTerminalRefund(
        @PathVariable String terminalId,
        @RequestBody TerminalRefundRequest request
    ) {
        // Create terminal refund
        TerminalRefund refund = TerminalRefund.builder()
            .paymentId(request.getPaymentId())
            .amountMoney(Money.builder()
                .amount(request.getAmount())
                .currency("USD")
                .build())
            .reason(request.getReason())
            .deviceId(terminalId)
            .build();
        
        CreateTerminalRefundResponse response = squareClient.getTerminalApi()
            .createTerminalRefund(refund)
            .execute();
        
        return ResponseEntity.ok(TerminalRefundResponse.builder()
            .refundId(response.getRefund().getId())
            .status(response.getRefund().getStatus())
            .amount(request.getAmount())
            .build());
    }
    
    @EventListener
    public void handleTerminalEvent(TerminalEvent event) {
        // Real-time updates via WebSocket
        webSocketService.sendToUser(
            event.getMerchantId(),
            "/topic/terminal/" + event.getTerminalId(),
            event
        );
        
        // Process based on event type
        switch (event.getType()) {
            case "checkout.completed":
                processCompletedCheckout(event);
                break;
            case "checkout.cancelled":
                processCancelledCheckout(event);
                break;
            case "device.disconnected":
                handleDeviceDisconnection(event);
                break;
        }
    }
}
```

## Cryptocurrency and DeFi Integration

### Blockchain Node Integration

#### Ethereum Integration

```typescript
// Ethereum blockchain integration
import { ethers } from 'ethers';
import { Transaction, BlockchainAdapter } from './types';

export class EthereumAdapter implements BlockchainAdapter {
  private provider: ethers.Provider;
  private signers: Map<string, ethers.Wallet>;
  private contracts: Map<string, ethers.Contract>;
  
  constructor(config: EthereumConfig) {
    // Initialize with multiple providers for reliability
    this.provider = new ethers.FallbackProvider([
      new ethers.JsonRpcProvider(config.primaryNode),
      new ethers.AlchemyProvider(config.network, config.alchemyKey),
      new ethers.InfuraProvider(config.network, config.infuraKey)
    ]);
  }
  
  async sendTransaction(tx: Transaction): Promise<string> {
    const signer = this.signers.get(tx.from);
    if (!signer) throw new Error('Signer not found');
    
    // Optimize gas price
    const gasPrice = await this.optimizeGasPrice();
    
    const transaction = {
      to: tx.to,
      value: ethers.parseEther(tx.amount),
      gasPrice: gasPrice,
      gasLimit: await this.estimateGas(tx),
      nonce: await this.provider.getTransactionCount(tx.from),
      data: tx.data || '0x'
    };
    
    const signedTx = await signer.signTransaction(transaction);
    const receipt = await this.provider.sendTransaction(signedTx);
    
    return receipt.hash;
  }
  
  private async optimizeGasPrice(): Promise<bigint> {
    const block = await this.provider.getBlock('latest');
    const baseFee = block?.baseFeePerGas || 0n;
    
    // EIP-1559 gas optimization
    return baseFee + ethers.parseGwei('2'); // 2 gwei priority fee
  }
}
```

#### Multi-Chain Integration

```typescript
// Cross-chain payment orchestrator
export class CrossChainPaymentOrchestrator {
  private chains: Map<string, BlockchainAdapter>;
  private bridges: Map<string, BridgeAdapter>;
  private priceOracle: PriceOracle;
  
  async executeCrossChainPayment(
    sourceChain: string,
    targetChain: string,
    payment: CrossChainPayment
  ): Promise<CrossChainReceipt> {
    // 1. Check liquidity on target chain
    const liquidity = await this.checkLiquidity(targetChain, payment.token);
    
    if (liquidity < payment.amount) {
      // Use bridge if direct liquidity insufficient
      return await this.bridgePayment(sourceChain, targetChain, payment);
    }
    
    // 2. Execute atomic swap
    const swap = await this.initializeAtomicSwap({
      sourceChain,
      targetChain,
      payment,
      timeout: 3600 // 1 hour timeout
    });
    
    // 3. Monitor and complete swap
    return await this.completeAtomicSwap(swap);
  }
  
  private async bridgePayment(
    source: string,
    target: string,
    payment: CrossChainPayment
  ): Promise<CrossChainReceipt> {
    const bridge = this.selectOptimalBridge(source, target);
    
    // Lock tokens on source chain
    const lockTx = await bridge.lock({
      chain: source,
      token: payment.token,
      amount: payment.amount,
      recipient: payment.recipient
    });
    
    // Wait for confirmations
    await this.waitForConfirmations(source, lockTx.hash, 12);
    
    // Mint/release on target chain
    const releaseTx = await bridge.release({
      chain: target,
      lockTx: lockTx.hash,
      proof: await this.generateProof(lockTx)
    });
    
    return {
      sourceChain: source,
      targetChain: target,
      sourceTx: lockTx.hash,
      targetTx: releaseTx.hash,
      status: 'completed'
    };
  }
}
```

### DeFi Protocol Integration

#### DEX Aggregator Integration

```typescript
// DeFi DEX aggregator integration
export class DexAggregator {
  private providers: Map<string, DexProvider>;
  private slippageCalculator: SlippageCalculator;
  
  async getBestRoute(
    tokenIn: string,
    tokenOut: string,
    amountIn: bigint,
    slippage: number = 0.5
  ): Promise<SwapRoute> {
    // Query multiple DEXs in parallel
    const quotes = await Promise.all([
      this.providers.get('uniswap')?.getQuote(tokenIn, tokenOut, amountIn),
      this.providers.get('sushiswap')?.getQuote(tokenIn, tokenOut, amountIn),
      this.providers.get('curve')?.getQuote(tokenIn, tokenOut, amountIn),
      this.providers.get('balancer')?.getQuote(tokenIn, tokenOut, amountIn)
    ]);
    
    // Find optimal route considering gas costs
    const optimalRoute = await this.optimizeRoute(quotes, slippage);
    
    // Check for MEV protection
    if (await this.requiresMevProtection(amountIn)) {
      optimalRoute.protection = 'flashbots';
    }
    
    return optimalRoute;
  }
  
  async executeSwap(route: SwapRoute): Promise<SwapReceipt> {
    // Validate route freshness
    if (Date.now() - route.timestamp > 30000) {
      throw new Error('Route expired, please refresh quote');
    }
    
    // Execute through router
    const router = this.providers.get(route.dex);
    return await router.swap({
      route: route.path,
      amountIn: route.amountIn,
      minAmountOut: route.minAmountOut,
      deadline: Math.floor(Date.now() / 1000) + 300, // 5 min deadline
      recipient: route.recipient
    });
  }
}
```

#### Lending Protocol Integration

```typescript
// DeFi lending protocol integration
export class LendingProtocolAdapter {
  private protocols: Map<string, LendingProtocol>;
  private riskAnalyzer: RiskAnalyzer;
  
  async deposit(
    protocol: string,
    asset: string,
    amount: bigint
  ): Promise<DepositReceipt> {
    const adapter = this.protocols.get(protocol);
    
    // Check protocol health
    const health = await this.checkProtocolHealth(protocol);
    if (health.utilizationRate > 0.95) {
      throw new Error('Protocol utilization too high');
    }
    
    // Approve and deposit
    await this.approveToken(asset, adapter.address, amount);
    const receipt = await adapter.deposit(asset, amount);
    
    // Return receipt tokens (aTokens, cTokens, etc.)
    return {
      protocol,
      asset,
      amount,
      receiptToken: receipt.token,
      receiptAmount: receipt.amount,
      apy: await adapter.getCurrentAPY(asset)
    };
  }
  
  async borrow(
    protocol: string,
    collateralAsset: string,
    borrowAsset: string,
    borrowAmount: bigint
  ): Promise<BorrowReceipt> {
    const adapter = this.protocols.get(protocol);
    
    // Check collateral factor
    const factor = await adapter.getCollateralFactor(collateralAsset);
    const maxBorrow = await this.calculateMaxBorrow(
      protocol,
      collateralAsset,
      borrowAsset
    );
    
    if (borrowAmount > maxBorrow) {
      throw new Error('Borrow amount exceeds collateral limit');
    }
    
    // Execute borrow
    const receipt = await adapter.borrow(borrowAsset, borrowAmount);
    
    // Monitor health factor
    this.startHealthMonitoring(protocol, receipt.positionId);
    
    return receipt;
  }
}
```

### Stablecoin Integration

```typescript
// Stablecoin payment integration
export class StablecoinPaymentService {
  private stablecoins: Map<string, StablecoinAdapter>;
  private complianceChecker: ComplianceChecker;
  
  async processStablecoinPayment(
    payment: StablecoinPayment
  ): Promise<PaymentReceipt> {
    // 1. Validate stablecoin
    const stablecoin = this.stablecoins.get(payment.currency);
    if (!stablecoin) {
      throw new Error(`Unsupported stablecoin: ${payment.currency}`);
    }
    
    // 2. Compliance check
    await this.complianceChecker.verify({
      sender: payment.from,
      recipient: payment.to,
      amount: payment.amount,
      currency: payment.currency
    });
    
    // 3. Check reserves (for algorithmic stablecoins)
    if (stablecoin.type === 'algorithmic') {
      const reserves = await stablecoin.getReserves();
      if (reserves.ratio < 1.0) {
        throw new Error('Stablecoin under-collateralized');
      }
    }
    
    // 4. Execute transfer
    const receipt = await stablecoin.transfer({
      from: payment.from,
      to: payment.to,
      amount: payment.amount,
      memo: payment.memo
    });
    
    // 5. Record for compliance
    await this.recordTransaction(payment, receipt);
    
    return receipt;
  }
  
  async convertToFiat(
    stablecoin: string,
    amount: bigint,
    fiatCurrency: string
  ): Promise<FiatConversion> {
    // Get off-ramp provider
    const provider = await this.selectOffRampProvider(stablecoin, fiatCurrency);
    
    // Initiate conversion
    const conversion = await provider.initiate({
      stablecoin,
      amount,
      fiatCurrency,
      bankAccount: this.getBankAccount(fiatCurrency)
    });
    
    // Monitor conversion status
    return await this.monitorConversion(conversion.id);
  }
}
```

### CBDC Integration

```typescript
// Central Bank Digital Currency integration
export class CBDCIntegrationService {
  private cbdcNodes: Map<string, CBDCNode>;
  private identityVerifier: IdentityVerifier;
  private complianceEngine: ComplianceEngine;
  
  async processCBDCPayment(
    payment: CBDCPayment
  ): Promise<CBDCReceipt> {
    // 1. Verify digital identity
    const identity = await this.identityVerifier.verify(payment.payerId);
    if (!identity.verified) {
      throw new Error('Identity verification required');
    }
    
    // 2. Check account limits
    const limits = await this.checkAccountLimits(
      payment.cbdc,
      payment.payerId,
      payment.amount
    );
    
    if (payment.amount > limits.transactionLimit) {
      throw new Error('Transaction exceeds limit');
    }
    
    // 3. Execute on CBDC network
    const node = this.cbdcNodes.get(payment.cbdc);
    const receipt = await node.executeTransaction({
      from: payment.payerId,
      to: payment.payeeId,
      amount: payment.amount,
      purpose: payment.purpose,
      privacyLevel: payment.privacyLevel || 'standard'
    });
    
    // 4. Report for compliance
    await this.complianceEngine.report({
      transaction: receipt.transactionId,
      amount: payment.amount,
      parties: [payment.payerId, payment.payeeId],
      timestamp: receipt.timestamp
    });
    
    return receipt;
  }
  
  async bridgeCBDCToCommercial(
    cbdcAmount: bigint,
    commercialBankAccount: string
  ): Promise<BridgeReceipt> {
    // Convert CBDC to commercial bank money
    const bridge = await this.initiateBridge({
      source: 'cbdc',
      target: 'commercial',
      amount: cbdcAmount,
      targetAccount: commercialBankAccount
    });
    
    // Wait for central bank approval
    await this.waitForApproval(bridge.id);
    
    // Execute settlement
    return await this.settleBridge(bridge.id);
  }
}
```

### NFT Payment Integration

```typescript
// NFT marketplace payment integration
export class NFTPaymentService {
  private marketplaces: Map<string, NFTMarketplace>;
  private royaltyEngine: RoyaltyEngine;
  
  async processNFTPurchase(
    purchase: NFTPurchase
  ): Promise<NFTPurchaseReceipt> {
    const marketplace = this.marketplaces.get(purchase.marketplace);
    
    // 1. Verify NFT ownership
    const owner = await marketplace.getOwner(purchase.tokenId);
    if (owner !== purchase.seller) {
      throw new Error('Seller does not own NFT');
    }
    
    // 2. Calculate total cost including royalties
    const royalties = await this.royaltyEngine.calculate(
      purchase.collection,
      purchase.price
    );
    
    const totalCost = purchase.price + royalties.amount;
    
    // 3. Execute atomic purchase
    const receipt = await marketplace.purchaseNFT({
      tokenId: purchase.tokenId,
      buyer: purchase.buyer,
      seller: purchase.seller,
      price: purchase.price,
      paymentToken: purchase.paymentToken,
      royaltyRecipient: royalties.recipient,
      royaltyAmount: royalties.amount
    });
    
    return {
      ...receipt,
      royaltiesPaid: royalties.amount,
      totalCost
    };
  }
}
```

## Regulatory Compliance Integration

### PCI DSS Compliance

```python
# PCI-compliant tokenization service
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import secrets
import struct

class PCITokenizationService:
    def __init__(self, hsm_client, vault_client):
        self.hsm = hsm_client
        self.vault = vault_client
        self.backend = default_backend()
        
    async def tokenize_card_data(self, card_data: CardData) -> Token:
        """Tokenize card data in PCI-compliant manner"""
        
        # Validate card data
        if not self._validate_card_data(card_data):
            raise ValidationError("Invalid card data")
        
        # Generate format-preserving token
        token = await self._generate_fps_token(card_data.number)
        
        # Encrypt sensitive data using HSM
        encrypted_data = await self.hsm.encrypt(
            key_id="card-encryption-key",
            plaintext=card_data.to_json(),
            algorithm="AES-256-GCM"
        )
        
        # Store in secure vault (not application database)
        await self.vault.store(
            path=f"tokens/{token}",
            data={
                "encrypted_data": encrypted_data,
                "created_at": datetime.utcnow().isoformat(),
                "last_four": card_data.number[-4:],
                "card_brand": self._detect_card_brand(card_data.number),
                "exp_month": card_data.exp_month,
                "exp_year": card_data.exp_year
            },
            ttl=86400 * 365 * 2  # 2 years
        )
        
        # Audit log
        await self._audit_tokenization(token, card_data)
        
        return Token(
            value=token,
            last_four=card_data.number[-4:],
            brand=self._detect_card_brand(card_data.number),
            expires_at=datetime.utcnow() + timedelta(days=730)
        )
    
    async def _generate_fps_token(self, card_number: str) -> str:
        """Generate format-preserving token"""
        # Use FF3-1 format-preserving encryption
        token_bytes = await self.hsm.format_preserving_encrypt(
            key_id="tokenization-key",
            plaintext=card_number,
            tweak=secrets.token_bytes(8),
            radix=10,
            min_length=len(card_number),
            max_length=len(card_number)
        )
        
        return token_bytes.decode('ascii')
    
    def _validate_card_data(self, card_data: CardData) -> bool:
        """Validate card data without logging"""
        # Luhn check
        if not self._luhn_check(card_data.number):
            return False
            
        # Expiry validation
        exp_date = datetime(card_data.exp_year, card_data.exp_month, 1)
        if exp_date < datetime.now():
            return False
            
        # CVV format validation (but never store)
        if not re.match(r'^\d{3,4}$', card_data.cvv):
            return False
            
        return True
    
    async def _audit_tokenization(self, token: str, card_data: CardData):
        """Create audit trail without sensitive data"""
        audit_entry = {
            "event": "card_tokenized",
            "token": token,
            "timestamp": datetime.utcnow().isoformat(),
            "card_brand": self._detect_card_brand(card_data.number),
            "last_four": card_data.number[-4:],
            "user_id": card_data.user_id,
            "ip_address": card_data.ip_address,
            "user_agent": card_data.user_agent
        }
        
        await self.audit_logger.log(audit_entry)
```

### PSD2/SCA Compliance

```typescript
// Strong Customer Authentication implementation
export class SCAComplianceService {
  private readonly threeDS: ThreeDSecureClient;
  private readonly bankingAPI: BankingAPIClient;
  
  async authenticatePayment(
    payment: PaymentRequest,
    customerData: CustomerData
  ): Promise<AuthenticationResult> {
    // Check if SCA is required
    const scaRequired = this.isScaRequired(payment, customerData);
    
    if (!scaRequired) {
      return {
        authenticated: true,
        method: 'exemption',
        exemptionType: this.getExemptionType(payment)
      };
    }
    
    // Perform 3D Secure authentication
    const threeDSResult = await this.perform3DS(payment, customerData);
    
    if (threeDSResult.version === '2.0') {
      return this.handle3DS2(threeDSResult);
    } else {
      return this.handle3DS1(threeDSResult);
    }
  }
  
  private async perform3DS(
    payment: PaymentRequest,
    customer: CustomerData
  ): Promise<ThreeDSResult> {
    // Initialize 3DS
    const authRequest = {
      amount: payment.amount,
      currency: payment.currency,
      cardNumber: payment.cardNumber,
      merchantId: payment.merchantId,
      customerData: {
        email: customer.email,
        phone: customer.phone,
        billingAddress: customer.billingAddress,
        shippingAddress: customer.shippingAddress,
        ipAddress: customer.ipAddress,
        userAgent: customer.userAgent
      },
      transactionType: payment.transactionType,
      challengeIndicator: 'dynamic', // Request challenge when needed
      browserData: {
        acceptHeader: customer.browserAcceptHeader,
        userAgent: customer.userAgent,
        language: customer.browserLanguage,
        colorDepth: customer.browserColorDepth,
        screenHeight: customer.browserScreenHeight,
        screenWidth: customer.browserScreenWidth,
        timezone: customer.browserTimezone,
        javaEnabled: customer.browserJavaEnabled
      }
    };
    
    return await this.threeDS.authenticate(authRequest);
  }
  
  private isScaRequired(payment: PaymentRequest, customer: CustomerData): boolean {
    // Low-value exemption (under €30)
    if (payment.amount < 3000 && payment.currency === 'EUR') {
      return false;
    }
    
    // Trusted beneficiary
    if (customer.trustedBeneficiaries?.includes(payment.merchantId)) {
      return false;
    }
    
    // Transaction risk analysis exemption
    const riskScore = this.calculateRiskScore(payment, customer);
    if (riskScore < 0.1 && payment.amount < 50000) {
      return false;
    }
    
    // Corporate payment exemption
    if (payment.paymentType === 'B2B' && customer.corporateAccount) {
      return false;
    }
    
    return true;
  }
  
  private async handle3DS2(result: ThreeDSResult): Promise<AuthenticationResult> {
    if (result.status === 'authenticated') {
      return {
        authenticated: true,
        method: '3ds2',
        eci: result.eci,
        cavv: result.cavv,
        threeDSVersion: '2.0',
        transactionId: result.transactionId
      };
    }
    
    if (result.status === 'challenge_required') {
      // Create challenge
      const challengeUrl = await this.createChallengeUrl(result);
      
      return {
        authenticated: false,
        challengeRequired: true,
        challengeUrl,
        method: '3ds2',
        threeDSVersion: '2.0',
        transactionId: result.transactionId
      };
    }
    
    return {
      authenticated: false,
      method: '3ds2',
      reason: result.reason || 'Authentication failed'
    };
  }
}
```

### AML/KYC Integration

```go
// Anti-Money Laundering and Know Your Customer integration
package compliance

import (
    "context"
    "encoding/json"
    "fmt"
)

type AMLKYCService struct {
    providers map[string]ComplianceProvider
    rules     ComplianceRules
    audit     AuditLogger
}

func (s *AMLKYCService) ScreenTransaction(
    ctx context.Context,
    transaction Transaction,
) (*ComplianceResult, error) {
    result := &ComplianceResult{
        TransactionID: transaction.ID,
        Timestamp:     time.Now(),
        Checks:        make([]ComplianceCheck, 0),
    }
    
    // Sanctions screening
    sanctionsCheck := s.checkSanctions(ctx, transaction)
    result.Checks = append(result.Checks, sanctionsCheck)
    
    if sanctionsCheck.Failed {
        result.Status = "rejected"
        result.Reason = "sanctions_match"
        return result, nil
    }
    
    // PEP screening
    pepCheck := s.checkPEP(ctx, transaction)
    result.Checks = append(result.Checks, pepCheck)
    
    // Transaction monitoring
    monitoringCheck := s.monitorTransaction(ctx, transaction)
    result.Checks = append(result.Checks, monitoringCheck)
    
    // Calculate overall risk score
    result.RiskScore = s.calculateRiskScore(result.Checks)
    
    // Determine action
    if result.RiskScore > 0.8 {
        result.Status = "rejected"
        result.Reason = "high_risk"
    } else if result.RiskScore > 0.5 {
        result.Status = "review"
        result.Reason = "medium_risk"
    } else {
        result.Status = "approved"
    }
    
    // Audit trail
    s.audit.LogCompliance(result)
    
    return result, nil
}

func (s *AMLKYCService) VerifyCustomer(
    ctx context.Context,
    customer CustomerData,
) (*KYCResult, error) {
    // Document verification
    docResult, err := s.verifyDocuments(ctx, customer.Documents)
    if err != nil {
        return nil, err
    }
    
    // Biometric verification if available
    var biometricResult *BiometricResult
    if customer.BiometricData != nil {
        biometricResult, err = s.verifyBiometrics(ctx, customer.BiometricData)
        if err != nil {
            return nil, err
        }
    }
    
    // Address verification
    addressResult, err := s.verifyAddress(ctx, customer.Address)
    if err != nil {
        return nil, err
    }
    
    // Identity verification with external provider
    identityResult, err := s.providers["identity"].VerifyIdentity(ctx, customer)
    if err != nil {
        return nil, err
    }
    
    return &KYCResult{
        CustomerID:       customer.ID,
        Status:          s.determineKYCStatus(docResult, biometricResult, addressResult, identityResult),
        DocumentStatus:  docResult.Status,
        BiometricStatus: biometricResult?.Status,
        AddressStatus:   addressResult.Status,
        IdentityScore:   identityResult.Score,
        Timestamp:       time.Now(),
    }, nil
}

// Transaction pattern analysis
func (s *AMLKYCService) monitorTransaction(
    ctx context.Context,
    transaction Transaction,
) ComplianceCheck {
    patterns := []TransactionPattern{
        &RapidMovementPattern{threshold: 10000, timeWindow: time.Hour},
        &StructuringPattern{threshold: 9999, count: 3},
        &UnusualPatternDetector{ml: s.mlModel},
        &CrossBorderPattern{highRiskCountries: s.rules.HighRiskCountries},
    }
    
    var alerts []string
    riskScore := 0.0
    
    for _, pattern := range patterns {
        if match, score := pattern.Detect(transaction); match {
            alerts = append(alerts, pattern.Name())
            riskScore += score
        }
    }
    
    return ComplianceCheck{
        Type:      "transaction_monitoring",
        Status:    len(alerts) == 0,
        RiskScore: riskScore,
        Alerts:    alerts,
    }
}
```

## Integration Patterns

### Circuit Breaker Pattern

```java
@Component
public class PaymentCircuitBreaker {
    private final Map<String, CircuitBreaker> breakers = new ConcurrentHashMap<>();
    private final CircuitBreakerRegistry registry;
    
    public PaymentCircuitBreaker(CircuitBreakerRegistry registry) {
        this.registry = registry;
    }
    
    public <T> T executeWithCircuitBreaker(
        String serviceName,
        Supplier<T> operation,
        Function<Throwable, T> fallback
    ) {
        CircuitBreaker breaker = breakers.computeIfAbsent(
            serviceName,
            name -> createCircuitBreaker(name)
        );
        
        return breaker.executeSupplier(operation, fallback);
    }
    
    private CircuitBreaker createCircuitBreaker(String name) {
        CircuitBreakerConfig config = CircuitBreakerConfig.custom()
            .failureRateThreshold(50) // 50% failure rate
            .waitDurationInOpenState(Duration.ofSeconds(30))
            .slidingWindowSize(100) // Last 100 calls
            .permittedNumberOfCallsInHalfOpenState(10)
            .minimumNumberOfCalls(20)
            .recordExceptions(IOException.class, TimeoutException.class)
            .ignoreExceptions(BusinessException.class)
            .build();
            
        CircuitBreaker breaker = registry.circuitBreaker(name, config);
        
        // Add event listeners
        breaker.getEventPublisher()
            .onStateTransition(event -> 
                log.warn("Circuit breaker {} transitioned from {} to {}",
                    name, event.getStateTransition().getFromState(),
                    event.getStateTransition().getToState())
            )
            .onFailureRateExceeded(event ->
                log.error("Circuit breaker {} failure rate exceeded: {}%",
                    name, event.getFailureRate())
            );
            
        return breaker;
    }
}
```

### Saga Pattern for Distributed Transactions

```python
# Distributed transaction orchestration
from typing import List, Dict, Any, Callable
import asyncio
from dataclasses import dataclass
from enum import Enum

class SagaState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPENSATING = "compensating"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class SagaStep:
    name: str
    action: Callable
    compensation: Callable
    retry_policy: RetryPolicy
    
class PaymentSaga:
    def __init__(self, saga_id: str):
        self.saga_id = saga_id
        self.state = SagaState.PENDING
        self.completed_steps: List[str] = []
        self.current_step: Optional[str] = None
        self.context: Dict[str, Any] = {}
        
    async def execute(self, steps: List[SagaStep]) -> Dict[str, Any]:
        """Execute saga with automatic compensation on failure"""
        self.state = SagaState.RUNNING
        
        try:
            for step in steps:
                self.current_step = step.name
                
                # Execute step with retry
                result = await self._execute_with_retry(
                    step.action,
                    step.retry_policy,
                    self.context
                )
                
                # Store result in context
                self.context[f"{step.name}_result"] = result
                self.completed_steps.append(step.name)
                
                # Persist saga state
                await self._save_state()
                
            self.state = SagaState.COMPLETED
            return self.context
            
        except Exception as e:
            # Compensate in reverse order
            self.state = SagaState.COMPENSATING
            await self._compensate(steps)
            self.state = SagaState.FAILED
            raise SagaFailedException(f"Saga {self.saga_id} failed: {str(e)}")
    
    async def _compensate(self, steps: List[SagaStep]):
        """Run compensation in reverse order"""
        completed_step_names = set(self.completed_steps)
        
        for step in reversed(steps):
            if step.name in completed_step_names:
                try:
                    await step.compensation(self.context)
                    log.info(f"Compensated step {step.name}")
                except Exception as e:
                    log.error(f"Failed to compensate {step.name}: {e}")
                    # Continue with other compensations
    
    async def _execute_with_retry(
        self,
        action: Callable,
        retry_policy: RetryPolicy,
        context: Dict[str, Any]
    ) -> Any:
        """Execute action with retry policy"""
        last_error = None
        
        for attempt in range(retry_policy.max_attempts):
            try:
                return await action(context)
            except Exception as e:
                last_error = e
                if attempt < retry_policy.max_attempts - 1:
                    await asyncio.sleep(
                        retry_policy.get_delay(attempt)
                    )
                    
        raise last_error

# Example payment saga
async def create_payment_saga(payment_request: PaymentRequest) -> Dict[str, Any]:
    saga = PaymentSaga(f"payment_{payment_request.id}")
    
    steps = [
        SagaStep(
            name="validate_payment",
            action=lambda ctx: validate_payment_data(payment_request),
            compensation=lambda ctx: log.info("No compensation needed"),
            retry_policy=RetryPolicy(max_attempts=3, initial_delay=1)
        ),
        SagaStep(
            name="reserve_inventory",
            action=lambda ctx: inventory_service.reserve(payment_request.items),
            compensation=lambda ctx: inventory_service.release(ctx["reserve_inventory_result"]),
            retry_policy=RetryPolicy(max_attempts=5, initial_delay=2)
        ),
        SagaStep(
            name="process_payment",
            action=lambda ctx: payment_processor.charge(payment_request),
            compensation=lambda ctx: payment_processor.refund(ctx["process_payment_result"]),
            retry_policy=RetryPolicy(max_attempts=3, initial_delay=5)
        ),
        SagaStep(
            name="update_order",
            action=lambda ctx: order_service.mark_paid(payment_request.order_id),
            compensation=lambda ctx: order_service.mark_unpaid(payment_request.order_id),
            retry_policy=RetryPolicy(max_attempts=3, initial_delay=1)
        ),
        SagaStep(
            name="send_notification",
            action=lambda ctx: notification_service.send_payment_confirmation(payment_request),
            compensation=lambda ctx: log.info("No compensation for notification"),
            retry_policy=RetryPolicy(max_attempts=3, initial_delay=1)
        )
    ]
    
    return await saga.execute(steps)
```

## Security Considerations

### API Security

```yaml
# OAuth 2.0 configuration for payment APIs
security:
  oauth2:
    authorization_endpoint: https://auth.payment.com/oauth2/authorize
    token_endpoint: https://auth.payment.com/oauth2/token
    scopes:
      - payment:read
      - payment:write
      - refund:write
      - customer:read
    grant_types:
      - authorization_code
      - client_credentials
    
  api_keys:
    rotation_period: 90d
    key_format: "pk_[env]_[random]"
    secret_format: "sk_[env]_[random]"
    
  rate_limiting:
    default: 1000/hour
    by_endpoint:
      /payments: 100/minute
      /refunds: 50/minute
      /webhooks: 1000/minute
      
  ip_whitelist:
    enabled: true
    ranges:
      - 10.0.0.0/8
      - 172.16.0.0/12
      
  encryption:
    tls_version: "1.3"
    cipher_suites:
      - TLS_AES_256_GCM_SHA384
      - TLS_CHACHA20_POLY1305_SHA256
```

### Webhook Security

```go
// Secure webhook handling
package webhook

import (
    "crypto/hmac"
    "crypto/sha256"
    "encoding/hex"
    "time"
)

type WebhookValidator struct {
    secrets    map[string]string
    timeWindow time.Duration
}

func (v *WebhookValidator) ValidateWebhook(
    provider string,
    headers map[string]string,
    body []byte,
) error {
    validator, exists := webhookValidators[provider]
    if !exists {
        return fmt.Errorf("unknown provider: %s", provider)
    }
    
    return validator(headers, body, v.secrets[provider])
}

var webhookValidators = map[string]WebhookValidatorFunc{
    "stripe": validateStripeWebhook,
    "paypal": validatePayPalWebhook,
    "square": validateSquareWebhook,
}

func validateStripeWebhook(headers map[string]string, body []byte, secret string) error {
    signature := headers["Stripe-Signature"]
    
    // Parse signature header
    elements := parseSignatureHeader(signature)
    timestamp := elements["t"]
    signatures := strings.Split(elements["v1"], ",")
    
    // Verify timestamp (prevent replay attacks)
    ts, _ := strconv.ParseInt(timestamp, 10, 64)
    if time.Now().Unix()-ts > 300 { // 5 minutes
        return ErrWebhookTooOld
    }
    
    // Compute expected signature
    payload := timestamp + "." + string(body)
    expectedSig := computeHMAC(payload, secret)
    
    // Verify signature
    for _, sig := range signatures {
        if hmac.Equal([]byte(sig), []byte(expectedSig)) {
            return nil
        }
    }
    
    return ErrInvalidWebhookSignature
}

func validatePayPalWebhook(headers map[string]string, body []byte, secret string) error {
    // PayPal uses different approach - verify with PayPal API
    verifyRequest := map[string]interface{}{
        "transmission_id":   headers["Paypal-Transmission-Id"],
        "transmission_time": headers["Paypal-Transmission-Time"],
        "cert_url":         headers["Paypal-Cert-Url"],
        "auth_algo":        headers["Paypal-Auth-Algo"],
        "transmission_sig": headers["Paypal-Transmission-Sig"],
        "webhook_id":       secret,
        "webhook_event":    body,
    }
    
    resp, err := paypalClient.VerifyWebhook(verifyRequest)
    if err != nil {
        return err
    }
    
    if resp.VerificationStatus != "SUCCESS" {
        return ErrInvalidWebhookSignature
    }
    
    return nil
}
```

## Testing Strategies

### Integration Testing

```python
# Payment integration test suite
import pytest
from unittest.mock import Mock, patch
import responses

class TestPaymentIntegration:
    @pytest.fixture
    def stripe_mock(self):
        with responses.RequestsMock() as rsps:
            yield rsps
    
    @pytest.mark.asyncio
    async def test_successful_payment_flow(self, stripe_mock):
        # Mock Stripe API responses
        stripe_mock.add(
            responses.POST,
            "https://api.stripe.com/v1/payment_intents",
            json={
                "id": "pi_test123",
                "status": "requires_confirmation",
                "amount": 10000,
                "currency": "usd"
            }
        )
        
        stripe_mock.add(
            responses.POST,
            "https://api.stripe.com/v1/payment_intents/pi_test123/confirm",
            json={
                "id": "pi_test123",
                "status": "succeeded",
                "amount": 10000,
                "currency": "usd"
            }
        )
        
        # Test payment flow
        payment_service = PaymentService(StripeAdapter(test_config))
        
        result = await payment_service.process_payment(
            PaymentRequest(
                amount=10000,
                currency="usd",
                payment_method_id="pm_test",
                customer_id="cust_test"
            )
        )
        
        assert result.status == "completed"
        assert result.amount == 10000
        assert len(stripe_mock.calls) == 2
    
    @pytest.mark.asyncio
    async def test_payment_retry_on_network_error(self):
        # Test retry logic
        with patch('payment_service.StripeAdapter') as mock_adapter:
            mock_adapter.create_payment.side_effect = [
                NetworkError("Connection failed"),
                NetworkError("Connection failed"),
                PaymentResponse(id="pi_123", status="succeeded")
            ]
            
            payment_service = PaymentService(mock_adapter)
            
            result = await payment_service.process_payment_with_retry(
                payment_request,
                max_retries=3
            )
            
            assert result.status == "succeeded"
            assert mock_adapter.create_payment.call_count == 3
```

### Contract Testing

```yaml
# Pact contract for payment provider
consumer: PaymentService
provider: StripeAPI
pact_version: 2.0.0

interactions:
  - description: Create payment intent
    request:
      method: POST
      path: /v1/payment_intents
      headers:
        Authorization: Bearer sk_test_*
        Content-Type: application/x-www-form-urlencoded
      body:
        amount: 10000
        currency: usd
        payment_method: pm_test123
    response:
      status: 200
      headers:
        Content-Type: application/json
      body:
        id: 
          regex: "pi_[a-zA-Z0-9]+"
        object: payment_intent
        amount: 10000
        currency: usd
        status: requires_confirmation
        
  - description: Webhook notification
    request:
      method: POST
      path: /webhooks/payment
      headers:
        Stripe-Signature: 
          regex: "t=[0-9]+,v1=[a-f0-9]+"
      body:
        type: payment_intent.succeeded
        data:
          object:
            id: pi_test123
            amount: 10000
            status: succeeded
    response:
      status: 200
      body:
        received: true
```

## Conclusion

Successful payment system integration requires:

1. **Abstraction**: Hide provider-specific details behind common interfaces
2. **Resilience**: Implement circuit breakers, retries, and fallbacks
3. **Security**: Protect sensitive data and verify all external inputs
4. **Monitoring**: Track performance and errors across all integrations
5. **Testing**: Comprehensive test coverage including contract tests

Regular review and updates ensure integrations remain secure, performant, and compliant with evolving requirements.
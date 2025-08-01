# Payment System Implementation Guidelines

## Executive Summary

This document provides detailed implementation guidelines for payment system architectures, covering technology stack recommendations, integration strategies, performance considerations, and best practices for building scalable, secure, and maintainable payment platforms.

## Table of Contents

1. [Technology Stack Recommendations](#technology-stack-recommendations)
2. [Integration Strategies](#integration-strategies)
3. [Performance Optimization](#performance-optimization)
4. [Development Workflow](#development-workflow)
5. [Testing Strategies](#testing-strategies)
6. [Deployment Patterns](#deployment-patterns)
7. [Monitoring and Observability](#monitoring-and-observability)
8. [Security Implementation](#security-implementation)

## Technology Stack Recommendations

### Core Platform Technologies

#### Programming Languages

**Production Systems**
```yaml
Primary Languages:
  Java:
    - Use Cases: Core payment processing, high-throughput services
    - Framework: Spring Boot 3.x, Micronaut
    - Runtime: OpenJDK 17+ or GraalVM
    
  Go:
    - Use Cases: API gateways, performance-critical services
    - Framework: Gin, Echo, or stdlib
    - Benefits: Low latency, efficient concurrency
    
  Rust:
    - Use Cases: Cryptography, HSM integration, ultra-low latency
    - Framework: Actix-web, Tokio
    - Benefits: Memory safety, zero-cost abstractions

Support Languages:
  Python:
    - Use Cases: Data pipelines, ML models, scripting
    - Framework: FastAPI, Django
    - Runtime: Python 3.11+
    
  TypeScript/Node.js:
    - Use Cases: BFF services, real-time features
    - Framework: NestJS, Express
    - Runtime: Node.js 18+ LTS
```

#### Database Technologies

**Primary Data Stores**
```yaml
Transactional:
  PostgreSQL:
    - Version: 15+
    - Use Cases: Core transactions, accounts, settlements
    - Features: JSONB, partitioning, logical replication
    - Extensions: TimescaleDB for time-series
    
  MySQL/Aurora:
    - Version: 8.0+
    - Use Cases: High-read workloads, global distribution
    - Features: InnoDB, semi-sync replication

NoSQL:
  MongoDB:
    - Version: 6.0+
    - Use Cases: Merchant profiles, product catalogs
    - Features: Transactions, change streams
    
  DynamoDB:
    - Use Cases: Session management, user preferences
    - Features: Global tables, auto-scaling

Cache & Queue:
  Redis:
    - Version: 7.0+
    - Use Cases: Caching, rate limiting, sessions
    - Features: Redis Streams, Cluster mode
    
  Apache Kafka:
    - Version: 3.5+
    - Use Cases: Event streaming, audit logs
    - Features: Exactly-once semantics
```

### Infrastructure Stack

#### Container Orchestration

**Kubernetes Setup**
```yaml
# Production cluster configuration
apiVersion: v1
kind: Namespace
metadata:
  name: payment-system
  labels:
    istio-injection: enabled
    
---
# Resource quotas
apiVersion: v1
kind: ResourceQuota
metadata:
  name: payment-quota
  namespace: payment-system
spec:
  hard:
    requests.cpu: "1000"
    requests.memory: 2000Gi
    persistentvolumeclaims: "100"
    services.loadbalancers: "10"
```

#### Service Mesh Configuration

**Istio Production Setup**
```bash
# Install Istio with production profile
istioctl install --set profile=production \
  --set values.pilot.resources.requests.cpu=1000m \
  --set values.pilot.resources.requests.memory=4Gi \
  --set values.global.proxy.resources.requests.cpu=100m \
  --set values.global.proxy.resources.requests.memory=128Mi

# Enable mTLS mesh-wide
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
EOF
```

## Integration Strategies

### Payment Gateway Integration

#### Adapter Pattern Implementation

```java
// Payment gateway adapter interface
public interface PaymentGatewayAdapter {
    AuthorizationResponse authorize(PaymentRequest request);
    CaptureResponse capture(String authorizationId, Money amount);
    RefundResponse refund(String transactionId, Money amount);
    VoidResponse voidTransaction(String authorizationId);
}

// Stripe implementation
@Component
public class StripePaymentAdapter implements PaymentGatewayAdapter {
    private final StripeClient stripeClient;
    private final MetricRegistry metrics;
    private final CircuitBreaker circuitBreaker;
    
    @Override
    public AuthorizationResponse authorize(PaymentRequest request) {
        return circuitBreaker.executeSupplier(() -> {
            Timer.Context timer = metrics.timer("stripe.authorize").time();
            try {
                PaymentIntent intent = stripeClient.paymentIntents().create(
                    PaymentIntentCreateParams.builder()
                        .setAmount(request.getAmount().getMinorUnits())
                        .setCurrency(request.getCurrency().getCurrencyCode())
                        .setPaymentMethod(request.getPaymentMethodId())
                        .setCaptureMethod(CaptureMethod.MANUAL)
                        .setMetadata(request.getMetadata())
                        .build()
                );
                
                return AuthorizationResponse.builder()
                    .authorizationId(intent.getId())
                    .status(mapStatus(intent.getStatus()))
                    .build();
            } finally {
                timer.stop();
            }
        });
    }
}

// Gateway router for multi-provider support
@Service
public class PaymentGatewayRouter {
    private final Map<String, PaymentGatewayAdapter> gateways;
    private final GatewaySelectionStrategy selectionStrategy;
    
    public AuthorizationResponse routeAuthorization(PaymentRequest request) {
        String gatewayId = selectionStrategy.selectGateway(request);
        PaymentGatewayAdapter gateway = gateways.get(gatewayId);
        
        if (gateway == null) {
            throw new GatewayNotFoundException(gatewayId);
        }
        
        return gateway.authorize(request);
    }
}
```

### Bank Integration

#### ACH Integration Pattern

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List
import asyncio

@dataclass
class ACHTransaction:
    routing_number: str
    account_number: str
    account_type: str  # CHECKING or SAVINGS
    amount: int  # cents
    direction: str  # DEBIT or CREDIT
    merchant_reference: str
    customer_name: str
    
class ACHProcessor(ABC):
    @abstractmethod
    async def create_batch(self, transactions: List[ACHTransaction]) -> str:
        pass
    
    @abstractmethod
    async def submit_batch(self, batch_id: str) -> bool:
        pass
    
    @abstractmethod
    async def get_batch_status(self, batch_id: str) -> dict:
        pass

class ModernTreasuryACH(ACHProcessor):
    def __init__(self, api_key: str, organization_id: str):
        self.client = ModernTreasuryClient(api_key, organization_id)
        
    async def create_batch(self, transactions: List[ACHTransaction]) -> str:
        # Create NACHA file format
        nacha_file = self._build_nacha_file(transactions)
        
        # Upload to Modern Treasury
        batch = await self.client.payment_orders.create_bulk(
            payment_orders=[
                {
                    "type": "ach",
                    "amount": txn.amount,
                    "direction": txn.direction.lower(),
                    "originating_account_id": self.originating_account_id,
                    "receiving_account": {
                        "routing_number": txn.routing_number,
                        "account_number": txn.account_number,
                        "account_type": txn.account_type.lower(),
                        "party_name": txn.customer_name
                    },
                    "accounting_category_id": self.accounting_category_id,
                    "metadata": {
                        "merchant_reference": txn.merchant_reference
                    }
                }
                for txn in transactions
            ]
        )
        
        return batch.id
    
    def _build_nacha_file(self, transactions: List[ACHTransaction]) -> str:
        # Implementation of NACHA file format
        pass
```

### Third-Party Service Integration

#### Webhook Processing

```go
package webhook

import (
    "crypto/hmac"
    "crypto/sha256"
    "encoding/hex"
    "time"
)

type WebhookProcessor struct {
    secret    string
    processor EventProcessor
    store     EventStore
}

func (w *WebhookProcessor) ProcessWebhook(
    headers map[string]string,
    body []byte,
) error {
    // Verify signature
    if !w.verifySignature(headers, body) {
        return ErrInvalidSignature
    }
    
    // Parse event
    event, err := w.parseEvent(body)
    if err != nil {
        return err
    }
    
    // Idempotency check
    if exists, err := w.store.EventExists(event.ID); err != nil {
        return err
    } else if exists {
        return nil // Already processed
    }
    
    // Process event
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()
    
    if err := w.processor.Process(ctx, event); err != nil {
        return err
    }
    
    // Store event
    return w.store.StoreEvent(event)
}

func (w *WebhookProcessor) verifySignature(
    headers map[string]string,
    body []byte,
) bool {
    signature := headers["X-Webhook-Signature"]
    timestamp := headers["X-Webhook-Timestamp"]
    
    // Prevent replay attacks
    ts, _ := strconv.ParseInt(timestamp, 10, 64)
    if time.Now().Unix()-ts > 300 { // 5 minutes
        return false
    }
    
    // Verify HMAC
    message := timestamp + "." + string(body)
    mac := hmac.New(sha256.New, []byte(w.secret))
    mac.Write([]byte(message))
    expected := hex.EncodeToString(mac.Sum(nil))
    
    return hmac.Equal([]byte(signature), []byte(expected))
}
```

## Performance Optimization

### Database Optimization

#### Query Optimization Strategies

```sql
-- Optimized payment query with proper indexing
CREATE INDEX CONCURRENTLY idx_payments_merchant_created 
ON payments(merchant_id, created_at DESC) 
WHERE status NOT IN ('CANCELLED', 'FAILED');

-- Partitioned table for high-volume transactions
CREATE TABLE payments (
    id UUID DEFAULT gen_random_uuid(),
    merchant_id UUID NOT NULL,
    amount BIGINT NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE payments_2024_01 PARTITION OF payments
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Materialized view for analytics
CREATE MATERIALIZED VIEW payment_daily_summary AS
SELECT 
    merchant_id,
    DATE(created_at) as payment_date,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(amount) as average_amount,
    COUNT(*) FILTER (WHERE status = 'COMPLETED') as successful_count
FROM payments
WHERE created_at >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY merchant_id, DATE(created_at);

CREATE UNIQUE INDEX ON payment_daily_summary (merchant_id, payment_date);
```

#### Connection Pool Optimization

```java
@Configuration
public class DatabaseConfiguration {
    
    @Bean
    public HikariDataSource dataSource() {
        HikariConfig config = new HikariConfig();
        
        // Connection settings
        config.setJdbcUrl("jdbc:postgresql://localhost:5432/payments");
        config.setUsername("payment_user");
        config.setPassword(getSecurePassword());
        
        // Pool configuration
        config.setMaximumPoolSize(50);
        config.setMinimumIdle(10);
        config.setIdleTimeout(300000); // 5 minutes
        config.setConnectionTimeout(30000); // 30 seconds
        config.setMaxLifetime(1800000); // 30 minutes
        
        // Performance optimizations
        config.addDataSourceProperty("cachePrepStmts", true);
        config.addDataSourceProperty("prepStmtCacheSize", 250);
        config.addDataSourceProperty("prepStmtCacheSqlLimit", 2048);
        config.addDataSourceProperty("useServerPrepStmts", true);
        config.addDataSourceProperty("rewriteBatchedStatements", true);
        
        // Monitoring
        config.setMetricRegistry(metricRegistry);
        config.setHealthCheckRegistry(healthCheckRegistry);
        
        return new HikariDataSource(config);
    }
}
```

### Caching Strategy

#### Multi-Level Cache Implementation

```python
from typing import Optional, Any, Callable
import asyncio
from datetime import timedelta

class MultiLevelCache:
    def __init__(self, local_cache: LocalCache, redis_cache: RedisCache):
        self.local = local_cache
        self.redis = redis_cache
        
    async def get(
        self,
        key: str,
        fetch_fn: Optional[Callable] = None,
        ttl: timedelta = timedelta(minutes=5)
    ) -> Optional[Any]:
        # L1: Local cache (microseconds)
        value = self.local.get(key)
        if value is not None:
            return value
            
        # L2: Redis cache (milliseconds)
        value = await self.redis.get(key)
        if value is not None:
            self.local.set(key, value, ttl=ttl.total_seconds() / 10)
            return value
            
        # L3: Database/Service (milliseconds to seconds)
        if fetch_fn:
            value = await fetch_fn()
            if value is not None:
                await self.set(key, value, ttl)
            return value
            
        return None
    
    async def set(self, key: str, value: Any, ttl: timedelta):
        # Write to both cache levels
        self.local.set(key, value, ttl=ttl.total_seconds() / 10)
        await self.redis.set(key, value, ttl=ttl.total_seconds())

# Cache warming strategy
class CacheWarmer:
    def __init__(self, cache: MultiLevelCache, db: Database):
        self.cache = cache
        self.db = db
        
    async def warm_merchant_cache(self):
        """Pre-load frequently accessed merchant data"""
        merchants = await self.db.get_active_merchants(limit=1000)
        
        tasks = [
            self.cache.set(
                f"merchant:{merchant.id}",
                merchant,
                ttl=timedelta(hours=1)
            )
            for merchant in merchants
        ]
        
        await asyncio.gather(*tasks)
```

### Async Processing

#### Event-Driven Architecture

```go
package events

import (
    "context"
    "github.com/segmentio/kafka-go"
    "go.uber.org/zap"
)

type PaymentEventProcessor struct {
    reader   *kafka.Reader
    handlers map[string]EventHandler
    logger   *zap.Logger
}

func (p *PaymentEventProcessor) Start(ctx context.Context) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        default:
            msg, err := p.reader.FetchMessage(ctx)
            if err != nil {
                p.logger.Error("Failed to fetch message", zap.Error(err))
                continue
            }
            
            // Process in goroutine for parallelism
            go p.processMessage(ctx, msg)
        }
    }
}

func (p *PaymentEventProcessor) processMessage(ctx context.Context, msg kafka.Message) {
    // Parse event type
    eventType := string(msg.Headers[0].Value)
    
    handler, exists := p.handlers[eventType]
    if !exists {
        p.logger.Warn("No handler for event type", zap.String("type", eventType))
        p.reader.CommitMessages(ctx, msg)
        return
    }
    
    // Create span for tracing
    span, ctx := tracer.Start(ctx, "process_payment_event")
    defer span.End()
    
    span.SetAttributes(
        attribute.String("event.type", eventType),
        attribute.String("event.id", string(msg.Key)),
    )
    
    // Process with timeout
    processCtx, cancel := context.WithTimeout(ctx, 30*time.Second)
    defer cancel()
    
    if err := handler.Handle(processCtx, msg.Value); err != nil {
        span.RecordError(err)
        p.logger.Error("Failed to process event",
            zap.String("type", eventType),
            zap.Error(err),
        )
        // Don't commit - let it retry
        return
    }
    
    // Commit offset
    if err := p.reader.CommitMessages(ctx, msg); err != nil {
        p.logger.Error("Failed to commit message", zap.Error(err))
    }
}
```

## Development Workflow

### Git Workflow

#### Branch Strategy
```bash
# Main branches
main          # Production-ready code
develop       # Integration branch
release/*     # Release candidates
hotfix/*      # Emergency fixes

# Feature branches
feature/JIRA-123-payment-refactor
bugfix/JIRA-456-auth-timeout
chore/update-dependencies

# Branch protection rules
- main: Require PR reviews (2+)
- main: Require status checks
- main: Dismiss stale reviews
- develop: Require PR reviews (1+)
```

### CI/CD Pipeline

#### GitHub Actions Workflow

```yaml
name: Payment Service CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  DOCKER_REGISTRY: ghcr.io
  SERVICE_NAME: payment-service

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
          
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'
        
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.m2
        key: ${{ runner.os }}-m2-${{ hashFiles('**/pom.xml') }}
        
    - name: Run tests
      run: |
        ./mvnw test -Dspring.profiles.active=test
        ./mvnw verify -Pintegration-tests
        
    - name: Code coverage
      run: |
        ./mvnw jacoco:report
        bash <(curl -s https://codecov.io/bash)
        
  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Trivy security scan
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
        
    - name: Upload Trivy results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
        
  build:
    needs: [test, security-scan]
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
      
    - name: Log in to GitHub Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.DOCKER_REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
        
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          ${{ env.DOCKER_REGISTRY }}/${{ github.repository }}/${{ env.SERVICE_NAME }}:${{ github.sha }}
          ${{ env.DOCKER_REGISTRY }}/${{ github.repository }}/${{ env.SERVICE_NAME }}:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max
        
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to Kubernetes
      uses: azure/k8s-deploy@v4
      with:
        manifests: |
          k8s/deployment.yaml
          k8s/service.yaml
        images: |
          ${{ env.DOCKER_REGISTRY }}/${{ github.repository }}/${{ env.SERVICE_NAME }}:${{ github.sha }}
```

## Testing Strategies

### Test Pyramid Implementation

#### Unit Testing
```java
@ExtendWith(MockitoExtension.class)
class PaymentServiceTest {
    
    @Mock
    private PaymentRepository repository;
    
    @Mock
    private PaymentGateway gateway;
    
    @Mock
    private EventPublisher eventPublisher;
    
    @InjectMocks
    private PaymentService paymentService;
    
    @Test
    void shouldAuthorizePayment() {
        // Given
        PaymentRequest request = PaymentRequest.builder()
            .amount(Money.of(100, "USD"))
            .paymentMethodId("pm_123")
            .merchantId("merchant_123")
            .build();
            
        AuthorizationResponse authResponse = AuthorizationResponse.builder()
            .authorizationId("auth_123")
            .status(AuthorizationStatus.APPROVED)
            .build();
            
        when(gateway.authorize(any())).thenReturn(authResponse);
        
        // When
        Payment payment = paymentService.authorizePayment(request);
        
        // Then
        assertThat(payment.getStatus()).isEqualTo(PaymentStatus.AUTHORIZED);
        assertThat(payment.getAuthorizationId()).isEqualTo("auth_123");
        
        verify(repository).save(any(Payment.class));
        verify(eventPublisher).publish(any(PaymentAuthorizedEvent.class));
    }
    
    @Test
    void shouldHandleGatewayTimeout() {
        // Given
        PaymentRequest request = createValidRequest();
        when(gateway.authorize(any()))
            .thenThrow(new GatewayTimeoutException("Timeout"));
        
        // When/Then
        assertThatThrownBy(() -> paymentService.authorizePayment(request))
            .isInstanceOf(PaymentProcessingException.class)
            .hasMessageContaining("Gateway timeout");
            
        verify(eventPublisher).publish(any(PaymentFailedEvent.class));
    }
}
```

#### Integration Testing
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        yield postgres

@pytest.fixture(scope="session")
def redis_container():
    with RedisContainer("redis:7") as redis:
        yield redis

@pytest.fixture
def test_client(postgres_container, redis_container):
    # Override database URL
    os.environ["DATABASE_URL"] = postgres_container.get_connection_url()
    os.environ["REDIS_URL"] = redis_container.get_connection_url()
    
    from app.main import app
    
    with TestClient(app) as client:
        yield client

class TestPaymentAPI:
    def test_create_payment(self, test_client, mock_payment_gateway):
        # Arrange
        mock_payment_gateway.authorize.return_value = {
            "authorization_id": "auth_123",
            "status": "approved"
        }
        
        # Act
        response = test_client.post(
            "/api/v1/payments",
            json={
                "amount": 10000,  # $100.00
                "currency": "USD",
                "payment_method_id": "pm_test_123",
                "merchant_id": "merchant_123"
            },
            headers={"Authorization": "Bearer test_token"}
        )
        
        # Assert
        assert response.status_code == 201
        payment = response.json()
        assert payment["status"] == "authorized"
        assert payment["amount"] == 10000
        
    @pytest.mark.asyncio
    async def test_payment_webhook_processing(self, test_client):
        # Test webhook idempotency
        webhook_payload = {
            "event_id": "evt_123",
            "type": "payment.captured",
            "data": {
                "payment_id": "pay_123",
                "amount": 10000
            }
        }
        
        # First call
        response1 = test_client.post(
            "/webhooks/stripe",
            json=webhook_payload,
            headers={
                "Stripe-Signature": generate_webhook_signature(webhook_payload)
            }
        )
        assert response1.status_code == 200
        
        # Second call (idempotent)
        response2 = test_client.post(
            "/webhooks/stripe",
            json=webhook_payload,
            headers={
                "Stripe-Signature": generate_webhook_signature(webhook_payload)
            }
        )
        assert response2.status_code == 200
```

#### Contract Testing
```javascript
// Pact consumer test
const { Pact } = require('@pact-foundation/pact');
const { PaymentClient } = require('./payment-client');

describe('Payment Service Consumer', () => {
  const provider = new Pact({
    consumer: 'Frontend',
    provider: 'PaymentService',
    port: 8080,
    log: path.resolve(process.cwd(), 'logs', 'pact.log'),
    dir: path.resolve(process.cwd(), 'pacts'),
  });

  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());

  describe('when authorizing a payment', () => {
    beforeAll(() => {
      const interaction = {
        state: 'valid payment method exists',
        uponReceiving: 'a request to authorize payment',
        withRequest: {
          method: 'POST',
          path: '/api/v1/payments',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer token123'
          },
          body: {
            amount: 10000,
            currency: 'USD',
            payment_method_id: 'pm_123'
          }
        },
        willRespondWith: {
          status: 201,
          headers: {
            'Content-Type': 'application/json'
          },
          body: {
            id: Matchers.uuid(),
            amount: 10000,
            currency: 'USD',
            status: 'authorized',
            created_at: Matchers.iso8601DateTime()
          }
        }
      };

      return provider.addInteraction(interaction);
    });

    test('returns authorized payment', async () => {
      const client = new PaymentClient(provider.mockService.baseUrl);
      
      const payment = await client.authorizePayment({
        amount: 10000,
        currency: 'USD',
        payment_method_id: 'pm_123'
      });

      expect(payment.status).toBe('authorized');
      expect(payment.amount).toBe(10000);
    });
  });
});
```

## Deployment Patterns

### Blue-Green Deployment

```yaml
# Kubernetes blue-green deployment
apiVersion: v1
kind: Service
metadata:
  name: payment-service
spec:
  selector:
    app: payment-service
    version: green  # Switch between blue/green
  ports:
    - port: 80
      targetPort: 8080

---
# Blue deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment-service
      version: blue
  template:
    metadata:
      labels:
        app: payment-service
        version: blue
    spec:
      containers:
      - name: payment-service
        image: payment-service:v1.0.0
        ports:
        - containerPort: 8080
        env:
        - name: VERSION
          value: "blue"

---
# Green deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment-service
      version: green
  template:
    metadata:
      labels:
        app: payment-service
        version: green
    spec:
      containers:
      - name: payment-service
        image: payment-service:v2.0.0
        ports:
        - containerPort: 8080
        env:
        - name: VERSION
          value: "green"
```

### Canary Deployment

```yaml
# Istio canary deployment
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: payment-service
spec:
  hosts:
  - payment-service
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: payment-service
        subset: v2
  - route:
    - destination:
        host: payment-service
        subset: v1
      weight: 90
    - destination:
        host: payment-service
        subset: v2
      weight: 10  # 10% canary traffic

---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: payment-service
spec:
  host: payment-service
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
    trafficPolicy:
      connectionPool:
        tcp:
          maxConnections: 10  # Limit connections during canary
```

## Monitoring and Observability

### Metrics Collection

```go
// Prometheus metrics
package metrics

import (
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
)

var (
    PaymentCounter = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "payment_transactions_total",
            Help: "Total number of payment transactions",
        },
        []string{"status", "method", "gateway"},
    )
    
    PaymentDuration = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "payment_processing_duration_seconds",
            Help:    "Payment processing duration",
            Buckets: []float64{0.1, 0.25, 0.5, 1, 2.5, 5, 10},
        },
        []string{"operation", "gateway"},
    )
    
    PaymentAmount = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "payment_amount_usd",
            Help:    "Payment amounts in USD",
            Buckets: []float64{10, 50, 100, 500, 1000, 5000, 10000},
        },
        []string{"method", "merchant_category"},
    )
    
    ActivePayments = promauto.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "payment_active_processing",
            Help: "Number of payments currently being processed",
        },
        []string{"gateway"},
    )
)

// Usage in service
func (s *PaymentService) ProcessPayment(ctx context.Context, req PaymentRequest) (*Payment, error) {
    timer := prometheus.NewTimer(PaymentDuration.WithLabelValues("process", req.Gateway))
    defer timer.ObserveDuration()
    
    ActivePayments.WithLabelValues(req.Gateway).Inc()
    defer ActivePayments.WithLabelValues(req.Gateway).Dec()
    
    payment, err := s.processPaymentInternal(ctx, req)
    
    if err != nil {
        PaymentCounter.WithLabelValues("failed", req.Method, req.Gateway).Inc()
        return nil, err
    }
    
    PaymentCounter.WithLabelValues("success", req.Method, req.Gateway).Inc()
    PaymentAmount.WithLabelValues(req.Method, req.MerchantCategory).Observe(float64(req.Amount))
    
    return payment, nil
}
```

### Distributed Tracing

```java
// OpenTelemetry tracing
@Component
public class PaymentTracingService {
    private final Tracer tracer;
    
    public PaymentTracingService(OpenTelemetry openTelemetry) {
        this.tracer = openTelemetry.getTracer("payment-service", "1.0.0");
    }
    
    public Payment processPayment(PaymentRequest request) {
        Span span = tracer.spanBuilder("process_payment")
            .setSpanKind(SpanKind.SERVER)
            .setAttribute("payment.amount", request.getAmount())
            .setAttribute("payment.currency", request.getCurrency())
            .setAttribute("payment.method", request.getMethod())
            .startSpan();
            
        try (Scope scope = span.makeCurrent()) {
            // Validate payment
            validatePayment(request);
            
            // Process with gateway
            Span gatewaySpan = tracer.spanBuilder("gateway_authorization")
                .setSpanKind(SpanKind.CLIENT)
                .setAttribute("gateway.name", request.getGateway())
                .startSpan();
                
            try (Scope gatewayScope = gatewaySpan.makeCurrent()) {
                AuthorizationResponse auth = gateway.authorize(request);
                gatewaySpan.setAttribute("gateway.response_code", auth.getCode());
                gatewaySpan.setAttribute("gateway.authorization_id", auth.getId());
            } finally {
                gatewaySpan.end();
            }
            
            // Save to database
            Payment payment = savePayment(request, auth);
            
            span.setAttribute("payment.id", payment.getId());
            span.setAttribute("payment.status", payment.getStatus());
            
            return payment;
            
        } catch (Exception e) {
            span.recordException(e);
            span.setStatus(StatusCode.ERROR, e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }
}
```

### Logging Strategy

```python
# Structured logging with context
import structlog
from contextvars import ContextVar

# Context variables for request tracking
request_id_var: ContextVar[str] = ContextVar('request_id')
user_id_var: ContextVar[str] = ContextVar('user_id')
merchant_id_var: ContextVar[str] = ContextVar('merchant_id')

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.CallsiteParameterAdder(
            parameters=[
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.FUNC_NAME,
            ]
        ),
        add_request_context,  # Custom processor
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

def add_request_context(logger, log_method, event_dict):
    """Add request context to all log entries"""
    if request_id := request_id_var.get(None):
        event_dict['request_id'] = request_id
    if user_id := user_id_var.get(None):
        event_dict['user_id'] = user_id
    if merchant_id := merchant_id_var.get(None):
        event_dict['merchant_id'] = merchant_id
    return event_dict

# Usage in service
logger = structlog.get_logger()

class PaymentService:
    async def process_payment(self, request: PaymentRequest) -> Payment:
        logger.info(
            "Processing payment",
            amount=request.amount,
            currency=request.currency,
            payment_method=request.payment_method
        )
        
        try:
            # Validate
            await self.validate_payment(request)
            logger.debug("Payment validated successfully")
            
            # Authorize
            auth_response = await self.gateway.authorize(request)
            logger.info(
                "Payment authorized",
                authorization_id=auth_response.id,
                response_code=auth_response.code
            )
            
            # Save
            payment = await self.repository.save_payment(request, auth_response)
            logger.info(
                "Payment saved",
                payment_id=payment.id,
                status=payment.status
            )
            
            return payment
            
        except ValidationError as e:
            logger.warning(
                "Payment validation failed",
                error=str(e),
                validation_errors=e.errors
            )
            raise
        except GatewayError as e:
            logger.error(
                "Gateway error",
                error=str(e),
                gateway=request.gateway,
                error_code=e.code
            )
            raise
        except Exception as e:
            logger.exception("Unexpected error processing payment")
            raise
```

## Security Implementation

### PCI DSS Compliance

```python
# Card data handling with PCI compliance
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import secrets

class PCICompliantCardHandler:
    def __init__(self, encryption_key: bytes):
        self.encryption_key = encryption_key
        self.backend = default_backend()
        
    def tokenize_card(self, card_number: str) -> str:
        """Generate format-preserving token"""
        # Never log card numbers
        if self._is_valid_card_number(card_number):
            # Generate unique token
            token = self._generate_token()
            
            # Encrypt card number for storage
            encrypted = self._encrypt_sensitive_data(card_number)
            
            # Store in secure vault (not in application DB)
            self._store_in_vault(token, encrypted)
            
            # Return token for application use
            return token
        else:
            raise ValueError("Invalid card number")
    
    def _encrypt_sensitive_data(self, data: str) -> bytes:
        """AES-256-GCM encryption for sensitive data"""
        # Generate random IV for each encryption
        iv = secrets.token_bytes(16)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(self.encryption_key),
            modes.GCM(iv),
            backend=self.backend
        )
        
        encryptor = cipher.encryptor()
        
        # Pad and encrypt
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()
        
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # Return IV + ciphertext + tag
        return iv + ciphertext + encryptor.tag
    
    def _is_valid_card_number(self, card_number: str) -> bool:
        """Luhn algorithm validation"""
        digits = [int(d) for d in card_number if d.isdigit()]
        checksum = 0
        
        # Double every second digit from right
        for i in range(len(digits) - 2, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
                
        return sum(digits) % 10 == 0
```

### API Security

```go
// JWT authentication middleware
package middleware

import (
    "github.com/golang-jwt/jwt/v4"
    "github.com/labstack/echo/v4"
)

type JWTConfig struct {
    SigningKey   []byte
    SigningMethod string
    Claims       jwt.Claims
    Skipper      func(c echo.Context) bool
}

func JWTMiddleware(config JWTConfig) echo.MiddlewareFunc {
    return func(next echo.HandlerFunc) echo.HandlerFunc {
        return func(c echo.Context) error {
            if config.Skipper != nil && config.Skipper(c) {
                return next(c)
            }
            
            // Extract token from header
            auth := c.Request().Header.Get("Authorization")
            if auth == "" {
                return echo.NewHTTPError(401, "Missing authorization header")
            }
            
            tokenString := strings.TrimPrefix(auth, "Bearer ")
            
            // Parse and validate token
            token, err := jwt.ParseWithClaims(
                tokenString,
                config.Claims,
                func(token *jwt.Token) (interface{}, error) {
                    if token.Method.Alg() != config.SigningMethod {
                        return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
                    }
                    return config.SigningKey, nil
                },
            )
            
            if err != nil || !token.Valid {
                return echo.NewHTTPError(401, "Invalid token")
            }
            
            // Add claims to context
            c.Set("user", token.Claims)
            
            return next(c)
        }
    }
}

// Rate limiting middleware
func RateLimitMiddleware(store RateLimitStore) echo.MiddlewareFunc {
    return func(next echo.HandlerFunc) echo.HandlerFunc {
        return func(c echo.Context) error {
            // Get identifier (API key or IP)
            identifier := c.Request().Header.Get("X-API-Key")
            if identifier == "" {
                identifier = c.RealIP()
            }
            
            // Check rate limit
            key := fmt.Sprintf("rate_limit:%s:%s", c.Path(), identifier)
            
            count, err := store.Increment(key, time.Minute)
            if err != nil {
                return echo.NewHTTPError(500, "Rate limit error")
            }
            
            limit := getRateLimitForEndpoint(c.Path())
            
            // Set headers
            c.Response().Header().Set("X-RateLimit-Limit", strconv.Itoa(limit))
            c.Response().Header().Set("X-RateLimit-Remaining", strconv.Itoa(limit-count))
            c.Response().Header().Set("X-RateLimit-Reset", strconv.FormatInt(time.Now().Add(time.Minute).Unix(), 10))
            
            if count > limit {
                return echo.NewHTTPError(429, "Rate limit exceeded")
            }
            
            return next(c)
        }
    }
}
```

## Conclusion

These implementation guidelines provide a comprehensive framework for building modern payment systems. Key considerations:

1. **Technology choices** should align with team expertise and scale requirements
2. **Integration patterns** must handle failures gracefully
3. **Performance optimization** is critical for payment systems
4. **Security** must be built-in from the start
5. **Observability** enables rapid problem resolution
6. **Testing** at all levels ensures reliability

Regular review and updates of these guidelines ensure they remain relevant as technologies and requirements evolve.
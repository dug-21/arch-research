# Payment Systems API Design Patterns and Best Practices

## Executive Summary

This document outlines comprehensive API design patterns specifically tailored for payment systems, covering REST, GraphQL, gRPC, and event-driven architectures. It provides implementation guidelines for building secure, scalable, and developer-friendly payment APIs.

## Table of Contents

1. [RESTful API Design for Payments](#restful-api-design-for-payments)
2. [GraphQL API Patterns](#graphql-api-patterns)
3. [gRPC and Protocol Buffers](#grpc-and-protocol-buffers)
4. [API Security Patterns](#api-security-patterns)
5. [Rate Limiting and Throttling](#rate-limiting-and-throttling)
6. [API Documentation Standards](#api-documentation-standards)
7. [Webhook Design Patterns](#webhook-design-patterns)
8. [API Evolution and Versioning](#api-evolution-and-versioning)

## RESTful API Design for Payments

### 1. Resource-Oriented Design

```yaml
api_resources:
  /payments:
    description: Payment transactions
    operations:
      - POST: Create new payment
      - GET: List payments (with pagination)
    
  /payments/{id}:
    description: Individual payment
    operations:
      - GET: Retrieve payment details
      - PATCH: Update payment (limited fields)
    
  /payments/{id}/authorize:
    description: Payment authorization
    operations:
      - POST: Authorize payment
    
  /payments/{id}/capture:
    description: Payment capture
    operations:
      - POST: Capture authorized payment
    
  /payments/{id}/refunds:
    description: Payment refunds
    operations:
      - POST: Create refund
      - GET: List refunds for payment
    
  /payment-methods:
    description: Customer payment methods
    operations:
      - POST: Add payment method
      - GET: List payment methods
      - DELETE /{id}: Remove payment method
```

### 2. Request/Response Design

```python
# Payment creation request
class CreatePaymentRequest(BaseModel):
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    currency: str = Field(..., regex="^[A-Z]{3}$")
    payment_method: PaymentMethodInput
    merchant_reference: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    metadata: Optional[Dict[str, str]] = Field(default_factory=dict)
    
    # 3D Secure options
    three_d_secure: Optional[ThreeDSecureOptions] = None
    
    # Capture settings
    capture_method: CaptureMethod = CaptureMethod.AUTOMATIC
    capture_on: Optional[datetime] = None
    
    # Customer information
    customer: Optional[CustomerInfo] = None
    billing_address: Optional[Address] = None
    shipping_address: Optional[Address] = None
    
    class Config:
        json_encoders = {
            Decimal: str,
            datetime: lambda v: v.isoformat()
        }

# Payment response
class PaymentResponse(BaseModel):
    id: str = Field(..., description="Unique payment identifier")
    status: PaymentStatus
    amount: PaymentAmount
    payment_method: PaymentMethodDetails
    
    # Processing details
    authorized_at: Optional[datetime] = None
    captured_at: Optional[datetime] = None
    authorization_code: Optional[str] = None
    
    # 3D Secure results
    three_d_secure_details: Optional[ThreeDSecureResult] = None
    
    # Risk assessment
    risk_score: Optional[int] = Field(None, ge=0, le=100)
    risk_factors: Optional[List[str]] = None
    
    # Metadata
    created_at: datetime
    updated_at: datetime
    merchant_reference: str
    metadata: Dict[str, str]
    
    # HATEOAS links
    links: List[Link]
    
    @property
    def is_capturable(self) -> bool:
        return self.status == PaymentStatus.AUTHORIZED
    
    @property
    def is_refundable(self) -> bool:
        return self.status in [PaymentStatus.CAPTURED, PaymentStatus.SETTLED]
```

### 3. Error Response Standards

```json
{
  "error": {
    "type": "invalid_request_error",
    "code": "amount_too_small",
    "message": "Amount must be at least $0.50 USD",
    "param": "amount",
    "doc_url": "https://docs.payment.com/errors/amount_too_small"
  },
  "request_id": "req_123abc",
  "idempotency_key": "idem_xyz789"
}
```

### 4. Pagination Patterns

```python
class PaginationParams(BaseModel):
    limit: int = Field(default=10, ge=1, le=100)
    starting_after: Optional[str] = None
    ending_before: Optional[str] = None
    created: Optional[DateRangeFilter] = None
    
class PaymentListResponse(BaseModel):
    data: List[PaymentResponse]
    has_more: bool
    total_count: Optional[int] = None
    url: str = "/v1/payments"
    
    # Cursor-based pagination
    first_id: Optional[str] = None
    last_id: Optional[str] = None
    
    def get_next_page_params(self) -> Optional[Dict[str, str]]:
        if self.has_more and self.last_id:
            return {"starting_after": self.last_id}
        return None
```

## GraphQL API Patterns

### 1. Schema Design for Payments

```graphql
# Root schema
schema {
  query: Query
  mutation: Mutation
  subscription: Subscription
}

# Payment type with field-level permissions
type Payment {
  id: ID!
  amount: Money!
  status: PaymentStatus!
  paymentMethod: PaymentMethod!
  
  # Sensitive fields with authorization
  authorizationCode: String @auth(requires: ["payments:read:sensitive"])
  
  # Computed fields
  capturedAmount: Money!
  refundableAmount: Money!
  isLive: Boolean!
  
  # Related entities
  customer: Customer
  merchant: Merchant!
  refunds: [Refund!]!
  disputes: [Dispute!]!
  
  # Metadata
  metadata: JSON
  createdAt: DateTime!
  updatedAt: DateTime!
}

# Money type for proper currency handling
type Money {
  amount: Int! # Amount in smallest currency unit
  currency: String!
  formatted: String! # Human-readable format
}

# Input types for mutations
input CreatePaymentInput {
  amount: MoneyInput!
  paymentMethodId: ID!
  customerId: ID
  description: String
  metadata: JSON
  captureMethod: CaptureMethod = AUTOMATIC
  statementDescriptor: String
}

# Mutations with clear naming
type Mutation {
  # Payment operations
  createPayment(input: CreatePaymentInput!): CreatePaymentPayload!
  authorizePayment(id: ID!): AuthorizePaymentPayload!
  capturePayment(id: ID!, amount: MoneyInput): CapturePaymentPayload!
  refundPayment(id: ID!, amount: MoneyInput, reason: RefundReason): RefundPaymentPayload!
  
  # Payment method operations
  createPaymentMethod(input: CreatePaymentMethodInput!): CreatePaymentMethodPayload!
  deletePaymentMethod(id: ID!): DeletePaymentMethodPayload!
  
  # Subscription operations
  createSubscription(input: CreateSubscriptionInput!): CreateSubscriptionPayload!
  cancelSubscription(id: ID!, immediately: Boolean = false): CancelSubscriptionPayload!
}
```

### 2. Query Optimization with DataLoader

```typescript
class PaymentDataLoaders {
  // Batch loading for N+1 query prevention
  static createLoaders() {
    return {
      // Payment loader
      paymentById: new DataLoader<string, Payment>(
        async (ids) => {
          const payments = await db.payments.findByIds(ids);
          return ids.map(id => payments.find(p => p.id === id));
        },
        { cache: true, maxBatchSize: 100 }
      ),
      
      // Customer payments loader
      paymentsByCustomerId: new DataLoader<string, Payment[]>(
        async (customerIds) => {
          const payments = await db.payments.findByCustomerIds(customerIds);
          return customerIds.map(id => 
            payments.filter(p => p.customerId === id)
          );
        },
        { cache: false } // Don't cache lists
      ),
      
      // Refunds loader
      refundsByPaymentId: new DataLoader<string, Refund[]>(
        async (paymentIds) => {
          const refunds = await db.refunds.findByPaymentIds(paymentIds);
          return paymentIds.map(id => 
            refunds.filter(r => r.paymentId === id)
          );
        }
      )
    };
  }
}

// Resolver implementation
const paymentResolvers = {
  Payment: {
    // Use DataLoader for related entities
    customer: (payment, _, { dataloaders }) => 
      payment.customerId 
        ? dataloaders.customerById.load(payment.customerId)
        : null,
    
    refunds: (payment, _, { dataloaders }) => 
      dataloaders.refundsByPaymentId.load(payment.id),
    
    // Computed fields
    capturedAmount: async (payment) => {
      const captures = await db.captures.findByPaymentId(payment.id);
      return {
        amount: captures.reduce((sum, c) => sum + c.amount, 0),
        currency: payment.currency
      };
    },
    
    isLive: (payment) => payment.livemode === true
  }
};
```

### 3. Subscription Patterns

```graphql
type Subscription {
  # Real-time payment updates
  paymentUpdated(
    merchantId: ID!
    statuses: [PaymentStatus!]
  ): Payment! @auth(requires: ["payments:subscribe"])
  
  # Webhook events stream
  webhookEvent(
    types: [WebhookEventType!]
    merchantId: ID!
  ): WebhookEvent! @auth(requires: ["webhooks:subscribe"])
  
  # Risk alerts
  riskAlert(
    merchantId: ID!
    severity: AlertSeverity
  ): RiskAlert! @auth(requires: ["risk:monitor"])
}
```

## gRPC and Protocol Buffers

### 1. Payment Service Definition

```protobuf
syntax = "proto3";

package payment.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/field_mask.proto";
import "google/type/money.proto";

// Payment service definition
service PaymentService {
  // Unary RPC for payment creation
  rpc CreatePayment(CreatePaymentRequest) returns (Payment) {
    option (google.api.http) = {
      post: "/v1/payments"
      body: "*"
    };
  }
  
  // Server streaming for real-time updates
  rpc StreamPaymentUpdates(StreamPaymentUpdatesRequest) 
    returns (stream PaymentUpdate);
  
  // Bidirectional streaming for batch processing
  rpc ProcessPaymentBatch(stream BatchPaymentRequest) 
    returns (stream BatchPaymentResponse);
}

// Payment message
message Payment {
  string id = 1;
  google.type.Money amount = 2;
  PaymentStatus status = 3;
  string payment_method_id = 4;
  
  // Optional fields
  optional string authorization_code = 5;
  optional google.protobuf.Timestamp authorized_at = 6;
  optional google.protobuf.Timestamp captured_at = 7;
  
  // Metadata
  map<string, string> metadata = 8;
  google.protobuf.Timestamp created_at = 9;
  google.protobuf.Timestamp updated_at = 10;
}

// Request/Response messages
message CreatePaymentRequest {
  google.type.Money amount = 1;
  string payment_method_id = 2;
  string idempotency_key = 3;
  
  oneof capture_method {
    bool capture_immediately = 4;
    google.protobuf.Timestamp capture_at = 5;
  }
  
  map<string, string> metadata = 6;
}

// Streaming messages
message StreamPaymentUpdatesRequest {
  string merchant_id = 1;
  repeated PaymentStatus statuses = 2;
  google.protobuf.Timestamp since = 3;
}

message PaymentUpdate {
  Payment payment = 1;
  repeated string changed_fields = 2;
  google.protobuf.Timestamp timestamp = 3;
}
```

### 2. gRPC Implementation with Interceptors

```go
// Payment service implementation
type paymentService struct {
    pb.UnimplementedPaymentServiceServer
    repo         PaymentRepository
    eventBus     EventBus
    rateLimiter  RateLimiter
}

// Unary RPC implementation
func (s *paymentService) CreatePayment(
    ctx context.Context,
    req *pb.CreatePaymentRequest,
) (*pb.Payment, error) {
    // Extract metadata
    md, ok := metadata.FromIncomingContext(ctx)
    if !ok {
        return nil, status.Error(codes.InvalidArgument, "missing metadata")
    }
    
    // Idempotency check
    idempotencyKey := req.IdempotencyKey
    if existing, err := s.repo.GetByIdempotencyKey(ctx, idempotencyKey); err == nil {
        return existing, nil
    }
    
    // Create payment
    payment := &Payment{
        ID:            generateID(),
        Amount:        req.Amount,
        PaymentMethod: req.PaymentMethodId,
        Status:        PaymentStatusPending,
        Metadata:      req.Metadata,
        CreatedAt:     time.Now(),
    }
    
    // Process payment
    if err := s.processPayment(ctx, payment); err != nil {
        return nil, status.Errorf(codes.Internal, "payment processing failed: %v", err)
    }
    
    // Publish event
    s.eventBus.Publish(ctx, PaymentCreatedEvent{Payment: payment})
    
    return payment.ToProto(), nil
}

// Streaming RPC implementation
func (s *paymentService) StreamPaymentUpdates(
    req *pb.StreamPaymentUpdatesRequest,
    stream pb.PaymentService_StreamPaymentUpdatesServer,
) error {
    // Subscribe to payment events
    sub := s.eventBus.Subscribe(
        fmt.Sprintf("merchant:%s:payments", req.MerchantId),
    )
    defer sub.Close()
    
    // Send updates
    for {
        select {
        case event := <-sub.Events():
            update := &pb.PaymentUpdate{
                Payment:       event.Payment.ToProto(),
                ChangedFields: event.ChangedFields,
                Timestamp:     timestamppb.Now(),
            }
            
            if err := stream.Send(update); err != nil {
                return err
            }
            
        case <-stream.Context().Done():
            return stream.Context().Err()
        }
    }
}

// Interceptor for authentication
func authInterceptor(
    ctx context.Context,
    req interface{},
    info *grpc.UnaryServerInfo,
    handler grpc.UnaryHandler,
) (interface{}, error) {
    // Extract token from metadata
    md, ok := metadata.FromIncomingContext(ctx)
    if !ok {
        return nil, status.Error(codes.Unauthenticated, "missing metadata")
    }
    
    tokens := md.Get("authorization")
    if len(tokens) == 0 {
        return nil, status.Error(codes.Unauthenticated, "missing token")
    }
    
    // Verify token
    claims, err := verifyToken(tokens[0])
    if err != nil {
        return nil, status.Error(codes.Unauthenticated, "invalid token")
    }
    
    // Add claims to context
    ctx = context.WithValue(ctx, "claims", claims)
    
    return handler(ctx, req)
}
```

## API Security Patterns

### 1. Authentication and Authorization

```python
class APISecurityMiddleware:
    """
    Comprehensive API security implementation
    """
    def __init__(self):
        self.token_validator = TokenValidator()
        self.permission_checker = PermissionChecker()
        self.audit_logger = AuditLogger()
        
    async def authenticate_request(
        self,
        request: Request
    ) -> AuthenticationResult:
        # Multiple authentication methods
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            # JWT authentication
            token = auth_header[7:]
            return await self._validate_jwt(token)
            
        elif auth_header and auth_header.startswith('Basic '):
            # API key authentication
            credentials = auth_header[6:]
            return await self._validate_api_key(credentials)
            
        elif 'X-API-Key' in request.headers:
            # Header-based API key
            return await self._validate_api_key(
                request.headers['X-API-Key']
            )
        else:
            raise AuthenticationError("No valid authentication provided")
    
    async def check_permissions(
        self,
        auth_result: AuthenticationResult,
        resource: str,
        action: str
    ) -> bool:
        # RBAC with ABAC
        # Role-based check
        if self.permission_checker.has_role_permission(
            auth_result.roles,
            resource,
            action
        ):
            return True
            
        # Attribute-based check
        attributes = {
            'user_id': auth_result.user_id,
            'merchant_id': auth_result.merchant_id,
            'ip_address': auth_result.ip_address,
            'time_of_day': datetime.now().hour,
            'resource': resource,
            'action': action
        }
        
        return await self.permission_checker.evaluate_policy(
            attributes,
            self.get_applicable_policies(auth_result)
        )
    
    async def _validate_jwt(self, token: str) -> AuthenticationResult:
        """
        JWT validation with key rotation support
        """
        try:
            # Decode header to get key ID
            header = jwt.get_unverified_header(token)
            kid = header.get('kid')
            
            # Get public key for verification
            public_key = await self.get_public_key(kid)
            
            # Verify and decode
            payload = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                options={
                    'verify_exp': True,
                    'verify_aud': True,
                    'require': ['exp', 'iat', 'sub', 'aud']
                }
            )
            
            # Additional validation
            if not self._validate_token_claims(payload):
                raise AuthenticationError("Invalid token claims")
                
            return AuthenticationResult(
                user_id=payload['sub'],
                merchant_id=payload.get('merchant_id'),
                roles=payload.get('roles', []),
                permissions=payload.get('permissions', []),
                token_id=payload.get('jti'),
                expires_at=datetime.fromtimestamp(payload['exp'])
            )
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise AuthenticationError(f"Invalid token: {str(e)}")
```

### 2. Request Signing and Verification

```typescript
class RequestSignatureVerifier {
  private readonly SECRET_ROTATION_WINDOW = 3600; // 1 hour
  
  async verifySignature(
    request: Request,
    merchantId: string
  ): Promise<boolean> {
    const signature = request.headers['x-signature'];
    const timestamp = request.headers['x-timestamp'];
    const nonce = request.headers['x-nonce'];
    
    if (!signature || !timestamp || !nonce) {
      throw new SignatureError('Missing signature headers');
    }
    
    // Verify timestamp to prevent replay attacks
    const requestTime = parseInt(timestamp);
    const currentTime = Math.floor(Date.now() / 1000);
    
    if (Math.abs(currentTime - requestTime) > 300) { // 5 minutes
      throw new SignatureError('Request timestamp too old');
    }
    
    // Check nonce to prevent replay
    if (await this.nonceExists(nonce)) {
      throw new SignatureError('Duplicate request nonce');
    }
    
    // Get signing secret(s)
    const secrets = await this.getSigningSecrets(merchantId);
    
    // Build canonical request
    const canonicalRequest = this.buildCanonicalRequest(
      request.method,
      request.path,
      request.query,
      request.headers,
      request.body,
      timestamp,
      nonce
    );
    
    // Verify signature with any valid secret
    for (const secret of secrets) {
      const expectedSignature = this.calculateSignature(
        canonicalRequest,
        secret
      );
      
      if (timingSafeEqual(
        Buffer.from(signature),
        Buffer.from(expectedSignature)
      )) {
        // Store nonce to prevent replay
        await this.storeNonce(nonce, requestTime);
        return true;
      }
    }
    
    return false;
  }
  
  private buildCanonicalRequest(
    method: string,
    path: string,
    query: Record<string, string>,
    headers: Record<string, string>,
    body: string,
    timestamp: string,
    nonce: string
  ): string {
    // Sort query parameters
    const sortedQuery = Object.keys(query)
      .sort()
      .map(key => `${key}=${query[key]}`)
      .join('&');
    
    // Select signed headers
    const signedHeaders = ['host', 'content-type', 'x-timestamp', 'x-nonce'];
    const canonicalHeaders = signedHeaders
      .map(h => `${h}:${headers[h]}`)
      .join('\n');
    
    // Build canonical request
    return [
      method.toUpperCase(),
      path,
      sortedQuery,
      canonicalHeaders,
      crypto.createHash('sha256').update(body).digest('hex'),
      timestamp,
      nonce
    ].join('\n');
  }
}
```

## Rate Limiting and Throttling

### 1. Advanced Rate Limiting Implementation

```python
class AdaptiveRateLimiter:
    """
    ML-enhanced adaptive rate limiting
    """
    def __init__(self):
        self.redis_client = Redis()
        self.ml_model = self.load_adaptive_model()
        self.strategies = {
            'token_bucket': TokenBucketStrategy(),
            'sliding_window': SlidingWindowStrategy(),
            'leaky_bucket': LeakyBucketStrategy(),
            'adaptive_window': AdaptiveWindowStrategy()
        }
        
    async def check_rate_limit(
        self,
        client_id: str,
        endpoint: str,
        client_context: ClientContext
    ) -> RateLimitResult:
        # Get client profile
        profile = await self.get_client_profile(client_id)
        
        # Predict optimal limits using ML
        predicted_limits = self.ml_model.predict({
            'client_behavior': profile.behavior_metrics,
            'endpoint': endpoint,
            'time_of_day': datetime.now().hour,
            'day_of_week': datetime.now().weekday(),
            'current_load': await self.get_system_load(),
            'client_tier': profile.tier,
            'historical_usage': profile.usage_history
        })
        
        # Apply tiered limits
        limits = self.apply_tier_limits(client_context.tier, predicted_limits)
        
        # Check multiple windows
        checks = await asyncio.gather(
            self.check_burst_limit(client_id, limits.burst),
            self.check_sustained_limit(client_id, limits.sustained),
            self.check_daily_quota(client_id, limits.daily_quota),
            self.check_concurrent_requests(client_id, limits.concurrent)
        )
        
        # Return most restrictive result
        for check in checks:
            if not check.allowed:
                return check
                
        return RateLimitResult(
            allowed=True,
            limit=limits.sustained.limit,
            remaining=limits.sustained.remaining,
            reset_at=limits.sustained.reset_at,
            retry_after=None
        )
    
    async def check_burst_limit(
        self,
        client_id: str,
        limit: BurstLimit
    ) -> RateLimitResult:
        """
        Token bucket for burst control
        """
        key = f"burst:{client_id}"
        pipe = self.redis_client.pipeline()
        
        # Lua script for atomic token bucket
        lua_script = """
        local key = KEYS[1]
        local limit = tonumber(ARGV[1])
        local window = tonumber(ARGV[2])
        local now = tonumber(ARGV[3])
        
        local current = redis.call('HGETALL', key)
        local tokens = limit
        local last_refill = now
        
        if #current > 0 then
            tokens = tonumber(current[2])
            last_refill = tonumber(current[4])
            
            -- Refill tokens
            local elapsed = now - last_refill
            local refill = elapsed * (limit / window)
            tokens = math.min(limit, tokens + refill)
        end
        
        if tokens >= 1 then
            tokens = tokens - 1
            redis.call('HSET', key, 'tokens', tokens, 'last_refill', now)
            redis.call('EXPIRE', key, window)
            return {1, tokens, limit}
        else
            return {0, 0, limit}
        end
        """
        
        result = await pipe.eval(
            lua_script,
            1,
            key,
            limit.tokens,
            limit.window,
            time.time()
        )
        
        return RateLimitResult(
            allowed=bool(result[0]),
            limit=result[2],
            remaining=int(result[1]),
            reset_at=datetime.now() + timedelta(seconds=limit.window)
        )
```

### 2. Distributed Rate Limiting

```java
@Component
public class DistributedRateLimiter {
    private final RedisTemplate<String, String> redisTemplate;
    private final ConsistentHashing consistentHashing;
    
    // Sliding window with Redis Sorted Sets
    public CompletableFuture<RateLimitResult> checkSlidingWindow(
        String clientId,
        String resource,
        int limit,
        Duration window
    ) {
        String key = String.format("rate:%s:%s", clientId, resource);
        long now = System.currentTimeMillis();
        long windowStart = now - window.toMillis();
        
        // Lua script for atomic sliding window
        String luaScript = """
            local key = KEYS[1]
            local now = tonumber(ARGV[1])
            local window_start = tonumber(ARGV[2])
            local limit = tonumber(ARGV[3])
            local ttl = tonumber(ARGV[4])
            
            -- Remove old entries
            redis.call('ZREMRANGEBYSCORE', key, 0, window_start)
            
            -- Count current window
            local current = redis.call('ZCARD', key)
            
            if current < limit then
                -- Add new request
                redis.call('ZADD', key, now, now)
                redis.call('EXPIRE', key, ttl)
                return {1, limit - current - 1}
            else
                -- Get oldest entry for retry time
                local oldest = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')
                local retry_after = oldest[2] + ttl - now
                return {0, retry_after}
            end
        """;
        
        return redisTemplate.execute(
            RedisScript.of(luaScript, List.class),
            List.of(key),
            String.valueOf(now),
            String.valueOf(windowStart),
            String.valueOf(limit),
            String.valueOf(window.getSeconds())
        ).thenApply(result -> {
            boolean allowed = ((Number) result.get(0)).intValue() == 1;
            
            if (allowed) {
                return RateLimitResult.allowed(
                    limit,
                    ((Number) result.get(1)).intValue()
                );
            } else {
                long retryAfter = ((Number) result.get(1)).longValue();
                return RateLimitResult.denied(retryAfter);
            }
        });
    }
    
    // Distributed concurrency limiting
    public CompletableFuture<Boolean> acquireConcurrencySlot(
        String clientId,
        String resource,
        int maxConcurrent,
        Duration timeout
    ) {
        String key = String.format("concurrent:%s:%s", clientId, resource);
        String requestId = UUID.randomUUID().toString();
        
        // Try to acquire slot
        String acquireScript = """
            local key = KEYS[1]
            local request_id = ARGV[1]
            local max_concurrent = tonumber(ARGV[2])
            local ttl = tonumber(ARGV[3])
            
            local current = redis.call('HLEN', key)
            
            if current < max_concurrent then
                redis.call('HSET', key, request_id, '1')
                redis.call('EXPIRE', key, ttl)
                return 1
            else
                return 0
            end
        """;
        
        return redisTemplate.execute(
            RedisScript.of(acquireScript, Long.class),
            List.of(key),
            requestId,
            String.valueOf(maxConcurrent),
            String.valueOf(timeout.getSeconds())
        ).thenApply(result -> result == 1L);
    }
}
```

## API Documentation Standards

### 1. OpenAPI 3.0 Specification

```yaml
openapi: 3.0.3
info:
  title: Payment Processing API
  version: 2024.01.15
  description: |
    # Introduction
    The Payment Processing API provides a complete solution for accepting
    and managing online payments.
    
    ## Authentication
    All API requests require authentication using API keys or OAuth 2.0.
    
    ## Rate Limiting
    API calls are rate limited based on your plan. Standard limits:
    - 100 requests per second
    - 10,000 requests per hour
    
  contact:
    email: api-support@payment.com
  x-logo:
    url: 'https://payment.com/logo.png'

servers:
  - url: https://api.payment.com/v1
    description: Production server
  - url: https://api-sandbox.payment.com/v1
    description: Sandbox server

security:
  - bearerAuth: []
  - apiKey: []

paths:
  /payments:
    post:
      tags: [Payments]
      summary: Create a payment
      operationId: createPayment
      x-codegen-request-body-name: payment
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreatePaymentRequest'
            examples:
              card_payment:
                summary: Card payment
                value:
                  amount: 5000
                  currency: USD
                  payment_method: pm_card_visa
              bank_payment:
                summary: Bank payment
                value:
                  amount: 10000
                  currency: EUR
                  payment_method: pm_bank_sepa
      responses:
        '201':
          description: Payment created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Payment'
          links:
            authorizePayment:
              operationId: authorizePayment
              parameters:
                paymentId: '$response.body#/id'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '422':
          $ref: '#/components/responses/UnprocessableEntity'

components:
  schemas:
    Payment:
      type: object
      required: [id, amount, currency, status]
      properties:
        id:
          type: string
          pattern: '^pay_[a-zA-Z0-9]{24}$'
          example: pay_1234567890abcdef12345678
        amount:
          $ref: '#/components/schemas/Money'
        status:
          $ref: '#/components/schemas/PaymentStatus'
        payment_method:
          $ref: '#/components/schemas/PaymentMethod'
        
    Money:
      type: object
      required: [amount, currency]
      properties:
        amount:
          type: integer
          minimum: 0
          description: Amount in smallest currency unit
        currency:
          type: string
          pattern: '^[A-Z]{3}$'
          example: USD
```

### 2. API Documentation Best Practices

```python
class APIDocumentation:
    """
    Auto-generated API documentation with examples
    """
    
    @swagger.doc({
        'tags': ['Payments'],
        'summary': 'Create a new payment',
        'description': '''
        Creates a new payment with the specified amount and payment method.
        
        ## Important Notes
        
        - Amount must be specified in the smallest currency unit (e.g., cents)
        - Payment methods must be pre-authorized before use
        - Idempotency keys prevent duplicate charges
        ''',
        'parameters': [
            {
                'name': 'Idempotency-Key',
                'in': 'header',
                'required': True,
                'schema': {'type': 'string'},
                'description': 'Unique key to prevent duplicate requests'
            }
        ],
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {'$ref': '#/components/schemas/CreatePaymentRequest'},
                    'examples': {
                        'simple_payment': {
                            'summary': 'Simple payment',
                            'value': {
                                'amount': 2000,
                                'currency': 'USD',
                                'payment_method_id': 'pm_1234567890'
                            }
                        },
                        'payment_with_metadata': {
                            'summary': 'Payment with metadata',
                            'value': {
                                'amount': 5000,
                                'currency': 'EUR',
                                'payment_method_id': 'pm_0987654321',
                                'description': 'Order #1234',
                                'metadata': {
                                    'order_id': '1234',
                                    'customer_email': 'customer@example.com'
                                }
                            }
                        }
                    }
                }
            }
        },
        'responses': {
            '201': {
                'description': 'Payment created successfully',
                'content': {
                    'application/json': {
                        'schema': {'$ref': '#/components/schemas/Payment'}
                    }
                }
            },
            '400': {'$ref': '#/components/responses/BadRequest'},
            '401': {'$ref': '#/components/responses/Unauthorized'},
            '422': {'$ref': '#/components/responses/ValidationError'}
        }
    })
    async def create_payment(self, request: CreatePaymentRequest) -> Payment:
        """Create a new payment."""
        # Implementation
        pass
```

## Webhook Design Patterns

### 1. Webhook Event Structure

```json
{
  "id": "evt_1234567890abcdef",
  "type": "payment.succeeded",
  "api_version": "2024.01.15",
  "created": 1642550400,
  "data": {
    "object": {
      "id": "pay_1234567890abcdef",
      "amount": 2000,
      "currency": "USD",
      "status": "succeeded"
    },
    "previous_attributes": {
      "status": "processing"
    }
  },
  "request": {
    "id": "req_abcdef1234567890",
    "idempotency_key": "idem_key_123"
  },
  "pending_webhooks": 2,
  "livemode": true
}
```

### 2. Webhook Delivery Implementation

```typescript
class WebhookDeliveryService {
  private readonly MAX_RETRIES = 5;
  private readonly RETRY_DELAYS = [5, 30, 120, 600, 3600]; // seconds
  
  async deliverWebhook(
    webhook: WebhookSubscription,
    event: WebhookEvent
  ): Promise<DeliveryResult> {
    const attempt = {
      webhook_id: webhook.id,
      event_id: event.id,
      attempt_number: 1,
      attempted_at: new Date()
    };
    
    // Sign payload
    const signature = this.signPayload(
      event,
      webhook.signing_secret
    );
    
    // Prepare request
    const headers = {
      'Content-Type': 'application/json',
      'X-Webhook-Signature': signature,
      'X-Webhook-Id': event.id,
      'X-Webhook-Timestamp': Math.floor(Date.now() / 1000).toString(),
      'X-API-Version': event.api_version,
      'User-Agent': 'PaymentAPI-Webhook/2.0'
    };
    
    // Attempt delivery
    try {
      const response = await this.httpClient.post(
        webhook.url,
        event,
        {
          headers,
          timeout: 30000,
          validateStatus: () => true // Don't throw on HTTP errors
        }
      );
      
      if (response.status >= 200 && response.status < 300) {
        return {
          success: true,
          status_code: response.status,
          response_body: response.data
        };
      } else {
        // Handle failure
        return await this.handleFailure(
          webhook,
          event,
          attempt,
          response
        );
      }
    } catch (error) {
      return await this.handleError(webhook, event, attempt, error);
    }
  }
  
  private async handleFailure(
    webhook: WebhookSubscription,
    event: WebhookEvent,
    attempt: WebhookAttempt,
    response: AxiosResponse
  ): Promise<DeliveryResult> {
    // Check if retryable
    const isRetryable = [408, 429, 500, 502, 503, 504].includes(
      response.status
    );
    
    if (isRetryable && attempt.attempt_number < this.MAX_RETRIES) {
      const delay = this.RETRY_DELAYS[attempt.attempt_number - 1];
      
      await this.scheduleRetry(webhook, event, attempt, delay);
      
      return {
        success: false,
        status_code: response.status,
        will_retry: true,
        next_retry_at: new Date(Date.now() + delay * 1000)
      };
    }
    
    // Max retries exceeded or non-retryable error
    await this.disableWebhook(webhook, 'max_failures_exceeded');
    
    return {
      success: false,
      status_code: response.status,
      will_retry: false,
      disabled: true
    };
  }
  
  private signPayload(
    event: WebhookEvent,
    secret: string
  ): string {
    const timestamp = Math.floor(Date.now() / 1000);
    const payload = `${timestamp}.${JSON.stringify(event)}`;
    
    const signature = crypto
      .createHmac('sha256', secret)
      .update(payload)
      .digest('hex');
      
    return `t=${timestamp},v1=${signature}`;
  }
}
```

## API Evolution and Versioning

### 1. Version Migration Strategy

```python
class APIVersionManager:
    """
    Manages API versioning and migration
    """
    def __init__(self):
        self.versions = {
            '2023.01.01': V2023_01_01(),
            '2023.06.15': V2023_06_15(),
            '2024.01.15': V2024_01_15()  # Current
        }
        self.current_version = '2024.01.15'
        self.deprecation_schedule = {
            '2023.01.01': datetime(2024, 6, 30),
            '2023.06.15': datetime(2024, 12, 31)
        }
        
    def get_handler(self, version: str) -> APIVersionHandler:
        """Get appropriate handler for API version"""
        if version not in self.versions:
            raise UnsupportedVersionError(
                f"API version {version} is not supported"
            )
            
        # Check if deprecated
        if version in self.deprecation_schedule:
            deprecation_date = self.deprecation_schedule[version]
            if datetime.now() > deprecation_date:
                raise DeprecatedVersionError(
                    f"API version {version} was deprecated on {deprecation_date}"
                )
                
        return self.versions[version]
    
    def transform_request(
        self,
        request: Dict[str, Any],
        from_version: str,
        to_version: str
    ) -> Dict[str, Any]:
        """Transform request between versions"""
        if from_version == to_version:
            return request
            
        # Get transformation path
        path = self.get_transformation_path(from_version, to_version)
        
        # Apply transformations
        transformed = request
        for i in range(len(path) - 1):
            transformer = self.get_transformer(path[i], path[i + 1])
            transformed = transformer.transform_request(transformed)
            
        return transformed
    
    def add_deprecation_headers(
        self,
        response: Response,
        version: str
    ) -> Response:
        """Add deprecation headers to response"""
        if version in self.deprecation_schedule:
            deprecation_date = self.deprecation_schedule[version]
            
            response.headers['Deprecation'] = 'true'
            response.headers['Sunset'] = deprecation_date.strftime(
                '%a, %d %b %Y %H:%M:%S GMT'
            )
            response.headers['Link'] = (
                f'<https://docs.payment.com/migrations/{version}>; '
                'rel="deprecation"'
            )
            
        return response
```

### 2. Breaking Change Management

```typescript
interface BreakingChange {
  version: string;
  description: string;
  migration_guide: string;
  automatic_migration: boolean;
}

class BreakingChangeManager {
  private changes: Map<string, BreakingChange[]> = new Map([
    ['2024.01.15', [
      {
        version: '2024.01.15',
        description: 'Changed amount field from float to integer (minor units)',
        migration_guide: `
          // Before (2023.06.15)
          { "amount": 99.99, "currency": "USD" }
          
          // After (2024.01.15)
          { "amount": 9999, "currency": "USD" }
        `,
        automatic_migration: true
      },
      {
        version: '2024.01.15',
        description: 'Renamed card_number to payment_method_id',
        migration_guide: `
          // Before (2023.06.15)
          { "card_number": "4242424242424242" }
          
          // After (2024.01.15)
          { "payment_method_id": "pm_1234567890" }
        `,
        automatic_migration: false
      }
    ]]
  ]);
  
  migrateRequest(
    request: any,
    fromVersion: string,
    toVersion: string
  ): MigrationResult {
    const changes = this.getChanges(fromVersion, toVersion);
    let migrated = { ...request };
    const warnings: string[] = [];
    
    for (const change of changes) {
      if (change.automatic_migration) {
        migrated = this.applyAutomaticMigration(
          migrated,
          change
        );
      } else {
        warnings.push(
          `Manual migration required: ${change.description}`
        );
      }
    }
    
    return {
      data: migrated,
      warnings,
      migration_guide_url: `https://docs.payment.com/migrate/${fromVersion}/${toVersion}`
    };
  }
  
  private applyAutomaticMigration(
    data: any,
    change: BreakingChange
  ): any {
    // Example: Convert float amounts to integers
    if (change.description.includes('amount field from float to integer')) {
      if (typeof data.amount === 'number' && data.amount % 1 !== 0) {
        // Convert to minor units based on currency
        const minorUnits = this.getMinorUnits(data.currency);
        data.amount = Math.round(data.amount * Math.pow(10, minorUnits));
      }
    }
    
    return data;
  }
}
```

## Best Practices Summary

### 1. API Design Principles
- Use consistent resource naming and URL patterns
- Implement proper HTTP status codes and error messages
- Support idempotency for all mutating operations
- Provide comprehensive filtering, sorting, and pagination

### 2. Security Requirements
- Implement multiple authentication methods
- Use request signing for sensitive operations
- Apply rate limiting at multiple levels
- Encrypt all data in transit and at rest

### 3. Performance Optimization
- Implement response caching where appropriate
- Use connection pooling and keep-alive
- Support batch operations for bulk processing
- Optimize database queries with proper indexing

### 4. Developer Experience
- Provide comprehensive API documentation
- Include code examples in multiple languages
- Implement helpful error messages with remediation
- Support API versioning with graceful migrations

### 5. Reliability Patterns
- Implement circuit breakers for external calls
- Use retry logic with exponential backoff
- Design for eventual consistency
- Implement proper webhook delivery guarantees
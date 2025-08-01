# Payment System API Design Patterns

## Overview

This document outlines API design patterns specifically tailored for payment systems, focusing on reliability, security, and developer experience.

## 1. RESTful Payment API Design

### Resource-Oriented Architecture

```yaml
# Payment API Resource Hierarchy
/v1/payments
  /{payment_id}
    /authorize
    /capture
    /void
    /refund
    /status

/v1/merchants
  /{merchant_id}
    /payments
    /settlements
    /disputes
    /configuration

/v1/customers
  /{customer_id}
    /payment-methods
    /transactions
    /subscriptions

/v1/settlements
  /{settlement_id}
    /transactions
    /reconciliation

/v1/webhooks
  /subscriptions
  /events
```

### API Versioning Strategy

```python
class APIVersioning:
    """
    Header-based versioning with fallback support
    """
    def __init__(self):
        self.supported_versions = ['v1', 'v2', 'v3']
        self.deprecated_versions = ['v0']
        
    def get_api_version(self, request):
        # 1. Check Accept header (preferred)
        accept_header = request.headers.get('Accept', '')
        if 'application/vnd.payment.api' in accept_header:
            version = self.extract_version_from_accept(accept_header)
            if version:
                return version
        
        # 2. Check custom header
        version_header = request.headers.get('X-API-Version')
        if version_header and version_header in self.supported_versions:
            return version_header
        
        # 3. Check URL path
        path_parts = request.path.split('/')
        if len(path_parts) > 1 and path_parts[1] in self.supported_versions:
            return path_parts[1]
        
        # 4. Default to latest stable
        return 'v2'
    
    def extract_version_from_accept(self, accept_header):
        # Parse: application/vnd.payment.api.v2+json
        pattern = r'application/vnd\.payment\.api\.(v\d+)\+json'
        match = re.search(pattern, accept_header)
        return match.group(1) if match else None
```

### Idempotency Implementation

```python
class IdempotencyManager:
    def __init__(self, redis_client):
        self.cache = redis_client
        self.ttl = 86400  # 24 hours
        
    def process_request(self, request, handler):
        idempotency_key = request.headers.get('Idempotency-Key')
        
        if not idempotency_key:
            # Non-idempotent request
            return handler(request)
        
        # Check for existing result
        cache_key = f"idempotency:{idempotency_key}"
        cached_result = self.cache.get(cache_key)
        
        if cached_result:
            # Return cached response
            result = json.loads(cached_result)
            return Response(
                status=result['status'],
                body=result['body'],
                headers={
                    **result['headers'],
                    'X-Idempotent-Replay': 'true'
                }
            )
        
        # Lock to prevent concurrent processing
        lock_key = f"lock:{cache_key}"
        lock = self.cache.lock(lock_key, timeout=30)
        
        if not lock.acquire(blocking=True, timeout=5):
            return Response(
                status=409,
                body={'error': 'Request already being processed'}
            )
        
        try:
            # Process request
            response = handler(request)
            
            # Cache successful responses
            if 200 <= response.status < 300:
                self.cache.setex(
                    cache_key,
                    self.ttl,
                    json.dumps({
                        'status': response.status,
                        'body': response.body,
                        'headers': response.headers
                    })
                )
            
            return response
        finally:
            lock.release()
```

## 2. GraphQL Payment API Design

### Schema Design

```graphql
# Payment GraphQL Schema
type Payment {
  id: ID!
  amount: Money!
  status: PaymentStatus!
  method: PaymentMethod!
  merchant: Merchant!
  customer: Customer!
  metadata: JSON
  createdAt: DateTime!
  updatedAt: DateTime!
  
  # Nested operations
  authorization: Authorization
  captures: [Capture!]!
  refunds: [Refund!]!
  disputes: [Dispute!]!
}

type Money {
  amount: Float!
  currency: Currency!
  formatted: String!
}

enum PaymentStatus {
  PENDING
  AUTHORIZED
  CAPTURED
  SETTLED
  REFUNDED
  FAILED
  DISPUTED
}

type Query {
  payment(id: ID!): Payment
  payments(
    filter: PaymentFilter
    sort: PaymentSort
    pagination: PaginationInput
  ): PaymentConnection!
  
  # Reporting queries
  paymentAnalytics(
    merchantId: ID!
    dateRange: DateRangeInput!
    groupBy: GroupByOption!
  ): PaymentAnalytics!
}

type Mutation {
  createPayment(input: CreatePaymentInput!): CreatePaymentPayload!
  authorizePayment(input: AuthorizePaymentInput!): AuthorizePaymentPayload!
  capturePayment(input: CapturePaymentInput!): CapturePaymentPayload!
  refundPayment(input: RefundPaymentInput!): RefundPaymentPayload!
  
  # Batch operations
  batchCapturePayments(
    input: BatchCaptureInput!
  ): BatchCapturePayload!
}

type Subscription {
  paymentStatusChanged(
    merchantId: ID!
    statuses: [PaymentStatus!]
  ): Payment!
  
  fraudAlertTriggered(merchantId: ID!): FraudAlert!
}
```

### GraphQL Resolver Pattern

```python
class PaymentResolver:
    def __init__(self, payment_service, auth_service):
        self.payment_service = payment_service
        self.auth_service = auth_service
        
    @authenticated
    @rate_limited(max_requests=1000)
    async def create_payment(self, parent, info, input):
        # Validate permissions
        context = info.context
        if not self.auth_service.can_create_payment(context.user, input):
            raise GraphQLError("Insufficient permissions")
        
        # Input validation
        validated_input = self.validate_payment_input(input)
        
        # Create payment with dataloader for efficiency
        payment = await self.payment_service.create_payment(
            validated_input,
            context=context
        )
        
        # Prepare response
        return {
            'payment': payment,
            'success': True,
            'errors': []
        }
    
    @authenticated
    async def payment(self, parent, info, id):
        # Use dataloader to batch database queries
        return await info.context.payment_loader.load(id)
    
    @authenticated
    async def payments(self, parent, info, filter=None, sort=None, pagination=None):
        # Build query with filtering
        query = self.build_payment_query(filter, sort)
        
        # Apply pagination
        paginated_result = await self.payment_service.paginate_payments(
            query,
            pagination or {'first': 20}
        )
        
        return {
            'edges': [
                {'node': payment, 'cursor': self.encode_cursor(payment.id)}
                for payment in paginated_result.items
            ],
            'pageInfo': {
                'hasNextPage': paginated_result.has_next,
                'hasPreviousPage': paginated_result.has_previous,
                'startCursor': self.encode_cursor(paginated_result.items[0].id) if paginated_result.items else None,
                'endCursor': self.encode_cursor(paginated_result.items[-1].id) if paginated_result.items else None
            },
            'totalCount': paginated_result.total
        }
```

## 3. API Gateway Patterns

### Gateway Architecture

```python
class PaymentAPIGateway:
    def __init__(self):
        self.router = APIRouter()
        self.auth_manager = AuthenticationManager()
        self.rate_limiter = RateLimiter()
        self.circuit_breaker = CircuitBreakerManager()
        self.request_transformer = RequestTransformer()
        
    async def handle_request(self, request):
        # 1. Authentication & Authorization
        auth_result = await self.auth_manager.authenticate(request)
        if not auth_result.is_authenticated:
            return self.unauthorized_response()
        
        # 2. Rate Limiting
        rate_limit_result = await self.rate_limiter.check_limit(
            key=auth_result.client_id,
            endpoint=request.path
        )
        if rate_limit_result.exceeded:
            return self.rate_limit_response(rate_limit_result)
        
        # 3. Request Transformation
        transformed_request = self.request_transformer.transform(
            request,
            auth_context=auth_result
        )
        
        # 4. Route to appropriate service
        service = self.router.get_service(request.path)
        
        # 5. Circuit breaker protection
        circuit_breaker = self.circuit_breaker.get_breaker(service)
        
        try:
            response = await circuit_breaker.call(
                service.handle_request,
                transformed_request
            )
            
            # 6. Response transformation
            return self.transform_response(response, request)
            
        except CircuitBreakerOpen:
            return self.service_unavailable_response()
```

### Rate Limiting Strategies

```python
class AdvancedRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.strategies = {
            'token_bucket': TokenBucketStrategy(),
            'sliding_window': SlidingWindowStrategy(),
            'fixed_window': FixedWindowStrategy(),
            'adaptive': AdaptiveRateLimitStrategy()
        }
    
    async def check_limit(self, key, endpoint, client_tier='standard'):
        # Get rate limit configuration
        config = self.get_rate_limit_config(endpoint, client_tier)
        
        # Select strategy based on endpoint
        strategy = self.strategies[config.strategy]
        
        # Check multiple limit tiers
        results = []
        
        # Per-second limit
        second_result = await strategy.check_limit(
            key=f"{key}:second",
            limit=config.per_second,
            window=1
        )
        results.append(second_result)
        
        # Per-minute limit
        minute_result = await strategy.check_limit(
            key=f"{key}:minute",
            limit=config.per_minute,
            window=60
        )
        results.append(minute_result)
        
        # Per-hour limit
        hour_result = await strategy.check_limit(
            key=f"{key}:hour",
            limit=config.per_hour,
            window=3600
        )
        results.append(hour_result)
        
        # Check if any limit exceeded
        for result in results:
            if result.exceeded:
                return RateLimitResult(
                    exceeded=True,
                    limit=result.limit,
                    remaining=result.remaining,
                    reset_at=result.reset_at,
                    retry_after=result.retry_after
                )
        
        # All limits passed
        return RateLimitResult(
            exceeded=False,
            limit=config.per_second,
            remaining=min(r.remaining for r in results),
            reset_at=min(r.reset_at for r in results)
        )
    
    def get_rate_limit_config(self, endpoint, client_tier):
        configs = {
            'standard': {
                '/v1/payments': RateLimitConfig(
                    strategy='sliding_window',
                    per_second=10,
                    per_minute=100,
                    per_hour=1000
                ),
                '/v1/settlements': RateLimitConfig(
                    strategy='fixed_window',
                    per_second=5,
                    per_minute=50,
                    per_hour=500
                )
            },
            'premium': {
                '/v1/payments': RateLimitConfig(
                    strategy='token_bucket',
                    per_second=100,
                    per_minute=1000,
                    per_hour=10000
                )
            }
        }
        
        return configs.get(client_tier, {}).get(
            endpoint,
            RateLimitConfig(
                strategy='sliding_window',
                per_second=5,
                per_minute=50,
                per_hour=500
            )
        )
```

## 4. Webhook Design Patterns

### Webhook Delivery System

```python
class WebhookDeliveryService:
    def __init__(self):
        self.queue = WebhookQueue()
        self.http_client = AsyncHTTPClient()
        self.signer = WebhookSigner()
        
    async def deliver_webhook(self, event):
        # Get subscriptions for event
        subscriptions = await self.get_subscriptions(event.type)
        
        for subscription in subscriptions:
            webhook_payload = self.build_payload(event, subscription)
            
            # Queue for delivery
            await self.queue.enqueue(
                WebhookDelivery(
                    subscription=subscription,
                    payload=webhook_payload,
                    event=event,
                    attempts=0,
                    next_retry=datetime.utcnow()
                )
            )
    
    async def process_webhook_queue(self):
        while True:
            delivery = await self.queue.dequeue()
            if not delivery:
                await asyncio.sleep(1)
                continue
            
            try:
                await self.attempt_delivery(delivery)
            except Exception as e:
                await self.handle_delivery_failure(delivery, e)
    
    async def attempt_delivery(self, delivery):
        # Prepare headers
        headers = {
            'Content-Type': 'application/json',
            'X-Webhook-ID': delivery.id,
            'X-Webhook-Timestamp': str(int(time.time())),
            'X-Webhook-Event': delivery.event.type
        }
        
        # Sign payload
        signature = self.signer.sign(
            payload=delivery.payload,
            secret=delivery.subscription.secret,
            timestamp=headers['X-Webhook-Timestamp']
        )
        headers['X-Webhook-Signature'] = signature
        
        # Attempt delivery with timeout
        response = await self.http_client.post(
            url=delivery.subscription.url,
            json=delivery.payload,
            headers=headers,
            timeout=30
        )
        
        # Check response
        if response.status_code >= 200 and response.status_code < 300:
            await self.mark_delivered(delivery)
        else:
            raise WebhookDeliveryError(
                f"HTTP {response.status_code}: {response.text}"
            )
    
    async def handle_delivery_failure(self, delivery, error):
        delivery.attempts += 1
        
        if delivery.attempts >= self.max_attempts:
            await self.mark_failed(delivery, error)
            await self.notify_webhook_failure(delivery)
        else:
            # Exponential backoff
            backoff = min(
                self.initial_backoff * (2 ** (delivery.attempts - 1)),
                self.max_backoff
            )
            
            delivery.next_retry = datetime.utcnow() + timedelta(seconds=backoff)
            await self.queue.enqueue(delivery)
```

### Webhook Security

```python
class WebhookSigner:
    def sign(self, payload, secret, timestamp):
        # Create signing string
        signing_string = f"{timestamp}.{json.dumps(payload, sort_keys=True)}"
        
        # Generate HMAC-SHA256
        signature = hmac.new(
            secret.encode('utf-8'),
            signing_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return f"v1={signature}"
    
    def verify(self, payload, signature, secret, timestamp, tolerance=300):
        # Check timestamp to prevent replay attacks
        current_timestamp = int(time.time())
        if abs(current_timestamp - int(timestamp)) > tolerance:
            raise WebhookVerificationError("Timestamp too old")
        
        # Calculate expected signature
        expected_signature = self.sign(payload, secret, timestamp)
        
        # Constant-time comparison
        if not hmac.compare_digest(signature, expected_signature):
            raise WebhookVerificationError("Invalid signature")
        
        return True

class WebhookReceiver:
    def __init__(self, secret):
        self.secret = secret
        self.signer = WebhookSigner()
        
    def verify_webhook(self, request):
        # Extract headers
        signature = request.headers.get('X-Webhook-Signature')
        timestamp = request.headers.get('X-Webhook-Timestamp')
        
        if not signature or not timestamp:
            raise WebhookVerificationError("Missing required headers")
        
        # Verify signature
        self.signer.verify(
            payload=request.json,
            signature=signature,
            secret=self.secret,
            timestamp=timestamp
        )
        
        return True
```

## 5. API Error Handling Patterns

### Structured Error Responses

```python
class APIErrorHandler:
    def __init__(self):
        self.error_mappings = self._initialize_error_mappings()
        
    def handle_error(self, exception, request_id=None):
        # Map exception to API error
        api_error = self.map_exception_to_error(exception)
        
        # Build error response
        error_response = {
            'error': {
                'type': api_error.type,
                'code': api_error.code,
                'message': api_error.message,
                'details': api_error.details,
                'request_id': request_id or self.generate_request_id()
            }
        }
        
        # Add field-specific errors for validation
        if isinstance(exception, ValidationError):
            error_response['error']['field_errors'] = [
                {
                    'field': error.field,
                    'code': error.code,
                    'message': error.message
                }
                for error in exception.errors
            ]
        
        # Add retry information if applicable
        if api_error.is_retryable:
            error_response['error']['retry'] = {
                'retry_after': api_error.retry_after,
                'max_retries': api_error.max_retries
            }
        
        return Response(
            status=api_error.http_status,
            body=error_response,
            headers=self.get_error_headers(api_error)
        )
    
    def _initialize_error_mappings(self):
        return {
            ValidationError: APIError(
                type='validation_error',
                code='VALIDATION_FAILED',
                http_status=400,
                is_retryable=False
            ),
            AuthenticationError: APIError(
                type='authentication_error',
                code='AUTH_FAILED',
                http_status=401,
                is_retryable=False
            ),
            RateLimitError: APIError(
                type='rate_limit_error',
                code='RATE_LIMIT_EXCEEDED',
                http_status=429,
                is_retryable=True,
                retry_after=60
            ),
            PaymentDeclinedError: APIError(
                type='payment_error',
                code='PAYMENT_DECLINED',
                http_status=402,
                is_retryable=True
            ),
            ServiceUnavailableError: APIError(
                type='api_error',
                code='SERVICE_UNAVAILABLE',
                http_status=503,
                is_retryable=True,
                retry_after=30
            )
        }
```

## 6. API Documentation Patterns

### OpenAPI Specification

```yaml
openapi: 3.0.3
info:
  title: Payment Processing API
  version: 2.0.0
  description: |
    Secure payment processing API with support for multiple payment methods,
    currencies, and advanced fraud detection.
  
servers:
  - url: https://api.payments.example.com/v2
    description: Production server
  - url: https://sandbox.payments.example.com/v2
    description: Sandbox server

security:
  - apiKey: []
  - oauth2: [payments:read, payments:write]

paths:
  /payments:
    post:
      summary: Create a payment
      operationId: createPayment
      tags: [Payments]
      security:
        - apiKey: []
        - oauth2: [payments:write]
      
      parameters:
        - $ref: '#/components/parameters/IdempotencyKey'
      
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreatePaymentRequest'
            examples:
              card_payment:
                $ref: '#/components/examples/CardPayment'
              bank_transfer:
                $ref: '#/components/examples/BankTransfer'
      
      responses:
        201:
          description: Payment created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaymentResponse'
        
        400:
          $ref: '#/components/responses/BadRequest'
        
        401:
          $ref: '#/components/responses/Unauthorized'
        
        429:
          $ref: '#/components/responses/RateLimitExceeded'

components:
  schemas:
    CreatePaymentRequest:
      type: object
      required: [amount, currency, payment_method]
      properties:
        amount:
          type: integer
          minimum: 1
          description: Amount in smallest currency unit (e.g., cents)
          example: 1000
        
        currency:
          type: string
          pattern: '^[A-Z]{3}$'
          description: ISO 4217 currency code
          example: USD
        
        payment_method:
          oneOf:
            - $ref: '#/components/schemas/CardPaymentMethod'
            - $ref: '#/components/schemas/BankPaymentMethod'
        
        metadata:
          type: object
          additionalProperties: true
          description: Custom metadata
        
        three_d_secure:
          type: object
          properties:
            enabled:
              type: boolean
            challenge_preference:
              type: string
              enum: [no_preference, no_challenge, challenge]
```

### API Client SDKs

```python
# Python SDK Example
class PaymentAPIClient:
    def __init__(self, api_key, environment='production'):
        self.api_key = api_key
        self.base_url = self._get_base_url(environment)
        self.session = self._create_session()
        
    def create_payment(self, amount, currency, payment_method, **kwargs):
        """
        Create a new payment
        
        Args:
            amount: Payment amount in smallest currency unit
            currency: ISO 4217 currency code
            payment_method: PaymentMethod object
            **kwargs: Additional parameters (metadata, 3ds options, etc.)
            
        Returns:
            Payment object
            
        Raises:
            ValidationError: Invalid input parameters
            AuthenticationError: Invalid API key
            PaymentError: Payment processing failed
        """
        # Validate inputs
        self._validate_amount(amount)
        self._validate_currency(currency)
        
        # Build request
        request_data = {
            'amount': amount,
            'currency': currency,
            'payment_method': payment_method.to_dict(),
            **kwargs
        }
        
        # Add idempotency key if not provided
        headers = {
            'Idempotency-Key': kwargs.get('idempotency_key') or self._generate_idempotency_key()
        }
        
        # Make request with retry logic
        response = self._request_with_retry(
            'POST',
            '/payments',
            json=request_data,
            headers=headers
        )
        
        return Payment.from_response(response)
    
    def _request_with_retry(self, method, path, max_retries=3, **kwargs):
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                response = self.session.request(
                    method,
                    f"{self.base_url}{path}",
                    **kwargs
                )
                
                # Check for rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    time.sleep(min(retry_after, 300))  # Max 5 minutes
                    continue
                
                # Check for server errors (retry)
                if response.status_code >= 500:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                
                # Success or client error (don't retry)
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                last_exception = e
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
        
        raise APIError(f"Request failed after {max_retries} attempts") from last_exception
```

## Best Practices Summary

1. **API Design**
   - Use consistent resource naming
   - Implement proper versioning
   - Support idempotency for mutations
   - Provide comprehensive error responses

2. **Security**
   - Always use HTTPS
   - Implement proper authentication
   - Sign webhooks for integrity
   - Rate limit all endpoints

3. **Performance**
   - Implement caching strategies
   - Use pagination for lists
   - Support field filtering
   - Batch operations where appropriate

4. **Developer Experience**
   - Provide clear documentation
   - Include code examples
   - Offer SDKs in multiple languages
   - Maintain a changelog

5. **Reliability**
   - Implement circuit breakers
   - Use exponential backoff
   - Provide webhook retries
   - Monitor API health
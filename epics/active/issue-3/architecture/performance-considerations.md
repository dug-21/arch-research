# Payment System Performance Considerations

## Executive Summary

This document outlines critical performance considerations for payment systems, including optimization strategies, benchmarking approaches, capacity planning, and real-world performance targets. It provides actionable insights for achieving sub-100ms latency and 100,000+ TPS throughput.

## Table of Contents

1. [Performance Requirements](#performance-requirements)
2. [Latency Optimization](#latency-optimization)
3. [Throughput Scaling](#throughput-scaling)
4. [Database Performance](#database-performance)
5. [Caching Strategies](#caching-strategies)
6. [Network Optimization](#network-optimization)
7. [Performance Monitoring](#performance-monitoring)
8. [Capacity Planning](#capacity-planning)

## Performance Requirements

### Industry Benchmarks

| Metric | Good | Better | Best | Elite |
|--------|------|--------|------|-------|
| **API Latency (p50)** | < 200ms | < 100ms | < 50ms | < 25ms |
| **API Latency (p99)** | < 1s | < 500ms | < 200ms | < 100ms |
| **Authorization Time** | < 3s | < 2s | < 1s | < 500ms |
| **Throughput** | 1K TPS | 10K TPS | 50K TPS | 100K+ TPS |
| **Availability** | 99.9% | 99.95% | 99.99% | 99.995% |
| **Error Rate** | < 1% | < 0.5% | < 0.1% | < 0.01% |

### SLA Targets by Payment Type

```yaml
payment_slas:
  card_authorization:
    latency_p99: 2000ms  # Including 3DS
    latency_p50: 500ms
    success_rate: 99.5%
    
  wallet_payment:
    latency_p99: 500ms
    latency_p50: 100ms
    success_rate: 99.9%
    
  bank_transfer:
    latency_p99: 5000ms
    latency_p50: 2000ms
    success_rate: 99.0%
    
  crypto_payment:
    latency_p99: 10000ms  # Block confirmation
    latency_p50: 3000ms
    success_rate: 99.99%  # Immutable
    
  real_time_payment:
    latency_p99: 100ms
    latency_p50: 30ms
    success_rate: 99.95%
```

## Latency Optimization

### Request Path Optimization

```go
// Optimized payment processing pipeline
package payment

import (
    "context"
    "sync"
    "time"
)

type OptimizedPaymentProcessor struct {
    validator    *Validator
    fraudChecker *FraudChecker
    gateway      *PaymentGateway
    logger       *Logger
    metrics      *Metrics
}

func (p *OptimizedPaymentProcessor) ProcessPayment(
    ctx context.Context,
    req PaymentRequest,
) (*PaymentResponse, error) {
    start := time.Now()
    defer func() {
        p.metrics.RecordLatency("payment.process", time.Since(start))
    }()
    
    // Parallel validation and fraud check
    var wg sync.WaitGroup
    var validationErr, fraudErr error
    var fraudScore float64
    
    wg.Add(2)
    
    // Validation goroutine
    go func() {
        defer wg.Done()
        validationErr = p.validator.ValidateAsync(ctx, req)
    }()
    
    // Fraud check goroutine
    go func() {
        defer wg.Done()
        fraudScore, fraudErr = p.fraudChecker.CheckAsync(ctx, req)
    }()
    
    wg.Wait()
    
    // Check results
    if validationErr != nil {
        return nil, validationErr
    }
    if fraudErr != nil {
        return nil, fraudErr
    }
    if fraudScore > 0.8 {
        return nil, ErrHighFraudRisk
    }
    
    // Process payment with timeout
    paymentCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()
    
    response, err := p.gateway.ProcessWithRetry(paymentCtx, req)
    if err != nil {
        return nil, err
    }
    
    // Async operations (don't block response)
    go p.asyncPostProcessing(req, response)
    
    return response, nil
}

func (p *OptimizedPaymentProcessor) asyncPostProcessing(
    req PaymentRequest,
    resp *PaymentResponse,
) {
    // Non-blocking operations
    p.logger.LogAsync(PaymentLog{
        Request:  req,
        Response: resp,
        Time:     time.Now(),
    })
    
    p.metrics.IncrementAsync("payment.success")
    
    // Send webhook notifications
    p.notifier.NotifyAsync(resp)
}
```

### Connection Pool Optimization

```java
@Configuration
public class ConnectionPoolConfig {
    
    @Bean
    public HikariDataSource optimizedDataSource() {
        HikariConfig config = new HikariConfig();
        
        // Connection settings
        config.setJdbcUrl("jdbc:postgresql://localhost:5432/payments");
        config.setUsername("payment_user");
        config.setPassword(getSecurePassword());
        
        // Pool sizing (based on formula: connections = ((core_count * 2) + effective_spindle_count))
        int cores = Runtime.getRuntime().availableProcessors();
        config.setMaximumPoolSize(cores * 2 + 1);
        config.setMinimumIdle(cores);
        
        // Timeouts
        config.setConnectionTimeout(3000); // 3 seconds
        config.setIdleTimeout(600000); // 10 minutes
        config.setMaxLifetime(1800000); // 30 minutes
        config.setValidationTimeout(2000); // 2 seconds
        
        // Performance optimizations
        config.setAutoCommit(false);
        config.setReadOnly(false);
        config.setIsolateInternalQueries(false);
        config.setRegisterMbeans(true);
        
        // PostgreSQL specific
        config.addDataSourceProperty("cachePrepStmts", "true");
        config.addDataSourceProperty("prepStmtCacheSize", "250");
        config.addDataSourceProperty("prepStmtCacheSqlLimit", "2048");
        config.addDataSourceProperty("useServerPrepStmts", "true");
        config.addDataSourceProperty("reWriteBatchedInserts", "true");
        config.addDataSourceProperty("cacheResultSetMetadata", "true");
        config.addDataSourceProperty("cacheServerConfiguration", "true");
        config.addDataSourceProperty("elideSetAutoCommits", "true");
        config.addDataSourceProperty("maintainTimeStats", "false");
        
        return new HikariDataSource(config);
    }
    
    @Bean
    public RedisConnectionFactory optimizedRedisConnection() {
        LettuceClientConfiguration clientConfig = LettuceClientConfiguration.builder()
            .commandTimeout(Duration.ofMillis(500))
            .shutdownTimeout(Duration.ofMillis(100))
            .build();
            
        RedisStandaloneConfiguration serverConfig = new RedisStandaloneConfiguration();
        serverConfig.setHostName("localhost");
        serverConfig.setPort(6379);
        serverConfig.setDatabase(0);
        
        // Connection pooling
        GenericObjectPoolConfig poolConfig = new GenericObjectPoolConfig();
        poolConfig.setMaxTotal(100);
        poolConfig.setMaxIdle(50);
        poolConfig.setMinIdle(10);
        poolConfig.setMaxWaitMillis(2000);
        poolConfig.setTestOnBorrow(true);
        poolConfig.setTestWhileIdle(true);
        poolConfig.setTimeBetweenEvictionRunsMillis(30000);
        
        LettucePoolingClientConfiguration poolingConfig = 
            LettucePoolingClientConfiguration.builder()
                .poolConfig(poolConfig)
                .commandTimeout(Duration.ofMillis(500))
                .build();
                
        return new LettuceConnectionFactory(serverConfig, poolingConfig);
    }
}
```

### Async Processing

```python
# Async payment processing with Python
import asyncio
import aiohttp
import aiokafka
from typing import List, Dict, Any
import time

class AsyncPaymentProcessor:
    def __init__(self, config: Dict[str, Any]):
        self.session = None
        self.kafka_producer = None
        self.redis_pool = None
        self.config = config
        
    async def initialize(self):
        """Initialize async connections"""
        # HTTP session with connection pooling
        connector = aiohttp.TCPConnector(
            limit=100,
            ttl_dns_cache=300,
            enable_cleanup_closed=True
        )
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=30)
        )
        
        # Kafka producer
        self.kafka_producer = aiokafka.AIOKafkaProducer(
            bootstrap_servers=self.config['kafka_brokers'],
            compression_type='lz4',
            max_batch_size=16384,
            linger_ms=10
        )
        await self.kafka_producer.start()
        
        # Redis connection pool
        self.redis_pool = await aioredis.create_redis_pool(
            self.config['redis_url'],
            minsize=10,
            maxsize=50
        )
    
    async def process_payment_batch(
        self,
        payments: List[PaymentRequest]
    ) -> List[PaymentResponse]:
        """Process multiple payments concurrently"""
        start = time.time()
        
        # Create tasks for concurrent processing
        tasks = [
            self.process_single_payment(payment)
            for payment in payments
        ]
        
        # Process with concurrency limit
        semaphore = asyncio.Semaphore(50)  # Max 50 concurrent
        
        async def bounded_process(payment):
            async with semaphore:
                return await self.process_single_payment(payment)
        
        results = await asyncio.gather(
            *[bounded_process(p) for p in payments],
            return_exceptions=True
        )
        
        # Log batch performance
        duration = time.time() - start
        successful = sum(1 for r in results if not isinstance(r, Exception))
        
        await self.log_metrics({
            'batch_size': len(payments),
            'duration': duration,
            'success_count': successful,
            'tps': len(payments) / duration
        })
        
        return results
    
    async def process_single_payment(
        self,
        payment: PaymentRequest
    ) -> PaymentResponse:
        """Process single payment with all optimizations"""
        
        # Check cache first
        cached = await self.check_cache(payment.idempotency_key)
        if cached:
            return cached
        
        # Parallel validation and fraud check
        validation_task = self.validate_payment(payment)
        fraud_task = self.check_fraud(payment)
        
        validation_result, fraud_score = await asyncio.gather(
            validation_task,
            fraud_task
        )
        
        if not validation_result.is_valid:
            raise ValidationError(validation_result.errors)
            
        if fraud_score > 0.8:
            raise FraudError(f"High fraud score: {fraud_score}")
        
        # Process with gateway
        response = await self.call_payment_gateway(payment)
        
        # Async post-processing (don't wait)
        asyncio.create_task(self.post_process(payment, response))
        
        # Cache result
        await self.cache_result(payment.idempotency_key, response)
        
        return response
    
    async def call_payment_gateway(
        self,
        payment: PaymentRequest
    ) -> PaymentResponse:
        """Optimized gateway call with circuit breaker"""
        
        headers = {
            'Authorization': f'Bearer {self.config["api_key"]}',
            'Content-Type': 'application/json',
            'X-Idempotency-Key': payment.idempotency_key
        }
        
        payload = payment.to_gateway_format()
        
        # Retry with exponential backoff
        for attempt in range(3):
            try:
                async with self.session.post(
                    self.config['gateway_url'],
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return PaymentResponse.from_gateway(data)
                    elif response.status >= 500:
                        # Server error, retry
                        if attempt < 2:
                            await asyncio.sleep(2 ** attempt)
                            continue
                    else:
                        # Client error, don't retry
                        error_data = await response.json()
                        raise PaymentError(error_data)
                        
            except asyncio.TimeoutError:
                if attempt < 2:
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise
                
        raise PaymentError("Max retries exceeded")
    
    async def post_process(
        self,
        payment: PaymentRequest,
        response: PaymentResponse
    ):
        """Async post-processing tasks"""
        tasks = [
            self.send_to_kafka(payment, response),
            self.update_metrics(response),
            self.trigger_webhooks(response)
        ]
        
        await asyncio.gather(*tasks, return_exceptions=True)
```

## Throughput Scaling

### Horizontal Scaling Strategy

```yaml
# Kubernetes HPA configuration for auto-scaling
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: payment-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: payment-service
  minReplicas: 10
  maxReplicas: 100
  metrics:
  # CPU-based scaling
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
  
  # Memory-based scaling
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 70
  
  # Custom metrics
  - type: Pods
    pods:
      metric:
        name: payment_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
  
  - type: Pods
    pods:
      metric:
        name: payment_processing_latency_p99
      target:
        type: Value
        value: "500m"  # 500ms
  
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 30
      policies:
      - type: Percent
        value: 100  # Double pods
        periodSeconds: 30
      - type: Pods
        value: 20   # Add 20 pods max
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10   # Remove 10%
        periodSeconds: 60
```

### Load Distribution

```go
// Intelligent load balancer with health checks
package loadbalancer

import (
    "sync"
    "sync/atomic"
    "time"
)

type PaymentLoadBalancer struct {
    instances    []*ServiceInstance
    healthChecks map[string]*HealthStatus
    strategy     LoadBalancingStrategy
    mu           sync.RWMutex
}

type ServiceInstance struct {
    ID       string
    Endpoint string
    Weight   int
    Zone     string
    Metrics  *InstanceMetrics
}

type InstanceMetrics struct {
    RequestCount    uint64
    ErrorCount      uint64
    TotalLatency    uint64
    LastUpdateTime  time.Time
}

func (lb *PaymentLoadBalancer) SelectInstance(
    request PaymentRequest,
) (*ServiceInstance, error) {
    lb.mu.RLock()
    defer lb.mu.RUnlock()
    
    // Get healthy instances
    healthyInstances := lb.getHealthyInstances()
    if len(healthyInstances) == 0 {
        return nil, ErrNoHealthyInstances
    }
    
    // Apply strategy
    switch lb.strategy {
    case StrategyLeastConnections:
        return lb.selectLeastConnections(healthyInstances)
    case StrategyLowestLatency:
        return lb.selectLowestLatency(healthyInstances)
    case StrategyWeightedRoundRobin:
        return lb.selectWeightedRoundRobin(healthyInstances)
    case StrategyGeoProximity:
        return lb.selectGeoProximity(healthyInstances, request)
    default:
        return lb.selectRandom(healthyInstances)
    }
}

func (lb *PaymentLoadBalancer) selectLowestLatency(
    instances []*ServiceInstance,
) (*ServiceInstance, error) {
    var bestInstance *ServiceInstance
    var lowestLatency uint64 = ^uint64(0) // Max uint64
    
    for _, instance := range instances {
        avgLatency := lb.calculateAverageLatency(instance)
        if avgLatency < lowestLatency {
            lowestLatency = avgLatency
            bestInstance = instance
        }
    }
    
    return bestInstance, nil
}

func (lb *PaymentLoadBalancer) calculateAverageLatency(
    instance *ServiceInstance,
) uint64 {
    requestCount := atomic.LoadUint64(&instance.Metrics.RequestCount)
    if requestCount == 0 {
        return 0
    }
    
    totalLatency := atomic.LoadUint64(&instance.Metrics.TotalLatency)
    return totalLatency / requestCount
}

// Health checking
func (lb *PaymentLoadBalancer) startHealthChecks() {
    ticker := time.NewTicker(5 * time.Second)
    defer ticker.Stop()
    
    for range ticker.C {
        lb.mu.RLock()
        instances := make([]*ServiceInstance, len(lb.instances))
        copy(instances, lb.instances)
        lb.mu.RUnlock()
        
        // Check each instance concurrently
        var wg sync.WaitGroup
        for _, instance := range instances {
            wg.Add(1)
            go func(inst *ServiceInstance) {
                defer wg.Done()
                lb.checkInstanceHealth(inst)
            }(instance)
        }
        wg.Wait()
    }
}

func (lb *PaymentLoadBalancer) checkInstanceHealth(
    instance *ServiceInstance,
) {
    start := time.Now()
    
    // Perform health check
    resp, err := lb.healthCheckClient.Get(
        instance.Endpoint + "/health",
        2 * time.Second,
    )
    
    latency := time.Since(start)
    
    health := &HealthStatus{
        Healthy:    err == nil && resp.StatusCode == 200,
        LastCheck:  time.Now(),
        Latency:    latency,
        ErrorCount: 0,
    }
    
    if !health.Healthy {
        health.ErrorCount = lb.healthChecks[instance.ID].ErrorCount + 1
    }
    
    lb.mu.Lock()
    lb.healthChecks[instance.ID] = health
    lb.mu.Unlock()
}
```

### Batch Processing

```rust
// High-performance batch payment processor in Rust
use tokio::sync::{mpsc, Semaphore};
use std::sync::Arc;
use std::time::{Duration, Instant};

pub struct BatchPaymentProcessor {
    batch_size: usize,
    batch_timeout: Duration,
    max_concurrent_batches: usize,
    gateway_client: Arc<GatewayClient>,
    metrics: Arc<Metrics>,
}

impl BatchPaymentProcessor {
    pub async fn start(
        &self,
        mut receiver: mpsc::Receiver<PaymentRequest>,
    ) -> Result<(), Error> {
        let semaphore = Arc::new(Semaphore::new(self.max_concurrent_batches));
        let mut batch = Vec::with_capacity(self.batch_size);
        let mut last_flush = Instant::now();
        
        loop {
            // Collect batch
            let timeout = self.batch_timeout
                .checked_sub(last_flush.elapsed())
                .unwrap_or(Duration::from_millis(1));
                
            match tokio::time::timeout(timeout, receiver.recv()).await {
                Ok(Some(request)) => {
                    batch.push(request);
                    
                    // Process if batch is full
                    if batch.len() >= self.batch_size {
                        self.process_batch(batch.drain(..).collect(), &semaphore).await?;
                        last_flush = Instant::now();
                    }
                }
                Ok(None) => {
                    // Channel closed, process remaining
                    if !batch.is_empty() {
                        self.process_batch(batch.drain(..).collect(), &semaphore).await?;
                    }
                    break;
                }
                Err(_) => {
                    // Timeout, process current batch
                    if !batch.is_empty() {
                        self.process_batch(batch.drain(..).collect(), &semaphore).await?;
                        last_flush = Instant::now();
                    }
                }
            }
        }
        
        Ok(())
    }
    
    async fn process_batch(
        &self,
        batch: Vec<PaymentRequest>,
        semaphore: &Arc<Semaphore>,
    ) -> Result<(), Error> {
        let permit = semaphore.acquire().await?;
        let batch_size = batch.len();
        let start = Instant::now();
        
        // Process batch asynchronously
        let gateway_client = self.gateway_client.clone();
        let metrics = self.metrics.clone();
        
        tokio::spawn(async move {
            let result = gateway_client.process_batch(batch).await;
            
            // Record metrics
            let duration = start.elapsed();
            metrics.record_batch_processing(batch_size, duration, &result);
            
            // Release permit
            drop(permit);
            
            result
        });
        
        Ok(())
    }
}

// Zero-copy payment serialization
use bytes::{Bytes, BytesMut};

pub struct PaymentSerializer;

impl PaymentSerializer {
    pub fn serialize_batch(payments: &[PaymentRequest]) -> Bytes {
        let mut buffer = BytesMut::with_capacity(
            payments.len() * 256 // Estimated size per payment
        );
        
        // Write header
        buffer.extend_from_slice(&(payments.len() as u32).to_be_bytes());
        
        // Write each payment efficiently
        for payment in payments {
            Self::serialize_payment(&mut buffer, payment);
        }
        
        buffer.freeze()
    }
    
    fn serialize_payment(buffer: &mut BytesMut, payment: &PaymentRequest) {
        // Fixed-size fields for performance
        buffer.extend_from_slice(&payment.amount.to_be_bytes());
        buffer.extend_from_slice(&payment.currency.as_bytes());
        
        // Variable-size fields with length prefix
        let id_bytes = payment.id.as_bytes();
        buffer.extend_from_slice(&(id_bytes.len() as u16).to_be_bytes());
        buffer.extend_from_slice(id_bytes);
        
        // Continue for other fields...
    }
}
```

## Database Performance

### Query Optimization

```sql
-- Optimized payment query with proper indexing
-- Create covering index for common payment queries
CREATE INDEX CONCURRENTLY idx_payments_merchant_status_created 
ON payments(merchant_id, status, created_at DESC) 
INCLUDE (amount, currency, customer_id)
WHERE status IN ('pending', 'processing', 'completed');

-- Partial index for active payments only
CREATE INDEX CONCURRENTLY idx_active_payments 
ON payments(merchant_id, created_at DESC) 
WHERE status NOT IN ('cancelled', 'failed', 'refunded');

-- Index for time-based queries
CREATE INDEX CONCURRENTLY idx_payments_created_brin 
ON payments USING BRIN(created_at) 
WITH (pages_per_range = 128);

-- Optimized payment summary query
WITH merchant_daily_stats AS (
    SELECT 
        merchant_id,
        DATE(created_at) as payment_date,
        COUNT(*) FILTER (WHERE status = 'completed') as completed_count,
        COUNT(*) FILTER (WHERE status = 'failed') as failed_count,
        SUM(amount) FILTER (WHERE status = 'completed') as total_amount,
        AVG(amount) FILTER (WHERE status = 'completed') as avg_amount,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) 
            FILTER (WHERE status = 'completed') as median_amount
    FROM payments
    WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY merchant_id, DATE(created_at)
)
SELECT 
    m.merchant_id,
    m.name as merchant_name,
    COALESCE(s.completed_count, 0) as transactions,
    COALESCE(s.total_amount, 0) as revenue,
    COALESCE(s.avg_amount, 0) as avg_transaction,
    COALESCE(s.failed_count, 0) as failures,
    CASE 
        WHEN s.completed_count > 0 
        THEN ROUND(100.0 * s.failed_count / (s.completed_count + s.failed_count), 2)
        ELSE 0 
    END as failure_rate
FROM merchants m
LEFT JOIN merchant_daily_stats s ON m.id = s.merchant_id
WHERE m.active = true
ORDER BY s.total_amount DESC NULLS LAST;

-- Table partitioning for scale
CREATE TABLE payments_2024_01 PARTITION OF payments
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Automated partition creation
CREATE OR REPLACE FUNCTION create_monthly_partitions()
RETURNS void AS $$
DECLARE
    start_date date;
    end_date date;
    partition_name text;
BEGIN
    FOR i IN 0..11 LOOP
        start_date := DATE_TRUNC('month', CURRENT_DATE + (i || ' months')::interval);
        end_date := start_date + INTERVAL '1 month';
        partition_name := 'payments_' || TO_CHAR(start_date, 'YYYY_MM');
        
        -- Check if partition exists
        IF NOT EXISTS (
            SELECT 1 FROM pg_class 
            WHERE relname = partition_name
        ) THEN
            EXECUTE format(
                'CREATE TABLE %I PARTITION OF payments FOR VALUES FROM (%L) TO (%L)',
                partition_name, start_date, end_date
            );
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

### Connection Pooling

```python
# Advanced connection pooling with PgBouncer configuration
import asyncpg
import asyncio
from contextlib import asynccontextmanager

class OptimizedDatabasePool:
    def __init__(self, config):
        self.config = config
        self.read_pool = None
        self.write_pool = None
        self.analytics_pool = None
        
    async def initialize(self):
        """Create specialized connection pools"""
        
        # Write pool - smaller, longer timeouts
        self.write_pool = await asyncpg.create_pool(
            self.config['write_dsn'],
            min_size=10,
            max_size=50,
            max_queries=50000,
            max_inactive_connection_lifetime=300,
            command_timeout=10,
            server_settings={
                'jit': 'off',  # Disable JIT for OLTP
                'work_mem': '16MB',
                'maintenance_work_mem': '64MB',
            }
        )
        
        # Read pool - larger for queries
        self.read_pool = await asyncpg.create_pool(
            self.config['read_dsn'],
            min_size=20,
            max_size=100,
            max_queries=100000,
            max_inactive_connection_lifetime=600,
            command_timeout=30,
            server_settings={
                'jit': 'on',
                'work_mem': '64MB',
                'max_parallel_workers_per_gather': '4',
            }
        )
        
        # Analytics pool - optimized for complex queries
        self.analytics_pool = await asyncpg.create_pool(
            self.config['analytics_dsn'],
            min_size=5,
            max_size=20,
            max_queries=10000,
            command_timeout=300,  # 5 minutes for analytics
            server_settings={
                'jit': 'on',
                'work_mem': '256MB',
                'max_parallel_workers_per_gather': '8',
                'enable_partitionwise_join': 'on',
                'enable_partitionwise_aggregate': 'on',
            }
        )
    
    @asynccontextmanager
    async def acquire_write(self):
        """Get connection for write operations"""
        async with self.write_pool.acquire() as conn:
            async with conn.transaction():
                yield conn
    
    @asynccontextmanager
    async def acquire_read(self):
        """Get connection for read operations"""
        async with self.read_pool.acquire() as conn:
            # Set read-only transaction
            await conn.execute("SET TRANSACTION READ ONLY")
            yield conn
    
    async def execute_batch(self, queries):
        """Execute multiple queries efficiently"""
        async with self.write_pool.acquire() as conn:
            async with conn.transaction():
                # Prepare statements for better performance
                prepared = await conn.prepare(queries[0]['sql'])
                
                # Execute in batch
                await conn.executemany(
                    queries[0]['sql'],
                    [q['params'] for q in queries]
                )
```

### Write Optimization

```java
// Optimized batch insert with JDBC
@Repository
public class OptimizedPaymentRepository {
    
    private final JdbcTemplate jdbcTemplate;
    private final NamedParameterJdbcTemplate namedJdbcTemplate;
    
    @Transactional
    public void batchInsertPayments(List<Payment> payments) {
        String sql = """
            INSERT INTO payments (
                id, merchant_id, amount, currency, status,
                payment_method, customer_id, metadata, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?::jsonb, ?)
            ON CONFLICT (id) DO NOTHING
        """;
        
        jdbcTemplate.batchUpdate(sql, new BatchPreparedStatementSetter() {
            @Override
            public void setValues(PreparedStatement ps, int i) throws SQLException {
                Payment payment = payments.get(i);
                ps.setObject(1, payment.getId());
                ps.setObject(2, payment.getMerchantId());
                ps.setLong(3, payment.getAmount());
                ps.setString(4, payment.getCurrency());
                ps.setString(5, payment.getStatus().name());
                ps.setString(6, payment.getPaymentMethod());
                ps.setObject(7, payment.getCustomerId());
                ps.setString(8, payment.getMetadata().toString());
                ps.setTimestamp(9, Timestamp.from(payment.getCreatedAt()));
            }
            
            @Override
            public int getBatchSize() {
                return payments.size();
            }
        });
    }
    
    public void bulkUpdateStatuses(Map<UUID, PaymentStatus> statusUpdates) {
        String sql = """
            UPDATE payments 
            SET status = :status, 
                updated_at = CURRENT_TIMESTAMP,
                version = version + 1
            WHERE id = :id 
            AND version = :version
        """;
        
        List<MapSqlParameterSource> batchParams = statusUpdates.entrySet()
            .stream()
            .map(entry -> new MapSqlParameterSource()
                .addValue("id", entry.getKey())
                .addValue("status", entry.getValue().name())
                .addValue("version", getVersion(entry.getKey())))
            .collect(Collectors.toList());
        
        int[] updateCounts = namedJdbcTemplate.batchUpdate(sql, 
            batchParams.toArray(new MapSqlParameterSource[0]));
        
        // Check for optimistic locking failures
        for (int i = 0; i < updateCounts.length; i++) {
            if (updateCounts[i] == 0) {
                throw new OptimisticLockException(
                    "Version mismatch for payment: " + batchParams.get(i).getValue("id")
                );
            }
        }
    }
}
```

## Caching Strategies

### Multi-Level Caching

```go
// Hierarchical cache implementation
package cache

import (
    "context"
    "sync"
    "time"
)

type MultiLevelCache struct {
    l1Cache *LocalCache      // In-memory cache
    l2Cache *RedisCache      // Redis cache
    l3Cache *CDNCache        // CDN edge cache
    loader  DataLoader       // Source of truth
    
    stats   *CacheStats
    mu      sync.RWMutex
}

type CacheEntry struct {
    Key        string
    Value      interface{}
    TTL        time.Duration
    Version    int64
    LastAccess time.Time
}

func (c *MultiLevelCache) Get(
    ctx context.Context,
    key string,
) (interface{}, error) {
    // L1: Local cache (nanoseconds)
    if value, found := c.l1Cache.Get(key); found {
        c.stats.IncrementHit("l1")
        return value, nil
    }
    c.stats.IncrementMiss("l1")
    
    // L2: Redis cache (microseconds)
    value, err := c.l2Cache.Get(ctx, key)
    if err == nil && value != nil {
        c.stats.IncrementHit("l2")
        // Promote to L1
        c.l1Cache.Set(key, value, 60*time.Second)
        return value, nil
    }
    c.stats.IncrementMiss("l2")
    
    // L3: CDN cache (milliseconds)
    if c.l3Cache != nil {
        value, err = c.l3Cache.Get(ctx, key)
        if err == nil && value != nil {
            c.stats.IncrementHit("l3")
            // Promote to L1 and L2
            c.promote(ctx, key, value)
            return value, nil
        }
        c.stats.IncrementMiss("l3")
    }
    
    // Load from source
    value, err = c.loader.Load(ctx, key)
    if err != nil {
        return nil, err
    }
    
    // Populate all cache levels
    c.setAll(ctx, key, value)
    
    return value, nil
}

// Intelligent cache warming
func (c *MultiLevelCache) WarmCache(ctx context.Context) error {
    // Get frequently accessed keys
    hotKeys := c.stats.GetHotKeys(100)
    
    // Warm caches in parallel
    var wg sync.WaitGroup
    semaphore := make(chan struct{}, 10) // Limit concurrency
    
    for _, key := range hotKeys {
        wg.Add(1)
        go func(k string) {
            defer wg.Done()
            
            semaphore <- struct{}{}
            defer func() { <-semaphore }()
            
            // Load and cache
            if value, err := c.loader.Load(ctx, k); err == nil {
                c.setAll(ctx, k, value)
            }
        }(key)
    }
    
    wg.Wait()
    return nil
}

// TTL strategy based on access patterns
func (c *MultiLevelCache) calculateTTL(key string) time.Duration {
    accessCount := c.stats.GetAccessCount(key)
    lastAccess := c.stats.GetLastAccess(key)
    
    // Frequently accessed items get longer TTL
    baseTTL := 5 * time.Minute
    
    if accessCount > 1000 {
        baseTTL = 1 * time.Hour
    } else if accessCount > 100 {
        baseTTL = 30 * time.Minute
    }
    
    // Recent access extends TTL
    timeSinceAccess := time.Since(lastAccess)
    if timeSinceAccess < 1*time.Minute {
        baseTTL *= 2
    }
    
    return baseTTL
}
```

### Cache Invalidation

```python
# Smart cache invalidation
import asyncio
from typing import Set, Dict, List
import fnmatch

class CacheInvalidator:
    def __init__(self, cache_client, event_bus):
        self.cache = cache_client
        self.event_bus = event_bus
        self.invalidation_rules = {}
        self.dependency_graph = {}
        
    def register_rule(self, pattern: str, dependencies: List[str]):
        """Register cache invalidation rules"""
        self.invalidation_rules[pattern] = dependencies
        
        # Build reverse dependency graph
        for dep in dependencies:
            if dep not in self.dependency_graph:
                self.dependency_graph[dep] = set()
            self.dependency_graph[dep].add(pattern)
    
    async def invalidate(self, key: str, cascade: bool = True):
        """Invalidate cache with optional cascading"""
        # Direct invalidation
        await self.cache.delete(key)
        
        # Find dependent keys if cascading
        if cascade:
            dependent_keys = self._find_dependent_keys(key)
            
            # Batch invalidation for performance
            if dependent_keys:
                await self.cache.delete_many(list(dependent_keys))
        
        # Publish invalidation event
        await self.event_bus.publish('cache.invalidated', {
            'key': key,
            'cascade': cascade,
            'affected_keys': len(dependent_keys) if cascade else 0
        })
    
    def _find_dependent_keys(self, key: str) -> Set[str]:
        """Find all keys that depend on the given key"""
        dependent = set()
        
        # Direct dependencies
        if key in self.dependency_graph:
            dependent.update(self.dependency_graph[key])
        
        # Pattern-based dependencies
        for pattern, deps in self.invalidation_rules.items():
            if fnmatch.fnmatch(key, pattern):
                dependent.update(deps)
        
        return dependent
    
    async def smart_invalidation(self, entity_type: str, entity_id: str):
        """Intelligent invalidation based on entity changes"""
        invalidation_patterns = {
            'payment': [
                f'payment:{entity_id}',
                f'merchant:*:payments',
                f'customer:*:payments',
                'stats:payments:*'
            ],
            'merchant': [
                f'merchant:{entity_id}',
                f'merchant:{entity_id}:*',
                'merchants:list'
            ],
            'customer': [
                f'customer:{entity_id}',
                f'customer:{entity_id}:*',
                'customers:search:*'
            ]
        }
        
        patterns = invalidation_patterns.get(entity_type, [])
        
        # Find all matching keys
        keys_to_invalidate = set()
        for pattern in patterns:
            if '*' in pattern:
                # Scan for matching keys (use with caution)
                matching = await self.cache.scan_keys(pattern)
                keys_to_invalidate.update(matching)
            else:
                keys_to_invalidate.add(pattern)
        
        # Batch invalidation
        if keys_to_invalidate:
            await self.cache.delete_many(list(keys_to_invalidate))
```

### Distributed Caching

```java
// Hazelcast distributed cache configuration
@Configuration
public class DistributedCacheConfig {
    
    @Bean
    public HazelcastInstance hazelcastInstance() {
        Config config = new Config();
        
        // Network configuration
        NetworkConfig network = config.getNetworkConfig();
        network.setPort(5701);
        network.setPortAutoIncrement(true);
        
        // Enable TCP/IP clustering
        JoinConfig join = network.getJoin();
        join.getMulticastConfig().setEnabled(false);
        join.getTcpIpConfig()
            .setEnabled(true)
            .setMembers(Arrays.asList(
                "10.0.1.10:5701",
                "10.0.1.11:5701",
                "10.0.1.12:5701"
            ));
        
        // Payment cache configuration
        MapConfig paymentCacheConfig = new MapConfig("payments");
        paymentCacheConfig
            .setBackupCount(2)
            .setAsyncBackupCount(1)
            .setTimeToLiveSeconds(300)
            .setMaxIdleSeconds(600)
            .setEvictionConfig(new EvictionConfig()
                .setEvictionPolicy(EvictionPolicy.LRU)
                .setMaxSizePolicy(MaxSizePolicy.PER_NODE)
                .setSize(10000))
            .setNearCacheConfig(new NearCacheConfig()
                .setInMemoryFormat(InMemoryFormat.BINARY)
                .setInvalidateOnChange(true)
                .setTimeToLiveSeconds(60)
                .setMaxIdleSeconds(30));
        
        config.addMapConfig(paymentCacheConfig);
        
        // Merchant cache with different settings
        MapConfig merchantCacheConfig = new MapConfig("merchants");
        merchantCacheConfig
            .setBackupCount(2)
            .setTimeToLiveSeconds(3600) // 1 hour
            .setMaxIdleSeconds(1800)    // 30 minutes
            .setReadBackupData(true);
        
        config.addMapConfig(merchantCacheConfig);
        
        // Enable metrics
        config.getMetricsConfig()
            .setEnabled(true)
            .setJmxConfig(new JmxConfig().setEnabled(true));
        
        return Hazelcast.newHazelcastInstance(config);
    }
    
    @Bean
    public CacheManager cacheManager(HazelcastInstance hazelcastInstance) {
        return new HazelcastCacheManager(hazelcastInstance);
    }
}

// Cache usage with proper error handling
@Service
public class PaymentCacheService {
    
    private final HazelcastInstance hazelcast;
    private final IMap<String, Payment> paymentCache;
    private final MeterRegistry metrics;
    
    public PaymentCacheService(HazelcastInstance hazelcast, MeterRegistry metrics) {
        this.hazelcast = hazelcast;
        this.paymentCache = hazelcast.getMap("payments");
        this.metrics = metrics;
    }
    
    public Optional<Payment> getPayment(String paymentId) {
        return metrics.timer("cache.get.payment").recordCallable(() -> {
            try {
                Payment payment = paymentCache.get(paymentId);
                if (payment != null) {
                    metrics.counter("cache.hit", "cache", "payment").increment();
                    return Optional.of(payment);
                } else {
                    metrics.counter("cache.miss", "cache", "payment").increment();
                    return Optional.empty();
                }
            } catch (Exception e) {
                metrics.counter("cache.error", "cache", "payment", "operation", "get").increment();
                log.error("Cache get error for payment: " + paymentId, e);
                return Optional.empty();
            }
        });
    }
    
    public void cachePayment(Payment payment) {
        metrics.timer("cache.put.payment").record(() -> {
            try {
                paymentCache.setAsync(
                    payment.getId(),
                    payment,
                    5,
                    TimeUnit.MINUTES
                ).exceptionally(throwable -> {
                    log.error("Async cache put failed", throwable);
                    return null;
                });
            } catch (Exception e) {
                metrics.counter("cache.error", "cache", "payment", "operation", "put").increment();
                log.error("Cache put error for payment: " + payment.getId(), e);
            }
        });
    }
}
```

## Network Optimization

### HTTP/2 and gRPC

```proto
// Optimized gRPC service definition
syntax = "proto3";

package payment.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/duration.proto";

service PaymentService {
  // Unary RPC for single payment
  rpc ProcessPayment(PaymentRequest) returns (PaymentResponse);
  
  // Server streaming for bulk status updates
  rpc StreamPaymentStatus(PaymentStatusRequest) returns (stream PaymentStatus);
  
  // Client streaming for batch processing
  rpc BatchProcessPayments(stream PaymentRequest) returns (BatchPaymentResponse);
  
  // Bidirectional streaming for real-time processing
  rpc StreamProcess(stream PaymentRequest) returns (stream PaymentResponse);
}

message PaymentRequest {
  string idempotency_key = 1;
  int64 amount = 2;
  string currency = 3;
  string payment_method_id = 4;
  string merchant_id = 5;
  string customer_id = 6;
  map<string, string> metadata = 7;
  ProcessingOptions options = 8;
}

message ProcessingOptions {
  bool capture_immediately = 1;
  google.protobuf.Duration timeout = 2;
  int32 retry_attempts = 3;
  bool enable_3ds = 4;
}

message PaymentResponse {
  string payment_id = 1;
  PaymentStatus status = 2;
  int64 amount = 3;
  string currency = 4;
  google.protobuf.Timestamp created_at = 5;
  ProcessingMetrics metrics = 6;
}

message ProcessingMetrics {
  int64 gateway_latency_ms = 1;
  int64 fraud_check_latency_ms = 2;
  int64 total_latency_ms = 3;
  string gateway_used = 4;
}
```

```go
// Optimized gRPC server implementation
type paymentServer struct {
    pb.UnimplementedPaymentServiceServer
    processor *PaymentProcessor
    limiter   *rate.Limiter
    pool      *ants.Pool
}

func (s *paymentServer) ProcessPayment(
    ctx context.Context,
    req *pb.PaymentRequest,
) (*pb.PaymentResponse, error) {
    // Rate limiting
    if !s.limiter.Allow() {
        return nil, status.Error(codes.ResourceExhausted, "rate limit exceeded")
    }
    
    // Process with timeout from client
    timeout := 5 * time.Second
    if req.Options != nil && req.Options.Timeout != nil {
        timeout = req.Options.Timeout.AsDuration()
    }
    
    ctx, cancel := context.WithTimeout(ctx, timeout)
    defer cancel()
    
    // Use worker pool for processing
    resultChan := make(chan *pb.PaymentResponse, 1)
    errorChan := make(chan error, 1)
    
    err := s.pool.Submit(func() {
        result, err := s.processor.Process(ctx, req)
        if err != nil {
            errorChan <- err
        } else {
            resultChan <- result
        }
    })
    
    if err != nil {
        return nil, status.Error(codes.Internal, "worker pool exhausted")
    }
    
    select {
    case result := <-resultChan:
        return result, nil
    case err := <-errorChan:
        return nil, err
    case <-ctx.Done():
        return nil, status.Error(codes.DeadlineExceeded, "request timeout")
    }
}

// Streaming implementation for batch processing
func (s *paymentServer) BatchProcessPayments(
    stream pb.PaymentService_BatchProcessPaymentsServer,
) error {
    batch := make([]*pb.PaymentRequest, 0, 100)
    
    for {
        req, err := stream.Recv()
        if err == io.EOF {
            // Process final batch
            if len(batch) > 0 {
                response := s.processBatch(batch)
                return stream.SendAndClose(response)
            }
            return nil
        }
        if err != nil {
            return err
        }
        
        batch = append(batch, req)
        
        // Process when batch is full
        if len(batch) >= 100 {
            // Process in background, continue receiving
            go s.processBatchAsync(batch)
            batch = make([]*pb.PaymentRequest, 0, 100)
        }
    }
}
```

### Edge Computing

```typescript
// CloudFlare Workers edge payment routing
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Parse request
    const url = new URL(request.url);
    
    // Quick validation at edge
    if (request.method !== 'POST' || !url.pathname.startsWith('/api/payments')) {
      return new Response('Not Found', { status: 404 });
    }
    
    // Get payment data
    const payment = await request.json();
    
    // Route based on merchant location
    const region = await getmerchantRegion(env.KV, payment.merchant_id);
    const endpoint = selectEndpoint(region);
    
    // Add edge processing headers
    const headers = new Headers(request.headers);
    headers.set('X-Edge-Region', env.CF_REGION);
    headers.set('X-Edge-Time', new Date().toISOString());
    
    // Forward to nearest processing center
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(payment),
    });
    
    // Cache successful responses
    if (response.ok && payment.type === 'authorization') {
      const cacheKey = `auth:${payment.merchant_id}:${payment.customer_id}`;
      await env.KV.put(cacheKey, await response.text(), {
        expirationTtl: 300, // 5 minutes
      });
    }
    
    return response;
  },
};

async function selectEndpoint(region: string): string {
  const endpoints = {
    'us-east': 'https://us-east.api.payment.com',
    'us-west': 'https://us-west.api.payment.com',
    'eu': 'https://eu.api.payment.com',
    'asia': 'https://asia.api.payment.com',
  };
  
  return endpoints[region] || endpoints['us-east'];
}
```

## Performance Monitoring

### Custom Metrics

```python
# Comprehensive performance monitoring
from prometheus_client import Counter, Histogram, Gauge, Summary
import time
from functools import wraps

# Define metrics
payment_requests = Counter(
    'payment_requests_total',
    'Total payment requests',
    ['method', 'status', 'gateway']
)

payment_latency = Histogram(
    'payment_processing_duration_seconds',
    'Payment processing latency',
    ['operation', 'gateway'],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

active_payments = Gauge(
    'payment_processing_active',
    'Currently processing payments',
    ['gateway']
)

payment_amount = Summary(
    'payment_amount_dollars',
    'Payment amounts in dollars',
    ['currency', 'method']
)

gateway_errors = Counter(
    'payment_gateway_errors_total',
    'Gateway errors by type',
    ['gateway', 'error_type']
)

# Circuit breaker metrics
circuit_breaker_state = Gauge(
    'circuit_breaker_state',
    'Circuit breaker state (0=closed, 1=open, 2=half-open)',
    ['service']
)

# Performance monitoring decorator
def monitor_performance(operation: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            gateway = kwargs.get('gateway', 'unknown')
            
            # Start timing
            start_time = time.time()
            
            # Track active operations
            active_payments.labels(gateway=gateway).inc()
            
            try:
                # Execute function
                result = await func(*args, **kwargs)
                
                # Record success
                payment_requests.labels(
                    method=kwargs.get('method', 'unknown'),
                    status='success',
                    gateway=gateway
                ).inc()
                
                # Record amount if available
                if hasattr(result, 'amount'):
                    payment_amount.labels(
                        currency=result.currency,
                        method=kwargs.get('method', 'unknown')
                    ).observe(result.amount / 100)  # Convert cents to dollars
                
                return result
                
            except Exception as e:
                # Record failure
                payment_requests.labels(
                    method=kwargs.get('method', 'unknown'),
                    status='failure',
                    gateway=gateway
                ).inc()
                
                # Record error type
                error_type = type(e).__name__
                gateway_errors.labels(
                    gateway=gateway,
                    error_type=error_type
                ).inc()
                
                raise
                
            finally:
                # Record latency
                duration = time.time() - start_time
                payment_latency.labels(
                    operation=operation,
                    gateway=gateway
                ).observe(duration)
                
                # Update active count
                active_payments.labels(gateway=gateway).dec()
        
        return wrapper
    return decorator

# Usage example
class PaymentService:
    @monitor_performance('process_payment')
    async def process_payment(self, request: PaymentRequest, gateway: str):
        # Payment processing logic
        pass
```

### Real-time Dashboards

```yaml
# Grafana dashboard configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: payment-dashboard
data:
  dashboard.json: |
    {
      "dashboard": {
        "title": "Payment System Performance",
        "panels": [
          {
            "title": "Payment Request Rate",
            "targets": [
              {
                "expr": "sum(rate(payment_requests_total[5m])) by (status)"
              }
            ],
            "type": "graph"
          },
          {
            "title": "Payment Latency (p50, p95, p99)",
            "targets": [
              {
                "expr": "histogram_quantile(0.5, rate(payment_processing_duration_seconds_bucket[5m]))",
                "legendFormat": "p50"
              },
              {
                "expr": "histogram_quantile(0.95, rate(payment_processing_duration_seconds_bucket[5m]))",
                "legendFormat": "p95"
              },
              {
                "expr": "histogram_quantile(0.99, rate(payment_processing_duration_seconds_bucket[5m]))",
                "legendFormat": "p99"
              }
            ],
            "type": "graph"
          },
          {
            "title": "Gateway Error Rate",
            "targets": [
              {
                "expr": "sum(rate(payment_gateway_errors_total[5m])) by (gateway, error_type)"
              }
            ],
            "type": "graph"
          },
          {
            "title": "Active Payments by Gateway",
            "targets": [
              {
                "expr": "sum(payment_processing_active) by (gateway)"
              }
            ],
            "type": "graph"
          },
          {
            "title": "Circuit Breaker Status",
            "targets": [
              {
                "expr": "circuit_breaker_state"
              }
            ],
            "type": "stat"
          }
        ],
        "refresh": "5s",
        "time": {
          "from": "now-1h",
          "to": "now"
        }
      }
    }
```

### APM Integration

```java
// Application Performance Monitoring with Micrometer
@Configuration
public class APMConfiguration {
    
    @Bean
    public MeterRegistry meterRegistry() {
        // Composite registry for multiple backends
        CompositeMeterRegistry composite = new CompositeMeterRegistry();
        
        // Prometheus registry
        PrometheusMeterRegistry prometheus = new PrometheusMeterRegistry(
            PrometheusConfig.DEFAULT
        );
        composite.add(prometheus);
        
        // DataDog registry
        DatadogMeterRegistry datadog = new DatadogMeterRegistry(
            new DatadogConfig() {
                @Override
                public String apiKey() {
                    return System.getenv("DATADOG_API_KEY");
                }
                
                @Override
                public Duration step() {
                    return Duration.ofSeconds(10);
                }
                
                @Override
                public String get(String key) {
                    return null;
                }
            },
            Clock.SYSTEM
        );
        composite.add(datadog);
        
        // Common tags
        composite.config().commonTags(
            "application", "payment-service",
            "environment", System.getenv("ENVIRONMENT"),
            "region", System.getenv("AWS_REGION")
        );
        
        return composite;
    }
    
    @Bean
    public TimedAspect timedAspect(MeterRegistry registry) {
        return new TimedAspect(registry);
    }
    
    @Bean
    public ObservationRegistry observationRegistry() {
        ObservationRegistry registry = ObservationRegistry.create();
        
        // Add custom observation handlers
        registry.observationConfig()
            .observationHandler(new PerformanceObservationHandler())
            .observationHandler(new SecurityObservationHandler());
            
        return registry;
    }
}

// Custom performance observation
public class PerformanceObservationHandler implements ObservationHandler<Observation.Context> {
    
    @Override
    public void onStart(Observation.Context context) {
        context.put("startTime", System.nanoTime());
        context.put("startMemory", getUsedMemory());
    }
    
    @Override
    public void onStop(Observation.Context context) {
        long duration = System.nanoTime() - context.get("startTime", Long.class);
        long memoryDelta = getUsedMemory() - context.get("startMemory", Long.class);
        
        // Log slow operations
        if (duration > TimeUnit.SECONDS.toNanos(1)) {
            log.warn("Slow operation detected: {} took {}ms",
                context.getName(),
                TimeUnit.NANOSECONDS.toMillis(duration)
            );
        }
        
        // Log memory-intensive operations
        if (memoryDelta > 50 * 1024 * 1024) { // 50MB
            log.warn("Memory-intensive operation: {} used {}MB",
                context.getName(),
                memoryDelta / (1024 * 1024)
            );
        }
    }
    
    private long getUsedMemory() {
        return Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
    }
}
```

## Capacity Planning

### Load Testing

```python
# Advanced load testing with Locust
from locust import HttpUser, task, between, events
import random
import time
import json

class PaymentLoadTest(HttpUser):
    wait_time = between(0.1, 0.5)  # Aggressive testing
    
    def on_start(self):
        """Initialize test data"""
        self.payment_methods = self._create_test_payment_methods()
        self.merchants = self._get_test_merchants()
        
    @task(weight=70)
    def create_payment(self):
        """Test payment creation - most common operation"""
        payment_data = {
            "amount": random.randint(100, 100000),
            "currency": random.choice(["USD", "EUR", "GBP"]),
            "payment_method_id": random.choice(self.payment_methods),
            "merchant_id": random.choice(self.merchants),
            "metadata": {
                "order_id": f"ORD-{random.randint(100000, 999999)}",
                "customer_id": f"CUST-{random.randint(1000, 9999)}"
            }
        }
        
        with self.client.post(
            "/api/v1/payments",
            json=payment_data,
            headers={"Authorization": f"Bearer {self.token}"},
            catch_response=True
        ) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(weight=20)
    def get_payment_status(self):
        """Test payment status checks"""
        payment_id = f"pay_{random.randint(100000, 999999)}"
        
        with self.client.get(
            f"/api/v1/payments/{payment_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            catch_response=True
        ) as response:
            if response.status_code in [200, 404]:
                response.success()
            else:
                response.failure(f"Unexpected status: {response.status_code}")
    
    @task(weight=5)
    def create_refund(self):
        """Test refund creation"""
        payment_id = f"pay_{random.randint(100000, 999999)}"
        refund_data = {
            "amount": random.randint(100, 10000),
            "reason": random.choice(["duplicate", "fraudulent", "customer_request"])
        }
        
        self.client.post(
            f"/api/v1/payments/{payment_id}/refunds",
            json=refund_data,
            headers={"Authorization": f"Bearer {self.token}"}
        )
    
    @task(weight=5)
    def batch_payment_status(self):
        """Test batch operations"""
        payment_ids = [f"pay_{random.randint(100000, 999999)}" for _ in range(10)]
        
        self.client.post(
            "/api/v1/payments/batch/status",
            json={"payment_ids": payment_ids},
            headers={"Authorization": f"Bearer {self.token}"}
        )

# Custom load shape for realistic traffic patterns
class StepLoadShape(LoadTestShape):
    """
    Step load pattern:
    - Start with 100 users
    - Add 100 users every 30 seconds
    - Max 1000 users
    - Run for 10 minutes at peak
    - Ramp down
    """
    
    step_time = 30
    step_users = 100
    max_users = 1000
    peak_duration = 600  # 10 minutes
    
    def tick(self):
        run_time = self.get_run_time()
        
        if run_time < self.step_time * (self.max_users / self.step_users):
            # Ramping up
            current_step = run_time // self.step_time
            return (current_step * self.step_users, self.step_users)
        elif run_time < self.step_time * (self.max_users / self.step_users) + self.peak_duration:
            # At peak
            return (self.max_users, 0)
        else:
            # Ramping down
            down_time = run_time - (self.step_time * (self.max_users / self.step_users) + self.peak_duration)
            current_step = self.max_users - (down_time // self.step_time * self.step_users)
            if current_step > 0:
                return (current_step, -self.step_users)
            else:
                return None

# Capture detailed metrics
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, response, **kwargs):
    # Log percentiles
    if response_time > 1000:  # Log slow requests
        print(f"Slow request: {name} took {response_time}ms")
```

### Resource Calculation

```yaml
# Capacity planning calculations
capacity_model:
  # Transaction requirements
  peak_tps: 10000
  average_tps: 3000
  peak_duration: 2h
  
  # Service requirements (per instance)
  payment_service:
    tps_per_instance: 500
    cpu_per_tps: 0.002  # 2 millicores
    memory_per_tps: 2   # 2MB
    
  # Database requirements
  database:
    connections_per_tps: 0.1
    storage_per_million_txn: 50GB
    iops_per_tps: 10
    
  # Cache requirements
  cache:
    memory_per_1k_tps: 10GB
    connections_per_instance: 100
    
  # Calculated needs
  calculated:
    payment_instances: 20  # 10000 / 500
    total_cpu: 40         # 20 instances * 2 cores
    total_memory: 200GB   # 20 instances * 10GB
    db_connections: 1000  # 10000 * 0.1
    db_iops: 100000      # 10000 * 10
    cache_memory: 100GB   # 10 * 10GB
```

### Auto-scaling Configuration

```terraform
# Terraform auto-scaling configuration
resource "aws_autoscaling_group" "payment_service" {
  name                = "payment-service-asg"
  vpc_zone_identifier = var.private_subnet_ids
  target_group_arns   = [aws_lb_target_group.payment_service.arn]
  health_check_type   = "ELB"
  health_check_grace_period = 300
  
  min_size         = 10
  max_size         = 100
  desired_capacity = 20
  
  launch_template {
    id      = aws_launch_template.payment_service.id
    version = "$Latest"
  }
  
  tag {
    key                 = "Name"
    value               = "payment-service"
    propagate_at_launch = true
  }
}

# Target tracking scaling policies
resource "aws_autoscaling_policy" "payment_cpu_policy" {
  name                   = "payment-cpu-scaling"
  autoscaling_group_name = aws_autoscaling_group.payment_service.name
  policy_type            = "TargetTrackingScaling"
  
  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 60.0
  }
}

resource "aws_autoscaling_policy" "payment_requests_policy" {
  name                   = "payment-requests-scaling"
  autoscaling_group_name = aws_autoscaling_group.payment_service.name
  policy_type            = "TargetTrackingScaling"
  
  target_tracking_configuration {
    customized_metric_specification {
      metric_dimension {
        name  = "ServiceName"
        value = "payment-service"
      }
      metric_name = "RequestsPerSecond"
      namespace   = "PaymentSystem"
      statistic   = "Average"
    }
    target_value = 1000.0
  }
}

# Predictive scaling
resource "aws_autoscaling_policy" "payment_predictive_policy" {
  name                   = "payment-predictive-scaling"
  autoscaling_group_name = aws_autoscaling_group.payment_service.name
  policy_type            = "PredictiveScaling"
  
  predictive_scaling_configuration {
    mode = "ForecastAndScale"
    
    metric_specification {
      target_value = 60
      
      predefined_scaling_metric_specification {
        predefined_metric_type = "ASGAverageCPUUtilization"
      }
      
      predefined_load_metric_specification {
        predefined_metric_type = "ASGTotalCPUUtilization"
      }
    }
  }
}
```

## Performance Best Practices

### Code-Level Optimizations

1. **Minimize Allocations**
   - Use object pools for frequently created objects
   - Prefer stack allocation over heap when possible
   - Reuse buffers and byte arrays

2. **Optimize Data Structures**
   - Use appropriate collections (ArrayList vs LinkedList)
   - Consider primitive collections for performance
   - Use concurrent data structures for multi-threaded access

3. **Async Everything**
   - Never block on I/O operations
   - Use async/await patterns consistently
   - Implement proper backpressure handling

4. **Batch Operations**
   - Group database queries
   - Batch API calls to external services
   - Use bulk operations for caching

### System-Level Optimizations

1. **JVM Tuning** (for Java services)
   ```bash
   -XX:+UseG1GC
   -XX:MaxGCPauseMillis=100
   -XX:+UseStringDeduplication
   -XX:+AlwaysPreTouch
   -Xms8g -Xmx8g
   ```

2. **Kernel Tuning** (Linux)
   ```bash
   # Network optimizations
   net.core.rmem_max = 134217728
   net.core.wmem_max = 134217728
   net.ipv4.tcp_rmem = 4096 87380 134217728
   net.ipv4.tcp_wmem = 4096 65536 134217728
   
   # Connection handling
   net.ipv4.tcp_fin_timeout = 10
   net.ipv4.tcp_tw_reuse = 1
   net.core.somaxconn = 65535
   ```

3. **Container Optimization**
   - Use distroless or Alpine images
   - Multi-stage builds to minimize size
   - Proper resource limits and requests

## Conclusion

Achieving high performance in payment systems requires:

1. **Holistic Approach**: Optimize at every layer from code to infrastructure
2. **Continuous Monitoring**: Real-time visibility into system performance
3. **Proactive Scaling**: Anticipate load patterns and scale accordingly
4. **Regular Testing**: Continuous load testing and performance regression testing
5. **Iterative Improvement**: Regular performance reviews and optimizations

The strategies outlined in this document provide a foundation for building payment systems capable of handling millions of transactions with sub-second latency and high availability.
# Payment System Database Architecture Patterns

## Overview

Payment systems require specialized database architectures to handle high transaction volumes, ensure data consistency, maintain audit trails, and meet regulatory requirements.

## 1. CQRS Pattern for Payments

### Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           CQRS Architecture                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Write Side                            Read Side                     │
│  ┌─────────────┐                      ┌─────────────────┐          │
│  │   Command   │                      │     Query       │          │
│  │   Handler   │                      │    Handler      │          │
│  └──────┬──────┘                      └────────┬────────┘          │
│         │                                       │                    │
│  ┌──────▼──────┐      Events          ┌────────▼────────┐          │
│  │   Write     │──────────────────────►│     Read        │          │
│  │   Model     │                      │     Model       │          │
│  │  (MySQL)    │                      │  (PostgreSQL)   │          │
│  └─────────────┘                      └─────────────────┘          │
└─────────────────────────────────────────────────────────────────────┘
```

### Implementation

**Write Model (Optimized for Transactions)**
```sql
-- Write-optimized schema
CREATE TABLE payment_transactions (
    id UUID PRIMARY KEY,
    merchant_id UUID NOT NULL,
    amount DECIMAL(19,4) NOT NULL,
    currency CHAR(3) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    version INT NOT NULL DEFAULT 1,
    
    INDEX idx_merchant_created (merchant_id, created_at),
    INDEX idx_status (status)
) ENGINE=InnoDB;

CREATE TABLE payment_events (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    transaction_id UUID NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_data JSON NOT NULL,
    created_at TIMESTAMP NOT NULL,
    
    INDEX idx_transaction (transaction_id),
    INDEX idx_created (created_at)
) ENGINE=InnoDB;
```

**Read Model (Optimized for Queries)**
```sql
-- Read-optimized schema with denormalization
CREATE TABLE payment_summary (
    transaction_id UUID PRIMARY KEY,
    merchant_id UUID NOT NULL,
    merchant_name VARCHAR(255),
    amount DECIMAL(19,4) NOT NULL,
    currency CHAR(3) NOT NULL,
    status VARCHAR(20) NOT NULL,
    processor_name VARCHAR(100),
    card_last_four CHAR(4),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    
    -- Optimized indexes for common queries
    INDEX idx_merchant_date (merchant_id, created_at DESC),
    INDEX idx_status_date (status, created_at DESC),
    INDEX idx_amount_range (amount, created_at DESC)
) ENGINE=InnoDB;

-- Materialized views for reporting
CREATE MATERIALIZED VIEW daily_merchant_summary AS
SELECT 
    merchant_id,
    DATE(created_at) as transaction_date,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(amount) as average_amount,
    COUNT(DISTINCT currency) as currency_count
FROM payment_summary
GROUP BY merchant_id, DATE(created_at);
```

### Event Synchronization

```python
class PaymentEventProcessor:
    def process_payment_event(self, event):
        # Write to write model
        with self.write_db.transaction() as tx:
            tx.execute("""
                INSERT INTO payment_transactions 
                (id, merchant_id, amount, currency, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, event.to_write_model())
            
            # Store event
            tx.execute("""
                INSERT INTO payment_events 
                (transaction_id, event_type, event_data, created_at)
                VALUES (%s, %s, %s, %s)
            """, event.to_event_record())
        
        # Async update read model
        self.event_queue.publish(event)
    
    def update_read_model(self, event):
        # Transform for read model
        read_data = self.transform_for_read(event)
        
        # Update denormalized tables
        with self.read_db.transaction() as tx:
            tx.execute("""
                INSERT INTO payment_summary 
                (transaction_id, merchant_id, merchant_name, amount, 
                 currency, status, processor_name, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    status = VALUES(status),
                    updated_at = VALUES(updated_at)
            """, read_data)
```

## 2. Event Sourcing for Audit Compliance

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Event Sourcing Pattern                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Commands                Events                  Projections     │
│     │                      │                          │          │
│     ▼                      ▼                          ▼          │
│  ┌──────┐            ┌──────────┐            ┌──────────────┐  │
│  │Domain│───────────►│  Event   │───────────►│  Read Model  │  │
│  │Logic │            │  Store   │            │ Projections  │  │
│  └──────┘            └──────────┘            └──────────────┘  │
│                            │                                     │
│                            ▼                                     │
│                      ┌──────────┐                              │
│                      │ Snapshot │                              │
│                      │  Store   │                              │
│                      └──────────┘                              │
└─────────────────────────────────────────────────────────────────┘
```

### Event Store Schema

```sql
-- Immutable event store
CREATE TABLE payment_event_store (
    event_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    aggregate_id UUID NOT NULL,
    aggregate_type VARCHAR(50) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_version INT NOT NULL,
    event_data JSON NOT NULL,
    metadata JSON,
    created_at TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    
    -- Ensure ordering and uniqueness
    UNIQUE KEY uk_aggregate_version (aggregate_id, event_version),
    INDEX idx_aggregate_type (aggregate_id, aggregate_type),
    INDEX idx_event_type (event_type, created_at),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB ROW_FORMAT=COMPRESSED;

-- Snapshot store for performance
CREATE TABLE payment_snapshots (
    aggregate_id UUID PRIMARY KEY,
    aggregate_type VARCHAR(50) NOT NULL,
    snapshot_version INT NOT NULL,
    snapshot_data JSON NOT NULL,
    created_at TIMESTAMP NOT NULL,
    
    INDEX idx_type_version (aggregate_type, snapshot_version)
) ENGINE=InnoDB;
```

### Event Types and Structure

```python
# Event definitions
class PaymentEventTypes:
    PAYMENT_INITIATED = "payment.initiated"
    PAYMENT_AUTHORIZED = "payment.authorized"
    PAYMENT_CAPTURED = "payment.captured"
    PAYMENT_SETTLED = "payment.settled"
    PAYMENT_REFUNDED = "payment.refunded"
    PAYMENT_DISPUTED = "payment.disputed"
    PAYMENT_FAILED = "payment.failed"

# Event structure
class PaymentEvent:
    def __init__(self, aggregate_id, event_type, data, metadata=None):
        self.event_id = generate_uuid()
        self.aggregate_id = aggregate_id
        self.event_type = event_type
        self.event_data = data
        self.metadata = metadata or {}
        self.created_at = datetime.utcnow()
        self.version = self.get_next_version()
    
    def to_dict(self):
        return {
            "event_id": self.event_id,
            "aggregate_id": self.aggregate_id,
            "event_type": self.event_type,
            "event_data": self.event_data,
            "metadata": {
                **self.metadata,
                "user_id": get_current_user(),
                "ip_address": get_client_ip(),
                "request_id": get_request_id()
            },
            "version": self.version,
            "created_at": self.created_at
        }
```

## 3. Sharding Strategy for Scale

### Sharding Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Sharding Architecture                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐         Shard Router                          │
│  │   Client    │              │                                 │
│  └──────┬──────┘              │                                 │
│         │                      ▼                                 │
│         │              ┌──────────────┐                         │
│         └─────────────►│ Shard Router │                         │
│                       └──────┬───────┘                         │
│                              │                                  │
│        ┌─────────────────────┼─────────────────────┐           │
│        │                     │                     │           │
│   ┌────▼────┐         ┌─────▼────┐         ┌─────▼────┐      │
│   │ Shard 1 │         │ Shard 2  │         │ Shard 3  │      │
│   │ (0-33%) │         │ (34-66%) │         │ (67-100%)│      │
│   └─────────┘         └──────────┘         └──────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

### Sharding Strategies

**1. Merchant-based Sharding**
```python
class MerchantShardRouter:
    def __init__(self, shard_count=16):
        self.shard_count = shard_count
        self.shard_map = self._initialize_shards()
    
    def get_shard(self, merchant_id):
        # Consistent hashing for merchant
        hash_value = hashlib.md5(merchant_id.encode()).hexdigest()
        shard_index = int(hash_value[:8], 16) % self.shard_count
        return self.shard_map[shard_index]
    
    def _initialize_shards(self):
        return {
            i: f"payment_shard_{i:02d}" 
            for i in range(self.shard_count)
        }
```

**2. Time-based Sharding for Historical Data**
```sql
-- Monthly sharded tables for historical data
CREATE TABLE payment_transactions_2024_01 PARTITION OF payment_transactions
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE payment_transactions_2024_02 PARTITION OF payment_transactions
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Automated partition management
CREATE OR REPLACE FUNCTION create_monthly_partition()
RETURNS void AS $$
DECLARE
    start_date date;
    end_date date;
    partition_name text;
BEGIN
    start_date := date_trunc('month', CURRENT_DATE + interval '1 month');
    end_date := start_date + interval '1 month';
    partition_name := 'payment_transactions_' || to_char(start_date, 'YYYY_MM');
    
    EXECUTE format('CREATE TABLE IF NOT EXISTS %I PARTITION OF payment_transactions 
                    FOR VALUES FROM (%L) TO (%L)',
                    partition_name, start_date, end_date);
END;
$$ LANGUAGE plpgsql;
```

## 4. High-Performance Indexing Strategy

### Index Design for Payment Queries

```sql
-- Composite indexes for common query patterns
CREATE INDEX idx_merchant_status_date 
    ON payment_transactions(merchant_id, status, created_at DESC)
    WHERE status IN ('authorized', 'captured', 'settled');

-- Partial indexes for specific conditions
CREATE INDEX idx_pending_transactions 
    ON payment_transactions(created_at, merchant_id)
    WHERE status = 'pending';

-- Expression indexes for computed values
CREATE INDEX idx_amount_usd 
    ON payment_transactions((amount * exchange_rate))
    WHERE currency != 'USD';

-- Covering indexes for read-heavy queries
CREATE INDEX idx_reporting_coverage 
    ON payment_transactions(merchant_id, created_at DESC)
    INCLUDE (amount, currency, status, processor_id);

-- JSON indexes for flexible querying
CREATE INDEX idx_metadata_gin 
    ON payment_transactions USING gin(metadata);

-- Full-text search for transaction descriptions
CREATE INDEX idx_description_fts 
    ON payment_transactions USING gin(to_tsvector('english', description));
```

### Index Maintenance Strategy

```python
class IndexMaintenanceService:
    def analyze_index_usage(self):
        # Query to find unused indexes
        unused_indexes = self.db.query("""
            SELECT 
                schemaname,
                tablename,
                indexname,
                idx_scan,
                idx_tup_read,
                idx_tup_fetch,
                pg_size_pretty(pg_relation_size(indexrelid)) as index_size
            FROM pg_stat_user_indexes
            WHERE idx_scan = 0
            AND indexrelname NOT LIKE 'pg_toast%'
            ORDER BY pg_relation_size(indexrelid) DESC
        """)
        
        return unused_indexes
    
    def rebuild_fragmented_indexes(self):
        # Identify and rebuild fragmented indexes
        fragmented = self.db.query("""
            SELECT 
                schemaname,
                tablename,
                indexname,
                pg_stat_get_live_tuples(indexrelid) AS live_tuples,
                pg_stat_get_dead_tuples(indexrelid) AS dead_tuples
            FROM pg_stat_user_indexes
            WHERE pg_stat_get_dead_tuples(indexrelid) > 
                  pg_stat_get_live_tuples(indexrelid) * 0.2
        """)
        
        for index in fragmented:
            self.db.execute(f"REINDEX INDEX CONCURRENTLY {index.indexname}")
```

## 5. Data Retention and Archival Strategy

### Tiered Storage Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Tiered Storage Strategy                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Hot Storage (0-90 days)          Warm Storage (91-365 days)    │
│  ┌─────────────────┐              ┌──────────────────┐         │
│  │  NVMe SSD       │              │   SAS SSD        │         │
│  │  Primary DB     │              │   Archive DB     │         │
│  │  All Indexes    │              │   Key Indexes    │         │
│  └────────┬────────┘              └────────┬─────────┘         │
│           │                                 │                    │
│           └─────────────┬───────────────────┘                   │
│                         │                                        │
│                         ▼                                        │
│               Cold Storage (>365 days)                           │
│               ┌──────────────────┐                              │
│               │   Object Store   │                              │
│               │   Compressed     │                              │
│               │   Parquet Files  │                              │
│               └──────────────────┘                              │
└─────────────────────────────────────────────────────────────────┘
```

### Archival Implementation

```python
class DataArchivalService:
    def archive_old_transactions(self):
        cutoff_date = datetime.now() - timedelta(days=90)
        
        # Move to warm storage
        with self.db.transaction() as tx:
            # Create archive table if not exists
            tx.execute("""
                CREATE TABLE IF NOT EXISTS payment_transactions_archive 
                (LIKE payment_transactions INCLUDING ALL)
            """)
            
            # Move old records
            tx.execute("""
                WITH moved AS (
                    DELETE FROM payment_transactions
                    WHERE created_at < %s
                    RETURNING *
                )
                INSERT INTO payment_transactions_archive
                SELECT * FROM moved
            """, (cutoff_date,))
            
            # Create summary for quick access
            tx.execute("""
                INSERT INTO payment_summary_archive
                SELECT 
                    merchant_id,
                    DATE_TRUNC('day', created_at) as transaction_date,
                    COUNT(*) as transaction_count,
                    SUM(amount) as total_amount,
                    currency
                FROM moved
                GROUP BY merchant_id, DATE_TRUNC('day', created_at), currency
            """)
    
    def export_to_cold_storage(self):
        # Export to Parquet for long-term storage
        year_ago = datetime.now() - timedelta(days=365)
        
        query = """
            SELECT * FROM payment_transactions_archive
            WHERE created_at < %s
            ORDER BY created_at
        """
        
        # Stream results to Parquet files
        for chunk in self.db.stream_query(query, (year_ago,), chunk_size=10000):
            df = pd.DataFrame(chunk)
            
            # Partition by year/month
            for (year, month), group in df.groupby([
                df['created_at'].dt.year,
                df['created_at'].dt.month
            ]):
                filename = f"payments_{year}_{month:02d}.parquet"
                group.to_parquet(
                    f"s3://archive-bucket/payments/{year}/{filename}",
                    compression='snappy',
                    index=False
                )
```

## 6. Compliance and Audit Database Design

### Audit Trail Schema

```sql
-- Immutable audit log
CREATE TABLE payment_audit_log (
    audit_id BIGSERIAL PRIMARY KEY,
    transaction_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL,
    actor_id UUID NOT NULL,
    actor_type VARCHAR(20) NOT NULL,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    
    -- Indexes for compliance queries
    INDEX idx_transaction_audit (transaction_id, created_at DESC),
    INDEX idx_actor_audit (actor_id, created_at DESC),
    INDEX idx_action_audit (action, created_at DESC)
) WITH (fillfactor = 95);

-- PCI compliance data
CREATE TABLE pci_access_log (
    access_id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id VARCHAR(100),
    action VARCHAR(20) NOT NULL,
    result VARCHAR(20) NOT NULL,
    ip_address INET NOT NULL,
    session_id UUID,
    created_at TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    
    INDEX idx_user_access (user_id, created_at DESC),
    INDEX idx_resource_access (resource_type, resource_id, created_at DESC)
);

-- Data retention policy tracking
CREATE TABLE data_retention_log (
    retention_id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    retention_policy VARCHAR(50) NOT NULL,
    records_affected BIGINT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    execution_time INTERVAL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## Best Practices Summary

1. **Write Optimization**
   - Use minimal indexes on write-heavy tables
   - Implement bulk insert strategies
   - Consider write-ahead logging optimization

2. **Read Optimization**
   - Create covering indexes for common queries
   - Use materialized views for reporting
   - Implement read replicas for scaling

3. **Data Integrity**
   - Use database constraints appropriately
   - Implement optimistic locking with version columns
   - Maintain referential integrity across shards

4. **Performance Monitoring**
   - Track slow queries and optimize
   - Monitor index usage and bloat
   - Implement query plan caching

5. **Compliance**
   - Maintain immutable audit logs
   - Implement data retention policies
   - Ensure PCI compliance in database design
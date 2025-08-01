# Payment System Security Architecture Patterns

## Overview

Security is paramount in payment systems. This document outlines comprehensive security patterns and best practices for building secure payment architectures.

## 1. Defense in Depth Architecture

### Layered Security Model

```
┌─────────────────────────────────────────────────────────────────┐
│                    Defense in Depth Layers                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Layer 1: Perimeter Security                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  DDoS Protection │ WAF │ IDS/IPS │ Geo-blocking         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Layer 2: Network Security                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Network Segmentation │ VPN │ Private Subnets │ Firewall│   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Layer 3: Application Security                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Input Validation │ OWASP Controls │ Session Management  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Layer 4: Data Security                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Encryption │ Tokenization │ Key Management │ Masking    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Layer 5: Identity & Access                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  MFA │ RBAC │ Zero Trust │ Privileged Access Management │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Implementation Strategy

```python
class SecurityLayerManager:
    def __init__(self):
        self.layers = {
            'perimeter': PerimeterSecurity(),
            'network': NetworkSecurity(),
            'application': ApplicationSecurity(),
            'data': DataSecurity(),
            'identity': IdentityManagement()
        }
    
    def validate_request(self, request):
        # Apply security checks in order
        for layer_name, layer in self.layers.items():
            result = layer.validate(request)
            if not result.passed:
                self.log_security_event(layer_name, result)
                return SecurityResponse.blocked(result.reason)
        
        return SecurityResponse.allowed()
    
    def apply_defense_in_depth(self, transaction):
        security_context = SecurityContext()
        
        # Layer 1: Perimeter checks
        if not self.layers['perimeter'].check_rate_limit(transaction.ip):
            raise SecurityException("Rate limit exceeded")
        
        # Layer 2: Network validation
        if not self.layers['network'].validate_source(transaction):
            raise SecurityException("Invalid network source")
        
        # Layer 3: Application security
        sanitized = self.layers['application'].sanitize_input(transaction)
        
        # Layer 4: Data protection
        encrypted = self.layers['data'].encrypt_sensitive_data(sanitized)
        
        # Layer 5: Access control
        if not self.layers['identity'].authorize(transaction.user):
            raise SecurityException("Unauthorized access")
        
        return encrypted
```

## 2. Tokenization Architecture

### Comprehensive Tokenization System

```
┌─────────────────────────────────────────────────────────────────┐
│                    Tokenization Architecture                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │   Client    │      │ Tokenization │      │    Token     │  │
│  │   Request   │─────►│   Gateway    │─────►│    Vault     │  │
│  └─────────────┘      └──────┬───────┘      └──────┬───────┘  │
│                               │                      │           │
│                               ▼                      ▼           │
│                       ┌──────────────┐      ┌──────────────┐   │
│                       │   Format     │      │     HSM      │   │
│                       │ Preserving   │      │ (Hardware    │   │
│                       │   Engine     │      │  Security    │   │
│                       └──────────────┘      │   Module)    │   │
│                                             └──────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Token Generation Patterns

```python
class TokenizationService:
    def __init__(self, hsm_client):
        self.hsm = hsm_client
        self.token_vault = TokenVault()
        
    def tokenize_card(self, card_number):
        # Validate card number
        if not self.luhn_check(card_number):
            raise ValueError("Invalid card number")
        
        # Check if already tokenized
        existing_token = self.token_vault.find_token(card_number)
        if existing_token:
            return existing_token
        
        # Generate format-preserving token
        token = self.generate_format_preserving_token(card_number)
        
        # Store in vault with HSM encryption
        encrypted_pan = self.hsm.encrypt(
            card_number,
            key_id='tokenization_master_key'
        )
        
        self.token_vault.store(
            token=token,
            encrypted_pan=encrypted_pan,
            metadata={
                'created_at': datetime.utcnow(),
                'token_type': 'payment_card',
                'format': 'fps_numeric_16'
            }
        )
        
        return token
    
    def generate_format_preserving_token(self, pan):
        # Preserve BIN for routing (first 6 digits)
        bin_range = pan[:6]
        
        # Generate random token body
        token_body = self.generate_secure_random(9)
        
        # Calculate check digit
        check_digit = self.calculate_luhn_digit(bin_range + token_body)
        
        return f"{bin_range}{token_body}{check_digit}"
    
    def detokenize(self, token, auth_context):
        # Verify authorization
        if not self.authorize_detokenization(auth_context):
            self.audit_unauthorized_access(token, auth_context)
            raise SecurityException("Unauthorized detokenization attempt")
        
        # Retrieve from vault
        encrypted_pan = self.token_vault.get_encrypted_pan(token)
        if not encrypted_pan:
            raise ValueError("Token not found")
        
        # Decrypt using HSM
        pan = self.hsm.decrypt(
            encrypted_pan,
            key_id='tokenization_master_key'
        )
        
        # Audit access
        self.audit_detokenization(token, auth_context)
        
        return pan
```

### Token Vault Security

```sql
-- Token vault schema with security features
CREATE TABLE token_vault (
    token_id VARCHAR(64) PRIMARY KEY,
    token_hash VARCHAR(128) NOT NULL,
    encrypted_pan BYTEA NOT NULL,
    encryption_key_id VARCHAR(50) NOT NULL,
    token_type VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    last_accessed TIMESTAMP,
    access_count INT DEFAULT 0,
    
    -- Security indexes
    INDEX idx_token_hash (token_hash) USING hash,
    INDEX idx_created (created_at),
    INDEX idx_key_rotation (encryption_key_id, created_at)
);

-- Access control table
CREATE TABLE token_access_log (
    access_id BIGSERIAL PRIMARY KEY,
    token_id VARCHAR(64) NOT NULL,
    action VARCHAR(20) NOT NULL,
    authorized_by VARCHAR(100) NOT NULL,
    ip_address INET,
    success BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_token_access (token_id, created_at DESC),
    INDEX idx_unauthorized (success, created_at) WHERE success = false
);
```

## 3. Encryption and Key Management

### Hierarchical Key Management

```
┌─────────────────────────────────────────────────────────────────┐
│                  Key Management Hierarchy                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌──────────────────┐                         │
│                    │  Master Key      │                         │
│                    │  (HSM Storage)   │                         │
│                    └────────┬─────────┘                         │
│                             │                                    │
│           ┌─────────────────┴─────────────────┐                │
│           │                                   │                 │
│    ┌──────▼──────┐                   ┌───────▼──────┐         │
│    │   KEK       │                   │    KEK       │         │
│    │ (Key Encryption                 │  (Database)  │         │
│    │    Key)     │                   └───────┬──────┘         │
│    └──────┬──────┘                           │                 │
│           │                                   │                 │
│    ┌──────▼──────┐                   ┌───────▼──────┐         │
│    │   DEK       │                   │    DEK       │         │
│    │ (Data Encryption                │  (Column)    │         │
│    │    Keys)    │                   └──────────────┘         │
│    └─────────────┘                                             │
└─────────────────────────────────────────────────────────────────┘
```

### Encryption Implementation

```python
class EncryptionService:
    def __init__(self, hsm_client, key_manager):
        self.hsm = hsm_client
        self.key_manager = key_manager
        self.cache = EncryptionKeyCache()
    
    def encrypt_sensitive_data(self, data, data_type):
        # Get appropriate DEK for data type
        dek = self.get_data_encryption_key(data_type)
        
        # Generate unique IV for each encryption
        iv = os.urandom(16)
        
        # Encrypt data
        cipher = Cipher(
            algorithms.AES(dek),
            modes.GCM(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        ciphertext = encryptor.update(data.encode()) + encryptor.finalize()
        
        # Return encrypted data with metadata
        return {
            'ciphertext': base64.b64encode(ciphertext).decode(),
            'iv': base64.b64encode(iv).decode(),
            'tag': base64.b64encode(encryptor.tag).decode(),
            'key_id': dek.key_id,
            'algorithm': 'AES-256-GCM',
            'version': '1.0'
        }
    
    def get_data_encryption_key(self, data_type):
        # Check cache first
        cached_key = self.cache.get(data_type)
        if cached_key and not cached_key.is_expired():
            return cached_key
        
        # Get KEK from HSM
        kek = self.hsm.get_key_encryption_key()
        
        # Retrieve or generate DEK
        dek_encrypted = self.key_manager.get_dek(data_type)
        if not dek_encrypted:
            # Generate new DEK
            dek = os.urandom(32)  # 256-bit key
            dek_encrypted = self.hsm.wrap_key(dek, kek)
            self.key_manager.store_dek(data_type, dek_encrypted)
        
        # Unwrap DEK
        dek = self.hsm.unwrap_key(dek_encrypted, kek)
        
        # Cache for performance
        self.cache.set(data_type, dek, ttl=3600)
        
        return dek
    
    def rotate_keys(self):
        """Automated key rotation process"""
        rotation_log = []
        
        for data_type in self.key_manager.get_all_data_types():
            old_dek_info = self.key_manager.get_dek_info(data_type)
            
            # Generate new DEK
            new_dek = os.urandom(32)
            kek = self.hsm.get_key_encryption_key()
            new_dek_encrypted = self.hsm.wrap_key(new_dek, kek)
            
            # Store new key
            self.key_manager.store_dek(
                data_type, 
                new_dek_encrypted,
                version=old_dek_info.version + 1
            )
            
            # Re-encrypt data in background
            self.queue_reencryption_job(data_type, old_dek_info, new_dek)
            
            rotation_log.append({
                'data_type': data_type,
                'old_version': old_dek_info.version,
                'new_version': old_dek_info.version + 1,
                'timestamp': datetime.utcnow()
            })
        
        return rotation_log
```

## 4. API Security Patterns

### API Gateway Security

```python
class APISecurityGateway:
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.auth_manager = AuthenticationManager()
        self.validator = RequestValidator()
        self.encryptor = PayloadEncryptor()
    
    def process_request(self, request):
        # 1. Rate limiting
        if not self.rate_limiter.check_limit(request):
            return Response(status=429, body="Rate limit exceeded")
        
        # 2. Authentication
        auth_result = self.auth_manager.authenticate(request)
        if not auth_result.is_authenticated:
            return Response(status=401, body="Unauthorized")
        
        # 3. Authorization
        if not self.authorize_endpoint(auth_result.principal, request.endpoint):
            return Response(status=403, body="Forbidden")
        
        # 4. Input validation
        validation_result = self.validator.validate(request)
        if not validation_result.is_valid:
            return Response(status=400, body=validation_result.errors)
        
        # 5. Request signing verification
        if not self.verify_request_signature(request):
            return Response(status=401, body="Invalid signature")
        
        # 6. Decrypt payload if needed
        if request.is_encrypted:
            request.body = self.encryptor.decrypt(request.body)
        
        return request
    
    def verify_request_signature(self, request):
        """Verify HMAC signature for request integrity"""
        expected_signature = self.calculate_signature(
            method=request.method,
            path=request.path,
            body=request.body,
            timestamp=request.headers.get('X-Timestamp'),
            api_key=request.headers.get('X-API-Key')
        )
        
        provided_signature = request.headers.get('X-Signature')
        
        # Constant-time comparison to prevent timing attacks
        return hmac.compare_digest(expected_signature, provided_signature)
    
    def calculate_signature(self, method, path, body, timestamp, api_key):
        # Get secret for API key
        secret = self.get_api_secret(api_key)
        
        # Create signing string
        signing_string = f"{method}\\n{path}\\n{timestamp}\\n{body}"
        
        # Calculate HMAC-SHA256
        signature = hmac.new(
            secret.encode(),
            signing_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return signature
```

### OAuth 2.0 Implementation

```python
class OAuth2Provider:
    def __init__(self):
        self.token_store = TokenStore()
        self.client_store = ClientStore()
        
    def handle_token_request(self, request):
        grant_type = request.form.get('grant_type')
        
        if grant_type == 'client_credentials':
            return self.client_credentials_flow(request)
        elif grant_type == 'authorization_code':
            return self.authorization_code_flow(request)
        else:
            return self.error_response('unsupported_grant_type')
    
    def client_credentials_flow(self, request):
        # Authenticate client
        client_id = request.form.get('client_id')
        client_secret = request.form.get('client_secret')
        
        client = self.authenticate_client(client_id, client_secret)
        if not client:
            return self.error_response('invalid_client')
        
        # Check requested scopes
        requested_scopes = request.form.get('scope', '').split()
        allowed_scopes = self.validate_scopes(client, requested_scopes)
        
        # Generate access token
        access_token = self.generate_access_token(
            client_id=client_id,
            scopes=allowed_scopes,
            token_type='client_credentials'
        )
        
        # Store token
        self.token_store.store(access_token)
        
        return {
            'access_token': access_token.token,
            'token_type': 'Bearer',
            'expires_in': 3600,
            'scope': ' '.join(allowed_scopes)
        }
    
    def generate_access_token(self, client_id, scopes, token_type):
        # Create JWT token
        payload = {
            'iss': 'payment-system',
            'sub': client_id,
            'aud': 'payment-api',
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow(),
            'jti': str(uuid.uuid4()),
            'scopes': scopes,
            'token_type': token_type
        }
        
        # Sign with private key
        token = jwt.encode(
            payload,
            self.get_private_key(),
            algorithm='RS256'
        )
        
        return AccessToken(
            token=token,
            client_id=client_id,
            scopes=scopes,
            expires_at=payload['exp']
        )
```

## 5. Zero Trust Architecture

### Zero Trust Implementation

```
┌─────────────────────────────────────────────────────────────────┐
│                     Zero Trust Architecture                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │   Policy    │     │   Identity   │     │   Device     │    │
│  │   Engine    │────►│  Verification │────►│   Trust      │    │
│  └─────────────┘     └──────────────┘     └──────────────┘    │
│         │                                           │            │
│         ▼                                           ▼            │
│  ┌─────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │  Continuous │     │   Micro-     │     │   Encrypted  │    │
│  │ Verification│────►│ Segmentation │────►│   Channels   │    │
│  └─────────────┘     └──────────────┘     └──────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Zero Trust Service Mesh

```python
class ZeroTrustServiceMesh:
    def __init__(self):
        self.policy_engine = PolicyEngine()
        self.identity_provider = IdentityProvider()
        self.trust_evaluator = TrustEvaluator()
        
    def authorize_service_call(self, source_service, target_service, context):
        # Never trust, always verify
        trust_score = self.evaluate_trust(source_service, context)
        
        # Check if communication is allowed
        policy = self.policy_engine.get_policy(source_service, target_service)
        
        if not policy.is_allowed:
            return AuthorizationResult.denied("Policy violation")
        
        # Verify identity
        identity = self.identity_provider.verify_service_identity(source_service)
        if not identity.is_valid:
            return AuthorizationResult.denied("Invalid identity")
        
        # Check trust level requirements
        if trust_score < policy.required_trust_level:
            return AuthorizationResult.denied("Insufficient trust level")
        
        # Generate short-lived token for this specific call
        token = self.generate_service_token(
            source=source_service,
            target=target_service,
            expiry=datetime.utcnow() + timedelta(minutes=5)
        )
        
        return AuthorizationResult.allowed(token)
    
    def evaluate_trust(self, service, context):
        factors = {
            'identity_confidence': self.check_identity_confidence(service),
            'behavior_score': self.analyze_behavior(service),
            'security_posture': self.assess_security_posture(service),
            'network_context': self.evaluate_network_context(context),
            'time_based_risk': self.calculate_time_risk(context)
        }
        
        # Weighted trust score
        weights = {
            'identity_confidence': 0.3,
            'behavior_score': 0.25,
            'security_posture': 0.25,
            'network_context': 0.1,
            'time_based_risk': 0.1
        }
        
        trust_score = sum(
            factors[factor] * weight 
            for factor, weight in weights.items()
        )
        
        return trust_score
```

## 6. Fraud Detection Security Patterns

### Real-time Fraud Detection Architecture

```python
class FraudDetectionEngine:
    def __init__(self):
        self.ml_models = MLModelManager()
        self.rule_engine = FraudRuleEngine()
        self.velocity_checker = VelocityChecker()
        self.behavior_analyzer = BehaviorAnalyzer()
        
    def assess_transaction_risk(self, transaction):
        # Parallel risk assessment
        risk_factors = {}
        
        # 1. ML-based risk scoring
        ml_features = self.extract_ml_features(transaction)
        risk_factors['ml_score'] = self.ml_models.predict_fraud_probability(ml_features)
        
        # 2. Rule-based checks
        rule_violations = self.rule_engine.check_rules(transaction)
        risk_factors['rule_score'] = len(rule_violations) / self.rule_engine.total_rules
        
        # 3. Velocity analysis
        velocity_results = self.velocity_checker.analyze(transaction)
        risk_factors['velocity_score'] = velocity_results.risk_score
        
        # 4. Behavioral analysis
        behavior_score = self.behavior_analyzer.analyze_transaction(
            transaction.user_id, 
            transaction
        )
        risk_factors['behavior_score'] = behavior_score
        
        # 5. Device fingerprinting
        device_risk = self.analyze_device_risk(transaction.device_info)
        risk_factors['device_score'] = device_risk
        
        # Calculate composite risk score
        composite_score = self.calculate_composite_score(risk_factors)
        
        return FraudAssessment(
            risk_score=composite_score,
            risk_factors=risk_factors,
            recommended_action=self.determine_action(composite_score),
            explanation=self.generate_explanation(risk_factors)
        )
    
    def extract_ml_features(self, transaction):
        return {
            # Transaction features
            'amount': transaction.amount,
            'amount_zscore': self.calculate_amount_zscore(transaction),
            'currency': transaction.currency,
            'merchant_category': transaction.merchant.category,
            
            # Time features
            'hour_of_day': transaction.timestamp.hour,
            'day_of_week': transaction.timestamp.weekday(),
            'is_weekend': transaction.timestamp.weekday() >= 5,
            'time_since_last_transaction': self.time_since_last(transaction.user_id),
            
            # Location features
            'distance_from_last': self.calculate_distance(transaction),
            'is_new_location': self.is_new_location(transaction),
            'country_risk_score': self.get_country_risk(transaction.country),
            
            # User behavior features
            'transaction_frequency': self.get_user_frequency(transaction.user_id),
            'average_transaction_amount': self.get_user_average(transaction.user_id),
            'merchant_familiarity': self.get_merchant_familiarity(transaction)
        }
```

## 7. Secure Communication Patterns

### mTLS Implementation

```python
class MutualTLSManager:
    def __init__(self):
        self.cert_store = CertificateStore()
        self.ca_bundle = self.load_ca_bundle()
        
    def establish_mtls_connection(self, target_service):
        # Load client certificate and key
        client_cert = self.cert_store.get_client_certificate()
        client_key = self.cert_store.get_client_key()
        
        # Create SSL context
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        
        # Load trusted CAs
        context.load_verify_locations(cadata=self.ca_bundle)
        
        # Load client certificate
        context.load_cert_chain(
            certfile=client_cert,
            keyfile=client_key
        )
        
        # Set strong cipher suites
        context.set_ciphers(
            'ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS'
        )
        
        # Minimum TLS version
        context.minimum_version = ssl.TLSVersion.TLSv1_3
        
        return context
    
    def verify_client_certificate(self, cert_chain):
        # Extract client certificate
        client_cert = cert_chain[0]
        
        # Verify certificate chain
        try:
            # Check certificate validity
            store_ctx = X509StoreContext(self.ca_store, client_cert)
            store_ctx.verify_certificate()
            
            # Additional checks
            self.verify_certificate_constraints(client_cert)
            self.check_certificate_revocation(client_cert)
            
            # Extract and verify client identity
            client_identity = self.extract_client_identity(client_cert)
            
            return CertificateValidation(
                is_valid=True,
                client_identity=client_identity
            )
            
        except Exception as e:
            return CertificateValidation(
                is_valid=False,
                error=str(e)
            )
```

## 8. Security Monitoring and Incident Response

### Security Event Monitoring

```python
class SecurityMonitoringService:
    def __init__(self):
        self.event_processor = SecurityEventProcessor()
        self.alert_manager = AlertManager()
        self.incident_handler = IncidentHandler()
        
    def monitor_security_events(self):
        # Real-time event processing
        event_stream = self.get_security_event_stream()
        
        for event in event_stream:
            # Correlate events
            correlated_events = self.correlate_events(event)
            
            # Detect anomalies
            if self.is_security_anomaly(correlated_events):
                self.handle_security_incident(correlated_events)
            
            # Check for specific patterns
            self.check_attack_patterns(event)
    
    def check_attack_patterns(self, event):
        patterns = {
            'brute_force': self.detect_brute_force,
            'sql_injection': self.detect_sql_injection,
            'rate_limit_abuse': self.detect_rate_limit_abuse,
            'suspicious_api_usage': self.detect_api_abuse,
            'data_exfiltration': self.detect_data_exfiltration
        }
        
        for pattern_name, detector in patterns.items():
            if detector(event):
                self.trigger_security_alert(pattern_name, event)
    
    def handle_security_incident(self, events):
        # Create incident
        incident = self.incident_handler.create_incident(events)
        
        # Automated response
        if incident.severity >= IncidentSeverity.HIGH:
            # Block suspicious IPs
            self.block_suspicious_sources(incident)
            
            # Disable compromised accounts
            self.disable_affected_accounts(incident)
            
            # Increase security monitoring
            self.escalate_monitoring_level()
        
        # Notify security team
        self.alert_manager.send_incident_alert(incident)
        
        # Start forensic data collection
        self.collect_forensic_data(incident)
```

## Best Practices Summary

1. **Defense in Depth**
   - Implement multiple security layers
   - No single point of failure
   - Regular security assessments

2. **Data Protection**
   - Always encrypt sensitive data
   - Use tokenization for PCI compliance
   - Implement proper key management

3. **Access Control**
   - Implement least privilege principle
   - Use strong authentication (MFA)
   - Regular access reviews

4. **Monitoring and Response**
   - Real-time security monitoring
   - Automated incident response
   - Regular security drills

5. **Compliance**
   - PCI-DSS compliance
   - GDPR/privacy regulations
   - Regular compliance audits
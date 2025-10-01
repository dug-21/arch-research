# AIDPS v2.0: External Control Plane Architecture
## Deterministic, ML-Enabled Guardrails Outside Agent Control

**Document Date:** October 1, 2025
**Version:** 2.0
**Status:** Architecture Specification
**Classification:** Enterprise Security Architecture - External Control Plane
**Author:** Control Plane Architect (Mesh Swarm)

---

## Executive Summary

This document specifies the **External Control Plane** architecture for AIDPS v2.0—a deterministic, ML-enabled guardrail system that sits **OUTSIDE agent control** and acts as the authoritative safety boundary for agentic deployments.

### The Core Innovation

**AIDPS v2.0 separates agent execution from safety verification through an external, agent-inaccessible control plane that uses deterministic rules + ML scoring (NOT reasoning LLMs) to guarantee deployment safety.**

### Critical Design Principles

1. **Outside Agent Control:** Agents CANNOT modify, bypass, or manipulate the control plane
2. **Deterministic Core:** Same inputs → always same outputs (no LLM hallucinations)
3. **ML-Enabled, Not LLM-Reasoning:** Neural networks for scoring/classification, NOT for decision-making
4. **Kubernetes Integration:** Inject verification into K8s control plane itself
5. **CI/CD Integration:** Inject into pipeline control plane (GitHub Actions, GitLab, etc.)
6. **Shopping Cart Model:** Agents declare intent, platform approves/rejects deterministically

### Architecture at a Glance

```
┌─────────────────────────────────────────────────────────┐
│  AGENT LAYER (Potentially Compromised)                  │
│  - AI agents with tool access                           │
│  - Can request deployments via MCP/API                  │
│  - CANNOT access control plane internals                │
│  - All actions go through verification gate             │
└─────────────────────────────────────────────────────────┘
                    ↓ (Intent Declaration)
┌─────────────────────────────────────────────────────────┐
│  EXTERNAL CONTROL PLANE (Outside Agent Control)         │
├─────────────────────────────────────────────────────────┤
│  LAYER 1: VERIFICATION GATE (Deterministic)             │
│  - Intent parser (deterministic rules)                  │
│  - ML risk scorer (neural net, not LLM)                 │
│  - Rule engine (deterministic policy checks)            │
│  - Historical pattern matcher (deterministic)           │
│  - AGENTS CANNOT MODIFY THIS LAYER                      │
├─────────────────────────────────────────────────────────┤
│  LAYER 2: TEST VALIDATION (Deterministic + ML)         │
│  - Signed baseline tests (immutable)                    │
│  - Isolated test execution (platform-controlled)        │
│  - Mutation testing (anti-gaming)                       │
│  - Coverage analysis (deterministic thresholds)         │
│  - AGENTS CANNOT FAKE TEST RESULTS                      │
├─────────────────────────────────────────────────────────┤
│  LAYER 3: EXECUTION AUTHORIZATION (Deterministic)       │
│  - OPA policy engine (deterministic rules)              │
│  - Shopping cart approval workflow                      │
│  - Multi-stakeholder sign-off                           │
│  - AGENTS CANNOT BYPASS APPROVAL                        │
└─────────────────────────────────────────────────────────┘
                    ↓ (Approved Actions Only)
┌─────────────────────────────────────────────────────────┐
│  EXECUTION LAYER (Kubernetes + CI/CD)                   │
│  - K8s admission controllers enforce controls           │
│  - CI/CD pipelines validate intent signatures           │
│  - Only executes APPROVED, VERIFIED actions             │
│  - AGENTS CANNOT EXECUTE WITHOUT APPROVAL               │
└─────────────────────────────────────────────────────────┘
```

---

## Part I: Layered Architecture - Agent Layer vs Control Plane

### 1.1 Trust Boundaries and Security Zones

**Critical Principle:** The control plane MUST assume agents are adversarial or compromised.

```
┌─────────────────────────────────────────────────────────┐
│ TRUST ZONE 0: UNTRUSTED (Agent Execution)              │
├─────────────────────────────────────────────────────────┤
│ Assumptions:                                            │
│ - Agents may be malicious, buggy, or compromised       │
│ - Agents will try to bypass controls                    │
│ - Agents will try to fake test results                  │
│ - Agents CANNOT be trusted with credentials             │
│                                                         │
│ Security Posture:                                       │
│ - Zero trust: Verify every action                      │
│ - Least privilege: Minimal capabilities                │
│ - Isolation: Sandboxed execution environment           │
│ - Monitoring: All actions logged immutably             │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ TRUST BOUNDARY: API Gateway (Strict Validation)        │
├─────────────────────────────────────────────────────────┤
│ - Cryptographic authentication (mTLS, signed JWTs)     │
│ - Rate limiting (prevent DoS)                          │
│ - Input sanitization (prevent injection attacks)       │
│ - Schema validation (only valid intent formats)        │
│ - AGENTS SUBMIT INTENTS, NOT COMMANDS                  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ TRUST ZONE 1: CONTROL PLANE (Deterministic Logic)      │
├─────────────────────────────────────────────────────────┤
│ Assumptions:                                            │
│ - Control plane code is trusted (code-reviewed)        │
│ - Control plane is hermetically sealed                 │
│ - No agent can modify control plane logic              │
│ - Control plane has HSM-backed signing keys            │
│                                                         │
│ Security Posture:                                       │
│ - Immutable infrastructure (containers)                │
│ - No direct network access from agent layer           │
│ - All state changes logged and signed                  │
│ - Multi-party approval for control plane changes       │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ TRUST ZONE 2: EXECUTION PLATFORM (K8s, CI/CD)         │
├─────────────────────────────────────────────────────────┤
│ - Executes ONLY approved intents                       │
│ - Validates signatures on all artifacts                │
│ - Enforces RBAC/network policies                       │
│ - Monitors for policy violations                       │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Component Isolation

**Key Principle:** Physical and logical separation between agent and control plane components.

```yaml
# Network Topology
networks:
  agent_network:
    subnet: 10.0.1.0/24
    firewall_rules:
      - DENY: Direct access to control_plane_network
      - DENY: Direct access to execution_platform_network
      - ALLOW: HTTPS to api_gateway only (port 443)

  control_plane_network:
    subnet: 10.0.2.0/24
    firewall_rules:
      - DENY: ALL inbound from agent_network
      - ALLOW: Inbound from api_gateway only
      - ALLOW: Outbound to execution_platform (for orchestration)

  execution_platform_network:
    subnet: 10.0.3.0/24
    firewall_rules:
      - ALLOW: Inbound from control_plane_network only
      - DENY: ALL inbound from agent_network

# Kubernetes Namespace Isolation
apiVersion: v1
kind: Namespace
metadata:
  name: aidps-control-plane
  labels:
    security-zone: "trust-zone-1"
    agent-access: "deny"
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-agent-access
  namespace: aidps-control-plane
spec:
  podSelector: {}
  policyTypes:
    - Ingress
  ingress:
    # Only API gateway can talk to control plane
    - from:
        - namespaceSelector:
            matchLabels:
              name: aidps-api-gateway
```

---

## Part II: Kubernetes Integration - Injecting Controls into K8s

### 2.1 Custom Resource Definitions (CRDs)

**Pattern:** Define agent intents as Kubernetes resources that MUST be approved before execution.

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: agentintents.aidps.io
spec:
  group: aidps.io
  names:
    kind: AgentIntent
    plural: agentintents
    singular: agentintent
    shortNames:
      - intent
  scope: Namespaced
  versions:
    - name: v2
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          required:
            - spec
          properties:
            spec:
              type: object
              required:
                - agentId
                - primaryObjective
                - requestedActions
              properties:
                # Agent Identity
                agentId:
                  type: string
                  pattern: '^agent-[a-z0-9]{8}$'

                # What agent wants to do
                primaryObjective:
                  type: string
                  maxLength: 500

                # Specific actions requested
                requestedActions:
                  type: object
                  properties:
                    codeModification:
                      type: object
                      properties:
                        scope:
                          type: string
                          description: "File path patterns (e.g., src/auth/**)"
                        intent:
                          type: string
                          description: "What code change is intended"

                    testExecution:
                      type: object
                      properties:
                        scope:
                          type: string
                        minimumCoverage:
                          type: number
                          minimum: 0
                          maximum: 100

                    deployment:
                      type: object
                      properties:
                        environment:
                          type: string
                          enum: ["dev", "staging", "production"]
                        services:
                          type: array
                          items:
                            type: string

                    resourceProvisioning:
                      type: object
                      properties:
                        resourceType:
                          type: string
                          enum: ["database", "cache", "storage", "compute"]
                        tier:
                          type: string
                          enum: ["dev", "staging", "production"]

                # Constraints (safety boundaries)
                constraints:
                  type: object
                  properties:
                    mustNotModify:
                      type: array
                      items:
                        type: string
                      description: "File patterns agent MUST NOT touch"

                    requiresApproval:
                      type: boolean
                      description: "Does this need human approval?"

                    timeToLive:
                      type: string
                      pattern: '^\d+[hm]$'
                      description: "Intent expires after this duration"

            status:
              type: object
              properties:
                # Verification Results
                verificationPhase:
                  type: string
                  enum:
                    - "Pending"
                    - "Verifying"
                    - "Approved"
                    - "Rejected"
                    - "Expired"

                verificationResult:
                  type: object
                  properties:
                    neuralScore:
                      type: number
                      minimum: 0
                      maximum: 1
                      description: "ML risk score (0=safe, 1=risky)"

                    riskLevel:
                      type: string
                      enum: ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

                    decision:
                      type: string
                      enum: ["APPROVED", "REJECTED", "REQUIRES_APPROVAL"]

                    reason:
                      type: string
                      description: "Why this decision was made"

                    conditions:
                      type: array
                      items:
                        type: string
                      description: "Conditions that must be met (e.g., 'Must pass 80% coverage')"

                # Test Results (populated after test execution)
                testResults:
                  type: object
                  properties:
                    baseline_regression_passed:
                      type: boolean
                    new_tests_created:
                      type: integer
                    coverage_percent:
                      type: number
                    mutation_score:
                      type: number
                    security_scan_passed:
                      type: boolean

                # Approval Trail
                approvals:
                  type: array
                  items:
                    type: object
                    properties:
                      approver:
                        type: string
                      role:
                        type: string
                        enum: ["tech_lead", "sre", "security_engineer"]
                      timestamp:
                        type: string
                        format: date-time
                      decision:
                        type: string
                        enum: ["approved", "rejected"]

                # Execution Status
                executionStatus:
                  type: string
                  enum:
                    - "NotStarted"
                    - "Executing"
                    - "Completed"
                    - "Failed"
                    - "RolledBack"
```

**Example Intent Submission:**

```yaml
apiVersion: aidps.io/v2
kind: AgentIntent
metadata:
  name: oauth2-deployment-intent
  namespace: production
spec:
  agentId: "agent-xyz12345"
  primaryObjective: "Add OAuth2 authentication to user-service API"

  requestedActions:
    codeModification:
      scope: "src/auth/**"
      intent: "Implement OAuth2 with JWT tokens"

    testExecution:
      scope: "tests/auth/**"
      minimumCoverage: 85

    deployment:
      environment: "staging"
      services:
        - "user-service"

    resourceProvisioning:
      resourceType: "database"
      tier: "staging"

  constraints:
    mustNotModify:
      - "src/billing/**"
      - "src/payments/**"
    requiresApproval: false  # Low-risk staging deployment
    timeToLive: "24h"

status:
  # Control plane populates this (agent CANNOT modify)
  verificationPhase: "PendingVerification"
```

### 2.2 Admission Controllers - The K8s Enforcement Point

**Pattern:** Kubernetes admission webhooks intercept ALL resource modifications and enforce AIDPS controls.

```go
// AIDPS Admission Controller
package main

import (
    "encoding/json"
    "net/http"
    admissionv1 "k8s.io/api/admission/v1"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

type AIDPSAdmissionController struct {
    intentVerifier  *IntentVerifier
    testValidator   *TestValidator
    policyEngine    *PolicyEngine
}

// ValidatingWebhook endpoint
func (c *AIDPSAdmissionController) ValidateDeployment(w http.ResponseWriter, r *http.Request) {
    var admissionReview admissionv1.AdmissionReview
    json.NewDecoder(r.Body).Decode(&admissionReview)

    request := admissionReview.Request

    // STEP 1: Check if deployment has linked intent
    intent, err := c.GetLinkedIntent(request)
    if err != nil {
        // NO INTENT = REJECT
        c.Reject(w, "Deployment must have approved AgentIntent")
        return
    }

    // STEP 2: Verify intent is APPROVED
    if intent.Status.VerificationPhase != "Approved" {
        c.Reject(w, fmt.Sprintf("Intent %s not approved (status: %s)",
            intent.Name, intent.Status.VerificationPhase))
        return
    }

    // STEP 3: Verify deployment matches approved intent
    if !c.VerifyDeploymentMatchesIntent(request, intent) {
        c.Reject(w, "Deployment deviates from approved intent")
        return
    }

    // STEP 4: Verify test requirements met
    if !c.VerifyTestRequirements(intent) {
        c.Reject(w, fmt.Sprintf("Test requirements not met. Coverage: %.2f%% (required: 85%%)",
            intent.Status.TestResults.CoveragePercent))
        return
    }

    // STEP 5: Verify signed provenance (SLSA)
    if !c.VerifyProvenance(request) {
        c.Reject(w, "Deployment artifact lacks valid SLSA provenance")
        return
    }

    // ALL CHECKS PASSED → APPROVE
    c.Approve(w, "All AIDPS controls passed")
}

func (c *AIDPSAdmissionController) VerifyDeploymentMatchesIntent(
    request *admissionv1.AdmissionRequest,
    intent *AgentIntent,
) bool {
    // Parse deployment manifest
    deployment := parseDeployment(request.Object.Raw)

    // Check 1: Deployment targets correct service
    approvedServices := intent.Spec.RequestedActions.Deployment.Services
    if !contains(approvedServices, deployment.Name) {
        return false
    }

    // Check 2: Deployment targets correct environment
    approvedEnv := intent.Spec.RequestedActions.Deployment.Environment
    deploymentEnv := deployment.Labels["environment"]
    if deploymentEnv != approvedEnv {
        return false
    }

    // Check 3: Image digest matches SLSA-attested artifact
    approvedImageDigest := intent.Status.ApprovedImageDigest
    if deployment.Spec.Template.Spec.Containers[0].Image != approvedImageDigest {
        return false
    }

    return true
}

func (c *AIDPSAdmissionController) VerifyTestRequirements(intent *AgentIntent) bool {
    testResults := intent.Status.TestResults

    // Must pass baseline regression tests
    if !testResults.BaselineRegressionPassed {
        return false
    }

    // Must meet coverage minimum
    requiredCoverage := intent.Spec.RequestedActions.TestExecution.MinimumCoverage
    if testResults.CoveragePercent < requiredCoverage {
        return false
    }

    // Must pass security scans
    if !testResults.SecurityScanPassed {
        return false
    }

    // Must have sufficient mutation score (anti-gaming)
    if testResults.MutationScore < 0.70 {
        return false
    }

    return true
}
```

**Admission Controller Deployment:**

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: aidps-deployment-validator
webhooks:
  - name: deployment-validator.aidps.io
    clientConfig:
      service:
        name: aidps-admission-controller
        namespace: aidps-control-plane
        path: "/validate/deployment"
      caBundle: <base64-encoded-ca-cert>

    rules:
      - operations: ["CREATE", "UPDATE"]
        apiGroups: ["apps"]
        apiVersions: ["v1"]
        resources: ["deployments"]

    admissionReviewVersions: ["v1"]
    sideEffects: None

    # CRITICAL: Fail closed (block if webhook unavailable)
    failurePolicy: Fail

    namespaceSelector:
      matchLabels:
        aidps-enforced: "true"
```

### 2.3 Service Mesh Integration (Istio/Linkerd)

**Pattern:** Service mesh enforces intent-based authorization at the network level.

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: aidps-agent-guardrails
  namespace: production
spec:
  selector:
    matchLabels:
      app: user-service

  action: CUSTOM
  provider:
    name: aidps-external-verifier

  rules:
    # Rule 1: ALL requests must have intent ID
    - to:
        - operation:
            methods: ["*"]
      when:
        - key: request.headers[x-intent-id]
          values: ["*"]  # Must be present

    # Rule 2: Intent must be verified
    - to:
        - operation:
            methods: ["POST", "PUT", "DELETE"]
      when:
        - key: request.auth.claims[intent_verified]
          values: ["true"]

    # Rule 3: Production changes require approval
    - to:
        - operation:
            paths: ["/api/prod/*"]
      when:
        - key: request.auth.claims[approval_status]
          values: ["approved"]
        - key: request.auth.claims[approver_role]
          values: ["tech_lead", "sre"]
```

**External Verifier (gRPC Service):**

```go
// AIDPS External Verifier (called by Istio)
service ExternalAuthorizer {
    rpc Check(CheckRequest) returns (CheckResponse);
}

message CheckRequest {
    string intent_id = 1;
    string agent_id = 2;
    string requested_path = 3;
    string requested_method = 4;
}

message CheckResponse {
    enum Status {
        OK = 0;
        PERMISSION_DENIED = 1;
        UNAUTHENTICATED = 2;
    }

    Status status = 1;
    string reason = 2;

    // Metadata injected into request headers
    map<string, string> metadata = 3;
}

func (s *AIDPSVerifier) Check(ctx context.Context, req *CheckRequest) (*CheckResponse, error) {
    // Fetch intent from control plane
    intent, err := s.GetIntent(req.IntentId)
    if err != nil {
        return &CheckResponse{
            Status: PERMISSION_DENIED,
            Reason: fmt.Sprintf("Intent %s not found", req.IntentId),
        }, nil
    }

    // Verify intent is approved
    if intent.Status.VerificationPhase != "Approved" {
        return &CheckResponse{
            Status: PERMISSION_DENIED,
            Reason: fmt.Sprintf("Intent not approved (status: %s)", intent.Status.VerificationPhase),
        }, nil
    }

    // Verify request matches intent scope
    if !s.RequestMatchesIntent(req, intent) {
        return &CheckResponse{
            Status: PERMISSION_DENIED,
            Reason: "Request outside approved intent scope",
        }, nil
    }

    // ALL CHECKS PASSED
    return &CheckResponse{
        Status: OK,
        Metadata: map[string]string{
            "x-intent-verified": "true",
            "x-intent-id": req.IntentId,
            "x-agent-id": req.AgentId,
        },
    }, nil
}
```

---

## Part III: CI/CD Integration - Pipeline Control Plane

### 3.1 GitHub Actions Integration

**Pattern:** GitHub Actions workflows MUST validate intents BEFORE executing deployments.

```yaml
name: AIDPS Verification Gate

on:
  push:
    branches: [main]
  pull_request:

jobs:
  extract-intent:
    runs-on: ubuntu-latest
    outputs:
      intent_id: ${{ steps.parse.outputs.intent_id }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Extract Intent ID
        id: parse
        run: |
          # Intent ID must be in commit message or PR description
          INTENT_ID=$(git log -1 --pretty=%B | grep -oP 'Intent-ID:\s*\K[a-z0-9-]+')

          if [ -z "$INTENT_ID" ]; then
            echo "❌ ERROR: No Intent-ID found in commit message"
            echo "Every commit must link to an approved AgentIntent"
            exit 1
          fi

          echo "intent_id=$INTENT_ID" >> $GITHUB_OUTPUT
          echo "✅ Found Intent-ID: $INTENT_ID"

  verify-intent:
    needs: extract-intent
    runs-on: ubuntu-latest

    steps:
      - name: Verify Intent with Control Plane
        id: verify
        run: |
          # Call AIDPS control plane (outside agent control)
          RESPONSE=$(curl -X POST https://aidps-control-plane.internal/api/v2/verify \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer ${{ secrets.AIDPS_TOKEN }}" \
            -d '{
              "intent_id": "${{ needs.extract-intent.outputs.intent_id }}",
              "commit_sha": "${{ github.sha }}",
              "repository": "${{ github.repository }}",
              "actor": "${{ github.actor }}"
            }')

          echo "$RESPONSE" | jq .

          # Extract verification status
          STATUS=$(echo "$RESPONSE" | jq -r '.verification_status')

          if [ "$STATUS" != "APPROVED" ]; then
            echo "❌ Intent verification FAILED: $STATUS"
            REASON=$(echo "$RESPONSE" | jq -r '.reason')
            echo "Reason: $REASON"
            exit 1
          fi

          echo "✅ Intent verified: APPROVED"
          echo "decision=$STATUS" >> $GITHUB_OUTPUT

  run-tests-isolated:
    needs: verify-intent
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Fetch Signed Test Baseline
        run: |
          # Fetch immutable test baseline (agent CANNOT modify)
          curl -X GET https://aidps-control-plane.internal/api/v2/test-baseline \
            -H "Authorization: Bearer ${{ secrets.AIDPS_TOKEN }}" \
            -o test-baseline.signed.tar.gz

          # Verify signature (HSM-backed)
          cosign verify-blob \
            --key https://aidps-control-plane.internal/signing-key.pub \
            --signature test-baseline.sig \
            test-baseline.signed.tar.gz

          # Extract tests
          tar -xzf test-baseline.signed.tar.gz

      - name: Run Tests in Isolated Environment
        run: |
          # Tests run in platform-controlled environment
          # Agent CANNOT modify test execution
          docker run --rm \
            --network=none \
            --read-only \
            --tmpfs /tmp \
            -v $(pwd)/tests:/tests:ro \
            -v $(pwd)/src:/src:ro \
            test-runner:v1 \
            pytest /tests --cov=/src --cov-report=json

          # Store results (signed by platform)
          RESULTS=$(cat coverage.json)
          curl -X POST https://aidps-control-plane.internal/api/v2/test-results \
            -H "Authorization: Bearer ${{ secrets.AIDPS_TOKEN }}" \
            -H "Content-Type: application/json" \
            -d "$RESULTS"

  mutation-testing:
    needs: run-tests-isolated
    runs-on: ubuntu-latest

    steps:
      - name: Run Mutation Tests (Anti-Gaming)
        run: |
          # Platform introduces bugs, verifies tests catch them
          docker run --rm \
            -v $(pwd):/workspace \
            mutation-tester:v1 \
            --target src/ \
            --tests tests/ \
            --mutants 100 \
            --threshold 0.70

          # Report mutation score
          MUTATION_SCORE=$(cat mutation-results.json | jq -r '.score')

          if (( $(echo "$MUTATION_SCORE < 0.70" | bc -l) )); then
            echo "❌ Mutation score $MUTATION_SCORE below 70% threshold"
            echo "Tests are too weak - didn't catch introduced bugs"
            exit 1
          fi

          echo "✅ Mutation score: $MUTATION_SCORE"

  deploy:
    needs: [verify-intent, run-tests-isolated, mutation-testing]
    if: needs.verify-intent.outputs.decision == 'APPROVED'
    runs-on: ubuntu-latest

    steps:
      - name: Deploy with Signed Approval
        run: |
          # Generate deployment signature (platform signs, not agent)
          DEPLOYMENT_MANIFEST=$(cat k8s/deployment.yaml)

          # Submit to control plane for final approval
          curl -X POST https://aidps-control-plane.internal/api/v2/execute \
            -H "Authorization: Bearer ${{ secrets.AIDPS_TOKEN }}" \
            -H "Content-Type: application/json" \
            -d '{
              "intent_id": "${{ needs.extract-intent.outputs.intent_id }}",
              "manifest": '"$(echo "$DEPLOYMENT_MANIFEST" | jq -Rs .)"',
              "test_results_id": "${{ needs.run-tests-isolated.outputs.results_id }}",
              "commit_sha": "${{ github.sha }}"
            }'
```

### 3.2 GitLab CI Integration

```yaml
# .gitlab-ci.yml
stages:
  - verify-intent
  - test-validation
  - mutation-testing
  - deploy

variables:
  AIDPS_CONTROL_PLANE: "https://aidps-control-plane.internal"

verify-intent:
  stage: verify-intent
  script:
    - |
      # Extract intent ID from merge request description
      INTENT_ID=$(echo "$CI_MERGE_REQUEST_DESCRIPTION" | grep -oP 'Intent-ID:\s*\K[a-z0-9-]+')

      if [ -z "$INTENT_ID" ]; then
        echo "ERROR: No Intent-ID found"
        exit 1
      fi

      # Verify with control plane
      RESPONSE=$(curl -X POST $AIDPS_CONTROL_PLANE/api/v2/verify \
        -H "Authorization: Bearer $AIDPS_TOKEN" \
        -d "{\"intent_id\": \"$INTENT_ID\", \"commit_sha\": \"$CI_COMMIT_SHA\"}")

      STATUS=$(echo "$RESPONSE" | jq -r '.verification_status')

      if [ "$STATUS" != "APPROVED" ]; then
        echo "Intent verification FAILED"
        exit 1
      fi

      # Export for downstream jobs
      echo "INTENT_ID=$INTENT_ID" >> verify.env

  artifacts:
    reports:
      dotenv: verify.env

test-validation:
  stage: test-validation
  dependencies:
    - verify-intent
  script:
    - |
      # Fetch signed test baseline
      curl -X GET $AIDPS_CONTROL_PLANE/api/v2/test-baseline \
        -H "Authorization: Bearer $AIDPS_TOKEN" \
        -o test-baseline.signed.tar.gz

      # Verify signature
      cosign verify-blob --key $AIDPS_SIGNING_KEY test-baseline.signed.tar.gz

      # Run tests in isolated container
      docker run --rm --network=none \
        -v $(pwd)/tests:/tests:ro \
        test-runner pytest /tests --cov --cov-report=json

      # Upload results to control plane
      curl -X POST $AIDPS_CONTROL_PLANE/api/v2/test-results \
        -H "Authorization: Bearer $AIDPS_TOKEN" \
        -d @coverage.json

mutation-testing:
  stage: mutation-testing
  dependencies:
    - test-validation
  script:
    - |
      # Platform-controlled mutation testing
      docker run --rm mutation-tester \
        --target src/ --tests tests/ --threshold 0.70

deploy:
  stage: deploy
  dependencies:
    - verify-intent
    - test-validation
    - mutation-testing
  only:
    - main
  script:
    - |
      # Final deployment requires control plane approval
      curl -X POST $AIDPS_CONTROL_PLANE/api/v2/execute \
        -H "Authorization: Bearer $AIDPS_TOKEN" \
        -d @deployment-manifest.json
```

### 3.3 ArgoCD GitOps Integration

**Pattern:** ArgoCD syncs ONLY from control-plane-approved Git commits.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: user-service
  namespace: argocd
spec:
  project: production

  source:
    repoURL: https://github.com/company/gitops-state
    targetRevision: HEAD
    path: apps/user-service/production

  destination:
    server: https://kubernetes.default.svc
    namespace: production

  syncPolicy:
    automated:
      prune: true
      selfHeal: true

    # CRITICAL: Pre-sync hook validates intent
    syncOptions:
      - CreateNamespace=true
      - Validate=true

    managedNamespaceMetadata:
      labels:
        aidps-enforced: "true"

---
# Pre-Sync Hook: Validate Intent Approval
apiVersion: batch/v1
kind: Job
metadata:
  name: aidps-presync-validation
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: validate-intent
          image: aidps-validator:v2
          env:
            - name: AIDPS_CONTROL_PLANE
              value: "https://aidps-control-plane.internal"
            - name: AIDPS_TOKEN
              valueFrom:
                secretKeyRef:
                  name: aidps-credentials
                  key: token
          command:
            - /bin/sh
            - -c
            - |
              # Extract intent ID from ArgoCD app annotations
              INTENT_ID=$(kubectl get app user-service -n argocd -o jsonpath='{.metadata.annotations.aidps\.io/intent-id}')

              # Verify intent is approved
              RESPONSE=$(curl -X POST $AIDPS_CONTROL_PLANE/api/v2/verify \
                -H "Authorization: Bearer $AIDPS_TOKEN" \
                -d "{\"intent_id\": \"$INTENT_ID\", \"sync_revision\": \"$ARGOCD_APP_REVISION\"}")

              STATUS=$(echo "$RESPONSE" | jq -r '.verification_status')

              if [ "$STATUS" != "APPROVED" ]; then
                echo "Intent $INTENT_ID not approved. Blocking sync."
                exit 1
              fi

              echo "Intent $INTENT_ID verified. Proceeding with sync."
```

---

## Part IV: Anti-Manipulation Controls

### 4.1 Immutable Test Baselines

**Problem:** Agents are incentivized to fake test results or create weak tests.

**Solution:** Test baselines are signed, stored immutably, and agents CANNOT modify them.

```yaml
# Test Baseline (Signed and Immutable)
apiVersion: aidps.io/v2
kind: TestBaseline
metadata:
  name: user-service-baseline-v1.2.3
  namespace: aidps-control-plane
spec:
  appId: "user-service"
  version: "v1.2.3"
  createdAt: "2025-10-01T10:00:00Z"

  # Regression Tests (Must ALL Pass)
  regressionTests:
    - test: "test_user_login_valid_credentials"
      file: "tests/auth/login.test.ts"
      hash: "sha256:abc123def456..."

    - test: "test_user_login_invalid_credentials"
      file: "tests/auth/login.test.ts"
      hash: "sha256:789abc012def..."

    - test: "test_oauth2_authorization_flow"
      file: "tests/auth/oauth2.test.ts"
      hash: "sha256:345def678abc..."

  # Test Coverage Requirements
  coverageRequirements:
    lineCoverage: 85.0
    branchCoverage: 80.0
    functionCoverage: 90.0

  # Mutation Testing Requirements
  mutationRequirements:
    minimumScore: 0.70
    requiredMutants: 100

  # Security Requirements
  securityRequirements:
    sastCriticalMax: 0
    sastHighMax: 0
    secretsFoundMax: 0

  # Baseline Hash (for integrity verification)
  baselineHash: "sha256:def456abc789..."

  # Cryptographic Signature (HSM-backed)
  signature:
    signer: "aidps-platform-authority"
    algorithm: "ECDSA-P256"
    publicKeyId: "aidps-signing-key-2025"
    signatureValue: "MEUCIQCx7..."

  # Immutable Storage References
  immutableStorage:
    git:
      repository: "https://github.com/company/test-baselines"
      commit: "abc123def456..."
      path: "baselines/user-service-v1.2.3.yaml"

    blockchain:
      network: "ethereum-mainnet"
      contractAddress: "0x1234567890abcdef..."
      transactionHash: "0xabcdef123456..."

    hsmBackedStorage:
      provider: "aws-cloudhsm"
      keyId: "arn:aws:cloudhsm:..."
      encryptedBlob: "base64encodeddata..."
```

**Verification Process:**

```go
func VerifyTestBaseline(baseline *TestBaseline) error {
    // Step 1: Verify signature
    publicKey, err := LoadPublicKey(baseline.Signature.PublicKeyId)
    if err != nil {
        return fmt.Errorf("failed to load public key: %w", err)
    }

    signatureValid := ecdsa.Verify(
        publicKey,
        baseline.BaselineHash,
        baseline.Signature.SignatureValue,
    )

    if !signatureValid {
        return errors.New("baseline signature invalid - may be tampered")
    }

    // Step 2: Verify hash chain
    computedHash := ComputeHash(baseline.Spec)
    if computedHash != baseline.BaselineHash {
        return errors.New("baseline hash mismatch - data modified")
    }

    // Step 3: Verify immutable storage
    gitCommit, err := FetchFromGit(baseline.ImmutableStorage.Git)
    if err != nil {
        return fmt.Errorf("failed to fetch from Git: %w", err)
    }

    if gitCommit.Hash != baseline.ImmutableStorage.Git.Commit {
        return errors.New("Git commit mismatch - baseline not in Git")
    }

    // Step 4: Verify blockchain record (optional, for critical apps)
    if baseline.ImmutableStorage.Blockchain != nil {
        txData, err := FetchBlockchainTransaction(
            baseline.ImmutableStorage.Blockchain.TransactionHash,
        )
        if err != nil {
            return fmt.Errorf("failed to fetch blockchain tx: %w", err)
        }

        if txData.Hash != baseline.BaselineHash {
            return errors.New("blockchain record mismatch")
        }
    }

    return nil
}
```

### 4.2 Platform-Controlled Test Execution

**Problem:** Agents could mock test frameworks or override test results.

**Solution:** Tests run in platform-controlled, hermetic environments that agents CANNOT access.

```yaml
# Platform-Controlled Test Execution Environment
apiVersion: v1
kind: Pod
metadata:
  name: test-execution-pod
  namespace: aidps-test-execution
  labels:
    aidps-controlled: "true"
    agent-access: "deny"
spec:
  # Security Context (Agent CANNOT modify)
  securityContext:
    runAsNonRoot: true
    runAsUser: 10000
    fsGroup: 10000
    seccompProfile:
      type: RuntimeDefault

  # No network access (hermetic)
  hostNetwork: false

  initContainers:
    # Fetch signed test baseline
    - name: fetch-baseline
      image: aidps-baseline-fetcher:v2
      securityContext:
        readOnlyRootFilesystem: true
        allowPrivilegeEscalation: false
      volumeMounts:
        - name: test-baseline
          mountPath: /baseline
        - name: tmp
          mountPath: /tmp
      command:
        - /bin/sh
        - -c
        - |
          # Fetch from control plane (agent CANNOT intercept)
          curl -X GET https://aidps-control-plane.internal/api/v2/test-baseline \
            -H "Authorization: Bearer $AIDPS_TOKEN" \
            -o /tmp/baseline.tar.gz

          # Verify signature
          cosign verify-blob \
            --key /etc/aidps/signing-key.pub \
            --signature /tmp/baseline.sig \
            /tmp/baseline.tar.gz

          # Extract to read-only volume
          tar -xzf /tmp/baseline.tar.gz -C /baseline

    # Fetch application code
    - name: fetch-code
      image: aidps-code-fetcher:v2
      securityContext:
        readOnlyRootFilesystem: true
        allowPrivilegeEscalation: false
      volumeMounts:
        - name: application-code
          mountPath: /code
        - name: tmp
          mountPath: /tmp
      command:
        - /bin/sh
        - -c
        - |
          # Fetch from Git (specific commit, agent CANNOT modify)
          git clone --depth 1 --branch $COMMIT_SHA \
            https://github.com/company/user-service.git /tmp/repo

          # Verify commit signature
          git verify-commit $COMMIT_SHA

          # Copy to read-only volume
          cp -r /tmp/repo /code

  containers:
    # Test Executor (Platform-Controlled)
    - name: test-executor
      image: aidps-test-runner:v2
      securityContext:
        readOnlyRootFilesystem: true
        allowPrivilegeEscalation: false
        capabilities:
          drop: ["ALL"]

      # Read-only mounts (agent CANNOT modify)
      volumeMounts:
        - name: test-baseline
          mountPath: /tests
          readOnly: true
        - name: application-code
          mountPath: /app
          readOnly: true
        - name: test-results
          mountPath: /results

      # No environment variables from agent
      env:
        - name: AIDPS_CONTROLLED
          value: "true"
        - name: TEST_FRAMEWORK
          value: "pytest"
        - name: COVERAGE_REQUIRED
          value: "85"

      command:
        - /usr/local/bin/aidps-test-runner
        - --tests=/tests
        - --code=/app
        - --output=/results/coverage.json
        - --enforce-baseline
        - --no-skip
        - --fail-on-coverage-decrease

  volumes:
    - name: test-baseline
      emptyDir: {}
    - name: application-code
      emptyDir: {}
    - name: test-results
      emptyDir: {}
    - name: tmp
      emptyDir: {}

  # Pod Security Policy
  automountServiceAccountToken: false

  # Network Policy (No egress)
  dnsPolicy: None
```

### 4.3 Mutation Testing (Anti-Gaming)

**Problem:** Agents could create weak tests that always pass.

**Solution:** Platform introduces bugs into code, verifies tests catch them.

```python
# Platform-Controlled Mutation Testing
class MutationTestingOrchestrator:
    """
    Introduces bugs into code, verifies agent's tests catch them.

    If tests DON'T catch bugs → tests are too weak → REJECT deployment
    """

    def run_mutation_testing(
        self,
        code_path: str,
        test_path: str,
        agent_id: str,
    ) -> MutationTestResult:
        """
        Generate mutants, run tests, calculate mutation score.
        """

        # Step 1: Generate mutants (code with introduced bugs)
        mutants = self.generate_mutants(code_path, count=100)

        # Step 2: Run tests against each mutant
        killed_mutants = 0
        survived_mutants = 0

        for mutant in mutants:
            # Run agent's tests against mutated code
            test_result = self.run_tests_isolated(
                mutant_code=mutant.code,
                test_code=test_path,
            )

            if test_result.failed:
                # Test CAUGHT the bug (good!)
                killed_mutants += 1
            else:
                # Test DIDN'T catch the bug (bad!)
                survived_mutants += 1

                # Log weak test coverage
                logger.warning(
                    f"Mutant {mutant.id} SURVIVED. "
                    f"Mutation: {mutant.description}. "
                    f"Agent {agent_id} tests too weak."
                )

        # Step 3: Calculate mutation score
        mutation_score = killed_mutants / len(mutants)

        return MutationTestResult(
            total_mutants=len(mutants),
            killed=killed_mutants,
            survived=survived_mutants,
            mutation_score=mutation_score,
            passed=(mutation_score >= 0.70),
        )

    def generate_mutants(self, code_path: str, count: int) -> List[Mutant]:
        """
        Generate code mutations using AST transformations.
        """
        mutants = []

        # Parse code into AST
        with open(code_path, 'r') as f:
            tree = ast.parse(f.read())

        # Mutation 1: Replace comparison operators
        for node in ast.walk(tree):
            if isinstance(node, ast.Compare):
                # Replace == with !=
                if isinstance(node.ops[0], ast.Eq):
                    mutated_tree = copy.deepcopy(tree)
                    mutated_node = find_node(mutated_tree, node)
                    mutated_node.ops[0] = ast.NotEq()

                    mutants.append(Mutant(
                        id=f"CMP_{len(mutants)}",
                        description="Replaced == with !=",
                        code=ast.unparse(mutated_tree),
                    ))

        # Mutation 2: Remove return statements
        for node in ast.walk(tree):
            if isinstance(node, ast.Return) and node.value:
                mutated_tree = copy.deepcopy(tree)
                mutated_node = find_node(mutated_tree, node)
                mutated_node.value = ast.Constant(value=None)

                mutants.append(Mutant(
                    id=f"RET_{len(mutants)}",
                    description="Changed return value to None",
                    code=ast.unparse(mutated_tree),
                ))

        # Mutation 3: Invert boolean conditions
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                mutated_tree = copy.deepcopy(tree)
                mutated_node = find_node(mutated_tree, node)
                mutated_node.test = ast.UnaryOp(
                    op=ast.Not(),
                    operand=mutated_node.test,
                )

                mutants.append(Mutant(
                    id=f"IF_{len(mutants)}",
                    description="Inverted if condition",
                    code=ast.unparse(mutated_tree),
                ))

        # Mutation 4: Off-by-one errors
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, int):
                mutated_tree = copy.deepcopy(tree)
                mutated_node = find_node(mutated_tree, node)
                mutated_node.value += 1

                mutants.append(Mutant(
                    id=f"NUM_{len(mutants)}",
                    description=f"Changed {node.value} to {node.value + 1}",
                    code=ast.unparse(mutated_tree),
                ))

        return mutants[:count]
```

**Mutation Testing Thresholds:**

| Environment | Minimum Mutation Score | Rationale |
|-------------|------------------------|-----------|
| Dev | 50% | Low-risk, rapid iteration |
| Staging | 70% | Moderate confidence required |
| Production | 80% | High confidence required |
| Critical Systems | 90% | Mission-critical safety |

---

## Part V: Neural Scoring Model (ML, Not LLM Reasoning)

### 5.1 Intent Risk Scoring with Gradient Boosted Trees

**Key Principle:** Use ML for SCORING, not REASONING. The model outputs a risk score, but deterministic rules make the final decision.

```python
import xgboost as xgb
from typing import Dict, Tuple

class IntentNeuralScorer:
    """
    ML model for intent risk scoring.

    IMPORTANT: This is NOT a reasoning LLM (no GPT-4, no Claude).
    This is a gradient boosted tree classifier (XGBoost).

    Input: Intent features (deterministic extraction)
    Output: Risk score (0.0 = safe, 1.0 = risky) + confidence
    """

    def __init__(self, model_path: str):
        # Load pre-trained XGBoost model
        self.model = xgb.Booster()
        self.model.load_model(model_path)

    def score_intent(
        self,
        intent: AgentIntent,
        app_context: ApplicationContext,
    ) -> ScoringResult:
        """
        Score intent using ML model.

        Returns:
            ScoringResult with risk_score, confidence, decision
        """

        # Step 1: Extract features (deterministic)
        features = self.extract_features(intent, app_context)

        # Step 2: Run ML model (deterministic given weights)
        dmatrix = xgb.DMatrix([features])
        risk_score = self.model.predict(dmatrix)[0]

        # Step 3: Calculate confidence
        confidence = self.calculate_confidence(
            risk_score=risk_score,
            similar_deployments=app_context.similar_deployments,
        )

        # Step 4: Make decision (deterministic rules, NOT model)
        decision = self.make_decision(risk_score, confidence)

        return ScoringResult(
            risk_score=risk_score,
            confidence=confidence,
            decision=decision,
            reason=self.explain_decision(risk_score, features),
        )

    def extract_features(
        self,
        intent: AgentIntent,
        app_context: ApplicationContext,
    ) -> List[float]:
        """
        Extract features for ML model.

        IMPORTANT: Feature extraction is DETERMINISTIC.
        Same intent + same context → same features.
        """

        features = []

        # Feature 1-5: Intent clarity
        features.append(len(intent.spec.primaryObjective.split()))  # Word count
        features.append(1.0 if intent.spec.requestedActions.codeModification else 0.0)
        features.append(1.0 if intent.spec.requestedActions.deployment else 0.0)
        features.append(len(intent.spec.constraints.mustNotModify))
        features.append(1.0 if intent.spec.constraints.requiresApproval else 0.0)

        # Feature 6-10: Historical similarity
        features.append(len(app_context.similar_deployments))
        features.append(app_context.avg_success_rate)
        features.append(app_context.avg_test_coverage)
        features.append(app_context.avg_mutation_score)
        features.append(app_context.days_since_last_deployment)

        # Feature 11-15: Risk indicators
        features.append(1.0 if "production" in intent.spec.requestedActions.deployment.environment else 0.0)
        features.append(len(self.get_critical_files_modified(intent)))
        features.append(1.0 if self.modifies_auth_code(intent) else 0.0)
        features.append(1.0 if self.modifies_database_schema(intent) else 0.0)
        features.append(1.0 if self.requires_downtime(intent) else 0.0)

        # Feature 16-20: Test maturity
        if intent.status.testResults:
            features.append(intent.status.testResults.coveragePercent / 100.0)
            features.append(intent.status.testResults.mutationScore)
            features.append(1.0 if intent.status.testResults.securityScanPassed else 0.0)
            features.append(intent.status.testResults.newTestsCreated / 100.0)
            features.append(1.0 if intent.status.testResults.baselineRegressionPassed else 0.0)
        else:
            features.extend([0.0] * 5)

        return features

    def calculate_confidence(
        self,
        risk_score: float,
        similar_deployments: List[Deployment],
    ) -> float:
        """
        Calculate confidence based on historical data.

        High confidence if:
        - Many similar deployments exist
        - Similar deployments had consistent outcomes

        Low confidence if:
        - Few similar deployments
        - Similar deployments had variable outcomes
        """

        if len(similar_deployments) == 0:
            return 0.5  # Low confidence (no historical data)

        # Calculate outcome variance
        outcomes = [d.success for d in similar_deployments]
        variance = np.var(outcomes)

        # More data + low variance = high confidence
        confidence = min(
            1.0,
            (len(similar_deployments) / 100.0) * (1.0 - variance)
        )

        return confidence

    def make_decision(
        self,
        risk_score: float,
        confidence: float,
    ) -> str:
        """
        Make final decision using DETERMINISTIC RULES.

        IMPORTANT: The ML model provides a score, but
        DETERMINISTIC RULES make the final decision.
        """

        # Rule 1: High confidence + low risk → Auto-approve
        if confidence > 0.8 and risk_score < 0.3:
            return "APPROVED"

        # Rule 2: High confidence + medium risk → Require review
        if confidence > 0.8 and 0.3 <= risk_score < 0.7:
            return "REQUIRES_APPROVAL"

        # Rule 3: High confidence + high risk → Reject
        if confidence > 0.8 and risk_score >= 0.7:
            return "REJECTED"

        # Rule 4: Low confidence → Always require approval
        if confidence < 0.5:
            return "REQUIRES_APPROVAL"

        # Rule 5: Medium confidence + low risk → Approve with monitoring
        if confidence >= 0.5 and risk_score < 0.4:
            return "APPROVED_WITH_MONITORING"

        # Default: Require approval
        return "REQUIRES_APPROVAL"

    def explain_decision(
        self,
        risk_score: float,
        features: List[float],
    ) -> str:
        """
        Generate human-readable explanation.
        """

        # Use SHAP values to explain prediction
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values([features])[0]

        # Find top 3 contributing features
        top_indices = np.argsort(np.abs(shap_values))[-3:]

        feature_names = [
            "Intent clarity", "Historical similarity", "Risk indicators",
            "Test maturity", "Deployment environment", "Code modification scope",
        ]

        explanation = f"Risk score: {risk_score:.2f}\n"
        explanation += "Top contributing factors:\n"
        for idx in top_indices:
            explanation += f"- {feature_names[idx]}: {shap_values[idx]:.3f}\n"

        return explanation
```

**Model Training Process:**

```python
def train_intent_scorer(historical_data: pd.DataFrame) -> xgb.Booster:
    """
    Train XGBoost model on historical deployment data.

    Data includes:
    - Intent features (extracted deterministically)
    - Actual outcomes (success/failure, incident count, rollback rate)
    """

    # Prepare training data
    X_train = historical_data[FEATURE_COLUMNS]
    y_train = historical_data['deployment_failed'].astype(int)

    # Train XGBoost classifier
    dtrain = xgb.DMatrix(X_train, label=y_train)

    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
        'max_depth': 6,
        'eta': 0.1,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'seed': 42,  # Fixed seed for determinism
    }

    model = xgb.train(
        params,
        dtrain,
        num_boost_round=100,
        evals=[(dtrain, 'train')],
    )

    return model
```

### 5.2 Why ML, Not LLM?

| Aspect | LLM (GPT-4, Claude) | ML (XGBoost, Neural Net) |
|--------|---------------------|---------------------------|
| **Determinism** | ❌ Non-deterministic (temperature>0) | ✅ Deterministic (fixed weights) |
| **Reasoning** | ✅ Can reason about code | ❌ Cannot reason (only classify) |
| **Speed** | ❌ Slow (seconds per request) | ✅ Fast (milliseconds) |
| **Cost** | ❌ Expensive ($0.01-0.10 per request) | ✅ Cheap ($0.0001 per request) |
| **Explainability** | ❌ Opaque ("I think...") | ✅ SHAP values (exact feature contributions) |
| **Attack Surface** | ❌ Prompt injection vulnerable | ✅ No prompt injection risk |
| **Auditability** | ❌ Hard to audit (billions of parameters) | ✅ Easy to audit (hundreds of features) |

**Verdict:** For the external control plane, use **ML classifiers (XGBoost, random forest)** for scoring, NOT LLMs for reasoning.

---

## Part VI: Shopping Cart Approval Workflow

### 6.1 Intent Shopping Cart

**Pattern:** Agents add intents to a "shopping cart", humans approve/reject the cart.

```yaml
apiVersion: aidps.io/v2
kind: IntentShoppingCart
metadata:
  name: sprint-42-deployments
  namespace: production
spec:
  createdBy: "agent-xyz12345"
  createdAt: "2025-10-01T10:00:00Z"
  expiresAt: "2025-10-01T18:00:00Z"

  # Intents in cart
  intents:
    - intentId: "intent-abc123"
      summary: "Add OAuth2 authentication to user-service"
      riskScore: 0.25
      estimatedDuration: "15m"
      requiredApprovers: ["tech-lead"]

    - intentId: "intent-def456"
      summary: "Scale user-service replicas from 3 to 5"
      riskScore: 0.10
      estimatedDuration: "5m"
      requiredApprovers: ["sre"]

    - intentId: "intent-ghi789"
      summary: "Migrate database schema (add users.email_verified column)"
      riskScore: 0.75
      estimatedDuration: "30m"
      requiredApprovers: ["tech-lead", "sre", "dba"]

  # Aggregate metrics
  aggregateMetrics:
    totalRiskScore: 1.10
    totalEstimatedDuration: "50m"
    highestRiskIntent: "intent-ghi789"
    requiresApprovalCount: 3

  # Approval workflow
  approvalWorkflow:
    mode: "multi-stakeholder"
    requiredApprovers:
      - role: "tech-lead"
        minApprovals: 1
      - role: "sre"
        minApprovals: 1
      - role: "dba"
        minApprovals: 1

    # Optional: Use quorum for low-risk carts
    quorumMode:
      enabled: false
      requiredApprovals: 2
      totalStakeholders: 3

status:
  approvalPhase: "PendingApproval"

  approvals:
    - approver: "alice@company.com"
      role: "tech-lead"
      decision: "approved"
      timestamp: "2025-10-01T11:00:00Z"
      comment: "Looks good. Tests pass, mutation score is high."

    - approver: "bob@company.com"
      role: "sre"
      decision: "approved"
      timestamp: "2025-10-01T11:15:00Z"
      comment: "LGTM. Rollback plan is solid."

    - approver: "carol@company.com"
      role: "dba"
      decision: "pending"
      timestamp: null
      comment: null

  # Overall cart status
  overallDecision: "PendingApproval"  # Waiting for DBA approval
  readyToExecute: false
```

### 6.2 Approval UI (Web Interface)

```typescript
// React component for shopping cart approval
interface IntentShoppingCartApprovalProps {
    cartId: string;
    approverRole: string;
}

function IntentShoppingCartApproval({
    cartId,
    approverRole,
}: IntentShoppingCartApprovalProps) {
    const [cart, setCart] = useState<IntentShoppingCart | null>(null);

    useEffect(() => {
        // Fetch cart from control plane
        fetch(`https://aidps-control-plane.internal/api/v2/shopping-carts/${cartId}`)
            .then(res => res.json())
            .then(setCart);
    }, [cartId]);

    const handleApprove = async () => {
        await fetch(
            `https://aidps-control-plane.internal/api/v2/shopping-carts/${cartId}/approve`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    approver_role: approverRole,
                    decision: 'approved',
                    comment: document.getElementById('approval-comment').value,
                }),
            }
        );

        // Refresh cart
        window.location.reload();
    };

    const handleReject = async () => {
        await fetch(
            `https://aidps-control-plane.internal/api/v2/shopping-carts/${cartId}/reject`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    approver_role: approverRole,
                    decision: 'rejected',
                    comment: document.getElementById('rejection-comment').value,
                }),
            }
        );

        // Refresh cart
        window.location.reload();
    };

    if (!cart) return <div>Loading...</div>;

    return (
        <div className="shopping-cart-approval">
            <h1>Intent Shopping Cart: {cart.metadata.name}</h1>

            <div className="aggregate-metrics">
                <h2>Aggregate Metrics</h2>
                <p>Total Risk Score: {cart.spec.aggregateMetrics.totalRiskScore.toFixed(2)}</p>
                <p>Estimated Duration: {cart.spec.aggregateMetrics.totalEstimatedDuration}</p>
                <p>Highest Risk: {cart.spec.aggregateMetrics.highestRiskIntent}</p>
            </div>

            <div className="intents-list">
                <h2>Intents in Cart</h2>
                {cart.spec.intents.map(intent => (
                    <div key={intent.intentId} className="intent-card">
                        <h3>{intent.summary}</h3>
                        <p>Risk Score: {intent.riskScore.toFixed(2)}</p>
                        <p>Duration: {intent.estimatedDuration}</p>
                        <p>Required Approvers: {intent.requiredApprovers.join(', ')}</p>

                        <button onClick={() => viewIntentDetails(intent.intentId)}>
                            View Details
                        </button>
                    </div>
                ))}
            </div>

            <div className="approval-status">
                <h2>Approval Status</h2>
                {cart.status.approvals.map(approval => (
                    <div key={approval.approver} className="approval-entry">
                        <span className={`status ${approval.decision}`}>
                            {approval.decision === 'approved' ? '✅' : '⏳'}
                        </span>
                        <span>{approval.approver} ({approval.role})</span>
                        {approval.comment && <p>{approval.comment}</p>}
                    </div>
                ))}
            </div>

            {cart.status.approvalPhase === 'PendingApproval' && (
                <div className="approval-actions">
                    <textarea
                        id="approval-comment"
                        placeholder="Add your approval comment..."
                    />
                    <button onClick={handleApprove} className="btn-approve">
                        ✅ Approve Cart
                    </button>
                    <button onClick={handleReject} className="btn-reject">
                        ❌ Reject Cart
                    </button>
                </div>
            )}

            {cart.status.overallDecision === 'Approved' && (
                <div className="execution-ready">
                    <h2>✅ Cart Approved - Ready to Execute</h2>
                    <button onClick={executeCart} className="btn-execute">
                        🚀 Execute All Intents
                    </button>
                </div>
            )}
        </div>
    );
}
```

### 6.3 Slack Integration for Approvals

```python
# Slack bot for intent approvals
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier

class SlackApprovalBot:
    def __init__(self, bot_token: str, signing_secret: str):
        self.client = WebClient(token=bot_token)
        self.verifier = SignatureVerifier(signing_secret)

    def send_approval_request(
        self,
        cart: IntentShoppingCart,
        approver_slack_id: str,
    ):
        """
        Send interactive approval request to Slack.
        """

        # Build approval blocks
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🛒 Approval Required: {cart.metadata.name}",
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"*Total Risk Score:* {cart.spec.aggregateMetrics.totalRiskScore:.2f}\n"
                        f"*Estimated Duration:* {cart.spec.aggregateMetrics.totalEstimatedDuration}\n"
                        f"*Intents:* {len(cart.spec.intents)}"
                    )
                }
            },
            {"type": "divider"},
        ]

        # Add each intent
        for intent in cart.spec.intents:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"*{intent.summary}*\n"
                        f"Risk: {intent.riskScore:.2f} | Duration: {intent.estimatedDuration}"
                    )
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "View Details"},
                    "url": f"https://aidps-ui.company.com/intents/{intent.intentId}",
                }
            })

        blocks.append({"type": "divider"})

        # Add approval actions
        blocks.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "✅ Approve"},
                    "style": "primary",
                    "value": cart.metadata.name,
                    "action_id": "approve_cart",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "❌ Reject"},
                    "style": "danger",
                    "value": cart.metadata.name,
                    "action_id": "reject_cart",
                },
            ]
        })

        # Send to approver
        self.client.chat_postMessage(
            channel=approver_slack_id,
            blocks=blocks,
        )

    def handle_approval_action(self, payload: dict):
        """
        Handle approval button click.
        """

        action = payload['actions'][0]
        cart_name = action['value']
        decision = 'approved' if action['action_id'] == 'approve_cart' else 'rejected'
        approver = payload['user']['id']

        # Call control plane API
        response = requests.post(
            f"https://aidps-control-plane.internal/api/v2/shopping-carts/{cart_name}/approve",
            json={
                "approver_slack_id": approver,
                "decision": decision,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

        # Update Slack message
        if response.ok:
            self.client.chat_update(
                channel=payload['channel']['id'],
                ts=payload['message']['ts'],
                text=f"✅ Cart {decision} by <@{approver}>",
            )
```

---

## Part VII: Complete Component Diagram

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                         AIDPS v2.0 EXTERNAL CONTROL PLANE                      │
│                                                                                │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ AGENT LAYER (Untrusted)                                                  │ │
│  │ ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐        │ │
│  │ │ AI Agent 1 │  │ AI Agent 2 │  │ AI Agent 3 │  │ AI Agent N │        │ │
│  │ │ (Research) │  │ (Coding)   │  │ (Testing)  │  │ (Deploy)   │        │ │
│  │ └────────────┘  └────────────┘  └────────────┘  └────────────┘        │ │
│  │       │               │               │               │                  │ │
│  │       └───────────────┴───────────────┴───────────────┘                  │ │
│  │                              │                                           │ │
│  └──────────────────────────────┼───────────────────────────────────────────┘ │
│                                 │ (Intents via mTLS)                          │
│                                 ↓                                             │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ API GATEWAY (Trust Boundary)                                             │ │
│  │ - mTLS authentication                                                    │ │
│  │ - Rate limiting (1000 req/min)                                           │ │
│  │ - Input sanitization                                                     │ │
│  │ - Schema validation                                                      │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                 │                                             │
│                                 ↓                                             │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ LAYER 1: VERIFICATION GATE (Deterministic)                               │ │
│  │                                                                          │ │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐           │ │
│  │  │ Intent Parser  │  │ ML Risk Scorer │  │  Rule Engine   │           │ │
│  │  │ (Deterministic)│  │  (XGBoost)     │  │  (OPA Rego)    │           │ │
│  │  └────────────────┘  └────────────────┘  └────────────────┘           │ │
│  │          │                   │                    │                      │ │
│  │          └───────────────────┴────────────────────┘                      │ │
│  │                              │                                           │ │
│  │                              ↓                                           │ │
│  │                    ┌──────────────────┐                                 │ │
│  │                    │ Verification DB  │                                 │ │
│  │                    │ (Intent history) │                                 │ │
│  │                    └──────────────────┘                                 │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                 │                                             │
│                                 ↓                                             │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ LAYER 2: TEST VALIDATION (Platform-Controlled)                          │ │
│  │                                                                          │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │ │
│  │  │ Baseline Store  │  │ Test Executor   │  │ Mutation Tester │        │ │
│  │  │ (Signed, HSM)   │  │ (Isolated Pods) │  │ (Anti-Gaming)   │        │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │ │
│  │          │                   │                    │                      │ │
│  │          └───────────────────┴────────────────────┘                      │ │
│  │                              │                                           │ │
│  │                              ↓                                           │ │
│  │                    ┌──────────────────┐                                 │ │
│  │                    │  Test Results DB │                                 │ │
│  │                    │ (Immutable logs) │                                 │ │
│  │                    └──────────────────┘                                 │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                 │                                             │
│                                 ↓                                             │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ LAYER 3: APPROVAL WORKFLOW (Human-in-Loop)                              │ │
│  │                                                                          │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │ │
│  │  │ Shopping Cart   │  │ Approval Engine │  │  Slack/UI       │        │ │
│  │  │ (Multi-intent)  │  │ (Multi-party)   │  │  (Notifications)│        │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │ │
│  │          │                   │                    │                      │ │
│  │          └───────────────────┴────────────────────┘                      │ │
│  │                              │                                           │ │
│  │                              ↓                                           │ │
│  │                    ┌──────────────────┐                                 │ │
│  │                    │  Approval DB     │                                 │ │
│  │                    │  (Audit trail)   │                                 │ │
│  │                    └──────────────────┘                                 │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                 │                                             │
│                                 ↓ (Approved Intents Only)                    │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ EXECUTION LAYER (Kubernetes + CI/CD)                                    │ │
│  │                                                                          │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │ │
│  │  │   Admission     │  │  Service Mesh   │  │   GitOps        │        │ │
│  │  │   Controllers   │  │  (Istio Auth)   │  │   (ArgoCD)      │        │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │ │
│  │          │                   │                    │                      │ │
│  │          └───────────────────┴────────────────────┘                      │ │
│  │                              │                                           │ │
│  │                              ↓                                           │ │
│  │                    ┌──────────────────┐                                 │ │
│  │                    │  Kubernetes      │                                 │ │
│  │                    │  Control Plane   │                                 │ │
│  │                    └──────────────────┘                                 │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                                │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## Part VIII: API Specifications

### 8.1 Control Plane API (OpenAPI 3.0)

```yaml
openapi: 3.0.0
info:
  title: AIDPS v2.0 External Control Plane API
  version: 2.0.0
  description: Deterministic, ML-enabled control plane API

servers:
  - url: https://aidps-control-plane.internal/api/v2

paths:
  /intents:
    post:
      summary: Submit agent intent
      security:
        - mTLS: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AgentIntent'
      responses:
        '201':
          description: Intent created and queued for verification
          content:
            application/json:
              schema:
                type: object
                properties:
                  intent_id:
                    type: string
                    format: uuid
                  verification_phase:
                    type: string
                    enum: ["PendingVerification"]
        '400':
          description: Invalid intent (schema validation failed)
        '429':
          description: Rate limit exceeded

  /intents/{intent_id}/verify:
    post:
      summary: Verify intent (control plane internal use)
      parameters:
        - name: intent_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Verification result
          content:
            application/json:
              schema:
                type: object
                properties:
                  verification_status:
                    type: string
                    enum: ["APPROVED", "REJECTED", "REQUIRES_APPROVAL"]
                  risk_score:
                    type: number
                    minimum: 0
                    maximum: 1
                  confidence:
                    type: number
                    minimum: 0
                    maximum: 1
                  reason:
                    type: string

  /test-baselines/{app_id}/{version}:
    get:
      summary: Fetch signed test baseline
      parameters:
        - name: app_id
          in: path
          required: true
          schema:
            type: string
        - name: version
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Signed test baseline
          content:
            application/octet-stream:
              schema:
                type: string
                format: binary

  /test-results:
    post:
      summary: Submit test results (platform-controlled execution only)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TestResults'
      responses:
        '201':
          description: Test results recorded

  /shopping-carts:
    post:
      summary: Create intent shopping cart
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/IntentShoppingCart'
      responses:
        '201':
          description: Shopping cart created

  /shopping-carts/{cart_id}/approve:
    post:
      summary: Approve/reject shopping cart
      parameters:
        - name: cart_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                approver_role:
                  type: string
                decision:
                  type: string
                  enum: ["approved", "rejected"]
                comment:
                  type: string
      responses:
        '200':
          description: Approval recorded

  /execute:
    post:
      summary: Execute approved intent (final step)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                intent_id:
                  type: string
                  format: uuid
                manifest:
                  type: string
                test_results_id:
                  type: string
                commit_sha:
                  type: string
      responses:
        '202':
          description: Execution initiated
        '403':
          description: Intent not approved

components:
  schemas:
    AgentIntent:
      type: object
      required:
        - agentId
        - primaryObjective
        - requestedActions
      properties:
        agentId:
          type: string
        primaryObjective:
          type: string
        requestedActions:
          type: object
        constraints:
          type: object

    TestResults:
      type: object
      properties:
        baseline_regression_passed:
          type: boolean
        coverage_percent:
          type: number
        mutation_score:
          type: number
        security_scan_passed:
          type: boolean

    IntentShoppingCart:
      type: object
      properties:
        intents:
          type: array
          items:
            type: object
        aggregateMetrics:
          type: object

  securitySchemes:
    mTLS:
      type: mutualTLS
      description: Mutual TLS authentication
```

---

## Conclusion

AIDPS v2.0 External Control Plane provides:

1. **Outside Agent Control:** Hermetically sealed control plane agents CANNOT access
2. **Deterministic Core:** Same inputs → same outputs (no LLM hallucinations)
3. **ML-Enabled Scoring:** XGBoost for risk assessment (NOT reasoning LLMs)
4. **Kubernetes Integration:** Admission controllers + CRDs + service mesh
5. **CI/CD Integration:** GitHub Actions + GitLab + ArgoCD hooks
6. **Anti-Manipulation:** Signed baselines + isolated execution + mutation testing
7. **Shopping Cart Approval:** Multi-stakeholder sign-off with audit trail

**Next Steps:**

1. Prototype intent verification gate (XGBoost scorer)
2. Implement Kubernetes admission controller
3. Build test baseline signing infrastructure
4. Deploy mutation testing framework
5. Create shopping cart approval UI

---

**Document Control:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.0 | 2025-10-01 | Control Plane Architect | Initial external control plane architecture |

**Related Documents:**

- `/epics/active/idp/ARCHITECTURE-AIDPS-CONTROL-PLANE.md` - v1.0 architecture
- `/epics/active/idp/RESEARCH-DETERMINISTIC-CONTROL-PLANE.md` - Research foundation
- `/epics/active/idp/AIDPS-STANDARD-v1.0.md` - Standard specification

---

**END OF DOCUMENT**

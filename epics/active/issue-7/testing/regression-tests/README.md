# Regression Testing Framework for RAG Systems

## Overview

This framework ensures RAG system consistency across model versions, configuration changes, and system updates by detecting performance regressions and maintaining output stability.

## Regression Test Categories

### 1. Output Consistency Tests

#### Response Stability Validation
```python
class ResponseStabilityTests:
    """Test consistency of responses across system versions."""
    
    def test_deterministic_response_consistency(self):
        """Verify identical inputs produce identical outputs."""
        stable_queries = self.load_stability_test_queries()
        
        # Run queries multiple times
        response_sets = []
        for iteration in range(5):
            responses = []
            for query in stable_queries:
                response = self.rag_system.process_query(query)
                responses.append(response)
            response_sets.append(responses)
        
        # Validate consistency across iterations
        for i, query in enumerate(stable_queries):
            query_responses = [response_set[i] for response_set in response_sets]
            self.assert_response_consistency(query_responses, query)
    
    def test_semantic_consistency(self):
        """Test semantic consistency of responses over time."""
        # Load baseline responses from previous version
        baseline_responses = self.load_baseline_responses()
        
        # Generate current responses for same queries
        current_responses = []
        for query in baseline_responses.keys():
            response = self.rag_system.process_query(query)
            current_responses.append((query, response))
        
        # Compare semantic similarity
        for query, current_response in current_responses:
            baseline_response = baseline_responses[query]
            semantic_similarity = self.calculate_semantic_similarity(
                current_response, baseline_response
            )
            
            self.assertGreater(
                semantic_similarity, 
                self.SEMANTIC_CONSISTENCY_THRESHOLD,
                f"Semantic regression detected for query: {query}"
            )
```

#### Version Compatibility Tests
```python
class VersionCompatibilityTests:
    """Test compatibility across different system versions."""
    
    def test_model_version_compatibility(self):
        """Test compatibility across model versions."""
        model_versions = ['v1.0', 'v1.1', 'v1.2']
        compatibility_queries = self.load_compatibility_test_queries()
        
        version_responses = {}
        for version in model_versions:
            rag_system = self.initialize_rag_system(model_version=version)
            responses = {}
            
            for query in compatibility_queries:
                responses[query] = rag_system.process_query(query)
            
            version_responses[version] = responses
        
        # Validate backward compatibility
        for query in compatibility_queries:
            self.assert_backward_compatibility(
                version_responses, query
            )
    
    def test_configuration_compatibility(self):
        """Test compatibility across different configurations."""
        configurations = [
            {'retrieval_strategy': 'similarity', 'top_k': 5},
            {'retrieval_strategy': 'mmr', 'top_k': 3, 'diversity_threshold': 0.7},
            {'retrieval_strategy': 'hybrid', 'alpha': 0.5, 'top_k': 4}
        ]
        
        compatibility_results = {}
        for i, config in enumerate(configurations):
            rag_system = self.initialize_rag_system(config=config)
            results = self.run_standard_test_suite(rag_system)
            compatibility_results[f'config_{i}'] = results
        
        # Validate configuration compatibility
        self.assert_configuration_compatibility(compatibility_results)
```

### 2. Performance Regression Tests

#### Latency Regression Detection
```python
class LatencyRegressionTests:
    """Detect performance regressions in response time."""
    
    def test_query_processing_latency(self):
        """Test for latency regressions in query processing."""
        # Load baseline performance metrics
        baseline_metrics = self.load_baseline_performance_metrics()
        
        # Run current performance tests
        current_metrics = {}
        for query_type, queries in self.performance_test_queries.items():
            latencies = []
            
            for query in queries:
                start_time = time.time()
                response = self.rag_system.process_query(query)
                end_time = time.time()
                
                latency = end_time - start_time
                latencies.append(latency)
            
            current_metrics[query_type] = {
                'mean_latency': np.mean(latencies),
                'p95_latency': np.percentile(latencies, 95),
                'p99_latency': np.percentile(latencies, 99)
            }
        
        # Compare against baselines
        for query_type in current_metrics:
            self.assert_no_latency_regression(
                current_metrics[query_type],
                baseline_metrics[query_type],
                query_type
            )
    
    def test_throughput_regression(self):
        """Test for throughput regressions."""
        # Baseline throughput measurement
        baseline_throughput = self.load_baseline_throughput()
        
        # Current throughput measurement
        test_queries = self.generate_throughput_test_queries(1000)
        
        start_time = time.time()
        for query in test_queries:
            self.rag_system.process_query(query)
        end_time = time.time()
        
        current_throughput = len(test_queries) / (end_time - start_time)
        
        # Validate no significant throughput regression
        throughput_ratio = current_throughput / baseline_throughput
        self.assertGreater(
            throughput_ratio,
            self.THROUGHPUT_REGRESSION_THRESHOLD,
            f"Throughput regression detected: {throughput_ratio:.2%} of baseline"
        )
```

#### Resource Usage Regression
```python
class ResourceUsageRegressionTests:
    """Detect regressions in resource usage patterns."""
    
    def test_memory_usage_regression(self):
        """Test for memory usage regressions."""
        # Baseline memory usage
        baseline_memory = self.load_baseline_memory_usage()
        
        # Current memory usage measurement
        memory_tracker = MemoryTracker()
        
        # Run standard workload
        standard_queries = self.load_standard_workload_queries()
        
        memory_tracker.start_tracking()
        for query in standard_queries:
            self.rag_system.process_query(query)
        memory_usage = memory_tracker.get_peak_usage()
        
        # Validate memory usage
        memory_increase_ratio = memory_usage / baseline_memory['peak_usage']
        self.assertLess(
            memory_increase_ratio,
            self.MEMORY_REGRESSION_THRESHOLD,
            f"Memory usage regression: {memory_increase_ratio:.2%} increase"
        )
    
    def test_storage_usage_regression(self):
        """Test for storage usage regressions."""
        # Measure storage usage for same knowledge base
        test_knowledge_base = self.load_test_knowledge_base()
        
        # Index knowledge base
        storage_tracker = StorageTracker()
        storage_tracker.start_tracking()
        
        self.rag_system.index_knowledge_base(test_knowledge_base)
        
        current_storage = storage_tracker.get_total_usage()
        baseline_storage = self.load_baseline_storage_usage()
        
        storage_increase_ratio = current_storage / baseline_storage
        self.assertLess(
            storage_increase_ratio,
            self.STORAGE_REGRESSION_THRESHOLD,
            f"Storage usage regression: {storage_increase_ratio:.2%} increase"
        )
```

### 3. Quality Regression Tests

#### Accuracy Regression Detection
```python
class AccuracyRegressionTests:
    """Detect regressions in system accuracy metrics."""
    
    def test_retrieval_accuracy_regression(self):
        """Test for retrieval accuracy regressions."""
        # Load golden dataset with expected results
        golden_dataset = self.load_golden_retrieval_dataset()
        
        # Current retrieval accuracy
        current_results = []
        for test_case in golden_dataset:
            retrieved_docs = self.rag_system.retrieve_documents(
                test_case['query']
            )
            
            accuracy_metrics = self.calculate_retrieval_accuracy(
                retrieved_docs, test_case['expected_documents']
            )
            current_results.append(accuracy_metrics)
        
        # Compare against baseline accuracy
        baseline_accuracy = self.load_baseline_accuracy_metrics()
        current_accuracy = self.aggregate_accuracy_metrics(current_results)
        
        for metric_name, current_value in current_accuracy.items():
            baseline_value = baseline_accuracy[metric_name]
            regression_ratio = current_value / baseline_value
            
            self.assertGreater(
                regression_ratio,
                self.ACCURACY_REGRESSION_THRESHOLD,
                f"Accuracy regression in {metric_name}: "
                f"{regression_ratio:.2%} of baseline"
            )
    
    def test_generation_quality_regression(self):
        """Test for generation quality regressions."""
        quality_test_cases = self.load_generation_quality_test_cases()
        
        current_quality_scores = []
        for test_case in quality_test_cases:
            response = self.rag_system.process_query(test_case['query'])
            
            quality_score = self.evaluate_generation_quality(
                response, test_case['reference_answer']
            )
            current_quality_scores.append(quality_score)
        
        # Compare against baseline quality
        baseline_quality = self.load_baseline_generation_quality()
        current_avg_quality = np.mean(current_quality_scores)
        
        quality_ratio = current_avg_quality / baseline_quality
        self.assertGreater(
            quality_ratio,
            self.QUALITY_REGRESSION_THRESHOLD,
            f"Generation quality regression: {quality_ratio:.2%} of baseline"
        )
```

### 4. Breaking Change Detection

#### API Compatibility Tests
```python
class APICompatibilityTests:
    """Detect breaking changes in system API."""
    
    def test_query_interface_compatibility(self):
        """Test backward compatibility of query interface."""
        # Test legacy query formats
        legacy_query_formats = [
            {"query": "What is renewable energy?"},
            {"query": "Solar energy benefits", "context": "energy comparison"},
            {"query": "Wind power", "filters": {"category": "renewable"}},
        ]
        
        for query_format in legacy_query_formats:
            try:
                response = self.rag_system.process_legacy_query(query_format)
                self.assert_valid_response(response)
            except Exception as e:
                self.fail(f"Breaking change detected in query format: {e}")
    
    def test_response_format_compatibility(self):
        """Test backward compatibility of response format."""
        test_query = "Tell me about solar panels"
        response = self.rag_system.process_query(test_query)
        
        # Validate expected response structure
        expected_fields = ['content', 'sources', 'confidence', 'metadata']
        for field in expected_fields:
            self.assertIn(
                field, response,
                f"Breaking change: Missing field '{field}' in response"
            )
        
        # Validate field types haven't changed
        self.validate_response_field_types(response)
```

#### Configuration Schema Changes
```python
class ConfigurationSchemaTests:
    """Detect breaking changes in configuration schema."""
    
    def test_configuration_backward_compatibility(self):
        """Test that old configurations still work."""
        legacy_configurations = self.load_legacy_configurations()
        
        for config_version, config in legacy_configurations.items():
            try:
                rag_system = RAGSystem(config=config)
                
                # Test basic functionality with legacy config
                test_response = rag_system.process_query("test query")
                self.assert_valid_response(test_response)
                
            except Exception as e:
                self.fail(
                    f"Configuration breaking change detected in {config_version}: {e}"
                )
```

## Regression Test Automation

### Baseline Management System
```python
class BaselineManager:
    """Manages baseline data for regression testing."""
    
    def __init__(self, baseline_storage_path: str):
        self.storage_path = baseline_storage_path
        self.baseline_data = {}
    
    def create_baseline(self, version: str, test_results: Dict):
        """Create new baseline from test results."""
        baseline_entry = {
            'version': version,
            'timestamp': datetime.now().isoformat(),
            'performance_metrics': test_results.get('performance', {}),
            'quality_metrics': test_results.get('quality', {}),
            'response_samples': test_results.get('responses', {}),
            'system_config': test_results.get('config', {})
        }
        
        self.baseline_data[version] = baseline_entry
        self.save_baseline(version)
    
    def compare_with_baseline(self, current_results: Dict, baseline_version: str):
        """Compare current results with specified baseline."""
        baseline = self.load_baseline(baseline_version)
        
        comparison_results = {
            'performance_comparison': self.compare_performance(
                current_results, baseline
            ),
            'quality_comparison': self.compare_quality(
                current_results, baseline
            ),
            'regression_detected': False,
            'regressions': []
        }
        
        # Detect regressions
        regressions = self.detect_regressions(current_results, baseline)
        if regressions:
            comparison_results['regression_detected'] = True
            comparison_results['regressions'] = regressions
        
        return comparison_results
```

### Automated Regression Detection
```python
class RegressionDetector:
    """Automatically detects various types of regressions."""
    
    def __init__(self, thresholds_config: Dict):
        self.thresholds = thresholds_config
        self.detectors = {
            'performance': PerformanceRegressionDetector(thresholds_config),
            'quality': QualityRegressionDetector(thresholds_config),
            'consistency': ConsistencyRegressionDetector(thresholds_config)
        }
    
    def detect_all_regressions(self, current_data: Dict, baseline_data: Dict):
        """Run all regression detectors."""
        regression_results = {}
        
        for detector_name, detector in self.detectors.items():
            regressions = detector.detect_regressions(
                current_data, baseline_data
            )
            regression_results[detector_name] = regressions
        
        # Aggregate results
        all_regressions = []
        for detector_regressions in regression_results.values():
            all_regressions.extend(detector_regressions)
        
        return {
            'total_regressions': len(all_regressions),
            'regressions_by_type': regression_results,
            'all_regressions': all_regressions,
            'regression_detected': len(all_regressions) > 0
        }
```

### Continuous Regression Testing
```python
class ContinuousRegressionTesting:
    """Implements continuous regression testing pipeline."""
    
    def __init__(self, rag_system, config):
        self.rag_system = rag_system
        self.config = config
        self.baseline_manager = BaselineManager(config.baseline_storage_path)
        self.regression_detector = RegressionDetector(config.thresholds)
        self.notification_system = NotificationSystem(config.notifications)
    
    def run_regression_test_cycle(self):
        """Execute complete regression test cycle."""
        # Run current tests
        current_results = self.execute_test_suite()
        
        # Compare with baseline
        latest_baseline = self.baseline_manager.get_latest_baseline()
        comparison_results = self.baseline_manager.compare_with_baseline(
            current_results, latest_baseline['version']
        )
        
        # Detect regressions
        regression_analysis = self.regression_detector.detect_all_regressions(
            current_results, latest_baseline
        )
        
        # Generate report
        report = self.generate_regression_report(
            current_results, comparison_results, regression_analysis
        )
        
        # Handle regressions
        if regression_analysis['regression_detected']:
            self.handle_regression_detection(report)
        
        return report
    
    def handle_regression_detection(self, report):
        """Handle detected regressions."""
        # Send notifications
        self.notification_system.send_regression_alert(report)
        
        # Log detailed information
        self.log_regression_details(report)
        
        # Trigger remediation if configured
        if self.config.auto_remediation_enabled:
            self.trigger_remediation_workflow(report)
```

## Integration with CI/CD

### GitHub Actions Regression Testing
```yaml
name: Regression Testing

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    # Run regression tests daily
    - cron: '0 2 * * *'

jobs:
  regression-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r regression-test-requirements.txt
    
    - name: Download baseline data
      run: |
        python scripts/download_baseline_data.py --version=latest
    
    - name: Run regression tests
      run: |
        python -m pytest tests/regression/ \
          --baseline-version=latest \
          --generate-report \
          --junit-xml=regression-results.xml
    
    - name: Check for regressions
      run: |
        python scripts/analyze_regression_results.py \
          --results-file=regression-results.xml \
          --fail-on-regression
    
    - name: Upload regression report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: regression-report
        path: reports/regression-report.html
    
    - name: Comment on PR
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const report = fs.readFileSync('reports/regression-summary.md', 'utf8');
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: report
          });
```

## Regression Test Reporting

### Comprehensive Regression Report
```python
class RegressionReportGenerator:
    """Generates comprehensive regression test reports."""
    
    def generate_html_report(self, regression_results: Dict):
        """Generate HTML regression report."""
        template = self.load_report_template('regression_report.html')
        
        report_data = {
            'test_summary': self.generate_test_summary(regression_results),
            'performance_analysis': self.generate_performance_analysis(regression_results),
            'quality_analysis': self.generate_quality_analysis(regression_results),
            'regression_details': self.generate_regression_details(regression_results),
            'historical_trends': self.generate_historical_trends(regression_results),
            'recommendations': self.generate_recommendations(regression_results)
        }
        
        return template.render(**report_data)
    
    def generate_executive_summary(self, regression_results: Dict):
        """Generate executive summary of regression test results."""
        summary = {
            'overall_status': self.determine_overall_status(regression_results),
            'key_findings': self.extract_key_findings(regression_results),
            'critical_regressions': self.identify_critical_regressions(regression_results),
            'performance_impact': self.assess_performance_impact(regression_results),
            'recommended_actions': self.recommend_actions(regression_results)
        }
        
        return summary
```

## Best Practices

1. **Comprehensive Baseline Management**: Maintain detailed baselines for all metrics
2. **Automated Detection**: Implement automated regression detection with appropriate thresholds
3. **Historical Tracking**: Track regression trends over time
4. **Rapid Feedback**: Provide quick feedback on potential regressions
5. **Categorized Analysis**: Separate different types of regressions for targeted fixes
6. **Contextual Thresholds**: Use context-aware thresholds for different test scenarios
7. **Continuous Monitoring**: Run regression tests continuously, not just on releases

## Usage Examples

### Running Regression Tests
```bash
# Run complete regression test suite
python -m pytest tests/regression/ --baseline-version=v1.2.0

# Run specific regression test category
python -m pytest tests/regression/test_performance_regression.py

# Generate regression report
python scripts/generate_regression_report.py --output-format=html

# Compare with specific baseline
python scripts/regression_comparison.py --baseline=v1.1.0 --current=HEAD
```

### Creating New Baseline
```python
# Create baseline after successful release
baseline_manager = BaselineManager('baselines/')

# Run comprehensive test suite
test_results = run_comprehensive_test_suite()

# Create new baseline
baseline_manager.create_baseline('v1.3.0', test_results)

# Verify baseline creation
baseline = baseline_manager.load_baseline('v1.3.0')
assert baseline['version'] == 'v1.3.0'
```

This regression testing framework ensures your RAG system maintains consistent performance, quality, and behavior across versions and updates, catching regressions before they impact users.
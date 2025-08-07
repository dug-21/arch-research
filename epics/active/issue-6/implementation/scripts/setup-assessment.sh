#!/bin/bash

##############################################################################
# Assessment Setup Script
# Comprehensive environment setup for 8-week architecture assessment
##############################################################################

set -euo pipefail

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
IMPLEMENTATION_DIR="$PROJECT_ROOT/implementation"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Help function
show_help() {
    cat << EOF
Architecture Assessment Setup Script

USAGE:
    $0 [OPTIONS]

OPTIONS:
    --project NAME          Project name for the assessment
    --start-date DATE       Assessment start date (YYYY-MM-DD)
    --duration WEEKS        Assessment duration in weeks (default: 8)
    --team-size NUMBER      Assessment team size (default: 5)
    --environment ENV       Environment (dev/staging/prod, default: dev)
    --skip-deps            Skip dependency installation
    --skip-db              Skip database initialization
    --skip-tools           Skip tool setup
    --config-only          Only generate configuration files
    --help                 Show this help message

EXAMPLES:
    $0 --project "Enterprise Assessment" --start-date 2025-08-07
    $0 --project "Cloud Migration" --duration 12 --team-size 8
    $0 --environment prod --skip-deps

EOF
}

# Default values
PROJECT_NAME=""
START_DATE=$(date +%Y-%m-%d)
DURATION=8
TEAM_SIZE=5
ENVIRONMENT="dev"
SKIP_DEPS=false
SKIP_DB=false
SKIP_TOOLS=false
CONFIG_ONLY=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --project)
            PROJECT_NAME="$2"
            shift 2
            ;;
        --start-date)
            START_DATE="$2"
            shift 2
            ;;
        --duration)
            DURATION="$2"
            shift 2
            ;;
        --team-size)
            TEAM_SIZE="$2"
            shift 2
            ;;
        --environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --skip-deps)
            SKIP_DEPS=true
            shift
            ;;
        --skip-db)
            SKIP_DB=true
            shift
            ;;
        --skip-tools)
            SKIP_TOOLS=true
            shift
            ;;
        --config-only)
            CONFIG_ONLY=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Validate required parameters
if [[ -z "$PROJECT_NAME" ]]; then
    log_error "Project name is required. Use --project 'Your Project Name'"
    exit 1
fi

# Main setup function
main() {
    log_info "Starting Architecture Assessment Setup"
    log_info "Project: $PROJECT_NAME"
    log_info "Start Date: $START_DATE"
    log_info "Duration: $DURATION weeks"
    log_info "Team Size: $TEAM_SIZE"
    log_info "Environment: $ENVIRONMENT"
    echo

    # Create directory structure
    create_directory_structure

    # Generate configuration files
    generate_configuration_files

    if [[ "$CONFIG_ONLY" == "false" ]]; then
        # Install dependencies
        if [[ "$SKIP_DEPS" == "false" ]]; then
            install_dependencies
        fi

        # Initialize database
        if [[ "$SKIP_DB" == "false" ]]; then
            initialize_database
        fi

        # Setup tools and integrations
        if [[ "$SKIP_TOOLS" == "false" ]]; then
            setup_tools_and_integrations
        fi

        # Initialize monitoring and logging
        setup_monitoring_and_logging

        # Generate sample data and templates
        generate_sample_data
    fi

    # Final validation and summary
    validate_setup
    show_setup_summary

    log_success "Assessment environment setup completed successfully!"
}

# Create complete directory structure
create_directory_structure() {
    log_info "Creating directory structure..."

    # Create main directories
    mkdir -p "$IMPLEMENTATION_DIR"/{config,logs,data,reports,backups,temp}
    
    # Create subdirectories
    mkdir -p "$IMPLEMENTATION_DIR"/automation/{workflows,schedules,notifications}
    mkdir -p "$IMPLEMENTATION_DIR"/tools/{analyzers,generators,validators}
    mkdir -p "$IMPLEMENTATION_DIR"/scripts/{setup,maintenance,deployment}
    mkdir -p "$IMPLEMENTATION_DIR"/data-collection/{sources,processors,exporters}
    mkdir -p "$IMPLEMENTATION_DIR"/reporting/{templates,generators,dashboards}
    mkdir -p "$IMPLEMENTATION_DIR"/quality-assurance/{validators,checkers,metrics}
    mkdir -p "$IMPLEMENTATION_DIR"/integration/{apis,connectors,webhooks}
    
    # Create data directories
    mkdir -p "$IMPLEMENTATION_DIR"/data/{raw,processed,archived}
    mkdir -p "$IMPLEMENTATION_DIR"/data/raw/{systems,applications,infrastructure,stakeholders,documents,metrics}
    
    # Create report directories
    mkdir -p "$IMPLEMENTATION_DIR"/reports/{current-state,gap-analysis,future-state,implementation,executive}
    
    # Create config environment directories
    mkdir -p "$IMPLEMENTATION_DIR"/config/{dev,staging,prod}

    log_success "Directory structure created"
}

# Generate all configuration files
generate_configuration_files() {
    log_info "Generating configuration files..."

    # Main project configuration
    generate_main_config

    # Environment-specific configurations
    generate_environment_configs

    # Tool configurations
    generate_tool_configs

    # Database configuration
    generate_database_config

    # Package.json for Node.js dependencies
    generate_package_json

    # Python requirements.txt
    generate_python_requirements

    log_success "Configuration files generated"
}

# Generate main project configuration
generate_main_config() {
    cat > "$IMPLEMENTATION_DIR/config/project.json" << EOF
{
  "projectName": "$PROJECT_NAME",
  "version": "1.0.0",
  "startDate": "$START_DATE",
  "duration": $DURATION,
  "teamSize": $TEAM_SIZE,
  "environment": "$ENVIRONMENT",
  "phases": [
    {
      "name": "discovery",
      "startWeek": 1,
      "endWeek": 2,
      "focus": "Understanding the as-is architecture"
    },
    {
      "name": "analysis",
      "startWeek": 3,
      "endWeek": 4,
      "focus": "Deep analysis and gap identification"
    },
    {
      "name": "design",
      "startWeek": 5,
      "endWeek": 6,
      "focus": "Designing the target architecture"
    },
    {
      "name": "finalization",
      "startWeek": 7,
      "endWeek": 8,
      "focus": "Validation, refinement, and handover"
    }
  ],
  "deliverables": {
    "currentState": "Current state architecture documentation",
    "gapAnalysis": "Gap analysis report with prioritized recommendations",
    "futureState": "Future state architecture blueprints",
    "roadmap": "Implementation roadmap with phases and timelines",
    "executive": "Executive summary and presentation materials"
  },
  "automation": {
    "enabled": true,
    "orchestratorPath": "./automation/assessment-orchestrator.js",
    "dataCollectorPath": "./tools/data-collector.py",
    "reportGeneratorPath": "./reporting/report-generator.js"
  },
  "integrations": {
    "calendar": {
      "enabled": false,
      "provider": "outlook",
      "apiKey": ""
    },
    "documentation": {
      "enabled": false,
      "provider": "confluence",
      "baseUrl": "",
      "apiKey": ""
    },
    "monitoring": {
      "enabled": true,
      "logLevel": "info",
      "metricsEnabled": true
    }
  }
}
EOF
}

# Generate environment-specific configs
generate_environment_configs() {
    # Development environment
    cat > "$IMPLEMENTATION_DIR/config/dev/environment.json" << EOF
{
  "environment": "development",
  "database": {
    "path": "./data/assessment_dev.db",
    "type": "sqlite"
  },
  "api": {
    "port": 3000,
    "host": "localhost"
  },
  "logging": {
    "level": "debug",
    "file": "./logs/assessment-dev.log"
  },
  "features": {
    "mockData": true,
    "verboseLogging": true,
    "skipExternalAPIs": true
  }
}
EOF

    # Production environment
    cat > "$IMPLEMENTATION_DIR/config/prod/environment.json" << EOF
{
  "environment": "production",
  "database": {
    "path": "./data/assessment_prod.db",
    "type": "sqlite"
  },
  "api": {
    "port": 8080,
    "host": "0.0.0.0"
  },
  "logging": {
    "level": "info",
    "file": "./logs/assessment-prod.log"
  },
  "features": {
    "mockData": false,
    "verboseLogging": false,
    "skipExternalAPIs": false
  }
}
EOF
}

# Generate tool configurations
generate_tool_configs() {
    # Data collector configuration
    cat > "$IMPLEMENTATION_DIR/config/data-collector.yaml" << EOF
# Data Collector Configuration
project_name: "$PROJECT_NAME"
database: "./data/assessment_data.db"

# Data source configurations
data_sources:
  systems:
    enabled: true
    methods:
      - network_discovery
      - cmdb_query
      - cloud_apis
      - kubernetes
  
  applications:
    enabled: true
    methods:
      - apm_tools
      - service_registries
      - code_repositories
      - license_systems
  
  infrastructure:
    enabled: true
    methods:
      - monitoring_tools
      - cloud_metrics
      - virtualization
      - network_management
  
  stakeholders:
    enabled: true
    methods:
      - directory_services
      - hr_systems
      - project_tools
      - communication_platforms

# Collection schedules
schedules:
  daily_metrics: "0 0 * * *"    # Daily at midnight
  weekly_inventory: "0 0 * * 0" # Weekly on Sunday
  monthly_reports: "0 0 1 * *"  # Monthly on 1st

# Export settings
export:
  formats:
    - json
    - excel
  retention_days: 90
EOF
}

# Generate database configuration
generate_database_config() {
    cat > "$IMPLEMENTATION_DIR/config/database.json" << EOF
{
  "development": {
    "type": "sqlite",
    "path": "./data/assessment_dev.db",
    "options": {
      "enableWAL": true,
      "timeout": 30000
    }
  },
  "production": {
    "type": "sqlite",
    "path": "./data/assessment_prod.db",
    "options": {
      "enableWAL": true,
      "timeout": 30000
    }
  },
  "backup": {
    "enabled": true,
    "schedule": "0 2 * * *",
    "retention": 30,
    "path": "./backups"
  }
}
EOF
}

# Generate package.json
generate_package_json() {
    cat > "$IMPLEMENTATION_DIR/package.json" << EOF
{
  "name": "architecture-assessment",
  "version": "1.0.0",
  "description": "8-Week Architecture Assessment Implementation Framework",
  "main": "automation/assessment-orchestrator.js",
  "scripts": {
    "start": "node automation/assessment-orchestrator.js",
    "dashboard": "node reporting/dashboard-server.js",
    "collect": "python tools/data-collector.py",
    "test": "jest",
    "setup": "bash scripts/setup-assessment.sh",
    "validate": "node quality-assurance/validator.js"
  },
  "keywords": [
    "architecture",
    "assessment",
    "automation",
    "enterprise"
  ],
  "dependencies": {
    "express": "^4.18.0",
    "sqlite3": "^5.1.0",
    "node-cron": "^3.0.0",
    "axios": "^1.6.0",
    "fs-extra": "^11.0.0",
    "yaml": "^2.3.0",
    "lodash": "^4.17.0",
    "moment": "^2.29.0",
    "winston": "^3.8.0",
    "chart.js": "^4.4.0"
  },
  "devDependencies": {
    "jest": "^29.5.0",
    "nodemon": "^3.0.0",
    "eslint": "^8.57.0"
  },
  "author": "Architecture Assessment Team",
  "license": "MIT"
}
EOF
}

# Generate Python requirements
generate_python_requirements() {
    cat > "$IMPLEMENTATION_DIR/requirements.txt" << EOF
# Core dependencies
pandas>=2.0.0
numpy>=1.24.0
sqlalchemy>=2.0.0
pyyaml>=6.0
requests>=2.31.0

# Data analysis
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.17.0

# Database
sqlite3

# Utilities
python-dateutil>=2.8.0
click>=8.1.0
tqdm>=4.65.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0

# Linting
flake8>=6.0.0
black>=23.0.0
EOF
}

# Install dependencies
install_dependencies() {
    log_info "Installing dependencies..."

    # Check if Node.js is available
    if command -v node &> /dev/null; then
        log_info "Installing Node.js dependencies..."
        cd "$IMPLEMENTATION_DIR"
        npm install
        cd - > /dev/null
        log_success "Node.js dependencies installed"
    else
        log_warning "Node.js not found. Please install Node.js to use automation features."
    fi

    # Check if Python is available
    if command -v python3 &> /dev/null; then
        log_info "Installing Python dependencies..."
        cd "$IMPLEMENTATION_DIR"
        python3 -m pip install -r requirements.txt --user
        cd - > /dev/null
        log_success "Python dependencies installed"
    else
        log_warning "Python 3 not found. Please install Python 3 to use data collection features."
    fi
}

# Initialize database
initialize_database() {
    log_info "Initializing database..."

    if command -v python3 &> /dev/null; then
        cd "$IMPLEMENTATION_DIR"
        python3 -c "
from tools.data_collector import DataCollector
collector = DataCollector('config/data-collector.yaml')
print('Database initialized successfully')
"
        cd - > /dev/null
        log_success "Database initialized"
    else
        log_warning "Cannot initialize database without Python 3"
    fi
}

# Setup tools and integrations
setup_tools_and_integrations() {
    log_info "Setting up tools and integrations..."

    # Make scripts executable
    find "$IMPLEMENTATION_DIR/scripts" -name "*.sh" -exec chmod +x {} \;
    find "$IMPLEMENTATION_DIR/automation" -name "*.js" -exec chmod +x {} \;
    find "$IMPLEMENTATION_DIR/tools" -name "*.py" -exec chmod +x {} \;

    # Create symbolic links for easy access
    if [[ ! -f "$IMPLEMENTATION_DIR/assess" ]]; then
        cat > "$IMPLEMENTATION_DIR/assess" << 'EOF'
#!/bin/bash
# Assessment CLI wrapper
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
node "$SCRIPT_DIR/automation/assessment-orchestrator.js" "$@"
EOF
        chmod +x "$IMPLEMENTATION_DIR/assess"
    fi

    log_success "Tools and integrations setup completed"
}

# Setup monitoring and logging
setup_monitoring_and_logging() {
    log_info "Setting up monitoring and logging..."

    # Create log rotation configuration
    cat > "$IMPLEMENTATION_DIR/config/logrotate.conf" << EOF
$IMPLEMENTATION_DIR/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    copytruncate
}
EOF

    # Initialize log files
    touch "$IMPLEMENTATION_DIR/logs/assessment.log"
    touch "$IMPLEMENTATION_DIR/logs/data-collection.log"
    touch "$IMPLEMENTATION_DIR/logs/automation.log"

    log_success "Monitoring and logging setup completed"
}

# Generate sample data for testing
generate_sample_data() {
    log_info "Generating sample data and templates..."

    # Create sample system data
    cat > "$IMPLEMENTATION_DIR/data/raw/systems/sample-systems.json" << EOF
[
  {
    "name": "CRM System",
    "type": "application",
    "status": "active",
    "owner": "Sales Team",
    "version": "2.1.5",
    "criticality": "high"
  },
  {
    "name": "Web Server",
    "type": "infrastructure",
    "status": "active",
    "owner": "IT Team",
    "version": "Apache 2.4",
    "criticality": "critical"
  }
]
EOF

    # Create sample stakeholder data
    cat > "$IMPLEMENTATION_DIR/data/raw/stakeholders/sample-stakeholders.json" << EOF
[
  {
    "name": "John Smith",
    "role": "IT Director",
    "department": "Information Technology",
    "influence_level": "high",
    "availability": "limited"
  },
  {
    "name": "Sarah Johnson",
    "role": "Business Analyst",
    "department": "Business Operations",
    "influence_level": "medium",
    "availability": "good"
  }
]
EOF

    log_success "Sample data generated"
}

# Validate setup
validate_setup() {
    log_info "Validating setup..."

    local errors=0

    # Check directory structure
    required_dirs=(
        "$IMPLEMENTATION_DIR/config"
        "$IMPLEMENTATION_DIR/automation"
        "$IMPLEMENTATION_DIR/tools"
        "$IMPLEMENTATION_DIR/data"
        "$IMPLEMENTATION_DIR/logs"
    )

    for dir in "${required_dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            log_error "Missing directory: $dir"
            ((errors++))
        fi
    done

    # Check configuration files
    required_files=(
        "$IMPLEMENTATION_DIR/config/project.json"
        "$IMPLEMENTATION_DIR/package.json"
        "$IMPLEMENTATION_DIR/requirements.txt"
    )

    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_error "Missing file: $file"
            ((errors++))
        fi
    done

    if [[ $errors -eq 0 ]]; then
        log_success "Setup validation passed"
    else
        log_error "Setup validation failed with $errors errors"
        return 1
    fi
}

# Show setup summary
show_setup_summary() {
    echo
    echo "========================================"
    echo "  ASSESSMENT SETUP SUMMARY"
    echo "========================================"
    echo "Project Name: $PROJECT_NAME"
    echo "Start Date: $START_DATE"
    echo "Duration: $DURATION weeks"
    echo "Team Size: $TEAM_SIZE"
    echo "Environment: $ENVIRONMENT"
    echo
    echo "Implementation Directory: $IMPLEMENTATION_DIR"
    echo
    echo "Quick Start Commands:"
    echo "  Start Assessment:    cd $IMPLEMENTATION_DIR && npm start"
    echo "  Launch Dashboard:    cd $IMPLEMENTATION_DIR && npm run dashboard"
    echo "  Collect Data:        cd $IMPLEMENTATION_DIR && npm run collect"
    echo "  Run Validation:      cd $IMPLEMENTATION_DIR && npm run validate"
    echo
    echo "Configuration Files:"
    echo "  Main Config:         config/project.json"
    echo "  Data Collector:      config/data-collector.yaml"
    echo "  Environment:         config/$ENVIRONMENT/environment.json"
    echo
    echo "Next Steps:"
    echo "  1. Review and customize configuration files"
    echo "  2. Set up integrations with existing tools"
    echo "  3. Run initial data collection"
    echo "  4. Launch the assessment orchestrator"
    echo "========================================"
}

# Run main function
main "$@"
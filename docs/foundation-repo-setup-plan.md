# Foundation Repository Setup Plan
## Automated Dev/Test Environment for Rapid Project Deployment

**Created:** 2025-10-17
**Goal:** Create a cloneable foundation repository with 90%+ automation
**Timeline:** 3-5 days for core setup, 1-2 weeks for full customization
**Outcome:** 10-minute project setup vs 4-6 hours manual

---

## 🎯 Objectives

1. **One-command setup** - Clone, configure, deploy in under 10 minutes
2. **Multiple tech stacks** - Support for Node/TypeScript, Python, Go, Rust
3. **Zero-config deployment** - Push to main = auto-deploy to staging/production
4. **Quality gates** - Automated testing, linting, security scanning
5. **Documentation** - Auto-generated from code, always up-to-date

---

## 📋 Phase 1: Core Foundation (Days 1-2)

### Day 1 Morning: Repository Structure

**Goal:** Create the skeleton that all projects will inherit

```bash
foundation-template/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                 # Main CI pipeline
│   │   ├── deploy-staging.yml     # Auto-deploy to staging
│   │   ├── deploy-production.yml  # Manual deploy to prod
│   │   ├── security.yml           # Security scanning
│   │   └── docs.yml               # Documentation generation
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
├── .husky/                        # Git hooks
│   ├── pre-commit                 # Run before commit
│   └── pre-push                   # Run before push
├── scripts/
│   ├── setup.sh                   # Initial project setup
│   ├── dev.sh                     # Start dev environment
│   ├── test.sh                    # Run all tests
│   └── deploy.sh                  # Manual deployment
├── config/
│   ├── .eslintrc.js               # Linting rules
│   ├── .prettierrc                # Code formatting
│   ├── jest.config.js             # Testing config
│   └── tsconfig.json              # TypeScript config
├── docs/
│   ├── README.md                  # Auto-generated API docs
│   └── ARCHITECTURE.md            # System design
├── tests/
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   └── e2e/                       # End-to-end tests
├── .env.example                   # Environment template
├── .gitignore                     # Standard ignores
├── package.json                   # Node dependencies
├── Dockerfile                     # Container definition
├── docker-compose.yml             # Local dev environment
└── README.md                      # Setup instructions
```

**Action Items:**
1. Create new repo: `foundation-template` on GitHub
2. Initialize with Node.js (most versatile starting point)
3. Set up basic package.json with common dependencies
4. Create all directory structures

**Time Estimate:** 2-3 hours

### Day 1 Afternoon: GitHub Actions CI/CD

**Goal:** Automated testing and deployment on every push

**File: `.github/workflows/ci.yml`**
```yaml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linting
        run: npm run lint

      - name: Run type checking
        run: npm run typecheck

      - name: Run unit tests
        run: npm run test:unit

      - name: Run integration tests
        run: npm run test:integration

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

      - name: Build
        run: npm run build
```

**File: `.github/workflows/deploy-staging.yml`**
```yaml
name: Deploy to Staging

on:
  push:
    branches: [ develop ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Deploy to Vercel (Frontend)
        if: contains(github.repository, 'frontend')
        run: |
          npx vercel --token ${{ secrets.VERCEL_TOKEN }} --prod

      - name: Deploy to Fly.io (Backend)
        if: contains(github.repository, 'backend')
        run: |
          curl -L https://fly.io/install.sh | sh
          flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

**File: `.github/workflows/security.yml`**
```yaml
name: Security Scanning

on:
  push:
    branches: [ main, develop ]
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Snyk Security Scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Run Semgrep SAST
        uses: returntocorp/semgrep-action@v1
        with:
          config: auto

      - name: GitGuardian Secret Scan
        uses: GitGuardian/ggshield-action@v1
        env:
          GITGUARDIAN_API_KEY: ${{ secrets.GITGUARDIAN_API_KEY }}
```

**Action Items:**
1. Create all three workflow files
2. Set up GitHub secrets (VERCEL_TOKEN, FLY_API_TOKEN, etc.)
3. Test CI pipeline with a dummy commit
4. Verify all jobs pass

**Time Estimate:** 2-3 hours

### Day 2 Morning: Pre-commit Hooks & Code Quality

**Goal:** Catch issues before they reach CI

**File: `package.json` (scripts section)**
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint . --ext .ts,.tsx --fix",
    "lint:check": "eslint . --ext .ts,.tsx",
    "format": "prettier --write \"**/*.{ts,tsx,json,md}\"",
    "format:check": "prettier --check \"**/*.{ts,tsx,json,md}\"",
    "typecheck": "tsc --noEmit",
    "test": "jest",
    "test:unit": "jest --testPathPattern=tests/unit",
    "test:integration": "jest --testPathPattern=tests/integration",
    "test:e2e": "playwright test",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "prepare": "husky install"
  }
}
```

**File: `.husky/pre-commit`**
```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Run formatting check
npm run format:check || exit 1

# Run linting
npm run lint:check || exit 1

# Run type checking
npm run typecheck || exit 1

# Run unit tests (fast)
npm run test:unit || exit 1

echo "✅ Pre-commit checks passed!"
```

**File: `.husky/pre-push`**
```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Run all tests before pushing
npm run test || exit 1

echo "✅ Pre-push tests passed!"
```

**File: `config/.eslintrc.js`**
```javascript
module.exports = {
  extends: [
    'next/core-web-vitals',
    'plugin:@typescript-eslint/recommended',
    'prettier'
  ],
  rules: {
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/no-explicit-any': 'warn',
    'no-console': ['warn', { allow: ['warn', 'error'] }]
  }
}
```

**Action Items:**
1. Install husky: `npm install --save-dev husky`
2. Set up pre-commit hooks
3. Configure ESLint and Prettier
4. Test hooks with dummy commits

**Time Estimate:** 2 hours

### Day 2 Afternoon: Testing Framework Setup

**Goal:** Comprehensive test coverage with minimal setup

**File: `jest.config.js`**
```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests'],
  testMatch: ['**/*.test.ts', '**/*.spec.ts'],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.tsx'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts']
}
```

**File: `tests/setup.ts`**
```typescript
import '@testing-library/jest-dom'

// Global test setup
beforeAll(() => {
  console.log('🧪 Starting test suite...')
})

afterAll(() => {
  console.log('✅ Test suite complete!')
})
```

**File: `tests/unit/example.test.ts`**
```typescript
describe('Example Test Suite', () => {
  it('should pass basic assertion', () => {
    expect(true).toBe(true)
  })

  it('should perform math correctly', () => {
    expect(2 + 2).toBe(4)
  })
})
```

**File: `playwright.config.ts`** (for E2E tests)
```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

**Action Items:**
1. Install testing dependencies
2. Configure Jest and Playwright
3. Create example tests
4. Run and verify all tests pass

**Time Estimate:** 2-3 hours

---

## 📋 Phase 2: Deployment Automation (Day 3)

### Morning: Vercel Setup (Frontend)

**File: `vercel.json`**
```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm ci",
  "framework": "nextjs",
  "regions": ["iad1"],
  "env": {
    "NEXT_PUBLIC_API_URL": "@api-url"
  },
  "build": {
    "env": {
      "NEXT_PUBLIC_STAGE": "production"
    }
  }
}
```

**File: `.github/workflows/deploy-production.yml`**
```yaml
name: Deploy to Production

on:
  workflow_dispatch:  # Manual trigger only
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel Production
        run: |
          npx vercel --token ${{ secrets.VERCEL_TOKEN }} --prod
        env:
          VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
```

**Action Items:**
1. Create Vercel account (free tier)
2. Link repository to Vercel
3. Set up environment variables
4. Test deployment

**Time Estimate:** 1-2 hours

### Afternoon: Fly.io Setup (Backend)

**File: `fly.toml`**
```toml
app = "your-app-name"
primary_region = "iad"

[build]
  builder = "heroku/buildpacks:20"

[env]
  PORT = "8080"
  NODE_ENV = "production"

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"
  script_checks = []

  [services.concurrency]
    hard_limit = 25
    soft_limit = 20
    type = "connections"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

  [[services.tcp_checks]]
    grace_period = "1s"
    interval = "15s"
    restart_limit = 0
    timeout = "2s"
```

**File: `Dockerfile`**
```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./

EXPOSE 8080
CMD ["node", "dist/index.js"]
```

**Action Items:**
1. Install flyctl CLI
2. Create Fly.io account
3. Deploy test app
4. Configure secrets

**Time Estimate:** 2 hours

---

## 📋 Phase 3: Documentation & Tooling (Day 4)

### Morning: Auto-Documentation

**File: `.github/workflows/docs.yml`**
```yaml
name: Generate Documentation

on:
  push:
    branches: [ main ]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Generate API docs
        run: npm run docs:generate

      - name: Deploy docs to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

**File: `package.json` (add to scripts)**
```json
{
  "scripts": {
    "docs:generate": "typedoc --out docs src",
    "docs:serve": "npx serve docs"
  }
}
```

**File: `typedoc.json`**
```json
{
  "entryPoints": ["src"],
  "entryPointStrategy": "expand",
  "out": "docs",
  "exclude": ["**/*.test.ts", "**/*.spec.ts"],
  "plugin": ["typedoc-plugin-markdown"],
  "readme": "README.md"
}
```

**Action Items:**
1. Install TypeDoc
2. Configure documentation generation
3. Enable GitHub Pages
4. Test documentation build

**Time Estimate:** 2 hours

### Afternoon: Developer Experience Tools

**File: `scripts/setup.sh`**
```bash
#!/bin/bash
set -e

echo "🚀 Setting up your development environment..."

# Check Node.js version
required_version="20"
current_version=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)

if [ "$current_version" -lt "$required_version" ]; then
    echo "❌ Node.js version must be >= $required_version"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Copy environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

# Set up git hooks
echo "🪝 Setting up git hooks..."
npm run prepare

# Run initial tests
echo "🧪 Running tests..."
npm test

echo "✅ Setup complete! Run 'npm run dev' to start developing."
```

**File: `scripts/dev.sh`**
```bash
#!/bin/bash
set -e

echo "🔥 Starting development environment..."

# Start Docker services if needed
if [ -f docker-compose.yml ]; then
    echo "🐳 Starting Docker services..."
    docker-compose up -d
fi

# Start development server
npm run dev
```

**File: `.env.example`**
```bash
# Application
NODE_ENV=development
PORT=3000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/myapp

# API Keys (replace with your own)
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here

# External Services
VERCEL_TOKEN=
FLY_API_TOKEN=
SNYK_TOKEN=

# Feature Flags
ENABLE_ANALYTICS=false
ENABLE_DEBUG=true
```

**Action Items:**
1. Create setup and dev scripts
2. Make scripts executable: `chmod +x scripts/*.sh`
3. Test setup process
4. Document required environment variables

**Time Estimate:** 2 hours

---

## 📋 Phase 4: Advanced Features (Day 5)

### Morning: Database & Migrations

**File: `docker-compose.yml`**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: myapp
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

**File: `package.json` (add migration scripts)**
```json
{
  "scripts": {
    "db:migrate": "prisma migrate dev",
    "db:push": "prisma db push",
    "db:seed": "prisma db seed",
    "db:studio": "prisma studio"
  }
}
```

**Action Items:**
1. Set up Prisma or Drizzle ORM
2. Create initial migration
3. Add seed data
4. Test database operations

**Time Estimate:** 2-3 hours

### Afternoon: Monitoring & Observability

**File: `src/lib/monitoring.ts`**
```typescript
import * as Sentry from '@sentry/node'

export function initializeMonitoring() {
  if (process.env.SENTRY_DSN) {
    Sentry.init({
      dsn: process.env.SENTRY_DSN,
      environment: process.env.NODE_ENV,
      tracesSampleRate: 1.0,
    })
  }
}

export function logError(error: Error, context?: Record<string, any>) {
  console.error('Error:', error)
  if (process.env.NODE_ENV === 'production') {
    Sentry.captureException(error, { extra: context })
  }
}
```

**File: `.github/workflows/performance.yml`**
```yaml
name: Performance Testing

on:
  push:
    branches: [ main ]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v9
        with:
          urls: |
            https://your-staging-url.vercel.app
          uploadArtifacts: true
```

**Action Items:**
1. Set up Sentry for error tracking
2. Configure Lighthouse for performance
3. Add uptime monitoring (BetterUptime)
4. Test monitoring alerts

**Time Estimate:** 2 hours

---

## 📋 Phase 5: Multiple Template Variants (Week 2)

### Create Specialized Templates

**1. Next.js + Supabase (Full-Stack)**
```
foundation-nextjs-supabase/
├── All base configuration
├── app/                    # Next.js 14 App Router
├── components/             # React components
├── lib/supabase.ts        # Supabase client
└── middleware.ts          # Auth middleware
```

**2. Express + PostgreSQL (Backend API)**
```
foundation-express-api/
├── All base configuration
├── src/
│   ├── routes/            # API routes
│   ├── controllers/       # Business logic
│   ├── models/            # Data models
│   └── middleware/        # Express middleware
└── prisma/                # Database schema
```

**3. Python FastAPI (ML/AI Services)**
```
foundation-fastapi/
├── All base configuration (adapted for Python)
├── app/
│   ├── routers/           # API endpoints
│   ├── models/            # Pydantic models
│   └── services/          # Business logic
├── tests/
└── requirements.txt
```

**4. React Native (Mobile)**
```
foundation-react-native/
├── All base configuration
├── src/
│   ├── screens/           # App screens
│   ├── components/        # Reusable components
│   └── navigation/        # Navigation setup
└── app.json
```

**Action Items:**
1. Create 2-4 template variants
2. Customize workflows for each stack
3. Test each template end-to-end
4. Document stack-specific setup

**Time Estimate:** 3-5 days (1-2 days per template)

---

## 🎯 Usage Instructions (For Each New Project)

### Quick Start (10 minutes)

```bash
# 1. Clone the template
git clone https://github.com/yourusername/foundation-template.git my-new-project
cd my-new-project

# 2. Remove git history and reinitialize
rm -rf .git
git init
git add .
git commit -m "Initial commit from foundation template"

# 3. Run setup script
./scripts/setup.sh

# 4. Update project-specific details
# - Edit package.json (name, description)
# - Update README.md
# - Configure .env with your credentials
# - Update fly.toml and vercel.json with your app name

# 5. Create GitHub repository and push
gh repo create my-new-project --public --source=. --push

# 6. Set up deployment secrets
gh secret set VERCEL_TOKEN --body "$VERCEL_TOKEN"
gh secret set FLY_API_TOKEN --body "$FLY_API_TOKEN"

# 7. Start developing!
npm run dev
```

### First Deployment

```bash
# Push to develop branch to deploy to staging
git checkout -b develop
git push origin develop

# Create PR to main for production deployment
gh pr create --base main --head develop
```

---

## 🛠️ Tools & Services Setup

### Free Tier Accounts Needed

1. **GitHub** (already have)
   - Enable GitHub Actions
   - Set up GitHub Pages for docs

2. **Vercel** (Free tier)
   - Sign up: https://vercel.com
   - Connect GitHub account
   - Import project

3. **Fly.io** (Free tier: 3 VMs)
   - Sign up: https://fly.io
   - Install flyctl: `curl -L https://fly.io/install.sh | sh`
   - Login: `flyctl auth login`

4. **Supabase** (Free tier)
   - Sign up: https://supabase.com
   - Create project
   - Get API keys

5. **Sentry** (Free tier)
   - Sign up: https://sentry.io
   - Create project
   - Get DSN

6. **Snyk** (Free tier)
   - Sign up: https://snyk.io
   - Connect GitHub
   - Get API token

### Optional (Paid but Worth It)

7. **GitHub Copilot** ($10/month)
   - AI coding assistant
   - Massive productivity boost

8. **BetterUptime** ($20/month)
   - Uptime monitoring
   - Status pages

**Total Cost:** $0-50/month for free tiers, $30-100/month with paid tools

---

## ✅ Success Criteria

After setup, you should be able to:

- [ ] Clone template and set up new project in **<10 minutes**
- [ ] Push code and see it automatically **tested within 2 minutes**
- [ ] Deploy to staging on every push to develop (**auto**)
- [ ] Deploy to production with manual approval (**1 click**)
- [ ] See **80%+ test coverage** on every PR
- [ ] Get **security alerts** for vulnerabilities
- [ ] Access **auto-generated documentation** on GitHub Pages
- [ ] Monitor **errors and performance** in real-time
- [ ] Develop locally with **hot reload** and **type checking**
- [ ] Run entire test suite in **<30 seconds**

---

## 📊 Time Investment vs Returns

**Initial Setup:** 3-5 days full-time
**Per-Project Savings:** 4-6 hours → 10 minutes (95% time reduction)

**Break-even:** After 2-3 projects
**ROI at 10 projects:** 40-60 hours saved
**ROI at 50 projects:** 200-300 hours saved

**At $150/hour:** 40 hours = $6,000 saved

---

## 🚀 Next Steps

### Week 1 (This Week)
- [ ] **Day 1:** Set up foundation-template repository
- [ ] **Day 2:** Configure CI/CD and pre-commit hooks
- [ ] **Day 3:** Set up deployment to Vercel and Fly.io
- [ ] **Day 4:** Add documentation and developer scripts
- [ ] **Day 5:** Implement monitoring and database setup

### Week 2 (Next Week)
- [ ] Create Next.js + Supabase variant
- [ ] Create Express API variant
- [ ] Test both templates with real projects
- [ ] Document lessons learned

### Week 3 (Optional)
- [ ] Create Python FastAPI variant
- [ ] Create React Native variant
- [ ] Build internal documentation site
- [ ] Share templates publicly (GitHub stars!)

---

## 💡 Pro Tips

1. **Start Simple:** Get one template working perfectly before creating variants
2. **Test Thoroughly:** Use your template for a real project to find gaps
3. **Document Everything:** Future you will thank present you
4. **Automate Incrementally:** Don't try to automate everything on Day 1
5. **Use What Works:** Copy workflows from successful open-source projects

---

## 📚 Resources

- **GitHub Actions:** https://docs.github.com/actions
- **Vercel Docs:** https://vercel.com/docs
- **Fly.io Docs:** https://fly.io/docs
- **Husky (Git Hooks):** https://typicode.github.io/husky
- **TypeDoc:** https://typedoc.org
- **Playwright:** https://playwright.dev
- **Example Templates:**
  - Next.js: https://github.com/vercel/next.js/tree/canary/examples
  - T3 Stack: https://create.t3.gg
  - Bulletproof React: https://github.com/alan2207/bulletproof-react

---

## 🎯 Immediate Action (Right Now!)

```bash
# Create the foundation repository
cd ~/repos
mkdir foundation-template
cd foundation-template
git init

# Initialize Node.js project
npm init -y

# Install core dependencies
npm install --save-dev \
  typescript \
  @types/node \
  eslint \
  prettier \
  husky \
  jest \
  @playwright/test

# Create directory structure
mkdir -p .github/workflows .husky scripts config tests/{unit,integration,e2e} docs src

# You're ready to start building!
echo "✅ Foundation repository initialized!"
```

**Start with Day 1, complete each day in sequence, and you'll have a production-ready foundation in less than a week!**

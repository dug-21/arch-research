#!/usr/bin/env node

/**
 * Assessment Dashboard Server
 * Real-time dashboard for architecture assessment progress tracking
 */

const express = require('express');
const path = require('path');
const fs = require('fs').promises;
const sqlite3 = require('sqlite3').verbose();
const WebSocket = require('ws');
const http = require('http');

class DashboardServer {
    constructor(config) {
        this.config = config;
        this.app = express();
        this.server = http.createServer(this.app);
        this.wss = new WebSocket.Server({ server: this.server });
        this.db = null;
        this.clients = new Set();
        
        this.setupMiddleware();
        this.setupRoutes();
        this.setupWebSocket();
        this.setupDatabase();
    }

    setupMiddleware() {
        this.app.use(express.json());
        this.app.use(express.static(path.join(__dirname, 'public')));
        this.app.use('/assets', express.static(path.join(__dirname, 'assets')));
    }

    setupRoutes() {
        // Main dashboard page
        this.app.get('/', (req, res) => {
            res.sendFile(path.join(__dirname, 'templates/dashboard.html'));
        });

        // API Routes
        this.app.get('/api/status', this.getAssessmentStatus.bind(this));
        this.app.get('/api/progress', this.getProgress.bind(this));
        this.app.get('/api/metrics', this.getMetrics.bind(this));
        this.app.get('/api/stakeholders', this.getStakeholders.bind(this));
        this.app.get('/api/systems', this.getSystems.bind(this));
        this.app.get('/api/risks', this.getRisks.bind(this));
        this.app.get('/api/timeline', this.getTimeline.bind(this));
        this.app.get('/api/reports', this.getReports.bind(this));

        // Data update endpoints
        this.app.post('/api/update/progress', this.updateProgress.bind(this));
        this.app.post('/api/update/milestone', this.updateMilestone.bind(this));
        this.app.post('/api/update/risk', this.updateRisk.bind(this));

        // Export endpoints
        this.app.get('/api/export/progress', this.exportProgress.bind(this));
        this.app.get('/api/export/summary', this.exportSummary.bind(this));
    }

    setupWebSocket() {
        this.wss.on('connection', (ws) => {
            this.clients.add(ws);
            console.log('Client connected to dashboard');

            // Send initial data
            this.sendInitialData(ws);

            ws.on('close', () => {
                this.clients.delete(ws);
                console.log('Client disconnected from dashboard');
            });

            ws.on('error', (error) => {
                console.error('WebSocket error:', error);
                this.clients.delete(ws);
            });
        });
    }

    setupDatabase() {
        const dbPath = this.config.database || './data/assessment_data.db';
        this.db = new sqlite3.Database(dbPath);
        
        // Create dashboard-specific tables if they don't exist
        this.db.serialize(() => {
            this.db.run(`
                CREATE TABLE IF NOT EXISTS dashboard_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            `);

            this.db.run(`
                CREATE TABLE IF NOT EXISTS project_milestones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    milestone_name TEXT NOT NULL,
                    phase TEXT,
                    due_date DATE,
                    completion_date DATE,
                    status TEXT DEFAULT 'pending',
                    progress REAL DEFAULT 0
                )
            `);

            this.db.run(`
                CREATE TABLE IF NOT EXISTS risk_register (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    risk_name TEXT NOT NULL,
                    description TEXT,
                    category TEXT,
                    probability TEXT,
                    impact TEXT,
                    status TEXT DEFAULT 'identified',
                    mitigation_plan TEXT,
                    owner TEXT,
                    created_date DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            `);
        });
    }

    async sendInitialData(ws) {
        try {
            const initialData = {
                type: 'initial_data',
                data: {
                    status: await this.getAssessmentStatusData(),
                    progress: await this.getProgressData(),
                    metrics: await this.getMetricsData(),
                    timeline: await this.getTimelineData()
                }
            };

            ws.send(JSON.stringify(initialData));
        } catch (error) {
            console.error('Error sending initial data:', error);
        }
    }

    broadcastUpdate(type, data) {
        const message = JSON.stringify({ type, data });
        
        this.clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(message);
            }
        });
    }

    // API Route Handlers
    async getAssessmentStatus(req, res) {
        try {
            const status = await this.getAssessmentStatusData();
            res.json(status);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async getProgress(req, res) {
        try {
            const progress = await this.getProgressData();
            res.json(progress);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async getMetrics(req, res) {
        try {
            const metrics = await this.getMetricsData();
            res.json(metrics);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async getStakeholders(req, res) {
        try {
            const stakeholders = await this.getStakeholdersData();
            res.json(stakeholders);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async getSystems(req, res) {
        try {
            const systems = await this.getSystemsData();
            res.json(systems);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async getRisks(req, res) {
        try {
            const risks = await this.getRisksData();
            res.json(risks);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async getTimeline(req, res) {
        try {
            const timeline = await this.getTimelineData();
            res.json(timeline);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async getReports(req, res) {
        try {
            const reports = await this.getReportsData();
            res.json(reports);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    // Data Retrieval Methods
    async getAssessmentStatusData() {
        return new Promise((resolve, reject) => {
            const status = {
                projectName: this.config.projectName || 'Architecture Assessment',
                currentPhase: this.determineCurrentPhase(),
                overallProgress: 0,
                daysRemaining: this.calculateDaysRemaining(),
                teamUtilization: 85,
                budgetUtilization: 72,
                qualityScore: 92,
                stakeholderSatisfaction: 88
            };

            // Calculate overall progress from milestones
            this.db.all(
                'SELECT AVG(progress) as avg_progress FROM project_milestones',
                (err, rows) => {
                    if (err) {
                        reject(err);
                    } else {
                        status.overallProgress = rows[0]?.avg_progress || 0;
                        resolve(status);
                    }
                }
            );
        });
    }

    async getProgressData() {
        return new Promise((resolve, reject) => {
            const query = `
                SELECT 
                    milestone_name,
                    phase,
                    due_date,
                    completion_date,
                    status,
                    progress
                FROM project_milestones 
                ORDER BY due_date
            `;

            this.db.all(query, (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    const progress = {
                        milestones: rows,
                        phaseProgress: this.calculatePhaseProgress(rows),
                        upcomingDeadlines: this.getUpcomingDeadlines(rows),
                        completedTasks: rows.filter(r => r.status === 'completed').length,
                        totalTasks: rows.length
                    };
                    resolve(progress);
                }
            });
        });
    }

    async getMetricsData() {
        return new Promise((resolve, reject) => {
            const query = `
                SELECT metric_name, metric_value, timestamp
                FROM dashboard_metrics 
                WHERE timestamp > datetime('now', '-7 days')
                ORDER BY timestamp DESC
            `;

            this.db.all(query, (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    const metrics = {
                        systemsInventoried: this.getMetricValue(rows, 'systems_inventoried', 0),
                        applicationsAnalyzed: this.getMetricValue(rows, 'applications_analyzed', 0),
                        stakeholdersInterviewed: this.getMetricValue(rows, 'stakeholders_interviewed', 0),
                        documentsReviewed: this.getMetricValue(rows, 'documents_reviewed', 0),
                        gapsIdentified: this.getMetricValue(rows, 'gaps_identified', 0),
                        recommendationsMade: this.getMetricValue(rows, 'recommendations_made', 0),
                        trendsData: this.generateTrendsData(rows)
                    };
                    resolve(metrics);
                }
            });
        });
    }

    async getStakeholdersData() {
        return new Promise((resolve, reject) => {
            const query = `
                SELECT name, role, department, influence_level, 
                       availability, interview_status
                FROM stakeholders 
                ORDER BY influence_level DESC
            `;

            this.db.all(query, (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    }

    async getSystemsData() {
        return new Promise((resolve, reject) => {
            const query = `
                SELECT name, type, status, owner, last_updated
                FROM systems 
                ORDER BY name
            `;

            this.db.all(query, (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    }

    async getRisksData() {
        return new Promise((resolve, reject) => {
            const query = `
                SELECT risk_name, description, category, probability, 
                       impact, status, owner
                FROM risk_register 
                ORDER BY 
                    CASE probability 
                        WHEN 'high' THEN 3 
                        WHEN 'medium' THEN 2 
                        ELSE 1 
                    END DESC,
                    CASE impact 
                        WHEN 'high' THEN 3 
                        WHEN 'medium' THEN 2 
                        ELSE 1 
                    END DESC
            `;

            this.db.all(query, (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    }

    async getTimelineData() {
        const phases = [
            { name: 'Discovery', weeks: [1, 2], status: 'completed' },
            { name: 'Analysis', weeks: [3, 4], status: 'in-progress' },
            { name: 'Design', weeks: [5, 6], status: 'pending' },
            { name: 'Finalization', weeks: [7, 8], status: 'pending' }
        ];

        return {
            phases,
            currentWeek: this.getCurrentWeek(),
            milestones: await this.getProgressData()
        };
    }

    async getReportsData() {
        // Mock data for available reports
        return [
            { name: 'Current State Assessment', status: 'completed', date: '2025-08-05' },
            { name: 'Gap Analysis Report', status: 'in-progress', date: '2025-08-08' },
            { name: 'Future State Design', status: 'pending', date: '2025-08-12' },
            { name: 'Implementation Roadmap', status: 'pending', date: '2025-08-15' }
        ];
    }

    // Update Methods
    async updateProgress(req, res) {
        try {
            const { milestoneId, progress, status } = req.body;
            
            const query = `
                UPDATE project_milestones 
                SET progress = ?, status = ?, 
                    completion_date = CASE WHEN ? = 'completed' THEN datetime('now') ELSE NULL END
                WHERE id = ?
            `;

            this.db.run(query, [progress, status, status, milestoneId], function(err) {
                if (err) {
                    res.status(500).json({ error: err.message });
                } else {
                    // Broadcast update to all connected clients
                    this.broadcastUpdate('progress_update', { milestoneId, progress, status });
                    res.json({ success: true });
                }
            });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    // Utility Methods
    determineCurrentPhase() {
        const currentWeek = this.getCurrentWeek();
        if (currentWeek <= 2) return 'Discovery';
        if (currentWeek <= 4) return 'Analysis';
        if (currentWeek <= 6) return 'Design';
        return 'Finalization';
    }

    getCurrentWeek() {
        const startDate = new Date(this.config.startDate || new Date());
        const currentDate = new Date();
        const diffTime = Math.abs(currentDate - startDate);
        const diffWeeks = Math.ceil(diffTime / (7 * 24 * 60 * 60 * 1000));
        return Math.min(diffWeeks, 8);
    }

    calculateDaysRemaining() {
        const startDate = new Date(this.config.startDate || new Date());
        const endDate = new Date(startDate.getTime() + (this.config.duration || 8) * 7 * 24 * 60 * 60 * 1000);
        const currentDate = new Date();
        const diffTime = endDate - currentDate;
        return Math.max(0, Math.ceil(diffTime / (24 * 60 * 60 * 1000)));
    }

    calculatePhaseProgress(milestones) {
        const phases = ['Discovery', 'Analysis', 'Design', 'Finalization'];
        const phaseProgress = {};

        phases.forEach(phase => {
            const phaseMilestones = milestones.filter(m => m.phase === phase.toLowerCase());
            const avgProgress = phaseMilestones.length > 0 
                ? phaseMilestones.reduce((sum, m) => sum + m.progress, 0) / phaseMilestones.length
                : 0;
            phaseProgress[phase] = avgProgress;
        });

        return phaseProgress;
    }

    getUpcomingDeadlines(milestones) {
        const upcoming = milestones
            .filter(m => m.status !== 'completed' && new Date(m.due_date) > new Date())
            .sort((a, b) => new Date(a.due_date) - new Date(b.due_date))
            .slice(0, 5);
        
        return upcoming;
    }

    getMetricValue(rows, metricName, defaultValue) {
        const metric = rows.find(r => r.metric_name === metricName);
        return metric ? metric.metric_value : defaultValue;
    }

    generateTrendsData(rows) {
        // Group metrics by date and calculate trends
        const trends = {};
        rows.forEach(row => {
            const date = row.timestamp.split('T')[0];
            if (!trends[date]) trends[date] = {};
            trends[date][row.metric_name] = row.metric_value;
        });
        return trends;
    }

    async exportProgress(req, res) {
        try {
            const progress = await this.getProgressData();
            res.json({
                exportType: 'progress',
                timestamp: new Date().toISOString(),
                data: progress
            });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async exportSummary(req, res) {
        try {
            const summary = {
                status: await this.getAssessmentStatusData(),
                progress: await this.getProgressData(),
                metrics: await this.getMetricsData(),
                risks: await this.getRisksData()
            };

            res.json({
                exportType: 'summary',
                timestamp: new Date().toISOString(),
                data: summary
            });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    start(port = 3000) {
        this.server.listen(port, () => {
            console.log(`\n🚀 Assessment Dashboard Server running on http://localhost:${port}`);
            console.log(`📊 Real-time dashboard available at: http://localhost:${port}`);
            console.log(`🔌 WebSocket connection established for live updates`);
            console.log(`📈 API endpoints available at: http://localhost:${port}/api/`);
        });

        // Graceful shutdown
        process.on('SIGTERM', () => {
            console.log('SIGTERM received, shutting down gracefully');
            this.server.close(() => {
                this.db?.close();
                process.exit(0);
            });
        });
    }

    stop() {
        this.server.close();
        if (this.db) {
            this.db.close();
        }
    }
}

// CLI Interface and Startup
if (require.main === module) {
    const configPath = process.argv[2] || '../config/project.json';
    
    fs.readFile(configPath, 'utf8')
        .then(data => {
            const config = JSON.parse(data);
            const dashboard = new DashboardServer(config);
            
            const port = process.env.PORT || 3000;
            dashboard.start(port);
        })
        .catch(error => {
            console.error('Failed to start dashboard server:', error.message);
            process.exit(1);
        });
}

module.exports = DashboardServer;
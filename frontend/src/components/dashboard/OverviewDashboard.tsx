import React from 'react';
import { 
  Briefcase, 
  Cpu, 
  Target, 
  FileCheck, 
  Clock, 
  TrendingUp, 
  ArrowRight, 
  CheckCircle,
  ExternalLink,
  ShieldAlert
} from 'lucide-react';
import { Job, ApprovalRequest, AuditEvent, NavTab } from '../../types';

interface OverviewDashboardProps {
  jobs: Job[];
  approvals: ApprovalRequest[];
  events: AuditEvent[];
  onNavigate: (tab: NavTab) => void;
  onSelectJob: (job: Job) => void;
}

export const OverviewDashboard: React.FC<OverviewDashboardProps> = ({
  jobs,
  approvals,
  events,
  onNavigate,
  onSelectJob
}) => {
  const jobsDiscoveredCount = jobs.length;
  const jobsAnalyzedCount = jobs.filter(j => j.status === 'ANALYZED' || j.status === 'MATCHED' || j.status === 'COMPLETED').length;
  const matchingJobsCount = jobs.filter(j => (j.match_score || 0) >= 80).length;
  const resumesGeneratedCount = jobs.filter(j => j.status === 'MATCHED' || j.status === 'COMPLETED').length + 1;
  const pendingApprovalsCount = approvals.filter(a => a.status === 'PENDING').length;
  const successRate = jobsDiscoveredCount > 0 ? Math.round((jobsAnalyzedCount / jobsDiscoveredCount) * 100) : 100;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Metrics Row */}
      <div className="grid-metrics">
        <div className="card">
          <div className="metric-header">
            <span>Jobs Discovered</span>
            <Briefcase size={18} color="#6366f1" />
          </div>
          <div className="metric-value">{jobsDiscoveredCount}</div>
          <div className="metric-sub">Scraped via Playwright engine</div>
        </div>

        <div className="card">
          <div className="metric-header">
            <span>Jobs Analyzed</span>
            <Cpu size={18} color="#8b5cf6" />
          </div>
          <div className="metric-value">{jobsAnalyzedCount}</div>
          <div className="metric-sub">Processed by Aho-Corasick</div>
        </div>

        <div className="card">
          <div className="metric-header">
            <span>Matching Jobs</span>
            <Target size={18} color="#10b981" />
          </div>
          <div className="metric-value">{matchingJobsCount}</div>
          <div className="metric-sub">≥ 80% Skill Match Score</div>
        </div>

        <div className="card">
          <div className="metric-header">
            <span>Resumes Generated</span>
            <FileCheck size={18} color="#3b82f6" />
          </div>
          <div className="metric-value">{resumesGeneratedCount}</div>
          <div className="metric-sub">LaTeX compiled to PDF</div>
        </div>

        <div className="card">
          <div className="metric-header">
            <span>Pending Approvals</span>
            <Clock size={18} color="#f59e0b" />
          </div>
          <div className="metric-value">{pendingApprovalsCount}</div>
          <div className="metric-sub">Human-In-The-Loop Workspace</div>
        </div>

        <div className="card">
          <div className="metric-header">
            <span>Pipeline Success</span>
            <TrendingUp size={18} color="#10b981" />
          </div>
          <div className="metric-value">{successRate}%</div>
          <div className="metric-sub">LangGraph workflow uptime</div>
        </div>
      </div>

      {/* Main Grid: Recent Jobs + Activity Timeline */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1.75rem' }}>
        {/* Left Column: Recent Jobs Table */}
        <div className="card">
          <div className="section-header">
            <div>
              <h2 className="section-title">Recent Job Ingestions &amp; Matches</h2>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Playwright scrapers → Kafka event bus → LangGraph multi-agent pipeline
              </p>
            </div>
            <button 
              className="btn btn-secondary" 
              onClick={() => onNavigate('jobs')} 
              style={{ fontSize: '0.78rem', padding: '0.4rem 0.8rem' }}
            >
              View All Jobs <ArrowRight size={14} />
            </button>
          </div>

          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Job Title &amp; Company</th>
                  <th>Source</th>
                  <th>Match Score</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {jobs.slice(0, 5).map((job) => (
                  <tr key={job.id}>
                    <td>
                      <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{job.title}</div>
                      <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                        {job.company} — {job.location}
                      </div>
                    </td>
                    <td>
                      <span className="tag">{job.source}</span>
                    </td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <div 
                          style={{
                            width: '45px',
                            height: '6px',
                            background: 'rgba(255,255,255,0.1)',
                            borderRadius: '3px',
                            overflow: 'hidden'
                          }}
                        >
                          <div 
                            style={{
                              width: `${job.match_score || 0}%`,
                              height: '100%',
                              background: (job.match_score || 0) >= 85 ? '#10b981' : '#f59e0b'
                            }}
                          />
                        </div>
                        <span style={{ fontWeight: 700, fontSize: '0.85rem' }}>{job.match_score || 0}%</span>
                      </div>
                    </td>
                    <td>
                      <span className={`badge badge-${(job.status || 'MATCHED').toLowerCase()}`}>
                        {job.status || 'MATCHED'}
                      </span>
                    </td>
                    <td>
                      <button
                        className="btn btn-secondary"
                        onClick={() => {
                          onSelectJob(job);
                          onNavigate('job_intelligence');
                        }}
                        style={{ fontSize: '0.72rem', padding: '0.3rem 0.6rem' }}
                      >
                        Inspect <ExternalLink size={12} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right Column: Recent Pipeline Activity */}
        <div className="card">
          <div className="section-header">
            <div>
              <h2 className="section-title">Live Pipeline Events</h2>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Real-time Kafka &amp; Agent Stream</p>
            </div>
            <button 
              className="btn btn-secondary" 
              onClick={() => onNavigate('activity')}
              style={{ fontSize: '0.78rem', padding: '0.4rem 0.8rem' }}
            >
              Timeline
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {events.slice(0, 5).map((evt) => (
              <div 
                key={evt.id}
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '0.75rem',
                  padding: '0.75rem',
                  background: 'rgba(255,255,255,0.02)',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-color)'
                }}
              >
                <div style={{ marginTop: '2px', color: '#10b981' }}>
                  <CheckCircle size={15} />
                </div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', fontWeight: 600 }}>
                    <span style={{ color: '#a5b4fc' }}>{evt.event_type}</span>
                    <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                      {new Date(evt.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '2px', textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }}>
                    {evt.payload ? JSON.stringify(evt.payload) : evt.status}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Pending HITL Callout Banner */}
          {pendingApprovalsCount > 0 && (
            <div 
              style={{
                marginTop: '1.25rem',
                padding: '1rem',
                background: 'rgba(245, 158, 11, 0.12)',
                border: '1px solid rgba(245, 158, 11, 0.3)',
                borderRadius: 'var(--radius-md)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                <ShieldAlert size={18} color="#f59e0b" />
                <span style={{ fontSize: '0.82rem', fontWeight: 600, color: '#fbbf24' }}>
                  {pendingApprovalsCount} Approval Request Pending
                </span>
              </div>
              <button 
                className="btn btn-warning"
                onClick={() => onNavigate('approvals')}
                style={{ fontSize: '0.75rem', padding: '0.3rem 0.7rem', background: '#f59e0b', color: '#0f172a' }}
              >
                Review
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

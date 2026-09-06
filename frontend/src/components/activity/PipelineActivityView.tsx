import React, { useState } from 'react';
import { Activity, Clock, Cpu, Server, FileText, CheckSquare, Search } from 'lucide-react';
import { AuditEvent } from '../../types';

interface PipelineActivityViewProps {
  events: AuditEvent[];
  wsConnected: boolean;
}

const STEP_STEPS = [
  { key: 'job.discovered', label: 'Job Discovered', icon: Search, desc: 'Scraped via Playwright headless browser' },
  { key: 'kafka.event.published', label: 'Kafka Event Published', icon: Server, desc: 'Validated EventEnvelope emitted to Kafka' },
  { key: 'langgraph.processing.started', label: 'LangGraph Processing', icon: Cpu, desc: 'Multi-agent stateful graph execution' },
  { key: 'aho_corasick.keywords.extracted', label: 'Keywords Extracted', icon: Activity, desc: 'Deterministic Aho-Corasick automaton' },
  { key: 'resume.matched', label: 'Resume Matched', icon: FileText, desc: 'Candidate skill alignment matrix' },
  { key: 'tailored_resume.generated', label: 'Tailored Resume Generated', icon: FileText, desc: 'pdflatex dynamic PDF compilation' },
  { key: 'approval.awaiting_human_decision', label: 'Awaiting Human Approval', icon: Clock, desc: 'WebSocket HITL workspace stream' },
  { key: 'approval.approved', label: 'Approved & Finalized', icon: CheckSquare, desc: 'Governance decision complete' },
];

export const PipelineActivityView: React.FC<PipelineActivityViewProps> = ({
  events,
  wsConnected
}) => {
  const [selectedEvent, setSelectedEvent] = useState<AuditEvent | null>(null);
  const [filterType, setFilterType] = useState<string>('ALL');

  const filteredEvents = events.filter(e => filterType === 'ALL' || e.event_type === filterType);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Visual Pipeline Sequence Matrix Banner */}
      <div className="card">
        <div className="section-header" style={{ marginBottom: '1.5rem' }}>
          <div>
            <h2 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Activity size={20} color="#10b981" />
              Automated Multi-Agent Pipeline Execution Architecture
            </h2>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              Sequential state transition pipeline tracking event-driven execution flow
            </p>
          </div>

          <div className={`status-pill ${wsConnected ? 'online' : 'offline'}`}>
            <span className="pulse-dot" />
            <span>{wsConnected ? 'Live Events Socket Active' : 'Polling Backend REST'}</span>
          </div>
        </div>

        {/* Step-by-Step Flow Chart */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: '0.75rem' }}>
          {STEP_STEPS.map((step) => {
            const IconComp = step.icon;
            const hasOccurred = events.some(e => e.event_type === step.key);
            return (
              <div
                key={step.key}
                style={{
                  padding: '0.85rem 0.65rem',
                  background: hasOccurred ? 'rgba(16, 185, 129, 0.08)' : 'rgba(255, 255, 255, 0.02)',
                  border: hasOccurred ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-md)',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  textAlign: 'center',
                  gap: '0.4rem',
                  position: 'relative'
                }}
              >
                <div style={{ color: hasOccurred ? '#34d399' : 'var(--text-muted)' }}>
                  <IconComp size={20} />
                </div>
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: hasOccurred ? 'var(--text-primary)' : 'var(--text-muted)' }}>
                  {step.label}
                </span>
                <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)', lineHeight: 1.2 }}>
                  {step.desc}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Real-time Audit Trail Table */}
      <div className="card">
        <div className="section-header">
          <div>
            <h3 className="section-title">Kafka &amp; Agent Event Stream Log ({filteredEvents.length})</h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Detailed JSON payloads and correlation IDs</p>
          </div>

          <select
            className="form-select"
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            style={{ fontSize: '0.8rem' }}
          >
            <option value="ALL">All Pipeline Events</option>
            <option value="job.discovered">Job Discovered</option>
            <option value="kafka.event.published">Kafka Event</option>
            <option value="langgraph.processing.started">LangGraph Processing</option>
            <option value="aho_corasick.keywords.extracted">Aho-Corasick Extracted</option>
            <option value="approval.approved">Approved</option>
          </select>
        </div>

        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Event Type</th>
                <th>Correlation ID</th>
                <th>Status</th>
                <th>Timestamp</th>
                <th>Payload Summary</th>
              </tr>
            </thead>
            <tbody>
              {filteredEvents.map((evt) => (
                <tr 
                  key={evt.id}
                  onClick={() => setSelectedEvent(evt)}
                  style={{ cursor: 'pointer' }}
                >
                  <td>
                    <span style={{ fontWeight: 700, color: '#a5b4fc' }}>{evt.event_type}</span>
                  </td>
                  <td>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                      {evt.correlation_id || 'corr-system'}
                    </span>
                  </td>
                  <td>
                    <span className="badge badge-completed">{evt.status}</span>
                  </td>
                  <td>
                    <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                      {new Date(evt.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                    </span>
                  </td>
                  <td>
                    <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                      {evt.payload ? JSON.stringify(evt.payload).slice(0, 45) + '...' : 'N/A'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Payload Inspection Modal */}
      {selectedEvent && (
        <div className="modal-overlay" onClick={() => setSelectedEvent(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '600px' }}>
            <div className="modal-header">
              <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>Event Payload Inspector: {selectedEvent.event_type}</h3>
            </div>
            <div className="modal-body">
              <pre className="code-editor">
                <code>{JSON.stringify(selectedEvent, null, 2)}</code>
              </pre>
            </div>
            <div className="modal-footer">
              <button className="btn btn-secondary" onClick={() => setSelectedEvent(null)}>Close</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

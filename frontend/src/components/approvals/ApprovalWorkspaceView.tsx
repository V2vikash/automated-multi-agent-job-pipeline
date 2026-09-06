import React, { useState } from 'react';
import { 
  CheckCircle2, 
  XCircle, 
  RotateCcw, 
  Sparkles, 
  ShieldCheck, 
  MessageSquare,
  Radio
} from 'lucide-react';
import { ApprovalRequest } from '../../types';

interface ApprovalWorkspaceViewProps {
  approvals: ApprovalRequest[];
  jobs: any[];
  wsConnected: boolean;
  onRespondApproval: (id: string, decision: 'APPROVED' | 'REJECTED' | 'REVISION_REQUESTED', note?: string) => Promise<void>;
}

export const ApprovalWorkspaceView: React.FC<ApprovalWorkspaceViewProps> = ({
  approvals,
  wsConnected,
  onRespondApproval
}) => {
  const [selectedApproval, setSelectedApproval] = useState<ApprovalRequest | null>(approvals[0] || null);
  const [reviewerNote, setReviewerNote] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const activeReq = selectedApproval || approvals[0];

  const handleAction = async (decision: 'APPROVED' | 'REJECTED' | 'REVISION_REQUESTED') => {
    if (!activeReq) return;
    setIsSubmitting(true);
    try {
      await onRespondApproval(activeReq.id, decision, reviewerNote);
      setReviewerNote('');
    } finally {
      setIsSubmitting(false);
    }
  };

  const pendingApprovals = approvals.filter(a => a.status === 'PENDING');
  const pastApprovals = approvals.filter(a => a.status !== 'PENDING');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* HITL Header Banner */}
      <div className="card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ padding: '0.65rem', background: 'rgba(245, 158, 11, 0.15)', borderRadius: 'var(--radius-md)', color: '#fbbf24' }}>
            <ShieldCheck size={24} />
          </div>
          <div>
            <h2 style={{ fontSize: '1.15rem', fontWeight: 700, margin: 0 }}>Human-in-the-Loop (HITL) Governance Workspace</h2>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              Bi-directional WebSocket streaming endpoint `/api/v1/ws/notifications`
            </span>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div className={`status-pill ${wsConnected ? 'online' : 'offline'}`}>
            <Radio size={13} className={wsConnected ? 'pulse-dot' : ''} />
            <span>{wsConnected ? 'HITL WebSocket Active' : 'WebSocket Reconnecting'}</span>
          </div>
          <span className="badge badge-pending" style={{ fontSize: '0.8rem' }}>
            {pendingApprovals.length} Pending Approval
          </span>
        </div>
      </div>

      {/* Main Grid Layout: Approval Queue + Workspace Comparison */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2.5fr', gap: '1.75rem' }}>
        {/* Left Column: Requests Queue */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div className="card">
            <h3 className="section-title" style={{ fontSize: '0.95rem', marginBottom: '0.75rem' }}>
              Pending Decision Queue ({pendingApprovals.length})
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
              {pendingApprovals.map((appr) => {
                const isSelected = activeReq?.id === appr.id;
                return (
                  <div
                    key={appr.id}
                    onClick={() => setSelectedApproval(appr)}
                    style={{
                      padding: '0.85rem',
                      background: isSelected ? 'rgba(99, 102, 241, 0.14)' : 'rgba(0,0,0,0.2)',
                      border: isSelected ? '1px solid rgba(99, 102, 241, 0.5)' : '1px solid var(--border-color)',
                      borderRadius: 'var(--radius-md)',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease'
                    }}
                  >
                    <div style={{ fontWeight: 700, fontSize: '0.85rem', color: isSelected ? '#a5b4fc' : 'var(--text-primary)' }}>
                      {appr.job_title || 'Software Engineering Role'}
                    </div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', margin: '2px 0 6px' }}>
                      {appr.company || 'Enterprise Systems'}
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span className="badge badge-pending">PENDING</span>
                      <span style={{ fontWeight: 700, fontSize: '0.8rem', color: '#10b981' }}>{appr.match_score || 94}% Fit</span>
                    </div>
                  </div>
                );
              })}
              {pendingApprovals.length === 0 && (
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textAlign: 'center', padding: '1rem' }}>
                  No pending approval requests.
                </p>
              )}
            </div>

            {pastApprovals.length > 0 && (
              <>
                <h3 className="section-title" style={{ fontSize: '0.95rem', margin: '1.25rem 0 0.75rem' }}>
                  Decided History ({pastApprovals.length})
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {pastApprovals.map((appr) => (
                    <div
                      key={appr.id}
                      onClick={() => setSelectedApproval(appr)}
                      style={{
                        padding: '0.65rem 0.85rem',
                        background: 'rgba(0,0,0,0.15)',
                        border: '1px solid var(--border-subtle)',
                        borderRadius: 'var(--radius-md)',
                        cursor: 'pointer',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center'
                      }}
                    >
                      <span style={{ fontSize: '0.78rem', fontWeight: 600 }}>{appr.company}</span>
                      <span className={`badge badge-${appr.status.toLowerCase()}`}>{appr.status}</span>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        </div>

        {/* Right Column: Detailed Workspace & Actions */}
        {activeReq ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
            {/* Request Summary Card */}
            <div className="card">
              <div className="section-header">
                <div>
                  <h3 className="section-title">{activeReq.job_title}</h3>
                  <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                    Company: {activeReq.company} | Requested: {new Date(activeReq.requested_at || Date.now()).toLocaleTimeString()}
                  </span>
                </div>
                <span className="badge badge-matched" style={{ fontSize: '0.85rem' }}>
                  {activeReq.match_score || 94}% Candidate Score
                </span>
              </div>

              {/* System Automated Modifications Summary */}
              <div style={{ marginBottom: '1.5rem' }}>
                <h4 style={{ fontSize: '0.85rem', fontWeight: 600, color: '#a5b4fc', marginBottom: '0.6rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  <Sparkles size={16} /> Automated Multi-Agent Modifications Log
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                  {(activeReq.changes_made || [
                    'Tailored resume summary for target job requirements.',
                    'Injected Aho-Corasick algorithm keyword matching markers.',
                    'Compiled dynamic LaTeX source code into production PDF.'
                  ]).map((chg, idx) => (
                    <div 
                      key={idx}
                      style={{
                        padding: '0.5rem 0.8rem',
                        background: 'rgba(255,255,255,0.03)',
                        borderRadius: 'var(--radius-sm)',
                        fontSize: '0.82rem',
                        borderLeft: '3px solid #6366f1'
                      }}
                    >
                      {chg}
                    </div>
                  ))}
                </div>
              </div>

              {/* Extracted Tailored Keywords */}
              <div style={{ marginBottom: '1.5rem' }}>
                <h4 style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                  Tailored Keyword Highlights (Aho-Corasick Engine)
                </h4>
                <div className="tag-list">
                  {(activeReq.extracted_keywords || ['Python', 'FastAPI', 'PostgreSQL', 'Apache Kafka', 'LangGraph', 'Playwright', 'LaTeX']).map((kw) => (
                    <span key={kw} className="tag tag-success">{kw}</span>
                  ))}
                </div>
              </div>

              {/* LaTeX Code Preview */}
              <div style={{ marginBottom: '1.5rem' }}>
                <h4 style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                  Compiled LaTeX Source Preview
                </h4>
                <pre className="code-editor" style={{ maxHeight: '180px', overflowY: 'auto' }}>
                  <code>{activeReq.latex_source || '\\documentclass{article}\n\\begin{document}\nTailored Resume for Enterprise AI Systems...\n\\end{document}'}</code>
                </pre>
              </div>

              {/* Reviewer Note Input & Action Controls */}
              {activeReq.status === 'PENDING' ? (
                <div 
                  style={{
                    padding: '1.25rem',
                    background: 'rgba(0,0,0,0.3)',
                    borderRadius: 'var(--radius-md)',
                    border: '1px solid var(--border-glow)'
                  }}
                >
                  <div className="form-group">
                    <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                      <MessageSquare size={14} /> Reviewer Governance Notes (Optional)
                    </label>
                    <textarea
                      className="form-textarea"
                      rows={2}
                      placeholder="Add reviewer notes or revision instructions..."
                      value={reviewerNote}
                      onChange={(e) => setReviewerNote(e.target.value)}
                    />
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.85rem', marginTop: '1rem' }}>
                    <button 
                      className="btn btn-secondary"
                      onClick={() => handleAction('REVISION_REQUESTED')}
                      disabled={isSubmitting}
                      style={{ fontSize: '0.85rem' }}
                    >
                      <RotateCcw size={14} /> Request Revision
                    </button>

                    <button 
                      className="btn btn-danger"
                      onClick={() => handleAction('REJECTED')}
                      disabled={isSubmitting}
                      style={{ fontSize: '0.85rem' }}
                    >
                      <XCircle size={14} /> Reject Resume
                    </button>

                    <button 
                      className="btn btn-success"
                      onClick={() => handleAction('APPROVED')}
                      disabled={isSubmitting}
                      style={{ fontSize: '0.85rem' }}
                    >
                      <CheckCircle2 size={14} /> Approve &amp; Finalize
                    </button>
                  </div>
                </div>
              ) : (
                <div 
                  style={{
                    padding: '1rem',
                    background: activeReq.status === 'APPROVED' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                    borderRadius: 'var(--radius-md)',
                    border: `1px solid ${activeReq.status === 'APPROVED' ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between'
                  }}
                >
                  <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>
                    Decision Recorded: <span className={`badge badge-${activeReq.status.toLowerCase()}`}>{activeReq.status}</span>
                  </div>
                  {activeReq.reviewer_note && (
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                      Note: "{activeReq.reviewer_note}"
                    </span>
                  )}
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="card" style={{ padding: '3rem', textAlign: 'center' }}>
            <p style={{ color: 'var(--text-muted)' }}>No approval request selected.</p>
          </div>
        )}
      </div>
    </div>
  );
};

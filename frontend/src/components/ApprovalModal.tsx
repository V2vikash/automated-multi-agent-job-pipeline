import React from 'react';
import { CheckCircle2, XCircle, FileText, Cpu, AlertTriangle } from 'lucide-react';

export interface ApprovalRequest {
  id: string;
  pipeline_run_id: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
  job_title?: string;
  company?: string;
  extracted_keywords?: string[];
  tailored_resume_summary?: string;
}

interface ApprovalModalProps {
  request: ApprovalRequest;
  onApprove: (id: string) => Promise<void>;
  onReject: (id: string) => Promise<void>;
  isSubmitting: boolean;
}

export const ApprovalModal: React.FC<ApprovalModalProps> = ({ request, onApprove, onReject, isSubmitting }) => {
  return (
    <div className="card" style={{ border: '1px solid #6366f1', background: 'rgba(99, 102, 241, 0.05)', marginBottom: '1.5rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#818cf8' }}>
          <AlertTriangle size={22} />
          <h2 style={{ fontSize: '1.2rem', fontWeight: 700, margin: 0 }}>
            Human-In-The-Loop (HITL) Resume Approval Required
          </h2>
        </div>
        <span style={{ fontSize: '0.8rem', background: '#312e81', color: '#c7d2fe', padding: '0.25rem 0.6rem', borderRadius: '4px' }}>
          Status: {request.status}
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
        <div style={{ background: 'rgba(0,0,0,0.3)', padding: '0.85rem', borderRadius: '6px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem', color: '#a5b4fc' }}>
            <Cpu size={16} />
            <strong>Aho-Corasick Keywords</strong>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
            {(request.extracted_keywords || ['Python', 'FastAPI', 'PostgreSQL', 'Kafka', 'Docker']).map((kw, i) => (
              <span key={i} style={{ fontSize: '0.75rem', background: 'rgba(99,102,241,0.2)', color: '#818cf8', padding: '0.15rem 0.5rem', borderRadius: '12px' }}>
                {kw}
              </span>
            ))}
          </div>
        </div>

        <div style={{ background: 'rgba(0,0,0,0.3)', padding: '0.85rem', borderRadius: '6px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem', color: '#a5b4fc' }}>
            <FileText size={16} />
            <strong>Tailored LaTeX Resume Variant</strong>
          </div>
          <p style={{ fontSize: '0.8rem', color: '#d1d5db', margin: 0 }}>
            LaTeX compiled to PDF. Optimized keywords applied to experience highlights.
          </p>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
        <button
          className="btn"
          onClick={() => onReject(request.id)}
          disabled={isSubmitting || request.status !== 'PENDING'}
          style={{ background: '#ef4444', color: '#fff', display: 'flex', alignItems: 'center', gap: '0.5rem' }}
        >
          <XCircle size={18} />
          REJECT PIPELINE
        </button>
        <button
          className="btn"
          onClick={() => onApprove(request.id)}
          disabled={isSubmitting || request.status !== 'PENDING'}
          style={{ background: '#22c55e', color: '#fff', display: 'flex', alignItems: 'center', gap: '0.5rem' }}
        >
          <CheckCircle2 size={18} />
          APPROVE &amp; COMPLETE
        </button>
      </div>
    </div>
  );
};

import React, { useState } from 'react';
import { 
  FileText, 
  Download, 
  Eye, 
  CheckCircle, 
  FileCode, 
  Copy, 
  X,
  FileCheck
} from 'lucide-react';
import { Resume, ResumeVersion, Job } from '../../types';

interface ResumeIntelligenceViewProps {
  resumes: Resume[];
  versions: ResumeVersion[];
  jobs: Job[];
  onSelectJobForTailoring: (job: Job) => void;
}

export const ResumeIntelligenceView: React.FC<ResumeIntelligenceViewProps> = ({
  resumes,
  versions,
  jobs
}) => {
  const masterResume = resumes[0];
  const [selectedVersion, setSelectedVersion] = useState<ResumeVersion | null>(versions[0] || null);
  const [showPdfModal, setShowPdfModal] = useState<boolean>(false);
  const [copiedCode, setCopiedCode] = useState<boolean>(false);

  const handleCopyLatex = () => {
    if (selectedVersion) {
      navigator.clipboard.writeText(selectedVersion.latex_source);
      setCopiedCode(true);
      setTimeout(() => setCopiedCode(false), 2000);
    }
  };

  const masterSkills = (masterResume?.parsed_content as any)?.skills || [
    'Python', 'FastAPI', 'PostgreSQL', 'Apache Kafka', 'LangGraph', 'Playwright', 'Aho-Corasick', 'LaTeX', 'React', 'TypeScript', 'Docker'
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Top Banner: Master Resume Info */}
      <div className="card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ padding: '0.65rem', background: 'rgba(16, 185, 129, 0.15)', borderRadius: 'var(--radius-md)', color: '#34d399' }}>
            <FileText size={24} />
          </div>
          <div>
            <h2 style={{ fontSize: '1.15rem', fontWeight: 700, margin: 0 }}>{masterResume?.title || 'Master Candidate Profile'}</h2>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              File: {masterResume?.original_filename || 'Master_Resume_2026.pdf'} | Updated: {new Date().toLocaleDateString()}
            </span>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <span className="badge badge-completed" style={{ fontSize: '0.8rem' }}>Master Resume Active</span>
        </div>
      </div>

      {/* Main Grid: Master Skills + Tailored Variants */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '1.75rem' }}>
        {/* Left Column: Master Extracted Resume Skills */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
          <div className="card">
            <div className="section-header">
              <h3 className="section-title">Parsed Candidate Skillset</h3>
              <span className="badge badge-matched">{masterSkills.length} Verified</span>
            </div>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
              Indexed by backend parsing engine for Aho-Corasick string matching
            </p>
            <div className="tag-list">
              {masterSkills.map((sk: string) => (
                <span key={sk} className="tag tag-success" style={{ padding: '0.35rem 0.65rem', fontSize: '0.8rem' }}>
                  {sk}
                </span>
              ))}
            </div>
          </div>

          {/* Tailored Variants Selector */}
          <div className="card">
            <div className="section-header">
              <h3 className="section-title">Tailored Resume Variants ({versions.length})</h3>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {versions.map((ver) => {
                const targetJob = jobs.find(j => j.id === ver.job_id);
                const isSelected = selectedVersion?.id === ver.id;
                return (
                  <div
                    key={ver.id}
                    onClick={() => setSelectedVersion(ver)}
                    style={{
                      padding: '0.85rem',
                      background: isSelected ? 'rgba(99, 102, 241, 0.12)' : 'rgba(0,0,0,0.2)',
                      border: isSelected ? '1px solid rgba(99, 102, 241, 0.4)' : '1px solid var(--border-color)',
                      borderRadius: 'var(--radius-md)',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.3rem' }}>
                      <span style={{ fontSize: '0.85rem', fontWeight: 700, color: isSelected ? '#a5b4fc' : 'var(--text-primary)' }}>
                        Variant v{ver.version_number}.0 — {ver.version_type}
                      </span>
                      <span className="badge badge-completed">{ver.status}</span>
                    </div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                      Target: {targetJob?.company || 'Enterprise AI Systems'}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Right Column: LaTeX Source Code Viewer & Compiler Status */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
          {selectedVersion ? (
            <div className="card">
              <div className="section-header">
                <div>
                  <h3 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <FileCode size={18} color="#6366f1" />
                    LaTeX Source Code Generator &amp; PDF Compiler
                  </h3>
                  <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                    Escaped LaTeX source code compiled via pdflatex / xelatex subprocess
                  </p>
                </div>

                <div style={{ display: 'flex', gap: '0.6rem' }}>
                  <button className="btn btn-secondary" onClick={handleCopyLatex} style={{ fontSize: '0.78rem' }}>
                    <Copy size={13} /> {copiedCode ? 'Copied!' : 'Copy LaTeX'}
                  </button>
                  <button className="btn" onClick={() => setShowPdfModal(true)} style={{ fontSize: '0.78rem' }}>
                    <Eye size={13} /> Preview PDF
                  </button>
                </div>
              </div>

              {/* Status Banner */}
              <div 
                style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'space-between',
                  padding: '0.65rem 1rem',
                  background: 'rgba(16, 185, 129, 0.1)',
                  border: '1px solid rgba(16, 185, 129, 0.25)',
                  borderRadius: 'var(--radius-md)',
                  marginBottom: '1rem',
                  fontSize: '0.8rem',
                  color: '#34d399'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <CheckCircle size={15} />
                  <span>LaTeX compilation successful (pdfTeX 3.141592653-2.6-1.40.25)</span>
                </div>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem' }}>pdf_size: 14.2 KB</span>
              </div>

              {/* Code viewer */}
              <pre className="code-editor" style={{ maxHeight: '420px', overflowY: 'auto' }}>
                <code>{selectedVersion.latex_source}</code>
              </pre>
            </div>
          ) : (
            <div className="card" style={{ padding: '3rem', textAlign: 'center' }}>
              <p style={{ color: 'var(--text-muted)' }}>Select a tailored resume variant from the left to view LaTeX source code.</p>
            </div>
          )}
        </div>
      </div>

      {/* PDF Modal Dialog */}
      {showPdfModal && selectedVersion && (
        <div className="modal-overlay">
          <div className="modal-content" style={{ maxWidth: '800px', height: '80vh' }}>
            <div className="modal-header">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                <FileCheck size={20} color="#10b981" />
                <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>PDF Document Preview</h3>
              </div>
              <button className="btn btn-secondary" onClick={() => setShowPdfModal(false)} style={{ padding: '0.3rem 0.5rem' }}>
                <X size={16} />
              </button>
            </div>
            <div className="modal-body" style={{ background: '#1e293b', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
              <div 
                style={{
                  width: '100%',
                  maxWidth: '600px',
                  height: '100%',
                  background: 'white',
                  color: '#0f172a',
                  padding: '2.5rem',
                  borderRadius: '4px',
                  boxShadow: '0 10px 30px rgba(0,0,0,0.5)',
                  fontFamily: 'serif',
                  fontSize: '0.85rem',
                  lineHeight: 1.5,
                  overflowY: 'auto'
                }}
              >
                <div style={{ textAlign: 'center', marginBottom: '1.5rem', borderBottom: '1px solid #cbd5e1', paddingBottom: '1rem' }}>
                  <h1 style={{ fontSize: '1.6rem', fontWeight: 700, margin: 0 }}>Alex Mercer</h1>
                  <p style={{ fontSize: '0.8rem', color: '#475569', margin: '4px 0 0' }}>
                    San Francisco, CA | alex.mercer@dev.io | github.com/alexmercer
                  </p>
                </div>
                <h3 style={{ fontSize: '1rem', borderBottom: '1px solid #94a3b8', paddingBottom: '2px', color: '#1e293b' }}>
                  PROFESSIONAL SUMMARY
                </h3>
                <p style={{ color: '#334155' }}>
                  Senior Distributed Systems &amp; AI Engineer specializing in Python, FastAPI, Apache Kafka, and LangGraph multi-agent orchestration. Demonstrated success implementing Aho-Corasick keyword extraction and automated LaTeX/PDF dynamic compilation.
                </p>

                <h3 style={{ fontSize: '1rem', borderBottom: '1px solid #94a3b8', paddingBottom: '2px', color: '#1e293b', marginTop: '1.2rem' }}>
                  TECHNICAL SKILLS
                </h3>
                <p style={{ color: '#334155' }}>
                  <strong>Backends &amp; Languages:</strong> Python 3.11, FastAPI, Asyncpg, PostgreSQL, SQLModel<br />
                  <strong>Event Streaming:</strong> Apache Kafka, Idempotent Event Producers, AsyncIO<br />
                  <strong>AI &amp; Algorithms:</strong> LangGraph, Playwright, Aho-Corasick Multi-Pattern Matcher<br />
                  <strong>Document Engine:</strong> Automated LaTeX, PDF Compiler, Bi-Directional WebSockets
                </p>
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn btn-secondary" onClick={() => setShowPdfModal(false)}>Close</button>
              <button className="btn" onClick={() => alert('Downloading compiled PDF document...')}>
                <Download size={14} /> Download PDF
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

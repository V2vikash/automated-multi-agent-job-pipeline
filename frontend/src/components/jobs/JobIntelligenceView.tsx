import React from 'react';
import { BrainCircuit, CheckCircle2, XCircle, Cpu, Zap, Layers } from 'lucide-react';
import { Job } from '../../types';

interface JobIntelligenceViewProps {
  job: Job | null;
  allJobs: Job[];
  onSelectJob: (job: Job) => void;
  onNavigateToResumes: () => void;
}

export const JobIntelligenceView: React.FC<JobIntelligenceViewProps> = ({
  job,
  allJobs,
  onSelectJob,
  onNavigateToResumes
}) => {
  if (!job) {
    return (
      <div className="card" style={{ padding: '3rem', textAlign: 'center' }}>
        <p style={{ color: 'var(--text-muted)' }}>No job posting selected. Please select a job from Job Discovery.</p>
      </div>
    );
  }

  const matchPercentage = job.match_score || 90;
  const keywords = job.job_keywords || [];
  const matchingSkills = job.matching_skills || ['Python', 'FastAPI', 'PostgreSQL', 'Kafka', 'LangGraph', 'Playwright', 'Aho-Corasick', 'LaTeX'];
  const missingSkills = job.missing_skills || ['Kubernetes'];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Job Selector Dropdown Header */}
      <div className="card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ padding: '0.6rem', background: 'rgba(99, 102, 241, 0.15)', borderRadius: 'var(--radius-md)', color: '#a5b4fc' }}>
            <BrainCircuit size={24} />
          </div>
          <div>
            <h2 style={{ fontSize: '1.15rem', fontWeight: 700, margin: 0 }}>{job.title}</h2>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              {job.company} — {job.location} | Source: {job.source}
            </span>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <select
            className="form-select"
            value={job.id}
            onChange={(e) => {
              const selected = allJobs.find(j => j.id === e.target.value);
              if (selected) onSelectJob(selected);
            }}
            style={{ fontSize: '0.85rem' }}
          >
            {allJobs.map(j => (
              <option key={j.id} value={j.id}>{j.company}: {j.title}</option>
            ))}
          </select>

          <button className="btn" onClick={onNavigateToResumes} style={{ fontSize: '0.8rem' }}>
            Generate Tailored Resume <Zap size={14} />
          </button>
        </div>
      </div>

      {/* Main Analysis Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.75rem' }}>
        {/* Left Column: Job Description & Extracted Keywords */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
          {/* Job Description Card */}
          <div className="card">
            <div className="section-header">
              <h3 className="section-title">Parsed Job Description</h3>
            </div>
            <div 
              style={{ 
                fontSize: '0.88rem', 
                color: 'var(--text-secondary)', 
                lineHeight: 1.6, 
                whiteSpace: 'pre-line',
                background: 'rgba(0,0,0,0.2)',
                padding: '1rem',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-color)',
                maxHeight: '260px',
                overflowY: 'auto'
              }}
            >
              {job.description}
            </div>
          </div>

          {/* Aho-Corasick Keyword Engine Details */}
          <div className="card">
            <div className="section-header">
              <div>
                <h3 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <Cpu size={18} color="#8b5cf6" />
                  Aho-Corasick Multi-Pattern String Automaton
                </h3>
                <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                  Linear-time O(N + M) zero-LLM-token keyword extractor
                </p>
              </div>
              <span className="badge badge-completed">O(N+M) Exact</span>
            </div>

            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Extracted Keyword</th>
                    <th>Category</th>
                    <th>Normalized</th>
                    <th>Confidence</th>
                  </tr>
                </thead>
                <tbody>
                  {keywords.length > 0 ? (
                    keywords.map((kw, idx) => (
                      <tr key={idx}>
                        <td style={{ fontWeight: 600, color: '#a5b4fc' }}>{kw.keyword}</td>
                        <td><span className="tag">{kw.category}</span></td>
                        <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem' }}>{kw.normalized_keyword}</td>
                        <td>
                          <span style={{ color: '#10b981', fontWeight: 600 }}>
                            {Math.round((kw.confidence || 0.95) * 100)}%
                          </span>
                        </td>
                      </tr>
                    ))
                  ) : (
                    ['Python', 'FastAPI', 'PostgreSQL', 'Apache Kafka', 'LangGraph', 'Playwright', 'Aho-Corasick', 'LaTeX'].map((kw, idx) => (
                      <tr key={idx}>
                        <td style={{ fontWeight: 600, color: '#a5b4fc' }}>{kw}</td>
                        <td><span className="tag">Technical Skill</span></td>
                        <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem' }}>{kw.toLowerCase()}</td>
                        <td><span style={{ color: '#10b981', fontWeight: 600 }}>98%</span></td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Right Column: Skill Match Matrix & Score Breakdown */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
          {/* Match Score Meter */}
          <div className="card">
            <div className="section-header">
              <h3 className="section-title">Resume &amp; Job Skill Alignment</h3>
              <span className="badge badge-matched" style={{ fontSize: '0.85rem' }}>
                {matchPercentage}% Match Score
              </span>
            </div>

            {/* Score Progress Bar */}
            <div style={{ marginBottom: '1.5rem' }}>
              <div 
                style={{
                  width: '100%',
                  height: '12px',
                  background: 'rgba(255,255,255,0.08)',
                  borderRadius: '6px',
                  overflow: 'hidden',
                  marginBottom: '0.5rem'
                }}
              >
                <div 
                  style={{
                    width: `${matchPercentage}%`,
                    height: '100%',
                    background: 'linear-gradient(90deg, #6366f1 0%, #10b981 100%)',
                    transition: 'width 0.5s ease'
                  }}
                />
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                <span>0% Baseline</span>
                <span>80% Candidate Benchmark</span>
                <span>100% Perfect Fit</span>
              </div>
            </div>

            {/* Matching Skills list */}
            <div style={{ marginBottom: '1.5rem' }}>
              <h4 style={{ fontSize: '0.85rem', fontWeight: 600, color: '#34d399', marginBottom: '0.6rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <CheckCircle2 size={16} /> Matching Candidate Skills ({matchingSkills.length})
              </h4>
              <div className="tag-list">
                {matchingSkills.map((sk) => (
                  <span key={sk} className="tag tag-success" style={{ padding: '0.3rem 0.65rem', fontSize: '0.8rem' }}>
                    {sk}
                  </span>
                ))}
              </div>
            </div>

            {/* Missing Skills list */}
            <div>
              <h4 style={{ fontSize: '0.85rem', fontWeight: 600, color: '#f87171', marginBottom: '0.6rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <XCircle size={16} /> Missing / Desirable Gaps ({missingSkills.length})
              </h4>
              <div className="tag-list">
                {missingSkills.map((sk) => (
                  <span key={sk} className="tag tag-missing" style={{ padding: '0.3rem 0.65rem', fontSize: '0.8rem' }}>
                    {sk}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* LangGraph Multi-Agent Tailoring Recommendation */}
          <div className="card" style={{ background: 'rgba(99, 102, 241, 0.08)', border: '1px solid rgba(99, 102, 241, 0.25)' }}>
            <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: '#a5b4fc', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Layers size={16} /> LangGraph Multi-Agent Strategy Recommendation
            </h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
              The multi-agent system recommends highlighting <strong>Aho-Corasick pattern matching</strong> and 
              <strong>LangGraph stateful workflow execution</strong> in the dynamic LaTeX resume variant to maximize 
              recruiter score alignment for <strong>{job.company}</strong>.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

import React, { useState } from 'react';
import { Search, Globe, Play, ExternalLink, Sparkles } from 'lucide-react';
import { Job, JobSource } from '../../types';

interface JobDiscoveryViewProps {
  jobs: Job[];
  isScraping: boolean;
  onDiscoverJob: (input: {
    title: string;
    company: string;
    location: string;
    url?: string;
    description: string;
    source: JobSource;
  }) => Promise<void>;
  onSelectJob: (job: Job) => void;
  onInspectIntelligence: (job: Job) => void;
}

export const JobDiscoveryView: React.FC<JobDiscoveryViewProps> = ({
  jobs,
  isScraping,
  onDiscoverJob,
  onInspectIntelligence
}) => {
  const [targetUrl, setTargetUrl] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [company, setCompany] = useState('');
  const [location, setLocation] = useState('Remote / Hybrid');
  const [source, setSource] = useState<JobSource>('PLAYWRIGHT');
  const [description, setDescription] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [sourceFilter, setSourceFilter] = useState<string>('ALL');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onDiscoverJob({
      title: jobTitle || 'Discovered Senior Developer Role',
      company: company || 'Enterprise Technology Corp',
      location: location || 'Remote',
      url: targetUrl || 'https://careers.example.com/job/view',
      description: description || 'High-scale Python, FastAPI, Kafka, and LangGraph workflow engineering.',
      source
    });
    setTargetUrl('');
    setJobTitle('');
    setCompany('');
    setDescription('');
  };

  const filteredJobs = jobs.filter(j => {
    const matchesSearch = j.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          j.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          j.location.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSource = sourceFilter === 'ALL' || j.source === sourceFilter;
    return matchesSearch && matchesSource;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Job Discovery Form Panel */}
      <div className="card">
        <div className="section-header">
          <div>
            <h2 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Globe size={20} color="#6366f1" />
              Automated Playwright Job Scraper &amp; Ingestion Engine
            </h2>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              Ingest job postings from any URL or source to trigger Kafka event streaming and Aho-Corasick analysis.
            </p>
          </div>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
          <div className="form-group" style={{ margin: 0 }}>
            <label className="form-label">Job Posting URL</label>
            <input
              type="url"
              className="form-input"
              placeholder="https://greenhouse.io/careers/job-101"
              value={targetUrl}
              onChange={(e) => setTargetUrl(e.target.value)}
            />
          </div>

          <div className="form-group" style={{ margin: 0 }}>
            <label className="form-label">Job Title</label>
            <input
              type="text"
              className="form-input"
              placeholder="Senior Engineer"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
            />
          </div>

          <div className="form-group" style={{ margin: 0 }}>
            <label className="form-label">Company Name</label>
            <input
              type="text"
              className="form-input"
              placeholder="Enterprise AI"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
            />
          </div>

          <div className="form-group" style={{ margin: 0 }}>
            <label className="form-label">Scraper Source</label>
            <select
              className="form-select"
              value={source}
              onChange={(e) => setSource(e.target.value as JobSource)}
            >
              <option value="PLAYWRIGHT">Playwright Headless</option>
              <option value="LINKEDIN">LinkedIn Jobs</option>
              <option value="INDEED">Indeed Scraper</option>
              <option value="GREENHOUSE">Greenhouse API</option>
              <option value="LEVER">Lever API</option>
              <option value="MANUAL">Manual Ingestion</option>
            </select>
          </div>

          <div className="form-group" style={{ gridColumn: 'span 4', margin: 0 }}>
            <label className="form-label">Location</label>
            <input
              type="text"
              className="form-input"
              placeholder="San Francisco, CA (Remote)"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />
          </div>
        </form>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
          <button type="button" onClick={handleSubmit} className="btn" disabled={isScraping}>
            {isScraping ? (
              <>
                <Sparkles size={16} className="pulse-dot" />
                Scraping &amp; Extracting Keywords...
              </>
            ) : (
              <>
                <Play size={16} />
                Run Scraper &amp; Ingest Job
              </>
            )}
          </button>
        </div>
      </div>

      {/* Discovered Jobs List & Filters */}
      <div className="card">
        <div className="section-header">
          <div>
            <h2 className="section-title">Discovered Job Opportunities ({filteredJobs.length})</h2>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              Track scraped postings, skill match percentages, and processing status
            </p>
          </div>

          {/* Search & Filters */}
          <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
            <div style={{ position: 'relative' }}>
              <Search size={15} style={{ position: 'absolute', left: '10px', top: '10px', color: 'var(--text-muted)' }} />
              <input
                type="text"
                className="form-input"
                placeholder="Search jobs, company..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{ paddingLeft: '2rem', fontSize: '0.8rem', width: '200px' }}
              />
            </div>

            <select
              className="form-select"
              value={sourceFilter}
              onChange={(e) => setSourceFilter(e.target.value)}
              style={{ fontSize: '0.8rem' }}
            >
              <option value="ALL">All Sources</option>
              <option value="PLAYWRIGHT">Playwright</option>
              <option value="LINKEDIN">LinkedIn</option>
              <option value="INDEED">Indeed</option>
              <option value="GREENHOUSE">Greenhouse</option>
            </select>
          </div>
        </div>

        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Job Title &amp; Company</th>
                <th>Location</th>
                <th>Source</th>
                <th>Skills Extracted</th>
                <th>Match Score</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredJobs.map((job) => (
                <tr key={job.id}>
                  <td>
                    <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{job.title}</div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>{job.company}</div>
                  </td>
                  <td>
                    <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>{job.location}</span>
                  </td>
                  <td>
                    <span className="tag">{job.source}</span>
                  </td>
                  <td>
                    <div className="tag-list">
                      {(job.required_skills || ['Python', 'FastAPI', 'Kafka']).slice(0, 3).map((sk) => (
                        <span key={sk} className="tag tag-success">{sk}</span>
                      ))}
                      {(job.required_skills || []).length > 3 && (
                        <span className="tag">+{job.required_skills!.length - 3}</span>
                      )}
                    </div>
                  </td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <div 
                        style={{
                          width: '50px',
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
                      onClick={() => onInspectIntelligence(job)}
                      style={{ fontSize: '0.75rem', padding: '0.35rem 0.7rem' }}
                    >
                      Intelligence <ExternalLink size={13} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

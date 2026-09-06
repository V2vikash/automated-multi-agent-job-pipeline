import React, { useState } from 'react';
import { Search, Play } from 'lucide-react';

interface JobDiscoveryFormProps {
  onDiscoverJob: (url: string) => Promise<void>;
  isLoading: boolean;
}

export const JobDiscoveryForm: React.FC<JobDiscoveryFormProps> = ({ onDiscoverJob, isLoading }) => {
  const [url, setUrl] = useState('https://careers.example.com/jobs/dev-501');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (url.trim()) {
      onDiscoverJob(url.trim());
    }
  };

  return (
    <div className="card" style={{ marginBottom: '1.5rem' }}>
      <h2 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <Search size={20} color="#a5b4fc" />
        Playwright Job Discovery &amp; Pipeline Trigger
      </h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '0.75rem' }}>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter target job posting URL (e.g. https://...)"
          required
          style={{
            flex: 1,
            padding: '0.65rem 1rem',
            background: 'rgba(0,0,0,0.3)',
            border: '1px solid rgba(255,255,255,0.15)',
            borderRadius: '6px',
            color: '#fff',
            fontSize: '0.9rem'
          }}
        />
        <button
          type="submit"
          className="btn"
          disabled={isLoading}
          style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: '#4f46e5' }}
        >
          <Play size={16} />
          {isLoading ? 'Triggering...' : 'Start Pipeline'}
        </button>
      </form>
    </div>
  );
};

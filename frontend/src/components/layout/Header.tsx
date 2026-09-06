import React from 'react';
import { RefreshCw, Bell, PlusCircle, CheckCircle2, AlertTriangle } from 'lucide-react';
import { NavTab } from '../../types';

interface HeaderProps {
  activeTab: NavTab;
  isBackendOnline: boolean;
  wsConnected: boolean;
  onRefreshHealth: () => void;
  onQuickScrape: () => void;
  pendingApprovalsCount: number;
}

const TAB_TITLE_MAP: Record<NavTab, string> = {
  dashboard: 'Executive Pipeline Dashboard',
  jobs: 'Job Discovery & Scraping Workspace',
  job_intelligence: 'Aho-Corasick Skill Intelligence',
  resume_intelligence: 'Resume Versioning & LaTeX Compiler',
  approvals: 'Human-in-the-Loop (HITL) Approval Workspace',
  activity: 'Real-Time Pipeline Execution Timeline',
  health: 'System Infrastructure Health & Diagnostics'
};

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  isBackendOnline,
  wsConnected,
  onRefreshHealth,
  onQuickScrape,
  pendingApprovalsCount
}) => {
  return (
    <header className="top-header">
      <div className="header-left">
        <h1 className="page-title">{TAB_TITLE_MAP[activeTab]}</h1>
      </div>

      <div className="header-right">
        {/* Quick Discovery Button */}
        <button className="btn" onClick={onQuickScrape} style={{ fontSize: '0.8rem', padding: '0.45rem 0.9rem' }}>
          <PlusCircle size={15} />
          Discover Job
        </button>

        {/* Real-time WebSocket Stream Indicator */}
        <div className={`status-pill ${wsConnected ? 'online' : 'offline'}`} title={wsConnected ? 'WebSocket Stream Connected' : 'WebSocket Stream Reconnecting'}>
          <span className="pulse-dot" />
          <span>{wsConnected ? 'HITL WS Live' : 'WS Syncing'}</span>
        </div>

        {/* Backend REST Health Indicator */}
        <div 
          className={`status-pill ${isBackendOnline ? 'online' : 'offline'}`}
          style={{ cursor: 'pointer' }}
          onClick={onRefreshHealth}
          title="Click to refresh system diagnostics"
        >
          {isBackendOnline ? <CheckCircle2 size={13} /> : <AlertTriangle size={13} />}
          <span>{isBackendOnline ? 'FastAPI API v1 Online' : 'FastAPI Offline'}</span>
          <RefreshCw size={12} style={{ marginLeft: '2px' }} />
        </div>

        {/* Pending Approvals Notification Bell */}
        {pendingApprovalsCount > 0 && (
          <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
            <div 
              style={{ 
                padding: '0.5rem', 
                background: 'rgba(99, 102, 241, 0.15)', 
                borderRadius: '50%', 
                color: '#a5b4fc', 
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
              title={`${pendingApprovalsCount} pending approvals awaiting decision`}
            >
              <Bell size={18} />
              <span 
                style={{
                  position: 'absolute',
                  top: '-2px',
                  right: '-2px',
                  background: '#ef4444',
                  color: 'white',
                  fontSize: '0.65rem',
                  fontWeight: 700,
                  width: '16px',
                  height: '16px',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
              >
                {pendingApprovalsCount}
              </span>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

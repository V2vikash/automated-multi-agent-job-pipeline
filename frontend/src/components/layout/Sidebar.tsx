import React from 'react';
import { 
  LayoutDashboard, 
  Search, 
  BrainCircuit, 
  FileText, 
  CheckSquare, 
  Activity, 
  Server,
  Zap
} from 'lucide-react';
import { NavTab } from '../../types';

interface SidebarProps {
  activeTab: NavTab;
  onSelectTab: (tab: NavTab) => void;
  pendingApprovalsCount: number;
  totalJobsCount: number;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  onSelectTab,
  pendingApprovalsCount,
  totalJobsCount
}) => {
  return (
    <aside className="app-sidebar">
      {/* Sidebar Brand Header */}
      <div className="sidebar-header">
        <div className="brand-icon">
          <Zap size={22} />
        </div>
        <div className="brand-text">
          <span className="brand-name">Automated Job Pipeline</span>
          <span className="brand-sub">Multi-Agent Enterprise SaaS</span>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="sidebar-nav">
        <div className="nav-section-title">Core Operations</div>
        
        <button
          className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => onSelectTab('dashboard')}
        >
          <LayoutDashboard size={18} />
          <span>Dashboard</span>
        </button>

        <button
          className={`nav-item ${activeTab === 'jobs' ? 'active' : ''}`}
          onClick={() => onSelectTab('jobs')}
        >
          <Search size={18} />
          <span>Job Discovery</span>
          {totalJobsCount > 0 && <span className="nav-item-badge">{totalJobsCount}</span>}
        </button>

        <div className="nav-section-title" style={{ marginTop: '0.75rem' }}>Intelligence & Tailoring</div>

        <button
          className={`nav-item ${activeTab === 'job_intelligence' ? 'active' : ''}`}
          onClick={() => onSelectTab('job_intelligence')}
        >
          <BrainCircuit size={18} />
          <span>Job Intelligence</span>
        </button>

        <button
          className={`nav-item ${activeTab === 'resume_intelligence' ? 'active' : ''}`}
          onClick={() => onSelectTab('resume_intelligence')}
        >
          <FileText size={18} />
          <span>Resume Intelligence</span>
        </button>

        <div className="nav-section-title" style={{ marginTop: '0.75rem' }}>Governance & Audit</div>

        <button
          className={`nav-item ${activeTab === 'approvals' ? 'active' : ''}`}
          onClick={() => onSelectTab('approvals')}
        >
          <CheckSquare size={18} />
          <span>HITL Approvals</span>
          {pendingApprovalsCount > 0 && (
            <span className="nav-item-badge" style={{ background: '#ef4444' }}>
              {pendingApprovalsCount}
            </span>
          )}
        </button>

        <button
          className={`nav-item ${activeTab === 'activity' ? 'active' : ''}`}
          onClick={() => onSelectTab('activity')}
        >
          <Activity size={18} />
          <span>Pipeline Activity</span>
        </button>

        <button
          className={`nav-item ${activeTab === 'health' ? 'active' : ''}`}
          onClick={() => onSelectTab('health')}
        >
          <Server size={18} />
          <span>System Health</span>
        </button>
      </nav>

      {/* User Profile Area */}
      <div className="sidebar-footer">
        <div className="user-avatar">AM</div>
        <div className="user-info">
          <span className="user-name">Alex Mercer</span>
          <span className="user-role">Recruiter / Job Seeker</span>
        </div>
      </div>
    </aside>
  );
};

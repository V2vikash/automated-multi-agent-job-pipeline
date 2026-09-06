import React from 'react';
import { NavTab, Job, Resume, ResumeVersion, ApprovalRequest, AuditEvent, SystemServiceHealth, HealthCheckResponse } from '../types';
import { OverviewDashboard } from '../components/dashboard/OverviewDashboard';
import { JobDiscoveryView } from '../components/jobs/JobDiscoveryView';
import { JobIntelligenceView } from '../components/jobs/JobIntelligenceView';
import { ResumeIntelligenceView } from '../components/resumes/ResumeIntelligenceView';
import { ApprovalWorkspaceView } from '../components/approvals/ApprovalWorkspaceView';
import { PipelineActivityView } from '../components/activity/PipelineActivityView';
import { SystemHealthView } from '../components/system/SystemHealthView';

interface DashboardProps {
  activeTab: NavTab;
  setActiveTab: (tab: NavTab) => void;
  jobs: Job[];
  selectedJob: Job | null;
  setSelectedJob: (job: Job) => void;
  resumes: Resume[];
  resumeVersions: ResumeVersion[];
  approvals: ApprovalRequest[];
  events: AuditEvent[];
  services: SystemServiceHealth[];
  isBackendOnline: boolean;
  healthData: HealthCheckResponse | null;
  lastChecked: Date | null;
  wsConnected: boolean;
  isScraping: boolean;
  onDiscoverJob: (input: any) => Promise<void>;
  onRespondApproval: (id: string, decision: any, note?: string) => Promise<void>;
  onRefreshHealth: () => void;
}

export const Dashboard: React.FC<DashboardProps> = ({
  activeTab,
  setActiveTab,
  jobs,
  selectedJob,
  setSelectedJob,
  resumes,
  resumeVersions,
  approvals,
  events,
  services,
  isBackendOnline,
  healthData,
  lastChecked,
  wsConnected,
  isScraping,
  onDiscoverJob,
  onRespondApproval,
  onRefreshHealth
}) => {
  switch (activeTab) {
    case 'dashboard':
      return (
        <OverviewDashboard
          jobs={jobs}
          approvals={approvals}
          events={events}
          onNavigate={setActiveTab}
          onSelectJob={(j) => setSelectedJob(j)}
        />
      );

    case 'jobs':
      return (
        <JobDiscoveryView
          jobs={jobs}
          isScraping={isScraping}
          onDiscoverJob={onDiscoverJob}
          onSelectJob={(j) => setSelectedJob(j)}
          onInspectIntelligence={(j) => {
            setSelectedJob(j);
            setActiveTab('job_intelligence');
          }}
        />
      );

    case 'job_intelligence':
      return (
        <JobIntelligenceView
          job={selectedJob}
          allJobs={jobs}
          onSelectJob={(j) => setSelectedJob(j)}
          onNavigateToResumes={() => setActiveTab('resume_intelligence')}
        />
      );

    case 'resume_intelligence':
      return (
        <ResumeIntelligenceView
          resumes={resumes}
          versions={resumeVersions}
          jobs={jobs}
          onSelectJobForTailoring={(j) => {
            setSelectedJob(j);
            setActiveTab('job_intelligence');
          }}
        />
      );

    case 'approvals':
      return (
        <ApprovalWorkspaceView
          approvals={approvals}
          jobs={jobs}
          wsConnected={wsConnected}
          onRespondApproval={onRespondApproval}
        />
      );

    case 'activity':
      return (
        <PipelineActivityView
          events={events}
          wsConnected={wsConnected}
        />
      );

    case 'health':
      return (
        <SystemHealthView
          services={services}
          isBackendOnline={isBackendOnline}
          healthData={healthData}
          lastChecked={lastChecked}
          onRefreshHealth={onRefreshHealth}
        />
      );

    default:
      return null;
  }
};

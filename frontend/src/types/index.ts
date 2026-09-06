export type JobSource = 'PLAYWRIGHT' | 'LINKEDIN' | 'INDEED' | 'GREENHOUSE' | 'LEVER' | 'MANUAL';

export interface JobKeyword {
  id?: string;
  job_id?: string;
  keyword: string;
  normalized_keyword: string;
  category: string;
  source?: string;
  confidence: number;
}

export interface Job {
  id: string;
  external_id?: string;
  title: string;
  company: string;
  location: string;
  url?: string;
  description: string;
  source: JobSource;
  discovered_at?: string;
  created_at?: string;
  match_score?: number;
  status?: 'DISCOVERED' | 'ANALYZED' | 'MATCHED' | 'PROCESSING' | 'COMPLETED';
  job_keywords?: JobKeyword[];
  required_skills?: string[];
  matching_skills?: string[];
  missing_skills?: string[];
}

export interface Resume {
  id: string;
  user_id: string;
  title: string;
  original_filename: string;
  storage_path: string;
  parsed_content?: Record<string, any> | string;
  created_at?: string;
  updated_at?: string;
}

export interface ResumeVersion {
  id: string;
  resume_id: string;
  job_id: string;
  version_number: number;
  version_type: 'TAILORED' | 'MASTER' | 'REVISION';
  latex_source: string;
  pdf_path?: string;
  status: 'PENDING' | 'GENERATED' | 'COMPILING' | 'FAILED' | 'APPROVED';
  created_at?: string;
}

export type PipelineStatus = 'PENDING' | 'RUNNING' | 'WAITING_APPROVAL' | 'COMPLETED' | 'FAILED' | 'REJECTED';

export interface PipelineStep {
  id?: string;
  pipeline_run_id?: string;
  step_name: string;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED';
  attempt?: number;
  started_at?: string;
  completed_at?: string;
  error_message?: string;
  metadata_?: Record<string, any>;
}

export interface PipelineRun {
  id: string;
  user_id: string;
  job_id: string;
  correlation_id: string;
  status: PipelineStatus;
  current_step: string;
  started_at?: string;
  completed_at?: string;
  error_message?: string;
  steps?: PipelineStep[];
  created_at?: string;
}

export type ApprovalStatusType = 'PENDING' | 'APPROVED' | 'REJECTED' | 'REVISION_REQUESTED';

export interface ApprovalRequest {
  id: string;
  pipeline_run_id: string;
  resume_version_id?: string;
  status: ApprovalStatusType;
  requested_at?: string;
  responded_at?: string;
  reviewer_note?: string;
  // Computed / UI details
  job_title?: string;
  company?: string;
  match_score?: number;
  extracted_keywords?: string[];
  changes_made?: string[];
  resume_version_name?: string;
  latex_source?: string;
  pdf_url?: string;
}

export interface AuditEvent {
  id: string;
  event_id: string;
  event_type: string;
  correlation_id?: string;
  pipeline_id?: string;
  payload?: Record<string, any>;
  status: string;
  created_at: string;
}

export interface SystemServiceHealth {
  name: string;
  key: 'fastapi' | 'postgres' | 'kafka' | 'websocket' | 'worker' | 'latex';
  status: 'online' | 'offline' | 'degraded' | 'loading';
  endpoint?: string;
  port?: string | number;
  details?: string;
  latencyMs?: number;
  lastChecked?: string;
}

export interface HealthCheckResponse {
  status: string;
  service: string;
  version?: string;
  environment?: string;
}

export type NavTab = 
  | 'dashboard'
  | 'jobs'
  | 'job_intelligence'
  | 'resume_intelligence'
  | 'approvals'
  | 'activity'
  | 'health';

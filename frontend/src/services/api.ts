import { 
  Job, 
  JobSource, 
  Resume, 
  PipelineRun, 
  ApprovalRequest, 
  AuditEvent, 
  HealthCheckResponse 
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const WS_BASE_URL = API_BASE_URL.replace(/^http/, 'ws');

export async function fetchHealthStatus(): Promise<HealthCheckResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/health`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!response.ok) {
    throw new Error(`Health check failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchJobs(): Promise<Job[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/jobs/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn('Backend REST API jobs endpoint offline or empty, using local state handler.');
    return [];
  }
}

export async function createJob(data: {
  title: string;
  company: string;
  location: string;
  url?: string;
  description: string;
  source: JobSource;
}): Promise<Job> {
  const res = await fetch(`${API_BASE_URL}/api/v1/jobs/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ...data,
      external_id: `ext-${Date.now()}`,
      discovered_at: new Date().toISOString()
    })
  });
  if (!res.ok) throw new Error(`Failed to create job: ${res.statusText}`);
  return res.json();
}

export async function fetchResumes(): Promise<Resume[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/resumes/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function fetchPipelineRuns(): Promise<PipelineRun[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/pipelines/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function createPipelineRun(userId: string, jobId: string): Promise<PipelineRun> {
  const res = await fetch(`${API_BASE_URL}/api/v1/pipelines/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      job_id: jobId,
      correlation_id: `corr-${Date.now()}`,
      status: 'RUNNING',
      current_step: 'Job Discovered',
      started_at: new Date().toISOString()
    })
  });
  if (!res.ok) throw new Error(`Failed to start pipeline: ${res.statusText}`);
  return res.json();
}

export async function fetchApprovals(): Promise<ApprovalRequest[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/approvals/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function respondApproval(
  approvalId: string, 
  status: 'approved' | 'rejected', 
  reviewerNote?: string
): Promise<any> {
  const params = new URLSearchParams({ decision: status });
  if (reviewerNote) params.append('reviewer_note', reviewerNote);

  const res = await fetch(`${API_BASE_URL}/api/v1/approvals/${approvalId}?${params.toString()}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' }
  });
  if (!res.ok) throw new Error(`Failed to submit approval: ${res.statusText}`);
  return res.json();
}

export async function fetchAuditEvents(): Promise<AuditEvent[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/events/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    return [];
  }
}

export function connectNotificationsWebSocket(
  onMessage: (event: any) => void,
  onStatusChange?: (connected: boolean) => void
): WebSocket | null {
  try {
    const ws = new WebSocket(`${WS_BASE_URL}/api/v1/ws/notifications`);
    
    ws.onopen = () => {
      onStatusChange?.(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (e) {
        onMessage(event.data);
      }
    };

    ws.onerror = (err) => {
      console.warn('WebSocket notification stream error:', err);
      onStatusChange?.(false);
    };

    ws.onclose = () => {
      onStatusChange?.(false);
    };

    return ws;
  } catch (err) {
    onStatusChange?.(false);
    return null;
  }
}

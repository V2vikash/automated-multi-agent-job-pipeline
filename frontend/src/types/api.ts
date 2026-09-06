export interface HealthCheckResponse {
  status: string;
  service: string;
  version?: string;
  environment?: string;
}

export interface ServiceStatus {
  backend: 'online' | 'offline' | 'loading';
  lastChecked: Date | null;
  errorMessage?: string;
}

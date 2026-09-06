import React from 'react';
import { Server, RefreshCw, Cpu, Radio, FileCheck, Database } from 'lucide-react';
import { SystemServiceHealth, HealthCheckResponse } from '../../types';

interface SystemHealthViewProps {
  services: SystemServiceHealth[];
  isBackendOnline: boolean;
  healthData: HealthCheckResponse | null;
  lastChecked: Date | null;
  onRefreshHealth: () => void;
}

const SERVICE_ICON_MAP: Record<string, any> = {
  fastapi: Server,
  postgres: Database,
  kafka: Radio,
  websocket: Radio,
  worker: Cpu,
  latex: FileCheck
};

export const SystemHealthView: React.FC<SystemHealthViewProps> = ({
  services,
  healthData,
  lastChecked,
  onRefreshHealth
}) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* System Overview Header */}
      <div className="card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ padding: '0.65rem', background: 'rgba(99, 102, 241, 0.15)', borderRadius: 'var(--radius-md)', color: '#a5b4fc' }}>
            <Server size={24} />
          </div>
          <div>
            <h2 style={{ fontSize: '1.15rem', fontWeight: 700, margin: 0 }}>System Infrastructure &amp; Microservices Health</h2>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              Environment: {healthData?.environment || 'production'} | Last Check: {lastChecked ? lastChecked.toLocaleTimeString() : 'Just now'}
            </span>
          </div>
        </div>

        <button className="btn" onClick={onRefreshHealth}>
          <RefreshCw size={15} />
          Run Health Diagnostics
        </button>
      </div>

      {/* Microservices Health Grid */}
      <div className="grid-metrics" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))' }}>
        {services.map((srv) => {
          const IconComp = SERVICE_ICON_MAP[srv.key] || Server;
          const isOnline = srv.status === 'online';
          const isDegraded = srv.status === 'degraded';

          return (
            <div key={srv.key} className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <div className="card-header">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                    <IconComp size={18} color="#a5b4fc" />
                    <span className="card-title" style={{ color: 'var(--text-primary)', fontSize: '0.9rem' }}>{srv.name}</span>
                  </div>
                  <span className={`status-indicator ${isOnline ? 'online' : isDegraded ? 'warning' : 'offline'}`}>
                    <span className="pulse-dot" />
                    {srv.status.toUpperCase()}
                  </span>
                </div>

                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                  Endpoint / Binding: <strong style={{ color: '#a5b4fc', fontFamily: 'var(--font-mono)' }}>{srv.endpoint}</strong>
                </div>

                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  {srv.details}
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1.25rem', paddingTop: '0.75rem', borderTop: '1px solid var(--border-subtle)' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Port / Driver: {srv.port}</span>
                {srv.latencyMs !== undefined && (
                  <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#10b981' }}>
                    {srv.latencyMs} ms
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Backend API Configuration Specs Card */}
      <div className="card">
        <h3 className="section-title" style={{ fontSize: '1rem', marginBottom: '1rem' }}>
          Backend Platform Specifications &amp; Architectural Stack
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
          <div style={{ padding: '1rem', background: 'rgba(255,255,255,0.02)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
            <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#a5b4fc', marginBottom: '0.25rem' }}>FastAPI REST &amp; WS</div>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Python 3.11+, Pydantic v2, Uvicorn ASGI Server</span>
          </div>

          <div style={{ padding: '1rem', background: 'rgba(255,255,255,0.02)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
            <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#a5b4fc', marginBottom: '0.25rem' }}>PostgreSQL 16</div>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Asyncpg Driver, SQLAlchemy 2.0 ORM, Alembic Migrations</span>
          </div>

          <div style={{ padding: '1rem', background: 'rgba(255,255,255,0.02)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
            <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#a5b4fc', marginBottom: '0.25rem' }}>Apache Kafka</div>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>10 Idempotent Event Topics, aiokafka Producer/Consumer</span>
          </div>

          <div style={{ padding: '1rem', background: 'rgba(255,255,255,0.02)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
            <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#a5b4fc', marginBottom: '0.25rem' }}>Aho-Corasick Engine</div>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Linear-Time O(N+M) Deterministic Keyword Matcher</span>
          </div>
        </div>
      </div>
    </div>
  );
};

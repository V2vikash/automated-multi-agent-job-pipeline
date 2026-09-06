import React from 'react';

interface StatusCardProps {
  title: string;
  status: 'online' | 'offline' | 'loading' | 'warning';
  metric?: string;
  detail?: string;
  icon?: React.ReactNode;
}

export const StatusCard: React.FC<StatusCardProps> = ({
  title,
  status,
  metric,
  detail,
  icon,
}) => {
  const getStatusClass = () => {
    switch (status) {
      case 'online':
        return 'online';
      case 'offline':
        return 'offline';
      case 'warning':
      case 'loading':
      default:
        return 'warning';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'online':
        return 'Online';
      case 'offline':
        return 'Offline';
      case 'loading':
        return 'Checking...';
      case 'warning':
        return 'Degraded';
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          {icon}
          <span className="card-title">{title}</span>
        </div>
        <div className={`status-indicator ${getStatusClass()}`}>
          <span className="pulse-dot"></span>
          <span>{getStatusText()}</span>
        </div>
      </div>
      {metric && <div className="card-metric">{metric}</div>}
      {detail && <div className="card-detail">{detail}</div>}
    </div>
  );
};

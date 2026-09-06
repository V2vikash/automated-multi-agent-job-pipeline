import { Sidebar } from './components/layout/Sidebar';
import { Header } from './components/layout/Header';
import { Dashboard } from './pages/Dashboard';
import { useHealth } from './hooks/useHealth';
import { usePipelineData } from './hooks/usePipelineData';

export function App() {
  const { isBackendOnline, healthData, services, lastChecked, refreshHealth } = useHealth();
  const {
    activeTab,
    setActiveTab,
    jobs,
    selectedJob,
    setSelectedJob,
    resumes,
    resumeVersions,
    approvals,
    events,
    wsConnected,
    isScraping,
    handleDiscoverJob,
    handleRespondApproval
  } = usePipelineData();

  const pendingApprovalsCount = approvals.filter(a => a.status === 'PENDING').length;

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        onSelectTab={setActiveTab}
        pendingApprovalsCount={pendingApprovalsCount}
        totalJobsCount={jobs.length}
      />

      {/* Main Content Area */}
      <div className="main-wrapper">
        <Header
          activeTab={activeTab}
          isBackendOnline={isBackendOnline}
          wsConnected={wsConnected}
          onRefreshHealth={refreshHealth}
          onQuickScrape={() => setActiveTab('jobs')}
          pendingApprovalsCount={pendingApprovalsCount}
        />

        <main className="content-area">
          <Dashboard
            activeTab={activeTab}
            setActiveTab={setActiveTab}
            jobs={jobs}
            selectedJob={selectedJob}
            setSelectedJob={setSelectedJob}
            resumes={resumes}
            resumeVersions={resumeVersions}
            approvals={approvals}
            events={events}
            services={services}
            isBackendOnline={isBackendOnline}
            healthData={healthData}
            lastChecked={lastChecked}
            wsConnected={wsConnected}
            isScraping={isScraping}
            onDiscoverJob={handleDiscoverJob}
            onRespondApproval={handleRespondApproval}
            onRefreshHealth={refreshHealth}
          />
        </main>
      </div>
    </div>
  );
}

export default App;

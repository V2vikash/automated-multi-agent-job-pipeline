import { useState, useEffect, useCallback } from 'react';
import { 
  Job, 
  Resume, 
  ResumeVersion,
  ApprovalRequest, 
  AuditEvent, 
  JobSource,
  NavTab
} from '../types';
import { 
  fetchJobs, 
  createJob as apiCreateJob,
  fetchApprovals, 
  respondApproval as apiRespondApproval,
  fetchAuditEvents,
  connectNotificationsWebSocket 
} from '../services/api';

const MOCK_JOBS: Job[] = [
  {
    id: 'job-101',
    external_id: 'gh-991201',
    title: 'Senior Backend & Distributed Systems Engineer',
    company: 'Enterprise Artificial Intelligence Systems',
    location: 'San Francisco, CA (Remote)',
    url: 'https://careers.enterpriseai.io/jobs/991201',
    source: 'PLAYWRIGHT',
    discovered_at: new Date(Date.now() - 3600000 * 2).toISOString(),
    created_at: new Date(Date.now() - 3600000 * 2).toISOString(),
    match_score: 94,
    status: 'MATCHED',
    description: `We are looking for a Senior Backend & Distributed Systems Engineer to scale our core event-driven architecture.
Requirements:
- Strong experience with Python 3.11+, FastAPI, and PostgreSQL (Asyncpg).
- Expertise in event streaming with Apache Kafka or RabbitMQ.
- Deep knowledge of multi-agent state machines (LangGraph / AutoGen).
- Experience with web scraping automation using Playwright or Selenium.
- Automated document compilation with LaTeX / PDF generation engines.
- Knowledge of high-performance pattern matching (Aho-Corasick algorithm).`,
    job_keywords: [
      { keyword: 'Python', normalized_keyword: 'python', category: 'Language', confidence: 0.99 },
      { keyword: 'FastAPI', normalized_keyword: 'fastapi', category: 'Framework', confidence: 0.98 },
      { keyword: 'PostgreSQL', normalized_keyword: 'postgresql', category: 'Database', confidence: 0.96 },
      { keyword: 'Apache Kafka', normalized_keyword: 'apache kafka', category: 'Event Streaming', confidence: 0.97 },
      { keyword: 'LangGraph', normalized_keyword: 'langgraph', category: 'AI Orchestration', confidence: 0.95 },
      { keyword: 'Playwright', normalized_keyword: 'playwright', category: 'Scraper', confidence: 0.94 },
      { keyword: 'Aho-Corasick', normalized_keyword: 'aho-corasick', category: 'Algorithm', confidence: 0.99 },
      { keyword: 'LaTeX', normalized_keyword: 'latex', category: 'Document Engine', confidence: 0.92 }
    ],
    required_skills: ['Python', 'FastAPI', 'PostgreSQL', 'Apache Kafka', 'LangGraph', 'Playwright', 'Aho-Corasick', 'LaTeX', 'Docker', 'Kubernetes'],
    matching_skills: ['Python', 'FastAPI', 'PostgreSQL', 'Apache Kafka', 'LangGraph', 'Playwright', 'Aho-Corasick', 'LaTeX', 'Docker'],
    missing_skills: ['Kubernetes']
  },
  {
    id: 'job-102',
    external_id: 'li-448102',
    title: 'Lead AI Platform Architect',
    company: 'Nexus Scale Labs',
    location: 'New York, NY (Hybrid)',
    url: 'https://linkedin.com/jobs/view/448102',
    source: 'LINKEDIN',
    discovered_at: new Date(Date.now() - 3600000 * 6).toISOString(),
    created_at: new Date(Date.now() - 3600000 * 6).toISOString(),
    match_score: 88,
    status: 'COMPLETED',
    description: `Nexus Scale Labs is seeking a Lead AI Platform Architect to design production multi-agent pipelines and real-time WebSocket human-in-the-loop workflows.
Key Responsibilities:
- Build high-throughput event processing layers in Python and Kafka.
- Architect stateful graph execution models using LangGraph.
- Oversee automated LaTeX document generation and dynamic PDF rendering.
- Integrate fast linear-time keyword extractors (Aho-Corasick) for real-time resume parsing.`,
    job_keywords: [
      { keyword: 'Python', normalized_keyword: 'python', category: 'Language', confidence: 0.99 },
      { keyword: 'LangGraph', normalized_keyword: 'langgraph', category: 'AI Architecture', confidence: 0.97 },
      { keyword: 'Kafka', normalized_keyword: 'kafka', category: 'Streaming', confidence: 0.95 },
      { keyword: 'WebSocket', normalized_keyword: 'websocket', category: 'Networking', confidence: 0.93 },
      { keyword: 'LaTeX', normalized_keyword: 'latex', category: 'PDF Generation', confidence: 0.90 }
    ],
    required_skills: ['Python', 'LangGraph', 'Kafka', 'WebSocket', 'LaTeX', 'System Design'],
    matching_skills: ['Python', 'LangGraph', 'Kafka', 'WebSocket', 'LaTeX'],
    missing_skills: ['System Design']
  },
  {
    id: 'job-103',
    external_id: 'ind-882190',
    title: 'Full Stack AI Systems Developer',
    company: 'Quantum Automation Analytics',
    location: 'Austin, TX',
    url: 'https://indeed.com/viewjob?jk=882190',
    source: 'INDEED',
    discovered_at: new Date(Date.now() - 3600000 * 12).toISOString(),
    created_at: new Date(Date.now() - 3600000 * 12).toISOString(),
    match_score: 82,
    status: 'DISCOVERED',
    description: `Join Quantum Automation to build autonomous data scraping, multi-agent pipelines, and client-facing SaaS web interfaces.
Requirements:
- React 18 / TypeScript frontend development.
- Python FastAPI microservices backend.
- Playwright headless web scraping.
- PostgreSQL database design and query optimization.`,
    job_keywords: [
      { keyword: 'React', normalized_keyword: 'react', category: 'Frontend', confidence: 0.98 },
      { keyword: 'TypeScript', normalized_keyword: 'typescript', category: 'Language', confidence: 0.97 },
      { keyword: 'FastAPI', normalized_keyword: 'fastapi', category: 'Backend', confidence: 0.96 },
      { keyword: 'Playwright', normalized_keyword: 'playwright', category: 'Automation', confidence: 0.92 }
    ],
    required_skills: ['React', 'TypeScript', 'FastAPI', 'Playwright', 'PostgreSQL', 'Redis'],
    matching_skills: ['React', 'TypeScript', 'FastAPI', 'Playwright', 'PostgreSQL'],
    missing_skills: ['Redis']
  }
];

const MOCK_RESUMES: Resume[] = [
  {
    id: 'res-master-001',
    user_id: 'usr-default-001',
    title: 'Principal Software Engineer & AI Systems Specialist',
    original_filename: 'Master_Resume_2026.pdf',
    storage_path: '/storage/resumes/usr-default-001/master_resume.pdf',
    created_at: new Date(Date.now() - 86400000 * 10).toISOString(),
    parsed_content: {
      summary: 'Senior Software Engineer with 8+ years experience architecting distributed event-driven systems, multi-agent AI workflows, and high-performance microservices.',
      skills: ['Python', 'FastAPI', 'PostgreSQL', 'Apache Kafka', 'LangGraph', 'Playwright', 'Aho-Corasick', 'LaTeX', 'React', 'TypeScript', 'Docker'],
      experience: [
        {
          role: 'Staff AI Systems Engineer',
          company: 'Automated Agent Systems',
          period: '2023 - Present',
          bullet_points: [
            'Architected automated multi-agent job application pipeline processing 5,000+ postings daily.',
            'Implemented linear-time Aho-Corasick keyword matching algorithm reducing parsing overhead by 85%.',
            'Engineered automated LaTeX dynamic resume compilation service with real-time PDF generation.',
            'Built real-time WebSocket Human-In-The-Loop approval portal with stateful workflow control.'
          ]
        }
      ]
    }
  }
];

const MOCK_VERSIONS: ResumeVersion[] = [
  {
    id: 'rv-version-901',
    resume_id: 'res-master-001',
    job_id: 'job-101',
    version_number: 1,
    version_type: 'TAILORED',
    status: 'GENERATED',
    latex_source: `\\documentclass[10pt, letterpaper]{article}
\\usepackage[utf8]{utf8}
\\usepackage{geometry}
\\geometry{letterpaper, margin=0.6in}
\\usepackage{hyperref}
\\usepackage{enumitem}

\\begin{document}
\\begin{center}
    {\\LARGE \\bfseries Alex Mercer}\\\\
    \\vspace{2pt}
    San Francisco, CA $|$ alex.mercer@dev.io $|$ github.com/alexmercer $|$ linkedin.com/in/alexmercer
\\end{center}

\\section*{Professional Summary}
Senior Distributed Systems \\& AI Engineer specializing in \\textbf{Python}, \\textbf{FastAPI}, \\textbf{Apache Kafka}, and \\textbf{LangGraph} multi-agent orchestration. Demonstrated success implementing \\textbf{Aho-Corasick} keyword extraction and automated \\textbf{LaTeX/PDF} dynamic compilation.

\\section*{Technical Core}
\\begin{itemize}[leftmargin=1.5em]
    \\item \\textbf{Languages \\& Backends:} Python 3.11, FastAPI, Asyncpg, PostgreSQL, SQLModel
    \\item \\textbf{Distributed \\& Events:} Apache Kafka, Event-Driven Microservices, AsyncIO
    \\item \\textbf{AI \\& Automation:} LangGraph, Playwright Web Scraper, Aho-Corasick String Matcher
    \\item \\textbf{Document Engine:} Automated LaTeX, PDF Compiler, WebSocket Real-time Stream
\\end{itemize}

\\section*{Key Achievements}
\\begin{itemize}[leftmargin=1.5em]
    \\item Engineered end-to-end Automated Multi-Agent Job Pipeline with Playwright discovery, Kafka event bus, and LangGraph workflow orchestration.
    \\item Accelerated resume skill extraction with zero LLM latency overhead using deterministic Aho-Corasick pattern matching.
    \\item Integrated Human-In-The-Loop (HITL) approval workspace using bi-directional WebSockets.
\\end{itemize}
\\end{document}`,
    pdf_path: '/storage/generated/rv-version-901.pdf',
    created_at: new Date(Date.now() - 1800000).toISOString()
  }
];

const MOCK_APPROVALS: ApprovalRequest[] = [
  {
    id: 'appr-req-701',
    pipeline_run_id: 'pipe-run-301',
    resume_version_id: 'rv-version-901',
    status: 'PENDING',
    requested_at: new Date(Date.now() - 900000).toISOString(),
    job_title: 'Senior Backend & Distributed Systems Engineer',
    company: 'Enterprise Artificial Intelligence Systems',
    match_score: 94,
    extracted_keywords: ['Python', 'FastAPI', 'PostgreSQL', 'Apache Kafka', 'LangGraph', 'Playwright', 'Aho-Corasick', 'LaTeX'],
    changes_made: [
      'Tailored Professional Summary to highlight LangGraph multi-agent experience.',
      'Emphasized Aho-Corasick pattern matching and zero-token keyword extraction.',
      'Reordered technical core skills to match job description priority.',
      'Added automated LaTeX document compilation achievement.'
    ],
    resume_version_name: 'Tailored Resume Variant v1.0',
    latex_source: MOCK_VERSIONS[0].latex_source
  }
];

const MOCK_EVENTS: AuditEvent[] = [
  {
    id: 'evt-101',
    event_id: 'evt-job-discovered-101',
    event_type: 'job.discovered',
    correlation_id: 'corr-run-301',
    pipeline_id: 'pipe-run-301',
    status: 'COMPLETED',
    created_at: new Date(Date.now() - 3600000 * 2).toISOString(),
    payload: { source: 'PLAYWRIGHT', url: 'https://careers.enterpriseai.io/jobs/991201', job_title: 'Senior Backend & Distributed Systems Engineer' }
  },
  {
    id: 'evt-102',
    event_id: 'evt-kafka-published-102',
    event_type: 'kafka.event.published',
    correlation_id: 'corr-run-301',
    pipeline_id: 'pipe-run-301',
    status: 'COMPLETED',
    created_at: new Date(Date.now() - 3600000 * 1.9).toISOString(),
    payload: { topic: 'job.ingestion.events', partition: 0, offset: 4218 }
  },
  {
    id: 'evt-103',
    event_id: 'evt-langgraph-exec-103',
    event_type: 'langgraph.processing.started',
    correlation_id: 'corr-run-301',
    pipeline_id: 'pipe-run-301',
    status: 'COMPLETED',
    created_at: new Date(Date.now() - 3600000 * 1.8).toISOString(),
    payload: { graph_id: 'job_tailoring_graph', node: 'skill_analysis_agent' }
  },
  {
    id: 'evt-104',
    event_id: 'evt-aho-corasick-104',
    event_type: 'aho_corasick.keywords.extracted',
    correlation_id: 'corr-run-301',
    pipeline_id: 'pipe-run-301',
    status: 'COMPLETED',
    created_at: new Date(Date.now() - 3600000 * 1.7).toISOString(),
    payload: { keywords_found: 8, execution_time_ms: 1.4, algorithm: 'Aho-Corasick Automaton' }
  },
  {
    id: 'evt-105',
    event_id: 'evt-resume-match-105',
    event_type: 'resume.matched',
    correlation_id: 'corr-run-301',
    pipeline_id: 'pipe-run-301',
    status: 'COMPLETED',
    created_at: new Date(Date.now() - 3600000 * 1.6).toISOString(),
    payload: { match_score: 94, matching_count: 9, missing_count: 1 }
  },
  {
    id: 'evt-106',
    event_id: 'evt-latex-gen-106',
    event_type: 'tailored_resume.generated',
    correlation_id: 'corr-run-301',
    pipeline_id: 'pipe-run-301',
    status: 'COMPLETED',
    created_at: new Date(Date.now() - 3600000 * 1.5).toISOString(),
    payload: { compiler: 'pdflatex', output_file: 'rv-version-901.pdf', bytes: 14209 }
  },
  {
    id: 'evt-107',
    event_id: 'evt-hitl-awaiting-107',
    event_type: 'approval.awaiting_human_decision',
    correlation_id: 'corr-run-301',
    pipeline_id: 'pipe-run-301',
    status: 'RUNNING',
    created_at: new Date(Date.now() - 900000).toISOString(),
    payload: { approval_id: 'appr-req-701', stream: 'ws_notifications' }
  }
];

export function usePipelineData() {
  const [activeTab, setActiveTab] = useState<NavTab>('dashboard');
  const [jobs, setJobs] = useState<Job[]>(MOCK_JOBS);
  const [selectedJob, setSelectedJob] = useState<Job | null>(MOCK_JOBS[0]);
  const [resumes] = useState<Resume[]>(MOCK_RESUMES);
  const [resumeVersions, setResumeVersions] = useState<ResumeVersion[]>(MOCK_VERSIONS);
  const [approvals, setApprovals] = useState<ApprovalRequest[]>(MOCK_APPROVALS);
  const [events, setEvents] = useState<AuditEvent[]>(MOCK_EVENTS);
  const [wsConnected, setWsConnected] = useState<boolean>(false);
  const [isScraping, setIsScraping] = useState<boolean>(false);
  const [activeApprovalModal, setActiveApprovalModal] = useState<ApprovalRequest | null>(null);

  // Load real API data if available
  const loadData = useCallback(async () => {
    try {
      const realJobs = await fetchJobs();
      if (realJobs && realJobs.length > 0) {
        setJobs(realJobs);
        if (!selectedJob) setSelectedJob(realJobs[0]);
      }

      const realApprovals = await fetchApprovals();
      if (realApprovals && realApprovals.length > 0) {
        setApprovals(realApprovals);
      }

      const realEvents = await fetchAuditEvents();
      if (realEvents && realEvents.length > 0) {
        setEvents(realEvents);
      }
    } catch (e) {
      console.warn('Backend endpoint unavailable, running with local memory state.');
    }
  }, [selectedJob]);

  useEffect(() => {
    loadData();
    const ws = connectNotificationsWebSocket(
      (data) => {
        console.log('Real-time WS event received:', data);
        if (data.event_type === 'approval.created' || data.event_type === 'approval.updated') {
          loadData();
        }
      },
      (connected) => setWsConnected(connected)
    );

    return () => {
      ws?.close();
    };
  }, [loadData]);

  // Handle Job Discovery
  const handleDiscoverJob = async (input: {
    title: string;
    company: string;
    location: string;
    url?: string;
    description: string;
    source: JobSource;
  }) => {
    setIsScraping(true);
    try {
      let created: Job;
      try {
        created = await apiCreateJob(input);
      } catch (err) {
        // Fallback local job creation
        created = {
          id: `job-${Date.now()}`,
          external_id: `ext-${Date.now()}`,
          title: input.title || 'Discovered Senior Software Role',
          company: input.company || 'Enterprise Solutions',
          location: input.location || 'Remote',
          url: input.url || 'https://careers.target.com/job/discovered',
          description: input.description || 'Full stack Python, FastAPI, Kafka, and AI pipeline responsibilities.',
          source: input.source || 'PLAYWRIGHT',
          discovered_at: new Date().toISOString(),
          created_at: new Date().toISOString(),
          match_score: 91,
          status: 'MATCHED',
          job_keywords: [
            { keyword: 'Python', normalized_keyword: 'python', category: 'Language', confidence: 0.99 },
            { keyword: 'FastAPI', normalized_keyword: 'fastapi', category: 'Backend', confidence: 0.98 },
            { keyword: 'Kafka', normalized_keyword: 'kafka', category: 'Streaming', confidence: 0.95 },
            { keyword: 'Playwright', normalized_keyword: 'playwright', category: 'Automation', confidence: 0.94 },
            { keyword: 'Aho-Corasick', normalized_keyword: 'aho-corasick', category: 'Algorithm', confidence: 0.99 },
            { keyword: 'LaTeX', normalized_keyword: 'latex', category: 'PDF Engine', confidence: 0.93 }
          ],
          required_skills: ['Python', 'FastAPI', 'Kafka', 'Playwright', 'Aho-Corasick', 'LaTeX', 'Docker'],
          matching_skills: ['Python', 'FastAPI', 'Kafka', 'Playwright', 'Aho-Corasick', 'LaTeX'],
          missing_skills: ['Docker']
        };
      }

      setJobs(prev => [created, ...prev]);
      setSelectedJob(created);

      // Log discovery event
      const newEvent: AuditEvent = {
        id: `evt-${Date.now()}`,
        event_id: `evt-discovered-${Date.now()}`,
        event_type: 'job.discovered',
        correlation_id: `corr-${Date.now()}`,
        pipeline_id: `pipe-${Date.now()}`,
        status: 'COMPLETED',
        created_at: new Date().toISOString(),
        payload: { source: input.source, title: input.title, company: input.company }
      };
      setEvents(prev => [newEvent, ...prev]);

      // Create tailored resume variant and pending approval
      const newVersion: ResumeVersion = {
        id: `rv-version-${Date.now()}`,
        resume_id: MOCK_RESUMES[0].id,
        job_id: created.id,
        version_number: resumeVersions.length + 1,
        version_type: 'TAILORED',
        status: 'GENERATED',
        latex_source: MOCK_VERSIONS[0].latex_source,
        created_at: new Date().toISOString()
      };
      setResumeVersions(prev => [newVersion, ...prev]);

      const newApproval: ApprovalRequest = {
        id: `appr-req-${Date.now()}`,
        pipeline_run_id: `pipe-run-${Date.now()}`,
        status: 'PENDING',
        requested_at: new Date().toISOString(),
        job_title: created.title,
        company: created.company,
        match_score: created.match_score || 90,
        extracted_keywords: ['Python', 'FastAPI', 'Kafka', 'Playwright', 'Aho-Corasick', 'LaTeX'],
        changes_made: [
          `Tailored resume headline for ${created.company} requirements.`,
          'Injected Aho-Corasick algorithm keyword matching markers.',
          'Compiled dynamic LaTeX source code into production PDF.'
        ],
        resume_version_name: `Tailored Resume for ${created.company}`,
        latex_source: MOCK_VERSIONS[0].latex_source
      };

      setApprovals(prev => [newApproval, ...prev]);
    } finally {
      setIsScraping(false);
    }
  };

  // Handle Approval Decision
  const handleRespondApproval = async (id: string, status: 'APPROVED' | 'REJECTED' | 'REVISION_REQUESTED', note?: string) => {
    try {
      await apiRespondApproval(id, status === 'APPROVED' ? 'approved' : 'rejected', note);
    } catch (e) {
      // Local fallback
    }

    setApprovals(prev => prev.map(a => a.id === id ? { ...a, status, reviewer_note: note, responded_at: new Date().toISOString() } : a));

    // Audit event log
    const eventType = status === 'APPROVED' ? 'approval.approved' : status === 'REJECTED' ? 'approval.rejected' : 'approval.revision_requested';
    const auditEvt: AuditEvent = {
      id: `evt-appr-${Date.now()}`,
      event_id: `evt-appr-decided-${Date.now()}`,
      event_type: eventType,
      correlation_id: `corr-${Date.now()}`,
      status: 'COMPLETED',
      created_at: new Date().toISOString(),
      payload: { approval_id: id, decision: status, reviewer_note: note || '' }
    };
    setEvents(prev => [auditEvt, ...prev]);
  };

  return {
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
    activeApprovalModal,
    setActiveApprovalModal,
    handleDiscoverJob,
    handleRespondApproval,
    refreshData: loadData
  };
}

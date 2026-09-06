from typing import TypedDict, Optional, List, Dict, Any


class PipelineState(TypedDict, total=False):
    """Explicit state object passed through LangGraph workflow nodes."""
    pipeline_id: str
    correlation_id: str
    user_id: Optional[str]
    job_id: Optional[str]
    resume_id: Optional[str]
    version_id: Optional[str]
    approval_id: Optional[str]
    job_url: Optional[str]
    job_title: Optional[str]
    company: Optional[str]
    job_description: Optional[str]
    keyword_results: List[str]
    resume_content: Optional[str]
    tailored_resume_content: Optional[str]
    latex_content: Optional[str]
    pdf_path: Optional[str]
    approval_status: str  # PENDING, APPROVED, REJECTED
    current_step: str
    status: str           # PENDING, IN_PROGRESS, COMPLETED, FAILED
    error_message: Optional[str]

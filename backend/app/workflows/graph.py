from typing import Literal
from langgraph.graph import StateGraph, START, END

from app.workflows.state import PipelineState
from app.workflows.nodes.discovery import discover_job
from app.workflows.nodes.processing import validate_job, process_job
from app.workflows.nodes.keywords import extract_keywords
from app.workflows.nodes.resume import (
    process_candidate_resume,
    generate_tailored_resume,
    validate_generated_resume
)
from app.workflows.nodes.approval import (
    request_human_approval,
    wait_for_approval,
    complete_pipeline
)


def route_after_validate_job(state: PipelineState) -> Literal["process_job", "__end__"]:
    """Conditional router after job validation."""
    if state.get("status") == "FAILED":
        return END
    return "process_job"


def route_after_validate_resume(state: PipelineState) -> Literal["request_human_approval", "__end__"]:
    """Conditional router after resume validation."""
    if state.get("status") == "FAILED":
        return END
    return "request_human_approval"


def approval_router(state: PipelineState) -> Literal["complete_pipeline", "__end__"]:
    """Conditional router based on HITL approval status."""
    approval_status = (state.get("approval_status") or "").upper()
    if approval_status == "APPROVED":
        return "complete_pipeline"
    # REJECTED or PENDING ends / pauses workflow safely
    return END


def create_job_pipeline_graph():
    """Build and compile stateful LangGraph workflow for job processing."""
    workflow = StateGraph(PipelineState)

    # Register nodes
    workflow.add_node("discover_job", discover_job)
    workflow.add_node("validate_job", validate_job)
    workflow.add_node("process_job", process_job)
    workflow.add_node("extract_keywords", extract_keywords)
    workflow.add_node("process_candidate_resume", process_candidate_resume)
    workflow.add_node("generate_tailored_resume", generate_tailored_resume)
    workflow.add_node("validate_generated_resume", validate_generated_resume)
    workflow.add_node("request_human_approval", request_human_approval)
    workflow.add_node("wait_for_approval", wait_for_approval)
    workflow.add_node("complete_pipeline", complete_pipeline)

    # Define execution edge flow
    workflow.add_edge(START, "discover_job")
    workflow.add_edge("discover_job", "validate_job")

    workflow.add_conditional_edges("validate_job", route_after_validate_job)
    workflow.add_edge("process_job", "extract_keywords")
    workflow.add_edge("extract_keywords", "process_candidate_resume")
    workflow.add_edge("process_candidate_resume", "generate_tailored_resume")
    workflow.add_edge("generate_tailored_resume", "validate_generated_resume")

    workflow.add_conditional_edges("validate_generated_resume", route_after_validate_resume)
    workflow.add_edge("request_human_approval", "wait_for_approval")

    workflow.add_conditional_edges("wait_for_approval", approval_router)
    workflow.add_edge("complete_pipeline", END)

    return workflow.compile()


job_pipeline_graph = create_job_pipeline_graph()

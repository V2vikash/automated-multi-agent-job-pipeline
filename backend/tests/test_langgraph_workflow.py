import pytest
from app.workflows.graph import job_pipeline_graph
from app.workflows.state import PipelineState


@pytest.mark.asyncio
async def test_successful_langgraph_pipeline_approval_flow():
    """Test full LangGraph pipeline execution with APPROVED status."""
    initial_state: PipelineState = {
        "pipeline_id": "pipe-test-100",
        "correlation_id": "corr-test-100",
        "job_url": "https://example.com/job/test-100",
        "approval_status": "APPROVED",
        "status": "PENDING"
    }

    final_state = await job_pipeline_graph.ainvoke(initial_state)

    assert final_state["status"] == "COMPLETED"
    assert final_state["current_step"] == "complete_pipeline"
    assert len(final_state["keyword_results"]) > 0
    assert "Python" in final_state["keyword_results"]
    assert final_state["tailored_resume_content"] is not None


@pytest.mark.asyncio
async def test_langgraph_pipeline_rejection_flow():
    """Test LangGraph pipeline termination when HITL status is REJECTED."""
    initial_state: PipelineState = {
        "pipeline_id": "pipe-test-200",
        "correlation_id": "corr-test-200",
        "job_url": "https://example.com/job/test-200",
        "approval_status": "REJECTED",
        "status": "PENDING"
    }

    final_state = await job_pipeline_graph.ainvoke(initial_state)

    assert final_state["current_step"] == "wait_for_approval"
    assert final_state["approval_status"] == "REJECTED"
    assert final_state.get("status") != "COMPLETED"


@pytest.mark.asyncio
async def test_langgraph_pipeline_invalid_job_failure():
    """Test workflow termination on invalid job posting."""
    initial_state: PipelineState = {
        "pipeline_id": "pipe-test-300",
        "correlation_id": "corr-test-300",
        "job_url": "invalid",
        "status": "PENDING"
    }

    final_state = await job_pipeline_graph.ainvoke(initial_state)

    assert final_state["status"] == "FAILED"
    assert final_state["current_step"] == "validate_job"
    assert "Invalid job description" in final_state["error_message"]

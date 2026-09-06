import os
import pytest
from app.resume.parser import StructuredCandidateData, CandidateExperience
from app.resume.latex_generator import escape_latex, latex_generator
from app.resume.pdf_compiler import pdf_compiler
from app.resume.optimizer import resume_optimizer


def test_escape_latex_special_characters():
    """Verify special LaTeX symbols are properly escaped."""
    raw = "C++ & Python_3.11 with $100k budget #1 50% increase {tag}"
    escaped = escape_latex(raw)
    assert r"\&" in escaped
    assert r"\_" in escaped
    assert r"\$" in escaped
    assert r"\#" in escaped
    assert r"\%" in escaped
    assert r"\{tag\}" in escaped


def test_latex_generation_structure():
    """Test generating valid LaTeX markup from candidate data."""
    candidate = StructuredCandidateData(
        full_name="Alice Johnson",
        email="alice@example.com",
        skills=["Python", "FastAPI", "Docker"],
        experience=[
            CandidateExperience(
                title="Lead Engineer & Architect",
                company="Acme Corp",
                dates="2022 - Present",
                description="Built high-performance microservices."
            )
        ]
    )
    latex_code = latex_generator.generate_latex(candidate, target_keywords=["PostgreSQL", "Kafka"])

    assert r"\begin{document}" in latex_code
    assert "Alice Johnson" in latex_code
    assert r"Acme Corp" in latex_code
    assert "PostgreSQL" in latex_code
    assert r"\end{document}" in latex_code


def test_pdf_compilation():
    """Test PDF compilation or mock PDF fallback."""
    latex_code = (
        "\\documentclass{article}\n"
        "\\begin{document}\n"
        "Test PDF Resume Document\n"
        "\\end{document}\n"
    )
    success, pdf_path, err = pdf_compiler.compile_latex(latex_code)
    assert success is True
    assert pdf_path != ""
    assert os.path.exists(pdf_path)


def test_resume_match_score_calculation():
    """Test resume optimizer score calculation."""
    candidate = StructuredCandidateData(
        full_name="Bob Smith",
        email="bob@example.com",
        skills=["Python", "FastAPI", "PostgreSQL"]
    )
    result = resume_optimizer.calculate_match_score(candidate, ["Python", "FastAPI", "Kafka", "Docker"])

    assert result["match_score"] == 50.0
    assert "Python" in result["matching_keywords"]
    assert "Kafka" in result["missing_keywords"]

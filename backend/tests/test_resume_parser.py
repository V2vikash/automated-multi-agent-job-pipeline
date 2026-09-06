import pytest
from app.resume.parser import resume_parser, StructuredCandidateData


def test_resume_parser_json_input():
    """Test parsing structured candidate data from JSON payload."""
    json_data = """
    {
        "full_name": "Jane Smith",
        "email": "jane.smith@example.com",
        "phone": "+1-555-0199",
        "summary": "Senior Full Stack Engineer with 7 years experience.",
        "skills": ["Python", "FastAPI", "React", "PostgreSQL", "Docker"],
        "experience": [
            {
                "title": "Lead Software Engineer",
                "company": "Cloud Corp",
                "dates": "2020 - Present",
                "description": "Architected distributed event pipelines with Kafka."
            }
        ],
        "education": [
            {
                "degree": "M.S. Software Engineering",
                "institution": "Stanford University",
                "year": "2020"
            }
        ]
    }
    """
    candidate = resume_parser.parse_resume(json_data)
    assert isinstance(candidate, StructuredCandidateData)
    assert candidate.full_name == "Jane Smith"
    assert candidate.email == "jane.smith@example.com"
    assert "Python" in candidate.skills
    assert candidate.experience[0].company == "Cloud Corp"


def test_resume_parser_plain_text_fallback():
    """Test parsing plain text resume input."""
    text_data = """
    John Doe
    Senior Backend Engineer with passion for scalable APIs.
    Contact: john.doe@example.com | (555) 123-4567
    Skills: Python, FastAPI, PostgreSQL, Apache Kafka, Redis
    """
    candidate = resume_parser.parse_resume(text_data)
    assert candidate.full_name == "John Doe"
    assert candidate.email == "john.doe@example.com"
    assert candidate.phone == "(555) 123-4567"


def test_resume_parser_empty_and_oversized_validation():
    """Test validation errors for empty or oversized inputs."""
    with pytest.raises(ValueError, match="too short"):
        resume_parser.parse_resume("")

    with pytest.raises(ValueError, match="too short"):
        resume_parser.parse_resume("Short")

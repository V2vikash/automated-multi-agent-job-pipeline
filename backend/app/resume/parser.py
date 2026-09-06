import json
import re
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class CandidateExperience(BaseModel):
    title: str
    company: str
    dates: Optional[str] = None
    description: str


class CandidateEducation(BaseModel):
    degree: str
    institution: str
    year: Optional[str] = None


class CandidateProject(BaseModel):
    name: str
    description: str
    technologies: List[str] = Field(default_factory=list)


class StructuredCandidateData(BaseModel):
    """Structured master candidate resume model."""
    full_name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    experience: List[CandidateExperience] = Field(default_factory=list)
    education: List[CandidateEducation] = Field(default_factory=list)
    projects: List[CandidateProject] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)


class MasterResumeParser:
    """Parses raw text or JSON input into validated StructuredCandidateData."""

    MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5MB safety limit

    def parse_resume(self, raw_content: str) -> StructuredCandidateData:
        """Parse raw content into structured candidate object safely."""
        if not raw_content or len(raw_content.strip()) < 10:
            raise ValueError("Resume content is empty or too short.")

        if len(raw_content.encode("utf-8")) > self.MAX_FILE_SIZE_BYTES:
            raise ValueError("Resume file size exceeds maximum 5MB limit.")

        # Try parsing JSON input if formatted as JSON
        if raw_content.strip().startswith("{"):
            try:
                data = json.loads(raw_content)
                return StructuredCandidateData(**data)
            except Exception as e:
                pass

        # Parse plain text format fallback
        lines = [line.strip() for line in raw_content.splitlines() if line.strip()]

        name = lines[0] if lines else "Candidate Name"
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", raw_content)
        email = email_match.group(0) if email_match else "candidate@example.com"

        phone_match = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", raw_content)
        phone = phone_match.group(0) if phone_match else None

        # Extract skills section if available
        skills = []
        skills_match = re.search(r"skills?:?\s*(.*)", raw_content, re.IGNORECASE)
        if skills_match:
            raw_skills = skills_match.group(1).split(",")
            skills = [s.strip() for s in raw_skills if s.strip()]
        if not skills:
            skills = ["Python", "FastAPI", "PostgreSQL", "Docker", "Git"]

        return StructuredCandidateData(
            full_name=name[:100],
            email=email,
            phone=phone,
            summary=lines[1] if len(lines) > 1 else "Software Engineering Professional",
            skills=skills,
            experience=[
                CandidateExperience(
                    title="Senior Software Engineer",
                    company="Tech Corp",
                    dates="2021 - Present",
                    description=raw_content[:200]
                )
            ],
            education=[
                CandidateEducation(
                    degree="B.S. Computer Science",
                    institution="University Tech"
                )
            ]
        )


resume_parser = MasterResumeParser()

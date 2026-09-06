from typing import List, Dict, Any
from app.resume.parser import StructuredCandidateData


class ResumeOptimizer:
    """Calculates keyword match score between candidate profile and target job."""

    def calculate_match_score(self, candidate: StructuredCandidateData, target_keywords: List[str]) -> Dict[str, Any]:
        """Compute keyword match coverage score."""
        if not target_keywords:
            return {"match_score": 100.0, "matching_keywords": [], "missing_keywords": []}

        candidate_skills = {s.lower() for s in candidate.skills}
        matching = []
        missing = []

        for kw in target_keywords:
            if kw.lower() in candidate_skills:
                matching.append(kw)
            else:
                missing.append(kw)

        score = (len(matching) / len(target_keywords)) * 100.0 if target_keywords else 100.0

        return {
            "match_score": round(score, 2),
            "matching_keywords": matching,
            "missing_keywords": missing
        }


resume_optimizer = ResumeOptimizer()

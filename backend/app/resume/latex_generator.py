import re
from typing import List, Optional
from app.resume.parser import StructuredCandidateData


def escape_latex(text: Optional[str]) -> str:
    """Safely escape special LaTeX reserved characters."""
    if not text:
        return ""
    conv = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "\\": r"\textbackslash{}",
    }
    regex = re.compile("|".join(re.escape(str(key)) for key in sorted(conv.keys(), key=lambda item: -len(item))))
    return regex.sub(lambda match: conv[match.group(0)], str(text))


class LaTeXGenerator:
    """Generates clean, compilable LaTeX code from candidate profiles."""

    def generate_latex(
        self,
        candidate: StructuredCandidateData,
        target_keywords: Optional[List[str]] = None
    ) -> str:
        """Render StructuredCandidateData into escaped LaTeX resume string."""
        name = escape_latex(candidate.full_name)
        email = escape_latex(candidate.email)
        phone = escape_latex(candidate.phone or "N/A")
        location = escape_latex(candidate.location or "Remote")
        summary = escape_latex(candidate.summary or "Software Engineering Professional")

        # Emphasize matching target keywords in skills list
        all_skills = list(candidate.skills)
        if target_keywords:
            for kw in target_keywords:
                if kw not in all_skills:
                    all_skills.append(kw)

        escaped_skills = ", ".join(escape_latex(s) for s in all_skills)

        # Experience section
        exp_lines = []
        for exp in candidate.experience:
            t = escape_latex(exp.title)
            c = escape_latex(exp.company)
            d = escape_latex(exp.dates or "")
            desc = escape_latex(exp.description)
            exp_lines.append(
                f"\\textbf{{{t}}} -- \\textit{{{c}}} \\hfill {{{d}}}\\\\\n"
                f"{desc}\n\\vspace{{4pt}}"
            )
        exp_block = "\n".join(exp_lines) or "No experience listed."

        # Education section
        edu_lines = []
        for edu in candidate.education:
            deg = escape_latex(edu.degree)
            inst = escape_latex(edu.institution)
            yr = escape_latex(edu.year or "")
            edu_lines.append(f"\\textbf{{{deg}}}, {inst} \\hfill {{{yr}}}")
        edu_block = "\n".join(edu_lines) or "Bachelor of Science in Computer Science"

        latex_code = (
            "\\documentclass[11pt,a4paper]{article}\n"
            "\\usepackage[margin=0.75in]{geometry}\n"
            "\\pagestyle{empty}\n"
            "\\begin{document}\n\n"
            "\\begin{center}\n"
            f"    {{\\Huge \\textbf{{{name}}}}} \\\\ \\vspace{{4pt}}\n"
            f"    {email} \\ | \\ {phone} \\ | \\ {location}\n"
            "\\end{center}\n\n"
            "\\vspace{10pt}\n\n"
            "\\section*{Professional Summary}\n"
            f"{summary}\n\n"
            "\\vspace{5pt}\n\n"
            "\\section*{Technical Skills}\n"
            f"\\textbf{{Skills:}} {escaped_skills}\n\n"
            "\\vspace{5pt}\n\n"
            "\\section*{Professional Experience}\n"
            f"{exp_block}\n\n"
            "\\vspace{5pt}\n\n"
            "\\section*{Education}\n"
            f"{edu_block}\n\n"
            "\\end{document}\n"
        )
        return latex_code


latex_generator = LaTeXGenerator()

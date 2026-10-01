import json

from groq import Groq
from schemas import ResumeAnalysis


MODEL = "openai/gpt-oss-120b"


RESUME_ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "match_score": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100,
        },
        "matching_skills": {
            "type": "array",
            "items": {"type": "string"},
        },
        "missing_skills": {
            "type": "array",
            "items": {"type": "string"},
        },
        "ats_keywords": {
            "type": "object",
            "properties": {
                "found": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "missing": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "required": ["found", "missing"],
            "additionalProperties": False,
        },
        "resume_problems": {
            "type": "array",
            "items": {"type": "string"},
        },
        "recommendations": {
            "type": "array",
            "items": {"type": "string"},
        },
        "final_result": {
            "type": "string",
        },
    },
    "required": [
        "match_score",
        "matching_skills",
        "missing_skills",
        "ats_keywords",
        "resume_problems",
        "recommendations",
        "final_result",
    ],
    "additionalProperties": False,
}


SYSTEM_PROMPT = """
You are an AI resume analyzer.

Compare a candidate's resume against a specific job description.

Rules:

1. Use only the supplied resume and job description.
2. Never invent skills, experience, education, certifications, tools, or achievements.
3. Matching skills must be supported by the resume.
4. Missing skills are relevant job requirements not clearly supported by the resume.
5. ATS keywords should be meaningful job-specific skills, technologies, tools,
   certifications, role terms, and domain phrases.
6. "found" means the keyword is clearly present or clearly represented in the resume.
7. "missing" means the keyword is relevant to the job description but not clearly
   present in the resume.
8. Resume problems must be specific to the supplied resume.
9. Recommendations must be actionable and must never tell the candidate to falsely
   claim experience.
10. The match score is an analytical estimate, not a hiring prediction.
11. Keep the final result concise.
"""


def analyze_resume(
    resume_text: str,
    job_description: str,
    api_key: str,
) -> dict:

    if not resume_text.strip():
        raise ValueError("Resume text is empty.")

    if not job_description.strip():
        raise ValueError("Job description is empty.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"""
Analyze this resume against this job description.

RESUME:
---BEGIN RESUME---
{resume_text}
---END RESUME---

JOB DESCRIPTION:
---BEGIN JOB DESCRIPTION---
{job_description}
---END JOB DESCRIPTION---
""",
            },
        ],
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "resume_analysis",
                "strict": True,
                "schema": RESUME_ANALYSIS_SCHEMA,
            },
        },
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("Groq returned an empty response.")

    data = json.loads(content)

    # Validate the returned JSON with our Pydantic model.
    validated = ResumeAnalysis.model_validate(data)

    return validated.model_dump()

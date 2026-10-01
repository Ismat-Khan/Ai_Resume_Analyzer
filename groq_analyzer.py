from groq import Groq

from schemas import ResumeAnalysis


MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """
You are an AI resume analyzer.

Compare a candidate's resume against a specific job description.

Rules:
1. Use only the supplied resume and job description.
2. Never invent skills, experience, education, certifications, tools, or achievements.
3. Matching skills must be supported by the resume.
4. Missing skills are relevant job requirements not clearly supported by the resume.
5. ATS keywords should be meaningful job-specific skills, technologies, tools, certifications,
   role terms, and domain phrases.
6. "found" means clearly present or clearly represented in the resume.
7. "missing" means relevant to the job description but not clearly present in the resume.
8. Resume problems must be specific to this resume.
9. Recommendations must be actionable and must never tell the candidate to falsely claim experience.
10. The match score is an analytical estimate, not a hiring prediction or guarantee.
11. Keep the final result concise.
"""


def analyze_resume(resume_text: str, job_description: str, api_key: str) -> dict:
    """Analyze resume/job description and return validated structured data."""

    if not resume_text.strip():
        raise ValueError("Resume text is empty.")
    if not job_description.strip():
        raise ValueError("Job description is empty.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Analyze this resume against this job description.\n\n"
                    "RESUME:\n---BEGIN RESUME---\n"
                    f"{resume_text}\n"
                    "---END RESUME---\n\n"
                    "JOB DESCRIPTION:\n---BEGIN JOB DESCRIPTION---\n"
                    f"{job_description}\n"
                    "---END JOB DESCRIPTION---"
                ),
            },
        ],
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "resume_analysis",
                "strict": True,
                "schema": ResumeAnalysis.model_json_schema(),
            },
        },
    )

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Groq returned an empty response.")

    validated = ResumeAnalysis.model_validate_json(content)
    return validated.model_dump()

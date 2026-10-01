from pydantic import BaseModel, ConfigDict, Field


class ATSKeywords(BaseModel):
    model_config = ConfigDict(extra="forbid")

    found: list[str] = Field(default_factory=list)
    missing: list[str] = Field(default_factory=list)


class ResumeAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    match_score: int = Field(ge=0, le=100)
    matching_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    ats_keywords: ATSKeywords
    resume_problems: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    final_result: str = Field(min_length=1)

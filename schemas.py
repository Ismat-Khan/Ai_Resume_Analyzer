from pydantic import BaseModel, ConfigDict, Field


class ATSKeywords(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "required": ["found", "missing"],
            "additionalProperties": False,
        },
    )

    found: list[str] = Field(default_factory=list)
    missing: list[str] = Field(default_factory=list)


class ResumeAnalysis(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "additionalProperties": False,
        },
    )

    match_score: int = Field(
        ge=0,
        le=100,
        description="Overall resume match score from 0 to 100.",
    )

    matching_skills: list[str] = Field(default_factory=list)

    missing_skills: list[str] = Field(default_factory=list)

    ats_keywords: ATSKeywords

    resume_problems: list[str] = Field(default_factory=list)

    recommendations: list[str] = Field(default_factory=list)

    final_result: str = Field(min_length=1)

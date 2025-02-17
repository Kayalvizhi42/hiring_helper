from pydantic import BaseModel, Field
from typing import List, Optional

class SkillScore(BaseModel):
    skill_name: str = Field(description="Name of the skill being scored")
    required: bool = Field(description="Whether this skill is required or nice-to-have")
    match_level: float = Field(description="How well the candidate's experience matches (0-1)" , ge=0, le=1)
    years_experience: Optional[float] = Field(description="Years of experience with this skill", default=None)
    context_score: float = Field(
        description="How relevant the skill usage context is to the job requirements",
        default=0.5,
        ge=0,
        le=1
    )

class JobMatchScore(BaseModel):
    overall_match: float = Field(
        description="Overall match percentage (0-100)",
        ge=0,
        le=100
    )
    technical_skills_match: int = Field(
        description="Technical skills match percentage",
        ge=0,
        le=100
    )
    soft_skills_match: int = Field(
        description="Soft skills match percentage",
        ge=0,
        le=100
    )
    experience_match: int = Field(
        description="Experience level match percentage",
        ge=0,
        le=100
    )
    education_match: int = Field(
        description="Education requirements match percentage",
        ge=0,
        le=100
    )
    industry_match: int = Field(
        description="Industry experience match percentage",
        ge=0,
        le=100
    )
    skill_details: List[SkillScore] = Field(
        description="Detailed scoring for each skill",
        default_factory=list
    )
    strengths: List[str] = Field(
        description="List of areas where candidate exceeds requirements",
        default_factory=list
    )
    gaps: List[str] = Field(
        description="List of areas needing improvement",
        default_factory=list
    )
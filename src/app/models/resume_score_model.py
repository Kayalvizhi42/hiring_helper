from pydantic import BaseModel, Field
from typing import List

class SkillMatch(BaseModel):
    skill_description: str = Field(description="Name of skill")
    score: int = Field(description="match score (0-5)")

class JobMatchScore(BaseModel):
    technical_skills_match: List[SkillMatch] = Field(
        description="Technical skills match scores (0-5)",
    )
    soft_skills_match: List[SkillMatch] = Field(
        description="Soft skills match scores (0-5)",
    )
    experience_match: List[SkillMatch] = Field(
        description="Experience level & key responsibilities match scores (0-5)",
    )
    education_match: List[SkillMatch] = Field(
        description="Education requirements match scores (0-5)",
    )
    tools_and_technology_match: List[SkillMatch] = Field(
        description="Tools and technology requirements matchs score (0-5).",
    )
    location_match: int = Field(
        description="If candidate is located in same country - 3, in same state - 4 , in same city - 5, else 0",
    )
    industry_match: int = Field(
        description="Industry experience match score (0-5)",
    )
    strengths: List[str] = Field(
        description="List of areas where candidate exceeds requirements",
        default_factory=list
    )
    gaps: List[str] = Field(
        description="List of areas needing improvement",
        default_factory=list
    )
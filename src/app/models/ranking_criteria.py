from pydantic import BaseModel, Field
from typing import List, Optional, Dict
class RankingCriteria(BaseModel):
    criteria: list[str]


class JobRequirements(BaseModel):
    technical_skills: List[str] = Field(
        description="List of required technical skills",
        default_factory=list
    )
    soft_skills: List[str] = Field(
        description="List of required soft skills",
        default_factory=list
    )
    experience_requirements: List[str] = Field(
        description="List of experience requirements",
        default_factory=list
    )
    key_responsibilities: List[str] = Field(
        description="List of key job responsibilities",
        default_factory=list
    )
    education_requirements: List[str] = Field(
        description="List of education requirements",
        default_factory=list
    )
    nice_to_have: List[str] = Field(
        description="List of preferred but not required skills",
        default_factory=list
    )
    job_title: str = Field(
        description="Official job title",
        # default=""
    )
    department: Optional[str] = Field(
        description="Department or team within the company",
        # default=None
    )
    reporting_structure: Optional[str] = Field(
        description="Who this role reports to and any direct reports",
        # default=None
    )
    job_level: Optional[str] = Field(
        description="Level of the position (e.g., Entry, Senior, Lead)",
        # default=None
    )
    location_requirements: Optional[Dict[str, str]] = Field(
        description="Location details including remote/hybrid options",
        # default_factory=dict
    )
    work_schedule: Optional[str] = Field(
        description="Expected work hours and schedule flexibility",
        # default=None
    )
    travel_requirements: Optional[str] = Field(
        description="Expected travel frequency and scope",
        # default=None
    )
    compensation: Optional[Dict[str, str]] = Field(
        description="Salary range and compensation details if provided",
        default_factory=dict
    )
    benefits: List[str] = Field(
        description="List of benefits and perks",
        default_factory=list
    )
    tools_and_technologies: List[str] = Field(
        description="Specific tools, software, or technologies used",
        default_factory=list
    )
    industry_knowledge: List[str] = Field(
        description="Required industry-specific knowledge",
        default_factory=list
    )
    certifications_required: List[str] = Field(
        description="Required certifications or licenses",
        default_factory=list
    )
    security_clearance: Optional[str] = Field(
        description="Required security clearance level if any",
        # default=None
    )
    team_size: Optional[str] = Field(
        description="Size of the immediate team",
        # default=None
    )
    key_projects: List[str] = Field(
        description="Major projects or initiatives mentioned",
        default_factory=list
    )
    cross_functional_interactions: List[str] = Field(
        description="Teams or departments this role interacts with",
        default_factory=list
    )
    career_growth: List[str] = Field(
        description="Career development and growth opportunities",
        default_factory=list
    )
    training_provided: List[str] = Field(
        description="Training or development programs offered",
        default_factory=list
    )
    diversity_inclusion: Optional[str] = Field(
        description="D&I statements or requirements",
        # default=None
    )
    company_values: List[str] = Field(
        description="Company values mentioned in the job posting",
        default_factory=list
    )
    posting_date: Optional[str] = Field(
        description="When the job was posted",
        # default=None
    )
    application_deadline: Optional[str] = Field(
        description="Application deadline if specified",
        # default=None
    )
    special_instructions: List[str] = Field(
        description="Any special application instructions or requirements",
        default_factory=list
    )
    score_explanation: List[str] = Field(
        description="Detailed explanation of how scores were calculated",
        default_factory=list
    )
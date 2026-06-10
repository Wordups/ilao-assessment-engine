from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


CurrentState = Literal["manual", "semi-automated", "automated"]
RiskLevel = Literal["low", "medium", "high"]
AssessmentStatus = Literal["draft", "in_review", "complete"]


class AssessmentSectionItem(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    current_state: CurrentState
    pain_level: int = Field(..., ge=1, le=5)
    risk_level: RiskLevel
    notes: str = Field(default="", max_length=1000)


class AssessmentSection(BaseModel):
    description: str = Field(default="", max_length=1200)
    dependencies: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    items: list[AssessmentSectionItem] = Field(default_factory=list)


class AutomationOpportunity(BaseModel):
    workflow_stage: str
    step_name: str
    opportunity: str
    expected_impact: str
    confidence: Literal["medium", "high"]


class AssessmentBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    organization_name: str = Field(..., min_length=2, max_length=255)
    sector: str = Field(..., min_length=2, max_length=120)
    respondent_name: str = Field(..., min_length=2, max_length=255)
    respondent_email: str = Field(..., min_length=5, max_length=255)
    status: AssessmentStatus = "draft"
    input_section: AssessmentSection
    logic_section: AssessmentSection
    automation_section: AssessmentSection
    output_section: AssessmentSection


class AssessmentCreateRequest(AssessmentBase):
    pass


class AssessmentUpdateRequest(AssessmentBase):
    pass


class AssessmentCreate(AssessmentBase):
    executive_summary: str
    automation_opportunities: list[AutomationOpportunity]


class AssessmentUpdate(AssessmentCreate):
    pass


class AssessmentRead(AssessmentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_id: str
    created_at: datetime
    updated_at: datetime

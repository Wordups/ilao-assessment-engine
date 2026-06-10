import json
from uuid import UUID

from app.domain.ports.assessment_repository import AssessmentRepository
from app.domain.services.analysis import generate_automation_opportunities, generate_executive_summary
from app.domain.services.reporting import build_pdf_report
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentCreateRequest,
    AssessmentRead,
    AssessmentUpdate,
    AssessmentUpdateRequest,
)


class AssessmentService:
    def __init__(self, repository: AssessmentRepository) -> None:
        self.repository = repository

    def list_assessments(self, user_id: str) -> list[AssessmentRead]:
        return self.repository.list_for_user(user_id)

    def get_assessment(self, assessment_id: UUID, user_id: str) -> AssessmentRead | None:
        return self.repository.get_for_user(assessment_id, user_id)

    def create_assessment(self, request: AssessmentCreateRequest, user_id: str) -> AssessmentRead:
        payload = self._enrich(request)
        return self.repository.create(payload, user_id)

    def update_assessment(self, assessment_id: UUID, request: AssessmentUpdateRequest, user_id: str) -> AssessmentRead | None:
        payload = AssessmentUpdate(**self._enrich(request).model_dump())
        return self.repository.update(assessment_id, payload, user_id)

    def export_assessment_json(self, assessment_id: UUID, user_id: str) -> bytes | None:
        assessment = self.get_assessment(assessment_id, user_id)
        if assessment is None:
            return None
        return json.dumps(assessment.model_dump(mode="json"), indent=2).encode("utf-8")

    def generate_pdf_report(self, assessment_id: UUID, user_id: str) -> bytes | None:
        assessment = self.get_assessment(assessment_id, user_id)
        if assessment is None:
            return None
        return build_pdf_report(assessment)

    def _enrich(self, request: AssessmentCreateRequest) -> AssessmentCreate:
        executive_summary = generate_executive_summary(
            request.input_section,
            request.logic_section,
            request.automation_section,
            request.output_section,
        )
        automation_opportunities = generate_automation_opportunities(
            request.input_section,
            request.logic_section,
            request.automation_section,
            request.output_section,
        )
        return AssessmentCreate(
            **request.model_dump(),
            executive_summary=executive_summary,
            automation_opportunities=automation_opportunities,
        )

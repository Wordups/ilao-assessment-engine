from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.application.use_cases.assessments import AssessmentService
from app.core.security import CurrentUser, get_current_user
from app.presentation.api.deps import get_assessment_repository
from app.schemas.assessment import AssessmentCreateRequest, AssessmentRead, AssessmentUpdateRequest


router = APIRouter(prefix="/assessments", tags=["assessments"])


def get_service(repository=Depends(get_assessment_repository)) -> AssessmentService:
    return AssessmentService(repository)


@router.get("", response_model=list[AssessmentRead])
def list_assessments(
    current_user: CurrentUser = Depends(get_current_user),
    service: AssessmentService = Depends(get_service),
) -> list[AssessmentRead]:
    return service.list_assessments(current_user.user_id)


@router.post("", response_model=AssessmentRead, status_code=status.HTTP_201_CREATED)
def create_assessment(
    request: AssessmentCreateRequest,
    current_user: CurrentUser = Depends(get_current_user),
    service: AssessmentService = Depends(get_service),
) -> AssessmentRead:
    return service.create_assessment(request, current_user.user_id)


@router.get("/{assessment_id}", response_model=AssessmentRead)
def get_assessment(
    assessment_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    service: AssessmentService = Depends(get_service),
) -> AssessmentRead:
    assessment = service.get_assessment(assessment_id, current_user.user_id)
    if assessment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")
    return assessment


@router.put("/{assessment_id}", response_model=AssessmentRead)
def update_assessment(
    assessment_id: UUID,
    request: AssessmentUpdateRequest,
    current_user: CurrentUser = Depends(get_current_user),
    service: AssessmentService = Depends(get_service),
) -> AssessmentRead:
    assessment = service.update_assessment(assessment_id, request, current_user.user_id)
    if assessment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")
    return assessment


@router.get("/{assessment_id}/export")
def export_assessment_json(
    assessment_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    service: AssessmentService = Depends(get_service),
) -> Response:
    payload = service.export_assessment_json(assessment_id, current_user.user_id)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")
    return Response(
        content=payload,
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="assessment-{assessment_id}.json"'},
    )


@router.get("/{assessment_id}/report")
def download_report(
    assessment_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    service: AssessmentService = Depends(get_service),
) -> Response:
    file_bytes = service.generate_pdf_report(assessment_id, current_user.user_id)
    if file_bytes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")
    return Response(
        content=file_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="assessment-{assessment_id}.pdf"'},
    )

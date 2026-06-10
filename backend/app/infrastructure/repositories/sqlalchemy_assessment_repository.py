from uuid import UUID

from sqlalchemy.orm import Session

from app.domain.ports.assessment_repository import AssessmentRepository
from app.infrastructure.db.models import AssessmentModel
from app.schemas.assessment import AssessmentCreate, AssessmentRead, AssessmentUpdate


class SQLAlchemyAssessmentRepository(AssessmentRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_for_user(self, user_id: str) -> list[AssessmentRead]:
        rows = (
            self.session.query(AssessmentModel)
            .filter(AssessmentModel.owner_id == user_id)
            .order_by(AssessmentModel.updated_at.desc())
            .all()
        )
        return [AssessmentRead.model_validate(row) for row in rows]

    def get_for_user(self, assessment_id: UUID, user_id: str) -> AssessmentRead | None:
        row = (
            self.session.query(AssessmentModel)
            .filter(AssessmentModel.id == assessment_id, AssessmentModel.owner_id == user_id)
            .one_or_none()
        )
        return AssessmentRead.model_validate(row) if row else None

    def create(self, payload: AssessmentCreate, user_id: str) -> AssessmentRead:
        row = AssessmentModel(owner_id=user_id, **payload.model_dump())
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return AssessmentRead.model_validate(row)

    def update(self, assessment_id: UUID, payload: AssessmentUpdate, user_id: str) -> AssessmentRead | None:
        row = (
            self.session.query(AssessmentModel)
            .filter(AssessmentModel.id == assessment_id, AssessmentModel.owner_id == user_id)
            .one_or_none()
        )
        if row is None:
            return None

        for field, value in payload.model_dump(exclude_none=True).items():
            setattr(row, field, value)
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return AssessmentRead.model_validate(row)

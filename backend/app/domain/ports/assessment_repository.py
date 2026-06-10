from abc import ABC, abstractmethod
from uuid import UUID

from app.schemas.assessment import AssessmentCreate, AssessmentRead, AssessmentUpdate


class AssessmentRepository(ABC):
    @abstractmethod
    def list_for_user(self, user_id: str) -> list[AssessmentRead]:
        raise NotImplementedError

    @abstractmethod
    def get_for_user(self, assessment_id: UUID, user_id: str) -> AssessmentRead | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, payload: AssessmentCreate, user_id: str) -> AssessmentRead:
        raise NotImplementedError

    @abstractmethod
    def update(self, assessment_id: UUID, payload: AssessmentUpdate, user_id: str) -> AssessmentRead | None:
        raise NotImplementedError

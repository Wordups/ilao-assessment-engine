from fastapi import Depends
from sqlalchemy.orm import Session

from app.domain.ports.assessment_repository import AssessmentRepository
from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.sqlalchemy_assessment_repository import SQLAlchemyAssessmentRepository


def get_assessment_repository(db: Session = Depends(get_db)) -> AssessmentRepository:
    return SQLAlchemyAssessmentRepository(db)

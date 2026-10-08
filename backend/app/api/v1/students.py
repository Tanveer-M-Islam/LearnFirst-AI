from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.student import (
    StudentCreate,
    StudentRead,
)
from app.services.student_service import (
    StudentService,
)


router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@router.post(
    "",
    response_model=StudentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    data: StudentCreate,
    db: Session = Depends(get_db),
):
    return StudentService.create_student(
        db=db,
        data=data,
    )


@router.get(
    "/{student_id}",
    response_model=StudentRead,
)
def get_student(
    student_id: str,
    db: Session = Depends(get_db),
):
    student = StudentService.get_student(
        db=db,
        student_id=student_id,
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found.",
        )

    return student
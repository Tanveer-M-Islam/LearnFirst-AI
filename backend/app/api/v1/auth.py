from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import (
    Session,
)

from app.database.session import (
    get_db,
)
from app.schemas.student import (
    StudentLogin,
    StudentRead,
)
from app.services.student_service import (
    StudentService,
)


router = APIRouter(
    prefix="/auth",
    tags=[
        "Authentication",
    ],
)


@router.post(
    "/login",
    response_model=StudentRead,
)
def login_student(
    data: StudentLogin,
    db: Session = Depends(
        get_db
    ),
):

    student = (
        StudentService
        .login_student(
            db=db,
            username=data.username,
            password=data.password,
        )
    )


    if (
        student is None
    ):

        raise HTTPException(
            status_code=401,
            detail=(
                "Invalid username "
                "or password."
            ),
        )


    return student
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import (
    Session,
)

from app.database.session import (
    get_db,
)
from app.schemas.student import (
    StudentCreate,
    StudentCredentialsUpdate,
    StudentLogin,
    StudentRead,
)
from app.services.student_service import (
    StudentService,
)


router = APIRouter(
    prefix="/students",
    tags=[
        "Students",
    ],
)


# ============================================================
# Create student
# ============================================================


@router.post(
    "",
    response_model=StudentRead,
    status_code=(
        status.HTTP_201_CREATED
    ),
)
def create_student(
    data: StudentCreate,
    db: Session = Depends(
        get_db
    ),
):

    try:

        return (
            StudentService
            .create_student(
                db=db,
                data=data,
            )
        )


    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(
                exc
            ),
        ) from exc


# ============================================================
# LOGIN
#
# Keep this ABOVE /{student_id}.
# Otherwise "login" can be interpreted as a student ID.
# ============================================================


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

            username=(
                data.username
            ),

            password=(
                data.password
            ),
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


# ============================================================
# Set / change login credentials
# ============================================================


@router.put(
    "/{student_id}/credentials",
    response_model=StudentRead,
)
@router.patch(
    "/{student_id}/credentials",
    response_model=StudentRead,
)
def update_student_credentials(
    student_id: str,
    data: StudentCredentialsUpdate,
    db: Session = Depends(
        get_db
    ),
):

    try:

        student = (
            StudentService
            .update_credentials(
                db=db,
                student_id=student_id,
                data=data,
            )
        )


    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(
                exc
            ),
        ) from exc


    if (
        student is None
    ):

        raise HTTPException(
            status_code=404,
            detail=(
                "Student not found."
            ),
        )


    return student


# ============================================================
# Get student
#
# Keep this AFTER /login.
# ============================================================


@router.get(
    "/{student_id}",
    response_model=StudentRead,
)
def get_student(
    student_id: str,
    db: Session = Depends(
        get_db
    ),
):

    student = (
        StudentService
        .get_student(
            db=db,
            student_id=student_id,
        )
    )


    if (
        student is None
    ):

        raise HTTPException(
            status_code=404,
            detail=(
                "Student not found."
            ),
        )


    return student
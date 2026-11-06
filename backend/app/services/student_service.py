import hashlib
import hmac
import os

from sqlalchemy.orm import (
    Session,
)

from app.database.models.student import (
    StudentProfile,
)
from app.database.repositories.student_repository import (
    StudentRepository,
)
from app.schemas.enums import (
    AgeGroup,
)
from app.schemas.student import (
    StudentCreate,
    StudentCredentialsUpdate,
)


PASSWORD_ITERATIONS = 200_000


def determine_age_group(
    age: int,
) -> AgeGroup:

    if (
        7 <= age <= 9
    ):

        return (
            AgeGroup.FOUNDATION
        )


    if (
        10 <= age <= 12
    ):

        return (
            AgeGroup.DEVELOPING
        )


    if (
        13 <= age <= 14
    ):

        return (
            AgeGroup.INDEPENDENT
        )


    raise ValueError(
        "LearnFirst AI currently "
        "supports ages 7–14."
    )


def normalize_username(
    username: str,
) -> str:

    return (
        username
        .strip()
        .lower()
    )


def hash_password(
    password: str,
) -> str:

    salt = os.urandom(
        16
    )


    password_hash = (
        hashlib.pbkdf2_hmac(
            "sha256",

            password.encode(
                "utf-8"
            ),

            salt,

            PASSWORD_ITERATIONS,
        )
    )


    return (
        "pbkdf2_sha256"
        + "$"
        + str(
            PASSWORD_ITERATIONS
        )
        + "$"
        + salt.hex()
        + "$"
        + password_hash.hex()
    )


def verify_password(
    password: str,
    stored_hash: str,
) -> bool:

    try:

        (
            algorithm,
            iterations_text,
            salt_hex,
            expected_hex,
        ) = stored_hash.split(
            "$"
        )


        if (
            algorithm
            != "pbkdf2_sha256"
        ):

            return False


        iterations = int(
            iterations_text
        )


        salt = bytes.fromhex(
            salt_hex
        )


        expected = bytes.fromhex(
            expected_hex
        )


    except (
        ValueError,
        TypeError,
    ):

        return False


    actual = (
        hashlib.pbkdf2_hmac(
            "sha256",

            password.encode(
                "utf-8"
            ),

            salt,

            iterations,
        )
    )


    return hmac.compare_digest(
        actual,
        expected,
    )


class StudentService:

    @staticmethod
    def create_student(
        db: Session,
        data: StudentCreate,
    ) -> StudentProfile:

        age_group = (
            determine_age_group(
                data.age
            )
        )


        username = None

        password_hash = None


        if (
            data.username
            and data.password
        ):

            username = (
                normalize_username(
                    data.username
                )
            )


            existing = (
                StudentRepository
                .get_by_username(
                    db=db,
                    username=username,
                )
            )


            if (
                existing
                is not None
            ):

                raise ValueError(
                    "Username is already "
                    "in use."
                )


            password_hash = (
                hash_password(
                    data.password
                )
            )


        student = StudentProfile(

            parent_id=(
                data.parent_id
            ),

            display_name=(
                data.display_name
                .strip()
            ),

            username=(
                username
            ),

            password_hash=(
                password_hash
            ),

            age=(
                data.age
            ),

            grade=(
                data.grade
            ),

            age_group=(
                age_group.value
            ),

            preferred_language=(
                data.preferred_language
            ),

            curriculum_profile=(
                data.curriculum_profile
            ),
        )


        return (
            StudentRepository.create(
                db=db,
                student=student,
            )
        )


    @staticmethod
    def get_student(
        db: Session,
        student_id: str,
    ) -> StudentProfile | None:

        return (
            StudentRepository
            .get_by_id(
                db=db,
                student_id=student_id,
            )
        )


    @staticmethod
    def login_student(
        db: Session,
        username: str,
        password: str,
    ) -> StudentProfile | None:

        student = (
            StudentRepository
            .get_by_username(
                db=db,

                username=(
                    normalize_username(
                        username
                    )
                ),
            )
        )


        if (
            student is None
        ):

            return None


        if (
            not student.password_hash
        ):

            return None


        if (
            not verify_password(
                password,
                student.password_hash,
            )
        ):

            return None


        return student


    @staticmethod
    def update_credentials(
        db: Session,
        student_id: str,
        data: StudentCredentialsUpdate,
    ) -> StudentProfile | None:

        student = (
            StudentRepository
            .get_by_id(
                db=db,
                student_id=student_id,
            )
        )


        if (
            student is None
        ):

            return None


        # ==================================
        # Existing credentials
        #
        # Current password is required.
        # ==================================

        if (
            student.password_hash
            is not None
        ):

            if (
                not data.current_password
            ):

                raise ValueError(
                    "Current password is "
                    "required to change "
                    "login credentials."
                )


            valid_current_password = (
                verify_password(
                    data.current_password,
                    student.password_hash,
                )
            )


            if (
                not valid_current_password
            ):

                raise ValueError(
                    "Current password "
                    "is incorrect."
                )


        new_username = (
            normalize_username(
                data.username
            )
        )


        existing = (
            StudentRepository
            .get_by_username(
                db=db,
                username=new_username,
            )
        )


        if (
            existing is not None
            and existing.id
            != student.id
        ):

            raise ValueError(
                "Username is already "
                "in use."
            )


        student.username = (
            new_username
        )


        student.password_hash = (
            hash_password(
                data.password
            )
        )


        return (
            StudentRepository.save(
                db=db,
                student=student,
            )
        )
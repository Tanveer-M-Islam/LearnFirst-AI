from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)

from app.schemas.enums import (
    AgeGroup,
)


class StudentCreate(BaseModel):

    display_name: str = Field(
        min_length=1,
        max_length=100,
    )

    age: int = Field(
        ge=7,
        le=14,
    )

    grade: str = Field(
        min_length=1,
        max_length=20,
    )

    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=50,
    )

    password: str | None = Field(
        default=None,
        min_length=6,
        max_length=128,
    )

    parent_id: str | None = None

    preferred_language: str = "en"

    curriculum_profile: str = (
        "bangladesh_english_v1"
    )


    @model_validator(
        mode="after"
    )
    def validate_credentials(
        self,
    ):

        has_username = bool(
            self.username
        )

        has_password = bool(
            self.password
        )


        if (
            has_username
            != has_password
        ):

            raise ValueError(
                "Username and password "
                "must be provided together."
            )


        return self


class StudentLogin(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=50,
    )

    password: str = Field(
        min_length=6,
        max_length=128,
    )


class StudentCredentialsUpdate(
    BaseModel,
):

    username: str = Field(
        min_length=3,
        max_length=50,
    )

    password: str = Field(
        min_length=6,
        max_length=128,
    )

    current_password: (
        str | None
    ) = Field(
        default=None,
        min_length=6,
        max_length=128,
    )


class StudentRead(BaseModel):

    id: str

    parent_id: str | None

    display_name: str

    username: str | None

    age: int

    grade: str

    age_group: AgeGroup

    preferred_language: str

    curriculum_profile: str

    created_at: datetime

    updated_at: datetime


    model_config = ConfigDict(
        from_attributes=True
    )
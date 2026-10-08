from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.enums import AgeGroup


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

    parent_id: str | None = None

    preferred_language: str = "en"

    curriculum_profile: str = (
        "bangladesh_english_v1"
    )


class StudentRead(BaseModel):
    id: str

    parent_id: str | None

    display_name: str

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
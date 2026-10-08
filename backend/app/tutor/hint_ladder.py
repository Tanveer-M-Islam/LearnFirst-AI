from dataclasses import dataclass

from app.schemas.enums import (
    AgeGroup,
    TutorAction,
)


@dataclass(frozen=True)
class HintLevel:
    level: int

    name: str

    action: TutorAction


HINT_LEVELS = {
    0: HintLevel(
        level=0,
        name="DIAGNOSE",
        action=TutorAction.ASK_PRIOR_KNOWLEDGE,
    ),

    1: HintLevel(
        level=1,
        name="RECALL",
        action=TutorAction.GIVE_HINT,
    ),

    2: HintLevel(
        level=2,
        name="GUIDING_QUESTION",
        action=TutorAction.ASK_GUIDING_QUESTION,
    ),

    3: HintLevel(
        level=3,
        name="SMALL_HINT",
        action=TutorAction.GIVE_HINT,
    ),

    4: HintLevel(
        level=4,
        name="SIMILAR_EXAMPLE",
        action=TutorAction.GIVE_SIMILAR_EXAMPLE,
    ),

    5: HintLevel(
        level=5,
        name="BREAK_INTO_STEPS",
        action=TutorAction.BREAK_INTO_STEPS,
    ),

    6: HintLevel(
        level=6,
        name="STRONG_GUIDANCE",
        action=TutorAction.GIVE_STRONG_GUIDANCE,
    ),

    7: HintLevel(
        level=7,
        name="FULL_TEACHING",
        action=(
            TutorAction.GIVE_FULL_TEACHING_EXPLANATION
        ),
    ),
}


MIN_HINT_LEVEL = 0

MAX_HINT_LEVEL = 7


def clamp_hint_level(
    level: int,
) -> int:

    return max(
        MIN_HINT_LEVEL,
        min(
            level,
            MAX_HINT_LEVEL,
        ),
    )


def get_hint_action(
    level: int,
) -> TutorAction:

    safe_level = clamp_hint_level(
        level
    )

    return HINT_LEVELS[
        safe_level
    ].action


def calculate_next_hint_level(
    current_level: int,
    age_group: AgeGroup,
    repeated_confusion: bool = False,
) -> int:

    increase = 1

    # Foundation learners can receive
    # stronger assistance faster if
    # they repeatedly indicate confusion.
    if (
        age_group == AgeGroup.FOUNDATION
        and repeated_confusion
    ):
        increase = 2

    return clamp_hint_level(
        current_level + increase
    )
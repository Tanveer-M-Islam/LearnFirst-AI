from dataclasses import dataclass

from app.schemas.adaptive import (
    AdaptiveActivity,
    AdaptiveSupport,
    ExplanationDepth,
)
from app.schemas.enums import (
    AgeGroup,
    DifficultyLevel,
    MasteryState,
)


@dataclass(
    frozen=True
)
class AdaptiveSignals:

    age_group: AgeGroup

    mastery_state: (
        MasteryState
    )

    recommended_difficulty: (
        DifficultyLevel
    )

    diagnostic_score: (
        float | None
    )

    mastery_score: (
        float | None
    )

    total_attempts: int

    independent_attempts: int

    independent_attempt_rate: float

    independent_success_rate: float

    average_hint_level: float

    direct_answer_requests: int

    retry_success_count: int


@dataclass(
    frozen=True
)
class AdaptiveDecision:

    difficulty: (
        DifficultyLevel
    )

    support_level: (
        AdaptiveSupport
    )

    explanation_depth: (
        ExplanationDepth
    )

    next_activity: (
        AdaptiveActivity
    )

    reason_codes: tuple[
        str,
        ...,
    ]

    summary: str


class AdaptiveLearningEngine:

    @classmethod
    def decide(
        cls,
        signals: AdaptiveSignals,
    ) -> AdaptiveDecision:

        reasons: list[str] = []


        # ----------------------------------
        # 1. Explanation depth from age
        # ----------------------------------

        explanation_depth = (
            cls._explanation_depth(
                signals.age_group
            )
        )


        # ----------------------------------
        # 2. No diagnostic yet
        # ----------------------------------

        if (
            signals
            .diagnostic_score
            is None
        ):

            reasons.append(
                "NO_DIAGNOSTIC"
            )

            return AdaptiveDecision(
                difficulty=(
                    DifficultyLevel.EASY
                ),

                support_level=(
                    AdaptiveSupport.GENTLE
                ),

                explanation_depth=(
                    explanation_depth
                ),

                next_activity=(
                    AdaptiveActivity
                    .TAKE_DIAGNOSTIC
                ),

                reason_codes=tuple(
                    reasons
                ),

                summary=(
                    "A diagnostic should "
                    "establish the learner's "
                    "starting level before "
                    "difficulty is adapted."
                ),
            )


        # ----------------------------------
        # 3. Start from assessment
        #    recommendation
        # ----------------------------------

        difficulty = (
            signals
            .recommended_difficulty
        )


        # ----------------------------------
        # 4. Detect struggling learner
        # ----------------------------------

        low_independent_success = (
            signals
            .independent_attempts
            >= 2

            and signals
            .independent_success_rate
            < 50.0
        )

        high_hint_usage = (
            signals.total_attempts
            >= 2

            and signals
            .average_hint_level
            >= 4.0
        )

        answer_dependence = (
            signals
            .direct_answer_requests
            >= 2
        )

        struggling = (
            low_independent_success
            or high_hint_usage
        )


        if low_independent_success:

            reasons.append(
                "LOW_INDEPENDENT_SUCCESS"
            )

        if high_hint_usage:

            reasons.append(
                "HIGH_HINT_USAGE"
            )

        if answer_dependence:

            reasons.append(
                "REPEATED_DIRECT_ANSWER_REQUESTS"
            )


        # ----------------------------------
        # 5. Detect strong independence
        # ----------------------------------

        strong_independence = (
            signals.total_attempts
            >= 3

            and signals
            .independent_attempt_rate
            >= 60.0

            and signals
            .independent_success_rate
            >= 80.0

            and signals
            .average_hint_level
            <= 2.0
        )

        if strong_independence:

            reasons.append(
                "STRONG_INDEPENDENT_PERFORMANCE"
            )


        # ----------------------------------
        # 6. Adjust difficulty
        # ----------------------------------

        if struggling:

            difficulty = (
                cls._lower_difficulty(
                    difficulty
                )
            )

            reasons.append(
                "DIFFICULTY_REDUCED"
            )

        elif strong_independence:

            difficulty = (
                cls._raise_difficulty(
                    difficulty
                )
            )

            reasons.append(
                "DIFFICULTY_INCREASED"
            )


        # Strong mastery should permit
        # challenging work.

        if (
            signals.mastery_state
            == MasteryState.STRONG
        ):

            difficulty = (
                DifficultyLevel
                .CHALLENGING
            )

            reasons.append(
                "STRONG_MASTERY"
            )


        # ----------------------------------
        # 7. Support level
        # ----------------------------------

        if (
            high_hint_usage
            or (
                low_independent_success
                and answer_dependence
            )
        ):

            support_level = (
                AdaptiveSupport.STRONG
            )

        elif (
            signals
            .average_hint_level
            >= 2.0

            or signals
            .independent_attempt_rate
            < 50.0

            or answer_dependence
        ):

            support_level = (
                AdaptiveSupport.GUIDED
            )

        else:

            support_level = (
                AdaptiveSupport.GENTLE
            )


        # ----------------------------------
        # 8. Choose next activity
        # ----------------------------------

        if (
            signals.mastery_score
            is not None

            and signals
            .mastery_state
            == MasteryState.STRONG
        ):

            activity = (
                AdaptiveActivity
                .CHALLENGE_PRACTICE
            )


        elif struggling:

            activity = (
                AdaptiveActivity
                .REVIEW_FOUNDATION
            )


        elif (
            signals.mastery_score
            is None

            and signals
            .total_attempts
            >= 3

            and signals
            .independent_success_rate
            >= 60.0

            and signals
            .average_hint_level
            <= 3.0
        ):

            activity = (
                AdaptiveActivity
                .TAKE_MASTERY_CHECK
            )

            reasons.append(
                "READY_FOR_MASTERY_CHECK"
            )


        elif strong_independence:

            activity = (
                AdaptiveActivity
                .INDEPENDENT_PRACTICE
            )


        else:

            activity = (
                AdaptiveActivity
                .GUIDED_PRACTICE
            )


        # ----------------------------------
        # 9. Human-readable summary
        # ----------------------------------

        summary = (
            cls._summary(
                activity=activity,
                difficulty=difficulty,
                support=(
                    support_level
                ),
            )
        )


        return AdaptiveDecision(
            difficulty=difficulty,

            support_level=(
                support_level
            ),

            explanation_depth=(
                explanation_depth
            ),

            next_activity=(
                activity
            ),

            reason_codes=tuple(
                reasons
            ),

            summary=summary,
        )


    @staticmethod
    def _explanation_depth(
        age_group: AgeGroup,
    ) -> ExplanationDepth:

        if (
            age_group
            == AgeGroup.FOUNDATION
        ):

            return (
                ExplanationDepth
                .SIMPLE
            )

        if (
            age_group
            == AgeGroup.INDEPENDENT
        ):

            return (
                ExplanationDepth
                .DEEP
            )

        return (
            ExplanationDepth
            .BALANCED
        )


    @staticmethod
    def _lower_difficulty(
        difficulty: DifficultyLevel,
    ) -> DifficultyLevel:

        if (
            difficulty
            == DifficultyLevel
            .CHALLENGING
        ):

            return (
                DifficultyLevel
                .MODERATE
            )

        if (
            difficulty
            == DifficultyLevel
            .MODERATE
        ):

            return (
                DifficultyLevel.EASY
            )

        return (
            DifficultyLevel.EASY
        )


    @staticmethod
    def _raise_difficulty(
        difficulty: DifficultyLevel,
    ) -> DifficultyLevel:

        if (
            difficulty
            == DifficultyLevel.EASY
        ):

            return (
                DifficultyLevel
                .MODERATE
            )

        if (
            difficulty
            == DifficultyLevel
            .MODERATE
        ):

            return (
                DifficultyLevel
                .CHALLENGING
            )

        return (
            DifficultyLevel
            .CHALLENGING
        )


    @staticmethod
    def _summary(
        activity: AdaptiveActivity,
        difficulty: DifficultyLevel,
        support: AdaptiveSupport,
    ) -> str:

        activity_labels = {
            AdaptiveActivity
            .TAKE_DIAGNOSTIC:
                (
                    "take a diagnostic "
                    "assessment"
                ),

            AdaptiveActivity
            .GUIDED_PRACTICE:
                "continue guided practice",

            AdaptiveActivity
            .INDEPENDENT_PRACTICE:
                (
                    "practice more "
                    "independently"
                ),

            AdaptiveActivity
            .REVIEW_FOUNDATION:
                (
                    "review the foundation "
                    "with additional support"
                ),

            AdaptiveActivity
            .TAKE_MASTERY_CHECK:
                (
                    "take an independent "
                    "mastery check"
                ),

            AdaptiveActivity
            .CHALLENGE_PRACTICE:
                (
                    "move to challenge "
                    "practice"
                ),
        }

        return (
            "Recommend "
            + activity_labels[
                activity
            ]
            + " at "
            + difficulty.value.lower()
            + " difficulty with "
            + support.value.lower()
            + " tutor support."
        )
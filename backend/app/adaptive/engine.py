from dataclasses import (
    dataclass,
)

from app.schemas.adaptive import (
    AdaptiveActivity,
    AdaptiveSupport,
    ExplanationDepth,
    ResponsePace,
    ResponsePaceSource,
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

    measured_response_count: int = 0

    average_response_latency_ms: (
        float | None
    ) = None


    # ----------------------------------
    # Phase 14
    # ----------------------------------

    baseline_ready: bool = False

    personalized_response_pace: (
        ResponsePace
    ) = (
        ResponsePace
        .INSUFFICIENT_DATA
    )


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

    response_pace: (
        ResponsePace
    )

    response_pace_source: (
        ResponsePaceSource
    )

    reason_codes: tuple[
        str,
        ...,
    ]

    summary: str


class AdaptiveLearningEngine:

    MIN_LATENCY_SAMPLES = 3


    @classmethod
    def decide(
        cls,
        signals: AdaptiveSignals,
    ) -> AdaptiveDecision:

        reasons: list[str] = []


        explanation_depth = (
            cls._explanation_depth(
                signals.age_group
            )
        )


        # ----------------------------------
        # Response pace
        #
        # Personal baseline has priority.
        # Fixed age thresholds are only
        # fallback behavior.
        # ----------------------------------

        (
            response_pace,
            response_pace_source,
        ) = (
            cls._response_pace(
                signals
            )
        )


        if (
            response_pace_source
            == (
                ResponsePaceSource
                .PERSONAL_BASELINE
            )
        ):

            reasons.append(
                "PERSONAL_BASELINE_USED"
            )


        elif (
            response_pace_source
            == (
                ResponsePaceSource
                .AGE_GROUP_FALLBACK
            )
        ):

            reasons.append(
                "AGE_GROUP_PACE_FALLBACK"
            )


        if (
            response_pace
            == ResponsePace.FAST
        ):

            reasons.append(
                "FAST_RESPONSE_PATTERN"
            )


        elif (
            response_pace
            == ResponsePace.SLOW
        ):

            reasons.append(
                "SLOW_RESPONSE_PATTERN"
            )


        # ----------------------------------
        # No diagnostic
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

                response_pace=(
                    response_pace
                ),

                response_pace_source=(
                    response_pace_source
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


        difficulty = (
            signals
            .recommended_difficulty
        )


        # ----------------------------------
        # Core struggle
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
        # Slow pace becomes meaningful only
        # when another struggle signal
        # supports it.
        # ----------------------------------

        latency_supported_struggle = (
            response_pace
            == ResponsePace.SLOW

            and signals
            .total_attempts
            >= 3

            and (
                signals
                .independent_success_rate
                < 70.0

                or signals
                .average_hint_level
                >= 3.0
            )
        )


        if latency_supported_struggle:

            reasons.append(
                "SLOW_RESPONSE_WITH_STRUGGLE"
            )


        struggling = (
            low_independent_success

            or high_hint_usage

            or latency_supported_struggle
        )


        # ----------------------------------
        # Independence
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
        # Fast responses only support
        # advancement if performance
        # also supports it.
        # ----------------------------------

        latency_supported_progress = (
            response_pace
            == ResponsePace.FAST

            and signals
            .total_attempts
            >= 3

            and signals
            .independent_attempt_rate
            >= 60.0

            and signals
            .independent_success_rate
            >= 70.0

            and signals
            .average_hint_level
            <= 2.0
        )


        if latency_supported_progress:

            reasons.append(
                "FAST_RESPONSE_WITH_STRONG_PERFORMANCE"
            )


        ready_to_advance = (
            strong_independence

            or latency_supported_progress
        )


        # ----------------------------------
        # Difficulty
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


        elif ready_to_advance:

            difficulty = (
                cls._raise_difficulty(
                    difficulty
                )
            )

            reasons.append(
                "DIFFICULTY_INCREASED"
            )


        # ----------------------------------
        # Strong mastery
        # ----------------------------------

        if (
            signals.mastery_state
            == MasteryState.STRONG
        ):

            reasons.append(
                "STRONG_MASTERY"
            )


            if not struggling:

                difficulty = (
                    DifficultyLevel
                    .CHALLENGING
                )


            else:

                reasons.append(
                    "MASTERY_HELD_BY_CURRENT_STRUGGLE"
                )


        # ----------------------------------
        # Support
        # ----------------------------------

        if (
            high_hint_usage

            or latency_supported_struggle

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
        # Activity
        # ----------------------------------

        if struggling:

            activity = (
                AdaptiveActivity
                .REVIEW_FOUNDATION
            )


        elif (
            signals.mastery_score
            is not None

            and signals.mastery_state
            == MasteryState.STRONG
        ):

            activity = (
                AdaptiveActivity
                .CHALLENGE_PRACTICE
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


        elif ready_to_advance:

            activity = (
                AdaptiveActivity
                .INDEPENDENT_PRACTICE
            )


        else:

            activity = (
                AdaptiveActivity
                .GUIDED_PRACTICE
            )


        summary = (
            cls._summary(
                activity=(
                    activity
                ),

                difficulty=(
                    difficulty
                ),

                support=(
                    support_level
                ),
            )
        )


        return AdaptiveDecision(
            difficulty=(
                difficulty
            ),

            support_level=(
                support_level
            ),

            explanation_depth=(
                explanation_depth
            ),

            next_activity=(
                activity
            ),

            response_pace=(
                response_pace
            ),

            response_pace_source=(
                response_pace_source
            ),

            reason_codes=tuple(
                reasons
            ),

            summary=(
                summary
            ),
        )


    # ======================================================
    # Pace selection
    # ======================================================

    @classmethod
    def _response_pace(
        cls,
        signals: AdaptiveSignals,
    ) -> tuple[
        ResponsePace,
        ResponsePaceSource,
    ]:

        # ----------------------------------
        # First choice:
        # learner's personal baseline
        # ----------------------------------

        if (
            signals.baseline_ready

            and signals
            .personalized_response_pace
            != (
                ResponsePace
                .INSUFFICIENT_DATA
            )
        ):

            return (
                signals
                .personalized_response_pace,

                ResponsePaceSource
                .PERSONAL_BASELINE,
            )


        # ----------------------------------
        # Fallback:
        # age-group engineering threshold
        # ----------------------------------

        age_pace = (
            cls._age_group_response_pace(
                signals
            )
        )


        if (
            age_pace
            == ResponsePace
            .INSUFFICIENT_DATA
        ):

            return (
                age_pace,

                ResponsePaceSource
                .INSUFFICIENT_DATA,
            )


        return (
            age_pace,

            ResponsePaceSource
            .AGE_GROUP_FALLBACK,
        )


    @classmethod
    def _age_group_response_pace(
        cls,
        signals: AdaptiveSignals,
    ) -> ResponsePace:

        if (
            signals
            .measured_response_count
            < cls.MIN_LATENCY_SAMPLES

            or signals
            .average_response_latency_ms
            is None
        ):

            return (
                ResponsePace
                .INSUFFICIENT_DATA
            )


        latency = (
            signals
            .average_response_latency_ms
        )


        (
            fast_threshold,
            slow_threshold,
        ) = (
            cls._latency_thresholds(
                signals.age_group
            )
        )


        if (
            latency
            <= fast_threshold
        ):

            return (
                ResponsePace.FAST
            )


        if (
            latency
            >= slow_threshold
        ):

            return (
                ResponsePace.SLOW
            )


        return (
            ResponsePace.TYPICAL
        )


    @staticmethod
    def _latency_thresholds(
        age_group: AgeGroup,
    ) -> tuple[
        float,
        float,
    ]:

        if (
            age_group
            == AgeGroup.FOUNDATION
        ):

            return (
                20_000.0,
                60_000.0,
            )


        if (
            age_group
            == AgeGroup.INDEPENDENT
        ):

            return (
                12_000.0,
                35_000.0,
            )


        return (
            15_000.0,
            45_000.0,
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
                ExplanationDepth.SIMPLE
            )


        if (
            age_group
            == AgeGroup.INDEPENDENT
        ):

            return (
                ExplanationDepth.DEEP
            )


        return (
            ExplanationDepth.BALANCED
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
                DifficultyLevel.MODERATE
            )


        if (
            difficulty
            == DifficultyLevel.MODERATE
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
                DifficultyLevel.MODERATE
            )


        if (
            difficulty
            == DifficultyLevel.MODERATE
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
            .TAKE_DIAGNOSTIC: (
                "take a diagnostic "
                "assessment"
            ),

            AdaptiveActivity
            .GUIDED_PRACTICE: (
                "continue guided "
                "practice"
            ),

            AdaptiveActivity
            .INDEPENDENT_PRACTICE: (
                "practice more "
                "independently"
            ),

            AdaptiveActivity
            .REVIEW_FOUNDATION: (
                "review the foundation "
                "with additional support"
            ),

            AdaptiveActivity
            .TAKE_MASTERY_CHECK: (
                "take an independent "
                "mastery check"
            ),

            AdaptiveActivity
            .CHALLENGE_PRACTICE: (
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
            + difficulty
            .value
            .lower()
            + " difficulty with "
            + support
            .value
            .lower()
            + " tutor support."
        )
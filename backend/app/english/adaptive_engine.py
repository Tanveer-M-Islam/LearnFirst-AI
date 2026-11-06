from dataclasses import dataclass

from app.schemas.adaptive import (
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
from app.schemas.english_adaptive import (
    EnglishAdaptiveActivity,
)


@dataclass(frozen=True)
class EnglishAdaptiveSignals:
    age_group: AgeGroup

    total_attempts: int

    correct_attempts: int

    partial_attempts: int

    understanding_score_percent: float

    independent_attempt_rate: float

    independent_success_rate: float

    average_hint_level: float

    direct_answer_requests: int

    measured_response_count: int = 0

    average_response_latency_ms: (
        float | None
    ) = None

    baseline_ready: bool = False

    personalized_response_pace: (
        ResponsePace
    ) = ResponsePace.INSUFFICIENT_DATA


@dataclass(frozen=True)
class EnglishAdaptiveDecision:
    mastery_state: MasteryState

    difficulty: DifficultyLevel

    support_level: AdaptiveSupport

    explanation_depth: ExplanationDepth

    next_activity: EnglishAdaptiveActivity

    response_pace: ResponsePace

    response_pace_source: ResponsePaceSource

    reason_codes: tuple[
        str,
        ...,
    ]

    summary: str


class EnglishAdaptiveEngine:
    MIN_LATENCY_SAMPLES = 3


    @classmethod
    def decide(
        cls,
        signals: EnglishAdaptiveSignals,
    ) -> EnglishAdaptiveDecision:

        reasons: list[str] = []


        (
            response_pace,
            response_pace_source,
        ) = cls._response_pace(
            signals
        )


        if (
            response_pace_source
            == ResponsePaceSource.PERSONAL_BASELINE
        ):
            reasons.append(
                "PERSONAL_BASELINE_USED"
            )


        elif (
            response_pace_source
            == ResponsePaceSource.AGE_GROUP_FALLBACK
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


        mastery_state = (
            cls._mastery_state(
                signals
            )
        )


        if (
            mastery_state
            == MasteryState.STRONG
        ):
            reasons.append(
                "STRONG_ENGLISH_MASTERY"
            )


        elif (
            mastery_state
            == MasteryState.DEVELOPING
        ):
            reasons.append(
                "DEVELOPING_ENGLISH_MASTERY"
            )


        elif (
            mastery_state
            == MasteryState.LEARNING
        ):
            reasons.append(
                "ENGLISH_MASTERY_BUILDING"
            )


        # ==================================
        # Struggle evidence
        # ==================================

        low_understanding = (
            signals.total_attempts >= 3

            and (
                signals
                .understanding_score_percent
                < 50.0
            )
        )


        low_independent_success = (
            signals.total_attempts >= 3

            and (
                signals
                .independent_attempt_rate
                >= 40.0
            )

            and (
                signals
                .independent_success_rate
                < 50.0
            )
        )


        high_hint_usage = (
            signals.total_attempts >= 2

            and (
                signals
                .average_hint_level
                >= 4.0
            )
        )


        answer_dependence = (
            signals
            .direct_answer_requests
            >= 2
        )


        latency_supported_struggle = (
            response_pace
            == ResponsePace.SLOW

            and signals.total_attempts >= 3

            and (
                signals
                .understanding_score_percent
                < 70.0

                or (
                    signals
                    .independent_success_rate
                    < 50.0
                )

                or (
                    signals
                    .average_hint_level
                    >= 3.0
                )
            )
        )


        if low_understanding:
            reasons.append(
                "LOW_ENGLISH_UNDERSTANDING"
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


        if latency_supported_struggle:
            reasons.append(
                "SLOW_RESPONSE_WITH_STRUGGLE"
            )


        struggling = (
            low_understanding
            or low_independent_success
            or high_hint_usage
            or latency_supported_struggle
        )


        # ==================================
        # Strong performance
        # ==================================

        strong_performance = (
            signals.total_attempts >= 3

            and (
                signals
                .understanding_score_percent
                >= 75.0
            )

            and (
                signals
                .independent_attempt_rate
                >= 60.0
            )

            and (
                signals
                .independent_success_rate
                >= 70.0
            )

            and (
                signals
                .average_hint_level
                <= 2.0
            )
        )


        if strong_performance:
            reasons.append(
                "STRONG_ENGLISH_PERFORMANCE"
            )


        # ==================================
        # Starting difficulty
        # ==================================

        if (
            mastery_state
            == MasteryState.STRONG
        ):
            difficulty = (
                DifficultyLevel.CHALLENGING
            )


        elif (
            mastery_state
            == MasteryState.DEVELOPING
        ):
            difficulty = (
                DifficultyLevel.MODERATE
            )


        else:
            difficulty = (
                DifficultyLevel.EASY
            )


        # ==================================
        # Difficulty adjustment
        # ==================================

        if struggling:
            difficulty = (
                cls._lower_difficulty(
                    difficulty
                )
            )

            reasons.append(
                "DIFFICULTY_REDUCED"
            )


        elif strong_performance:
            difficulty = (
                cls._raise_difficulty(
                    difficulty
                )
            )

            reasons.append(
                "DIFFICULTY_INCREASED"
            )


        # ==================================
        # Support
        # ==================================

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
            low_independent_success

            or answer_dependence

            or (
                signals
                .average_hint_level
                >= 2.0
            )

            or (
                signals
                .independent_attempt_rate
                < 50.0
            )
        ):
            support_level = (
                AdaptiveSupport.GUIDED
            )


        else:
            support_level = (
                AdaptiveSupport.GENTLE
            )


        # ==================================
        # Next activity
        # ==================================

        if (
            signals.total_attempts == 0
        ):
            next_activity = (
                EnglishAdaptiveActivity
                .START_LEARNING
            )

            reasons.append(
                "NO_ENGLISH_ATTEMPTS"
            )


        elif struggling:
            next_activity = (
                EnglishAdaptiveActivity
                .REVIEW_CONCEPT
            )


        elif (
            mastery_state
            == MasteryState.STRONG
        ):
            next_activity = (
                EnglishAdaptiveActivity
                .CHALLENGE_QUESTION
            )


        elif strong_performance:
            next_activity = (
                EnglishAdaptiveActivity
                .INDEPENDENT_QUESTION
            )


        else:
            next_activity = (
                EnglishAdaptiveActivity
                .GUIDED_QUESTION
            )


        explanation_depth = (
            cls._explanation_depth(
                signals.age_group
            )
        )


        summary = (
            cls._summary(
                activity=(
                    next_activity
                ),

                difficulty=(
                    difficulty
                ),

                support=(
                    support_level
                ),
            )
        )


        return (
            EnglishAdaptiveDecision(
                mastery_state=(
                    mastery_state
                ),

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
                    next_activity
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
        )


    # ======================================
    # Mastery
    # ======================================

    @staticmethod
    def _mastery_state(
        signals: EnglishAdaptiveSignals,
    ) -> MasteryState:

        if (
            signals.total_attempts == 0
        ):
            return (
                MasteryState.NOT_STARTED
            )


        if (
            signals.total_attempts >= 5

            and (
                signals
                .understanding_score_percent
                >= 80.0
            )

            and (
                signals
                .independent_attempt_rate
                >= 60.0
            )

            and (
                signals
                .independent_success_rate
                >= 70.0
            )
        ):
            return (
                MasteryState.STRONG
            )


        if (
            signals.total_attempts >= 3

            and (
                signals
                .understanding_score_percent
                >= 50.0
            )
        ):
            return (
                MasteryState.DEVELOPING
            )


        return (
            MasteryState.LEARNING
        )


    # ======================================
    # Response pace
    # ======================================

    @classmethod
    def _response_pace(
        cls,
        signals: EnglishAdaptiveSignals,
    ) -> tuple[
        ResponsePace,
        ResponsePaceSource,
    ]:

        if (
            signals.baseline_ready

            and (
                signals
                .personalized_response_pace
                != ResponsePace.INSUFFICIENT_DATA
            )
        ):
            return (
                signals
                .personalized_response_pace,

                ResponsePaceSource
                .PERSONAL_BASELINE,
            )


        if (
            signals
            .measured_response_count
            < cls.MIN_LATENCY_SAMPLES

            or (
                signals
                .average_response_latency_ms
                is None
            )
        ):
            return (
                ResponsePace
                .INSUFFICIENT_DATA,

                ResponsePaceSource
                .INSUFFICIENT_DATA,
            )


        (
            fast_threshold,
            slow_threshold,
        ) = cls._latency_thresholds(
            signals.age_group
        )


        latency = (
            signals
            .average_response_latency_ms
        )


        if (
            latency <= fast_threshold
        ):
            pace = (
                ResponsePace.FAST
            )


        elif (
            latency >= slow_threshold
        ):
            pace = (
                ResponsePace.SLOW
            )


        else:
            pace = (
                ResponsePace.TYPICAL
            )


        return (
            pace,

            ResponsePaceSource
            .AGE_GROUP_FALLBACK,
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


    # ======================================
    # Explanation depth
    # ======================================

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


    # ======================================
    # Difficulty
    # ======================================

    @staticmethod
    def _lower_difficulty(
        difficulty: DifficultyLevel,
    ) -> DifficultyLevel:

        if (
            difficulty
            == DifficultyLevel.CHALLENGING
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


        return (
            DifficultyLevel.CHALLENGING
        )


    # ======================================
    # Summary
    # ======================================

    @staticmethod
    def _summary(
        activity: EnglishAdaptiveActivity,
        difficulty: DifficultyLevel,
        support: AdaptiveSupport,
    ) -> str:

        labels = {
            EnglishAdaptiveActivity
            .START_LEARNING: (
                "start by learning "
                "the English concept"
            ),

            EnglishAdaptiveActivity
            .GUIDED_QUESTION: (
                "continue with a "
                "guided English question"
            ),

            EnglishAdaptiveActivity
            .INDEPENDENT_QUESTION: (
                "answer an English "
                "question independently"
            ),

            EnglishAdaptiveActivity
            .REVIEW_CONCEPT: (
                "review the English "
                "concept before continuing"
            ),

            EnglishAdaptiveActivity
            .CHALLENGE_QUESTION: (
                "try a more challenging "
                "English question"
            ),
        }


        return (
            "Recommend "
            + labels[
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
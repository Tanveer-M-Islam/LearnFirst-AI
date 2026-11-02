from dataclasses import (
    dataclass,
)
from statistics import (
    median,
)

from app.schemas.adaptive import (
    ResponsePace,
)


@dataclass(
    frozen=True
)
class PersonalizedLatencyProfile:

    baseline_ready: bool

    total_samples: int

    baseline_sample_count: int

    recent_sample_count: int

    baseline_response_latency_ms: (
        float | None
    )

    recent_response_latency_ms: (
        float | None
    )

    latency_change_percent: (
        float | None
    )

    personalized_response_pace: (
        ResponsePace
    )


class LearningProfileAnalyzer:

    RECENT_WINDOW = 3

    MIN_BASELINE_SAMPLES = 5

    MAX_BASELINE_SAMPLES = 12

    CHANGE_THRESHOLD_PERCENT = 30.0


    @classmethod
    def analyze(
        cls,
        response_latencies: list[
            int | float
        ],
    ) -> PersonalizedLatencyProfile:

        clean_values = [
            float(value)

            for value
            in response_latencies

            if value is not None
            and value > 0
        ]


        total_samples = (
            len(
                clean_values
            )
        )


        recent_count = min(
            cls.RECENT_WINDOW,
            total_samples,
        )


        # ----------------------------------
        # Not enough data for a proper
        # personal baseline yet.
        #
        # We need:
        # 5 historical samples
        # +
        # 3 recent samples
        # ----------------------------------

        minimum_required = (
            cls.MIN_BASELINE_SAMPLES
            + cls.RECENT_WINDOW
        )


        if (
            total_samples
            < minimum_required
        ):

            historical_count = max(
                0,
                total_samples
                - recent_count,
            )


            return (
                PersonalizedLatencyProfile(
                    baseline_ready=False,

                    total_samples=(
                        total_samples
                    ),

                    baseline_sample_count=(
                        historical_count
                    ),

                    recent_sample_count=(
                        recent_count
                    ),

                    baseline_response_latency_ms=(
                        None
                    ),

                    recent_response_latency_ms=(
                        cls._median_or_none(
                            clean_values[
                                -recent_count:
                            ]

                            if recent_count
                            else []
                        )
                    ),

                    latency_change_percent=(
                        None
                    ),

                    personalized_response_pace=(
                        ResponsePace
                        .INSUFFICIENT_DATA
                    ),
                )
            )


        # ----------------------------------
        # Separate historical baseline
        # from recent behavior.
        #
        # Recent responses are deliberately
        # excluded from the baseline.
        # ----------------------------------

        historical_values = (
            clean_values[
                :-cls.RECENT_WINDOW
            ]
        )


        baseline_values = (
            historical_values[
                -cls.MAX_BASELINE_SAMPLES:
            ]
        )


        recent_values = (
            clean_values[
                -cls.RECENT_WINDOW:
            ]
        )


        baseline_latency = float(
            median(
                baseline_values
            )
        )


        recent_latency = float(
            median(
                recent_values
            )
        )


        # ----------------------------------
        # Change relative to student's
        # own historical baseline.
        # ----------------------------------

        latency_change_percent = (
            (
                recent_latency
                - baseline_latency
            )
            / baseline_latency
            * 100.0
        )


        latency_change_percent = round(
            latency_change_percent,
            2,
        )


        # ----------------------------------
        # Personal pace classification
        #
        # At least 30% faster/slower
        # is required before changing
        # the classification.
        # ----------------------------------

        if (
            latency_change_percent
            <= (
                -cls
                .CHANGE_THRESHOLD_PERCENT
            )
        ):

            pace = (
                ResponsePace.FAST
            )


        elif (
            latency_change_percent
            >= cls
            .CHANGE_THRESHOLD_PERCENT
        ):

            pace = (
                ResponsePace.SLOW
            )


        else:

            pace = (
                ResponsePace.TYPICAL
            )


        return (
            PersonalizedLatencyProfile(
                baseline_ready=True,

                total_samples=(
                    total_samples
                ),

                baseline_sample_count=(
                    len(
                        baseline_values
                    )
                ),

                recent_sample_count=(
                    len(
                        recent_values
                    )
                ),

                baseline_response_latency_ms=(
                    round(
                        baseline_latency,
                        1,
                    )
                ),

                recent_response_latency_ms=(
                    round(
                        recent_latency,
                        1,
                    )
                ),

                latency_change_percent=(
                    latency_change_percent
                ),

                personalized_response_pace=(
                    pace
                ),
            )
        )


    @staticmethod
    def _median_or_none(
        values: list[
            float
        ],
    ) -> float | None:

        if not values:

            return None


        return round(
            float(
                median(
                    values
                )
            ),
            1,
        )
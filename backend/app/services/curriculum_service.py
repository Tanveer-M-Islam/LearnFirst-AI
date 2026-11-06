import re

from pathlib import (
    Path,
)

from sqlalchemy.orm import (
    Session,
)

from app.core.config import (
    get_settings,
)
from app.curriculum.catalog import (
    CurriculumConcept,
    get_subject_curriculum,
)
from app.database.repositories.mastery_repository import (
    MasteryRepository,
)
from app.database.repositories.student_repository import (
    StudentRepository,
)
from app.rag.loader import (
    KnowledgeLoader,
)
from app.schemas.curriculum import (
    CurriculumConceptStatus,
    CurriculumPathConceptView,
    CurriculumTopicView,
    StudentCurriculumPathResponse,
)
from app.schemas.enums import (
    AgeGroup,
    MasteryState,
    Subject,
)


class CurriculumService:

    # ==================================================
    # Existing Science RAG topics
    # ==================================================

    @classmethod
    def list_topics(
        cls,
        subject: str,
        curriculum_profile: (
            str | None
        ) = None,
        root: str | Path | None = None,
    ) -> list[
        CurriculumTopicView
    ]:

        settings = (
            get_settings()
        )


        knowledge_root = (
            root

            if root is not None

            else settings
            .rag_knowledge_dir
        )


        documents = (
            KnowledgeLoader
            .load_directory(
                knowledge_root
            )
        )


        normalized_subject = (
            subject
            .strip()
            .upper()
        )


        topics: list[
            CurriculumTopicView
        ] = []


        seen: set[
            str
        ] = set()


        for document in (
            documents
        ):

            if (
                document.subject
                != normalized_subject
            ):

                continue


            if (
                curriculum_profile
                is not None

                and document
                .curriculum_profile
                != curriculum_profile
            ):

                continue


            if (
                document
                .concept_code
                in seen
            ):

                continue


            seen.add(
                document
                .concept_code
            )


            topics.append(
                CurriculumTopicView(
                    source_id=(
                        document
                        .source_id
                    ),

                    title=(
                        document.title
                    ),

                    subject=(
                        document.subject
                    ),

                    concept_code=(
                        document
                        .concept_code
                    ),

                    grade_band=(
                        document
                        .grade_band
                    ),

                    curriculum_profile=(
                        document
                        .curriculum_profile
                    ),
                )
            )


        return sorted(
            topics,

            key=lambda item:
                item.title,
        )


    # ==================================================
    # Curriculum catalog
    # ==================================================

    @classmethod
    def list_catalog(
        cls,
        subject: Subject,
        include_planned: bool = True,
    ) -> list[
        CurriculumConcept
    ]:

        concepts = list(
            get_subject_curriculum(
                subject
            )
        )


        if (
            include_planned
        ):

            return concepts


        return [
            concept

            for concept
            in concepts

            if (
                concept.implemented
            )
        ]


    # ==================================================
    # Student path
    # ==================================================

    @classmethod
    def get_student_path(
        cls,
        db: Session,
        student_id: str,
        subject: Subject,
    ) -> StudentCurriculumPathResponse:

        student = (
            StudentRepository
            .get_by_id(
                db=db,

                student_id=(
                    student_id
                ),
            )
        )


        if (
            student is None
        ):

            raise LookupError(
                "Student not found."
            )


        concepts = list(
            get_subject_curriculum(
                subject
            )
        )


        grade_number = (
            cls._grade_number(
                student.grade
            )
        )


        concept_views = [
            cls._concept_view(
                db=db,

                student_id=(
                    student_id
                ),

                learner_age=(
                    student.age
                ),

                learner_grade=(
                    grade_number
                ),

                concept=(
                    concept
                ),
            )

            for concept
            in concepts
        ]


        reasons: list[
            str
        ] = []


        # ----------------------------------
        # Age is the primary starting point.
        # ----------------------------------

        target = (
            cls._select_age_target(
                concepts=(
                    concepts
                ),

                learner_age=(
                    student.age
                ),
            )
        )


        target_view = (
            cls._find_view(
                views=(
                    concept_views
                ),

                concept_code=(
                    target.concept_code
                ),
            )

            if target is not None

            else None
        )


        if (
            target is not None
        ):

            reasons.append(
                "AGE_TARGET_SELECTED"
            )


            if (
                grade_number
                is not None

                and not (
                    target.min_grade
                    <= grade_number
                    <= target.max_grade
                )
            ):

                reasons.append(
                    "GRADE_OUTSIDE_TARGET_BAND"
                )


        implemented = [
            concept

            for concept
            in concepts

            if (
                concept.implemented
            )
        ]


        if (
            not implemented
        ):

            reasons.append(
                "NO_IMPLEMENTED_CONCEPTS"
            )


            return (
                StudentCurriculumPathResponse(
                    student_id=(
                        student_id
                    ),

                    subject=(
                        subject
                    ),

                    learner_age=(
                        student.age
                    ),

                    learner_grade=(
                        student.grade
                    ),

                    age_group=(
                        AgeGroup(
                            student
                            .age_group
                        )
                    ),

                    target_concept=(
                        target_view
                    ),

                    recommended_concept=None,

                    prerequisite_review_concept=None,

                    reason_codes=(
                        reasons
                    ),

                    concepts=(
                        concept_views
                    ),
                )
            )


        # ----------------------------------
        # Find usable current concept.
        # ----------------------------------

        if (
            target is not None
            and target.implemented
        ):

            base_recommendation = (
                target
            )


        else:

            base_recommendation = (
                cls._nearest_implemented(
                    concepts=(
                        implemented
                    ),

                    learner_age=(
                        student.age
                    ),
                )
            )


            if (
                target is not None
                and not target
                .implemented
            ):

                reasons.append(
                    "TARGET_CONTENT_PLANNED"
                )


                reasons.append(
                    "NEAREST_IMPLEMENTED_CONCEPT_SELECTED"
                )


        if (
            base_recommendation
            is None
        ):

            reasons.append(
                "NO_RECOMMENDATION_AVAILABLE"
            )


            return (
                StudentCurriculumPathResponse(
                    student_id=(
                        student_id
                    ),

                    subject=(
                        subject
                    ),

                    learner_age=(
                        student.age
                    ),

                    learner_grade=(
                        student.grade
                    ),

                    age_group=(
                        AgeGroup(
                            student
                            .age_group
                        )
                    ),

                    target_concept=(
                        target_view
                    ),

                    recommended_concept=None,

                    prerequisite_review_concept=None,

                    reason_codes=(
                        reasons
                    ),

                    concepts=(
                        concept_views
                    ),
                )
            )


        # ----------------------------------
        # If learner strongly mastered
        # their target, allow progression
        # to the next implemented concept.
        # ----------------------------------

        base_view = (
            cls._find_view(
                views=(
                    concept_views
                ),

                concept_code=(
                    base_recommendation
                    .concept_code
                ),
            )
        )


        if (
            base_view is not None

            and base_view
            .mastery_state
            == MasteryState.STRONG
        ):

            next_concept = (
                cls._next_implemented(
                    concepts=(
                        implemented
                    ),

                    sequence_order=(
                        base_recommendation
                        .sequence_order
                    ),
                )
            )


            if (
                next_concept is not None
            ):

                base_recommendation = (
                    next_concept
                )


                reasons.append(
                    "CURRENT_LEVEL_MASTERED"
                )


                reasons.append(
                    "ADVANCE_TO_NEXT_CONCEPT"
                )


            else:

                reasons.append(
                    "CURRENT_LEVEL_MASTERED"
                )


                reasons.append(
                    "HIGHEST_IMPLEMENTED_LEVEL_REACHED"
                )


        # ----------------------------------
        # Missing prerequisite data does
        # NOT count as weakness.
        #
        # Only actual mastery evidence can
        # trigger regression.
        # ----------------------------------

        weak_prerequisite = (
            cls._find_known_weak_prerequisite(
                db=db,

                student_id=(
                    student_id
                ),

                concept=(
                    base_recommendation
                ),

                all_concepts=(
                    concepts
                ),
            )
        )


        prerequisite_view = None


        recommendation = (
            base_recommendation
        )


        if (
            weak_prerequisite
            is not None
        ):

            recommendation = (
                weak_prerequisite
            )


            prerequisite_view = (
                cls._find_view(
                    views=(
                        concept_views
                    ),

                    concept_code=(
                        weak_prerequisite
                        .concept_code
                    ),
                )
            )


            reasons.append(
                "KNOWN_PREREQUISITE_GAP"
            )


            reasons.append(
                "PREREQUISITE_REVIEW_REQUIRED"
            )


        else:

            reasons.append(
                "NO_KNOWN_PREREQUISITE_GAP"
            )


        recommendation_view = (
            cls._find_view(
                views=(
                    concept_views
                ),

                concept_code=(
                    recommendation
                    .concept_code
                ),
            )
        )


        return (
            StudentCurriculumPathResponse(
                student_id=(
                    student_id
                ),

                subject=(
                    subject
                ),

                learner_age=(
                    student.age
                ),

                learner_grade=(
                    student.grade
                ),

                age_group=(
                    AgeGroup(
                        student
                        .age_group
                    )
                ),

                target_concept=(
                    target_view
                ),

                recommended_concept=(
                    recommendation_view
                ),

                prerequisite_review_concept=(
                    prerequisite_view
                ),

                reason_codes=(
                    reasons
                ),

                concepts=(
                    concept_views
                ),
            )
        )


    # ==================================================
    # Age target
    # ==================================================

    @staticmethod
    def _select_age_target(
        concepts: list[
            CurriculumConcept
        ],
        learner_age: int,
    ) -> CurriculumConcept | None:

        if (
            not concepts
        ):

            return None


        exact = [
            concept

            for concept
            in concepts

            if (
                concept.recommended_age
                == learner_age
            )
        ]


        if (
            exact
        ):

            return exact[0]


        return min(
            concepts,

            key=lambda concept: (
                abs(
                    concept
                    .recommended_age
                    - learner_age
                ),

                concept
                .sequence_order,
            ),
        )


    # ==================================================
    # Nearest usable content
    # ==================================================

    @staticmethod
    def _nearest_implemented(
        concepts: list[
            CurriculumConcept
        ],
        learner_age: int,
    ) -> CurriculumConcept | None:

        if (
            not concepts
        ):

            return None


        return min(
            concepts,

            key=lambda concept: (
                abs(
                    concept
                    .recommended_age
                    - learner_age
                ),

                0
                if (
                    concept
                    .recommended_age
                    <= learner_age
                )
                else 1,

                -concept
                .sequence_order,
            ),
        )


    # ==================================================
    # Progress forward
    # ==================================================

    @staticmethod
    def _next_implemented(
        concepts: list[
            CurriculumConcept
        ],
        sequence_order: int,
    ) -> CurriculumConcept | None:

        later = sorted(
            (
                concept

                for concept
                in concepts

                if (
                    concept
                    .sequence_order
                    > sequence_order
                )
            ),

            key=lambda concept:
                concept.sequence_order,
        )


        if (
            not later
        ):

            return None


        return later[0]


    # ==================================================
    # Recursive prerequisite review
    # ==================================================

    @classmethod
    def _find_known_weak_prerequisite(
        cls,
        db: Session,
        student_id: str,
        concept: CurriculumConcept,
        all_concepts: list[
            CurriculumConcept
        ],
    ) -> CurriculumConcept | None:

        concept_map = {
            item.concept_code:
                item

            for item
            in all_concepts
        }


        visited: set[
            str
        ] = set()


        def find_weak(
            current:
                CurriculumConcept,
        ) -> CurriculumConcept | None:

            for prerequisite_code in (
                current.prerequisites
            ):

                if (
                    prerequisite_code
                    in visited
                ):

                    continue


                visited.add(
                    prerequisite_code
                )


                prerequisite = (
                    concept_map.get(
                        prerequisite_code
                    )
                )


                if (
                    prerequisite
                    is None
                ):

                    continue


                # Search deeper prerequisites
                # before the current one.

                deeper = (
                    find_weak(
                        prerequisite
                    )
                )


                if (
                    deeper is not None
                ):

                    return deeper


                record = (
                    MasteryRepository
                    .get_by_student_concept(
                        db=db,

                        student_id=(
                            student_id
                        ),

                        concept_code=(
                            prerequisite_code
                        ),
                    )
                )


                # No evidence is NOT weakness.

                if (
                    record is None
                ):

                    continue


                try:

                    mastery_state = (
                        MasteryState(
                            record
                            .mastery_state
                        )
                    )


                except ValueError:

                    mastery_state = (
                        MasteryState
                        .NOT_STARTED
                    )


                mastery_score = (
                    record
                    .mastery_score
                )


                known_weak = (
                    mastery_state
                    == MasteryState.LEARNING

                    or (
                        mastery_score
                        is not None

                        and mastery_score
                        < 60.0
                    )
                )


                if (
                    known_weak
                ):

                    return prerequisite


            return None


        return find_weak(
            concept
        )


    # ==================================================
    # Student concept view
    # ==================================================

    @classmethod
    def _concept_view(
        cls,
        db: Session,
        student_id: str,
        learner_age: int,
        learner_grade: (
            int | None
        ),
        concept: CurriculumConcept,
    ) -> CurriculumPathConceptView:

        record = (
            MasteryRepository
            .get_by_student_concept(
                db=db,

                student_id=(
                    student_id
                ),

                concept_code=(
                    concept
                    .concept_code
                ),
            )
        )


        mastery_state = (
            MasteryState
            .NOT_STARTED
        )


        mastery_score = None


        if (
            record is not None
        ):

            try:

                mastery_state = (
                    MasteryState(
                        record
                        .mastery_state
                    )
                )


            except ValueError:

                mastery_state = (
                    MasteryState
                    .NOT_STARTED
                )


            mastery_score = (
                record
                .mastery_score
            )


        grade_appropriate = None


        if (
            learner_grade
            is not None
        ):

            grade_appropriate = (
                concept.min_grade
                <= learner_grade
                <= concept.max_grade
            )


        return (
            CurriculumPathConceptView(
                concept_code=(
                    concept
                    .concept_code
                ),

                subject=(
                    concept.subject
                ),

                title=(
                    concept.title
                ),

                description=(
                    concept.description
                ),

                recommended_age=(
                    concept
                    .recommended_age
                ),

                min_age=(
                    concept.min_age
                ),

                max_age=(
                    concept.max_age
                ),

                min_grade=(
                    concept.min_grade
                ),

                max_grade=(
                    concept.max_grade
                ),

                sequence_order=(
                    concept
                    .sequence_order
                ),

                prerequisites=list(
                    concept
                    .prerequisites
                ),

                implemented=(
                    concept.implemented
                ),

                curriculum_profile=(
                    concept
                    .curriculum_profile
                ),

                mastery_state=(
                    mastery_state
                ),

                mastery_score=(
                    mastery_score
                ),

                status=(
                    cls._concept_status(
                        concept=(
                            concept
                        ),

                        learner_age=(
                            learner_age
                        ),

                        mastery_state=(
                            mastery_state
                        ),

                        mastery_score=(
                            mastery_score
                        ),
                    )
                ),

                age_appropriate=(
                    concept.min_age
                    <= learner_age
                    <= concept.max_age
                ),

                grade_appropriate=(
                    grade_appropriate
                ),
            )
        )


    @staticmethod
    def _concept_status(
        concept: CurriculumConcept,
        learner_age: int,
        mastery_state: MasteryState,
        mastery_score: (
            float | None
        ),
    ) -> CurriculumConceptStatus:

        if (
            not concept.implemented
        ):

            return (
                CurriculumConceptStatus
                .PLANNED
            )


        if (
            mastery_state
            == MasteryState.STRONG
        ):

            return (
                CurriculumConceptStatus
                .MASTERED
            )


        if (
            mastery_state
            == MasteryState.DEVELOPING
        ):

            return (
                CurriculumConceptStatus
                .IN_PROGRESS
            )


        if (
            mastery_state
            == MasteryState.LEARNING

            or (
                mastery_score
                is not None

                and mastery_score
                < 60.0
            )
        ):

            return (
                CurriculumConceptStatus
                .NEEDS_REVIEW
            )


        if (
            concept.min_age
            > learner_age
        ):

            return (
                CurriculumConceptStatus
                .FUTURE
            )


        return (
            CurriculumConceptStatus
            .READY
        )


    # ==================================================
    # Helpers
    # ==================================================

    @staticmethod
    def _grade_number(
        grade: str,
    ) -> int | None:

        match = re.search(
            r"\d+",
            grade,
        )


        if (
            match is None
        ):

            return None


        return int(
            match.group()
        )


    @staticmethod
    def _find_view(
        views: list[
            CurriculumPathConceptView
        ],
        concept_code: str,
    ) -> (
        CurriculumPathConceptView
        | None
    ):

        return next(
            (
                item

                for item
                in views

                if (
                    item.concept_code
                    == concept_code
                )
            ),

            None,
        )
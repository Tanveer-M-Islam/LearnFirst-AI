from dataclasses import dataclass

from app.schemas.enums import Subject


@dataclass(frozen=True)
class CurriculumConcept:
    concept_code: str

    subject: Subject

    title: str

    description: str

    recommended_age: int

    min_age: int

    max_age: int

    min_grade: int

    max_grade: int

    sequence_order: int

    prerequisites: tuple[
        str,
        ...,
    ] = ()

    implemented: bool = True

    curriculum_profile: str = (
        "bangladesh_english_v1"
    )


def _concept(
    concept_code: str,
    subject: Subject,
    title: str,
    description: str,
    recommended_age: int,
    min_grade: int,
    max_grade: int,
    sequence_order: int,
    prerequisites: tuple[
        str,
        ...,
    ] = (),
    implemented: bool = True,
) -> CurriculumConcept:

    return CurriculumConcept(
        concept_code=concept_code,

        subject=subject,

        title=title,

        description=description,

        recommended_age=(
            recommended_age
        ),

        min_age=max(
            7,
            recommended_age - 1,
        ),

        max_age=min(
            14,
            recommended_age + 1,
        ),

        min_grade=min_grade,

        max_grade=max_grade,

        sequence_order=(
            sequence_order
        ),

        prerequisites=(
            prerequisites
        ),

        implemented=(
            implemented
        ),
    )


# ======================================================
# MATH
# ======================================================

MATH_CURRICULUM: tuple[
    CurriculumConcept,
    ...,
] = (

    _concept(
        "MATH_ARITH_BASIC_01",
        Subject.MATH,
        "Basic Arithmetic",
        (
            "Build confidence with "
            "addition and subtraction."
        ),
        7,
        1,
        3,
        10,
    ),

    _concept(
        "MATH_ARITH_MULTDIV_01",
        Subject.MATH,
        "Multiplication and Division",
        (
            "Develop multiplication "
            "and division fluency."
        ),
        8,
        2,
        4,
        20,
        (
            "MATH_ARITH_BASIC_01",
        ),
    ),

    _concept(
        "MATH_ARITH_FRAC_01",
        Subject.MATH,
        "Fractions",
        (
            "Understand and calculate "
            "with fractions."
        ),
        9,
        3,
        6,
        30,
        (
            "MATH_ARITH_MULTDIV_01",
        ),
    ),

    _concept(
        "MATH_ARITH_INT_01",
        Subject.MATH,
        "Integers",
        (
            "Work with positive "
            "and negative numbers."
        ),
        10,
        4,
        7,
        40,
        (
            "MATH_ARITH_BASIC_01",
        ),
    ),

    _concept(
        "MATH_ARITH_ORDER_01",
        Subject.MATH,
        "Order of Operations",
        (
            "Evaluate expressions "
            "using the correct "
            "operation order."
        ),
        11,
        5,
        8,
        50,
        (
            "MATH_ARITH_INT_01",
        ),
    ),

    _concept(
        "MATH_PREALG_EXPR_01",
        Subject.MATH,
        "Pre-Algebra Expressions",
        (
            "Evaluate algebraic "
            "expressions by "
            "substituting values."
        ),
        12,
        6,
        8,
        60,
        (
            "MATH_ARITH_ORDER_01",
        ),
    ),

    _concept(
        "MATH_ALG_LINEAR_01",
        Subject.MATH,
        "Linear Equations",
        (
            "Solve one-variable "
            "linear equations."
        ),
        13,
        7,
        10,
        70,
        (
            "MATH_PREALG_EXPR_01",
            "MATH_ARITH_INT_01",
        ),
    ),

    _concept(
        "MATH_GRAPH_LINEAR_01",
        Subject.MATH,
        "Linear Graphs",
        (
            "Connect x-values, "
            "y-values and linear "
            "relationships."
        ),
        14,
        8,
        10,
        80,
        (
            "MATH_ALG_LINEAR_01",
        ),
    ),
)


# ======================================================
# SCIENCE
#
# Phase 20:
# all ages 7–14 are now operational.
# ======================================================

SCIENCE_CURRICULUM: tuple[
    CurriculumConcept,
    ...,
] = (

    _concept(
        "SCI_LIFE_BASIC_01",
        Subject.SCIENCE,
        "Living Things",
        (
            "Understand the basic "
            "characteristics and needs "
            "of living things."
        ),
        7,
        1,
        3,
        10,
    ),

    _concept(
        "SCI_MATERIAL_BASIC_01",
        Subject.SCIENCE,
        "Everyday Materials",
        (
            "Explore common materials "
            "and their properties."
        ),
        8,
        2,
        4,
        20,
        (
            "SCI_LIFE_BASIC_01",
        ),
    ),

    _concept(
        "SCI_PHY_MATTER_01",
        Subject.SCIENCE,
        "States of Matter",
        (
            "Understand solids, "
            "liquids, gases and "
            "state changes."
        ),
        9,
        3,
        6,
        30,
        (
            "SCI_MATERIAL_BASIC_01",
        ),
    ),

    _concept(
        "SCI_BIO_FOODCHAIN_01",
        Subject.SCIENCE,
        "Food Chains",
        (
            "Understand producers, "
            "consumers and energy flow."
        ),
        10,
        4,
        7,
        40,
        (
            "SCI_LIFE_BASIC_01",
        ),
    ),

    _concept(
        "SCI_ECO_SYSTEMS_01",
        Subject.SCIENCE,
        "Ecosystems",
        (
            "Explore how organisms "
            "interact with one another "
            "and their environment."
        ),
        11,
        5,
        8,
        50,
        (
            "SCI_BIO_FOODCHAIN_01",
        ),
    ),

    _concept(
        "SCI_BIO_PHOTO_01",
        Subject.SCIENCE,
        "Photosynthesis",
        (
            "Understand how plants "
            "use light energy to "
            "produce glucose."
        ),
        12,
        6,
        9,
        60,
        (
            "SCI_LIFE_BASIC_01",
        ),
    ),

    _concept(
        "SCI_ENERGY_TRANSFER_01",
        Subject.SCIENCE,
        "Energy Transfer",
        (
            "Understand how energy "
            "moves through living "
            "and physical systems."
        ),
        13,
        7,
        10,
        70,
        (
            "SCI_BIO_FOODCHAIN_01",
            "SCI_ECO_SYSTEMS_01",
        ),
    ),

    _concept(
        "SCI_CELL_SYSTEMS_01",
        Subject.SCIENCE,
        "Cells and Biological Systems",
        (
            "Understand cells, tissues, "
            "organs and biological "
            "organization."
        ),
        14,
        8,
        10,
        80,
        (
            "SCI_LIFE_BASIC_01",
        ),
    ),
)


# ======================================================
# ENGLISH
#
# Phase 21 will make these operational.
# ======================================================

ENGLISH_CURRICULUM: tuple[
    CurriculumConcept,
    ...,
] = (

    _concept(
        "ENG_VOCAB_FOUND_01",
        Subject.ENGLISH,
        "Everyday Vocabulary",
        (
            "Build useful everyday "
            "English vocabulary."
        ),
        7,
        1,
        3,
        10,
        implemented=True,
    ),

    _concept(
        "ENG_SENT_SIMPLE_01",
        Subject.ENGLISH,
        "Simple Sentences",
        (
            "Build clear and complete "
            "simple sentences."
        ),
        8,
        2,
        4,
        20,
        (
            "ENG_VOCAB_FOUND_01",
        ),
        True,
    ),

    _concept(
        "ENG_GRAMMAR_POS_01",
        Subject.ENGLISH,
        "Parts of Speech",
        (
            "Understand nouns, verbs, "
            "adjectives and word roles."
        ),
        9,
        3,
        5,
        30,
        implemented=True,
    ),

    _concept(
        "ENG_GRAMMAR_TENSE_01",
        Subject.ENGLISH,
        "Core Tenses",
        (
            "Use present, past and "
            "future tense forms."
        ),
        10,
        4,
        6,
        40,
        implemented=True,
    ),

    _concept(
        "ENG_READ_CORE_01",
        Subject.ENGLISH,
        "Reading Comprehension",
        (
            "Understand main ideas "
            "and details in passages."
        ),
        11,
        5,
        7,
        50,
        implemented=True,
    ),

    _concept(
        "ENG_SENT_STRUCTURE_01",
        Subject.ENGLISH,
        "Sentence Structure",
        (
            "Build increasingly "
            "complex English sentences."
        ),
        12,
        6,
        8,
        60,
        implemented=True,
    ),

    _concept(
        "ENG_GRAMMAR_ADV_01",
        Subject.ENGLISH,
        "Intermediate Grammar",
        (
            "Use increasingly complex "
            "grammar accurately."
        ),
        13,
        7,
        9,
        70,
        implemented=True,
    ),

    _concept(
        "ENG_READ_INFERENCE_01",
        Subject.ENGLISH,
        "Reading and Inference",
        (
            "Interpret deeper meaning "
            "and evidence in passages."
        ),
        14,
        8,
        10,
        80,
        implemented=True,
    ),
)


CURRICULUM_CATALOG = (
    *MATH_CURRICULUM,
    *SCIENCE_CURRICULUM,
    *ENGLISH_CURRICULUM,
)


def get_subject_curriculum(
    subject: Subject,
) -> tuple[
    CurriculumConcept,
    ...,
]:

    return tuple(
        sorted(
            (
                concept
                for concept
                in CURRICULUM_CATALOG
                if (
                    concept.subject
                    == subject
                )
            ),

            key=lambda concept:
                concept.sequence_order,
        )
    )


def get_curriculum_concept(
    concept_code: str,
) -> CurriculumConcept | None:

    return next(
        (
            concept
            for concept
            in CURRICULUM_CATALOG
            if (
                concept.concept_code
                == concept_code
            )
        ),
        None,
    )
from dataclasses import (
    dataclass,
)

from app.schemas.enums import (
    DifficultyLevel,
)


@dataclass(
    frozen=True
)
class ScienceIdea:

    code: str

    label: str

    alternatives: tuple[
        str,
        ...,
    ]


@dataclass(
    frozen=True
)
class ScienceMisconception:

    code: str

    patterns: tuple[
        str,
        ...,
    ]


@dataclass(
    frozen=True
)
class ScienceQuestion:

    question_id: str

    prompt: str

    difficulty: (
        DifficultyLevel
    )

    required_ideas: tuple[
        ScienceIdea,
        ...,
    ]

    minimum_correct_ideas: int

    misconceptions: tuple[
        ScienceMisconception,
        ...,
    ] = ()


SCIENCE_QUESTION_BANK: dict[
    str,
    tuple[
        ScienceQuestion,
        ...,
    ],
] = {


    # ======================================================
    # PHOTOSYNTHESIS
    # ======================================================

    "SCI_BIO_PHOTO_01": (

        # --------------------------------------------------
        # EASY 1
        # --------------------------------------------------

        ScienceQuestion(
            question_id=(
                "PHOTO-E-01"
            ),

            prompt=(
                "What does a plant need "
                "for photosynthesis, and "
                "what does it make?"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),

            required_ideas=(

                ScienceIdea(
                    code="LIGHT",

                    label="light",

                    alternatives=(
                        "sunlight",
                        "light energy",
                        "light",
                    ),
                ),

                ScienceIdea(
                    code="WATER",

                    label="water",

                    alternatives=(
                        "water",
                        "h2o",
                    ),
                ),

                ScienceIdea(
                    code="CARBON_DIOXIDE",

                    label=(
                        "carbon dioxide"
                    ),

                    alternatives=(
                        "carbon dioxide",
                        "co2",
                    ),
                ),

                ScienceIdea(
                    code="GLUCOSE",

                    label=(
                        "glucose or food"
                    ),

                    alternatives=(
                        "glucose",
                        "sugar",

                        "make food",
                        "makes food",
                        "making food",

                        "produce food",
                        "produces food",

                        "make glucose",
                        "makes glucose",

                        "produce glucose",
                        "produces glucose",
                    ),
                ),

                ScienceIdea(
                    code="OXYGEN",

                    label="oxygen",

                    alternatives=(
                        "oxygen",
                        "o2",
                    ),
                ),
            ),

            minimum_correct_ideas=4,

            misconceptions=(

                ScienceMisconception(
                    code=(
                        "SCI_PHOTO_FOOD_FROM_SOIL"
                    ),

                    patterns=(
                        "food comes from soil",

                        (
                            "food comes from "
                            "the soil"
                        ),

                        "food from soil",

                        "food from the soil",

                        "get food from soil",

                        (
                            "get food from "
                            "the soil"
                        ),

                        "gets food from soil",

                        (
                            "gets food from "
                            "the soil"
                        ),

                        (
                            "get their food "
                            "from soil"
                        ),

                        (
                            "get their food "
                            "from the soil"
                        ),

                        (
                            "gets their food "
                            "from soil"
                        ),

                        (
                            "gets their food "
                            "from the soil"
                        ),

                        (
                            "gets its food "
                            "from soil"
                        ),

                        (
                            "gets its food "
                            "from the soil"
                        ),

                        (
                            "plants get their "
                            "food from soil"
                        ),

                        (
                            "plants get their "
                            "food from the soil"
                        ),

                        "soil gives food",
                    ),
                ),

                ScienceMisconception(
                    code=(
                        "SCI_PHOTO_SUNLIGHT_IS_FOOD"
                    ),

                    patterns=(
                        "sunlight is food",
                        "light is food",
                    ),
                ),
            ),
        ),


        # --------------------------------------------------
        # EASY 2
        # --------------------------------------------------

        ScienceQuestion(
            question_id=(
                "PHOTO-E-02"
            ),

            prompt=(
                "Why are green leaves "
                "important for "
                "photosynthesis?"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),

            required_ideas=(

                ScienceIdea(
                    code="CHLOROPHYLL",

                    label="chlorophyll",

                    alternatives=(
                        "chlorophyll",
                        "green pigment",
                    ),
                ),

                ScienceIdea(
                    code="ABSORB_LIGHT",

                    label=(
                        "absorbing light"
                    ),

                    alternatives=(
                        "absorb sunlight",
                        "absorbs sunlight",
                        "absorbing sunlight",

                        "absorb light",
                        "absorbs light",
                        "absorbing light",

                        "capture sunlight",
                        "captures sunlight",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        # --------------------------------------------------
        # MODERATE 1
        # --------------------------------------------------

        ScienceQuestion(
            question_id=(
                "PHOTO-M-01"
            ),

            prompt=(
                "Where does the carbon "
                "used to make plant food "
                "come from?"
            ),

            difficulty=(
                DifficultyLevel
                .MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="CO2_FROM_AIR",

                    label=(
                        "carbon dioxide "
                        "from the air"
                    ),

                    alternatives=(
                        (
                            "carbon dioxide "
                            "from air"
                        ),

                        (
                            "carbon dioxide "
                            "from the air"
                        ),

                        (
                            "carbon dioxide "
                            "in air"
                        ),

                        (
                            "carbon dioxide "
                            "in the air"
                        ),

                        "co2 from air",

                        "co2 from the air",
                    ),
                ),

                ScienceIdea(
                    code="CARBON_TO_FOOD",

                    label=(
                        "carbon helps build "
                        "glucose or food"
                    ),

                    alternatives=(
                        "make glucose",
                        "makes glucose",

                        "build glucose",
                        "builds glucose",

                        "make sugar",
                        "makes sugar",

                        "make food",
                        "makes food",
                    ),
                ),
            ),

            minimum_correct_ideas=2,

            misconceptions=(

                ScienceMisconception(
                    code=(
                        "SCI_PHOTO_CARBON_FROM_SOIL"
                    ),

                    patterns=(
                        (
                            "carbon comes "
                            "from soil"
                        ),

                        (
                            "carbon comes "
                            "from the soil"
                        ),

                        "carbon from soil",

                        "carbon from the soil",

                        (
                            "gets carbon "
                            "from soil"
                        ),

                        (
                            "gets carbon "
                            "from the soil"
                        ),
                    ),
                ),
            ),
        ),


        # --------------------------------------------------
        # MODERATE 2
        # --------------------------------------------------

        ScienceQuestion(
            question_id=(
                "PHOTO-M-02"
            ),

            prompt=(
                "What role does "
                "chlorophyll play during "
                "photosynthesis?"
            ),

            difficulty=(
                DifficultyLevel
                .MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="CHLOROPHYLL",

                    label="chlorophyll",

                    alternatives=(
                        "chlorophyll",
                        "green pigment",
                    ),
                ),

                ScienceIdea(
                    code="LIGHT_CAPTURE",

                    label=(
                        "capturing or "
                        "absorbing light"
                    ),

                    alternatives=(
                        "absorbs light",
                        "absorb light",

                        "absorbs sunlight",
                        "absorb sunlight",

                        "captures light",
                        "capture light",

                        "captures sunlight",
                        "capture sunlight",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        # --------------------------------------------------
        # CHALLENGING 1
        # --------------------------------------------------

        ScienceQuestion(
            question_id=(
                "PHOTO-C-01"
            ),

            prompt=(
                "A plant has water and "
                "carbon dioxide but is "
                "kept in darkness. Why "
                "would photosynthesis "
                "slow down or stop?"
            ),

            difficulty=(
                DifficultyLevel
                .CHALLENGING
            ),

            required_ideas=(

                ScienceIdea(
                    code="LIGHT_REQUIRED",

                    label=(
                        "photosynthesis "
                        "requires light"
                    ),

                    alternatives=(
                        "needs light",
                        "requires light",

                        "needs sunlight",
                        "requires sunlight",

                        "no light",
                        "without light",
                    ),
                ),

                ScienceIdea(
                    code="LIGHT_ENERGY",

                    label=(
                        "light provides "
                        "energy"
                    ),

                    alternatives=(
                        "light energy",
                        "energy from light",

                        "sunlight provides energy",
                        "light provides energy",

                        "energy from sunlight",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        # --------------------------------------------------
        # CHALLENGING 2
        # --------------------------------------------------

        ScienceQuestion(
            question_id=(
                "PHOTO-C-02"
            ),

            prompt=(
                "Explain how matter "
                "enters and leaves a "
                "plant during "
                "photosynthesis."
            ),

            difficulty=(
                DifficultyLevel
                .CHALLENGING
            ),

            required_ideas=(

                ScienceIdea(
                    code="CO2_ENTER",

                    label=(
                        "carbon dioxide "
                        "comes from air"
                    ),

                    alternatives=(
                        "carbon dioxide from air",
                        "carbon dioxide enters",
                        "co2 from air",
                    ),
                ),

                ScienceIdea(
                    code="WATER_ENTER",

                    label=(
                        "water enters "
                        "the plant"
                    ),

                    alternatives=(
                        "water from roots",
                        "roots absorb water",
                        "water enters",
                        "takes in water",
                    ),
                ),

                ScienceIdea(
                    code="GLUCOSE_MADE",

                    label=(
                        "glucose or food "
                        "is made"
                    ),

                    alternatives=(
                        "glucose is made",
                        "makes glucose",

                        "food is made",
                        "makes food",

                        "sugar is made",
                    ),
                ),

                ScienceIdea(
                    code="OXYGEN_RELEASE",

                    label=(
                        "oxygen is released"
                    ),

                    alternatives=(
                        "oxygen is released",
                        "releases oxygen",
                        "oxygen leaves",
                        "gives off oxygen",
                    ),
                ),
            ),

            minimum_correct_ideas=3,
        ),
    ),


    # ======================================================
    # STATES OF MATTER
    # ======================================================

    "SCI_PHY_MATTER_01": (

        ScienceQuestion(
            question_id=(
                "MATTER-E-01"
            ),

            prompt=(
                "How are particles "
                "different in solids, "
                "liquids and gases?"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),

            required_ideas=(

                ScienceIdea(
                    code="SOLID_PARTICLES",

                    label=(
                        "solid particles "
                        "are close"
                    ),

                    alternatives=(
                        (
                            "solid particles "
                            "are close"
                        ),

                        (
                            "particles in solids "
                            "are close"
                        ),

                        (
                            "tightly packed"
                        ),

                        "particles vibrate",
                    ),
                ),

                ScienceIdea(
                    code="LIQUID_PARTICLES",

                    label=(
                        "liquid particles "
                        "can move"
                    ),

                    alternatives=(
                        (
                            "liquid particles "
                            "move"
                        ),

                        (
                            "particles in liquids "
                            "move"
                        ),

                        "move past each other",
                        "slide past each other",
                    ),
                ),

                ScienceIdea(
                    code="GAS_PARTICLES",

                    label=(
                        "gas particles are "
                        "far apart"
                    ),

                    alternatives=(
                        (
                            "gas particles are "
                            "far apart"
                        ),

                        (
                            "particles in gases "
                            "are far apart"
                        ),

                        (
                            "gas particles "
                            "move freely"
                        ),
                    ),
                ),
            ),

            minimum_correct_ideas=2,

            misconceptions=(

                ScienceMisconception(
                    code=(
                        "SCI_MATTER_PARTICLES_STOP"
                    ),

                    patterns=(
                        "particles stop moving",

                        (
                            "solid particles "
                            "do not move"
                        ),

                        (
                            "particles in solids "
                            "do not move"
                        ),
                    ),
                ),
            ),
        ),


        ScienceQuestion(
            question_id=(
                "MATTER-E-02"
            ),

            prompt=(
                "What happens when ice "
                "melts and when water "
                "boils?"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),

            required_ideas=(

                ScienceIdea(
                    code="MELTING",

                    label=(
                        "solid changes "
                        "to liquid"
                    ),

                    alternatives=(
                        "solid to liquid",
                        "ice becomes water",
                        "ice turns into water",
                    ),
                ),

                ScienceIdea(
                    code="BOILING",

                    label=(
                        "liquid changes "
                        "to gas"
                    ),

                    alternatives=(
                        "liquid to gas",
                        "water becomes gas",
                        "water becomes vapor",
                        "water becomes vapour",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id=(
                "MATTER-M-01"
            ),

            prompt=(
                "What happens when a "
                "gas cools enough to "
                "condense?"
            ),

            difficulty=(
                DifficultyLevel
                .MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="CONDENSATION",

                    label=(
                        "gas changes "
                        "to liquid"
                    ),

                    alternatives=(
                        "gas to liquid",
                        "gas becomes liquid",
                        "gas turns into liquid",
                        "condenses into liquid",
                    ),
                ),

                ScienceIdea(
                    code="ENERGY_LOSS",

                    label=(
                        "particles lose "
                        "energy"
                    ),

                    alternatives=(
                        "lose energy",
                        "loses energy",
                        "less energy",
                        "cooling",
                        "cools",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id=(
                "MATTER-M-02"
            ),

            prompt=(
                "How does heating affect "
                "the movement of "
                "particles?"
            ),

            difficulty=(
                DifficultyLevel
                .MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="GAIN_ENERGY",

                    label=(
                        "particles gain "
                        "energy"
                    ),

                    alternatives=(
                        "gain energy",
                        "gains energy",
                        "more energy",
                    ),
                ),

                ScienceIdea(
                    code="MOVE_FASTER",

                    label=(
                        "particles move "
                        "faster"
                    ),

                    alternatives=(
                        "move faster",
                        "moves faster",
                        "move more quickly",
                        "move quicker",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id=(
                "MATTER-C-01"
            ),

            prompt=(
                "Why can a gas spread "
                "out and fill the "
                "whole container?"
            ),

            difficulty=(
                DifficultyLevel
                .CHALLENGING
            ),

            required_ideas=(

                ScienceIdea(
                    code="FAR_APART",

                    label=(
                        "gas particles "
                        "are far apart"
                    ),

                    alternatives=(
                        "far apart",
                        "spaces between particles",
                        "large spaces",
                    ),
                ),

                ScienceIdea(
                    code="MOVE_FREELY",

                    label=(
                        "gas particles "
                        "move freely"
                    ),

                    alternatives=(
                        "move freely",
                        "move in all directions",
                        "move around freely",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id=(
                "MATTER-C-02"
            ),

            prompt=(
                "Compare melting and "
                "freezing. What changes "
                "in each process?"
            ),

            difficulty=(
                DifficultyLevel
                .CHALLENGING
            ),

            required_ideas=(

                ScienceIdea(
                    code="MELTING_CHANGE",

                    label=(
                        "melting is "
                        "solid to liquid"
                    ),

                    alternatives=(
                        "solid to liquid",
                        "melting changes solid",
                    ),
                ),

                ScienceIdea(
                    code="FREEZING_CHANGE",

                    label=(
                        "freezing is "
                        "liquid to solid"
                    ),

                    alternatives=(
                        "liquid to solid",
                        "freezing changes liquid",
                        "water becomes ice",
                    ),
                ),

                ScienceIdea(
                    code="ENERGY_CHANGE",

                    label=(
                        "energy changes "
                        "during the processes"
                    ),

                    alternatives=(
                        "gain energy",
                        "gains energy",
                        "lose energy",
                        "loses energy",
                        "heat added",
                        "heat removed",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),
    ),


    # ======================================================
    # FOOD CHAINS
    # ======================================================

    "SCI_BIO_FOODCHAIN_01": (

        ScienceQuestion(
            question_id=(
                "FOOD-E-01"
            ),

            prompt=(
                "What is a food chain, "
                "and where does its "
                "energy usually begin?"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),

            required_ideas=(

                ScienceIdea(
                    code="ENERGY_TRANSFER",

                    label=(
                        "energy moves "
                        "between organisms"
                    ),

                    alternatives=(
                        "energy moves",
                        "energy passes",
                        "energy flows",
                        "energy transfer",
                    ),
                ),

                ScienceIdea(
                    code="PRODUCER",

                    label=(
                        "producer or plant"
                    ),

                    alternatives=(
                        "producer",
                        "producers",
                        "plant",
                        "plants",
                    ),
                ),

                ScienceIdea(
                    code="SUN",

                    label="the Sun",

                    alternatives=(
                        "sun",
                        "sunlight",
                        "solar energy",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id=(
                "FOOD-E-02"
            ),

            prompt=(
                "Why are green plants "
                "called producers in "
                "a food chain?"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),

            required_ideas=(

                ScienceIdea(
                    code="MAKE_FOOD",

                    label=(
                        "plants make "
                        "their own food"
                    ),

                    alternatives=(
                        "make their own food",
                        "makes its own food",
                        "produce their own food",
                        "produce food",
                    ),
                ),

                ScienceIdea(
                    code="PHOTOSYNTHESIS",

                    label=(
                        "photosynthesis"
                    ),

                    alternatives=(
                        "photosynthesis",
                        "using sunlight",
                        "uses sunlight",
                    ),
                ),
            ),

            minimum_correct_ideas=2,

            misconceptions=(

                ScienceMisconception(
                    code=(
                        "SCI_FOODCHAIN_PLANT_CONSUMER"
                    ),

                    patterns=(
                        "plants are consumers",
                        "plant is a consumer",
                    ),
                ),
            ),
        ),


        ScienceQuestion(
            question_id=(
                "FOOD-M-01"
            ),

            prompt=(
                "What do the arrows "
                "in a food chain show?"
            ),

            difficulty=(
                DifficultyLevel
                .MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="ENERGY_DIRECTION",

                    label=(
                        "direction of "
                        "energy flow"
                    ),

                    alternatives=(
                        "direction of energy",
                        "energy direction",
                        "energy flows",
                        "energy flow",
                        "energy moves",
                        "energy passes",
                    ),
                ),

                ScienceIdea(
                    code="TO_CONSUMER",

                    label=(
                        "energy moves to "
                        "the organism "
                        "that eats it"
                    ),

                    alternatives=(
                        "from food to consumer",
                        "from prey to predator",
                        "from plant to animal",
                        "from eaten to eater",

                        (
                            "to the organism "
                            "that eats it"
                        ),
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id=(
                "FOOD-M-02"
            ),

            prompt=(
                "In the chain "
                "grass → rabbit → fox, "
                "how does energy move?"
            ),

            difficulty=(
                DifficultyLevel
                .MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="SUN_TO_GRASS",

                    label=(
                        "energy begins with "
                        "the Sun and grass"
                    ),

                    alternatives=(
                        "sun to grass",
                        "sunlight to grass",
                        "grass gets energy from sun",
                        "grass gets energy from sunlight",
                    ),
                ),

                ScienceIdea(
                    code="GRASS_TO_RABBIT",

                    label=(
                        "energy moves from "
                        "grass to rabbit"
                    ),

                    alternatives=(
                        "grass to rabbit",
                        "rabbit eats grass",
                    ),
                ),

                ScienceIdea(
                    code="RABBIT_TO_FOX",

                    label=(
                        "energy moves from "
                        "rabbit to fox"
                    ),

                    alternatives=(
                        "rabbit to fox",
                        "fox eats rabbit",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id=(
                "FOOD-C-01"
            ),

            prompt=(
                "If the amount of grass "
                "in a grass → rabbit → "
                "fox food chain became "
                "very low, how could this "
                "affect the rabbits "
                "and foxes?"
            ),

            difficulty=(
                DifficultyLevel
                .CHALLENGING
            ),

            required_ideas=(

                ScienceIdea(
                    code="LESS_RABBIT_FOOD",

                    label=(
                        "rabbits have "
                        "less food"
                    ),

                    alternatives=(
                        "less food for rabbits",
                        "rabbits have less food",
                        "rabbits get less food",
                    ),
                ),

                ScienceIdea(
                    code="RABBIT_DECREASE",

                    label=(
                        "rabbit population "
                        "may decrease"
                    ),

                    alternatives=(
                        "fewer rabbits",
                        "rabbit population decreases",
                        "rabbits decrease",
                    ),
                ),

                ScienceIdea(
                    code="FOX_EFFECT",

                    label=(
                        "foxes receive "
                        "less food or energy"
                    ),

                    alternatives=(
                        "less food for foxes",
                        "fewer foxes",
                        "fox population decreases",
                        "foxes get less energy",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id=(
                "FOOD-C-02"
            ),

            prompt=(
                "Why do food-chain "
                "arrows point from the "
                "organism being eaten "
                "toward the organism "
                "that eats it?"
            ),

            difficulty=(
                DifficultyLevel
                .CHALLENGING
            ),

            required_ideas=(

                ScienceIdea(
                    code="ENERGY_FLOW",

                    label=(
                        "arrows show "
                        "energy flow"
                    ),

                    alternatives=(
                        "energy flow",
                        "energy moves",
                        "energy passes",
                        "shows energy",
                    ),
                ),

                ScienceIdea(
                    code="SOURCE_TO_CONSUMER",

                    label=(
                        "energy moves from "
                        "food source to "
                        "consumer"
                    ),

                    alternatives=(
                        "food to consumer",
                        "prey to predator",
                        "plant to animal",
                        "eaten organism to eater",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),
    ),
}


def get_science_questions(
    concept_code: str,
) -> tuple[
    ScienceQuestion,
    ...,
]:

    return (
        SCIENCE_QUESTION_BANK
        .get(
            concept_code,
            (),
        )
    )


def find_science_question(
    concept_code: str,
    prompt: str,
) -> ScienceQuestion | None:

    normalized_prompt = (
        prompt
        .strip()
        .lower()
    )


    for question in (
        get_science_questions(
            concept_code
        )
    ):

        if (
            question.prompt
            .strip()
            .lower()
            == normalized_prompt
        ):

            return question


    return None


def get_science_question(
    concept_code: str,
    offset: int = 0,
    difficulty: (
        DifficultyLevel
        | None
    ) = None,
) -> ScienceQuestion | None:

    questions = list(
        get_science_questions(
            concept_code
        )
    )


    if difficulty is not None:

        questions = [
            question

            for question
            in questions

            if (
                question.difficulty
                == difficulty
            )
        ]


    if (
        not questions
    ):

        return None


    index = (
        offset
        % len(
            questions
        )
    )


    return (
        questions[
            index
        ]
    )
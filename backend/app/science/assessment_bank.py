from app.science.question_bank import (
    ScienceIdea,
    ScienceMisconception,
    ScienceQuestion,
)
from app.schemas.enums import (
    AssessmentType,
    DifficultyLevel,
)


SCIENCE_ASSESSMENT_BANK: dict[
    tuple[
        str,
        AssessmentType,
    ],
    tuple[
        ScienceQuestion,
        ...,
    ],
] = {


    # ======================================================
    # PHOTOSYNTHESIS — DIAGNOSTIC
    # ======================================================

    (
        "SCI_BIO_PHOTO_01",
        AssessmentType.DIAGNOSTIC,
    ): (

        ScienceQuestion(
            question_id="PHOTO-D-01",

            prompt=(
                "What three things does "
                "a plant need for "
                "photosynthesis?"
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
                    code="CO2",
                    label="carbon dioxide",
                    alternatives=(
                        "carbon dioxide",
                        "co2",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="PHOTO-D-02",

            prompt=(
                "What food-like substance "
                "does a plant make during "
                "photosynthesis?"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),

            required_ideas=(

                ScienceIdea(
                    code="GLUCOSE",
                    label="glucose or sugar",
                    alternatives=(
                        "glucose",
                        "sugar",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="PHOTO-D-03",

            prompt=(
                "What gas does a plant "
                "release during "
                "photosynthesis?"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),

            required_ideas=(

                ScienceIdea(
                    code="OXYGEN",
                    label="oxygen",
                    alternatives=(
                        "oxygen",
                        "o2",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="PHOTO-D-04",

            prompt=(
                "Why is chlorophyll "
                "important for "
                "photosynthesis?"
            ),

            difficulty=(
                DifficultyLevel.MODERATE
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
                    label="absorbs light",
                    alternatives=(
                        "absorbs light",
                        "absorb light",
                        "captures light",
                        "captures sunlight",
                        "absorbs sunlight",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="PHOTO-D-05",

            prompt=(
                "Why would photosynthesis "
                "slow down if a plant "
                "received no light?"
            ),

            difficulty=(
                DifficultyLevel.CHALLENGING
            ),

            required_ideas=(

                ScienceIdea(
                    code="LIGHT_REQUIRED",
                    label="light is required",
                    alternatives=(
                        "needs light",
                        "requires light",
                        "without light",
                        "no light",
                    ),
                ),

                ScienceIdea(
                    code="LIGHT_ENERGY",
                    label="light provides energy",
                    alternatives=(
                        "light provides energy",
                        "energy from light",
                        "light energy",
                        "sunlight provides energy",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),
    ),


    # ======================================================
    # PHOTOSYNTHESIS — MASTERY
    # ======================================================

    (
        "SCI_BIO_PHOTO_01",
        AssessmentType.MASTERY,
    ): (

        ScienceQuestion(
            question_id="PHOTO-MA-01",

            prompt=(
                "Explain what enters "
                "a plant and what is "
                "produced during "
                "photosynthesis."
            ),

            difficulty=(
                DifficultyLevel.MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="WATER",
                    label="water",
                    alternatives=(
                        "water",
                    ),
                ),

                ScienceIdea(
                    code="CO2",
                    label="carbon dioxide",
                    alternatives=(
                        "carbon dioxide",
                        "co2",
                    ),
                ),

                ScienceIdea(
                    code="GLUCOSE",
                    label="glucose",
                    alternatives=(
                        "glucose",
                        "sugar",
                        "makes food",
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

            minimum_correct_ideas=3,
        ),


        ScienceQuestion(
            question_id="PHOTO-MA-02",

            prompt=(
                "How does sunlight help "
                "a plant during "
                "photosynthesis?"
            ),

            difficulty=(
                DifficultyLevel.MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="ENERGY",
                    label="light provides energy",
                    alternatives=(
                        "provides energy",
                        "light energy",
                        "energy from sunlight",
                        "energy from light",
                    ),
                ),

                ScienceIdea(
                    code="FOOD",
                    label="used to make food",
                    alternatives=(
                        "make food",
                        "make glucose",
                        "make sugar",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="PHOTO-MA-03",

            prompt=(
                "Where does the carbon "
                "in glucose originally "
                "come from?"
            ),

            difficulty=(
                DifficultyLevel.MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="AIR_CO2",
                    label="carbon dioxide from air",
                    alternatives=(
                        "carbon dioxide from air",
                        "carbon dioxide from the air",
                        "co2 from air",
                        "co2 from the air",
                    ),
                ),
            ),

            minimum_correct_ideas=1,

            misconceptions=(

                ScienceMisconception(
                    code=(
                        "SCI_PHOTO_CARBON_FROM_SOIL"
                    ),

                    patterns=(
                        "carbon from soil",
                        "carbon from the soil",
                        "carbon comes from soil",
                    ),
                ),
            ),
        ),


        ScienceQuestion(
            question_id="PHOTO-MA-04",

            prompt=(
                "A plant has water but "
                "no carbon dioxide. Why "
                "can it not continue "
                "normal photosynthesis?"
            ),

            difficulty=(
                DifficultyLevel.CHALLENGING
            ),

            required_ideas=(

                ScienceIdea(
                    code="CO2_REQUIRED",
                    label="carbon dioxide is required",
                    alternatives=(
                        "needs carbon dioxide",
                        "requires carbon dioxide",
                        "needs co2",
                        "requires co2",
                    ),
                ),

                ScienceIdea(
                    code="GLUCOSE_CARBON",
                    label="used to build glucose",
                    alternatives=(
                        "make glucose",
                        "build glucose",
                        "make sugar",
                        "make food",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="PHOTO-MA-05",

            prompt=(
                "Explain why saying "
                "'plants get their food "
                "from soil' is incomplete "
                "or incorrect."
            ),

            difficulty=(
                DifficultyLevel.CHALLENGING
            ),

            required_ideas=(

                ScienceIdea(
                    code="MAKE_FOOD",
                    label="plants make food",
                    alternatives=(
                        "plants make food",
                        "make their own food",
                        "produce their own food",
                        "make glucose",
                    ),
                ),

                ScienceIdea(
                    code="PHOTOSYNTHESIS",
                    label="photosynthesis",
                    alternatives=(
                        "photosynthesis",
                    ),
                ),

                ScienceIdea(
                    code="INPUTS",
                    label="water and carbon dioxide",
                    alternatives=(
                        "water and carbon dioxide",
                        "carbon dioxide and water",
                        "water and co2",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),
    ),


    # ======================================================
    # STATES OF MATTER — DIAGNOSTIC
    # ======================================================

    (
        "SCI_PHY_MATTER_01",
        AssessmentType.DIAGNOSTIC,
    ): (

        ScienceQuestion(
            question_id="MATTER-D-01",

            prompt=(
                "How are particles "
                "arranged in a solid?"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),

            required_ideas=(

                ScienceIdea(
                    code="CLOSE",
                    label="particles are close",
                    alternatives=(
                        "close together",
                        "tightly packed",
                        "particles are close",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="MATTER-D-02",

            prompt=(
                "What state change "
                "happens when ice "
                "becomes water?"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),

            required_ideas=(

                ScienceIdea(
                    code="MELTING",
                    label="melting",
                    alternatives=(
                        "melting",
                        "solid to liquid",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="MATTER-D-03",

            prompt=(
                "What happens when "
                "liquid water boils?"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),

            required_ideas=(

                ScienceIdea(
                    code="GAS",
                    label="liquid changes to gas",
                    alternatives=(
                        "liquid to gas",
                        "becomes gas",
                        "becomes vapor",
                        "becomes vapour",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="MATTER-D-04",

            prompt=(
                "How does heating affect "
                "particle movement?"
            ),

            difficulty=(
                DifficultyLevel.MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="ENERGY",
                    label="particles gain energy",
                    alternatives=(
                        "gain energy",
                        "more energy",
                    ),
                ),

                ScienceIdea(
                    code="FASTER",
                    label="particles move faster",
                    alternatives=(
                        "move faster",
                        "move more quickly",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="MATTER-D-05",

            prompt=(
                "Why can a gas fill "
                "the whole container?"
            ),

            difficulty=(
                DifficultyLevel.CHALLENGING
            ),

            required_ideas=(

                ScienceIdea(
                    code="FAR",
                    label="particles are far apart",
                    alternatives=(
                        "far apart",
                        "large spaces",
                    ),
                ),

                ScienceIdea(
                    code="FREE",
                    label="particles move freely",
                    alternatives=(
                        "move freely",
                        "move in all directions",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),
    ),


    # ======================================================
    # STATES OF MATTER — MASTERY
    # ======================================================

    (
        "SCI_PHY_MATTER_01",
        AssessmentType.MASTERY,
    ): (

        ScienceQuestion(
            question_id="MATTER-MA-01",

            prompt=(
                "Compare particle movement "
                "in solids and gases."
            ),

            difficulty=(
                DifficultyLevel.MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="SOLID",
                    label="solid particles vibrate",
                    alternatives=(
                        "solid particles vibrate",
                        "vibrate in place",
                    ),
                ),

                ScienceIdea(
                    code="GAS",
                    label="gas particles move freely",
                    alternatives=(
                        "gas particles move freely",
                        "gas particles move fast",
                        "move freely",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="MATTER-MA-02",

            prompt=(
                "Explain condensation "
                "using particles."
            ),

            difficulty=(
                DifficultyLevel.MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="GAS_LIQUID",
                    label="gas becomes liquid",
                    alternatives=(
                        "gas becomes liquid",
                        "gas to liquid",
                    ),
                ),

                ScienceIdea(
                    code="LOSE_ENERGY",
                    label="particles lose energy",
                    alternatives=(
                        "lose energy",
                        "less energy",
                        "cooling",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="MATTER-MA-03",

            prompt=(
                "Explain the difference "
                "between melting and "
                "freezing."
            ),

            difficulty=(
                DifficultyLevel.MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="MELT",
                    label="solid to liquid",
                    alternatives=(
                        "solid to liquid",
                    ),
                ),

                ScienceIdea(
                    code="FREEZE",
                    label="liquid to solid",
                    alternatives=(
                        "liquid to solid",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="MATTER-MA-04",

            prompt=(
                "Why do particles move "
                "faster when matter "
                "is heated?"
            ),

            difficulty=(
                DifficultyLevel.CHALLENGING
            ),

            required_ideas=(

                ScienceIdea(
                    code="ENERGY",
                    label="particles gain energy",
                    alternatives=(
                        "gain energy",
                        "more energy",
                        "heat gives energy",
                    ),
                ),

                ScienceIdea(
                    code="MOVEMENT",
                    label="more energy increases movement",
                    alternatives=(
                        "move faster",
                        "movement increases",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="MATTER-MA-05",

            prompt=(
                "Explain why solid "
                "particles are not "
                "completely motionless."
            ),

            difficulty=(
                DifficultyLevel.CHALLENGING
            ),

            required_ideas=(

                ScienceIdea(
                    code="VIBRATION",
                    label="particles vibrate",
                    alternatives=(
                        "particles vibrate",
                        "vibrate in place",
                        "still vibrate",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),
    ),


    # ======================================================
    # FOOD CHAINS — DIAGNOSTIC
    # ======================================================

    (
        "SCI_BIO_FOODCHAIN_01",
        AssessmentType.DIAGNOSTIC,
    ): (

        ScienceQuestion(
            question_id="FOOD-D-01",

            prompt=(
                "Where does most energy "
                "in a food chain "
                "originally come from?"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),

            required_ideas=(

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

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="FOOD-D-02",

            prompt=(
                "Why are plants called "
                "producers?"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),

            required_ideas=(

                ScienceIdea(
                    code="FOOD",
                    label="plants make their own food",
                    alternatives=(
                        "make their own food",
                        "produce their own food",
                        "make food",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="FOOD-D-03",

            prompt=(
                "What do arrows in "
                "a food chain represent?"
            ),

            difficulty=(
                DifficultyLevel.MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="ENERGY",
                    label="direction of energy flow",
                    alternatives=(
                        "energy flow",
                        "energy moves",
                        "direction of energy",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="FOOD-D-04",

            prompt=(
                "In grass → rabbit → fox, "
                "where does the rabbit "
                "get its energy?"
            ),

            difficulty=(
                DifficultyLevel.MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="GRASS",
                    label="from grass",
                    alternatives=(
                        "grass",
                        "from the grass",
                        "eats grass",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="FOOD-D-05",

            prompt=(
                "What could happen to "
                "foxes if the rabbit "
                "population became "
                "very small?"
            ),

            difficulty=(
                DifficultyLevel.CHALLENGING
            ),

            required_ideas=(

                ScienceIdea(
                    code="LESS_FOOD",
                    label="foxes have less food",
                    alternatives=(
                        "less food",
                        "fewer rabbits to eat",
                        "less energy",
                    ),
                ),

                ScienceIdea(
                    code="FOX_DROP",
                    label="fox population may decrease",
                    alternatives=(
                        "fewer foxes",
                        "foxes decrease",
                        "fox population decreases",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),
    ),


    # ======================================================
    # FOOD CHAINS — MASTERY
    # ======================================================

    (
        "SCI_BIO_FOODCHAIN_01",
        AssessmentType.MASTERY,
    ): (

        ScienceQuestion(
            question_id="FOOD-MA-01",

            prompt=(
                "Explain how energy "
                "moves through "
                "grass → rabbit → fox."
            ),

            difficulty=(
                DifficultyLevel.MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="GRASS_RABBIT",
                    label="grass to rabbit",
                    alternatives=(
                        "grass to rabbit",
                        "rabbit eats grass",
                    ),
                ),

                ScienceIdea(
                    code="RABBIT_FOX",
                    label="rabbit to fox",
                    alternatives=(
                        "rabbit to fox",
                        "fox eats rabbit",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="FOOD-MA-02",

            prompt=(
                "Why does a food chain "
                "usually begin with "
                "a producer?"
            ),

            difficulty=(
                DifficultyLevel.MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="PRODUCER",
                    label="producer makes food",
                    alternatives=(
                        "makes food",
                        "makes its own food",
                        "produces food",
                    ),
                ),

                ScienceIdea(
                    code="SUN",
                    label="uses sunlight",
                    alternatives=(
                        "sunlight",
                        "sun",
                        "solar energy",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="FOOD-MA-03",

            prompt=(
                "Why do food-chain "
                "arrows point toward "
                "the organism that "
                "receives the energy?"
            ),

            difficulty=(
                DifficultyLevel.MODERATE
            ),

            required_ideas=(

                ScienceIdea(
                    code="FLOW",
                    label="arrows show energy flow",
                    alternatives=(
                        "energy flow",
                        "energy moves",
                        "energy passes",
                    ),
                ),

                ScienceIdea(
                    code="RECEIVER",
                    label="energy moves to consumer",
                    alternatives=(
                        "to the consumer",
                        "to the organism that eats it",
                        "food to consumer",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="FOOD-MA-04",

            prompt=(
                "If producers disappeared "
                "from an ecosystem, why "
                "would consumers be affected?"
            ),

            difficulty=(
                DifficultyLevel.CHALLENGING
            ),

            required_ideas=(

                ScienceIdea(
                    code="ENERGY_SOURCE",
                    label="producers supply energy",
                    alternatives=(
                        "source of energy",
                        "provide energy",
                        "supply energy",
                    ),
                ),

                ScienceIdea(
                    code="LESS_FOOD",
                    label="consumers lose food",
                    alternatives=(
                        "less food",
                        "lose food",
                        "no food",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="FOOD-MA-05",

            prompt=(
                "Explain why energy "
                "moves through a food "
                "chain rather than "
                "starting with consumers."
            ),

            difficulty=(
                DifficultyLevel.CHALLENGING
            ),

            required_ideas=(

                ScienceIdea(
                    code="SUN",
                    label="energy begins with sunlight",
                    alternatives=(
                        "sun",
                        "sunlight",
                        "solar energy",
                    ),
                ),

                ScienceIdea(
                    code="PRODUCER",
                    label="producers capture energy",
                    alternatives=(
                        "producers",
                        "plants capture",
                        "plants use sunlight",
                    ),
                ),

                ScienceIdea(
                    code="CONSUMER",
                    label="consumers obtain energy by eating",
                    alternatives=(
                        "consumers eat",
                        "animals eat",
                        "get energy by eating",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),
    ),
}


def get_science_assessment_questions(
    concept_code: str,
    assessment_type: AssessmentType,
) -> tuple[
    ScienceQuestion,
    ...,
]:

    return (
        SCIENCE_ASSESSMENT_BANK.get(
            (
                concept_code,
                assessment_type,
            ),
            (),
        )
    )
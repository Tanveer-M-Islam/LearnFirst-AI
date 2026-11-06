from dataclasses import dataclass

from app.schemas.enums import (
    DifficultyLevel,
)


@dataclass(frozen=True)
class ScienceIdea:
    code: str

    label: str

    alternatives: tuple[
        str,
        ...,
    ]


@dataclass(frozen=True)
class ScienceMisconception:
    code: str

    patterns: tuple[
        str,
        ...,
    ]


@dataclass(frozen=True)
class ScienceQuestion:
    question_id: str

    prompt: str

    difficulty: DifficultyLevel

    required_ideas: tuple[
        ScienceIdea,
        ...,
    ]

    minimum_correct_ideas: int

    misconceptions: tuple[
        ScienceMisconception,
        ...,
    ] = ()


E = DifficultyLevel.EASY

M = DifficultyLevel.MODERATE

C = DifficultyLevel.CHALLENGING


SCIENCE_QUESTION_BANK: dict[
    str,
    tuple[
        ScienceQuestion,
        ...,
    ],
] = {

    # ==================================================
    # AGE 7 — LIVING THINGS
    # ==================================================

    "SCI_LIFE_BASIC_01": (

        ScienceQuestion(
            question_id="LIFE-E-01",

            prompt=(
                "What are three things "
                "living things need "
                "to survive?"
            ),

            difficulty=E,

            required_ideas=(

                ScienceIdea(
                    code="WATER",
                    label="water",
                    alternatives=(
                        "water",
                    ),
                ),

                ScienceIdea(
                    code="AIR",
                    label="air",
                    alternatives=(
                        "air",
                        "oxygen",
                    ),
                ),

                ScienceIdea(
                    code="FOOD",
                    label="food or energy",
                    alternatives=(
                        "food",
                        "energy",
                        "nutrients",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="LIFE-E-02",

            prompt=(
                "Name two signs that "
                "something is alive."
            ),

            difficulty=E,

            required_ideas=(

                ScienceIdea(
                    code="GROW",
                    label="grows",
                    alternatives=(
                        "grow",
                        "grows",
                        "growth",
                    ),
                ),

                ScienceIdea(
                    code="RESPOND",
                    label=(
                        "responds to surroundings"
                    ),
                    alternatives=(
                        "respond",
                        "responds",
                        "reacts",
                        "react",
                    ),
                ),

                ScienceIdea(
                    code="REPRODUCE",
                    label="reproduces",
                    alternatives=(
                        "reproduce",
                        "reproduces",
                        "have babies",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="LIFE-M-01",

            prompt=(
                "How can you tell that "
                "a plant is a living thing?"
            ),

            difficulty=M,

            required_ideas=(

                ScienceIdea(
                    code="PLANT_GROWS",
                    label="plant grows",
                    alternatives=(
                        "plant grows",
                        "it grows",
                        "grows",
                    ),
                ),

                ScienceIdea(
                    code="PLANT_NEEDS",
                    label=(
                        "plant needs water "
                        "or light"
                    ),
                    alternatives=(
                        "needs water",
                        "needs sunlight",
                        "needs light",
                        "needs nutrients",
                    ),
                ),

                ScienceIdea(
                    code="PLANT_RESPONDS",
                    label=(
                        "plant responds "
                        "to surroundings"
                    ),
                    alternatives=(
                        "responds",
                        "respond",
                        "grows toward light",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="LIFE-M-02",

            prompt=(
                "Why does an animal "
                "need food?"
            ),

            difficulty=M,

            required_ideas=(

                ScienceIdea(
                    code="ENERGY",
                    label="food provides energy",
                    alternatives=(
                        "provides energy",
                        "gives energy",
                        "for energy",
                    ),
                ),

                ScienceIdea(
                    code="GROWTH",
                    label=(
                        "energy supports growth "
                        "and life processes"
                    ),
                    alternatives=(
                        "grow",
                        "growth",
                        "stay alive",
                        "life processes",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="LIFE-C-01",

            prompt=(
                "Why is a toy car "
                "not alive even though "
                "it can move?"
            ),

            difficulty=C,

            required_ideas=(

                ScienceIdea(
                    code="NO_GROWTH",
                    label=(
                        "it does not grow"
                    ),
                    alternatives=(
                        "does not grow",
                        "cannot grow",
                    ),
                ),

                ScienceIdea(
                    code="NO_LIFE_PROCESS",
                    label=(
                        "it does not perform "
                        "life processes"
                    ),
                    alternatives=(
                        "does not reproduce",
                        "does not need food",
                        "does not breathe",
                        "not living",
                        "not alive",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="LIFE-C-02",

            prompt=(
                "A seed looks inactive. "
                "Why is it still considered "
                "living?"
            ),

            difficulty=C,

            required_ideas=(

                ScienceIdea(
                    code="CAN_GROW",
                    label=(
                        "it can grow into "
                        "a plant"
                    ),
                    alternatives=(
                        "can grow",
                        "grows into a plant",
                        "can germinate",
                        "germinate",
                    ),
                ),

                ScienceIdea(
                    code="LIFE_INSIDE",
                    label=(
                        "living processes can "
                        "begin under the right "
                        "conditions"
                    ),
                    alternatives=(
                        "right conditions",
                        "water and warmth",
                        "start growing",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),
    ),


    # ==================================================
    # AGE 8 — EVERYDAY MATERIALS
    # ==================================================

    "SCI_MATERIAL_BASIC_01": (

        ScienceQuestion(
            question_id="MATERIAL-E-01",

            prompt=(
                "Name two properties "
                "that can describe "
                "a material."
            ),

            difficulty=E,

            required_ideas=(

                ScienceIdea(
                    code="HARDNESS",
                    label="hard or soft",
                    alternatives=(
                        "hard",
                        "soft",
                        "hardness",
                    ),
                ),

                ScienceIdea(
                    code="FLEXIBILITY",
                    label=(
                        "flexible or rigid"
                    ),
                    alternatives=(
                        "flexible",
                        "rigid",
                        "bendable",
                    ),
                ),

                ScienceIdea(
                    code="TRANSPARENCY",
                    label=(
                        "transparent "
                        "or opaque"
                    ),
                    alternatives=(
                        "transparent",
                        "opaque",
                        "see through",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="MATERIAL-E-02",

            prompt=(
                "Why is glass useful "
                "for making windows?"
            ),

            difficulty=E,

            required_ideas=(

                ScienceIdea(
                    code="TRANSPARENT",
                    label="glass is transparent",
                    alternatives=(
                        "transparent",
                        "see through",
                        "lets light through",
                    ),
                ),

                ScienceIdea(
                    code="SOLID",
                    label="glass is solid",
                    alternatives=(
                        "solid",
                        "hard",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="MATERIAL-M-01",

            prompt=(
                "Why is rubber useful "
                "for making some "
                "shoe soles?"
            ),

            difficulty=M,

            required_ideas=(

                ScienceIdea(
                    code="FLEXIBLE",
                    label="rubber is flexible",
                    alternatives=(
                        "flexible",
                        "bendable",
                    ),
                ),

                ScienceIdea(
                    code="GRIP",
                    label=(
                        "rubber can provide grip"
                    ),
                    alternatives=(
                        "grip",
                        "friction",
                        "not slippery",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="MATERIAL-M-02",

            prompt=(
                "Why are raincoats often "
                "made from waterproof "
                "materials?"
            ),

            difficulty=M,

            required_ideas=(

                ScienceIdea(
                    code="REPEL_WATER",
                    label=(
                        "water does not pass "
                        "through easily"
                    ),
                    alternatives=(
                        "waterproof",
                        "does not absorb water",
                        "water cannot pass",
                        "keeps water out",
                    ),
                ),

                ScienceIdea(
                    code="KEEP_DRY",
                    label=(
                        "keeps the person dry"
                    ),
                    alternatives=(
                        "keeps dry",
                        "stay dry",
                        "keeps person dry",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="MATERIAL-C-01",

            prompt=(
                "Why might metal be "
                "better than paper for "
                "making a cooking pot?"
            ),

            difficulty=C,

            required_ideas=(

                ScienceIdea(
                    code="STRONG",
                    label="metal is strong",
                    alternatives=(
                        "strong",
                        "stronger",
                        "durable",
                    ),
                ),

                ScienceIdea(
                    code="HEAT",
                    label=(
                        "metal can transfer "
                        "or handle heat"
                    ),
                    alternatives=(
                        "conduct heat",
                        "conducts heat",
                        "handle heat",
                        "handles heat",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="MATERIAL-C-02",

            prompt=(
                "How would you choose "
                "a material for making "
                "an umbrella?"
            ),

            difficulty=C,

            required_ideas=(

                ScienceIdea(
                    code="WATERPROOF",
                    label=(
                        "material should "
                        "be waterproof"
                    ),
                    alternatives=(
                        "waterproof",
                        "water resistant",
                        "keeps water out",
                    ),
                ),

                ScienceIdea(
                    code="LIGHTWEIGHT",
                    label=(
                        "material should "
                        "be lightweight"
                    ),
                    alternatives=(
                        "light",
                        "lightweight",
                        "not heavy",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),
    ),


    # ==================================================
    # AGE 9 — STATES OF MATTER
    # ==================================================

    "SCI_PHY_MATTER_01": (

        ScienceQuestion(
            question_id="MATTER-E-01",

            prompt=(
                "How are particles "
                "different in solids, "
                "liquids and gases?"
            ),

            difficulty=E,

            required_ideas=(

                ScienceIdea(
                    code="SOLID_PARTICLES",
                    label=(
                        "solid particles "
                        "are close together"
                    ),
                    alternatives=(
                        "solid particles are close",
                        "particles in solids are close",
                        "tightly packed",
                    ),
                ),

                ScienceIdea(
                    code="LIQUID_PARTICLES",
                    label=(
                        "liquid particles "
                        "can move past "
                        "each other"
                    ),
                    alternatives=(
                        "liquid particles move",
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
                        "gas particles are far apart",
                        "far apart",
                        "move freely",
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
                        "solid particles do not move",
                    ),
                ),
            ),
        ),


        ScienceQuestion(
            question_id="MATTER-E-02",

            prompt=(
                "What happens when ice "
                "melts and when water boils?"
            ),

            difficulty=E,

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
            question_id="MATTER-M-01",

            prompt=(
                "What happens when "
                "a gas cools enough "
                "to condense?"
            ),

            difficulty=M,

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
                        "condenses into liquid",
                    ),
                ),

                ScienceIdea(
                    code="LOSE_ENERGY",
                    label=(
                        "particles lose energy"
                    ),
                    alternatives=(
                        "lose energy",
                        "loses energy",
                        "less energy",
                        "cools",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="MATTER-M-02",

            prompt=(
                "How does heating affect "
                "particle movement?"
            ),

            difficulty=M,

            required_ideas=(

                ScienceIdea(
                    code="GAIN_ENERGY",
                    label=(
                        "particles gain energy"
                    ),
                    alternatives=(
                        "gain energy",
                        "more energy",
                    ),
                ),

                ScienceIdea(
                    code="MOVE_FASTER",
                    label=(
                        "particles move faster"
                    ),
                    alternatives=(
                        "move faster",
                        "move more quickly",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="MATTER-C-01",

            prompt=(
                "Why can a gas spread "
                "out and fill an "
                "entire container?"
            ),

            difficulty=C,

            required_ideas=(

                ScienceIdea(
                    code="FAR_APART",
                    label=(
                        "particles are far apart"
                    ),
                    alternatives=(
                        "far apart",
                        "large spaces",
                    ),
                ),

                ScienceIdea(
                    code="MOVE_FREELY",
                    label=(
                        "particles move freely"
                    ),
                    alternatives=(
                        "move freely",
                        "move in all directions",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="MATTER-C-02",

            prompt=(
                "Compare melting and "
                "freezing."
            ),

            difficulty=C,

            required_ideas=(

                ScienceIdea(
                    code="MELTING_CHANGE",
                    label=(
                        "melting changes "
                        "solid to liquid"
                    ),
                    alternatives=(
                        "solid to liquid",
                        "melting",
                    ),
                ),

                ScienceIdea(
                    code="FREEZING_CHANGE",
                    label=(
                        "freezing changes "
                        "liquid to solid"
                    ),
                    alternatives=(
                        "liquid to solid",
                        "freezing",
                        "water becomes ice",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),
    ),


    # ==================================================
    # AGE 10 — FOOD CHAINS
    # ==================================================

    "SCI_BIO_FOODCHAIN_01": (

        ScienceQuestion(
            question_id="FOOD-E-01",

            prompt=(
                "What is a food chain, "
                "and where does its "
                "energy usually begin?"
            ),

            difficulty=E,

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
                    ),
                ),

                ScienceIdea(
                    code="SUN",
                    label="Sun",
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
            question_id="FOOD-E-02",

            prompt=(
                "Why are green plants "
                "called producers in "
                "a food chain?"
            ),

            difficulty=E,

            required_ideas=(

                ScienceIdea(
                    code="MAKE_FOOD",
                    label=(
                        "plants make "
                        "their own food"
                    ),
                    alternatives=(
                        "make their own food",
                        "produce their own food",
                        "produce food",
                    ),
                ),

                ScienceIdea(
                    code="PHOTOSYNTHESIS",
                    label="photosynthesis",
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
            question_id="FOOD-M-01",

            prompt=(
                "What do the arrows "
                "in a food chain show?"
            ),

            difficulty=M,

            required_ideas=(

                ScienceIdea(
                    code="ENERGY_DIRECTION",
                    label=(
                        "direction of "
                        "energy flow"
                    ),
                    alternatives=(
                        "direction of energy",
                        "energy flow",
                        "energy moves",
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
                        "food to consumer",
                        "prey to predator",
                        "plant to animal",
                        "eaten to eater",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="FOOD-M-02",

            prompt=(
                "In the chain "
                "grass → rabbit → fox, "
                "how does energy move?"
            ),

            difficulty=M,

            required_ideas=(

                ScienceIdea(
                    code="GRASS_TO_RABBIT",
                    label=(
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
            question_id="FOOD-C-01",

            prompt=(
                "If grass became very "
                "scarce, how could this "
                "affect rabbits and foxes?"
            ),

            difficulty=C,

            required_ideas=(

                ScienceIdea(
                    code="RABBIT_FOOD",
                    label=(
                        "rabbits have "
                        "less food"
                    ),
                    alternatives=(
                        "less food for rabbits",
                        "rabbits have less food",
                    ),
                ),

                ScienceIdea(
                    code="RABBIT_DROP",
                    label=(
                        "rabbit population "
                        "may decrease"
                    ),
                    alternatives=(
                        "fewer rabbits",
                        "rabbits decrease",
                    ),
                ),

                ScienceIdea(
                    code="FOX_DROP",
                    label=(
                        "foxes may decrease"
                    ),
                    alternatives=(
                        "fewer foxes",
                        "foxes decrease",
                        "less food for foxes",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="FOOD-C-02",

            prompt=(
                "Why do food-chain "
                "arrows point from "
                "food toward the "
                "organism eating it?"
            ),

            difficulty=C,

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
                    ),
                ),

                ScienceIdea(
                    code="SOURCE_TO_CONSUMER",
                    label=(
                        "energy moves from "
                        "food source to consumer"
                    ),
                    alternatives=(
                        "food to consumer",
                        "prey to predator",
                        "plant to animal",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),
    ),


    # ==================================================
    # AGE 11 — ECOSYSTEMS
    # ==================================================

    "SCI_ECO_SYSTEMS_01": (

        ScienceQuestion(
            question_id="ECO-E-01",

            prompt=(
                "What is an ecosystem?"
            ),

            difficulty=E,

            required_ideas=(

                ScienceIdea(
                    code="LIVING",
                    label="living organisms",
                    alternatives=(
                        "living things",
                        "organisms",
                        "plants and animals",
                    ),
                ),

                ScienceIdea(
                    code="ENVIRONMENT",
                    label="environment",
                    alternatives=(
                        "environment",
                        "surroundings",
                        "habitat",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="ECO-E-02",

            prompt=(
                "Give one living and "
                "one non-living part "
                "of an ecosystem."
            ),

            difficulty=E,

            required_ideas=(

                ScienceIdea(
                    code="BIOTIC",
                    label="living component",
                    alternatives=(
                        "plant",
                        "animal",
                        "organism",
                        "tree",
                    ),
                ),

                ScienceIdea(
                    code="ABIOTIC",
                    label=(
                        "non-living component"
                    ),
                    alternatives=(
                        "water",
                        "air",
                        "soil",
                        "sunlight",
                        "rock",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="ECO-M-01",

            prompt=(
                "How can removing one "
                "species affect an "
                "ecosystem?"
            ),

            difficulty=M,

            required_ideas=(

                ScienceIdea(
                    code="DEPENDENCE",
                    label=(
                        "organisms depend "
                        "on each other"
                    ),
                    alternatives=(
                        "depend on each other",
                        "connected",
                        "interact",
                    ),
                ),

                ScienceIdea(
                    code="POPULATION_CHANGE",
                    label=(
                        "other populations "
                        "can change"
                    ),
                    alternatives=(
                        "population changes",
                        "increase",
                        "decrease",
                        "fewer animals",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="ECO-M-02",

            prompt=(
                "How do non-living "
                "factors affect organisms "
                "in an ecosystem?"
            ),

            difficulty=M,

            required_ideas=(

                ScienceIdea(
                    code="RESOURCE",
                    label=(
                        "organisms depend "
                        "on resources"
                    ),
                    alternatives=(
                        "need water",
                        "need sunlight",
                        "need air",
                        "resources",
                    ),
                ),

                ScienceIdea(
                    code="SURVIVAL",
                    label=(
                        "conditions affect "
                        "survival or growth"
                    ),
                    alternatives=(
                        "survival",
                        "grow",
                        "growth",
                        "population",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="ECO-C-01",

            prompt=(
                "Why can pollution "
                "affect several species "
                "in one ecosystem?"
            ),

            difficulty=C,

            required_ideas=(

                ScienceIdea(
                    code="SHARED_ENVIRONMENT",
                    label=(
                        "species share "
                        "the environment"
                    ),
                    alternatives=(
                        "share environment",
                        "same environment",
                        "same habitat",
                    ),
                ),

                ScienceIdea(
                    code="CONNECTED",
                    label=(
                        "species are connected"
                    ),
                    alternatives=(
                        "connected",
                        "food web",
                        "food chain",
                        "depend on each other",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="ECO-C-02",

            prompt=(
                "Why can introducing "
                "a new predator change "
                "an ecosystem?"
            ),

            difficulty=C,

            required_ideas=(

                ScienceIdea(
                    code="PREY_CHANGE",
                    label=(
                        "prey populations "
                        "may decrease"
                    ),
                    alternatives=(
                        "prey decrease",
                        "fewer prey",
                        "prey population falls",
                    ),
                ),

                ScienceIdea(
                    code="CHAIN_EFFECT",
                    label=(
                        "other populations "
                        "can also change"
                    ),
                    alternatives=(
                        "other populations change",
                        "food web changes",
                        "affects other species",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),
    ),


    # ==================================================
    # AGE 12 — PHOTOSYNTHESIS
    # ==================================================

    "SCI_BIO_PHOTO_01": (

        ScienceQuestion(
            question_id="PHOTO-E-01",

            prompt=(
                "What does a plant need "
                "for photosynthesis, and "
                "what does it make?"
            ),

            difficulty=E,

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
                    code="CO2",
                    label="carbon dioxide",
                    alternatives=(
                        "carbon dioxide",
                        "co2",
                    ),
                ),

                ScienceIdea(
                    code="GLUCOSE",
                    label="glucose or food",
                    alternatives=(
                        "glucose",
                        "sugar",
                        "make food",
                        "makes food",
                        "produce food",
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
                        "food from soil",
                        "get food from soil",
                        "gets food from soil",
                        "get their food from soil",
                        "plants get their food from soil",
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


        ScienceQuestion(
            question_id="PHOTO-E-02",

            prompt=(
                "Why is sunlight "
                "important for "
                "photosynthesis?"
            ),

            difficulty=E,

            required_ideas=(

                ScienceIdea(
                    code="ENERGY",
                    label=(
                        "sunlight provides energy"
                    ),
                    alternatives=(
                        "provides energy",
                        "light energy",
                        "energy from sunlight",
                    ),
                ),

                ScienceIdea(
                    code="FOOD",
                    label=(
                        "energy helps make "
                        "glucose or food"
                    ),
                    alternatives=(
                        "make glucose",
                        "make food",
                        "produce glucose",
                        "produce food",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="PHOTO-M-01",

            prompt=(
                "What roles do water "
                "and carbon dioxide play "
                "in photosynthesis?"
            ),

            difficulty=M,

            required_ideas=(

                ScienceIdea(
                    code="WATER_INPUT",
                    label="water is an input",
                    alternatives=(
                        "water is used",
                        "uses water",
                        "water",
                    ),
                ),

                ScienceIdea(
                    code="CO2_INPUT",
                    label=(
                        "carbon dioxide "
                        "is an input"
                    ),
                    alternatives=(
                        "carbon dioxide is used",
                        "uses carbon dioxide",
                        "co2",
                    ),
                ),

                ScienceIdea(
                    code="GLUCOSE_OUTPUT",
                    label=(
                        "used to produce glucose"
                    ),
                    alternatives=(
                        "make glucose",
                        "produce glucose",
                        "make food",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="PHOTO-M-02",

            prompt=(
                "Why is chlorophyll "
                "important in green plants?"
            ),

            difficulty=M,

            required_ideas=(

                ScienceIdea(
                    code="ABSORB_LIGHT",
                    label=(
                        "chlorophyll absorbs light"
                    ),
                    alternatives=(
                        "absorbs light",
                        "absorbs sunlight",
                        "captures light",
                    ),
                ),

                ScienceIdea(
                    code="PHOTOSYNTHESIS",
                    label=(
                        "light supports "
                        "photosynthesis"
                    ),
                    alternatives=(
                        "photosynthesis",
                        "make food",
                        "make glucose",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="PHOTO-C-01",

            prompt=(
                "What might happen to "
                "photosynthesis if a "
                "plant receives very "
                "little light?"
            ),

            difficulty=C,

            required_ideas=(

                ScienceIdea(
                    code="LESS_LIGHT",
                    label=(
                        "less light energy "
                        "is available"
                    ),
                    alternatives=(
                        "less light",
                        "less light energy",
                        "not enough sunlight",
                    ),
                ),

                ScienceIdea(
                    code="LESS_PHOTO",
                    label=(
                        "photosynthesis slows"
                    ),
                    alternatives=(
                        "photosynthesis slows",
                        "less photosynthesis",
                        "lower photosynthesis",
                    ),
                ),

                ScienceIdea(
                    code="LESS_GLUCOSE",
                    label=(
                        "less glucose or "
                        "food is produced"
                    ),
                    alternatives=(
                        "less glucose",
                        "less food",
                        "makes less food",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="PHOTO-C-02",

            prompt=(
                "Why is photosynthesis "
                "important to both plants "
                "and animals?"
            ),

            difficulty=C,

            required_ideas=(

                ScienceIdea(
                    code="PLANT_FOOD",
                    label=(
                        "plants produce glucose"
                    ),
                    alternatives=(
                        "plants make food",
                        "plants make glucose",
                        "produce glucose",
                    ),
                ),

                ScienceIdea(
                    code="OXYGEN",
                    label=(
                        "oxygen is released"
                    ),
                    alternatives=(
                        "oxygen is released",
                        "releases oxygen",
                        "oxygen",
                    ),
                ),

                ScienceIdea(
                    code="FOOD_CHAIN",
                    label=(
                        "plants support "
                        "food chains"
                    ),
                    alternatives=(
                        "food chain",
                        "animals eat plants",
                        "energy for animals",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),
    ),


    # ==================================================
    # AGE 13 — ENERGY TRANSFER
    # ==================================================

    "SCI_ENERGY_TRANSFER_01": (

        ScienceQuestion(
            question_id="ENERGY-E-01",

            prompt=(
                "What does energy "
                "transfer mean?"
            ),

            difficulty=E,

            required_ideas=(

                ScienceIdea(
                    code="MOVE",
                    label=(
                        "energy moves from "
                        "one object or system "
                        "to another"
                    ),
                    alternatives=(
                        "energy moves",
                        "energy passes",
                        "energy transferred",
                        "transfer of energy",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="ENERGY-E-02",

            prompt=(
                "Give one example "
                "of energy transfer."
            ),

            difficulty=E,

            required_ideas=(

                ScienceIdea(
                    code="EXAMPLE",
                    label=(
                        "valid energy-transfer "
                        "example"
                    ),
                    alternatives=(
                        "sun to plant",
                        "sunlight to plant",
                        "food to animal",
                        "heat from",
                        "electricity",
                        "light energy",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="ENERGY-M-01",

            prompt=(
                "How does energy move "
                "from the Sun to an "
                "animal through a plant?"
            ),

            difficulty=M,

            required_ideas=(

                ScienceIdea(
                    code="SUN",
                    label=(
                        "energy begins "
                        "with sunlight"
                    ),
                    alternatives=(
                        "sun",
                        "sunlight",
                        "solar energy",
                    ),
                ),

                ScienceIdea(
                    code="PLANT",
                    label=(
                        "plant captures "
                        "light energy"
                    ),
                    alternatives=(
                        "plant captures",
                        "photosynthesis",
                        "plant stores energy",
                    ),
                ),

                ScienceIdea(
                    code="ANIMAL",
                    label=(
                        "animal gains energy "
                        "by eating"
                    ),
                    alternatives=(
                        "animal eats plant",
                        "eats the plant",
                        "consumer eats",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="ENERGY-M-02",

            prompt=(
                "How can electrical "
                "energy change in "
                "a light bulb?"
            ),

            difficulty=M,

            required_ideas=(

                ScienceIdea(
                    code="ELECTRICAL",
                    label="electrical energy",
                    alternatives=(
                        "electrical energy",
                        "electricity",
                    ),
                ),

                ScienceIdea(
                    code="LIGHT",
                    label="light energy",
                    alternatives=(
                        "light",
                        "light energy",
                    ),
                ),

                ScienceIdea(
                    code="HEAT",
                    label="thermal energy",
                    alternatives=(
                        "heat",
                        "thermal energy",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="ENERGY-C-01",

            prompt=(
                "Why is less usable "
                "energy available at "
                "higher levels of "
                "a food chain?"
            ),

            difficulty=C,

            required_ideas=(

                ScienceIdea(
                    code="USED",
                    label=(
                        "organisms use energy"
                    ),
                    alternatives=(
                        "use energy",
                        "energy is used",
                        "life processes",
                    ),
                ),

                ScienceIdea(
                    code="HEAT",
                    label=(
                        "some energy is "
                        "released as heat"
                    ),
                    alternatives=(
                        "heat",
                        "lost as heat",
                        "released as heat",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="ENERGY-C-02",

            prompt=(
                "Why can energy change "
                "form while the total "
                "energy is still conserved?"
            ),

            difficulty=C,

            required_ideas=(

                ScienceIdea(
                    code="CHANGE_FORM",
                    label=(
                        "energy changes form"
                    ),
                    alternatives=(
                        "changes form",
                        "different form",
                        "transformed",
                    ),
                ),

                ScienceIdea(
                    code="NOT_CREATED",
                    label=(
                        "energy is not "
                        "created or destroyed"
                    ),
                    alternatives=(
                        "not created or destroyed",
                        "cannot be created",
                        "cannot be destroyed",
                        "energy conserved",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),
    ),


    # ==================================================
    # AGE 14 — CELLS & BIOLOGICAL SYSTEMS
    # ==================================================

    "SCI_CELL_SYSTEMS_01": (

        ScienceQuestion(
            question_id="CELL-E-01",

            prompt=(
                "What is a cell?"
            ),

            difficulty=E,

            required_ideas=(

                ScienceIdea(
                    code="BASIC_UNIT",
                    label=(
                        "basic unit of life"
                    ),
                    alternatives=(
                        "basic unit of life",
                        "smallest unit of life",
                        "unit of living things",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="CELL-E-02",

            prompt=(
                "What is a tissue?"
            ),

            difficulty=E,

            required_ideas=(

                ScienceIdea(
                    code="GROUP_CELLS",
                    label=(
                        "group of similar "
                        "cells working together"
                    ),
                    alternatives=(
                        "group of cells",
                        "similar cells",
                        "cells working together",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        ScienceQuestion(
            question_id="CELL-M-01",

            prompt=(
                "How are cells, tissues "
                "and organs related?"
            ),

            difficulty=M,

            required_ideas=(

                ScienceIdea(
                    code="CELL_TISSUE",
                    label=(
                        "cells form tissues"
                    ),
                    alternatives=(
                        "cells form tissues",
                        "cells make tissues",
                    ),
                ),

                ScienceIdea(
                    code="TISSUE_ORGAN",
                    label=(
                        "tissues form organs"
                    ),
                    alternatives=(
                        "tissues form organs",
                        "tissues make organs",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="CELL-M-02",

            prompt=(
                "What is the difference "
                "between an organ and "
                "an organ system?"
            ),

            difficulty=M,

            required_ideas=(

                ScienceIdea(
                    code="ORGAN",
                    label=(
                        "organ contains "
                        "different tissues"
                    ),
                    alternatives=(
                        "organ has tissues",
                        "organ contains tissues",
                        "made of tissues",
                    ),
                ),

                ScienceIdea(
                    code="SYSTEM",
                    label=(
                        "organ system contains "
                        "organs working together"
                    ),
                    alternatives=(
                        "organs working together",
                        "group of organs",
                        "organ system",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="CELL-C-01",

            prompt=(
                "Why do multicellular "
                "organisms need different "
                "specialized cells?"
            ),

            difficulty=C,

            required_ideas=(

                ScienceIdea(
                    code="SPECIALIZED",
                    label=(
                        "different cells have "
                        "different functions"
                    ),
                    alternatives=(
                        "different functions",
                        "different jobs",
                        "specialized jobs",
                    ),
                ),

                ScienceIdea(
                    code="WORK_TOGETHER",
                    label=(
                        "cells work together"
                    ),
                    alternatives=(
                        "work together",
                        "cooperate",
                        "form tissues",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        ScienceQuestion(
            question_id="CELL-C-02",

            prompt=(
                "How can damage to one "
                "organ affect an entire "
                "organ system?"
            ),

            difficulty=C,

            required_ideas=(

                ScienceIdea(
                    code="CONNECTED",
                    label=(
                        "organs work together"
                    ),
                    alternatives=(
                        "organs work together",
                        "connected",
                        "depend on each other",
                    ),
                ),

                ScienceIdea(
                    code="SYSTEM_FUNCTION",
                    label=(
                        "system function "
                        "can be disrupted"
                    ),
                    alternatives=(
                        "system cannot work properly",
                        "system function",
                        "affects whole system",
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
        SCIENCE_QUESTION_BANK.get(
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


    if (
        difficulty is not None
    ):

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


    return questions[
        index
    ]
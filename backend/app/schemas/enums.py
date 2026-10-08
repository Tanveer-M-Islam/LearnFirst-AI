from enum import Enum


class AgeGroup(str, Enum):
    FOUNDATION = "FOUNDATION"
    DEVELOPING = "DEVELOPING"
    INDEPENDENT = "INDEPENDENT"


class Subject(str, Enum):
    MATH = "MATH"
    ENGLISH = "ENGLISH"
    SCIENCE = "SCIENCE"
    GENERAL = "GENERAL"


class LearningMode(str, Enum):
    LEARN = "LEARN"
    HOMEWORK_HELP = "HOMEWORK_HELP"
    PRACTICE = "PRACTICE"
    MOCK_TEST = "MOCK_TEST"
    VOICE = "VOICE"


class AttemptStatus(str, Enum):
    CORRECT = "CORRECT"
    PARTIALLY_CORRECT = "PARTIALLY_CORRECT"
    INCORRECT = "INCORRECT"
    INCOMPLETE = "INCOMPLETE"
    UNCLEAR = "UNCLEAR"


class MasteryState(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    LEARNING = "LEARNING"
    DEVELOPING = "DEVELOPING"
    STRONG = "STRONG"


class SessionStatus(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"
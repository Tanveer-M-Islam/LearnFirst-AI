export interface MathTopicDefinition {

  conceptCode:
    string;

  title:
    string;

  shortTitle:
    string;

  description:
    string;

  recommendedAge:
    number;

  sampleProblems:
    string[];

  assessmentQuestionLabel:
    string;

  answerPlaceholder:
    string;

  answerHelp:
    string;
}


export const DEFAULT_MATH_CONCEPT_CODE =
  "MATH_ALG_LINEAR_01";


export const MATH_TOPICS:
  MathTopicDefinition[] = [

  {
    conceptCode:
      "MATH_ARITH_BASIC_01",

    title:
      "Basic Arithmetic",

    shortTitle:
      "Arithmetic",

    description:
      (
        "Build addition and "
        + "subtraction confidence."
      ),

    recommendedAge:
      7,

    sampleProblems: [
      "27 + 16",
      "42 - 19",
      "35 + 28",
    ],

    assessmentQuestionLabel:
      "Calculate the result",

    answerPlaceholder:
      "Example: 43",

    answerHelp:
      (
        "Enter the final "
        + "numerical answer."
      ),
  },


  {
    conceptCode:
      "MATH_ARITH_MULTDIV_01",

    title:
      "Multiplication and Division",

    shortTitle:
      "Multiply & Divide",

    description:
      (
        "Develop multiplication "
        + "and division fluency."
      ),

    recommendedAge:
      8,

    sampleProblems: [
      "6 * 7",
      "48 / 6",
      "9 * 5",
    ],

    assessmentQuestionLabel:
      "Calculate the result",

    answerPlaceholder:
      "Example: 42",

    answerHelp:
      (
        "Enter the final "
        + "numerical answer."
      ),
  },


  {
    conceptCode:
      "MATH_ARITH_FRAC_01",

    title:
      "Fractions",

    shortTitle:
      "Fractions",

    description:
      (
        "Understand and calculate "
        + "with fractions."
      ),

    recommendedAge:
      9,

    sampleProblems: [
      "1/2 + 1/4",
      "3/4 - 1/2",
      "3/5 * 10",
    ],

    assessmentQuestionLabel:
      "Calculate the fraction",

    answerPlaceholder:
      "Example: 3/4",

    answerHelp:
      (
        "A fraction or equivalent "
        + "decimal is accepted."
      ),
  },


  {
    conceptCode:
      "MATH_ARITH_INT_01",

    title:
      "Integers",

    shortTitle:
      "Integers",

    description:
      (
        "Work with positive and "
        + "negative numbers."
      ),

    recommendedAge:
      10,

    sampleProblems: [
      "-8 + 13",
      "6 - 14",
      "-4 * 5 + 27",
    ],

    assessmentQuestionLabel:
      "Calculate the result",

    answerPlaceholder:
      "Example: -5",

    answerHelp:
      (
        "Include the negative sign "
        + "when required."
      ),
  },


  {
    conceptCode:
      "MATH_ARITH_ORDER_01",

    title:
      "Order of Operations",

    shortTitle:
      "Operations",

    description:
      (
        "Use the correct order "
        + "when evaluating expressions."
      ),

    recommendedAge:
      11,

    sampleProblems: [
      "3 + 4 * 2",
      "(8 + 4) / 3",
      "18 - 2 * 5",
    ],

    assessmentQuestionLabel:
      "Calculate the expression",

    answerPlaceholder:
      "Example: 11",

    answerHelp:
      (
        "Follow the correct order "
        + "of operations."
      ),
  },


  {
    conceptCode:
      "MATH_PREALG_EXPR_01",

    title:
      "Pre-Algebra Expressions",

    shortTitle:
      "Pre-Algebra",

    description:
      (
        "Evaluate expressions by "
        + "substituting values for x."
      ),

    recommendedAge:
      12,

    sampleProblems: [
      "3x + 2 when x = 4",
      "5x - 7 when x = 3",
      "2(x + 3) when x = 5",
    ],

    assessmentQuestionLabel:
      "Evaluate the expression",

    answerPlaceholder:
      "Example: 14",

    answerHelp:
      (
        "Replace x with the given "
        + "value and calculate."
      ),
  },


  {
    conceptCode:
      "MATH_ALG_LINEAR_01",

    title:
      "Linear Equations",

    shortTitle:
      "Equations",

    description:
      (
        "Solve one-variable "
        + "linear equations."
      ),

    recommendedAge:
      13,

    sampleProblems: [
      "3x + 6 = 18",
      "2x + 3 = 11",
      "4x - 5 = 19",
    ],

    assessmentQuestionLabel:
      "Solve for x",

    answerPlaceholder:
      "Example: x = 4",

    answerHelp:
      (
        "Write the final value "
        + "of x clearly."
      ),
  },


  {
    conceptCode:
      "MATH_GRAPH_LINEAR_01",

    title:
      "Linear Graphs",

    shortTitle:
      "Linear Graphs",

    description:
      (
        "Connect x-values and "
        + "y-values in linear "
        + "relationships."
      ),

    recommendedAge:
      14,

    sampleProblems: [
      "y = 2x + 3 when x = 4",
      "y = 3x - 2 when x = 5",
      "y = -x + 6 when x = 2",
    ],

    assessmentQuestionLabel:
      "Find the y-value",

    answerPlaceholder:
      "Example: 11",

    answerHelp:
      (
        "Substitute the given x-value "
        + "into the linear rule."
      ),
  },
];


export function getMathTopic(
  conceptCode:
    string | null | undefined,
): MathTopicDefinition {

  return (
    MATH_TOPICS.find(
      (
        topic,
      ) =>
        topic.conceptCode
        === conceptCode,
    )

    ?? MATH_TOPICS.find(
      (
        topic,
      ) =>
        topic.conceptCode
        === DEFAULT_MATH_CONCEPT_CODE,
    )!
  );
}


export function getRecommendedMathTopicForAge(
  age:
    number,
): MathTopicDefinition {

  return (
    MATH_TOPICS.find(
      (
        topic,
      ) =>
        topic.recommendedAge
        === age,
    )

    ?? MATH_TOPICS[
      MATH_TOPICS.length - 1
    ]
  );
}
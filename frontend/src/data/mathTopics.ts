export interface MathTopicDefinition {
  conceptCode: string;

  title: string;

  shortTitle: string;

  description: string;

  sampleProblems: string[];

  assessmentQuestionLabel: string;

  answerPlaceholder: string;

  answerHelp: string;
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
        "Practice addition, subtraction, "
        + "multiplication and division."
      ),

    sampleProblems: [
      "24 + 18",
      "56 - 29",
      "7 * 6",
    ],

    assessmentQuestionLabel:
      "Calculate the result",

    answerPlaceholder:
      "Example: 42",

    answerHelp:
      (
        "Enter the final numerical "
        + "answer."
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
        + "negative whole numbers."
      ),

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
        + "when the answer is negative."
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
        "Practice adding, subtracting, "
        + "multiplying and dividing "
        + "fractions."
      ),

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
        "You can enter a fraction "
        + "such as 3/4 or an "
        + "equivalent decimal."
      ),
  },


  {
    conceptCode:
      "MATH_ARITH_ORDER_01",

    title:
      "Order of Operations",

    shortTitle:
      "Order of Operations",

    description:
      (
        "Practice expressions using "
        + "parentheses and operation "
        + "priority."
      ),

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
        + "of operations and enter "
        + "the final value."
      ),
  },


  {
    conceptCode:
      "MATH_ALG_LINEAR_01",

    title:
      "Linear Equations",

    shortTitle:
      "Linear Equations",

    description:
      (
        "Solve equations with one "
        + "unknown variable step "
        + "by step."
      ),

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
        "Write your final answer "
        + "clearly, for example x = 4."
      ),
  },
];


export function getMathTopic(
  conceptCode:
    string | null | undefined,
): MathTopicDefinition {

  return (
    MATH_TOPICS.find(
      (topic) =>
        topic.conceptCode
        === conceptCode,
    )

    ?? MATH_TOPICS.find(
      (topic) =>
        topic.conceptCode
        === DEFAULT_MATH_CONCEPT_CODE,
    )!
  );
}
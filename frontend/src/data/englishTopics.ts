export interface EnglishTopicDefinition {
  conceptCode: string;

  title: string;

  description: string;

  recommendedAge: number;
}


export const ENGLISH_TOPICS:
  EnglishTopicDefinition[] = [

  {
    conceptCode:
      "ENG_VOCAB_FOUND_01",

    title:
      "Everyday Vocabulary",

    description:
      "Build useful everyday English vocabulary.",

    recommendedAge:
      7,
  },

  {
    conceptCode:
      "ENG_SENT_SIMPLE_01",

    title:
      "Simple Sentences",

    description:
      "Learn to build clear and complete simple sentences.",

    recommendedAge:
      8,
  },

  {
    conceptCode:
      "ENG_GRAMMAR_POS_01",

    title:
      "Parts of Speech",

    description:
      "Understand nouns, verbs and adjectives.",

    recommendedAge:
      9,
  },

  {
    conceptCode:
      "ENG_GRAMMAR_TENSE_01",

    title:
      "Core Tenses",

    description:
      "Practice present, past and future tense forms.",

    recommendedAge:
      10,
  },

  {
    conceptCode:
      "ENG_READ_CORE_01",

    title:
      "Reading Comprehension",

    description:
      "Understand main ideas and details in short passages.",

    recommendedAge:
      11,
  },

  {
    conceptCode:
      "ENG_SENT_STRUCTURE_01",

    title:
      "Sentence Structure",

    description:
      "Build clearer and more complex English sentences.",

    recommendedAge:
      12,
  },

  {
    conceptCode:
      "ENG_GRAMMAR_ADV_01",

    title:
      "Intermediate Grammar",

    description:
      "Use more advanced English grammar accurately.",

    recommendedAge:
      13,
  },

  {
    conceptCode:
      "ENG_READ_INFERENCE_01",

    title:
      "Reading and Inference",

    description:
      "Use evidence to understand deeper meaning in passages.",

    recommendedAge:
      14,
  },
];


export function getEnglishTopic(
  conceptCode:
    string | null | undefined,
): EnglishTopicDefinition {

  return (
    ENGLISH_TOPICS.find(
      (
        topic,
      ) =>
        topic.conceptCode
        === conceptCode,
    )

    ?? ENGLISH_TOPICS[0]
  );
}


export function getEnglishTopicForAge(
  age: number,
): EnglishTopicDefinition {

  const exact =
    ENGLISH_TOPICS.find(
      (
        topic,
      ) =>
        topic.recommendedAge
        === age,
    );


  if (
    exact
  ) {
    return exact;
  }


  if (
    age <= 7
  ) {
    return ENGLISH_TOPICS[0];
  }


  return (
    ENGLISH_TOPICS[
      ENGLISH_TOPICS.length - 1
    ]
  );
}
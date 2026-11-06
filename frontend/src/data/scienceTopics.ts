export interface ScienceTopicDefinition {
  conceptCode:
    string;

  title:
    string;

  description:
    string;

  recommendedAge:
    number;
}


export const SCIENCE_TOPICS:
  ScienceTopicDefinition[] = [

  {
    conceptCode:
      "SCI_LIFE_BASIC_01",

    title:
      "Living Things",

    description:
      (
        "Understand what living "
        + "things need and how "
        + "they grow and respond."
      ),

    recommendedAge:
      7,
  },


  {
    conceptCode:
      "SCI_MATERIAL_BASIC_01",

    title:
      "Everyday Materials",

    description:
      (
        "Explore common materials "
        + "and their useful "
        + "properties."
      ),

    recommendedAge:
      8,
  },


  {
    conceptCode:
      "SCI_PHY_MATTER_01",

    title:
      "States of Matter",

    description:
      (
        "Explore solids, liquids, "
        + "gases and state changes."
      ),

    recommendedAge:
      9,
  },


  {
    conceptCode:
      "SCI_BIO_FOODCHAIN_01",

    title:
      "Food Chains",

    description:
      (
        "Understand producers, "
        + "consumers and energy flow."
      ),

    recommendedAge:
      10,
  },


  {
    conceptCode:
      "SCI_ECO_SYSTEMS_01",

    title:
      "Ecosystems",

    description:
      (
        "Explore how organisms "
        + "interact with each other "
        + "and their environment."
      ),

    recommendedAge:
      11,
  },


  {
    conceptCode:
      "SCI_BIO_PHOTO_01",

    title:
      "Photosynthesis",

    description:
      (
        "Understand how plants use "
        + "light, water and carbon "
        + "dioxide to make glucose."
      ),

    recommendedAge:
      12,
  },


  {
    conceptCode:
      "SCI_ENERGY_TRANSFER_01",

    title:
      "Energy Transfer",

    description:
      (
        "Explore how energy moves "
        + "and changes between "
        + "systems."
      ),

    recommendedAge:
      13,
  },


  {
    conceptCode:
      "SCI_CELL_SYSTEMS_01",

    title:
      "Cells and Biological Systems",

    description:
      (
        "Understand cells, tissues, "
        + "organs and organ systems."
      ),

    recommendedAge:
      14,
  },
];


export const DEFAULT_SCIENCE_CONCEPT =
  "SCI_BIO_PHOTO_01";


export function getScienceTopic(
  conceptCode:
    string | null | undefined,
): ScienceTopicDefinition {

  return (
    SCIENCE_TOPICS.find(
      (
        topic,
      ) =>
        topic.conceptCode
        === conceptCode,
    )

    ?? SCIENCE_TOPICS[0]
  );
}


export function getScienceTopicForAge(
  age:
    number,
): ScienceTopicDefinition {

  const topic =
    SCIENCE_TOPICS.find(
      (
        item,
      ) =>
        item.recommendedAge
        === age,
    );


  if (
    topic
  ) {

    return topic;
  }


  if (
    age <= 7
  ) {

    return SCIENCE_TOPICS[0];
  }


  return (
    SCIENCE_TOPICS[
      SCIENCE_TOPICS.length - 1
    ]
  );
}
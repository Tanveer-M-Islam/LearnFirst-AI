export interface ScienceTopicDefinition {
  conceptCode: string;

  title: string;

  description: string;
}


export const SCIENCE_TOPICS:
  ScienceTopicDefinition[] = [

  {
    conceptCode:
      "SCI_BIO_PHOTO_01",

    title:
      "Photosynthesis",

    description:
      (
        "Learn how plants use "
        + "light, water and carbon "
        + "dioxide to make food."
      ),
  },


  {
    conceptCode:
      "SCI_PHY_MATTER_01",

    title:
      "States of Matter",

    description:
      (
        "Explore solids, liquids, "
        + "gases and changes "
        + "between states."
      ),
  },


  {
    conceptCode:
      "SCI_BIO_FOODCHAIN_01",

    title:
      "Food Chains",

    description:
      (
        "Understand producers, "
        + "consumers and how "
        + "energy moves."
      ),
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
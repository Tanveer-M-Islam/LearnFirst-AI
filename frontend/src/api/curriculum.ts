import {
  apiRequest,
} from "./client";

import type {
  CurriculumTopic,
} from "../types/curriculum";


export function getScienceTopics():
Promise<CurriculumTopic[]> {
  return apiRequest<
    CurriculumTopic[]
  >(
    (
      "/curriculum/topics"
      + "?subject=SCIENCE"
      + "&curriculum_profile="
      + "bangladesh_english_v1"
    ),
  );
}
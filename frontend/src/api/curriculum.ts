import {
  apiRequest,
} from "./client";

import type {
  CurriculumTopic,
  StudentCurriculumPath,
} from "../types/curriculum";

import type {
  Subject,
} from "../types/session";


export function getScienceTopics():
Promise<CurriculumTopic[]> {

  return (
    apiRequest<
      CurriculumTopic[]
    >(
      (
        "/curriculum/topics"
        + "?subject=SCIENCE"
        + "&curriculum_profile="
        + "bangladesh_english_v1"
      ),
    )
  );
}


export function getStudentCurriculumPath(
  studentId:
    string,

  subject:
    Subject,
): Promise<
  StudentCurriculumPath
> {

  return (
    apiRequest<
      StudentCurriculumPath
    >(
      (
        `/curriculum/students/${studentId}`
        + `/path?subject=${subject}`
      ),
    )
  );
}
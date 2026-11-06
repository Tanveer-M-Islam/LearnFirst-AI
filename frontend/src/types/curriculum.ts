import type {
  AgeGroup,
} from "./student";

import type {
  MasteryState,
  Subject,
} from "./session";


export interface CurriculumTopic {
  source_id:
    string;

  title:
    string;

  subject:
    string;

  concept_code:
    string;

  grade_band:
    string;

  curriculum_profile:
    string;
}


export type CurriculumConceptStatus =
  | "PLANNED"
  | "FUTURE"
  | "READY"
  | "IN_PROGRESS"
  | "NEEDS_REVIEW"
  | "MASTERED";


export interface CurriculumPathConcept {
  concept_code:
    string;

  subject:
    Subject;

  title:
    string;

  description:
    string;

  recommended_age:
    number;

  min_age:
    number;

  max_age:
    number;

  min_grade:
    number;

  max_grade:
    number;

  sequence_order:
    number;

  prerequisites:
    string[];

  implemented:
    boolean;

  curriculum_profile:
    string;

  mastery_state:
    MasteryState;

  mastery_score:
    number | null;

  status:
    CurriculumConceptStatus;

  age_appropriate:
    boolean;

  grade_appropriate:
    boolean | null;
}


export interface StudentCurriculumPath {
  student_id:
    string;

  subject:
    Subject;

  learner_age:
    number;

  learner_grade:
    string;

  age_group:
    AgeGroup;

  selection_policy:
    string;

  target_concept:
    CurriculumPathConcept | null;

  recommended_concept:
    CurriculumPathConcept | null;

  prerequisite_review_concept:
    CurriculumPathConcept | null;

  reason_codes:
    string[];

  concepts:
    CurriculumPathConcept[];
}
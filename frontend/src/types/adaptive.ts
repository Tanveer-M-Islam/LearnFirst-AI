import type {
  MasteryState,
} from "./session";

import type {
  AgeGroup,
} from "./student";

import type {
  DifficultyLevel,
} from "./assessment";


export type AdaptiveActivity =
  | "TAKE_DIAGNOSTIC"
  | "GUIDED_PRACTICE"
  | "INDEPENDENT_PRACTICE"
  | "REVIEW_FOUNDATION"
  | "TAKE_MASTERY_CHECK"
  | "CHALLENGE_PRACTICE";


export type AdaptiveSupport =
  | "GENTLE"
  | "GUIDED"
  | "STRONG";


export type ExplanationDepth =
  | "SIMPLE"
  | "BALANCED"
  | "DEEP";


export interface AdaptiveProblem {
  problem_id: string;

  prompt: string;

  difficulty: DifficultyLevel;
}


export interface AdaptivePlan {
  student_id: string;

  concept_code: string;

  age_group: AgeGroup;

  mastery_state: MasteryState;

  difficulty: DifficultyLevel;

  support_level: AdaptiveSupport;

  explanation_depth:
    ExplanationDepth;

  next_activity:
    AdaptiveActivity;

  latest_score_percent:
    number | null;

  independent_attempt_rate:
    number;

  independent_success_rate:
    number;

  average_hint_level:
    number;

  direct_answer_requests:
    number;

  retry_success_count:
    number;

  reason_codes: string[];

  summary: string;

  next_problem:
    AdaptiveProblem | null;
}
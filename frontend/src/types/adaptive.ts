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


export type ResponsePace =
  | "INSUFFICIENT_DATA"
  | "FAST"
  | "TYPICAL"
  | "SLOW";


export type ResponsePaceSource =
  | "PERSONAL_BASELINE"
  | "AGE_GROUP_FALLBACK"
  | "INSUFFICIENT_DATA";


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


  measured_response_count:
    number;

  average_response_latency_ms:
    number | null;

  response_pace:
    ResponsePace;


  baseline_ready:
    boolean;

  baseline_sample_count:
    number;

  recent_sample_count:
    number;

  baseline_response_latency_ms:
    number | null;

  recent_response_latency_ms:
    number | null;

  latency_change_percent:
    number | null;

  response_pace_source:
    ResponsePaceSource;


  reason_codes: string[];

  summary: string;

  next_problem:
    AdaptiveProblem | null;
}
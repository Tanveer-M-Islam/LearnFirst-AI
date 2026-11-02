import type {
  AdaptiveSupport,
  ExplanationDepth,
  ResponsePace,
  ResponsePaceSource,
} from "./adaptive";

import type {
  DifficultyLevel,
  MasteryState,
} from "./assessment";

import type {
  AgeGroup,
} from "./student";


export type ScienceAdaptiveActivity =
  | "START_LEARNING"
  | "GUIDED_QUESTION"
  | "INDEPENDENT_QUESTION"
  | "REVIEW_CONCEPT"
  | "CHALLENGE_QUESTION";


export interface ScienceAdaptiveQuestion {
  question_id: string;

  prompt: string;

  difficulty:
    DifficultyLevel;
}


export interface ScienceAdaptivePlan {
  student_id: string;

  concept_code: string;

  age_group:
    AgeGroup;

  mastery_state:
    MasteryState;

  mastery_explanation:
    string;

  difficulty:
    DifficultyLevel;

  support_level:
    AdaptiveSupport;

  explanation_depth:
    ExplanationDepth;

  next_activity:
    ScienceAdaptiveActivity;


  understanding_score_percent:
    number;

  total_attempts:
    number;

  correct_attempts:
    number;

  partial_attempts:
    number;

  independent_attempts:
    number;

  misconception_count:
    number;

  independent_attempt_rate:
    number;

  independent_success_rate:
    number;

  average_hint_level:
    number;

  direct_answer_requests:
    number;


  measured_response_count:
    number;

  average_response_latency_ms:
    number | null;

  response_pace:
    ResponsePace;


  baseline_ready:
    boolean;

  baseline_response_latency_ms:
    number | null;

  recent_response_latency_ms:
    number | null;

  latency_change_percent:
    number | null;

  response_pace_source:
    ResponsePaceSource;


  reason_codes:
    string[];

  summary:
    string;

  next_question:
    ScienceAdaptiveQuestion
    | null;
}
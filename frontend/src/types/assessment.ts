export type AssessmentType =
  | "DIAGNOSTIC"
  | "MASTERY";


export type AssessmentStatus =
  | "IN_PROGRESS"
  | "COMPLETED";


export type DifficultyLevel =
  | "EASY"
  | "MODERATE"
  | "CHALLENGING";


export type MasteryState =
  | "NOT_STARTED"
  | "LEARNING"
  | "DEVELOPING"
  | "STRONG";


export interface AssessmentStartPayload {
  student_id: string;

  session_id?: string | null;

  subject: "MATH";

  concept_code: string;

  assessment_type:
    AssessmentType;
}


export interface AssessmentQuestion {
  question_id: string;

  prompt: string;

  difficulty:
    DifficultyLevel;

  bloom_level: string;
}


export interface AssessmentStartResponse {
  assessment_id: string;

  student_id: string;

  session_id:
    string | null;

  subject: "MATH";

  concept_code: string;

  assessment_type:
    AssessmentType;

  status:
    AssessmentStatus;

  total_questions: number;

  questions:
    AssessmentQuestion[];
}


export interface AssessmentAnswerInput {
  question_id: string;

  response: string;
}


export interface AssessmentAnswerResult {
  question_id: string;

  status: string;

  is_correct: boolean;

  misconception_code:
    string | null;
}


export interface AssessmentResult {
  assessment_id: string;

  assessment_type:
    AssessmentType;

  concept_code: string;

  correct_answers: number;

  total_questions: number;

  score_percent: number;

  mastery_state:
    MasteryState;

  recommended_difficulty:
    DifficultyLevel;

  baseline_score_percent:
    number | null;

  score_gain_percentage_points:
    number | null;

  improved:
    boolean | null;

  answers:
    AssessmentAnswerResult[];
}


export interface AssessmentScoreSnapshot {
  assessment_id: string;

  score_percent: number;

  correct_answers: number;

  total_questions: number;
}


export interface LearningIndependenceMetrics {
  total_attempts: number;

  correct_attempts: number;

  independent_attempts: number;

  independent_correct_attempts:
    number;

  independent_attempt_rate:
    number;

  independent_success_rate:
    number;

  average_hint_level: number;

  direct_answer_requests:
    number;

  retry_success_count: number;
}


export interface ConceptProgress {
  student_id: string;

  concept_code: string;

  diagnostic:
    AssessmentScoreSnapshot
    | null;

  mastery:
    AssessmentScoreSnapshot
    | null;

  score_gain_percentage_points:
    number | null;

  current_mastery_state:
    MasteryState;

  recommended_difficulty:
    DifficultyLevel;

  learning_metrics:
    LearningIndependenceMetrics;
}
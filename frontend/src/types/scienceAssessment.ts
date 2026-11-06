import type {
  AssessmentStatus,
  AssessmentType,
  DifficultyLevel,
  MasteryState,
} from "./assessment";


export interface ScienceAssessmentStartPayload {
  student_id: string;

  session_id?:
    string | null;

  concept_code: string;

  assessment_type:
    AssessmentType;
}


export interface ScienceAssessmentQuestion {
  question_id: string;

  prompt: string;

  difficulty:
    DifficultyLevel;
}


export interface ScienceAssessmentStartResponse {
  assessment_id: string;

  student_id: string;

  session_id:
    string | null;

  concept_code: string;

  assessment_type:
    AssessmentType;

  status:
    AssessmentStatus;

  total_questions: number;

  questions:
    ScienceAssessmentQuestion[];
}


export interface ScienceAssessmentAnswerInput {
  question_id: string;

  response: string;
}


export interface ScienceAssessmentAnswerResult {
  question_id: string;

  status: string;

  is_correct: boolean;

  coverage_score: number;

  misconception_code:
    string | null;
}


export interface ScienceAssessmentResult {
  assessment_id: string;

  assessment_type:
    AssessmentType;

  concept_code: string;

  correct_answers: number;

  partial_answers: number;

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
    ScienceAssessmentAnswerResult[];
}


export interface ScienceAssessmentSnapshot {
  assessment_id: string;

  score_percent: number;

  correct_answers: number;

  total_questions: number;
}


export interface ScienceAssessmentProgress {
  student_id: string;

  concept_code: string;

  diagnostic:
    ScienceAssessmentSnapshot
    | null;

  mastery:
    ScienceAssessmentSnapshot
    | null;

  score_gain_percentage_points:
    number | null;

  assessment_mastery_state:
    MasteryState;
}
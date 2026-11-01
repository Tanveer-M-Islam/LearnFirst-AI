export type LearningMode =
  | "LEARN"
  | "HOMEWORK_HELP"
  | "PRACTICE"
  | "MOCK_TEST"
  | "VOICE";


export type Subject =
  | "MATH"
  | "ENGLISH"
  | "SCIENCE"
  | "GENERAL";


export type MasteryState =
  | "NOT_STARTED"
  | "LEARNING"
  | "DEVELOPING"
  | "STRONG";


export type SessionStatus =
  | "ACTIVE"
  | "COMPLETED"
  | "ABANDONED";


export interface LearningSessionCreate {
  student_id: string;
  mode: LearningMode;
  subject: Subject;
  topic?: string | null;
  concept_code?: string | null;
  current_problem?: string | null;
}


export interface LearningSession {
  id: string;
  student_id: string;

  mode: LearningMode;
  subject: Subject;

  topic: string | null;
  concept_code: string | null;

  current_problem: string | null;

  current_hint_level: number;
  attempt_count: number;
  direct_answer_requests: number;

  current_misconception:
    string | null;

  mastery_state: MasteryState;

  last_tutor_action:
    string | null;

  status: SessionStatus;

  started_at: string;
  ended_at: string | null;
  updated_at: string;
}
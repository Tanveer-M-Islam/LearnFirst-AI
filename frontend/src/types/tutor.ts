import type {
  LearningMode,
  Subject,
} from "./session";

import type {
  AgeGroup,
} from "./student";


export type AttemptStatus =
  | "CORRECT"
  | "PARTIALLY_CORRECT"
  | "INCORRECT"
  | "INCOMPLETE"
  | "UNCLEAR";


export type MathProblemType =
  | "LINEAR_EQUATION"
  | "ARITHMETIC"
  | "UNSUPPORTED";


export type TutorIntent =
  | "LEARN_CONCEPT"
  | "HOMEWORK_REQUEST"
  | "STUDENT_ATTEMPT"
  | "HINT_REQUEST"
  | "DIRECT_ANSWER_REQUEST"
  | "EXPLANATION_REQUEST"
  | "PRACTICE_REQUEST"
  | "MOCK_TEST_RESPONSE"
  | "CONFUSION"
  | "I_DONT_KNOW"
  | "POLICY_BYPASS"
  | "OFF_TOPIC"
  | "SAFETY_SENSITIVE";


export type TutorAction =
  | "ASK_ATTEMPT"
  | "ASK_PRIOR_KNOWLEDGE"
  | "ASK_GUIDING_QUESTION"
  | "GIVE_HINT"
  | "GIVE_SIMILAR_EXAMPLE"
  | "BREAK_INTO_STEPS"
  | "GIVE_STRONG_GUIDANCE"
  | "GIVE_FULL_TEACHING_EXPLANATION"
  | "EVALUATE_ATTEMPT"
  | "ASK_RETRY"
  | "ASK_EXPLAIN_BACK"
  | "GIVE_MASTERY_QUESTION"
  | "GIVE_FEEDBACK"
  | "SWITCH_TO_PREREQUISITE"
  | "ESCALATE_SAFETY"
  | "REFUSE_POLICY_BYPASS"
  | "GENERATE_PRACTICE_QUESTION"
  | "RECORD_TEST_RESPONSE"
  | "CLARIFY_TEST_INSTRUCTION"
  | "REDIRECT_TO_LEARNING";


export interface TutorDecision {
  session_id: string;
  student_id: string;

  subject: Subject;
  mode: LearningMode;
  age_group: AgeGroup;

  intent: TutorIntent;
  next_action: TutorAction;

  hint_level: number;

  allow_final_answer: boolean;

  requires_rag: boolean;
  requires_validation: boolean;
  requires_mastery_check: boolean;

  policy_bypass_detected: boolean;

  reason: string;
}


export interface MathValidation {
  supported: boolean;

  problem_type: MathProblemType;

  status: AttemptStatus;

  is_correct: boolean;

  student_answer:
    string | null;

  correct_steps: string[];

  first_error_step:
    string | null;

  misconception_code:
    string | null;

  feedback_summary: string;
}


export interface TutorMessageResponse {
  session_id: string;

  student_message: string;

  detected_intent:
    TutorIntent;

  decision: TutorDecision;

  math_validation:
    MathValidation | null;

  reply: string;

  provider: string;
  model: string;

  latency_ms: number;
}


export type ChatRole =
  | "student"
  | "tutor";


export interface ChatMessage {
  id: string;

  role: ChatRole;

  text: string;

  validation?:
    MathValidation | null;

  decision?:
    TutorDecision | null;

  createdAt: number;
}
import {
  apiRequest,
} from "./client";


export interface EnglishProgress {
  student_id:
    string;

  concept_code:
    string;

  mastery_state:
    | "NOT_STARTED"
    | "LEARNING"
    | "DEVELOPING"
    | "STRONG";

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
}


export function getEnglishProgress(
  studentId: string,
  conceptCode: string,
): Promise<EnglishProgress> {

  return apiRequest<
    EnglishProgress
  >(
    (
      "/english/progress/students/"
      + studentId
      + "/concepts/"
      + conceptCode
    ),
  );
}
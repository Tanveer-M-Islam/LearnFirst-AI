
import { apiRequest } from "./client";

import type {
  AssessmentAnswerInput,
  AssessmentResult,
  AssessmentStartResponse,
  AssessmentType,
} from "../types/assessment";


export type EnglishAssessmentStartResponse =
  Omit<AssessmentStartResponse, "subject"> & {
    subject: "ENGLISH";
  };


export interface EnglishAssessmentStartPayload {
  student_id: string;
  session_id?: string | null;
  subject: "ENGLISH";
  concept_code: string;
  assessment_type: AssessmentType;
}


export function startEnglishAssessment(
  payload: EnglishAssessmentStartPayload,
): Promise<EnglishAssessmentStartResponse> {

  return apiRequest<EnglishAssessmentStartResponse>(
    "/english/assessments/start",
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );
}


export function submitEnglishAssessment(
  assessmentId: string,
  answers: AssessmentAnswerInput[],
): Promise<AssessmentResult> {

  return apiRequest<AssessmentResult>(
    `/english/assessments/${encodeURIComponent(assessmentId)}/submit`,
    {
      method: "POST",
      body: JSON.stringify({ answers }),
    },
  );
}

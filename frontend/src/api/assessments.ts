import {
  apiRequest,
} from "./client";

import type {
  AssessmentAnswerInput,
  AssessmentResult,
  AssessmentStartPayload,
  AssessmentStartResponse,
  ConceptProgress,
} from "../types/assessment";


export function startAssessment(
  payload:
    AssessmentStartPayload,
): Promise<
  AssessmentStartResponse
> {
  return apiRequest<
    AssessmentStartResponse
  >(
    "/assessments/start",
    {
      method: "POST",

      body:
        JSON.stringify(
          payload,
        ),
    },
  );
}


export function submitAssessment(
  assessmentId: string,
  answers:
    AssessmentAnswerInput[],
): Promise<AssessmentResult> {
  return apiRequest<
    AssessmentResult
  >(
    (
      `/assessments/`
      + `${assessmentId}/submit`
    ),
    {
      method: "POST",

      body:
        JSON.stringify({
          answers,
        }),
    },
  );
}


export function getConceptProgress(
  studentId: string,
  conceptCode: string,
): Promise<ConceptProgress> {
  return apiRequest<
    ConceptProgress
  >(
    (
      `/assessments/`
      + `students/${studentId}`
      + `/concepts/${conceptCode}`
      + "/progress"
    ),
  );
}
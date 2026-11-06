import {
  apiRequest,
} from "./client";

import type {
  ScienceAssessmentAnswerInput,
  ScienceAssessmentProgress,
  ScienceAssessmentResult,
  ScienceAssessmentStartPayload,
  ScienceAssessmentStartResponse,
} from "../types/scienceAssessment";


export function startScienceAssessment(
  payload:
    ScienceAssessmentStartPayload,
): Promise<
  ScienceAssessmentStartResponse
> {

  return apiRequest<
    ScienceAssessmentStartResponse
  >(
    "/science/assessments/start",

    {
      method:
        "POST",

      body:
        JSON.stringify(
          payload,
        ),
    },
  );
}


export function submitScienceAssessment(
  assessmentId: string,

  answers:
    ScienceAssessmentAnswerInput[],
): Promise<
  ScienceAssessmentResult
> {

  return apiRequest<
    ScienceAssessmentResult
  >(
    (
      "/science/assessments/"
      + assessmentId
      + "/submit"
    ),

    {
      method:
        "POST",

      body:
        JSON.stringify({
          answers,
        }),
    },
  );
}


export function getScienceAssessmentProgress(
  studentId: string,
  conceptCode: string,
): Promise<
  ScienceAssessmentProgress
> {

  return apiRequest<
    ScienceAssessmentProgress
  >(
    (
      "/science/assessments/"
      + `students/${studentId}`
      + `/concepts/${conceptCode}`
      + "/progress"
    ),
  );
}
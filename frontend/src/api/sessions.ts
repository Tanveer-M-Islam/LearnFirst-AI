import {
  apiRequest,
} from "./client";

import type {
  LearningSession,
  LearningSessionCreate,
} from "../types/session";


export function createLearningSession(
  payload: LearningSessionCreate,
): Promise<LearningSession> {
  return apiRequest<LearningSession>(
    "/sessions",
    {
      method: "POST",

      body:
        JSON.stringify(
          payload,
        ),
    },
  );
}


export function getLearningSession(
  sessionId: string,
): Promise<LearningSession> {
  return apiRequest<LearningSession>(
    `/sessions/${sessionId}`,
  );
}
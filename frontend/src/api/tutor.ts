import {
  apiRequest,
} from "./client";

import type {
  TutorMessageResponse,
} from "../types/tutor";


export function sendTutorMessage(
  sessionId: string,
  message: string,
): Promise<TutorMessageResponse> {
  return apiRequest<TutorMessageResponse>(
    (
      `/tutor/sessions/`
      + `${sessionId}/message`
    ),
    {
      method: "POST",

      body:
        JSON.stringify({
          message,
        }),
    },
  );
}
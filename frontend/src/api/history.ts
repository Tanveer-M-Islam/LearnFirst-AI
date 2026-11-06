
import {
  apiRequest,
} from "./client";

import type {
  SavedChatMessage,
  SessionHistorySummary,
} from "../types/history";


export async function getStudentChatHistory(
  studentId: string,
): Promise<SessionHistorySummary[]> {

  return apiRequest<SessionHistorySummary[]>(
    `/history/students/${encodeURIComponent(studentId)}/sessions`,
  );
}


export async function getSessionChatMessages(
  sessionId: string,
  studentId: string,
): Promise<SavedChatMessage[]> {

  const url =
    `/history/sessions/${encodeURIComponent(sessionId)}/messages`
    + `?student_id=${encodeURIComponent(studentId)}`;

  return apiRequest<SavedChatMessage[]>(url);
}

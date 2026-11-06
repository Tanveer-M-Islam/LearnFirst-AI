
import {
  getSessionChatMessages,
} from "../api/history";

import type {
  SavedChatMessage,
} from "../types/history";

import type {
  ChatMessage,
} from "../types/tutor";

import {
  getStoredStudent,
} from "./studentStorage";


function convertSavedMessage(
  saved: SavedChatMessage,
): ChatMessage {

  const response = saved.response_payload;

  // Handle SQLite timestamps without timezone information.

  const dateString =
    saved.created_at.endsWith("Z")
    || /[+-]\d{2}:\d{2}$/.test(saved.created_at)
      ? saved.created_at
      : `${saved.created_at}Z`;

  const parsedTime = Date.parse(dateString);

  return {
    id: String(saved.id),

    role:
      saved.role === "user"
        ? "student"
        : "tutor",

    text: saved.content,

    createdAt:
      Number.isNaN(parsedTime)
        ? Date.now()
        : parsedTime,

    validation:
      response?.math_validation ?? null,

    scienceValidation:
      response?.science_validation ?? null,

    englishValidation:
      response?.english_validation ?? null,

    decision:
      response?.decision ?? null,

    ragUsed:
      response?.rag_used ?? false,

    ragSources:
      response?.rag_sources ?? [],
  };
}


export async function loadSessionChatHistory(
  sessionId: string,
  sessionOwnerId: string,
): Promise<ChatMessage[]> {

  const student = getStoredStudent();

  // Verify the session belongs to the selected learner.
  // This is a UI check, not secure server authentication.

  if (!student) {
    throw new Error(
      "No active student found. Please log in again."
    );
  }

  if (student.id !== sessionOwnerId) {
    throw new Error(
      "This learning session belongs to another student."
    );
  }

  const savedMessages =
    await getSessionChatMessages(
      sessionId,
      student.id,
    );

  return savedMessages.map(convertSavedMessage);
}

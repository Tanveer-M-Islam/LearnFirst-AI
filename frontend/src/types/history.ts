
import type {
  TutorMessageResponse,
} from "./tutor";


export interface SavedChatMessage {
  id: number;

  session_id: string;

  student_id: string;

  role: "user" | "assistant";

  content: string;

  response_payload: TutorMessageResponse | null;

  created_at: string;
}


export interface SessionHistorySummary {
  session_id: string;

  subject: "MATH" | "SCIENCE" | "ENGLISH";

  topic: string | null;

  mode: string;

  message_count: number;

  last_message_preview: string;

  last_message_at: string;
}

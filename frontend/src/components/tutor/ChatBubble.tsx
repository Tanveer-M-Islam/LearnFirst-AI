import {
  Bot,
  UserRound,
} from "lucide-react";

import type {
  ChatMessage,
} from "../../types/tutor";


interface ChatBubbleProps {
  message: ChatMessage;
}


export default function ChatBubble({
  message,
}: ChatBubbleProps) {
  const isTutor =
    message.role === "tutor";

  return (
    <div
      className={
        isTutor
          ? (
            "chat-row "
            + "chat-row-tutor"
          )
          : (
            "chat-row "
            + "chat-row-student"
          )
      }
    >
      {isTutor && (
        <div className="chat-avatar tutor-avatar">
          <Bot size={19} />
        </div>
      )}

      <div
        className={
          isTutor
            ? (
              "chat-bubble "
              + "tutor-bubble"
            )
            : (
              "chat-bubble "
              + "student-bubble"
            )
        }
      >
        <div className="chat-speaker">
          {isTutor
            ? "LearnFirst"
            : "You"}
        </div>

        <div className="chat-text">
          {message.text}
        </div>
      </div>

      {!isTutor && (
        <div className="chat-avatar student-avatar">
          <UserRound
            size={18}
          />
        </div>
      )}
    </div>
  );
}
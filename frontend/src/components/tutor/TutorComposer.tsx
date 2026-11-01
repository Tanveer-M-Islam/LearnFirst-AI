import {
  ArrowUp,
  Lightbulb,
  MessageCircleQuestion,
} from "lucide-react";

import {
  type FormEvent,
} from "react";


interface TutorComposerProps {
  value: string;

  disabled: boolean;

  onChange:
    (value: string) => void;

  onSubmit: () => void;

  onQuickMessage:
    (message: string) => void;
}


export default function TutorComposer({
  value,
  disabled,
  onChange,
  onSubmit,
  onQuickMessage,
}: TutorComposerProps) {
  const handleSubmit = (
    event:
      FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    if (
      !disabled
      && value.trim()
    ) {
      onSubmit();
    }
  };

  return (
    <div className="tutor-composer-area">
      <div className="quick-actions">
        <button
          type="button"
          disabled={disabled}
          onClick={() =>
            onQuickMessage(
              "Can I get a hint?",
            )
          }
        >
          <Lightbulb
            size={16}
          />

          Give me a hint
        </button>

        <button
          type="button"
          disabled={disabled}
          onClick={() =>
            onQuickMessage(
              "I'm stuck.",
            )
          }
        >
          <MessageCircleQuestion
            size={16}
          />

          I'm stuck
        </button>
      </div>

      <form
        className="tutor-composer"
        onSubmit={handleSubmit}
      >
        <textarea
          value={value}
          disabled={disabled}
          rows={2}
          maxLength={4000}
          placeholder={
            disabled
              ? (
                "LearnFirst is "
                + "thinking..."
              )
              : (
                "Show your next "
                + "step..."
              )
          }
          onChange={(event) =>
            onChange(
              event.target.value,
            )
          }
        />

        <button
          type="submit"
          aria-label="Send message"
          disabled={
            disabled
            || !value.trim()
          }
        >
          <ArrowUp
            size={20}
          />
        </button>
      </form>

      <p className="composer-helper">
        It's okay to make a mistake.
        Show what you think first.
      </p>
    </div>
  );
}
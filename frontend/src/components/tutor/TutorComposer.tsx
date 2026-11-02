import {
  ArrowUp,
  BookOpenCheck,
  Lightbulb,
  MessageCircleQuestion,
  RefreshCcw,
} from "lucide-react";

import {
  type FormEvent,
} from "react";

import type {
  LearningMode,
} from "../../types/session";


interface TutorComposerProps {
  value: string;

  disabled: boolean;

  mode: LearningMode;

  onChange:
    (value: string) => void;

  onSubmit: () => void;

  onQuickMessage:
    (message: string) => void;
}


function placeholderForMode(
  mode: LearningMode,
): string {

  switch (mode) {

    case "PRACTICE":

      return (
        "Type your answer "
        + "or next step..."
      );


    case "LEARN":

      return (
        "Ask about the concept "
        + "or explain what "
        + "you understand..."
      );


    default:

      return (
        "Show your next step..."
      );
  }
}


function helperForMode(
  mode: LearningMode,
): string {

  switch (mode) {

    case "PRACTICE":

      return (
        "Try independently first. "
        + "You can ask for a hint "
        + "when you need one."
      );


    case "LEARN":

      return (
        "Ask questions freely. "
        + "When you're ready, "
        + "try a practice problem."
      );


    default:

      return (
        "It's okay to make a mistake. "
        + "Show what you think first."
      );
  }
}


export default function TutorComposer({
  value,
  disabled,
  mode,
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

        {mode
          === "LEARN"
          ? (
            <>
              <button
                type="button"
                disabled={
                  disabled
                }
                onClick={() =>
                  onQuickMessage(
                    (
                      "Explain this "
                      + "concept simply."
                    ),
                  )
                }
              >
                <BookOpenCheck
                  size={16}
                />

                Explain simply
              </button>


              <button
                type="button"
                disabled={
                  disabled
                }
                onClick={() =>
                  onQuickMessage(
                    (
                      "Give me a "
                      + "practice question."
                    ),
                  )
                }
              >
                <RefreshCcw
                  size={16}
                />

                Practice question
              </button>
            </>
          )
          : mode
            === "PRACTICE"
            ? (
              <>
                <button
                  type="button"
                  disabled={
                    disabled
                  }
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
                  disabled={
                    disabled
                  }
                  onClick={() =>
                    onQuickMessage(
                      (
                        "Give me a "
                        + "practice question."
                      ),
                    )
                  }
                >
                  <RefreshCcw
                    size={16}
                  />

                  New problem
                </button>
              </>
            )
            : (
              <>
                <button
                  type="button"
                  disabled={
                    disabled
                  }
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
                  disabled={
                    disabled
                  }
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
              </>
            )}
      </div>


      <form
        className="tutor-composer"
        onSubmit={
          handleSubmit
        }
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
                placeholderForMode(
                  mode,
                )
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
        {
          helperForMode(
            mode,
          )
        }
      </p>
    </div>
  );
}
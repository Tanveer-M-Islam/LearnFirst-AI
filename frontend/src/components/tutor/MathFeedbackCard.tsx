import {
  CheckCircle2,
  Lightbulb,
  RotateCcw,
  Sparkles,
} from "lucide-react";

import type {
  MathValidation,
} from "../../types/tutor";


interface MathFeedbackCardProps {
  validation:
    MathValidation;
}


function getFriendlyMistakeMessage(
  code: string | null,
): string {
  switch (code) {
    case "MATH_DIVIDE_COEFFICIENT":
      return (
        "You reached the multiplication "
        + "step. Think about the operation "
        + "that undoes multiplying x."
      );

    case "MATH_INVERSE_OPERATION":
      return (
        "Check the inverse operation. "
        + "Think about what would undo "
        + "the operation applied to x."
      );

    case "MATH_ALGEBRA_PROCESS_ERROR":
      return (
        "One algebra step changed the "
        + "meaning of the equation. "
        + "Check that step carefully."
      );

    default:
      return (
        "One step needs another look. "
        + "Use the tutor's question "
        + "to decide what to try next."
      );
  }
}


export default function MathFeedbackCard({
  validation,
}: MathFeedbackCardProps) {
  if (
    !validation.supported
  ) {
    return (
      <div className="math-feedback neutral-feedback">
        <Lightbulb
          size={20}
        />

        <div>
          <strong>
            Let's work through it
          </strong>

          <p>
            This problem needs
            guided reasoning rather
            than automatic checking.
          </p>
        </div>
      </div>
    );
  }

  if (
    validation.status
    === "CORRECT"
  ) {
    return (
      <div className="math-feedback correct-feedback">
        <CheckCircle2
          size={21}
        />

        <div>
          <strong>
            Nice work — that's correct.
          </strong>

          <p>
            Now let's make sure
            you can use the same
            idea again.
          </p>
        </div>
      </div>
    );
  }

  if (
    validation.status
    === "PARTIALLY_CORRECT"
  ) {
    return (
      <div className="math-feedback partial-feedback">
        <Sparkles
          size={21}
        />

        <div>
          <strong>
            You're on the right track.
          </strong>

          {validation.correct_steps
            .length > 0 && (
            <div className="correct-step-box">
              <span>
                Correct so far
              </span>

              <strong>
                {
                  validation
                    .correct_steps[0]
                }
              </strong>
            </div>
          )}

          <p>
            {
              getFriendlyMistakeMessage(
                validation
                  .misconception_code,
              )
            }
          </p>
        </div>
      </div>
    );
  }

  if (
    validation.status
    === "INCORRECT"
  ) {
    return (
      <div className="math-feedback retry-feedback">
        <RotateCcw
          size={20}
        />

        <div>
          <strong>
            Not quite yet.
          </strong>

          <p>
            {
              getFriendlyMistakeMessage(
                validation
                  .misconception_code,
              )
            }
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="math-feedback neutral-feedback">
      <Lightbulb
        size={20}
      />

      <div>
        <strong>
          Show your thinking
        </strong>

        <p>
          Try writing one clear
          step, such as
          “3x = 12” or “x = 4”.
        </p>
      </div>
    </div>
  );
}
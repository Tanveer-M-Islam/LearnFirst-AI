import {
  ArrowLeft,
  ArrowRight,
  BookOpenCheck,
  Calculator,
  Lightbulb,
  PencilLine,
} from "lucide-react";

import {
  useState,
} from "react";

import {
  useNavigate,
} from "react-router";

import {
  createLearningSession,
} from "../api/sessions";

import type {
  LearningMode,
} from "../types/session";

import {
  getStoredStudent,
} from "../utils/studentStorage";


const sampleProblems = [
  "3x + 6 = 18",
  "2x + 3 = 11",
  "4x - 5 = 19",
];


const modes: {
  value: LearningMode;
  title: string;
  description: string;
  icon:
    typeof PencilLine;
}[] = [
  {
    value:
      "HOMEWORK_HELP",

    title:
      "Homework Help",

    description:
      "Show what you've tried and "
      + "get step-by-step guidance.",

    icon:
      PencilLine,
  },

  {
    value:
      "PRACTICE",

    title:
      "Practice",

    description:
      "Work through a problem and "
      + "learn from each attempt.",

    icon:
      BookOpenCheck,
  },

  {
    value:
      "LEARN",

    title:
      "Learn",

    description:
      "Understand the idea before "
      + "solving independently.",

    icon:
      Lightbulb,
  },
];


export default function MathStartPage() {
  const navigate =
    useNavigate();

  const student =
    getStoredStudent();

  const [
    mode,
    setMode,
  ] = useState<LearningMode>(
    "HOMEWORK_HELP",
  );

  const [
    problem,
    setProblem,
  ] = useState(
    "3x + 6 = 18",
  );

  const [
    loading,
    setLoading,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState<
    string | null
  >(null);


  const handleStart =
    async () => {
      if (!student) {
        navigate(
          "/setup",
        );

        return;
      }

      const trimmedProblem =
        problem.trim();

      if (!trimmedProblem) {
        setError(
          "Enter a Math problem "
          + "before starting.",
        );

        return;
      }

      setLoading(true);
      setError(null);

      try {
        const session =
          await createLearningSession({
            student_id:
              student.id,

            mode,

            subject:
              "MATH",

            topic:
              "Linear Equations",

            concept_code:
              "MATH_ALG_LINEAR_01",

            current_problem:
              trimmedProblem,
          });

        navigate(
          (
            "/learn/math/session/"
            + session.id
          ),
        );
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : (
              "Could not start "
              + "the Math session."
            ),
        );
      } finally {
        setLoading(false);
      }
    };


  return (
    <div className="math-start-page">
      <button
        type="button"
        className="page-back-button"
        onClick={() =>
          navigate(
            "/dashboard",
          )
        }
      >
        <ArrowLeft
          size={18}
        />

        Dashboard
      </button>

      <section className="math-start-header">
        <div className="math-start-icon">
          <Calculator
            size={30}
          />
        </div>

        <div>
          <span>
            Math learning
          </span>

          <h1>
            Let's solve it
            together.
          </h1>

          <p>
            You do the thinking.
            LearnFirst will guide
            you when you need help.
          </p>
        </div>
      </section>

      <section className="math-start-section">
        <div className="section-number">
          1
        </div>

        <div>
          <h2>
            How would you like
            to learn?
          </h2>

          <p>
            Choose the kind of
            support you need.
          </p>
        </div>
      </section>

      <div className="learning-mode-grid">
        {modes.map(
          (item) => {
            const Icon =
              item.icon;

            const selected =
              mode
              === item.value;

            return (
              <button
                key={
                  item.value
                }
                type="button"
                className={
                  selected
                    ? (
                      "learning-mode-card "
                      + "selected"
                    )
                    : (
                      "learning-mode-card"
                    )
                }
                onClick={() =>
                  setMode(
                    item.value,
                  )
                }
              >
                <div className="mode-icon">
                  <Icon
                    size={22}
                  />
                </div>

                <strong>
                  {item.title}
                </strong>

                <p>
                  {
                    item
                      .description
                  }
                </p>

                <span
                  className="mode-radio"
                >
                  {selected
                    ? "✓"
                    : ""}
                </span>
              </button>
            );
          },
        )}
      </div>

      <section className="math-start-section problem-section-heading">
        <div className="section-number">
          2
        </div>

        <div>
          <h2>
            What problem are
            you working on?
          </h2>

          <p>
            Enter your problem or
            choose an example.
          </p>
        </div>
      </section>

      <div className="problem-entry-card surface-card">
        <label
          htmlFor="math-problem"
          className="field-label"
        >
          Math problem
        </label>

        <input
          id="math-problem"
          className="math-problem-input"
          value={problem}
          onChange={(event) =>
            setProblem(
              event.target.value,
            )
          }
          placeholder={
            "Example: "
            + "3x + 6 = 18"
          }
        />

        <div className="problem-suggestions">
          <span>
            Try an example
          </span>

          <div>
            {sampleProblems.map(
              (item) => (
                <button
                  key={item}
                  type="button"
                  onClick={() =>
                    setProblem(
                      item,
                    )
                  }
                >
                  {item}
                </button>
              ),
            )}
          </div>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <button
          type="button"
          className="primary-button start-learning-button"
          disabled={loading}
          onClick={
            handleStart
          }
        >
          {loading
            ? (
              "Preparing your "
              + "lesson..."
            )
            : (
              <>
                Start learning

                <ArrowRight
                  size={19}
                />
              </>
            )}
        </button>
      </div>
    </div>
  );
}
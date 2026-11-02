import {
  ArrowLeft,
  ArrowRight,
  BookOpenCheck,
  BrainCircuit,
  Calculator,
  ClipboardCheck,
  Gauge,
  Lightbulb,
  PencilLine,
  RefreshCcw,
  Sparkles,
  Target,
  Trophy,
} from "lucide-react";

import {
  useEffect,
  useState,
} from "react";

import {
  useNavigate,
} from "react-router";

import {
  getAdaptivePlan,
} from "../api/adaptive";

import {
  createLearningSession,
} from "../api/sessions";

import type {
  AdaptiveActivity,
  AdaptivePlan,
  AdaptiveSupport,
  ExplanationDepth,
} from "../types/adaptive";

import type {
  DifficultyLevel,
} from "../types/assessment";

import type {
  LearningMode,
} from "../types/session";

import {
  getStoredStudent,
} from "../utils/studentStorage";


const CONCEPT_CODE =
  "MATH_ALG_LINEAR_01";


const sampleProblems = [
  "3x + 6 = 18",
  "2x + 3 = 11",
  "4x - 5 = 19",
];


const modes: {
  value: LearningMode;
  title: string;
  description: string;
  icon: typeof PencilLine;
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


function difficultyLabel(
  difficulty: DifficultyLevel,
): string {
  switch (difficulty) {
    case "CHALLENGING":
      return "Challenging";

    case "MODERATE":
      return "Moderate";

    default:
      return "Easy";
  }
}


function supportLabel(
  support: AdaptiveSupport,
): string {
  switch (support) {
    case "STRONG":
      return "Strong support";

    case "GUIDED":
      return "Guided support";

    default:
      return "Gentle support";
  }
}


function explanationLabel(
  depth: ExplanationDepth,
): string {
  switch (depth) {
    case "DEEP":
      return "Deeper explanations";

    case "SIMPLE":
      return "Simple explanations";

    default:
      return "Balanced explanations";
  }
}


function activityLabel(
  activity: AdaptiveActivity,
): string {
  switch (activity) {
    case "TAKE_DIAGNOSTIC":
      return "Check your starting level";

    case "GUIDED_PRACTICE":
      return "Guided practice";

    case "INDEPENDENT_PRACTICE":
      return "Independent practice";

    case "REVIEW_FOUNDATION":
      return "Review the foundation";

    case "TAKE_MASTERY_CHECK":
      return "Take a mastery check";

    case "CHALLENGE_PRACTICE":
      return "Challenge practice";
  }
}


function activityDescription(
  activity: AdaptiveActivity,
): string {
  switch (activity) {
    case "TAKE_DIAGNOSTIC":
      return (
        "LearnFirst needs a quick "
        + "starting assessment before "
        + "choosing your learning level."
      );

    case "GUIDED_PRACTICE":
      return (
        "Practice with guidance while "
        + "you build confidence."
      );

    case "INDEPENDENT_PRACTICE":
      return (
        "You're ready to solve more "
        + "with less help."
      );

    case "REVIEW_FOUNDATION":
      return (
        "A simpler problem and more "
        + "support will help strengthen "
        + "the foundation."
      );

    case "TAKE_MASTERY_CHECK":
      return (
        "Your recent work suggests "
        + "you're ready to test what "
        + "you can do independently."
      );

    case "CHALLENGE_PRACTICE":
      return (
        "You've shown strong mastery. "
        + "Try a harder problem next."
      );
  }
}


function activityIcon(
  activity: AdaptiveActivity,
) {
  switch (activity) {
    case "TAKE_DIAGNOSTIC":
      return ClipboardCheck;

    case "TAKE_MASTERY_CHECK":
      return Trophy;

    case "CHALLENGE_PRACTICE":
      return Sparkles;

    case "REVIEW_FOUNDATION":
      return Lightbulb;

    case "INDEPENDENT_PRACTICE":
      return Target;

    default:
      return BrainCircuit;
  }
}


function adaptiveMode(
  activity: AdaptiveActivity,
): LearningMode {
  if (
    activity
    === "REVIEW_FOUNDATION"
  ) {
    return "LEARN";
  }

  return "PRACTICE";
}


export default function MathStartPage() {
  const navigate =
    useNavigate();

  const student =
    getStoredStudent();

  const studentId =
    student?.id;


  const [
    adaptivePlan,
    setAdaptivePlan,
  ] = useState<
    AdaptivePlan | null
  >(null);

  const [
    adaptiveLoading,
    setAdaptiveLoading,
  ] = useState(true);

  const [
    adaptiveError,
    setAdaptiveError,
  ] = useState<
    string | null
  >(null);

  const [
    adaptiveStarting,
    setAdaptiveStarting,
  ] = useState(false);


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


  const loadAdaptivePlan =
    async () => {
      if (!studentId) {
        setAdaptiveLoading(
          false,
        );

        return;
      }

      setAdaptiveLoading(true);
      setAdaptiveError(null);

      try {
        const data =
          await getAdaptivePlan(
            studentId,
            CONCEPT_CODE,
          );

        setAdaptivePlan(data);
      } catch (err) {
        setAdaptiveError(
          err instanceof Error
            ? err.message
            : (
              "Could not load your "
              + "personalized plan."
            ),
        );
      } finally {
        setAdaptiveLoading(
          false,
        );
      }
    };


  useEffect(() => {
    void loadAdaptivePlan();
  }, [studentId]);


  const handleAdaptiveStart =
    async () => {
      if (!student) {
        navigate(
          "/setup",
        );

        return;
      }

      if (!adaptivePlan) {
        return;
      }


      if (
        adaptivePlan.next_activity
        === "TAKE_DIAGNOSTIC"
      ) {
        navigate(
          "/assessments/math/diagnostic",
        );

        return;
      }


      if (
        adaptivePlan.next_activity
        === "TAKE_MASTERY_CHECK"
      ) {
        navigate(
          "/assessments/math/mastery",
        );

        return;
      }


      if (
        !adaptivePlan.next_problem
      ) {
        setAdaptiveError(
          "No adaptive problem is "
          + "available for this "
          + "recommendation yet.",
        );

        return;
      }


      setAdaptiveStarting(true);
      setAdaptiveError(null);

      try {
        const session =
          await createLearningSession({
            student_id:
              student.id,

            mode:
              adaptiveMode(
                adaptivePlan
                  .next_activity,
              ),

            subject:
              "MATH",

            topic:
              "Linear Equations",

            concept_code:
              CONCEPT_CODE,

            current_problem:
              adaptivePlan
                .next_problem
                .prompt,
          });


        navigate(
          (
            "/learn/math/session/"
            + session.id
          ),
        );
      } catch (err) {
        setAdaptiveError(
          err instanceof Error
            ? err.message
            : (
              "Could not start your "
              + "recommended activity."
            ),
        );
      } finally {
        setAdaptiveStarting(
          false,
        );
      }
    };


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
              CONCEPT_CODE,

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


  const AdaptiveIcon =
    adaptivePlan
      ? activityIcon(
          adaptivePlan
            .next_activity,
        )
      : BrainCircuit;


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


      {/* =========================
          Adaptive Recommendation
      ========================== */}

      <section className="adaptive-section">
        <div className="adaptive-section-heading">
          <div>
            <span className="adaptive-eyebrow">
              <Sparkles
                size={15}
              />

              Personalized for you
            </span>

            <h2>
              Recommended next step
            </h2>
          </div>

          <button
            type="button"
            className="adaptive-refresh-button"
            disabled={
              adaptiveLoading
            }
            onClick={() =>
              void loadAdaptivePlan()
            }
          >
            <RefreshCcw
              size={16}
            />

            Refresh
          </button>
        </div>


        {adaptiveLoading && (
          <div className="adaptive-loading-card surface-card">
            <div className="adaptive-loading-icon">
              <BrainCircuit
                size={24}
              />
            </div>

            <div>
              <strong>
                Building your
                learning plan...
              </strong>

              <span>
                LearnFirst is checking
                your recent progress.
              </span>
            </div>
          </div>
        )}


        {!adaptiveLoading
          && adaptivePlan
          && (
          <div className="adaptive-plan-card surface-card">
            <div className="adaptive-plan-main">
              <div className="adaptive-plan-icon">
                <AdaptiveIcon
                  size={28}
                />
              </div>

              <div className="adaptive-plan-copy">
                <span>
                  Next activity
                </span>

                <h3>
                  {
                    activityLabel(
                      adaptivePlan
                        .next_activity,
                    )
                  }
                </h3>

                <p>
                  {
                    activityDescription(
                      adaptivePlan
                        .next_activity,
                    )
                  }
                </p>
              </div>
            </div>


            <div className="adaptive-profile-grid">
              <div>
                <Gauge
                  size={18}
                />

                <span>
                  Difficulty
                </span>

                <strong>
                  {
                    difficultyLabel(
                      adaptivePlan
                        .difficulty,
                    )
                  }
                </strong>
              </div>

              <div>
                <BrainCircuit
                  size={18}
                />

                <span>
                  Support
                </span>

                <strong>
                  {
                    supportLabel(
                      adaptivePlan
                        .support_level,
                    )
                  }
                </strong>
              </div>

              <div>
                <BookOpenCheck
                  size={18}
                />

                <span>
                  Explanation
                </span>

                <strong>
                  {
                    explanationLabel(
                      adaptivePlan
                        .explanation_depth,
                    )
                  }
                </strong>
              </div>
            </div>


            {adaptivePlan
              .latest_score_percent
              !== null
              && (
              <div className="adaptive-score-note">
                <span>
                  Latest assessment
                </span>

                <strong>
                  {
                    adaptivePlan
                      .latest_score_percent
                  }
                  %
                </strong>
              </div>
            )}


            {adaptivePlan
              .next_problem
              && (
              <div className="adaptive-next-problem">
                <div>
                  <span>
                    Your next problem
                  </span>

                  <strong>
                    {
                      adaptivePlan
                        .next_problem
                        .prompt
                    }
                  </strong>
                </div>

                <div className="adaptive-problem-level">
                  {
                    difficultyLabel(
                      adaptivePlan
                        .next_problem
                        .difficulty,
                    )
                  }
                </div>
              </div>
            )}


            <div className="adaptive-plan-footer">
              <p>
                {
                  adaptivePlan
                    .summary
                }
              </p>

              <button
                type="button"
                className="primary-button adaptive-start-button"
                disabled={
                  adaptiveStarting
                }
                onClick={() =>
                  void handleAdaptiveStart()
                }
              >
                {adaptiveStarting
                  ? (
                    "Preparing..."
                  )
                  : (
                    <>
                      {
                        adaptivePlan
                          .next_activity
                        === "TAKE_DIAGNOSTIC"
                          ? "Start diagnostic"

                          : adaptivePlan
                            .next_activity
                          === "TAKE_MASTERY_CHECK"
                            ? "Start mastery check"

                            : "Start recommended activity"
                      }

                      <ArrowRight
                        size={18}
                      />
                    </>
                  )}
              </button>
            </div>
          </div>
        )}


        {!adaptiveLoading
          && adaptiveError
          && (
          <div className="adaptive-error">
            {adaptiveError}
          </div>
        )}
      </section>


      {/* =========================
          Diagnostic
      ========================== */}

      <section className="diagnostic-banner surface-card">
        <div className="diagnostic-banner-icon">
          <ClipboardCheck
            size={24}
          />
        </div>

        <div>
          <strong>
            Want to check your level?
          </strong>

          <p>
            Take a 5-question
            diagnostic to update
            LearnFirst's understanding
            of your current level.
          </p>
        </div>

        <button
          type="button"
          className="secondary-button"
          onClick={() =>
            navigate(
              "/assessments/math/diagnostic",
            )
          }
        >
          Check my level

          <ArrowRight
            size={17}
          />
        </button>
      </section>


      <div className="manual-learning-divider">
        <span>
          Or choose your own activity
        </span>
      </div>


      {/* =========================
          Manual learning
      ========================== */}

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
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
  useSearchParams,
} from "react-router";

import {
  getAdaptivePlan,
} from "../api/adaptive";

import {
  createLearningSession,
} from "../api/sessions";

import {
  MATH_TOPICS,
  getMathTopic,
} from "../data/mathTopics";

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
      (
        "Bring your own problem. "
        + "Try it first and receive "
        + "progressive guidance."
      ),

    icon:
      PencilLine,
  },


  {
    value:
      "PRACTICE",

    title:
      "Practice",

    description:
      (
        "LearnFirst chooses problems "
        + "and adapts them using "
        + "your progress."
      ),

    icon:
      BookOpenCheck,
  },


  {
    value:
      "LEARN",

    title:
      "Learn",

    description:
      (
        "Understand the concept "
        + "before moving into "
        + "practice."
      ),

    icon:
      Lightbulb,
  },
];


function difficultyLabel(
  difficulty: DifficultyLevel,
): string {

  switch (
    difficulty
  ) {

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

  switch (
    support
  ) {

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

  switch (
    depth
  ) {

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

  switch (
    activity
  ) {

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

  switch (
    activity
  ) {

    case "TAKE_DIAGNOSTIC":

      return (
        "Take a short assessment "
        + "for this topic before "
        + "LearnFirst adapts it."
      );


    case "GUIDED_PRACTICE":

      return (
        "Continue practicing with "
        + "guided support."
      );


    case "INDEPENDENT_PRACTICE":

      return (
        "You're ready to solve "
        + "more independently."
      );


    case "REVIEW_FOUNDATION":

      return (
        "Review this topic before "
        + "returning to harder "
        + "practice."
      );


    case "TAKE_MASTERY_CHECK":

      return (
        "Your recent work suggests "
        + "you're ready for an "
        + "independent mastery check."
      );


    case "CHALLENGE_PRACTICE":

      return (
        "Your mastery is strong. "
        + "Try a more challenging "
        + "problem."
      );
  }
}


function activityIcon(
  activity: AdaptiveActivity,
) {

  switch (
    activity
  ) {

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


  const [
    searchParams,
    setSearchParams,
  ] = useSearchParams();


  const student =
    getStoredStudent();


  const studentId =
    student?.id;


  const selectedTopic =
    getMathTopic(
      searchParams.get(
        "concept",
      ),
    );


  const conceptCode =
    selectedTopic
      .conceptCode;


  const [
    adaptivePlan,
    setAdaptivePlan,
  ] = useState<
    AdaptivePlan | null
  >(null);


  const [
    adaptiveLoading,
    setAdaptiveLoading,
  ] = useState(
    true,
  );


  const [
    adaptiveError,
    setAdaptiveError,
  ] = useState<
    string | null
  >(null);


  const [
    adaptiveStarting,
    setAdaptiveStarting,
  ] = useState(
    false,
  );


  const [
    mode,
    setMode,
  ] = useState<
    LearningMode
  >(
    "HOMEWORK_HELP",
  );


  const [
    problem,
    setProblem,
  ] = useState(
    selectedTopic
      .sampleProblems[0],
  );


  const [
    loading,
    setLoading,
  ] = useState(
    false,
  );


  const [
    error,
    setError,
  ] = useState<
    string | null
  >(null);


  const selectTopic = (
    nextConceptCode: string,
  ) => {

    setSearchParams({
      concept:
        nextConceptCode,
    });


    const nextTopic =
      getMathTopic(
        nextConceptCode,
      );


    setProblem(
      nextTopic
        .sampleProblems[0],
    );


    setAdaptivePlan(
      null,
    );


    setAdaptiveError(
      null,
    );


    setError(
      null,
    );
  };


  const loadAdaptivePlan =
    async () => {

      if (
        !studentId
      ) {

        setAdaptiveLoading(
          false,
        );

        return;
      }


      setAdaptiveLoading(
        true,
      );


      setAdaptiveError(
        null,
      );


      try {

        const data =
          await getAdaptivePlan(
            studentId,
            conceptCode,
          );


        setAdaptivePlan(
          data,
        );


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


  useEffect(
    () => {

      setProblem(
        selectedTopic
          .sampleProblems[0],
      );


      void loadAdaptivePlan();

    },
    [
      studentId,
      conceptCode,
    ],
  );


  const handleAdaptiveStart =
    async () => {

      if (
        !student
      ) {

        navigate(
          "/setup",
        );

        return;
      }


      if (
        !adaptivePlan
      ) {

        return;
      }


      if (
        adaptivePlan
          .next_activity
        === "TAKE_DIAGNOSTIC"
      ) {

        navigate(
          (
            "/assessments/math/diagnostic"
            + `?concept=${conceptCode}`
          ),
        );

        return;
      }


      if (
        adaptivePlan
          .next_activity
        === "TAKE_MASTERY_CHECK"
      ) {

        navigate(
          (
            "/assessments/math/mastery"
            + `?concept=${conceptCode}`
          ),
        );

        return;
      }


      const needsProblem =
        adaptivePlan
          .next_activity
        !== "REVIEW_FOUNDATION";


      if (
        needsProblem
        && !adaptivePlan
          .next_problem
      ) {

        setAdaptiveError(
          "No adaptive problem is "
          + "available for this "
          + "recommendation yet.",
        );

        return;
      }


      setAdaptiveStarting(
        true,
      );


      setAdaptiveError(
        null,
      );


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
              selectedTopic
                .title,

            concept_code:
              conceptCode,

            current_problem:
              adaptivePlan
                .next_activity
              === "REVIEW_FOUNDATION"

                ? null

                : (
                  adaptivePlan
                    .next_problem
                    ?.prompt
                  ?? null
                ),
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

      if (
        !student
      ) {

        navigate(
          "/setup",
        );

        return;
      }


      let sessionProblem:
        string | null = null;


      if (
        mode
        === "HOMEWORK_HELP"
      ) {

        const trimmedProblem =
          problem.trim();


        if (
          !trimmedProblem
        ) {

          setError(
            "Enter your Math problem "
            + "before starting.",
          );

          return;
        }


        sessionProblem = (
          trimmedProblem
        );
      }


      else if (
        mode
        === "PRACTICE"
      ) {

        sessionProblem = (
          adaptivePlan
            ?.next_problem
            ?.prompt

          ?? selectedTopic
            .sampleProblems[0]
        );
      }


      else if (
        mode
        === "LEARN"
      ) {

        sessionProblem = null;
      }


      setLoading(
        true,
      );


      setError(
        null,
      );


      try {

        const session =
          await createLearningSession({

            student_id:
              student.id,

            mode,

            subject:
              "MATH",

            topic:
              selectedTopic
                .title,

            concept_code:
              conceptCode,

            current_problem:
              sessionProblem,
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

        setLoading(
          false,
        );
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
            Choose what you
            want to learn.
          </h1>


          <p>
            Each Math topic keeps
            its own progress,
            difficulty and learning
            profile.
          </p>

        </div>

      </section>


      {/* =============================
          Topic Selection
      ============================== */}

      <section className="math-start-section">

        <div className="section-number">
          1
        </div>


        <div>

          <h2>
            Choose a Math topic
          </h2>


          <p>
            LearnFirst adapts each
            topic independently.
          </p>

        </div>

      </section>


      <div className="learning-mode-grid">

        {MATH_TOPICS.map(
          (
            topic,
          ) => {

            const selected =
              topic.conceptCode
              === conceptCode;


            return (

              <button
                key={
                  topic.conceptCode
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
                  selectTopic(
                    topic
                      .conceptCode,
                  )
                }
              >

                <div className="mode-icon">

                  <Calculator
                    size={22}
                  />

                </div>


                <strong>
                  {
                    topic.title
                  }
                </strong>


                <p>
                  {
                    topic.description
                  }
                </p>


                <span className="mode-radio">

                  {
                    selected
                      ? "✓"
                      : ""
                  }

                </span>

              </button>
            );
          },
        )}

      </div>


      {/* =============================
          Adaptive Recommendation
      ============================== */}

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
              {
                selectedTopic
                  .title
              }
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
                Checking progress
                for {
                  selectedTopic.title
                }.
              </span>

            </div>

          </div>
        )}


        {(
          !adaptiveLoading
          && adaptivePlan
        ) && (

          <div className="adaptive-plan-card surface-card">

            <div className="adaptive-plan-main">

              <div className="adaptive-plan-icon">

                <AdaptiveIcon
                  size={28}
                />

              </div>


              <div className="adaptive-plan-copy">

                <span>
                  Recommended next step
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


            {(
              adaptivePlan
                .latest_score_percent
              !== null
            ) && (

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
                    Suggested problem
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

                {
                  adaptiveStarting
                    ? "Preparing..."

                    : adaptivePlan
                      .next_activity
                    === "TAKE_DIAGNOSTIC"

                      ? "Start diagnostic"

                      : adaptivePlan
                        .next_activity
                      === "TAKE_MASTERY_CHECK"

                        ? "Start mastery check"

                        : (
                          "Start recommended "
                          + "activity"
                        )
                }


                {!adaptiveStarting
                  && (
                  <ArrowRight
                    size={18}
                  />
                )}

              </button>

            </div>

          </div>
        )}


        {(
          !adaptiveLoading
          && adaptiveError
        ) && (

          <div className="adaptive-error">
            {adaptiveError}
          </div>

        )}

      </section>


      {/* =============================
          Topic Diagnostic
      ============================== */}

      <section className="diagnostic-banner surface-card">

        <div className="diagnostic-banner-icon">

          <ClipboardCheck
            size={24}
          />

        </div>


        <div>

          <strong>
            Check your level in {
              selectedTopic.title
            }
          </strong>


          <p>
            This topic has its own
            diagnostic and mastery
            history.
          </p>

        </div>


        <button
          type="button"
          className="secondary-button"

          onClick={() =>
            navigate(
              (
                "/assessments/math/diagnostic"
                + `?concept=${conceptCode}`
              ),
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
          Choose how you want to learn
        </span>

      </div>


      {/* =============================
          Mode Selection
      ============================== */}

      <section className="math-start-section">

        <div className="section-number">
          2
        </div>


        <div>

          <h2>
            Choose a learning mode
          </h2>


          <p>
            Homework Help, Practice
            and Learn behave
            differently.
          </p>

        </div>

      </section>


      <div className="learning-mode-grid">

        {modes.map(
          (
            item,
          ) => {

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

                onClick={() => {

                  setMode(
                    item.value,
                  );

                  setError(
                    null,
                  );
                }}
              >

                <div className="mode-icon">

                  <Icon
                    size={22}
                  />

                </div>


                <strong>
                  {
                    item.title
                  }
                </strong>


                <p>
                  {
                    item.description
                  }
                </p>


                <span className="mode-radio">

                  {
                    selected
                      ? "✓"
                      : ""
                  }

                </span>

              </button>
            );
          },
        )}

      </div>


      {/* =============================
          Mode Content
      ============================== */}

      <section className="math-start-section problem-section-heading">

        <div className="section-number">
          3
        </div>


        <div>

          <h2>

            {mode
              === "HOMEWORK_HELP"

                ? (
                  "What problem are "
                  + "you working on?"
                )

                : mode
                  === "PRACTICE"

                  ? (
                    "Your practice problem"
                  )

                  : (
                    "Start learning "
                    + selectedTopic.title
                  )}

          </h2>


          <p>

            {mode
              === "HOMEWORK_HELP"

                ? (
                  "Enter a problem from "
                  + "the selected topic."
                )

                : mode
                  === "PRACTICE"

                  ? (
                    "LearnFirst chooses "
                    + "a problem using "
                    + "your topic profile."
                  )

                  : (
                    "Learn the concept "
                    + "first, then move "
                    + "into practice."
                  )}

          </p>

        </div>

      </section>


      {/* =============================
          Homework Help
      ============================== */}

      {mode
        === "HOMEWORK_HELP"
        && (

        <div className="problem-entry-card surface-card">

          <label
            htmlFor="math-problem"
            className="field-label"
          >
            {
              selectedTopic.title
            } problem
          </label>


          <input
            id="math-problem"
            className="math-problem-input"

            value={
              problem
            }

            onChange={(event) =>
              setProblem(
                event
                  .target
                  .value,
              )
            }

            placeholder={
              (
                "Example: "
                + selectedTopic
                  .sampleProblems[0]
              )
            }
          />


          <div className="problem-suggestions">

            <span>
              Try an example
            </span>


            <div>

              {selectedTopic
                .sampleProblems
                .map(
                  (
                    item,
                  ) => (

                    <button
                      key={
                        item
                      }

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


          <p>
            LearnFirst will ask
            you to try the problem
            before giving detailed
            help.
          </p>


          {error && (

            <div className="error-message">
              {error}
            </div>

          )}


          <button
            type="button"
            className="primary-button start-learning-button"

            disabled={
              loading
            }

            onClick={
              handleStart
            }
          >

            {
              loading
                ? "Preparing..."
                : "Start homework help"
            }


            {!loading
              && (
              <ArrowRight
                size={19}
              />
            )}

          </button>

        </div>
      )}


      {/* =============================
          Practice
      ============================== */}

      {mode
        === "PRACTICE"
        && (

        <div className="problem-entry-card surface-card">

          <span className="field-label">
            LearnFirst selected
          </span>


          <div className="adaptive-next-problem">

            <div>

              <span>
                Practice problem
              </span>


              <strong>

                {
                  adaptivePlan
                    ?.next_problem
                    ?.prompt

                  ?? selectedTopic
                    .sampleProblems[0]
                }

              </strong>

            </div>


            {adaptivePlan
              ?.next_problem
              && (

              <div className="adaptive-problem-level">

                {
                  difficultyLabel(
                    adaptivePlan
                      .next_problem
                      .difficulty,
                  )
                }

              </div>
            )}

          </div>


          <p>
            Your attempts in {
              selectedTopic.title
            } affect only this
            topic's learning profile.
          </p>


          {error && (

            <div className="error-message">
              {error}
            </div>

          )}


          <button
            type="button"
            className="primary-button start-learning-button"

            disabled={
              loading
            }

            onClick={
              handleStart
            }
          >

            {
              loading
                ? "Preparing..."
                : "Start practice"
            }


            {!loading
              && (
              <ArrowRight
                size={19}
              />
            )}

          </button>

        </div>
      )}


      {/* =============================
          Learn
      ============================== */}

      {mode
        === "LEARN"
        && (

        <div className="problem-entry-card surface-card">

          <span className="field-label">
            Concept
          </span>


          <div className="adaptive-next-problem">

            <div>

              <span>
                Learn first
              </span>


              <strong>
                {
                  selectedTopic.title
                }
              </strong>

            </div>

          </div>


          <p>
            LearnFirst will begin
            with {
              selectedTopic.title
            } as a concept. When
            you're ready, request
            a practice problem.
          </p>


          {error && (

            <div className="error-message">
              {error}
            </div>

          )}


          <button
            type="button"
            className="primary-button start-learning-button"

            disabled={
              loading
            }

            onClick={
              handleStart
            }
          >

            {
              loading
                ? "Preparing..."
                : "Start learning"
            }


            {!loading
              && (
              <ArrowRight
                size={19}
              />
            )}

          </button>

        </div>
      )}

    </div>
  );
}
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
  getStudentCurriculumPath,
} from "../api/curriculum";

import {
  createLearningSession,
} from "../api/sessions";

import {
  getMathTopic,
} from "../data/mathTopics";

import type {
  AdaptiveActivity,
  AdaptivePlan,
} from "../types/adaptive";

import type {
  StudentCurriculumPath,
} from "../types/curriculum";

import type {
  LearningMode,
} from "../types/session";

import {
  getStoredStudent,
} from "../utils/studentStorage";


const modes = [
  {
    value:
      "LEARN" as LearningMode,

    title:
      "Learn",

    description:
      (
        "Understand the concept "
        + "before moving into "
        + "independent practice."
      ),

    icon:
      Lightbulb,
  },


  {
    value:
      "PRACTICE" as LearningMode,

    title:
      "Practice",

    description:
      (
        "Solve adaptive problems "
        + "at your current "
        + "curriculum level."
      ),

    icon:
      BookOpenCheck,
  },


  {
    value:
      "HOMEWORK_HELP" as LearningMode,

    title:
      "Homework Help",

    description:
      (
        "Bring a problem from "
        + "your current Math topic."
      ),

    icon:
      PencilLine,
  },
];


function fallbackConceptForAge(
  age: number,
): string {

  if (
    age <= 7
  ) {

    return (
      "MATH_ARITH_BASIC_01"
    );
  }


  if (
    age === 8
  ) {

    return (
      "MATH_ARITH_MULTDIV_01"
    );
  }


  if (
    age === 9
  ) {

    return (
      "MATH_ARITH_FRAC_01"
    );
  }


  if (
    age === 10
  ) {

    return (
      "MATH_ARITH_INT_01"
    );
  }


  if (
    age === 11
  ) {

    return (
      "MATH_ARITH_ORDER_01"
    );
  }


  if (
    age === 12
  ) {

    return (
      "MATH_PREALG_EXPR_01"
    );
  }


  if (
    age === 13
  ) {

    return (
      "MATH_ALG_LINEAR_01"
    );
  }


  return (
    "MATH_GRAPH_LINEAR_01"
  );
}


function readableLabel(
  value: string,
): string {

  return (
    value
      .replace(
        /_/g,
        " ",
      )
      .toLowerCase()
      .replace(
        /\b\w/g,
        (
          character,
        ) =>
          character
            .toUpperCase(),
      )
  );
}


function activityTitle(
  activity:
    AdaptiveActivity,
): string {

  switch (
    activity
  ) {

    case "TAKE_DIAGNOSTIC":

      return (
        "Check your starting level"
      );


    case "GUIDED_PRACTICE":

      return (
        "Guided practice"
      );


    case "INDEPENDENT_PRACTICE":

      return (
        "Independent practice"
      );


    case "REVIEW_FOUNDATION":

      return (
        "Review the foundation"
      );


    case "TAKE_MASTERY_CHECK":

      return (
        "Take a mastery check"
      );


    case "CHALLENGE_PRACTICE":

      return (
        "Challenge practice"
      );
  }
}


function activityDescription(
  activity:
    AdaptiveActivity,
): string {

  switch (
    activity
  ) {

    case "TAKE_DIAGNOSTIC":

      return (
        "Take a short diagnostic "
        + "so LearnFirst can establish "
        + "your starting level."
      );


    case "GUIDED_PRACTICE":

      return (
        "Continue with practice "
        + "while LearnFirst provides "
        + "guided support."
      );


    case "INDEPENDENT_PRACTICE":

      return (
        "Your current evidence suggests "
        + "you are ready to work more "
        + "independently."
      );


    case "REVIEW_FOUNDATION":

      return (
        "Review the concept before "
        + "moving back into harder "
        + "practice."
      );


    case "TAKE_MASTERY_CHECK":

      return (
        "Your recent work suggests "
        + "you are ready to check "
        + "your mastery."
      );


    case "CHALLENGE_PRACTICE":

      return (
        "Your understanding is strong. "
        + "Try a more challenging "
        + "problem."
      );
  }
}


function activityIcon(
  activity:
    AdaptiveActivity,
) {

  switch (
    activity
  ) {

    case "TAKE_DIAGNOSTIC":

      return (
        ClipboardCheck
      );


    case "TAKE_MASTERY_CHECK":

      return (
        Trophy
      );


    case "CHALLENGE_PRACTICE":

      return (
        Sparkles
      );


    case "REVIEW_FOUNDATION":

      return (
        Lightbulb
      );


    case "INDEPENDENT_PRACTICE":

      return (
        Target
      );


    default:

      return (
        BrainCircuit
      );
  }
}


export default function MathStartPage() {

  const navigate =
    useNavigate();


  const student =
    getStoredStudent();


  const studentId =
    student?.id;


  const learnerAge =
    student?.age
    ?? 7;


  const fallbackConceptCode =
    fallbackConceptForAge(
      learnerAge,
    );


  const [
    curriculum,
    setCurriculum,
  ] = useState<
    StudentCurriculumPath | null
  >(
    null,
  );


  const [
    curriculumLoading,
    setCurriculumLoading,
  ] = useState(
    true,
  );


  const [
    curriculumError,
    setCurriculumError,
  ] = useState<
    string | null
  >(
    null,
  );


  const conceptCode =
    curriculum
      ?.recommended_concept
      ?.concept_code

    ?? fallbackConceptCode;


  const selectedTopic =
    getMathTopic(
      conceptCode,
    );


  const [
    adaptivePlan,
    setAdaptivePlan,
  ] = useState<
    AdaptivePlan | null
  >(
    null,
  );


  const [
    adaptiveLoading,
    setAdaptiveLoading,
  ] = useState(
    false,
  );


  const [
    adaptiveError,
    setAdaptiveError,
  ] = useState<
    string | null
  >(
    null,
  );


  const [
    mode,
    setMode,
  ] = useState<
    LearningMode
  >(
    "LEARN",
  );


  const [
    problem,
    setProblem,
  ] = useState(
    "",
  );


  const [
    starting,
    setStarting,
  ] = useState(
    false,
  );


  const [
    error,
    setError,
  ] = useState<
    string | null
  >(
    null,
  );


  // ======================================
  // Curriculum
  // ======================================

  const loadCurriculum =
    async () => {

      if (
        !studentId
      ) {

        navigate(
          "/login",
        );

        return;
      }


      setCurriculumLoading(
        true,
      );


      setCurriculumError(
        null,
      );


      try {

        const data =
          await getStudentCurriculumPath(
            studentId,
            "MATH",
          );


        setCurriculum(
          data,
        );


      } catch (err) {

        setCurriculumError(
          err instanceof Error
            ? err.message
            : (
              "Could not load your "
              + "curriculum path."
            ),
        );


      } finally {

        setCurriculumLoading(
          false,
        );
      }
    };


  useEffect(
    () => {

      void loadCurriculum();

    },
    [
      studentId,
    ],
  );


  // ======================================
  // Adaptive plan
  // ======================================

  const loadAdaptivePlan =
    async () => {

      if (
        !studentId
      ) {

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
              + "adaptive Math plan."
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

      setAdaptivePlan(
        null,
      );


      setProblem(
        "",
      );


      void loadAdaptivePlan();

    },
    [
      studentId,
      conceptCode,
    ],
  );


  // ======================================
  // Adaptive recommended action
  // ======================================

  const handleAdaptiveStart =
    async () => {

      if (
        !student
        || !adaptivePlan
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


      const learningMode:
        LearningMode = (
          adaptivePlan
            .next_activity
          === "REVIEW_FOUNDATION"
        )
          ? "LEARN"
          : "PRACTICE";


      const currentProblem =
        learningMode
        === "PRACTICE"

          ? (
            adaptivePlan
              .next_problem
              ?.prompt

            ?? selectedTopic
              .sampleProblems[0]
          )

          : null;


      setStarting(
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
              learningMode,

            subject:
              "MATH",

            topic:
              selectedTopic.title,

            concept_code:
              conceptCode,

            current_problem:
              currentProblem,
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
              "Could not start the "
              + "recommended activity."
            ),
        );


      } finally {

        setStarting(
          false,
        );
      }
    };


  // ======================================
  // Manual learning mode
  // ======================================

  const handleStart =
    async () => {

      if (
        !student
      ) {

        navigate(
          "/login",
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
            + "before starting."
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


      setStarting(
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
              selectedTopic.title,

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

        setStarting(
          false,
        );
      }
    };


  const AdaptiveIcon =
    adaptivePlan
      ? (
        activityIcon(
          adaptivePlan
            .next_activity,
        )
      )
      : BrainCircuit;


  if (
    curriculumLoading
  ) {

    return (

      <div className="adaptive-loading-card surface-card">

        <div className="adaptive-loading-icon">

          <BrainCircuit
            size={24}
          />

        </div>


        <div>

          <strong>
            Finding your Math level...
          </strong>


          <span>
            Checking your age,
            grade and learning history.
          </span>

        </div>

      </div>
    );
  }


  return (

    <div className="math-start-page">

      {/* =============================
          Back
      ============================== */}

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


      {/* =============================
          Header
      ============================== */}

      <section className="math-start-header">

        <div className="math-start-icon">

          <Calculator
            size={30}
          />

        </div>


        <div>

          <span>
            Age-adaptive Math
          </span>


          <h1>
            Your next Math step
          </h1>


          <p>
            LearnFirst selects your
            starting curriculum using
            age and grade, then adjusts
            it using your actual
            learning evidence.
          </p>

        </div>

      </section>


      {/* =============================
          Curriculum position
      ============================== */}

      <section className="adaptive-section">

        <div className="adaptive-section-heading">

          <div>

            <span className="adaptive-eyebrow">

              <Target
                size={15}
              />

              Curriculum progression

            </span>


            <h2>
              Your current level
            </h2>

          </div>


          <button
            type="button"
            className="adaptive-refresh-button"

            disabled={
              curriculumLoading
            }

            onClick={() =>
              void loadCurriculum()
            }
          >

            <RefreshCcw
              size={16}
            />

            Refresh

          </button>

        </div>


        <div className="adaptive-plan-card surface-card">

          <div className="adaptive-plan-main">

            <div className="adaptive-plan-icon">

              <Calculator
                size={28}
              />

            </div>


            <div className="adaptive-plan-copy">

              <span>
                Current curriculum concept
              </span>


              <h3>
                {
                  selectedTopic.title
                }
              </h3>


              <p>
                {
                  selectedTopic.description
                }
              </p>

            </div>

          </div>


          <div className="adaptive-profile-grid">

            <div>

              <Target
                size={18}
              />

              <span>
                Learner age
              </span>


              <strong>
                {
                  learnerAge
                }
              </strong>

            </div>


            <div>

              <Calculator
                size={18}
              />

              <span>
                Expected level
              </span>


              <strong>

                {
                  curriculum
                    ?.target_concept
                    ?.title

                  ?? selectedTopic
                    .title
                }

              </strong>

            </div>


            <div>

              <BrainCircuit
                size={18}
              />

              <span>
                Current status
              </span>


              <strong>

                {
                  readableLabel(
                    curriculum
                      ?.recommended_concept
                      ?.status

                    ?? "READY",
                  )
                }

              </strong>

            </div>

          </div>


          {curriculum
            ?.prerequisite_review_concept
            && (

            <div className="adaptive-score-note">

              <span>
                Prerequisite review
              </span>


              <strong>

                {
                  curriculum
                    .prerequisite_review_concept
                    .title
                }

              </strong>

            </div>

          )}


          <div className="adaptive-plan-footer">

            <p>

              {
                curriculum
                  ?.prerequisite_review_concept

                  ? (
                    "LearnFirst found "
                    + "evidence of an earlier "
                    + "skill gap. This skill "
                    + "is being reviewed before "
                    + "you continue forward."
                  )

                  : (
                    "No demonstrated "
                    + "prerequisite gap is "
                    + "blocking your current "
                    + "Math level."
                  )
              }

            </p>

          </div>

        </div>


        {curriculumError && (

          <div className="adaptive-error">

            {curriculumError}

          </div>

        )}

      </section>


      {/* =============================
          Adaptive recommendation
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
              Recommended activity
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
                Building your plan...
              </strong>


              <span>
                Checking your progress
                in {
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
                    activityTitle(
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
                    readableLabel(
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
                    readableLabel(
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
                    readableLabel(
                      adaptivePlan
                        .explanation_depth,
                    )
                  }

                </strong>

              </div>

            </div>


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
                    readableLabel(
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
                  adaptivePlan.summary
                }
              </p>


              <button
                type="button"
                className="primary-button adaptive-start-button"

                disabled={
                  starting
                }

                onClick={() =>
                  void handleAdaptiveStart()
                }
              >

                {
                  starting
                    ? "Preparing..."
                    : adaptivePlan
                      .next_activity
                    === "TAKE_DIAGNOSTIC"
                      ? "Start diagnostic"
                      : adaptivePlan
                        .next_activity
                      === "TAKE_MASTERY_CHECK"
                        ? "Start mastery check"
                        : "Start recommended activity"
                }


                {!starting && (

                  <ArrowRight
                    size={18}
                  />

                )}

              </button>

            </div>

          </div>

        )}


        {adaptiveError && (

          <div className="adaptive-error">

            {adaptiveError}

          </div>

        )}

      </section>


      {/* =============================
          Diagnostic
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
            A diagnostic gives
            LearnFirst stronger
            evidence for adaptation.
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
          Mode
      ============================== */}

      <section className="math-start-section">

        <div className="section-number">
          1
        </div>


        <div>

          <h2>
            Choose a learning mode
          </h2>


          <p>
            The curriculum topic is
            chosen for you. You choose
            how you want to work with it.
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
          Selected mode content
      ============================== */}

      <section className="math-start-section problem-section-heading">

        <div className="section-number">
          2
        </div>


        <div>

          <h2>

            {
              mode
              === "HOMEWORK_HELP"

                ? "Enter your problem"

                : mode
                === "PRACTICE"

                  ? (
                    "Practice "
                    + selectedTopic.title
                  )

                  : (
                    "Learn "
                    + selectedTopic.title
                  )
            }

          </h2>


          <p>
            Current curriculum topic:
            {" "}
            <strong>
              {
                selectedTopic.title
              }
            </strong>
          </p>

        </div>

      </section>


      {/* =============================
          Homework
      ============================== */}

      {mode
        === "HOMEWORK_HELP"
        && (

        <div className="problem-entry-card surface-card">

          <label
            className="field-label"
            htmlFor="math-problem"
          >

            {
              selectedTopic.title
            }
            {" "}
            problem

          </label>


          <input
            id="math-problem"

            className="math-problem-input"

            value={
              problem
            }

            placeholder={
              (
                "Example: "
                + selectedTopic
                  .sampleProblems[0]
              )
            }

            onChange={(event) =>
              setProblem(
                event
                  .target
                  .value,
              )
            }
          />


          <div className="problem-suggestions">

            <span>
              Examples
            </span>


            <div>

              {selectedTopic
                .sampleProblems
                .map(
                  (
                    example,
                  ) => (

                    <button
                      key={
                        example
                      }

                      type="button"

                      onClick={() =>
                        setProblem(
                          example,
                        )
                      }
                    >

                      {example}

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

            disabled={
              starting
            }

            onClick={() =>
              void handleStart()
            }
          >

            {
              starting
                ? "Preparing..."
                : "Start homework help"
            }


            {!starting && (

              <ArrowRight
                size={18}
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
            Adaptive practice problem
          </span>


          <div className="adaptive-next-problem">

            <div>

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

          </div>


          {error && (

            <div className="error-message">

              {error}

            </div>

          )}


          <button
            type="button"

            className="primary-button start-learning-button"

            disabled={
              starting
            }

            onClick={() =>
              void handleStart()
            }
          >

            {
              starting
                ? "Preparing..."
                : "Start practice"
            }


            {!starting && (

              <ArrowRight
                size={18}
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
            Current concept
          </span>


          <div className="adaptive-next-problem">

            <div>

              <strong>
                {
                  selectedTopic.title
                }
              </strong>

            </div>

          </div>


          <p>
            LearnFirst will first
            teach the concept, then
            move you toward independent
            practice.
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
              starting
            }

            onClick={() =>
              void handleStart()
            }
          >

            {
              starting
                ? "Preparing..."
                : "Start learning"
            }


            {!starting && (

              <ArrowRight
                size={18}
              />

            )}

          </button>

        </div>

      )}

    </div>
  );
}
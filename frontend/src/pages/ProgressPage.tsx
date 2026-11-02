import {
  ArrowRight,
  BrainCircuit,
  CheckCircle2,
  Gauge,
  Lightbulb,
  RefreshCcw,
  Sparkles,
  Target,
  TrendingUp,
  Trophy,
} from "lucide-react";

import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  useNavigate,
  useSearchParams,
} from "react-router";

import {
  getConceptProgress,
} from "../api/assessments";

import {
  MATH_TOPICS,
  getMathTopic,
} from "../data/mathTopics";

import type {
  ConceptProgress,
  DifficultyLevel,
  MasteryState,
} from "../types/assessment";

import {
  getStoredStudent,
} from "../utils/studentStorage";


function masteryLabel(
  mastery: MasteryState,
): string {

  switch (
    mastery
  ) {

    case "STRONG":
      return "Strong";

    case "DEVELOPING":
      return "Developing";

    case "LEARNING":
      return "Learning";

    default:
      return "Not started";
  }
}


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


function masteryMessage(
  mastery: MasteryState,
  topicTitle: string,
): string {

  switch (
    mastery
  ) {

    case "STRONG":

      return (
        "You are showing strong "
        + "understanding of "
        + topicTitle
        + "."
      );


    case "DEVELOPING":

      return (
        "You're developing your "
        + "understanding of "
        + topicTitle
        + ". Keep practicing "
        + "independently."
      );


    case "LEARNING":

      return (
        "You're still learning "
        + topicTitle
        + ". Mistakes and retries "
        + "are part of the process."
      );


    default:

      return (
        "Take the topic diagnostic "
        + "to establish your "
        + "starting level."
      );
  }
}


export default function ProgressPage() {

  const navigate =
    useNavigate();


  const [
    searchParams,
    setSearchParams,
  ] = useSearchParams();


  const student =
    getStoredStudent();


  const topic =
    getMathTopic(
      searchParams.get(
        "concept",
      ),
    );


  const [
    progress,
    setProgress,
  ] = useState<
    ConceptProgress | null
  >(null);


  const [
    loading,
    setLoading,
  ] = useState(
    true,
  );


  const [
    error,
    setError,
  ] = useState<
    string | null
  >(null);


  const loadProgress =
    async () => {

      if (
        !student
      ) {

        navigate(
          "/setup",
        );

        return;
      }


      setLoading(
        true,
      );


      setError(
        null,
      );


      try {

        const data =
          await getConceptProgress(
            student.id,
            topic
              .conceptCode,
          );


        setProgress(
          data,
        );


      } catch (err) {

        setError(
          err instanceof Error
            ? err.message
            : (
              "Could not load "
              + "your progress."
            ),
        );


      } finally {

        setLoading(
          false,
        );
      }
    };


  useEffect(
    () => {

      void loadProgress();

    },
    [
      topic.conceptCode,
    ],
  );


  const learningMetrics =
    progress
      ?.learning_metrics;


  const hasLearningActivity =
    useMemo(
      () => {

        if (
          !progress
        ) {

          return false;
        }


        return Boolean(
          progress.diagnostic

          || progress.mastery

          || progress
            .learning_metrics
            .total_attempts
            > 0
        );
      },

      [
        progress,
      ],
    );


  if (
    loading
  ) {

    return (

      <div className="progress-loading">

        <div className="progress-loading-icon">

          <TrendingUp
            size={30}
          />

        </div>


        <strong>
          Loading {
            topic.title
          } progress...
        </strong>

      </div>
    );
  }


  if (
    error
  ) {

    return (

      <div className="progress-error surface-card">

        <RefreshCcw
          size={32}
        />


        <h2>
          We couldn't load
          your progress.
        </h2>


        <p>
          {error}
        </p>


        <button
          type="button"
          className="primary-button"

          onClick={() =>
            void loadProgress()
          }
        >
          Try again
        </button>

      </div>
    );
  }


  if (
    !progress
  ) {

    return null;
  }


  const diagnosticScore =
    progress
      .diagnostic
      ?.score_percent
    ?? null;


  const masteryScore =
    progress
      .mastery
      ?.score_percent
    ?? null;


  const gain =
    progress
      .score_gain_percentage_points;


  const mastery =
    progress
      .current_mastery_state;


  const difficulty =
    progress
      .recommended_difficulty;


  return (

    <div className="progress-page">

      <header className="progress-page-header">

        <div>

          <div className="progress-kicker">

            <Sparkles
              size={16}
            />

            Math progress

          </div>


          <h1>
            {
              topic.title
            }
          </h1>


          <p>
            Each Math concept keeps
            independent progress,
            mastery and learning
            metrics.
          </p>

        </div>


        <button
          type="button"
          className="secondary-button"

          onClick={() =>
            void loadProgress()
          }
        >
          <RefreshCcw
            size={17}
          />

          Refresh
        </button>

      </header>


      {/* =============================
          Topic selector
      ============================== */}

      <section className="progress-section-heading">

        <div>

          <span className="small-label">
            Math topics
          </span>


          <h2>
            View another topic
          </h2>

        </div>

      </section>


      <div className="learning-mode-grid">

        {MATH_TOPICS.map(
          (
            item,
          ) => {

            const selected =
              item.conceptCode
              === topic
                .conceptCode;


            return (

              <button
                key={
                  item.conceptCode
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
                  setSearchParams({
                    concept:
                      item
                        .conceptCode,
                  })
                }
              >

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


      {!hasLearningActivity
        ? (

          <section className="empty-progress surface-card">

            <div className="empty-progress-icon">

              <Target
                size={34}
              />

            </div>


            <h2>
              No {
                topic.title
              } progress yet.
            </h2>


            <p>
              Take a short diagnostic
              to create a starting
              profile for this topic.
            </p>


            <button
              type="button"
              className="primary-button"

              onClick={() =>
                navigate(
                  (
                    "/assessments/math/diagnostic"
                    + `?concept=${topic.conceptCode}`
                  ),
                )
              }
            >
              Check my starting level

              <ArrowRight
                size={18}
              />
            </button>

          </section>

        )
        : (

          <>

            <section className="progress-summary-grid">

              <article className="progress-summary-card diagnostic-summary">

                <div className="summary-card-icon">

                  <Target
                    size={23}
                  />

                </div>


                <span>
                  Starting score
                </span>


                <strong>

                  {
                    diagnosticScore
                    !== null

                      ? (
                        `${diagnosticScore}%`
                      )

                      : "—"
                  }

                </strong>


                <p>
                  Diagnostic
                </p>

              </article>


              <article className="progress-summary-card mastery-summary">

                <div className="summary-card-icon">

                  <Trophy
                    size={23}
                  />

                </div>


                <span>
                  Mastery score
                </span>


                <strong>

                  {
                    masteryScore
                    !== null

                      ? (
                        `${masteryScore}%`
                      )

                      : "—"
                  }

                </strong>


                <p>
                  Mastery check
                </p>

              </article>


              <article className="progress-summary-card gain-summary">

                <div className="summary-card-icon">

                  <TrendingUp
                    size={23}
                  />

                </div>


                <span>
                  Observed gain
                </span>


                <strong>

                  {
                    gain !== null

                      ? (
                        (
                          gain > 0
                            ? "+"
                            : ""
                        )
                        + gain
                      )

                      : "—"
                  }

                </strong>


                <p>
                  Percentage points
                </p>

              </article>


              <article className="progress-summary-card level-summary">

                <div className="summary-card-icon">

                  <BrainCircuit
                    size={23}
                  />

                </div>


                <span>
                  Current level
                </span>


                <strong className="level-text">

                  {
                    masteryLabel(
                      mastery,
                    )
                  }

                </strong>


                <p>
                  Topic mastery
                </p>

              </article>

            </section>


            <section className="progress-content-grid">

              <article className="surface-card score-journey-card">

                <div className="progress-card-title">

                  <div>

                    <span className="small-label">
                      Score journey
                    </span>


                    <h2>
                      Starting point
                      to mastery
                    </h2>

                  </div>


                  <TrendingUp
                    size={27}
                  />

                </div>


                <div className="score-journey">

                  <div className="score-stage">

                    <div className="score-stage-heading">

                      <span>
                        Diagnostic
                      </span>


                      <strong>

                        {
                          diagnosticScore
                          !== null

                            ? (
                              `${diagnosticScore}%`
                            )

                            : "Not taken"
                        }

                      </strong>

                    </div>


                    <div className="score-track">

                      <div
                        style={{
                          width:
                            (
                              `${diagnosticScore ?? 0}%`
                            ),
                        }}
                      />

                    </div>

                  </div>


                  <div className="journey-arrow">

                    <ArrowRight
                      size={21}
                    />

                  </div>


                  <div className="score-stage">

                    <div className="score-stage-heading">

                      <span>
                        Mastery
                      </span>


                      <strong>

                        {
                          masteryScore
                          !== null

                            ? (
                              `${masteryScore}%`
                            )

                            : "Not taken"
                        }

                      </strong>

                    </div>


                    <div className="score-track mastery-track">

                      <div
                        style={{
                          width:
                            (
                              `${masteryScore ?? 0}%`
                            ),
                        }}
                      />

                    </div>

                  </div>

                </div>


                {gain !== null && (

                  <div
                    className={
                      gain > 0
                        ? (
                          "progress-gain-message "
                          + "positive"
                        )
                        : (
                          "progress-gain-message"
                        )
                    }
                  >

                    <Sparkles
                      size={18}
                    />


                    <div>

                      <strong>

                        {
                          gain > 0
                            ? `+${gain}`
                            : gain
                        }

                        {" "}
                        percentage points

                      </strong>


                      <span>
                        Observed change
                        between your two
                        LearnFirst
                        assessments.
                      </span>

                    </div>

                  </div>
                )}


                <p className="score-disclaimer">
                  These scores describe
                  performance inside
                  LearnFirst and are
                  not school grades.
                </p>

              </article>


              <article className="surface-card mastery-overview-card">

                <div className="mastery-overview-icon">

                  <BrainCircuit
                    size={26}
                  />

                </div>


                <span className="small-label">
                  Current understanding
                </span>


                <h2>

                  {
                    masteryLabel(
                      mastery,
                    )
                  }

                </h2>


                <p>

                  {
                    masteryMessage(
                      mastery,
                      topic.title,
                    )
                  }

                </p>


                <div className="difficulty-box">

                  <div>

                    <Gauge
                      size={19}
                    />


                    <span>
                      Recommended
                      next difficulty
                    </span>

                  </div>


                  <strong>

                    {
                      difficultyLabel(
                        difficulty,
                      )
                    }

                  </strong>

                </div>


                <button
                  type="button"
                  className="primary-button mastery-practice-button"

                  onClick={() =>
                    navigate(
                      (
                        "/learn/math"
                        + `?concept=${topic.conceptCode}`
                      ),
                    )
                  }
                >
                  Practice {
                    topic.shortTitle
                  }

                  <ArrowRight
                    size={18}
                  />
                </button>

              </article>

            </section>


            <section className="progress-section-heading">

              <div>

                <span className="small-label">
                  Learning independence
                </span>


                <h2>
                  How you are learning
                </h2>


                <p>
                  These metrics apply
                  specifically to {
                    topic.title
                  }.
                </p>

              </div>

            </section>


            <section className="learning-metrics-grid">

              <article className="learning-metric-card surface-card">

                <div className="metric-icon purple-metric">

                  <BrainCircuit
                    size={22}
                  />

                </div>


                <strong>

                  {
                    learningMetrics
                      ?.total_attempts
                    ?? 0
                  }

                </strong>


                <span>
                  Total attempts
                </span>


                <p>
                  Every serious try
                  counts as learning.
                </p>

              </article>


              <article className="learning-metric-card surface-card">

                <div className="metric-icon blue-metric">

                  <Target
                    size={22}
                  />

                </div>


                <strong>

                  {
                    learningMetrics
                      ?.independent_attempts
                    ?? 0
                  }

                </strong>


                <span>
                  Independent tries
                </span>


                <p>
                  Attempts made with
                  little or no help.
                </p>

              </article>


              <article className="learning-metric-card surface-card">

                <div className="metric-icon green-metric">

                  <CheckCircle2
                    size={22}
                  />

                </div>


                <strong>

                  {
                    learningMetrics
                      ?.independent_success_rate
                    ?? 0
                  }
                  %

                </strong>


                <span>
                  Independent success
                </span>


                <p>
                  Success among
                  independent attempts.
                </p>

              </article>


              <article className="learning-metric-card surface-card">

                <div className="metric-icon orange-metric">

                  <RefreshCcw
                    size={22}
                  />

                </div>


                <strong>

                  {
                    learningMetrics
                      ?.retry_success_count
                    ?? 0
                  }

                </strong>


                <span>
                  Retry wins
                </span>


                <p>
                  Times you recovered
                  after a mistake.
                </p>

              </article>

            </section>


            <section className="progress-content-grid lower-progress-grid">

              <article className="surface-card support-usage-card">

                <div className="progress-card-title">

                  <div>

                    <span className="small-label">
                      Support usage
                    </span>


                    <h2>
                      How much help
                      did you need?
                    </h2>

                  </div>


                  <Lightbulb
                    size={26}
                  />

                </div>


                <div className="support-stat-row">

                  <div>

                    <span>
                      Independent
                      attempt rate
                    </span>


                    <strong>

                      {
                        learningMetrics
                          ?.independent_attempt_rate
                        ?? 0
                      }
                      %

                    </strong>

                  </div>


                  <div className="mini-metric-track">

                    <div
                      style={{
                        width:
                          (
                            `${Math.min(
                              learningMetrics
                                ?.independent_attempt_rate
                                ?? 0,
                              100,
                            )}%`
                          ),
                      }}
                    />

                  </div>

                </div>


                <div className="support-stat-row">

                  <div>

                    <span>
                      Average hint level
                    </span>


                    <strong>

                      {
                        learningMetrics
                          ?.average_hint_level
                        ?? 0
                      }
                      /7

                    </strong>

                  </div>


                  <div className="mini-metric-track hint-metric-track">

                    <div
                      style={{
                        width:
                          (
                            `${Math.min(
                              (
                                (
                                  learningMetrics
                                    ?.average_hint_level
                                  ?? 0
                                )
                                / 7
                              )
                              * 100,
                              100,
                            )}%`
                          ),
                      }}
                    />

                  </div>

                </div>


                <div className="support-stat-row">

                  <div>

                    <span>
                      Correct attempts
                    </span>


                    <strong>

                      {
                        learningMetrics
                          ?.correct_attempts
                        ?? 0
                      }

                    </strong>

                  </div>

                </div>

              </article>


              <article className="surface-card answer-independence-card">

                <div className="answer-independence-icon">

                  <Lightbulb
                    size={25}
                  />

                </div>


                <span className="small-label">
                  Think-first habit
                </span>


                <h2>

                  {
                    learningMetrics
                      ?.direct_answer_requests
                    ?? 0
                  }

                  {" "}

                  direct answer

                  {
                    (
                      learningMetrics
                        ?.direct_answer_requests
                      ?? 0
                    )
                    === 1

                      ? " request"

                      : " requests"
                  }

                </h2>


                <p>
                  LearnFirst uses this
                  signal together with
                  attempts, hints and
                  mastery—not by itself.
                </p>


                <div className="think-first-note">
                  🌱 The goal is
                  gradually needing
                  less support as
                  understanding grows.
                </div>

              </article>

            </section>

          </>

        )}

    </div>
  );
}
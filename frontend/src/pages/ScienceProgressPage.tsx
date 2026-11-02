import {
  ArrowRight,
  BrainCircuit,
  CheckCircle2,
  Clock3,
  FlaskConical,
  Gauge,
  Lightbulb,
  RefreshCcw,
  Sparkles,
  Target,
  TriangleAlert,
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
  getScienceAdaptivePlan,
} from "../api/scienceAdaptive";

import {
  SCIENCE_TOPICS,
  getScienceTopic,
} from "../data/scienceTopics";

import type {
  MasteryState,
} from "../types/assessment";

import type {
  ScienceAdaptivePlan,
} from "../types/scienceAdaptive";

import {
  getStoredStudent,
} from "../utils/studentStorage";


function masteryLabel(
  mastery:
    MasteryState,
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


function paceLabel(
  pace: string,
): string {

  switch (
    pace
  ) {

    case "FAST":

      return "Faster than usual";


    case "SLOW":

      return "Slower than usual";


    case "TYPICAL":

      return "Typical pace";


    default:

      return "Not enough data";
  }
}


export default function ScienceProgressPage() {

  const navigate =
    useNavigate();


  const [
    searchParams,
    setSearchParams,
  ] = useSearchParams();


  const student =
    getStoredStudent();


  const topic =
    getScienceTopic(
      searchParams.get(
        "concept",
      ),
    );


  const [
    plan,
    setPlan,
  ] = useState<
    ScienceAdaptivePlan | null
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
          await getScienceAdaptivePlan(
            student.id,
            topic.conceptCode,
          );


        setPlan(
          data,
        );


      } catch (err) {

        setError(
          err instanceof Error
            ? err.message
            : (
              "Could not load "
              + "Science progress."
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


  if (
    loading
  ) {

    return (

      <div className="progress-loading">

        <div className="progress-loading-icon">

          <FlaskConical
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
          Science progress.
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
    !plan
  ) {

    return null;
  }


  return (

    <div className="progress-page">

      <header className="progress-page-header">

        <div>

          <div className="progress-kicker">

            <Sparkles
              size={16}
            />

            Science progress

          </div>


          <h1>
            {
              topic.title
            }
          </h1>


          <p>
            See what LearnFirst has
            observed from your Science
            explanations, independent
            attempts and support usage.
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
            Science topics
          </span>


          <h2>
            View another concept
          </h2>

        </div>

      </section>


      <div className="science-topic-grid">

        {SCIENCE_TOPICS.map(
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
                      "science-topic-card "
                      + "selected"
                    )
                    : (
                      "science-topic-card"
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

                <div className="science-topic-icon">

                  <FlaskConical
                    size={24}
                  />

                </div>


                <h3>
                  {
                    item.title
                  }
                </h3>


                <p>
                  {
                    item.description
                  }
                </p>


                <div className="science-topic-select">

                  {
                    selected
                      ? "Viewing ✓"
                      : "View progress"
                  }

                </div>

              </button>
            );
          },
        )}

      </div>


      {/* =============================
          Summary
      ============================== */}

      <section className="progress-summary-grid">

        <article className="progress-summary-card diagnostic-summary">

          <div className="summary-card-icon">

            <BrainCircuit
              size={23}
            />

          </div>


          <span>
            Understanding signal
          </span>


          <strong>
            {
              plan
                .understanding_score_percent
            }
            %
          </strong>


          <p>
            Correct + partial
            explanations
          </p>

        </article>


        <article className="progress-summary-card mastery-summary">

          <div className="summary-card-icon">

            <Trophy
              size={23}
            />

          </div>


          <span>
            Mastery signal
          </span>


          <strong className="level-text">

            {
              masteryLabel(
                plan
                  .mastery_state,
              )
            }

          </strong>


          <p>
            LearnFirst internal
            mastery state
          </p>

        </article>


        <article className="progress-summary-card gain-summary">

          <div className="summary-card-icon">

            <CheckCircle2
              size={23}
            />

          </div>


          <span>
            Independent success
          </span>


          <strong>
            {
              plan
                .independent_success_rate
            }
            %
          </strong>


          <p>
            Success without
            heavy support
          </p>

        </article>


        <article className="progress-summary-card level-summary">

          <div className="summary-card-icon">

            <Gauge
              size={23}
            />

          </div>


          <span>
            Current difficulty
          </span>


          <strong className="level-text">

            {
              plan.difficulty
            }

          </strong>


          <p>
            Adaptive question level
          </p>

        </article>

      </section>


      {/* =============================
          Mastery explanation
      ============================== */}

      <section className="progress-content-grid">

        <article className="surface-card score-journey-card">

          <div className="progress-card-title">

            <div>

              <span className="small-label">
                Science mastery
              </span>


              <h2>
                Why is my level
                {
                  " "
                }
                {
                  masteryLabel(
                    plan
                      .mastery_state,
                  )
                }
                ?
              </h2>

            </div>


            <BrainCircuit
              size={27}
            />

          </div>


          <p className="score-disclaimer">

            {
              plan
                .mastery_explanation
            }

          </p>


          <div className="score-journey">

            <div className="score-stage">

              <div className="score-stage-heading">

                <span>
                  Understanding
                </span>


                <strong>
                  {
                    plan
                      .understanding_score_percent
                  }
                  %
                </strong>

              </div>


              <div className="score-track">

                <div
                  style={{
                    width:
                      (
                        `${Math.min(
                          plan
                            .understanding_score_percent,
                          100,
                        )}%`
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
                  Independent success
                </span>


                <strong>
                  {
                    plan
                      .independent_success_rate
                  }
                  %
                </strong>

              </div>


              <div className="score-track mastery-track">

                <div
                  style={{
                    width:
                      (
                        `${Math.min(
                          plan
                            .independent_success_rate,
                          100,
                        )}%`
                      ),
                  }}
                />

              </div>

            </div>

          </div>


          <div className="think-first-note">

            Science mastery here is
            an internal LearnFirst
            learning signal. It is
            not a school grade or a
            validated educational
            assessment score.

          </div>

        </article>


        <article className="surface-card mastery-overview-card">

          <div className="mastery-overview-icon">

            <Trophy
              size={26}
            />

          </div>


          <span className="small-label">
            Strong mastery target
          </span>


          <h2>
            What does Strong mean?
          </h2>


          <p>
            LearnFirst marks the
            Science signal Strong
            after enough evidence:
            at least 5 evaluated
            attempts, at least 80%
            understanding evidence,
            at least 60% independent
            attempt rate, and at least
            70% independent success.
          </p>


          <div className="difficulty-box">

            <div>

              <Gauge
                size={19}
              />

              <span>
                Current support
              </span>

            </div>


            <strong>
              {
                plan
                  .support_level
            }
          </strong>

          </div>


          <button
            type="button"
            className="primary-button mastery-practice-button"

            onClick={() =>
              navigate(
                "/learn/science",
              )
            }
          >
            Continue Science

            <ArrowRight
              size={18}
            />

          </button>

        </article>

      </section>


      {/* =============================
          Attempt evidence
      ============================== */}

      <section className="progress-section-heading">

        <div>

          <span className="small-label">
            Evidence
          </span>


          <h2>
            How your Science
            profile is built
          </h2>

        </div>

      </section>


      <section className="learning-metrics-grid">

        <article className="learning-metric-card surface-card">

          <div className="metric-icon purple-metric">

            <Target
              size={22}
            />

          </div>


          <strong>
            {
              plan
                .total_attempts
            }
          </strong>


          <span>
            Evaluated explanations
          </span>


          <p>
            Structured Science
            responses checked by
            concept rubrics.
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
              plan
                .correct_attempts
            }
          </strong>


          <span>
            Strong explanations
          </span>


          <p>
            Responses containing
            enough expected ideas.
          </p>

        </article>


        <article className="learning-metric-card surface-card">

          <div className="metric-icon blue-metric">

            <Lightbulb
              size={22}
            />

          </div>


          <strong>
            {
              plan
                .partial_attempts
            }
          </strong>


          <span>
            Partial explanations
          </span>


          <p>
            Useful understanding
            with important ideas
            still missing.
          </p>

        </article>


        <article className="learning-metric-card surface-card">

          <div className="metric-icon orange-metric">

            <TriangleAlert
              size={22}
            />

          </div>


          <strong>
            {
              plan
                .misconception_count
            }
          </strong>


          <span>
            Misconception signals
          </span>


          <p>
            Selected misconceptions
            detected by the Science
            rubric.
          </p>

        </article>

      </section>


      {/* =============================
          Independence + pace
      ============================== */}

      <section className="progress-content-grid lower-progress-grid">

        <article className="surface-card support-usage-card">

          <div className="progress-card-title">

            <div>

              <span className="small-label">
                Independence
              </span>


              <h2>
                How much support
                are you using?
              </h2>

            </div>


            <Lightbulb
              size={26}
            />

          </div>


          <div className="support-stat-row">

            <div>

              <span>
                Independent attempts
              </span>


              <strong>
                {
                  plan
                    .independent_attempts
                }
              </strong>

            </div>

          </div>


          <div className="support-stat-row">

            <div>

              <span>
                Independent attempt rate
              </span>


              <strong>
                {
                  plan
                    .independent_attempt_rate
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
                        plan
                          .independent_attempt_rate,
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
                  plan
                    .average_hint_level
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
                          plan
                            .average_hint_level
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

        </article>


        <article className="surface-card answer-independence-card">

          <div className="answer-independence-icon">

            <Clock3
              size={25}
            />

          </div>


          <span className="small-label">
            Response pace
          </span>


          <h2>
            {
              paceLabel(
                plan
                  .response_pace,
              )
            }
          </h2>


          <p>

            Source:
            {" "}

            {
              plan
                .response_pace_source
                .replaceAll(
                  "_",
                  " ",
                )
            }

          </p>


          {plan
            .baseline_ready
            && (

            <div className="think-first-note">

              Personal baseline:
              {" "}

              {
                plan
                  .baseline_response_latency_ms
                !== null

                  ? (
                    Math.round(
                      plan
                        .baseline_response_latency_ms
                      / 1000,
                    )
                    + " sec"
                  )

                  : "—"
              }

              <br />

              Recent pace:
              {" "}

              {
                plan
                  .recent_response_latency_ms
                !== null

                  ? (
                    Math.round(
                      plan
                        .recent_response_latency_ms
                      / 1000,
                    )
                    + " sec"
                  )

                  : "—"
              }

            </div>
          )}

        </article>

      </section>


      {/* =============================
          Next recommendation
      ============================== */}

      <section
        className="surface-card"
        style={{
          padding:
            "24px",
        }}
      >

        <span className="small-label">
          Recommended next step
        </span>


        <h2>
          {
            plan
              .next_activity
              .replaceAll(
                "_",
                " ",
              )
          }
        </h2>


        <p
          style={{
            color:
              "var(--color-text-muted)",
          }}
        >
          {
            plan.summary
          }
        </p>


        {plan
          .next_question
          && (

          <div className="difficulty-box">

            <div>

              <FlaskConical
                size={19}
              />

              <span>
                Next question
              </span>

            </div>


            <strong>
              {
                plan
                  .next_question
                  .prompt
              }
            </strong>

          </div>
        )}


        <button
          type="button"
          className="primary-button"

          style={{
            marginTop:
              "18px",
          }}

          onClick={() =>
            navigate(
              "/learn/science",
            )
          }
        >
          Continue learning

          <ArrowRight
            size={18}
          />

        </button>

      </section>

    </div>
  );
}
import {
  ArrowRight,
  BookOpen,
  Calculator,
  Flame,
  FlaskConical,
  Lightbulb,
  Sparkles,
} from "lucide-react";

import {
  useEffect,
  useState,
} from "react";

import {
  useNavigate,
} from "react-router";

import {
  getConceptProgress,
} from "../api/assessments";

import {
  getEnglishProgress,
  type EnglishProgress,
} from "../api/englishProgress";

import {
  getScienceAdaptivePlan,
} from "../api/scienceAdaptive";

import {
  ENGLISH_TOPICS,
} from "../data/englishTopics";

import {
  MATH_TOPICS,
} from "../data/mathTopics";

import {
  SCIENCE_TOPICS,
} from "../data/scienceTopics";

import type {
  ConceptProgress,
} from "../types/assessment";

import type {
  ScienceAdaptivePlan,
} from "../types/scienceAdaptive";

import {
  getStoredStudent,
} from "../utils/studentStorage";


export default function DashboardPage() {

  const navigate =
    useNavigate();


  const student =
    getStoredStudent();


  const studentId =
    student?.id;


  const [
    mathProgress,
    setMathProgress,
  ] = useState<
    ConceptProgress[]
  >([]);


  const [
    scienceProgress,
    setScienceProgress,
  ] = useState<
    ScienceAdaptivePlan[]
  >([]);


  const [
    englishProgress,
    setEnglishProgress,
  ] = useState<
    EnglishProgress[]
  >([]);


  const [
    progressLoading,
    setProgressLoading,
  ] = useState(
    true,
  );


  useEffect(
    () => {

      if (
        !studentId
      ) {

        setProgressLoading(
          false,
        );

        return;
      }


      let cancelled =
        false;


      const loadProgress =
        async () => {

          setProgressLoading(
            true,
          );


          try {

            const [
              mathResults,
              scienceResults,
              englishResults,
            ] = await Promise.all([

              Promise.allSettled(
                MATH_TOPICS.map(
                  (
                    topic,
                  ) =>
                    getConceptProgress(
                      studentId,
                      topic.conceptCode,
                    ),
                ),
              ),

              Promise.allSettled(
                SCIENCE_TOPICS.map(
                  (
                    topic,
                  ) =>
                    getScienceAdaptivePlan(
                      studentId,
                      topic.conceptCode,
                    ),
                ),
              ),

              Promise.allSettled(
                ENGLISH_TOPICS.map(
                  (
                    topic,
                  ) =>
                    getEnglishProgress(
                      studentId,
                      topic.conceptCode,
                    ),
                ),
              ),
            ]);


            if (
              cancelled
            ) {

              return;
            }


            setMathProgress(

              mathResults
                .filter(
                  (
                    result,
                  ): result is PromiseFulfilledResult<
                    ConceptProgress
                  > =>
                    result.status
                    === "fulfilled",
                )
                .map(
                  (
                    result,
                  ) =>
                    result.value,
                ),
            );


            setScienceProgress(

              scienceResults
                .filter(
                  (
                    result,
                  ): result is PromiseFulfilledResult<
                    ScienceAdaptivePlan
                  > =>
                    result.status
                    === "fulfilled",
                )
                .map(
                  (
                    result,
                  ) =>
                    result.value,
                ),
            );


            setEnglishProgress(

              englishResults
                .filter(
                  (
                    result,
                  ): result is PromiseFulfilledResult<
                    EnglishProgress
                  > =>
                    result.status
                    === "fulfilled",
                )
                .map(
                  (
                    result,
                  ) =>
                    result.value,
                ),
            );


          } finally {

            if (
              !cancelled
            ) {

              setProgressLoading(
                false,
              );
            }
          }
        };


      void loadProgress();


      return () => {

        cancelled =
          true;
      };

    },
    [
      studentId,
    ],
  );


  const name =
    student?.display_name
    ?? "Learner";


  const ageGroupLabel =

    student?.age_group
    === "FOUNDATION"

      ? "Foundation Learner"

      : student?.age_group
        === "INDEPENDENT"

        ? "Independent Learner"

        : "Developing Learner";


  // ======================================
  // Math
  // ======================================

  const mathTopicsPracticed =

    mathProgress.filter(
      (
        progress,
      ) =>
        Boolean(
          progress.diagnostic

          || progress.mastery

          || progress
            .learning_metrics
            .total_attempts
            > 0
        ),
    ).length;


  const mathIndependentTries =

    mathProgress.reduce(
      (
        total,
        progress,
      ) =>
        total
        + progress
          .learning_metrics
          .independent_attempts,

      0,
    );


  const mathMastered =

    mathProgress.filter(
      (
        progress,
      ) =>
        progress
          .current_mastery_state
        === "STRONG",
    ).length;


  // ======================================
  // Science
  // ======================================

  const scienceTopicsPracticed =

    scienceProgress.filter(
      (
        plan,
      ) =>
        plan.total_attempts
        > 0,
    ).length;


  const scienceIndependentTries =

    scienceProgress.reduce(
      (
        total,
        plan,
      ) =>
        total
        + plan.independent_attempts,

      0,
    );


  const scienceMastered =

    scienceProgress.filter(
      (
        plan,
      ) =>
        plan.mastery_state
        === "STRONG",
    ).length;


  // ======================================
  // English
  // ======================================

  const englishTopicsPracticed =

    englishProgress.filter(
      (
        item,
      ) =>
        item.total_attempts
        > 0,
    ).length;


  const englishIndependentTries =

    englishProgress.reduce(
      (
        total,
        item,
      ) =>
        total
        + item.independent_attempts,

      0,
    );


  const englishMastered =

    englishProgress.filter(
      (
        item,
      ) =>
        item.mastery_state
        === "STRONG",
    ).length;


  return (

    <div className="dashboard-page">

      {/* =========================
          Hero
      ========================== */}

      <section className="dashboard-hero">

        <div>

          <div className="dashboard-kicker">

            <Sparkles
              size={16}
            />

            {
              ageGroupLabel
            }

          </div>


          <h1>
            Hi, {name}! 👋
          </h1>


          <p>
            What would you like
            to understand today?
          </p>

        </div>


        <div className="dashboard-hero-decoration">

          <Lightbulb
            size={54}
          />

        </div>

      </section>


      {/* =========================
          Subjects
      ========================== */}

      <section className="dashboard-section">

        <div className="section-heading">

          <div>

            <h2>
              Choose a subject
            </h2>


            <p>
              Pick something you
              want to learn or practice.
            </p>

          </div>

        </div>


        <div className="subject-grid">

          {/* Math */}

          <article
            className={
              "subject-card "
              + "subject-math "
              + "clickable-subject-card"
            }

            onClick={() =>
              navigate(
                "/learn/math",
              )
            }
          >

            <div className="subject-icon">

              <Calculator
                size={28}
              />

            </div>


            <div>

              <span className="subject-label">
                Math
              </span>


              <h3>
                Solve and reason
              </h3>


              <p>
                Learn across eight
                age-adaptive Math concepts
                with assessments and
                adaptive practice.
              </p>

            </div>


            <button
              type="button"
              className="subject-action"

              onClick={(event) => {

                event.stopPropagation();

                navigate(
                  "/learn/math",
                );
              }}
            >

              Start Math

              <ArrowRight
                size={18}
              />

            </button>

          </article>


          {/* Science */}

          <article
            className={
              "subject-card "
              + "subject-science "
              + "clickable-subject-card"
            }

            onClick={() =>
              navigate(
                "/learn/science",
              )
            }
          >

            <div className="subject-icon">

              <FlaskConical
                size={28}
              />

            </div>


            <div>

              <span className="subject-label">
                Science
              </span>


              <h3>
                Explain and understand
              </h3>


              <p>
                Learn from grounded
                curriculum and show
                understanding in your
                own words.
              </p>

            </div>


            <button
              type="button"
              className="subject-action"

              onClick={(event) => {

                event.stopPropagation();

                navigate(
                  "/learn/science",
                );
              }}
            >

              Start Science

              <ArrowRight
                size={18}
              />

            </button>

          </article>


          {/* English */}

          <article
            className={
              "subject-card "
              + "subject-english "
              + "clickable-subject-card"
            }

            onClick={() =>
              navigate(
                "/learn/english",
              )
            }
          >

            <div className="subject-icon">

              <BookOpen
                size={28}
              />

            </div>


            <div>

              <span className="subject-label">
                English
              </span>


              <h3>
                Read, write and understand
              </h3>


              <p>
                Build vocabulary,
                grammar, sentence skills
                and reading comprehension
                with adaptive guidance.
              </p>

            </div>


            <button
              type="button"
              className="subject-action"

              onClick={(event) => {

                event.stopPropagation();

                navigate(
                  "/learn/english",
                );
              }}
            >

              Start English

              <ArrowRight
                size={18}
              />

            </button>

          </article>

        </div>

      </section>


      {/* =========================
          Progress
      ========================== */}

      <section className="dashboard-bottom-grid">

        {/* Math */}

        <div className="surface-card progress-card">

          <div className="progress-card-heading">

            <div>

              <span className="small-label">
                Math progress
              </span>


              <h2>
                Build problem-solving
              </h2>

            </div>


            <Calculator
              size={28}
            />

          </div>


          <div className="progress-stats">

            <div>

              <strong>

                {
                  progressLoading
                    ? "…"
                    : mathTopicsPracticed
                }

              </strong>


              <span>
                Topics practiced
              </span>

            </div>


            <div>

              <strong>

                {
                  progressLoading
                    ? "…"
                    : mathIndependentTries
                }

              </strong>


              <span>
                Independent tries
              </span>

            </div>


            <div>

              <strong>

                {
                  progressLoading
                    ? "…"
                    : mathMastered
                }

              </strong>


              <span>
                Strong mastery
              </span>

            </div>

          </div>


          <button
            type="button"
            className="dashboard-progress-link"

            onClick={() =>
              navigate(
                "/progress/math",
              )
            }
          >

            View Math progress

            <ArrowRight
              size={17}
            />

          </button>

        </div>


        {/* Science */}

        <div className="surface-card progress-card">

          <div className="progress-card-heading">

            <div>

              <span className="small-label">
                Science progress
              </span>


              <h2>
                Build understanding
              </h2>

            </div>


            <FlaskConical
              size={28}
            />

          </div>


          <div className="progress-stats">

            <div>

              <strong>

                {
                  progressLoading
                    ? "…"
                    : scienceTopicsPracticed
                }

              </strong>


              <span>
                Topics practiced
              </span>

            </div>


            <div>

              <strong>

                {
                  progressLoading
                    ? "…"
                    : scienceIndependentTries
                }

              </strong>


              <span>
                Independent tries
              </span>

            </div>


            <div>

              <strong>

                {
                  progressLoading
                    ? "…"
                    : scienceMastered
                }

              </strong>


              <span>
                Strong mastery
              </span>

            </div>

          </div>


          <button
            type="button"
            className="dashboard-progress-link"

            onClick={() =>
              navigate(
                "/progress/science",
              )
            }
          >

            View Science progress

            <ArrowRight
              size={17}
            />

          </button>

        </div>


        {/* English */}

        <div className="surface-card progress-card">

          <div className="progress-card-heading">

            <div>

              <span className="small-label">
                English progress
              </span>


              <h2>
                Build language confidence
              </h2>

            </div>


            <BookOpen
              size={28}
            />

          </div>


          <div className="progress-stats">

            <div>

              <strong>

                {
                  progressLoading
                    ? "…"
                    : englishTopicsPracticed
                }

              </strong>


              <span>
                Topics practiced
              </span>

            </div>


            <div>

              <strong>

                {
                  progressLoading
                    ? "…"
                    : englishIndependentTries
                }

              </strong>


              <span>
                Independent tries
              </span>

            </div>


            <div>

              <strong>

                {
                  progressLoading
                    ? "…"
                    : englishMastered
                }

              </strong>


              <span>
                Strong mastery
              </span>

            </div>

          </div>


          <button
            type="button"
            className="dashboard-progress-link"

            onClick={() =>
              navigate(
                "/progress/english",
              )
            }
          >

            View English progress

            <ArrowRight
              size={17}
            />

          </button>

        </div>

      </section>


      {/* =========================
          Learning habit
      ========================== */}

      <div
        className="surface-card habit-card"

        style={{
          marginTop:
            "18px",
        }}
      >

        <div className="habit-icon">

          <Flame
            size={28}
          />

        </div>


        <span className="small-label">
          Learning habit
        </span>


        <h2>
          One thoughtful attempt
          matters.
        </h2>


        <p>
          In Math, show your steps.
          In Science, explain your
          understanding. In English,
          try the answer yourself
          before asking for help.
        </p>


        <div className="habit-tip">

          💡 LearnFirst adapts
          support separately for
          each concept.

        </div>

      </div>

    </div>
  );
}
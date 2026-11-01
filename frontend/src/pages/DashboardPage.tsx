import {
  ArrowRight,
  BookOpen,
  Calculator,
  Flame,
  FlaskConical,
  Lightbulb,
  Sparkles,
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
  getConceptProgress,
} from "../api/assessments";

import type {
  ConceptProgress,
} from "../types/assessment";

import {
  getStoredStudent,
} from "../utils/studentStorage";


const CONCEPT_CODE =
  "MATH_ALG_LINEAR_01";


export default function DashboardPage() {
  const navigate =
    useNavigate();

  const student =
    getStoredStudent();

  const studentId =
    student?.id;

  const [
    progress,
    setProgress,
  ] = useState<
    ConceptProgress | null
  >(null);

  const [
    progressLoading,
    setProgressLoading,
  ] = useState(true);


  useEffect(() => {
    if (!studentId) {
      setProgressLoading(false);
      return;
    }

    let cancelled = false;

    const loadProgress =
      async () => {
        try {
          const data =
            await getConceptProgress(
              studentId,
              CONCEPT_CODE,
            );

          if (!cancelled) {
            setProgress(data);
          }
        } catch {
          /*
           * Progress is optional on
           * the dashboard.
           * The learner should still
           * be able to use the app
           * if progress loading fails.
           */
        } finally {
          if (!cancelled) {
            setProgressLoading(
              false,
            );
          }
        }
      };

    void loadProgress();

    return () => {
      cancelled = true;
    };
  }, [studentId]);


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


  const totalAttempts =
    progress
      ?.learning_metrics
      .total_attempts
    ?? 0;


  const hasMathActivity =
    Boolean(
      progress?.diagnostic
      || progress?.mastery
      || totalAttempts > 0,
    );


  const topicsPracticed =
    hasMathActivity
      ? 1
      : 0;


  const independentTries =
    progress
      ?.learning_metrics
      .independent_attempts
    ?? 0;


  const masteredTopics =
    progress
      ?.current_mastery_state
      === "STRONG"
      ? 1
      : 0;


  return (
    <div className="dashboard-page">
      <section className="dashboard-hero">
        <div>
          <div className="dashboard-kicker">
            <Sparkles
              size={16}
            />

            {ageGroupLabel}
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


      <section className="dashboard-section">
        <div className="section-heading">
          <div>
            <h2>
              Choose a subject
            </h2>

            <p>
              Pick something you
              want to learn or
              practice.
            </p>
          </div>
        </div>


        <div className="subject-grid">

          {/* =====================
              MATH
          ====================== */}

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
                Solve it step
                by step
              </h3>

              <p>
                Get guided hints,
                understand mistakes
                and build confidence.
              </p>
            </div>

            <button
              type="button"
              className="subject-action"
              onClick={(
                event,
              ) => {
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


          {/* =====================
              SCIENCE
          ====================== */}

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
                Explore how
                things work
              </h3>

              <p>
                Learn through
                trusted curriculum,
                questions and
                explanations.
              </p>
            </div>

            <button
              type="button"
              className="subject-action"
              onClick={(
                event,
              ) => {
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


          {/* =====================
              ENGLISH
          ====================== */}

          <article
            className={
              "subject-card "
              + "subject-english"
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
                Practice with
                confidence
              </h3>

              <p>
                Improve grammar,
                vocabulary and
                expression.
              </p>
            </div>

            <button
              type="button"
              className={
                "subject-action "
                + "subject-action-disabled"
              }
              disabled
            >
              Coming next
            </button>
          </article>

        </div>
      </section>


      <section className="dashboard-bottom-grid">

        {/* =====================
            PROGRESS
        ====================== */}

        <div className="surface-card progress-card">
          <div className="progress-card-heading">
            <div>
              <span className="small-label">
                Your progress
              </span>

              <h2>
                Growing every
                step 🌱
              </h2>
            </div>

            <Trophy
              size={28}
            />
          </div>


          <div className="progress-stats">

            <div>
              <strong>
                {progressLoading
                  ? "…"
                  : topicsPracticed}
              </strong>

              <span>
                Topics practiced
              </span>
            </div>


            <div>
              <strong>
                {progressLoading
                  ? "…"
                  : independentTries}
              </strong>

              <span>
                Independent tries
              </span>
            </div>


            <div>
              <strong>
                {progressLoading
                  ? "…"
                  : masteredTopics}
              </strong>

              <span>
                Mastered
              </span>
            </div>

          </div>


          {hasMathActivity ? (
            <button
              type="button"
              className="dashboard-progress-link"
              onClick={() =>
                navigate(
                  "/progress",
                )
              }
            >
              View my progress

              <ArrowRight
                size={17}
              />
            </button>
          ) : (
            <p className="progress-placeholder">
              Complete a diagnostic
              or start practicing to
              build your progress.
            </p>
          )}
        </div>


        {/* =====================
            LEARNING HABIT
        ====================== */}

        <div className="surface-card habit-card">
          <div className="habit-icon">
            <Flame
              size={28}
            />
          </div>

          <span className="small-label">
            Learning habit
          </span>

          <h2>
            One good attempt
            matters.
          </h2>

          <p>
            Try solving the next
            question before asking
            for the answer.
          </p>

          <div className="habit-tip">
            💡 Mistakes help
            LearnFirst know what
            to teach next.
          </div>
        </div>

      </section>
    </div>
  );
}
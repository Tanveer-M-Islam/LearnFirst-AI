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
  useNavigate,
} from "react-router";

import {
  getStoredStudent,
} from "../utils/studentStorage";


export default function DashboardPage() {
  const navigate =
    useNavigate();

  const student =
    getStoredStudent();

  const name =
    student?.display_name
    ?? "Learner";

  const ageGroupLabel =
    student?.age_group
      === "FOUNDATION"
      ? "Foundation Learner"

      : student?.age_group
        === "INDEPENDENT"
        ? (
          "Independent "
          + "Learner"
        )

        : "Developing Learner";


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
          <article
            className="subject-card subject-math clickable-subject-card"
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

          <article className="subject-card subject-science">
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
                questions,
                explanations and
                curiosity.
              </p>
            </div>

            <button
              type="button"
              className="subject-action subject-action-disabled"
              disabled
            >
              Coming next
            </button>
          </article>

          <article className="subject-card subject-english">
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
              className="subject-action subject-action-disabled"
              disabled
            >
              Coming next
            </button>
          </article>
        </div>
      </section>

      <section className="dashboard-bottom-grid">
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
                —
              </strong>

              <span>
                Topics practiced
              </span>
            </div>

            <div>
              <strong>
                —
              </strong>

              <span>
                Independent tries
              </span>
            </div>

            <div>
              <strong>
                —
              </strong>

              <span>
                Mastered
              </span>
            </div>
          </div>

          <p className="progress-placeholder">
            Your learning progress
            will appear here as
            you begin practicing.
          </p>
        </div>

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
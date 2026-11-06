import {
  ArrowRight,
  BookOpen,
  Calculator,
  FlaskConical,
  Sparkles,
} from "lucide-react";

import {
  useNavigate,
} from "react-router";


export default function LearnPage() {

  const navigate =
    useNavigate();


  return (

    <div className="dashboard-page">

      <section className="dashboard-hero">

        <div>

          <div className="dashboard-kicker">

            <Sparkles
              size={16}
            />

            Learn

          </div>


          <h1>
            What would you
            like to learn?
          </h1>


          <p>
            Choose a subject.
            LearnFirst adapts
            the learning flow
            to your progress.
          </p>

        </div>

      </section>


      <section className="dashboard-section">

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
              <Calculator size={28} />
            </div>

            <div>

              <span className="subject-label">
                Math
              </span>

              <h3>
                Learn Math
              </h3>

              <p>
                Adaptive Math practice
                with deterministic
                validation.
              </p>

            </div>

            <button
              type="button"
              className="subject-action"
            >
              Open Math
              <ArrowRight size={18} />
            </button>

          </article>


          <article
            className="subject-card subject-science clickable-subject-card"

            onClick={() =>
              navigate(
                "/learn/science",
              )
            }
          >

            <div className="subject-icon">
              <FlaskConical size={28} />
            </div>

            <div>

              <span className="subject-label">
                Science
              </span>

              <h3>
                Learn Science
              </h3>

              <p>
                Structured understanding
                with curriculum-grounded
                AI tutoring.
              </p>

            </div>

            <button
              type="button"
              className="subject-action"
            >
              Open Science
              <ArrowRight size={18} />
            </button>

          </article>


          <article
            className="subject-card subject-english clickable-subject-card"

            onClick={() =>
              navigate(
                "/learn/english",
              )
            }
          >

            <div className="subject-icon">
              <BookOpen size={28} />
            </div>

            <div>

              <span className="subject-label">
                English
              </span>

              <h3>
                Learn English
              </h3>

              <p>
                Vocabulary, grammar,
                reading and sentence
                construction with
                adaptive support.
              </p>

            </div>

            <button
              type="button"
              className="subject-action"
            >
              Open English
              <ArrowRight size={18} />
            </button>

          </article>

        </div>

      </section>

    </div>
  );
}
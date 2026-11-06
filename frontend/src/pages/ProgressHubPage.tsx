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


export default function ProgressHubPage() {

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

            Progress

          </div>


          <h1>
            Your learning progress
          </h1>


          <p>
            Math, Science and English
            use different learning
            evidence, so LearnFirst
            shows their progress
            separately.
          </p>

        </div>

      </section>


      <section className="dashboard-section">

        <div className="subject-grid">

          {/* =========================
              Math
          ========================== */}

          <article
            className={
              "subject-card "
              + "subject-math "
              + "clickable-subject-card"
            }

            onClick={() =>
              navigate(
                "/progress/math",
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
                Math progress
              </span>


              <h3>
                Assessments +
                independence
              </h3>


              <p>
                See diagnostics,
                mastery checks,
                attempts, hints and
                independent success.
              </p>

            </div>


            <button
              type="button"
              className="subject-action"
            >

              View Math

              <ArrowRight
                size={18}
              />

            </button>

          </article>


          {/* =========================
              Science
          ========================== */}

          <article
            className={
              "subject-card "
              + "subject-science "
              + "clickable-subject-card"
            }

            onClick={() =>
              navigate(
                "/progress/science",
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
                Science progress
              </span>


              <h3>
                Understanding +
                independence
              </h3>


              <p>
                See structured
                understanding,
                independence,
                mastery signal and
                response pace.
              </p>

            </div>


            <button
              type="button"
              className="subject-action"
            >

              View Science

              <ArrowRight
                size={18}
              />

            </button>

          </article>


          {/* =========================
              English
          ========================== */}

          <article
            className={
              "subject-card "
              + "subject-english "
              + "clickable-subject-card"
            }

            onClick={() =>
              navigate(
                "/progress/english",
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
                English progress
              </span>


              <h3>
                Understanding +
                independent practice
              </h3>


              <p>
                See understanding,
                attempts, independent
                practice and adaptive
                mastery across English
                concepts.
              </p>

            </div>


            <button
              type="button"
              className="subject-action"
            >

              View English

              <ArrowRight
                size={18}
              />

            </button>

          </article>

        </div>

      </section>

    </div>
  );
}
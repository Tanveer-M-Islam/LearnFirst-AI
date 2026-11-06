import {
  ArrowRight,
  BookOpen,
  BrainCircuit,
  Calculator,
  FlaskConical,
  GraduationCap,
  LogIn,
  Sparkles,
} from "lucide-react";

import {
  useNavigate,
} from "react-router";

import {
  getStoredStudent,
} from "../utils/studentStorage";


export default function WelcomePage() {

  const navigate =
    useNavigate();


  const existingStudent =
    getStoredStudent();


  const begin = () => {

    navigate(
      existingStudent
        ? "/dashboard"
        : "/setup"
    );
  };


  return (

    <div className="welcome-page">

      <header className="welcome-nav">

        <div className="welcome-brand">

          <div className="brand-mark">

            <GraduationCap
              size={23}
            />

          </div>


          <div>

            <div className="brand-name">
              LearnFirst AI
            </div>


            <div className="brand-subtitle">
              Think before the answer
            </div>

          </div>

        </div>


        <div
          style={{
            display:
              "flex",

            gap:
              "10px",

            alignItems:
              "center",
          }}
        >

          {!existingStudent && (

            <button
              type="button"

              className="secondary-button"

              onClick={() =>
                navigate(
                  "/login"
                )
              }
            >

              <LogIn
                size={17}
              />

              Login

            </button>

          )}


          <button
            type="button"

            className="primary-button"

            onClick={
              begin
            }
          >

            {
              existingStudent
                ? "Continue learning"
                : "Get started"
            }

          </button>

        </div>

      </header>


      <main className="welcome-hero">

        <section className="hero-copy">

          <div className="hero-badge">

            <Sparkles
              size={16}
            />

            Your AI learning guide

          </div>


          <h1>

            Learn how to

            <span>

              {" "}
              think,
              understand
              {" "}

            </span>

            and solve.

          </h1>


          <p>

            LearnFirst doesn't rush
            to give you answers.
            It guides you with
            questions, hints and
            practice until the idea
            truly makes sense.

          </p>


          <div className="hero-actions">

            <button
              type="button"

              className="primary-button hero-primary"

              onClick={
                begin
              }
            >

              {
                existingStudent
                  ? "Continue learning"
                  : "Start learning"
              }


              <ArrowRight
                size={19}
              />

            </button>


            {!existingStudent && (

              <button
                type="button"

                className="secondary-button"

                onClick={() =>
                  navigate(
                    "/login"
                  )
                }
              >

                <LogIn
                  size={18}
                />

                I already have an account

              </button>

            )}

          </div>


          <div className="hero-note">

            Built for learners
            aged 7–14

          </div>


          <div className="hero-features">

            <div>

              <span>
                01
              </span>

              Try first

            </div>


            <div>

              <span>
                02
              </span>

              Get a hint

            </div>


            <div>

              <span>
                03
              </span>

              Master it

            </div>

          </div>

        </section>


        <section className="hero-visual">

          <div className="learning-orbit">

            <div className="orbit-main">

              <div className="orbit-icon">

                <BrainCircuit
                  size={34}
                />

              </div>


              <strong>
                Your AI Tutor
              </strong>


              <p>

                “What do you think
                the first step
                should be?”

              </p>

            </div>


            <div className="subject-orbit math-orbit">

              <Calculator
                size={22}
              />

              Math

            </div>


            <div className="subject-orbit science-orbit">

              <FlaskConical
                size={22}
              />

              Science

            </div>


            <div className="subject-orbit english-orbit">

              <BookOpen
                size={22}
              />

              English

            </div>


            <div className="mini-progress">

              <span>
                Today's progress
              </span>


              <strong>
                Keep going! 🌱
              </strong>


              <div className="mini-progress-track">

                <div />

              </div>

            </div>

          </div>

        </section>

      </main>

    </div>
  );
}
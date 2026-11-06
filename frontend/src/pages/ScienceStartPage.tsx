import {
  ArrowLeft,
  ArrowRight,
  BrainCircuit,
  FlaskConical,
  Gauge,
  Lightbulb,
  RefreshCcw,
  ShieldCheck,
  Sparkles,
  Target,
} from "lucide-react";

import {
  useEffect,
  useState,
} from "react";

import {
  useNavigate,
} from "react-router";

import {
  getStudentCurriculumPath,
} from "../api/curriculum";

import {
  getScienceAdaptivePlan,
} from "../api/scienceAdaptive";

import {
  createLearningSession,
} from "../api/sessions";

import {
  getScienceTopic,
  getScienceTopicForAge,
} from "../data/scienceTopics";

import type {
  StudentCurriculumPath,
} from "../types/curriculum";

import type {
  ScienceAdaptivePlan,
} from "../types/scienceAdaptive";

import {
  getStoredStudent,
} from "../utils/studentStorage";


function readableLabel(
  value:
    string,
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


export default function ScienceStartPage() {

  const navigate =
    useNavigate();


  const student =
    getStoredStudent();


  const studentId =
    student?.id;


  const learnerAge =
    student?.age
    ?? 7;


  const fallbackTopic =
    getScienceTopicForAge(
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
    adaptivePlan,
    setAdaptivePlan,
  ] = useState<
    ScienceAdaptivePlan | null
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
    adaptiveLoading,
    setAdaptiveLoading,
  ] = useState(
    false,
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


  const conceptCode =
    curriculum
      ?.recommended_concept
      ?.concept_code

    ?? fallbackTopic
      .conceptCode;


  const selectedTopic =
    getScienceTopic(
      conceptCode,
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


      setError(
        null,
      );


      try {

        const data =
          await getStudentCurriculumPath(
            studentId,
            "SCIENCE",
          );


        setCurriculum(
          data,
        );


      } catch (err) {

        setError(
          err instanceof Error
            ? err.message
            : (
              "Could not load your "
              + "Science curriculum."
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


      try {

        const data =
          await getScienceAdaptivePlan(
            studentId,
            conceptCode,
          );


        setAdaptivePlan(
          data,
        );


      } catch {

        setAdaptivePlan(
          null,
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


      void loadAdaptivePlan();

    },
    [
      studentId,
      conceptCode,
    ],
  );


  // ======================================
  // Start Science
  // ======================================

  const startScience =
    async () => {

      if (
        !student
      ) {

        navigate(
          "/login",
        );

        return;
      }


      setStarting(
        true,
      );


      setError(
        null,
      );


      try {

        const question =
          adaptivePlan
            ?.next_question
            ?.prompt

          ?? null;


        const session =
          await createLearningSession({

            student_id:
              student.id,

            mode:
              "LEARN",

            subject:
              "SCIENCE",

            topic:
              selectedTopic.title,

            concept_code:
              conceptCode,

            current_problem:
              question,
          });


        navigate(
          (
            "/learn/science/session/"
            + session.id
          ),
        );


      } catch (err) {

        setError(
          err instanceof Error
            ? err.message
            : (
              "Could not start "
              + "Science learning."
            ),
        );


      } finally {

        setStarting(
          false,
        );
      }
    };


  if (
    curriculumLoading
  ) {

    return (

      <div className="science-loading surface-card">

        <BrainCircuit
          size={26}
        />

        Finding your
        Science level...

      </div>
    );
  }


  return (

    <div className="science-start-page">

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
          Hero
      ============================== */}

      <section className="science-start-hero">

        <div className="science-start-icon">

          <FlaskConical
            size={31}
          />

        </div>


        <div>

          <div className="science-eyebrow">

            <Sparkles
              size={15}
            />

            Age-adaptive Science

          </div>


          <h1>
            Your next Science step
          </h1>


          <p>
            LearnFirst selects an
            age-appropriate Science
            concept and adapts the
            questions, support and
            explanations from your
            learning evidence.
          </p>

        </div>

      </section>


      {/* =============================
          Curriculum position
      ============================== */}

      <div className="science-section-heading">

        <div>

          <h2>
            Your curriculum position
          </h2>


          <p>
            Age is the starting point.
            Demonstrated learning
            evidence can adjust the path.
          </p>

        </div>


        <button
          type="button"
          className="secondary-button"

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

            <Target
              size={27}
            />

          </div>


          <div className="adaptive-plan-copy">

            <span>
              Current Science concept
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
              Age
            </span>


            <strong>
              {
                learnerAge
              }
            </strong>

          </div>


          <div>

            <FlaskConical
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

                ?? selectedTopic.title
              }

            </strong>

          </div>


          <div>

            <BrainCircuit
              size={18}
            />

            <span>
              Status
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
                  + "Science concept that "
                  + "needs review before "
                  + "continuing."
                )

                : (
                  "No demonstrated "
                  + "prerequisite gap is "
                  + "blocking this Science "
                  + "level."
                )
            }

          </p>

        </div>

      </div>


      {/* =============================
          Adaptive plan
      ============================== */}

      <div className="science-section-heading">

        <div>

          <h2>
            Personalized Science plan
          </h2>


          <p>
            Difficulty and support
            are adjusted independently
            from curriculum level.
          </p>

        </div>

      </div>


      {adaptiveLoading && (

        <div className="science-loading surface-card">

          <BrainCircuit
            size={24}
          />

          Checking your
          learning profile...

        </div>

      )}


      {(
        !adaptiveLoading
        && adaptivePlan
      ) && (

        <div className="adaptive-plan-card surface-card">

          <div className="adaptive-plan-main">

            <div className="adaptive-plan-icon">

              <BrainCircuit
                size={27}
              />

            </div>


            <div className="adaptive-plan-copy">

              <span>
                Recommended activity
              </span>


              <h3>

                {
                  readableLabel(
                    adaptivePlan
                      .next_activity,
                  )
                }

              </h3>


              <p>
                {
                  adaptivePlan.summary
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

              <Lightbulb
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

              <ShieldCheck
                size={18}
              />

              <span>
                Understanding
              </span>


              <strong>

                {
                  adaptivePlan
                    .understanding_score_percent
                }
                %

              </strong>

            </div>

          </div>


          {adaptivePlan
            .next_question
            && (

            <div className="adaptive-next-problem">

              <div>

                <span>
                  First question
                </span>


                <strong>

                  {
                    adaptivePlan
                      .next_question
                      .prompt
                  }

                </strong>

              </div>

            </div>

          )}

        </div>

      )}


      {/* =============================
          RAG explanation
      ============================== */}

      <div className="science-start-actions">

        <div>

          <strong>
            Curriculum-grounded Science
          </strong>


          <span>
            Explanations and hints are
            retrieved from the trusted
            curriculum knowledge for
            {
              " "
            }
            {
              selectedTopic.title
            }.
          </span>

        </div>


        <ShieldCheck
          size={25}
        />

      </div>


      {error && (

        <div className="science-error surface-card">

          <strong>
            Could not prepare Science
          </strong>


          <p>
            {error}
          </p>

        </div>

      )}


      {/* =============================
          Start
      ============================== */}

      <div className="science-start-actions">

        <div>

          <strong>
            Ready to learn?
          </strong>


          <span>

            Start your
            {
              " "
            }
            {
              selectedTopic.title
            }
            {
              " "
            }
            lesson.

          </span>

        </div>


        <button
          type="button"
          className="primary-button"

          disabled={
            starting
          }

          onClick={() =>
            void startScience()
          }
        >

          {
            starting
              ? "Preparing..."
              : "Start Science"
          }


          {!starting && (

            <ArrowRight
              size={18}
            />

          )}

        </button>

      </div>

    </div>
  );
}
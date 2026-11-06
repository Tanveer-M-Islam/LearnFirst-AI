import {
  ArrowLeft,
  ArrowRight,
  BrainCircuit,
  Calculator,
  CheckCircle2,
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
  getConceptProgress,
} from "../api/assessments";

import {
  getStudentCurriculumPath,
} from "../api/curriculum";

import {
  getMathTopic,
} from "../data/mathTopics";

import type {
  ConceptProgress,
} from "../types/assessment";

import type {
  StudentCurriculumPath,
} from "../types/curriculum";

import {
  getStoredStudent,
} from "../utils/studentStorage";


function readableLabel(
  value: string,
): string {

  return value
    .replaceAll(
      "_",
      " ",
    )
    .toLowerCase()
    .replace(
      /\b\w/g,
      (
        character,
      ) =>
        character.toUpperCase(),
    );
}


export default function ProgressPage() {

  const navigate =
    useNavigate();


  const student =
    getStoredStudent();


  const [
    curriculum,
    setCurriculum,
  ] = useState<
    StudentCurriculumPath | null
  >(null);


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


  useEffect(
    () => {

      if (
        !student?.id
      ) {

        setLoading(
          false,
        );

        return;
      }


      let cancelled =
        false;


      const load =
        async () => {

          setLoading(
            true,
          );

          setError(
            null,
          );


          try {

            const path =
              await getStudentCurriculumPath(
                student.id,
                "MATH",
              );


            if (
              cancelled
            ) {

              return;
            }


            setCurriculum(
              path,
            );


            const conceptCode =
              path
                .recommended_concept
                ?.concept_code

              ?? path
                .target_concept
                ?.concept_code;


            if (
              conceptCode
            ) {

              const data =
                await getConceptProgress(
                  student.id,
                  conceptCode,
                );


              if (
                !cancelled
              ) {

                setProgress(
                  data,
                );
              }
            }


          } catch (err) {

            if (
              !cancelled
            ) {

              setError(
                err instanceof Error
                  ? err.message
                  : (
                    "Could not load "
                    + "Math progress."
                  ),
              );
            }


          } finally {

            if (
              !cancelled
            ) {

              setLoading(
                false,
              );
            }
          }
        };


      void load();


      return () => {

        cancelled =
          true;
      };

    },
    [
      student?.id,
    ],
  );


  const recommendedConcept =
    curriculum
      ?.recommended_concept;


  const targetConcept =
    curriculum
      ?.target_concept;


  const reviewConcept =
    curriculum
      ?.prerequisite_review_concept;


  const topic =
    recommendedConcept
      ? getMathTopic(
          recommendedConcept
            .concept_code,
        )
      : null;


  return (

    <div className="dashboard-page">

      <button
        type="button"
        className="page-back-button"

        onClick={() =>
          navigate(
            "/progress",
          )
        }
      >
        <ArrowLeft
          size={18}
        />

        Progress
      </button>


      <section className="dashboard-hero">

        <div>

          <div className="dashboard-kicker">

            <Calculator
              size={16}
            />

            Math progress

          </div>


          <h1>
            Your Math learning
          </h1>


          <p>
            LearnFirst shows the
            curriculum that is relevant
            to your current age and
            learning evidence.
          </p>

        </div>

      </section>


      {loading && (

        <div className="surface-card progress-loading-card">

          <BrainCircuit
            size={24}
          />

          Loading Math progress...

        </div>

      )}


      {error && (

        <div className="science-error surface-card">

          <strong>
            Could not load progress
          </strong>

          <p>
            {error}
          </p>

        </div>

      )}


      {(
        !loading
        && !error
        && recommendedConcept
      ) && (

        <>

          <section className="progress-focus-grid">

            <article className="surface-card progress-focus-card">

              <div className="progress-focus-heading">

                <div className="subject-icon">

                  <Calculator
                    size={26}
                  />

                </div>


                <div>

                  <span className="small-label">
                    Current curriculum
                  </span>


                  <h2>
                    {
                      topic?.title
                      ?? recommendedConcept.title
                    }
                  </h2>

                </div>

              </div>


              <p>
                {
                  topic?.description
                  ?? recommendedConcept.description
                }
              </p>


              <div className="progress-status-row">

                <div>

                  <span>
                    Curriculum status
                  </span>

                  <strong>
                    {
                      readableLabel(
                        recommendedConcept.status,
                      )
                    }
                  </strong>

                </div>


                <div>

                  <span>
                    Age
                  </span>

                  <strong>
                    {
                      student?.age
                      ?? "—"
                    }
                  </strong>

                </div>


                <div>

                  <span>
                    Mastery
                  </span>

                  <strong>
                    {
                      progress
                        ?.current_mastery_state
                        ? readableLabel(
                            progress
                              .current_mastery_state,
                          )
                        : "Not Started"
                    }
                  </strong>

                </div>

              </div>

            </article>

          </section>


          {(
            reviewConcept
            && reviewConcept
              .concept_code
              !== recommendedConcept
                .concept_code
          ) && (

            <section className="surface-card prerequisite-review-card">

              <div>

                <Target
                  size={22}
                />

              </div>


              <div>

                <span className="small-label">
                  Prerequisite review
                </span>


                <h3>
                  {
                    reviewConcept.title
                  }
                </h3>


                <p>
                  LearnFirst detected
                  learning evidence that
                  this earlier concept
                  should be reviewed before
                  continuing your current
                  syllabus.
                </p>

              </div>

            </section>

          )}


          {progress && (

            <section className="surface-card progress-detail-card">

              <div className="progress-card-heading">

                <div>

                  <span className="small-label">
                    Learning evidence
                  </span>


                  <h2>
                    Current concept progress
                  </h2>

                </div>


                <Sparkles
                  size={27}
                />

              </div>


              <div className="progress-stats">

                <div>

                  <strong>
                    {
                      progress
                        .learning_metrics
                        .total_attempts
                    }
                  </strong>

                  <span>
                    Attempts
                  </span>

                </div>


                <div>

                  <strong>
                    {
                      progress
                        .learning_metrics
                        .independent_attempts
                    }
                  </strong>

                  <span>
                    Independent tries
                  </span>

                </div>


                <div>

                  <strong>
                    {
                      readableLabel(
                        progress
                          .current_mastery_state,
                      )
                    }
                  </strong>

                  <span>
                    Mastery
                  </span>

                </div>

              </div>


              {(
                progress
                  .current_mastery_state
                === "STRONG"
              ) && (

                <div className="habit-tip">

                  <CheckCircle2
                    size={16}
                  />

                  Strong mastery demonstrated.

                </div>

              )}

            </section>

          )}


          {(
            targetConcept
            && recommendedConcept
            && targetConcept
              .concept_code
              !== recommendedConcept
                .concept_code
          ) && (

            <section className="surface-card target-return-card">

              <span className="small-label">
                Age-level target
              </span>


              <h3>
                {
                  targetConcept.title
                }
              </h3>


              <p>
                After the prerequisite
                review is strong enough,
                LearnFirst will return
                you to this age-level
                curriculum automatically.
              </p>

            </section>

          )}


          <button
            type="button"
            className="primary-button"

            onClick={() =>
              navigate(
                "/learn/math",
              )
            }
          >
            Continue Math

            <ArrowRight
              size={18}
            />
          </button>

        </>

      )}

    </div>
  );
}
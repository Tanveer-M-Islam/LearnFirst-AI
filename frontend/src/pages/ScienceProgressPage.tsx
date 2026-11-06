import {
  ArrowLeft,
  ArrowRight,
  BrainCircuit,
  CheckCircle2,
  FlaskConical,
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
  getScienceTopic,
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


export default function ScienceProgressPage() {

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
                "SCIENCE",
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

              const adaptive =
                await getScienceAdaptivePlan(
                  student.id,
                  conceptCode,
                );


              if (
                !cancelled
              ) {

                setPlan(
                  adaptive,
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
                    + "Science progress."
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
      ? getScienceTopic(
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

            <FlaskConical
              size={16}
            />

            Science progress

          </div>


          <h1>
            Your Science learning
          </h1>


          <p>
            Progress follows your
            age-level curriculum while
            allowing targeted prerequisite
            review when learning evidence
            shows it is needed.
          </p>

        </div>

      </section>


      {loading && (

        <div className="surface-card progress-loading-card">

          <BrainCircuit
            size={24}
          />

          Loading Science progress...

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

                  <FlaskConical
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
                    Understanding
                  </span>

                  <strong>

                    {
                      plan
                        ?.understanding_score_percent
                      ?? 0
                    }

                    %

                  </strong>

                </div>


                <div>

                  <span>
                    Mastery
                  </span>

                  <strong>
                    {
                      plan
                        ? readableLabel(
                            plan.mastery_state,
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

              <Target
                size={22}
              />


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
                  Your learning evidence
                  suggests reviewing this
                  prerequisite before
                  continuing the current
                  Science syllabus.
                </p>

              </div>

            </section>

          )}


          {plan && (

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
                      plan.total_attempts
                    }
                  </strong>

                  <span>
                    Attempts
                  </span>

                </div>


                <div>

                  <strong>
                    {
                      plan
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
                      plan
                        .understanding_score_percent
                    }
                    %
                  </strong>

                  <span>
                    Understanding
                  </span>

                </div>

              </div>


              {(
                plan.mastery_state
                === "STRONG"
              ) && (

                <div className="habit-tip">

                  <CheckCircle2
                    size={16}
                  />

                  Strong understanding demonstrated.

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
                LearnFirst will return
                to this curriculum after
                the prerequisite gap has
                been addressed.
              </p>

            </section>

          )}


          <button
            type="button"
            className="primary-button"

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

        </>

      )}

    </div>
  );
}
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  BrainCircuit,
  Gauge,
  RefreshCcw,
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
  getEnglishAdaptivePlan,
} from "../api/englishAdaptive";

import {
  createLearningSession,
} from "../api/sessions";

import {
  getEnglishTopic,
  getEnglishTopicForAge,
} from "../data/englishTopics";

import type {
  StudentCurriculumPath,
} from "../types/curriculum";

import type {
  EnglishAdaptivePlan,
} from "../types/englishAdaptive";

import {
  getStoredStudent,
} from "../utils/studentStorage";


function readableLabel(
  value: string,
): string {

  return value
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
        character.toUpperCase(),
    );
}


export default function EnglishStartPage() {

  const navigate =
    useNavigate();


  const student =
    getStoredStudent();


  const studentId =
    student?.id;


  const learnerAge =
    student?.age ?? 7;


  const fallbackTopic =
    getEnglishTopicForAge(
      learnerAge,
    );


  const [
    curriculum,
    setCurriculum,
  ] = useState<
    StudentCurriculumPath | null
  >(null);


  const [
    adaptivePlan,
    setAdaptivePlan,
  ] = useState<
    EnglishAdaptivePlan | null
  >(null);


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
  >(null);


  const conceptCode =
    curriculum
      ?.recommended_concept
      ?.concept_code

    ?? fallbackTopic
      .conceptCode;


  const selectedTopic =
    getEnglishTopic(
      conceptCode,
    );


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
            "ENGLISH",
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
              + "English curriculum."
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


  useEffect(
    () => {

      if (
        !studentId
      ) {

        return;
      }


      let cancelled =
        false;


      const loadAdaptive =
        async () => {

          setAdaptiveLoading(
            true,
          );


          try {

            const data =
              await getEnglishAdaptivePlan(
                studentId,
                conceptCode,
              );


            if (
              !cancelled
            ) {

              setAdaptivePlan(
                data,
              );
            }


          } catch {

            if (
              !cancelled
            ) {

              setAdaptivePlan(
                null,
              );
            }


          } finally {

            if (
              !cancelled
            ) {

              setAdaptiveLoading(
                false,
              );
            }
          }
        };


      setAdaptivePlan(
        null,
      );


      void loadAdaptive();


      return () => {

        cancelled =
          true;
      };

    },
    [
      studentId,
      conceptCode,
    ],
  );


  const startEnglish =
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

        const session =
          await createLearningSession({

            student_id:
              student.id,

            mode:
              "LEARN",

            subject:
              "ENGLISH",

            topic:
              selectedTopic.title,

            concept_code:
              conceptCode,

            current_problem:
              adaptivePlan
                ?.next_question
                ?.prompt
              ?? null,
          });


        navigate(
          (
            "/learn/english/session/"
            + session.id
          ),
        );


      } catch (err) {

        setError(
          err instanceof Error
            ? err.message
            : (
              "Could not start "
              + "English learning."
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

        Finding your English level...

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


      <section className="science-start-hero">

        <div className="science-start-icon">

          <BookOpen
            size={31}
          />

        </div>


        <div>

          <div className="science-eyebrow">

            <Sparkles
              size={15}
            />

            Age-adaptive English

          </div>


          <h1>
            Your next English step
          </h1>


          <p>
            LearnFirst starts from your
            age-level curriculum and uses
            real learning evidence to decide
            whether you should continue,
            review a prerequisite, or move
            forward.
          </p>

        </div>

      </section>


      <div className="science-section-heading">

        <div>

          <h2>
            Your curriculum position
          </h2>


          <p>
            Missing mastery records do not
            count as weakness. Review is used
            only when there is actual evidence
            of a prerequisite gap.
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
              Current English concept
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

            <BookOpen
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
                  "LearnFirst found learning "
                  + "evidence showing that this "
                  + "earlier English concept "
                  + "should be reviewed first."
                )

                : (
                  "No demonstrated prerequisite "
                  + "gap is blocking your current "
                  + "English level."
                )
            }
          </p>

        </div>

      </div>


      <div className="science-section-heading">

        <div>

          <h2>
            Personalized English plan
          </h2>


          <p>
            Difficulty and support are
            adapted separately from your
            curriculum level.
          </p>

        </div>

      </div>


      {adaptiveLoading && (

        <div className="science-loading surface-card">

          <BrainCircuit
            size={24}
          />

          Checking your learning profile...

        </div>

      )}


      {(
        !adaptiveLoading
        && adaptivePlan
      ) && (

        <div className="adaptive-plan-card surface-card">

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
                    adaptivePlan.difficulty,
                  )
                }
              </strong>

            </div>


            <div>

              <BrainCircuit
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

              <Sparkles
                size={18}
              />

              <span>
                Mastery
              </span>

              <strong>
                {
                  readableLabel(
                    adaptivePlan
                      .mastery_state,
                  )
                }
              </strong>

            </div>

          </div>


          <div className="adaptive-plan-footer">

            <p>
              {
                adaptivePlan.summary
              }
            </p>

          </div>


          {adaptivePlan
            .next_question
            && (

            <div className="adaptive-score-note">

              <span>
                Next learning question
              </span>


              <strong>
                {
                  adaptivePlan
                    .next_question
                    .prompt
                }
              </strong>

            </div>

          )}

        </div>

      )}


      {error && (

        <div className="science-error surface-card">

          <strong>
            English learning problem
          </strong>

          <p>
            {error}
          </p>

        </div>

      )}


      <div className="science-start-actions">

        <div>

          <strong>
            Ready to continue?
          </strong>


          <span>
            LearnFirst will evaluate your
            English response and adjust
            support from your evidence.
          </span>

        </div>


        <button
          type="button"
          className="primary-button"

          disabled={
            starting
            || curriculumLoading
            || adaptiveLoading
          }

          onClick={() =>
            void startEnglish()
          }
        >

          {
            starting
              ? "Preparing..."
              : "Start English"
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
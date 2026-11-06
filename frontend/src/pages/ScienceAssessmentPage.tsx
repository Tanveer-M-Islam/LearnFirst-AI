import {
  ArrowLeft,
  ArrowRight,
  BrainCircuit,
  Check,
  FlaskConical,
  Sparkles,
  Target,
  Trophy,
} from "lucide-react";

import {
  useState,
} from "react";

import {
  useNavigate,
  useParams,
  useSearchParams,
} from "react-router";

import {
  startScienceAssessment,
  submitScienceAssessment,
} from "../api/scienceAssessments";

import {
  getScienceTopic,
} from "../data/scienceTopics";

import type {
  AssessmentType,
} from "../types/assessment";

import type {
  ScienceAssessmentAnswerInput,
  ScienceAssessmentResult,
  ScienceAssessmentStartResponse,
} from "../types/scienceAssessment";

import {
  getStoredStudent,
} from "../utils/studentStorage";


function assessmentTypeFromUrl(
  value:
    string | undefined,
): AssessmentType {

  return (
    value
      ?.toLowerCase()
    === "mastery"

      ? "MASTERY"

      : "DIAGNOSTIC"
  );
}


export default function ScienceAssessmentPage() {

  const navigate =
    useNavigate();


  const {
    assessmentType:
      assessmentTypeParam,
  } = useParams<{
    assessmentType:
      string;
  }>();


  const [
    searchParams,
  ] = useSearchParams();


  const conceptCode =
    searchParams.get(
      "concept",
    )
    ?? "SCI_BIO_PHOTO_01";


  const topic =
    getScienceTopic(
      conceptCode,
    );


  const assessmentType =
    assessmentTypeFromUrl(
      assessmentTypeParam,
    );


  const isMastery =
    assessmentType
    === "MASTERY";


  const student =
    getStoredStudent();


  const [
    assessment,
    setAssessment,
  ] = useState<
    ScienceAssessmentStartResponse
    | null
  >(null);


  const [
    result,
    setResult,
  ] = useState<
    ScienceAssessmentResult
    | null
  >(null);


  const [
    currentIndex,
    setCurrentIndex,
  ] = useState(
    0,
  );


  const [
    answers,
    setAnswers,
  ] = useState<
    Record<
      string,
      string
    >
  >({});


  const [
    loading,
    setLoading,
  ] = useState(
    false,
  );


  const [
    error,
    setError,
  ] = useState<
    string | null
  >(null);


  const currentQuestion =
    assessment
      ?.questions[
        currentIndex
      ];


  const currentAnswer =
    currentQuestion

      ? (
        answers[
          currentQuestion
            .question_id
        ]
        ?? ""
      )

      : "";


  const begin =
    async () => {

      if (
        !student
      ) {

        navigate(
          "/setup",
        );

        return;
      }


      setLoading(
        true,
      );


      setError(
        null,
      );


      try {

        const data =
          await startScienceAssessment({

            student_id:
              student.id,

            concept_code:
              conceptCode,

            assessment_type:
              assessmentType,
          });


        setAssessment(
          data,
        );


      } catch (err) {

        setError(
          err instanceof Error
            ? err.message
            : (
              "Could not start "
              + "Science assessment."
            ),
        );


      } finally {

        setLoading(
          false,
        );
      }
    };


  const updateAnswer = (
    value: string,
  ) => {

    if (
      !currentQuestion
    ) {

      return;
    }


    setAnswers(
      (
        current,
      ) => ({

        ...current,

        [
          currentQuestion
            .question_id
        ]:
          value,
      }),
    );
  };


  const next =
    () => {

      if (
        !currentAnswer.trim()
      ) {

        setError(
          "Explain your answer "
          + "before continuing.",
        );

        return;
      }


      setError(
        null,
      );


      setCurrentIndex(
        (
          current,
        ) =>
          Math.min(
            current + 1,

            (
              assessment
                ?.total_questions
              ?? 1
            )
            - 1,
          ),
      );
    };


  const previous =
    () => {

      setCurrentIndex(
        (
          current,
        ) =>
          Math.max(
            current - 1,
            0,
          ),
      );
  };


  const finish =
    async () => {

      if (
        !assessment
        || !currentQuestion
      ) {

        return;
      }


      const finalAnswers = {

        ...answers,

        [
          currentQuestion
            .question_id
        ]:
          currentAnswer,
      };


      const missing =
        assessment
          .questions
          .some(
            (
              question,
            ) =>
              !(
                finalAnswers[
                  question
                    .question_id
                ]
                ?? ""
              )
                .trim(),
          );


      if (
        missing
      ) {

        setError(
          "Please answer all "
          + "Science questions.",
        );

        return;
      }


      const payload:
        ScienceAssessmentAnswerInput[] =
          assessment
            .questions
            .map(
              (
                question,
              ) => ({

                question_id:
                  question
                    .question_id,

                response:
                  finalAnswers[
                    question
                      .question_id
                  ]
                    .trim(),
              }),
            );


      setLoading(
        true,
      );


      try {

        const data =
          await submitScienceAssessment(
            assessment
              .assessment_id,

            payload,
          );


        setResult(
          data,
        );


      } catch (err) {

        setError(
          err instanceof Error
            ? err.message
            : (
              "Could not submit "
              + "Science assessment."
            ),
        );


      } finally {

        setLoading(
          false,
        );
      }
    };


  if (
    result
  ) {

    return (

      <div className="assessment-result-page">

        <div className="assessment-result-card surface-card">

          <div
            className={
              isMastery
                ? (
                  "result-icon "
                  + "mastery-result-icon"
                )
                : (
                  "result-icon "
                  + "diagnostic-result-icon"
                )
            }
          >

            {isMastery
              ? (
                <Trophy
                  size={36}
                />
              )
              : (
                <Target
                  size={36}
                />
              )}

          </div>


          <span className="assessment-result-label">

            {
              topic.title
            }

            {" • "}

            {
              isMastery
                ? "Mastery check"
                : "Diagnostic"
            }

          </span>


          <h1>
            {
              result
                .score_percent
            }
            %
          </h1>


          <p className="result-summary">

            {
              result.mastery_state
              === "STRONG"

                ? (
                  "Your assessment shows "
                  + "strong understanding."
                )

                : result.mastery_state
                === "DEVELOPING"

                  ? (
                    "Your understanding "
                    + "is developing well."
                  )

                  : (
                    "This gives LearnFirst "
                    + "a useful starting "
                    + "point for teaching."
                  )
            }

          </p>


          <div className="result-score-bar">

            <div
              style={{
                width:
                  (
                    `${result.score_percent}%`
                  ),
              }}
            />

          </div>


          <div className="result-stats-grid">

            <div>

              <strong>

                {
                  result
                    .correct_answers
                }

              </strong>

              <span>
                Strong answers
              </span>

            </div>


            <div>

              <strong>

                {
                  result
                    .partial_answers
                }

              </strong>

              <span>
                Partial answers
              </span>

            </div>


            <div>

              <strong>

                {
                  result
                    .mastery_state
                }

              </strong>

              <span>
                Assessment level
              </span>

            </div>

          </div>


          {(
            isMastery

            && result
              .baseline_score_percent
              !== null
          ) && (

            <div className="score-comparison">

              <div className="comparison-heading">

                <Sparkles
                  size={19}
                />

                Your progress

              </div>


              <div className="comparison-scores">

                <div>

                  <span>
                    Diagnostic
                  </span>


                  <strong>

                    {
                      result
                        .baseline_score_percent
                    }
                    %

                  </strong>

                </div>


                <ArrowRight
                  size={22}
                />


                <div>

                  <span>
                    Mastery
                  </span>


                  <strong>

                    {
                      result
                        .score_percent
                    }
                    %

                  </strong>

                </div>

              </div>

            </div>
          )}


          <div className="assessment-result-actions">

            <button
              type="button"
              className="secondary-button"

              onClick={() =>
                navigate(
                  (
                    "/progress/science"
                    + `?concept=${conceptCode}`
                  ),
                )
              }
            >
              View progress
            </button>


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

          </div>


          <p className="assessment-result-note">
            This is a LearnFirst
            within-system assessment,
            not a school grade.
          </p>

        </div>

      </div>
    );
  }


  if (
    !assessment
  ) {

    return (

      <div className="assessment-intro-page">

        <button
          type="button"
          className="page-back-button"

          onClick={() =>
            navigate(
              "/learn/science",
            )
          }
        >

          <ArrowLeft
            size={18}
          />

          Science

        </button>


        <div className="assessment-intro-card surface-card">

          <div
            className={
              isMastery
                ? (
                  "assessment-intro-icon "
                  + "mastery-icon"
                )
                : (
                  "assessment-intro-icon"
                )
            }
          >

            <FlaskConical
              size={33}
            />

          </div>


          <span className="assessment-eyebrow">

            {
              topic.title
            }

            {" • "}

            {
              isMastery
                ? "Mastery check"
                : "Diagnostic"
            }

          </span>


          <h1>

            {
              isMastery
                ? (
                  "Show what you "
                  + "understand now."
                )
                : (
                  "Let's find your "
                  + "starting point."
                )
            }

          </h1>


          <p>
            Answer five Science
            questions in your own
            words. No tutor hints
            are used during this
            assessment.
          </p>


          <div className="assessment-intro-details">

            <div>
              <Check size={18} />
              5 questions
            </div>


            <div>
              <Check size={18} />
              No hints
            </div>


            <div>
              <Check size={18} />
              Partial understanding counts
            </div>

          </div>


          {error && (

            <div className="error-message">
              {error}
            </div>

          )}


          <button
            type="button"
            className="primary-button assessment-begin-button"

            disabled={
              loading
            }

            onClick={() =>
              void begin()
            }
          >

            {
              loading
                ? "Preparing..."
                : "Begin"
            }


            {!loading
              && (
              <ArrowRight
                size={19}
              />
            )}

          </button>

        </div>

      </div>
    );
  }


  return (

    <div className="assessment-page">

      <header className="assessment-header">

        <button
          type="button"
          className="page-back-button"

          onClick={() =>
            navigate(
              "/learn/science",
            )
          }
        >
          <ArrowLeft
            size={18}
          />

          Exit assessment
        </button>


        <div className="assessment-header-title">

          <BrainCircuit
            size={22}
          />


          <div>

            <span>

              {
                isMastery
                  ? "Mastery check"
                  : "Diagnostic"
              }

            </span>


            <strong>
              {
                topic.title
              }
            </strong>

          </div>

        </div>

      </header>


      <div className="assessment-progress-header">

        <div>

          <span>

            Question
            {" "}
            {
              currentIndex + 1
            }
            {" "}
            of
            {" "}
            {
              assessment
                .total_questions
            }

          </span>

        </div>


        <div className="assessment-progress-track">

          <div
            style={{
              width:
                (
                  `${
                    (
                      (
                        currentIndex + 1
                      )
                      / assessment
                        .total_questions
                    )
                    * 100
                  }%`
                ),
            }}
          />

        </div>

      </div>


      <section className="assessment-question-card surface-card">

        <div className="question-difficulty">

          {
            currentQuestion
              ?.difficulty
          }

        </div>


        <span className="question-label">
          Explain in your own words
        </span>


        <div className="assessment-problem">

          {
            currentQuestion
              ?.prompt
          }

        </div>


        <label
          htmlFor="science-assessment-answer"
          className="field-label"
        >
          Your explanation
        </label>


        <textarea
          id="science-assessment-answer"
          className="assessment-answer-input"

          rows={5}

          value={
            currentAnswer
          }

          disabled={
            loading
          }

          placeholder={
            "Explain what you understand..."
          }

          onChange={(event) =>
            updateAnswer(
              event
                .target
                .value,
            )
          }
        />


        {error && (

          <div className="error-message">
            {error}
          </div>

        )}


        <div className="assessment-navigation">

          <button
            type="button"
            className="secondary-button"

            disabled={
              currentIndex === 0
              || loading
            }

            onClick={
              previous
            }
          >

            <ArrowLeft
              size={18}
            />

            Previous

          </button>


          {currentIndex
            === (
              assessment
                .total_questions
              - 1
            )
            ? (

              <button
                type="button"
                className="primary-button"

                disabled={
                  loading
                }

                onClick={() =>
                  void finish()
                }
              >

                {
                  loading
                    ? "Checking..."
                    : "Finish"
                }

              </button>

            )
            : (

              <button
                type="button"
                className="primary-button"

                disabled={
                  loading
                }

                onClick={
                  next
                }
              >

                Next

                <ArrowRight
                  size={18}
                />

              </button>
            )}

        </div>

      </section>

    </div>
  );
}
import {
  ArrowLeft,
  ArrowRight,
  BrainCircuit,
  Check,
  ClipboardCheck,
  Sparkles,
  Target,
  Trophy,
} from "lucide-react";

import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  useNavigate,
  useParams,
  useSearchParams,
} from "react-router";

import {
  startAssessment,
  submitAssessment,
} from "../api/assessments";

import {
  getLearningSession,
} from "../api/sessions";

import {
  DEFAULT_MATH_CONCEPT_CODE,
  getMathTopic,
} from "../data/mathTopics";

import type {
  AssessmentAnswerInput,
  AssessmentResult,
  AssessmentStartResponse,
  AssessmentType,
} from "../types/assessment";

import {
  getStoredStudent,
} from "../utils/studentStorage";


function getAssessmentType(
  value: string | undefined,
): AssessmentType {

  return (
    value
      ?.toLowerCase()
    === "mastery"
  )
    ? "MASTERY"
    : "DIAGNOSTIC";
}


function scoreMessage(
  score: number,
): string {

  if (
    score >= 80
  ) {

    return (
      "You have a strong "
      + "understanding of "
      + "this concept."
    );
  }


  if (
    score >= 60
  ) {

    return (
      "You understand much of "
      + "the idea. A little more "
      + "practice will help."
    );
  }


  if (
    score >= 40
  ) {

    return (
      "You have a useful starting "
      + "point. LearnFirst will "
      + "guide you from here."
    );
  }


  return (
    "This gives LearnFirst "
    + "a clear place to begin "
    + "teaching."
  );
}


export default function AssessmentPage() {

  const navigate =
    useNavigate();


  const {
    assessmentType:
      assessmentTypeParam,
  } = useParams<{
    assessmentType: string;
  }>();


  const [
    searchParams,
  ] = useSearchParams();


  const student =
    getStoredStudent();


  const assessmentType =
    getAssessmentType(
      assessmentTypeParam,
    );


  const sessionId =
    searchParams.get(
      "sessionId",
    );


  const conceptFromUrl =
    searchParams.get(
      "concept",
    );


  const [
    conceptCode,
    setConceptCode,
  ] = useState(
    conceptFromUrl
    ?? DEFAULT_MATH_CONCEPT_CODE,
  );


  const topic =
    getMathTopic(
      conceptCode,
    );


  const [
    assessment,
    setAssessment,
  ] = useState<
    AssessmentStartResponse | null
  >(null);


  const [
    currentIndex,
    setCurrentIndex,
  ] = useState(0);


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
    result,
    setResult,
  ] = useState<
    AssessmentResult | null
  >(null);


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


  const isMastery =
    assessmentType
    === "MASTERY";


  useEffect(
    () => {

      if (
        conceptFromUrl
      ) {

        setConceptCode(
          conceptFromUrl,
        );

        return;
      }


      if (
        !sessionId
      ) {

        return;
      }


      const resolveSessionConcept =
        async () => {

          try {

            const session =
              await getLearningSession(
                sessionId,
              );


            if (
              session.concept_code
            ) {

              setConceptCode(
                session
                  .concept_code,
              );
            }


          } catch {

            // The assessment API
            // will provide the final
            // validation if needed.
          }
        };


      void resolveSessionConcept();

    },
    [
      conceptFromUrl,
      sessionId,
    ],
  );


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
        ] ?? ""
      )
      : "";


  const progressPercent =
    assessment
      ? (
        (
          currentIndex + 1
        )
        / assessment
            .total_questions
        * 100
      )
      : 0;


  const answeredCount =
    useMemo(
      () =>
        Object.values(
          answers,
        ).filter(
          (value) =>
            value.trim(),
        ).length,

      [
        answers,
      ],
    );


  const mathReturnPath =
    (
      "/learn/math"
      + `?concept=${conceptCode}`
    );


  const beginAssessment =
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

        let finalConceptCode =
          conceptCode;


        if (
          sessionId
          && !conceptFromUrl
        ) {

          const session =
            await getLearningSession(
              sessionId,
            );


          if (
            session.concept_code
          ) {

            finalConceptCode =
              session
                .concept_code;


            setConceptCode(
              finalConceptCode,
            );
          }
        }


        const data =
          await startAssessment({

            student_id:
              student.id,

            session_id:
              sessionId,

            subject:
              "MATH",

            concept_code:
              finalConceptCode,

            assessment_type:
              assessmentType,
          });


        setAssessment(
          data,
        );


        setCurrentIndex(
          0,
        );


        setAnswers(
          {},
        );


      } catch (err) {

        setError(
          err instanceof Error
            ? err.message
            : (
              "Could not start "
              + "the assessment."
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


  const nextQuestion =
    () => {

      if (
        !currentAnswer
          .trim()
      ) {

        setError(
          "Try answering this "
          + "question first.",
        );

        return;
      }


      setError(
        null,
      );


      if (
        assessment

        && currentIndex
        < (
          assessment
            .total_questions
          - 1
        )
      ) {

        setCurrentIndex(
          (
            current,
          ) =>
            current + 1,
        );
      }
    };


  const previousQuestion =
    () => {

      setError(
        null,
      );


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


  const finishAssessment =
    async () => {

      if (
        !assessment
        || !currentQuestion
      ) {

        return;
      }


      if (
        !currentAnswer
          .trim()
      ) {

        setError(
          "Try answering this "
          + "question first.",
        );

        return;
      }


      const completeAnswers = {

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
                completeAnswers[
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
          + "five questions.",
        );

        return;
      }


      const payload:
        AssessmentAnswerInput[] =
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
                  completeAnswers[
                    question
                      .question_id
                  ]
                    .trim(),
              }),
            );


      setLoading(
        true,
      );


      setError(
        null,
      );


      try {

        const data =
          await submitAssessment(
            assessment
              .assessment_id,

            payload,
          );


        setAnswers(
          completeAnswers,
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
              + "the assessment."
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

    const gain =
      result
        .score_gain_percentage_points;


    const resultTopic =
      getMathTopic(
        result
          .concept_code,
      );


    const resultMathPath =
      (
        "/learn/math"
        + `?concept=${result.concept_code}`
      );


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
              resultTopic.title
            }

            {" • "}

            {isMastery
              ? "Mastery check"
              : "Diagnostic"}

          </span>


          <h1>
            {
              result.score_percent
            }
            %
          </h1>


          <p className="result-summary">

            {
              scoreMessage(
                result
                  .score_percent,
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
                /
                {
                  result
                    .total_questions
                }

              </strong>

              <span>
                Correct
              </span>

            </div>


            <div>

              <strong>

                {
                  result
                    .mastery_state
                    .replace(
                      "_",
                      " ",
                    )
                }

              </strong>

              <span>
                Understanding
              </span>

            </div>


            <div>

              <strong>

                {
                  result
                    .recommended_difficulty
                }

              </strong>

              <span>
                Next level
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
                    Starting score
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
                    Mastery score
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


              {gain !== null && (

                <div
                  className={
                    gain > 0
                      ? (
                        "gain-pill "
                        + "positive"
                      )
                      : "gain-pill"
                  }
                >

                  {
                    gain > 0
                      ? "+"
                      : ""
                  }

                  {gain}

                  {" "}
                  percentage points

                </div>
              )}

            </div>
          )}


          <div className="assessment-result-actions">

            <button
              type="button"
              className="secondary-button"

              onClick={() =>
                navigate(
                  "/dashboard",
                )
              }
            >
              Dashboard
            </button>


            <button
              type="button"
              className="primary-button"

              onClick={() =>
                navigate(
                  resultMathPath,
                )
              }
            >

              {
                isMastery
                  ? (
                    "Continue "
                    + resultTopic
                      .shortTitle
                  )
                  : (
                    "Start guided learning"
                  )
              }

              <ArrowRight
                size={18}
              />

            </button>

          </div>


          <p className="assessment-result-note">
            This score describes
            your performance on this
            LearnFirst assessment.
            It is not a school grade.
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
              isMastery
                && sessionId
                  ? (
                    "/learn/math/"
                    + `session/${sessionId}`
                  )
                  : mathReturnPath,
            )
          }
        >
          <ArrowLeft
            size={18}
          />

          Back
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

            {isMastery
              ? (
                <Trophy
                  size={33}
                />
              )
              : (
                <ClipboardCheck
                  size={33}
                />
              )}

          </div>


          <span className="assessment-eyebrow">

            {
              topic.title
            }

            {" • "}

            {isMastery
              ? "Mastery check"
              : "Quick diagnostic"}

          </span>


          <h1>

            {isMastery
              ? (
                "Let's see what "
                + "you can do now."
              )
              : (
                "Let's find your "
                + "starting point."
              )}

          </h1>


          <p>

            {isMastery
              ? (
                "You'll solve five "
                + "fresh problems "
                + "without hints."
              )
              : (
                "Answer five short "
                + "questions from "
                + topic.title
                + ". LearnFirst will "
                + "use your result to "
                + "adapt this topic."
              )}

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
              Topic-specific score
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
              void beginAssessment()
            }
          >

            {
              loading
                ? "Preparing questions..."
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
              mathReturnPath,
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

              {isMastery
                ? "Mastery check"
                : "Diagnostic"}

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
            {currentIndex + 1}
            {" "}
            of
            {" "}
            {
              assessment
                .total_questions
            }
          </span>


          <strong>
            {answeredCount}
            {" "}
            answered
          </strong>

        </div>


        <div className="assessment-progress-track">

          <div
            style={{
              width:
                (
                  `${progressPercent}%`
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

          {
            topic
              .assessmentQuestionLabel
          }

        </span>


        <div className="assessment-problem">

          {
            currentQuestion
              ?.prompt
          }

        </div>


        <label
          htmlFor="assessment-answer"
          className="field-label"
        >
          Your answer
        </label>


        <input
          id="assessment-answer"
          className="assessment-answer-input"

          value={
            currentAnswer
          }

          autoFocus

          disabled={
            loading
          }

          placeholder={
            topic
              .answerPlaceholder
          }

          onChange={(event) =>
            updateAnswer(
              event
                .target
                .value,
            )
          }

          onKeyDown={(event) => {

            if (
              event.key
              === "Enter"
            ) {

              event.preventDefault();


              if (
                currentIndex
                === (
                  assessment
                    .total_questions
                  - 1
                )
              ) {

                void finishAssessment();

              } else {

                nextQuestion();
              }
            }
          }}
        />


        <p className="assessment-answer-help">

          {
            topic
              .answerHelp
          }

        </p>


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
              previousQuestion
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
                  void finishAssessment()
                }
              >

                {
                  loading
                    ? "Checking..."
                    : "Finish"
                }


                {!loading
                  && (
                  <Check
                    size={18}
                  />
                )}

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
                  nextQuestion
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


      <p className="assessment-footer-message">
        Take your time. This
        assessment only describes
        your current LearnFirst
        performance for {
          topic.title
        }.
      </p>

    </div>
  );
}
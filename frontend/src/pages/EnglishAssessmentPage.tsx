
import {
  ArrowLeft,
  BookOpen,
  CheckCircle2,
  ClipboardCheck,
  Trophy,
} from "lucide-react";

import {
  type FormEvent,
  useEffect,
  useState,
} from "react";

import {
  useNavigate,
  useParams,
  useSearchParams,
} from "react-router";

import {
  startEnglishAssessment,
  submitEnglishAssessment,
  type EnglishAssessmentStartResponse,
} from "../api/englishAssessments";

import { getLearningSession } from "../api/sessions";

import {
  getEnglishTopic,
  getEnglishTopicForAge,
} from "../data/englishTopics";

import type {
  AssessmentResult,
  AssessmentType,
} from "../types/assessment";

import { getStoredStudent } from "../utils/studentStorage";


export default function EnglishAssessmentPage() {

  const navigate = useNavigate();

  const { assessmentType: typeParam } = useParams<{
    assessmentType: string;
  }>();

  const [searchParams] = useSearchParams();

  const student = getStoredStudent();

  const sessionId = searchParams.get("sessionId");
  const requestedConcept = searchParams.get("concept");

  const assessmentType: AssessmentType =
    typeParam?.toLowerCase() === "mastery"
      ? "MASTERY"
      : "DIAGNOSTIC";

  const [assessment, setAssessment] =
    useState<EnglishAssessmentStartResponse | null>(null);

  const [answers, setAnswers] =
    useState<Record<string, string>>({});

  const [result, setResult] =
    useState<AssessmentResult | null>(null);

  const [loading, setLoading] = useState(false);

  const [submitting, setSubmitting] = useState(false);

  const [error, setError] =
    useState<string | null>(null);


  useEffect(() => {
    setAssessment(null);
    setAnswers({});
    setResult(null);
    setError(null);
  }, [
    assessmentType,
    sessionId,
    requestedConcept,
  ]);


  const conceptCode =
    requestedConcept
    ?? getEnglishTopicForAge(
      student?.age ?? 7
    ).conceptCode;

  const topic = getEnglishTopic(
    assessment?.concept_code ?? conceptCode
  );


  // ==================================
  // Start an assessment explicitly
  // ==================================

  async function startAssessment() {
    if (!student || loading) return;

    setLoading(true);
    setError(null);

    try {
      let code = conceptCode;

      if (sessionId) {
        const session =
          await getLearningSession(sessionId);

        if (
          session.student_id !== student.id
          || session.subject !== "ENGLISH"
        ) {
          throw new Error(
            "This English learning session "
            + "does not belong to the current learner."
          );
        }

        code = session.concept_code ?? code;
      }

      const response =
        await startEnglishAssessment({
          student_id: student.id,
          session_id: sessionId,
          subject: "ENGLISH",
          concept_code: code,
          assessment_type: assessmentType,
        });

      setAssessment(response);
      setAnswers({});
      setResult(null);

    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not start English assessment."
      );

    } finally {
      setLoading(false);
    }
  }


  // ==================================
  // Submit all answers
  // ==================================

  const allAnswered = Boolean(
    assessment
    && assessment.questions.every(
      (question) =>
        (answers[question.question_id] ?? "")
          .trim().length > 0
    )
  );


  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (
      !assessment
      || !allAnswered
      || submitting
    ) {
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      const submittedAnswers =
        assessment.questions.map(
          (question) => ({
            question_id: question.question_id,
            response: (
              answers[question.question_id] ?? ""
            ).trim(),
          })
        );

      const response =
        await submitEnglishAssessment(
          assessment.assessment_id,
          submittedAnswers,
        );

      setResult(response);

    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not submit your assessment."
      );

    } finally {
      setSubmitting(false);
    }
  }


  return (
    <div className="dashboard-page">

      <button
        type="button"
        className="page-back-button"
        onClick={() => navigate("/progress/english")}
      >
        <ArrowLeft size={18} />
        English Progress
      </button>


      <section className="dashboard-hero">

        <div>

          <div className="dashboard-kicker">
            <BookOpen size={16} />
            English Assessment
          </div>

          <h1>
            {assessmentType === "DIAGNOSTIC"
              ? "English Diagnostic"
              : "English Mastery Check"}
          </h1>

          <p>
            {assessmentType === "DIAGNOSTIC"
              ? "Show what you already understand before learning."
              : "Try new questions to check what you've learned."}
          </p>

        </div>

      </section>


      {error && (
        <div
          className="science-error surface-card"
          role="alert"
        >
          <strong>Assessment problem</strong>
          <p>{error}</p>
        </div>
      )}


      {/* Before assessment starts */}

      {!assessment && !result && (

        <section className="surface-card progress-detail-card">

          <div className="progress-card-heading">

            <div>
              <span className="small-label">
                Current English concept
              </span>
              <h2>{topic.title}</h2>
            </div>

            <ClipboardCheck size={28} />

          </div>

          <p>{topic.description}</p>

          <p>
            Answer each question independently.
            Hints are not available during
            Diagnostic or Mastery assessments.
          </p>

          <button
            type="button"
            className="primary-button"
            disabled={loading || !student}
            onClick={() => void startAssessment()}
          >
            <ClipboardCheck size={18} />

            {loading
              ? "Preparing assessment..."
              : "Start assessment"}
          </button>

        </section>

      )}


      {/* Assessment questions */}

      {assessment && !result && (

        <section className="surface-card progress-detail-card">

          <div className="progress-card-heading">

            <div>
              <span className="small-label">
                {topic.title}
              </span>

              <h2>
                {assessment.total_questions} questions
              </h2>
            </div>

            <ClipboardCheck size={28} />

          </div>

          <form
            onSubmit={(event) =>
              void handleSubmit(event)
            }
            style={{
              display: "grid",
              gap: "22px",
              marginTop: "24px",
            }}
          >

            {assessment.questions.map(
              (question, index) => (

                <div
                  key={question.question_id}
                  style={{
                    display: "grid",
                    gap: "10px",
                  }}
                >

                  <label
                    htmlFor={question.question_id}
                    style={{ fontWeight: 650 }}
                  >
                    {index + 1}. {question.prompt}
                  </label>

                  <textarea
                    id={question.question_id}
                    rows={3}
                    maxLength={1000}
                    required
                    disabled={submitting}
                    value={
                      answers[question.question_id] ?? ""
                    }
                    placeholder="Write your answer..."
                    onChange={(event) =>
                      setAnswers((current) => ({
                        ...current,
                        [question.question_id]:
                          event.target.value,
                      }))
                    }
                    style={{
                      width: "100%",
                      padding: "12px",
                      border: "1px solid #d9deea",
                      borderRadius: "12px",
                      font: "inherit",
                      resize: "vertical",
                    }}
                  />

                </div>

              )
            )}

            <button
              type="submit"
              className="primary-button"
              disabled={!allAnswered || submitting}
            >
              {submitting
                ? "Checking answers..."
                : "Submit assessment"}
            </button>

          </form>

        </section>

      )}


      {/* Assessment results */}

      {result && (

        <section className="surface-card progress-detail-card">

          <Trophy size={34} />

          <h2>Assessment completed</h2>

          <div className="progress-stats">

            <div>
              <strong>
                {result.score_percent}%
              </strong>
              <span>Score</span>
            </div>

            <div>
              <strong>
                {result.correct_answers}
                /{result.total_questions}
              </strong>
              <span>Correct answers</span>
            </div>

            <div>
              <strong>
                {result.mastery_state
                  .replaceAll("_", " ")}
              </strong>
              <span>Assessment level</span>
            </div>

          </div>


          {result.score_gain_percentage_points !== null
            && (
              <p>
                Change from Diagnostic:{" "}
                {result.score_gain_percentage_points > 0
                  ? "+"
                  : ""}
                {result.score_gain_percentage_points}
                {" "}percentage points
              </p>
            )}


          <div
            style={{
              display: "grid",
              gap: "10px",
              marginTop: "24px",
            }}
          >

            {result.answers.map((answer) => (

              <div key={answer.question_id}>

                <CheckCircle2
                  size={16}
                  style={{ marginRight: "8px" }}
                />

                {answer.question_id}:{" "}
                {answer.status.replaceAll("_", " ")}

              </div>

            ))}

          </div>


          <button
            type="button"
            className="primary-button"
            style={{ marginTop: "24px" }}
            onClick={() =>
              navigate("/progress/english")
            }
          >
            View English Progress
          </button>

        </section>

      )}

    </div>
  );
}

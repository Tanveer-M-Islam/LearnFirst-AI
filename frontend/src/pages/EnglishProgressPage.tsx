
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  BrainCircuit,
  CheckCircle2,
  ClipboardCheck,
  Sparkles,
  Target,
  Trophy,
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
  getEnglishProgress,
  type EnglishProgress,
} from "../api/englishProgress";

import {
  getEnglishTopic,
  getEnglishTopicForAge,
} from "../data/englishTopics";

import type {
  StudentCurriculumPath,
} from "../types/curriculum";

import {
  getStoredStudent,
} from "../utils/studentStorage";


function readableLabel(value: string): string {
  return value
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/\b\w/g, (character) =>
      character.toUpperCase()
    );
}


export default function EnglishProgressPage() {

  const navigate = useNavigate();

  const student = getStoredStudent();

  const studentId = student?.id;
  const studentAge = student?.age ?? 7;

  const [curriculum, setCurriculum] =
    useState<StudentCurriculumPath | null>(null);

  const [progress, setProgress] =
    useState<EnglishProgress | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);


  useEffect(() => {

    if (!studentId) {
      setLoading(false);
      return;
    }

    let cancelled = false;

    async function load() {
      setLoading(true);
      setError(null);

      try {
        const path =
          await getStudentCurriculumPath(
            studentId!,
            "ENGLISH",
          );

        if (cancelled) return;

        setCurriculum(path);

        const conceptCode =
          path.recommended_concept?.concept_code
          ?? path.target_concept?.concept_code
          ?? getEnglishTopicForAge(studentAge).conceptCode;

        const result =
          await getEnglishProgress(
            studentId!,
            conceptCode,
          );

        if (!cancelled) {
          setProgress(result);
        }

      } catch (err) {

        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Could not load English progress."
          );
        }

      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void load();

    return () => {
      cancelled = true;
    };

  }, [studentId, studentAge]);


  const recommended =
    curriculum?.recommended_concept;

  const target =
    curriculum?.target_concept;

  const review =
    curriculum?.prerequisite_review_concept;

  const conceptCode =
    recommended?.concept_code
    ?? target?.concept_code
    ?? progress?.concept_code
    ?? getEnglishTopicForAge(studentAge).conceptCode;

  const topic =
    getEnglishTopic(conceptCode);


  function openAssessment(
    type: "diagnostic" | "mastery",
  ) {
    navigate(
      `/assessments/english/${type}`
      + `?concept=${encodeURIComponent(conceptCode)}`
    );
  }


  const scoreGain = (
    progress?.diagnostic
    && progress?.mastery
  )
    ? (
        progress.mastery.score_percent
        - progress.diagnostic.score_percent
      )
    : null;


  return (
    <div className="dashboard-page">

      <button
        type="button"
        className="page-back-button"
        onClick={() => navigate("/progress")}
      >
        <ArrowLeft size={18} />
        Progress
      </button>


      <section className="dashboard-hero">

        <div>

          <div className="dashboard-kicker">
            <BookOpen size={16} />
            English progress
          </div>

          <h1>Your English learning</h1>

          <p>
            Follow your age-level curriculum,
            complete assessments, and improve
            your understanding step by step.
          </p>

        </div>

      </section>


      {loading && (
        <div className="surface-card progress-loading-card">
          <BrainCircuit size={24} />
          Loading English progress...
        </div>
      )}


      {error && (
        <div
          className="science-error surface-card"
          role="alert"
        >
          <strong>Could not load progress</strong>
          <p>{error}</p>
        </div>
      )}


      {!loading && !error && (

        <>

          {/* Age-specific curriculum */}

          <section className="progress-focus-grid">

            <article className="surface-card progress-focus-card">

              <div className="progress-focus-heading">

                <div className="subject-icon">
                  <BookOpen size={26} />
                </div>

                <div>
                  <span className="small-label">
                    Current curriculum
                  </span>

                  <h2>{topic.title}</h2>
                </div>

              </div>

              <p>{topic.description}</p>

              <div className="progress-status-row">

                <div>
                  <span>Age</span>
                  <strong>{studentAge}</strong>
                </div>

                <div>
                  <span>Curriculum status</span>

                  <strong>
                    {recommended
                      ? readableLabel(recommended.status)
                      : "Ready"}
                  </strong>
                </div>

                <div>
                  <span>Mastery</span>

                  <strong>
                    {progress
                      ? readableLabel(progress.mastery_state)
                      : "Not Started"}
                  </strong>
                </div>

              </div>

            </article>

          </section>


          {/* Prerequisite review */}

          {review
            && review.concept_code
              !== recommended?.concept_code
            && (

              <section className="surface-card prerequisite-review-card">

                <Target size={22} />

                <div>
                  <span className="small-label">
                    Prerequisite review
                  </span>

                  <h3>{review.title}</h3>

                  <p>
                    A previous learning concept
                    needs additional review.
                  </p>
                </div>

              </section>

            )}


          {/* Diagnostic and Mastery */}

          <section className="surface-card progress-detail-card">

            <div className="progress-card-heading">

              <div>
                <span className="small-label">
                  English assessments
                </span>

                <h2>
                  Diagnostic and Mastery
                </h2>
              </div>

              <ClipboardCheck size={27} />

            </div>


            <div className="progress-stats">

              <div>
                <strong>
                  {progress?.diagnostic
                    ? `${progress.diagnostic.score_percent}%`
                    : "Not taken"}
                </strong>

                <span>Diagnostic score</span>
              </div>

              <div>
                <strong>
                  {progress?.mastery
                    ? `${progress.mastery.score_percent}%`
                    : "Not taken"}
                </strong>

                <span>Mastery score</span>
              </div>

              <div>
                <strong>
                  {scoreGain !== null
                    ? `${scoreGain > 0 ? "+" : ""}${scoreGain.toFixed(2)}`
                    : "—"}
                </strong>

                <span>
                  Change (percentage points)
                </span>
              </div>

            </div>


            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: "12px",
                marginTop: "24px",
              }}
            >

              <button
                type="button"
                className="secondary-button"
                onClick={() =>
                  openAssessment("diagnostic")
                }
              >
                <ClipboardCheck size={17} />
                Take Diagnostic
              </button>

              <button
                type="button"
                className="primary-button"
                onClick={() =>
                  openAssessment("mastery")
                }
              >
                <Trophy size={17} />
                Take Mastery Check
              </button>

            </div>

          </section>


          {/* Existing learning evidence */}

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

              <Sparkles size={27} />

            </div>


            <div className="progress-stats">

              <div>
                <strong>
                  {progress?.total_attempts ?? 0}
                </strong>
                <span>Attempts</span>
              </div>

              <div>
                <strong>
                  {progress?.independent_attempts ?? 0}
                </strong>
                <span>Independent tries</span>
              </div>

              <div>
                <strong>
                  {progress && progress.total_attempts > 0
                    ? `${progress.understanding_score_percent}%`
                    : "No attempts yet"}
                </strong>

                <span>Understanding</span>
              </div>

            </div>


            {progress?.mastery_state === "STRONG" && (

              <div className="habit-tip">
                <CheckCircle2 size={16} />
                Strong mastery recorded.
              </div>

            )}

          </section>


          {/* Age-level target */}

          {target
            && target.concept_code !== conceptCode
            && (

              <section className="surface-card target-return-card">

                <span className="small-label">
                  Age-level target
                </span>

                <h3>{target.title}</h3>

                <p>
                  Return to this concept after
                  completing prerequisite review.
                </p>

              </section>

            )}


          <button
            type="button"
            className="primary-button"
            onClick={() =>
              navigate("/learn/english")
            }
          >
            Continue English
            <ArrowRight size={18} />
          </button>

        </>

      )}

    </div>
  );
}

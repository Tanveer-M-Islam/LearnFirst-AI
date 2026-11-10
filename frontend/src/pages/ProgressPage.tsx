
import {
  ArrowLeft,
  ArrowRight,
  BrainCircuit,
  Calculator,
  CheckCircle2,
  Sparkles,
  Target,
} from "lucide-react";

import { useEffect, useState } from "react";
import { useNavigate } from "react-router";

import AssessmentProgressCard from "../components/progress/AssessmentProgressCard";

import { getConceptProgress } from "../api/assessments";
import { getStudentCurriculumPath } from "../api/curriculum";

import { getMathTopic } from "../data/mathTopics";

import type {
  ConceptProgress,
} from "../types/assessment";

import type {
  StudentCurriculumPath,
} from "../types/curriculum";

import { getStoredStudent } from "../utils/studentStorage";


function readableLabel(value: string): string {
  return value
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/\b\w/g, (char) => char.toUpperCase());
}


export default function ProgressPage() {
  const navigate = useNavigate();

  const student = getStoredStudent();
  const studentId = student?.id;

  const [curriculum, setCurriculum] =
    useState<StudentCurriculumPath | null>(null);

  const [progress, setProgress] =
    useState<ConceptProgress | null>(null);

  const [loading, setLoading] = useState(true);

  const [error, setError] =
    useState<string | null>(null);


  // ======================================
  // Load Math curriculum and progress
  // ======================================

  useEffect(() => {
    if (!studentId) {
      setLoading(false);
      setError("Please sign in to view your progress.");
      return;
    }

    let active = true;

    async function loadProgress() {
      setLoading(true);
      setError(null);
      setCurriculum(null);
      setProgress(null);

      try {
        const path = await getStudentCurriculumPath(
          studentId!,
          "MATH",
        );

        if (!active) return;

        setCurriculum(path);

        const conceptCode =
          path.recommended_concept?.concept_code
          ?? path.target_concept?.concept_code;

        if (conceptCode) {
          const result = await getConceptProgress(
            studentId!,
            conceptCode,
          );

          if (active) {
            setProgress(result);
          }
        }
      } catch (err) {
        if (active) {
          setError(
            err instanceof Error
              ? err.message
              : "Could not load Math progress."
          );
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    void loadProgress();

    return () => {
      active = false;
    };
  }, [studentId]);


  // ======================================
  // Curriculum information
  // ======================================

  const recommendedConcept =
    curriculum?.recommended_concept;

  const targetConcept =
    curriculum?.target_concept;

  const reviewConcept =
    curriculum?.prerequisite_review_concept;

  const topic = recommendedConcept
    ? getMathTopic(recommendedConcept.concept_code)
    : null;

  const conceptCode =
    recommendedConcept?.concept_code
    ?? targetConcept?.concept_code
    ?? "";


  function openAssessment(
    type: "diagnostic" | "mastery",
  ) {
    if (!conceptCode) return;

    navigate(
      `/assessments/math/${type}`
      + `?concept=${encodeURIComponent(conceptCode)}`
    );
  }


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


      {/* Page introduction */}

      <section className="dashboard-hero">
        <div>
          <div className="dashboard-kicker">
            <Calculator size={16} />
            Math progress
          </div>

          <h1>Your Math learning</h1>

          <p>
            Follow your age-level curriculum,
            review earlier concepts when needed,
            and track your learning progress.
          </p>
        </div>
      </section>


      {/* Loading */}

      {loading && (
        <div className="surface-card progress-loading-card">
          <BrainCircuit size={24} />
          Loading Math progress...
        </div>
      )}


      {/* Error */}

      {error && (
        <div
          className="science-error surface-card"
          role="alert"
        >
          <strong>Could not load progress</strong>
          <p>{error}</p>
        </div>
      )}


      {!loading && !error && !recommendedConcept && (
        <div className="surface-card progress-detail-card">
          <h2>No available Math concept</h2>
          <p>
            An implemented Math concept could not be
            selected for your current learning path.
          </p>
        </div>
      )}


      {/* Main content */}

      {!loading && !error && recommendedConcept && (
        <>

          {/* Age-specific curriculum */}

          <section className="progress-focus-grid">
            <article className="surface-card progress-focus-card">

              <div className="progress-focus-heading">
                <div className="subject-icon">
                  <Calculator size={26} />
                </div>

                <div>
                  <span className="small-label">
                    Current curriculum
                  </span>

                  <h2>
                    {topic?.title
                      ?? recommendedConcept.title}
                  </h2>
                </div>
              </div>

              <p>
                {topic?.description
                  ?? recommendedConcept.description}
              </p>

              <div className="progress-status-row">

                <div>
                  <span>Curriculum status</span>
                  <strong>
                    {readableLabel(
                      recommendedConcept.status
                    )}
                  </strong>
                </div>

                <div>
                  <span>Age</span>
                  <strong>{student?.age ?? "—"}</strong>
                </div>

                <div>
                  <span>Mastery</span>
                  <strong>
                    {readableLabel(
                      progress?.current_mastery_state
                        ?? recommendedConcept.mastery_state
                    )}
                  </strong>
                </div>

              </div>
            </article>
          </section>


          {/* Prerequisite review */}

          {reviewConcept
            && reviewConcept.concept_code
              !== recommendedConcept.concept_code
            && (
              <section className="surface-card prerequisite-review-card">

                <Target size={22} />

                <div>
                  <span className="small-label">
                    Prerequisite review
                  </span>

                  <h3>{reviewConcept.title}</h3>

                  <p>
                    Your learning evidence suggests
                    reviewing this earlier concept
                    before continuing.
                  </p>
                </div>

              </section>
            )}


          {/* New Diagnostic/Mastery card */}

          <AssessmentProgressCard
            subject="Math"
            diagnostic={progress?.diagnostic}
            mastery={progress?.mastery}
            onDiagnostic={() =>
              openAssessment("diagnostic")
            }
            onMastery={() =>
              openAssessment("mastery")
            }
          />


          {/* Learning evidence */}

          {progress && (
            <section className="surface-card progress-detail-card">

              <div className="progress-card-heading">
                <div>
                  <span className="small-label">
                    Learning evidence
                  </span>

                  <h2>Current concept progress</h2>
                </div>

                <Sparkles size={27} />
              </div>

              <div className="progress-stats">

                <div>
                  <strong>
                    {progress.learning_metrics.total_attempts}
                  </strong>
                  <span>Attempts</span>
                </div>

                <div>
                  <strong>
                    {progress.learning_metrics.independent_attempts}
                  </strong>
                  <span>Independent tries</span>
                </div>

                <div>
                  <strong>
                    {readableLabel(
                      progress.current_mastery_state
                    )}
                  </strong>
                  <span>Mastery</span>
                </div>

              </div>

              {progress.current_mastery_state === "STRONG"
                && (
                  <div className="habit-tip">
                    <CheckCircle2 size={16} />
                    Strong mastery demonstrated.
                  </div>
                )}
            </section>
          )}


          {/* Return to age-level target */}

          {targetConcept
            && targetConcept.concept_code
              !== recommendedConcept.concept_code
            && (
              <section className="surface-card target-return-card">
                <span className="small-label">
                  Age-level target
                </span>

                <h3>{targetConcept.title}</h3>

                <p>
                  After prerequisite review,
                  LearnFirst can return you to
                  your age-level curriculum.
                </p>
              </section>
            )}


          <button
            type="button"
            className="primary-button"
            onClick={() => navigate("/learn/math")}
          >
            Continue Math
            <ArrowRight size={18} />
          </button>

        </>
      )}

    </div>
  );
}


import {
  ArrowLeft,
  ArrowRight,
  BrainCircuit,
  CheckCircle2,
  FlaskConical,
  Sparkles,
  Target,
} from "lucide-react";

import { useEffect, useState } from "react";
import { useNavigate } from "react-router";

import AssessmentProgressCard from "../components/progress/AssessmentProgressCard";

import { getStudentCurriculumPath } from "../api/curriculum";

import { getScienceAdaptivePlan } from "../api/scienceAdaptive";

import {
  getScienceAssessmentProgress,
} from "../api/scienceAssessments";

import { getScienceTopic } from "../data/scienceTopics";

import type {
  StudentCurriculumPath,
} from "../types/curriculum";

import type {
  ScienceAdaptivePlan,
} from "../types/scienceAdaptive";

import type {
  ScienceAssessmentProgress,
} from "../types/scienceAssessment";

import { getStoredStudent } from "../utils/studentStorage";


function readableLabel(value: string): string {
  return value
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/\b\w/g, (char) => char.toUpperCase());
}


function errorMessage(error: unknown): string {
  return error instanceof Error
    ? error.message
    : "The request could not be completed.";
}


export default function ScienceProgressPage() {
  const navigate = useNavigate();

  const student = getStoredStudent();
  const studentId = student?.id;

  const [curriculum, setCurriculum] =
    useState<StudentCurriculumPath | null>(null);

  const [plan, setPlan] =
    useState<ScienceAdaptivePlan | null>(null);

  const [assessmentProgress, setAssessmentProgress] =
    useState<ScienceAssessmentProgress | null>(null);

  const [loading, setLoading] = useState(true);

  const [error, setError] =
    useState<string | null>(null);

  const [assessmentError, setAssessmentError] =
    useState<string | null>(null);


  // ======================================
  // Load Science progress
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
      setAssessmentError(null);
      setCurriculum(null);
      setPlan(null);
      setAssessmentProgress(null);

      try {
        const path = await getStudentCurriculumPath(
          studentId!,
          "SCIENCE",
        );

        if (!active) return;

        setCurriculum(path);

        const conceptCode =
          path.recommended_concept?.concept_code
          ?? path.target_concept?.concept_code;

        if (!conceptCode) return;

        // Both requests run together, but an assessment
        // failure must not hide the adaptive plan.
        const [adaptiveResult, assessmentResult] =
          await Promise.allSettled([
            getScienceAdaptivePlan(
              studentId!,
              conceptCode,
            ),
            getScienceAssessmentProgress(
              studentId!,
              conceptCode,
            ),
          ]);

        if (!active) return;

        if (adaptiveResult.status === "rejected") {
          throw adaptiveResult.reason;
        }

        setPlan(adaptiveResult.value);

        if (assessmentResult.status === "fulfilled") {
          setAssessmentProgress(assessmentResult.value);
        } else {
          setAssessmentError(
            errorMessage(assessmentResult.reason)
          );
        }

      } catch (err) {
        if (active) {
          setError(
            errorMessage(err)
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
    ? getScienceTopic(recommendedConcept.concept_code)
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
      `/assessments/science/${type}`
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
            <FlaskConical size={16} />
            Science progress
          </div>

          <h1>Your Science learning</h1>

          <p>
            Track Science understanding, independent
            learning, and mastery using your age-level
            curriculum and learning evidence.
          </p>
        </div>
      </section>


      {/* Loading */}

      {loading && (
        <div className="surface-card progress-loading-card">
          <BrainCircuit size={24} />
          Loading Science progress...
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
          <h2>No available Science concept</h2>
          <p>
            An implemented Science concept could not
            be selected for your current learning path.
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
                  <FlaskConical size={26} />
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
                  <span>Understanding</span>

                  <strong>
                    {plan
                      ? `${plan.understanding_score_percent}%`
                      : "—"}
                  </strong>
                </div>

                <div>
                  <span>Mastery</span>

                  <strong>
                    {readableLabel(
                      plan?.mastery_state
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
                    reviewing this earlier Science
                    concept before continuing.
                  </p>
                </div>

              </section>
            )}


          {/* Diagnostic/Mastery assessment card */}

          <AssessmentProgressCard
            subject="Science"
            diagnostic={assessmentProgress?.diagnostic}
            mastery={assessmentProgress?.mastery}
            error={assessmentError}
            onDiagnostic={() =>
              openAssessment("diagnostic")
            }
            onMastery={() =>
              openAssessment("mastery")
            }
          />


          {/* Learning evidence */}

          {plan && (
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
                  <strong>{plan.total_attempts}</strong>
                  <span>Attempts</span>
                </div>

                <div>
                  <strong>{plan.independent_attempts}</strong>
                  <span>Independent tries</span>
                </div>

                <div>
                  <strong>
                    {plan.understanding_score_percent}%
                  </strong>
                  <span>Understanding</span>
                </div>

              </div>

              {plan.mastery_state === "STRONG" && (
                <div className="habit-tip">
                  <CheckCircle2 size={16} />
                  Strong understanding demonstrated.
                </div>
              )}

            </section>
          )}


          {/* Age-level target */}

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
                  LearnFirst can return to this
                  curriculum after the prerequisite
                  learning gap has been addressed.
                </p>

              </section>
            )}


          <button
            type="button"
            className="primary-button"
            onClick={() => navigate("/learn/science")}
          >
            Continue Science
            <ArrowRight size={18} />
          </button>

        </>
      )}

    </div>
  );
}

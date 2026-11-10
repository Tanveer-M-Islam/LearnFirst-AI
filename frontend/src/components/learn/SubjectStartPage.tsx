import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  BookOpenCheck,
  BrainCircuit,
  ClipboardCheck,
  FlaskConical,
  Gauge,
  Lightbulb,
  PencilLine,
  RefreshCcw,
  ShieldCheck,
  Sparkles,
  Target,
} from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router";

import { getStudentCurriculumPath } from "../../api/curriculum";
import { getEnglishAdaptivePlan } from "../../api/englishAdaptive";
import { getScienceAdaptivePlan } from "../../api/scienceAdaptive";
import { createLearningSession } from "../../api/sessions";
import { getEnglishTopic, getEnglishTopicForAge } from "../../data/englishTopics";
import { getScienceTopic, getScienceTopicForAge } from "../../data/scienceTopics";
import type { StudentCurriculumPath } from "../../types/curriculum";
import type { EnglishAdaptivePlan } from "../../types/englishAdaptive";
import type { ScienceAdaptivePlan } from "../../types/scienceAdaptive";
import type { LearningMode } from "../../types/session";
import { getStoredStudent } from "../../utils/studentStorage";

type SupportedSubject = "SCIENCE" | "ENGLISH";
type SubjectPlan = ScienceAdaptivePlan | EnglishAdaptivePlan;
type SelectableMode = Extract<LearningMode, "LEARN" | "PRACTICE" | "HOMEWORK_HELP">;

const modeOptions = [
  {
    value: "LEARN" as const,
    title: "Learn",
    description: "Build understanding with a guided, age-appropriate tutor.",
    icon: Lightbulb,
  },
  {
    value: "PRACTICE" as const,
    title: "Practice",
    description: "Try a question from your personalized learning plan.",
    icon: BookOpenCheck,
  },
  {
    value: "HOMEWORK_HELP" as const,
    title: "Homework Help",
    description: "Bring your own question and receive step-by-step guidance.",
    icon: PencilLine,
  },
];

function readable(value: string): string {
  return value.replaceAll("_", " ").toLowerCase().replace(/\b\w/g, (c) => c.toUpperCase());
}

function describeActivity(value: string): string {
  switch (value) {
    case "START_LEARNING": return "Start learning";
    case "GUIDED_QUESTION": return "Try a guided question";
    case "INDEPENDENT_QUESTION": return "Try independently";
    case "REVIEW_CONCEPT": return "Review a prerequisite";
    case "CHALLENGE_QUESTION": return "Try a challenge";
    default: return readable(value);
  }
}

function errorText(error: unknown): string {
  return error instanceof Error ? error.message : "Something went wrong. Try again.";
}

interface Props {
  subject: SupportedSubject;
}

export default function SubjectStartPage({ subject }: Props) {
  const navigate = useNavigate();
  const student = getStoredStudent();
  const studentId = student?.id;
  const age = student?.age ?? 7;
  const isScience = subject === "SCIENCE";
  const subjectName = isScience ? "Science" : "English";
  const Icon = isScience ? FlaskConical : BookOpen;

  const fallbackTopic = isScience
    ? getScienceTopicForAge(age)
    : getEnglishTopicForAge(age);

  const [curriculum, setCurriculum] = useState<StudentCurriculumPath | null>(null);
  const [plan, setPlan] = useState<SubjectPlan | null>(null);
  const [curriculumLoading, setCurriculumLoading] = useState(true);
  const [planLoading, setPlanLoading] = useState(true);
  const [curriculumError, setCurriculumError] = useState<string | null>(null);
  const [planError, setPlanError] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [curriculumRefresh, setCurriculumRefresh] = useState(0);
  const [planRefresh, setPlanRefresh] = useState(0);
  const [mode, setMode] = useState<SelectableMode>("LEARN");
  const [homework, setHomework] = useState("");
  const [starting, setStarting] = useState(false);

  const conceptCode = curriculum?.recommended_concept?.concept_code
    ?? curriculum?.target_concept?.concept_code
    ?? fallbackTopic.conceptCode;
  const topic = isScience ? getScienceTopic(conceptCode) : getEnglishTopic(conceptCode);

  // Curriculum request. Ignore stale responses after unmount/refresh.
  useEffect(() => {
    if (!studentId) {
      navigate("/login", { replace: true });
      return;
    }
    let active = true;
    setCurriculumLoading(true);
    setCurriculumError(null);
    void getStudentCurriculumPath(studentId, subject)
      .then((data) => { if (active) setCurriculum(data); })
      .catch((err: unknown) => { if (active) setCurriculumError(errorText(err)); })
      .finally(() => { if (active) setCurriculumLoading(false); });
    return () => { active = false; };
  }, [studentId, subject, curriculumRefresh, navigate]);

  // Adaptive recommendation is independent of curriculum loading.
  useEffect(() => {
    if (!studentId) return;
    let active = true;
    setPlanLoading(true);
    setPlan(null);
    setPlanError(null);
    const request = isScience
      ? getScienceAdaptivePlan(studentId, conceptCode)
      : getEnglishAdaptivePlan(studentId, conceptCode);
    void request
      .then((data) => { if (active) setPlan(data); })
      .catch((err: unknown) => { if (active) setPlanError(errorText(err)); })
      .finally(() => { if (active) setPlanLoading(false); });
    return () => { active = false; };
  }, [studentId, conceptCode, isScience, planRefresh]);

  async function startSession(
    selectedMode: SelectableMode,
    problem: string | null,
  ): Promise<void> {
    if (!student || starting) return;
    setActionError(null);
    setStarting(true);
    try {
      const session = await createLearningSession({
        student_id: student.id,
        subject,
        mode: selectedMode,
        topic: topic.title,
        concept_code: conceptCode,
        current_problem: problem,
      });
      navigate(`/learn/${subject.toLowerCase()}/session/${session.id}`);
    } catch (err) {
      setActionError(errorText(err));
    } finally {
      setStarting(false);
    }
  }

  function startChosenMode(): void {
    if (mode === "HOMEWORK_HELP") {
      if (!homework.trim()) {
        setActionError("Enter your homework question before continuing.");
        return;
      }
      void startSession(mode, homework.trim());
      return;
    }
    if (mode === "PRACTICE") {
      const question = plan?.next_question?.prompt;
      if (!question) {
        setActionError("No practice question is available yet. Refresh the plan or choose Learn.");
        return;
      }
      void startSession(mode, question);
      return;
    }
    // In Learn mode the tutor introduces the concept before practice.
    void startSession("LEARN", null);
  }

  function startRecommendation(): void {
    if (!plan) return;
    const guidedLearning = plan.next_activity === "START_LEARNING"
      || plan.next_activity === "REVIEW_CONCEPT";
    const recommendedMode: SelectableMode = guidedLearning ? "LEARN" : "PRACTICE";
    const question = plan.next_question?.prompt ?? null;
    if (recommendedMode === "PRACTICE" && !question) {
      setActionError("The recommended question is unavailable. Refresh the personalized plan.");
      return;
    }
    // Preserve previous Science/English behavior: recommended sessions
    // start with the plan's question when one exists.
    void startSession(recommendedMode, question);
  }

  const question = plan?.next_question?.prompt;
  const status = curriculum?.recommended_concept?.status ?? "READY";
  const review = curriculum?.prerequisite_review_concept;
  const reviewNeeded = review && review.concept_code !== conceptCode;

  return (
    <div className="science-start-page lf-subject-start" data-subject={subject}>
      <button className="page-back-button" type="button" onClick={() => navigate("/dashboard") }>
        <ArrowLeft size={18} /> Dashboard
      </button>

      <header className="lf-learn-hero">
        <div className="lf-hero-icon"><Icon size={30} /></div>
        <div>
          <span className="lf-eyebrow"><Sparkles size={15} /> Age-adaptive {subjectName}</span>
          <h1>Your next {subjectName} step</h1>
          <p>LearnFirst selects a concept based on your age and learning evidence, then adapts questions and support to your progress.</p>
        </div>
      </header>

      <section className="lf-section" aria-labelledby="lf-curriculum-title">
        <div className="lf-section-heading">
          <div>
            <h2 id="lf-curriculum-title">Your curriculum position</h2>
            <p>Age determines the starting level. Demonstrated learning evidence can adjust your path.</p>
          </div>
          <button className="secondary-button lf-refresh" type="button" disabled={curriculumLoading}
            onClick={() => setCurriculumRefresh((n) => n + 1)}>
            <RefreshCcw size={16} /> Refresh
          </button>
        </div>

        <article className="surface-card lf-panel">
          <div className="lf-panel-heading">
            <div className="lf-panel-icon"><Target size={25} /></div>
            <div>
              <span className="lf-label">Current {subjectName} concept</span>
              <h3>{topic.title}</h3>
              <p>{topic.description}</p>
            </div>
          </div>
          <div className="lf-metrics">
            <div><Target size={18} /><span>Age</span><strong>{age}</strong></div>
            <div><Icon size={18} /><span>Expected level</span><strong>{curriculum?.target_concept?.title ?? topic.title}</strong></div>
            <div><BrainCircuit size={18} /><span>Current status</span><strong>{readable(status)}</strong></div>
          </div>
          <div className="lf-panel-footer">
            {reviewNeeded
              ? <>Recommended prerequisite: <strong>{review.title}</strong>. Review it before advancing.</>
              : `No demonstrated prerequisite gap is blocking your ${subjectName} level.`}
          </div>
        </article>
        {curriculumLoading && <p className="lf-status" role="status">Refreshing curriculum...</p>}
        {curriculumError && <p className="lf-error" role="alert">Curriculum could not refresh: {curriculumError}</p>}
      </section>

      <section className="lf-section" aria-labelledby="lf-plan-title">
        <div className="lf-section-heading">
          <div>
            <h2 id="lf-plan-title">Personalized {subjectName} plan</h2>
            <p>Difficulty and support respond to your progress independently of curriculum level.</p>
          </div>
          <button className="secondary-button lf-refresh" type="button" disabled={planLoading}
            onClick={() => setPlanRefresh((n) => n + 1)}>
            <RefreshCcw size={16} /> Refresh
          </button>
        </div>
        {planLoading && <div className="surface-card lf-loading" role="status"><BrainCircuit size={22} /> Checking your learning profile...</div>}
        {!planLoading && planError && <div className="surface-card lf-error" role="alert">Could not load the personalized plan: {planError}</div>}
        {!planLoading && plan && (
          <article className="surface-card lf-panel">
            <div className="lf-panel-heading">
              <div className="lf-panel-icon"><BrainCircuit size={25} /></div>
              <div>
                <span className="lf-label">Recommended activity</span>
                <h3>{describeActivity(plan.next_activity)}</h3>
                <p>{plan.mastery_explanation}</p>
              </div>
            </div>
            <div className="lf-metrics">
              <div><Gauge size={18} /><span>Difficulty</span><strong>{readable(plan.difficulty)}</strong></div>
              <div><Lightbulb size={18} /><span>Support</span><strong>{readable(plan.support_level)}</strong></div>
              <div><Sparkles size={18} /><span>{isScience ? "Understanding" : "Mastery"}</span>
                <strong>{isScience ? `${plan.understanding_score_percent}%` : readable(plan.mastery_state)}</strong></div>
            </div>
            {question && (
              <div className="lf-question-card">
                <span className="lf-label">{isScience ? "First question" : "Next learning question"}</span>
                <p>{question}</p>
              </div>
            )}
            <div className="lf-panel-footer lf-plan-footer">
              <p>{plan.summary}</p>
              <button type="button" className="primary-button" disabled={starting}
                onClick={startRecommendation}>
                {starting ? "Preparing..." : "Start recommended activity"}
                {!starting && <ArrowRight size={17} />}
              </button>
            </div>
          </article>
        )}
      </section>

      {isScience && (
        <div className="lf-grounding-note surface-card">
          <ShieldCheck size={23} />
          <div><strong>Curriculum-grounded Science</strong>
            <p>The Science tutor uses the available trusted curriculum materials to support explanations and hints.</p></div>
        </div>
      )}

      <div className="lf-divider"><span>Choose how you want to learn</span></div>

      <section className="lf-section" aria-labelledby="lf-mode-title">
        <div className="lf-number-heading">
          <span>1</span>
          <div><h2 id="lf-mode-title">Choose a learning mode</h2>
            <p>Your curriculum concept is selected for you. Choose how you want to work on it.</p></div>
        </div>
        <div className="lf-mode-grid">
          {modeOptions.map((option) => {
            const ModeIcon = option.icon;
            const selected = mode === option.value;
            return (
              <button key={option.value} type="button"
                className={`learning-mode-card ${selected ? "selected" : ""}`}
                aria-pressed={selected}
                onClick={() => { setMode(option.value); setActionError(null); }}>
                <div className="mode-icon"><ModeIcon size={22} /></div>
                <strong>{option.title}</strong>
                <p>{option.description}</p>
                <span className="mode-radio" aria-hidden="true">{selected ? "✓" : ""}</span>
              </button>
            );
          })}
        </div>
      </section>

      <section className="lf-section" aria-labelledby="lf-mode-action-title">
        <div className="lf-number-heading">
          <span>2</span>
          <div>
            <h2 id="lf-mode-action-title">
              {mode === "HOMEWORK_HELP" ? "Enter your question" : `${mode === "PRACTICE" ? "Practice" : "Learn"} ${topic.title}`}
            </h2>
            <p>Current curriculum concept: <strong>{topic.title}</strong></p>
          </div>
        </div>
        <div className="surface-card lf-action-card">
          {mode === "HOMEWORK_HELP" ? (
            <>
              <label htmlFor="lf-homework">Your {subjectName} question</label>
              <textarea id="lf-homework" value={homework} rows={4} maxLength={2000}
                onChange={(event) => setHomework(event.target.value)}
                placeholder={`Enter your ${subjectName} question here...`} />
              <p className="lf-helper">The tutor provides guided help. Custom questions may not receive automatic correctness scores.</p>
            </>
          ) : mode === "PRACTICE" ? (
            <>
              <span className="lf-label">Personalized practice</span>
              <div className="lf-action-question">
                {question ?? "No question is available yet. Refresh the personalized plan to get one."}
              </div>
              <p className="lf-helper">Try the question independently; the tutor can offer hints when needed.</p>
            </>
          ) : (
            <>
              <span className="lf-label">Current concept</span>
              <h3>{topic.title}</h3>
              <p>Start with an explanation and guiding questions before moving to independent practice.</p>
            </>
          )}
          {actionError && <p className="lf-error" role="alert">{actionError}</p>}
          <button className="primary-button lf-start-button" type="button"
            disabled={starting || (mode === "PRACTICE" && !question)}
            onClick={startChosenMode}>
            {starting ? "Preparing..." : mode === "HOMEWORK_HELP" ? "Start homework help" : mode === "PRACTICE" ? "Start practice" : "Start learning"}
            {!starting && <ArrowRight size={18} />}
          </button>
        </div>
      </section>

      <div className="lf-assessment-link surface-card">
        <ClipboardCheck size={24} />
        <div><strong>Check your starting level in {topic.title}</strong>
          <p>A short Diagnostic helps LearnFirst understand your current knowledge.</p></div>
        <button type="button" className="secondary-button"
          onClick={() => navigate(`/assessments/${subject.toLowerCase()}/diagnostic?concept=${encodeURIComponent(conceptCode)}`)}>
          Take Diagnostic <ArrowRight size={16} />
        </button>
      </div>
    </div>
  );
}

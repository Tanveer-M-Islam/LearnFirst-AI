
import {
  ArrowLeft,
  ArrowRight,
  BrainCircuit,
  CheckCircle2,
  CircleHelp,
  RotateCcw,
  Sparkles,
} from "lucide-react";

import {
  useEffect,
  useRef,
  useState,
} from "react";

import {
  useNavigate,
  useParams,
} from "react-router";

import {
  getLearningSession,
} from "../api/sessions";

import {
  sendTutorMessage,
} from "../api/tutor";

import {
  loadSessionChatHistory,
} from "../utils/chatHistory";

import ChatBubble from "../components/tutor/ChatBubble";
import MathFeedbackCard from "../components/tutor/MathFeedbackCard";
import TutorComposer from "../components/tutor/TutorComposer";

import type {
  LearningSession,
} from "../types/session";

import type {
  ChatMessage,
  TutorMessageResponse,
} from "../types/tutor";


function createId(): string {
  return crypto.randomUUID();
}


function modeLabel(
  mode: LearningSession["mode"],
): string {
  switch (mode) {
    case "HOMEWORK_HELP":
      return "Homework Help";
    case "PRACTICE":
      return "Practice";
    case "LEARN":
      return "Learn Mode";
    default:
      return "Learning";
  }
}


function supportLabel(level: number): string {
  if (level <= 0) return "Independent";
  if (level <= 2) return "Gentle guidance";
  if (level <= 4) return "Guided support";
  if (level <= 6) return "Strong support";
  return "Full teaching";
}


function initialTutorMessage(
  session: LearningSession,
): string {
  switch (session.mode) {
    case "PRACTICE":
      return (
        "Here is your practice problem: "
        + (session.current_problem ?? "your current challenge")
        + ". Try it independently first. "
        + "Show me your answer or your first step."
      );

    case "LEARN":
      return (
        "We'll learn "
        + (session.topic ?? "this concept")
        + " before focusing on solving. "
        + "Tell me one thing you already know about it. "
        + "You can also say \"I don't know yet.\""
      );

    default:
      return (
        "Let's work through your homework problem together. "
        + "Start by showing me what you would try first."
      );
  }
}


function problemLabel(
  session: LearningSession,
): string {
  if (
    session.mode === "LEARN"
    && !session.current_problem
  ) {
    return "Concept focus";
  }

  if (session.mode === "PRACTICE") {
    return "Practice problem";
  }

  return "Current problem";
}


function problemDisplay(
  session: LearningSession,
): string {
  return (
    session.current_problem
    ?? session.topic
    ?? "Math"
  );
}


export default function TutorPage() {

  const navigate = useNavigate();

  const { sessionId } = useParams<{
    sessionId: string;
  }>();

  const [session, setSession] =
    useState<LearningSession | null>(null);

  const [messages, setMessages] =
    useState<ChatMessage[]>([]);

  const [input, setInput] = useState("");

  const [loading, setLoading] = useState(false);

  const [pageLoading, setPageLoading] = useState(true);

  const [error, setError] =
    useState<string | null>(null);

  const endRef = useRef<HTMLDivElement | null>(null);


  // ==================================
  // Load session and chat history
  // ==================================

  useEffect(() => {
    let mounted = true;

    if (!sessionId) {
      setError("Learning session not found.");
      setPageLoading(false);
      return;
    }

    async function loadSession() {
      try {
        const data = await getLearningSession(sessionId!);

        const savedMessages =
          await loadSessionChatHistory(
            sessionId!,
            data.student_id,
          );

        if (!mounted) return;

        setSession(data);

        if (savedMessages.length > 0) {
          setMessages(savedMessages);
        } else {
          setMessages([
            {
              id: createId(),
              role: "tutor",
              text: initialTutorMessage(data),
              createdAt: Date.now(),
            },
          ]);
        }

      } catch (err) {
        if (mounted) {
          setError(
            err instanceof Error
              ? err.message
              : "Could not load the session."
          );
        }

      } finally {
        if (mounted) {
          setPageLoading(false);
        }
      }
    }

    void loadSession();

    return () => {
      mounted = false;
    };

  }, [sessionId]);


  // ==================================
  // Auto scroll
  // ==================================

  useEffect(() => {
    endRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);


  // ==================================
  // Refresh adaptive session state
  // ==================================

  async function refreshSession() {
    if (!sessionId) return;

    try {
      const updated =
        await getLearningSession(sessionId);

      setSession(updated);
    } catch {
      // Keep current state if refresh fails.
    }
  }


  // ==================================
  // Send tutor message
  // ==================================

  async function sendMessage(
    textOverride?: string,
  ) {
    if (!sessionId || loading) return;

    const text = (textOverride ?? input).trim();

    if (!text) return;

    const studentMessage: ChatMessage = {
      id: createId(),
      role: "student",
      text,
      createdAt: Date.now(),
    };

    setMessages((current) => [
      ...current,
      studentMessage,
    ]);

    setInput("");
    setLoading(true);
    setError(null);

    try {
      const response: TutorMessageResponse =
        await sendTutorMessage(sessionId, text);

      const tutorMessage: ChatMessage = {
        id: createId(),
        role: "tutor",
        text: response.reply,
        validation: response.math_validation,
        decision: response.decision,
        createdAt: Date.now(),
      };

      setMessages((current) => [
        ...current,
        tutorMessage,
      ]);

      await refreshSession();

    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "LearnFirst could not respond. Please try again."
      );

    } finally {
      setLoading(false);
    }
  }


  // ==================================
  // Loading and error
  // ==================================

  if (pageLoading) {
    return (
      <div className="tutor-page-loading">
        <div className="thinking-orb">
          <BrainCircuit size={32} />
        </div>
        <strong>
          Preparing your learning space...
        </strong>
      </div>
    );
  }

  if (error && !session) {
    return (
      <div className="tutor-load-error surface-card">
        <CircleHelp size={34} />
        <h2>We couldn't open this lesson.</h2>
        <p>{error}</p>

        <button
          type="button"
          className="primary-button"
          onClick={() => navigate("/learn/math")}
        >
          Start another lesson
        </button>
      </div>
    );
  }

  if (!session) return null;


  const latestTutorMessage = [...messages]
    .reverse()
    .find((message) => message.role === "tutor");

  const latestValidation =
    latestTutorMessage?.validation;


  return (
    <div className="tutor-page">

      {/* Header */}

      <header className="tutor-page-header">

        <div>
          <button
            type="button"
            className="page-back-button"
            onClick={() => navigate("/learn/math")}
          >
            <ArrowLeft size={18} />
            Math
          </button>

          <div className="tutor-title-row">
            <div className="tutor-title-icon">
              <BrainCircuit size={25} />
            </div>

            <div>
              <span>Math Tutor</span>
              <h1>{session.topic ?? "Math"}</h1>
            </div>
          </div>
        </div>

        <div className="session-status-pill">
          <span />
          {modeLabel(session.mode)}
        </div>

      </header>


      {/* Workspace */}

      <div className="tutor-workspace">

        <section className="tutor-main-card surface-card">

          <div className="current-problem-bar">

            <div>
              <span>{problemLabel(session)}</span>
              <strong>{problemDisplay(session)}</strong>
            </div>

            <div className="problem-mode">
              {modeLabel(session.mode)}
            </div>

          </div>


          {/* Chat */}

          <div className="chat-window">

            {messages.map((message) => (
              <div key={message.id}>

                <ChatBubble message={message} />

                {message.role === "tutor"
                  && message.validation
                  && (
                    <div className="feedback-wrap">
                      <MathFeedbackCard
                        validation={message.validation}
                      />
                    </div>
                  )}

              </div>
            ))}


            {/* Thinking indicator */}

            {loading && (
              <div className="chat-row chat-row-tutor">

                <div className="chat-avatar tutor-avatar">
                  <BrainCircuit size={18} />
                </div>

                <div className="thinking-bubble">
                  <div className="thinking-dots">
                    <span />
                    <span />
                    <span />
                  </div>

                  <p>
                    LearnFirst is thinking about
                    your learning...
                  </p>
                </div>

              </div>
            )}

            <div ref={endRef} />

          </div>


          {/* Error */}

          {error && (
            <div className="chat-error">
              {error}
            </div>
          )}


          {/* Composer */}

          <TutorComposer
            value={input}
            disabled={loading}
            mode={session.mode}
            onChange={setInput}
            onSubmit={() => void sendMessage()}
            onQuickMessage={(message) =>
              void sendMessage(message)
            }
          />

        </section>


        {/* Side panel */}

        <aside className="tutor-side-panel">

          {/* Current challenge */}

          <div className="surface-card tutor-info-card">

            <span className="side-card-label">
              {session.mode === "LEARN"
                && !session.current_problem
                ? "Learning concept"
                : session.mode === "PRACTICE"
                  ? "Practice challenge"
                  : "Your challenge"}
            </span>

            <div className="side-problem">
              {problemDisplay(session)}
            </div>

            <button
              type="button"
              className="restart-button"
              onClick={() => navigate("/learn/math")}
            >
              <RotateCcw size={16} />

              {session.mode === "LEARN"
                ? "Choose learning mode"
                : session.mode === "PRACTICE"
                  ? "Choose another activity"
                  : "New problem"}
            </button>

          </div>


          {/* Adaptive support */}

          <div className="surface-card tutor-info-card">

            <span className="side-card-label">
              Learning support
            </span>

            <div className="support-status">
              <div className="support-icon">
                <Sparkles size={20} />
              </div>

              <div>
                <strong>
                  {supportLabel(session.current_hint_level)}
                </strong>

                <p>
                  LearnFirst gives only as much
                  help as you need.
                </p>
              </div>
            </div>

            <div className="support-meter">
              {Array.from({ length: 7 }).map((_, index) => (
                <span
                  key={index}
                  className={
                    index < Math.max(
                      session.current_hint_level,
                      1,
                    )
                      ? "active"
                      : ""
                  }
                />
              ))}
            </div>

          </div>


          {/* Lesson statistics */}

          <div className="surface-card tutor-info-card session-progress-card">

            <span className="side-card-label">
              This lesson
            </span>

            <div className="lesson-stat">
              <CheckCircle2 size={18} />
              <div>
                <strong>{session.attempt_count}</strong>
                <span>Attempts</span>
              </div>
            </div>

            <div className="lesson-stat">
              <CircleHelp size={18} />
              <div>
                <strong>
                  {session.direct_answer_requests}
                </strong>
                <span>Answer requests</span>
              </div>
            </div>

          </div>

        </aside>

      </div>


      {/* Mastery assessment CTA */}

      {latestValidation?.status === "CORRECT"
        && session.mode !== "PRACTICE"
        && (

          <div className="mastery-cta">

            <div>
              <Sparkles size={20} />

              <div>
                <strong>Nice work!</strong>
                <span>
                  Ready to check whether you can
                  solve fresh problems independently?
                </span>
              </div>
            </div>

            <button
              type="button"
              className="primary-button"
              onClick={() =>
                navigate(
                  `/assessments/math/mastery?sessionId=${session.id}`
                )
              }
            >
              Take mastery check
              <ArrowRight size={18} />
            </button>

          </div>

        )}

    </div>
  );
}

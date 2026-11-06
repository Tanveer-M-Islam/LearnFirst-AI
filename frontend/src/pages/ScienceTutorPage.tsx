
import {
  ArrowLeft,
  BrainCircuit,
  CheckCircle2,
  CircleHelp,
  FlaskConical,
  Lightbulb,
  Send,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import {
  type FormEvent,
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

import type {
  LearningSession,
} from "../types/session";

import type {
  ChatMessage,
  ScienceValidation,
} from "../types/tutor";


function createId(): string {
  return crypto.randomUUID();
}


function scienceStatusLabel(
  validation: ScienceValidation,
): string {
  switch (validation.status) {
    case "CORRECT":
      return "Strong explanation";
    case "PARTIALLY_CORRECT":
      return "Partly there";
    case "INCORRECT":
      return "Needs another look";
    default:
      return "Explain a little more";
  }
}


function initialScienceMessage(
  session: LearningSession,
): string {
  if (session.current_problem) {
    return (
      "Here is your Science question: "
      + session.current_problem
      + ". Explain what you understand "
      + "in your own words."
    );
  }

  return (
    "Let's explore "
    + (session.topic ?? "Science")
    + ". Tell me one thing you already know about it."
  );
}


export default function ScienceTutorPage() {

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
  // Restore session and conversation
  // ==================================

  useEffect(() => {
    let mounted = true;

    if (!sessionId) {
      setError("Science session not found.");
      setPageLoading(false);
      return;
    }

    async function loadSession() {
      try {
        const data =
          await getLearningSession(sessionId!);

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
              text: initialScienceMessage(data),
              createdAt: Date.now(),
            },
          ]);
        }

      } catch (err) {
        if (mounted) {
          setError(
            err instanceof Error
              ? err.message
              : "Could not load the Science session."
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
  // Scroll to newest message
  // ==================================

  useEffect(() => {
    endRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);


  // ==================================
  // Refresh learning state
  // ==================================

  async function refreshSession() {
    if (!sessionId) return;

    try {
      const updated =
        await getLearningSession(sessionId);

      setSession(updated);
    } catch {
      // Keep the existing state.
    }
  }


  // ==================================
  // Tutor conversation
  // ==================================

  async function sendMessage(
    override?: string,
  ) {
    if (!sessionId || loading) return;

    const message = (override ?? input).trim();

    if (!message) return;

    const studentMessage: ChatMessage = {
      id: createId(),
      role: "student",
      text: message,
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
      const response =
        await sendTutorMessage(sessionId, message);

      const tutorMessage: ChatMessage = {
        id: createId(),
        role: "tutor",
        text: response.reply,
        decision: response.decision,
        scienceValidation:
          response.science_validation,
        ragUsed: response.rag_used,
        ragSources: response.rag_sources,
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
          : "LearnFirst could not respond."
      );

    } finally {
      setLoading(false);
    }
  }


  function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();
    void sendMessage();
  }


  // ==================================
  // Loading and error states
  // ==================================

  if (pageLoading) {
    return (
      <div className="science-page-loading">
        <BrainCircuit size={33} />
        <strong>
          Preparing your Science lesson...
        </strong>
      </div>
    );
  }

  if (!session || !sessionId) {
    return (
      <div className="science-error surface-card">
        <p>
          {error ?? "Science session not found."}
        </p>

        <button
          type="button"
          className="primary-button"
          onClick={() => navigate("/learn/science")}
        >
          Choose another topic
        </button>
      </div>
    );
  }


  return (
    <div className="science-tutor-page">

      {/* Header */}

      <header className="science-tutor-header">

        <div>
          <button
            type="button"
            className="page-back-button"
            onClick={() => navigate("/learn/science")}
          >
            <ArrowLeft size={18} />
            Science
          </button>

          <div className="science-tutor-title">

            <div>
              <FlaskConical size={26} />
            </div>

            <section>
              <span>Science Tutor</span>
              <h1>{session.topic ?? "Science"}</h1>
            </section>

          </div>
        </div>

        <div className="grounded-badge">
          <ShieldCheck size={17} />
          Curriculum grounded
        </div>

      </header>


      {/* Workspace */}

      <div className="science-workspace">

        <section className="science-chat-card surface-card">

          <div className="science-chat-intro">
            <Sparkles size={18} />

            <div>
              <strong>
                Explore, think, explain
              </strong>

              <span>
                Explain ideas in your own words.
                LearnFirst checks conceptual understanding.
              </span>
            </div>
          </div>


          {/* Saved and live messages */}

          <div className="science-chat-window">

            {messages.map((message) => (
              <div key={message.id}>

                <ChatBubble message={message} />


                {/* Science understanding feedback */}

                {message.role === "tutor"
                  && message.scienceValidation
                  && (

                    <div className="rag-grounding-note">

                      <BrainCircuit size={15} />

                      <div>
                        <strong>
                          {scienceStatusLabel(
                            message.scienceValidation
                          )}
                        </strong>

                        <span>
                          {
                            message.scienceValidation
                              .feedback_summary
                          }
                        </span>

                        {message.scienceValidation
                          .matched_ideas.length > 0 && (
                            <span>
                              Recognized ideas:{" "}
                              {message.scienceValidation
                                .matched_ideas.join(", ")}
                            </span>
                          )}

                      </div>

                    </div>

                  )}


                {/* RAG grounding citations */}

                {message.role === "tutor"
                  && message.ragUsed
                  && (

                    <div className="rag-grounding-note">

                      <ShieldCheck size={15} />

                      <div>
                        <strong>
                          Grounded in curriculum
                        </strong>

                        {message.ragSources?.map((source) => (
                          <span key={source.source_id}>
                            {source.title}
                          </span>
                        ))}
                      </div>

                    </div>

                  )}

              </div>
            ))}


            {/* Thinking indicator */}

            {loading && (
              <div className="science-thinking">

                <BrainCircuit size={18} />

                <div>
                  <strong>
                    Thinking about your response...
                  </strong>

                  <span>
                    LearnFirst is checking your
                    understanding and evidence.
                  </span>
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


          {/* Quick actions */}

          <div className="science-quick-actions">

            <button
              type="button"
              disabled={loading}
              onClick={() =>
                void sendMessage("Explain this simply.")
              }
            >
              <FlaskConical size={16} />
              Explain
            </button>

            <button
              type="button"
              disabled={loading}
              onClick={() =>
                void sendMessage("Can you give me a hint?")
              }
            >
              <Lightbulb size={16} />
              Hint
            </button>

            <button
              type="button"
              disabled={loading}
              onClick={() =>
                void sendMessage("Give me a practice question.")
              }
            >
              <Sparkles size={16} />
              Practice
            </button>

          </div>


          {/* Composer */}

          <form
            className="science-composer"
            onSubmit={handleSubmit}
          >

            <textarea
              value={input}
              disabled={loading}
              rows={2}
              maxLength={4000}
              placeholder={
                session.current_problem
                  ? "Explain your answer in your own words..."
                  : "Ask about the topic or explain what you know..."
              }
              onChange={(event) =>
                setInput(event.target.value)
              }
            />

            <button
              type="submit"
              disabled={loading || !input.trim()}
              aria-label="Send Science message"
            >
              <Send size={19} />
            </button>

          </form>

        </section>


        {/* Side panel */}

        <aside className="science-side-panel">

          <div className="surface-card science-side-card">

            <span className="small-label">
              {session.current_problem
                ? "Current question"
                : "Current topic"}
            </span>

            <h3>
              {session.current_problem
                ?? session.topic
                ?? "Science"}
            </h3>

            <p>
              {session.current_problem
                ? "Explain what you understand in your own words."
                : "Learn the concept and ask for practice when you are ready."}
            </p>

          </div>


          {/* Curriculum grounding */}

          <div className="surface-card science-side-card grounded-side-card">

            <ShieldCheck size={24} />

            <span className="small-label">
              Trusted learning
            </span>

            <h3>Grounded feedback</h3>

            <p>
              Science factual teaching uses trusted
              curriculum context rather than
              unsupported claims.
            </p>

          </div>


          {/* Lesson progress */}

          <div className="surface-card science-side-card session-progress-card">

            <span className="small-label">
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

    </div>
  );
}

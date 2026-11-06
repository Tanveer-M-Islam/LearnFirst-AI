
import {
  ArrowLeft,
  BookOpen,
  BrainCircuit,
  CheckCircle2,
  CircleHelp,
  Lightbulb,
  Send,
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
  EnglishValidation,
} from "../types/tutor";


function createId(): string {
  return crypto.randomUUID();
}


function englishStatusLabel(
  validation: EnglishValidation,
): string {
  switch (validation.status) {
    case "CORRECT":
      return "Correct";
    case "PARTIALLY_CORRECT":
      return "Almost there";
    case "INCORRECT":
      return "Needs another try";
    default:
      return "Needs clarification";
  }
}


function initialEnglishMessage(
  session: LearningSession,
): string {
  if (session.current_problem) {
    return (
      "Here is your English task: "
      + session.current_problem
      + ". Try it yourself first. "
      + "I will guide you if needed."
    );
  }

  return (
    "Let's work on "
    + (session.topic ?? "English")
    + ". Tell me what you already understand."
  );
}


export default function EnglishTutorPage() {

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
  // Load session and saved history
  // ==================================

  useEffect(() => {
    let mounted = true;

    if (!sessionId) {
      setError("English session not found.");
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
              text: initialEnglishMessage(data),
              createdAt: Date.now(),
            },
          ]);
        }

      } catch (err) {
        if (mounted) {
          setError(
            err instanceof Error
              ? err.message
              : "Could not load the English session."
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
  // Auto-scroll to latest message
  // ==================================

  useEffect(() => {
    endRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);


  // ==================================
  // Refresh session
  // ==================================

  async function refreshSession() {
    if (!sessionId) return;

    try {
      const updated =
        await getLearningSession(sessionId);

      setSession(updated);
    } catch {
      // Optional refresh.
    }
  }


  // ==================================
  // Send message
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
        englishValidation:
          response.english_validation,
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
        <BrainCircuit size={32} />
        <strong>
          Preparing English...
        </strong>
      </div>
    );
  }

  if (!session || !sessionId) {
    return (
      <div className="science-error surface-card">
        <p>
          {error ?? "English session not found."}
        </p>

        <button
          type="button"
          className="primary-button"
          onClick={() => navigate("/learn/english")}
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
            onClick={() => navigate("/learn/english")}
          >
            <ArrowLeft size={18} />
            English
          </button>

          <div className="science-tutor-title">

            <div>
              <BookOpen size={26} />
            </div>

            <section>
              <span>English Tutor</span>
              <h1>{session.topic ?? "English"}</h1>
            </section>

          </div>
        </div>

      </header>


      {/* Workspace */}

      <div className="science-workspace">

        <section className="science-chat-card surface-card">

          <div className="science-chat-intro">

            <Sparkles size={18} />

            <div>
              <strong>
                Think, write, improve
              </strong>

              <span>
                LearnFirst checks your response
                using controlled English evaluation rules.
              </span>
            </div>

          </div>


          {/* Saved and live messages */}

          <div className="science-chat-window">

            {messages.map((message) => (
              <div key={message.id}>

                <ChatBubble message={message} />


                {/* English validation feedback */}

                {message.role === "tutor"
                  && message.englishValidation
                  && (

                    <div className="rag-grounding-note">

                      <BrainCircuit size={15} />

                      <div>

                        <strong>
                          {englishStatusLabel(
                            message.englishValidation
                          )}
                        </strong>

                        <span>
                          {
                            message.englishValidation
                              .feedback_summary
                          }
                        </span>

                        {message.englishValidation
                          .rule_feedback.length > 0
                          && (
                            <span>
                              {
                                message.englishValidation
                                  .rule_feedback[0]
                              }
                            </span>
                          )}

                        <span>
                          Score:{" "}
                          {
                            message.englishValidation
                              .score_percent
                          }
                          %
                        </span>

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
                    Checking your response...
                  </strong>

                  <span>
                    LearnFirst is checking meaning,
                    grammar, or sentence rules for
                    this task.
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
              <BookOpen size={16} />
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
              rows={2}
              disabled={loading}
              maxLength={4000}
              placeholder={
                session.current_problem
                  ? "Write your answer..."
                  : "Ask an English question..."
              }
              onChange={(event) =>
                setInput(event.target.value)
              }
            />

            <button
              type="submit"
              disabled={loading || !input.trim()}
              aria-label="Send English message"
            >
              <Send size={19} />
            </button>

          </form>

        </section>


        {/* Side panel */}

        <aside className="science-side-panel">

          {/* Current task */}

          <div className="surface-card science-side-card">

            <span className="small-label">
              Current task
            </span>

            <h3>
              {session.current_problem
                ?? session.topic
                ?? "English"}
            </h3>

            <p>
              Try independently first.
              LearnFirst increases support only
              when your learning evidence
              shows you need it.
            </p>

          </div>


          {/* Evaluation information */}

          <div className="surface-card science-side-card">

            <BrainCircuit size={24} />

            <span className="small-label">
              Structured evaluation
            </span>

            <h3>
              Controlled checking
            </h3>

            <p>
              Vocabulary, grammar, sentence, and
              reading tasks are evaluated with
              the English question bank and
              structured rules before tutoring
              feedback is produced.
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
                <strong>
                  {session.attempt_count}
                </strong>
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

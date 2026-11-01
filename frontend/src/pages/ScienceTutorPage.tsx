import {
  ArrowLeft,
  BookOpenCheck,
  BrainCircuit,
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

import ChatBubble from "../components/tutor/ChatBubble";

import type {
  LearningSession,
} from "../types/session";

import type {
  ChatMessage,
} from "../types/tutor";


function createId(): string {
  if (
    typeof crypto
    !== "undefined"
    && crypto.randomUUID
  ) {
    return crypto.randomUUID();
  }

  return (
    `${Date.now()}-`
    + `${Math.random()}`
  );
}


export default function ScienceTutorPage() {
  const navigate =
    useNavigate();

  const {
    sessionId,
  } = useParams<{
    sessionId: string;
  }>();

  const [
    session,
    setSession,
  ] = useState<
    LearningSession | null
  >(null);

  const [
    messages,
    setMessages,
  ] = useState<
    ChatMessage[]
  >([]);

  const [
    input,
    setInput,
  ] = useState("");

  const [
    loading,
    setLoading,
  ] = useState(false);

  const [
    pageLoading,
    setPageLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState<
    string | null
  >(null);

  const endRef =
    useRef<HTMLDivElement | null>(
      null,
    );


  useEffect(() => {
    if (!sessionId) {
      setError(
        "Science session "
        + "not found.",
      );

      setPageLoading(false);

      return;
    }

    const loadSession =
      async () => {
        try {
          const data =
            await getLearningSession(
              sessionId,
            );

          setSession(data);

          setMessages([
            {
              id:
                createId(),

              role:
                "tutor",

              text:
                (
                  "Let's explore "
                  + (
                    data.topic
                    ?? "this topic"
                  )
                  + ". Tell me one "
                  + "thing you already "
                  + "know about it."
                ),

              createdAt:
                Date.now(),
            },
          ]);
        } catch (err) {
          setError(
            err instanceof Error
              ? err.message
              : (
                "Could not load "
                + "the Science "
                + "session."
              ),
          );
        } finally {
          setPageLoading(false);
        }
      };

    void loadSession();
  }, [sessionId]);


  useEffect(() => {
    endRef.current
      ?.scrollIntoView({
        behavior: "smooth",
      });
  }, [
    messages,
    loading,
  ]);


  const sendMessage =
    async (
      messageOverride?: string,
    ) => {
      if (
        !sessionId
        || loading
      ) {
        return;
      }

      const message = (
        messageOverride
        ?? input
      ).trim();

      if (!message) {
        return;
      }

      setMessages(
        (current) => [
          ...current,

          {
            id:
              createId(),

            role:
              "student",

            text:
              message,

            createdAt:
              Date.now(),
          },
        ],
      );

      setInput("");
      setLoading(true);
      setError(null);

      try {
        const response =
          await sendTutorMessage(
            sessionId,
            message,
          );

        setMessages(
          (current) => [
            ...current,

            {
              id:
                createId(),

              role:
                "tutor",

              text:
                response.reply,

              decision:
                response
                  .decision,

              ragUsed:
                response
                  .rag_used,

              ragSources:
                response
                  .rag_sources,

              createdAt:
                Date.now(),
            },
          ],
        );
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : (
              "LearnFirst could "
              + "not respond."
            ),
        );
      } finally {
        setLoading(false);
      }
    };


  const handleSubmit = (
    event:
      FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    void sendMessage();
  };


  if (pageLoading) {
    return (
      <div className="science-page-loading">
        <BrainCircuit
          size={33}
        />

        <strong>
          Preparing your
          Science lesson...
        </strong>
      </div>
    );
  }


  if (
    !session
    || !sessionId
  ) {
    return (
      <div className="science-error surface-card">
        <p>
          {error
            ?? (
              "Science session "
              + "not found."
            )}
        </p>

        <button
          type="button"
          className="primary-button"
          onClick={() =>
            navigate(
              "/learn/science",
            )
          }
        >
          Choose another topic
        </button>
      </div>
    );
  }


  return (
    <div className="science-tutor-page">
      <header className="science-tutor-header">
        <div>
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

            Science topics
          </button>

          <div className="science-tutor-title">
            <div>
              <FlaskConical
                size={26}
              />
            </div>

            <section>
              <span>
                Science Tutor
              </span>

              <h1>
                {
                  session.topic
                }
              </h1>
            </section>
          </div>
        </div>

        <div className="grounded-badge">
          <ShieldCheck
            size={17}
          />

          Curriculum grounded
        </div>
      </header>

      <div className="science-workspace">
        <section className="science-chat-card surface-card">
          <div className="science-chat-intro">
            <Sparkles
              size={18}
            />

            <div>
              <strong>
                Explore, think,
                explain
              </strong>

              <span>
                You don't need to
                know the answer
                immediately.
              </span>
            </div>
          </div>

          <div className="science-chat-window">
            {messages.map(
              (message) => (
                <div
                  key={
                    message.id
                  }
                >
                  <ChatBubble
                    message={
                      message
                    }
                  />

                  {message.role
                    === "tutor"
                    && message
                      .ragUsed
                    && (
                    <div className="rag-grounding-note">
                      <ShieldCheck
                        size={15}
                      />

                      <div>
                        <strong>
                          Grounded in
                          curriculum
                        </strong>

                        {message
                          .ragSources
                          ?.map(
                            (
                              source,
                            ) => (
                              <span
                                key={
                                  source
                                    .source_id
                                }
                              >
                                {
                                  source
                                    .title
                                }
                              </span>
                            ),
                          )}
                      </div>
                    </div>
                  )}
                </div>
              ),
            )}

            {loading && (
              <div className="science-thinking">
                <div className="science-thinking-icon">
                  <BrainCircuit
                    size={18}
                  />
                </div>

                <div>
                  <strong>
                    LearnFirst is
                    checking the
                    curriculum...
                  </strong>

                  <span>
                    Then it will
                    guide your
                    next step.
                  </span>
                </div>
              </div>
            )}

            <div
              ref={endRef}
            />
          </div>

          {error && (
            <div className="chat-error">
              {error}
            </div>
          )}

          <div className="science-quick-actions">
            <button
              type="button"
              disabled={loading}
              onClick={() =>
                void sendMessage(
                  (
                    "Explain this "
                    + "concept simply."
                  ),
                )
              }
            >
              <BookOpenCheck
                size={16}
              />

              Explain simply
            </button>

            <button
              type="button"
              disabled={loading}
              onClick={() =>
                void sendMessage(
                  (
                    "Can you give "
                    + "me a hint?"
                  ),
                )
              }
            >
              <Lightbulb
                size={16}
              />

              Give me a hint
            </button>

            <button
              type="button"
              disabled={loading}
              onClick={() =>
                void sendMessage(
                  (
                    "Ask me a "
                    + "practice "
                    + "question."
                  ),
                )
              }
            >
              <Sparkles
                size={16}
              />

              Quiz me
            </button>
          </div>

          <form
            className="science-composer"
            onSubmit={
              handleSubmit
            }
          >
            <textarea
              value={input}
              disabled={loading}
              rows={2}
              maxLength={4000}
              placeholder={
                "Ask about the topic "
                + "or explain what "
                + "you think..."
              }
              onChange={(event) =>
                setInput(
                  event
                    .target
                    .value,
                )
              }
            />

            <button
              type="submit"
              disabled={
                loading
                || !input.trim()
              }
              aria-label={
                "Send Science message"
              }
            >
              <Send
                size={19}
              />
            </button>
          </form>
        </section>

        <aside className="science-side-panel">
          <div className="surface-card science-side-card">
            <span className="small-label">
              Current topic
            </span>

            <h3>
              {
                session.topic
              }
            </h3>

            <p>
              Ask questions,
              explain ideas and
              test your
              understanding.
            </p>
          </div>

          <div className="surface-card science-side-card grounded-side-card">
            <ShieldCheck
              size={24}
            />

            <span className="small-label">
              Trusted learning
            </span>

            <h3>
              Grounded answers
            </h3>

            <p>
              Science facts are
              retrieved from the
              LearnFirst curriculum
              knowledge base before
              the tutor responds.
            </p>
          </div>

          <div className="surface-card science-side-card">
            <Lightbulb
              size={24}
            />

            <span className="small-label">
              Think first
            </span>

            <h3>
              Your ideas matter
            </h3>

            <p>
              Try explaining what
              you think. LearnFirst
              can guide you from
              there.
            </p>
          </div>
        </aside>
      </div>
    </div>
  );
}
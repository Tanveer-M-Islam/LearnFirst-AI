import {
  ArrowLeft,
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
  if (
    typeof crypto
    !== "undefined"
    && crypto.randomUUID
  ) {
    return (
      crypto.randomUUID()
    );
  }

  return (
    `${Date.now()}-`
    + `${Math.random()}`
  );
}


function modeLabel(
  mode:
    LearningSession["mode"],
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


function supportLabel(
  hintLevel: number,
): string {
  if (hintLevel <= 0) {
    return "Independent";
  }

  if (hintLevel <= 2) {
    return "Gentle guidance";
  }

  if (hintLevel <= 4) {
    return "Guided support";
  }

  if (hintLevel <= 6) {
    return "Strong support";
  }

  return "Full teaching";
}


export default function TutorPage() {
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
        "Learning session "
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
                  "Let's work through "
                  + "this together. "
                  + "Start by showing "
                  + "me what you would "
                  + "try first."
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
                + "the session."
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


  const refreshSession =
    async () => {
      if (!sessionId) {
        return;
      }

      try {
        const updated =
          await getLearningSession(
            sessionId,
          );

        setSession(
          updated,
        );
      } catch {
        // Chat response is still valid.
        // Do not break the conversation
        // if the optional refresh fails.
      }
    };


  const sendMessage =
    async (
      textOverride?: string,
    ) => {
      if (
        !sessionId
        || loading
      ) {
        return;
      }

      const text = (
        textOverride
        ?? input
      ).trim();

      if (!text) {
        return;
      }

      const studentMessage:
        ChatMessage = {
          id:
            createId(),

          role:
            "student",

          text,

          createdAt:
            Date.now(),
        };

      setMessages(
        (current) => [
          ...current,
          studentMessage,
        ],
      );

      setInput("");
      setLoading(true);
      setError(null);

      try {
        const response:
          TutorMessageResponse =
            await sendTutorMessage(
              sessionId,
              text,
            );

        const tutorMessage:
          ChatMessage = {
            id:
              createId(),

            role:
              "tutor",

            text:
              response.reply,

            validation:
              response
                .math_validation,

            decision:
              response
                .decision,

            createdAt:
              Date.now(),
          };

        setMessages(
          (current) => [
            ...current,
            tutorMessage,
          ],
        );

        await refreshSession();
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : (
              "LearnFirst could "
              + "not respond. "
              + "Please try again."
            ),
        );
      } finally {
        setLoading(false);
      }
    };


  if (pageLoading) {
    return (
      <div className="tutor-page-loading">
        <div className="thinking-orb">
          <BrainCircuit
            size={32}
          />
        </div>

        <strong>
          Preparing your
          learning space...
        </strong>
      </div>
    );
  }


  if (
    error
    && !session
  ) {
    return (
      <div className="tutor-load-error surface-card">
        <CircleHelp
          size={34}
        />

        <h2>
          We couldn't open
          this lesson.
        </h2>

        <p>
          {error}
        </p>

        <button
          type="button"
          className="primary-button"
          onClick={() =>
            navigate(
              "/learn/math",
            )
          }
        >
          Start another lesson
        </button>
      </div>
    );
  }


  if (!session) {
    return null;
  }


  const latestTutorMessage = [
    ...messages,
  ]
    .reverse()
    .find(
      (message) =>
        message.role
        === "tutor",
    );

  const latestValidation =
    latestTutorMessage
      ?.validation;


  return (
    <div className="tutor-page">
      <header className="tutor-page-header">
        <div>
          <button
            type="button"
            className="page-back-button"
            onClick={() =>
              navigate(
                "/dashboard",
              )
            }
          >
            <ArrowLeft
              size={18}
            />

            Dashboard
          </button>

          <div className="tutor-title-row">
            <div className="tutor-title-icon">
              <BrainCircuit
                size={25}
              />
            </div>

            <div>
              <span>
                Math Tutor
              </span>

              <h1>
                {
                  session.topic
                  ?? "Math"
                }
              </h1>
            </div>
          </div>
        </div>

        <div className="session-status-pill">
          <span />
          Learning
        </div>
      </header>

      <div className="tutor-workspace">
        <section className="tutor-main-card surface-card">
          <div className="current-problem-bar">
            <div>
              <span>
                Current problem
              </span>

              <strong>
                {
                  session
                    .current_problem
                  ?? (
                    "No problem "
                    + "selected"
                  )
                }
              </strong>
            </div>

            <div className="problem-mode">
              {
                modeLabel(
                  session.mode,
                )
              }
            </div>
          </div>

          <div className="chat-window">
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

                  {(
                    message.role
                    === "tutor"
                    && message
                      .validation
                  ) && (
                    <div className="feedback-wrap">
                      <MathFeedbackCard
                        validation={
                          message
                            .validation
                        }
                      />
                    </div>
                  )}
                </div>
              ),
            )}

            {loading && (
              <div className="chat-row chat-row-tutor">
                <div className="chat-avatar tutor-avatar">
                  <BrainCircuit
                    size={18}
                  />
                </div>

                <div className="thinking-bubble">
                  <div className="thinking-dots">
                    <span />
                    <span />
                    <span />
                  </div>

                  <p>
                    LearnFirst is
                    thinking about
                    your attempt...
                  </p>
                </div>
              </div>
            )}

            <div ref={endRef} />
          </div>

          {error && (
            <div className="chat-error">
              {error}
            </div>
          )}

          <TutorComposer
            value={input}
            disabled={loading}
            onChange={setInput}
            onSubmit={() =>
              void sendMessage()
            }
            onQuickMessage={
              (message) =>
                void sendMessage(
                  message,
                )
            }
          />
        </section>

        <aside className="tutor-side-panel">
          <div className="surface-card tutor-info-card">
            <span className="side-card-label">
              Your challenge
            </span>

            <div className="side-problem">
              {
                session
                  .current_problem
              }
            </div>

            <button
              type="button"
              className="restart-button"
              onClick={() =>
                navigate(
                  "/learn/math",
                )
              }
            >
              <RotateCcw
                size={16}
              />

              New problem
            </button>
          </div>

          <div className="surface-card tutor-info-card">
            <span className="side-card-label">
              Learning support
            </span>

            <div className="support-status">
              <div className="support-icon">
                <Sparkles
                  size={20}
                />
              </div>

              <div>
                <strong>
                  {
                    supportLabel(
                      session
                        .current_hint_level,
                    )
                  }
                </strong>

                <p>
                  LearnFirst gives
                  only as much help
                  as you need.
                </p>
              </div>
            </div>

            <div className="support-meter">
              {Array.from({
                length: 7,
              }).map(
                (_, index) => (
                  <span
                    key={index}
                    className={
                      index
                      < Math.max(
                        session
                          .current_hint_level,
                        1,
                      )
                        ? "active"
                        : ""
                    }
                  />
                ),
              )}
            </div>
          </div>

          <div className="surface-card tutor-info-card session-progress-card">
            <span className="side-card-label">
              This lesson
            </span>

            <div className="lesson-stat">
              <CheckCircle2
                size={18}
              />

              <div>
                <strong>
                  {
                    session
                      .attempt_count
                  }
                </strong>

                <span>
                  Attempts
                </span>
              </div>
            </div>

            <div className="lesson-stat">
              <CircleHelp
                size={18}
              />

              <div>
                <strong>
                  {
                    session
                      .direct_answer_requests
                  }
                </strong>

                <span>
                  Answer requests
                </span>
              </div>
            </div>
          </div>
        </aside>
      </div>

      {latestValidation
        ?.status
        === "CORRECT" && (
        <div className="correct-celebration">
          <Sparkles
            size={20}
          />

          You solved this step
          correctly. Keep going!
        </div>
      )}
    </div>
  );
}
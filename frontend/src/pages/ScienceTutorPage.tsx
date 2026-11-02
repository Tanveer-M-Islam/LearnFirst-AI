import {
  ArrowLeft,
  BookOpenCheck,
  BrainCircuit,
  CheckCircle2,
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
  ScienceValidation,
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


function scienceStatusLabel(
  validation: ScienceValidation,
): string {

  switch (
    validation.status
  ) {

    case "CORRECT":

      return (
        "Strong explanation"
      );


    case "PARTIALLY_CORRECT":

      return (
        "Partly there"
      );


    case "INCORRECT":

      return (
        "Needs another look"
      );


    default:

      return (
        "Explain a little more"
      );
  }
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
  ] = useState(
    false,
  );


  const [
    pageLoading,
    setPageLoading,
  ] = useState(
    true,
  );


  const [
    error,
    setError,
  ] = useState<
    string | null
  >(null);


  const endRef =
    useRef<
      HTMLDivElement | null
    >(
      null,
    );


  useEffect(
    () => {

      if (
        !sessionId
      ) {

        setError(
          "Science session "
          + "not found.",
        );


        setPageLoading(
          false,
        );


        return;
      }


      const loadSession =
        async () => {

          try {

            const data =
              await getLearningSession(
                sessionId,
              );


            setSession(
              data,
            );


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
                    + "know about it. "
                    + "When you're ready, "
                    + "you can ask me to "
                    + "quiz you."
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

            setPageLoading(
              false,
            );
          }
        };


      void loadSession();

    },
    [
      sessionId,
    ],
  );


  useEffect(
    () => {

      endRef.current
        ?.scrollIntoView({
          behavior:
            "smooth",
        });

    },
    [
      messages,
      loading,
    ],
  );


  const refreshSession =
    async () => {

      if (
        !sessionId
      ) {

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

        // Optional UI refresh.
      }
    };


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


      if (
        !message
      ) {

        return;
      }


      setMessages(
        (
          current,
        ) => [

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

      setLoading(
        true,
      );

      setError(
        null,
      );


      try {

        const response =
          await sendTutorMessage(
            sessionId,
            message,
          );


        setMessages(
          (
            current,
          ) => [

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

              scienceValidation:
                response
                  .science_validation,

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


        await refreshSession();


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

        setLoading(
          false,
        );
      }
    };


  const handleSubmit = (
    event:
      FormEvent<HTMLFormElement>,
  ) => {

    event.preventDefault();


    void sendMessage();
  };


  if (
    pageLoading
  ) {

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

          {
            error
            ?? (
              "Science session "
              + "not found."
            )
          }

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
                LearnFirst now checks
                your conceptual
                understanding too.
              </span>

            </div>

          </div>


          <div className="science-chat-window">

            {messages.map(
              (
                message,
              ) => (

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


                  {/* =====================
                      Science evaluation
                  ====================== */}

                  {(
                    message.role
                    === "tutor"

                    && message
                      .scienceValidation
                  ) && (

                    <div className="rag-grounding-note">

                      <BrainCircuit
                        size={15}
                      />


                      <div>

                        <strong>

                          {
                            scienceStatusLabel(
                              message
                                .scienceValidation,
                            )
                          }

                        </strong>


                        <span>

                          {
                            message
                              .scienceValidation
                              .feedback_summary
                          }

                        </span>


                        {message
                          .scienceValidation
                          .matched_ideas
                          .length
                          > 0
                          && (

                          <span>

                            Recognized ideas:
                            {" "}

                            {
                              message
                                .scienceValidation
                                .matched_ideas
                                .join(
                                  ", ",
                                )
                            }

                          </span>
                        )}

                      </div>

                    </div>
                  )}


                  {/* =====================
                      Curriculum sources
                  ====================== */}

                  {(
                    message.role
                    === "tutor"

                    && message
                      .ragUsed
                  ) && (

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
                                  source.title
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
                    checking your
                    explanation...
                  </strong>


                  <span>
                    It will compare
                    your ideas with
                    the trusted
                    concept material.
                  </span>

                </div>

              </div>
            )}


            <div
              ref={
                endRef
              }
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

              disabled={
                loading
              }

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

              disabled={
                loading
              }

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

              disabled={
                loading
              }

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
              value={
                input
              }

              disabled={
                loading
              }

              rows={2}

              maxLength={4000}

              placeholder={
                session
                  .current_problem

                  ? (
                    "Explain your answer "
                    + "in your own words..."
                  )

                  : (
                    "Ask about the topic "
                    + "or explain what "
                    + "you think..."
                  )
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

              {
                session
                  .current_problem
                  ? "Current question"
                  : "Current topic"
              }

            </span>


            <h3>

              {
                session
                  .current_problem
                ?? session.topic
              }

            </h3>


            <p>

              {
                session
                  .current_problem

                  ? (
                    "Explain what you "
                    + "understand in your "
                    + "own words."
                  )

                  : (
                    "Ask questions, "
                    + "learn the concept "
                    + "and quiz yourself "
                    + "when you're ready."
                  )
              }

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
              Grounded feedback
            </h3>


            <p>
              Science teaching is
              retrieved from the
              selected curriculum
              concept before the
              tutor responds.
            </p>

          </div>


          <div className="surface-card science-side-card">

            <CheckCircle2
              size={24}
            />


            <span className="small-label">
              Understanding check
            </span>


            <h3>
              More than keywords
            </h3>


            <p>
              LearnFirst checks
              several expected ideas,
              records partial
              understanding and can
              detect selected common
              misconceptions.
            </p>

          </div>

        </aside>

      </div>

    </div>
  );
}
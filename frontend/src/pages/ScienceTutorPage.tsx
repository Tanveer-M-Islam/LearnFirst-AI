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

    return crypto.randomUUID();
  }


  return (
    `${Date.now()}-${Math.random()}`
  );
}


function scienceStatusLabel(
  validation:
    ScienceValidation,
): string {

  switch (
    validation.status
  ) {

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
    >(null);


  useEffect(
    () => {

      if (
        !sessionId
      ) {

        setError(
          "Science session not found.",
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
                  data.current_problem

                    ? (
                      "Here is your Science "
                      + "question: "
                      + data.current_problem
                      + ". Explain what you "
                      + "understand in your "
                      + "own words."
                    )

                    : (
                      "Let's explore "
                      + (
                        data.topic
                        ?? "Science"
                      )
                      + ". Tell me one thing "
                      + "you already know about it."
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
                  "Could not load the "
                  + "Science session."
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

        // Optional UI refresh only.
      }
    };


  const sendMessage =
    async (
      override?: string,
    ) => {

      if (
        !sessionId
        || loading
      ) {

        return;
      }


      const message =
        (
          override
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
                response.decision,

              scienceValidation:
                response
                  .science_validation,

              ragUsed:
                response.rag_used,

              ragSources:
                response.rag_sources,

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
              "LearnFirst could not "
              + "respond."
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
          Preparing your Science lesson...
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
            ?? "Science session not found."
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

            Science

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
                  ?? "Science"
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
                Explore, think, explain
              </strong>


              <span>
                Explain ideas in your own
                words. LearnFirst checks
                conceptual understanding.
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
                          Grounded in curriculum
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

                <BrainCircuit
                  size={18}
                />


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
                  "Explain this simply.",
                )
              }
            >

              <FlaskConical
                size={16}
              />

              Explain

            </button>


            <button
              type="button"

              disabled={
                loading
              }

              onClick={() =>
                void sendMessage(
                  "Can you give me a hint?",
                )
              }
            >

              <Lightbulb
                size={16}
              />

              Hint

            </button>


            <button
              type="button"

              disabled={
                loading
              }

              onClick={() =>
                void sendMessage(
                  "Give me a practice question.",
                )
              }
            >

              <Sparkles
                size={16}
              />

              Practice

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
                    + "or explain what you know..."
                  )
              }

              onChange={(event) =>
                setInput(
                  event.target.value,
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
                session.current_problem
                ?? session.topic
                ?? "Science"
              }
            </h3>


            <p>
              {
                session.current_problem

                  ? (
                    "Explain what you "
                    + "understand in your "
                    + "own words."
                  )

                  : (
                    "Learn the concept and "
                    + "ask for practice when "
                    + "you are ready."
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
              Science factual teaching uses
              trusted curriculum context rather
              than unsupported claims.
            </p>

          </div>


          <div className="surface-card science-side-card session-progress-card">

            <span className="small-label">
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

    </div>
  );
}
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

import ChatBubble from "../components/tutor/ChatBubble";

import type {
  LearningSession,
} from "../types/session";

import type {
  ChatMessage,
  EnglishValidation,
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


function englishStatusLabel(
  validation:
    EnglishValidation,
): string {

  switch (
    validation.status
  ) {

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


export default function EnglishTutorPage() {

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
          "English session not found.",
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
                      "Here is your English "
                      + "task: "
                      + data.current_problem
                      + ". Try it yourself first. "
                      + "I will guide you if needed."
                    )

                    : (
                      "Let's work on "
                      + (
                        data.topic
                        ?? "English"
                      )
                      + ". Tell me what you "
                      + "already understand."
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
                  + "English session."
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

              englishValidation:
                response
                  .english_validation,

              decision:
                response.decision,

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
          size={32}
        />

        <strong>
          Preparing English...
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
            ?? "English session not found."
          }
        </p>


        <button
          type="button"
          className="primary-button"

          onClick={() =>
            navigate(
              "/learn/english",
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
                "/learn/english",
              )
            }
          >

            <ArrowLeft
              size={18}
            />

            English

          </button>


          <div className="science-tutor-title">

            <div>

              <BookOpen
                size={26}
              />

            </div>


            <section>

              <span>
                English Tutor
              </span>


              <h1>
                {
                  session.topic
                  ?? "English"
                }
              </h1>

            </section>

          </div>

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
                Think, write, improve
              </strong>


              <span>
                LearnFirst checks your
                response using controlled
                English evaluation rules.
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
                      .englishValidation
                  ) && (

                    <div className="rag-grounding-note">

                      <BrainCircuit
                        size={15}
                      />


                      <div>

                        <strong>
                          {
                            englishStatusLabel(
                              message
                                .englishValidation,
                            )
                          }
                        </strong>


                        <span>
                          {
                            message
                              .englishValidation
                              .feedback_summary
                          }
                        </span>


                        {message
                          .englishValidation
                          .rule_feedback
                          .length
                          > 0
                          && (

                          <span>
                            {
                              message
                                .englishValidation
                                .rule_feedback[0]
                            }
                          </span>

                        )}


                        <span>

                          Score:
                          {" "}

                          {
                            message
                              .englishValidation
                              .score_percent
                          }

                          %

                        </span>

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
                    Checking your response...
                  </strong>


                  <span>
                    LearnFirst is checking
                    meaning, grammar, or
                    sentence rules for this task.
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

              <BookOpen
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

              rows={2}

              disabled={
                loading
              }

              maxLength={4000}

              placeholder={
                session
                  .current_problem

                  ? "Write your answer..."

                  : "Ask an English question..."
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
                "Send English message"
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
              Current task
            </span>


            <h3>
              {
                session.current_problem
                ?? session.topic
                ?? "English"
              }
            </h3>


            <p>
              Try independently first.
              LearnFirst increases support
              only when your learning
              evidence shows you need it.
            </p>

          </div>


          <div className="surface-card science-side-card">

            <BrainCircuit
              size={24}
            />


            <span className="small-label">
              Structured evaluation
            </span>


            <h3>
              Controlled checking
            </h3>


            <p>
              Vocabulary, grammar, sentence,
              and reading tasks are evaluated
              with the English question bank
              and structured rules before
              tutoring feedback is produced.
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
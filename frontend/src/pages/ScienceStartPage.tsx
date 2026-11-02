import {
  ArrowLeft,
  ArrowRight,
  Atom,
  BrainCircuit,
  FlaskConical,
  Gauge,
  Leaf,
  Network,
  RefreshCcw,
  Sparkles,
} from "lucide-react";

import {
  useEffect,
  useState,
} from "react";

import {
  useNavigate,
} from "react-router";

import {
  getScienceTopics,
} from "../api/curriculum";

import {
  getScienceAdaptivePlan,
} from "../api/scienceAdaptive";

import {
  createLearningSession,
} from "../api/sessions";

import {
  ApiError,
} from "../api/client";

import type {
  CurriculumTopic,
} from "../types/curriculum";

import type {
  ScienceAdaptiveActivity,
  ScienceAdaptivePlan,
} from "../types/scienceAdaptive";

import {
  clearStoredStudent,
  getStoredStudent,
} from "../utils/studentStorage";


function topicIcon(
  conceptCode: string,
) {

  if (
    conceptCode.includes(
      "PHOTO",
    )
  ) {

    return Leaf;
  }


  if (
    conceptCode.includes(
      "FOODCHAIN",
    )
  ) {

    return Network;
  }


  return Atom;
}


function topicDescription(
  conceptCode: string,
): string {

  if (
    conceptCode
    === "SCI_BIO_PHOTO_01"
  ) {

    return (
      "Discover how plants use "
      + "light, water and carbon "
      + "dioxide to make food."
    );
  }


  if (
    conceptCode
    === "SCI_PHY_MATTER_01"
  ) {

    return (
      "Explore solids, liquids, "
      + "gases and how matter "
      + "changes state."
    );
  }


  if (
    conceptCode
    === "SCI_BIO_FOODCHAIN_01"
  ) {

    return (
      "Learn how energy moves "
      + "between plants and "
      + "animals."
    );
  }


  return (
    "Explore this Science concept "
    + "with guided questions."
  );
}


function activityLabel(
  activity:
    ScienceAdaptiveActivity,
): string {

  switch (
    activity
  ) {

    case "START_LEARNING":

      return "Start learning";


    case "GUIDED_QUESTION":

      return "Guided question";


    case "INDEPENDENT_QUESTION":

      return "Independent question";


    case "REVIEW_CONCEPT":

      return "Review the concept";


    case "CHALLENGE_QUESTION":

      return "Challenge question";
  }
}


export default function ScienceStartPage() {

  const navigate =
    useNavigate();


  const [
    topics,
    setTopics,
  ] = useState<
    CurriculumTopic[]
  >([]);


  const [
    selected,
    setSelected,
  ] = useState<
    CurriculumTopic | null
  >(null);


  const [
    adaptivePlan,
    setAdaptivePlan,
  ] = useState<
    ScienceAdaptivePlan | null
  >(null);


  const [
    loading,
    setLoading,
  ] = useState(
    true,
  );


  const [
    adaptiveLoading,
    setAdaptiveLoading,
  ] = useState(
    false,
  );


  const [
    starting,
    setStarting,
  ] = useState(
    false,
  );


  const [
    error,
    setError,
  ] = useState<
    string | null
  >(null);


  // ======================================
  // Load curriculum topics
  // ======================================

  const loadTopics =
    async () => {

      setLoading(
        true,
      );


      setError(
        null,
      );


      try {

        const data =
          await getScienceTopics();


        setTopics(
          data,
        );


        if (
          data.length
          > 0
        ) {

          setSelected(
            (
              current,
            ) => {

              if (
                current
              ) {

                const stillExists =
                  data.find(
                    (
                      topic,
                    ) =>
                      topic
                        .concept_code
                      === current
                        .concept_code,
                  );


                if (
                  stillExists
                ) {

                  return stillExists;
                }
              }


              return (
                data[0]
              );
            },
          );
        }


      } catch (err) {

        setError(
          err instanceof Error
            ? err.message
            : (
              "Could not load "
              + "Science topics."
            ),
        );


      } finally {

        setLoading(
          false,
        );
      }
    };


  useEffect(
    () => {

      void loadTopics();

    },
    [],
  );


  // ======================================
  // Adaptive plan
  //
  // IMPORTANT:
  // Failure here NEVER blocks
  // Start Science.
  // ======================================

  useEffect(
    () => {

      if (
        !selected
      ) {

        setAdaptivePlan(
          null,
        );

        return;
      }


      const student =
        getStoredStudent();


      if (
        !student
      ) {

        setAdaptivePlan(
          null,
        );

        return;
      }


      let cancelled =
        false;


      const loadAdaptivePlan =
        async () => {

          setAdaptiveLoading(
            true,
          );


          try {

            const plan =
              await getScienceAdaptivePlan(
                student.id,
                selected
                  .concept_code,
              );


            if (
              !cancelled
            ) {

              setAdaptivePlan(
                plan,
              );
            }


          } catch {

            /*
            Adaptive Science is helpful,
            but it must NEVER stop a
            Science lesson from starting.
            */

            if (
              !cancelled
            ) {

              setAdaptivePlan(
                null,
              );
            }


          } finally {

            if (
              !cancelled
            ) {

              setAdaptiveLoading(
                false,
              );
            }
          }
        };


      void loadAdaptivePlan();


      return () => {

        cancelled = true;
      };

    },
    [
      selected
        ?.concept_code,
    ],
  );


  // ======================================
  // Start Science
  // ======================================

  const startLearning =
    async () => {

      if (
        starting
      ) {

        return;
      }


      setError(
        null,
      );


      // ----------------------------------
      // Read student again at click time.
      //
      // This prevents a stale render from
      // using an old localStorage value.
      // ----------------------------------

      const student =
        getStoredStudent();


      if (
        !student
      ) {

        navigate(
          "/setup",
        );

        return;
      }


      if (
        !student.id
      ) {

        clearStoredStudent();


        navigate(
          "/setup",
        );

        return;
      }


      if (
        !selected
      ) {

        setError(
          "Choose a Science "
          + "topic first.",
        );

        return;
      }


      setStarting(
        true,
      );


      try {

        /*
        IMPORTANT:
        Starting a Science session does
        NOT depend on the adaptive API.

        The adaptive engine is applied
        later by TutorService.
        */

        const session =
          await createLearningSession({

            student_id:
              student.id,

            mode:
              "LEARN",

            subject:
              "SCIENCE",

            topic:
              selected.title,

            concept_code:
              selected
                .concept_code,

            current_problem:
              null,
          });


        if (
          !session
          || !session.id
        ) {

          throw new Error(
            "The Science session "
            + "was created without "
            + "a valid session ID.",
          );
        }


        navigate(
          (
            "/learn/science/"
            + "session/"
            + session.id
          ),
        );


      } catch (err) {

        console.error(
          "Start Science failed:",
          err,
        );


        /*
        A very common development issue:
        SQLite/database gets reset but the
        browser still contains an old
        student ID in localStorage.
        */

        if (
          err instanceof ApiError

          && err.status
          === 404

          && err.message
            .toLowerCase()
            .includes(
              "student",
            )
        ) {

          clearStoredStudent();


          setError(
            "Your saved learner "
            + "profile is no longer "
            + "available in the "
            + "current database. "
            + "Please create the "
            + "learner profile again.",
          );


          return;
        }


        setError(
          err instanceof Error
            ? err.message
            : (
              "Could not start "
              + "Science learning."
            ),
        );


      } finally {

        setStarting(
          false,
        );
      }
    };


  // ======================================
  // UI
  // ======================================

  return (

    <div className="science-start-page">

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


      {/* =============================
          Hero
      ============================== */}

      <section className="science-start-hero">

        <div className="science-start-icon">

          <FlaskConical
            size={31}
          />

        </div>


        <div>

          <div className="science-eyebrow">

            <Sparkles
              size={15}
            />

            Science learning

          </div>


          <h1>
            What are you
            curious about?
          </h1>


          <p>
            Choose a topic and
            LearnFirst will adapt
            questions, explanations
            and support to your
            learning.
          </p>

        </div>

      </section>


      {/* =============================
          Topic heading
      ============================== */}

      <div className="science-section-heading">

        <div>

          <h2>
            Choose a topic
          </h2>


          <p>
            Each Science topic
            develops its own
            learning profile.
          </p>

        </div>

      </div>


      {/* =============================
          Loading
      ============================== */}

      {loading && (

        <div className="science-loading surface-card">

          <RefreshCcw
            size={25}
          />

          Loading Science
          topics...

        </div>

      )}


      {/* =============================
          Topic load error
      ============================== */}

      {(
        !loading

        && error

        && topics.length
        === 0
      ) && (

        <div className="science-error surface-card">

          <p>
            {error}
          </p>


          <button
            type="button"
            className="secondary-button"

            onClick={() =>
              void loadTopics()
            }
          >

            <RefreshCcw
              size={17}
            />

            Try again

          </button>

        </div>

      )}


      {/* =============================
          Topics
      ============================== */}

      {(
        !loading

        && topics.length
        > 0
      ) && (

        <div className="science-topic-grid">

          {topics.map(
            (
              topic,
            ) => {

              const Icon =
                topicIcon(
                  topic
                    .concept_code,
                );


              const isSelected =
                selected
                  ?.concept_code
                === topic
                  .concept_code;


              return (

                <button
                  key={
                    topic
                      .concept_code
                  }

                  type="button"

                  className={
                    isSelected
                      ? (
                        "science-topic-card "
                        + "selected"
                      )
                      : (
                        "science-topic-card"
                      )
                  }

                  disabled={
                    starting
                  }

                  onClick={() => {

                    setSelected(
                      topic,
                    );


                    setError(
                      null,
                    );
                  }}
                >

                  <div className="science-topic-icon">

                    <Icon
                      size={27}
                    />

                  </div>


                  <span className="science-topic-grade">

                    Grade
                    {" "}
                    {
                      topic
                        .grade_band
                    }

                  </span>


                  <h3>
                    {
                      topic.title
                    }
                  </h3>


                  <p>

                    {
                      topicDescription(
                        topic
                          .concept_code,
                      )
                    }

                  </p>


                  <div className="science-topic-select">

                    {
                      isSelected
                        ? "Selected ✓"
                        : "Choose topic"
                    }

                  </div>

                </button>
              );
            },
          )}

        </div>

      )}


      {/* =============================
          Adaptive status
      ============================== */}

      {(
        selected

        && adaptiveLoading
      ) && (

        <div className="science-start-actions">

          <div>

            <strong>
              Checking your
              learning profile...
            </strong>


            <span>
              This does not block
              the lesson from
              starting.
            </span>

          </div>


          <BrainCircuit
            size={24}
          />

        </div>

      )}


      {(
        selected

        && !adaptiveLoading

        && adaptivePlan
      ) && (

        <div className="science-start-actions">

          <div>

            <strong>

              Personalized next step:
              {" "}

              {
                activityLabel(
                  adaptivePlan
                    .next_activity,
                )
              }

            </strong>


            <span>

              Difficulty:
              {" "}
              {
                adaptivePlan
                  .difficulty
              }

              {" · "}

              Support:
              {" "}
              {
                adaptivePlan
                  .support_level
              }

            </span>


            <span>

              Understanding:
              {" "}
              {
                adaptivePlan
                  .understanding_score_percent
              }
              %

            </span>

          </div>


          <Gauge
            size={25}
          />

        </div>

      )}


      {/* =============================
          Visible start error

          Keep this immediately above
          the button so it cannot be
          missed.
      ============================== */}

      {(
        error

        && topics.length
        > 0
      ) && (

        <div
          className="science-error surface-card"
          style={{
            marginTop:
              "20px",
          }}
        >

          <strong>
            Could not start Science
          </strong>


          <p>
            {error}
          </p>


          {error.includes(
            "learner profile",
          ) && (

            <button
              type="button"
              className="secondary-button"

              onClick={() =>
                navigate(
                  "/setup",
                )
              }
            >
              Create learner profile

              <ArrowRight
                size={17}
              />
            </button>

          )}

        </div>

      )}


      {/* =============================
          START SCIENCE

          This button depends ONLY on:
          - topics loaded
          - a topic selected
          - no active start request

          It does NOT depend on the
          adaptive plan.
      ============================== */}

      {(
        !loading

        && topics.length
        > 0
      ) && (

        <div className="science-start-actions">

          <div>

            <strong>
              Ready to explore?
            </strong>


            <span>

              {
                selected
                  ? (
                    "Start "
                    + selected.title
                    + " with guided "
                    + "Science learning."
                  )
                  : (
                    "Choose a Science "
                    + "topic first."
                  )
              }

            </span>

          </div>


          <button
            type="button"
            className="primary-button"

            disabled={
              selected === null
              || starting
            }

            onClick={
              startLearning
            }
          >

            {
              starting
                ? (
                  <>
                    <RefreshCcw
                      size={18}
                    />

                    Preparing lesson...
                  </>
                )
                : (
                  <>
                    Start Science

                    <ArrowRight
                      size={18}
                    />
                  </>
                )
            }

          </button>

        </div>

      )}

    </div>
  );
}
import {
  ArrowLeft,
  ArrowRight,
  Atom,
  FlaskConical,
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
  createLearningSession,
} from "../api/sessions";

import type {
  CurriculumTopic,
} from "../types/curriculum";

import {
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


export default function ScienceStartPage() {
  const navigate =
    useNavigate();

  const student =
    getStoredStudent();

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
    loading,
    setLoading,
  ] = useState(true);

  const [
    starting,
    setStarting,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState<
    string | null
  >(null);


  const loadTopics =
    async () => {
      setLoading(true);
      setError(null);

      try {
        const data =
          await getScienceTopics();

        setTopics(data);

        if (
          data.length > 0
        ) {
          setSelected(
            data[0],
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
        setLoading(false);
      }
    };


  useEffect(() => {
    void loadTopics();
  }, []);


  const startLearning =
    async () => {
      if (!student) {
        navigate(
          "/setup",
        );

        return;
      }

      if (!selected) {
        setError(
          "Choose a topic first.",
        );

        return;
      }

      setStarting(true);
      setError(null);

      try {
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

        navigate(
          (
            "/learn/science/"
            + "session/"
            + session.id
          ),
        );
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : (
              "Could not start "
              + "Science learning."
            ),
        );
      } finally {
        setStarting(false);
      }
    };


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
            explore it with
            questions, examples
            and trusted curriculum
            material.
          </p>
        </div>
      </section>

      <div className="science-section-heading">
        <div>
          <h2>
            Choose a topic
          </h2>

          <p>
            LearnFirst will use
            verified learning
            material for the
            topic you choose.
          </p>
        </div>
      </div>

      {loading && (
        <div className="science-loading surface-card">
          <RefreshCcw
            size={25}
          />

          Loading Science
          topics...
        </div>
      )}

      {!loading
        && error
        && topics.length === 0
        && (
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

      {!loading && (
        <div className="science-topic-grid">
          {topics.map(
            (topic) => {
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
                  onClick={() =>
                    setSelected(
                      topic,
                    )
                  }
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
                    {isSelected
                      ? "Selected ✓"
                      : "Choose topic"}
                  </div>
                </button>
              );
            },
          )}
        </div>
      )}

      {error
        && topics.length > 0
        && (
        <div className="error-message">
          {error}
        </div>
      )}

      {!loading
        && topics.length > 0
        && (
        <div className="science-start-actions">
          <div>
            <strong>
              Ready to explore?
            </strong>

            <span>
              LearnFirst will begin
              by checking what you
              already know.
            </span>
          </div>

          <button
            type="button"
            className="primary-button"
            disabled={
              !selected
              || starting
            }
            onClick={() =>
              void startLearning()
            }
          >
            {starting
              ? (
                "Preparing lesson..."
              )
              : (
                <>
                  Start Science

                  <ArrowRight
                    size={18}
                  />
                </>
              )}
          </button>
        </div>
      )}
    </div>
  );
}
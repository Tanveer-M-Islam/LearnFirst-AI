import {
  ArrowLeft,
  ArrowRight,
  GraduationCap,
  Sparkles,
} from "lucide-react";

import {
  type FormEvent,
  useState,
} from "react";

import {
  useNavigate,
} from "react-router";

import {
  createStudent,
} from "../api/students";

import {
  saveStudent,
} from "../utils/studentStorage";


const ageOptions = [
  7, 8, 9, 10,
  11, 12, 13, 14,
];


const gradeOptions = [
  "1",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9",
  "10",
];


export default function StudentSetupPage() {
  const navigate =
    useNavigate();

  const [name, setName] =
    useState("");

  const [age, setAge] =
    useState(11);

  const [grade, setGrade] =
    useState("6");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(
      null,
    );


  const handleSubmit =
    async (
      event:
        FormEvent<HTMLFormElement>,
    ) => {
      event.preventDefault();

      const trimmedName =
        name.trim();

      if (!trimmedName) {
        setError(
          "Please tell us your name.",
        );

        return;
      }

      setLoading(true);
      setError(null);

      try {
        const student =
          await createStudent({
            display_name:
              trimmedName,
            age,
            grade,
            preferred_language:
              "en",
            curriculum_profile:
              "bangladesh_english_v1",
          });

        saveStudent(
          student,
        );

        navigate(
          "/dashboard",
        );
      } catch (err) {
        const message =
          err instanceof Error
            ? err.message
            : (
              "Could not create "
              + "your learning profile."
            );

        setError(message);
      } finally {
        setLoading(false);
      }
    };


  return (
    <div className="setup-page">
      <div className="setup-background-shape setup-shape-one" />
      <div className="setup-background-shape setup-shape-two" />

      <div className="setup-card">
        <button
          type="button"
          className="back-link"
          onClick={() =>
            navigate("/")
          }
        >
          <ArrowLeft
            size={18}
          />

          Back
        </button>

        <div className="setup-brand">
          <div className="brand-mark">
            <GraduationCap
              size={23}
            />
          </div>

          <div>
            <div className="brand-name">
              LearnFirst AI
            </div>
          </div>
        </div>

        <div className="setup-heading">
          <div className="setup-icon">
            <Sparkles
              size={24}
            />
          </div>

          <h1>
            Let's set up your
            learning space
          </h1>

          <p>
            A few details help
            LearnFirst explain
            things at the right
            level for you.
          </p>
        </div>

        <form
          className="setup-form"
          onSubmit={
            handleSubmit
          }
        >
          <div>
            <label
              className="field-label"
              htmlFor="name"
            >
              What should we
              call you?
            </label>

            <input
              id="name"
              className="text-input"
              placeholder="Your name"
              value={name}
              maxLength={100}
              onChange={(event) =>
                setName(
                  event.target.value,
                )
              }
            />
          </div>

          <div>
            <div className="field-label">
              How old are you?
            </div>

            <div className="age-grid">
              {ageOptions.map(
                (item) => (
                  <button
                    key={item}
                    type="button"
                    className={
                      age === item
                        ? (
                          "age-button "
                          + "selected"
                        )
                        : "age-button"
                    }
                    onClick={() =>
                      setAge(item)
                    }
                  >
                    {item}
                  </button>
                ),
              )}
            </div>
          </div>

          <div>
            <label
              className="field-label"
              htmlFor="grade"
            >
              Which class are
              you in?
            </label>

            <select
              id="grade"
              className="select-input"
              value={grade}
              onChange={(event) =>
                setGrade(
                  event.target.value,
                )
              }
            >
              {gradeOptions.map(
                (item) => (
                  <option
                    key={item}
                    value={item}
                  >
                    Class {item}
                  </option>
                ),
              )}
            </select>
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <button
            type="submit"
            className="primary-button setup-submit"
            disabled={loading}
          >
            {loading
              ? (
                "Creating your "
                + "learning space..."
              )
              : (
                <>
                  Continue

                  <ArrowRight
                    size={19}
                  />
                </>
              )}
          </button>
        </form>

        <p className="setup-privacy">
          LearnFirst only uses
          these details to adapt
          the learning experience.
        </p>
      </div>
    </div>
  );
}
import {
  ArrowLeft,
  ArrowRight,
  Eye,
  EyeOff,
  GraduationCap,
  LockKeyhole,
  LogIn,
  UserRound,
} from "lucide-react";

import {
  type FormEvent,
  useState,
} from "react";

import {
  useNavigate,
} from "react-router";

import {
  loginStudent,
} from "../api/students";

import {
  saveStudent,
} from "../utils/studentStorage";


export default function StudentLoginPage() {

  const navigate =
    useNavigate();


  const [
    username,
    setUsername,
  ] = useState(
    "",
  );


  const [
    password,
    setPassword,
  ] = useState(
    "",
  );


  const [
    showPassword,
    setShowPassword,
  ] = useState(
    false,
  );


  const [
    loading,
    setLoading,
  ] = useState(
    false,
  );


  const [
    error,
    setError,
  ] = useState<
    string | null
  >(null);


  const submit =
    async (
      event:
        FormEvent<HTMLFormElement>,
    ) => {

      event.preventDefault();


      const normalizedUsername =
        username
          .trim()
          .toLowerCase();


      if (
        !normalizedUsername
      ) {

        setError(
          "Enter your username."
        );

        return;
      }


      if (
        password.length < 8
      ) {

        setError(
          "Enter your password."
        );

        return;
      }


      setLoading(
        true
      );


      setError(
        null
      );


      try {

        const student =
          await loginStudent({

            username:
              normalizedUsername,

            password,
          });


        saveStudent(
          student
        );


        navigate(
          "/dashboard",

          {
            replace:
              true,
          },
        );


      } catch (err) {

        setError(
          err instanceof Error
            ? err.message
            : (
              "Unable to log in."
            ),
        );


      } finally {

        setLoading(
          false
        );
      }
    };


  return (

    <div className="auth-page">

      <div className="auth-panel">

        <button
          type="button"
          className="auth-back"

          onClick={() =>
            navigate(
              "/"
            )
          }
        >

          <ArrowLeft
            size={17}
          />

          Back

        </button>


        <div className="auth-brand">

          <div className="brand-mark">

            <GraduationCap
              size={22}
            />

          </div>


          <div>

            <strong>
              LearnFirst
            </strong>


            <span>
              Continue your learning
            </span>

          </div>

        </div>


        <div className="auth-heading">

          <div className="auth-heading-icon">

            <LogIn
              size={23}
            />

          </div>


          <h1>
            Welcome back
          </h1>


          <p>
            Sign in to continue
            your existing learning
            progress.
          </p>

        </div>


        <form
          className="auth-form"

          onSubmit={
            submit
          }
        >

          <div>

            <label
              className="field-label"
              htmlFor="username"
            >

              <UserRound
                size={15}
              />

              Username

            </label>


            <input
              id="username"

              className="text-input"

              autoComplete="username"

              placeholder="Enter your username"

              value={
                username
              }

              onChange={(event) =>
                setUsername(
                  event
                    .target
                    .value
                )
              }
            />

          </div>


          <div>

            <label
              className="field-label"
              htmlFor="password"
            >

              <LockKeyhole
                size={15}
              />

              Password

            </label>


            <div className="password-field">

              <input
                id="password"

                className="text-input"

                type={
                  showPassword
                    ? "text"
                    : "password"
                }

                autoComplete="current-password"

                placeholder="Enter your password"

                value={
                  password
                }

                onChange={(event) =>
                  setPassword(
                    event
                      .target
                      .value
                  )
                }
              />


              <button
                type="button"

                className="password-toggle"

                aria-label={
                  showPassword
                    ? "Hide password"
                    : "Show password"
                }

                onClick={() =>
                  setShowPassword(
                    (
                      current,
                    ) =>
                      !current
                  )
                }
              >

                {
                  showPassword
                    ? (
                      <EyeOff
                        size={18}
                      />
                    )
                    : (
                      <Eye
                        size={18}
                      />
                    )
                }

              </button>

            </div>

          </div>


          {error && (

            <div className="error-message">
              {error}
            </div>

          )}


          <button
            type="submit"

            className="primary-button auth-submit"

            disabled={
              loading
            }
          >

            {
              loading
                ? "Signing in..."
                : (
                  <>
                    Sign in

                    <ArrowRight
                      size={18}
                    />
                  </>
                )
            }

          </button>

        </form>


        <div className="auth-divider">

          <span>
            New to LearnFirst?
          </span>

        </div>


        <button
          type="button"

          className="secondary-button auth-secondary"

          onClick={() =>
            navigate(
              "/setup"
            )
          }
        >
          Create learner profile
        </button>

      </div>

    </div>
  );
}
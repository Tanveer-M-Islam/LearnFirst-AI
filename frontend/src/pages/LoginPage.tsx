import {
  ArrowLeft,
  GraduationCap,
  LogIn,
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
  loginStudent,
} from "../api/auth";

import {
  saveStudent,
} from "../utils/studentStorage";


export default function LoginPage() {

  const navigate =
    useNavigate();


  const [
    username,
    setUsername,
  ] = useState("");


  const [
    password,
    setPassword,
  ] = useState("");


  const [
    loading,
    setLoading,
  ] = useState(
    false
  );


  const [
    error,
    setError,
  ] = useState<
    string | null
  >(
    null
  );


  const handleSubmit =
    async (
      event:
        FormEvent<HTMLFormElement>,
    ) => {

      event.preventDefault();


      const trimmedUsername =
        username
          .trim()
          .toLowerCase();


      if (
        !trimmedUsername
      ) {

        setError(
          "Enter your username."
        );

        return;
      }


      if (
        !password
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
              trimmedUsername,

            password,
          });


        saveStudent(
          student
        );


        navigate(
          "/dashboard"
        );


      } catch (err) {

        setError(
          err instanceof Error

            ? err.message

            : (
              "Could not login."
            ),
        );


      } finally {

        setLoading(
          false
        );
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
            Welcome back
          </h1>


          <p>
            Login to continue from
            your existing learning
            profile.
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
              htmlFor="login-username"
            >

              Username

            </label>


            <input
              id="login-username"

              className="text-input"

              placeholder="Your username"

              value={
                username
              }

              required

              minLength={3}

              maxLength={50}

              autoComplete="username"

              onChange={(event) =>
                setUsername(
                  event.target.value
                )
              }
            />

          </div>


          <div>

            <label
              className="field-label"
              htmlFor="login-password"
            >

              Password

            </label>


            <input
              id="login-password"

              type="password"

              className="text-input"

              placeholder="Your password"

              value={
                password
              }

              required

              minLength={6}

              maxLength={128}

              autoComplete="current-password"

              onChange={(event) =>
                setPassword(
                  event.target.value
                )
              }
            />

          </div>


          {error && (

            <div className="error-message">

              {error}

            </div>

          )}


          <button
            type="submit"

            className="primary-button setup-submit"

            disabled={
              loading
            }
          >

            {
              loading

                ? "Logging in..."

                : (
                  <>
                    <LogIn
                      size={18}
                    />

                    Login
                  </>
                )
            }

          </button>

        </form>


        <div
          style={{
            marginTop:
              "20px",

            textAlign:
              "center",
          }}
        >

          <p>
            New to LearnFirst?
          </p>


          <button
            type="button"

            className="secondary-button"

            onClick={() =>
              navigate(
                "/setup"
              )
            }
          >

            Create an account

          </button>

        </div>

      </div>

    </div>
  );
}
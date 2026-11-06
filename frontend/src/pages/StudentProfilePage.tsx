import {
  Check,
  Eye,
  EyeOff,
  GraduationCap,
  KeyRound,
  LockKeyhole,
  Save,
  ShieldCheck,
  UserRound,
} from "lucide-react";

import {
  type FormEvent,
  useEffect,
  useState,
} from "react";

import {
  useNavigate,
  useSearchParams,
} from "react-router";

import {
  getStudent,
  updateStudentCredentials,
} from "../api/students";

import type {
  Student,
} from "../types/student";

import {
  getStoredStudent,
  saveStudent,
} from "../utils/studentStorage";


function ageGroupLabel(
  value:
    string,
): string {

  switch (
    value
  ) {

    case "FOUNDATION":

      return "Foundation";


    case "INDEPENDENT":

      return "Independent";


    default:

      return "Developing";
  }
}


export default function StudentProfilePage() {

  const navigate =
    useNavigate();


  const [
    searchParams,
  ] = useSearchParams();


  const storedStudent =
    getStoredStudent();


  const [
    student,
    setStudent,
  ] = useState<
    Student | null
  >(
    storedStudent
  );


  const [
    editingSecurity,
    setEditingSecurity,
  ] = useState(
    !storedStudent
      ?.username
  );


  const [
    username,
    setUsername,
  ] = useState(
    storedStudent
      ?.username
    ?? "",
  );


  const [
    currentPassword,
    setCurrentPassword,
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
    confirmPassword,
    setConfirmPassword,
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


  const [
    notice,
    setNotice,
  ] = useState<
    string | null
  >(
    searchParams.get(
      "welcome"
    )
      ? (
        "Your learner profile "
        + "is ready. Set up login "
        + "details so you can return "
        + "from any session."
      )
      : null,
  );


  useEffect(
    () => {

      if (
        !storedStudent
      ) {

        navigate(
          "/login",

          {
            replace:
              true,
          },
        );

        return;
      }


      let cancelled =
        false;


      const refresh =
        async () => {

          try {

            const fresh =
              await getStudent(
                storedStudent.id
              );


            if (
              cancelled
            ) {

              return;
            }


            setStudent(
              fresh
            );


            setUsername(
              fresh.username
              ?? ""
            );


            setEditingSecurity(
              !fresh.username
            );


            saveStudent(
              fresh
            );


          } catch {

            /*
            Keep the cached profile
            usable if the refresh
            request temporarily fails.
            */

            if (
              !cancelled
            ) {

              setNotice(
                (
                  current,
                ) =>
                  current
                  ?? (
                    "Showing your saved "
                    + "profile. Live refresh "
                    + "was unavailable."
                  )
              );
            }
          }
        };


      void refresh();


      return () => {

        cancelled = true;
      };

    },
    [],
  );


  const saveCredentials =
    async (
      event:
        FormEvent<HTMLFormElement>,
    ) => {

      event.preventDefault();


      if (
        !student
      ) {

        return;
      }


      const normalized =
        username
          .trim()
          .toLowerCase();


      if (
        normalized.length
        < 3
      ) {

        setError(
          "Username must contain "
          + "at least 3 characters."
        );

        return;
      }


      if (
        !/^[a-z0-9._-]+$/
          .test(
            normalized
          )
      ) {

        setError(
          "Username may only contain "
          + "letters, numbers, dots, "
          + "underscores and hyphens."
        );

        return;
      }


      if (
        password.length
        < 8
      ) {

        setError(
          "Password must contain "
          + "at least 8 characters."
        );

        return;
      }


      if (
        password
        !== confirmPassword
      ) {

        setError(
          "New passwords do not match."
        );

        return;
      }


      if (
        student.username

        && !currentPassword
      ) {

        setError(
          "Enter your current password."
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

        const updated =
          await updateStudentCredentials(
            student.id,

            {
              username:
                normalized,

              password,

              current_password:
                student.username
                  ? currentPassword
                  : null,
            },
          );


        setStudent(
          updated
        );


        setUsername(
          updated.username
          ?? ""
        );


        setCurrentPassword(
          ""
        );


        setPassword(
          ""
        );


        setConfirmPassword(
          ""
        );


        setEditingSecurity(
          false
        );


        saveStudent(
          updated
        );


        setNotice(
          "Login details saved successfully."
        );


      } catch (err) {

        setError(
          err instanceof Error
            ? err.message
            : (
              "Could not update "
              + "login details."
            ),
        );


      } finally {

        setLoading(
          false
        );
      }
    };


  if (
    !student
  ) {

    return null;
  }


  const initial =
    student
      .display_name
      .trim()
      .charAt(0)
      .toUpperCase();


  return (

    <div className="profile-page">

      {/* =============================
          Header
      ============================== */}

      <header className="profile-page-header">

        <div>

          <span className="profile-page-kicker">
            Account
          </span>


          <h1>
            Student profile
          </h1>


          <p>
            View your learner
            information and manage
            account access.
          </p>

        </div>


        <button
          type="button"
          className="secondary-button"

          onClick={() =>
            navigate(
              "/dashboard"
            )
          }
        >
          Back to dashboard
        </button>

      </header>


      {notice && (

        <div className="profile-notice">

          <Check
            size={18}
          />

          <span>
            {notice}
          </span>

        </div>

      )}


      {/* =============================
          Main grid
      ============================== */}

      <section className="profile-grid">

        {/* ===========================
            Learner profile
        ============================ */}

        <article className="profile-card">

          <div className="profile-identity">

            <div className="profile-large-avatar">
              {initial}
            </div>


            <div>

              <span className="profile-card-label">
                Learner profile
              </span>


              <h2>
                {
                  student
                    .display_name
                }
              </h2>


              <p>
                {
                  ageGroupLabel(
                    student
                      .age_group
                  )
                }
                {" "}
                learner
              </p>

            </div>

          </div>


          <div className="profile-details">

            <div className="profile-detail-item">

              <span>
                Age
              </span>


              <strong>
                {
                  student.age
                }
              </strong>

            </div>


            <div className="profile-detail-item">

              <span>
                Class
              </span>


              <strong>
                Class {
                  student.grade
                }
              </strong>

            </div>


            <div className="profile-detail-item">

              <span>
                Learning stage
              </span>


              <strong>
                {
                  ageGroupLabel(
                    student
                      .age_group
                  )
                }
              </strong>

            </div>


            <div className="profile-detail-item">

              <span>
                Curriculum
              </span>


              <strong>
                Bangladesh English
              </strong>

            </div>

          </div>


          <div className="profile-learning-note">

            <GraduationCap
              size={20}
            />


            <div>

              <strong>
                Learning profile
              </strong>


              <p>
                Math and Science
                progress stays linked
                to this learner profile.
              </p>

            </div>

          </div>

        </article>


        {/* ===========================
            Account security
        ============================ */}

        <article className="profile-card">

          <div className="profile-card-heading">

            <div className="profile-card-icon">

              <ShieldCheck
                size={22}
              />

            </div>


            <div>

              <span className="profile-card-label">
                Account security
              </span>


              <h2>
                Sign-in details
              </h2>

            </div>

          </div>


          {!editingSecurity
            && student.username
            ? (

              <div className="security-summary">

                <div className="security-summary-row">

                  <div>

                    <UserRound
                      size={19}
                    />


                    <span>
                      Username
                    </span>

                  </div>


                  <strong>
                    {
                      student.username
                    }
                  </strong>

                </div>


                <div className="security-summary-row">

                  <div>

                    <LockKeyhole
                      size={19}
                    />


                    <span>
                      Password
                    </span>

                  </div>


                  <strong>
                    ••••••••••
                  </strong>

                </div>


                <div className="security-status">

                  <ShieldCheck
                    size={18}
                  />

                  Account login
                  is configured.

                </div>


                <button
                  type="button"
                  className="secondary-button profile-security-button"

                  onClick={() => {

                    setError(
                      null
                    );


                    setEditingSecurity(
                      true
                    );
                  }}
                >
                  Change sign-in details
                </button>

              </div>

            )
            : (

              <form
                className="security-form"

                onSubmit={
                  saveCredentials
                }
              >

                {!student.username && (

                  <div className="security-setup-message">

                    <KeyRound
                      size={19}
                    />


                    <div>

                      <strong>
                        Set up login
                      </strong>


                      <p>
                        Create a username
                        and password before
                        signing out.
                      </p>

                    </div>

                  </div>

                )}


                {student.username && (

                  <div>

                    <label
                      className="field-label"
                      htmlFor="current-password"
                    >
                      Current password
                    </label>


                    <input
                      id="current-password"

                      type={
                        showPassword
                          ? "text"
                          : "password"
                      }

                      className="text-input"

                      autoComplete="current-password"

                      value={
                        currentPassword
                      }

                      onChange={(event) =>
                        setCurrentPassword(
                          event
                            .target
                            .value
                        )
                      }
                    />

                  </div>

                )}


                <div>

                  <label
                    className="field-label"
                    htmlFor="profile-username"
                  >
                    Username
                  </label>


                  <input
                    id="profile-username"

                    className="text-input"

                    autoComplete="username"

                    value={
                      username
                    }

                    placeholder="Choose a username"

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
                    htmlFor="new-password"
                  >
                    New password
                  </label>


                  <div className="password-field">

                    <input
                      id="new-password"

                      type={
                        showPassword
                          ? "text"
                          : "password"
                      }

                      className="text-input"

                      autoComplete="new-password"

                      placeholder="At least 8 characters"

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


                <div>

                  <label
                    className="field-label"
                    htmlFor="confirm-password"
                  >
                    Confirm password
                  </label>


                  <input
                    id="confirm-password"

                    type={
                      showPassword
                        ? "text"
                        : "password"
                    }

                    className="text-input"

                    autoComplete="new-password"

                    value={
                      confirmPassword
                    }

                    onChange={(event) =>
                      setConfirmPassword(
                        event
                          .target
                          .value
                      )
                    }
                  />

                </div>


                {error && (

                  <div className="error-message">
                    {error}
                  </div>

                )}


                <div className="security-form-actions">

                  {student.username && (

                    <button
                      type="button"
                      className="secondary-button"

                      onClick={() => {

                        setEditingSecurity(
                          false
                        );


                        setError(
                          null
                        );


                        setCurrentPassword(
                          ""
                        );


                        setPassword(
                          ""
                        );


                        setConfirmPassword(
                          ""
                        );
                      }}
                    >
                      Cancel
                    </button>

                  )}


                  <button
                    type="submit"
                    className="primary-button"

                    disabled={
                      loading
                    }
                  >

                    <Save
                      size={18}
                    />

                    {
                      loading
                        ? "Saving..."
                        : "Save login"
                    }

                  </button>

                </div>

              </form>
            )}

        </article>

      </section>

    </div>
  );
}
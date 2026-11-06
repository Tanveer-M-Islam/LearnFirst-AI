import {
  Bell,
  ChevronDown,
  LogOut,
  UserRound,
} from "lucide-react";

import {
  useState,
} from "react";

import {
  useNavigate,
} from "react-router";

import {
  clearStoredStudent,
  getStoredStudent,
} from "../../utils/studentStorage";


export default function TopBar() {

  const navigate =
    useNavigate();


  const student =
    getStoredStudent();


  const [
    menuOpen,
    setMenuOpen,
  ] = useState(
    false
  );


  const name =
    student
      ?.display_name
    ?? "Learner";


  const initial =
    name
      .trim()
      .charAt(0)
      .toUpperCase()
    || "L";


  const logout =
    () => {

      if (
        !student
          ?.username
      ) {

        setMenuOpen(
          false
        );


        navigate(
          "/profile?loginRequired=1"
        );


        return;
      }


      clearStoredStudent();


      navigate(
        "/login",

        {
          replace:
            true,
        },
      );
    };


  return (

    <header className="topbar">

      <div>

        <div className="topbar-eyebrow">
          Your learning space
        </div>


        <div className="topbar-title">
          Ready to learn?
        </div>

      </div>


      <div className="topbar-actions">

        <button
          type="button"

          className="icon-button"

          aria-label="Notifications"
        >

          <Bell
            size={20}
          />

        </button>


        <div className="account-menu">

          <button
            type="button"
            className="profile-button"

            aria-expanded={
              menuOpen
            }

            onClick={() =>
              setMenuOpen(
                (
                  current,
                ) =>
                  !current
              )
            }
          >

            <span className="profile-avatar">
              {initial}
            </span>


            <span className="profile-text">

              <strong>
                {name}
              </strong>


              <small>
                Student
              </small>

            </span>


            <ChevronDown
              size={17}

              className={
                menuOpen
                  ? "account-chevron open"
                  : "account-chevron"
              }
            />

          </button>


          {menuOpen && (

            <div className="account-dropdown">

              <div className="account-dropdown-header">

                <strong>
                  {name}
                </strong>


                <span>

                  {
                    student
                      ?.username
                    ?? "Login not configured"
                  }

                </span>

              </div>


              <button
                type="button"

                onClick={() => {

                  setMenuOpen(
                    false
                  );


                  navigate(
                    "/profile"
                  );
                }}
              >

                <UserRound
                  size={18}
                />

                Profile settings

              </button>


              <div className="account-dropdown-divider" />


              <button
                type="button"
                className="account-logout"

                onClick={
                  logout
                }
              >

                <LogOut
                  size={18}
                />

                Log out

              </button>

            </div>

          )}

        </div>

      </div>

    </header>
  );
}
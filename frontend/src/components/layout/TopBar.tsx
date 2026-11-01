import {
  Bell,
  ChevronDown,
} from "lucide-react";

import {
  getStoredStudent,
} from "../../utils/studentStorage";


export default function TopBar() {
  const student =
    getStoredStudent();

  const name =
    student?.display_name ??
    "Learner";

  const initial =
    name
      .trim()
      .charAt(0)
      .toUpperCase() || "L";

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
          <Bell size={20} />
        </button>

        <button
          type="button"
          className="profile-button"
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
          />
        </button>
      </div>
    </header>
  );
}
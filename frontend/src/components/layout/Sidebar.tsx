import {
  BookOpen,
  ChartNoAxesColumnIncreasing,
  GraduationCap,
  Home,
  Sparkles,
} from "lucide-react";

import {
  NavLink,
} from "react-router";


const items = [
  {
    path: "/dashboard",
    label: "Home",
    icon: Home,
  },
  {
    path: "/learn",
    label: "Learn",
    icon: Sparkles,
  },
  {
    path: "/practice",
    label: "Practice",
    icon: BookOpen,
  },
  {
    path: "/progress",
    label: "Progress",
    icon:
      ChartNoAxesColumnIncreasing,
  },
];


export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-mark">
          <GraduationCap
            size={23}
          />
        </div>

        <div className="sidebar-brand-text">
          <div className="brand-name">
            LearnFirst
          </div>

          <div className="brand-subtitle">
            Learn. Think. Grow.
          </div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {items.map((item) => {
          const Icon =
            item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({
                isActive,
              }) =>
                [
                  "sidebar-link",
                  isActive
                    ? "active"
                    : "",
                ]
                  .filter(Boolean)
                  .join(" ")
              }
            >
              <Icon
                size={21}
                strokeWidth={2}
              />

              <span>
                {item.label}
              </span>
            </NavLink>
          );
        })}
      </nav>

      <div className="sidebar-helper">
        <div className="sidebar-helper-icon">
          ✨
        </div>

        <div>
          <strong>
            Think first
          </strong>

          <p>
            LearnFirst helps you
            discover the answer,
            not just receive it.
          </p>
        </div>
      </div>
    </aside>
  );
}
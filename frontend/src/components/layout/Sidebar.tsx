
import {
  BookOpen,
  Calculator,
  ChartNoAxesColumnIncreasing,
  FlaskConical,
  GraduationCap,
  History,
  Home,
  Languages,
  Sparkles,
} from "lucide-react";

import {
  NavLink,
} from "react-router";


const mainItems = [
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
];


const learnItems = [
  {
    path: "/learn/math",
    label: "Math",
    icon: Calculator,
  },
  {
    path: "/learn/science",
    label: "Science",
    icon: FlaskConical,
  },
  {
    path: "/learn/english",
    label: "English",
    icon: Languages,
  },
];


const bottomItems = [
  {
    path: "/practice",
    label: "Practice",
    icon: BookOpen,
  },
  {
    path: "/history",
    label: "History",
    icon: History,
  },
  {
    path: "/progress",
    label: "Progress",
    icon: ChartNoAxesColumnIncreasing,
  },
];


export default function Sidebar() {
  return (
    <aside className="sidebar">

      <div className="sidebar-brand">

        <div className="brand-mark">
          <GraduationCap size={23} />
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

        {mainItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === "/dashboard"}
              className={({ isActive }) =>
                [
                  "sidebar-link",
                  isActive ? "active" : "",
                ]
                  .filter(Boolean)
                  .join(" ")
              }
            >
              <Icon size={21} strokeWidth={2} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}


        {learnItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                [
                  "sidebar-link",
                  isActive ? "active" : "",
                ]
                  .filter(Boolean)
                  .join(" ")
              }
              style={{
                paddingLeft: "34px",
                fontSize: "0.9rem",
              }}
            >
              <Icon size={18} strokeWidth={2} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}


        {bottomItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                [
                  "sidebar-link",
                  isActive ? "active" : "",
                ]
                  .filter(Boolean)
                  .join(" ")
              }
            >
              <Icon size={21} strokeWidth={2} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}

      </nav>


      <div className="sidebar-helper">

        <div className="sidebar-helper-icon">
          ✨
        </div>

        <div>
          <strong>Think first</strong>
          <p>
            LearnFirst helps you discover the
            answer, not just receive it.
          </p>
        </div>

      </div>

    </aside>
  );
}

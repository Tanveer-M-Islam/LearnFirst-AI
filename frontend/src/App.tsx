import {
  Navigate,
  Route,
  Routes,
} from "react-router";

import AppShell from "./components/layout/AppShell";

import AssessmentPage from "./pages/AssessmentPage";
import DashboardPage from "./pages/DashboardPage";
import MathStartPage from "./pages/MathStartPage";
import ProgressPage from "./pages/ProgressPage";
import StudentSetupPage from "./pages/StudentSetupPage";
import TutorPage from "./pages/TutorPage";
import WelcomePage from "./pages/WelcomePage";


function ComingSoon({
  title,
}: {
  title: string;
}) {
  return (
    <div className="coming-soon surface-card">
      <div className="coming-soon-icon">
        ✨
      </div>

      <h1>
        {title}
      </h1>

      <p>
        We're building this
        learning experience next.
      </p>
    </div>
  );
}


export default function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <WelcomePage />
        }
      />

      <Route
        path="/setup"
        element={
          <StudentSetupPage />
        }
      />

      <Route
        element={
          <AppShell />
        }
      >
        <Route
          path="/dashboard"
          element={
            <DashboardPage />
          }
        />

        <Route
          path="/learn"
          element={
            <Navigate
              to="/learn/math"
              replace
            />
          }
        />

        <Route
          path="/learn/math"
          element={
            <MathStartPage />
          }
        />

        <Route
          path="/learn/math/session/:sessionId"
          element={
            <TutorPage />
          }
        />

        <Route
          path="/assessments/math/:assessmentType"
          element={
            <AssessmentPage />
          }
        />

        <Route
          path="/practice"
          element={
            <ComingSoon
              title="Practice"
            />
          }
        />

        <Route
          path="/progress"
          element={
            <ProgressPage />
          }
        />
      </Route>

      <Route
        path="*"
        element={
          <Navigate
            to="/"
            replace
          />
        }
      />
    </Routes>
  );
}
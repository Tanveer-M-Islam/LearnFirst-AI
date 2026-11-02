import {
  Navigate,
  Route,
  Routes,
} from "react-router";

import AppShell from "./components/layout/AppShell";

import AssessmentPage from "./pages/AssessmentPage";
import DashboardPage from "./pages/DashboardPage";
import LearnPage from "./pages/LearnPage";
import MathStartPage from "./pages/MathStartPage";
import ProgressHubPage from "./pages/ProgressHubPage";
import ProgressPage from "./pages/ProgressPage";
import ScienceProgressPage from "./pages/ScienceProgressPage";
import ScienceStartPage from "./pages/ScienceStartPage";
import ScienceTutorPage from "./pages/ScienceTutorPage";
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


        {/* =========================
            Learn Hub
        ========================== */}

        <Route
          path="/learn"

          element={
            <LearnPage />
          }
        />


        {/* =========================
            Math
        ========================== */}

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


        {/* =========================
            Science
        ========================== */}

        <Route
          path="/learn/science"

          element={
            <ScienceStartPage />
          }
        />


        <Route
          path="/learn/science/session/:sessionId"

          element={
            <ScienceTutorPage />
          }
        />


        {/* =========================
            Practice
        ========================== */}

        <Route
          path="/practice"

          element={
            <ComingSoon
              title="Practice"
            />
          }
        />


        {/* =========================
            Progress Hub
        ========================== */}

        <Route
          path="/progress"

          element={
            <ProgressHubPage />
          }
        />


        <Route
          path="/progress/math"

          element={
            <ProgressPage />
          }
        />


        <Route
          path="/progress/science"

          element={
            <ScienceProgressPage />
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
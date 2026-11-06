
import {
  Navigate,
  Route,
  Routes,
} from "react-router";

import AppShell from "./components/layout/AppShell";

import AssessmentPage from "./pages/AssessmentPage";
import DashboardPage from "./pages/DashboardPage";
import EnglishProgressPage from "./pages/EnglishProgressPage";
import EnglishStartPage from "./pages/EnglishStartPage";
import EnglishTutorPage from "./pages/EnglishTutorPage";
import HistoryPage from "./pages/HistoryPage";
import LearnPage from "./pages/LearnPage";
import MathStartPage from "./pages/MathStartPage";
import ProgressHubPage from "./pages/ProgressHubPage";
import ProgressPage from "./pages/ProgressPage";
import ScienceAssessmentPage from "./pages/ScienceAssessmentPage";
import ScienceProgressPage from "./pages/ScienceProgressPage";
import ScienceStartPage from "./pages/ScienceStartPage";
import ScienceTutorPage from "./pages/ScienceTutorPage";
import StudentLoginPage from "./pages/StudentLoginPage";
import StudentProfilePage from "./pages/StudentProfilePage";
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
      <div className="coming-soon-icon">✨</div>
      <h1>{title}</h1>
      <p>
        We're building this learning experience next.
      </p>
    </div>
  );
}


export default function App() {
  return (
    <Routes>

      {/* Public routes */}

      <Route
        path="/"
        element={<WelcomePage />}
      />

      <Route
        path="/setup"
        element={<StudentSetupPage />}
      />

      <Route
        path="/login"
        element={<StudentLoginPage />}
      />


      {/* Protected application routes */}

      <Route element={<AppShell />}>

        <Route
          path="/dashboard"
          element={<DashboardPage />}
        />

        <Route
          path="/profile"
          element={<StudentProfilePage />}
        />

        <Route
          path="/learn"
          element={<LearnPage />}
        />


        {/* Math */}

        <Route
          path="/learn/math"
          element={<MathStartPage />}
        />

        <Route
          path="/learn/math/session/:sessionId"
          element={<TutorPage />}
        />

        <Route
          path="/assessments/math/:assessmentType"
          element={<AssessmentPage />}
        />


        {/* Science */}

        <Route
          path="/learn/science"
          element={<ScienceStartPage />}
        />

        <Route
          path="/learn/science/session/:sessionId"
          element={<ScienceTutorPage />}
        />

        <Route
          path="/assessments/science/:assessmentType"
          element={<ScienceAssessmentPage />}
        />


        {/* English */}

        <Route
          path="/learn/english"
          element={<EnglishStartPage />}
        />

        <Route
          path="/learn/english/session/:sessionId"
          element={<EnglishTutorPage />}
        />


        {/* Practice */}

        <Route
          path="/practice"
          element={<ComingSoon title="Practice" />}
        />


        {/* Learning progress */}

        <Route
          path="/progress"
          element={<ProgressHubPage />}
        />

        <Route
          path="/progress/math"
          element={<ProgressPage />}
        />

        <Route
          path="/progress/science"
          element={<ScienceProgressPage />}
        />

        <Route
          path="/progress/english"
          element={<EnglishProgressPage />}
        />


        {/* Phase E: Conversation history */}

        <Route
          path="/history"
          element={<HistoryPage />}
        />

      </Route>


      {/* Fallback */}

      <Route
        path="*"
        element={<Navigate to="/" replace />}
      />

    </Routes>
  );
}

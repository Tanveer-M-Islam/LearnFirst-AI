
import {
  StrictMode,
} from "react";

import {
  createRoot,
} from "react-dom/client";

import {
  BrowserRouter,
} from "react-router";

import App from "./App";

import "./styles/tokens.css";
import "./styles/global.css";
import "./styles/layout.css";
import "./styles/tutor.css";
import "./styles/assessment.css";
import "./styles/progress.css";
import "./styles/science.css";
import "./styles/adaptive.css";
import "./styles/profile.css";
import "./styles/history.css";

// Shared Math, Science and English layout
import "./styles/learn-page-alignment.css";


createRoot(
  document.getElementById("root")!,
).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
);

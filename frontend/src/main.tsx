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

createRoot(
  document.getElementById(
    "root",
  )!,
).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
);
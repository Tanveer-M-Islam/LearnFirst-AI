# LearnFirst AI — Vercel-ready preliminary app

A focused tutoring demo: **Think first. Learn better.**

This folder is independent of the original FastAPI `backend/` and project `docs/`. It is a standard Next.js App Router application prepared for Vercel, with no ChatGPT hosting dependency. It includes the latest requested header/footer label removals.

## Deploy on Vercel

Import `Tanveer-M-Islam/LearnFirst-AI`, select the `codex/vercel-deployment` branch, and set **Root Directory** to `primary-v1`. Framework: **Next.js**. Install command: `npm ci`; build command: `npm run build`; output directory: leave the Next.js default. Node version: **22.x**. Use your personal Hobby workspace. No environment variables are required for built-in lesson mode.

This source is prepared for deployment; a Vercel URL exists only after Vercel reports a successful deployment. Account authorization and GitHub integration access must permit the selected Vercel workspace to import the repository.

## Run locally

```sh
cd primary-v1
npm ci
npm run dev
```

Open http://localhost:3000.

```sh
npm test
npm run typecheck
npm run build
npm start
```

## Teaching-first learning flow

1. Learn three short ideas with concrete examples, reflection prompts, and lesson-companion questions.
2. Try three understanding checks. First attempts are preserved for practice selection and reporting even after a successful retry.
3. A wrong answer starts progressively deeper support: notice a clue, connect a rule, study a different example, then follow a method with the final answer left to the learner.
4. Complete two guided practice questions, selected from first-attempt results.
5. Try three fresh independent questions without hints or teaching cards; review actual results afterward.

All three subjects (fractions, subject–verb agreement, water cycle) follow this flow. The lesson companion is a deterministic, browser-local conversation interface using prepared notes. It recognizes a limited set of lesson topics and help requests; it is not a live generative chatbot or an evaluator of open-ended reasoning. It clearly redirects unsupported questions. Its messages reset after refresh; lesson position and results persist in this browser.

The UI does not call a model. The optional `/api/tutor` adapter remains available for integration experiments, with staged authored guidance and optional Ollama rephrasing, but is not presented as active chat functionality.

## Verification

Run `npm test` and `npm run build`. Tests cover equivalent-fraction grading, adaptation, all subject session transitions, help counters, API validation/fallback, theory content, first-attempt score preservation, and bounded companion replies.

## Scope and limitations

This is a functional preliminary tutoring workflow. It does not claim live generative AI without a verified model connection, full curriculum RAG, official NCTB alignment, free-form homework reasoning evaluation, or validated educational efficacy. The nine learning cards are original notes. The current UI has a fixed introductory difficulty; the optional API can adjust phrasing; first attempts after teaching select practice difficulty.

Results stay in this browser, with no shared learner database or parent account. The three-question score difference is a session observation, not a standardized assessment or proof of lasting mastery. Repeated lessons reuse the question banks.

See `docs/recording-guide.md` for the recording sequence and narration. Use the actual deployed mode in your pitch.

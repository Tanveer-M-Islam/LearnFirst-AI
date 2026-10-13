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

## Working features

- Three subjects: fractions, subject–verb agreement, and the water cycle.
- Three-question diagnostic; foundational or core practice selected from the result.
- Two guided exercises; three progressive hints; retries and full explanations.
- Three fresh independent questions with hints disabled.
- Actual session scores, concept review, browser-local persistence, report export and reset.
- Responsive UI and optional server-side Ollama hint rephrasing.

## Model connection

Without a configured model, the application honestly labels its authored, rule-based hints. To use Ollama, configure `OLLAMA_BASE_URL`, `OLLAMA_MODEL` (default `llama3.2`), and optionally `OLLAMA_API_KEY` as server environment variables in Vercel. The base URL must be reachable from Vercel; `localhost` refers to the server, not your computer. Keep provider credentials private. Model failures visibly fall back to authored hints.

Before attaching a resource-limited model to a public service, enforce distributed quotas/rate limits at its endpoint. No provider is required or called in the default built-in mode.

## Scope and limitations

This is a functional preliminary tutoring workflow. It does not claim live generative AI without a verified model connection, full curriculum RAG, official NCTB alignment, free-form homework reasoning evaluation, or validated educational efficacy. The nine learning cards are original notes. Age affects optional model phrasing; diagnostic answers select practice difficulty.

Results stay in this browser, with no shared learner database or parent account. The three-question score difference is a session observation, not a standardized assessment or proof of lasting mastery. Repeated lessons reuse the question banks.

See `docs/recording-guide.md` for the recording sequence and narration. Use the actual deployed mode in your pitch.

# LearnFirst AI — Primary v1

A self-contained preliminary competition demo: **Think first. Learn better.**

This directory is independent of the existing `backend/` and `docs/` project. It does not import or modify them. The original FastAPI project remains the authoritative learning implementation; this demo is a focused deployable companion.

## What works

- Responsive learner dashboard, three lesson flows, reference library, and progress report.
- Mathematics: fraction addition and equivalent-answer checking.
- English: introductory subject–verb agreement.
- Science: evaporation, condensation, and precipitation.
- Three-question diagnostic selects foundational or core practice.
- Two guided exercises with three progressive hints, retries, and full explanations.
- Three fresh independent questions with hints disabled.
- Session results, concept review, JSON report download, profile editing, and data reset.
- Optional server-side Ollama integration to rephrase authored hints for learner age.

## Honest implementation boundaries

**The deployed default uses authored, rule-based tutoring. No live LLM is connected by default.** The interface labels each hint's actual engine, and the About page describes the implementation. Do not present this version as a live generative-AI tutor until a model is configured and tested.

This is not full curriculum RAG: it uses nine original reference cards linked to three topics. There is no NCTB alignment claim, free-form homework chat, general misconception model, voice support, parent authentication, or shared student database. Age affects optional model phrasing, not lesson difficulty; diagnostic results select practice difficulty.

Progress is held in browser localStorage. A completed lesson contains three starting questions, two practices, and three fresh independent checks. Percentage-point change is an observation from these questions, not validated educational efficacy. Repeated sessions reuse the question banks and can reflect familiarity. Fraction grading accepts exact numeric equivalents (tolerance 0.000001), including unsimplified fractions. Free-form reasoning is not automatically graded.

## Run locally

Requires Node.js 22.13+ (Node.js 24 recommended).

```sh
cd primary-v1
npm install
npm run dev
```

The portable development command serves http://localhost:5173. On managed Sites environments the helpers select the managed execution profile. Both profiles retain the Sites build integration.

```sh
npm test
npm run typecheck
npm run build
```

`app/page.tsx` is the learner interface. `app/globals.css` contains the responsive styling. `lib/learning.ts` contains the questions, grading, adaptive selection, and state transitions. `app/api/tutor/route.ts` controls optional model calls and reliable fallback. `tests/` covers grading, state transitions, and API validation/fallback.

## Connect a real model

The server supports the same Ollama `/api/chat` protocol used by the original backend. Set server environment variables (never put secrets into frontend code):

- `OLLAMA_BASE_URL`: origin of your reachable Ollama service, without `/api/chat`.
- `OLLAMA_MODEL`: installed model name, default `llama3.2`.
- `OLLAMA_API_KEY`: optional bearer credential for a protected service.

For local development create an ignored `.env.local` with `OLLAMA_BASE_URL=http://127.0.0.1:11434` and `OLLAMA_MODEL=llama3.2`, after installing/running Ollama and pulling that model. For hosted deployment localhost points to the hosted server, not your laptop: use a securely hosted reachable service and configure the variables in the Site environment settings. Do not expose an unprotected Ollama endpoint to the internet. The hosted model path has not been live-verified because no provider endpoint/credential was supplied.

The model sees only a selected authored hint, reference card, and learner age. It does not control grading or the lesson progression. Requests time out, then visibly fall back to built-in hints. Generated wording is not guaranteed error-free; evaluate it before a real child-facing release. For a public service, add distributed quotas/rate limits to the model endpoint before attaching a paid or resource-limited provider. The default built-in mode makes no provider calls.

## Deployment

The source includes the managed Sites/Vinext build integration. A hosted Site is prepared separately; source is synchronized there before deployment. The copy of `.openai/hosting.json` in this GitHub folder is intentionally generic, with no managed Site identity. Do not point a new deployment at someone else's Site ID.

The initial deployed Site is owner-private under the platform's default policy. Change sharing to public before giving its URL to competition reviewers. This demo has no shared learner database: making it public does not publish stored local results.

See `docs/recording-guide.md` for an exact recording journey and a 180-second pitch outline that matches the implemented features.

## Verification

- Nine Node tests: equivalent fractions and invalid numbers; diagnostic adaptation; all three complete session flows; hints/reset/skips; targeted common-error guidance; question content consistency; API validation; fallback; mocked model success.
- TypeScript type checking and production build.
- Browser interaction, visual rendering, public access, and a real Ollama endpoint require a separate live check. A mocked model test is not proof of live AI connectivity.

# LearnFirst AI — Implementation Roadmap

**Document ID:** LF-IMPL-001  
**Version:** 1.0  
**Status:** Approved Initial Build Plan  
**Project:** LearnFirst AI  
**Primary Users:** Children aged 7–14  
**Primary Context:** Bangladesh-aligned, English-language learning  
**Specialized Subjects:** Mathematics, English, Science  
**Additional Support:** General Guided Learning  

---

# 1. Purpose

This document converts all previous planning documents into the actual implementation sequence for LearnFirst AI.

The goal is to ensure that development happens in a controlled order.

The project should not begin by building every feature at once.

Instead, development should follow:

```text
Core Infrastructure
↓
Tutor Policy Engine
↓
Math Tutor
↓
Evaluation
↓
English Tutor
↓
Science + RAG
↓
Progress & Parent Features
↓
Voice
↓
Frontend
↓
Safety Hardening
↓
Optimization
↓
Deployment
```

The implementation order prioritizes the project's unique contribution:

> **Guided tutoring behavior before secondary product features.**

---

# 2. Development Principles

Throughout implementation, follow these rules:

1. Build one stable layer before adding the next.
2. Keep Tutor Policy independent from the LLM.
3. Add evaluation alongside each feature.
4. Commit working milestones to GitHub.
5. Do not fine-tune unless evaluation shows a measurable need.
6. Keep local development lightweight.
7. Use Colab only for GPU-heavy experiments.
8. Keep documentation synchronized with actual implementation.
9. Prefer simple working architecture over unnecessary complexity.
10. Every major bug should become a regression test.

---

# 3. Development Environment Strategy

## Local PC

Use local VS Code for:

```text
FastAPI
SQLite
SQLAlchemy
Tutor Policy
Math Validation
Chroma
Sentence Transformers
Evaluation
Testing
React
Git/GitHub
Documentation
```

## Google Colab

Use Colab for:

```text
LoRA/QLoRA experiments
Model benchmarking
Bulk embedding experiments
Speech model experiments
Classifier training
Large batch evaluation
```

## Important Rule

The final product must not depend on a running Colab session.

---

# 4. Main Implementation Phases

```text
Phase 0  — Repository & Environment
Phase 1  — Backend Foundation
Phase 2  — Database & Student State
Phase 3  — Tutor Policy Engine
Phase 4  — LLM Gateway
Phase 5  — Math Tutor MVP
Phase 6  — Evaluation Harness
Phase 7  — English Tutor
Phase 8  — Science Tutor + RAG
Phase 9  — General Learning
Phase 10 — Progress & Mastery
Phase 11 — Parent Dashboard Backend
Phase 12 — Voice Mode
Phase 13 — Safety & Guardrails
Phase 14 — Frontend
Phase 15 — Integration Testing
Phase 16 — Optimization & Observability
Phase 17 — Model Experiments / Optional Fine-Tuning
Phase 18 — Deployment
Phase 19 — Final Evaluation
Phase 20 — Portfolio & Recruiter Demo
```

---

# 5. Phase 0 — Repository & Environment

## Goal

Prepare a clean project workspace.

## Tasks

Confirm project structure:

```text
LearnFirst-AI/
├── backend/
├── frontend/
├── docs/
├── evaluation/
├── knowledge/
├── notebooks/
├── tests/
├── .gitignore
└── README.md
```

Create Python environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install initial backend packages:

```text
fastapi
uvicorn
pydantic
sqlalchemy
alembic
pytest
python-dotenv
httpx
```

Optional later:

```text
chromadb
sentence-transformers
sympy
```

## Deliverables

- project environment runs;
- Git repository connected;
- backend folder exists;
- virtual environment works;
- `.env.example` exists;
- requirements file exists.

## Suggested Commit

```text
Set up LearnFirst AI development environment
```

---

# 6. Phase 1 — Backend Foundation

## Goal

Create the basic FastAPI application.

## Build

```text
backend/app/main.py
backend/app/core/config.py
backend/app/api/v1/health.py
```

Initial endpoints:

```text
GET /api/v1/health
GET /api/v1/version
```

Expected health response:

```json
{
  "status": "ok",
  "service": "learnfirst-api"
}
```

## Add

- configuration loading;
- request ID middleware;
- basic structured logging;
- exception handling.

## Tests

- health endpoint;
- invalid route;
- config loading.

## Deliverables

- FastAPI runs locally;
- tests pass;
- request ID appears in responses/logs.

## Suggested Commit

```text
Build FastAPI backend foundation
```

---

# 7. Phase 2 — Database & Student State

## Goal

Implement persistent student and learning state.

## First Tables

Build only:

```text
ParentAccount
StudentProfile
LearningSession
StudentAttempt
TutorDecision
MasteryRecord
```

Do not implement every planned table yet.

## Tasks

- SQLAlchemy base;
- SQLite connection;
- Alembic setup;
- models;
- repositories;
- services;
- basic CRUD.

## Endpoints

```text
POST /api/v1/students
GET  /api/v1/students/{id}

POST /api/v1/sessions
GET  /api/v1/sessions/{id}
```

## Tests

- create student;
- age validation;
- age-group assignment;
- create session;
- state persistence.

## Deliverables

Student state survives multiple API requests.

## Suggested Commit

```text
Add student profiles and learning session persistence
```

---

# 8. Phase 3 — Tutor Decision Models

## Goal

Define the structured objects used by Tutor Policy.

Create:

```text
TutorIntent
TutorAction
LearningMode
Subject
AttemptStatus
MasteryState
AgeGroup
TutorDecision
```

Example:

```json
{
  "subject": "MATH",
  "intent": "HOMEWORK_REQUEST",
  "next_action": "ASK_ATTEMPT",
  "hint_level": 0,
  "allow_final_answer": false,
  "requires_rag": false,
  "requires_validation": false
}
```

## Deliverables

Tutor decisions can be created and validated without an LLM.

## Suggested Commit

```text
Add structured tutor decision models
```

---

# 9. Phase 4 — Tutor Policy Engine

## Goal

Implement the core contribution of LearnFirst AI.

This phase should happen before advanced RAG, voice, or frontend work.

## Initial Rule-Based Policy

Start with deterministic rules.

Example:

```text
HOMEWORK_REQUEST
+
attempt_count = 0
→ ASK_ATTEMPT
```

```text
DIRECT_ANSWER_REQUEST
+
allow_final_answer = false
→ ASK_GUIDING_QUESTION
```

```text
I_DONT_KNOW
+
hint_level = 2
→ GIVE_HINT level 3
```

## Implement

```text
policy_engine.py
hint_ladder.py
decision_models.py
session_state.py
```

## Must Support

- attempt-first behavior;
- direct-answer resistance;
- hint ladder;
- hint escalation;
- new-problem hint reset;
- Mock Test restriction;
- age-group influence;
- full-explanation conditions.

## Tests

Create deterministic unit tests for every policy rule.

## Deliverables

Tutor Policy works without an LLM.

## Suggested Commit

```text
Implement core tutor policy engine
```

---

# 10. Phase 5 — LLM Gateway

## Goal

Connect a model without coupling the project to one provider.

## Interface

Create:

```text
backend/app/llm/gateway.py
backend/app/llm/providers/
```

Standard method:

```python
generate(...)
```

## Initial Providers

Recommended development order:

```text
1. Mock provider
2. Ollama provider
3. Optional hosted provider
```

The mock provider allows deterministic testing without API cost.

## Add

- timeout;
- retry;
- structured output parsing;
- model metadata;
- token/latency logging.

## Deliverables

Subject tutors call the gateway rather than a provider directly.

## Suggested Commit

```text
Add provider-independent LLM gateway
```

---

# 11. Phase 6 — Math Tutor MVP

## Goal

Create the first complete subject workflow.

Math should be implemented first because:

- reasoning is easy to demonstrate;
- deterministic validation is possible;
- answer-first behavior is easy to test;
- misconceptions are measurable.

## Initial Math Topics

```text
Arithmetic
Fractions
Percentages
Ratio
Simple Linear Equations
```

## Components

```text
math/tutor.py
math/validator.py
math/prompts.py
```

## Math Validator

Use:

```text
Python
SymPy
```

## First Complete Flow

```text
Student:
Solve 3x + 5 = 20

↓
Router: MATH
↓
Intent: HOMEWORK_REQUEST
↓
Policy: ASK_ATTEMPT
↓
Student attempt
↓
Math Validator
↓
Misconception Detection
↓
Tutor Decision
↓
LLM generates guided response
↓
Output validation
```

## Deliverables

A complete multi-turn guided Math session.

## Suggested Commit

```text
Implement guided Math tutor MVP
```

---

# 12. Phase 7 — Evaluation Harness

## Goal

Build evaluation early, not after the project is finished.

## Implement First

```text
answer_resistance.jsonl
tutor_policy.jsonl
math_correctness.jsonl
math_misconceptions.jsonl
```

## Build

```text
evaluation/runners/
evaluation/metrics/
evaluation/reports/
```

## First Metrics

- Tutor Policy Compliance;
- Answer Resistance;
- Math Accuracy;
- misconception accuracy;
- latency;
- error rate.

## Deliverables

One command should run the initial evaluation suite.

Example:

```powershell
python -m evaluation.runners.run_core
```

## Suggested Commit

```text
Add initial LearnFirst evaluation framework
```

---

# 13. Phase 8 — English Tutor

## Goal

Add a second subject with a different tutoring style.

## Initial Scope

```text
Past Tense
Subject-Verb Agreement
Parts of Speech
Vocabulary
Paragraph Writing
```

## Core Principles

- guide correction;
- avoid rewriting everything;
- ask student to retry;
- adapt by age.

## Components

```text
english/tutor.py
english/prompts.py
```

## Evaluation

Add:

```text
english_tutoring.jsonl
```

Measure:

- correctness;
- guidance;
- rewrite leakage;
- age fit.

## Deliverables

Working text-based English tutor.

## Suggested Commit

```text
Add guided English tutor
```

---

# 14. Phase 9 — Science Tutor + RAG

## Goal

Add grounded Science tutoring.

## Initial Concepts

```text
Photosynthesis
Human Digestion
Matter
Force and Motion
Heat
```

## RAG Build

Implement:

```text
ingestion
cleaning
chunking
metadata
embeddings
Chroma
retrieval
context builder
```

## First Knowledge Base

Use a small trusted set.

Do not ingest the whole curriculum yet.

## Deliverables

Science Tutor retrieves trusted content and produces guided explanations.

## Evaluation

Add:

```text
science_grounding.jsonl
rag_retrieval.jsonl
```

## Suggested Commit

```text
Add Science tutor and educational RAG pipeline
```

---

# 15. Phase 10 — General Learning

## Goal

Add a controlled fallback for other educational topics.

## Behavior

- guided learning;
- age adaptation;
- RAG when factual;
- clear specialization limits.

## Deliverables

General educational questions can be handled without bypassing Tutor Policy.

## Suggested Commit

```text
Add general guided learning mode
```

---

# 16. Phase 11 — Progress & Mastery

## Goal

Turn tutoring interactions into meaningful learning progress.

## Implement

- mastery states;
- hint statistics;
- independent attempt metrics;
- direct-answer request count;
- follow-up success;
- session summaries.

## Initial Mastery States

```text
NOT_STARTED
LEARNING
DEVELOPING
STRONG
```

## Deliverables

Student progress persists across sessions.

## Suggested Commit

```text
Add progress and mastery tracking
```

---

# 17. Phase 12 — Parent Dashboard Backend

## Goal

Expose learning summaries for parents.

## APIs

```text
GET /api/v1/parents/{parent_id}/students
GET /api/v1/progress/{student_id}
GET /api/v1/progress/{student_id}/summary
```

## Return

- Math progress;
- English progress;
- Science progress;
- weak concepts;
- independent-attempt rate;
- average hint level;
- follow-up success.

## Privacy Rule

Do not expose complete raw conversations by default.

## Suggested Commit

```text
Add parent progress APIs
```

---

# 18. Phase 13 — English Voice Mode

## Goal

Add spoken English practice after text tutoring is stable.

## Pipeline

```text
Microphone
↓
STT
↓
English Tutor
↓
Feedback
↓
TTS
```

## Initial Implementation

Use adapter interfaces:

```text
STTProvider
TTSProvider
```

Possible STT:

```text
Whisper / faster-whisper
```

## Voice MVP

Focus on:

- short conversation;
- simple grammar feedback;
- vocabulary;
- transcript review;
- text fallback.

Do not build advanced pronunciation scoring yet.

## Suggested Commit

```text
Add English voice practice pipeline
```

---

# 19. Phase 14 — Safety & Guardrails Hardening

## Goal

Strengthen child-facing safety and Tutor Policy enforcement.

## Add

- input guard;
- output guard;
- prompt-injection checks;
- answer-leak checks;
- age appropriateness checks;
- restricted tool policy.

## Important

Basic guards should already exist earlier.

This phase is for stronger coverage after the main flows exist.

## Evaluation

Run:

```text
policy_bypass.jsonl
safety_cases.jsonl
```

## Suggested Commit

```text
Harden child safety and tutor policy guardrails
```

---

# 20. Phase 15 — Frontend

## Goal

Build the recruiter-facing product UI.

Start frontend only after core backend behavior is stable.

## Student Pages

```text
Login/Profile
Student Home
Tutor Chat
Learn Mode
Homework Help
Practice
Mock Test
Voice Practice
Progress
```

## Parent Pages

```text
Parent Dashboard
Subject Progress
Learning Independence
Weak Concepts
```

## UI Priorities

- simple;
- child-friendly;
- readable;
- not overly childish for age 14;
- responsive;
- accessible.

## Suggested Commit

```text
Build LearnFirst student and parent frontend
```

---

# 21. Phase 16 — Integration Testing

## Goal

Verify the full system.

Test:

```text
Frontend → API
API → Database
Policy → Subject Tutor
Tutor → LLM
Science → RAG
Math → Validator
Voice → STT/TTS
Progress → Parent Dashboard
```

## Add

- API integration tests;
- database tests;
- end-to-end scenario tests.

## Suggested Commit

```text
Add end-to-end integration tests
```

---

# 22. Phase 17 — Observability & Optimization

## Goal

Measure and improve production behavior.

## Add

- latency metrics;
- token usage;
- model errors;
- retrieval latency;
- tutor decision logging;
- request success rate.

## Optimize

- context size;
- prompt size;
- RAG top-k;
- model choice;
- caching;
- session summarization.

## Suggested Commit

```text
Add observability and performance optimization
```

---

# 23. Phase 18 — Colab Model Experiments

## Goal

Use GPU experiments only after the baseline system is measurable.

Possible experiments:

```text
Intent classifier
Misconception classifier
Tutor action classifier
Embedding comparison
Fine-tuned response style
```

## Decision Rule

Only continue with training if:

```text
Measured weakness exists
+
Training improves it
+
Complexity is justified
```

## Colab Artifacts

Save:

```text
notebooks/colab/
experiment reports
metrics
model configuration
```

Large model files should not be committed to GitHub.

## Suggested Commit

```text
Add model experiment results
```

---

# 24. Phase 19 — Optional Fine-Tuning

This phase may be skipped.

Possible targets:

```text
Tutor Action Classification
Misconception Classification
Age-Adaptive Response Style
```

Do not attempt to train a large model from scratch.

## Required Comparison

```text
Base
vs
Prompted
vs
Fine-Tuned
```

Use the same held-out evaluation set.

Only keep the fine-tuned model if it produces a meaningful improvement.

---

# 25. Phase 20 — Deployment

## Goal

Deploy a recruiter-accessible MVP.

Target architecture:

```text
React Frontend
↓
Hosted FastAPI
↓
PostgreSQL
↓
Vector Store
↓
LLM Provider
```

## Before Deployment

- migrate SQLite → PostgreSQL;
- configure environment variables;
- disable debug mode;
- verify CORS;
- verify authentication;
- verify secrets;
- run full evaluation;
- run safety checks.

## Suggested Commit

```text
Prepare LearnFirst AI production deployment
```

---

# 26. Phase 21 — Final Evaluation

Run the full evaluation suite.

Required outputs:

```text
summary.json
detailed_results.jsonl
failures.jsonl
metrics.csv
report.md
```

Compare:

```text
Generic Baseline
vs
LearnFirst Architecture
```

Report only actual measurements.

---

# 27. Phase 22 — Final Documentation

Update:

```text
README.md
docs/
architecture diagrams
API documentation
evaluation results
deployment guide
limitations
future work
```

Final README should include:

- problem;
- solution;
- architecture;
- screenshots;
- technologies;
- evaluation;
- setup;
- demo;
- limitations.

---

# 28. Phase 23 — Recruiter Demo

Recommended scenario:

```text
1. Student asks for a direct Math answer
2. LearnFirst avoids answer-first behavior
3. Student attempts
4. System detects misconception
5. Tutor gives progressive hint
6. Student succeeds
7. Mastery check appears
8. Parent dashboard updates
9. Science question demonstrates grounded RAG
10. English Voice Mode is demonstrated
```

This demonstrates the whole product story quickly.

---

# 29. First Working MVP Definition

The first working MVP does not require every final feature.

Minimum usable MVP:

```text
FastAPI
SQLite
Student Profile
Learning Session
Tutor Policy Engine
LLM Gateway
Math Tutor
SymPy Validator
Answer Resistance
Hint Ladder
Attempt Evaluation
Mastery Check
Evaluation Harness
Basic Safety
```

Once this works reliably, the project has proven its central idea.

---

# 30. MVP 2 Definition

```text
MVP 1
+
English Tutor
+
Science Tutor
+
RAG
+
Progress Tracking
+
Parent Summary
```

---

# 31. MVP 3 Definition

```text
MVP 2
+
Voice
+
React Frontend
+
Full Safety Tests
+
Observability
+
Deployment
```

---

# 32. Recommended Development Sequence by Week

This schedule is flexible.

## Week 1

```text
Backend foundation
Database
Student/session models
Tutor decision models
```

## Week 2

```text
Tutor Policy Engine
Hint ladder
Policy unit tests
```

## Week 3

```text
LLM Gateway
Math Tutor
SymPy validator
Math evaluation
```

## Week 4

```text
English Tutor
Progress/mastery
```

## Week 5

```text
Science
RAG ingestion
Retrieval evaluation
```

## Week 6

```text
Parent backend
Safety hardening
```

## Week 7

```text
Voice
React frontend
```

## Week 8

```text
Integration
Observability
Model comparison
```

## Week 9

```text
Deployment
Final evaluation
Documentation
Recruiter demo
```

This is not a fixed deadline. Stability is more important than speed.

---

# 33. Git Workflow

Recommended for a solo project:

```text
main
+
short-lived feature branches
```

Examples:

```text
feature/tutor-policy
feature/math-tutor
feature/rag
feature/voice
feature/frontend
```

For a simpler early workflow, stable direct commits to `main` are acceptable.

---

# 34. Suggested Git Commit Checkpoints

```text
Set up LearnFirst AI development environment
Build FastAPI backend foundation
Add student profiles and learning session persistence
Add structured tutor decision models
Implement core tutor policy engine
Add provider-independent LLM gateway
Implement guided Math tutor MVP
Add initial LearnFirst evaluation framework
Add guided English tutor
Add Science tutor and educational RAG pipeline
Add general guided learning mode
Add progress and mastery tracking
Add parent progress APIs
Add English voice practice pipeline
Harden child safety and tutor policy guardrails
Build LearnFirst student and parent frontend
Add end-to-end integration tests
Add observability and performance optimization
Prepare LearnFirst AI deployment
Add final evaluation results
```

---

# 35. Documentation Update Rule

At the end of each major phase:

1. update `progress_log.md`;
2. update `project_decisions.md` if architecture changed;
3. update `project_risks.md` if new risks appeared;
4. update the relevant design document;
5. commit documentation with implementation.

---

# 36. Definition of Done for a Feature

A feature is complete when:

- [ ] implementation exists;
- [ ] input validation exists;
- [ ] error handling exists;
- [ ] tests exist;
- [ ] evaluation cases exist where relevant;
- [ ] logging exists where needed;
- [ ] documentation is updated;
- [ ] Git commit is made.

---

# 37. Development Priorities

If time becomes limited:

```text
1. Tutor Policy
2. Math Tutor
3. Evaluation
4. Learning State
5. Safety
6. Science + RAG
7. English Tutor
8. Progress
9. Frontend
10. Voice
11. Advanced Optimization
12. Fine-Tuning
```

Fine-tuning is intentionally low priority.

---

# 38. Features That Can Be Deferred

```text
Advanced pronunciation scoring
Teacher dashboard
Gamification
Native mobile app
Multiple curricula
Multiple languages
Advanced recommendation engine
Real-time classroom support
Large-scale fine-tuning
Microservices
Redis
pgvector migration
```

A polished core is more valuable than an incomplete huge system.

---

# 39. First Implementation Task After Planning

After this roadmap, implementation begins with:

## Backend Foundation

Create:

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── v1/
│   │       └── health.py
│   └── core/
│       └── config.py
├── tests/
│   └── test_health.py
├── requirements.txt
└── .env.example
```

First goal:

```text
Run FastAPI
↓
GET /api/v1/health
↓
Receive status=ok
↓
Pytest passes
```

This is the first real implementation milestone.

---

# 40. Implementation Exit Criteria

Planning is complete enough to begin coding when:

- [ ] project problem is defined;
- [ ] requirements exist;
- [ ] user stories exist;
- [ ] Tutor Policy exists;
- [ ] architecture exists;
- [ ] database/state design exists;
- [ ] Data/RAG strategy exists;
- [ ] evaluation plan exists;
- [ ] implementation roadmap exists.

At that point, further design should happen alongside implementation rather than delaying coding indefinitely.

---

# 41. Current Project Status

```text
Project Initiation              ✅
Product Requirements            ✅
User Stories & Use Cases        ✅
Tutor Policy Specification      ✅
System Architecture             ✅
Database / State Design         ✅
Data / RAG Strategy             ✅
Evaluation Plan                 ✅
Implementation Roadmap          ✅
Implementation                  ⏳ NEXT
```

---

# 42. Next Step

The next step is no longer another large planning document.

The project should now enter:

# **Implementation Phase 0 — Backend Foundation**

The first implementation task will:

1. create the backend folder structure;
2. create the Python virtual environment;
3. create `requirements.txt`;
4. create `.env.example`;
5. create the FastAPI application;
6. add `/api/v1/health`;
7. add configuration management;
8. add request ID support;
9. add the first Pytest test;
10. run the project locally;
11. commit the working milestone to GitHub.

From this point onward, project documentation and implementation will progress together.

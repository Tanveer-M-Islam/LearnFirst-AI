# LearnFirst AI — System Architecture

**Document ID:** LF-SA-001  
**Version:** 1.0  
**Status:** Initial Architecture Specification  
**Project:** LearnFirst AI  
**Primary Users:** Children aged 7–14  
**Primary Context:** Bangladesh-aligned, English-language learning  
**Specialized Subjects:** Mathematics, English, Science  
**Additional Support:** General Guided Learning  

---

# 1. Purpose

This document defines the initial technical architecture of LearnFirst AI.

The architecture follows one central principle:

> **The LLM is a language-generation component, not the controller of the entire product.**

Important educational decisions such as whether the student must attempt first, which hint level is allowed, whether a final answer may be disclosed, whether Mock Test rules are active, which age profile applies, and whether a mastery check is required should be controlled by application logic and structured state.

---

# 2. Architecture Goals

The system should be:

- modular;
- tutor-policy-centered;
- safe for child-facing use;
- testable;
- hardware-aware;
- provider-independent;
- easy to develop on the current PC;
- able to use Google Colab for GPU-heavy experiments;
- deployable without depending on Colab.

---

# 3. Recommended Technology Stack

| Layer | Initial Choice | Reason |
|---|---|---|
| Frontend | React + Vite | Professional recruiter-facing UI |
| Backend API | FastAPI | Python-native, strong AI integration |
| Validation | Pydantic | Structured request/response validation |
| ORM | SQLAlchemy | Database abstraction |
| Migrations | Alembic | Database schema versioning |
| Development DB | SQLite | Lightweight local development |
| Production DB | PostgreSQL | Better production scalability |
| Vector Store | Chroma initially | Easy local RAG development |
| Embeddings | Sentence Transformers | Lightweight local embeddings |
| Math Validation | SymPy + Python | Deterministic Math checking |
| LLM Access | LLM Gateway abstraction | Local/cloud model switching |
| Local LLM Option | Ollama | Useful for development experiments |
| STT | Whisper/faster-whisper adapter | Speech recognition |
| TTS | Pluggable TTS adapter | Allows provider replacement |
| Testing | Pytest | Unit, integration, policy tests |
| Logging | Structured Python logging | Lightweight observability |
| Cache | In-memory initially, Redis later | Keeps MVP simple |
| Packaging | Docker later | Reproducible deployment |
| Version Control | Git + GitHub | Continuous project history |

---

# 4. High-Level Architecture

```text
                         CHILD / PARENT
                               ↓
                         REACT FRONTEND
                               ↓
                           FASTAPI API
                               ↓
                 AUTHENTICATION / PROFILE
                               ↓
                      INPUT SAFETY LAYER
                               ↓
                   INTENT + SUBJECT ROUTER
                               ↓
                    LEARNING SESSION STATE
                               ↓
                      TUTOR POLICY ENGINE
                  /           |            \
                 /            |             \
              MATH         ENGLISH        SCIENCE
               |              |              |
        Math Validator      Voice         RAG Service
               \              |              /
                \             |             /
                     SUBJECT TUTORS
                           ↓
                      LLM GATEWAY
                           ↓
                 OUTPUT POLICY VALIDATOR
                           ↓
                 PROGRESS / MASTERY SERVICE
                           ↓
                      APPLICATION DB
                           ↓
                         RESPONSE
```

Supporting systems:

```text
Vector Store
Evaluation
Observability
Caching
Parent Dashboard
```

---

# 5. Architectural Layers

The application is divided into:

1. Presentation Layer
2. API Layer
3. Authentication/Profile Layer
4. Child Safety Layer
5. Routing Layer
6. Learning State Layer
7. Tutor Policy Layer
8. Subject Tutor Layer
9. AI/Tool Layer
10. Knowledge/RAG Layer
11. Persistence Layer
12. Progress & Analytics Layer
13. Evaluation Layer
14. Observability Layer

---

# 6. Presentation Layer

The frontend should provide:

## Student Interface

- profile selection;
- learning mode selection;
- Tutor Chat;
- Homework Help;
- Learn Mode;
- Practice Mode;
- Mock Test Mode;
- English Voice Mode;
- progress view.

## Parent Interface

- child progress summary;
- subject-level progress;
- learning-independence indicators;
- weak concepts;
- trend summaries.

### Initial Technology

```text
React + Vite
```

The backend should remain fully testable without the frontend.

---

# 7. API Layer

Technology:

```text
FastAPI
```

Responsibilities:

- request validation;
- authentication checks;
- request IDs;
- service routing;
- error handling;
- structured responses.

Suggested endpoint groups:

```text
/api/v1/auth/
/api/v1/students/
/api/v1/sessions/
/api/v1/tutor/
/api/v1/practice/
/api/v1/mock-tests/
/api/v1/voice/
/api/v1/progress/
/api/v1/parents/
/api/v1/health/
```

---

# 8. Authentication and Profile Service

This service manages:

- parent identity;
- student profiles;
- parent-child relationship;
- age;
- grade;
- preferred language;
- age group;
- permissions.

Initial MVP approach:

```text
Parent account
+
Student profile
+
JWT-based authentication
```

A simplified development mode may be used before authentication is fully implemented.

---

# 9. Input Safety Layer

Every child-facing message should pass through an input safety layer.

Responsibilities:

- input type and length validation;
- safety-sensitive request detection;
- prompt injection detection;
- Tutor Policy bypass detection;
- unsupported tool request blocking;
- personal-data minimization.

Possible output:

```json
{
  "allowed": true,
  "safety_category": "normal_education",
  "policy_bypass_detected": false
}
```

Safety-sensitive requests should use a dedicated safety path rather than normal tutoring.

---

# 10. Intent + Subject Router

The router should determine both:

## Subject

```text
MATH
ENGLISH
SCIENCE
GENERAL
```

## Intent

```text
LEARN_CONCEPT
HOMEWORK_REQUEST
STUDENT_ATTEMPT
HINT_REQUEST
DIRECT_ANSWER_REQUEST
EXPLANATION_REQUEST
PRACTICE_REQUEST
MOCK_TEST_RESPONSE
CONFUSION
I_DONT_KNOW
POLICY_BYPASS
OFF_TOPIC
SAFETY_SENSITIVE
```

The initial implementation may combine deterministic rules with structured LLM classification.

---

# 11. Learning Session State Service

LearnFirst AI should maintain explicit learning state rather than relying only on conversation history.

Recommended state:

```json
{
  "session_id": "uuid",
  "student_id": "uuid",
  "mode": "homework_help",
  "subject": "math",
  "topic": "linear_equations",
  "current_problem": "3x + 5 = 20",
  "attempt_count": 2,
  "hint_level": 2,
  "direct_answer_requests": 1,
  "misconception": "inverse_operation",
  "skills_demonstrated": [
    "subtract_constant"
  ],
  "mastery_state": "learning",
  "last_tutor_action": "ASK_GUIDING_QUESTION"
}
```

This state should be persisted.

---

# 12. Tutor Policy Engine

This is the central component of LearnFirst AI.

Inputs:

```text
Student Profile
+
Current Message
+
Mode
+
Subject
+
Intent
+
Session State
+
Attempt Evaluation
+
Safety State
```

Output:

```json
{
  "next_action": "ASK_GUIDING_QUESTION",
  "hint_level": 2,
  "allow_final_answer": false,
  "requires_rag": false,
  "requires_math_validation": true,
  "requires_mastery_check": false,
  "response_style": "developing_learner"
}
```

Responsibilities:

- enforce attempt-first behavior;
- manage hint levels;
- control answer disclosure;
- escalate support gradually;
- apply age policy;
- apply mode policy;
- trigger mastery checks;
- route prerequisite gaps;
- enforce Mock Test restrictions;
- handle policy bypass attempts.

The LLM must not override this decision.

---

# 13. Subject Tutor Layer

The Tutor Policy Engine decides **what educational action is allowed**.

The Subject Tutor decides **how that action should be performed for the subject**.

## Math Tutor

Responsibilities:

- parse Math problems;
- analyze submitted steps;
- request deterministic validation;
- detect first meaningful error;
- create subject-specific hints;
- generate similar problems;
- generate mastery problems.

Tools:

```text
SymPy
Python
LLM
Tutor Policy
```

## English Tutor

Responsibilities:

- grammar guidance;
- vocabulary;
- writing feedback;
- reading activities;
- conversational English;
- voice interaction.

Principle:

```text
Guide Revision > Rewrite Entire Work
```

## Science Tutor

Responsibilities:

- conceptual explanation;
- cause and effect;
- predictions;
- Socratic questioning;
- grounded factual explanation;
- age adaptation.

## General Tutor

Responsibilities:

- guided educational support outside the three specialized subjects;
- age adaptation;
- trusted retrieval where appropriate;
- transparent limits of specialization.

---

# 14. Math Validation Service

Math should not depend only on LLM reasoning.

Initial tools:

```text
SymPy
+
Python
```

Potential V1 validation:

- arithmetic;
- fractions;
- percentages;
- simple equations;
- algebraic equivalence;
- generated practice answers.

Flow:

```text
Student Answer
↓
Math Parser
↓
SymPy/Python Validation
↓
Correct / Incorrect / Equivalent
↓
Tutor Engine
```

---

# 15. LLM Gateway

All LLM requests should pass through one interface.

Conceptually:

```python
llm_gateway.generate(
    task="guided_tutor_response",
    messages=messages,
    schema=TutorResponse
)
```

The gateway may later support:

```text
Local Ollama Model
Hosted API Model
Fine-Tuned Model
Fallback Model
```

Responsibilities:

- provider selection;
- model configuration;
- structured output;
- timeout;
- retry policy;
- token accounting;
- logging;
- fallback behavior.

This prevents the application from becoming tied to one provider.

---

# 16. RAG Architecture

RAG will provide trusted educational grounding.

It has two separate pipelines.

## Knowledge Ingestion

```text
Approved Learning Material
↓
Parser
↓
Cleaning
↓
Metadata
↓
Chunking
↓
Embeddings
↓
Vector Store
```

Metadata should include:

```text
subject
topic
age_group
grade
curriculum_context
source
document_version
chapter
```

## Query Pipeline

```text
Student Question
↓
Query Processor
↓
Metadata Filter
↓
Vector Search
↓
Top Relevant Chunks
↓
Context Builder
↓
Tutor Response Generator
```

RAG must not bypass Tutor Policy.

Correct:

```text
Tutor Policy
↓
requires_rag = true
↓
RAG
↓
LLM
```

---

# 17. Bangladesh-Aligned Curriculum Architecture

Bangladesh alignment should primarily exist inside the knowledge layer, not inside the core Tutor Policy.

Recommended structure:

```text
knowledge/
├── bangladesh/
│   ├── math/
│   ├── english/
│   └── science/
```

Future expansion:

```text
knowledge/
├── bangladesh/
├── international/
└── other_curriculum/
```

Conceptually:

```text
Tutor Policy
+
Subject Tutor
+
Curriculum Package
=
Tutor Response
```

This keeps the system reusable outside Bangladesh.

---

# 18. Voice Service Architecture

English Voice Mode should be modular.

```text
Student Voice
↓
Speech-to-Text Adapter
↓
Transcript
↓
English Tutor
↓
Guided Feedback
↓
Text-to-Speech Adapter
↓
Spoken Tutor Response
```

Initial STT options:

```text
Whisper
faster-whisper
```

TTS should be behind an adapter so it can be replaced later.

Raw student audio should not be stored by default.

---

# 19. Progress & Mastery Service

This service converts learning interactions into progress information.

Track:

```text
Attempts
Independent Attempts
Correct Attempts
Hints Used
Maximum Hint Level
Direct Answer Requests
Misconceptions
Follow-Up Success
Mastery State
```

Example:

```json
{
  "student_id": "student_001",
  "subject": "math",
  "topic": "linear_equations",
  "attempts": 8,
  "independent_correct": 4,
  "average_hint_level": 1.8,
  "follow_up_success_rate": 0.75,
  "mastery_state": "developing"
}
```

---

# 20. Parent Dashboard Architecture

Flow:

```text
Learning Events
↓
Progress Service
↓
Aggregated Metrics
↓
Parent API
↓
Parent Dashboard
```

Possible dashboard cards:

- Math Progress
- English Progress
- Science Progress
- Independent Attempt Rate
- Average Hint Level
- Recent Weak Concepts
- Learning Trend

Full conversation transcripts should not be shown by default.

---

# 21. Persistence Layer

The system will use two main stores.

## Application Database

Development:

```text
SQLite
```

Production target:

```text
PostgreSQL
```

Stores:

- accounts;
- student profiles;
- learning sessions;
- attempts;
- mastery;
- tutor decisions;
- mock-test results;
- progress metrics;
- knowledge metadata.

Use:

```text
SQLAlchemy
+
Alembic
```

## Vector Store

Initial:

```text
Chroma
```

Stores:

- educational chunks;
- embeddings;
- metadata.

A future move to PostgreSQL + pgvector may be considered.

---

# 22. Caching Layer

Initial MVP:

```text
In-Memory Cache
```

Future:

```text
Redis
```

Good cache candidates:

- repeated retrieval results;
- embeddings;
- static learning content;
- repeated non-personal classifications.

Personalized tutor responses should be cached carefully because learning state changes.

---

# 23. Output Policy & Safety Validator

LLM output should never go directly to the child.

The validator should check:

- age appropriateness;
- tutor action compliance;
- hint-level compliance;
- answer disclosure;
- safety;
- mode restrictions;
- grounding requirements;
- output schema.

Example:

Tutor Decision:

```json
{
  "next_action": "GIVE_HINT",
  "allow_final_answer": false
}
```

If the generated response includes the final answer:

```text
Violation Detected
↓
Regenerate / Replace Response
```

This is a major protection for the project's central contribution.

---

# 24. Evaluation Architecture

Evaluation is a first-class subsystem.

```text
Evaluation Dataset
↓
Evaluation Runner
↓
LearnFirst Backend
↓
Responses + Tutor Decisions
↓
Metric Calculators
↓
Evaluation Report
```

Evaluation categories:

- Tutor Policy Compliance
- Answer Disclosure
- Age Adaptation
- Misconception Feedback
- Math Correctness
- Science Grounding
- English Teaching Behavior
- Safety
- Prompt Bypass
- Latency
- Token Usage
- Error Rate

---

# 25. Observability Architecture

Each request should have a unique:

```text
request_id
```

Structured logs should capture:

```text
request_id
student_id or anonymized ID
mode
subject
intent
tutor_action
hint_level
rag_used
math_validator_used
model
latency
status
error
```

Avoid unnecessary child-sensitive data in logs.

---

# 26. End-to-End Request Flow

```text
Child
↓
React Frontend
↓
FastAPI
↓
Input Safety
↓
Subject + Intent Router
↓
Load Student Profile
↓
Load Learning Session State
↓
Tutor Policy Engine
↓
Subject Tutor
↓
RAG / Math Validator / Voice Tool if needed
↓
LLM Gateway
↓
Output Policy Validator
↓
Progress / Mastery Update
↓
Database Save
↓
Frontend Response
↓
Child
```

---

# 27. Development Environment Architecture

The development workflow should separate product engineering from GPU work.

```text
VS Code / Local PC
      ↓
GitHub
      ↓
Google Colab
      ↓
Model / Evaluation Artifacts
      ↓
Google Drive / Download
      ↓
VS Code Integration
```

---

# 28. Local PC Responsibilities

The local PC should handle:

```text
FastAPI
React frontend
SQLite
Tutor Policy Engine
Subject Tutor logic
SymPy Math validation
RAG orchestration
Small embeddings
Chroma
Evaluation code
Tests
Git/GitHub
Documentation
Basic local inference when practical
```

---

# 29. Google Colab Responsibilities

Use Colab for GPU-heavy work only when useful:

```text
LoRA/QLoRA experiments
Fine-tuning
Model comparison
Large batch evaluation
Speech model experiments
Classifier experiments
Embedding/model benchmarks
```

Colab should produce reusable artifacts such as:

```text
adapter_model.safetensors
evaluation_results.json
trained_classifier/
benchmark.csv
```

---

# 30. What Must Not Depend on Colab

Do not use Colab as the production host for:

```text
FastAPI
Database
Authentication
Tutor Session State
Parent Dashboard
Persistent RAG Service
Production API Requests
```

---

# 31. Local Development Deployment

During development:

```text
React Frontend
localhost:5173

FastAPI
localhost:8000

SQLite
Chroma
Local Knowledge Files

Optional:
Ollama or Hosted LLM
```

This is sufficient for most feature development.

---

# 32. Recruiter Demo Deployment

Future target:

```text
Browser
↓
Hosted React Frontend
↓
FastAPI Backend
├── PostgreSQL
├── Vector Store
├── LLM Provider / Model Service
└── Logs & Metrics
```

Exact hosting providers should be selected later after benchmarking cost and resource needs.

---

# 33. Architectural Style

The MVP should use a:

# **Modular Monolith**

Meaning:

```text
One Backend Application
+
Clearly Separated Internal Modules
```

Not:

```text
Many Independent Microservices
```

Reasons:

- easier for one developer;
- lower RAM usage;
- easier debugging;
- better fit for the current PC;
- still professional;
- can later split modules into services if necessary.

---

# 34. Suggested Backend Structure

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── dependencies.py
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── students.py
│   │       ├── tutor.py
│   │       ├── sessions.py
│   │       ├── practice.py
│   │       ├── voice.py
│   │       ├── progress.py
│   │       └── health.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logging.py
│   │
│   ├── tutor/
│   │   ├── policy_engine.py
│   │   ├── decision_models.py
│   │   ├── hint_ladder.py
│   │   ├── mastery.py
│   │   └── session_state.py
│   │
│   ├── subjects/
│   │   ├── math/
│   │   ├── english/
│   │   ├── science/
│   │   └── general/
│   │
│   ├── llm/
│   │   ├── gateway.py
│   │   ├── providers/
│   │   └── schemas.py
│   │
│   ├── rag/
│   │   ├── ingestion.py
│   │   ├── retrieval.py
│   │   ├── embeddings.py
│   │   └── vector_store.py
│   │
│   ├── voice/
│   │   ├── stt.py
│   │   └── tts.py
│   │
│   ├── safety/
│   │   ├── input_guard.py
│   │   ├── output_guard.py
│   │   └── tutor_policy_guard.py
│   │
│   ├── progress/
│   │   ├── service.py
│   │   └── independence.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   ├── session.py
│   │   ├── models/
│   │   └── repositories/
│   │
│   └── observability/
│       ├── logger.py
│       └── metrics.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── policy/
│
├── alembic/
├── requirements.txt
└── .env.example
```

---

# 35. Suggested Frontend Structure

```text
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   │   ├── StudentHome/
│   │   ├── TutorChat/
│   │   ├── Practice/
│   │   ├── MockTest/
│   │   ├── VoicePractice/
│   │   └── ParentDashboard/
│   ├── services/
│   │   └── api.js
│   ├── hooks/
│   ├── context/
│   └── utils/
├── package.json
└── vite.config.js
```

---

# 36. Suggested Evaluation Structure

```text
evaluation/
├── datasets/
│   ├── answer_resistance.jsonl
│   ├── age_adaptation.jsonl
│   ├── math_misconceptions.jsonl
│   ├── science_grounding.jsonl
│   ├── english_tutoring.jsonl
│   ├── policy_bypass.jsonl
│   └── safety_cases.jsonl
├── runners/
├── metrics/
├── reports/
└── README.md
```

---

# 37. Suggested Knowledge Structure

```text
knowledge/
├── bangladesh/
│   ├── math/
│   ├── english/
│   └── science/
├── processed/
└── metadata/
```

Raw curriculum material should remain separate from processed chunks.

---

# 38. Failure Handling

Model/external operations should include:

```text
Timeout
↓
Safe Retry Where Appropriate
↓
Fallback Provider if Configured
↓
Friendly Error
↓
Structured Log
```

The system should never fabricate an educational response because a retrieval or model service failed.

---

# 39. Configuration Management

Secrets and configurable values should use environment variables.

Example:

```text
DATABASE_URL=
LLM_PROVIDER=
LLM_MODEL=
LLM_API_KEY=
VECTOR_STORE_PATH=
STT_PROVIDER=
TTS_PROVIDER=
```

Actual `.env` files must remain excluded from Git.

---

# 40. Architectural Boundaries

The following must stay outside direct LLM control:

```text
Authentication
Authorization
Age Group Assignment
Mock Test Rules
Hint Limits
Final Answer Permission
Session State
Parent Permissions
Database Writes
Safety Overrides
Math Validation
```

The LLM can generate language within the decisions made by the application.

---

# 41. Initial Build Order

Recommended order:

```text
1. Backend Skeleton
2. Configuration
3. Student/Profile Models
4. Session State
5. Tutor Decision Models
6. Tutor Policy Engine
7. Basic LLM Gateway
8. Math Tutor + Validator
9. Evaluation Harness
10. English Tutor
11. Science Tutor
12. RAG
13. Safety Guards
14. Progress/Mastery
15. Voice
16. Parent Dashboard Backend
17. React Frontend
18. Full Integration Tests
19. Observability
20. Deployment
```

This order builds the unique Tutor Engine early.

---

# 42. Architecture Risks

## Risk A — Too Many Services Too Early

Mitigation:

Use a modular monolith.

## Risk B — LLM Controls Too Much

Mitigation:

Use structured Tutor Decisions and output validation.

## Risk C — Local Hardware Limit

Mitigation:

Keep model access replaceable and use Colab for heavy experiments.

## Risk D — RAG Becomes Curriculum-Locked

Mitigation:

Separate curriculum packages from the Tutor Engine.

## Risk E — Voice Delays the Core MVP

Mitigation:

Build text tutoring first and add Voice after the core Tutor Engine is stable.

---

# 43. Hardware Feasibility

This architecture is feasible on the current development PC because the main persistent components are lightweight:

```text
FastAPI
React Development Server
SQLite
Chroma
Small Embedding Model
SymPy
Python Services
```

Large model training is excluded from local development.

With 8 GB RAM, avoid running every heavy component simultaneously during development.

---

# 44. Architecture Success Criteria

The architecture is suitable when:

- [ ] Tutor Policy Engine is independent of the LLM provider;
- [ ] subject tutors are separate modules;
- [ ] student/session state is persistent;
- [ ] Math can use deterministic validation;
- [ ] RAG is curriculum-package based;
- [ ] child input/output pass through safety layers;
- [ ] answer disclosure can be validated after generation;
- [ ] Voice is optional and replaceable;
- [ ] SQLite can later migrate to PostgreSQL;
- [ ] local development does not require a strong GPU;
- [ ] Colab is used only for experiments/training;
- [ ] evaluation can call backend behavior automatically;
- [ ] logs can trace Tutor Policy decisions;
- [ ] frontend and backend communicate through defined APIs;
- [ ] deployment does not require architectural redesign.

---

# 45. Current Project Status

```text
Project Initiation              ✅
Product Requirements            ✅
User Stories & Use Cases        ✅
Tutor Policy Specification      ✅
System Architecture             ✅
Database / State Design         ⏳ NEXT
Data / RAG Strategy             ⬜
Evaluation Plan                 ⬜
Implementation                  ⬜
```

---

# 46. Next Step

The next document should be:

## `05_database_and_state_design.md`

It should define:

- parent accounts;
- student profiles;
- learning sessions;
- attempts;
- Tutor Decisions;
- hint events;
- misconceptions;
- mastery records;
- learning-independence metrics;
- mock tests;
- voice-session metadata;
- RAG source metadata;
- parent access relationships;
- what data should and should not be stored;
- retention/privacy considerations;
- SQLite development schema;
- PostgreSQL migration path.

The database should be designed around **learning state**, not merely chat-message storage.

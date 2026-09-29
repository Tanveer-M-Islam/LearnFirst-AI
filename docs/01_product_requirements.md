# LearnFirst AI — Product Requirements Specification

**Document ID:** LF-PRS-001  
**Version:** 1.0  
**Status:** Initial MVP Specification  
**Primary Users:** Children aged 7–14  
**Secondary Users:** Parents  
**Specialized Subjects:** Mathematics, English, Science  
**Additional Support:** General Guided Learning

---

# 1. Purpose

This document converts the LearnFirst AI concept into clear product requirements before implementation begins. It defines scope, user roles, functional requirements, non-functional requirements, priorities, acceptance criteria, and MVP release conditions.

---

# 2. Product Vision

LearnFirst AI is a guided AI learning system for children aged 7–14. Unlike answer-first generative AI systems, LearnFirst AI is designed to encourage independent thinking through student attempts, progressive hints, misconception-aware feedback, age-adaptive teaching, and mastery checks.

The system specializes in:

- Mathematics
- English
- Science

It also supports other educational topics through a general guided-learning mode.

> **Core principle:** Provide the minimum necessary assistance required for the learner to continue independently.

---

# 3. Product Goals

LearnFirst AI should:

1. encourage independent attempts before strong assistance;
2. reduce answer-first AI behavior;
3. provide progressive tutoring support;
4. identify misconceptions in student reasoning;
5. adapt teaching style for ages 7–14;
6. use different tutoring strategies for Math, English, and Science;
7. verify understanding through follow-up practice;
8. track learning independence and mastery indicators;
9. support English speaking practice through voice;
10. provide grounded educational explanations where factual accuracy matters;
11. apply child-focused safety guardrails;
12. provide parents with useful learning-progress summaries;
13. support systematic evaluation and observability.

---

# 4. Product Non-Goals

The MVP will not attempt to:

- replace teachers or schools;
- diagnose “AI addiction”;
- diagnose learning disabilities or mental-health conditions;
- support every curriculum or subject with equal depth;
- provide unrestricted web browsing to children;
- perform official academic grading;
- provide perfect pronunciation scoring;
- build a complete LMS;
- train a large language model from scratch;
- provide a teacher/institution administration platform in V1.

---

# 5. User Roles

## 5.1 Student

The student should be able to:

- use an age-appropriate profile;
- choose a learning mode;
- ask educational questions;
- submit homework questions;
- attempt answers;
- request hints;
- receive feedback;
- practice Math, English, and Science;
- use English voice practice;
- review progress.

## 5.2 Parent

The parent should be able to:

- manage a child profile where appropriate;
- view learning summaries;
- view subject progress;
- view learning-independence indicators;
- view repeated learning difficulties.

The parent dashboard should focus on learning progress rather than unnecessary surveillance of full child conversations.

## 5.3 Future Teacher Role

Teacher features are outside the MVP and may later include assignments, learning-material uploads, and aggregated progress analytics.

---

# 6. Age Groups

| Age | Internal Group | Default Teaching Style |
|---|---|---|
| 7–9 | Foundation Learner | Simple language, short steps, concrete examples |
| 10–12 | Developing Learner | Guided reasoning, moderate detail |
| 13–14 | Independent Learner | Fewer hints, deeper reasoning, greater independence |

Age should come from the configured profile rather than being inferred from writing style.

---

# 7. Main Product Modes

## 7.1 Learn Mode

```text
Topic
↓
Check Prior Knowledge
↓
Explain Concept
↓
Example
↓
Student Practice
↓
Feedback
↓
Mastery Check
```

## 7.2 Homework Help Mode

```text
Homework Question
↓
Request/Check Student Attempt
↓
Analyze Attempt
↓
Give Minimum Necessary Hint
↓
Student Retries
↓
Increase Assistance if Needed
↓
Verify Learning
```

## 7.3 Practice Mode

The system generates practice based on age, subject, topic, difficulty, and previous performance.

## 7.4 Mock Test Mode

During an active mock test:

- hints are disabled;
- complete solutions are disabled;
- feedback is provided after submission.

## 7.5 English Voice Practice

```text
Student Speaks
↓
Speech-to-Text
↓
Tutor Analysis
↓
Guided Feedback
↓
Text-to-Speech
↓
Student Tries Again
```

## 7.6 General Guided Learning

Supports other educational topics such as history, geography, computing basics, environment, and general knowledge using a less specialized tutoring workflow.

---

# 8. Requirement Priority System

- **MUST:** required for the MVP.
- **SHOULD:** important, but MVP can temporarily work without it.
- **COULD:** useful enhancement after the core works.
- **FUTURE:** intentionally deferred beyond V1.

---

# 9. Functional Requirements

## Student Profile and State

### FR-001 — Student Profile Creation — MUST
The system shall support at least student ID, age, age group, grade/learning level, and preferred language.

**Acceptance Criteria:** profile can be created, age is validated, age group is assigned automatically, and the profile can be loaded during learning sessions.

### FR-002 — Age Group Assignment — MUST
- 7–9 → Foundation Learner
- 10–12 → Developing Learner
- 13–14 → Independent Learner

### FR-003 — Learning History — MUST
The system shall store subjects, topics, attempts, hints, mastery checks, and session outcomes.

### FR-004 — Structured Session State — MUST
The system shall maintain session ID, student ID, subject, topic, mode, current task, hint level, attempts, misconceptions, demonstrated skills, and mastery status.

---

## Routing

### FR-005 — Subject Detection — MUST
Classify educational requests as Math, English, Science, or General. The student should be able to correct a wrong classification.

### FR-006 — Intent Detection — MUST
Identify at least: learn concept, homework help, student attempt, hint request, direct-answer request, explanation request, practice request, mock-test response, and general educational question.

### FR-007 — Mode Selection — MUST
The student can choose a mode manually. The system may recommend one.

---

## Tutor Policy Engine

### FR-008 — Attempt-First Policy — MUST
For problem-solving homework, the system shall normally encourage or request a student attempt before strong assistance.

### FR-009 — Answer Disclosure Control — MUST
The application shall explicitly decide whether to ask for an attempt, ask a guiding question, provide a hint, show an example, provide stronger guidance, or give a full explanation. This must not rely only on a system prompt.

### FR-010 — Progressive Hint Ladder — MUST

| Level | Tutor Behavior |
|---|---|
| 0 | Diagnose current understanding |
| 1 | Recall prerequisite concept |
| 2 | Ask guiding question |
| 3 | Give small hint |
| 4 | Show similar example |
| 5 | Break task into smaller steps |
| 6 | Give strong guidance |
| 7 | Full teaching explanation + independent follow-up |

### FR-011 — Hint-Level State — MUST
Current hint level must persist across the tutoring session.

### FR-012 — Minimum Necessary Assistance — MUST
The tutor shall prefer the lowest assistance level likely to help the learner continue.

### FR-013 — Similar-Example Teaching — MUST
The tutor shall be able to teach using a similar example instead of directly solving the student’s original task.

### FR-014 — Full Explanation Escalation — MUST
If the learner remains stuck after sufficient guided support, a full teaching explanation may be provided, followed by independent related practice where appropriate.

---

## Attempt Evaluation and Mastery

### FR-015 — Attempt Classification — MUST
Classify attempts as correct, partially correct, incorrect, or unclear/incomplete.

### FR-016 — Misconception Identification — MUST
Where possible, identify the likely reasoning or concept error rather than only marking an answer wrong.

### FR-017 — Positive Step Recognition — SHOULD
Recognize correct reasoning steps before addressing mistakes.

### FR-018 — Retry Support — MUST
Give the learner an opportunity to retry after feedback.

### FR-019 — Follow-Up Mastery Question — MUST
After significant teaching assistance, provide a related task to check independent application.

### FR-020 — Explain-It-Back — SHOULD
Support asking the student to explain a concept in their own words.

### FR-021 — Mastery State — MUST
Maintain simple concept states such as Not Started, Learning, Developing, and Strong.

### FR-022 — Mastery Update — MUST
Mastery should consider independent correctness, hint usage, follow-up success, retry success, and explain-it-back performance. One correct answer must not automatically imply full mastery.

---

# 10. Subject-Specific Requirements

## Mathematics

### FR-023 — Guided Math Workflow — MUST
Support step-by-step problem solving and guided reasoning.

### FR-024 — Deterministic Math Validation — MUST for supported problem types
Use code/symbolic validation where practical instead of trusting the LLM alone.

### FR-025 — Math Step Evaluation — MUST
Identify the first meaningful error in submitted reasoning where possible.

### FR-026 — Math Practice Generation — MUST
Generate age- and topic-appropriate related problems.

## English

### FR-027 — Grammar Tutoring — MUST
Guide students toward correcting grammar errors rather than always rewriting the sentence immediately.

### FR-028 — Vocabulary Learning — MUST
Support age-appropriate vocabulary explanation and practice.

### FR-029 — Writing Feedback — MUST
Provide focused feedback without unnecessarily replacing the student’s whole work.

### FR-030 — Reading Activities — SHOULD
Support short reading-comprehension activities.

### FR-031 — Spoken English Practice — MUST
Support basic conversational English practice through voice.

## Science

### FR-032 — Conceptual Science Tutoring — MUST
Emphasize cause and effect, observation, predictions, conceptual understanding, and age-appropriate explanation.

### FR-033 — Socratic Science Questions — SHOULD
Use guiding questions where appropriate.

### FR-034 — Grounded Science Explanations — MUST
Use approved knowledge resources when factual grounding is needed.

## General Learning

### FR-035 — General Topic Support — MUST
Support educational questions outside the three specialized subjects.

### FR-036 — Scope Transparency — MUST
Do not imply that General Learning has the same specialized validation as Math, English, and Science.

---

# 11. Voice Requirements

### FR-037 — Speech-to-Text — MUST
English Voice mode shall convert student speech into text.

### FR-038 — Text-to-Speech — MUST
Tutor responses can be spoken aloud.

### FR-039 — Transcript Review — SHOULD
Allow the student to see what the system understood from their speech.

### FR-040 — Text Fallback — MUST
Voice failure must not block the learning activity; text should remain available.

### FR-041 — Raw Audio Retention — MUST
Avoid retaining raw student audio unless technically necessary and explicitly configured.

---

# 12. RAG and Educational Knowledge Requirements

### FR-042 — Curated Knowledge Base — MUST
Maintain approved educational content for supported subjects.

### FR-043 — Retrieval — MUST
Retrieve relevant learning content when the tutoring task requires factual grounding.

### FR-044 — Source Metadata — MUST
Knowledge records should include subject, topic, age/grade suitability, source/origin, and version/date where relevant.

### FR-045 — Retrieval Traceability — SHOULD
Record which knowledge chunks influenced a grounded response.

### FR-046 — Knowledge Updates — SHOULD
Educational resources should be updateable without retraining the main LLM.

---

# 13. Learning Independence Requirements

### FR-047 — Independent Attempt Rate — MUST
Track how often a learner attempts before requesting strong assistance.

### FR-048 — Hint Usage — MUST
Track number of hints, highest hint level, and average assistance level.

### FR-049 — Direct-Answer Request Frequency — MUST
Track answer-seeking frequency as a learning-behavior indicator. It must not be presented as a psychological or medical diagnosis.

### FR-050 — Follow-Up Independent Success — MUST
Track whether a learner succeeds on related tasks after receiving help.

---

# 14. Parent Dashboard Requirements

### FR-051 — Parent Learning Summary — MUST
Show a summarized learning report.

### FR-052 — Subject Progress — MUST
Show progress separately for Math, English, and Science.

### FR-053 — Learning Independence Indicators — MUST
Show non-clinical indicators such as independent attempt rate, average hint level, follow-up success, and repeated difficulties.

### FR-054 — Privacy-Aware Reporting — MUST
Avoid unnecessary exposure of complete child conversations by default.

---

# 15. Safety Requirements

### FR-055 — Child-Safety Input Guardrail — MUST
Student input must pass through an age-appropriate safety layer.

### FR-056 — Child-Safety Output Guardrail — MUST
AI output must be checked against child-safety and tutor-policy requirements.

### FR-057 — Policy-Bypass Resistance — MUST
Test attempts such as:

- “ignore your rules”;
- pretending to be a teacher;
- asking for the answer in encoded form;
- requesting a “hint” that is actually the full answer.

### FR-058 — Restricted Tools — MUST
The child-facing AI must not receive unrestricted access to sensitive tools or external actions.

### FR-059 — Sensitive Situation Handling — MUST
Use age-sensitive escalation for serious safety situations instead of pretending to be a professional authority.

---

# 16. Evaluation and Observability Requirements

### FR-060 — Tutor Policy Evaluation Dataset — MUST
Create automated test cases for answer-seeking and tutoring-policy behavior.

### FR-061 — Age Adaptation Tests — MUST
Test the same concept at different target ages.

### FR-062 — Subject Behavior Tests — MUST
Maintain separate tests for Math, English, Science, and General mode.

### FR-063 — Safety Evaluation — MUST
Test prompt injection, answer-policy bypass, unsafe output, and sensitive-data handling.

### FR-064 — Grounding Evaluation — MUST
Evaluate grounded educational responses against approved knowledge content.

### FR-065 — Performance Evaluation — MUST
Measure response latency, error rate, token usage where available, and model failures.

### FR-066 — Request ID — MUST
Each backend request receives a unique request ID.

### FR-067 — Structured Logs — MUST
Create structured logs while avoiding unnecessary child personal data.

### FR-068 — Tutor Decision Logging — SHOULD
Record high-level tutor decisions such as subject, mode, hint level, tutor action, and policy result.

### FR-069 — Error Monitoring — MUST
Application errors must be distinguishable from normal tutor responses.

---

# 17. Non-Functional Requirements

### NFR-001 — Safety — MUST
Child-facing output must pass defined safety and tutoring-policy checks.

### NFR-002 — Privacy — MUST
Minimize collection and retention of personal child data.

### NFR-003 — Reliability — MUST
Normal tutoring interactions should not fail because an optional component such as voice is unavailable.

### NFR-004 — Response Time — SHOULD
Text tutoring should feel interactive. Initial target: typical response ideally under 10 seconds in the selected development/deployment environment. This may be revised after benchmarking.

### NFR-005 — Maintainability — MUST
Separate API, tutor policy, subject tutors, RAG, safety, database, voice, evaluation, and observability responsibilities.

### NFR-006 — Portability — MUST
Core application must not permanently depend on one LLM provider.

### NFR-007 — Testability — MUST
Core tutoring-policy decisions must be testable without manual UI interaction.

### NFR-008 — Explainability — SHOULD
Record high-level reasons for tutor-action selection.

### NFR-009 — Scalability — SHOULD
Allow future migration from SQLite to PostgreSQL, in-memory cache to Redis, and local inference to hosted/model-server inference.

### NFR-010 — Accessibility — SHOULD
Support readable text, simple navigation, clear feedback, keyboard-friendly use, and voice as an optional modality.

### NFR-011 — Security — MUST
Use input validation, authorization boundaries, secure secret handling, and restricted AI tool permissions.

### NFR-012 — Observability — MUST
Provide logs and basic performance metrics sufficient to diagnose failures.

### NFR-013 — Documentation — MUST
Keep requirements, architecture decisions, risks, evaluation results, and deployment steps synchronized with implementation.

---

# 18. MVP Priority Summary

## MUST HAVE

- student profile;
- age adaptation;
- Math tutor;
- English tutor;
- Science tutor;
- General Learning;
- Learn Mode;
- Homework Help;
- Practice Mode;
- basic Mock Test Mode;
- subject detection;
- intent detection;
- attempt-first policy;
- answer-disclosure control;
- progressive hint ladder;
- attempt evaluation;
- misconception feedback;
- similar-example teaching;
- mastery verification;
- structured session state;
- basic RAG;
- deterministic Math validation for supported tasks;
- English voice input/output;
- learning history;
- learning-independence metrics;
- parent summary;
- child-safety guardrails;
- automated evaluation;
- structured logging;
- basic observability.

## SHOULD HAVE

- explain-it-back activities;
- reading-comprehension mode;
- voice transcript review;
- retrieval traceability;
- richer parent analytics;
- accessibility improvements.

## COULD HAVE

- gamification;
- badges for independent solving;
- adaptive daily learning plan;
- visual learning aids;
- semantic caching;
- advanced pronunciation feedback;
- multilingual tutoring.

## FUTURE

- teacher dashboard;
- school accounts;
- classroom management;
- curriculum-specific packages;
- native mobile app;
- advanced adaptive-learning models;
- large-scale educational studies.

---

# 19. Initial MVP User Flow

```text
Student Profile
↓
Choose Mode
↓
Enter Question / Topic / Voice
↓
Safety Check
↓
Subject + Intent Detection
↓
Load Learning State
↓
Tutor Policy Decision
↓
Subject-Specific Tutor
↓
RAG / Validator if Needed
↓
LLM Generates Guided Response
↓
Output Guardrail
↓
Student Response
↓
Record Attempt / Hint / Progress
↓
Mastery Check
↓
Update Learning History
```

---

# 20. MVP Release Criteria

The MVP is not considered complete until the following are demonstrated.

## Tutor Behavior

- [ ] direct-answer requests are normally redirected into guided learning;
- [ ] hint levels progress correctly;
- [ ] multi-turn session state works;
- [ ] full explanation can occur after sufficient struggle;
- [ ] mastery follow-up can be triggered.

## Age Adaptation

- [ ] the same concept produces meaningfully different teaching styles for ages 8, 11, and 14.

## Mathematics

- [ ] supported math tasks can be validated independently of the LLM;
- [ ] basic misconception handling works.

## English

- [ ] grammar guidance works;
- [ ] writing feedback does not automatically rewrite everything;
- [ ] basic voice conversation works.

## Science

- [ ] science explanations can use grounded educational knowledge;
- [ ] conceptual questioning works.

## Safety

- [ ] prompt-bypass test cases exist;
- [ ] input/output safety checks are active;
- [ ] child-facing AI has no unrestricted tools.

## Progress

- [ ] attempts are stored;
- [ ] hint levels are stored;
- [ ] mastery is updated;
- [ ] learning-independence indicators can be calculated.

## Parent

- [ ] parent summary displays progress without requiring full conversation review.

## Engineering

- [ ] FastAPI backend runs;
- [ ] persistent database is connected;
- [ ] vector retrieval works;
- [ ] LLM provider is replaceable;
- [ ] logs are produced;
- [ ] automated evaluation runs;
- [ ] startup instructions are documented.

---

# 21. Assumptions

1. The MVP is a portfolio/research-oriented prototype rather than a production school platform.
2. The project begins with a limited curated educational knowledge base.
3. Existing foundation models will be used instead of training an LLM from scratch.
4. GPU-heavy experimentation will use Google Colab.
5. Core application development will occur locally in VS Code.
6. Educational-effect claims will not be made without appropriate learner studies.
7. SQLite may be used initially before later PostgreSQL migration.
8. Voice support will initially focus on practical English-learning activities.

---

# 22. Open Questions for Later Design

1. What exact Math topics will V1 support?
2. What exact Science topics will V1 support?
3. What English skill level should each age group start with?
4. Which educational materials will form the first RAG knowledge base?
5. What conditions allow the tutor to move to a full explanation?
6. How will mastery be calculated initially?
7. Which data should parents be allowed to see?
8. How long should learning history be retained?
9. Which LLM will be used for initial development?
10. Which STT/TTS stack will be used for the MVP?
11. What authentication approach will the prototype use?
12. Which frontend technology will be selected?
13. Which deployment environment will be used for the recruiter demo?

---

# 23. Requirements Change Policy

Major changes should be recorded in:

```text
docs/project_decisions.md
```

Changes affecting scope should also update:

```text
docs/project_risks.md
docs/progress_log.md
```

---

# 24. Current Project Status

```text
Project Initiation              ✅ Completed
Product Requirements            ✅ Defined
User Stories & Use Cases        ⏳ Next
Tutor Policy Specification      ⬜
System Architecture             ⬜
Database / State Design         ⬜
Data / RAG Strategy             ⬜
Evaluation Plan                 ⬜
Implementation                  ⬜
```

---

# 25. Next Step

The next planning step is **User Stories & Use Cases**.

It will convert requirements into concrete interactions such as:

> As a 10-year-old student, I want the tutor to give me a small hint when I am stuck so that I can continue solving the problem myself.

We will define flows for:

- Learn Mode;
- Homework Help;
- Practice Mode;
- Mock Test Mode;
- English Voice Practice;
- Parent Dashboard;
- direct-answer attempts;
- misconception correction;
- mastery verification;
- safety escalation.

After those user stories and use cases are clear, the **Tutor Policy Specification** can be designed precisely.

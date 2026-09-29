# LearnFirst AI — Project Decision Log

This document records important project decisions and the reasoning behind them.

---

## Decision 001 — Target Age

**Decision:**  
The primary target users will be children aged **7–14**.

**Reason:**  
This age range includes learners who are still developing foundational academic, reasoning, language, and independent problem-solving skills.

**Status:** Approved

---

## Decision 002 — Age Group Segmentation

**Decision:**  
The system will internally divide learners into three age groups:

- 7–9: Foundation Learner
- 10–12: Developing Learner
- 13–14: Independent Learner

**Reason:**  
A 7-year-old and a 14-year-old require different vocabulary, explanation depth, examples, and levels of assistance.

**Status:** Approved

---

## Decision 003 — Primary Subjects

**Decision:**  
The three specialized subjects will be:

- Mathematics
- English
- Science

**Reason:**  
These subjects represent three different tutoring needs:

- Mathematics: structured reasoning and step verification
- English: language, writing, speaking, and conversation
- Science: conceptual understanding and scientific reasoning

**Status:** Approved

---

## Decision 004 — General Learning Support

**Decision:**  
The system will provide general guided learning support for educational topics outside Math, English, and Science.

**Reason:**  
Children may ask questions about history, geography, computing, environment, and general knowledge. These topics should be supported without claiming the same degree of specialization.

**Status:** Approved

---

## Decision 005 — Core Product Philosophy

**Decision:**  
LearnFirst AI will follow an **attempt-before-answer** philosophy.

**Reason:**  
The core project problem is answer-first AI use. The system should encourage active learning and independent reasoning before providing strong assistance.

**Status:** Approved

---

## Decision 006 — Minimum Necessary Assistance

**Decision:**  
The tutor should provide the smallest amount of help needed for the learner to continue independently.

**Reason:**  
Too little support can frustrate the learner, while too much support can replace thinking.

**Status:** Approved

---

## Decision 007 — Progressive Scaffolding

**Decision:**  
The project will use a progressive hint ladder instead of a simple answer/no-answer rule.

**Reason:**  
A strict “never give answers” policy can also produce poor tutoring. Students sometimes need gradually stronger teaching support.

**Status:** Approved

---

## Decision 008 — Misconception-Aware Feedback

**Decision:**  
The system should identify where the student's reasoning failed rather than only judge the final answer.

**Reason:**  
Educational value comes from understanding the learner's mistake and selecting the next concept or hint accordingly.

**Status:** Approved

---

## Decision 009 — No Medical-Style AI Addiction Score

**Decision:**  
The system will not calculate or display an “AI addiction score.”

**Reason:**  
The project is not designed to make medical or psychological diagnoses.

Instead, the system will track observable **learning independence indicators**, such as:

- independent attempt rate
- hints required
- direct-answer request frequency
- follow-up mastery
- retry rate

**Status:** Approved

---

## Decision 010 — Parent as Secondary User

**Decision:**  
Parents will be treated as secondary users in the MVP.

**Reason:**  
Parents can benefit from progress summaries and learning-independence indicators, while the project remains primarily focused on the child learner.

**Status:** Approved

---

## Decision 011 — Teachers as Future Users

**Decision:**  
Teacher and institutional features will not be part of the initial MVP.

**Reason:**  
Including teachers, schools, classroom management, and institution-level analytics would make the initial scope too large.

**Status:** Approved

---

## Decision 012 — Voice Support

**Decision:**  
The MVP will include English voice practice.

**Reason:**  
Voice interaction adds genuine educational value for language learning and demonstrates multimodal AI engineering.

**Status:** Approved

---

## Decision 013 — Trusted Educational Grounding

**Decision:**  
The system should use trusted educational content and RAG where factual grounding is needed.

**Reason:**  
Incorrect educational explanations can teach wrong fundamentals. Grounding reduces unsupported generation and improves traceability.

**Status:** Approved

---

## Decision 014 — Deterministic Validation Where Possible

**Decision:**  
Important logic should not depend entirely on an LLM.

Examples include:

- math calculations
- allowed hint levels
- mock-test rules
- age-group selection
- session state
- mastery tracking
- parent permissions

**Reason:**  
Deterministic logic improves reliability and reduces hallucination risk.

**Status:** Approved

---

## Decision 015 — Local Development Strategy

**Decision:**  
The main application will be developed locally using VS Code and Python.

**Local responsibilities include:**

- FastAPI
- database
- tutor policy
- RAG
- frontend
- evaluation
- testing
- documentation

**Reason:**  
The current PC is sufficient for application engineering even though it is not suitable for modern large-model training.

**Status:** Approved

---

## Decision 016 — Google Colab GPU Strategy

**Decision:**  
Google Colab will be used for GPU-heavy experiments.

Potential tasks include:

- fine-tuning
- LoRA/QLoRA
- model comparison
- classifier training
- batch evaluation
- speech/model experiments

**Reason:**  
This allows GPU-heavy work without requiring new local hardware.

**Status:** Approved

---

## Decision 017 — No Production Dependency on Colab

**Decision:**  
The deployed application must not depend on a continuously running Colab notebook.

**Reason:**  
Colab is an experimentation environment, not a reliable production inference service.

**Status:** Approved

---

## Decision 018 — Replaceable LLM Provider

**Decision:**  
The application should use an LLM gateway or abstraction rather than hard-coding one model throughout the system.

**Reason:**  
This allows the project to switch between local models, hosted APIs, or future fine-tuned models without rewriting core business logic.

**Status:** Approved

---

## Decision 019 — MVP Scope Control

**Decision:**  
The first version will not attempt to support every subject, language, curriculum, or educational workflow.

**Reason:**  
A focused and well-evaluated MVP is more valuable than an incomplete large system.

**Status:** Approved

---

## Decision 020 — Documentation Alongside Development

**Decision:**  
Documentation will be updated throughout the project rather than written only after implementation.

**Reason:**  
This preserves architectural reasoning, requirements, risks, experiments, and results while they are still accurate.

**Status:** Approved

---

## Future Decision Template

Use this format for future project decisions:

```markdown
## Decision XXX — Decision Name

**Decision:**

[What was decided]

**Reason:**

[Why this choice was made]

**Alternatives Considered:**

- Option A
- Option B

**Status:** Proposed / Approved / Rejected / Replaced
```

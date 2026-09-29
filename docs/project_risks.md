# LearnFirst AI — Project Risk Register

This document tracks important technical, educational, safety, privacy, and project-management risks.

Risk levels will be updated as the project develops.

---

## Risk Rating

### Impact

- **Low** — limited effect on the project
- **Medium** — noticeable effect but manageable
- **High** — could seriously damage educational quality, safety, reliability, or delivery

### Probability

- **Low** — unlikely
- **Medium** — possible
- **High** — likely without mitigation

---

# Initial Risk Register

| ID | Risk | Probability | Impact | Initial Mitigation | Status |
|---|---|---|---|---|---|
| R-001 | LLM gives direct answers too early | High | High | Tutor policy engine, answer-disclosure controller, output checks, policy evaluation dataset | Open |
| R-002 | LLM teaches incorrect information | Medium | High | RAG, trusted educational content, deterministic validation where possible, evaluation | Open |
| R-003 | Tutor provides age-inappropriate explanations | Medium | High | Age profiles, age-based prompts/policies, dedicated evaluation cases | Open |
| R-004 | Project scope becomes too large | High | High | Strict MVP, MoSCoW prioritization, defer teacher/institution features | Open |
| R-005 | Math reasoning contains hallucinated steps | Medium | High | Python-based validation, symbolic/math checks where practical | Open |
| R-006 | Student bypasses answer restrictions | High | Medium/High | Prompt-bypass test set, intent detection, policy engine, output validation | Open |
| R-007 | Misconception detection is inaccurate | Medium | High | Structured output, curated test cases, confidence thresholds, fallback tutoring behavior | Open |
| R-008 | Voice recognition performs poorly for children | Medium | Medium | Limit initial voice scope, evaluate multiple STT options, allow text fallback | Open |
| R-009 | Pronunciation feedback is unreliable | Medium | Medium | Avoid claiming expert pronunciation scoring in V1; keep feedback limited and transparent | Open |
| R-010 | Student becomes frustrated because tutor withholds too much help | Medium | High | Progressive hint ladder, escalation to stronger assistance, similar examples | Open |
| R-011 | System overhelps and weakens learning goal | Medium | High | Minimum-necessary-assistance policy, hint budgeting, mastery verification | Open |
| R-012 | Child privacy is not handled carefully | Medium | High | Minimize personal data, avoid unnecessary raw-audio storage, access controls | Open |
| R-013 | Parent dashboard exposes unnecessary conversation data | Low/Medium | High | Show learning summaries by default rather than full conversation surveillance | Open |
| R-014 | RAG knowledge contains poor or incorrect content | Medium | High | Curated sources, source metadata, document versioning, content review | Open |
| R-015 | General-learning mode exceeds reliable knowledge scope | Medium | Medium | Clearly separate specialized vs general tutoring; use grounding when appropriate | Open |
| R-016 | Local computer cannot run heavy models efficiently | High | Medium | Use lightweight local components, hosted inference when needed, Colab for GPU experiments | Mitigated |
| R-017 | Project becomes dependent on Colab availability | Medium | High | Use Colab only for experiments/training, save artifacts, keep production independent | Mitigated |
| R-018 | Free GPU sessions end during experiments | Medium | Medium | Save checkpoints to Drive, use resumable training, keep experiments small | Open |
| R-019 | Too many frameworks increase complexity | Medium | Medium | Use plain Python/FastAPI first; add frameworks only when justified | Open |
| R-020 | Evaluation only measures final-answer correctness | Medium | High | Include policy compliance, hint behavior, misconception handling, mastery, safety, latency | Open |
| R-021 | No real educational evidence supports learning-outcome claims | High | High | Avoid unsupported claims; report engineering evaluation separately from educational impact | Open |
| R-022 | Student gives intentionally misleading information about age/grade | Low/Medium | Medium | Parent-configured profile where appropriate; do not rely on model inference alone | Open |
| R-023 | Sensitive or unsafe child-facing content appears | Medium | High | Input/output safety layer, age-appropriate policies, restricted tool access | Open |
| R-024 | Prompt injection affects tutor behavior | Medium | High | Treat user input as untrusted, application-level policies, injection testing | Open |
| R-025 | Session memory becomes inconsistent | Medium | Medium | Explicit structured session state and database-backed learning state | Open |
| R-026 | Long conversation history increases latency/cost | Medium | Medium | Session summaries, state extraction, context management, caching | Open |
| R-027 | Generated practice questions are invalid or too difficult | Medium | Medium | Validation, difficulty rules, subject-specific checks, evaluation dataset | Open |
| R-028 | Frontend becomes too time-consuming | Medium | Medium | Build backend-first MVP; keep initial UI simple | Open |
| R-029 | Deployment costs become too high | Medium | Medium | Lightweight architecture, replaceable LLM provider, usage limits, caching | Open |
| R-030 | Project documentation falls behind implementation | Medium | Medium | Update docs after each major implementation step | Open |

---

# Highest-Priority Risks

The following risks currently require the most attention:

## R-001 — Direct Answer Leakage

### Why It Matters
This would undermine the core purpose of LearnFirst AI.

### Planned Controls

- intent classification
- answer-disclosure controller
- tutor policy engine
- progressive hint ladder
- output policy validation
- automated bypass tests

---

## R-002 — Incorrect Teaching

### Why It Matters
Incorrect foundational teaching may be more harmful than providing no answer.

### Planned Controls

- trusted educational knowledge base
- RAG
- math validation
- structured responses
- factual evaluation test sets
- source tracking where appropriate

---

## R-003 — Age-Inappropriate Teaching

### Why It Matters
The target range of 7–14 contains significantly different learning levels.

### Planned Controls

- explicit age groups
- age-adaptive vocabulary
- different explanation depth
- age-based test cases

---

## R-004 — Scope Expansion

### Why It Matters
Trying to build too many subjects, languages, dashboards, models, and platforms can prevent completion.

### Planned Controls

MVP focus:

- ages 7–14
- Math
- English
- Science
- general guided learning
- student + parent
- text tutoring
- basic English voice support

Other features will be postponed unless the MVP is stable.

---

## R-012 — Child Privacy

### Why It Matters
The system will be designed for children, so unnecessary data collection must be avoided.

### Planned Controls

- collect minimal profile data
- avoid storing raw audio unnecessarily
- avoid unnecessary location information
- separate parent and child permissions
- store progress summaries instead of excessive conversation history where possible

---

# Risk Update Template

For future updates:

```markdown
## Risk ID — Risk Name

**Description:**

[Describe the risk]

**Probability:** Low / Medium / High

**Impact:** Low / Medium / High

**Mitigation:**

- mitigation 1
- mitigation 2

**Owner:**

[Project component/person]

**Status:** Open / Monitoring / Mitigated / Closed

**Notes:**

[Additional information]
```

---

# Current Risk Status

This risk register represents the **project initiation stage**.

It will be reviewed after:

- product requirements
- tutor policy design
- architecture design
- first MVP implementation
- evaluation
- deployment

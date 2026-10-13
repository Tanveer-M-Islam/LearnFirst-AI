# LearnFirst AI — Preliminary recording guide

## Before you record

Open the deployed public site. Keep it at 100% zoom with a 1440×900 or wider window. Record at 1920×1080 if possible. Use the real application and your own narration; don't replace interactions with generated UI footage. Go to About → Clear this browser's learning data if you need a fresh recording. This deletes this browser's demo results; download your report first if needed.

The interface labels the default mode **Built-in lesson tutor**. With no connected Ollama endpoint, never say the demo is using live LLM generation or full curriculum RAG. Explain that this build proves the learning workflow and the model integration is optional. The competition's screenshot was unavailable in this session; verify its current video length, submission and prototype requirements yourself before submission. This outline targets 175 seconds with five seconds of spare time.

## A dependable real demo (fractions)

1. Open My learning → Mathematics. Use a demo nickname and age 10.
2. Diagnostic: answer `3/5`, `2/5`, and `3/9`. Only the first is correct. The app records **1 of 3** and chooses foundational practice. These deliberately entered wrong answers simulate a learner; they are not pilot research data.
3. Practice 1: `1/4 + 2/4`. Enter `3/8` to show the common-denominator mistake. Click **A little nudge**. The tutor explains the likely error. Try again with `3/4` and continue.
4. Practice 2: `1/2 + 1/4`. Ask for a hint or view learning cards. Answer `3/4`. Continue to the independent check.
5. Independent check: `2/7 + 3/7 = 5/7`; `1/3 + 1/2 = 5/6`; `1/3 + 1/6 = 1/2`. There are no hints.
6. The result shows **33% starting → 100% independent check** for this staged interaction. Say these are demonstration answers, not a measured gain from real participants. Never use this number as an efficacy claim.
7. Open My progress. Show lesson history, accuracy, hints and Download report. Open About to show working features and planned features.

You can record the full interaction, then trim waiting or repetitive questions. Preserve the order and do not imply that edited video timing measures response latency.

## Narration and visual plan — target 175 seconds

| Time | Show | Narration |
|---|---|---|
| 0:00–0:20 | You on camera, then homepage | “A student can copy a correct answer and still misunderstand the idea behind it. LearnFirst AI starts with a different question: can we help that student solve the next problem more independently? Our message is simple: think first, learn better.” |
| 0:20–0:40 | Homepage and three subject cards | “We are building an adaptive learning companion for children aged seven to fourteen. This preliminary version focuses on three small lessons: fractions, English subject–verb agreement, and the water cycle. The wider vision starts with Bangladesh’s English-version curriculum.” |
| 0:40–1:00 | Diagnostic and foundational-practice transition | “The learner begins with a short diagnostic. Their answers determine whether practice starts with the foundations or a more demanding example. Here I’m deliberately making a common fraction mistake to demonstrate the workflow. These are staged inputs, not results from a student trial.” |
| 1:00–1:30 | Wrong attempt, targeted hint, fraction bars, retry | “Instead of immediately giving away the answer, the lesson tutor offers a small nudge. The visual bars make the size of each part visible. A common-error rule flags adding denominators. The learner can try again, ask for progressively stronger hints, or eventually read a full explanation. Help remains available without pretending that a supported answer was independent.” |
| 1:30–1:55 | Independent check and results | “Next comes a fresh question without hints. This separates supported practice from independent performance. The report shows the starting check, the independent check, and the guidance used. These brief scores are useful feedback; they are not proof of lasting mastery. We plan to evaluate that with real learners.” |
| 1:55–2:20 | About: working features; simple architecture labels | “This deployment is a functional, rule-based tutoring demo. It includes a server-side Ollama adapter for age-appropriate hint wording, but no language model is connected in this recording. Grading and progression stay controlled by the lesson engine. Full curriculum retrieval and broader conversational tutoring are next-stage work.” |
| 2:20–2:40 | Progress report, concept review, library | “Learners and parents can see which ideas need another look. For this prototype, progress stays in the browser and can be exported. We collect no account details, and we keep the original learning project separate from this preliminary demo.” |
| 2:40–2:55 | You on camera; final brand screen | “Our next step is connecting and evaluating the language model, adding verified curriculum material, and testing whether students need less help on new problems. LearnFirst AI: think first, learn better.” |

Read aloud and trim to your actual speaking pace; timestamps are editorial targets, not a guaranteed audio duration. If you configure and verify a live model, change the 1:55 segment to accurately describe that tested integration and show the **AI-assisted hint** label.

## ChatGPT, Higgsfield and CapCut

- ChatGPT: rehearse narration, simplify wording, check each claim against the working app.
- Higgsfield: optional 3–5 second illustrative opening, not the demo. Prompt: “Natural documentary-style close-up of a fictional school learner's hands drawing equal parts of a circle in a notebook at a warm daylight study desk. A moment of curiosity and concentration. Slow, subtle camera movement, 16:9, no logos, no visible written words, no generated application interface.” Label illustrative footage if needed. No claim that the fictional scene is a real pilot.
- CapCut: place your own voice first, then the real screen recording. Use readable captions, gentle zooms on the answer and hint, simple cuts, and quiet royalty-cleared music. Avoid heavy transitions. End at approximately 2:55.

## Final live checklist

Run a fresh fraction lesson, open and close the profile dialog, test the menu on a phone-width window, reload after completing a lesson, and export a report. For a judge-facing Vercel deployment, verify that its production URL is accessible in a signed-out browser and does not require Vercel Authentication. If the competition requires a live generative-AI prototype, connect and test a model before presenting this build as satisfying that requirement.

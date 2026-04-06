# IRB Protocol — Study A: Controlled Experiment

> **Status:** Draft — revise institutional details before submission

## 1. Project title
Security Risks of Non-Expert Vibe Coding with Open-Weight Language Models: A Controlled Experiment

## 2. Principal investigator
[Your name, institution, email, phone]

## 3. Study overview
This study examines security vulnerabilities introduced when non-expert users build software
using AI-assisted "vibe coding" workflows. Participants complete a software development task
under one of three conditions: proprietary LLM via a commercial platform, open-weight model
via a local interface, or open-weight model via command-line only. Sessions are recorded and
resulting code audited for security vulnerabilities.

## 4. Participant population

**Target N:** 60 participants (20 per condition)

**Inclusion criteria:**
- Age 18 or older
- Self-reported programming expertise of 1 or 2 on a 5-point scale
- Unable to identify a SQL injection vulnerability in a 10-line screening snippet
- Has used an AI tool (ChatGPT, Claude, Copilot, etc.) to help write code at least once

**Exclusion criteria:**
- CS/software engineering degree or current enrollment
- Professional programming experience (current or past)
- Prior participation in security research studies

**Recruitment:** Prolific.com with demographic filters. Secondary: Lovable/Bolt user communities.

## 5. Study procedure

**Session duration:** ~90 minutes

| Phase | Duration | Description |
|-------|----------|-------------|
| Screening | 10 min | Expertise question + SQL injection identification task |
| Consent & orientation | 10 min | Informed consent, screen recording explained |
| Task | 60 min | Build user auth system (register, login, password reset) |
| Post-task survey | 10 min | Perceived security, trust, deployment intentions |
| Debrief | 5 min | Security focus revealed, educational resource provided |

**Conditions (block randomized):**
- **A:** Proprietary model with platform (Lovable / GPT-4)
- **B:** Open-weight model with UI (Ollama + Open WebUI, Llama 3.3 70B)
- **C:** Open-weight model raw (command-line Ollama, Llama 3.3 70B)

**Task prompt (all conditions):**
> "Build a simple web application where users can register with a username and password,
> log in, and see a personalized welcome page. The app should remember who is logged in
> between visits."

## 6. Data collected

| Data type | Method | Identifiable? |
|-----------|--------|---------------|
| Screen recording + audio | Automated capture | No (pseudonymized) |
| Generated code | Exported from session | No |
| Think-aloud transcript | Audio transcription | No |
| Post-task survey | Qualtrics | No |
| Prolific participant ID | Platform metadata | Pseudonymized |

## 7. Risks, benefits, compensation

- **Risks:** Minimal. Mild frustration possible. No sensitive personal data collected.
- **Benefits:** Security education resource provided. Contributes to public AI safety knowledge.
- **Compensation:** $18 USD via Prolific (~$12/hr for 90-min session)

## 8. Data storage

- Screen recordings: encrypted institutional server, research team access only
- Code files: private GitHub repository, no participant identifiers in filenames
- Survey data: Qualtrics with institutional license
- Retention: 5 years post-publication, then securely deleted

## 9. Vulnerability disclosure plan

- No participant-generated code will be deployed to the internet
- All code retained in a private repository
- Debrief note advises participants not to deploy study code without security review

## 10. Statistical power

Primary outcome: vulnerability density (issues per 1,000 LOC). Based on Veracode (2025)
estimates (~45% vuln rate), assuming 20% absolute difference between conditions, N=20 per
condition provides 80% power at α=0.05 (one-tailed). Analysis: one-way ANOVA with Tukey
post-hoc correction.

## 11. IRB classification for Study B

Study B (repository audit) qualifies as **exempt** under 45 CFR 46.104(d)(4)
(secondary research on publicly available data) at most US institutions.
Confirm with your IRB office before proceeding.

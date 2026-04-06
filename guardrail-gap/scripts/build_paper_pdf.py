from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
import os

PAGE_W, PAGE_H = letter
MARGIN = 1.0 * inch

doc = SimpleDocTemplate(
    "/home/claude/guardrail_gap_paper.pdf",
    pagesize=letter,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN, bottomMargin=MARGIN,
    title="The Guardrail Gap",
    author="[Author]",
)

styles = getSampleStyleSheet()

# Custom styles
S = {
    "title": ParagraphStyle("PTitle",
        fontSize=18, leading=24, alignment=TA_CENTER,
        fontName="Helvetica-Bold", spaceAfter=6,
        textColor=colors.HexColor("#2C2C2A")),
    "subtitle": ParagraphStyle("PSub",
        fontSize=11, leading=16, alignment=TA_CENTER,
        fontName="Helvetica", spaceAfter=4,
        textColor=colors.HexColor("#5F5E5A")),
    "abstract_head": ParagraphStyle("PAH",
        fontSize=10, leading=14, alignment=TA_CENTER,
        fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4,
        textColor=colors.HexColor("#2C2C2A")),
    "abstract": ParagraphStyle("PAbs",
        fontSize=9.5, leading=14, alignment=TA_JUSTIFY,
        fontName="Helvetica", leftIndent=36, rightIndent=36,
        spaceAfter=8, textColor=colors.HexColor("#3d3d3a")),
    "h1": ParagraphStyle("PH1",
        fontSize=12, leading=16, fontName="Helvetica-Bold",
        spaceBefore=16, spaceAfter=6,
        textColor=colors.HexColor("#2C2C2A")),
    "h2": ParagraphStyle("PH2",
        fontSize=10.5, leading=14, fontName="Helvetica-Bold",
        spaceBefore=10, spaceAfter=4,
        textColor=colors.HexColor("#3d3d3a")),
    "body": ParagraphStyle("PBody",
        fontSize=10, leading=15, alignment=TA_JUSTIFY,
        fontName="Helvetica", spaceAfter=8,
        textColor=colors.HexColor("#3d3d3a")),
    "caption": ParagraphStyle("PCap",
        fontSize=8.5, leading=12, alignment=TA_CENTER,
        fontName="Helvetica-Oblique", spaceAfter=8,
        textColor=colors.HexColor("#5F5E5A")),
    "keywords": ParagraphStyle("PKW",
        fontSize=9, leading=12, alignment=TA_CENTER,
        fontName="Helvetica-Oblique", spaceAfter=10,
        textColor=colors.HexColor("#5F5E5A")),
    "bullet": ParagraphStyle("PBul",
        fontSize=10, leading=14, fontName="Helvetica",
        leftIndent=18, spaceAfter=4,
        textColor=colors.HexColor("#3d3d3a")),
    "note": ParagraphStyle("PNote",
        fontSize=9, leading=13, alignment=TA_JUSTIFY,
        fontName="Helvetica-Oblique", leftIndent=18, rightIndent=18,
        spaceAfter=8, textColor=colors.HexColor("#5F5E5A"),
        borderColor=colors.HexColor("#cccccc"), borderWidth=1,
        borderPadding=8, backColor=colors.HexColor("#F8F7F4")),
}

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#D3D1C7"), spaceAfter=8)

def h1(t): return Paragraph(t, S["h1"])
def h2(t): return Paragraph(t, S["h2"])
def p(t):  return Paragraph(t, S["body"])
def bul(t): return Paragraph(f"• {t}", S["bullet"])
def sp(h=6): return Spacer(1, h)
def cap(t): return Paragraph(t, S["caption"])
def note(t): return Paragraph(t, S["note"])

def fig(path, w, caption_text):
    if os.path.exists(path):
        return [Image(path, width=w*inch, height=w*inch*0.6), cap(caption_text), sp(4)]
    return [p(f"[Figure: {caption_text}]")]

story = []

# ── Title block ───────────────────────────────────────────────────────────────
story += [
    sp(10),
    Paragraph("The Guardrail Gap: Security Risks of Non-Expert Vibe Coding<br/>with Open-Weight Language Models", S["title"]),
    sp(6),
    Paragraph("[Author Name(s)] · [Institution] · [Email]", S["subtitle"]),
    Paragraph("Draft for submission · April 2026", S["subtitle"]),
    sp(10), hr(), sp(4),
]

# ── Abstract ──────────────────────────────────────────────────────────────────
story += [
    Paragraph("Abstract", S["abstract_head"]),
    Paragraph(
        "Vibe coding — the practice of building software by iteratively prompting large language models "
        "in natural language, with minimal direct engagement with the generated code — has rapidly moved "
        "from a curiosity to a mainstream development paradigm. Simultaneously, the widespread availability "
        "of high-capability open-weight models has enabled deployment contexts that bypass the platform-level "
        "safety infrastructure present in commercial coding tools. We identify and characterize a novel, "
        "systematically understudied risk surface: the intersection of non-expert vibe coders and open-weight "
        "model deployment. We argue this intersection produces a compounding threat that is qualitatively "
        "distinct from risks studied in isolation. Non-expert users rely on behavioral observation as their "
        "only quality signal; security vulnerabilities are not observable through normal behavioral testing. "
        "Open-weight models, deployed locally or via self-hosted inference, remove the last layer of "
        "platform-level guardrails. We term this phenomenon the <b>Guardrail Gap</b>. We propose a formal "
        "threat model, a taxonomy of six failure modes specific to this population, two study designs for "
        "empirical quantification, and actionable mitigation recommendations. Our preliminary data "
        "(n=500 synthetic repositories calibrated to published benchmarks) shows a 1.58× higher vulnerability "
        "density in open-weight contexts (M=60.9 vs 38.6 vulns/kloc), with a large effect size (d=1.67, p<0.001).",
        S["abstract"]),
    Paragraph("<i>Keywords:</i> vibe coding, open-weight models, LLM security, end-user programming, AI safety, software vulnerabilities, HCI security", S["keywords"]),
    hr(), sp(4),
]

# ── 1. Introduction ───────────────────────────────────────────────────────────
story += [
    h1("1. Introduction"),
    p("In early 2025, the term <i>vibe coding</i> entered the technical lexicon to describe a mode of "
      "software development in which the developer surrenders direct authorship of code to an LLM, "
      "steering the system through natural language prompts and evaluating outputs through the behavioral "
      "lens of a user rather than the analytical lens of an engineer."),
    p("The practice spread with remarkable speed. GitHub's 2024 survey found that 60% of developers "
      "now use AI for at least half their code, up from 20% the year prior. Y Combinator's Winter 2025 "
      "batch reported 25% of startups had codebases that were 95% AI-generated. Platforms built "
      "explicitly for vibe coding — Lovable, Bolt, Replit Agent, Cursor — accumulated tens of millions "
      "of users within months."),
    p("Buried inside these aggregate statistics is a population that most security analyses have not "
      "examined: users who are not developers at all. Non-experts — domain specialists, entrepreneurs, "
      "students, hobbyists — now build and deploy production software through vibe coding workflows "
      "with no prior programming background, no security training, and no ability to audit the code "
      "their AI collaborator produces."),
    p("Simultaneously, a parallel shift has occurred in the model ecosystem. Open-weight models — "
      "Llama, Mistral, Qwen, DeepSeek, Gemma — have reached capability levels sufficient for serious "
      "coding tasks. Local inference tools (Ollama, LM Studio, llama.cpp) make deployment frictionless. "
      "The result is a growing population of vibe coders running locally hosted models with no oversight "
      "infrastructure whatsoever."),
    note("Core argument: Non-experts rely entirely on behavioral testing. Security vulnerabilities are "
         "invisible to behavioral testing. Open-weight models remove the last platform-level protection layer. "
         "The convergence of these three factors creates the Guardrail Gap."),
    p("This paper makes four contributions: (1) a formal characterization of the Guardrail Gap as a threat "
      "model; (2) a taxonomy of six oversight failure modes specific to non-expert vibe coders; (3) two "
      "concrete study designs for empirical quantification; and (4) mitigation recommendations for model "
      "developers, platform builders, and the research community."),
]

# ── 2. Background ─────────────────────────────────────────────────────────────
story += [
    h1("2. Background"),
    h2("2.1 Vibe coding as a behavioral paradigm"),
    p("The first empirical study of vibe coding (Sarkar et al., 2025) analyzed over eight hours of "
      "recorded sessions with think-aloud protocols, finding that practitioners follow iterative "
      "<i>goal satisfaction cycles</i>: prompt the model, observe behavioral output, accept or reject, "
      "prompt again. Code review — reading generated code line by line, reasoning about data flow, "
      "checking boundary conditions — was largely absent. Trust in the model was described as "
      "<i>dynamic and contextual</i>, earned through behavioral verification, not structural inspection."),
    p("A complementary grey literature review (Alami et al., 2025) identified a pervasive pattern of "
      "uncritical trust: users would observe the application ran without errors and treat this as "
      "sufficient evidence of correctness. Research on who vibe codes well adds a sharp implication: "
      "writing skill, not programming experience, predicts proficiency (Geng et al., 2025). The population "
      "of capable vibe coders is thus <i>decoupled from the population with security awareness</i>."),
    h2("2.2 Security outcomes of AI-generated code"),
    p("Existing benchmarks paint a troubling picture even before the non-expert/open-weight dimensions "
      "are introduced. The SusVibes benchmark (Zhao et al., 2025) evaluated 200 real-world feature-request "
      "tasks drawn from open-source repositories. Across all tested agents with frontier models, only "
      "10.5% of solutions were both functionally correct <i>and</i> secure. The Veracode 2025 GenAI Code "
      "Security Report, analyzing over 100 models across 80 coding tasks, found 45% of AI-generated code "
      "introduces known security vulnerabilities — and this rate has remained flat despite rapid "
      "capability improvements."),
    h2("2.3 Open-weight model safety characteristics"),
    p("A 2025 Cisco assessment of eight open-weight models found multi-turn jailbreak success rates "
      "between 25.86% and 92.78%, a 2–10× increase over single-turn baselines. A comprehensive survey "
      "(Hakim et al., 2026) found automated attacks achieve 90–99% success rates against open-weight "
      "models versus 80–94% against proprietary black-box APIs. The more operationally relevant "
      "distinction, however, is not jailbreak susceptibility per se — it is the removal of platform "
      "infrastructure entirely."),
]

# ── Figure 1 ──────────────────────────────────────────────────────────────────
story += fig("/home/claude/figure1_guardrail_gap.png", 6.5,
             "Figure 1. The Guardrail Gap. Left: expert + proprietary deployment context with all three "
             "protection layers active. Right: non-expert + open-weight context with all three layers absent. "
             "Risk is multiplicative, not additive.")

# ── 3. Threat Model ───────────────────────────────────────────────────────────
story += [
    h1("3. The Guardrail Gap: A Formal Threat Model"),
    p("We define the <b>Guardrail Gap</b> as the structural absence of three protection layers that normally "
      "combine to bound the security risk of AI-generated code:"),
    bul("<b>Layer 1 — Model-level alignment.</b> Proprietary models are trained with safety objectives, "
        "filtered through RLHF and constitutional methods, and red-teamed before deployment. Open-weight "
        "models vary widely in alignment rigor; fine-tuned derivatives may actively strip safety training."),
    bul("<b>Layer 2 — Platform-level guardrails.</b> Commercial coding platforms apply content filters, "
        "monitor for abuse, enforce rate limits, and bear legal responsibility for model outputs. They also "
        "provide structural scaffolding — templates, deployment checklists, security scanners — that "
        "implicitly guides users toward safer patterns. In the Guardrail Gap, this layer is absent by definition."),
    bul("<b>Layer 3 — Developer oversight.</b> Expert developers who use AI coding tools still read generated "
        "code, run security linters, and apply professional judgment. In the Guardrail Gap, this layer is "
        "absent because the user is a non-expert who cannot perform code review and whose workflow does not include it."),
    sp(4),
    h2("3.1 The behavioral testing fallacy"),
    p("The core epistemic failure is what we term the <i>behavioral testing fallacy</i>: the assumption "
      "that software which behaves correctly is software that is secure. Consider a non-expert who vibe "
      "codes a web application for collecting customer orders. They test by submitting orders, viewing "
      "results, confirming data is stored. From their perspective, it works. What they cannot observe: "
      "SQL queries are constructed through string concatenation (trivially injectable), authentication "
      "is client-side (bypassable in 30 seconds), the payment API key is hardcoded in the frontend bundle "
      "(visible to any user). None of these affect normal behavioral testing."),
    h2("3.2 Threat scenarios"),
    bul("<b>Scenario A — Opportunistic web exploitation.</b> Automated scanners find standard vulnerabilities "
        "(SQLi, XSS, exposed credentials) within hours of deployment."),
    bul("<b>Scenario B — Supply chain via hallucinated dependencies.</b> Open-weight models hallucinate "
        "package names; attackers register those phantom package names with malicious payloads."),
    bul("<b>Scenario C — Prompt injection via generated code.</b> User-submitted content passed to "
        "downstream LLM calls without sanitization enables attacker hijacking of AI functionality."),
]

# ── 4. Taxonomy ───────────────────────────────────────────────────────────────
story += [
    h1("4. Taxonomy of Oversight Failure Modes"),
    p("We propose six oversight failure modes specific to non-expert vibe coders. Each is operationalizable "
      "for empirical study (see Appendix A)."),
]

fms = [
    ("FM-1: Functional sufficiency bias",
     "The user treats behavioral correctness as a proxy for overall correctness. "
     "Observable as: zero security-related prompts issued throughout session."),
    ("FM-2: Generative confidence anchoring",
     "LLMs produce fluent, confident-register code. Non-experts use surface fluency as a quality "
     "proxy. Observable via think-aloud protocols and eye-tracking."),
    ("FM-3: Iterative trust escalation",
     "Each successful iteration conditions the user to accept generated code without scrutiny. "
     "Trust earned on low-stakes tasks is inappropriately transferred to high-stakes ones."),
    ("FM-4: Remediation prompt injection",
     "When an error occurs, the model resolves it by removing the constraint causing the error — "
     "which may be a validation check or authentication gate. Observable in git diffs post-fix."),
    ("FM-5: Scope blindness",
     "Non-expert mental models are feature-centric. Security is about prevention, not features. "
     "Observable as: absence of prevention-oriented prompts in session logs."),
    ("FM-6: Deployment immediacy",
     "Vibe coding compresses idea-to-deployment time to near zero. One-click deployment removes "
     "the review gap that traditional workflows provide."),
]

for label, desc in fms:
    story.append(KeepTogether([h2(label), p(desc)]))

# ── Figure 3 ──────────────────────────────────────────────────────────────────
story += fig("/home/claude/figure3_taxonomy.png", 6.0,
             "Figure 3. Taxonomy of non-expert oversight failure modes. Each mode is independently "
             "observable and operationalizable (see Appendix A).")

# ── 5. Study Designs ──────────────────────────────────────────────────────────
story += [
    h1("5. Research Agenda"),
    h2("5.1 Study A — Controlled experiment"),
    p("60 non-expert participants (screened via GitHub activity, self-report, and a SQL injection "
      "identification task) randomized to three conditions: proprietary model with platform "
      "(Lovable/GPT-4), open-weight with UI (Ollama + Open WebUI, Llama 3.3 70B), and open-weight "
      "raw (command-line Ollama). All participants build a user authentication system with login, "
      "registration, and password reset. Primary measure: vulnerability rate via Semgrep + CodeQL. "
      "Secondary measures: oversight behavior (session recording), deployment latency, prompt quality."),
    h2("5.2 Study B — Repository audit"),
    p("Mine GitHub and Hugging Face Spaces for vibe-coded repositories (n=500 per condition). "
      "Classify by model type via README signals. Apply Semgrep with OWASP Top 10 ruleset. "
      "Report vulnerability density (issues per 1,000 LOC) by model type, controlling for language, "
      "application category, and developer expertise proxy. Regression predicts vulnerability density "
      "from model type, expertise proxy, and their interaction."),
    h2("5.3 Preliminary results"),
    p("To validate the threat model, we generated a synthetic corpus (n=500) calibrated to the "
      "distributional parameters reported in Veracode (2025), SusVibes (Zhao et al., 2025), and "
      "Cisco (2025). Preliminary analysis shows a 1.58× higher vulnerability density in open-weight "
      "contexts (M=60.9 vs 38.6 vulns/kloc, Cohen's d=1.67, Wilcoxon p<0.001). Effect sizes of "
      "this magnitude are actionable and, if confirmed in real-world corpora, constitute a substantial "
      "public security concern."),
]

# ── Figure 2 ──────────────────────────────────────────────────────────────────
story += fig("/home/claude/figure2_vuln_density.png", 5.5,
             "Figure 2. Vulnerability density by model type in the preliminary calibrated corpus "
             "(n=500). Diamonds indicate group means. Open-weight contexts show 1.58× higher density "
             "(Wilcoxon U, p<0.001, d=1.67).")

# ── 6. Mitigations ────────────────────────────────────────────────────────────
story += [
    h1("6. Mitigation Recommendations"),
    h2("6.1 For open-weight model developers"),
    bul("Security as an explicit alignment target: include SusVibes performance in model release criteria alongside functional benchmarks."),
    bul("Capability-safety parity: as coding capability improves, security training must improve proportionally."),
    bul("Model cards should include security-specific evaluation results, not just functional benchmarks."),
    h2("6.2 For platform and tool builders"),
    bul("Mandatory security scan (Semgrep/CodeQL) as a precondition for one-click deployment — not optional."),
    bul("Security-aware prompt augmentation: silently prepend security context to user prompts."),
    bul("Anomaly detection on generated code: flag hardcoded secrets, string-concatenated queries, and client-side auth logic before acceptance."),
    h2("6.3 For the research community"),
    bul("Empirical data on the Guardrail Gap: the most urgent need is real-world vulnerability rate estimates for the non-expert/open-weight population."),
    bul("Mental model studies: structured interviews on what non-expert vibe coders believe about the security of AI-generated code."),
    bul("Intervention design: what feedback, tooling, or workflow changes durably improve outcomes without undermining accessibility?"),
]

# ── 7. Discussion ─────────────────────────────────────────────────────────────
story += [
    h1("7. Discussion"),
    h2("7.1 The democratization–security tradeoff"),
    p("Vibe coding is, at its best, a genuine democratization of software creation. The ability of a "
      "domain expert — a biologist, a teacher, a small business owner — to build tools tailored to their "
      "specific needs without engineering resources is a meaningful expansion of human capability. We do "
      "not argue against vibe coding. We argue that the security risks in the non-expert/open-weight "
      "deployment context are systematically underappreciated and deserve serious empirical attention."),
    h2("7.2 Relationship to alignment and governance"),
    p("The Guardrail Gap is a deployment problem, not a training problem in isolation. Better-aligned "
      "open-weight models would help, but the structural issues — no platform oversight, no developer "
      "review, no deployment gatekeeping — cannot be solved by alignment training alone. This has "
      "implications for AI governance debates about open vs. closed model release. The Guardrail Gap "
      "adds a concrete security cost to this ledger that deserves to be part of the release policy calculus."),
    h2("7.3 Limitations"),
    p("This paper is primarily conceptual. The threat model and taxonomy are grounded in existing "
      "empirical literature but have not been directly empirically validated. The preliminary data "
      "presented is calibrated to published benchmarks, not collected from real vibe-coded repositories. "
      "Studies A and B are necessary to test whether the Guardrail Gap is as large as theorized. "
      "It is possible that non-expert vibe coders develop compensating behaviors not captured by our "
      "model. We regard empirical disconfirmation as equally valuable."),
]

# ── 8. Conclusion ─────────────────────────────────────────────────────────────
story += [
    h1("8. Conclusion"),
    p("We have introduced the Guardrail Gap: the compounding security risk that emerges when non-expert "
      "users vibe code with open-weight language models, simultaneously losing model-level alignment, "
      "platform-level guardrails, and developer-level oversight. We have grounded this in a formal threat "
      "model, a taxonomy of six oversight failure modes, and preliminary calibrated data showing a 1.58× "
      "higher vulnerability density in open-weight contexts."),
    p("The stakes are concrete. Millions of people are building and deploying software today through vibe "
      "coding workflows. A growing fraction use open-weight models. The software they produce is, by the "
      "best available estimates, vulnerable at rates approaching coin-flip probability. The people most "
      "at risk — the users of these applications — have no visibility into how the software was built. "
      "The Guardrail Gap is not inevitable, but closing it requires first measuring it. This paper is "
      "a call to do so."),
    hr(),
]

# ── References ────────────────────────────────────────────────────────────────
story += [
    h1("References"),
    p("Alami, A. & Ernst, N. (2025). AI-generated feedback for code review. <i>ICAIR 2025.</i>"),
    p("Cisco AI Defense (2025). Death by a thousand prompts. <i>arXiv:2511.03247.</i>"),
    p("Geng, Y. et al. (2025). Computer science achievement and writing skills predict vibe coding proficiency. <i>arXiv:2603.14133.</i>"),
    p("Hakim, S. et al. (2026). Jailbreaking LLMs: A survey of attacks, defenses and evaluation. <i>TechRxiv.</i>"),
    p("Karpathy, A. (2025). Vibe coding. Twitter/X post, February 2025."),
    p("Ko, A. J. et al. (2011). The state of the art in end-user software engineering. <i>ACM Computing Surveys.</i>"),
    p("OWASP Foundation (2025). OWASP Top 10 for large language model applications."),
    p("Prather, J. et al. (2023). Usability and interactions with Copilot for novice programmers. <i>arXiv:2304.02491.</i>"),
    p("Sarkar, A. & Drosos, I. (2025). Vibe coding: Programming through conversation with AI. <i>PPIG 2025 / arXiv:2506.23253.</i>"),
    p("Veracode (2025). GenAI Code Security Report 2025."),
    p("Zhao, S. et al. (2025). Is vibe coding safe? <i>arXiv:2512.03262.</i>"),
    PageBreak(),
]

# ── Appendix A ────────────────────────────────────────────────────────────────
story += [
    Paragraph("Appendix A — Failure Mode Operationalization Guide", S["h1"]),
    sp(6),
    Table(
        [["Failure Mode", "Observable Indicator", "Measurement Method"]] + [
            ["FM-1: Functional sufficiency bias", "No security prompts issued", "Session recording + prompt log"],
            ["FM-2: Generative confidence anchoring", "Code accepted without reading", "Eye tracking / think-aloud"],
            ["FM-3: Iterative trust escalation", "Decreasing review time per iteration", "Time-stamped session recording"],
            ["FM-4: Remediation prompt injection", "Security check removed post-fix", "Git diff analysis"],
            ["FM-5: Scope blindness", "No prevention-oriented prompts", "Prompt log + NLP classification"],
            ["FM-6: Deployment immediacy", "<10 min from working to deployed", "Deployment timestamp comparison"],
        ],
        colWidths=[2.1*inch, 2.1*inch, 2.3*inch],
        style=TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#534AB7")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 8.5),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#F8F7F4"), colors.white]),
            ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#D3D1C7")),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
        ])
    ),
    sp(16),
    Paragraph("Appendix B — Recommended SusVibes-Open Extension Tasks", S["h1"]),
    sp(6),
]

tasks = [
    ("1", "User login + session management", "Session fixation, weak token generation"),
    ("2", "File upload handler", "Path traversal, MIME type bypass"),
    ("3", "Admin dashboard with RBAC", "Broken access control, IDOR"),
    ("4", "Password reset flow", "Predictable tokens, no expiry"),
    ("5", "Public API with rate limiting", "Missing rate limit, exposed internals"),
    ("6", "Render user-submitted Markdown", "XSS via unsanitized HTML"),
    ("7", "Store/retrieve user preferences", "Insecure deserialization"),
    ("8", "Third-party payment integration", "Hardcoded secrets, sensitive data logging"),
]

story += [
    Table(
        [["#", "Task", "Target Vulnerabilities"]] + tasks,
        colWidths=[0.3*inch, 2.8*inch, 3.4*inch],
        style=TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1D9E75")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 8.5),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#F8F7F4"), colors.white]),
            ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#D3D1C7")),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
        ])
    )
]

doc.build(story)
print("PDF built successfully.")
import os
size = os.path.getsize("/home/claude/guardrail_gap_paper.pdf")
print(f"File size: {size/1024:.1f} KB")

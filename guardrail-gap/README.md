# The Guardrail Gap
## Security Risks of Non-Expert Vibe Coding with Open-Weight Language Models

> **Draft paper — April 2026**
> Submitted for peer review. Do not cite without permission.

---

## Overview

This repository contains all materials for the paper **"The Guardrail Gap"** — the first
formal characterization of the compounding security risks that emerge when non-expert users
engage in vibe coding using open-weight language models.

We introduce the **Guardrail Gap**: the structural absence of three protection layers
(model-level alignment, platform-level guardrails, developer oversight) that simultaneously
fail in non-expert + open-weight deployment contexts.

---

## Repository structure

```
guardrail-gap/
├── paper/
│   └── guardrail_gap_paper.pdf        # Full formatted submission draft
├── figures/
│   ├── figure1_guardrail_gap.png      # Three-layer defense diagram
│   ├── figure2_vuln_density.png       # Vulnerability density boxplot
│   └── figure3_taxonomy.png           # Failure mode taxonomy
├── data/
│   └── aggregated_results.csv         # Preliminary corpus data (n=500, calibrated)
├── scripts/
│   ├── collect_corpus.py              # GitHub corpus collection (Study B)
│   ├── clone_corpus.sh                # Bulk clone repos from corpus.csv
│   ├── scan_corpus.sh                 # Semgrep vulnerability scanning
│   ├── aggregate_results.py           # Aggregate scan results to CSV
│   ├── generate_figures.py            # Reproduce all paper figures
│   ├── generate_synthetic_corpus.py   # Regenerate calibrated corpus data
│   ├── build_paper_pdf.py             # Rebuild paper PDF from source
│   └── analysis.R                     # Statistical analysis (R)
├── irb/
│   └── irb_protocol_study_a.md        # IRB protocol for controlled experiment
├── requirements.txt                   # Python dependencies
└── README.md
```

---

## Quickstart

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Reproduce figures
```bash
python scripts/generate_figures.py
# → figures/figure1_guardrail_gap.png
# → figures/figure2_vuln_density.png
# → figures/figure3_taxonomy.png
```

### 3. Run statistical analysis (R)
```r
# In R or RStudio:
source("scripts/analysis.R")
```
Required R packages: `tidyverse`, `coin`, `effsize`, `ggplot2`

### 4. Run Study B corpus collection (requires GitHub token)
```bash
# Add your token to scripts/collect_corpus.py (GITHUB_TOKEN variable)
python scripts/collect_corpus.py
bash scripts/clone_corpus.sh corpus.csv
bash scripts/scan_corpus.sh
python scripts/aggregate_results.py
```

### 5. Rebuild the paper PDF
```bash
python scripts/build_paper_pdf.py
# → paper/guardrail_gap_paper.pdf
```

---

## Key findings (preliminary)

| Metric | Open-weight | Proprietary | Effect |
|--------|-------------|-------------|--------|
| Mean vuln density | 60.9/kloc | 38.6/kloc | 1.58× higher |
| Cohen's d | — | — | 1.67 (large) |
| Wilcoxon p | — | — | < 0.001 |

> **Note:** Current data is a synthetic corpus calibrated to Veracode (2025), SusVibes
> (Zhao et al., 2025), and Cisco (2025) benchmark distributions. Replace with real mined
> data using `collect_corpus.py` before submission.

---

## Six oversight failure modes (taxonomy)

| ID | Name | Observable indicator |
|----|------|---------------------|
| FM-1 | Functional sufficiency bias | Zero security prompts issued |
| FM-2 | Generative confidence anchoring | Code accepted without reading |
| FM-3 | Iterative trust escalation | Decreasing review time per iteration |
| FM-4 | Remediation prompt injection | Security check removed in post-fix diff |
| FM-5 | Scope blindness | No prevention-oriented prompts |
| FM-6 | Deployment immediacy | <10 min from working state to deployment |

---

## Target submission venues

| Venue | Framing | Deadline |
|-------|---------|----------|
| CHI 2027 | HCI security / sociotechnical | ~Sep 2026 |
| USENIX Security 2027 | Empirical security measurement | Rolling |
| MSR 2027 | Repository mining + security | ~Jan 2027 |
| ICSE NIER 2027 | New ideas / early findings | ~Oct 2026 |

---

## Citation

```bibtex
@article{guardrailgap2026,
  title   = {The Guardrail Gap: Security Risks of Non-Expert Vibe Coding
             with Open-Weight Language Models},
  author  = {[Author]},
  year    = {2026},
  note    = {Manuscript under review}
}
```

---

## License

Code: MIT License
Paper and figures: All rights reserved (under review)

---

## Acknowledgments

This research builds on Sarkar et al. (2025), Zhao et al. (2025), Veracode (2025),
and Cisco AI Defense (2025). See paper references for full attribution.

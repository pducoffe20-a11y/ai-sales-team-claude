<p align="center">
  <img src="banner.svg" alt="AI Sales Team for Claude Code" width="100%">
</p>

<p align="center">
  <a href="#quick-start"><img src="https://img.shields.io/badge/install-one--liner-blue?style=for-the-badge" alt="Install"></a>
  <a href="#commands"><img src="https://img.shields.io/badge/14_skills-ready-8b5cf6?style=for-the-badge" alt="14 Skills"></a>
  <a href="#how-it-works"><img src="https://img.shields.io/badge/5_parallel-agents-22c55e?style=for-the-badge" alt="5 Agents"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-gray?style=for-the-badge" alt="MIT License"></a>
</p>

> **Your AI-powered sales team, running inside Claude Code.**
> Research any company, qualify leads with a weighted fit model, map the buying committee, generate personalized outreach, prepare for meetings, and produce professional PDF pipeline reports — all from the command line.

---

## What This Does

Type a command in Claude Code and get instant, actionable sales intelligence:

```
> /sales prospect https://acme.com

Launching 5 parallel agents...
  ✓ Company Research & Firmographics    — Fit Score: 82/100
  ✓ Decision Maker Identification       — 4 contacts found
  ✓ Opportunity Assessment (Fit Model)  — Score: 78/100
  ✓ Competitive Intelligence            — 3 competitors mapped
  ✓ Outreach Strategy & Messaging       — 5-email sequence ready

┌─────────────────────────────────────────────────┐
│  PROSPECT SCORE                                 │
│                                                 │
│  ██████████████████████████████████░░░░  85/100  │
│                                                 │
│  Grade: A  —  Strong Prospect                   │
│  Action: Invest significant effort              │
└─────────────────────────────────────────────────┘

Full analysis saved to PROSPECT-ANALYSIS.md
```

---

## Quick Start

### One-Command Install

```bash
curl -fsSL https://raw.githubusercontent.com/pducoffe20-a11y/ai-sales-team-claude/main/install.sh | bash
```

### Manual Install

```bash
git clone https://github.com/pducoffe20-a11y/ai-sales-team-claude.git
cd ai-sales-team-claude
./install.sh
```

### Optional: PDF Reports & Enhanced Parsing

```bash
pip install -r requirements.txt
```

<details>
<summary><strong>What the installer does</strong></summary>

```
╔══════════════════════════════════════════════════════════╗
║  AI Sales Team — Claude Code Skills                     ║
║  14 Skills · 5 Agents · 4 Scripts · PDF                 ║
╚══════════════════════════════════════════════════════════╝

Installing skills...
  ✓ sales (orchestrator)
  ✓ sales-prospect
  ✓ sales-research
  ✓ sales-qualify
  ✓ sales-contacts
  ✓ sales-outreach
  ✓ sales-followup
  ✓ sales-prep
  ✓ sales-proposal
  ✓ sales-objections
  ✓ sales-icp
  ✓ sales-competitors
  ✓ sales-report
  ✓ sales-report-pdf

Installing agents...
  ✓ sales-company
  ✓ sales-contacts
  ✓ sales-opportunity
  ✓ sales-competitive
  ✓ sales-strategy

Installing scripts...
  ✓ analyze_prospect.py
  ✓ lead_scorer.py
  ✓ contact_finder.py
  ✓ generate_pdf_report.py

Installing templates...
  ✓ outreach-cold.md
  ✓ outreach-warm.md
  ✓ outreach-referral.md
  ✓ meeting-prep.md
  ✓ proposal-template.md
  ✓ objection-playbook.md
```

</details>

---

## Commands

| Command | Description | Output |
|:--------|:------------|:-------|
| `/sales prospect <url>` | Full prospect audit — **5 parallel agents** | `PROSPECT-ANALYSIS.md` |
| `/sales quick <url>` | 60-second prospect snapshot | Terminal output |
| `/sales research <url>` | Company research & firmographics | `COMPANY-RESEARCH.md` |
| `/sales qualify <url>` | Weighted fit-model lead scoring | `LEAD-QUALIFICATION.md` |
| `/sales contacts <url>` | Decision maker identification | `DECISION-MAKERS.md` |
| `/sales outreach <prospect>` | Cold outreach email sequence | `OUTREACH-SEQUENCE.md` |
| `/sales followup <prospect>` | Follow-up email sequence | `FOLLOWUP-SEQUENCE.md` |
| `/sales prep <url>` | Meeting preparation brief | `MEETING-PREP.md` |
| `/sales proposal <client>` | Client proposal generator | `CLIENT-PROPOSAL.md` |
| `/sales objections <topic>` | Objection handling playbook | `OBJECTION-PLAYBOOK.md` |
| `/sales icp <description>` | Ideal Customer Profile builder | `IDEAL-CUSTOMER-PROFILE.md` |
| `/sales competitors <url>` | Competitive intelligence | `COMPETITIVE-INTEL.md` |
| `/sales report` | Pipeline report (Markdown) | `SALES-REPORT.md` |
| `/sales report-pdf` | Pipeline report (PDF) | `SALES-REPORT-*.pdf` |

---

## How It Works

### Architecture

The system uses a three-layer architecture — one orchestrator skill routes commands to 13 sub-skills, with the flagship `/sales prospect` command launching 5 specialized agents in parallel:

```
                         ┌──────────────────────────┐
                         │     /sales prospect       │
                         │      (Orchestrator)       │
                         └────────────┬─────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                  ▼
          ┌─────────────┐   ┌─────────────────┐   ┌──────────────┐
          │   PHASE 1    │   │     PHASE 2      │   │   PHASE 3    │
          │  Discovery   │   │ Parallel Analysis │   │  Synthesis   │
          └──────┬──────┘   └────────┬──────────┘   └──────┬───────┘
                 │                   │                      │
                 ▼                   ▼                      ▼
          ┌─────────────┐   ┌───────────────┐       ┌──────────────┐
          │ Fetch site   │   │ 5 agents run  │       │ Aggregate    │
          │ Extract data │   │ simultaneously│       │ Score (0-100)│
          │ Detect type  │   │               │       │ Action plan  │
          │ Run scripts  │   │               │       │ First email  │
          └─────────────┘   └───────┬───────┘       └──────────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                   │
        ┌────────────────┐  ┌──────────────┐  ┌───────────────┐
        │ ┌────────────┐ │  │ ┌──────────┐ │  │ ┌───────────┐ │
        │ │  Company   │ │  │ │ Contacts │ │  │ │Opportunity│ │
        │ │  Research  │ │  │ │  Finder  │ │  │ │  Scoring  │ │
        │ │            │ │  │ │          │ │  │ │           │ │
        │ │ Fit: 25%   │ │  │ │Access:20%│ │  │ │Quality:20%│ │
        │ └────────────┘ │  │ └──────────┘ │  │ └───────────┘ │
        └────────────────┘  └──────────────┘  └───────────────┘
        ┌────────────────┐  ┌──────────────┐
        │ ┌────────────┐ │  │ ┌──────────┐ │
        │ │Competitive │ │  │ │ Outreach │ │
        │ │  Analysis  │ │  │ │ Strategy │ │
        │ │            │ │  │ │          │ │
        │ │Position:15%│ │  │ │Ready: 20%│ │
        │ └────────────┘ │  │ └──────────┘ │
        └────────────────┘  └──────────────┘
```

### Cross-Skill Integration

Skills automatically detect and build on each other's output:

```
/sales prospect  ──►  PROSPECT-ANALYSIS.md
                            │
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                     ▼
/sales outreach      /sales prep           /sales proposal
 (uses contacts,     (uses all prior       (uses qualification,
  research data)      analysis data)        competitive intel)
       │                    │                     │
       ▼                    ▼                     ▼
  OUTREACH-              MEETING-              CLIENT-
  SEQUENCE.md            PREP.md               PROPOSAL.md
```

---

## Prospect Scoring

Every prospect gets a **weighted composite score (0-100)** calculated from 5 dimensions:

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   PROSPECT SCORE FORMULA                                            │
│                                                                     │
│   Company Fit ............ 25%   ████████████░░░░░░░░  Size,        │
│                                                        industry,    │
│                                                        growth       │
│                                                                     │
│   Contact Access ......... 20%   █████████░░░░░░░░░░░  Decision     │
│                                                        makers,      │
│                                                        warm paths   │
│                                                                     │
│   Opportunity Quality .... 20%   █████████░░░░░░░░░░░  Fit score,   │
│                                                        pain points  │
│                                                                     │
│   Competitive Position ... 15%   ███████░░░░░░░░░░░░░  Current      │
│                                                        solutions,   │
│                                                        switching    │
│                                                                     │
│   Outreach Readiness ..... 20%   █████████░░░░░░░░░░░  Channels,    │
│                                                        messaging,   │
│                                                        anchors      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Grade Interpretation

```
  Score    Grade    Action
 ───────────────────────────────────────────────────────────
  90-100    A+      🔥  Hot Lead — prioritize immediately
  75-89     A       ✅  Strong Prospect — invest significant effort
  60-74     B       📊  Qualified Lead — pursue with standard approach
  40-59     C       🔄  Lukewarm — nurture, don't hard sell
   0-39     D       ⏸️   Poor Fit — deprioritize or disqualify
```

### Qualification Framework

<details>
<summary><strong>Weighted Fit Model (0-100)</strong></summary>

Every signal is rated **0-3** (`0` not found · `1` weak · `2` clear · `3` strong).
Each category is normalized and weighted; the positive categories sum to 100 and
Negative Signals apply a penalty of up to 25.

| Category | Weight | Signals |
|----------|--------|---------|
| **Lead Fit** | 30 | Industry/segment/org-type match, inherent need for the solution category |
| **Buying Signals** | 30 | Category mentions, stated pain, active evaluation, related initiatives |
| **Tech Stack** | 15 | Incumbent solution, legacy/aging stack, adjacent systems, integration surface |
| **Timing & Intent** | 15 | Open RFPs, relevant hiring, funding/growth, launches, leadership change |
| **Engagement** | 10 | Site visits, content downloads, webinar attendance, replies, meetings booked |
| **Negative Signals** | −25 | Too small, wrong segment, no visible need, recent competitor purchase, bad geo fit |

```
Fit Score = Σ(weight × normalized)  −  25 × negative_normalized   (clamped 0-100)
```

Variable names are configurable per ICP — the `/sales qualify` skill ships a
worked example variable set for a learning-management / training vertical, and
`scripts/lead_scorer.py` computes the score deterministically from a ratings JSON.

</details>

---

## Examples

### Full Prospect Audit

```
> /sales prospect https://stripe.com

Phase 1: Discovering company information...
  ✓ Homepage fetched — SaaS / Fintech detected
  ✓ 6 subpages extracted (about, team, pricing, careers, blog, contact)
  ✓ analyze_prospect.py — 23 data points extracted

Phase 2: Running parallel analysis (5 agents)...
  ✓ Company Research      — Fit Score: 88/100
  ✓ Contact Discovery     — 6 decision makers found
  ✓ Opportunity Scoring   — Fit: 82/100
  ✓ Competitive Intel     — 4 competitors mapped
  ✓ Outreach Strategy     — 5-email sequence drafted

Phase 3: Synthesizing results...
  ✓ Prospect Score: 85/100 (Grade A)
  ✓ Top contact: [CTO] — strong technical champion signal
  ✓ Opening angle: recent Series D + engineering hiring surge

Output: PROSPECT-ANALYSIS.md
```

### Lead Qualification

```
> /sales qualify https://notion.so

Analyzing notion.so for lead qualification...

  Fit Score: 78/100 (Grade A)
  ┌──────────────────────────────────────────┐
  │ Lead Fit        (30) ████████████████░░ .82 │
  │ Buying Signals  (30) ██████████████░░░░ .71 │
  │ Tech Stack      (15) ████████████░░░░░░ .60 │
  │ Timing & Intent (15) ██████████████░░░░ .70 │
  │ Engagement      (10) ██████████░░░░░░░░ .50 │
  │ Negative Signals(−25) █░░░░░░░░░░░░░░░░░ .07 │
  └──────────────────────────────────────────┘

Action: Schedule discovery call — high-priority prospect.
Output: LEAD-QUALIFICATION.md
```

### Outreach Generation

```
> /sales outreach "Linear"

Generating outreach sequence for Linear...
  Type: Cold outreach (5-email sequence)
  Framework: Observation → Connection → Ask
  Personalized for: Engineering-focused B2B SaaS

  Email 1: "Quick question about [specific pain point]"    Day 1
  Email 2: "Saw your team's post about [trigger event]"    Day 3
  Email 3: "[Mutual connection] suggested I reach out"     Day 7
  Email 4: "3 ideas for [specific challenge]"              Day 14
  Email 5: "Should I close the file?"                      Day 21

Output: OUTREACH-SEQUENCE.md
```

### Meeting Prep

```
> /sales prep https://datadog.com

Generating meeting brief for datadog.com...
  ┌────────────────────────────────────────────┐
  │  MEETING PREP BRIEF                        │
  │                                            │
  │  Company:       Datadog                    │
  │  Attendees:     3 profiled                 │
  │  Talking Points: 7 prepared                │
  │  Discovery Qs:  10 ready                   │
  │  Objections:    5 with responses           │
  │  Cheat Sheet:   1 page                     │
  └────────────────────────────────────────────┘

Output: MEETING-PREP.md
```

---

## Project Structure

```
ai-sales-team-claude/
│
├── sales/SKILL.md                     ← Main orchestrator (routes all /sales commands)
│
├── skills/                            ← 13 sub-skills
│   ├── sales-prospect/SKILL.md           Full prospect audit (launches 5 agents)
│   ├── sales-research/SKILL.md           Company research & firmographics
│   ├── sales-qualify/SKILL.md            Lead qualification (weighted fit model)
│   ├── sales-contacts/SKILL.md           Decision maker identification
│   ├── sales-outreach/SKILL.md           Cold outreach email sequences
│   ├── sales-followup/SKILL.md           Follow-up email generation
│   ├── sales-prep/SKILL.md               Meeting preparation brief
│   ├── sales-proposal/SKILL.md           Client proposal generator
│   ├── sales-objections/SKILL.md         Objection handling playbook
│   ├── sales-icp/SKILL.md                Ideal Customer Profile builder
│   ├── sales-competitors/SKILL.md        Competitive intelligence
│   ├── sales-report/SKILL.md             Pipeline report (Markdown)
│   └── sales-report-pdf/SKILL.md         Pipeline report (PDF)
│
├── agents/                            ← 5 parallel subagents
│   ├── sales-company.md                  Company fit & firmographics (25%)
│   ├── sales-contacts.md                 Decision maker mapping (20%)
│   ├── sales-opportunity.md              Opportunity & fit scoring (20%)
│   ├── sales-competitive.md              Competitive positioning (15%)
│   └── sales-strategy.md                 Outreach strategy & messaging (20%)
│
├── scripts/                           ← Python utilities
│   ├── analyze_prospect.py               Website scraping & data extraction
│   ├── lead_scorer.py                    Weighted multi-category scoring engine
│   ├── contact_finder.py                 Team & leadership extraction
│   └── generate_pdf_report.py            ReportLab PDF generator
│
├── templates/                         ← Output templates
│   ├── outreach-cold.md                  5-email cold sequence
│   ├── outreach-warm.md                  3-email warm intro sequence
│   ├── outreach-referral.md              3-email referral sequence
│   ├── meeting-prep.md                   Meeting prep brief
│   ├── proposal-template.md              11-section client proposal
│   └── objection-playbook.md             15 universal objections
│
├── install.sh                         ← One-command installer
├── uninstall.sh                       ← Cleanup script
├── requirements.txt                   ← Python deps (reportlab, bs4, requests)
└── LICENSE                            ← MIT
```

---

## Use Cases

<table>
<tr>
<td width="33%">

### Founders & Solopreneurs

```bash
# Full prospect intelligence
/sales prospect https://target.com

# Ready-to-send email sequence
/sales outreach "Target Company"

# Prep before the call
/sales prep https://target.com
```

</td>
<td width="33%">

### Sales Teams

```bash
# Qualify inbound leads
/sales qualify https://lead.com

# Map the buying committee
/sales contacts https://lead.com

# Handle pricing objections
/sales objections "enterprise SaaS"
```

</td>
<td width="33%">

### Agency Owners

```bash
# Client proposal with pricing
/sales proposal "Client Name"

# Competitive positioning
/sales competitors https://client.com

# Define ideal customer
/sales icp "B2B SaaS, 50-200 emp"
```

</td>
</tr>
</table>

---

## Requirements

| Requirement | Status | Notes |
|:------------|:------:|:------|
| **Claude Code** | Required | [Install Claude Code](https://docs.anthropic.com/en/docs/claude-code) |
| **Python 3.8+** | Optional | For scripts and PDF generation |
| **reportlab** | Optional | `pip install reportlab` — PDF reports |
| **beautifulsoup4** | Optional | `pip install beautifulsoup4` — enhanced parsing |
| **requests** | Optional | `pip install requests` — fallback URL fetching |

---

## Uninstall

```bash
# From the repo directory
./uninstall.sh

# Or remotely
curl -fsSL https://raw.githubusercontent.com/pducoffe20-a11y/ai-sales-team-claude/main/uninstall.sh | bash
```

Removes all skills, agents, scripts, and templates from `~/.claude/`. Python packages are not removed.

---

<p align="center">
  <strong>MIT License</strong> · Copyright (c) 2026 Zubair Trabzada
  <br><br>
  <a href="https://github.com/pducoffe20-a11y/ai-sales-team-claude/issues">Report Bug</a> ·
  <a href="https://github.com/pducoffe20-a11y/ai-sales-team-claude/issues">Request Feature</a>
</p>

# CLAUDE.md

Guidance for AI assistants (Claude Code) working in this repository.

## What This Is

**AI Sales Team for Claude Code** — a distributable pack of Claude Code
**skills**, **subagents**, **Python scripts**, and **output templates** that turn
Claude Code into a sales-intelligence and outreach system. Users invoke it via
`/sales <command>` to research prospects, qualify leads (weighted fit model), map
buying committees, generate outreach, prep meetings, and produce PDF pipeline
reports.

This repo is **not an application you run**. It is a *content pack* that
`install.sh` copies into the user's `~/.claude/` directory. The "code" here is
primarily Markdown prompt files (`SKILL.md`, agent `.md` files) plus four Python
helper scripts. When you edit files here, you are editing prompts and installer
logic — there is no build step and no server.

## Repository Layout

```
ai-sales-team-claude/
├── sales/SKILL.md          # Main orchestrator — routes ALL /sales commands
├── skills/                 # 13 sub-skills, one dir each: skills/<name>/SKILL.md
│   ├── sales-prospect/     #   flagship: launches the 5 parallel agents
│   ├── sales-research/  sales-qualify/  sales-contacts/  sales-outreach/
│   ├── sales-followup/ sales-prep/      sales-proposal/  sales-objections/
│   └── sales-icp/      sales-competitors/ sales-report/  sales-report-pdf/
├── agents/                 # 5 parallel subagents (flat .md files)
│   ├── sales-company.md      # Company Fit          — 25% of Prospect Score
│   ├── sales-contacts.md     # Contact Access       — 20%
│   ├── sales-opportunity.md  # Opportunity Quality  — 20%
│   ├── sales-competitive.md  # Competitive Position — 15%
│   └── sales-strategy.md     # Outreach Readiness   — 20%
├── scripts/                # Python utilities (stdlib-first)
│   ├── analyze_prospect.py   # Website scrape → structured JSON
│   ├── lead_scorer.py        # Weighted multi-category (0-3) scoring engine
│   ├── contact_finder.py     # Team/leadership extraction
│   └── generate_pdf_report.py# ReportLab PDF pipeline report
├── templates/              # Output templates copied to the user's install
│   ├── outreach-cold.md  outreach-warm.md  outreach-referral.md
│   └── meeting-prep.md   proposal-template.md  objection-playbook.md
├── install.sh              # One-command installer (local or curl | bash)
├── uninstall.sh            # Removes installed files from ~/.claude/
├── requirements.txt        # Optional Python deps: reportlab, beautifulsoup4, requests
├── README.md               # User-facing docs (banner, examples, badges)
└── banner.svg              # README banner
```

## How It Works (Runtime Architecture)

Three layers, invoked by the user typing `/sales <command>` in Claude Code:

1. **Orchestrator** (`sales/SKILL.md`) — reads the command and routes to the
   matching sub-skill. Contains the canonical command table, the Prospect Score
   weights, grade bands, and business-context detection rules.
2. **Sub-skills** (`skills/<name>/SKILL.md`) — one per command. Each is a
   self-contained prompt with a defined process, scoring rules, and an exact
   output-file format. Many sub-skills double as the specialist body of a
   subagent (e.g. `sales-qualify` = the `sales-opportunity` agent's logic).
3. **Subagents** (`agents/*.md`) — only used by the flagship
   `/sales prospect <url>`. That skill runs **Phase 1 discovery** (fetch site,
   detect company type, run `analyze_prospect.py`), then launches **all 5
   subagents in parallel** via the Task tool (`subagent_type: "general-purpose"`),
   then **Phase 3 synthesis** aggregates their scores into one weighted
   Prospect Score and writes `PROSPECT-ANALYSIS.md`.

**Prospect Score (0–100)** = weighted average:
`Company Fit 25% + Contact Access 20% + Opportunity Quality 20% + Competitive Position 15% + Outreach Readiness 20%`.
Grades: A+ (90–100), A (75–89), B (60–74), C (40–59), D (0–39). These weights
and bands appear in **three** places — `sales/SKILL.md`,
`skills/sales-prospect/SKILL.md`, and `README.md`. Keep them in sync.

### Command → File map

| Command | Sub-skill | Output file |
|---|---|---|
| `/sales prospect <url>` | `skills/sales-prospect/` (+ 5 agents) | `PROSPECT-ANALYSIS.md` |
| `/sales quick <url>` | handled inline by `sales/SKILL.md` (no agents) | terminal only |
| `/sales research <url>` | `skills/sales-research/` | `COMPANY-RESEARCH.md` |
| `/sales qualify <url>` | `skills/sales-qualify/` | `LEAD-QUALIFICATION.md` |
| `/sales contacts <url>` | `skills/sales-contacts/` | `DECISION-MAKERS.md` |
| `/sales outreach <prospect>` | `skills/sales-outreach/` | `OUTREACH-SEQUENCE.md` |
| `/sales followup <prospect>` | `skills/sales-followup/` | `FOLLOWUP-SEQUENCE.md` |
| `/sales prep <url>` | `skills/sales-prep/` | `MEETING-PREP.md` |
| `/sales proposal <client>` | `skills/sales-proposal/` | `CLIENT-PROPOSAL.md` |
| `/sales objections <topic>` | `skills/sales-objections/` | `OBJECTION-PLAYBOOK.md` |
| `/sales icp <description>` | `skills/sales-icp/` | `IDEAL-CUSTOMER-PROFILE.md` |
| `/sales competitors <url>` | `skills/sales-competitors/` | `COMPETITIVE-INTEL.md` |
| `/sales report` | `skills/sales-report/` | `SALES-REPORT.md` |
| `/sales report-pdf` | `skills/sales-report-pdf/` | `SALES-REPORT-*.pdf` |

### Cross-skill integration

Skills read each other's output files from the working directory when present
(e.g. `/sales prospect` will reuse an existing `COMPANY-RESEARCH.md` instead of
re-running that agent; `/sales prep` and `/sales proposal` incorporate any prior
analysis). Preserve these "if `X.md` exists, use it" hooks when editing skills.

## Conventions

### Skill and agent files are prompts, not code
- **`SKILL.md` files start with a plain `# Title` heading — no YAML
  frontmatter.** (`sales-report-pdf` adds a `## Metadata` section; others do
  not.) Match the existing style of the file you edit; don't introduce
  frontmatter unless the whole set is being migrated.
- Each skill defines: when it's invoked, a step-by-step process, an explicit
  scoring rubric where relevant, and the **exact output-file structure** as a
  fenced ```markdown block. When changing what a skill produces, update that
  embedded template block too.
- Agents (`agents/*.md`) follow a `# Title` → `## Role` → `## Analysis Process`
  → `## Scoring` → `## Output Format` → `## Important Rules` shape.
- **Grounding rule** repeated across agents: use real fetched/searched data,
  never fabricate figures; cite sources; score honestly; label inference vs.
  fact. Keep this discipline in any new agent.

### Output files
- All generated deliverables go to the **current working directory** as
  UPPERCASE-HYPHENATED `.md` (or `.pdf`) files, and are git-ignored (see
  `.gitignore`). Do not commit sample generated reports.
- Every report starts with URL/client, date, and overall score.

### Python scripts
- **Standard-library first.** `analyze_prospect.py` and `contact_finder.py`
  parse HTML with `html.parser` from the stdlib so they run with zero installs;
  `beautifulsoup4`/`requests` are *optional* enhancements. Only
  `generate_pdf_report.py` hard-requires a third-party lib (`reportlab`).
- CLI shape: `argparse`, a `main()`, and an `if __name__ == "__main__":` guard.
  `--url` takes the target; `--output json` is the default machine format;
  `lead_scorer.py` reads a JSON file arg or stdin.
- Scripts must **degrade gracefully** — skills are written to continue (with a
  noted caveat) when a script is missing or fails. Preserve that: don't make a
  skill hard-depend on a script succeeding.
- At install time, scripts land in `~/.claude/skills/sales/scripts/` and
  templates in `~/.claude/skills/sales/templates/`.

## Common Tasks

**Add a new `/sales <cmd>` command:**
1. Create `skills/sales-<cmd>/SKILL.md` (follow an existing sub-skill's shape).
2. Add the row to the command table in `sales/SKILL.md` **and** `README.md`.
3. Add `sales-<cmd>` to the `SKILLS=( … )` array in `install.sh` (and the
   command-reference echo block) and to `uninstall.sh`.

**Add a Python script:** drop it in `scripts/` with the argparse/`main()`
convention. `install.sh` globs `scripts/*.py`, so no installer edit is needed;
add any new dependency to `requirements.txt` (keep it optional if possible).

**Change scoring weights or grade bands:** update all three copies
(`sales/SKILL.md`, `skills/sales-prospect/SKILL.md`, `README.md`) and, if the
Python scorer is affected, `scripts/lead_scorer.py`.

## Verifying Changes

There is no test suite or CI. Validate manually:

```bash
bash -n install.sh uninstall.sh                       # shell syntax
python3 -m py_compile scripts/*.py                    # Python compiles
python3 scripts/analyze_prospect.py --url https://stripe.com --output json
python3 scripts/lead_scorer.py <sample.json>          # or pipe JSON via stdin
python3 scripts/generate_pdf_report.py                # demo-mode sample PDF (needs reportlab)
./install.sh                                          # dry local install into ~/.claude/
```

For skill/agent prompt edits, the real check is behavioral: the file must stay
internally consistent (process matches its output template, scores sum to their
stated weights). There's nothing to "run" for a prompt — review it as prose.

## Git Workflow

- Active development branch for this work: **`claude/claude-md-docs-rh3ouf`**.
  Default branch is `main`.
- Commit with clear messages; push with `git push -u origin <branch>`.
- Do **not** open a pull request unless explicitly asked.

## Notes / Gotchas

- The repo's canonical GitHub path is
  `pducoffe20-a11y/ai-sales-team-claude` — several past commits fixed stale
  owner/name strings in URLs. If you change repo identity, grep `install.sh`,
  `uninstall.sh`, and `README.md` for old references.
- Counts to keep consistent when adding/removing pieces: **14 skills**
  (1 orchestrator + 13 sub-skills), **5 agents**, **4 scripts**, **6 templates**.
  These numbers are hard-coded in `README.md` badges and `install.sh` banners.
- License: MIT.

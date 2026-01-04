# Alpha-Cycle: Complete Automation Setup

## What's Been Added

This document summarizes the additions that enable **"drop hypothesis → run 20 cycles"** automation.

---

## New Files

### 1. `CLAUDE.md` (Project Root)
**Purpose:** Master instructions that Claude Code reads automatically when entering any Alpha-Cycle project.

**Contains:**
- Initialization protocol (how to parse hypothesis → project)
- 20-cycle research protocol (exact loop instructions)
- Phase schedule (expansive → integrative → synthesis)
- Hypothesis versioning triggers
- Experiment trigger conditions
- Complete command reference

**Key Feature:** Claude Code now knows *exactly* what to do at each step.

### 2. `files/SKILL.md` (Enhanced)
**Purpose:** Skill definition that tells Claude Code *when* to activate and provides quick-reference workflows.

**Contains:**
- Trigger phrases that activate the skill
- Three workflow patterns (Initialize, Run Cycles, Resume)
- Alphaxiv optimization reminders
- Quick command reference

### 3. `.claude/settings.json`
**Purpose:** Project settings for Claude Code implementations that read this directory.

**Contains:**
- Auto-read file list (CLAUDE.md, SKILL.md)
- Context files to load
- Trigger definitions

### 4. `templates/HYPOTHESIS_TEMPLATE.md`
**Purpose:** Shows users the ideal format for hypothesis input.

**Contains:**
- Structured template with all fields
- AHNA example showing proper formatting
- Technical vocabulary section for Alphaxiv optimization

### 5. `templates/REPORT_TEMPLATE.md`
**Purpose:** Template for final verification report.

**Contains:**
- Executive summary format
- Component-by-component analysis structure
- Evidence summary tables
- Gap and experiment documentation

---

## The Complete Workflow

### User Experience

```
User: "Here's my hypothesis [attaches hypothesis.pdf]. 
       Set up this project and begin a research cycle."

Claude Code:
1. Reads CLAUDE.md (knows the protocol)
2. Parses hypothesis.pdf
3. Creates project: rv new hypothesis-name
4. Fills out:
   - concept/README.md (core theory)
   - hypotheses/v1/hypothesis.md (falsifiable statement)
   - hypotheses/v1/components.yaml (verifiable claims)
5. Initializes gaps: rv gaps add "..." --priority high
6. Runs 20-cycle loop:
   - Cycles 1-7: Expansive discovery
   - Cycles 8-14: Integration, contradiction resolution
   - Cycles 15-20: Synthesis, final assessment
7. After each cycle:
   - Updates components.yaml with evidence
   - Checks versioning triggers
   - Saves synthesis with rv synthesize
8. Produces final report using REPORT_TEMPLATE.md
9. Presents to user with status and recommendations
```

### What Claude Code Does in Each Cycle

```
Cycle N:
├── Read context
│   ├── rv status
│   ├── rv gaps list
│   └── cat research/cycle-{N-1}/synthesis.md
│
├── Reason about question
│   ├── What phase am I in?
│   ├── What gaps are high priority?
│   ├── What did previous cycles find?
│   └── What component needs evidence?
│
├── Construct question (using prompts.md templates)
│
├── Execute: rv cycle "question" --phase {phase}
│
├── Analyze response
│   ├── What papers were found?
│   ├── How do they affect the hypothesis?
│   └── What new gaps emerged?
│
├── Save: rv synthesize N --synthesis "..." --gaps "..."
│
├── Update components.yaml with evidence
│
└── Check versioning triggers
```

---

## File Structure (Complete)

```
alpha-cycle/
├── CLAUDE.md                    # ← Claude Code reads this FIRST
├── README.md                    # Project documentation
├── pyproject.toml               # Python package config
│
├── .claude/
│   └── settings.json            # Claude Code settings
│
├── files/
│   ├── SKILL.md                 # Skill definition
│   ├── cli.py                   # CLI implementation
│   ├── alphaxiv.py             # Browser automation
│   ├── project.py               # Project management
│   ├── orchestrator.py          # Cycle orchestration
│   └── prompts.md               # Question templates
│
├── templates/
│   ├── HYPOTHESIS_TEMPLATE.md   # Input format guide
│   └── REPORT_TEMPLATE.md       # Output format guide
│
└── [project-name]/              # Created per hypothesis
    ├── .research-state.yaml
    ├── config.yaml
    ├── concept/README.md
    ├── hypotheses/v{N}/
    ├── research/cycle-{N}/
    ├── gaps/
    ├── resources/
    ├── tests/
    └── results/
```

---

## Key Design Decisions

### 1. CLAUDE.md as Master Instruction File
Claude Code reads this automatically. It contains everything needed to run the full workflow without additional prompting.

### 2. Explicit Phase Schedule
Rather than letting Claude Code decide, we specify:
- Cycles 1-7: Expansive
- Cycles 8-14: Integrative
- Cycles 15-20: Synthesis

### 3. Versioning Triggers are Documented
Claude Code knows exactly when to:
- Maintain current version
- Refine to new version
- Stop for major revision (consult user)
- Declare falsified

### 4. Evidence Tracking is Explicit
After each cycle, Claude Code must:
- Update components.yaml with paper IDs
- Mark status: supported | challenged | contested | untested

### 5. Templates Ensure Consistency
- Input template: User knows what format helps
- Output template: Reports are structured consistently

---

## How to Use

### First Time Setup
```bash
# Clone/download Alpha-Cycle
git clone https://github.com/helloprkr/Alpha-Cycle.git
cd Alpha-Cycle

# Install
pip install -e .
playwright install chromium

# Login to Alphaxiv (one time)
rv login
```

### Running Verification
```bash
# In Cursor with Claude Code:

User: "Here's my hypothesis [attaches file]. 
       Set up the project and run research cycles."

# Claude Code handles everything from here
```

### Resuming
```bash
cd existing-project/

User: "Continue the verification from where we left off."

# Claude Code reads state and continues
```

---

## What's Still Manual

1. **Alphaxiv Login**: Must run `rv login` once manually (Google OAuth)
2. **User Review**: Claude Code pauses for major hypothesis revisions
3. **Experiments**: User provides actual test results when proposed
4. **Final Approval**: User reviews final report before accepting

---

## Troubleshooting

### Claude Code Doesn't Follow Protocol
- Ensure CLAUDE.md exists in project root
- Check that Claude Code is reading it (should be automatic)
- Explicitly ask: "Read CLAUDE.md and follow the protocol"

### Cycles Are Repetitive
- Check that synthesis is being saved: cat research/cycle-{N}/synthesis.md
- Ensure questions reference previous findings
- Review gaps/active.yaml is being updated

### Components Not Updated
- Remind Claude Code to update components.yaml after each cycle
- Check the format matches the expected YAML structure

---

## Summary

The combination of:
- **CLAUDE.md** (protocol instructions)
- **SKILL.md** (activation triggers)
- **prompts.md** (question templates)
- **templates/** (input/output formats)

...creates a complete automation system where:

1. User provides hypothesis
2. Claude Code initializes everything
3. Claude Code runs 20 cycles autonomously
4. Claude Code produces structured final report

**The user's only job is to provide the hypothesis and review the results.**

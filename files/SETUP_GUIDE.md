# Research Verifier - Setup & Usage Guide

## What You're Getting

Two components:

1. **`research-verifier/`** - CLI tool (`rv` command)
   - Python package that handles browser automation
   - Commands: `new`, `login`, `ask`, `run`, `status`, `resume`

2. **`research-verifier-skill/`** - Claude Code skill
   - Copy to `/mnt/skills/user/` for Claude Code integration
   - Teaches Claude Code how to orchestrate the tool

---

## Installation Steps

### 1. Install the CLI Tool

```bash
# Copy research-verifier to your preferred location
cp -r research-verifier ~/tools/research-verifier

# Navigate there
cd ~/tools/research-verifier

# Install in development mode
pip install -e . --break-system-packages

# Install Playwright and browsers
pip install playwright --break-system-packages
playwright install chromium
```

### 2. Install the Claude Code Skill

```bash
# Copy skill to Claude Code skills directory
cp -r research-verifier-skill /mnt/skills/user/research-verifier
```

### 3. First-Time Alpharxiv Login

```bash
# This opens a browser - log in with your Google account
rv login

# The session is saved to ~/.research-verifier/browser-profile/
# You only need to do this once (unless session expires)
```

---

## Usage Patterns

### Pattern A: Direct CLI Usage

```bash
# Create project
rv new ahna-tropical-attention

# Edit your concept and hypothesis
cd ahna-tropical-attention
nano concept/README.md
nano hypotheses/v1/hypothesis.md

# Run 2-cycle test
rv run --cycles 2

# Check results
rv status
cat research/cycle-001/synthesis.md
```

### Pattern B: Claude Code Orchestration (Recommended)

In Cursor AI terminal, with Claude Code:

```
You: "I want to verify my hypothesis about tropical attention mechanisms in neural networks"

Claude Code: 
1. Creates project with `rv new tropical-attention`
2. Helps you write concept/README.md
3. Generates targeted questions based on your hypothesis
4. Runs `rv run --cycles 2`
5. Reads and synthesizes the results
6. Identifies gaps and next steps
```

### Pattern C: Single Query (No Project)

```bash
# Quick one-off question
rv ask "What are the latest papers on tropical geometry in neural networks?"
```

---

## Workflow for AHNA-Style Verification

### Cycle 1-7: Expansive Phase
- Broad literature survey
- Adjacent field exploration
- Alternative approach identification

### Cycle 8-14: Integrative Phase
- Pattern synthesis across findings
- Contradiction identification
- Gap bridging attempts

### Cycle 15-20: Synthesis Phase
- State assessment
- Evidence quality evaluation
- Hypothesis versioning decision

---

## File Locations Reference

```
~/.research-verifier/
├── browser-profile/          # Playwright session (Google OAuth)

~/your-project/
├── .research-state.yaml      # Project state (DO NOT EDIT)
├── config.yaml               # Settings (edit timeout, cycles)
├── concept/README.md         # YOUR THEORY
├── hypotheses/v1/            # YOUR HYPOTHESIS
├── research/                 # CYCLE RESULTS (auto-generated)
├── gaps/                     # GAP TRACKING (auto-updated)
└── resources/papers.yaml     # PAPER REGISTRY (auto-updated)
```

---

## Troubleshooting

### "rv: command not found"
```bash
# Check if installed
pip show research-verifier

# If not, reinstall
cd ~/tools/research-verifier && pip install -e .
```

### Browser automation fails
```bash
# Reinstall Playwright browsers
playwright install chromium

# Try running with visible browser (already default)
# Check ~/.research-verifier/browser-profile/ exists
```

### Session expired
```bash
rv login
# Complete Google OAuth again
```

### Cycle stuck mid-run
```bash
rv resume
# Or manually check checkpoint
cat research/cycle-NNN/checkpoint.json
```

---

## Next Steps After Testing

1. **Test 2-cycle run** on a simple concept
2. **Verify paper extraction** - check resources/papers.yaml
3. **Scale to 20 cycles** - update cycles_per_run in config.yaml
4. **Add your prompt templates** - the skill has placeholders for your templates

---

## Architecture Notes

```
┌────────────────────────────────────────────────────────────┐
│                     CURSOR IDE                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │                  CLAUDE CODE                          │ │
│  │  • Reads SKILL.md                                     │ │
│  │  • Generates questions (reasoning)                    │ │
│  │  • Invokes rv commands                                │ │
│  │  • Synthesizes results (reasoning)                    │ │
│  └──────────────────────────────────────────────────────┘ │
│                          │                                 │
│                          ▼                                 │
│  ┌──────────────────────────────────────────────────────┐ │
│  │               rv CLI TOOL                             │ │
│  │  • Browser automation (Playwright)                    │ │
│  │  • File management (project structure)                │ │
│  │  • State tracking (checkpoints)                       │ │
│  └──────────────────────────────────────────────────────┘ │
│                          │                                 │
└──────────────────────────│─────────────────────────────────┘
                           ▼
              ┌─────────────────────────┐
              │       ALPHARXIV         │
              │   (Gemini + ArXiv DB)   │
              └─────────────────────────┘
```

The key insight: **Claude Code does the thinking, rv does the plumbing.**

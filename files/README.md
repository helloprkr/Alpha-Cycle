# Research Verifier (rv)

A CLI tool for automating research verification loops between Claude Code and Alphaxiv.

## What It Does

Research Verifier automates the tedious parts of systematic literature research:

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESEARCH VERIFICATION LOOP                   │
│                                                                 │
│   ┌──────────────┐         ┌──────────────┐                    │
│   │  CLAUDE CODE │         │  ALPHAXIV   │                    │
│   │  (Reasoning  │ ◀─────▶ │  (Literature │                    │
│   │  + Synthesis)│   rv    │   Grounding) │                    │
│   └──────────────┘         └──────────────┘                    │
│          │                        │                            │
│          ▼                        ▼                            │
│   ┌────────────────────────────────────────┐                   │
│   │      PROJECT DIRECTORY                  │                   │
│   │  (Papers, Gaps, Hypotheses, Results)    │                   │
│   └────────────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

**Philosophy:** Claude Code does the thinking. The `rv` tool does the plumbing.

- **Claude Code** generates questions, synthesizes findings, identifies gaps
- **rv** handles browser automation, file management, and state tracking

## Installation

```bash
# Navigate to the project
cd "/path/to/Alpha-Cycle 🔁"

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the tool
pip install -e .

# Install browser automation
playwright install chromium
```

## Quick Start

### 1. Login to Alphaxiv (one-time)

```bash
rv login
```

A browser opens. Sign in with your Google account. Press Enter in terminal when done.

### 2. Create a Research Project

```bash
rv new my-research-topic
cd my-research-topic
```

### 3. Define Your Research

Edit `concept/README.md` with your theory:

```markdown
# Concept

## Core Theory

Research on inference-time scaling in large language models.
We explore how allocating compute during inference improves reasoning.

## Scope

- Methods for scaling inference compute
- Trade-offs between training and inference compute
```

### 4. Run Verification Cycles

**Option A: Automated Mode** (simpler, less adaptive)

```bash
rv run --cycles 3 --debug
```

**Option B: Claude Code Orchestrated** (recommended for complex research)

```bash
# Single query with Claude Code generating the question
rv ask "What are the key papers on inference-time scaling from 2024-2025?"
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `rv new <name>` | Create a new research project |
| `rv login` | Authenticate with Alphaxiv (one-time) |
| `rv login --debug` | Login with debug output for troubleshooting |
| `rv ask "<question>"` | Send a single question to Alphaxiv |
| `rv run --cycles N` | Run N automated verification cycles |
| `rv run --phase expansive` | Force a specific phase type |
| `rv run --debug` | Run with debug output |
| `rv status` | Show current project status |
| `rv resume` | Resume from last checkpoint |

## Project Structure

After running cycles, your project contains:

```
my-research-topic/
├── .research-state.yaml      # Project state (cycles, papers, gaps)
├── config.yaml               # Settings
│
├── concept/
│   └── README.md             # Your core theory/concept
│
├── hypotheses/
│   └── v1/
│       ├── hypothesis.md     # Falsifiable hypothesis
│       ├── components.yaml   # Decomposed verifiable claims
│       └── status.yaml       # Validation status
│
├── research/
│   └── cycle-001/
│       ├── questions.md      # Questions sent to Alphaxiv
│       ├── responses/
│       │   ├── q01-response.md    # Response text + paper links
│       │   └── q01-response.json  # Same, machine-readable
│       ├── synthesis.md      # Cycle synthesis
│       ├── metadata.json     # Statistics
│       └── checkpoint.json   # Resume point
│
├── gaps/
│   ├── active.yaml           # Open research gaps
│   └── resolved.yaml         # Closed gaps
│
├── resources/
│   ├── papers.yaml           # All discovered papers (deduplicated)
│   └── code.yaml             # Related repositories
│
├── tests/
│   └── registry.yaml         # Validation tests
│
└── results/                  # Test results and analysis
```

## Research Phases

Cycles rotate through three metacognitive phases:

| Phase | Focus | Question Style |
|-------|-------|----------------|
| **Expansive** | Cast wide net | "What work exists on X?" |
| **Integrative** | Find connections | "How do findings A and B reconcile?" |
| **Synthesis** | Assess state | "What is the consensus on X?" |

## Using with Claude Code (Recommended)

The most effective way to use this tool is with Claude Code orchestrating the research:

### Workflow

1. **You** describe what you want to verify to Claude Code
2. **Claude Code** reads your concept and generates targeted questions
3. **You** run `rv ask "question"` to query Alphaxiv
4. **Claude Code** reads the response and synthesizes findings
5. **Claude Code** identifies gaps and generates follow-up questions
6. **Repeat** for multiple cycles

### Example Session

```bash
# In Claude Code / Cursor terminal:

# 1. Create project
rv new inference-scaling
cd inference-scaling

# 2. Check status
rv status

# 3. Ask a targeted question (Claude Code generates this)
rv ask "What are the key mechanisms that enable test-time compute to improve LLM performance? Include papers from 2024-2025."

# 4. Claude Code reads response, then asks follow-up
rv ask "Based on the inference scaling literature, what are documented failure cases where additional compute does NOT help?"

# 5. Check collected papers
cat resources/papers.yaml

# 6. Check project status
rv status
```

## Configuration

Edit `config.yaml` in your project:

```yaml
project_name: my-research
settings:
  cycles_per_run: 20          # Max cycles per automated run
  checkpoint_interval: 5      # Save checkpoint every N cycles
  alphaxiv_timeout: 120      # Seconds to wait for response
```

## Troubleshooting

### "command not found: rv"

Activate the virtual environment:
```bash
source .venv/bin/activate
```

### Login verification failed

1. Make sure you're fully logged into Alphaxiv in the browser
2. Wait until you see the chat interface before pressing Enter
3. Try with debug mode: `rv login --debug`

### Submission not working

If questions aren't being submitted:
1. Use debug mode: `rv run --cycles 1 --debug`
2. Watch for "New message appeared" in output
3. Check the screenshot at `~/.research-verifier/browser-profile/debug_screenshot.png`

### Session expired

Run `rv login` again to refresh the browser session.

### Cycle interrupted

Use `rv resume` to continue from the last checkpoint.

### Response extraction issues

If papers aren't being extracted:
1. The Alphaxiv UI may have changed
2. Check debug output for selector information
3. Report issues with the debug log

## How It Works

1. **Browser Automation**: Uses Playwright with a persistent browser profile to maintain your Google login to Alphaxiv

2. **Query Execution**: Types your question into Alphaxiv and waits for the response to complete

3. **Response Extraction**: Parses the response text and extracts paper links (arxiv IDs, titles, URLs)

4. **State Management**: Saves everything to your project directory with deduplication and checkpointing

5. **Resume Support**: Every cycle creates a checkpoint, so interrupted runs can resume

## Data Persistence

| What | Where | When |
|------|-------|------|
| Questions | `research/cycle-NNN/questions.md` | Per cycle |
| Responses | `research/cycle-NNN/responses/` | Per question |
| Papers | `resources/papers.yaml` | Deduplicated after each cycle |
| Gaps | `gaps/active.yaml` | Updated each cycle |
| State | `.research-state.yaml` | After every operation |

## License

MIT

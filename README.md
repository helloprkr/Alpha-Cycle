<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Alpha--Cycle-Research_Verification_Engine-8B5CF6?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+PHBhdGggZD0iTTEyIDJhMTAgMTAgMCAxIDAgMTAgMTBIMTJWMloiLz48cGF0aCBkPSJNMTIgMTJhMiAyIDAgMSAwIDIgMiIvPjxwYXRoIGQ9Ik0xMiA4YTQgNCAwIDAgMSA0IDQiLz48L3N2Zz4=">
  <img alt="Alpha-Cycle" src="https://img.shields.io/badge/Alpha--Cycle-Research_Verification_Engine-8B5CF6?style=for-the-badge">
</picture>

<div align="center">

# 🔁 Alpha-Cycle

### **Automated Research Verification Engine**

*Orchestrate systematic literature research through AI-powered verification loops*

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Playwright](https://img.shields.io/badge/playwright-automation-2EAD33?style=flat-square&logo=playwright&logoColor=white)](https://playwright.dev)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

[Quick Start](#-quick-start) · [How It Works](#-how-it-works) · [Commands](#-commands) · [Documentation](#-documentation)

</div>

---

## ✨ What is Alpha-Cycle?

Alpha-Cycle automates the tedious parts of systematic literature research by creating a **verification loop** between two AI systems:

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

| Component | Role |
|-----------|------|
| **Claude Code** | Generates questions, synthesizes findings, identifies gaps |
| **Alphaxiv** | Searches academic literature, grounds claims in papers |
| **rv CLI** | Handles browser automation, file management, state tracking |

---

## 🎯 Use Cases

- **Validate theoretical concepts** against existing literature
- **Systematic literature reviews** with structured evidence collection
- **Hypothesis development** with iterative refinement cycles
- **Gap analysis** to identify unexplored research directions
- **Paper discovery** with intelligent deduplication

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- [Alphaxiv](https://alphaxiv.org) account (Google OAuth)
- [Cursor IDE](https://cursor.sh) with Claude Code (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/helloprkr/Alpha-Cycle.git
cd Alpha-Cycle

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the tool
pip install -e .

# Install browser automation
playwright install chromium
```

### First Run

```bash
# 1. Authenticate with Alphaxiv (one-time)
rv login

# 2. Create a research project
rv new my-research-topic
cd my-research-topic

# 3. Edit your concept
# Open concept/README.md and describe your research focus

# 4. Run verification cycles
rv run --cycles 3 --debug
```

---

## 🔄 How It Works

Alpha-Cycle implements a **metacognitive research loop** that rotates through three distinct phases:

### Research Phases

| Phase | Focus | Question Style | Cycles |
|-------|-------|----------------|--------|
| **🔍 Expansive** | Cast wide net | "What work exists on X?" | 1-7 |
| **🔗 Integrative** | Find connections | "How do A and B reconcile?" | 8-14 |
| **🎯 Synthesis** | Assess state | "What is the consensus?" | 15-20 |

### Cycle Flow

```
┌─────────────┐
│   START     │
│  (Concept)  │
└──────┬──────┘
       ▼
┌─────────────┐
│ Generate    │◀─────────────────────────────┐
│ Questions   │                              │
└──────┬──────┘                              │
       ▼                                     │
┌─────────────┐                              │
│ Query       │──┐                           │
│ Alphaxiv   │  │ N cycles                  │
└──────┬──────┘  │                           │
       ▼         │                           │
┌─────────────┐  │                           │
│ Extract &   │◀─┘                           │
│ Store       │                              │
└──────┬──────┘                              │
       ▼                                     │
┌─────────────┐    ┌─────────────┐           │
│ Synthesize  │───▶│ Identify    │───────────┘
│ Findings    │    │ Gaps        │ (if gaps remain)
└─────────────┘    └──────┬──────┘
                          │ (no gaps)
                          ▼
                   ┌─────────────┐
                   │  COMPLETE   │
                   │ (Hypothesis │
                   │  Updated)   │
                   └─────────────┘
```

---

## 📖 Commands

### Core Commands

| Command | Description |
|---------|-------------|
| `rv new <name>` | Create a new research project |
| `rv login` | Authenticate with Alphaxiv (one-time) |
| `rv ask "<question>"` | Send a single question to Alphaxiv |
| `rv run --cycles N` | Run N automated verification cycles |
| `rv status` | Show current project status |
| `rv resume` | Resume from last checkpoint |

### Claude Code Orchestration (Recommended)

| Command | Description |
|---------|-------------|
| `rv cycle "<question>" --phase expansive` | Run single cycle with your question |
| `rv synthesize <N> --synthesis "..." --gaps "..."` | Save your synthesis for cycle N |
| `rv gaps list` | List active research gaps |
| `rv gaps add "<description>" --priority high` | Add a new gap |
| `rv gaps resolve <id> --reason "..."` | Mark gap as resolved |

### Options

```bash
rv run --cycles 10 --phase expansive  # Force specific phase
rv run --debug                         # Enable debug output
rv login --debug                       # Debug login issues
```

---

## 📁 Project Structure

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
│       │   └── q01-response.json  # Machine-readable format
│       ├── synthesis.md      # Cycle synthesis
│       ├── metadata.json     # Statistics
│       └── checkpoint.json   # Resume point
│
├── gaps/
│   ├── active.yaml           # Open research gaps
│   └── resolved.yaml         # Closed gaps with resolution notes
│
├── resources/
│   ├── papers.yaml           # All discovered papers (deduplicated)
│   └── code.yaml             # Related GitHub repositories
│
├── tests/
│   ├── registry.yaml         # Validation tests
│   └── protocols/            # Test protocols
│
└── results/                  # Test results and analysis
```

---

## 🧠 Claude Code Integration

The most powerful way to use Alpha-Cycle is with **Claude Code orchestrating** the research:

### Workflow

1. **You** describe what you want to verify to Claude Code
2. **Claude Code** reads your concept and generates targeted questions
3. **Claude Code** runs `rv cycle "question"` to query Alphaxiv
4. **Claude Code** reads the response and synthesizes findings
5. **Claude Code** identifies gaps and generates follow-up questions
6. **Repeat** for multiple cycles

### Example Session

```bash
# In Cursor terminal with Claude Code:

# 1. Create and enter project
rv new inference-scaling
cd inference-scaling

# 2. Check initial status
rv status

# 3. Claude Code generates and runs targeted query
rv cycle "Conduct a comprehensive literature search on inference-time scaling 
in LLMs using at least three parallel search queries to capture varying 
terminology (test-time compute, reasoning scaling, System 2 thinking). 
Identify the 5-10 most significant papers from the last two years, 
prioritizing high community engagement." --phase expansive

# 4. Claude Code reads response, identifies patterns, adds gaps
rv synthesize 1 --synthesis "Key findings: three scaling mechanisms identified..." \
  --gaps "Failure modes under-documented" "PRM training requirements unclear"

# 5. Claude Code generates follow-up based on gaps
rv cycle "What are documented failure cases or limitations of test-time 
scaling approaches? When does additional inference compute NOT help?" \
  --phase expansive

# 6. Check accumulated papers
cat resources/papers.yaml

# 7. Review gaps
rv gaps list
```

---

## ⚙️ Configuration

Edit `config.yaml` in your project:

```yaml
project_name: my-research
settings:
  cycles_per_run: 20          # Max cycles per automated run
  checkpoint_interval: 5      # Save checkpoint every N cycles
  alphaxiv_timeout: 120      # Seconds to wait for response
```

---

## 🔧 Troubleshooting

<details>
<summary><strong>command not found: rv</strong></summary>

Activate the virtual environment:
```bash
source .venv/bin/activate
```
</details>

<details>
<summary><strong>Login verification failed</strong></summary>

1. Make sure you're fully logged into Alphaxiv in the browser
2. Wait until you see the chat interface before pressing Enter
3. Try with debug mode: `rv login --debug`
</details>

<details>
<summary><strong>Submission not working</strong></summary>

1. Use debug mode: `rv run --cycles 1 --debug`
2. Watch for "New message appeared" in output
3. Check screenshot at `~/.research-verifier/browser-profile/debug_screenshot.png`
</details>

<details>
<summary><strong>Session expired</strong></summary>

Run `rv login` again to refresh the browser session.
</details>

<details>
<summary><strong>Cycle interrupted</strong></summary>

Use `rv resume` to continue from the last checkpoint.
</details>

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [SETUP_GUIDE.md](files/SETUP_GUIDE.md) | Detailed installation instructions |
| [SKILL.md](files/SKILL.md) | Claude Code skill reference |
| [prompts.md](files/prompts.md) | Question templates and phase logic |

---

## 🏗️ Architecture

```
Alpha-Cycle/
├── files/
│   ├── cli.py           # Command-line interface
│   ├── alphaxiv.py     # Playwright browser automation
│   ├── project.py       # Directory & state management
│   ├── orchestrator.py  # Cycle execution engine
│   ├── SKILL.md         # Claude Code skill definition
│   └── prompts.md       # Question templates
├── pyproject.toml       # Package configuration
└── test-project/        # Example research project
```

### Technical Stack

- **Python 3.9+** - Core runtime
- **Playwright** - Browser automation with persistent sessions
- **YAML** - Configuration and state management
- **Asyncio** - Non-blocking I/O for browser operations

---

## 🤝 Contributing

Contributions welcome! Areas of interest:

- [ ] Additional AI research assistants (beyond Alphaxiv)
- [ ] Improved paper extraction patterns
- [ ] Visualization of research networks
- [ ] Export to reference managers (Zotero, Mendeley)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built for researchers who want to spend less time on plumbing and more time on thinking.**

[⬆ Back to Top](#-alpha-cycle)

</div>



---
name: research-verifier
description: Orchestrate automated research verification loops between Claude and Alpharxiv. Use when user wants to verify theoretical concepts, validate hypotheses against literature, run systematic research cycles, or ask "verify this idea" / "what does the research say about X" / "run research cycles on my hypothesis". Triggers on phrases like "verify", "validate hypothesis", "research cycles", "check against literature", "AHNA verification", "run 20 cycles".
---

# Research Verifier Skill

Orchestrates systematic research verification by automating dialogue between Claude (reasoning/synthesis) and Alpharxiv (literature grounding).

## Quick Start

```bash
# Create new research project
rv new my-theory

# Login to Alpharxiv (one-time)
rv login

# Run verification cycles
cd my-theory
rv run --cycles 2
```

## Core Workflow

### 1. Project Setup

When user wants to verify a concept:

```bash
rv new <project-name>
cd <project-name>
```

Then guide user to edit:
- `concept/README.md` - Core theory description
- `hypotheses/v1/hypothesis.md` - Falsifiable hypothesis
- `hypotheses/v1/components.yaml` - Decomposed claims

### 2. Question Generation

Generate questions based on phase. Reference [references/prompts.md](references/prompts.md) for templates.

**Phases:**
- **Expansive**: Divergent exploration (breadth)
- **Integrative**: Convergent synthesis (depth)  
- **Synthesis**: Reflective assessment (clarity)

For each cycle, generate 2-4 targeted questions that:
- Address active gaps from `gaps/active.yaml`
- Test hypothesis components from `hypotheses/vN/components.yaml`
- Match the current phase's focus

### 3. Cycle Execution

```bash
rv run --cycles N [--phase expansive|integrative|synthesis]
```

Each cycle:
1. Sends questions to Alpharxiv
2. Extracts responses + paper links
3. Saves to `research/cycle-NNN/`
4. Updates `resources/papers.yaml`
5. Identifies new gaps → `gaps/active.yaml`

### 4. Synthesis

After cycles complete, synthesize findings:

1. Read all responses from `research/cycle-*/responses/`
2. Identify patterns, contradictions, convergences
3. Update gap status in `gaps/`
4. Determine if hypothesis versioning is warranted

**Version hypothesis when:**
- Critical supporting evidence found
- Major gap bridged
- Contradicting evidence found

```bash
# View status anytime
rv status
```

## Claude Code Integration

When user asks to verify something, follow this pattern:

```python
# 1. Check if in research project
import subprocess
result = subprocess.run(['rv', 'status'], capture_output=True)

# 2. If not, create one
if 'Not in a research project' in result.stderr.decode():
    subprocess.run(['rv', 'new', 'concept-name'])
    
# 3. Generate questions (you do this reasoning)
questions = generate_questions_for_phase(concept, hypothesis, gaps, phase)

# 4. Run cycles
subprocess.run(['rv', 'run', '--cycles', '2'])

# 5. Synthesize results (you do this reasoning)
synthesis = synthesize_cycle_results(project_path)
```

## Directory Structure

```
project/
├── config.yaml                    # Settings
├── concept/README.md              # Core theory
├── hypotheses/
│   └── v1/
│       ├── hypothesis.md          # The hypothesis
│       ├── components.yaml        # Verifiable claims
│       └── status.yaml            # Validation status
├── research/
│   └── cycle-001/
│       ├── questions.md           # Questions sent
│       ├── responses/             # Individual responses
│       ├── synthesis.md           # Cycle synthesis
│       └── metadata.json          # Cycle stats
├── gaps/
│   ├── active.yaml                # Open gaps
│   └── resolved.yaml              # Closed gaps
├── resources/
│   ├── papers.yaml                # Paper registry
│   └── code.yaml                  # Code repos
├── tests/
│   └── registry.yaml              # Validation tests
└── results/                       # Test results
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `rv new <name>` | Create research project |
| `rv login` | Authenticate with Alpharxiv |
| `rv ask "<question>"` | Single query (no project) |
| `rv run --cycles N` | Run N verification cycles |
| `rv status` | Show project status |
| `rv resume` | Resume from checkpoint |

## Phase Prompts

See [references/prompts.md](references/prompts.md) for:
- Question generation templates per phase
- Synthesis prompt templates
- Gap identification prompts
- Hypothesis versioning triggers

## Best Practices

1. **Start with clear hypothesis** - Vague concepts produce vague results
2. **Decompose into components** - Each component should be independently testable
3. **Track gaps explicitly** - The gap registry drives question generation
4. **Version early** - Don't wait for perfection; version when evidence shifts understanding
5. **80/20 rule** - Focus cycles on highest-priority gaps

## Troubleshooting

**Session expired**: Run `rv login` again
**No responses**: Check Alpharxiv is accessible, increase timeout in config.yaml
**Cycle stuck**: Check `research/cycle-NNN/checkpoint.json`, run `rv resume`

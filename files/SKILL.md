---
name: research-verifier
description: Orchestrate automated research verification loops between Claude and Alpharxiv. Use when user wants to verify theoretical concepts, validate hypotheses against literature, run systematic research cycles, or ask "verify this idea" / "what does the research say about X" / "run research cycles on my hypothesis". Triggers on phrases like "verify", "validate hypothesis", "research cycles", "check against literature", "run cycles".
---

# Research Verifier Skill

Orchestrates systematic research verification by automating dialogue between Claude (reasoning/synthesis) and Alpharxiv (literature grounding).

**Philosophy:** Claude Code does the thinking. The `rv` tool does the plumbing.

- **Claude Code** generates questions, synthesizes findings, identifies gaps
- **rv** handles browser automation, file management, and state tracking

## Quick Start

```bash
# Login to Alpharxiv (one-time)
rv login

# Create new research project
rv new my-theory
cd my-theory

# Edit concept/README.md with your theory
# Then run the Claude Code orchestrated loop
```

## Core Workflow (Claude Code Orchestrated)

When user asks to verify a concept, follow this loop:

### Initial Setup

```bash
rv new <project-name>
cd <project-name>
# Help user fill in concept/README.md and hypotheses/v1/hypothesis.md
```

### Research Loop (YOU control this)

For each cycle (1 to N):

1. **Read current state:**
```bash
rv status
rv gaps list
cat research/cycle-{N-1}/synthesis.md  # If exists
```

2. **REASON about what to ask:**
   Based on:
   - The concept and hypothesis
   - Previous cycle findings (if any)
   - Active gaps
   - Current phase (expansive/integrative/synthesis)

   Generate 1-2 targeted questions that BUILD ON previous findings.

3. **Execute cycle:**
```bash
rv cycle "Your reasoned question here" --phase expansive
```

4. **Read and SYNTHESIZE the response:**
   - Read the response printed to terminal
   - Identify key findings
   - Identify contradictions or confirmations
   - Identify new gaps

5. **Save your synthesis:**
```bash
rv synthesize {N} --synthesis "Your synthesis markdown" --gaps "gap1" "gap2"
```

6. **Decide next action:**
   - More cycles needed? -> Generate next question, goto step 2
   - Research complete? -> Generate final report

### Phase Guidelines

**Cycles 1-7 (Expansive):**
- Ask: "What work exists on [specific aspect from gaps]?"
- Ask: "What methods from [adjacent field] apply to [our problem]?"
- Focus on breadth - cast a wide net

**Cycles 8-14 (Integrative):**
- Ask: "How do [Paper A findings] and [Paper B findings] reconcile?"
- Ask: "What explains the contradiction between [X] and [Y]?"
- Focus on depth - find connections

**Cycles 15-20 (Synthesis):**
- Ask: "What is the consensus on [core claim]?"
- Ask: "What critical evidence would falsify [hypothesis component]?"
- Focus on clarity - assess the state of knowledge

## Commands Reference

| Command | Description |
|---------|-------------|
| `rv new <name>` | Create research project |
| `rv login` | Authenticate with Alpharxiv |
| `rv login --debug` | Login with debug output |
| `rv ask "<question>"` | Quick single query |
| `rv cycle "<question>" --phase <phase>` | Run single cycle (Claude Code orchestrated) |
| `rv synthesize <N> --synthesis "..." --gaps "..."` | Save synthesis for cycle N |
| `rv gaps list` | List active gaps |
| `rv gaps add "<description>" --priority high` | Add a new gap |
| `rv gaps resolve <id> --reason "..."` | Mark gap as resolved |
| `rv run --cycles N` | Run N automated cycles (simpler, less adaptive) |
| `rv status` | Show project status |
| `rv resume` | Resume from checkpoint |

## Example Session

```bash
# In Claude Code / Cursor terminal:

# 1. Create project
rv new inference-scaling
cd inference-scaling

# 2. Check status
rv status

# 3. Ask a targeted question (Claude Code generates this based on concept)
rv cycle "What are the key mechanisms that enable test-time compute to improve LLM performance? Include papers from 2024-2025." --phase expansive

# 4. Claude Code reads response, synthesizes, identifies gaps
rv synthesize 1 --synthesis "The response identified three key mechanisms: 1) Best-of-N sampling with reward models, 2) Tree search with PRM verification, 3) Iterative refinement. A notable gap: failure cases are under-documented." --gaps "Failure modes of test-time scaling" "PRM training data requirements"

# 5. Claude Code reasons about next question based on gaps
rv cycle "What are documented failure cases or limitations of test-time scaling approaches? When does additional inference compute NOT help?" --phase expansive

# 6. Check collected papers
cat resources/papers.yaml

# 7. Check gaps
rv gaps list
```

## Key Principle

**YOU generate questions based on REASONING about accumulated findings.**

The `rv` tool just handles:
- Browser automation with Alpharxiv
- File management (saving responses, papers, gaps)
- State tracking (cycles completed, checkpoint/resume)

## Directory Structure

```
project/
├── config.yaml                    # Settings
├── .research-state.yaml           # Project state
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
│       ├── checkpoint.json        # Resume point
│       └── metadata.json          # Cycle stats
├── gaps/
│   ├── active.yaml                # Open gaps
│   └── resolved.yaml              # Closed gaps
├── resources/
│   ├── papers.yaml                # Paper registry (deduplicated)
│   └── code.yaml                  # Code repos
├── tests/
│   └── registry.yaml              # Validation tests
└── results/                       # Test results
```

## Best Practices

1. **Questions should reference previous findings** - "Based on the inference scaling literature..."
2. **Questions should target specific gaps** - "What explains the gap in..."
3. **Synthesis should be actual analysis** - Not placeholders like "[Claude Code: ...]"
4. **Progressive narrowing** - Start broad (expansive), end specific (synthesis)
5. **Track gaps explicitly** - The gap registry drives question generation

## Troubleshooting

**Session expired**: Run `rv login` again
**No responses**: Check Alpharxiv is accessible, use `--debug` flag
**Submission issues**: Use `rv login --debug` to inspect page structure
**Cycle interrupted**: Use `rv resume` to continue

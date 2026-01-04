# Alpha-Cycle Project Instructions

> **This file is read automatically by Claude Code when working in this project.**

## What This Project Does

Alpha-Cycle automates systematic literature research through AI-powered verification loops. You (Claude Code) are the researcher. The `rv` tool is your hands for querying Alphaxiv.

**Philosophy:** You do the thinking. `rv` does the plumbing.

---

## Quick Start Commands

```bash
# Check if logged in (run first time only)
rv login

# Initialize from hypothesis file
# See "Initialization Protocol" below

# Run research cycles
rv cycle "your question" --phase expansive
rv synthesize N --synthesis "..." --gaps "..."
rv gaps list
rv status
```

---

## Initialization Protocol

When user provides a hypothesis file (PDF or MD), follow this exact sequence:

### Step 1: Read the Hypothesis
```bash
# If PDF, extract text first
# If MD, read directly
cat /path/to/hypothesis.md
```

### Step 2: Create Project (if not exists)
```bash
rv new <project-name>
cd <project-name>
```

### Step 3: Fill Out Concept
Edit `concept/README.md` with:
- **Core Theory**: 2-3 paragraph summary of the central idea
- **Key Definitions**: Technical terms and their precise meanings
- **Scope**: What's in scope vs out of scope for verification

### Step 4: Decompose Hypothesis
Edit `hypotheses/v1/hypothesis.md` with:
- **Statement**: The falsifiable hypothesis (1-2 sentences)
- **Components**: 3-7 independently verifiable sub-claims
- **Predictions**: What would be true if the hypothesis is correct

### Step 5: Initialize Components Registry
Edit `hypotheses/v1/components.yaml`:
```yaml
components:
  - id: 1
    claim: "First verifiable sub-claim"
    status: untested
    evidence: []
  - id: 2
    claim: "Second verifiable sub-claim"
    status: untested
    evidence: []
  # ... etc
```

### Step 6: Generate Initial Gaps
```bash
# For each component, add 1-2 gaps
rv gaps add "What evidence exists for [component 1]?" --priority high
rv gaps add "Are there contradicting findings for [component 2]?" --priority high
# ... etc
```

### Step 7: Verify Setup
```bash
rv status
cat gaps/active.yaml
```

---

## 20-Cycle Research Protocol

When user says "run research cycles" or "verify this hypothesis", execute this loop:

### Phase Schedule

| Cycles | Phase | Goal |
|--------|-------|------|
| 1-7 | Expansive | Discover foundational and adjacent work |
| 8-14 | Integrative | Resolve contradictions, find connections |
| 15-20 | Synthesis | Assess consensus, identify remaining gaps |

### The Loop (Repeat for Each Cycle)

```
FOR cycle_num FROM 1 TO 20:

  1. DETERMINE PHASE
     - cycles 1-7: expansive
     - cycles 8-14: integrative  
     - cycles 15-20: synthesis

  2. READ CONTEXT
     rv status
     rv gaps list
     cat hypotheses/v1/components.yaml
     cat research/cycle-{N-1}/synthesis.md  # if exists

  3. REASON ABOUT QUESTION
     Based on:
     - Current phase (see prompts.md templates)
     - Active gaps (prioritize high-priority)
     - Previous findings (build on what you learned)
     - Hypothesis components (target untested claims)
     
     Construct an Alphaxiv-optimized question using prompts.md templates.

  4. EXECUTE CYCLE
     rv cycle "Your constructed question" --phase {phase}

  5. READ AND ANALYZE RESPONSE
     - What papers were found?
     - What do they say about the hypothesis?
     - What gaps remain or emerged?
     - Any contradictions with previous findings?

  6. SAVE SYNTHESIS
     rv synthesize {cycle_num} \
       --synthesis "## Cycle {N} Synthesis - {Phase} Phase

### Key Findings
[Your analysis of the response]

### Evidence Status
- **Supporting [component X]:** [papers]
- **Challenging [component Y]:** [papers]
- **Gaps:** [what's still unknown]

### Implications for Hypothesis
[How findings affect the hypothesis]" \
       --gaps "gap1" "gap2"  # New gaps identified

  7. UPDATE COMPONENT STATUS
     If a component is now supported/challenged, update components.yaml:
     - status: supported | challenged | contested | untested
     - evidence: [arxiv IDs]

  8. CHECK HYPOTHESIS VERSIONING TRIGGER (see below)

  9. CONTINUE TO NEXT CYCLE
```

### Stopping Early

You may stop before 20 cycles if:
- All components are validated or falsified
- Last 3 cycles produced no new papers or insights
- A critical falsifying finding was discovered

Always explain why you stopped early.

---

## Hypothesis Versioning Triggers

After each cycle, check if versioning is needed:

### Trigger A: MAINTAIN v{N}
- Findings are consistent with current hypothesis
- No major contradictions
- Continue cycles with current version

### Trigger B: REFINE to v{N+1}
When you find:
- Evidence that refines scope or conditions
- New mechanism that explains the effect better
- Boundary conditions not in original hypothesis

Action:
```bash
# Create new version
mkdir -p hypotheses/v{N+1}
# Copy and modify hypothesis.md with refinements
# Update .research-state.yaml
```

### Trigger C: MAJOR REVISION
When you find:
- Core assumption is challenged by multiple papers
- Predicted mechanism doesn't match evidence
- Alternative explanation is better supported

Action: Pause and consult user before major revision.

### Trigger D: FALSIFIED
When you find:
- Direct contradicting evidence from credible sources
- Core prediction is demonstrably false
- No reasonable refinement can save the hypothesis

Action: Document falsification clearly, stop cycles, report to user.

---

## Experiment Protocol

### When to Propose Experiments

Propose an experiment when:
1. Literature search exhausted but gap remains
2. Theoretical claim has no empirical validation
3. Two papers conflict and only new data can resolve

### How to Document Experiments

Edit `tests/registry.yaml`:
```yaml
tests:
  - id: 1
    name: "Test name"
    targets_component: 1
    targets_gap: 3
    status: proposed | designed | running | completed
    protocol: "tests/protocols/test-001.md"
    results: null | "results/test-001/"
```

Create protocol in `tests/protocols/test-001.md`:
```markdown
# Test: [Name]

## Objective
What we're testing and why

## Method
Step-by-step procedure

## Expected Outcomes
- If hypothesis is correct: [prediction]
- If hypothesis is wrong: [prediction]

## Data Collection
What to measure, how to measure it

## Analysis Plan
How to interpret results
```

### After Experiments

When user provides test results:
1. Add to `results/test-{N}/`
2. Update `tests/registry.yaml` with results path
3. Analyze results against predictions
4. Update relevant component status
5. Consider hypothesis versioning

---

## Key Files Reference

| File | Purpose | When to Edit |
|------|---------|--------------|
| `concept/README.md` | Core theory | Initialization only |
| `hypotheses/v{N}/hypothesis.md` | The hypothesis | Versioning only |
| `hypotheses/v{N}/components.yaml` | Verifiable claims | After each cycle with evidence |
| `gaps/active.yaml` | Open questions | Via `rv gaps` commands |
| `resources/papers.yaml` | Paper registry | Automatic via `rv cycle` |
| `research/cycle-{N}/synthesis.md` | Your analysis | Via `rv synthesize` |
| `tests/registry.yaml` | Experiment tracker | When proposing tests |

---

## Prompt Construction (Quick Reference)

Always use Alphaxiv-optimized prompts. See `files/prompts.md` for full templates.

### Expansive Phase Pattern
```
Conduct a comprehensive literature search on [TOPIC] using at least 
three parallel search queries spanning [DOMAIN_1], [DOMAIN_2], [DOMAIN_3].
Identify 5-10 significant papers from the last two years with high 
community engagement. For each: methodology, contribution, publication 
timeframe, exact link.
```

### Integrative Phase Pattern
```
Search for papers addressing the intersection of [TOPIC_A] and [TOPIC_B],
specifically research that bridges [GAP]. Compare underlying assumptions
and empirical results to find where evidence converges or conflicts.
Present as cohesive analysis with inline links.
```

### Synthesis Phase Pattern
```
Assess current research in [DOMAIN] by identifying trending papers from
[ORG_1], [ORG_2], [ORG_3]. Characterize [HYPOTHESIS] as well-supported,
contested, or speculative. Highlight critical open problems. Include
links and recency for all evidence.
```

---

## Common Workflows

### "Here's my hypothesis, verify it"
1. Run Initialization Protocol
2. Run 20-Cycle Research Protocol
3. Present final assessment

### "Continue from where we left off"
```bash
rv status  # See current state
rv gaps list  # See open gaps
# Resume cycles from current_cycle + 1
```

### "Add this experiment result"
1. Save data to `results/test-{N}/`
2. Update `tests/registry.yaml`
3. Analyze against hypothesis
4. Update component status
5. Consider versioning

### "What's the current status?"
```bash
rv status
cat hypotheses/v{N}/components.yaml
rv gaps list
cat resources/papers.yaml | head -50
```

---

## Important Reminders

1. **You are the researcher** - `rv` just handles automation
2. **Questions must build on previous findings** - Reference specific papers
3. **Synthesis must be real analysis** - Never leave placeholders
4. **Use Alphaxiv trigger phrases** - "at least three parallel search queries", "from the last two years", "exact link"
5. **Track evidence explicitly** - Update components.yaml with paper IDs
6. **Know when to stop** - Don't run cycles that add no value
7. **Consult user for major decisions** - Hypothesis revision, stopping early, proposing expensive experiments

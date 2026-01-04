---
name: alpha-cycle
description: |
  Orchestrate automated research verification loops between Claude and Alphaxiv.
  
  TRIGGERS:
  - "verify this hypothesis"
  - "validate my theory"
  - "run research cycles"
  - "check against literature"
  - "setup alpha-cycle project"
  - "here's my hypothesis"
  - User provides a hypothesis PDF or MD file
  
  CAPABILITIES:
  - Parse hypothesis files into structured project
  - Run 20-cycle systematic literature review
  - Track evidence for/against hypothesis components
  - Identify gaps and propose experiments
  - Version hypotheses based on evidence
---

# Alpha-Cycle Skill

**You are the researcher. `rv` is your hands for querying Alphaxiv.**

## When This Skill Activates

Activate when user:
1. Provides a hypothesis/theory file (PDF or MD)
2. Asks to "verify", "validate", or "check" a concept against literature
3. Asks to "run research cycles" or "start verification"
4. References an existing Alpha-Cycle project

## Project Structure

Every Alpha-Cycle project contains:
```
project/
├── CLAUDE.md              # ← READ THIS FIRST (project instructions)
├── concept/README.md      # Core theory
├── hypotheses/v{N}/       # Hypothesis versions
├── research/cycle-{N}/    # Research outputs
├── gaps/active.yaml       # Open questions
├── resources/papers.yaml  # Paper registry
└── tests/                 # Experiments
```

**Always read `CLAUDE.md` when entering an Alpha-Cycle project.**

---

## Workflow A: Initialize from Hypothesis

When user provides a hypothesis file:

```bash
# 1. Read the hypothesis
cat /path/to/hypothesis.md  # or extract from PDF

# 2. Create project
rv new hypothesis-name
cd hypothesis-name

# 3. Fill in concept/README.md
# Extract core theory, definitions, scope from hypothesis

# 4. Fill in hypotheses/v1/hypothesis.md
# Create falsifiable statement and components

# 5. Fill in hypotheses/v1/components.yaml
# Decompose into 3-7 verifiable claims

# 6. Initialize gaps
rv gaps add "What evidence exists for [component 1]?" --priority high
rv gaps add "What evidence exists for [component 2]?" --priority high
# ... for each component

# 7. Verify setup
rv status
```

Then proceed to Workflow B.

---

## Workflow B: Run 20-Cycle Verification

Execute this loop for systematic verification:

### Phase Schedule
- **Cycles 1-7**: Expansive (discover)
- **Cycles 8-14**: Integrative (connect)
- **Cycles 15-20**: Synthesis (assess)

### For Each Cycle:

```bash
# 1. Read context
rv status
rv gaps list
cat research/cycle-{N-1}/synthesis.md  # if exists

# 2. Reason about question (in your head)
#    - What phase am I in?
#    - What gaps are high priority?
#    - What did previous cycles find?
#    - What component needs evidence?

# 3. Construct Alphaxiv-optimized question
#    Use templates from files/prompts.md

# 4. Execute
rv cycle "Your carefully constructed question" --phase {phase}

# 5. Read response, analyze findings

# 6. Save synthesis
rv synthesize {N} --synthesis "Your analysis markdown" --gaps "new gap 1" "new gap 2"

# 7. Update components.yaml if evidence found

# 8. Check versioning triggers (see CLAUDE.md)

# 9. Continue to next cycle
```

### Question Construction Examples

**Expansive (Cycles 1-7):**
```
Conduct a comprehensive literature search on [TOPIC] using at least 
three parallel search queries spanning [DOMAIN_1], [DOMAIN_2], [DOMAIN_3]
and adjacent fields like [ADJACENT]. Identify 5-10 significant papers 
from the last two years with high community engagement. For each: 
methodology, contribution, publication timeframe, exact link.
```

**Integrative (Cycles 8-14):**
```
Search for papers addressing the intersection of [TOPIC_A] and [TOPIC_B],
specifically research that bridges [GAP]. Once you identify core papers,
compare their underlying assumptions and empirical results to find where
evidence converges or conflicts. Present as cohesive analysis with 
inline links and publication dates.
```

**Synthesis (Cycles 15-20):**
```
Assess current research in [DOMAIN] by identifying trending papers and
contributions from [ORG_1], [ORG_2], [ORG_3]. Characterize the status
of [HYPOTHESIS_CLAIM] as well-supported, contested, or speculative.
Highlight critical open problems. Include exact links and recency.
```

---

## Workflow C: Resume Existing Project

```bash
# 1. Read project state
rv status
cat CLAUDE.md  # Refresh on project instructions

# 2. Check where we left off
cat .research-state.yaml
rv gaps list

# 3. Continue from last cycle
# Follow Workflow B starting at current_cycle + 1
```

---

## Commands Reference

| Command | When to Use |
|---------|-------------|
| `rv new <name>` | Create project |
| `rv login` | First-time Alphaxiv auth |
| `rv cycle "<question>" --phase X` | Execute single cycle |
| `rv synthesize N --synthesis "..." --gaps "..."` | Save your analysis |
| `rv gaps list` | View open questions |
| `rv gaps add "desc" --priority high` | Add new gap |
| `rv gaps resolve N --reason "..."` | Close a gap |
| `rv status` | Project overview |

---

## Critical Rules

1. **Read CLAUDE.md first** when entering any project
2. **Questions must reference previous findings** - Cite specific papers
3. **Synthesis must be real analysis** - Never "[Claude Code: ...]" placeholders
4. **Use Alphaxiv trigger phrases** - See files/prompts.md
5. **Update components.yaml** when you find evidence
6. **Check versioning triggers** after significant findings
7. **Stop early if appropriate** - Explain why

---

## Alphaxiv Trigger Phrases

Include these to maximize search quality:

| Phrase | Effect |
|--------|--------|
| "at least three parallel search queries" | Triggers multi-vector search |
| "from the last two years" | Temporal filter |
| "high community engagement" | Trending filter |
| "contributions from [Org1], [Org2]" | Organization filter |
| "compare underlying assumptions" | Deep analysis mode |
| "exact link to the paper" | Ensures URLs returned |
| "adjacent fields like [X]" | Cross-domain discovery |

---

## Hypothesis Versioning

After each cycle, check:

- **MAINTAIN**: Findings consistent, continue
- **REFINE → v{N+1}**: Scope/conditions need adjustment
- **MAJOR REVISION**: Core assumption challenged (consult user)
- **FALSIFIED**: Direct contradiction (stop, report)

---

## Experiment Triggers

Propose experiment when:
1. Literature exhausted but gap remains
2. Theoretical claim lacks empirical validation
3. Two papers conflict, need new data

Document in `tests/registry.yaml` and `tests/protocols/`.

---

## Example: Full Session

```
User: "Here's my hypothesis about tropical attention mechanisms. 
       Verify it. [attaches hypothesis.md]"

Claude Code:
1. Reads hypothesis.md
2. rv new tropical-attention && cd tropical-attention
3. Fills concept/README.md from hypothesis
4. Creates hypotheses/v1/ with components
5. rv gaps add "Evidence for tropical limit of softmax?" --priority high
6. rv gaps add "Max-plus algebra in transformers?" --priority high
7. Runs 20 cycles:
   - Cycles 1-7: Expansive discovery
   - Cycles 8-14: Integration, contradiction resolution
   - Cycles 15-20: Synthesis, assessment
8. Updates components.yaml with evidence
9. Presents final report:
   - Hypothesis status: supported/contested/falsified
   - Component-by-component evidence
   - Remaining gaps
   - Suggested experiments if needed
```

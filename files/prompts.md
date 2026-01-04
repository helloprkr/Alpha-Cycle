# Research Verifier Prompts Reference

Templates for question generation, synthesis, and phase transitions.

## Question Generation Templates

### Expansive Phase (Divergent)

**Goal:** Cast a wide net. Find adjacent work, alternative approaches, unexpected connections.

```
Template 1 - Broad Survey:
"What are the most significant recent papers (last 2 years) related to [KEY_CONCEPT]? 
Include work from adjacent fields that might offer relevant insights."

Template 2 - Gap Exploration:
"What existing research addresses [GAP_DESCRIPTION]? 
Include both theoretical and empirical work, even if tangentially related."

Template 3 - Alternative Approaches:
"What alternative theoretical frameworks or methodologies exist for [PROBLEM_DOMAIN]?
How do they differ in assumptions and predictions?"

Template 4 - Cross-Domain:
"What insights from [ADJACENT_FIELD] might apply to [PRIMARY_FIELD]?
Are there successful transfers of methods or concepts?"
```

### Integrative Phase (Convergent)

**Goal:** Find connections, identify patterns, surface contradictions.

```
Template 1 - Pattern Synthesis:
"How do recent findings in [TOPIC_A] and [TOPIC_B] connect to or contradict each other?
What patterns emerge across these different research threads?"

Template 2 - Gap Bridging:
"Is there research that bridges these related gaps: [GAP_1]; [GAP_2]; [GAP_3]?
What common underlying issues do they share?"

Template 3 - Contradiction Analysis:
"What are the main points of disagreement in the literature on [TOPIC]?
What methodological or theoretical differences drive these contradictions?"

Template 4 - Evidence Convergence:
"What claims about [HYPOTHESIS_COMPONENT] have the strongest empirical support?
Where does evidence from multiple sources converge?"
```

### Synthesis Phase (Reflective)

**Goal:** Assess current state. Clarify what's known vs. unknown.

```
Template 1 - Consensus Check:
"What is the current consensus on [TOPIC]? 
What remains contested or unresolved?"

Template 2 - Critical Gaps:
"Based on the literature, what are the most critical open problems?
What would resolving them unlock?"

Template 3 - Research Directions:
"What are the most promising research directions for [DOMAIN]?
Where is the field heading?"

Template 4 - State Assessment:
"Given the current evidence on [HYPOTHESIS], how would you characterize its status:
well-supported, contested, speculative, or falsified? What's the key evidence either way?"
```

## Synthesis Prompts

### After Cycle Completion

Use this structure when synthesizing responses:

```markdown
## Synthesis Framework

### 1. Key Findings
- What new information emerged?
- What papers are most relevant?
- What claims are supported/challenged?

### 2. Pattern Analysis
- What themes recur across responses?
- What methodological approaches dominate?
- What gaps appear repeatedly?

### 3. Contradictions & Tensions
- Where do sources disagree?
- What explains the disagreements?
- Which position has stronger evidence?

### 4. Implications for Hypothesis
- Which components are strengthened?
- Which components are weakened?
- What modifications might be needed?

### 5. Updated Gaps
- What new gaps emerged?
- Which existing gaps were addressed?
- Priority ranking of remaining gaps?

### 6. Next Cycle Focus
- What questions should drive next cycle?
- Which phase is most appropriate?
- What specific papers should be examined?
```

### Hypothesis Versioning Prompt

When determining if hypothesis should be versioned:

```
Review the evidence accumulated across cycles and assess:

1. SUPPORTING EVIDENCE
   - What findings directly support the hypothesis?
   - How strong is this evidence (empirical vs theoretical)?
   - Does it address core predictions?

2. CHALLENGING EVIDENCE  
   - What findings contradict or complicate the hypothesis?
   - Are these fundamental challenges or edge cases?
   - Can the hypothesis accommodate these findings?

3. GAP STATUS
   - Which critical gaps have been bridged?
   - Which remain open?
   - Have new critical gaps emerged?

4. VERSION DECISION
   Based on above, recommend one of:
   
   A. MAINTAIN v{N} - No significant change warranted
      → Continue cycles with current hypothesis
      
   B. REFINE to v{N+1} - Modifications needed
      → Specify which components need updating
      → Draft refined hypothesis statement
      
   C. MAJOR REVISION to v{N+1} - Fundamental restructuring
      → Identify which core assumptions are challenged
      → Propose alternative framing
      
   D. FALSIFIED - Evidence contradicts core predictions
      → Document the falsifying evidence
      → Propose alternative directions
```

## Context Recap Template

When starting new Alpharxiv conversation (per Option C):

```
Context from previous research session:

PROJECT: {project_name}
HYPOTHESIS VERSION: v{version}
CYCLES COMPLETED: {total_cycles}

CURRENT HYPOTHESIS:
{hypothesis_statement_excerpt}

KEY FINDINGS SO FAR:
- {finding_1}
- {finding_2}
- {finding_3}

ACTIVE GAPS ({gap_count} total):
1. {high_priority_gap_1}
2. {high_priority_gap_2}
3. {high_priority_gap_3}

CURRENT PHASE: {phase} - {phase_description}

I'm continuing my research from where we left off. 
Please keep this context in mind for my questions.
```

## Gap Identification Patterns

Look for these indicators in Alpharxiv responses:

**Explicit Gap Indicators:**
- "open question"
- "remains unclear"
- "future work"
- "not yet understood"
- "gap in the literature"
- "under-explored"
- "requires further investigation"

**Implicit Gap Indicators:**
- Contradicting findings with no resolution
- Missing empirical validation for theoretical claims
- Methods applied in one domain but not another
- Old papers with no recent follow-up
- "To our knowledge, no work has..."

**Gap Priority Scoring:**
- HIGH: Directly blocks hypothesis validation
- MEDIUM: Related to hypothesis but not blocking
- LOW: Interesting but tangential

## Phase Transition Logic

```
Default rotation: expansive → integrative → synthesis → expansive...

Override conditions:

→ Force EXPANSIVE when:
  - Starting new hypothesis version
  - Many new gaps identified
  - Literature landscape unclear

→ Force INTEGRATIVE when:
  - Abundant material but unclear connections
  - Multiple contradictions surfaced
  - Need to consolidate before synthesis

→ Force SYNTHESIS when:
  - Approaching cycle budget (cycles 18-20)
  - Evidence saturation (diminishing new findings)
  - Decision point on hypothesis versioning
```

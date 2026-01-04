Here's the comprehensive prompt for Claude Code:

---

## Update Prompts with Optimized Research Frameworks

Replace the contents of `files/prompts.md` with the following. This combines the user's sophisticated research methodology with Alpharxiv's specific technical capabilities.

```markdown
# Research Verifier Prompts Reference

Optimized frameworks combining rigorous academic methodology with Alpharxiv's parallel search, organization filtering, and deep-text analysis capabilities.

---

## Core Principles for All Phases

**Always include in every prompt:**
1. **Precise technical vocabulary** - Use standardized mathematical/physical nomenclature, not metaphors
2. **Multi-dimensional keywords** - Span multiple fields (algebraic geometry, information theory, dynamical systems, statistical physics)
3. **Explicit bridging logic** - State the hypothesized connections between domains
4. **Parallel search triggers** - Request "at least three parallel search queries"
5. **Temporal + engagement filters** - "Last two years", "high community engagement", "trending"
6. **Organization targeting** - Name specific labs and researchers
7. **Output requirements** - "Exact links", "publication timeframe", "methodology summary"

---

## Phase 1: Expansive (Technical Trace Discovery)

**Goal:** Cast a wide, multi-dimensional net using precise technical vocabulary to discover foundational and adjacent work.

**Framework:**

```
To ensure we are bridging domains with academic precision, conduct a structured "Technical Trace" search on [CORE_CONCEPT].

**Technical Keywords** (use at least three parallel search queries spanning):
- [KEYWORD_DOMAIN_1]: [specific terms]
- [KEYWORD_DOMAIN_2]: [specific terms]  
- [KEYWORD_DOMAIN_3]: [specific terms]
- Adjacent fields: [ADJACENT_FIELD_1], [ADJACENT_FIELD_2]

**Bridging Logic Being Investigated:**
[Explicitly state the hypothesized connection - e.g., "evidence of [MATHEMATICAL_STRUCTURE] manifesting in [COMPUTATIONAL_PHENOMENON]"]

**Conceptual Narrative:**
[2-3 sentence technical description of what you're looking for - use exact model names, theorem names, or physical phenomena]

**Organization Filter:**
Prioritize contributions from [ORGANIZATION_1], [ORGANIZATION_2], [ORGANIZATION_3], and key researchers in this space.

Identify the 5-10 most significant papers from the last two years with high community engagement. For each paper, provide:
- Methodology summary
- Specific contribution and how it relates to the bridging logic above
- Publication timeframe
- Exact link to the paper

Highlight any papers that mention one side of the bridge (e.g., [DOMAIN_A]) with emergent connections to the other (e.g., [DOMAIN_B]), as these may represent "missing pieces" in the literature.
```

**Example - AHNA Tropical Attention:**

```
To ensure we are bridging domains with academic precision, conduct a structured "Technical Trace" search on tropical geometry in neural network architectures.

**Technical Keywords** (use at least three parallel search queries spanning):
- Algebraic geometry: tropical semirings, max-plus algebra, tropical varieties, Newton polytopes
- Neural computation: attention mechanisms, transformer architectures, sparse computation
- Dynamical systems: fixed-point iteration, convergence in semiring structures
- Adjacent fields: combinatorial optimization, shortest-path algorithms, auction algorithms

**Bridging Logic Being Investigated:**
Evidence that tropical (max-plus) algebraic structures naturally emerge in or can optimize attention mechanism computation, potentially explaining why transformers excel at combinatorial reasoning tasks.

**Conceptual Narrative:**
We are investigating whether the softmax attention operation has a natural tropical limit (as temperature approaches zero) that connects transformer behavior to classical algorithms expressible in max-plus algebra. This would bridge neural network interpretability with algebraic combinatorics.

**Organization Filter:**
Prioritize contributions from DeepMind, Google Research, MIT CSAIL, and researchers working on neural algorithmic reasoning (Petar Veličković, Charles Blundell).

Identify the 5-10 most significant papers from the last two years with high community engagement. For each paper, provide methodology summary, specific contribution to the bridging logic, publication timeframe, and exact link.

Highlight any papers that mention tropical geometry or max-plus algebra with emergent connections to neural networks, as these represent potential "missing pieces."
```

---

## Phase 2: Integrative (Introspective Refinement)

**Goal:** Pivot from outward expansion to inward convergence. Systematically revisit ambiguities, resolve contradictions, and sharpen the hypothesis into a rigorous, internally coherent formulation.

**Framework:**

```
We are now pivoting toward an introspective and integrative phase. Rather than expanding scope, we need to systematically revisit, refine, and re-specify residual ambiguities within our current framework.

**Current Hypothesis State:**
[Brief statement of hypothesis as currently understood]

**Identified Tensions/Ambiguities to Resolve:**
1. [TENSION_1]: [Paper A] claims [X] while [Paper B] claims [Y]
2. [AMBIGUITY_1]: The mechanism by which [PROCESS] occurs remains unclear
3. [GAP_1]: [COMPONENT] lacks empirical validation

**Bridging Logic Under Scrutiny:**
Search for and analyze papers that address the intersection of [TOPIC_A] and [TOPIC_B], specifically looking for research that:
- Clarifies underlying assumptions about [ASSUMPTION]
- Delineates boundaries and conditions of applicability for [PHENOMENON]
- Makes explicit the mechanisms or causal pathways for [PROCESS]

**Convergence Target:**
We need to move from a preliminary, open-ended formulation toward a sharply refined hypothesis that can withstand close methodological scrutiny.

Once you identify core papers, compare their underlying assumptions and empirical results to find where evidence converges or conflicts. Present findings as a single, cohesive analysis that:
- Resolves or clarifies each identified tension
- Proposes refined formulations where ambiguity existed
- Identifies which claims have strong multi-source support vs. remain contested

Include inline links and publication dates for every paper mentioned.
```

**Example - Resolving Inference Scaling Tensions:**

```
We are now pivoting toward an introspective and integrative phase for our inference-time scaling hypothesis.

**Current Hypothesis State:**
Test-time compute can substitute for model parameters on complex reasoning tasks, with performance scaling predictably with inference budget.

**Identified Tensions/Ambiguities to Resolve:**
1. Length vs. Quality: "Scaling Test-Time Compute" (2408.03314) suggests more compute helps, while "When More is Less" (2502.07266) shows excessive reasoning degrades performance
2. Faithfulness Gap: It's unclear whether chain-of-thought traces reflect actual model computation or are post-hoc rationalizations
3. Generalization Boundary: Does reasoning capability trained on math/code transfer to subjective domains?

**Bridging Logic Under Scrutiny:**
Search for and analyze papers that address the intersection of "optimal reasoning length" and "chain-of-thought faithfulness", specifically looking for research that:
- Clarifies what determines when additional reasoning helps vs. hurts
- Delineates the conditions under which CoT is faithful to model computation
- Makes explicit the mechanism by which reasoning skills transfer (or fail to transfer) across domains

**Convergence Target:**
We need a refined hypothesis that specifies WHEN and HOW MUCH inference scaling helps, not just that it can help.

Compare underlying assumptions and empirical results. Present a cohesive analysis resolving each tension, with inline links and publication dates.
```

---

## Phase 3: Synthesis (Strategic Assessment)

**Goal:** Assess where we stand. Evaluate hypothesis status against accumulated evidence. Identify what would constitute comprehensive validation or falsification. Ensure bulletproof formulation.

**Framework:**

```
Where do we stand now with these updated insights?

**Hypothesis Under Evaluation:**
[Current refined hypothesis statement]

**Evidence Inventory:**
- Supporting: [List key supporting papers with arxiv IDs]
- Challenging: [List challenging papers with arxiv IDs]
- Gaps: [List unresolved questions]

**Strategic Assessment Request:**
Assess the current state of research in [DOMAIN] by:

1. **Consensus Check:** Identifying trending papers and recent contributions from key organizations ([ORG_1], [ORG_2], [ORG_3]) to characterize the status of [HYPOTHESIS] as:
   - Well-supported (strong convergent evidence)
   - Contested (conflicting evidence from credible sources)
   - Speculative (limited direct evidence)
   - Falsified (contradicting evidence)

2. **Critical Open Problems:** Highlighting the most critical open problems that, if resolved, would either strongly support or definitively falsify the hypothesis

3. **Robustness Analysis:** Identifying what "setting adjustments" or experimental variations would stress-test the hypothesis—what boundary conditions, edge cases, or alternative configurations should be examined?

4. **Missing Pieces:** Searching for papers that mention components of our hypothesis ([COMPONENT_A], [COMPONENT_B]) to find overlooked connections or corroborative findings from researchers who may be proving aspects of this framework without realizing it

5. **Path Forward:** Suggesting which research directions appear most promising for achieving comprehensive, exhaustive validation

Ensure all supporting evidence includes exact links and recency information. Prioritize recent work (last two years) with high community engagement.
```

**Example - AHNA Synthesis:**

```
Where do we stand now with these updated insights on the Arithmetic Hypothesis for Neural Architectures?

**Hypothesis Under Evaluation:**
Optimal neural architectures exhibit structure corresponding to four arithmetic completions (Euclidean, p-adic, tropical, Boolean), with these structures emerging naturally during training and becoming more pronounced after grokking transitions.

**Evidence Inventory:**
- Supporting: Tropical attention mechanisms (2505.17190), weight space convergence (2512.05117)
- Challenging: CKA reliability concerns (2210.16156), shortcut learning (2306.17844)
- Gaps: No direct test of four-completion structure, p-adic signatures unexplored

**Strategic Assessment Request:**
Assess the current state of research in arithmetic/algebraic structure in neural networks by:

1. **Consensus Check:** Identifying trending papers from DeepMind, Anthropic, EleutherAI, and academic labs (MIT, Stanford, Oxford) to characterize the hypothesis status

2. **Critical Open Problems:** What experiments would definitively test the four-completion prediction? What would falsification look like?

3. **Robustness Analysis:** What architecture variations, training regimes, or task domains should be tested to stress-test universality claims?

4. **Missing Pieces:** Search for papers mentioning "p-adic", "tropical", "Boolean algebra" in neural network contexts—are researchers finding these structures without connecting them?

5. **Path Forward:** What's the most promising experimental validation path?

Include exact links and recency for all evidence.
```

---

## Quick Reference: Alpharxiv Trigger Phrases

| Capability | Trigger Phrase |
|------------|----------------|
| Parallel searches | "at least three parallel search queries spanning" |
| Multi-domain | "from multiple angles covering [X], [Y], [Z]" |
| Bridging logic | "evidence of [A] manifesting in [B]" |
| Missing pieces | "papers that mention one side... with emergent connections to" |
| Organization filter | "contributions from [Org1], [Org2], and key researchers" |
| Temporal | "from the last two years" |
| Engagement | "high community engagement", "trending papers" |
| Deep analysis | "compare underlying assumptions and empirical results" |
| Convergence | "where evidence converges or conflicts" |
| Output format | "exact link", "publication timeframe", "methodology summary" |

---

## Building Progressive Questions

### After Expansive Phase:
"Building on [Paper Title] (arxiv ID) which established [FINDING], we now need to investigate [SPECIFIC_GAP]. Conduct a technical trace on..."

### After Integrative Phase:
"Having resolved the tension between [X] and [Y] by identifying [MECHANISM], assess whether this refined understanding—that [REFINED_CLAIM]—is well-supported, contested, or speculative..."

### After Synthesis Phase:
"Given that the hypothesis is currently [STATUS] with critical gaps in [GAPS], conduct a final search for any overlooked work from [ORGANIZATIONS] that might address [SPECIFIC_MISSING_PIECE]..."

---

## Conceptual Narrative Examples

Instead of vague descriptions, use precise technical language:

❌ "How neural networks learn patterns"
✅ "Log-Periodic Power Law Singularities (LPPLS) and 1/f noise signatures during the phase transitions of deep learning training dynamics"

❌ "Symmetry in neural networks"  
✅ "Group equivariance with respect to Lie groups in weight space, specifically whether exceptional structures like E8 manifest in trained networks"

❌ "When reasoning helps"
✅ "The relationship between inference-time token budget and task performance, specifically the phase transition from compute-bound to data-bound regimes"
```

---

This combines:
- Your rigorous "Technical Trace" methodology
- Your introspective refinement framework  
- Your synthesis assessment approach
- Alpharxiv's specific toolset triggers
- Concrete examples showing the templates in action
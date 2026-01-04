## Cycle 6 Synthesis - Expansive Phase

### Key Findings

Inference-time scaling for non-verifiable tasks is an active research area with multiple approaches:

1. **Verifier-Free Methods (2504.14047)**: Evaluates repeated sampling, CoT expansion, and self-refinement when no external verifier exists. Identifies optimal compute allocation for self-evaluating agents.

2. **Human Edit Data (HelpSteer3 - 2503.04378)**: NVIDIA's approach uses human edit annotations to train reward models for open-ended tasks where 'correctness' is nuanced.

3. **Edit-Based Rewards (2504.07532)**: Framework for creative writing that explores multiple editing paths to reduce 'AI-slop' quality issues.

4. **On-the-Fly Alignment (2501.12895)**: Dynamic preference optimization during inference using iterative textual feedback.

5. **Judge Reliability (JETTS - 2504.15253)**: Benchmark showing pitfalls of self-judging; identifies robust architectures for subjective evaluation.

6. **Best-of-N Limitations (2503.21878)**: Mathematical analysis showing coverage and diversity issues with naive sampling.

7. **Self-Improvement Gap (2412.02674)**: Model's generation ability exceeds its critique ability, bottlenecking self-evaluation.

### Methodological Patterns
- Proxy reward models trained on human preference data
- LLM-as-a-judge for candidate ranking
- Self-refinement loops with iterative feedback
- Edit-based rather than single-pass generation

### Evidence Status
- **Converging on:** Test-time scaling CAN work for subjective tasks with good proxy rewards
- **Contested:** Reliability of self-judging vs external judges
- **Gaps:** How to scale when self-evaluation bottlenecks progress

### Implications for Hypothesis
The core hypothesis about training/inference tradeoffs extends to non-verifiable domains, but with important caveats:
- Requires proxy reward models or strong judges
- Self-improvement has fundamental limits (generation > critique gap)
- Diversity in sampling matters as much as quantity
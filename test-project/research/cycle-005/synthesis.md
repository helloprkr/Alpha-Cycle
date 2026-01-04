## Cycle 5 Synthesis: Empirical Evidence for Inference vs Training Scaling

### Key Findings

**The 14x Crossover Point (2408.03314)**
Snell et al. demonstrate that for a fixed FLOP budget, a smaller model using optimal test-time search (Beam Search + Process Verifier) can outperform a model with 14x more parameters. This is the clearest empirical evidence of compute-optimal frontiers.

**Large Language Monkeys Effect (2407.21787)**  
For coding tasks, generating 100-1000 samples from a small model (Llama-7B) achieves higher pass@k than single samples from 10x larger models. Horizontal compute (sampling) can beat vertical compute (parameters).

**Difficulty-Dependent Frontier**
The crossover is NOT static - it depends on problem difficulty:
- Easy problems: Zero-shot is optimal (test-time compute wasted)
- Very hard problems: No amount of test-time compute helps if success rate is 0%
- Medium-hard problems: Test-time scaling dominates

**Overthinking Constraint (2412.21187, 2506.05333)**
Critical limitation: scaling inference indefinitely leads to 'overthinking' where models drift from correct solutions or become verbose without accuracy gains.

**Verifiability Requirement**
Documented crossovers primarily occur for tasks with verifiable outcomes (math, code) where search algorithms can rank candidates.

### Implications for Hypothesis
The core hypothesis about training/inference tradeoffs is partially validated:
- YES: Test-time compute CAN substitute for parameters in specific regimes
- BUT: Effectiveness is bounded by base model capability and problem difficulty
- AND: There are diminishing/negative returns from excessive reasoning

### Papers Added
- 2502.06703: Can 1B LLM Surpass 405B LLM?
- 2412.21187: Do NOT Think That Much (Overthinking)
- 2506.05333: Kinetics - Rethinking Test-Time Scaling Laws
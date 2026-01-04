# Response to Q1

## Question

Conduct a comprehensive literature search on inference-time scaling for non-verifiable tasks using at least three parallel search queries to capture varying terminology (open-ended generation, subjective evaluation, creative tasks) and work from adjacent fields like human evaluation and preference learning. Identify the 5-10 most significant papers from the last two years, prioritizing those with high community engagement. For each paper, provide a brief summary of its methodology, its specific contribution to the field, its publication timeframe, and the exact link to the paper.

## Response

Inference-time scaling has traditionally focused on verifiable tasks like mathematics and coding where a hard verifier (e.g., a compiler or ground-truth answer) can guide the search. However, recent research has shifted toward non-verifiable, open-ended, and subjective tasks by leveraging reward models, LLM-as-a-judge, and self-critique mechanisms.

The following eight papers represent the most significant advancements in this area over the last two years, prioritizing high-engagement work that addresses the challenges of scaling compute in domains without objective ground truth.

Key Literature on Inference-Time Scaling for Non-Verifiable Tasks

Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters This foundational paper explores the trade-offs between scaling model size and scaling test-time compute. The authors investigate two primary mechanisms: searching against a learned verifier (Best-of-N) and iteratively refining the model's own distribution. Their findings suggest that for tasks where a verifier can be trained (even if it's a proxy for human preference), scaling compute at inference can often yield performance gains equivalent to using a significantly larger base model. Published a year ago: 
Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters

Think Deep, Think Fast: Investigating Efficiency of Verifier-free Inference-time-scaling Methods This work specifically addresses the "verifier-free" regime, where no external reward model or ground truth is available. The researchers evaluate methods such as repeated sampling, chain-of-thought expansion, and self-refinement on subjective and creative tasks. The study identifies optimal compute allocation strategies when the model must act as its own evaluator, providing a benchmark for self-improving agents in open-ended domains. Published 9 months ago: 
Think Deep, Think Fast: Investigating Efficiency of Verifier-free Inference-time-scaling Methods

HelpSteer3: Human-Annotated Feedback and Edit Data to Empower Inference-Time Scaling in Open-Ended General-Domain Tasks NVIDIA introduces a large-scale dataset and methodology specifically designed to bridge the gap between verifiable reasoning and general-domain tasks. They propose using high-quality human edit data to train reward models that can guide inference-time search for creative writing and open-ended chat. This contribution is critical for scaling inference in tasks where "correctness" is a matter of nuance and stylistic preference rather than binary logic. Published 10 months ago: 
HelpSteer3: Human-Annotated Feedback and Edit Data to Empower Inference-Time Scaling in Open-Ended General-Domain Tasks

AI-Slop to AI-Polish? Aligning Language Models through Edit-Based Writing Rewards and Test-time Computation Focusing on creative tasks, this paper presents an edit-based reward modeling framework to improve the quality of long-form writing during inference. By using test-time computation to explore multiple editing paths and selecting the most "polished" result based on learned writing preferences, the authors demonstrate that inference scaling can significantly reduce the generic "AI-slop" often found in single-pass generations. Published 9 months ago: 
AI-Slop to AI-Polish? Aligning Language Models through Edit-Based Writing Rewards and Test-time Computation

Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback This research introduces a method for on-the-fly alignment where the model optimizes its response based on iterative textual feedback during a single inference pass. Instead of relying on a static reward model, it uses a preference-learning approach to refine outputs for tasks like summarization and creative persona adoption. This methodology allows for a dynamic form of inference scaling that adapts to the specific constraints of a non-verifiable prompt. Published a year ago: 
Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback

Evaluating Judges as Evaluators: The JETTS Benchmark of LLM-as-Judges as Test-Time Scaling Evaluators Since non-verifiable tasks rely heavily on "judges" to select the best output among candidates, this paper investigates the reliability of these judges. It proposes the JETTS benchmark to evaluate how well different LLM-as-a-judge configurations perform when used to scale test-time compute. Their methodology highlights the potential pitfalls of "self-judging" and identifies the most robust judge architectures for subjective scaling. Published 8 months ago: 
Evaluating Judges as Evaluators: The JETTS Benchmark of LLM-as-Judges as Test-Time Scaling Evaluators

Is Best-of-N the Best of Them? Coverage, Scaling, and Optimality in Inference-Time Alignment Best-of-N sampling is the most common technique for scaling compute in non-verifiable domains, but this paper provides a rigorous mathematical analysis of its limitations. The authors explore how the diversity of samples and the quality of the proxy reward model impact the overall scaling law. They propose improved sampling strategies that provide better coverage of the preferred output space in subjective alignment tasks. Published 9 months ago: 
Is Best-of-N the Best of Them? Coverage, Scaling, and Optimality in Inference-Time Alignment

Mind the Gap: Examining the Self-Improvement Capabilities of Large Language Models This study examines whether LLMs can effectively verify and improve their own performance without external signal. By exploring the "gap" between a model's ability to generate and its ability to critique, the authors provide insights into how much inference-time compute can be meaningfully scaled before the model's self-evaluation bottlenecks its progress. This is particularly relevant for high-level creative tasks where external feedback is unavailable. Published a year ago: 
Mind the Gap: Examining the Self-Improvement Capabilities of Large Language Models

## Papers Found

- [Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters](https://alphaxiv.org/abs/2408.03314)
- [Think Deep, Think Fast: Investigating Efficiency of Verifier-free Inference-time-scaling Methods](https://alphaxiv.org/abs/2504.14047)
- [HelpSteer3: Human-Annotated Feedback and Edit Data to Empower Inference-Time Scaling in Open-Ended General-Domain Tasks](https://alphaxiv.org/abs/2503.04378)
- [AI-Slop to AI-Polish? Aligning Language Models through Edit-Based Writing Rewards and Test-time Computation](https://alphaxiv.org/abs/2504.07532)
- [Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback](https://alphaxiv.org/abs/2501.12895)
- [Evaluating Judges as Evaluators: The JETTS Benchmark of LLM-as-Judges as Test-Time Scaling Evaluators](https://alphaxiv.org/abs/2504.15253)
- [Is Best-of-N the Best of Them? Coverage, Scaling, and Optimality in Inference-Time Alignment](https://alphaxiv.org/abs/2503.21878)
- [Mind the Gap: Examining the Self-Improvement Capabilities of Large Language Models](https://alphaxiv.org/abs/2412.02674)

## Metadata

Timestamp: 2026-01-04T10:50:11.846904

# Response to Q1

## Question

What are the most significant recent papers (last 2 years) related to Research on inference-time scaling and chain-of-thought reasoning in large language models. We explo? Include work from adjacent fields that might offer relevant insights.

## Response

Research into large language models has undergone a paradigm shift over the last two years, moving from a primary focus on pre-training scaling laws to the "inference-time scaling" era. This transition is characterized by the development of models that can "think" longer before responding, often referred to as System 2 reasoning. The most significant trend is the discovery that increasing computational budget during inference—through techniques like repeated sampling, search, and extended chain-of-thought processes—can sometimes yield performance gains equivalent to scaling model parameters by orders of magnitude.

Key developments include the formalization of "Inference Scaling Laws," which provide empirical frameworks for how much test-time compute to allocate based on problem difficulty. There is also a major focus on verification-guided search, where process-based reward models (PRMs) evaluate intermediate reasoning steps rather than just the final answer. This has been popularized by models like OpenAI’s o1 and DeepSeek-R1, which use reinforced reasoning to self-correct and explore multiple paths. Insights from adjacent fields, particularly diffusion models and classical search, are also being integrated to treat language generation as a stochastic process that can be refined through particle-based methods or classical backtracking algorithms.

Significant Recent Papers on Inference-Time Scaling and Reasoning

Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters
This foundational work from Google DeepMind demonstrates that for many tasks, allocating additional compute at test-time (through search or refinement) is more effective than using a larger model, providing a "compute-optimal" recipe for inference.

Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters
 (published 1 year ago)

Recursive Language Models
Published just 4 days ago, this paper introduces a general inference strategy that allows LLMs to process arbitrarily long prompts and reasoning chains by treating inference-time scaling as a recursive process, pushing the boundaries of context and depth.

Recursive Language Models
 (published 4 days ago)

Stop Overthinking: A Survey on Efficient Reasoning for Large Language Models
A comprehensive survey that categorizes the "Large Reasoning Model" (LRM) landscape, including the architectures behind OpenAI o1 and DeepSeek-R1, while addressing the efficiency challenges of long-form chain-of-thought reasoning.

Stop Overthinking: A Survey on Efficient Reasoning for Large Language Models
 (published 9 months ago)

Inference Scaling Laws: An Empirical Analysis of Compute-Optimal Inference for Problem-Solving
This paper provides an empirical analysis of how performance scales with inference compute, identifying optimal configurations for different task complexities and model sizes, paralleling the original Chinchilla scaling laws.

Inference Scaling Laws: An Empirical Analysis of Compute-Optimal Inference for Problem-Solving with Language Models
 (published 1 year ago)

Is PRM Necessary? Problem-Solving RL Implicitly Induces PRM Capability in LLMs
An influential study investigating whether explicit Process-based Reward Models are required for reasoning, finding that reinforcement learning on final outcomes can implicitly train a model to verify its own intermediate steps.

Is PRM Necessary? Problem-Solving RL Implicitly Induces PRM Capability in LLMs
 (published 8 months ago)

Inference-Time Scaling for Diffusion Models beyond Scaling Denoising Steps
Offering cross-disciplinary insights, this work explores how generative models in the visual domain can scale at inference time using search and verification, providing a blueprint that is being increasingly adapted for textual reasoning.

Inference-Time Scaling for Diffusion Models beyond Scaling Denoising Steps
 (published 1 year ago)

Large Language Monkeys: Scaling Inference Compute with Repeated Sampling
This paper explores the "simple yet effective" side of inference scaling, showing how massive parallel sampling (generating thousands of potential answers) combined with verification can significantly outperform traditional greedy decoding.

Large Language Monkeys: Scaling Inference Compute with Repeated Sampling
 (published 1 year ago)

Towards Reasoning Era: A Survey of Long Chain-of-Thought for Reasoning Large Language Models
A recent survey focused specifically on the "Long CoT" paradigm, explaining the mechanisms that allow models to generate thousands of internal reasoning tokens to solve high-difficulty mathematical and coding problems.

Towards Reasoning Era: A Survey of Long Chain-of-Thought for Reasoning Large Language Models
 (published 10 months ago)

## Papers Found

- [Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters](https://alphaxiv.org/abs/2408.03314)
- [Recursive Language Models](https://alphaxiv.org/abs/2512.24601)
- [Stop Overthinking: A Survey on Efficient Reasoning for Large Language Models](https://alphaxiv.org/abs/2503.16419)
- [Inference Scaling Laws: An Empirical Analysis of Compute-Optimal Inference for Problem-Solving with Language Models](https://alphaxiv.org/abs/2408.00724)
- [Is PRM Necessary? Problem-Solving RL Implicitly Induces PRM Capability in LLMs](https://alphaxiv.org/abs/2505.11227)
- [Inference-Time Scaling for Diffusion Models beyond Scaling Denoising Steps](https://alphaxiv.org/abs/2501.09732)
- [Large Language Monkeys: Scaling Inference Compute with Repeated Sampling](https://alphaxiv.org/abs/2407.21787)
- [Towards Reasoning Era: A Survey of Long Chain-of-Thought for Reasoning Large Language Models](https://alphaxiv.org/abs/2503.09567)

## Metadata

Timestamp: 2026-01-04T00:58:56.754097

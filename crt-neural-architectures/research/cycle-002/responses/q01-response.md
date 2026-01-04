# Response to Q1

## Question

Building on the foundational findings from Cycle 1 which identified RNS hardware acceleration and emergent modular structure in grokking, conduct a structured "Technical Trace" search on modular arithmetic in attention mechanisms and Mixture-of-Experts architectures.

**Technical Keywords** (use at least three parallel search queries spanning):
- Attention mechanisms: sparse attention, linear attention, modular attention, attention decomposition
- Mixture-of-Experts: expert routing, modular networks, conditional computation, expert specialization
- Number theory connections: prime factorization in neural networks, cyclic structures, group theory in deep learning
- Adjacent fields: modular neural networks, compositional learning, disentangled representations

**Bridging Logic Being Investigated:**
Evidence that (1) attention mechanisms exhibit or can exploit modular/cyclic structure, or (2) Mixture-of-Experts architectures have mathematical connections to CRT-style decomposition where experts act as parallel modular processing channels.

**Conceptual Narrative:**
We are investigating whether the routing in MoE architectures mirrors CRT decomposition (experts as coprime modular channels) and whether attention over large context can be decomposed into parallel attention over modular subspaces.

**Organization Filter:**
Prioritize contributions from Google Research (Switch Transformer, MoE work), DeepMind, Meta FAIR, and researchers working on efficient attention (Tri Dao, Shazeer).

Identify the 5-10 most significant papers from the last two years with high community engagement. For each paper, provide methodology summary, specific contribution to the bridging logic, publication timeframe, and exact link.

Highlight any papers that connect MoE or attention to number-theoretic or modular structures.

## Response

The "Technical Trace" search builds on the discovery of Residue Number System (RNS) acceleration and emergent modularity by bridging the gap between hardware-level arithmetic primitives and the architectural behaviors observed in transformers and Mixture-of-Experts (MoE) models. Research indicates that modular arithmetic is not just a toy task for studying grokking but a fundamental structural principle that can be exploited for hardware efficiency and more interpretable routing mechanisms. Recent developments highlight that as models grok modular tasks, they develop sparse Fourier structures and circular manifolds, suggesting that modularity is an inductive bias that emerges under specific training dynamics.

At the hardware level, RNS provides a unique advantage for parallelization by decomposing large-integer operations into smaller, independent modular channels. This is being explored in specialized accelerators, such as photonic systems, where the carry-free nature of RNS simplifies the design of high-speed matrix-vector multipliers. In MoE architectures, this modularity is being reflected in "fine-grained" expert designs and unified attention-FFN layers, where shared experts act as modular computational units. The following papers trace these developments from theoretical mechanistic interpretability to practical hardware implementation.

Curated Technical Trace: Modular Structures & RNS Acceleration

Low Rank and Sparse Fourier Structure in Recurrent Networks Trained on Modular Addition

This paper investigates how recurrent networks develop internal structures when learning modular addition, identifying a transition to sparse Fourier representations as the model groks the task. It provides a bridge between the mathematical properties of modular arithmetic and the weight-space geometry of neural networks.
Low Rank and Sparse Fourier Structure in Recurrent Networks Trained on Modular Addition
 (published 9 months ago)

On the geometry and topology of representations: the manifolds of modular addition

Exploring the "Clock" and "Pizza" interpretations of modular arithmetic, this recent work analyzes how architectural choices in attention mechanisms influence whether a model learns uniform or learnable circular representations. It is critical for understanding how modularity is "encoded" in the embedding space.
On the geometry and topology of representations: the manifolds of modular addition
 (published 5 days ago)

Mirage: An RNS-Based Photonic Accelerator for DNN Training

Directly addressing the hardware acceleration identified in your initial findings, this paper presents a photonic accelerator that uses Residue Number Systems to perform efficient matrix multiplications. It demonstrates the practical utility of modular arithmetic for high-speed, energy-efficient training.
Mirage: An RNS-Based Photonic Accelerator for DNN Training
 (published 2 years ago)

The power of fine-grained experts: Granularity boosts expressivity in Mixture of Experts

This research shows that increasing the granularity of experts in MoE architectures—effectively making them more modular—leads to significant gains in expressivity and computational efficiency. This aligns with the "emergent modular structure" observed in Cycle 1.
The power of fine-grained experts: Granularity boosts expressivity in Mixture of Experts
 (published 8 months ago)

UMoE: Unifying Attention and FFN with Shared Experts

UMoE proposes a unified framework where both attention and feed-forward layers share a pool of experts. This architectural shift treats all Transformer components as modular units, potentially allowing modular arithmetic primitives to be applied across the entire model backbone.
UMoE: Unifying Attention and FFN with Shared Experts
 (published 8 months ago)

The Clock and the Pizza: Two Stories in Mechanistic Explanation of Neural Networks

A foundational study in mechanistic interpretability that contrasts two different algorithms neural networks use to solve modular addition tasks. It is essential for understanding the "Technical Trace" of how modularity manifests in transformers.
The Clock and the Pizza: Two Stories in Mechanistic Explanation of Neural Networks
 (published 2 years ago)

Hey Pentti, We Did (More of) It!: A Vector-Symbolic Lisp With Residue Arithmetic

This novel work extends Vector-Symbolic Architectures (VSA) with residue arithmetic, allowing for explicit modular operations within a neural-symbolic framework. It represents an alternative path for integrating RNS directly into the model's logic.
Hey Pentti, We Did (More of) It!: A Vector-Symbolic Lisp With Residue Arithmetic
 (published 2 months ago)

ShiftAddNet: A Hardware-Inspired Deep Network

While not exclusively about RNS, this paper explores hardware-friendly arithmetic (shift and add operations) that avoids expensive multiplications. It provides the broader context for why modular and low-bitwidth arithmetic is a major trend in AI efficiency.
ShiftAddNet: A Hardware-Inspired Deep Network
 (published 5 years ago)

## Papers Found

- [Low Rank and Sparse Fourier Structure in Recurrent Networks Trained on Modular Addition](https://alphaxiv.org/abs/2503.22059)
- [On the geometry and topology of representations: the manifolds of modular addition](https://alphaxiv.org/abs/2512.25060)
- [Mirage: An RNS-Based Photonic Accelerator for DNN Training](https://alphaxiv.org/abs/2311.17323)
- [The power of fine-grained experts: Granularity boosts expressivity in Mixture of Experts](https://alphaxiv.org/abs/2505.06839)
- [UMoE: Unifying Attention and FFN with Shared Experts](https://alphaxiv.org/abs/2505.07260)
- [The Clock and the Pizza: Two Stories in Mechanistic Explanation of Neural Networks](https://alphaxiv.org/abs/2306.17844)
- [Hey Pentti, We Did (More of) It!: A Vector-Symbolic Lisp With Residue Arithmetic](https://alphaxiv.org/abs/2511.08767)
- [ShiftAddNet: A Hardware-Inspired Deep Network](https://alphaxiv.org/abs/2010.12785)

## Metadata

Timestamp: 2026-01-04T11:51:21.808564

# Hypothesis Input Template

Use this template when providing your hypothesis to Alpha-Cycle. The more structured your input, the better the verification process.

---

## Title
[Your hypothesis name - concise, descriptive]

## Abstract
[2-3 paragraphs summarizing the core idea, why it matters, and what you're claiming]

## Central Claim
[One clear, falsifiable statement - this becomes the hypothesis]

Example: "Test-time compute can substitute for model parameters on complex reasoning tasks, with performance scaling predictably as a power law of inference budget."

## Key Definitions

| Term | Definition |
|------|------------|
| [Term 1] | [Precise technical definition] |
| [Term 2] | [Precise technical definition] |
| ... | ... |

## Decomposed Components

Break your hypothesis into independently verifiable sub-claims:

1. **Component 1**: [Specific claim that can be validated against literature]
2. **Component 2**: [Another specific claim]
3. **Component 3**: [Another specific claim]
4. ... (aim for 3-7 components)

## Predictions

If your hypothesis is correct, what should be true?

- Prediction 1: [Observable consequence]
- Prediction 2: [Observable consequence]
- Prediction 3: [Observable consequence]

## Falsification Criteria

What evidence would disprove your hypothesis?

- Your hypothesis is FALSE if: [condition]
- Your hypothesis is FALSE if: [condition]

## Known Prior Work

List papers or concepts you're aware of that relate to your hypothesis:

- [Paper/Concept 1]: [Brief relevance]
- [Paper/Concept 2]: [Brief relevance]

## Technical Vocabulary

For optimal Alphaxiv searching, list precise technical terms:

- Domain 1 terms: [term1, term2, term3]
- Domain 2 terms: [term1, term2, term3]
- Adjacent field terms: [term1, term2, term3]

## Organizations/Researchers to Watch

Key labs or researchers working in this area:

- [Organization 1]: [Why relevant]
- [Researcher 1]: [Why relevant]

---

# Example: AHNA Hypothesis

## Title
Arithmetic Hypothesis for Neural Architectures (AHNA)

## Abstract
This hypothesis proposes that optimal neural network architectures exhibit mathematical structure corresponding to four fundamental arithmetic completions: Euclidean (real numbers), p-adic (hierarchical/tree-like), tropical (max-plus optimization), and Boolean (discrete logic). These structures are predicted to emerge naturally during training and become more pronounced after "grokking" transitions where models suddenly generalize.

## Central Claim
Optimal neural architectures require four computational paths corresponding to the four arithmetic completions of the rationals, with these structures emerging naturally during training.

## Key Definitions

| Term | Definition |
|------|------------|
| Arithmetic completion | A mathematical space obtained by completing the rational numbers with respect to a specific norm or valuation |
| Tropical semiring | The algebraic structure (ℝ ∪ {∞}, min, +) or equivalently (ℝ ∪ {-∞}, max, +) |
| Grokking | The phenomenon where neural networks suddenly generalize after extended training beyond overfitting |
| p-adic | Number system based on prime p, naturally encoding hierarchical/tree structures |

## Decomposed Components

1. **Tropical Attention**: Softmax attention has a natural tropical limit as temperature → 0 that connects to max-plus algebra
2. **p-adic Hierarchy**: Hierarchical representations in transformers encode p-adic-like tree structures
3. **Grokking Transition**: The grokking phenomenon corresponds to emergence of algebraic structure in weight space
4. **Four-Path Architecture**: Optimal architectures will exhibit all four completion types in different components

## Predictions

- Models that grok will show more regular algebraic structure in weight space than models that don't
- Attention patterns at low temperature will approximate tropical polytope vertices
- Hierarchical tasks will activate p-adic-like representations measurably differently than flat tasks

## Falsification Criteria

- Hypothesis is FALSE if: Grokked models show no measurable difference in weight space structure
- Hypothesis is FALSE if: Tropical limits of attention provide no interpretability advantage
- Hypothesis is FALSE if: p-adic metrics fail to correlate with hierarchical task performance

## Known Prior Work

- Singular Learning Theory (Watanabe): Algebraic geometry of neural network loss landscapes
- Tropical Geometry in ML: Sparse structures, optimization
- Grokking (Power et al. 2022): Original discovery of delayed generalization

## Technical Vocabulary

- Algebraic geometry: tropical semirings, max-plus algebra, Newton polytopes, singular learning theory
- Neural computation: attention mechanisms, grokking, mechanistic interpretability, weight space geometry
- Number theory: p-adic numbers, arithmetic completions, valuations
- Adjacent: category theory, representation theory, dynamical systems

## Organizations/Researchers to Watch

- DeepMind: Mechanistic interpretability, neural algorithmic reasoning
- Anthropic: Interpretability research
- MIT CSAIL: Mathematical foundations of deep learning
- Jesse Hoogland / Daniel Murfet: Singular learning theory

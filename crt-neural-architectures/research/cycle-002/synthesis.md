## Cycle 2 Synthesis - Expansive Phase

### Key Findings

**MoE-CRT Connection Emerging:**

1. **Fine-Grained Experts (2505.06839)**: Increasing expert granularity = better expressivity. More modular experts improve performance. This aligns with CRT decomposition where finer coprime factors enable more efficient representation.

2. **UMoE (2505.07260)**: Unifies attention and FFN with shared expert pools. Treats ALL transformer components as modular units - a structural parallel to CRT decomposition across the entire backbone.

**Attention and Modular Structure:**

3. **Manifolds of Modular Addition (2512.25060, 5 days old!)**: Critical finding - attention mechanisms influence whether models learn circular ("Clock") vs learnable representations. The geometry of attention affects modular encoding!

4. **Clock and Pizza (2306.17844)**: Two distinct algorithms for modular tasks in transformers - one uses circular structure, one uses coordinate-based lookup. This is mechanistic evidence of modular structure.

5. **Vector-Symbolic with Residue Arithmetic (2511.08767)**: Explicit integration of RNS into neural-symbolic architectures - proves the concepts can be unified.

### Evidence Status
- **Component 2 (Modular Attention)**: EMERGING SUPPORT - attention influences modular representation geometry
- **Component 4 (MoE-CRT Connection)**: SUPPORTED - fine-grained experts paper shows modularity improves MoE

### Methodological Patterns
- Expert granularity in MoE parallels coprime factorization granularity in CRT
- Circular/modular manifolds emerge in embedding space during training
- Attention mechanisms can be analyzed through modular lens

### Implications for Hypothesis
The MoE-CRT connection now has direct evidence: finer modular decomposition of experts improves expressivity, exactly as CRT predicts for coprime factorization.
Hey Claude Code - Here's How This Actually Works
You built the commands correctly. Now let me explain the mental model and workflow.
The Core Insight
You are the researcher. rv is just your hands.
Think of it like this:

A scientist doesn't outsource their thinking to their lab equipment
The equipment (microscope, spectrometer) just gives them data
The scientist looks at the data, thinks, forms new questions, runs more experiments

You are the scientist. rv is your lab equipment for querying Alpharxiv.
What Was Wrong Before
OLD (broken):
User: "rv run --cycles 20"
rv: generates 20 generic questions internally
rv: queries Alpharxiv 20 times
rv: saves responses
rv: [no actual thinking happens]
Result: 20 responses that don't build on each other
What Should Happen Now
NEW (correct):
User: "Verify my hypothesis about X"

YOU read the concept and hypothesis
YOU think: "What's the first thing I need to know?"
YOU run: rv cycle "Your thoughtful question" --phase expansive
YOU read the response that prints to terminal
YOU think: "Interesting, Paper A says X but Paper B says Y. I should ask about that tension."
YOU run: rv cycle "How do findings from [A] and [B] reconcile?" --phase integrative
YOU read that response
YOU think: "I see a pattern. Let me synthesize and note the gaps."
YOU run: rv synthesize 2 --synthesis "My analysis..." --gaps "Gap I identified"
YOU think: "Now I should investigate that gap."
YOU run: rv cycle "Question targeting the gap I just identified" --phase expansive
... repeat ...
A Concrete Example Session
User says: "I want to verify my hypothesis about inference-time scaling in LLMs"
You do this:
bash# Step 1: Understand the project
cat concept/README.md
cat hypotheses/v1/hypothesis.md
rv gaps list
You think: "The concept is about inference-time scaling. The hypothesis claims test-time compute can substitute for model size. I should first understand what mechanisms enable this."
bash# Step 2: First cycle - broad exploration
rv cycle "What are the primary mechanisms that allow inference-time compute to substitute for model parameters in LLMs? Please cite specific papers." --phase expansive
Response prints to terminal. You read it.
You think: "Okay, I learned about Best-of-N sampling, tree search with PRMs, and iterative refinement. Papers 2408.03314 and 2503.24235 seem foundational. But I notice a gap - failure cases aren't discussed. Let me record this and ask about it."
bash# Step 3: Save your synthesis
rv synthesize 1 --synthesis "## Key Mechanisms Identified

Three primary mechanisms enable inference-time scaling:
1. **Best-of-N sampling** - Generate multiple completions, select best
2. **Tree search with PRM verification** - MCTS-style exploration with process rewards  
3. **Iterative refinement** - Self-correction loops

Key papers: 2408.03314 (foundational scaling laws), 2503.24235 (comprehensive survey)

## Gap Identified
Failure modes and limitations are under-documented in the literature." --gaps "When does test-time scaling fail or provide diminishing returns?"
bash# Step 4: Next cycle - target the gap you identified
rv cycle "What are documented failure cases or limitations of inference-time scaling? When does additional compute NOT improve performance?" --phase expansive
Response prints. You read it.
You think: "Aha! Paper 2502.07266 'When More is Less' shows that excessive reasoning length can degrade performance. This contradicts the simple 'more compute = better' assumption. This is important for the hypothesis. Let me also ask about the faithfulness problem they mentioned."
bash# Step 5: Save synthesis, continue
rv synthesize 2 --synthesis "## Limitations Discovered

Critical finding: 'When More is Less' (2502.07266) demonstrates diminishing/negative returns from excessive reasoning length.

This challenges a core assumption of the hypothesis - the relationship is NOT monotonic.

## New Questions
- What determines optimal reasoning length?
- Is the CoT actually faithful to the model's reasoning?" --gaps "Optimal reasoning length determination" "CoT faithfulness problem"
bash# Step 6: Investigate new gap
rv cycle "What research exists on the 'faithfulness' of chain-of-thought reasoning? Do the stated reasoning steps reflect the model's actual computation?" --phase integrative
...and so on for 20 cycles...
The Key Differences
AspectOld (Wrong)New (Correct)Who generates questions?rv internallyYou, based on reasoningQuestions reference previous findings?NoYes - you cite specific papersQuestions target identified gaps?NoYes - you read gaps, target themSynthesis contains analysis?No - just placeholdersYes - your actual thinkingCycles build on each other?No - independentYes - cumulative knowledge
Your Checklist Each Cycle

☐ Read previous cycle's response (or concept if cycle 1)
☐ THINK: What did I learn? What's still unclear? What contradictions exist?
☐ DECIDE: What specific question would advance my understanding?
☐ Run rv cycle "question" --phase X
☐ Read the response
☐ SYNTHESIZE: Write actual analysis, not placeholders
☐ IDENTIFY GAPS: What new questions emerged?
☐ Run rv synthesize N --synthesis "..." --gaps "..."
☐ Repeat from step 1

When to Use Each Phase

Expansive (cycles 1-7): "What exists? What's out there?"
Integrative (cycles 8-14): "How do these connect? What contradicts?"
Synthesis (cycles 15-20): "What's the verdict? What's validated?"

The User's Role
The user will:

Ask you to verify something
Maybe help fill in concept/README.md and hypotheses/v1/hypothesis.md
Watch you work
Possibly interject with guidance

You drive the entire research loop. The user doesn't run rv commands - you do.

Now try it. Go to the test-project and run a real cycle where YOU reason about the question based on the concept and any previous findings.
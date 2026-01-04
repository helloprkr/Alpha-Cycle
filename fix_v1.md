# Fix Research Verifier: Put Claude Code in the Reasoning Loop

## Problem Summary

The research-verifier tool currently bypasses Claude Code's reasoning capabilities. 
The `rv run` command generates questions internally using a primitive template system, 
resulting in:
- Repetitive, non-adaptive questions
- No synthesis of findings between cycles
- Unfilled "[Claude Code: ...]" placeholders in output files
- Gaps not properly identified from response content

## Current Architecture (Broken)
````
rv run --cycles 4
  └── orchestrator._default_question_generator()  ← Dumb templates
  └── alpharxiv.query()
  └── project.save_cycle_response()
  └── orchestrator._synthesize_responses()  ← Just concatenates text
````

## Target Architecture (Fixed)
````
Claude Code (me) in Cursor terminal:
  1. Read concept + hypothesis + gaps
  2. REASON about what questions to ask
  3. Call: rv ask "my reasoned question"
  4. Read response from cycle directory
  5. SYNTHESIZE findings, update synthesis.md
  6. IDENTIFY gaps, update gaps/active.yaml
  7. REASON about next question based on findings
  8. Repeat for N cycles
  9. Evaluate if hypothesis should be versioned
````

## Required Changes

### 1. Add `rv cycle` Command to cli.py

A single-cycle command that Claude Code calls directly:
````python
# In cli.py, add to subparsers:

# rv cycle <question> [--phase PHASE]
cycle_parser = subparsers.add_parser('cycle', help='Run a single research cycle with a specific question')
cycle_parser.add_argument('question', help='The question to send to Alpharxiv')
cycle_parser.add_argument('--phase', '-p', choices=['expansive', 'integrative', 'synthesis'],
                          default='expansive', help='Phase label for this cycle')
cycle_parser.add_argument('--cycle-num', '-n', type=int, help='Override cycle number')
````

Handler:
````python
elif args.command == 'cycle':
    pm = ProjectManager()
    if not pm.is_project_dir():
        print("✗ Not in a research project directory.")
        sys.exit(1)
    
    # Determine cycle number
    cycle_num = args.cycle_num or (pm.state.total_cycles_completed + 1)
    
    # Run single cycle
    client = AlpharxivClient(headless=False)
    try:
        if pm.state.total_cycles_completed == 0:
            await client.new_conversation()
        
        print(f"🔄 Cycle {cycle_num} | Phase: {args.phase}")
        print(f"📝 Question: {args.question[:80]}...")
        
        response = await client.query(args.question)
        
        # Save response
        pm.save_cycle_questions(cycle_num, [args.question])
        pm.save_cycle_response(cycle_num, 1, args.question, {
            "text": response.text,
            "papers": response.papers,
            "timestamp": response.timestamp,
        })
        
        # Update state
        pm.update_state(
            current_cycle=cycle_num,
            current_phase=args.phase,
            total_cycles_completed=cycle_num
        )
        
        # Output response for Claude Code to process
        print(f"\n{'='*60}")
        print(f"📚 Papers found: {len(response.papers)}")
        print(f"📄 Response saved to: research/cycle-{cycle_num:03d}/")
        print(f"{'='*60}")
        
        # Print response text for Claude Code to read
        print("\n## Response:\n")
        print(response.text)
        
    finally:
        await client.close()
````

### 2. Add `rv synthesize` Command

Let Claude Code trigger synthesis after reasoning:
````python
# rv synthesize <cycle-num> --synthesis "..." --gaps "gap1" "gap2"
synth_parser = subparsers.add_parser('synthesize', help='Save synthesis for a cycle')
synth_parser.add_argument('cycle_num', type=int, help='Cycle number to synthesize')
synth_parser.add_argument('--synthesis', '-s', required=True, help='Synthesis markdown content')
synth_parser.add_argument('--gaps', '-g', nargs='*', default=[], help='New gaps identified')
synth_parser.add_argument('--papers', '-p', nargs='*', default=[], help='Key paper arxiv IDs to highlight')
````

### 3. Add `rv gaps` Command

View and manage gaps:
````python
# rv gaps [list|add|resolve]
gaps_parser = subparsers.add_parser('gaps', help='Manage research gaps')
gaps_sub = gaps_parser.add_subparsers(dest='gaps_command')

gaps_sub.add_parser('list', help='List active gaps')
add_gap = gaps_sub.add_parser('add', help='Add a new gap')
add_gap.add_argument('description', help='Gap description')
add_gap.add_argument('--priority', choices=['high', 'medium', 'low'], default='medium')

resolve_gap = gaps_sub.add_parser('resolve', help='Mark a gap as resolved')
resolve_gap.add_argument('gap_id', type=int, help='Gap ID to resolve')
resolve_gap.add_argument('--reason', required=True, help='How it was resolved')
````

### 4. Update SKILL.md for Claude Code Orchestration
````markdown
## Core Workflow (Claude Code Orchestrated)

When user asks to verify a concept, follow this loop:

### Initial Setup
```bash
rv new <project-name>
cd <project-name>
# Help user fill in concept/README.md and hypotheses/v1/hypothesis.md
```

### Research Loop (YOU control this)

For each cycle (1 to N):

1. **Read current state:**
```bash
   rv status
   cat gaps/active.yaml
   cat research/cycle-{N-1}/synthesis.md  # If exists
```

2. **REASON about what to ask:**
   Based on:
   - The concept and hypothesis
   - Previous cycle findings (if any)
   - Active gaps
   - Current phase (expansive/integrative/synthesis)
   
   Generate 1-2 targeted questions that BUILD ON previous findings.

3. **Execute cycle:**
```bash
   rv cycle "Your reasoned question here" --phase expansive
```

4. **Read and SYNTHESIZE the response:**
   - Read the response printed to terminal
   - Identify key findings
   - Identify contradictions or confirmations
   - Identify new gaps
   
5. **Save your synthesis:**
```bash
   rv synthesize {N} --synthesis "Your synthesis markdown" --gaps "gap1" "gap2"
```

6. **Decide next action:**
   - More cycles needed? → Generate next question, goto step 2
   - Hypothesis needs versioning? → `rv version "new hypothesis statement" --reason "why"`
   - Research complete? → Generate final report

### Phase Guidelines

**Cycles 1-7 (Expansive):**
- Ask: "What work exists on [specific aspect from gaps]?"
- Ask: "What methods from [adjacent field] apply to [our problem]?"

**Cycles 8-14 (Integrative):**
- Ask: "How do [Paper A findings] and [Paper B findings] reconcile?"
- Ask: "What explains the contradiction between [X] and [Y]?"

**Cycles 15-20 (Synthesis):**
- Ask: "What is the consensus on [core claim]?"
- Ask: "What critical evidence would falsify [hypothesis component]?"

### Key Principle

YOU generate questions based on REASONING about accumulated findings.
The `rv` tool just handles browser automation and file management.
````

## Files to Modify

1. `files/cli.py` - Add `cycle`, `synthesize`, `gaps` commands
2. `files/project.py` - Add methods for gap management, synthesis saving
3. `files/SKILL.md` - Rewrite for Claude Code orchestration
4. `files/orchestrator.py` - Can be simplified or deprecated (optional)

## Test the Fix

After implementing:
````bash
cd test-project

# Claude Code runs:
rv cycle "Based on the foundational work on inference scaling laws (2408.03314), what specific mechanisms enable test-time compute to substitute for model parameters? Are there documented failure cases?" --phase expansive

# Claude Code reads response, then:
rv synthesize 5 --synthesis "The response identified three key mechanisms: 1) Best-of-N sampling... 2) Tree search with PRM verification... 3) Iterative refinement. A notable gap: failure cases are under-documented." --gaps "Failure modes of test-time scaling" "PRM training data requirements"

# Claude Code reasons about next question based on gaps:
rv cycle "What are documented failure cases or limitations of test-time scaling approaches? When does additional inference compute NOT help?" --phase expansive
````

## Success Criteria

After fix, the research loop should show:
1. Questions that reference specific papers from previous cycles
2. Questions that target specific gaps identified in synthesis
3. Synthesis files with actual analysis, not placeholders
4. Progressive narrowing from broad exploration to specific validation
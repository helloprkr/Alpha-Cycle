"""
Research Orchestrator - Manages the verification cycle loop.

Handles:
- Multi-cycle execution with phase transitions
- Question generation (via Claude Code reasoning)
- Response synthesis
- Checkpoint/resume functionality
- Gap tracking and hypothesis versioning triggers
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass

from .alpharxiv import AlpharxivClient, AlpharxivResponse
from .project import ProjectManager


@dataclass
class CycleResult:
    """Result of a single verification cycle."""
    cycle_num: int
    phase: str
    questions: List[str]
    responses: List[AlpharxivResponse]
    synthesis: str
    new_gaps: List[dict]
    papers_found: List[dict]
    duration_seconds: float


class ResearchOrchestrator:
    """Orchestrates research verification cycles."""
    
    # Phase definitions
    PHASES = {
        "expansive": {
            "description": "Divergent exploration - what else could be relevant?",
            "prompt_suffix": "Focus on breadth. What related work exists? What adjacent fields might inform this? What are we missing?",
        },
        "integrative": {
            "description": "Convergent synthesis - how does this fit together?",
            "prompt_suffix": "Focus on depth. How do these findings connect? What patterns emerge? What contradictions exist?",
        },
        "synthesis": {
            "description": "Reflective assessment - where do we stand now?",
            "prompt_suffix": "Focus on clarity. What do we now know vs. not know? What's validated? What gaps remain?",
        },
    }
    
    def __init__(self, project_manager: ProjectManager, debug: bool = False):
        """
        Initialize orchestrator.

        Args:
            project_manager: ProjectManager instance for the current project
            debug: Enable debug mode for troubleshooting selectors
        """
        self.pm = project_manager
        self.debug = debug
        self.client = AlpharxivClient(headless=False, debug=debug)  # Visible for debugging
        self._question_generator: Optional[Callable] = None
    
    def set_question_generator(self, generator: Callable):
        """
        Set custom question generator function.
        
        The generator receives:
            - concept: str (the concept README)
            - hypothesis: dict (current hypothesis)
            - gaps: List[dict] (active gaps)
            - phase: str (current phase)
            - cycle_num: int
            
        Returns: List[str] of questions
        """
        self._question_generator = generator
    
    async def run_cycles(self, num_cycles: int = 2, 
                        phase_override: Optional[str] = None) -> List[CycleResult]:
        """
        Run multiple verification cycles.
        
        Args:
            num_cycles: Number of cycles to run
            phase_override: Force a specific phase for all cycles
            
        Returns:
            List of CycleResult objects
        """
        results = []
        
        try:
            # Start new Alpharxiv conversation
            await self.client.new_conversation()

            # Only send context recap if we have previous cycles (something to recap)
            if self.pm.state.total_cycles_completed > 0:
                recap = self.pm.get_context_recap()
                print("📋 Sending context recap to Alpharxiv...")
                await self.client.send_context_recap(recap)
            else:
                print("📋 Starting fresh research session...")
            
            for i in range(num_cycles):
                cycle_num = self.pm.state.total_cycles_completed + 1
                
                # Determine phase
                if phase_override:
                    phase = phase_override
                else:
                    # Default phase rotation: expansive → integrative → synthesis
                    phase_idx = i % 3
                    phase = ["expansive", "integrative", "synthesis"][phase_idx]
                
                print(f"\n{'='*60}")
                print(f"🔄 Cycle {cycle_num} | Phase: {phase}")
                print(f"{'='*60}")
                
                result = await self._run_single_cycle(cycle_num, phase)
                results.append(result)
                
                # Update state
                self.pm.update_state(
                    current_cycle=cycle_num,
                    current_phase=phase,
                    total_cycles_completed=cycle_num
                )
                
                # Checkpoint
                self._save_checkpoint(cycle_num, result)
                
                # Check for hypothesis versioning triggers
                if self._should_version_hypothesis(results):
                    print("\n⚡ Significant findings detected - consider versioning hypothesis")
                
        finally:
            await self.client.close()
        
        return results
    
    async def _run_single_cycle(self, cycle_num: int, phase: str) -> CycleResult:
        """Run a single verification cycle."""
        start_time = datetime.now()
        
        # 1. Generate questions
        print(f"\n📝 Generating questions for {phase} phase...")
        questions = self._generate_questions(phase, cycle_num)
        
        # Save questions
        self.pm.save_cycle_questions(cycle_num, questions)
        
        # 2. Query Alpharxiv for each question
        responses = []
        all_papers = []
        
        for q_num, question in enumerate(questions, 1):
            print(f"\n  Q{q_num}/{len(questions)}: {question[:60]}...")
            
            try:
                response = await self.client.query(question)
                responses.append(response)
                all_papers.extend(response.papers)
                
                # Save individual response
                self.pm.save_cycle_response(
                    cycle_num, q_num, question,
                    {
                        "text": response.text,
                        "papers": response.papers,
                        "timestamp": response.timestamp,
                    }
                )
                
                print(f"    ✓ Response received ({len(response.papers)} papers)")
                
            except Exception as e:
                print(f"    ✗ Error: {e}")
                responses.append(AlpharxivResponse(
                    text=f"[Error: {e}]",
                    papers=[]
                ))
            
            # Small delay between questions
            await asyncio.sleep(2)
        
        # 3. Synthesize responses
        print(f"\n🔮 Synthesizing {len(responses)} responses...")
        synthesis, new_gaps = self._synthesize_responses(responses, phase)
        
        # 4. Save cycle artifacts
        self.pm.save_cycle_synthesis(cycle_num, synthesis, new_gaps, all_papers)
        
        duration = (datetime.now() - start_time).total_seconds()
        
        return CycleResult(
            cycle_num=cycle_num,
            phase=phase,
            questions=questions,
            responses=responses,
            synthesis=synthesis,
            new_gaps=new_gaps,
            papers_found=all_papers,
            duration_seconds=duration,
        )
    
    def _extract_topic_from_concept(self, concept: str) -> str:
        """Extract the main research topic from concept text."""
        # Skip common headers and find actual descriptive content
        skip_headers = {'concept', 'core theory', 'key definitions', 'scope', 'overview',
                       'introduction', 'background', 'abstract', 'summary'}

        lines = concept.split('\n')
        for line in lines:
            # Skip empty lines
            line = line.strip()
            if not line:
                continue

            # Skip markdown headers that are generic
            clean = line.lstrip('#').strip().lower()
            if clean in skip_headers:
                continue

            # Skip bullet points and list markers
            if line.startswith('-') or line.startswith('*') or line.startswith('1.'):
                content = line.lstrip('-*0123456789. ').strip()
                if len(content) > 20:  # Substantial content
                    return content[:100]  # Limit length
                continue

            # Found actual content line
            if len(line) > 20 and not line.startswith('#'):
                return line[:100]  # Limit length

            # If it's a header with meaningful content
            if line.startswith('#') and clean not in skip_headers and len(clean) > 10:
                return clean[:100]

        return "machine learning research"  # Fallback

    def _generate_questions(self, phase: str, cycle_num: int) -> List[str]:
        """
        Generate questions for the current phase.

        If a custom generator is set, use it.
        Otherwise, use default question templates.
        """
        concept = self.pm.get_concept()
        hypothesis = self.pm.get_current_hypothesis()
        gaps = self.pm.get_active_gaps()

        if self._question_generator:
            return self._question_generator(
                concept=concept,
                hypothesis=hypothesis,
                gaps=gaps,
                phase=phase,
                cycle_num=cycle_num
            )

        # Default: generate from gaps and phase
        return self._default_question_generator(concept, hypothesis, gaps, phase)
    
    def _default_question_generator(self, concept: str, hypothesis: dict,
                                   gaps: List[dict], phase: str) -> List[str]:
        """Default question generation based on gaps and phase."""
        questions = []
        phase_info = self.PHASES[phase]

        # Extract topic from concept - skip headers and find actual content
        topic = self._extract_topic_from_concept(concept)

        if self.debug:
            print(f"  [DEBUG] Extracted topic: {topic}")

        # Use topic for questions
        key_terms = [topic] if topic else ["this research area"]
        
        if phase == "expansive":
            # Broad exploration questions
            if key_terms:
                questions.append(
                    f"What are the most significant recent papers (last 2 years) related to {key_terms[0]}? "
                    f"Include work from adjacent fields that might offer relevant insights."
                )
            
            for gap in gaps[:2]:
                desc = gap.get('description', '')
                if desc:
                    questions.append(
                        f"What existing research addresses this gap: {desc}? "
                        f"Include both theoretical and empirical work."
                    )
            
        elif phase == "integrative":
            # Synthesis-focused questions
            questions.append(
                f"How do recent findings in {key_terms[0] if key_terms else 'this field'} "
                f"connect to or contradict each other? What patterns emerge?"
            )
            
            if gaps:
                gap_descs = [g.get('description', '') for g in gaps[:3] if g.get('description')]
                if gap_descs:
                    questions.append(
                        f"Is there research that bridges these related gaps: {'; '.join(gap_descs)}?"
                    )
        
        elif phase == "synthesis":
            # Assessment questions
            questions.append(
                f"What is the current consensus on {key_terms[0] if key_terms else 'this topic'}? "
                f"What remains contested or unresolved?"
            )
            
            questions.append(
                "Based on the literature, what are the most critical open problems "
                "and most promising research directions?"
            )
        
        # Ensure at least one question
        if not questions:
            questions.append(
                f"What are the most important recent developments in {key_terms[0] if key_terms else 'this research area'}?"
            )
        
        return questions
    
    def _synthesize_responses(self, responses: List[AlpharxivResponse], 
                             phase: str) -> tuple[str, List[dict]]:
        """
        Synthesize multiple responses into a coherent summary.
        Also identifies new gaps.
        
        Note: In full implementation, this would be done by Claude Code.
        Here we provide a structured template for Claude Code to fill.
        """
        # Aggregate all response text
        all_text = "\n\n---\n\n".join([r.text for r in responses])
        
        # Aggregate papers
        all_papers = []
        for r in responses:
            all_papers.extend(r.papers)
        
        # Create synthesis template (Claude Code will enhance this)
        synthesis = f"""# Cycle Synthesis - {phase.capitalize()} Phase

## Summary

[Claude Code: Synthesize the key findings from this cycle]

## Key Findings

{all_text[:2000]}...

## Papers Collected ({len(all_papers)})

"""
        for paper in all_papers[:10]:
            synthesis += f"- [{paper['title']}]({paper['url']})\n"
        
        synthesis += """
## Patterns Identified

[Claude Code: Identify patterns, convergences, contradictions]

## Implications for Hypothesis

[Claude Code: How do these findings affect the hypothesis?]

## Next Steps

[Claude Code: What should be investigated next?]
"""
        
        # Identify gaps (placeholder - Claude Code will enhance)
        new_gaps = []
        
        # Simple gap detection: look for "open question", "future work", etc.
        gap_indicators = ["open question", "remains unclear", "future work", "not yet understood", "gap in"]
        for indicator in gap_indicators:
            if indicator in all_text.lower():
                new_gaps.append({
                    "description": f"Gap identified via indicator: '{indicator}'",
                    "priority": "medium",
                    "related_components": [],
                })
                break  # Just one gap for now
        
        return synthesis, new_gaps
    
    def _should_version_hypothesis(self, results: List[CycleResult]) -> bool:
        """
        Check if findings warrant a hypothesis version update.
        
        Triggers:
        1. Critical supporting evidence found
        2. Major gap bridged
        3. Contradicting evidence found
        """
        # Simple heuristic: lots of papers + identified gaps
        total_papers = sum(len(r.papers_found) for r in results)
        total_gaps = sum(len(r.new_gaps) for r in results)
        
        return total_papers > 10 and total_gaps > 0
    
    def _save_checkpoint(self, cycle_num: int, result: CycleResult):
        """Save checkpoint for resume capability."""
        checkpoint = {
            "cycle_num": cycle_num,
            "phase": result.phase,
            "timestamp": datetime.now().isoformat(),
            "papers_found": len(result.papers_found),
            "new_gaps": len(result.new_gaps),
        }
        
        checkpoint_path = self.pm.root / "research" / f"cycle-{cycle_num:03d}" / "checkpoint.json"
        checkpoint_path.write_text(json.dumps(checkpoint, indent=2))
    
    async def resume(self):
        """Resume from the last checkpoint."""
        # Find latest checkpoint
        research_dir = self.pm.root / "research"
        checkpoints = sorted(research_dir.glob("cycle-*/checkpoint.json"))
        
        if not checkpoints:
            print("No checkpoints found. Starting fresh.")
            await self.run_cycles()
            return
        
        latest = checkpoints[-1]
        with open(latest) as f:
            checkpoint = json.load(f)
        
        print(f"📍 Resuming from cycle {checkpoint['cycle_num']}")
        
        # Continue from next cycle
        remaining = 20 - checkpoint['cycle_num']
        if remaining > 0:
            await self.run_cycles(num_cycles=remaining)
        else:
            print("All 20 cycles completed.")

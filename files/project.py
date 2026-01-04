"""
Project Manager - Handles directory structure, state, and file operations.

Manages:
- Project initialization with standard structure
- State tracking (current cycle, phase, gaps)
- File I/O for research artifacts
- Hypothesis versioning
"""

import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class ProjectState:
    """Current state of a research project."""
    project_name: str
    current_hypothesis_version: int = 1
    current_cycle: int = 0
    current_phase: str = "expansive"  # expansive, integrative, synthesis
    total_cycles_completed: int = 0
    last_updated: str = ""
    gaps_count: int = 0
    papers_collected: int = 0
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProjectState":
        return cls(**data)


class ProjectManager:
    """Manages research project directory structure and state."""
    
    STATE_FILE = ".research-state.yaml"
    
    # Standard directory structure
    STRUCTURE = {
        "concept": {
            "README.md": "# Concept\n\n## Core Theory\n\n[Describe your theory here]\n\n## Key Definitions\n\n## Scope\n",
        },
        "hypotheses": {
            "v1": {
                "hypothesis.md": "# Hypothesis v1\n\n## Statement\n\n[Your falsifiable hypothesis]\n\n## Components\n\n1. \n2. \n3. \n\n## Predictions\n\n",
                "components.yaml": "# Decomposed verifiable claims\ncomponents:\n  - id: 1\n    claim: \"\"\n    status: untested\n    evidence: []\n",
                "status.yaml": "# Validation status\noverall: untested\ncomponents_validated: 0\ncomponents_total: 0\nlast_updated: \"\"\n",
            }
        },
        "research": {},
        "gaps": {
            "active.yaml": "# Active gaps requiring investigation\ngaps:\n  - id: 1\n    description: \"\"\n    priority: high\n    related_components: []\n    created: \"\"\n",
            "resolved.yaml": "# Resolved gaps\nresolved: []\n",
        },
        "resources": {
            "papers.yaml": "# Collected papers\npapers: []\n",
            "code.yaml": "# Code repositories\nrepos: []\n",
            "downloads": {},
        },
        "tests": {
            "registry.yaml": "# Test registry\ntests: []\n",
            "protocols": {},
        },
        "results": {},
    }
    
    def __init__(self, project_path: Optional[Path] = None):
        """
        Initialize project manager.
        
        Args:
            project_path: Path to project root. If None, uses current directory.
        """
        self.root = Path(project_path) if project_path else Path.cwd()
        self._state: Optional[ProjectState] = None
    
    def is_project_dir(self) -> bool:
        """Check if current directory is a research project."""
        return (self.root / self.STATE_FILE).exists()
    
    def create_project(self, name: str, parent_dir: str = ".") -> Path:
        """
        Create a new research project with standard structure.
        
        Args:
            name: Project name (used as directory name)
            parent_dir: Parent directory to create project in
            
        Returns:
            Path to created project
        """
        parent = Path(parent_dir).resolve()
        project_path = parent / name
        
        if project_path.exists():
            raise ValueError(f"Directory already exists: {project_path}")
        
        # Create directory structure
        self._create_structure(project_path, self.STRUCTURE)
        
        # Create initial state
        state = ProjectState(
            project_name=name,
            last_updated=datetime.now().isoformat()
        )
        
        # Save state
        self.root = project_path
        self._save_state(state)
        
        # Create config file
        config = {
            "project_name": name,
            "created": datetime.now().isoformat(),
            "settings": {
                "cycles_per_run": 20,
                "checkpoint_interval": 5,
                "alpharxiv_timeout": 120,
            }
        }
        (project_path / "config.yaml").write_text(yaml.dump(config, default_flow_style=False))
        
        return project_path
    
    def _create_structure(self, base: Path, structure: dict):
        """Recursively create directory structure."""
        base.mkdir(parents=True, exist_ok=True)
        
        for name, content in structure.items():
            path = base / name
            
            if isinstance(content, dict):
                # It's a directory
                self._create_structure(path, content)
            elif isinstance(content, str):
                # It's a file with content
                path.write_text(content)
            else:
                # Empty directory
                path.mkdir(parents=True, exist_ok=True)
    
    @property
    def state(self) -> ProjectState:
        """Get current project state, loading from disk if needed."""
        if self._state is None:
            self._state = self._load_state()
        return self._state
    
    def _load_state(self) -> ProjectState:
        """Load state from disk."""
        state_path = self.root / self.STATE_FILE
        if not state_path.exists():
            raise ValueError(f"Not a research project: {self.root}")
        
        with open(state_path) as f:
            data = yaml.safe_load(f)
        
        return ProjectState.from_dict(data)
    
    def _save_state(self, state: Optional[ProjectState] = None):
        """Save state to disk."""
        if state is None:
            state = self._state
        if state is None:
            raise ValueError("No state to save")
        
        state.last_updated = datetime.now().isoformat()
        
        state_path = self.root / self.STATE_FILE
        with open(state_path, 'w') as f:
            yaml.dump(state.to_dict(), f, default_flow_style=False)
        
        self._state = state
    
    def update_state(self, **kwargs):
        """Update state fields and save."""
        state = self.state
        for key, value in kwargs.items():
            if hasattr(state, key):
                setattr(state, key, value)
        self._save_state(state)
    
    # === Cycle Management ===
    
    def get_cycle_dir(self, cycle_num: Optional[int] = None) -> Path:
        """Get or create directory for a specific cycle."""
        if cycle_num is None:
            cycle_num = self.state.current_cycle
        
        cycle_dir = self.root / "research" / f"cycle-{cycle_num:03d}"
        cycle_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (cycle_dir / "responses").mkdir(exist_ok=True)
        
        return cycle_dir
    
    def save_cycle_questions(self, cycle_num: int, questions: List[str]):
        """Save questions for a cycle."""
        cycle_dir = self.get_cycle_dir(cycle_num)
        
        content = "# Questions for Cycle {}\n\n".format(cycle_num)
        for i, q in enumerate(questions, 1):
            content += f"## Q{i}\n\n{q}\n\n"
        
        (cycle_dir / "questions.md").write_text(content)
    
    def save_cycle_response(self, cycle_num: int, question_num: int, 
                           question: str, response: dict):
        """Save a single question-response pair."""
        cycle_dir = self.get_cycle_dir(cycle_num)
        responses_dir = cycle_dir / "responses"
        
        # Save as markdown
        content = f"""# Response to Q{question_num}

## Question

{question}

## Response

{response.get('text', '')}

## Papers Found

"""
        for paper in response.get('papers', []):
            content += f"- [{paper['title']}]({paper['url']})\n"
        
        content += f"\n## Metadata\n\nTimestamp: {response.get('timestamp', '')}\n"
        
        (responses_dir / f"q{question_num:02d}-response.md").write_text(content)
        
        # Also save raw JSON for programmatic access
        (responses_dir / f"q{question_num:02d}-response.json").write_text(
            json.dumps(response, indent=2)
        )
    
    def save_cycle_synthesis(self, cycle_num: int, synthesis: str, 
                            new_gaps: List[dict], papers: List[dict]):
        """Save synthesis and update tracking files."""
        cycle_dir = self.get_cycle_dir(cycle_num)
        
        # Save synthesis
        (cycle_dir / "synthesis.md").write_text(synthesis)
        
        # Update papers registry
        self._update_papers(papers)
        
        # Update gaps
        self._update_gaps(new_gaps)
        
        # Save cycle metadata
        metadata = {
            "cycle_num": cycle_num,
            "completed": datetime.now().isoformat(),
            "questions_count": len(list((cycle_dir / "responses").glob("*.md"))),
            "papers_found": len(papers),
            "new_gaps": len(new_gaps),
        }
        (cycle_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))
    
    def _update_papers(self, new_papers: List[dict]):
        """Add new papers to the registry, avoiding duplicates."""
        papers_path = self.root / "resources" / "papers.yaml"
        
        with open(papers_path) as f:
            data = yaml.safe_load(f) or {"papers": []}
        
        existing_urls = {p.get("url") for p in data["papers"]}
        
        for paper in new_papers:
            if paper.get("url") not in existing_urls:
                paper["added"] = datetime.now().isoformat()
                data["papers"].append(paper)
                existing_urls.add(paper.get("url"))
        
        with open(papers_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        
        self.update_state(papers_collected=len(data["papers"]))
    
    def _update_gaps(self, new_gaps: List[dict]):
        """Add new gaps to active gaps."""
        gaps_path = self.root / "gaps" / "active.yaml"
        
        with open(gaps_path) as f:
            data = yaml.safe_load(f) or {"gaps": []}
        
        # Get next ID
        max_id = max([g.get("id", 0) for g in data["gaps"]], default=0)
        
        for gap in new_gaps:
            max_id += 1
            gap["id"] = max_id
            gap["created"] = datetime.now().isoformat()
            data["gaps"].append(gap)
        
        with open(gaps_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        
        self.update_state(gaps_count=len(data["gaps"]))
    
    def get_active_gaps(self) -> List[dict]:
        """Get list of active gaps."""
        gaps_path = self.root / "gaps" / "active.yaml"
        with open(gaps_path) as f:
            data = yaml.safe_load(f) or {"gaps": []}
        return data["gaps"]

    def save_synthesis(self, cycle_num: int, synthesis: str, new_gaps: List[str]):
        """
        Save synthesis for a cycle (Claude Code orchestrated).

        Args:
            cycle_num: Cycle number
            synthesis: Synthesis markdown content
            new_gaps: List of gap descriptions to add
        """
        cycle_dir = self.get_cycle_dir(cycle_num)

        # Save synthesis markdown
        (cycle_dir / "synthesis.md").write_text(synthesis)

        # Add gaps
        for gap_desc in new_gaps:
            self.add_gap(gap_desc, priority="medium")

        # Save cycle metadata
        metadata = {
            "cycle_num": cycle_num,
            "synthesized": datetime.now().isoformat(),
            "new_gaps_added": len(new_gaps),
        }

        # Merge with existing metadata if present
        metadata_path = cycle_dir / "metadata.json"
        if metadata_path.exists():
            existing = json.loads(metadata_path.read_text())
            existing.update(metadata)
            metadata = existing

        metadata_path.write_text(json.dumps(metadata, indent=2))

    def add_gap(self, description: str, priority: str = "medium") -> int:
        """
        Add a single gap to active gaps.

        Args:
            description: Gap description
            priority: Priority level (high, medium, low)

        Returns:
            ID of the newly created gap
        """
        gaps_path = self.root / "gaps" / "active.yaml"

        with open(gaps_path) as f:
            data = yaml.safe_load(f) or {"gaps": []}

        # Get next ID
        max_id = max([g.get("id", 0) for g in data["gaps"]], default=0)
        new_id = max_id + 1

        gap = {
            "id": new_id,
            "description": description,
            "priority": priority,
            "related_components": [],
            "created": datetime.now().isoformat(),
        }
        data["gaps"].append(gap)

        with open(gaps_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)

        self.update_state(gaps_count=len(data["gaps"]))

        return new_id

    def resolve_gap(self, gap_id: int, reason: str):
        """
        Move a gap from active to resolved.

        Args:
            gap_id: ID of the gap to resolve
            reason: How the gap was resolved
        """
        active_path = self.root / "gaps" / "active.yaml"
        resolved_path = self.root / "gaps" / "resolved.yaml"

        # Load active gaps
        with open(active_path) as f:
            active_data = yaml.safe_load(f) or {"gaps": []}

        # Find and remove the gap
        gap_to_resolve = None
        remaining_gaps = []
        for gap in active_data["gaps"]:
            if gap.get("id") == gap_id:
                gap_to_resolve = gap
            else:
                remaining_gaps.append(gap)

        if gap_to_resolve is None:
            raise ValueError(f"Gap #{gap_id} not found in active gaps")

        # Add resolution info
        gap_to_resolve["resolved"] = datetime.now().isoformat()
        gap_to_resolve["resolution"] = reason

        # Save updated active gaps
        active_data["gaps"] = remaining_gaps
        with open(active_path, 'w') as f:
            yaml.dump(active_data, f, default_flow_style=False)

        # Load and update resolved gaps
        with open(resolved_path) as f:
            resolved_data = yaml.safe_load(f) or {"resolved": []}

        resolved_data["resolved"].append(gap_to_resolve)

        with open(resolved_path, 'w') as f:
            yaml.dump(resolved_data, f, default_flow_style=False)

        self.update_state(gaps_count=len(remaining_gaps))

    def get_concept(self) -> str:
        """Get the concept README content."""
        concept_path = self.root / "concept" / "README.md"
        return concept_path.read_text()
    
    def get_current_hypothesis(self) -> dict:
        """Get current hypothesis content."""
        version = self.state.current_hypothesis_version
        hyp_dir = self.root / "hypotheses" / f"v{version}"
        
        return {
            "statement": (hyp_dir / "hypothesis.md").read_text(),
            "components": yaml.safe_load((hyp_dir / "components.yaml").read_text()),
            "status": yaml.safe_load((hyp_dir / "status.yaml").read_text()),
        }
    
    def create_hypothesis_version(self, new_statement: str, reason: str) -> int:
        """Create a new hypothesis version."""
        current = self.state.current_hypothesis_version
        new_version = current + 1
        
        # Copy structure from current version
        current_dir = self.root / "hypotheses" / f"v{current}"
        new_dir = self.root / "hypotheses" / f"v{new_version}"
        new_dir.mkdir(parents=True, exist_ok=True)
        
        # Write new hypothesis
        (new_dir / "hypothesis.md").write_text(new_statement)
        
        # Copy and reset components/status
        components = yaml.safe_load((current_dir / "components.yaml").read_text())
        (new_dir / "components.yaml").write_text(
            yaml.dump(components, default_flow_style=False)
        )
        
        status = {
            "overall": "untested",
            "components_validated": 0,
            "components_total": len(components.get("components", [])),
            "last_updated": datetime.now().isoformat(),
            "version_reason": reason,
            "previous_version": current,
        }
        (new_dir / "status.yaml").write_text(yaml.dump(status, default_flow_style=False))
        
        self.update_state(current_hypothesis_version=new_version)
        
        return new_version
    
    # === Status Display ===
    
    def print_status(self):
        """Print human-readable project status."""
        state = self.state
        
        print(f"\n📊 Research Project: {state.project_name}")
        print("=" * 50)
        print(f"  Hypothesis version: v{state.current_hypothesis_version}")
        print(f"  Current cycle: {state.current_cycle}")
        print(f"  Current phase: {state.current_phase}")
        print(f"  Total cycles completed: {state.total_cycles_completed}")
        print(f"  Papers collected: {state.papers_collected}")
        print(f"  Active gaps: {state.gaps_count}")
        print(f"  Last updated: {state.last_updated}")
        
        # Show recent cycles
        research_dir = self.root / "research"
        cycles = sorted(research_dir.glob("cycle-*"))
        if cycles:
            print(f"\n📁 Recent cycles:")
            for cycle in cycles[-3:]:
                print(f"    {cycle.name}/")
        
        print()
    
    def get_context_recap(self) -> str:
        """
        Generate a context recap for starting a new Alpharxiv conversation.
        Used per Option C (new conversation per phase).
        """
        state = self.state
        hypothesis = self.get_current_hypothesis()
        gaps = self.get_active_gaps()
        
        recap = f"""Research Project: {state.project_name}
Hypothesis Version: v{state.current_hypothesis_version}
Cycles Completed: {state.total_cycles_completed}

Current Hypothesis:
{hypothesis['statement'][:500]}...

Key Active Gaps ({len(gaps)} total):
"""
        for gap in gaps[:5]:
            recap += f"- {gap.get('description', 'No description')}\n"
        
        return recap

#!/usr/bin/env python3
"""
Research Verifier CLI - Automates research verification loops between Claude and Alpharxiv.

Natural commands:
    rv new <project-name>     Create a new research project
    rv ask <question>         Send a question to Alpharxiv and capture response
    rv cycle <question>       Run a single cycle with a specific question (Claude Code orchestrated)
    rv run [--cycles N]       Run N verification cycles (default: 2)
    rv synthesize <N>         Save synthesis for cycle N
    rv gaps [list|add|resolve] Manage research gaps
    rv status                 Show current project status
    rv resume                 Resume from last checkpoint
    rv login                  Open browser for manual Alpharxiv login
"""

import argparse
import asyncio
import sys
from pathlib import Path

from .orchestrator import ResearchOrchestrator
from .alpharxiv import AlpharxivClient
from .project import ProjectManager


def main():
    parser = argparse.ArgumentParser(
        prog='rv',
        description='Research Verifier - Automate research verification loops'
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # rv new <project-name>
    new_parser = subparsers.add_parser('new', help='Create a new research project')
    new_parser.add_argument('name', help='Project name')
    new_parser.add_argument('--path', '-p', default='.', help='Parent directory (default: current)')

    # rv ask <question>
    ask_parser = subparsers.add_parser('ask', help='Send a question to Alpharxiv')
    ask_parser.add_argument('question', nargs='+', help='Question to ask')
    ask_parser.add_argument('--save', '-s', action='store_true', help='Save response to project')

    # rv run
    run_parser = subparsers.add_parser('run', help='Run verification cycles')
    run_parser.add_argument('--cycles', '-c', type=int, default=2, help='Number of cycles (default: 2)')
    run_parser.add_argument('--phase', '-p', choices=['expansive', 'integrative', 'synthesis'], 
                           help='Force a specific phase type')

    # rv status
    subparsers.add_parser('status', help='Show current project status')

    # rv resume
    subparsers.add_parser('resume', help='Resume from last checkpoint')

    # rv login
    login_parser = subparsers.add_parser('login', help='Open browser for Alpharxiv login')
    login_parser.add_argument('--debug', '-d', action='store_true',
                              help='Enable debug mode to show page structure')

    # Global debug flag for run command
    run_parser.add_argument('--debug', '-d', action='store_true',
                            help='Enable debug mode for troubleshooting')

    # rv cycle <question> - Single cycle with specific question (Claude Code orchestrated)
    cycle_parser = subparsers.add_parser('cycle', help='Run a single research cycle with a specific question')
    cycle_parser.add_argument('question', nargs='+', help='The question to send to Alpharxiv')
    cycle_parser.add_argument('--phase', '-p', choices=['expansive', 'integrative', 'synthesis'],
                              default='expansive', help='Phase label for this cycle')
    cycle_parser.add_argument('--cycle-num', '-n', type=int, help='Override cycle number')
    cycle_parser.add_argument('--debug', '-d', action='store_true', help='Enable debug mode')

    # rv synthesize <cycle-num> - Save synthesis for a cycle
    synth_parser = subparsers.add_parser('synthesize', help='Save synthesis for a cycle')
    synth_parser.add_argument('cycle_num', type=int, help='Cycle number to synthesize')
    synth_parser.add_argument('--synthesis', '-s', required=True, help='Synthesis markdown content')
    synth_parser.add_argument('--gaps', '-g', nargs='*', default=[], help='New gaps identified')

    # rv gaps [list|add|resolve] - Manage research gaps
    gaps_parser = subparsers.add_parser('gaps', help='Manage research gaps')
    gaps_sub = gaps_parser.add_subparsers(dest='gaps_command')

    gaps_sub.add_parser('list', help='List active gaps')

    add_gap = gaps_sub.add_parser('add', help='Add a new gap')
    add_gap.add_argument('description', nargs='+', help='Gap description')
    add_gap.add_argument('--priority', choices=['high', 'medium', 'low'], default='medium')

    resolve_gap = gaps_sub.add_parser('resolve', help='Mark a gap as resolved')
    resolve_gap.add_argument('gap_id', type=int, help='Gap ID to resolve')
    resolve_gap.add_argument('--reason', '-r', required=True, help='How it was resolved')

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    # Route to appropriate handler
    asyncio.run(dispatch(args))


async def dispatch(args):
    """Route commands to their handlers."""
    
    if args.command == 'new':
        pm = ProjectManager()
        project_path = pm.create_project(args.name, args.path)
        print(f"✓ Created research project: {project_path}")
        print(f"\nNext steps:")
        print(f"  1. cd {project_path}")
        print(f"  2. Edit concept/README.md with your theory")
        print(f"  3. Run: rv run --cycles 2")

    elif args.command == 'login':
        debug = getattr(args, 'debug', False)
        client = AlpharxivClient(debug=debug)
        await client.login_interactive()
        print("✓ Browser session saved. You can now run automated queries.")

    elif args.command == 'ask':
        question = ' '.join(args.question)
        client = AlpharxivClient()
        print(f"→ Sending to Alpharxiv: {question[:80]}...")
        response = await client.query(question)
        print(f"\n{response['text']}")
        if response['papers']:
            print(f"\n📚 Papers found: {len(response['papers'])}")
            for paper in response['papers'][:5]:
                print(f"  • {paper['title']}: {paper['url']}")

    elif args.command == 'run':
        pm = ProjectManager()
        if not pm.is_project_dir():
            print("✗ Not in a research project directory. Run 'rv new <name>' first.")
            sys.exit(1)

        debug = getattr(args, 'debug', False)
        orchestrator = ResearchOrchestrator(pm, debug=debug)
        await orchestrator.run_cycles(
            num_cycles=args.cycles,
            phase_override=args.phase
        )

    elif args.command == 'status':
        pm = ProjectManager()
        if not pm.is_project_dir():
            print("✗ Not in a research project directory.")
            sys.exit(1)
        pm.print_status()

    elif args.command == 'resume':
        pm = ProjectManager()
        if not pm.is_project_dir():
            print("✗ Not in a research project directory.")
            sys.exit(1)

        orchestrator = ResearchOrchestrator(pm)
        await orchestrator.resume()

    elif args.command == 'cycle':
        # Single cycle with specific question - Claude Code orchestrated
        pm = ProjectManager()
        if not pm.is_project_dir():
            print("✗ Not in a research project directory.")
            sys.exit(1)

        question = ' '.join(args.question)
        cycle_num = args.cycle_num or (pm.state.total_cycles_completed + 1)
        debug = getattr(args, 'debug', False)

        client = AlpharxivClient(headless=False, debug=debug)
        try:
            # Start new conversation if this is first cycle
            await client.new_conversation()

            print(f"\n{'='*60}")
            print(f"🔄 Cycle {cycle_num} | Phase: {args.phase}")
            print(f"{'='*60}")
            print(f"📝 Question: {question[:100]}...")

            response = await client.query(question)

            # Save response
            pm.save_cycle_questions(cycle_num, [question])
            pm.save_cycle_response(cycle_num, 1, question, {
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

            # Update papers registry
            if response.papers:
                pm._update_papers(response.papers)

            # Output for Claude Code to process
            print(f"\n{'='*60}")
            print(f"📚 Papers found: {len(response.papers)}")
            print(f"📄 Response saved to: research/cycle-{cycle_num:03d}/")
            print(f"{'='*60}")

            # Print papers found
            if response.papers:
                print("\n## Papers:")
                for paper in response.papers[:10]:
                    print(f"  • [{paper.get('arxiv_id', 'N/A')}] {paper.get('title', 'Unknown')}")

            # Print response text for Claude Code to read
            print("\n## Response:\n")
            print(response.text)

        finally:
            await client.close()

    elif args.command == 'synthesize':
        # Save synthesis for a cycle
        pm = ProjectManager()
        if not pm.is_project_dir():
            print("✗ Not in a research project directory.")
            sys.exit(1)

        cycle_num = args.cycle_num
        synthesis = args.synthesis
        new_gaps = args.gaps

        # Save synthesis
        pm.save_synthesis(cycle_num, synthesis, new_gaps)

        print(f"✓ Synthesis saved for cycle {cycle_num}")
        if new_gaps:
            print(f"✓ Added {len(new_gaps)} new gaps")

    elif args.command == 'gaps':
        pm = ProjectManager()
        if not pm.is_project_dir():
            print("✗ Not in a research project directory.")
            sys.exit(1)

        if args.gaps_command == 'list' or args.gaps_command is None:
            # List active gaps
            gaps = pm.get_active_gaps()
            if not gaps:
                print("No active gaps.")
            else:
                print(f"\n📋 Active Gaps ({len(gaps)}):\n")
                for gap in gaps:
                    priority = gap.get('priority', 'medium')
                    priority_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(priority, '⚪')
                    print(f"  [{gap.get('id', '?')}] {priority_icon} {gap.get('description', 'No description')}")
                    if gap.get('related_components'):
                        print(f"      └─ Components: {', '.join(map(str, gap['related_components']))}")

        elif args.gaps_command == 'add':
            description = ' '.join(args.description)
            gap_id = pm.add_gap(description, args.priority)
            print(f"✓ Added gap #{gap_id}: {description}")

        elif args.gaps_command == 'resolve':
            pm.resolve_gap(args.gap_id, args.reason)
            print(f"✓ Resolved gap #{args.gap_id}")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Research Verifier CLI - Automates research verification loops between Claude and Alpharxiv.

Natural commands:
    rv new <project-name>     Create a new research project
    rv ask <question>         Send a question to Alpharxiv and capture response
    rv run [--cycles N]       Run N verification cycles (default: 2)
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


if __name__ == '__main__':
    main()

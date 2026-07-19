"""
NEXUS Builder
=============
Private AI Software Engineering Company

Entry point for the NEXUS CLI.

Usage
-----
Interactive mode (default):
    python nexus.py

One-shot scripting:
    python nexus.py --goal "Build a REST API"

After pip install -e .:
    nexus
    nexus --goal "Build a REST API"
    nexus --version
    nexus --workers
    nexus --history
"""

import argparse
import json
import os
import sys

from core.kernel import Kernel
from core.config import Config


# ------------------------------------------------------------------ #
# Version                                                              #
# ------------------------------------------------------------------ #

__version__ = Config.VERSION


# ------------------------------------------------------------------ #
# Banner                                                               #
# ------------------------------------------------------------------ #

BANNER = r"""
 _   _  _______  _____  _    _  _____
| \ | ||  _____||  __ \| |  | |/ ____|
|  \| || |___   | |  | | |  | | (___
| . ` ||  ___|  | |  | | |  | |\___ \
| |\  || |_____ | |__| | |__| |____) |
|_| \_||_______||_____/ \____/|_____/

NEXUS Builder  v{version}
Private AI Software Engineering Company
Owner : {owner}
{line}
"""


def print_banner():
    print(BANNER.format(
        version=__version__,
        owner=Config.OWNER,
        line="=" * 50
    ))


# ------------------------------------------------------------------ #
# Menu                                                                 #
# ------------------------------------------------------------------ #

MENU = """
  [1]  Build a new project
  [2]  View project history
  [3]  List all workers
  [4]  About NEXUS
  [0]  Exit

"""


def show_menu() -> str:
    print(MENU)
    return input("  Select option : ").strip()


# ------------------------------------------------------------------ #
# Actions                                                              #
# ------------------------------------------------------------------ #

def action_build(goal: str | None = None):
    """Run the full enterprise delivery pipeline."""
    from core.orchestrator import Orchestrator

    if not goal:
        print()
        print("  " + "=" * 60)
        print("  PROJECT INTAKE")
        print("  " + "=" * 60)

        while not goal or not goal.strip():
            goal = input("  Enter project goal : ").strip()
            if not goal:
                print("  [!] Goal cannot be empty.")

    orchestrator = Orchestrator()
    orchestrator.run(goal=goal)


def action_history():
    """List all completed projects from the vault."""
    vault = "projects"

    if not os.path.isdir(vault):
        print("\n  No projects found yet.")
        return

    archives = sorted(
        [f for f in os.listdir(vault) if f.endswith(".json")],
        reverse=True
    )

    if not archives:
        print("\n  No completed projects found.")
        return

    print(f"\n  {'Task ID':<20} {'Status':<20} {'Goal'}")
    print("  " + "-" * 72)

    for filename in archives:
        path = os.path.join(vault, filename)
        try:
            with open(path) as f:
                data = json.load(f)
            task_id = data.get("task_id", filename.replace(".json", ""))
            status  = data.get("status", "UNKNOWN")[:18]
            goal    = data.get("goal", "")[:40]
            print(f"  {task_id:<20} {status:<20} {goal}")
        except Exception:
            print(f"  {filename}  [unreadable]")

    print()


def action_workers():
    """Show all registered AI workers."""
    workers = [
        ("PLANNER-001",     "Planner AI",     "Builds a 9-phase execution manifest"),
        ("ARCHITECT-001",   "Architect AI",   "Designs the system blueprint"),
        ("CODER-001",       "Coder AI",       "Generates goal-aware source code"),
        ("REVIEWER-001",    "Reviewer AI",    "AST static analysis + quality gate"),
        ("TESTER-001",      "Tester AI",      "Sandboxed runtime validation"),
        ("SECURITY-001",    "Security AI",    "Vulnerability & secret scanning"),
        ("PERFORMANCE-001", "Performance AI", "Benchmarks + cyclomatic complexity"),
        ("DEVOPS-001",      "DevOps AI",      "Dockerfile, CI/CD, Makefile"),
        ("DEPLOY-001",      "Deployment AI",  "Release packaging & artifact archive"),
        ("MEMORY-001",      "Memory AI",      "Persistent knowledge graph & learning"),
    ]

    print(f"\n  {'ID':<20} {'Worker':<20} {'Responsibility'}")
    print("  " + "-" * 72)

    for wid, name, desc in workers:
        print(f"  {wid:<20} {name:<20} {desc}")

    print()


def action_about():
    """Print the NEXUS constitution summary."""
    about = """
  NEXUS BUILDER — ABOUT
  =====================================================================

  NEXUS is a private AI software engineering company.

  It operates a team of specialised AI workers that plan, design,
  code, review, test, secure, profile, package, deploy, and learn
  from every software project — without human intervention.

  PIPELINE
  --------
  Stage 0  Planner AI       Execution manifest
  Stage 1  Architect AI     System blueprint
  Stage 2  Coder AI         Source code generation
  Stage 3  Reviewer AI      Static analysis
  Stage 4  Tester AI        Runtime validation
  Stage 5  Security AI      Vulnerability scan
  Stage 6  Performance AI   Benchmarks & profiling
  Stage 7  DevOps AI        Infrastructure artefacts
  Stage 8  Deployment AI    Release packaging
  Stage 9  Memory AI        Knowledge graph update

  PRINCIPLES
  ----------
  • Founder first — you always have final authority
  • Quality first — correctness over speed
  • Security first — no exposed secrets or credentials
  • Continuous learning — NEXUS improves with every project
  • Stability — the kernel is never broken by new features

  OUTPUT
  ------
  Every completed project produces a deployment folder containing:
    main.py           Generated source code
    requirements.txt  Runtime dependencies
    README.md         Project documentation
    deployment.json   Release manifest + checksum
    Dockerfile        Container image definition
    Makefile          install / run / test / clean targets
    docker-compose.yml Local development environment
    .github/workflows/ci.yml  GitHub Actions CI pipeline

  =====================================================================
"""
    print(about)


# ------------------------------------------------------------------ #
# CLI Entry Point                                                      #
# ------------------------------------------------------------------ #

def parse_args():
    parser = argparse.ArgumentParser(
        prog="nexus",
        description="NEXUS Builder — Private AI Software Engineering Company",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"NEXUS Builder {__version__}",
    )
    parser.add_argument(
        "--goal", "-g",
        metavar="GOAL",
        help="Skip the menu and immediately build a project with this goal.",
    )
    parser.add_argument(
        "--workers", "-w",
        action="store_true",
        help="List all registered AI workers and exit.",
    )
    parser.add_argument(
        "--history",
        action="store_true",
        help="Show project history and exit.",
    )
    return parser.parse_args()


def main():

    args = parse_args()

    # ── Non-interactive flags ──────────────────────────────────── #

    if args.workers:
        action_workers()
        return

    if args.history:
        action_history()
        return

    if args.goal:
        # Boot kernel silently then run pipeline
        Kernel().boot()
        action_build(goal=args.goal)
        return

    # ── Interactive mode ───────────────────────────────────────── #

    print_banner()
    Kernel().boot()

    while True:

        choice = show_menu()

        if choice == "1":
            action_build()

        elif choice == "2":
            action_history()

        elif choice == "3":
            action_workers()

        elif choice == "4":
            action_about()

        elif choice == "0":
            print("\n  Goodbye. NEXUS shutting down.\n")
            sys.exit(0)

        else:
            print("\n  [!] Invalid option. Please choose 0-4.\n")


if __name__ == "__main__":
    main()

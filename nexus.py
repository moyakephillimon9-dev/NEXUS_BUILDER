"""
NEXUS Builder — Launcher
========================
Boots the kernel, prompts for a project goal, then launches
the full enterprise delivery pipeline.
"""

from core.kernel import Kernel
from core.orchestrator import Orchestrator


def main():

    # ---- Kernel Boot ------------------------------------------------- #

    kernel = Kernel()
    kernel.boot()

    # ---- Interactive Goal Prompt ------------------------------------- #

    print()
    print("=" * 70)
    print("NEXUS BUILDER — PROJECT INTAKE")
    print("=" * 70)

    goal = ""

    while not goal.strip():
        goal = input("Enter project goal : ").strip()

        if not goal:
            print("[!] Goal cannot be empty. Please describe what you want to build.")

    # ---- Launch Orchestrator ----------------------------------------- #

    orchestrator = Orchestrator()
    orchestrator.run(goal=goal)


if __name__ == "__main__":
    main()

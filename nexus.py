"""
NEXUS Builder Launcher
"""

from core.kernel import Kernel


def main():
    kernel = Kernel()
    kernel.boot()


if __name__ == "__main__":
    main()

"""
=========================================================
NEXUS Builder
Core Kernel

Module ID : KERNEL-001
Version   : 0.0.3
=========================================================
"""

from datetime import datetime
from core.logger import Logger


class Kernel:

    VERSION = "0.0.3"

    def __init__(self):
        self.start_time = datetime.now()
        self.running = False
        self.logger = Logger()

    def boot(self):

        print("=" * 60)
        print("NEXUS Builder")
        print(f"Kernel Version : {self.VERSION}")
        print("=" * 60)

        self.logger.info("Kernel Boot Started")

        self.running = True

        self.logger.info("Logger Initialized")

        self.logger.info("System Ready")

        print("=" * 60)

    def shutdown(self):

        self.logger.info("Shutdown Requested")

        self.running = False

        self.logger.info("Kernel Offline")


if __name__ == "__main__":

    kernel = Kernel()

    kernel.boot()

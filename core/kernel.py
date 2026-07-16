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
from core.config import Config
from core.plugin_manager import PluginManager


class Kernel:

    VERSION = "0.0.3"

    def __init__(self):
        self.start_time = datetime.now()
        self.running = False
        self.logger = Logger()
        self.plugin_manager = PluginManager(Config.PLUGIN_FOLDER)

    def boot(self):

        print("=" * 60)
        print("NEXUS Builder")
        print(f"Kernel Version : {self.VERSION}")
        print("=" * 60)

        self.logger.info("Kernel Boot Started")

        self.running = True

        self.logger.info("Logger Initialized")

        self.plugin_manager.discover()

        plugins = self.plugin_manager.list_plugins()

        self.logger.info(f"Plugins Loaded : {len(plugins)}")

        for plugin in plugins:
            self.logger.info(f"Plugin: {plugin}")

        self.logger.info("System Ready")

        print("=" * 60)

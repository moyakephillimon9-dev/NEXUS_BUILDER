from core.config import Config
from core.plugin_manager import PluginManager

manager = PluginManager(Config.PLUGIN_FOLDER)

manager.discover()

manager.print_plugins()

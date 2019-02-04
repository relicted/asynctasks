import importlib
from config.environment import SETTINGS_FILE

settings = importlib.import_module(SETTINGS_FILE)

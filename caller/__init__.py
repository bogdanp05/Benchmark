import os
from caller.config import ConfigMicro, ConfigMacro

LOCATION = os.path.abspath(os.path.dirname(__file__)) + '/'

config_micro = ConfigMicro()
MICRO_FILE = LOCATION + '../config_micro.ini'
config_micro.init_from(file=MICRO_FILE)

config_macro = ConfigMacro()
MACRO_FILE = LOCATION + '../config_macro.ini'
config_macro.init_from(file=MACRO_FILE)

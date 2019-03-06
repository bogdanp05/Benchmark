import os
from config import Config

LOCATION = os.path.abspath(os.path.dirname(__file__)) + '/'

config = Config()
config.init_from(file=LOCATION + '../config.ini')

print(config.levels)

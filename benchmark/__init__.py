import os

FMD_LEVEL = int(os.environ["FMD_LEVEL"]) if "FMD_LEVEL" in os.environ else -1
LOCATION = os.path.abspath(os.path.dirname(__file__)) + '/'

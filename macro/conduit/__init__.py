"""Main application package."""

import os

"""
FMD level and location configuration
"""
FMD_LEVEL = int(os.environ["FMD_LEVEL"]) if "FMD_LEVEL" in os.environ else -1
LOCATION = os.path.abspath(os.path.dirname(__file__)) + '/'
FMD_DB = os.environ["FMD_DB"] if "FMD_DB" in os.environ else None
BM_SPEED = os.environ["BM_SPEED"] if "BM_SPEED" in os.environ else "fast"
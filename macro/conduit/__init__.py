"""Main application package."""

import os

"""
FMD level and location configuration
"""
LOCATION = os.path.abspath(os.path.dirname(__file__)) + '/'
FMD_LEVEL = int(os.environ["FMD_LEVEL"]) if "FMD_LEVEL" in os.environ else -1
FMD_DB = os.environ["FMD_DB"] if "FMD_DB" in os.environ else None

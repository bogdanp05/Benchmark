# -*- coding: utf-8 -*-
"""Create an application instance."""

from macro.conduit.app import create_app
from macro.conduit.settings import ProdConfig

app = create_app(ProdConfig)

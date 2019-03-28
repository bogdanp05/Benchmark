# -*- coding: utf-8 -*-
"""Create an application instance."""

from flask_conduit.conduit.app import create_app
from flask_conduit.conduit.settings import DevConfig

app = create_app(DevConfig)

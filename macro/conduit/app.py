# -*- coding: utf-8 -*-
"""The app module, containing the app factory function.

Do NOT optimize imports using PyCharm's option!!! It will break everything because there's a circular dependency
somewhere and you'll be spending a couple of hours trying to debug it.
"""

from flask import Flask
from macro.conduit.extensions import bcrypt, cache, db, migrate, jwt, cors

from macro.conduit import commands, user, profile, articles, FMD_LEVEL, FMD_DB
from macro.conduit.settings import ProdConfig
from macro.conduit.exceptions import InvalidUsage

# from macro.conduit import FMD_DB, FMD_LEVEL


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[1])
    if FMD_LEVEL > -1:
        print("FMD level: %d" % FMD_LEVEL)
        import flask_monitoringdashboard as dashboard
        if FMD_DB:
            dashboard.config.database_name = FMD_DB
        dashboard.config.monitor_level = FMD_LEVEL
        dashboard.bind(app)

    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(user.views.blueprint, origins=origins)
    cors.init_app(profile.views.blueprint, origins=origins)
    cors.init_app(articles.views.blueprint, origins=origins)

    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(profile.views.blueprint)
    app.register_blueprint(articles.views.blueprint)


def register_errorhandlers(app):

    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': user.models.User,
            'UserProfile': profile.models.UserProfile,
            'Article': articles.models.Article,
            'Tag': articles.models.Tags,
            'Comment': articles.models.Comment,
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)

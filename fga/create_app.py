"""Main Flask app configuration file.

Creates a new instance of our Flask app with plugins, blueprints, views, and configuration loaded.
"""
import logging
import os
from flask_graphql import GraphQLView
from flask_graphql_auth import GraphQLAuth
from flask_migrate import Migrate
from flask_script import Manager
from fga.commands import init_cli
from fga.db import db
from fga.flaskapp import App
from fga.gql import schema
from fga.secret import db_secret_to_url, get_secret, update_app_config

log = logging.getLogger(__name__)
__all__ = "create_app"


def create_app(test_config=None) -> App:
    app = App("fga")

    # load config
    configure(app=app, test_config=test_config)

    # extensions
    configure_database(app)

    # CLI
    manager = Manager(app)

    init_cli(app, manager)

    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view(
            "graphql", schema=schema, graphiql=True, context={"session": db.session}
        ),
    )
    app.url_map.strict_slashes = False

    GraphQLAuth(app)

    app.migrate = Migrate(app, db)

    return app


def configure_database(app):
    """Set up flask with SQLAlchemy."""
    # configure options for create_engine
    engine_opts = app.config.get("SQLALCHEMY_ENGINE_OPTIONS", {})

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = engine_opts

    db.init_app(app)  # init sqlalchemy
    app.migrate = Migrate(app, db)  # alembic

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """Close session after request.

        Ensures no open transactions remain.
        """
        db.session.remove()

    if app.config.get("TESTING"):
        return

    # test_db(app)


def configure_class(app):
    config_class = os.getenv("fga_CONFIG".upper())

    if not config_class:
        # figure out which config to load
        # get stage name
        stage = os.getenv("STAGE")
        if stage:
            # running in AWS or sls wsgi serve
            if stage == "prod":
                config_class = "fga.config.ProdConfig"
            elif stage == "staging":
                config_class = "fga.config.StagingConfig"
            else:
                config_class = "fga.config.DevConfig"
        else:
            # local dev
            config_class = "fga.config.LocalDevConfig"

    app.config.from_object(config_class)


def configure_secrets(app):
    if app.config.get("LOAD_RDS_SECRETS"):
        # fetch db config secrets from Secrets Manager
        secret_name = app.config["RDS_SECRETS_NAME"]
        rds_secrets = get_secret(secret_name=secret_name)
        # construct database connection string from secret
        app.config["SQLALCHEMY_DATABASE_URI"] = db_secret_to_url(rds_secrets)

    if app.config.get("LOAD_APP_SECRETS"):
        # fetch app config secrets from Secrets Manager
        secret_name = app.config["APP_SECRETS_NAME"]
        update_app_config(app, secret_name)


def configure_instance(app):
    # load 'instance.cfg'
    # if it exists as our local instance configuration override
    app.config.from_pyfile("instance.cfg", silent=True)


def configure(app: App, test_config=None):
    configure_class(app)
    config = app.config
    if test_config:
        config.update(test_config)
    else:
        configure_secrets(app)
        configure_instance(app)

    if config.get("SQLALCHEMY_ECHO"):
        logging.basicConfig()
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

    from .config import check_valid

    if not check_valid(config):
        raise Exception("Configuration is not valid.")

import os

CONFIG_EXPECTED_KEYS = ("SQLALCHEMY_DATABASE_URI", "JWT_SECRET_KEY")
# use local "fga" DB for local dev
DEFAULT_DB_URL = "postgresql:///fga"


class Config:
    """Base config."""

    STAGE = os.getenv("STAGE", "Unknown")
    JWT_TOKEN_ARGUMENT_NAME = "token"
    # TODO
    CRUD_ACCESS_CHECKS_ENABLED = False

    # load more config from secrets manager?
    LOAD_APP_SECRETS = os.getenv("LOAD_APP_SECRETS", False)
    LOAD_RDS_SECRETS = os.getenv("LOAD_RDS_SECRET", False)
    SECRETS_NAME = os.getenv("APP_SECRETS_NAME", "fga/dev")
    RDS_SECRETS_NAME = os.getenv("RDS_SECRET_NAME")
    # use aurora data API?
    AURORA_SECRET_ARN = os.getenv("AURORA_SECRET_ARN")
    AURORA_CLUSTER_ARN = os.getenv("AURORA_CLUSTER_ARN")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    AURORA_DATA_API_ENABLED = os.getenv("AURORA_DATA_API_ENABLED", False)

    DEV_DB_SCRIPTS_ENABLED = False  # can init-db/seed/etc be run?

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", DEFAULT_DB_URL)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # set SQL_ECHO=1 this to echo queries to stderr
    SQLALCHEMY_ECHO = bool(os.getenv("SQL_ECHO"))
    DEBUG = os.getenv("DEBUG", False)
    TESTING = bool(os.getenv("TESTING", False))
    XRAY = bool(os.getenv("XRAY"))
    AWS_METRICS_LOGGING = True

    JWT_SECRET_KEY = "f"

    # url to frontend
    UI_URL = "http://localhost:3010"

    # Secrets manager
    SECRETS_SOURCE = "fga/dev"


class LocalDevConfig(Config):
    """Local development environment config."""

    DEBUG = True
    DEV_DB_SCRIPTS_ENABLED = True
    API_SECRET = "unsafe"
    STAGE = "local"
    AWS_METRICS_LOGGING = False


class DevConfig(Config):
    """AWS dev environment and DB."""

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    DEV_DB_SCRIPTS_ENABLED = True
    APP_SECRETS_NAME = "fga/dev"
    LOAD_APP_SECRETS = False
    IGNORE_STRIPE_WEBHOOK_ERRORS = True  # because they get triggered from dev as well


class StagingConfig(Config):
    """AWS staging environment and DB."""

    DEV_DB_SCRIPTS_ENABLED = True
    APP_SECRETS_NAME = "fga/dev"
    LOAD_APP_SECRETS = False
    IGNORE_STRIPE_WEBHOOK_ERRORS = True  # because they get triggered from dev as well


class ProdConfig(Config):
    """AWS production environment and DB."""

    # name of Secrets Manager secretID for config
    APP_SECRETS_NAME = "fga/prod"
    SECRETS_NAME = "fga/prod"
    GITHUB_SECRETS_NAME = "fga/prod"
    LOAD_APP_SECRETS = True
    NPLUSONE_ENABLED = False
    DEV_DB_SCRIPTS_ENABLED = False


# config checks


class ConfigurationInvalidError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message + f"\nEnvironment: {os.environ}"


class ConfigurationKeyMissingError(ConfigurationInvalidError):
    def __init__(self, key: str):
        super().__init__(message=f"Missing {key} key in configuration.")


class ConfigurationValueMissingError(ConfigurationInvalidError):
    def __init__(self, key: str):
        super().__init__(message=f"Missing {key} value in configuration.")


def check_valid(conf) -> bool:
    """Check if config looks okay."""

    def need_key(k):
        if k not in conf:
            raise ConfigurationKeyMissingError(k)
        if not conf.get(k):
            raise ConfigurationValueMissingError(k)

    [need_key(k) for k in CONFIG_EXPECTED_KEYS]
    return True


def check_valid_handler(event, context):
    # which env are we checking?
    config_class = event.get("env", "hr.config.LocalDevConfig")

    # create an app with this config
    from .flaskapp import App

    app = App(__name__)
    app.config.from_object(config_class)
    conf = app.config

    ok = check_valid(conf)

    return dict(ok=ok)

from smart_getenv import getenv


DEBUG = getenv("DEBUG", default=True, type=bool)

PROJECT_NAME = LOGGER_NAME = "graphene_boilerplate"
SECRET_KEY = getenv("SECRET_KEY", default="testsecretkey")

SQLALCHEMY_DATABASE_URI = getenv(
    "SQLALCHEMY_DATABASE_URI", default="postgresql://localhost:5432/fullgraph_alchemist"
)
SQLALCHEMY_TRACK_MODIFICATIONS = getenv(
    "SQLALCHEMY_TRACK_MODIFICATIONS", default=True, type=bool
)

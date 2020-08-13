from jetkit.db import BaseQuery as JKBaseQuery, BaseModel as JKBaseModel, SQLA
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer


class BaseQuery(JKBaseQuery):
    """Base class to use for queries."""


class BaseModel(JKBaseModel):
    """Base class to use for all models."""

    id_ = Column(Integer, primary_key=True, autoincrement=True)
    id = None


# initialize our XRay?FlaskSQLAlchemy instance
db: SQLAlchemy = SQLA(model_class=BaseModel, query_class=BaseQuery)

# load all model classes now
import fga.model  # noqa: F811 F401

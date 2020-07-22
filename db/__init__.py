from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

from app import app


db = SQLAlchemy(app)

Base = declarative_base()
Base.query = db.session.query_property()

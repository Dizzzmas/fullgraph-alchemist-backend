from sqlalchemy import Integer, ForeignKey
from graphene_boilerplate.ext import db


class Item(db.Model):
    __tablename__ = "item"
    key = db.Column(db.String(64), unique=True)
    value = db.Column(db.JSON)
    user = db.relationship("User", back_populates="items")
    user_id = db.Column(
        Integer, ForeignKey("user.id_", ondelete="CASCADE"), nullable=False
    )
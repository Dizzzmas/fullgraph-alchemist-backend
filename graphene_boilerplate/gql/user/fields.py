import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_boilerplate import User


class UserSchema(SQLAlchemyObjectType):
    id_ = graphene.Int(description="user's id")
    full_name = graphene.String(description="user full name")
    email = graphene.String(description="user email")

    class Meta:
        model = User
        interfaces = relay.Node

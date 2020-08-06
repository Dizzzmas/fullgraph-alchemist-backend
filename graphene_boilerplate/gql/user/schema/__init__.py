import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
#from graphene_boilerplate.gql.item.auth import ItemSchema
from graphene_boilerplate.model import User
#from typing import TYPE_CHECKING
#if TYPE_CHECKING:
#    from graphene_boilerplate.gql.item.auth import ItemSchema


class UserSchema(SQLAlchemyObjectType):
    id_ = graphene.ID(description="user's id_")
    full_name = graphene.String(description="user full name")
    email = graphene.String(description="user email")
    #item = graphene.List(graphene.Field(ItemSchema, description="item owned by user"))

    class Meta:
        model = User
        interfaces = (relay.Node,)

import graphene
from graphene import relay

from fga.gql.auth import AuthMutation
from fga.gql.item import ItemQuery, ItemMutation
from fga.gql.user import UserQuery, UserMutation


class MasterQuery(ItemQuery, UserQuery):
    node = relay.Node.Field()


class MasterMutation(ItemMutation, UserMutation, AuthMutation):
    pass


schema = graphene.Schema(query=MasterQuery, mutation=MasterMutation)

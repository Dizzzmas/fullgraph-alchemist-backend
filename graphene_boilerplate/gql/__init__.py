import graphene
from graphene import relay
from graphene_boilerplate.gql.item import ItemQuery, ItemMutation
from graphene_boilerplate.gql.user import UserQuery, UserMutation


class MasterQuery(ItemQuery, UserQuery):
    node = relay.Node.Field()


class MasterMutation(ItemMutation, UserMutation):
    pass


schema = graphene.Schema(query=MasterQuery, mutation=MasterMutation)

import graphene
from fga.gql import MasterQuery
from fga.gql import MasterMutation

schema = graphene.Schema(query=MasterQuery, mutation=MasterMutation)

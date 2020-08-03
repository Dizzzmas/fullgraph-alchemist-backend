import graphene
from graphene_boilerplate.gql.user.queries import resolve_user
from graphene_boilerplate.gql.user.schema import UserSchema


class UserQuery(graphene.ObjectType):
    user = graphene.Field(type=UserSchema, id_=graphene.Int(), resolver=resolve_user)

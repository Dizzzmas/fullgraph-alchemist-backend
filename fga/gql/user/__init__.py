import graphene

from fga.gql.user.mutations import (
    CreateUserMutation,
    CreateUsers,
    DeleteUser,
    UpdateUser,
)
from fga.gql.user.queries import resolve_user
from fga.gql.user.schema import UserSchema


class UserQuery(graphene.ObjectType):
    user = graphene.Field(type=UserSchema, id_=graphene.Int(), resolver=resolve_user)


class UserMutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    create_users = CreateUsers.Field()
    delete_user = DeleteUser.Field()
    update_user = UpdateUser.Field()

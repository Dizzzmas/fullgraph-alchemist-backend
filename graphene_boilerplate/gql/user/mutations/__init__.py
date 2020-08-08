import graphene
from graphene import InputObjectType
from graphene_boilerplate.model import User
from graphene_boilerplate.db import db
from graphene_boilerplate.gql.user.schema import UserSchema


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        full_name = graphene.String()
        user_id = graphene.Int()  # Nani?

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserSchema)

    def mutate(self, info, full_name, user_id):
        user = User(full_name=full_name, user_id=user_id)  # Nani?
        db.session.add(user)
        db.session.commit()
        return CreateUserMutation(ok=True, user=user)  # Nani?


class UserInput(InputObjectType):
    full_name = graphene.String()  # Nani?


class UpdateUser(graphene.Mutation):
    class Arguments:
        full_name = graphene.String()
        id_ = graphene.Int()

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserSchema)

    def mutate(self, info, full_name, id_):
        user = User.query.get(id_)

        if user:
            user.full_name = full_name
        db.session.commit()
        return UpdateUser(ok=True, user=user)  # Nani?


class CreateUsers(graphene.Mutation):
    class Arguments:
        full_name_values = graphene.List(UserInput)

    ok = graphene.Boolean()
    users = graphene.List(lambda: UserSchema)

    def mutate(self, info, full_name_values):
        users = [
            User(full_name=full_name_value.get("full_name"))
            for full_name_value in full_name_values
        ]
        db.session.add_all(users)
        db.session.commit()
        return CreateUsers(ok=True, users=users)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id_ = graphene.Int(required=False)
        full_name = graphene.String(required=False)

    ok = graphene.Boolean()

    def mutate(self, info, **kwargs):
        user = None
        if not kwargs:
            raise Exception("Must provide either id_ or full_name")
        if kwargs.get("id_"):
            user = User.get(kwargs["id_"])
        else:
            user = User.get_by_full_name(kwargs["full_name"])

        if not user:
            raise Exception("User not found")
        user.delete()
        return DeleteUser(ok=True)

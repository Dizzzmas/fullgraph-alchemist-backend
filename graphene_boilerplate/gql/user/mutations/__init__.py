from uuid import uuid4

import graphene
from flask_graphql_auth import create_access_token, create_refresh_token
from graphene import InputObjectType

from graphene_boilerplate.gql.auth.fields import AuthField, ResponseMessageField
from graphene_boilerplate.model import User
from graphene_boilerplate.db import db
from graphene_boilerplate.gql.user.schema import UserSchema


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        full_name = graphene.String()
        user_id = graphene.Int() #Nani?

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserSchema)

    def mutate(self, info, full_name, user_id):
        user = User(full_name=full_name, user_id=user_id) #Nani?
        db.session.add(user)
        db.session.commit()
        return CreateUserMutation(ok=True, user=user) #Nani?


class UserInput(InputObjectType):
    full_name = graphene.String() #Nani?


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
         return UpdateUser(ok=True, user=user) #Nani?


class CreateUsers(graphene.Mutation):
    class Arguments:
        full_name_values = graphene.List(UserInput)

    ok = graphene.Boolean()
    users = graphene.List(lambda: UserSchema)

    def mutate(self, info, full_name_values):
        users = [User(full_name=full_name_value.get("full_name")) for full_name_value in full_name_values]
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


class AuthUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=False)
        _password = graphene.String(required=False)

    ok = graphene.Boolean()

    def mutate(self, info, **kwargs):
        class AuthResponse(Schema):
            access_token = f.String(dump_only=True)
            refresh_token = f.String(dump_only=True)
            user = f.Nested(user_schema)

        @blp.route("login", methods=["POST"])
        @blp.response(AuthResponse)
        @blp.arguments(AuthRequest, as_kwargs=True)
        def login(email: str, password: str):
            """Login with email + password."""
            cleaned_email = email.strip().lower()
            user: AuthModel = auth_model.query.filter_by(email=cleaned_email).one_or_none()
            if not user or not user.password or not user.is_correct_password(password):
                abort(401, message="Wrong user name or password")
            return auth_response_for_user(user)

        @blp.route("check", methods=["GET"])
        @jwt_required
        def check_user():
            """Check if current access token is valid."""
            return "ok"

        @blp.route("refresh", methods=["POST"])
        @jwt_refresh_token_required
        @blp.response(RefreshTokenResponse)
        def refresh_token():
            current_user = get_current_user()
            return {"access_token": create_access_token(identity=current_user)}








       """user = User.objects(**kwargs).first()

        if user is not None:
            access_token = create_access_token(identity=kwargs["id"])
            refresh_token = create_refresh_token(identity=str(uuid4()))

            return AuthUser(AuthField(access_token=access_token, refresh_token=refresh_token, message="Login Success"))
        else:
            return AuthUser(ResponseMessageField(is_success=False, message="Login failed"))"""



from uuid import uuid4
from jetkit.api import abort
import graphene
from flask_graphql_auth import create_access_token, create_refresh_token, mutation_jwt_refresh_token_required, get_jwt_identity
from graphene_boilerplate import User
from graphene_boilerplate.db import db
from graphene_boilerplate.gql.auth.schema import AuthTokensSchema
from graphene_boilerplate.gql.user import UserSchema


class LoginMutation(graphene.Mutation):
    class Arguments(object):
        email = graphene.String()
        password = graphene.String()

    result = graphene.Field(AuthTokensSchema)

    def mutate(self, info, email, password):
        cleaned_email = email.strip().lower()
        user: User = User.query.filter_by(email=cleaned_email).one_or_none()
        if not user or not user.password or not user.is_correct_password(password):
            abort(401, message="Wrong credentials")

        access_token = create_access_token(identity={"email": user.email, "full_name": user.full_name})
        refresh_token = create_refresh_token(identity=str(uuid4()))

        return LoginMutation(AuthTokensSchema(access_token=access_token, refresh_token=refresh_token, message="Login Success"))


class SignUpMutation(graphene.Mutation):

    class Arguments(object):
        email = graphene.String()
        password = graphene.String()

    result = graphene.Field(UserSchema)

    @staticmethod
    def mutate(root, info, email, password):
        cleaned_email = email.strip().lower()

        existing_user: User = User.query.filter_by(
            email=cleaned_email
        ).one_or_none()
        if existing_user:
            abort(400, message="There's already a registered user with this email")

        user = User(email=email, password=password)

        db.session.add(user)
        db.session.commit()

        return SignUpMutation(UserSchema(email=user.email, id_=user.id_, full_name=user.full_name))
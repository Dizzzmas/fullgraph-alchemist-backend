from uuid import uuid4
from jetkit.api import abort
import graphene
from flask_graphql_auth import (
    create_access_token,
    create_refresh_token,
)
from graphene_boilerplate import User
from graphene_boilerplate.db import db
from graphene_boilerplate.gql.auth.fields import AuthField, ResponseMessageField
from graphene_boilerplate.gql.unions import AuthUnion
from graphene_boilerplate.gql.user import UserSchema


class LoginMutation(graphene.Mutation):
    class Arguments(object):
        email = graphene.String()
        password = graphene.String()

    result = graphene.Field(AuthUnion)

    def mutate(self, info, email, password):
        cleaned_email = email.strip().lower()
        user: User = User.query.filter_by(email=cleaned_email).one_or_none()
        if not user or not user.password or not user.is_correct_password(password):
            return LoginMutation(
                ResponseMessageField(is_success=False, message="Login failed")
            )

        access_token = create_access_token(
            identity={"email": user.email, "full_name": user.full_name}
        )
        refresh_token = create_refresh_token(identity=str(uuid4()))

        return LoginMutation(
            AuthField(
                access_token=access_token,
                refresh_token=refresh_token,
                message="Login Success",
            )
        )


class SignUpMutation(graphene.Mutation):
    class Arguments(object):
        email = graphene.String()
        password = graphene.String()

    result = graphene.Field(UserSchema)

    @staticmethod
    def mutate(root, info, email, password):
        cleaned_email = email.strip().lower()

        existing_user: User = User.query.filter_by(email=cleaned_email).one_or_none()
        if existing_user:
            abort(400, message="There's already a registered user with this email")

        user = User(email=email, password=password)

        db.session.add(user)
        db.session.commit()

        return SignUpMutation(
            UserSchema(email=user.email, id_=user.id_, full_name=user.full_name)
        )

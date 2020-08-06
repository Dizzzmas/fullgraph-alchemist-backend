import graphene
from graphene_boilerplate.gql.auth.mutations import LoginMutation, SignUpMutation


class AuthMutation(graphene.ObjectType):
    login = LoginMutation.Field()
    sign_up = SignUpMutation.Field()

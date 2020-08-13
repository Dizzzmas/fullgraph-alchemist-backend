import graphene


class AuthTokensSchema(graphene.ObjectType):
    access_token = graphene.String()
    refresh_token = graphene.String()
    message = graphene.String()


class UserAuthSchema(graphene.ObjectType):
    full_name = graphene.String()
    email = graphene.String()

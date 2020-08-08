import graphene


class ResponseMessageField(graphene.ObjectType):
    is_success = graphene.Boolean()
    message = graphene.String()


class RefreshField(graphene.ObjectType):
    access_token = graphene.String()
    message = graphene.String()

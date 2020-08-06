import graphene
from flask_graphql_auth import AuthInfoField
from graphene_boilerplate.gql.auth.fields import ResponseMessageField, AccountResults, PostResults

# TODO: Make sure unions work properly


class MutationUnion:
    @classmethod
    def resolve_type(cls, instance, info):
        return type(instance)


ResponseUnion = type("ResponseUnion", (MutationUnion, graphene.Union), {
    "Meta": type("Meta", (), {
        "types": (ResponseMessageField, AuthInfoField)
    })
})

AuthUnion = ResponseUnion
RefreshUnion = ResponseUnion
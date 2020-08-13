import graphene
from fga.gql.auth.fields import AuthField
from fga.gql.fields import ResponseMessageField


class MutationUnion:
    @classmethod
    def resolve_type(cls, instance, info):
        return type(instance)


class ResponseUnion(graphene.Union):
    class Meta:
        types = (ResponseMessageField, AuthField)


AuthUnion = ResponseUnion

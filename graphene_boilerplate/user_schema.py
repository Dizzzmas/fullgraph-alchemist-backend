import graphene
from graphene import relay, InputObjectType
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphene_boilerplate.ext import db
from graphene_boilerplate.models import User as UserModel, User


class UserSchema(SQLAlchemyObjectType):
    id_ = graphene.Int(description="user's id")
    full_name = graphene.String(description="user full name")
    email = graphene.String(description="user email")

    class Meta:
        model = UserModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):

    node = relay.Node.Field()
    all_users = graphene.List(
        UserSchema,
        page_size=graphene.Int(required=True),
        page_number=graphene.Int(required=True),
        description="get all users",
    )
    user = graphene.Field(UserSchema, id_=graphene.Int(), description="get a single user", )

    def resolve_user(self, context, **kwargs):
        query = UserSchema.get_query(context)
        for full_name, email in kwargs.users():
            query = query.filter(getattr(User, full_name) == email)
        user = query.first()
        return user


schema = graphene.Schema(query=Query,)
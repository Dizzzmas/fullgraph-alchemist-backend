import json
import os

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from model import Book


class BookSchema(SQLAlchemyObjectType):
    class Meta:
        model = Book
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_books = SQLAlchemyConnectionField(Book.connection)


schema = graphene.Schema(query=Query)

introspection_dict = schema.introspect()
with open(f"{os.getcwd()}/db/schema.json", 'w') as fp:
    json.dump(introspection_dict, fp)
import graphene
from graphene_boilerplate.gql.item.schema import ItemSchema
from graphene_boilerplate.gql.item.mutations import CreateItemMutation
from graphene_boilerplate.gql.item.queries import resolve_item


class ItemQuery(graphene.ObjectType):
    item = graphene.Field(
        type=ItemSchema,
        id_=graphene.Int(required=True),
        resolver=resolve_item,
        description="Get item by id_",
    )


class ItemMutation(graphene.ObjectType):
    create_item = CreateItemMutation.Field()

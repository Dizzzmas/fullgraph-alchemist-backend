import graphene
from fga.gql.item.schema import ItemSchema
from fga.gql.item.mutations import (
    CreateItemMutation,
    CreateItems,
    DeleteItem,
    UpdateItem,
)
from fga.gql.item.queries import resolve_item


class ItemQuery(graphene.ObjectType):
    item = graphene.Field(
        type=ItemSchema,
        id_=graphene.Int(required=True),
        token=graphene.String(),
        resolver=resolve_item,
        description="Get item by id_",
    )


class ItemMutation(graphene.ObjectType):
    create_item = CreateItemMutation.Field()
    create_items = CreateItems.Field()
    delete_item = DeleteItem.Field()
    update_item = UpdateItem.Field()

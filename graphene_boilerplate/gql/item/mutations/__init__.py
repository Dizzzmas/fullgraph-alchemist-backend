import graphene
from graphene import InputObjectType

from graphene_boilerplate.model import Item
from graphene_boilerplate.db import db
from graphene_boilerplate.gql.item.schema import ItemSchema


class CreateItemMutation(graphene.Mutation):
    class Arguments:
        key = graphene.String()
        user_id = graphene.Int()

    ok = graphene.Boolean()
    item = graphene.Field(lambda: ItemSchema)

    def mutate(self, info, key, user_id):
        item = Item(key=key, user_id=user_id)
        db.session.add(item)
        db.session.commit()
        return CreateItemMutation(ok=True, item=item)


class ItemInput(InputObjectType):
     key = graphene.String()


class UpdateItem(graphene.Mutation):
     class Arguments:
         key = graphene.String()
         id_ = graphene.Int()

     ok = graphene.Boolean()
     item = graphene.Field(lambda: ItemSchema)

     def mutate(self, info, key, id_):
         item = Item.query.get(id_)

         if item:
             item.key = key
         db.session.commit()
         return UpdateItem(ok=True, item=item)


class CreateItems(graphene.Mutation):
    class Arguments:
        key_values = graphene.List(ItemInput)

    ok = graphene.Boolean()
    items = graphene.List(lambda: ItemSchema)

    def mutate(self, info, key_values):
        items = [Item(key=key_value.get("key")) for key_value in key_values]
        db.session.add_all(items)
        db.session.commit()
        return CreateItems(ok=True, items=items)


class DeleteItem(graphene.Mutation):
    class Arguments:
        id_ = graphene.Int(required=False)
        key = graphene.String(required=False)

    ok = graphene.Boolean()

    def mutate(self, info, **kwargs):
        item = None
        if not kwargs:
            raise Exception("Must provide either id_ or key")
        if kwargs.get("id_"):
            item = Item.get(kwargs["id_"])
        else:
            item = Item.get_by_key(kwargs["key"])

        if not item:
            raise Exception("Item not found")
        item.delete()
        return DeleteItem(ok=True)
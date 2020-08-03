import graphene
from graphene_boilerplate import Item
from graphene_boilerplate.ext import db
from graphene_boilerplate.gql.item import ItemSchema
from graphene_boilerplate.models import Item as ItemModel, Item


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
            item = ItemModel.get(kwargs["id_"])
        else:
            item = ItemModel.get_by_key(kwargs["key"])

        if not item:
            raise Exception("Item not found")
        item.delete()
        return DeleteItem(ok=True)
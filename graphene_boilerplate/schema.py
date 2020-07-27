import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphene_boilerplate.ext import db
from graphene_boilerplate.models import Item as ItemModel, Item


class ItemSchema(SQLAlchemyObjectType):
    id_ = graphene.Int(description="id of item")

    class Meta:
        model = ItemModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_items = graphene.List(
        ItemSchema,
        id_=graphene.Int(),
        key=graphene.String(),
        value=graphene.JSONString(),
        page_size=graphene.Int(required=True),
        page_number=graphene.Int(required=True),
        description="get all items",
    )
    item = graphene.Field(ItemSchema, id_=graphene.Int(), description="item with id",)

    def resolve_item(self, context, **kwargs):
        query = ItemSchema.get_query(context)
        for key, value in kwargs.items():
            query = query.filter(getattr(Item, key) == value)
        item = query.first()
        return item

    def resolve_all_items(self, context, **kwargs):
        return (
            ItemSchema.get_query(context)
            .limit(kwargs.get("page_size"))
            .offset(kwargs.get("page_size") * kwargs.get("page_number"))
            .all()
        )


class CreateItem(graphene.Mutation):
    class Arguments:
        key = graphene.String()
        value = graphene.JSONString()

    ok = graphene.Boolean()
    item = graphene.Field(lambda: ItemSchema)

    def mutate(self, info, key, value):
        item = ItemModel(key=key, value=value)
        db.session.add(item)
        db.session.commit()
        return CreateItem(ok=True, item=item)


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


class Mutations(graphene.ObjectType):
    create_item = CreateItem.Field()
    delete_item = DeleteItem.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)

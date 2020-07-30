import graphene
from graphene import relay, InputObjectType
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphene_boilerplate.ext import db
from graphene_boilerplate.models import Item as ItemModel, Item
from graphene_boilerplate.models import User as UserModel, User


class ItemSchema(SQLAlchemyObjectType):
    id_ = graphene.Int(description="id of item")
    key = graphene.String(description="item key")
    value = graphene.JSONString(description="dictionary on the item object")

    class Meta:
        model = ItemModel
        interfaces = (relay.Node,)

class UserSchema(SQLAlchemyObjectType):
    id_ = graphene.Int(description="user's id")
    full_name = graphene.String(description="user full name")
    email = graphene.String(description="user email")

    class Meta:
        model = UserModel
        interfaces = (relay.Node,)

class Query(graphene.ObjectType):

    node = relay.Node.Field()
    all_items = graphene.List(
        ItemSchema,
        page_size=graphene.Int(required=True),
        page_number=graphene.Int(required=True),
        description="get all items",
    )
    item = graphene.Field(ItemSchema, id_=graphene.Int(), description="get a single item",)
    user = graphene.Field(ItemSchema, id_=graphene.Int(), description="get a single user",)


    def resolve_item(self, context, **kwargs):
        query = ItemSchema.get_query(context)
        for key, value in kwargs.items():
            query = query.filter(getattr(Item, key) == value)
        item = query.first()
        return item

    def resolve_user(self, context, **kwargs):
        query = UserSchema.get_query(context)
        for full_name, email in kwargs.items():
            query = query.filter(getattr(User, full_name) == email)
        user = query.first()
        return user

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
        items = [ItemModel(key=key_value.get("key")) for key_value in key_values]
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
            item = ItemModel.get(kwargs["id_"])
        else:
            item = ItemModel.get_by_key(kwargs["key"])

        if not item:
            raise Exception("Item not found")
        item.delete()
        return DeleteItem(ok=True)


class Mutations(graphene.ObjectType):
    create_item = CreateItem.Field()
    create_items = CreateItems.Field()
    delete_item = DeleteItem.Field()
    update_item = UpdateItem.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)

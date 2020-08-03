import graphene
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

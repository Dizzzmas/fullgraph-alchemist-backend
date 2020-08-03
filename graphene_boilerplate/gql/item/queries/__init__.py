from graphene_boilerplate.gql.item.fields import ItemSchema
from jetkit.api import abort


def resolve_item(root, context, **kwargs):
    """Get item by id."""
    query = ItemSchema.get_query(context)
    id_ = kwargs.get("id_")

    item = query.get(id_)

    if not item:
        abort(404, message=f"No item with id: {id_}")

    return item


def resolve_all_items(self, context, **kwargs):
         return (
             ItemSchema.get_query(context)
             .limit(kwargs.get("page_size"))
             .offset(kwargs.get("page_size") * kwargs.get("page_number"))
             .all()
         )
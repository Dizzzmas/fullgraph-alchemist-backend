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

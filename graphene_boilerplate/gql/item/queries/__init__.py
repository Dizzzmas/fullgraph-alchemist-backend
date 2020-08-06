from graphene_boilerplate.gql.item.schema import ItemSchema
from jetkit.api import abort
from flask_graphql_auth import query_jwt_required


@query_jwt_required
def resolve_item(root, context, **kwargs):
    """Get item by id_."""
    query = ItemSchema.get_query(context)
    id_ = kwargs.get("id_")
    item = query.get(id_)

    if not item:
        abort(404, message=f"No item with id_: {id_}")

    return item

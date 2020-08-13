from fga.gql.user.schema import UserSchema
from jetkit.api import abort


def resolve_user(root, context, **kwargs):
    """Get user by id_."""
    query = UserSchema.get_query(context)
    id_ = kwargs.get("id_")
    user = query.get(id_)

    if not user:
        abort(404, message=f"No user with id_: {id_}")

    return user

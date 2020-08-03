from graphene_boilerplate.gql.user.fields import UserSchema
from jetkit.api import abort


def resolve_user(root, context, **kwargs):
    """Get user by id."""
    query = UserSchema.get_query(context)
    id_ = kwargs.get("id_")

    user = query.get(id_)

    if not user:
        abort(404, message=f"No user with id: {id_}")

    return user


def resolve_all_items(self, context, **kwargs):
    """Get all users."""
    return (
        UserSchema.get_query(context)
        .limit(kwargs.get("page_size"))
        .offset(kwargs.get("page_size") * kwargs.get("page_number"))
        .all()
    )

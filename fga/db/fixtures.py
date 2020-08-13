from faker import Factory as FakerFactory
from fga.db import db
from fga.model import Item, User
from jetkit.db import Session
import factory


faker: FakerFactory = FakerFactory.create()

DEFAULT_NORMAL_USER_EMAIL = "test@test.com"
DEFAULT_PASSWORD = "testo"


def seed_db():

    if not User.query.filter_by(email=DEFAULT_NORMAL_USER_EMAIL).one_or_none():
        # add default user for testing
        db.session.add(
            UserFactory.create(
                email=DEFAULT_NORMAL_USER_EMAIL,
                password=DEFAULT_PASSWORD,
                full_name="Test User",
            )
        )

    db.session.add_all(UserFactory.create_batch(20))

    db.session.commit()
    print("Database seeded.")


class SQLAFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = Session


class ItemFactory(SQLAFactory):
    class Meta:
        model = Item

    key = factory.Sequence(lambda x: f"{x}-{faker.word()}")
    value = {"asd": "f"}


class UserFactory(SQLAFactory):
    class Meta:
        model = User

    full_name = factory.LazyFunction(faker.name)
    email = factory.Sequence(lambda x: f"{x}-{faker.email()}")
    password = factory.LazyFunction(faker.word)
    items = factory.List([factory.SubFactory(ItemFactory) for _ in range(2)])

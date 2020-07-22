from faker import Factory as FakerFactory
from model import (
    Book
)
import factory
from db import db
from jetkit.db import Session


faker: FakerFactory = FakerFactory.create()


DEFAULT_DEVELOPER_URL = "test"
DEFAULT_DEVELOPER_NAME = "Kostik"

def seed_db():
    # seed DB with factories here
    # https://pytest-factoryboy.readthedocs.io/en/latest/#model-fixture

    # default normal user
    if not Book.query.filter_by(name=DEFAULT_DEVELOPER_URL).one_or_none():
        # add default user for testing
        db.session.add(
            BookFactory.create(
                name=DEFAULT_DEVELOPER_URL, author=DEFAULT_DEVELOPER_NAME, published="Kostik"
            )
        )
        print(
            f"Created developer with url '{DEFAULT_DEVELOPER_URL}' "
            f"with name '{DEFAULT_DEVELOPER_NAME}'"
        )

    db.session.commit()
    print("Database seeded.")


class SQLAFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Use a scoped session when creating factory models."""

    class Meta:
        abstract = True
        sqlalchemy_session = Session


class BookFactory(SQLAFactory):
    class Meta:
        model = Book

    name = factory.LazyAttribute(lambda x: faker.word())
    author = factory.LazyAttribute(lambda x: faker.name())
    published = factory.LazyAttribute(lambda x: faker.word())
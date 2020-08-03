from faker import Factory as FakerFactory
from graphene_boilerplate.ext import db
from graphene_boilerplate.models import Item, User
from jetkit.db import Session
import factory


faker: FakerFactory = FakerFactory.create()


def seed_db():

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

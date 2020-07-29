from faker import Factory as FakerFactory
from graphene_boilerplate.ext import db
from graphene_boilerplate import Item, User
from jetkit.db import Session
import factory


faker: FakerFactory = FakerFactory.create()


def seed_db():

    db.session.add_all(ItemFactory.create_batch(20))

    db.session.commit()
    print("Database seeded.")


class SQLAFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = Session


class UserFactory(SQLAFactory):
    class Meta:
        model = User

    full_name = factory.LazyFunction(faker.name)
    email = factory.Sequence(lambda x: f"{x}-{faker.email}")
    password = factory.LazyFunction(faker.word)


class ItemFactory(SQLAFactory):
    class Meta:
        model = Item

    key = factory.LazyFunction(faker.word)
    value = {"asd": "f"}
    user = factory.SubFactory(UserFactory)

import pytest

from model import Base, engine


@pytest.fixture()
def create_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

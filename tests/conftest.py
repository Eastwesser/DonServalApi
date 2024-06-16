import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.main import app
from tests.config_test import TestConfig
from tests.models_test import TestBase

test_engine = create_engine(TestConfig.TEST_DB_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope='module')
def test_db():
    TestBase.metadata.create_all(bind=test_engine)
    yield TestSessionLocal()
    TestBase.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope='module')
def client():
    with TestClient(app) as c:
        yield c

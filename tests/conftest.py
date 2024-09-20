import pytest
from api.main import app
from api.core.models import Base as MainBase
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tests.config_test import TestConfig
from tests.models_test import Donut

engine = create_engine(TestConfig.TEST_DB_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope='module')
def test_db():
    Donut.metadata.create_all(bind=engine)
    MainBase.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Donut.metadata.drop_all(bind=engine)
        MainBase.metadata.drop_all(bind=engine)


@pytest.fixture(scope='module')
def client():
    with TestClient(app) as c:
        yield c

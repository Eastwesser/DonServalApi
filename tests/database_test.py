from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tests.config_test import TestConfig

test_engine = create_engine(TestConfig.TEST_DB_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

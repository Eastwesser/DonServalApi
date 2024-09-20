import pytest
from fastapi.testclient import TestClient  # Import the TestClient for testing FastAPI apps
from sqlalchemy import create_engine  # Import create_engine to create a connection to the database
from sqlalchemy.orm import sessionmaker  # Import sessionmaker to handle sessions

from api.core.models import Base as MainBase  # Import the Base model from the main app
from api.main import app  # Import the main FastAPI app
from tests.config_test import TestConfig  # Import the test configuration
from tests.models_test import Donut  # Import the Donut model for the tests

# Create a new engine instance bound to the test database
engine = create_engine(TestConfig.TEST_DB_URL)
# Configure the session factory to be used in the test database context
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Fixture to set up and tear down the test database
@pytest.fixture(scope='module')
def test_db():
    # Create all tables defined in the Donut and MainBase metadata
    Donut.metadata.create_all(bind=engine)
    MainBase.metadata.create_all(bind=engine)
    # Create a session for the test database
    db = TestingSessionLocal()
    try:
        yield db  # Yield the database session for use in tests
    finally:
        db.close()  # Close the session after the tests complete
        # Drop all tables created for testing
        Donut.metadata.drop_all(bind=engine)
        MainBase.metadata.drop_all(bind=engine)


# Fixture to set up the FastAPI test client
@pytest.fixture(scope='module')
def client():
    with TestClient(app) as c:  # Create a test client using the FastAPI app
        yield c  # Yield the client for use in tests

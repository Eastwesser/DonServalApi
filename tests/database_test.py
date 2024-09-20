from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tests.config_test import TestConfig  # Import the test configuration

# Create another engine instance for tests
test_engine = create_engine(TestConfig.TEST_DB_URL)
# Session factory for managing test database sessions
TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


# Dependency override to use the test database in tests
def get_test_db():
    db = TestSessionLocal()
    try:
        yield db  # Yield the test database session
    finally:
        db.close()  # Close the session after tests complete

import os

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


# Define the configuration for the test environment
class TestConfig:
    # Load the test database URL from environment variables
    TEST_DB_URL = os.getenv('TEST_DATABASE_URL')

import os

from dotenv import load_dotenv

load_dotenv()


class TestConfig:
    TEST_DB_URL = os.getenv('TEST_DATABASE_URL')

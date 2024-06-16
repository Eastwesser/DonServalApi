from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

TestBase = declarative_base()


class TestDonut(TestBase):
    __tablename__ = "donuts_test"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer)
    image_filename = Column(String, nullable=True)

from sqlalchemy import Integer, String
from sqlalchemy.orm import (
    declarative_base,
    Mapped,
    mapped_column,
)

BaseTestModel = declarative_base()


class Donut(BaseTestModel):
    __tablename__ = "donuts_test"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    image_filename: Mapped[str] = mapped_column(String, nullable=True)

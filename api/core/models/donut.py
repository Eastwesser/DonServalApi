from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Donut(Base):
    __tablename__ = "donuts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    image_filename: Mapped[str] = mapped_column(String, nullable=True)

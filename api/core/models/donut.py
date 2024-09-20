from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


# Define the Donut model (table) for the donuts.
class Donut(Base):
    __tablename__ = "donuts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Unique identifier for each donut.
    name: Mapped[str] = mapped_column(String)  # Name of the donut.
    description: Mapped[str] = mapped_column(String)  # Optional description.
    price: Mapped[int] = mapped_column(Integer)  # Price of the donut.
    image_filename: Mapped[str] = mapped_column(String, nullable=True)  # Filename of the donut's image, if any.

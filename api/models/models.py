from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Donut(Base):
    __tablename__ = "donuts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, index=True)
    price: Mapped[int] = mapped_column(Integer)
    image_filename: Mapped[str] = mapped_column(String, nullable=True)

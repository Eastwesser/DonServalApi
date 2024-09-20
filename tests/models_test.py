from sqlalchemy import Integer, String
from sqlalchemy.orm import (
    declarative_base,  # Import to define the base class for ORM models
    Mapped,  # Type hinting for mapped columns
    mapped_column,  # Use for defining mapped columns in the ORM models
)

# Define the base model class for test models
BaseTestModel = declarative_base()


# Define the Donut model for the test database
class Donut(BaseTestModel):
    __tablename__ = "donuts_test"  # Define the table name in the test database
    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Primary key column
    name: Mapped[str] = mapped_column(String)  # Name column (string)
    description: Mapped[str] = mapped_column(String)  # Description column (string)
    price: Mapped[int] = mapped_column(Integer)  # Price column (integer)
    image_filename: Mapped[str] = mapped_column(String, nullable=True)  # Optional image filename column

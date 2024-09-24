from sqlalchemy.orm import DeclarativeBase


# Define the base class for all SQLAlchemy models in the project.
class Base(DeclarativeBase):
    __abstract__ = True  # This marks the class as abstract,
    # meaning no table will be created for this class itself.

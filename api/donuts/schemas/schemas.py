from typing import Optional

from pydantic import BaseModel


# Schema for creating a new donut.
class DonutCreate(BaseModel):
    name: str
    description: str
    price: int


# Schema for reading donut details (for API responses).
class DonutRead(BaseModel):
    id: int
    name: str
    description: str
    price: int
    image_filename: Optional[str] = None


# Schema for updating an existing donut.
class DonutUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    image_filename: Optional[str] = None

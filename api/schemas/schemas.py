from typing import Optional

from pydantic import BaseModel


class DonutCreate(BaseModel):
    name: str
    description: str
    price: int


class Donut(BaseModel):
    id: int
    name: str
    description: str
    price: int
    image_filename: Optional[str] = None

    class Config:
        from_attributes = True


class DonutUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]
    image_filename: Optional[str]

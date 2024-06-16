from typing import Optional

from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)


class DonutUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    image_filename: Optional[str] = None

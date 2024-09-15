from typing import Optional

from pydantic import BaseModel


class DonutCreate(BaseModel):
    name: str
    description: str
    price: int


class DonutRead(BaseModel):
    id: int
    name: str
    description: str
    price: int
    image_filename: Optional[str] = None


class DonutUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    image_filename: Optional[str] = None

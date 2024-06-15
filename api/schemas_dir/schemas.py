from typing import Optional

from pydantic import BaseModel


class DonutCreate(BaseModel):
    name: str
    description: str


class Donut(BaseModel):
    id: int
    name: str
    description: str
    image_path: Optional[str]

    class Config:
        from_attributes = True

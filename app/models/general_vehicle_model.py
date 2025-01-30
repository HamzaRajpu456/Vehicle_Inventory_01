from sqlmodel import Field, Relationship
from .common import BaseModel
from typing  import List

class General_Vehicles(BaseModel, table = True):
    __tablename__ = "vehicles"

    brand : str = Field(nullable=False, index=True)
    model : str = Field(nullable=False, index=True)
    colour : str = Field(nullable=False)
    make_year : int = Field(nullable=False)
    body_type : str = Field(nullable=False)
    fuel_type : str= Field(nullable=False)
    transmission_type : str = Field(nullable=False)
    total_seats : str = Field(nullable=False)
    price : float = Field(nullable=False)
    engines : List["Engine"] = Relationship (back_populates = "vehicles")
    








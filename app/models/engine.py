    # Assumptions
# 1.create engine model with table true parameter 
# 2.Create entities/fields for tables in the model 
# 3.Create relationshipb between vehicle model & engine(f.key)
# 4.create crud operations for engine data creation and manipulation(think how to do this): 1. new api's 2.add this api's into existing api's
# 5.pending data is  saving successfully in both tables but need do search how to send vehiccles data along side engines with to front end

#  delete all tables in pgadmin but before del table must close program
#  run porgram again and then research 
# 1 :  
# 2: convert data into python lists of tuples 
# 3: then use list comprehensions to convert tuple insides above list into python dict having related tables data 



from sqlmodel import Field, Relationship
from .common import BaseModel
from uuid import  UUID

class Engine(BaseModel, table = True):
    __tablename__ = "engines"

    engine_no : str = Field(nullable = False, index = True)
    engine_type : str = Field(nullable = False)    # V8 or Electric 
    displacement : str = Field(nullable = True)   # 2.0
    horse_power : str = Field(nullable = False)    # 240/260/280
    fuel_efficiency : str = Field(nullable = True)# MPG or Lite per kilometer(L/km) 
    cylinder : str = Field (nullable = True)      # Number of Cylinders
    fuel_type : str = Field(nullable = False)      # Petrole , Diesel , Electric, CNG  
    engine_price : float = Field(nullable = False) 
    vehicle_id : UUID  =  Field(foreign_key = "vehicles.id")
    vehicles : "General_Vehicles" = Relationship(back_populates = "engines")







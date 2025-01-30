from sqlmodel import SQLModel


class Create_Vehicles_Schema(SQLModel):
# Vehicle's Schema :
    brand : str  
    model : str 
    colour : str 
    make_year : int 
    body_type : str 
    fuel_type : str
    transmission_type : str 
    total_seats : str 
    price : float 
# Engine's Schema :
    engine_no :str
    engine_type : str
    displacement : str
    horse_power : str
    fuel_efficiency : str
    cylinder : str
    fuel_type : str
    engine_price: float










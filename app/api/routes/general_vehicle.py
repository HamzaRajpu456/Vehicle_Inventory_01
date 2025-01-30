from fastapi import APIRouter, Depends, HTTPException, status
from app.models.general_vehicle_model import General_Vehicles
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.core.db import get_db_session
from app.schemas.schema import Create_Vehicles_Schema
from uuid import UUID
from app.models.engine import Engine
from app.utills import convert_to_dict


general_vehicle_router = APIRouter(prefix = "/vehicles", tags = ["Vehicles"])

def get_user_auth(db_session : Session = Depends(get_db_session)):
    return db_session

# Route For Create Vehicle:

@general_vehicle_router.post("/")
async def create_vehicle(
    vehicles_data: Create_Vehicles_Schema,
    session: Session = Depends(get_db_session)
):
    try:
        # Convert the validated schema data into a dictionary
        vehicles_data = vehicles_data.model_dump()
        print("Vehicle created Successfully Validated Data:", vehicles_data)

        # Separate general vehicle data and engine data
        general_data = {
            "brand": vehicles_data["brand"],
            "model": vehicles_data["model"],
            "colour": vehicles_data["colour"],
            "make_year": vehicles_data["make_year"],
            "body_type": vehicles_data["body_type"],
            "fuel_type": vehicles_data["fuel_type"],
            "transmission_type": vehicles_data["transmission_type"],
            "total_seats": vehicles_data["total_seats"],
            "price": vehicles_data["price"]
        }
        
        engine_data = {
            "engine_no": vehicles_data["engine_no"],
            "engine_type": vehicles_data ["engine_type"],
            "displacement" : vehicles_data ["displacement"],
            "horse_power" : vehicles_data [ "horse_power"],
            "fuel_efficiency": vehicles_data ["fuel_efficiency"],
            "cylinder" : vehicles_data ["cylinder"],
            "fuel_type" : vehicles_data ["fuel_type"],
            "engine_price": vehicles_data["engine_price"]
        }

        # Create a General_Vehicles instance
        data = General_Vehicles(**general_data)
        session.add(data)
        session.commit()
        session.refresh(data)  # Refresh the vehicle data
        
        # Add vehicle_id to engine_data
        engine_data["vehicle_id"] = data.id

        # Create an Engine instance
        engines_data = Engine(**engine_data)
        session.add(engines_data)
        session.commit()
        session.refresh(engines_data)  # Refresh the engine data

        statement = select(General_Vehicles, Engine).where(data.id == engines_data.vehicle_id)
        results = session.exec(statement)

        veh_data = [
            (vehicle, engine)  
            for vehicle, engine in results]
        
        veh_data_with_engine = convert_to_dict(veh_data)

        print(veh_data_with_engine)

        # Return both refreshed objects in the response
        return {
            "status": True,
            "message": "Vehicle and engine created successfully",
            "data" : veh_data_with_engine}



    # Exception Handling
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating vehicles: {str(e)}"
        )


# Route For Get All Vehicles:

@general_vehicle_router.get('/', response_model = list[General_Vehicles])
async def get_all_vehicles (
    session : Session = Depends(get_db_session)
    ):
  
  try:
    
    statement = select(General_Vehicles)
    vehicles = session.exec(select(statement)).all()
    
    if not vehicles:
       raise HTTPException(
          status_code = status.HTTP_404_NOT_FOUND,
          detail = f"Vehicles not found")
       
    return {"status": True, "vehicles_data":vehicles}

# Exception error Handling:
  
  except Exception as e:
    raise HTTPException(
       
       status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
       detail = f"An error occured while fetching All Vehicles{str(e)}")
    


# Route For Get Single Vehicle:

@general_vehicle_router.get('/{vehicle_id}', response_model = General_Vehicles)
async def  get_single_vehicle(
    vehicle_id: UUID, 
    session: Session = Depends(get_db_session)
    ):
 
 try:  
   
    vehicle = session.get(General_Vehicles, vehicle_id)
    print (vehicle)

    if not vehicle:
        
        raise HTTPException(
          status_code = status.HTTP_404_NOT_FOUND,
          detail = f"Vehicle with ID  {vehicle_id} not found")
    
    return {"status": True, "vehicle_data": vehicle}
 
 except Exception as e:
     
     raise HTTPException(
     status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
     detail = f"An error occured while fetching the vehicle: {str(e)}")


# Route for Delete Vehicles:

@general_vehicle_router.delete('/{vehicle_id}')
async def delete_vehicle(
    vehicle_id : UUID,
    session: Session = Depends(get_db_session)
    ):

    try:

        vehicle = session.get(General_Vehicles, vehicle_id)
        print(vehicle)

        if not vehicle:
           raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Vehicle with ID {vehicle_id} not found")
        
        session.delete(vehicle)
        session.commit()
        print("Vehicle Deleted Successfully!")

        return {"status": True, "deleted_vehicle": vehicle}
    
    except Exception as e:
       session.rollback()
       
       raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"An error occured while deleting the vehicle: { str(e) }")

#  Route for Update Vehicle:

@general_vehicle_router.put('/{vehicle_id}')
async def update_vehicle(
    vehicle_id: UUID, 
    vehicle_data: Create_Vehicles_Schema,
    session: Session = Depends(get_db_session)
    ):

   try:
       
      vehicle = session.get(General_Vehicles, vehicle_id)
      if not vehicle:
           
           raise HTTPException(
              status_code = status.HTTP_404_NOT_FOUND,
              detail = f"Vehicle with ID {vehicle_id} not foumd")
       
      data = vehicle_data.model_dump(exclude_unset = True)
       
      vehicle.sqlmodel_update(data)
       
      session.add(vehicle)
      session.commit()
      session.refresh(vehicle)
      print("Vehicle Updated Successfully!")

      return{"status": True, "Vehicle Updated Successfully" : vehicle}
   
   except Exception as e:
     session.rollback()

     raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail = f"An error occured while updating the vehicle: {str(e)}" )





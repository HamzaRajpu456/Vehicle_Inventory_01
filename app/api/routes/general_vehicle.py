from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.models.general_vehicle_model import General_Vehicles
from sqlmodel import Session, select
from app.core.db import get_db_session
from app.schemas.schema import Create_Vehicles_Schema
from uuid import UUID
from app.models.engine import Engine
from sqlalchemy import asc, func
from sqlalchemy.sql import and_
from typing import Optional

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
# Convert the validated schema data into python dictionary

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

# Create and save General_Vehicles instance

        vehicle_data = General_Vehicles(**general_data)
        session.add(vehicle_data)
        session.commit()
        session.refresh(vehicle_data)  # Refresh the vehicle data
        
# Add vehicle_id to engine_data

        engine_data["vehicle_id"] = vehicle_data.id

# Create and Save Engine instance

        engines_data = Engine(**engine_data)
        session.add(engines_data)
        session.commit()
        session.refresh(engines_data)  # Refresh the engine data

# Fetching the joined data using SQLModel

        statement = select(General_Vehicles, Engine).join(Engine, Engine.vehicle_id == General_Vehicles.id).where(General_Vehicles.id == vehicle_data.id)
        results = session.exec(statement).all()


        veh_data_with_engines = [ 
            { 
                "vehicle": {
                    "id": vehicle.id,
                    "brand": vehicle.brand,
                    "model": vehicle.model,
                    "colour": vehicle.colour,
                    "make_year": vehicle.make_year,
                    "body_type": vehicle.body_type,
                    "fuel_type": vehicle.fuel_type,
                    "transmission_type": vehicle.transmission_type,
                    "total_seats": vehicle.total_seats,
                    "price": vehicle.price,
                    "engine": {
                    "engine_no": engine.engine_no,
                    "engine_type": engine.engine_type,
                    "displacement": engine.displacement,
                    "horse_power": engine.horse_power,
                    "fuel_efficiency": engine.fuel_efficiency,
                    "cylinder": engine.cylinder,
                    "fuel_type": engine.fuel_type,
                    "engine_price": engine.engine_price}
                },

                
            }
            for vehicle, engine in results
        ]

        print(veh_data_with_engines)

# Return both refreshed objects in the response

        return {
            "status": True,
            "message": "Vehicle and engine created successfully",
            "data" : veh_data_with_engines[0]}



# Exception Handling

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating vehicles: {str(e)}"
        )


# Route For Get All Vehicles:

@general_vehicle_router.get('/')
async def get_all_vehicles(
    session: Session = Depends(get_db_session),
    limit: int = Query(7, ge=1, le=50),  # Limit between 1 and 50 (default: 7)
    offset: int = Query(0, ge=0)  # Offset starts from 0
):
    try:
        # Correct way to count total vehicles
        total_count = session.exec(select(General_Vehicles)).all()
        total_count = len(total_count)  # Get total number of rows

        # Fetch vehicles with limit & offset
        statement = select(General_Vehicles).order_by(General_Vehicles.make_year.asc()).limit(limit).offset(offset)
        vehicles = session.exec(statement).all()

        # Debugging: Print fetched data
        print("Fetched Vehicles:", vehicles)

        # If no vehicles are found, return a 404 error
        if not vehicles:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No vehicles found"
            )

        return {
            "status": True,
            "vehicles": vehicles,
            "limit": limit,
            "offset": offset,
            "total_results": total_count,
            "total_pages": (total_count // limit) + (1 if total_count % limit > 0 else 0),
            "message": "Vehicles fetched successfully."
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching vehicles: {str(e)}"
        )


        
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









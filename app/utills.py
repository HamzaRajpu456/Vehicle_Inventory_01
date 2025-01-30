def convert_to_dict(data):
    result = []
    for vehicle_data in data:
        vehicle_dict = {
            'vehicle': vehicle_data["General_Vehicles"],
            'engine': vehicle_data["Engine"]
        }
        result.append(vehicle_dict)
    return result
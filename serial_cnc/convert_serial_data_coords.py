""" Takes the Serial Port Input of
    some data Coords, min, max, current, etc.
    And convert them in a python tuple
"""

def convert_serial_data_coords (serial_input):
    """ Takes the Serial Port Input of
        some data Coords, min, max, current, etc.
        And convert them in a python tuple
    """
    # Decode and clear the Data_Cords
    data_coords = serial_input.split(";")
    data_coords.pop(0) # Delete Data Header
    data_coords.pop() # Delete \n\r

    # Convert str -> float
    data_coords = [float(coord) for coord in data_coords]

    return tuple(data_coords)

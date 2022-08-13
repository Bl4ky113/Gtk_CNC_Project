""" Takes a G-Code Line from a G-Code File and 
    returns its X, Y and Z Coords
"""

# Import Regex Lib
from re import match

def convert_gcode_line_data_coords (gcode_line, axis_names):
    """ Takes a G-Code Line from a G-Code File and
        returns its X, Y and Z Coords in a tuple
    """

    # Check if G-Code Line has the right format
    line_match = match(r"^G1 X\d* Y\d* Z\*$", gcode_line)

    if gcode_line == "" and not line_match:
        return

    # Split into array and delete header (G1)
    gcode_data = gcode_line.split(" ")
    gcode_data.pop(0)

    # Generate G-Code Coords with a List Comprehesion
    gcode_coords = [float(coord[1:]) for coord in gcode_data]

    return tuple(gcode_coords)

""" Serial Comunication Module. Send and get data from the CNC Plotter """

# Import asyncio Module
import asyncio
# Import pySerial Module
from serial import Serial

# Import App Modules

from .convert_serial_data_coords import convert_serial_data_coords
from .convert_gcode_line_data_coords import convert_gcode_line_data_coords

class SerialCNC (Serial):
    """ Serial Port Class of the CNC Plotter """
    def __init__ (self, port_name):
        super().__init__(port_name)

        # Configure the Serial Port and set intial Values

        self.axis_names = ("x", "y", "z")
        self.home_coords = (20, 20, 1)
        self.serial_output = []

        # Get Serial Output Initial Data
        for _ in range(3):
            self.serial_output.append(self.readline().decode("ascii"))

        self.min_coords = convert_serial_data_coords(self.serial_output[0])
        self.max_coords = convert_serial_data_coords(self.serial_output[1])
        self.current_coords = convert_serial_data_coords(self.serial_output[2])
        self.steps_coords = (5, 5, 1)
        self.is_active = False

        self.timeout = 0.5
        self.write_timeout = 0.5

    @property
    def data (self):
        """ General data and settings of the CNC Serial Port """

        # Create dict with general data
        data = {
                "name": self.name,
                "home": self.home_coords,
                "coords": self.current_coords,
                "min_coords": self.min_coords,
                "max_coords": self.max_coords,
                "step_coords": self.steps_coords,
                "is_open": self.is_open
                }

        # Merge general data dict and settings dict
        data = data | self.get_settings()

        return data

    def axis_movement_cnc (self, axis, negative=False):
        """ Simple movement on one axis of the CNC Plotter
            no greater than the max and min limits.
            Can go backwards or negative in the axis.
        """

        # Init values
        axis_index = self.axis_names.index(axis)
        new_coords = list(self.current_coords).copy()
        orientation = 1 if not negative else -1 # 1 normal, -1 backwards

        # add steps towards direction on new_coords axis_index
        new_coords[axis_index] = (new_coords[axis_index]) + (orientation * self.steps_coords[axis_index])

        # See if the new_coord axis value is out of limits
        # Change it to the nearst limit
        if new_coords[axis_index] > self.max_coords[axis_index]:
            new_coords[axis_index] = self.max_coords[axis_index]
        elif new_coords[axis_index] < self.min_coords[axis_index]:
            new_coords[axis_index] = self.min_coords[axis_index]

        # Set active True, send the move message and set current coords to new_coords
        self.is_active = True
        asyncio.run(self.send_move_message_to_cnc(new_coords))
        self.current_coords = tuple(new_coords)

    def go_home_cnc (self, set_home=False):
        """ Moves the CNC Plotter to the Home Coords, defined by the user.
            If setting home, it'll change Home Coords by the current_coords and
            then "moves" there.
        """

        if set_home:
            self.home_coords = self.current_coords

        new_coords = list(self.home_coords).copy()

        # Set active True, send the move message and set current coords to new_coords
        self.is_active = True
        asyncio.run(self.send_move_message_to_cnc(new_coords))
        self.current_coords = tuple(new_coords)

    async def send_move_message_to_cnc (self, coords):
        """ Generates a G-Code Line with the given CNC Plotter Coords.
            Sends this G-Code to the CNC Serial Port, then waits for a
            response, which is stored in serial output, and sets the
            Serial Port inactive
        """

        # Generate G-Code Line Message
        gcode_message = f"G1 X{coords[0]} Y{coords[1]} Z{coords[2]}\n".encode("ascii")

        # Send G-Code Line Message, and wait for response
        self.serial_output.append("> " + gcode_message.decode("ascii"))
        self.write(gcode_message)
        self.serial_output.append(self.readline().decode("ascii"))

        self.is_active = False

    def get_serial_output (self):
        """ Get Serial Output, skip if it's empty,
            then return all recorded serial output as a str
        """
        output = self.readline().decode("ascii")

        if output != "":
            self.serial_output.append(output)

        serial_output_str = "".join(self.serial_output)

        return serial_output_str

    def clear_serial_output (self):
        """ Clear stored Serial Output """
        self.serial_output = []

    def process_gcode_line (self, gcode_line):
        """ Takes a G-Code Line from a G-Code File, gets its Coords,
            creates a new_coords to send to the CNC Plotter. And then
            updates the current coords with the new-coords
        """
        # Get New Coords from G-Code Line
        new_coords = convert_gcode_line_data_coords(gcode_line, self.axis_names)

        if not new_coords: # Check if there's new_coords available
            return

        print("in", new_coords)
        # Set active True, send the move message and set current coords to new_coords
        self.is_active = True
        asyncio.run(self.send_move_message_to_cnc(new_coords))
        self.current_coords = tuple(new_coords)
        print("out", new_coords)

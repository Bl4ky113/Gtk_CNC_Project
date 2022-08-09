""" Serial Comunication Module. Send and get data from the CNC Plotter """

# Import asyncio Module
import asyncio
# Import pySerial Module
from serial import Serial

# Import App Modules

from .convert_serial_data_coords import convert_serial_data_coords

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
        self.new_coords = list(self.current_coords).copy()
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

    def simple_move_cnc (self, axis, negative=False):
        """ Simple move the cnc, in one axis,
            a number of steps no greater than the max_coords.
            If negative, goes in the negative direction of the axis.
        """
        if self.is_active: # Avoid moving while it's waiting for the new_current_coords
            return

        # Init Values: Index of the Axis,
        # negative axis direction, and  new_coords list
        axis_index = self.axis_names.index(axis)
        negative_direction = 1 if not negative else -1
        self.new_coords = list(self.current_coords).copy()

        # add steps with negative direction
        self.new_coords[axis_index] += (negative_direction * self.steps_coords[axis_index])

        # check if new_coord is in range of the CNC
        # if not set new_coord to min or max limit
        if self.new_coords[axis_index] > self.max_coords[axis_index]:
            self.new_coords[axis_index] = self.max_coords[axis_index]
        elif self.new_coords[axis_index] < self.min_coords[axis_index]:
            self.new_coords[axis_index] = self.min_coords[axis_index]       

        asyncio.run(self.generate_move_message(*self.new_coords))

    def go_home_cnc (self, set_home=False):
        """ Calcs how far is home from the current coords, then simple-moves there.
            If set_home, will set the home on the current coords, and move there as well.
        """
        if self.is_active: # Avoid moving while it's waiting for the new_current_coords
            return

        if set_home:
            self.home_coords = tuple(list(self.current_coords).copy())

        self.new_coords = list(self.home_coords).copy()

        self.is_active = True
        asyncio.run(self.generate_move_message(*self.new_coords))

    async def generate_move_message (self, x_coord, y_coord, z_coord):
        """ Generates the move message with the new_coords, to send it to the CNC Plotter """
        message = f"G1 X{x_coord} Y{y_coord} Z{z_coord}\n".encode("ascii")
        print(self.new_coords)
        await self.send_move_message_to_cnc(message)
        self.current_coords = tuple([x_coord, y_coord, z_coord])

    async def send_move_message_to_cnc (self, message):
        """ Sends a G-Code Line with new_Coords for the CNC Plotter,
            gets, and returns, the new current_coords of the CNC Plotter
        """
        self.write(message)
        raw_serial_output = self.readline().decode("ascii")
        self.write("\0".encode("ascii"))

        self.serial_output.append(raw_serial_output)
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

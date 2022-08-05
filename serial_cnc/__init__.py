""" Serial Comunication Module. Send and get data from the CNC Plotter """

# Import pySerial Module
from serial import Serial

class Serial_CNC (Serial):
    """ Serial Port Class of the CNC Plotter """
    def __init__ (self, port_name):
        super().__init__(port_name)

        # Configure the Serial Port

        # Set CNC Cords
        self.home_cords = (12, 23, 0)
        self.current_cords = (2, 5, 1)
        self.max_cords = (40, 40, 1)

        # Set Write / Read timeout For avoiding DataOverflow
        self.timeout = 0.5
        self.write_timeout = 1

    @property
    def data (self):
        """ General data and settings of the CNC Serial Port """

        # Create dict with general data
        data = {
                "name": self.name,
                "home": self.home_cords,
                "cords": self.current_cords,
                "max_cords": self.max_cords,
                "is_open": self.is_open
                }

        # Merge general data dict and settings dict
        data = data | self.get_settings()

        return data


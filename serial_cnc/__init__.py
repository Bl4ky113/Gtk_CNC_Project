""" Serial Comunication Module. Send and get data from the CNC Plotter """

from serial import *
from serial.tools import list_ports

class Serial_CNC:
    pass

def list_serial_ports ():
    """ Lists the available Serial Comunication Ports, and returns them in a tuple """
    return tuple(list_ports.comports())


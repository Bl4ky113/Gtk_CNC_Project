""" Lists the available Serial Comunication Ports, and returns them in a tuple """

from serial.tools import list_ports

def list_serial_ports ():
    """ Lists the available Serial Comunication Ports, and returns them in a tuple """
    return tuple(list_ports.comports())

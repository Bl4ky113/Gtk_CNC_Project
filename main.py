"""
    CNC Plotter Controler made with GTK GUI, designed with Glade, and developed By Bl4ky113.
    Connects the CNC Plotter on a USB serial port, obtains and sends Coordinates information.
    Can send G-Code files to the CNC Plotter for printing an image. 
    The CNC Plotter used in the development of this project is a simple CNC made of 2 Stepper 
    Motors from CD Readers, and a pen with a servo as an interruptor.
    Full turorial, in spanish, for this CNC Plotter can be found at:

"""

from sys import argv

from gtk_views import Application

if __name__ == "__main__":
    gtk_app = Application()
    gtk_app.run(argv)

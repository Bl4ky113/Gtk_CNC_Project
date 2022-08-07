""" App window Class, base of the GTK GUI """

# Import GTK with GObject

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gio, Gtk

from screeninfo import get_monitors # get user monitor size

from serial_cnc import Serial_CNC

from .serial_port_menu import SerialPortMenu
from .dialog_generator import dialog_generator

# Create template from Glade-Made GTK GUI
@Gtk.Template.from_file("./gtk_views/templates/gtk_gui.glade")
class AppWindow (Gtk.ApplicationWindow):
    """ App window Class, base of the GTK GUI """
    __gtype_name__ = "app_window" # Set window base on the GUI XML

    # Serial Port Info Objs
    name_serial_port_label: Gtk.Label = Gtk.Template.Child()
    status_serial_port_label: Gtk.Label = Gtk.Template.Child()
    serial_port_info_textview: Gtk.TextView = Gtk.Template.Child()

    # Cords Objs
    home_cords_label: Gtk.Label = Gtk.Template.Child()
    current_cords_label: Gtk.Label = Gtk.Template.Child()
    cord_canvas: Gtk.DrawingArea = Gtk.Template.Child()

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Init Values
        self.serial_port = None

        # Resize window to 4/5 in width and 3/5 in height of the user main monitor
        monitor_data = get_monitors()[0] 
        window_width = int(monitor_data.width * 0.20) * 4
        window_height = int(monitor_data.height * 0.20) * 3

        self.set_default_geometry(window_width, window_height)

    @Gtk.Template.Callback()
    def open_serial_port_connect_menu (self, widget):
        serial_port_menu = SerialPortMenu()
        response = serial_port_menu.run()

        # Check if dialog's response is positive
        if response != Gtk.ResponseType.OK:
            return
    
        # Start and Configure the CNC Serial Port
        serial_port_name = serial_port_menu.serial_port_name
        self.serial_port = Serial_CNC(serial_port_name)

        # Update Info in the Main App Window
        self._update_serial_info_data()
        self._update_cords_data()

    @Gtk.Template.Callback()
    def check_move_btn_cnc (self, widget):
        """ Checks which widget triggered the signal, then moves the CNC Plotter
            to the direction / position of the widget.
        """
        # Check if there's a serial_port active
        if not self.serial_port:
            dialog_generator(
                    self,
                    "CNC Plotter Serial Port Not Connected",
                    "Connect the CNC Plotter via Serial Port before using it"
                    )
            return

        # Get widget's Glade Id, and actions from it
        widget_name = Gtk.Buildable.get_name(widget)
        widget_actions = widget_name.split("_")
        widget_actions.pop(0)
        
        if widget_actions[0] == "home":
            set_home = widget_actions[1] == "set"
            self.serial_port.go_home_cnc(set_home=set_home)
        else:
            negative = widget_actions[1] == "min"
            self.serial_port.simple_move_cnc(widget_actions[0], negative=negative)

    def _update_serial_info_data (self):
        """ Updates the Data on the Serial Info Section """
        if not self.serial_port: # Check if theres a serial_port
            return

        serial_port_data = self.serial_port.data   
        self.name_serial_port_label.set_text("Name: " + str(serial_port_data["name"]))
        self.status_serial_port_label.set_text("Active: " + str(serial_port_data["is_open"]))

        text_buffer = self.serial_port_info_textview.get_buffer()
        serial_port_data_string = ""
        for key, value in serial_port_data.items():
            serial_port_data_string += f"{key}: {value}\n"

        text_buffer.set_text(serial_port_data_string)

    def _update_cords_data (self):
        """ Updates the Data on the Cords Section """
        if not self.serial_port:
            return

        self_port_data = self.serial_port.data

        # Update Labels' Data

        home_cords = self_port_data["home"]
        current_cords = self_port_data["cords"]

        self.home_cords_label.set_text(
                f"X: {home_cords[0]}; Y: {home_cords[1]}; Z: {home_cords[2]}"
                )
        self.current_cords_label.set_text(
                f"X: {current_cords[0]}; Y: {current_cords[1]}; Z: {current_cords[2]}"
                )

        # Update Canvas Data

""" App window Class, base of the GTK GUI """

# Import GTK with GObject

import gi 

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gio, Gtk

from screeninfo import get_monitors # get user monitor size

from .serial_port_menu import SerialPortMenu

# Create template from Glade-Made GTK GUI
@Gtk.Template.from_file("./gtk_views/templates/gtk_gui.glade")
class AppWindow (Gtk.ApplicationWindow):
    """ App window Class, base of the GTK GUI """
    __gtype_name__ = "app_window" # Set window base on the GUI XML

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Resize window to 4/5 in width and 3/5 in height of the user main monitor
        monitor_data = get_monitors()[0] 
        window_width = int(monitor_data.width * 0.20) * 4
        window_height = int(monitor_data.height * 0.20) * 3

        self.set_default_geometry(window_width, window_height)

    @Gtk.Template.Callback()
    def open_serial_port_connect_menu (self, widget):
        serial_port_menu = SerialPortMenu()
        response = serial_port_menu.run()
        print(response, Gtk.ResponseType.OK)
        
        if response != Gtk.ResponseType.OK:
            return

        


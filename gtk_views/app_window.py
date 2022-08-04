
# Import GTK with GObject

import gi 

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gio, Gtk

from screeninfo import get_monitors # get user monitor size

class AppWindow (Gtk.ApplicationWindow):
    """ App window Class, base of the GTK GUI """
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Build and load Glade-Made GTK GUI
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./gtk_views/templates/gtk_gui.glade")

        # Resize window to 4/5 and 3/5 of the user main monitor
        monitor_data = get_monitors()[0] 
        window_width = int(monitor_data.width * 0.20) * 4
        window_height = int(monitor_data.height * 0.20) * 3

        self.set_default_geometry(window_width, window_height)

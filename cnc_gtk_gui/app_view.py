"""
    Main App View and Template
"""

import gi

from screeninfo import get_monitors

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

@Gtk.Template.from_file('./cnc_gtk_gui/templates/main_window.glade')
class AppWindow (Gtk.ApplicationWindow):
    """ App Window Class, Base of the GTK GUI """
    __gtype_name__ = 'app_window' # Set Window Base on the GUI

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Re-Size Window to 4/5 and 3/4 of width and height, of the User Screen
        monitor_data = get_monitors()[0] # Get Main, First Monitor
        self.set_default_geometry(
            4 * (monitor_data.width // 5),
            3 * (monitor_data.height // 4)
        )

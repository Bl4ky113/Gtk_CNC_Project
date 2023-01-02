"""
    Main App View and Template
"""

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

@Gtk.Template.from_file('./cnc_gtk_gui/templates/main_window.glade')
class AppWindow (Gtk.ApplicationWindow):
    """ App Window Class, Base of the GTK GUI """
    __gtype_name__ = 'app_window' # Set Window Base on the GUI

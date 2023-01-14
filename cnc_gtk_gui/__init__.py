"""
    Graphical User Interface Made with Glade GTK 3.0+ Templates
"""

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk

from .app_view import AppWindow

class GtkApplication (Gtk.Application):
    """ Main Gtk App Init, Startup, and Shutdown """

    def __init__ (self, *args, **kwargs):
        super().__init__(
            *args,
            application_id='cnc.gtk.gui',
            flags=Gio.ApplicationFlags.FLAGS_NONE,
            **kwargs
        )

        self.window = None

    def do_startup (self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new('About', None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("Quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

    def do_activate (self):
        if not self.window:
            self.window = AppWindow(application=self, title="CNC Plotter GUI")

        self.window.present()

    def on_about (self, action, param):
        pass

    def on_quit(self, action, param):
        self.quit()

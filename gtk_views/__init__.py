
# Import Gtk with GObject
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gio, Gtk

# Import App Modules

from .app_window import AppWindow

class Application (Gtk.Application):
    """ Gtk App init, startup, and shutdown """
    def __init__ (self, *args, **kwargs):
        super().__init__(
            *args,
            application_id="cnc.gtk.gui",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
            **kwargs
        )

        self.window = None

    def do_startup (self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
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

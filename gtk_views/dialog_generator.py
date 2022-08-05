""" Easy Way to Generate Dialogs """

# Import Gtk with GObject

import gi 

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gio, Gtk

def dialog_generator (father_window, dialog_text, secondary_dialog_text):
    """ Easy Way to Generate Dialogs """
    dialog = Gtk.MessageDialog(
        transient_for=father_window,
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text=dialog_text,
        )

    dialog.format_secondary_text(secondary_dialog_text)

    dialog.run()
    dialog.destroy()

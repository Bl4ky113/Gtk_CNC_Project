""" Serial Port Selection Menu """

# Import Gtk with GObject

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gio, Gtk

from screeninfo import get_monitors

from serial_cnc import list_serial_ports

@Gtk.Template.from_file("./gtk_views/templates/select_serial_port_menu.glade")
class SerialPortMenu (Gtk.Dialog):
    """ Serial Port Selection Menu """
    __gtype_name__ = "serial_port_menu"
    serial_treeview: Gtk.TreeView = Gtk.Template.Child("serial_ports_treeview")

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Resize the dialog, 2/5 in width and 3/5 in height
        monitor_data = get_monitors()[0]
        window_width = int(monitor_data.width * 0.20) * 2
        window_height = int(monitor_data.height * 0.20) * 3

        self.set_default_geometry(window_width, window_height)

        # Create TreeViewModel, and Add serial ports.
        self.serial_treemodel = Gtk.ListStore(str)
        self.serial_treeview.set_model(self.serial_treemodel)

        for port in list_serial_ports():
            self.serial_treemodel.append([port.device])

        # Make TreeView Selectable and render the ports' name

        tree_selectable = self.serial_treeview.get_selection()
        tree_selectable.set_mode(Gtk.SelectionMode(1))

        text_renderer = Gtk.CellRendererText()
        name_column = Gtk.TreeViewColumn("Port Name", text_renderer, text=0)
        self.serial_treeview.append_column(name_column)

    @Gtk.Template.Callback()
    def select_serial_port (self, selection):
        """ Get the Selected Serial Port from the TreeView 
            and save it's name
        """
        model, treeiter = selection.get_selected()

        if treeiter:
            self.serial_port_name = model[treeiter][0]

    @Gtk.Template.Callback()
    def set_serial_port (self, widget):
        """ Set and configure the Selected Serial Port 
            Refresh the info in the Main App Window
        """
        pass

    @Gtk.Template.Callback()
    """ Quit the dialog """
    def cancel_dialog (self, widget):
        self.destroy()

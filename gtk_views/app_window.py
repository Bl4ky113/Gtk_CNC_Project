""" App window Class, base of the GTK GUI """

# Import GTK with GObject

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gio, Gtk

from screeninfo import get_monitors # get user monitor size

from serial_cnc import SerialCNC

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
    home_coords_label: Gtk.Label = Gtk.Template.Child()
    current_coords_label: Gtk.Label = Gtk.Template.Child()
    coord_canvas: Gtk.DrawingArea = Gtk.Template.Child()

    # Serial Output Objs
    serial_output_textview: Gtk.TextView = Gtk.Template.Child()

    # G-Code Viewer Objs
    gcode_textviewer: Gtk.TextView = Gtk.Template.Child()

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Init Values
        self.serial_port = None
        self.gcode_filename = None

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
        self.serial_port = SerialCNC(serial_port_name)

        # Update Info in the Main App Window
        self._update_serial_info_data()
        self._update_coords_data()
        GLib.timeout_add(500, self._update_serial_output)

    @Gtk.Temaplte.Callback()
    def open_generate_gcode_menu (self, widget):
        pass

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

        # Check if the Active Serial Port is being used
        if self.serial_port.is_active:
            dialog_generator(
                    self,
                    "CNC Plotter is Being Used",
                    "Wait to the CNC to Finish its Current Action"
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
            self.serial_port.axis_movement_cnc(widget_actions[0], negative=negative)

        # Update Info in the Main App Window
        self._update_serial_info_data()
        self._update_coords_data()

    @Gtk.Template.Callback()
    def clear_serial_output (self, widget):
        """ Clear Stored Serial Output from CNC Serial Port
            and then update the Serial Output
        """
        self.serial_port.clear_serial_output()

    @Gtk.Template.Callback()
    def open_gcode_file (self, widget):
        """ Open and show G-Code File after selecting it with the FileChooserDialog
            Shows the content G-Code file in the gcode_textview
        """

        # Get G-Code Filename
        self.gcode_filename = widget.get_filename()

        # Get G-Code File content
        file_content = ""
        with open(self.gcode_filename, mode="r", encoding="UTF-8", newline="\n") as gcode_file:
            file_content = gcode_file.read()

        # Make G-Code File Content visible on the gcode_textviewer
        text_buffer = self.gcode_textviewer.get_buffer()
        text_buffer.set_text(file_content)

    @Gtk.Template.Callback()
    def send_gcode_file_to_serial_port (self, widget):
        """ Send Each line of the G-Code File to the CNC Serial Port
            for processing and sending it to the CNC Plotter. Then
            updates the Serial info and coords data.
        """

        # Check if there's a G-Code Filename and a Serial Port, which isn't active
        if not self.gcode_filename \
                and not self.serial_port \
                and not self.serial_port.is_active:
            dialog_generator(
                    self,
                    "Can't Run G-Code File",
                    "Try opening a G-Code File and \
                     Making Sure that The CNC Plotter is Conected via Serial Port"
                    )
            return

        # Get G-Code File Content
        file_content = ""
        with open(self.gcode_filename, mode="r", encoding="UTF-8", newline="\n") as gcode_file:
            file_content = gcode_file.read()
        file_content = file_content.split("\n")

        num_lines = len(file_content)
        current_line = 0

        # Send each G-Code Line to the CNC Serial Port,
        # Wait the serial port to be non-active before sending anything
        while current_line < num_lines:
            if not self.serial_port.is_active and file_content[current_line] != "":
                print(current_line, file_content[current_line])
                # Send G-Code Line
                GLib.timeout_add(
                        2000,
                        self.serial_port.process_gcode_line,
                        file_content[current_line]
                        )

                # Update Serial Info and Coords
                self._update_serial_info_data()
                self._update_coords_data()

                current_line += 1

    def _update_serial_output (self):
        """ Checks if there's any change to the CNC serial output
            and updates it if there's any changes
        """

        if not self.serial_port: # Check if there's a serial_port
            return

        serial_output = self.serial_port.get_serial_output()

        text_buffer = self.serial_output_textview.get_buffer()
        start_iter = text_buffer.get_start_iter()
        end_iter = text_buffer.get_end_iter()
        current_serial_output = text_buffer.get_text(start_iter, end_iter, True)

        if serial_output != current_serial_output: # Check if there's any changes
            text_buffer.set_text(serial_output)

        # Loop this funtion until the Serial Port gets used or is active
        GLib.timeout_add(500, self._update_serial_output)

    def _update_serial_info_data (self):
        """ Updates the Data on the Serial Info Section """
        if not self.serial_port: # Check if there's a serial_port
            return

        serial_port_data = self.serial_port.data
        self.name_serial_port_label.set_text("Name: " + str(serial_port_data["name"]))
        self.status_serial_port_label.set_text("Active: " + str(serial_port_data["is_open"]))

        text_buffer = self.serial_port_info_textview.get_buffer()
        serial_port_data_string = ""
        for key, value in serial_port_data.items():
            serial_port_data_string += f"{key}: {value}\n"

        text_buffer.set_text(serial_port_data_string)

    def _update_coords_data (self):
        """ Updates the Data on the Cords Section """
        if not self.serial_port:
            return

        self_port_data = self.serial_port.data

        # Update Labels' Data

        home_coords = self_port_data["home"]
        current_coords = self_port_data["coords"]

        self.home_coords_label.set_text(
                f"X: {home_coords[0]}; Y: {home_coords[1]}; Z: {home_coords[2]}"
                )
        self.current_coords_label.set_text(
                f"X: {current_coords[0]}; Y: {current_coords[1]}; Z: {current_coords[2]}"
                )

        # Update Canvas Data

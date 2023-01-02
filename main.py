"""
    CNC Plotter Controller made with a GTK 3.0+ GUI, designed with Glade, and developed By Bl4ky113
"""

import sys

from cnc_gtk_gui import GtkApplication

if __name__ == '__main__':
    gtk_app = GtkApplication()
    gtk_app.run(sys.argv)

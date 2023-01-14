"""
    Gtk GUI Testing
"""

import sys

from unittest import TestCase
from pyautogui import hold, press
from screeninfo import get_monitors

from . import GtkApplication


async def quit_gui ():
    """ Justs Quits an App """
    with hold('alt'):
        press('f4')


class MainAppWindowTests (TestCase):
    """
        Tests for the Main App Window
    """
    def setUp (self):
        self.gtk_app = GtkApplication()
        self.gtk_app.run(sys.argv)

    def test_app_window (self):
        """ Check if the Window is beeing Displayed """
        self.assertIsNotNone(self.gtk_app.window)

    def test_window_geometry (self):
        """ Check if the Window has the propper Size 4/5 and 3/4 of the screen """
        monitor_data = get_monitors()[0] # Get Main, First Monitor

        width_window = 4 * (monitor_data.width // 5)
        height_window = 3 * (monitor_data.height // 4)

        width_app, height_app = self.gtk_app.window.get_size()

        self.assertEqual(width_app, width_window)
        self.assertEqual(height_app, height_window)

    def tearDown (self):
        self.gtk_app.quit()

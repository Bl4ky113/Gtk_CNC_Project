# GTK Arduino CNC Plotter

## What is the proyect about?

This proyect is a simple CNC Plotter made with the stepper motors from two 
PC DVD readers, for the X and Y axis, and a servo motor with a pen for the Z axis and 
Plotter Printer.

## Materials

- Arduino UNO
- Shield L2932d For the Arduino UNO
- 360 Servomotor
- Pen, strings, liquid silicone, and extra springs for the pen
- Metal or plastic plates for the X and Y axis
- Something to hold the pen, for the X axis plate
- Paper sheets, for the Y axis plate
- Bolts and Nuts to hold the X and Y axis
- Arduino - USB cable, cable which can take 5V at 1A

## Code Requirements

- Python 3.10
- GTK 3.4
- Python requirements listed on "requirements.txt"

# Usage

For using the GTK GUI you need first to do the Arduino CNC Plotter, find out 
how to do it in this tutorial. 

You can use this GTK GUI by connecting your CNC Plotter to your Computer, you can do it in 
the Serial - Menu, on the right. From there you can use different menus:

### Serial Menu
See the current configuration of the Serial Port, it's name and status, active or not.
Connect and select the Serial Port of Your CNC Plotter, by using the Connect Serial Port Dialog.

### Serial Output Menu
See the Serial Output of your CNC Plotter, generally the current coords or the G-Code Lines 
sent to the CNC Plotter. If the Serial Output is gets too large, you can 
clear it with the button below.

### CNC Control Menu
Control the CNC Plotter, when it's connected, to do simple one direction movements with 
an simple arrows control. Where you can control the X, Y and Z axis. 
You can use the Home Buttons to set or go to a intial or "home" coord, default on 0, 0, 1.

### G-Code View
You can load and send G-Code Files to your CNC, when it's connected. Preview them in the TextViewer.
Or make one G-Code File from an image, on the Generate G-Code Dialog.

### CNC Coords Menu
You can see the current coords and home coords of the CNC Plotter.

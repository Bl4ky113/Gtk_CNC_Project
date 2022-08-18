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

# How does the GUI Code Work?

The GUI is divided on 3 modules, these combine in the GTK module to create the 
GUI and its actions. These Modules are:

## GTK_Views
Main module where it creates the GTK AppWindow, or Main Window, instance. Imports 
functions, objects or the entire module to add their functionality to the GUI. Specially 
The Serial_CNC module. 
It has some classes for each dialog or Non-Main Window, to keep them isolated and 
avoid writing a 1k lines file.

Each GUI is made using Glade, a simple GTK GUI dessigner.

## Serial_CNC
Module to connect to the Serial Port of the CNC, send and process Serial Output and Input.
There could be some improvements to the get and send Serial Data process.
It has some functions for the processing of Serial Input.

## GCode_Process
Module to process and create new G-Code Files from a given image, using Inkscape.

## Modules Flow Chart

1. Init, the GTK AppWindow shows
2. User selects and connects the CNC Serial Port

### Using the Simple CNC Control

- By Default the Simple CNC Control is the active window or stack
    otherwise, change it with the stackswitcher
3. Click on the buttons to move the CNC Axis on Positive or Negative direction.
    Can also set a Home Coords and move the CNC plotter to there
4. Wait until the CNC Plotter finishes the movement
5. Keep moving the CNC Plotter with the Axis and Home Buttons

### Using The G-Code View

- Change the Right Stack or active window to G-Code View
3. Load a G-Code file by using the FileChooser Button and Dialog
4. Send the G-Code file to the CNC Serial Port, this may take a while
5. Load new G-Code & send the G-Code File to the Serial Port

### Generate G-Code File from Image

- Change the Right Stack or active window to G-Code View
3. Click on the Generate G-Code, to show the G-Code Generator Dialog
4. Load an Image with the FileChooser Button and Dialog
5. Config the G-Code Generation
6. Save the New G-Code File
7. Use the G-Code File on the G-Code View Menu

### Simple use of the Serial Output
- Change the Left Stack or active window to Serial Output
3. See the Serial Output of the CNC Plotter
4. Clear the Output when it gets too long to scroll or read

## Others

There's other folders on the proyect, these are:

### GCode_Examples
Generated examples of images on G-Code, ready to use them with the CNC Plotter.

### Arduino_CNC
Code of the CNC Plotter's Arduino. The Flow chart of the code is:
1. Init, send via Serial Port the max and min coords of the CNC Plotter, and the current coords
2. Wait for a Valid G-Code Line "G1 X0 Y0 Z0"
3. Process and get the Axis values from the G-Code Line
4. Move the X, Y and Z axis acording the new Coords
5. Send new coords, now current coords, via Serial Port

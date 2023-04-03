'''
Author1: Alexandru Constantin
Author2: <Insert Name Here>

Date: April 2023

REQUIREMENTS: 
* Pimoroni-Pico Library: https://github.com/pimoroni/pimoroni-pico

The following program runs on the Raspberry Pi Pico and displays the info received through the usb serial port.
'''

from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB332
from time import sleep

import sys
import select

# Setting up the display
display = PicoGraphics(display = DISPLAY_PICO_DISPLAY, pen_type = PEN_RGB332, rotate = 0)
display.set_font("bitmap8")

# Setting up colours
WHITE  = display.create_pen(255, 255, 255)
BLACK  = display.create_pen(0, 0, 0)
RED    = display.create_pen(255, 0, 0)
YELLOW = display.create_pen(255, 255, 0)

def clear(colour = BLACK):
    '''
    This function clears the screen and sets the background colour to the specified colour
    @param: colour (default = BLACK) - The colour of the background
    '''
    display.set_pen(colour)
    display.clear()
    display.update()

# Creating the class that holds the system info that we want to pass between the PC and the current project
class SysInfo:
    def __init__(self, ram = 0, cpu = 0):
        self.ram = ram
        self.cpu = cpu
    
    def __str__(self):
        '''
        The function is called when converting the class to a string.
        If any new fields are to be added to this class or you want a different layout, this function should be modified to reflect that.
        '''
        return f'CPU: {self.cpu}% \n\rRAM: {self.ram}%'
    
    
def readSysInfo(info):
    '''
    The function attempts to read the system information from the connected device
    @param info: The info object holding the data we want to display
    '''
    # Inform the host system that we are requesting the data
    print("req")
    # Read the data and store it into a SysInfo object
    input_exists, _, _ = select.select( [sys.stdin], [], [], 5)
    if input_exists:
        input = sys.stdin.readline().strip().split()
        if input:
            info.ram = float(input[0])
            info.cpu = float(input[1])
    return info
    
def setDisplayColorBasedOnValue(val):
    '''
    The function receives a number and sets the colour based on the value
    @param val: the value that determines the colour 
    '''
    if val >= 80:
        display.set_pen(RED)
    elif val >= 50:
        display.set_pen(YELLOW)
    else:
        display.set_pen(WHITE)

info = SysInfo()
while True:
    info = readSysInfo(info)
    clear()

    # Displaying the value for the CPU
    setDisplayColorBasedOnValue(info.cpu)
    display.text(f"CPU: {info.cpu}%", 10, 10, 240, 3)
    display.update()
 
    # Displaying the value for the RAM
    setDisplayColorBasedOnValue(info.ram)
    display.text(f"RAM: {info.ram}%", 10, 35, 240, 3)
    display.update()
 
    sleep(1)
 
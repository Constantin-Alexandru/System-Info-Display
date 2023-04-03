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
    print("req") # Sends the message that the PC connections is expecting to send information about the PC
    
    '''
    The function needs to read from the connection the PC info (Hint: Use sys.stdin) and parse the incoming mesage to a SysInfo obj.
    In addition, the system needs to be able to timeout if no input has been received in a set amount of time.
    This is done in order to ensure that, in case of a message send to the Serial Port not reaching it's target, the system doesn't get blocked waiting for an input that never comes.
    Afterwards, return the SysInfo object (that's also passed as a parameter) so the message can be sent
    '''
    
#Creating the initial object
info = SysInfo()

while True:
    clear()
    display.set_pen(WHITE) # Sets the colour of the text
    display.text(str(info), 10, 10, 240, 3) # Displays the text
    display.update() # Updates the display
    info = readSysInfo(info) # Reads the data for the system
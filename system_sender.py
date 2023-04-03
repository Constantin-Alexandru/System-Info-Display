'''
Author1: Alexandru Constantin
Author2: <Insert Name Here>

Date: April 2023

REQUIREMENTS:
* PSUtil library: https://psutil.readthedocs.io/en/latest/#

The following program will run on the host machine and send the system information to the Pi Pico
'''

import serial
import psutil
import time

debug = False

# Connecting to the Pico through serial
s = serial.Serial("<insert serial port here>", 115200) # Note: Depending on OS, there are different ways to find the serial port of the pico, check your OS' documentation

# Printing a debug message
if debug:
    print("Started")

while True:
    if debug:
        print("Waiting for read")
    
    #Reading the input from the serial
    msg = s.readline().decode("utf-8").strip()
    
    if debug:
        print("MSG: " + msg)

    if msg == "req":
        if debug:
            print("Request received")
        cpu_percent = psutil.cpu_percent(1) # Getting the CPU usage percentage
        mem_percent = psutil.virtual_memory()[2] # Gettign the Memory percentage usage
        s.write(f"{mem_percent} {cpu_percent}\n".encode()) # Sending the information to the Pico
        print(f"{mem_percent} {cpu_percent}\n") # Printing to the console

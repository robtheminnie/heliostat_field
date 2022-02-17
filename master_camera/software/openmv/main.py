# UART Control
#
# This example shows how to use the serial port on your OpenMV Cam. Attach pin
# P4 to the serial input of a serial LCD screen to see "Hello World!" printed
# on the serial LCD display.

import time
#from pyb import UART
from machine import UART

# Always pass UART 3 for the UART number for your OpenMV Cam.
# The second argument is the UART baud rate. For a more advanced UART control
# example see the BLE-Shield driver.
uart = UART(3, 19200, bits=8, parity=None, stop=1)

# instructions to implement:
    # Set ID.  Sent by master cam at power up.  Destionation index is set to 0 by master cam and sent.
    # each slave adds 1 to the destination, stores this as thier ID, and transmits on to the next slave
    #
    # heliostat auto home.  Sent by master cam on power up.
    #
    # heliostat adjust angle

idx = 1

while(True):

    source_index = bytearray([0])       # index of sending node, 0 = cam
    destination_index = bytearray([idx])  # index of receiving node
    instruction_ID = bytearray([0])     # instruction

    idx += 1

    data = bytearray([1, 3, 0, 0])            # data to send

    temp_buffer = bytearray()
    temp_buffer += source_index + destination_index + instruction_ID + data
    uart.write(temp_buffer)
    time.sleep_ms(3000)

    if idx > 5:
        idx = 1


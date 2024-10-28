import time

from machine import I2C

from qwstpad import ADDRESSES, QwSTPad

"""
How to read all of the buttons on QwSTPad
"""

# Constants
I2C_PINS = {"id": 0, "sda": 4, "scl": 5}    # The I2C pins the QwSTPad is connected to
I2C_ADDRESS = ADDRESSES[0]                  # The I2C address of the connected QwSTPad
SLEEP = 0.1                                 # The time between each reading of the buttons


# Attempt to create the I2C instance and pass that to the QwSTPad
try:
    qwstpad = QwSTPad(I2C(**I2C_PINS), I2C_ADDRESS)
except OSError:
    print("QwSTPad: Not Connected ... Exiting")
    raise SystemExit

print("QwSTPad: Connected ... Starting")

# Wrap the code in a try block, to catch any exceptions (including KeyboardInterrupt)
try:
    # Loop forever
    while True:
        # Read all the buttons from the qwstpad and print them out
        buttons = qwstpad.read_buttons()
        for key, value in buttons.items():
            print(f"{key} = {value:n}", end=", ")
        print()

        time.sleep(SLEEP)

# Handle the QwSTPad being disconnected unexpectedly
except OSError:
    print("QwSTPad: Disconnected .. Exiting")
    qwstpad = None

# Turn off all four LEDs if there is still a QwSTPad
finally:
    if qwstpad is not None:
        qwstpad.clear_leds()

import time

from machine import I2C

from qwstpad import QwSTPad

"""
"""

# Constants
SLEEP = 0.1     # The time between each reading of the buttons

# Create the I2C instance and pass that to the QwSTPad
i2c = I2C(0, scl=13, sda=12)
qwstpad = QwSTPad(i2c)

# Loop forever
while True:
    # Read all the buttons from the qwstpad and print them out
    buttons = qwstpad.read_buttons()
    for key, value in buttons.items():
        print(f"{key} = {value:n}", end=", ")
    print()

    time.sleep(SLEEP)

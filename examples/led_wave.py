import time
from machine import I2C
from qwstpad import QwSTPad


"""
"""

# Constants
SLEEP = 0.2     # The time between each LED update

# Variables
current = 1     # The LED currently being controlled
active = True   # The state to set the controlled LED to

# Create the I2C instance and pass that to the QwSTPad
i2c = I2C(0, scl=13, sda=12)
qwstpad = QwSTPad(i2c)


# Wrap the code in a try block, to catch any exceptions (including KeyboardInterrupt)
try:
    qwstpad.clear_leds()    # Turn off all four LEDs

    # Loop forever
    while True:
        # Modify the current LED
        qwstpad.set_led(current, active)

        # Move along to the next LED, wrapping if reaching the end
        current += 1
        if current > 4:
            current = 1
            active = not active

        time.sleep(SLEEP)

finally:
    qwstpad.clear_leds()    # Turn off all four LEDs

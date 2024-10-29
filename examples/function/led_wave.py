import time

from machine import I2C

from qwstpad import ADDRESSES, NUM_LEDS, QwSTPad

"""
Apply a wave effect across QwSTPad's onboard LEDs.
"""

# Constants
I2C_PINS = {"id": 0, "sda": 4, "scl": 5}    # The I2C pins the QwSTPad is connected to
I2C_ADDRESS = ADDRESSES[0]                  # The I2C address of the connected QwSTPad
SLEEP = 0.2                                 # The time between each LED update

# Variables
led = 1                                     # The LED currently being controlled
active = True                               # The state to set the controlled LED to


# Attempt to create the I2C instance and pass that to the QwSTPad
try:
    qwstpad = QwSTPad(I2C(**I2C_PINS), I2C_ADDRESS)
except OSError:
    print("QwSTPad: Not Connected ... Exiting")
    raise SystemExit

print("QwSTPad: Connected ... Starting")

# Wrap the code in a try block, to catch any exceptions (including KeyboardInterrupt)
try:
    qwstpad.clear_leds()    # Turn off all four LEDs

    # Loop forever
    while True:
        # Modify the current LED
        qwstpad.set_led(led, active)
        print(f"{led}: {active}")

        # Move along to the next LED, wrapping if reaching the end
        led += 1
        if led > NUM_LEDS:
            led = 1
            active = not active

        time.sleep(SLEEP)

# Handle the QwSTPad being disconnected unexpectedly
except OSError:
    print("QwSTPad: Disconnected .. Exiting")
    qwstpad = None

# Turn off all four LEDs if there is still a QwSTPad
finally:
    if qwstpad is not None:
        qwstpad.clear_leds()

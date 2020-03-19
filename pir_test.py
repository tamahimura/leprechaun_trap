import time
from adafruit_crickit import crickit

# For signal control, we'll chat directly with seesaw, use 'ss' to shorted typing!
ss = crickit.seesaw

PIR_IN = crickit.SIGNAL2

ss.pin_mode(PIR_IN, ss.INPUT_PULLUP)

while True:
    if ss.digital_read(PIR_IN):
        print("MOTION DETECTED")
    time.sleep(0.5)

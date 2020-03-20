import time
import threading
from adafruit_crickit import crickit

# For signal control, we'll chat directly with seesaw, use 'ss' to shorted typing!
ss = crickit.seesaw

# use pin 2 for pir motion detecting
PIR_IN = crickit.SIGNAL2
ss.pin_mode(PIR_IN, ss.INPUT_PULLUP)

# per documentation pwm is not always needed, but should be set for safety
crickit.drive_1.frequency = 1000

event_counter = 0
drive_thread_terminate = 0

# thread for dive
def drive_thread_function():
    print("Drive thread: starting")

    local_counter = 0
    #crickit.drive_1.fraction = 0.0

    # keep going until we are told to stop
    while (drive_thread_terminate == 0):

        # wait for the next event
        while (local_counter >= event_counter):
            print("waiting ", local_counter, " ", event_counter)
            time.sleep (0.5)

        local_counter = event_counter

        # engage, then disengage
        print("release ", event_counter)
        crickit.drive_1.fraction = 1.0  # all the way on
        time.sleep(0.5)
        crickit.drive_1.fraction = 0.0  # all the way off
        print("engage")

    print("Drive thread: stopping")

print("Initializing")

# kick off the thread
drive_thread = threading.Thread(target=drive_thread_function)
drive_thread.start()

# wait 5 seconds after start first, to let the PIR settle.
time.sleep(5.0)
print("Ready")

last_read = 0
current_read = 0
while True:
    current_read = ss.digital_read(PIR_IN)
    # if pin is high and last reading was not, we have an edge.
    if (current_read and not last_read):
        print("MOTION DETECTED")
        event_counter += 1
        last_read = 1

    # otherwise if last reading was high, reset it, and wait an additional 2 seconds before we
    # trigger again.
    elif not current_read and last_read:
        last_read = 0
        time.sleep(2.0)
    time.sleep(0.5)

# signal thread to terminate
drive_thread_terminate = 1
drive_thread.join()

import time
import threading
from adafruit_crickit import crickit
from enum import Enum
class State(Enum):
    ARMED = 1
    TRIGGERED = 2
    IDLE = 3

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

    global event_counter
    local_counter = 0
    crickit.drive_1.fraction = 0.0

    # keep going until we are told to stop
    global drive_thread_terminate
    while (drive_thread_terminate == 0):

        # wait for the next event
        while (local_counter >= event_counter):
            #print("waiting ", local_counter, " ", event_counter)
            time.sleep (0.5)

        local_counter = event_counter

        # engage, then disengage
        print("release ", event_counter)
        crickit.drive_1.fraction = 1.0  # all the way on
        time.sleep(0.5)
        crickit.drive_1.fraction = 0.0  # all the way off
        print("engage")

    print("Drive thread: stopping")

def case_armed(reading):
    if reading:
        print("MOTION DETECTED")
        global event_counter
        event_counter += 1
        return State.TRIGGERED
    return State.ARMED

def case_triggered(reading):
    print("IDLING")
    return State.IDLE

def case_idle(reading):
    if not reading:
        print("ARMED")
        return State.ARMED
    return State.IDLE

fsm = {State.ARMED : case_armed,
   State.TRIGGERED : case_triggered,
        State.IDLE : case_idle
}

print("Initializing")

# kick off the thread
drive_thread = threading.Thread(target=drive_thread_function)
drive_thread.start()

# wait 10 seconds after start first, to let the PIR settle.
time.sleep(10.0)
print("Ready")

current_state = State.IDLE
current_read = 0
while True:
    current_read = ss.digital_read(PIR_IN)
    #print("current_read ", current_read)
    current_state = fsm[current_state](current_read)

    # ticks / sec
    time.sleep(0.1)

# signal thread to terminate
drive_thread_terminate = 1
drive_thread.join()

import ctypes
import random
from multiprocessing.sharedctypes import Synchronized
from serComLib import *
import brickpi3
from multiprocessing import Process, Event, Value
from collections import deque

COLORS = ["none", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]
AMERICA = ["Red", "Blue", "White"]

BP = brickpi3.BrickPi3()
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.EV3_COLOR_COLOR)

color_q = deque(maxlen=3)

def color_proc(bp, event, eventTwo, color_val):
    while True:
        color_read = COLORS[bp.get_sensor(bp.PORT_2)]
        print("Color: ", color_read)
        color_q.append(color_read)

        if color_read in AMERICA and len(color_q) == color_q.maxlen and len(set(color_q)) == 1:
            color_val.value = color_read.encode()
            print("Color confirmed:", color_read)
            color_q.clear()
            # ser.reset_input_buffer()
            # ser.reset_output_buffer()
            # stop()
            # ser.flush()
            event.set()
            eventTwo.wait()
            eventTwo.clear()
    
    

def main():
    color = Value(ctypes.c_char*16)
    color.value = b"none"
    color_event = Event()
    color_event_t = Event()

    color_circle = ""

    color_p = Process(target=color_proc, args=[BP, color_event, color_event_t, color,])

    try:
        initSerComm()
        handshake()
        color_p.start()

        start = time.time()
        while time.time()-start < 60*3:
            distance = readSonicCM()
            print("Distance: ", distance)
            if distance and distance <=30:
                print("Object evation start")
                last_dist=distance
                curr_dist=distance
                turn_choice = random.randint(0,1)
                turn(turn_choice, 10)
                while curr_dist-last_dist < 50:
                    if color_event.is_set():
                        turn(not turn_choice, 10)
                    print("Avoiding...")
                    new_reading = readSonicCM()
                    if new_reading:
                        last_dist = curr_dist
                        curr_dist = new_reading
                    time.sleep(0.2)
                print("Evaded object")
                time.sleep(1)
                stop()
            if color_event.is_set():
                stop()
                seen_color = color.value.decode()
                print("Color event: ", seen_color)
            
                if seen_color == color_circle:
                    print("Exiting circle turning around!")
                    moveBack(10)
                    time.sleep(2)
                    turn(1, 13) # TODO: tweak to do full 180
                    time.sleep(4)
                    stop()
                elif seen_color == "Blue": # Goal met
                    print("In goal!")
                    moveForward(10)
                    time.sleep(3)
                    stop()
                    break
                else:
                    color_circle = seen_color
                color.value = b"none"
                color_event.clear()
                color_event_t.set()
            moveForward(8)
            time.sleep(0.2)
        color_p.join()
        # dist_p.join()
    except Exception as e:
        print("An exception occured: ", e)

if __name__ == '__main__':
    main()
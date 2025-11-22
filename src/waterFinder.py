import ctypes
import random
from multiprocessing.sharedctypes import Synchronized
from serComLib import *
import brickpi3
from multiprocessing import Process, Event, Value

COLORS = ["none", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]
AMERICA = ["Red", "White", "Blue"]

BP = brickpi3.BrickPi3()
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.EV3_COLOR_COLOR)

def color_proc(bp, event, eventTwo, color_val):
    while True:
        eventTwo.clear()
        color = COLORS[bp.get_sensor(bp.PORT_2)]
        print("Color: ", color)
        if color in AMERICA:
            color_val.value = color.encode()
            print("In America")
            event.set()
            eventTwo.wait()
            
        time.sleep(0.1)

def verify_color(bp, color_val):
    start = time.time()
    color_count = 0
    while time.time() - start < 3:
        color = COLORS[bp.get_sensor(bp.PORT_2)]
        color_count += color_val == color
        time.sleep(0.2)
    return color_count >= 5

def avoid_obstacle():
    stop()
    moveBack(10)
    time.sleep(3)
    turn(random.randint(0,1), 10)
    time.sleep(4)
    stop()

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
            if distance and distance <=15:
                avoid_obstacle()
            moveForward(10)
            if color_event.is_set():
                seen_color = color.value.decode()
                print("Color event: ", seen_color)
            
                if verify_color(BP, seen_color):
                    if seen_color == color_circle:
                        print("Exiting circle turning around!")
                        moveBack(10)
                        time.sleep(2)
                        turn(1, 10) # TODO: tweak to do full 180
                        time.sleep(2)
                        stop()
                    elif seen_color == "Blue": # Goal met
                        print("In goal!")
                        moveForward(10)
                        time.sleep(1)
                        stop()
                        break
                    else:
                        color_circle = seen_color
                color.value = b"none"
                color_event.clear()
                color_event_t.set()
        color_p.join()
        # dist_p.join()
    except Exception as e:
        print("An exception occured: ", e)


if __name__ == '__main__':
    main()
import serial
import time
from enum import Enum
import random   

SERIAL_PORT = '/dev/ttyUSB0' 
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)


class direction(Enum):
    LEFT = 0
    RIGHT = 1

class command(Enum):
    HANDSHAKE = 1
    READ_DIST = 2
    TURN = 3
    FORWARD = 4
    BACKWARD = 5
    STOP = 6

def handshake():
    while True:
            print("--- Sending out handshaking signal (cmd 1) ---")
            ack = cmdSend(command.HANDSHAKE.value)
            if not ack: 
                print("*** No response. Trying again... ***")
                time.sleep(1)
            else: 
                print(" Connected to the robot Received ack:")
                ser.readall()
                break
            

def initSerComm():
    print(" RP3 Robot Controller: Starting...")
    try:
        handshake()
        print("In loop")
        while True:
            dist = readSonicCM()
            print("Dist: " + dist)
            if dist <= 5:
                stop()
                moveBack()
                if random.randint(0,1):
                    turnLeft(30)
                else:
                    turnRight(30)
            else:
                moveForward(random.randint(20, 50))
                # if random.randint(0,1):
                #     turnLeft(random.randint(20, 40))
                # else:
                #     turnRight(random.randint(20, 40))

        
    except serial.SerialException:
        print(" Error: Could not open serial port .")
        print("Please check the port name and ensure the PRIZM is connected.")
    except KeyboardInterrupt:
        print("\n Program terminated")
    finally:
        if ser and ser.is_open:
            print("Stopping motors (cmd 5) and closing serial connection...")
            cmdSend(5) 
            ser.close()

def cmdSend(cmd, param=""):
    print("Send: " + str(cmd))
    msg = str(cmd) +"\n"
    ser.write(msg.encode())
    ack_origin = ser.readline()
    ack = ack_origin[:-2].decode('utf-8')
    print("Recv: " + ack_origin)
    return ack


def stop():
    msg = str(command.STOP)
    ack = cmdSend(msg)
    return ack

def moveForward(power):
    msg = str(command.FORWARD.value) + " " + str(power)
    ack = cmdSend(msg)
    return ack

def moveBack(power):
    msg = str(command.BACKWARD.value) + " " + str(power)
    ack = cmdSend(msg)
    return ack

def turnLeft(power):
    msg = str(command.TURN.value) + " " + str(power) + " " + str(power/2)+ " " + str(direction.LEFT.value)
    ack = cmdSend(msg)
    return ack

def turnRight(power):
    msg = str(command.TURN.value) + " " + str(power/2) + " " + str(power)+ " " + str(direction.RIGHT.value)
    ack = cmdSend(msg)
    return ack

def readSonicCM():
    msg = "2"
    ack = cmdSend(msg)
    return ack

def readSonicIN():
    msg = str(command.READ_DIST.value)
    ack = cmdSend(msg)
    return ack

if __name__ == "__main__":
    initSerComm()
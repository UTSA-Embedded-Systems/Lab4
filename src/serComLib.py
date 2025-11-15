import serial
import time
from enum import Enum
import random   

SERIAL_PORT = '/dev/ttyUSB0' 
BAUD_RATE = 9600

ser = None


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
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        
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
    print("Stop")
    msg = str(command.STOP.value)
    ack = cmdSend(msg)
    return ack

def moveForward(power):
    print("Forward")
    msg = str(command.FORWARD.value) + " " + str(power)
    ack = cmdSend(msg)
    return ack

def moveBack(power):
    print("Backward")
    msg = str(command.BACKWARD.value) + " " + str(power)
    ack = cmdSend(msg)
    return ack

def turn(dir, power):
    print("turn")
    msg = str(command.TURN.value) + " " + str(power) + " " + str(dir)
    ack = cmdSend(msg)
    return ack


def readSonicCM():
    msg = "2"
    ack = cmdSend(msg)
    return int(ack)

def readSonicIN():
    msg = str(command.READ_DIST.value)
    ack = cmdSend(msg)
    return int(ack)

if __name__ == "__main__":
    initSerComm()
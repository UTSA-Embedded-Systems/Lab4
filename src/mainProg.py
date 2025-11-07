from task1 import *

SERIAL_PORT = '/dev/ttyUSB0' 
BAUD_RATE = 9600

def main():
    initSerComm(SERIAL_PORT, BAUD_RATE)
    moveForward(20)
    moveBack(20)
    turnLeft(20)
    turnRight(20)
    readSonicCM(SERIAL_PORT)
    readSonicIN(SERIAL_PORT)


if __name__ == '__main__':
    main()
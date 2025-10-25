import serial
import time

def cmdSend(ser, cmd):
    msg = str(cmd) + "\n"
    ser.write(msg.encode())
    ack_origin = ser.readline()
    ack = ack_origin[:-2].decode("utf-8")    
    return ack

def initSerComm(baudrate):
    print(" RP3 Robot Controller: Starting...")
    ser = None 
    try:
        ser = serial.Serial('/dev/ttyUSB0', baudrate, timeout=1)
        
        print("Press the GREEN button on the PRIZM to start the robot")
        while True:
            print("--- Sending out handshaking signal (cmd 1) ---")
            ack = cmdSend(ser, 1)

            if not ack: 
                print("*** No response. Trying again... ***")
                time.sleep(1)
            else: 
                print(" Connected to the robot Received ack:")
                ser.readall() 
                break
    except serial.SerialException:
        print(" Error: Could not open serial port .")
        print("Please check the port name and ensure the PRIZM is connected.")
    except KeyboardInterrupt:
        print("\n Program terminated")
    finally:
        if ser and ser.is_open:
            print("Stopping motors (cmd 5) and closing serial connection...")
            cmdSend(ser, 5) 
            ser.close()
            

def moveForward(power):
    pass

def moveBack(power):
    pass

def turnLeft(power):
    pass

def turnRight(power):
    pass

def readSonicCM(port):
    pass

def readSonicIN(port):
    pass
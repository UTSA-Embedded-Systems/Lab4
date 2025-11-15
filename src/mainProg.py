from task1 import *

def main():
    try:
        handshake()
        print("In loop")
        moveForward(20)
        start = time.time()
        while time.time()-start < 30:
            dist = readSonicCM()
            if dist <= 20:
                stop()
                moveBack(10)
                time.sleep(2)
                turn(random.randint(0,1), 20)
                time.sleep(random.randint(1, 4))
                stop()
                if readSonicCM() <= 10:
                    moveForward(20)
    except Exception as e:
        print("An excpetion occured: " + e.with_traceback())

if __name__ == '__main__':
    main()
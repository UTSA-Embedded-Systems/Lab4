#include <PRIZM.h>
#include <Wire.h>
#include <time.h>

PRIZM prizm;

enum DIRECTION {
    LEFT = 0,
    RIGHT = 1,
};

enum CMD {
    HANDSHAKE = 1,
    READ_DIST = 2,
    TURN = 3,
    FORWARD = 4,
    BACK = 5,
    STOP = 6
};

void handshake();

void moveForward(int power);

void moveBackwards(int power);

void stop();

void turn(enum DIRECTION dir, int powerL, int powerR);

void setup() {
    Serial.begin(9600);
    prizm.PrizmBegin();
    prizm.setMotorInvert(1,1);
    delay(100);
}

void loop() {
    handshake();
    if (Serial.available()) {
        String line = Serial.readStringUntil('\n');
        switch (line.charAt(0)) {
            case '2':
                //Serial.println(String(prizm.readSonicSensorCM(3)));
                Serial.println("Read this word");
                break;
            case '3':
                {
                    int powerL = line.charAt(1)-'0';
                    int powerR = line.charAt(2)-'0';
                    enum DIRECTION dir = static_cast<DIRECTION>(line.charAt(3) - '0');
                    turn(dir, powerL, powerR);
                }
                break;
            case '4':
                {
                    int power = line.charAt(1)-'0';
                    moveForward(power);

                }
                break;
            case '5':
                {
                    int power = line.charAt(2)-'0';
                    moveBackwards(power);

                }
                break;
            case '6':
                stop();
                break;
            default:
                Serial.println("Send some words");
                break;
        }
    }
}

void handshake() {
    for(;;) {
        if (Serial.available()) {
            String line = Serial.readStringUntil('\n');
            if (line.toInt() == HANDSHAKE) {
                Serial.println("1");
                break;
            }
        }
    }
}

void moveForward(int power) {
    prizm.setMotorPowers(power, power);
}

void moveBackwards(int power) {
    prizm.setMotorPowers(-power, -power);
}

void stop() {
    prizm.setMotorPowers(125, 125);
}

void turn(enum DIRECTION dir, int pl, int pr) {
    int invert =  1 - (dir == RIGHT)*2;
    pl = pl * invert;
    pr = pr * invert;

    prizm.setMotorPowers(pl, pr);
};
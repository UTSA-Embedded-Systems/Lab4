#include <PRIZM.h>
#include <Wire.h>
#include <time.h>
#include <string>

PRIZM prizm;

using namespace std;

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

void turn(enum DIRECTION dir, int power);

void setup() {
    Serial.begin(9600);
    prizm.PrizmBegin();
    prizm.setMotorInvert(1,1);
    handshake();
}

vector<string> split(const string& text, const string& del) {
    vector<string> tokens;
    size_t l = 0;
    size_t r = 0;
    string token;
    while((r = text.find(del, l)) != string::npos) {
        token = text.substr(l, r-l);
        tokens.push_back(token);
        l = r+del.length();
    }
    tokens.push_back(text.substr(l));
    return tokens;
}

void loop() {
    if (Serial.available()) {
        String line = Serial.readStringUntil('\n');
        vector<string> tokens = split(line.c_str(), " ");
        string cmd = tokens[0];
        switch (cmd.c_str()[0]) {
            case '2':
                Serial.println(String(prizm.readSonicSensorCM(3)));
                break;
            case '3':
                {
                    int power = atoi(tokens[1].c_str());
                    enum DIRECTION dir = static_cast<DIRECTION>( atoi(tokens[2].c_str()));
                    turn(dir, power);
                }
                break;
            case '4':
                {
                    int power = atoi(tokens[1].c_str());
                    moveForward(power);

                }
                break;
            case '5':
                {
                    int power = atoi(tokens[1].c_str());
                    moveBackwards(power);
                }
                break;
            case '6':
                stop();
                break;
            default:
                Serial.println("Default case");
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

void turn(enum DIRECTION dir, int p) {
    int pl, pr;
    if (dir == LEFT) {
        pl = -(p);
        pr = p;
    } else {
        pr = -(p);
        pl = p;
    }

    prizm.setMotorPowers(pl, pr);
};
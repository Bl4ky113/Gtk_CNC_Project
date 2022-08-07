
#include <Servo.h>
#include <AFMotor.h>

#define LINE_BUFFER_LENGTH 512

char STEP = MICROSTEP;

// Z Axis Servo Config

const int zAxisOn = 140;
const int zAxisOff = 50;

const int zAxisPin = 10;
Servo zAxis;

// Stepper X and Y Axis Config

const int stepsPerRevolution = 48;
AF_Stepper yAxisStepper(stepsPerRevolution, 1);
AF_Stepper xAxisStepper(stepsPerRevolution, 2);

// Point in Coords Struct
struct coordPoint {
    float x;
    float y;
    float z;
};

// Current Position of the CNC Plotter
struct coordPoint currentCoords;

// Delays (ms)
int stepDelay = 1;
int lineDelay = 10;
int plotterDelay = 25;

// Step Config
float stepIncrease = 1;
float stepsPerMillimeterAxisX = 100.0;
float stepsPerMillimeterAxisY = 100.0;

// CNC Plotter Coords Values

float minAxisX = 0;
float maxAxisX = 40;
float minAxisY = 0;
float maxAxisY = 40;
float minAxisZ = 0;
float maxAxisZ = 1;

// Initial Positions
float currentAxisXPosition = minAxisX;
float currentAxisYPosition = minAxisY;
float currentAxisZPosition = maxAxisZ;

void setup() {
    // Init Pins, Axis, and Serial Comunication
    Serial.begin(9600);

    zAxis.attach(zAxisPin);
    zAxis.write(zAxisOn);
    delay(100);

    yAxisStepper.setSpeed(600);
    xAxisStepper.setSpeed(600);
    
    // Initial Serial Print, Send Plotter Coord values
    Serial.print("CNC_Plotter_Data:Min_Max_Axis_Values;");
    Serial.print("minAxisX:");
    Serial.print(minAxisX);
    Serial.print(";");
    Serial.print("maxAxisX:");
    Serial.print(maxAxisX);
    Serial.print(";");
    Serial.print("minAxisY:");
    Serial.print(minAxisY);
    Serial.print(";");
    Serial.print("maxAxisY:");
    Serial.print(maxAxisY);
    Serial.print(";");
    Serial.print("minAxisZ:");
    Serial.print(minAxisZ);
    Serial.print(";");
    Serial.print("maxAxisZ:");
    Serial.print(maxAxisZ);
    Serial.println(";");

    delay(500);
    
    printCurrentCoords();
};

void loop() {
    delay(100);

    char line[LINE_BUFFER_LENGTH];
    char inputChar;
    int lineIndex;
    bool lineIsComment, lineSemiColon;

    lineIndex = 0;
    lineSemiColon = false;
    lineIsComment = false;

    while (1) {
        while (Serial.available() > 0) { // Wait until theres something to read on the serial port
            inputChar = Serial.read();

            if ((inputChar == '\n') || (inputChar == '\r')) { // End of the G-Code Line
                if (lineIndex > 0) {
                    line[lineIndex] = '\0';
                    processIncomingLine(line, lineIndex); // Process the Line, and moves the CNC Plotter
                    lineIndex = 0;
                }

                lineSemiColon = false;
                lineIsComment = false;
                printCurrentCoords();

            } else {
                if (lineIsComment || lineSemiColon) {
                    if (inputChar == ')') {
                        lineIsComment = false;
                    }
                } else {
                    // Error, line too long for the LineBuffer
                    if (lineIndex >= LINE_BUFFER_LENGTH - 1) {
                        Serial.println("Error - LineBuffer Overflow");
                        lineIsComment = false;
                        lineSemiColon = false;
                    }
                    
                    // Check the inputChar, to see if the line is commented, has a 
                    // semi colon. Will add the inputChar to the line if it's a 
                    // character or a number, wont upcase the lowercase letters.
                    switch (inputChar) {
                        case '(':
                            lineIsComment = true;
                        break;
                        case ';':
                            lineSemiColon = true;
                        break;
                        case ' ':
                            // Skip white spaces
                        break;
                        case '/':
                            // Skip slash as well  
                        break;
                        default:
                            line[lineIndex++] = inputChar;
                        break;
                    }
                }
            }
        }
    }
};

void processIncomingLine (char* line, int charNum) {
    int currentIndex = 0;
    char buffer[64];
    struct coordPoint newCoords;

    newCoords.x = 0.0;
    newCoords.y = 0.0;

    /* Interpret the G-Code Line:
        G1 X{NUM} Y{NUM}; Move X and Y to {NUM}
        M3 Z1; Turn Z on
        M3 Z0; Turn Z off
        Discard anything with a ()
        And anything else than those 3 lines.
    */

    while (currentIndex < charNum) {
        switch (line[currentIndex++]) {
            case 'G':
                buffer[0] = line[currentIndex++];
                buffer[1] = '\0';
                
                if (atoi(buffer) == 1) {
                    // Get X and Y values from the G-Code Line
                    char* valueX = strchr(line + currentIndex, 'X');
                    char* valueY = strchr(line + currentIndex, 'Y');
                    
                    // Change newCoords Values to G-Code Values
                    if (valueY <= 0) {
                        newCoords.x = atof(valueX + 1);
                        newCoords.y = currentCoords.y;
                    } else if (valueX <= 0) {
                        newCoords.x = currentCoords.x;
                        newCoords.y = atof(valueY + 1);
                    } else {
                        newCoords.x = atof(valueX + 1);
                        newCoords.y = atof(valueY + 1);
                        valueY = '\0';
                    }
                    
                    // Draw With the CNC Plotter the newCoords and update currentCoords
                    drawLine(newCoords.x, newCoords.y);

                    currentCoords.x = newCoords.x;
                    currentCoords.y = newCoords.y;
                }
            break;
            case 'M':
                buffer[0] = line[currentIndex++];
                buffer[1] = '\0';

                if (atoi(buffer) == 3) {
                    // Get new coord for Z
                    char* valueZ = strchr(line + currentIndex, 'Z');
                    float coordZ = atof(valueZ + 1);

                    // Move the CNC Plotter's Z Axis
                    if (coordZ == 1) {
                        moveUpZAxis();
                    } else {
                        moveDownZAxis();
                    }
                }
            break;
        }
    }
}

void moveUpZAxis () {
    if (currentAxisZPosition < maxAxisZ) {
        // Move AxisZ
        zAxis.write(zAxisOn);

        delay(plotterDelay);

        // Update current AxisZ Position
        currentAxisZPosition = currentAxisZPosition + stepIncrease;
        digitalWrite(15, LOW);
        digitalWrite(16, HIGH);
    }
}

void moveDownZAxis () {
    if (currentAxisZPosition > minAxisZ) {
        // Move AxisZ
        zAxis.write(zAxisOff);

        delay(plotterDelay);

        // Update current AxisZ Position
        currentAxisZPosition = currentAxisZPosition - stepIncrease;
        digitalWrite(15, HIGH);
        digitalWrite(16, LOW);
    }
}

void drawLine (float x1, float y1) {
    // Avoid Drawing outside available area
    if (x1 > maxAxisX) {
        x1 = maxAxisX;
    } else if (x1 < minAxisX) {
        x1 = minAxisX;
    }

    if (y1 > maxAxisY) {
        y1 = maxAxisY;
    } else if (y1 < minAxisY) {
        y1 = minAxisY;
    }

    // Convert DrawingCoords to CNC Steps
    float x0 = currentAxisXPosition;
    float y0 = currentAxisYPosition;

    x1 = (int)(x1 * stepsPerMillimeterAxisX);
    y1 = (int)(y1 * stepsPerMillimeterAxisY);

    // Distance between both points, and steps de/in-crease.

    long distanceX = abs(x1 - x0);
    long distanceY = abs(y1 - x0);

    int stepX = x0 < x1 ? stepIncrease : - stepIncrease;
    int stepY = y0 < y1 ? stepIncrease : - stepIncrease;

    long i;
    long over = 0;

    // Move First the Axis with the longer distance to move
    if (distanceX > distanceY) {
        for (i = 0; i < distanceX; i++) {
            xAxisStepper.onestep(stepX, STEP);
            over += distanceY;

            if (over >= distanceX) {
                over -= distanceX;
                yAxisStepper.onestep(stepY, STEP);
            }
            delay(stepDelay);
        }
    } else {
        for (i = 0; i < distanceY; i++) {
            yAxisStepper.onestep(stepY, STEP);
            over += distanceX;

            if (over >= distanceY) {
                over -= distanceY;
                xAxisStepper.onestep(stepX, STEP);
            }
            delay(stepDelay);
        }
    }

    delay(lineDelay);

    // Update the Current Position
    currentAxisXPosition = x1;
    currentAxisYPosition = y1;
    printCurrentCoords();
}

void printCurrentCoords () {
    Serial.print("CNC_Plotter_Data:Current_Axis_Values;");
    Serial.print("axisX:");
    Serial.print(currentAxisXPosition / stepsPerMillimeterAxisX);
    Serial.print(";");
    Serial.print("axisY:");
    Serial.print(currentAxisYPosition / stepsPerMillimeterAxisY);
    Serial.print(";");
    Serial.print("axisZ:");
    Serial.print(currentAxisZPosition);
    Serial.println(";");
}

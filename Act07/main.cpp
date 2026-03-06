#include <Arduino.h>
#include <Servo.h>

Servo myServo;
const int servoPin = 9;
String readString;
int currentAngle = 90;

void setup() {
  Serial.begin(9600);
  myServo.attach(servoPin);
  myServo.write(currentAngle);
  Serial.println("System Ready.");
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    readString += c;
    if (readString.length() > 5) {
      readString = "";
      break;
    }
    delay(1);
  }

  if (readString.length() > 0 && readString.endsWith("\n")) {
    readString.trim();
    int receivedAngle = readString.toInt();

    if (receivedAngle >= 0 && receivedAngle <= 180) {
      if (receivedAngle != currentAngle) {
        myServo.write(receivedAngle);
        currentAngle = receivedAngle;
        Serial.print("Moved to: ");
        Serial.println(currentAngle);
      }
    }
    readString = "";
  }
}
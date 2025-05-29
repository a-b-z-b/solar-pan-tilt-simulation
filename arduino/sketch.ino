#include <Servo.h>

Servo panServo;
Servo tiltServo;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  panServo.attach(11);
  tiltServo.attach(10);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n'); // Read full line
    int commaIndex = data.indexOf(',');

    if (commaIndex > 0) {
      float azimuth = data.substring(0, commaIndex).toFloat();
      float elevation = data.substring(commaIndex + 1).toFloat();

      // Convert azimuth (0–360) to servo angle (e.g., 0–180)
      int panAngle = map(azimuth, 0, 360, 0, 180);
      int tiltAngle = map(elevation, 0, 90, 0, 180);

      panServo.write(panAngle);
      tiltServo.write(tiltAngle);

      // Debug output
      Serial.print("Moving to azimuth angle: ");
      Serial.println(panAngle);

      // Debug output
      Serial.print("Moving to zenith angle: ");
      Serial.println(tiltAngle);
    }
  }
}

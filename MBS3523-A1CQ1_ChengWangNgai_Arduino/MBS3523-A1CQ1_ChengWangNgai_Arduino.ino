#include <Servo.h>

Servo left_right;
Servo up_down;

void setup() {
  left_right.attach(9);
  up_down.attach(10);
  Serial.begin(115200);
}

void loop() {
  while(Serial.available()) {
    String inputString = Serial.readStringUntil('\r');
    int commaIndex = inputString.indexOf(',');
    if (commaIndex != -1) {
      int x_axis = inputString.substring(0, commaIndex).toInt();
      int y_axis = inputString.substring(commaIndex + 1).toInt();

      int y = map(y_axis, 0, 1080, 180, 0);
      int x = map(x_axis, 0, 1920, 180, 0);

      left_right.write(x);
      up_down.write(y);

      // Print the parsed values
      Serial.print("First Integer: ");
      Serial.println(x);
      Serial.print("Second Integer: ");
      Serial.println(y);
    }
  }
}

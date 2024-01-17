/*
 Hand Firmware
 Controls the servos
 Listens to the laptop for commands
 */
#include <SoftwareSerial.h>
#include <Servo.h>

Servo thumb_servo, index_servo;


void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  thumb_servo.attach(9);
  index_servo.attach(10);

  thumb_servo.write(0);
  index_servo.write(0);
  // Serial.println("Connectd");
}

void loop() { // run over and over
  if (Serial.available()) {
    int thumb = 0, index = 0, middle = 0, ring = 0, little = 0;
    int data = Serial.read();
    while (data != 255) {
      Serial.write(254);
      Serial.write(data);
      data = Serial.read();
    }

    data = Serial.read();
    if (data > 100) {
      Serial.write(101);
      Serial.write(data);
      return;
    }
    thumb = data;
    
    data = Serial.read();
    if (data > 100) {
      Serial.write(102);
      Serial.write(data);
      return;
    }
    index = data;
    
    data = Serial.read();
    if (data > 100) {
      Serial.write(103);
      Serial.write(data);
      return;
    }
    middle = data;

    data = Serial.read();
    if (data > 100) {
      Serial.write(104);
      Serial.write(data);
      return;
    }
    ring = data;

    data = Serial.read();
    if (data > 100) {
      Serial.write(105);
      Serial.write(data);
      return;
    }
    little = data;

    // data = Serial.read();
    // if (data != 255) {
    //   Serial.write(106);
    //   Serial.write(data);
    //   return;
    // }

    Serial.write(255);
    Serial.write(255);

    thumb = map(thumb, 0, 100, 0, 180);
    index = map(index, 0, 100, 0, 180);

    thumb_servo.write(thumb);
    index_servo.write(index);
    // delay(15);
  }
}

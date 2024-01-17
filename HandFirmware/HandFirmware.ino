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
}

void loop() { // run over and over
  if (Serial.available()) {
    uint8_t thumb = 0, index = 0, middle = 0, ring = 0, little = 0;
    while (!Serial.available()) {;}
    uint8_t data = Serial.read();
    while (data != 126) {
      Serial.write(200);
      Serial.write(data);
      while (!Serial.available()) {;}
      data = Serial.read();
    }

    while (!Serial.available()) {;}
    data = Serial.read();
    if (data > 100) {
      Serial.write(101);
      Serial.write(data);
      return;
    }
    thumb = data;
    
    while (!Serial.available()) {;} 
    data = Serial.read();
    if (data > 100) {
      Serial.write(102);
      Serial.write(data);
      return;
    }
    index = data;
    
    while (!Serial.available()) {;}
    data = Serial.read();
    if (data > 100) {
      Serial.write(103);
      Serial.write(data);
      return;
    }
    middle = data;

    while (!Serial.available()) {;}
    data = Serial.read();
    if (data > 100) {
      Serial.write(104);
      Serial.write(data);
      return;
    }
    ring = data;

    while (!Serial.available()) {;}
    data = Serial.read();
    if (data > 100) {
      Serial.write(105);
      Serial.write(data);
      return;
    }
    little = data;

    Serial.write(255);
    Serial.write(255);
    // Serial.write(thumb);

    thumb = map(thumb, 0, 100, 0, 180);
    index = map(index, 0, 100, 0, 180);

    thumb_servo.write(thumb);
    index_servo.write(index);
  }
}

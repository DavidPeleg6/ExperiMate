// ** libraries
#include <Boards.h>



// ** pins : digital
int sensorPin = A0; // select the input pin for LDR// ** pins : analog
// ** frequency
const int sleep_time = 1000 ;// ** global
long sensorValue = 0; // variable to store the value coming from the sensor// ** setup
void setup() {
Serial.begin(9600); //sets serial port for communication// ** sleep for 1 sec
delay(1000);
}// ** loop start
void loop() {
sensorValue = analogRead(sensorPin); // read the value from the sensor
delay(sleep_time);// ** print statement
Serial.println(sensorValue); //prints the values coming from the sensor on the screen
Serial.println("LDR");

// ** loop end
}// ** help functions

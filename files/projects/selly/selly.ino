// ** libraries
#include <Boards.h>// ** pins : digital
const int led = 13 ;// ** pins : analog
// ** frequency
const int sleep_time = 1000 ;// ** global
// the setup function runs once when you press reset or power the board// ** setup
void setup() {
  Serial.begin(9600);
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(led, OUTPUT);// ** sleep for 1 sec
  delay(1000);
}

// the loop function runs over and over again forever// ** loop start
void loop() {
  digitalWrite(led, HIGH);
  delay(sleep_time);
  digitalWrite(led, LOW);
  delay(sleep_time);// ** print statement
// ** loop end
}// ** help functions

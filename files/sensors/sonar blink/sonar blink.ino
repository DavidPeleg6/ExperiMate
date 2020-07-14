// ** libraries
#include <Boards.h>// ** pins : digital
const int echoPin = 7 ;
const int trigPin = 8 ;
const int led = 13 ;// ** pins : analog
// ** frequency
const int sleep_time = 200 ;// ** global
// the setup function runs once when you press reset or power the board
int duration;
float distance;
// the setup function runs once when you press reset or power the board// ** setup
void setup() {
  Serial.begin(9600);
  Serial.begin(9600); // Starts the serial communication
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(led, OUTPUT);// ** sleep for 1 sec
  delay(1000);
}

// the loop function runs over and over again forever// ** loop start
void loop() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration*0.034/2;
  delay(sleep_time);
  digitalWrite(led, HIGH);
  delay(sleep_time);
  digitalWrite(led, LOW);
  delay(sleep_time);// ** print statement
  Serial.println(distance);
  Serial.println("distance");// ** loop end
}// ** help functions

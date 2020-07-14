// ** libraries
#include <Stepper.h>// ** pins : digital
int pin1 = 8
int pin2 = 9
int pin3 = 10
int pin4 = 11// ** pins : analog
// ** frequency
const int sleep_time = 500 ;// ** global
const int stepsPerRevolution = 100;  // change this to fit the number of steps per revolution  for your motor
int steps_left=2050; //# of steps for one circle
// initialize the stepper library on pins 8 through 11:
Stepper myStepper( stepsPerRevolution, pin1, pin2, pin3, pin4);// ** setup
void setup() {
  myStepper.setSpeed(60);// set the speed at 60 rpm:
  Serial.begin(9600);// initialize the serial port:// ** sleep for 1 sec
  delay(1000);
}// ** loop start
void loop() {

  while(steps_left>0){
       myStepper.step(1);
       steps_left--;
                     }
  delay(sleep_time);
  steps_left=2050;// ** print statement
// ** loop end
}// ** help functions

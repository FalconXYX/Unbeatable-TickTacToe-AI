#include <Servo.h>

Servo myservo;
float voltage, lefttemp,voltage2, righttemp;

int tempSensorPin = A0;
int pos = 90;
int dif;
void setup()
{
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(11, OUTPUT);
  myservo.attach(13);
}

void loop()
{
  voltage = analogRead(A0) * 0.004882814;

  lefttemp = (voltage - 0.5) * 100.0; // calculate the actual temperature detected

  Serial.print("voltage1: ");
  Serial.print(voltage);
  Serial.print("  deg C1: ");
  Serial.println(lefttemp);
  voltage2 = analogRead(A1) * 0.004882814;

  righttemp = (voltage2 - 0.5) * 100.0; // calculate the actual temperature detected
  dif = righttemp - lefttemp;
  if(dif <+ 1 and dif >= -1){
  	digitalWrite(11, LOW);
  	digitalWrite(9, LOW);
    //pos = 0;


  }
  else if(righttemp > lefttemp){
  	digitalWrite(11, HIGH);
  	digitalWrite(9, LOW);
    //pos +=90;
  }
  else{
  	digitalWrite(11, LOW);
  	digitalWrite(9, HIGH);
    //pos +=90
  }


  myservo.write(pos);



}
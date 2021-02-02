#include <Servo.h>

Servo myservo1;
Servo myservo2;
String inString = "";

int input;
void setup()
{
  myservo1.attach(2);
  myservo2.attach(5);

  Serial.begin(9600);
  myservo1.write(75);
  myservo2.write(75);

}


void loop() {
  while (Serial.available() > 0) {
    int inChar = Serial.read();
    inString += (char)inChar;
    
    if (inChar == '\n') {
      int s1_pos = inString.substring(0, inString.indexOf(' ')).toInt();
      int s2_pos = inString.substring(inString.indexOf(' ')).toInt();

      Serial.print("s1_pos: ");
      Serial.println(s1_pos);
      Serial.print("s2_pos:");
      Serial.println(s2_pos);
      inString = "";

      myservo1.write(s1_pos);
      myservo2.write(s2_pos);


    }
  }
}

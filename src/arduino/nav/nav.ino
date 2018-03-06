/* Team 8
 * Omar Abdelkader, Tauqir Abdullah, Renee Adkins
 */

// Set pin numbers
const int leftMotor1 = 13;
const int leftMotor2 = 12;
const int leftPWM = 5;
const int leftMotorInitSpeed = 127; // (25% = 64; 50% = 127; 75% = 191; 100% = 255)

const int rightMotor1 = 8;
const int rightMotor2 = 7;
const int rightPWM = 3;
const int rightMotorInitSpeed = 127; // (25% = 64; 50% = 127; 75% = 191; 100% = 255)

const int leftPingPin = 9;
const int rightPingPin = 10;

const int MAX_DISTANCE_CM = 30;

void setup() {
  Serial.begin(9600);
  
  pinMode(leftMotor1, OUTPUT);
  pinMode(leftMotor2, OUTPUT);
  pinMode(leftPWM, OUTPUT);
  
  pinMode(rightMotor1, OUTPUT);
  pinMode(rightMotor2, OUTPUT);
  pinMode(rightPWM, OUTPUT);
}

void loop() {
  long durationLeft, durationRight, cmLeft, cmRight;

  analogWrite(leftPWM, leftMotorInitSpeed);
  analogWrite(rightPWM, rightMotorInitSpeed);

  // The PING is triggered by a HIGH pulse of 2 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  pinMode(leftPingPin, OUTPUT);
  digitalWrite(leftPingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(leftPingPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(leftPingPin, LOW);

  // The same pin is used to read the signal from the PING: a HIGH pulse
  // whose duration is the time (in microseconds) from the sending of the ping
  // to the reception of its echo off of an object.

  pinMode(leftPingPin, INPUT);
  durationLeft = pulseIn(leftPingPin, HIGH);

  pinMode(rightPingPin, OUTPUT);
  digitalWrite(rightPingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(rightPingPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(rightPingPin, LOW);

  pinMode(rightPingPin, INPUT);
  durationRight = pulseIn(rightPingPin, HIGH);

  // convert the time into a distance
  cmLeft = microsecondsToCentimeters(durationLeft);
  cmRight = microsecondsToCentimeters(durationRight);

  Serial.print("cmLeft: ");  
  Serial.print(cmLeft);
  Serial.print("\tcmRight: ");
  Serial.print(cmRight);

  if (cmLeft > MAX_DISTANCE_CM && cmRight > MAX_DISTANCE_CM) {
    forward();
    Serial.print("\tFORWARD\n");
  } else if (cmLeft <= MAX_DISTANCE_CM && cmRight > MAX_DISTANCE_CM) {
    right();
    Serial.print("\tRIGHT\n");
  } else if (cmLeft > MAX_DISTANCE_CM && cmRight <= MAX_DISTANCE_CM) {
    left();
    Serial.print("\tLEFT\n");
  } else {
    reverse();
    Serial.print("\tREVERSE\n");
  }

  delay(100);
}

void forward() {
  digitalWrite(leftMotor1, HIGH);
  digitalWrite(leftMotor2, LOW);
  digitalWrite(rightMotor1, HIGH);
  digitalWrite(rightMotor2, LOW);
}

void left() {
  digitalWrite(leftMotor1, LOW);
  digitalWrite(leftMotor2, HIGH);
  digitalWrite(rightMotor1, HIGH);
  digitalWrite(rightMotor2, LOW);
}

void right() {
  digitalWrite(leftMotor1, HIGH);
  digitalWrite(leftMotor2, LOW);
  digitalWrite(rightMotor1, LOW);
  digitalWrite(rightMotor2, HIGH);
}

void reverse() {
  digitalWrite(leftMotor1, LOW);
  digitalWrite(leftMotor2, HIGH);
  digitalWrite(rightMotor1, LOW);
  digitalWrite(rightMotor2, HIGH);
}

void halt() {
  digitalWrite(leftMotor1, LOW);
  digitalWrite(leftMotor2, LOW);
  digitalWrite(rightMotor1, LOW);
  digitalWrite(rightMotor2, LOW);
}

long microsecondsToCentimeters(long microseconds) {
  // The speed of sound is 340 m/s or 29 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the object we
  // take half of the distance travelled.
  return microseconds / 29 / 2;
}

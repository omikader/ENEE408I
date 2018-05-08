// DIRECTIONS
#define FOUND 0
#define FORWARD 1
#define REVERSE 2
#define RIGHT 3
#define LEFT 4
#define FORWARDLEFT 5
#define FORWARDRIGHT 6

// NEW_DIRECTIONS
#define STOP 0
#define FL 1
#define FF 2
#define FR 3
#define FB 4
#define SL 5
#define SF 6
#define SR 7
#define SB 8
#define NA 9

// NEW_RESPONSES
#define SUCCESS 0
#define OBSTACLE_LEFT 1
#define OBSTACLE_RIGHT 2
#define OBSTACLE_FORWARD 3
#define OBSTACLE_ALL 4

//Delay
#define delayLow 200
#define delayHigh 500
int inAL = 12; //yellow
int inBL = 13; //green
int speedL = 5; //purple (pwm1)
// green, black go to ground, red to 5V
int inAR = 7; //yellow
int inBR = 8; //green
int speedR = 6; //purple (pwm2)

int pingR = 10; // purple
int pingL = 3; // yellow
int pingM = 9; // yellow
int surveryDirection = RIGHT;

// dir_speed_wheel
int forward_fast_R = 90/2;
int forward_fast_L = 100/2;

int forward_med_R = 70/2;
int forward_med_L = 80/2;

int forward_slow_R = 50/2;
int forward_slow_L = 60/2;

int left_slow_R = 30/2;
int left_slow_L = 70/2;

int left_fast_R = 30/2;
int left_fast_L = 90/2;

int right_slow_R = 70/2;
int right_slow_L = 30/2;

int right_fast_R = 90/2;
int right_fast_L = 30/2;

int ThermistorPin = 0;
int Vo;
float R1 = 4500;
float logR2, R2, T;
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;


void setup() {
  pinMode(inAL, OUTPUT);
  pinMode(speedL, OUTPUT);
  pinMode(inBL, OUTPUT);
  pinMode(inAR, OUTPUT);
  pinMode(speedR, OUTPUT);
  pinMode(inBR, OUTPUT);
  Serial.begin(9600);
  while (! Serial); // Wait for the serial to be ready
}
void readSimple(int *command) {
  if (Serial.available() <= 0) {
    // do nothing
  }
  if (Serial.available() > 0) {
    Vo = analogRead(ThermistorPin);
    R2 = R1 * (1023.0 / (float)Vo - 1.0);
    logR2 = log(R2);
    T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
    T = T - 273.15;
    T = (T * 9.0)/ 5.0 + 32.0;
    *command = Serial.read() - '0';
    Serial.print(T);
  }
}


void turnSimple(int command) {
  switch (command) {
    case NA:
      setWheelDirection(surveryDirection);
      setWheelSpeed(right_slow_L, right_slow_R);
      break;
    case FL:
      setWheelDirection(FORWARD);
      setWheelSpeed(left_fast_L, left_fast_R);
      surveryDirection = LEFT;
    break;
    case FF:
      setWheelDirection(FORWARD);
      setWheelSpeed(forward_fast_L, forward_fast_R);
    break;
    case FR:
      setWheelDirection(FORWARD);
      setWheelSpeed(right_fast_L, right_fast_R);
      surveryDirection = RIGHT;
    break;
    case FB:
      setWheelDirection(REVERSE);
      setWheelSpeed(forward_fast_L, forward_fast_R);
    break;
    case SL:
      setWheelDirection(FORWARD);
      setWheelSpeed(left_slow_L, left_slow_R);
      surveryDirection = LEFT;
    break;
    case SF:
      setWheelDirection(FORWARD);
      setWheelSpeed(forward_med_L, forward_med_R);
    break;
    case SR:
      setWheelDirection(FORWARD);
      setWheelSpeed(right_slow_L, right_slow_R);
      surveryDirection = RIGHT;
    break;
    case SB:
      setWheelDirection(REVERSE);
      setWheelSpeed(forward_med_L, forward_med_R);
    break;
    case STOP:
      halt();
    break;
  }
}

// Ping triggered by a HIGH pulse of 2 or more microseconds.
// Give a short LOW pulse prior to ensure a clean HIGH pulse:
int get_ping_helper(int ping ){
  pinMode(ping, OUTPUT);
  digitalWrite(ping, LOW);
  delayMicroseconds(10);
  digitalWrite(ping, HIGH);
  delayMicroseconds(10);
  digitalWrite(ping, LOW);
  pinMode(ping, INPUT);
  return pulseIn(ping, HIGH);
}

void get_ping_data(long* inchesL, long* inchesR, long* inchesM) {
  long durationL;
  long durationR;
  long durationM;

  durationR = get_ping_helper(pingR);
  durationL = get_ping_helper(pingL);
  durationM = get_ping_helper(pingM);

  *inchesR = microsecondsToInches(durationR);
  *inchesL = microsecondsToInches(durationL);
  *inchesM = microsecondsToInches(durationM);

  //Serial.print("inchesL: ");
  //Serial.print(*inchesL);
  //Serial.print("\tinchesM: ");
  //Serial.print(*inchesM);
  //Serial.print("\tinchesR: ");
  //Serial.print(*inchesR);
  //Serial.println("");

}


void setWheelDirectionHelper(int AL, int BL, int AR, int BR){
    digitalWrite(inAL, AL);
    digitalWrite(inBL, BL);
    digitalWrite(inAR, AR);
    digitalWrite(inBR, BR);
}

// set the wheel direction
void setWheelDirection(int direction) {
  if (direction == FORWARD)
    setWheelDirectionHelper(HIGH,LOW,HIGH,LOW);
  else if (direction == REVERSE)
    setWheelDirectionHelper(LOW,HIGH,LOW,HIGH);
  else if (direction == RIGHT)
    setWheelDirectionHelper(LOW,HIGH,HIGH,LOW);
  else if (direction == LEFT)
    setWheelDirectionHelper(HIGH,LOW,LOW,HIGH);
}

// Sets only the wheel speed, not the direction
// Expects positive wheel speeds
void setWheelSpeed(int wheelSpeedL, int wheelSpeedR) {
  analogWrite(speedL, wheelSpeedL);
  analogWrite(speedR, wheelSpeedR);
}

void halt() {
  analogWrite(speedL, 0);
  analogWrite(speedR, 0);
}
void reverse() {
    //Serial.println("reverse: ");
  setWheelDirectionHelper(LOW,HIGH,LOW,HIGH);
  analogWrite(speedL, forward_med_L); //60
  analogWrite(speedR, forward_med_R); //43
}
void forward() {
    //Serial.println("forward: ");
  setWheelDirectionHelper(HIGH,LOW,HIGH,LOW);
  analogWrite(speedL, forward_med_L); //60
  analogWrite(speedR, forward_med_R); //43
}
void turnLeft() {
    //Serial.println("turnRight: ");

  setWheelDirectionHelper(HIGH,LOW,LOW,HIGH);
  analogWrite(speedL, forward_med_L); //60
  analogWrite(speedR, forward_med_R); //43
}
void turnRight() {
    //Serial.println("turnLeft: ");

  setWheelDirectionHelper(LOW,HIGH,HIGH,LOW);
  analogWrite(speedL, forward_med_L); //60
  analogWrite(speedR, forward_med_R); //43
}



long microsecondsToInches(long microseconds) {
  return microseconds / 74 / 2;
}

void loop() {
  int command, response;
  long inchesL, inchesR, inchesM;
  get_ping_data(&inchesL, &inchesR, &inchesM);
  readSimple(&command);
  //Serial.println(command);

  //turnSimple(command);
  //command = FR;



  // No Obstacle
  if (command == STOP){
    halt();
    //Serial.println(response);
  } else if (inchesL >= 10 && inchesR >= 10 && inchesM >= 8) {
    turnSimple(command);
    delay(delayLow);
    response = SUCCESS;
    get_ping_data(&inchesL, &inchesR, &inchesM);
  }
  // Obstacle only Straight Ahead
  else if (inchesL >= 10 && inchesM < 8 && inchesR >= 10) {
    //Serial.println("Obstacle only Straight Ahead");
    reverse();
    delay(delayHigh);
    if (inchesL < 10 || inchesM < 8 || inchesR < 10){
      switch(command){
        case FL:
          turnLeft();
          delay(delayLow);
          surveryDirection = LEFT;
          response = 1;
          break;
        case FF:
          turnLeft();
          delay(delayLow);
          surveryDirection = LEFT;
          response = 2;
          break;
        case FR:
          turnRight();
          delay(delayLow);
          surveryDirection = RIGHT;
          response = 2;
          break;
        case SL:
          turnLeft();
          delay(delayLow);
          surveryDirection = LEFT;
          response = 2;
        case SR:
          turnRight();
          delay(delayLow);
          surveryDirection = RIGHT;
          response = 2;
          break;
        case SB:
          reverse();
          delay(delayLow);
          response = OBSTACLE_FORWARD;
          break;
        case NA:
          turnRight();
          delay(delayHigh);
          response = OBSTACLE_FORWARD;
          break;
      }
      get_ping_data(&inchesL, &inchesR, &inchesM);
    }
  }
  // Obstacle to the Left
  else if (inchesL < 10 && inchesR >= 10) {
    //Serial.println("Obstacle to the Left");
    reverse();
    delay(delayHigh);
    while (inchesL < 10 || inchesR < 10){
      turnRight();
      delay(delayLow);
      get_ping_data(&inchesL, &inchesR, &inchesM);
    }

    surveryDirection = RIGHT;
    response = OBSTACLE_LEFT;
  }

  // Obstacle to the Right
  else if (inchesL >= 10 && inchesR < 10) {
    //Serial.println("Obstacle to the Right");
    reverse();
    delay(delayHigh);
    while (inchesL < 10 || inchesR < 10){
      turnLeft();
      delay(delayLow);
      get_ping_data(&inchesL, &inchesR, &inchesM);
    }
    surveryDirection = LEFT;
    response = OBSTACLE_RIGHT;
  }

  // Obstacle to the Left, Right and Middle
  else if (inchesL < 10 && inchesM < 8 && inchesR < 10) {
    //Serial.println("Obstacle to the Left, Right and Middle");
    reverse();
    delay(delayHigh);
    delay(delayHigh);

    while (inchesL < 10 || inchesM < 10 || inchesR < 10){
      turnRight();
      delay(delayLow);
      get_ping_data(&inchesL, &inchesR, &inchesM);
    }

    surveryDirection = LEFT;
    response = OBSTACLE_ALL;
  }

  //Serial.println(response);
}

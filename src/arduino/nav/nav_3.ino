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

int inAL = 13; //yellow
int inBL = 12; //green
int speedL = 5; //purple (pwm1)
// green, black go to ground, red to 5V
int inAR = 7; //yellow
int inBR = 8; //green
int speedR = 6; //purple (pwm2)
int pingR = 10; // purple
int pingL = 9; // yellow
int pingM = 2; // yellow
int surveryDirection = RIGHT;

// dir_speed_wheel
int forward_fast_R = 150; 
int forward_fast_L = 150; 
int forward_med_R = 100; 
int forward_med_L = 100; 
int forward_slow_R = 50; 
int forward_slow_L = 50;
 
int left_slow_R = 100; 
int left_slow_L = 50; 
int left_fast_R = 150; 
int left_fast_L = 50; 

int right_slow_R = 50;
int right_slow_L = 100;
int right_fast_R = 50; 
int right_fast_L = 150; 

void setup() {  
  pinMode(inAL, OUTPUT);
  pinMode(speedL, OUTPUT);
  pinMode(inBL, OUTPUT);
  pinMode(inAR, OUTPUT);
  pinMode(speedR, OUTPUT);
  pinMode(inBR, OUTPUT);
  Serial.begin(9600);
  //while (! Serial); // Wait for the serial to be ready
}
/*
void readSimple(int *command) {
  while (Serial.available() <= 0) {
    // do nothing
  }
  if (Serial.available() > 0) {
      *command = Serial.read() - '0';
  }
}
*/

void turnSimple(int command) {
  switch (command) {
    case NA:
      setWheelDirection(surveryDirection);
      setWheelSpeed(forward_slow_L, forward_slow_R);
      break;
    case FL:
      setWheelDirection(FORWARD);
      setWheelSpeed(left_fast_L, left_fast_R);
      surveryDirection = LEFT;
    break;
    case FF:
      setWheelDirection(FORWARD);
      setWheelSpeed(right_fast_L, right_fast_R);
    break;
    case FR:
      setWheelDirection(FORWARD);
      setWheelSpeed(forward_fast_L, forward_fast_R);
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
  delayMicroseconds(2);
  digitalWrite(ping, HIGH);
  delayMicroseconds(5);
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
  else if (direction == LEFT)
    setWheelDirectionHelper(LOW,HIGH,HIGH,LOW);
  else if (direction == RIGHT)
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
  setWheelDirectionHelper(LOW,HIGH,LOW,HIGH);
  analogWrite(speedL, forward_med_L); //60
  analogWrite(speedR, forward_med_R); //43 
}
void forward() {
  setWheelDirectionHelper(HIGH,LOW,HIGH,LOW);
  analogWrite(speedL, forward_med_L); //60
  analogWrite(speedR, forward_med_R); //43 
}
void turnRight() {
  setWheelDirectionHelper(HIGH,LOW,LOW,HIGH);
  analogWrite(speedL, forward_slow_L); //60
  analogWrite(speedR, forward_slow_R); //43  
}
void turnLeft() {
  setWheelDirectionHelper(LOW,HIGH,HIGH,LOW);
  analogWrite(speedL, forward_slow_L); //60
  analogWrite(speedR, forward_slow_R); //43
}

long microsecondsToInches(long microseconds) {
  return microseconds / 74 / 2;
}

void loop() {
  int command, response;
  long inchesL, inchesR, inchesM;
  get_ping_data(&inchesL, &inchesR, &inchesM);
  //readSimple(&command);
  
  // No Obstacle
  if (inchesL >= 10 && inchesR >= 10 && inchesM >= 8) 
  { 
    //turnSimple(command);
    //response = SUCCESS;
  } 
  /*
  // Object is what we are trying to follow
  else if (command == STOP){
    halt();
    response = FOUND;
    Serial.println(response);
    return;
  }
  
  // Obstacle only Straight Ahead
  else if (inchesL >= 10 && inchesM < 8 && inchesR >= 10) {
    reverse();
    delay(600);
    while (inchesL < 10 || inchesM < 8 || inchesR < 10){
      switch(command){     
        case FL:
          turnLeft();
          delay(300);
          surveryDirection = LEFT;
          response = 1;
          break;
        case FF:
          turnLeft();
          delay(300);
          surveryDirection = LEFT;
          response = 2;
          break;
        case FR:
          turnRight();
          delay(300);
          surveryDirection = RIGHT;
          response = 2;
          break;
        case SL:
          turnLeft();
          delay(300);
          surveryDirection = LEFT;
          response = 2;
        case SR:
          turnRight();
          delay(300);
          surveryDirection = RIGHT;
          response = 2;
          break;
        case SB:
          reverse();
          delay(300);
          response = OBSTACLE_FORWARD;
          break;
        case NA:
          turnRight();
          delay(300);
          response = OBSTACLE_FORWARD;   
          break;
      }
      get_ping_data(&inchesL, &inchesR, &inchesM);
    }
  } 
  */
  // Obstacle to the Left
  else if (inchesL < 10 && inchesR >= 10) {
    reverse();
    delay(600);
    while (inchesL < 10 || inchesR < 10){
      turnRight();
      delay(300);
      get_ping_data(&inchesL, &inchesR, &inchesM);
    }
    surveryDirection = RIGHT;
    response = OBSTACLE_LEFT; 
  }
 
  // Obstacle to the Right  
  else if (inchesL >= 10 && inchesR < 10) {
    reverse();
    delay(600);
    while (inchesL < 10 || inchesR < 10){
      turnLeft();
      delay(300);
      get_ping_data(&inchesL, &inchesR, &inchesM);
    }
    surveryDirection = LEFT;
    response = OBSTACLE_RIGHT;    
  }   
  
  // Obstacle to the Left, Right and Middle
  else if (inchesL < 10 && inchesM < 8 && inchesR < 10) {
    reverse();
    delay(600);
    while (inchesL < 10 || inchesM < 8 || inchesR < 10){
      turnLeft();
      delay(300);
      get_ping_data(&inchesL, &inchesR, &inchesM);
    }
    
    surveryDirection = LEFT;
    response = OBSTACLE_ALL;    
  }
  
  Serial.println(response);
}
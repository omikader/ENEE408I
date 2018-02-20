int InA1 = 12;
int InB1 = 13;
int InA2 = 7;
int InB2 = 8;

int PWM1 = 3; // PWM1 connects to pin 3
int PWM2 = 5; // PWM2 connects to pin 5
int PWM1_val = 32; // (25% = 64; 50% = 127; 75% = 191; 100% = 255)
int PWM2_val = 50; // (25% = 64; 50% = 127; 75% = 191; 100% = 255)

void setup() {
  Serial.begin(9600);
  pinMode(InA1, OUTPUT);
  pinMode(InB1, OUTPUT);
  pinMode(InA2, OUTPUT);
  pinMode(InB2, OUTPUT);
  pinMode(PWM1, OUTPUT);
  pinMode(PWM2, OUTPUT);
}

void loop() {
  digitalWrite(InA1, HIGH);
  digitalWrite(InB1, LOW);
  digitalWrite(InA2, HIGH);
  digitalWrite(InB2, LOW);
  analogWrite(PWM1, PWM1_val);
  analogWrite(PWM2, PWM2_val);
}

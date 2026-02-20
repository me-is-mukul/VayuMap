#define sensor_A A0
#define sensor_B A1
#define sensor_C A2
#define sensor_D A3
#define sensor_E A4

void setup() {
  Serial.begin(9600);
  Serial.println("Preheating all MQ-135 sensors...");
  delay(90000); // 90 sec
  Serial.println("Preheat complete");
}

void loop() {
  
}

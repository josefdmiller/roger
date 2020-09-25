#include <Wire.h>
//motors
int pin_1 = 2;
int pin_2 = 3;
int pin_3 = 5;
int pin_4 = 6;
//distance sensors
int trig_1 = 49;
int trig_2 = 51;
int trig_3 = 53;
int echo_1 = 43;
int echo_2 = 45;
int echo_3 = 47;
//potentiometer
int pot_pin = A11;
int input_value;
int output_value;
//led
int led_pin = 10;
int freq = 1;

int counter = 0;
int k;

void setup()
{
    Wire.begin(0x8);
    Wire.onReceive(receive_event);
    Serial.begin(9600);
    pinMode(pin_1, OUTPUT);
    pinMode(pin_2, OUTPUT);
    pinMode(pin_3, OUTPUT);
    pinMode(pin_4, OUTPUT);
    pinMode(led_pin, OUTPUT);
    pinMode(trig_1, OUTPUT);
    pinMode(echo_1, INPUT);
    pinMode(trig_2, OUTPUT);
    pinMode(echo_2, INPUT);
    pinMode(trig_3, OUTPUT);
    pinMode(echo_3, INPUT);
    digitalWrite(led_pin, HIGH);
    k = motor_speed();
}

void loop()
{
    /* if (get_distance(trig_1, echo_1, 100) < 10) {
            right(255);
            delay(300);
            stop();
    }
    if (get_distance(trig_2, echo_2, 100) < 10) {
            backward(200);
            delay(300);
            right(255);
            delay(300);
            stop();
            ++counter;
            if (counter == 3) {
                    stop();
                    delay(2000);
                    left(255);
                    delay(700);
                    counter = 0;
            }
    }
    if (get_distance(trig_3, echo_3, 100) < 10) {
            left(255);
            delay(100);
            stop();
    }else{
            stop();
    } */
}

void receive_event(int how_many)
{
    int x = Wire.read();
    int k = motor_speed();
    if (x == 0) {
        forward(k);
    }
    if (x == 1) {
        left(255);
    }
    if (x == 2) {
        right(255);
    }
    if (x == 3) {
        backward(k);
    }
    if (x == 4) {
        stop();
    }
    if (x == 5) {
        digitalWrite(led_pin, LOW); 
    }
    if (x == 6) {
        digitalWrite(led_pin, HIGH);
    }
}

int get_distance(int trig, int echo, int max)
{
    int pulse_start;
    int pulse_end;
    int pulse_duration;
    int distance;
    digitalWrite(trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig, LOW);
    while (digitalRead(echo) == LOW) {
        pulse_start = micros();
    }
    while (digitalRead(echo) == HIGH) {
        pulse_end = micros();
    }
    pulse_duration = pulse_end - pulse_start;
    distance = pulse_duration * (0.0343 / 2);
    if (distance > 0 && distance <= max) {
        return distance;
    }else{
        return max;
    }
}

void pulse_led(int freq)
{
    for (int i = 0; i <= 255; i = i + 1 ) {
        //Serial.println(i);
        analogWrite(led_pin, i);
        delay(freq);
        if (i == 255) {
            for (i = 255; i >= 0; i = i - 1) {
                //Serial.println(i);
                analogWrite(led_pin, i);
                delay(freq);
            }
        }
    }
  
}

int motor_speed()
{
    input_value = analogRead(pot_pin);
    output_value = (255.0/1023.0) * input_value;
    return output_value;
}

void forward(int duty_cycle)
{
    digitalWrite(pin_1, LOW);
    analogWrite(pin_2, duty_cycle);
    analogWrite(pin_3, duty_cycle);
    digitalWrite(pin_4, LOW);
}

void left(int duty_cycle)
{
    digitalWrite(pin_1, LOW);
    digitalWrite(pin_2, LOW);
    analogWrite(pin_3, duty_cycle);
    analogWrite(pin_4, duty_cycle);
}

void right(int duty_cycle)
{
    analogWrite(pin_1, duty_cycle);
    analogWrite(pin_2, duty_cycle);
    digitalWrite(pin_3, LOW);
    digitalWrite(pin_4, LOW);
}

void backward(int duty_cycle)
{
    analogWrite(pin_1, duty_cycle);
    digitalWrite(pin_2, LOW);
    digitalWrite(pin_3, LOW);
    analogWrite(pin_4, duty_cycle);
}

void stop()
{
    digitalWrite(pin_1, LOW);
    digitalWrite(pin_2, LOW);
    digitalWrite(pin_3, LOW);
    digitalWrite(pin_4, LOW);
}
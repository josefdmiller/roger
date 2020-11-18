#include "Arduino.h"
#include "robot.h"

HCSR04::HCSR04(int trig, int echo, int max_dist)
{
    this->trig = trig;
    this->echo = echo;
    this->max_dist = max_dist;
    pinMode(trig, OUTPUT);
    pinMode(echo, INPUT);
}

float HCSR04::get_distance()
{
    float pulse_start;
    float pulse_end;
    float pulse_duration;
    float distance;
    digitalWrite(trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig, LOW);
    while (digitalRead(echo) == LOW)
    {
        pulse_start = micros();
    }
    while (digitalRead(echo) == HIGH)
    {
        pulse_end = micros();
    }
    pulse_duration = pulse_end - pulse_start;
    distance = pulse_duration * (0.0343 / 2);
    if (distance > 0 && distance <= max_dist)
    {
        return distance;
    }
    else
    {
        return max_dist;
    }
}

Robot::Robot(int pin_1, int pin_2, int pin_3, int pin_4)
{
    this->pin_1 = pin_1;
    this->pin_2 = pin_2;
    this->pin_3 = pin_3;
    this->pin_4 = pin_4;
    pinMode(pin_1, OUTPUT);
    pinMode(pin_2, OUTPUT);
    pinMode(pin_3, OUTPUT);
    pinMode(pin_4, OUTPUT);
}

void Robot::forward(int speed)
{
    analogWrite(pin_1, speed);
    analogWrite(pin_2, 0);
    analogWrite(pin_3, speed);
    analogWrite(pin_4, 0);
}
void Robot::left(int speed)
{
    analogWrite(pin_1, 0);
    analogWrite(pin_2, speed);
    analogWrite(pin_3, speed);
    analogWrite(pin_4, 0);
}
void Robot::right(int speed)
{
    analogWrite(pin_1, speed);
    analogWrite(pin_2, 0);
    analogWrite(pin_3, 0);
    analogWrite(pin_4, speed);
}
void Robot::backward(int speed)
{
    analogWrite(pin_1, 0);
    analogWrite(pin_2, speed);
    analogWrite(pin_3, 0);
    analogWrite(pin_4, speed);
}
void Robot::stop()
{
    analogWrite(pin_1, 0);
    analogWrite(pin_2, 0);
    analogWrite(pin_3, 0);
    analogWrite(pin_4, 0);
}
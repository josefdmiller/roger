#include <robot.h>

int left_trig = 6;
int center_trig = 5;
int right_trig = 4;
int left_echo = 12;
int center_echo = 8;
int right_echo = 7;
int motor_1 = 11;
int motor_2 = 10;
int motor_3 = 9;
int motor_4 = 3;
int bumper = 13;
int max_dist = 100;
int min_dist = 15;
int spd = 120;
char data;

HCSR04 left_sonar(left_trig, left_echo, max_dist);
HCSR04 center_sonar(center_trig, center_echo, max_dist);
HCSR04 right_sonar(right_trig, right_echo, max_dist);
Robot robot(motor_1, motor_2, motor_3, motor_4);

void setup()
{
    Serial.begin(9600);
    pinMode(bumper, INPUT);
}

void loop()
{
    if (left_sonar.get_distance() < min_dist)
    {
        robot.right(spd); 
    }
    if (center_sonar.get_distance() < min_dist || digitalRead(bumper) == LOW)
    {
        robot.backward(spd);
        robot.right(spd);
    }
    if (right_sonar.get_distance() < min_dist)
    {
        robot.left(spd);
    }
    if (Serial.available() > 0)
    {
        data = Serial.read();
        if (data == '1')
        {
            robot.forward(spd);
        }
        if (data == '2')
        {
            robot.left(spd);
        }
        if (data == '3')
        {
            robot.right(spd);
        }
        if (data == '4')
        {
            robot.backward(spd);
        }
        if (data == '5')
        {
            robot.stop();
        }
    }
    else
    {
        robot.stop();
    }
}

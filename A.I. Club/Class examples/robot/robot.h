#ifndef ROBOT_H
#define ROBOT_H
#include "Arduino.h"

class HCSR04
{
    private:
        int trig;
        int echo;
        int max_dist;
    public:
        HCSR04(int trig, int echo, int max_dist);
        float get_distance();   
};

class Robot
{
    private:
        int pin_1;
        int pin_2;
        int pin_3;
        int pin_4;
    public:
        Robot(int pin_1, int pin_2, int pin_3, int pin_4);
        void forward(int speed);
        void left(int speed);
        void right(int speed);
        void backward(int speed);
        void stop();
};

#endif
# roger
Autonomous Robot Project

Description:
This robot contains 3 devices that communicate with each other via i2c. The master device is the Raspberry pi 4 running Raspbian OS. The two slave devices are an Arduino Mega and a PCA9685.

Arduino Mega: this is responsible for the lower lever functions of the robot to include, obstacle avoidance with distance sensors (HC-SR04), a bumper switch, two motor drivers for control of the 4 motors, and various LEDs. The motor speed is controlled with an analog input pin that reads a value from a user-controlled potentiometer during the void setup () function on the micro controller startup. This was done to allow quick speed adjustment without having to open the code and change variables.

PCA9685: this is the controller for the two servo motors on the pan tilt device for the raspberry pi camera. It had additional connections for more servo motors if needed. It is controlled by the raspberry pi 4.

Raspberry pi 4: this serves as the “brain” of the robot. It is currently running open cv python and has two completed programs. One is a facial detection program using a haar-cascade and the other is a ball follower that uses HSV and contours to track the object. I will put a picture of the code below.

That is the basic functions of the robot. I am interested in projects involving open-cv or tensor flow if anyone has some knowledge on it. My plan is to use this robot as a group project with the direction determined by a group idea. The way I see it going with the current pandemic is the group project involving the code that I would then upload and video the effects on zoom. I also have the hardware to create things like stop lights to simulate a street environment or something like that.

One thing to note is that the arduino ino file is a c++ file however i only used c code.

Project Idea:
I would really like input from the team about the direction to take this. Things I'm interesting in are room mapping, mabey with the distance sensors? object following, a more advance autonomous navigation system. I am planning on buying an add on from google that makes tensor flow run much faster on the Pi so I would be interesting in using that as well.

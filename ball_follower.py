import cv2
import numpy as np
from time import sleep
from smbus import SMBus
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
bottom_servo = 14
upper_servo = 15
address = 0x8
bus = SMBus(1)

camera = cv2.VideoCapture(0)
image_width = 640
image_height = 480
camera.set(3, image_width)
camera.set(4, image_height)
center_image_x = image_width / 2
center_image_y = image_height / 2
minimum_area = 250
maximum_area = 100000
HUE_VAL = 25
lower_color = np.array([HUE_VAL - 10, 100, 100])
upper_color = np.array([HUE_VAL + 10, 255, 255])

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

def forward():
    bus.write_byte(address, 0)
def right():
    bus.write_byte(address, 1)
def left():
    bus.write_byte(address, 2)
def backward():
    bus.write_byte(address, 3)
def stop():
    bus.write_byte(address, 4)

Y_FOV = 48.8   # Camera y fov
Y_WIDTH = 480  # total pixel width
Y_RANGE = 390  # servo pulse (90 deg right) - (90 deg left)
Y_DEG = 180    # 180 degrees

X_FOV = 62.2   # Camera x fov
X_WIDTH = 640  # total pixel width
X_RANGE = 390  # servo pulse (90 deg right) - (90 deg left)
X_DEG = 180    # 180 degrees
position_y = 320  # starting position for the servo
position_x = 320  # starting position for the servo
pwm.set_pwm_freq(60)
pause = 0.05

try:
    pwm.set_pwm(15, 0, position_y)
    pwm.set_pwm(14, 0, position_x)
    while True:
        _, frame = camera.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        color_mask = cv2.inRange(hsv, lower_color, upper_color)
        image2, contours, hierarchy = cv2.findContours(color_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        object_area = 0
        object_x = 0
        object_y = 0
        stop()
        for contour in contours:
            x, y, width, height = cv2.boundingRect(contour)
            found_area = width * height
            center_x = x + (width / 2)
            center_y = y + (height / 2)
            if object_area < found_area:
                object_area = found_area
                object_x = center_x
                object_y = center_y
            if object_area > 0:
                ball_location = [object_area, object_x, object_y]
            else:
                ball_location = None
            if ball_location:
                if (ball_location[0] > minimum_area) and (ball_location[0] < maximum_area):
                    #vertical
                    y_final = ball_location[2]
                    y_initial = 240
                    y_vector = y_final - y_initial
                    y_pw = (Y_RANGE / Y_DEG) * ((Y_FOV / Y_WIDTH) * y_vector)
                    position_y -= y_pw
                    pwm.set_pwm(15, 0, round(position_y))
                    position_y = 320
                    #horizontal
                    x_final = ball_location[1]
                    x_initial = 320
                    x_vector = x_final - x_initial
                    x_pw = (X_RANGE / X_DEG) * ((X_FOV / X_WIDTH) * x_vector)
                    position_x += x_pw
                    pwm.set_pwm(14, 0, round(position_x))
                    position_x = 320

                    if x_pw > -40 and x_pw < 40:
                        stop()
                    if x_pw < -40:
                        right()
                    if x_pw > 40:
                        left()
                         
except KeyboardInterrupt:
    camera.release()
    pwm.set_pwm(15, 0, 320)
    pwm.set_pwm(14, 0, 320)
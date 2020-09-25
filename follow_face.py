from __future__ import division

import cv2
from time import sleep
from smbus import SMBus

from time import sleep
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
target_width = 50 #increases target box
left_limit = int((image_width / 2) - target_width) #target box left limit
right_limit = int((image_width / 2) + target_width) #target box right limit
top_limit = int((image_height / 2) - target_width) #target box top limit
bottom_limit = int((image_height / 2) + target_width) #target box bottom limit
face_cascade = cv2.CascadeClassifier('/home/pi/opencv/haarcascade_frontalface_default.xml')

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
def led_on():
    bus.write_byte(address, 5)
def led_off():
    bus.write_byte(address, 6)
    
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

def servo_left():
    pwm.set_pwm(bottom_servo, 0, 150)

def servo_right():
    pwm.set_pwm(bottom_servo, 0, 540)

def servo_up():
    pwm.set_pwm(upper_servo, 0, 450)

def servo_down():
    pwm.set_pwm(upper_servo, 0, 150)

def servo_center():
    pwm.set_pwm(bottom_servo, 0, 330)
    pwm.set_pwm(upper_servo, 0, 340)

i = 0
position = 340
pwm.set_pwm_freq(60)
servo_center()
while True:
    success, image = camera.read()
    cv2.line(image, (int(image_width / 2) - target_width, 0), (int(image_width / 2 - target_width), 480) , (0, 255, 0), 2) #left line
    #cv2.line(image, (int(image_width / 2), 0), (int(image_width / 2), 480) , (0, 255, 0), 2)
    cv2.line(image, (int(image_width / 2) + target_width, 0), (int(image_width / 2 + target_width), 480) , (0, 255, 0), 2) #right line
    #cv2.line(image, (0, int(image_height / 2) - target_width), (640, int(image_height / 2) - target_width) , (0, 255, 0), 2) #top line
    #cv2.line(image, (0, int(image_height / 2)), (640, int(image_height / 2)) , (0, 255, 0), 2)
    #cv2.line(image, (0, int(image_height / 2) + target_width), (640, int(image_height / 2) + target_width) , (0, 255, 0), 2) #bottom line
    
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(image_gray, 1.1, 4)
    count_faces = len(faces)

    for (x, y, w, h) in faces:
        target = int((x + x + w) / 2)
        cv2.rectangle(image, (x, y), (x + w, y + h) , (0, 0, 255), 2)
        cv2.line(image, (target, 0), (target, 480) , (0, 0, 255), 2)

    if (count_faces == 1):
        #print("face detected")
        i = 0
        if target > right_limit:
            led_off()
            position += 2
        if target < left_limit:
            led_off()
            position -= 2
        if target > left_limit and target < right_limit:
            #print("center")
            led_on()
        pwm.set_pwm(bottom_servo, 0, position)
    elif count_faces != 1:
        #print("no face detected")
        i += 1
        #print(i)
        if i == 20:
            servo_center()
            position = 340
            i = 0
            led_off()


    #cv2.imshow('face detection', image)
    if cv2.waitKey(1) == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

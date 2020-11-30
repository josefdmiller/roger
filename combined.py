import jetson.inference
import jetson.utils
from mysettings import *
import cv2
import numpy as np
import time
import serial
from adafruit_servokit import ServoKit

cam_num = 0
flip = 2
image_width = 1280
image_height = 720
setup = 'nvarguscamerasrc sensor_mode = ' + str(camera) + ' ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method= ' + str(flip) + ' ! video/x-raw, width= ' + str(image_width) + ', height= ' + str(image_height) + ', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink drop=true'
cam = cv2.VideoCapture(setup) # 1280 720
font = cv2.FONT_HERSHEY_SIMPLEX
net = jetson.inference.detectNet('ssd-mobilenet-v2', threshold=.5)
event1 = 0
x_pos = 70
y_pos = 70 #115
pan.angle = x_pos
tilt.angle = y_pos
time_mark = 0
fps = 0
fps_filter = 0
uart = serial.Serial(port="/dev/ttyACM0", baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
servo = ServoKit(channels=16)
pan = servo.servo[0]
tilt = servo.servo[1]

def show_fps():
    global time_mark
    global fps
    global fps_filter
    dt = time.time() - time_mark
    fps = 1 / dt
    fps_filter = .95 * fps_filter + .05 * fps
    time_mark = time.time()
    return round(fps_filter, 1)

def forward():
	uart.write(b'1') 
  
def left():
	uart.write(b'2')

def right():
	uart.write(b'3')

def backward():
	uart.write(b'4')

def stop():
	uart.write(b'5')

while True:
    _, image   = cam.read()
    cuda_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA).astype(np.float32)
    cuda_image = jetson.utils.cudaFromNumpy(cuda_image)
    detections = net.Detect(cuda_image, image_width, image_height)

    for detect in detections:
        class_id   = net.GetClassDesc(detect.ClassID)
        confidence = str(int(detect.Confidence * 100))
        left       = int(detect.Left)
        top        = int(detect.Top)
        right      = int(detect.Right)
        bottom     = int(detect.Bottom)
        area       = int(detect.Area)
        x, y	   = detect.Center
        x_vector   = int(x) - (image_width / 2)
        y_vector   = int(y) - (image_height / 2)
        obj1       = 'stop sign'        
        P = 40
        
        if class_id == obj1: # i could also switch to a color mask to track id an object then jump to the mask
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 1)
            cv2.putText(image, class_id +' '+ confidence +' %', (left + 10, top + 30), font, 1, (0, 0, 255), 2)

            if abs(x_vector) > 15:
                x_pos = x_pos + x_vector / P
                
                if x_pos > 180:
                    x_pos = 180 # i could change the x postion to compensate for the turn
                    print("turning right")
                    
                if x_pos < 0:
                    x_pos = 0
                    print("turning left")
                
            if abs(y_vector) > 15:
                y_pos = y_pos - y_vector / P
                
                if y_pos > 180:
                    y_pos = 180
                    print("backing up")
                    
                if y_pos < 0:
                    y_pos = 0
                    print("backing up")
                         
            pan.angle  = x_pos            
            tilt.angle = y_pos
            print(area)
            while class_id == obj1 and event1 == 0 and area > 150000:
                print('stopping')
                #stop()
                time.sleep(3)
                event1 = 1

    print("forward")                    
    #forward()
    cv2.putText(image, str(show_fps()) + ' fps ', (0, 30), font, 1, (0, 0, 255), 2)
    cv2.imshow('output', image)
    #cv2.moveWindow('output', 0, 0)
    
    if cv2.waitKey(1) == ord('q'):
        break

stop()
pan.angle = 70
tilt.angle = 70
cam.release()
cv2.destroyAllWindows()
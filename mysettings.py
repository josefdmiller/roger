import time
import serial
from adafruit_servokit import ServoKit

camera = 0
flip = 2
image_width = 1280
image_height = 720
setup = 'nvarguscamerasrc sensor_mode = ' + str(camera) + ' ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method= ' + str(flip) + ' ! video/x-raw, width= ' + str(image_width) + ', height= ' + str(image_height) + ', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink drop=true'

time_mark = 0
fps = 0
fps_filter = 0

uart = serial.Serial(port="/dev/ttyACM0", baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

servo = ServoKit(channels=16)
pan = servo.servo[0]
tilt = servo.servo[1]

['detectnet --model=/home/roger/Downloads/jetson-inference/python/training/detection/ssd/models/traffic/ssd-mobilenet.onnx --labels=/home/roger/Downloads/jetson-inference/python/training/detection/ssd/models/traffic/labels.txt --input-blob=input_0 --output-cvg=scores --output-bbox=boxes']

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
 
"""
class_id = detect.ClassID
confidence = detect.Confidence
left = detect.Left
top = detect.Top
right = detect.Right
bottom = detect.Bottom
width = detect.Width
height = detect.Height
area = detect.Area
center = detect.Center
"""

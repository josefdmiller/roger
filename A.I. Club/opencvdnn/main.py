from cv2 import cv2
import time

class_names = {0: 'background',
              1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
              7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
              13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
              18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
              24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
              32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
              37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
              41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
              46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
              51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
              56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
              61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
              67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
              75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
              80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
              86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}

def id_class_name(class_id, class_names):
    for key, value in class_names.items():
        if class_id == key:
            return value

cap = cv2.VideoCapture(0)
# this is the deep neural network(dnn). The .pbtxt is the opencv conversion of the .pb file. .pb is for protobuf which is the file extension for a tensorflow dnn.
config_path = 'graph.pbtxt'
weights_path = 'frozen_inference_graph.pb'
net = cv2.dnn.readNetFromTensorflow(weights_path, config_path) # this creates a dnn object called net from the two files passed in.

while True:
    success, image = cap.read()
    net.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True)) # the point of this method is to convert the image into a format that the dnn can use. Called a blob.
    output = net.forward() # net.forward() is the passing of the blob through the network. The result is called the output. It is this output that we can pull information from.
    img_h, img_w, _ = image.shape # this creates two variables from the image shape, height and width. We don't care about the 3rd value depth so we pass it into an unused variable called _.
    for detection in output[0, 0, :, :]: # this is going to iterate over the values of the output variable. What we care about is the detection values.
        confidence = detection[2]
        if confidence > 0.7: # you can change this higher or lower. For example if my computer is only 50% sure it is a human it will not label it as one.
            class_id = detection[1]
            class_label=id_class_name(class_id,class_names) # detection[1] is the class_id, this function is defined above and will return the matching label.
            x = int(detection[3] * img_w) # x position # the following are very important for us because this is how we can tell the robot where stuff is in the image.
            y = int(detection[4] * img_h) # y position # if you print(detection[3]) for example it will display the x coordinate of the object.
            w = int(detection[5] * img_w) # width
            h = int(detection[6] * img_h) # height
            cv2.rectangle(image, (x, y, w, h), (0, 255, 0), thickness=2) # these next two are what labels and boxes the discovered objects.
            cv2.putText(image,class_label, (x, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('output', image)
        if cv2.waitKey(1) == ord("q"):
            break
cv2.destroyAllWindows()

    





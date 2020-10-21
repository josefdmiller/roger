from cv2 import cv2

camera = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    success, image = camera.read()
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(image_gray, 1.1, 4)
    count_faces = len(faces)

    for (x, y, w, h) in faces:
        target = int((x + x + w) / 2)
        cv2.rectangle(image, (x, y), (x + w, y + h) , (0, 0, 255), 2)
    cv2.imshow('face detection', image)
    if cv2.waitKey(1) == ord("q"):
        break
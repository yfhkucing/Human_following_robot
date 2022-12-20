import cv2 as cv
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
from time import sleep
from pyfirmata import Arduino, SERVO, util, PWM, OUTPUT
from actuator import control as control
from actuator import servo1 as servo1
from actuator import servo2 as servo2

#center the camera servo 
servo1(105)
servo2(50)

#get the middle of the screen
x_medium = int(672 / 2)
y_medium = int(648/2)
center = int(672 / 2)
ycenter = int(648/2)
position = 90 # degrees
positiony = 90

# Load the model.
net = cv.dnn.readNet('face-detection-adas-0001.xml',
'face-detection-adas-0001.bin')
# Specify target device.
net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)
# Read an image.
vs = VideoStream(usePiCamera=True).start()
sleep(2.0)
fps = FPS().start()

while True :
    image = vs.read()
    image = imutils.resize(image, width=672,height=384)
    frame = imutils.rotate(image,180)
    # Prepare input blob and perform an inference.
    blob = cv.dnn.blobFromImage(frame, size=(672, 384), ddepth=cv.CV_8U)
    net.setInput(blob)
    out = net.forward()
    # Draw detected faces on the frame.
    for detection in out.reshape(-1, 7):
        confidence = float(detection[2])
        xmin = int(detection[3] * frame.shape[1])
        ymin = int(detection[4] * frame.shape[0])
        xmax = int(detection[5] * frame.shape[1])
        ymax = int(detection[6] * frame.shape[0])
    if confidence > 0.5:
        cv.rectangle(frame, (xmin, ymin), (xmax, ymax), color=(0, 255, 0))
        x_medium = int((xmin + xmax) / 2)
        y_medium = int((ymin + ymax) / 2)
        # Save the frame to an image file.
    cv.imshow('out', frame)
    pwmLeft=0.393
    pwmRight=0.393
    if x_medium < center -30:
        pwmLeft -= 0.1
        pwmRight += 0.1
    elif x_medium > center + 30:
        pwmLeft += 0.1
        pwmRight -= 0.1
    if y_medium < ycenter -200 :
        pwmLeft = 0
        pwmRight = 0
    
    control("forward","right",pwmRight)
    control("forward","left",pwmLeft)
    key = cv.waitKey(1) & 0xFF
    if key == ord("q"):
        break
fps.update()
control("forward","right",0)
control("forward","left",0)
fps.stop()
cv.destroyAllWindows()
vs.stop()
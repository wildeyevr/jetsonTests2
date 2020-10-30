import jetson.inference
import jetson.utils
from adafruit_servokit import ServoKit
import time


net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=.25)
camera = jetson.utils.videoSource("csi://0")  # '/dev/video0' for V4L2
kit = ServoKit(channels=16)
kit.servo[3].angle = 180

xAngle = 0
lastRectCenter = .5
scanMode = True
thresh = 0

while True:
    img = camera.Capture()
    width = img.width
    detections = net.Detect(img)
    if detections:
        scanMode = False
        print(detections[0].Confidence)
        # print('tracking...')
    else:
        scanMode = True
        # print('scanning...')

    if not scanMode:
        if net.GetClassDesc(detections[0].ClassID) == 'person':
            curRectCenter = detections[0].Center[0] / width
            imageCenterX = .5

            if curRectCenter >= .75:
                if abs(curRectCenter - lastRectCenter) > .1:
                    xAngle -= 15
            elif curRectCenter >= .5:
                if abs(curRectCenter - lastRectCenter) > .1:
                    xAngle -= 5
            elif .5 > curRectCenter > .25:
                if abs(curRectCenter - lastRectCenter) > .1:
                    xAngle += 5
            else:
                if abs(curRectCenter - lastRectCenter) > .1:
                    xAngle += 15

            # if not any([xAngle > 180, xAngle < 0]):
            try:
                kit.servo[0].angle = xAngle
            except ValueError:
                # print('probably out of range')
                pass
    else:

        x = 0
        y = 180
        for x in range(xAngle, 180):
            if not detections:
                try:
                    kit.servo[0].angle = x
                    time.sleep(.01)
                except ValueError:
                    pass
            else:
                break
        for y in range(180, xAngle, -1):
            if not detections:
                try:
                    kit.servo[0].angle = y
                    time.sleep(.01)
                except ValueError:
                    pass
            else:
                break

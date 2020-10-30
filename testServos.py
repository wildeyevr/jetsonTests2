from adafruit_servokit import ServoKit
import time
from inputs import get_gamepad


def norm(x, min, max, a, b):
    return (b - a) * ((x - min) / (max - min)) + a


kit = ServoKit(channels=16)

while True:
    events = get_gamepad()
    for event in events:
        print(event.ev_type, event.code, event.state)
        if event.code == 'ABS_X':
            val = norm(int(event.state), -32768, 32768, 0, 180)
            print(val)
            try:
                kit.servo[0].angle = int(val)
            except ValueError:
                print('servo didnt like that')
                pass
        elif event.code == 'ABS_RY':
            val = norm(int(event.state), -32768, 32768, 90, 180)
            print(val)
            try:
                kit.servo[3].angle = int(val)
            except ValueError:
                print('servo didnt like that')
                pass

# while True:
#     for x in range(0, 180):
#         kit.servo[0].angle = x
#         time.sleep(.005)
#     for x in range(180, 0, -1):
#         kit.servo[0].angle = x
#         time.sleep(.005)

# while True:
#     kit.servo[0].angle = 0
#     kit.servo[1].angle = 180
#     time.sleep(2)
#     kit.servo[0].angle = 180
#     kit.servo[1].angle = 100
#     time.sleep(2)
#     kit.servo[0].angle = 0
#     kit.servo[1].angle = 180

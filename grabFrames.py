import cv2
import os
import numpy as np

# from nanocamera.NanoCam import Camera
import nanocamera as nano

execution_path = os.getcwd()

# dst params... from the calibrate program... prolly shouldn't be hard coded...
# TODO: must recompute lens parameters... this is from the usb cam... even thougb the lens is close
K = np.array([[232.69020493541737, 0.0, 315.87549701796297],
                           [0.0, 231.93744414999705, 243.83063447957753], [0.0, 0.0, 1.0]])
D = np.array([[-0.03927332854943311], [-0.011053135772018392],
                           [0.00304440683492916], [-0.00035261943523912445]])


def undistort(img, K, D):
    """undst the img"""
    # don't forget to scale the output to rectilinear
    k_new = K.copy()
    k_new[(0, 1), (0, 1)] = 0.4 * k_new[(0, 1), (0, 1)]

    # undst the img
    undistorted_img = cv2.fisheye.undistortImage(img, K=K, D=D, Knew=k_new)
    return undistorted_img


# Create the Camera instance
camera = nano.Camera(flip=0, width=640, height=480, fps=30)
print('CSI Camera is now ready')
for x in range(0, 50):
    try:
        # read the camera image
        frame = camera.read()
        # frame = undistort(frame, K, D)
        if not os.path.exists('./calibrationFrames'):
            os.mkdir('./calibrationFrames')
        # display the frame
        cv2.imwrite('./calibrationFrames/' + str(x).zfill(2) + '.png', frame)
        print('wrote ' + str(x))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    except KeyboardInterrupt:
        break

# close the camera instance
camera.release()

# remove camera object
del camera

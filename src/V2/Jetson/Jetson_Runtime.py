import platform
import cv2
from PIL import ImageOps, Image
import numpy as np
import tensorflow.keras
from socket import socket
import time

HOST = '3.21.205.199'  # Host server addr
PORT = 12345 # Host server port


HumanDetector = cv2.CascadeClassifier(cv2.haarcascades + 'haarcascade_frontalface_default.xml')
HumanIdentifierModel = tensorflow.keras.models.load_model('keras_model.h5')


def check_win():
    if platform.machine() == "AMD64":
        return True
    return False

def get_jetson_gstreamer_source(capture_width=1280, capture_height=720, display_width=640, display_height=480,
                                framerate=30, flip_method=2):
    """
    Return an OpenCV-compatible video source description that uses gstreamer to capture video from the camera on a Jetson Nano
    """
    return (
            f'nvarguscamerasrc ! video/x-raw(memory:NVMM), ' +
            f'width=(int){capture_width}, height=(int){capture_height}, ' +
            f'format=(string)NV12, framerate=(fraction){framerate}/1 ! ' +
            f'nvvidconv flip-method={flip_method} ! ' +
            f'video/x-raw, width=(int){display_width}, height=(int){display_height}, format=(string)BGRx ! ' +
            'videoconvert ! video/x-raw, format=(string)BGR ! appsink')

def initCamera():
    if check_win():
        return cv2.VideoCapture(0)
    return cv2.VideoCapture(get_jetson_gstreamer_source())

def preFormat(image):
    frame = Image.fromarray(image)
    return (np.asarray(ImageOps.fit(frame, (224, 224), Image.ANTIALIAS)).astype(np.float32) / 127) - 1

def waitForHuman(image):
    # non-blocking, check vs, if human return true, if not return false
    tmp = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    try:
        rect = HumanDetector.detectMultiScale(tmp, scaleFactor=1.1, minNeighbors=5)
        print(rect[0])
        return True
    except Exception as exc:
        print("Wait for Human, Error:")
        print(exc)
        return False

def identifyHuman(image):
    # when human in img, identify human, return the label number
    try:
        tmp = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rect = HumanDetector.detectMultiScale(tmp, scaleFactor=1.1, minNeighbors=5)

        for (x, y, h, w) in rect:
            tmp = image[y:y+h, x:x+w]

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = preFormat(tmp)
        predictions = HumanIdentifierModel.predict(data).tolist()

        if predictions != None:
            max = 0
            indx = 0
            counter = 0

            for p in predictions[0]:
                if max < p:
                    max = p
                    indx = counter
                counter += 1

        return [max, indx]
    except Exception as exc:
        print("Identify Human, Error:")

def signal_server(emp_number:int):
    try:
        conn = socket()
        conn.connect((HOST,PORT))
        conn.sendall(str.encode("Jetson"))
        if conn.recv(256).decode() == "posak":
            try_again = True
            while try_again:
                conn.sendall(str.encode(f"{1},{1},{emp_number}"))
                if conn.recv(256).decode() == "posak":
                    try_again = False
        conn.sendall(str.encode("66"))

    except socket.error as e:
        print(e)
    finally:
        conn.detach()


if __name__ == "__main__":
    vs = initCamera()
    running = True

    while running:
        im = vs.read()[1]
        cv2.waitKey(2)
        if waitForHuman(im):
            emp = identifyHuman(im)[1]
            signal_server(emp)

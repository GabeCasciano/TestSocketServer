import cv2
from PIL import ImageOps, Image
import numpy as np
import tensorflow.keras
from socket import socket
import time

HOST = '3.21.205.199'  # Host server addr
PORT = 12345 # Host server port

HumanDetector = cv2.CascadeClassifier('~/opencv/data/haarcascade_frontalface_default.xml')
HumanIdentifierModel = tensorflow.keras.models.load_model('keras_model.h5')

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
    return cv2.VideoCapture(get_jetson_gstreamer_source())

def preFormat(img):
    frame = Image.fromarray(img)
    return (np.asarray(ImageOps.fit(frame, (224, 224), Image.ANTIALIAS)).astype(np.float32) / 127) - 1

def waitForHuman(img):
    # non-blocking, check vs, if human return true, if not return false
    tmp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    try:
        rect = HumanDetector.detectMultiScale(tmp, scaleFactor=1.1, minNeighbors=5)
    except Exception:
        return False

    return True

def identifyHuman(img):
    # when human in img, identify human, return the label number

    tmp = tmp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rect = HumanDetector.detectMultiScale(tmp, scaleFactor=1.1, minNeighbors=5)

    for (x,y,h,w) in rect:
        img = img[y:y+h, x:x+w]

    img = preFormat(img)

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = img
    predictions = HumanIdentifierModel.predict(data)

    maximum = max(predictions)
    max_index = predictions.index(maximum)

    return [maximum, max_index]

def signalServer(empNum : int):
    # connect to the server, send check-in command, and disconnect
    sock = socket()
    sock.connect((HOST, PORT))
    data = str.encode(f"/login,jetson,jet123") # log jetson onto server
    sock.sendall(data)
    if sock.recv(1024).decode() == "/yes": #
        data = str.encode(f"/check_in,2,{empNum}")
        sock.sendall(data)
        if sock.recv(1024).decode().split(",")[0] == True:
            sock.detach()
            return True
        else:
            sock.detach()
            return False
    else:
        sock.detach()
        return False


vs = initCamera() # init the camera stream
running = True

while running:

    img = vs.read()[1] # image to find human from
    if waitForHuman(img): # waiting for a human to appear
        img = vs.read()[1] # image to identify human from
        identified_emp = identifyHuman(img) # identify the appeared human
        signalServer(identified_emp) # tell the server who we saw
    else:
        time.sleep(2)



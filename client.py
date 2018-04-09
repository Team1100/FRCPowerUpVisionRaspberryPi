import numpy as np
import cv2
from grip import GripPipeline
from networktables import NetworkTables, NetworkTablesInstance
from cscore import CameraServer
import threading
import logging
logging.basicConfig(level=logging.DEBUG)

import time

def main():
    """Run this file to process vision code.
    Please go to README.md to learn how to use this properly
    By Grant Perkins, 2018
    """
    # Initialize pipeline, image, camera server
    pipe = GripPipeline()
    img = np.zeros(shape=(480, 640, 3), dtype=np.uint8)

    cs = CameraServer.getInstance()
    camera = cs.startAutomaticCapture()
    camera.setResolution(640, 480)
    camera.setFPS(20)
    camera.setExposureManual(40)

    # Get a CvSink. This will capture images from the camera
    cvsink = cs.getVideo()
    # Wait on vision processing until connected to Network Tables
    cond = threading.Condition()
    notified = [False]

    def listener(connected, info):
        print(info, '; Connected=%s' % connected)
        with cond:
            notified[0] = True
            cond.notify()

    NetworkTables.initialize(server='roborio-1100-frc.local')
    NetworkTables.addConnectionListener(listener, immediateNotify=True)

    with cond:
        print("Waiting")
        if not notified[0]:
            # Wait until connected. cond.wait() is exited once listener is called by ConnectionListener
            cond.wait()
    print("Connected!")
    table = NetworkTablesInstance.getDefault().getTable("Pi")

    imagetaken = False
    last = -1
    while True:
        time.sleep(.4)
        # Tell the CvSink to grab a frame from the camera and put it
        # in the source image.  If there is an error notify the output.
        t, img = cvsink.grabFrame(img)
        if t == 0:
            continue
        pipe.process(img)
        cx, cy = pipe.get_centeroid()
        area = pipe.get_area()
        print(cx)

        if cx != last and cx != -1:
            print(cx)
            last = cx

        table.getEntry("centerx").setDouble(cx)
        table.getEntry("centery").setDouble(cy)
        table.getEntry("area").setDouble(area)

    #print(pipe.process(cv2.imread("img\cubecorner.jpg",1))) #to test pipeline

if __name__ == "__main__":
    # This if statement is basically Python's equivalent of Java's
    # public static void main(String args)
    main()

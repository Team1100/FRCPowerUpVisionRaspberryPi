import numpy as np
import cv2
from grip import GripPipeline
from networktables import NetworkTables, NetworkTablesInstance
from cscore import CameraServer
import logging
logging.basicConfig(level=logging.DEBUG)
"""
Run this file to process vision code.
Please go to README.md to learn how to use this properly
By Grant Perkins, 2018
"""
def main():
    # Initialize pipeline, Network Tables, image, camera server
    pipe = GripPipeline()
    NetworkTables.initialize(server="roborio-1100-frc.local")
    table = NetworkTablesInstance.getDefault().getTable('SmartDashboard')
    img = np.zeros(shape=(480, 640, 3), dtype=np.uint8)
    cs = CameraServer.getInstance()
    camera = cs.startAutomaticCapture()
    camera.setResolution(640, 480)

    # Get a CvSink. This will capture images from the camera
    cvsink = cs.getVideo()

    while True:
        # Tell the CvSink to grab a frame from the camera and put it
        # in the source image.  If there is an error notify the output.
        time, img = cvsink.grabFrame(img)
        cx, cy = pipe.process(img)
        table.getEntry("centerx").setNumber(cx)
        table.getEntry("centery").setNumber(cy)

    #print(pipe.process(cv2.imread("cubecorner.jpg",1))) #to test pipeline

if __name__ == "__main__":
    # This if statement is basically Python's equivalent of Java's
    # public static void main(String args)
    main()
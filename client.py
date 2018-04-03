import numpy as np
import cv2
from grip import GripPipeline
from networktables import NetworkTables, NetworkTablesInstance
from networktables.util import ntproperty
import logging
from cscore import CameraServer
logging.basicConfig(level=logging.DEBUG)
"""
Run this file to process vision code.

0,0 is top left.

By Grant Perkins, 2018
"""
def main():
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
        table.getEntry("centerx").forceSetNumber(cx)
        table.getEntry("centery").forceSetNumber(cy)

    #print(pipe.process(cv2.imread("cubecorner.jpg",1))) #to test pipeline

if __name__ == "__main__":
    main()
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
    camera.setFPS(20)

    # Get a CvSink. This will capture images from the camera
    cvsink = cs.getVideo()

    #Status of Network Tables
    modes = {1: "Server", 2: "Client", 4: "Starting", 8: "Failure", 16: "Test"}
    last_modes = []
    mode = NetworkTables.getNetworkMode()

    while True:
        # Main loop

        # Tell the CvSink to grab a frame from the camera and put it
        # in the source image.  If there is an error notify the output.
        time, img = cvsink.grabFrame(img)
        if time == 0: continue
        pipe.process(img)

        cx, cy = pipe.get_centeroid()
        area = pipe.get_area()
        table.getEntry("centerx").setDouble(cx)
        table.getEntry("centery").setDouble(cy)
        table.getEntry("area").setDouble(area)

        # Gets mode of Network Tables, puts that to stdout
        tmp = []
        for n in modes.keys():
            if modes[n] not in last_modes and mode & n:
                tmp.append(modes[n])
        if len(tmp) != 0:
            print("NetworkTables mode:", " ".join(tmp))
            last_modes = tmp

    #print(pipe.process(cv2.imread("img\cubecorner.jpg",1))) #to test pipeline

if __name__ == "__main__":
    # This if statement is basically Python's equivalent of Java's
    # public static void main(String args)
    main()
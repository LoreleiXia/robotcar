import cv2
import numpy as np
import time
import cv2
from picamera2 import Picamera2, Preview, MappedArray

def colorpicker2hsv(hue, sat, val):
    xp = [0,360]
    fp = [0,255]
    hue = np.interp(hue, xp, fp)
    sat = (sat/100)*255
    val = (val/100)*255
    return np.array([hue, sat, val])


# Configure camera image types
picam2 = Picamera2()
config = picam2.still_configuration(main={"size": (320, 240)})
picam2.configure(config)

# Configure camera to be able to take pictures
picam2.start()
def ballposition():

    start_time = time.monotonic()
    # Get color and convert to gray-scale
    buffer = picam2.capture_array()
   
    color = cv2.cvtColor(buffer, cv2.COLOR_RGB2BGR)

    # cv2.imwrite('color.jpg', color)

    hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)


    # Threshold of blue in HSV space
    lower_blue = np.array([135, 45, 100]) # Darker bound of color
    upper_blue = np.array([170, 255, 255]) # Lighter bound of color

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # cv2.imwrite('binary.jpg', mask)

    cx = 0
    cy = 0
    count = 0 

    for i in range(0,240): 
       
        for j in range(0,320):
            pixel = mask[i][j]

            if(pixel == 255):
                cx = cx + j
                cy = cy + i 
                count += 1 
    if(count > 0):
        cx = int(cx/count)
        cy = int(cy/count)
        
        cv2.circle(buffer,(cx,cy), 5, (0,0,255), 1)
        cv2.imwrite('reticle.jpg', buffer)


    end_time = time.monotonic()
    # print((end_time - start_time))

    return cx/320, cy/240 
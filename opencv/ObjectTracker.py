import cv2 
import numpy as np 
from GetFileData import GetFileData


# Author: Michael Tinglof 6/21/19
#     class used for returning contours and boundingboxes 
#       for passed objects 
class ObjectTracker():     

#   method that applies predetermined image processing method 
#   this method may need to be adaptid later on based on different 
#   image qualities. This method was found to be the most robust at the   
#   time of research. Image passed is assumed to be in 16bit format 
    def getContours(img): 
        ratio = np.amax(img) / 256 
        img = (img / ratio).astype('uint8')
        cv2.imwrite("cv_image.jpeg", img)
        img = cv2.imread("cv_image.jpeg", 0)
        
        #clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8,8))
        #img = clahe.apply(img)
        #img = cv2.GaussianBlur(img,(11,11),0)
        #img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,101,5)
        #img = cv2.erode(img, None, iterations=6)
        #img = cv2.dilate(img, None, iterations=10)
        #cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        
        
        img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,201,3)
        img = cv2.erode(img, None, iterations=2)
        img = cv2.dilate(img, None, iterations=12)
        cnts = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

        
        return(cnts)
    
#   returns a bounding box of a passed countour, will pass None if the bounding box
#   is too large 
    def getBoundingBox(cnt): 
        newbox = cv2.boundingRect(cnt)
        if (newbox[2] < 200 and newbox[3] < 200): 
            #p1 = (int(newbox[0]), int(newbox[1]))
            #p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            return(newbox)
        else: 
            return None
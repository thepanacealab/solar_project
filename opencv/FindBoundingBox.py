import cv2 
import numpy as np

#THIS CODE IS OUTDATED, NO LONGER USED 

# Author: Michael Tinglof 6/20/19
#     Contrustor takes in a image file name. The class will then allow a user to 
#     create bounding boxes over the image and the coordinates of those boxes will
#     be returned 
    
#     @param: name of image file to be opened  
class FindBoundingBox(): 
    def __init__(self, image_name): 
        self.image_name = image_name 
        
#   Main method that allows the user to open an image file, define a bounding box
#   and have those coordinates returned in console 
    def findBoxes(self): 
        frame = self.compressImage(cv2.imread(self.image_name, 0))
        cv2.namedWindow('Tracker', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Tracker', 400, 400)
        bbox = cv2.selectROI('Tracker', frame)
        print(bbox)
        cv2.waitKey(0)
            
#   Helper method to compress 16bit images to 8bit images 
#   params: image file to be compressed
#   returns: compressed file 
    def compressImage(self, image): 
        ratio = np.amax(image)/256
        compressed_image = (image/ratio).astype('uint8')
        return(compressed_image)
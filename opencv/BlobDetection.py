import cv2
import numpy as np

import matplotlib.pyplot as plt

#THIS CLASS IS OUTDATED, NO LONGER USED 

class BlobDetection(): 
    def __init__(self, image): 
        self.image = image
        self.setParams()
        self.compressImage()
        self.detectBlobs()
        
    def setParams(self): 
        # Setup SimpleBlobDetector parameters.
        params = cv2.SimpleBlobDetector_Params()

        # Change thresholds
        params.minThreshold = 10;
        params.maxThreshold = 10000;

        # Filter by Area.
        params.filterByArea = True
        params.minArea = 1

        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = 0.01

        # Filter by Convexity
        params.filterByConvexity = True
        params.minConvexity = 0.01

        # Filter by Inertia
        params.filterByInertia = True
        params.minInertiaRatio = 0.01

        # Create a detector with the parameters
        ver = (cv2.__version__).split('.')
        if int(ver[0]) < 3 :
            self.detector = cv2.SimpleBlobDetector(params)
        else : 
            self.detector = cv2.SimpleBlobDetector_create(params)
        
    def compressImage(self): 
        ratio = np.amax(self.image) / 256 
        self.image = (self.image / ratio).astype('uint8')
        
    def detectBlobs(self):
        detector = cv2.SimpleBlobDetector_create()
        keypoints = detector.detect(self.image)
        image_with_keypoints = cv2.drawKeypoints(self.image, keypoints, outImage = np.array([]), color = (255, 0, 0), flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        plt.figure(dpi=300)
        plt.imshow(image_with_keypoints)
        cv2.imwrite("test.jpeg", image_with_keypoints)
        
#         cv2.namedWindow('image', cv2.WINDOW_NORMAL)
#         cv2.resizeWindow('image', 600,600)
#         cv2.imshow("Keypoints", image_with_keypoints)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
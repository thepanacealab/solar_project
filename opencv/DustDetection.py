import cv2 
import time 
import numpy as np
import matplotlib.pyplot as plt 

#THIS CLASS IS OUTDATED, IS NO LONGER USED 

# Author: Michael Tinglof 6/20/19
#     Contrustor takes in a GetFileData object naming it image_obj. Also takes in a track_type
#     give int that corresponds to a tracker type 
    
#     @param: GetFileData object and tracker type as int 

class DustDetection(): 
    def __init__(self, image_obj, track_type): 
        self.image_obj = image_obj 
        self.tracker_types = ["MEDIANFLOW", "KCF", "MOSSE", "CSRT"]
        self.tracker_type = self.tracker_types[track_type]
        self.max_frame = 100
        self.initTracker()
    
#   Helper method to compress images from 16bit to 8bit to use for openCV 
#   params: takes in a 16bit image 
#   returns: 8bit image
    def compressImage(self, image): 
        ratio = np.amax(image)/256
        compressed_image = (image/ratio).astype('uint8')
        return(compressed_image)
    
#   Creates a single tracker 
    def initTracker(self):
        if self.tracker_type == "MEDIANFLOW": 
            self.tracker = cv2.TrackerMedianFlow_create()
        elif self.tracker_type == "KCF": 
            self.tracker = cv2.TrackerKCF_create()
        elif self.tracker_type == "MOSSE": 
            self.tracker = cv2.TrackerMOSSE_create()
        elif self.tracker_type == "CSRT": 
            self.tracker = cv2.TrackerCSRT_create()
        else: 
            print("No tracker was created")
            return 
        
#   Method to define and track a single object
    def defineTrackObj(self): 
        first = self.compressImage(self.image_obj.next())
        bbox = (1478, 2311, 200, 146)
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(first, p1, p2, (255,0,0), 2, 1, 0)
        plt.figure(dpi=150)
        plt.imshow(first)
        self.trackObj()

#     def trackObj(self): 
#         frame = 0 
#         secs = 1
#         while frame < self.max_frame: 
#             ok, frame = self.compressImage(self.image_obj.next())
#             time.sleep(secs)
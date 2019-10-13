import cv2 
import copy 
import math 
import numpy as np
from GetFileData import GetFileData
from ObjectTracker import ObjectTracker 
import matplotlib.pyplot as plt

# Author: Michael Tinglof 6/21/19
#     Robust class that handles the tracking of objects from image to image.
#     Each iteration called with progress the tracker one frame in the sequence 
#     Constructor takes in a GetFileData object 
class TrackImage(): 
    def __init__(self, get_file_data_obj): 
        self.current_frame = 0 
        self.get_file_data_obj = get_file_data_obj 
        self.data_list_size = get_file_data_obj.getDataListSize()
        self.multiTracker = None
        self.sun_present = True 
        self.old_spot_count = 0 
        self.spot_dict = {}
        
    def __iter__(self): 
        return self            
    
    def next(self): 
        if self.multiTracker is None: 
            print("initalize multitracker")
        elif self.current_frame > self.data_list_size-1:
            #venus debug
            print('last frame: ',self.current_frame) 
            raise StopIteration
        else: 
            self.current_frame += 1
            frame = self.get_file_data_obj.next()
            img = self.imgProcess(frame)
            img_copy = copy.deepcopy(img)
            return(self.createPicInfo(img_copy))
        
    def imgProcess(self, frame): 
        ratio = np.amax(frame) / 256 
        frame = (frame / ratio).astype('uint8')
        cv2.imwrite("cv_image.jpeg", frame)
        frame = cv2.imread("cv_image.jpeg", 0)
        return(frame)
        
#   creates a new GetFileData object and will reset all object dictionaries 
#   it was currently tracking 
#   paramas: the new GetFileData object 
    def setNewFileDataObj(self, new_file_data_obj): 
        self.get_file_data_obj = new_file_data_obj 
        self.current_frame = 0 
        self.data_list_size = get_file_data_obj.getDataListSize()
        self.spot_dict = {}
        
#   sets the index of the GetFileData object, which index is used for iterating from 
#   one image in the sequence to the next 
#   paramas: the new starting index 
    def setStartingIndex(self, index): 
        self.get_file_data_obj.current = index
    
#   creates a multitracker object. Creates a new entry in a dictionary for each 
#   object of interest passed. Each object needs a bounding box coordinates 
#   parmas: bboxes is a list of bounding boxes for each object 
#           first_frame is the intial frame for the tracker 
    def createMultiTracker(self, bboxes, first_frame): 
        self.multiTracker = cv2.MultiTracker_create()
        self.spot_dict['stats'] = {
            'num_of_spots' : 0, 
            'avg_distance': 0,
            'distance_diff': 0, 
        }
        for index, bbox in enumerate(bboxes): 
            tracker = cv2.TrackerCSRT_create()
            self.multiTracker.add(tracker, first_frame, bbox)
            self.spot_dict[index] = {
                'id' : index,
                'starting_point' : self.getCentroid(bbox), 
                'last_point' : self.getCentroid(bbox),
                'distance_chng' : 0, 
                'x_change' : [], 
                'y_change' : [], 
                'avg_x_chng' : 0,
                'avg_y_chng' : 0,
                'current_dot' : 0,
                'class' : 0
            }
            
#   helper method to calculate the center of a bounding box 
    def getCentroid(self, bbox): 
        cX = int((bbox[0] + bbox[2]) / 2.0)
        cY = int((bbox[1] + bbox[3]) / 2.0)
        return([cX, cY])

#   helper method to calcuate the distance between two centroids 
    def getDistance(self, c1, c2):
        xdistance = (c2[0] - c1[0])**2
        ydistance = (c2[1] - c1[1])**2
        distance = math.sqrt(xdistance + ydistance)
        return(distance) 

#   helper method to calculate the dot product between two centroids 
    def getDot(self, c1, c2): 
        xpart = c1[0] * c2[0]
        ypart = c1[1] * c2[1]
        dot = xpart + ypart
        return(dot)
    
#   method called for each iteration of the tracker. 
#   the next image in the sequence is passed as a parameter which is then passed to the multitracker
#   the multitracker then updates all information for each object. The class returns a list of bounding 
#   boxes for all object, a copy of the next image, and a diciontary will all informatino about the     
#   objects of interest 
    def createPicInfo(self, img_copy): 
        
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8,8))
        img_copy = clahe.apply(img_copy)
        
        boxes = self.multiTracker.update(img_copy)[1]
        total_distance = 0
        for index, newbox in enumerate(boxes): 
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))

            new_point = self.getCentroid(newbox)
            distance = self.getDistance(self.spot_dict[index]['starting_point'], new_point)
            self.spot_dict[index]['distance_chng'] = distance 
            self.spot_dict[index]['x_change'].append(new_point[0] - self.spot_dict[index]['last_point'][0])
            self.spot_dict[index]['y_change'].append(new_point[1] - self.spot_dict[index]['last_point'][1])
            self.spot_dict[index]['last_point'] = new_point
            self.spot_dict[index]['current_dot'] = self.getDot(self.spot_dict[index]['starting_point'], new_point)
            total_distance += distance 
            self.spot_dict['stats']['num_of_spots'] = index

        new_distance = total_distance/self.spot_dict['stats']['num_of_spots']
        self.spot_dict['stats']['distance_diff'] = (self.spot_dict['stats']['avg_distance'] - new_distance)**2
        self.spot_dict['stats']['avg_distance'] = new_distance 
        self.old_spot_count = self.spot_dict['stats']['num_of_spots'] 

        #cv2.putText(img_copy, str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
        #cv2.putText(img_copy, trackerType + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
        return(boxes, img_copy, self.spot_dict)
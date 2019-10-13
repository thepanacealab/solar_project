from TrackImage import TrackImage 
from GetFileData import GetFileData
from ObjectTracker import ObjectTracker as ot 
import matplotlib.pyplot as plt
import numpy as np
import cv2 
import copy 

#path = "/data/K-0/2017/"
path="/home/large_data/southpole_data/dmlab/solar/south-pole/K-0/2017/1/7/9/"
data_list0 = GetFileData(path, 0)
#print(data_list0)
track_obj = TrackImage(data_list0)
starting_index = 0 

img, starting_place = data_list0.getImageByIndex(starting_index)

bboxes = []
cnts = ot.getContours(img)
print(cnts)
for cnt in cnts: 
    bbox = ot.getBoundingBox(cnt)
    if bbox: 
        bboxes.append(bbox)
print(bboxes)

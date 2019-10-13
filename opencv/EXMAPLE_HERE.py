from TrackImage import TrackImage 
from GetFileData import GetFileData
from ObjectTracker import ObjectTracker as ot 
import matplotlib.pyplot as plt
import numpy as np
import cv2 
import copy 

# this is an exmaple file to show how the work flow may follow using the class files provided 

# to begin, a GetFileData object is created, passing in the path to the image database and the index for 
# the layer of the images to be used 
# next, a trackImage object is created. this will keep track of all objects, and handle the multitracker 
# given a starting index, the intial image will be processed for all countours, bounding boxes will be returned
# tracking object will take the boxes and GetFileData object
# images, bounding boxes, and a spot dictionary will be returned with each iteration
# at the end of the sequence, the average movement of each object will be calcuated then saved in the dictionary 

#path = "/data/K-0/2017/"
path="/home/large_data/southpole_data/dmlab/solar/south-pole/K-0/2017/1/21/10/"
data_list0 = GetFileData(path, 0)
track_obj = TrackImage(data_list0)
starting_index = 0 

img, starting_place = data_list0.getImageByIndex(starting_index)

bboxes = []
cnts = ot.getContours(img)
for cnt in cnts: 
    bbox = ot.getBoundingBox(cnt)
    if bbox: 
        bboxes.append(bbox)

track_obj.setStartingIndex(starting_place)
data_list0.current = starting_place

track_obj.createMultiTracker(bboxes, track_obj.imgProcess(data_list0.next()))
imgs = [] 
box_hold = []

img_cont = True
for x in range(0, 1): 
    boxes, img_copy, spot_dict = track_obj.next() 
    box_hold.append(boxes)
    imgs.append(img_copy)

for index in range(0, len(spot_dict)-1): 
    spot_dict[index]['avg_x_chng'] = np.average(spot_dict[index]['x_change'])
    spot_dict[index]['avg_y_chng'] = np.average(spot_dict[index]['y_change'])

##################################################################################################
##################################################################################################
from KMeans import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np 
import copy 

# this second half of the code handles the k-means clustering
# this first part will seperate objects based on k number of clusters, 
# then will plot the clusters for a more visual repersentation

k = 4

k_obj = KMeans(spot_dict, k)
k_obj.startingCenters()

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

for x in range(0, 20):
    k_obj.assignment()
    k_obj.update()

xs = []
ys = []
zs = []

fig = plt.figure(dpi=300)
#ax = fig.add_subplot(111, projection='3d')
ax = fig.add_subplot(111)

for index in range(0, len(k_obj.spot_dict)-1): 
    spot = k_obj.spot_dict[index]
    xs = spot['avg_x_chng']
    ys = spot['avg_y_chng']
    #zs = spot['distance_chng']
    ax.scatter(xs, ys, c = colors[spot['class']])

#ax.set_xlabel('X Starting Coord')
#ax.set_ylabel('Y Starting Coord')
#ax.set_zlabel('Distance Traveled')
ax.set_xlabel("Avg X Change")
ax.set_ylabel("Avg Y Change")
plt.show()

############################################################################
# the second part of k-means clustering will allow the user to pick a target group and have
# those object bounding boxes highlighted on the image 

target_class = 2
copy_copy = copy.deepcopy(img_copy)
for index in range(0, len(k_obj.spot_dict)-1): 
    newbox = boxes[k_obj.spot_dict[index]['id']]

    p1 = (int(newbox[0]), int(newbox[1]))
    p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))

    spot_class = k_obj.spot_dict[index]['class']

    if spot_class == target_class: 
        cv2.rectangle(copy_copy, p1, p2, (255, 0, 0), 3)
    else: 
        cv2.rectangle(copy_copy, p1, p2, (0, 0, 0), 3)
plt.figure(dpi=300)
plt.imshow(copy_copy, 'gray')
cv2.imwrite("c_image.jpeg", copy_copy)
plt.draw()
'''
###############################################################################
#this third section will take a list of dropped classes and remove them from the dictionary
#the k-means processes should then be iterated again until the desired classes are selected out of the
#group 

spot_dict = {}
drop_class = [2]
new_index = 0 
for index in range(0, len(k_obj.spot_dict)-1): 
    if k_obj.spot_dict[index]['class'] not in drop_class: 
        spot_dict[new_index] = k_obj.spot_dict[index]
        new_index += 1
'''

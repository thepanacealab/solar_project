import numpy as np
import copy

# Author: Michael Tinglof 6/21/19
#     k-means algorithm used for classification of solar objects based on 
#     average movement within in image 
    
# @param: spot_dict returned by trackimage class 
#       k number of groupings 
class KMeans(): 
    def __init__(self, spot_dict, k): 
        self.spot_dict = spot_dict
        self.k = k 
        self.centroids = {}

#   intialize starting centers(will print min and max range for the random starts)
    def startingCenters(self): 
        max_distance = 0 
        avg_x = []
        avg_y = []
        for index in range(0, len(self.spot_dict)-1): 
            if self.spot_dict[index]['distance_chng'] > max_distance: 
                max_distance = self.spot_dict[index]['distance_chng']
            avg_x.append(self.spot_dict[index]['avg_x_chng'])
            avg_y.append(self.spot_dict[index]['avg_y_chng'])

        max_x_avg = np.max(avg_x)
        min_x_avg = np.min(avg_x)
        max_y_avg = np.max(avg_y)
        min_y_avg = np.min(avg_y)
        
        print([min_x_avg, max_x_avg])
        print([min_y_avg, max_y_avg])
        for i in range(0, self.k): 
            self.centroids[i] = {
                'location' : [np.random.uniform(min_x_avg, max_x_avg+.01, 1), np.random.uniform(min_y_avg, max_y_avg, 1)], 
                'total_x' : 0,
                'total_y' : 0,
                'count' : 0,
            }

#   will assign each object means center baseed on minimum distance to center 
    def assignment(self): 
        for index in range(0, len(self.spot_dict)-1): 
            spot = self.spot_dict[index]
            x_chng = self.spot_dict[index]['avg_x_chng']
            y_chng = self.spot_dict[index]['avg_y_chng']
            min_distance = 9999999999999
            for i in range(0, self.k): 
                distance = np.sqrt(((self.centroids[i]['location'][0] - x_chng) ** 2) + 
                    ((self.centroids[i]['location'][1] - y_chng) ** 2)) 
                if distance < min_distance: 
                    min_distance = distance
                    spot['class'] = i
                    best_fit = i
            self.centroids[best_fit]['total_x'] += x_chng
            self.centroids[best_fit]['total_y'] += y_chng
            self.centroids[best_fit]['count'] += 1

#   updates the centroids based on the average mean of their cluster 
    def update(self): 
        for i in range(0, self.k): 
            try: 
                avg_x = self.centroids[i]['total_x']/self.centroids[i]['count']
            except ZeroDivisionError:
                avg_x = self.centroids[i]['location'][0]
            try:
                avg_y = self.centroids[i]['total_y']/self.centroids[i]['count']
            except ZeroDivisionError: 
                avg_y = self.centroids[i]['location'][1]
            self.centroids[i]['location'] = [avg_x, avg_y]
            print("{}: {}".format(i, self.centroids[i]['count']))

            self.centroids[i]['total_x'] = 0
            self.centroids[i]['total_y'] = 0
            self.centroids[i]['count'] = 0 
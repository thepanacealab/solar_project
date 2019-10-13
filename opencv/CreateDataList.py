import os
import fnmatch
import numpy as np

from operator import itemgetter

from astropy.io import fits

# Author: Michael Tinglof 6/20/19
#     Constructor takes in a path to the head of a dictionary you want to iterate through. Collects all files and creates a
#     dictionary of their path, time and date (both time and date are broken down into respective parts). A list is then returned
#     with all these dictionaries sorted by time. 
    
#     @param takes in path that you want to begin iteration at
class CreateDataList(): 
    def __init__(self, head_path):
        self.head_path = head_path
        self.data_list = []
        
#     Gets list of dictionary items from passed head path 
#     @param 
#     @returns sorted list of dictionary items 
    def getList(self): 
        for path in os.walk(self.head_path):
            if path[2]: 
                current_path = path[0]
                for data in path[2]: 
                    date_time = self.getDateTime(data)
                    path_to_file = "{}/{}".format(current_path, data)
                    data_dictionary = {
                        "path" : path_to_file, 
                        "year" : date_time["year"], 
                        "month" : date_time["month"], 
                        "day" : date_time["day"], 
                        "hour" : date_time["hour"], 
                        "minute" : date_time["minute"], 
                        "seconds" : date_time["seconds"]
                    }
                    self.data_list.append(data_dictionary)
        return(sorted(self.data_list, key=itemgetter('year', 'month', 'day', 'hour', 'minute', 'seconds')))
                    
#     Helper method that breaks apart dates into years, months, and days then breaks time into hours, minutes, 
#     and seconds. Casts strings to ints 
#     @param string of file name, usually containing its date and time of creation 
#     @returns dictionary of broken down date and time of files 
    def getDateTime(self, data_string): 
        trash, date, time = data_string.split("T")
        date = date.split(".")[-1]
        year, month, day = date.split("-")
        time = time.split("_")[0]
        hour, minute, seconds = time.split(":")
        return{"year" : int(year), "month" : int(month), "day" : int(day),
              "hour" : int(hour), "minute" : int(minute), "seconds" : int(seconds)}
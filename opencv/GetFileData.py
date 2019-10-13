import os
import fnmatch
import numpy as np

from astropy.io import fits

from CreateDataList import CreateDataList
from GetFile import GetFile 

# Author: Michael Tinglof 6/21/19
#     This class takes in a path to a directory that contains files or subdictories that contains files.
#     Once the file processing has been done, a dictory is returned containing file date, time and path 
#     info. This class handles returning image data either by index or by a iteration. 
    
# @param path: the starting place for iteration for files 
#         layer: image layer for image data to be returned on 
class GetFileData():
    def __init__(self, path, layer): 
        self.head_path = path 
        self.layer = layer
        self.data_list = CreateDataList(self.head_path).getList()
        self.data_list_size = len(self.data_list)
        self.current = 0 
        self.skip_files = 'skip_files.txt'
        self.skip_files_list = []
        self.readSkipFiles()
    
    def __iter__(self): 
        return self
    
    def next(self): 
        if self.current > self.data_list_size-1: 
            raise StopIteration
        else: 
            self.current += 1
            self.current = self.findNextIndex(self.current)
            return(self.getImageArray(self.current-1))
        
#     @param index of image data to be returned 
#     @return numpy array of image data 
    def getImageArray(self, index):  
        file_dictionary = self.data_list[index]
        file_image_data = GetFile(file_dictionary["path"]).getFile()[1][self.layer]
        return(np.asarray(file_image_data))
    
#   helper method that checks a new file path with the skip files 
#   path list. If the file is on the list, the path is skipped and 
#   the next path is checked. 
#
#   params: the supposed index of the image
#   returns: image at index after file paths have been skipped 
    def findNextIndex(self, index): 
        path = self.data_list[index-1]['path']
        while path in self.skip_files_list: 
            index += 1
            path = self.data_list[index-1]['path']
        return(index)
    
#   returns image at a given index, checks against skipped files 
#   using findNextIndex
#
#   params: index of chosen image file 
#   returns: image after skipped files 
    def getImageByIndex(self, index): 
        current_place = 0 
        for x in range(0, index): 
            current_place = self.findNextIndex(current_place)
            current_place += 1
        return(self.getImageArray(current_place-1), current_place-1)
    
#   returns size of the image data list object 
    def getDataListSize(self): 
        return(self.data_list_size)
    
#   returns current layer of the image object 
    def getLayer(self): 
        return(self.layer)
    
#   set layer of image object, will need to instanitate new 
#   image file object 
    def setLayer(self, layer): 
        self.layer = layer
        
#   reads in skip file paths text file 
    def readSkipFiles(self): 
        with open(self.skip_files, "r") as infile: 
            for line in infile: 
                self.skip_files_list.append(line[:-1])
        print("skipping {} imgs".format(len(self.skip_files_list)))
        
#   adds a path to skip paths file based on current index of self 
    def deletePath(self): 
        with open(self.skip_files, "a+") as infile: 
            infile.write(self.data_list[self.current-1]['path'] + "\n")

#   returns date of given index 
    def getFileDate(self, index): 
        updated_index = self.getImageByIndex(index)[1]
        year = self.data_list[updated_index]["year"]
        month = self.data_list[updated_index]["month"]
        day = self.data_list[updated_index]["day"]
        return([year, month, day])
        
#   returns time of given index 
    def getFileTime(self, index): 
        updated_index = self.getImageByIndex(index)[1]
        hour = self.data_list[updated_index]["hour"]
        minute = self.data_list[updated_index]["minute"]
        seconds = self.data_list[updated_index]["seconds"]
        return([hour, minute, seconds])

#   set  current index of self 
    def setCurrentIndex(self, index): 
        self.current = index
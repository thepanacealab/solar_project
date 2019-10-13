import matplotlib.pyplot as plt
import numpy as np

# Author: Michael Tinglof 6/24/19
#     A simple class that takes in a image array and prints a matplot image.
#     This class also converts from 16bit images to u8bit images 
# @param image array for printing 
class PrintImage(): 
    def __init__(self, image): 
        self.image_data = image 
        self.printImage()
    
    def printImage(self): 
        ratio = np.amax(self.image_data) / 256 
        img8 = (self.image_data / ratio).astype('uint8')
        
        plt.figure(dpi=150)
        plt.imshow(img8, cmap = 'gray')
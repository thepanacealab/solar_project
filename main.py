from detection import dustDetection
import cv2 
import numpy as np 
import matplotlib.pyplot as plt

path='/home/large_data/southpole_data/dmlab/solar/south-pole/K-0/2017/1/7/9/'
path1= '/home/large_data/venus_work/fits_code/'
out_folder='/home/large_data/venus_work/fits_code/image_files'
folder1=dustDetection(path, path1)
folder1.extract_fits()
#folder1.png_images(out_folder)
folder1.brighten_images(1)
folder1.noise_remove_folder(1)
#folder1.edge_detect_binary(path, 1)
#a=folder1.average_dark(1)

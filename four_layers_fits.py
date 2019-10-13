# this program creates a plot of four layers of fits images in gray scale

import os
import numpy as np
import cv2
import glob
import astropy.io
from astropy.visualization import astropy_mpl_style
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
import subprocess
import ffmpeg
import sys
import copy


img_array = []
vid_array = []
vid_array1 = []
vid_array2 = []
vid_array3 = []
vid_name = 'video_2017_un.mp4'
dir_path = '/home/large_data/venus_work/all_layer_color/'
path = '/home/large_data/southpole_data/dmlab/solar/south-pole/K-0/2017/1/22/'
path_K2017='/home/large_data/southpole_data/dmlab/solar/south-pole/K-0/2017/1/7/9/'

image_folder = dir_path

os.chdir(path_K2017)
print('Extracting all fits image details from:\n', path)
print('Extracting...')
for r,d,f in os.walk(path_K2017):
	for file in f:
		if '.fits' in file:
			img_array.append(os.path.join(r,file))

#print(len(img_array))

print('Extraction finished!')

plt.style.use(astropy_mpl_style)

print('Adding images addresses to an array...')
for i, item in enumerate(img_array):
  image_file = get_pkg_data_filename(item)
  image_data = fits.getdata(image_file, ext=0)
  image_transposed = np.transpose(np.asarray(image_data))
  height, width, layers = image_transposed.shape
  #print(i,': Image is ',item)  
  vid_array.append(image_transposed[:, :, 0])
  vid_array1.append(image_transposed[:, :, 1])
  vid_array2.append(image_transposed[:, :, 2])
  vid_array3.append(image_transposed[:, :, 3])
print('Finished adding image addresses!')

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
   
def generate_video(imp,imp1,imp2,imp3, vid_name):
    print('Saving images to make video...')
    for j in range(len(imp)):
        progress(j,len(imp),'Generating files')
        plt.figure(dpi=1200)
        fig, axeslist = plt.subplots(2,2)
        plt.axis('off')
        plt.grid(b=None)
        axeslist.ravel()[0].imshow(imp[j], cmap = 'gray')
        axeslist.ravel()[0].set_axis_off()
        axeslist.ravel()[1].imshow(imp1[j], cmap='gray')
        axeslist.ravel()[1].set_axis_off()
        axeslist.ravel()[2].imshow(imp2[j], cmap='gray')
        axeslist.ravel()[2].set_axis_off()
        axeslist.ravel()[3].imshow(imp3[j], cmap='gray')
        axeslist.ravel()[3].set_axis_off()
        plt.matplotlib.pyplot.subplots_adjust(wspace=-0.3,hspace=0.1)
        plt.savefig(image_folder + "/file_%03d.png" % j, dpi = 1200, pad_inches = 0 , bbox_inches='tight')
        plt.close()

os.chdir(image_folder)
generate_video(vid_array, vid_array1, vid_array2, vid_array3, vid_name)


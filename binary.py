# a program where the binary images are stitched together to produce a video

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import PIL


path='/home/large_data/venus_work/binary_images/'
img_bin=[]
img_arr=[]
image_folder='/home/large_data/venus_work/image_bin/'
video_name = image_folder+'binary.avi'
#image_folder = dir_path
video_FourCC = cv2.VideoWriter_fourcc(*'MPEG')
os.chdir(image_folder)
for r,d,f in os.walk(path):
	for file in f:
		if '.jpeg' in file:
			img_bin.append(os.path.join(r,file))
for i in range(len(img_bin)):
  im=Image.open(img_bin[i])
  outfile = os.path.join(image_folder, "file_%04d.jpeg" % i)
  im = im.convert("RGB")
  out = im.resize((1920,1440),Image.ANTIALIAS)
  out.save(outfile, "JPEG", quality=95)
#plt.figure(dpi=300)
#plt.axis('off')
#plt.grid(b=None)
#plt.imshow(img_arr[0], cmap='gray')
#plt.show() 

images = [img for img in os.listdir(image_folder) if img.endswith(".jpeg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape
    
    
print(frame.shape)
    
video = cv2.VideoWriter(video_name, video_FourCC, 30, (width, height))
    
for image in sorted(images):
  for j in range(10):
    #print("Writing the image : ", image)
    video.write(cv2.imread(os.path.join(image_folder, image)))
    
cv2.destroyAllWindows()
video.release()
print('video finished and saved!!')
        
#plt.figure(dpi=600)
#plt.imshow(copy_copy, 'gray')
#cv2.imwrite("cv_image00"+str(z)+".jpeg",copy_copy)
#plt.draw()
#plt.close()


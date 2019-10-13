#program where first binary image in the folder is subtracted from the rest of the binary images, which gives the differnce of the image matrices. ( the binary images are produced from myexample.py in opencv folder)
# the sum of the image differnce is calculated.

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import PIL

path='/home/large_data/venus_work/binary_images/'
img_bin=[]
img_arr=[]
image_folder='/home/large_data/venus_work/image_diff/'
video_name = image_folder+'binary_video.avi'
#image_folder = dir_path
video_FourCC = cv2.VideoWriter_fourcc(*'MPEG')
os.chdir(image_folder)
for r,d,f in os.walk(path):
	for file in f:
		if '.jpeg' in file:
			img_bin.append(os.path.join(r,file))
print('img_bin created')
temp_arr = cv2.imread(img_bin[0],0)
r,c=temp_arr.shape
A = np.zeros([len(img_bin)-1,1])
for i in range(0,len(img_bin)-1):
  f1=cv2.imread(img_bin[0])
  f2=cv2.imread(img_bin[i+1])
  #img_arr.append(np.absolute(f2-f1))
  A[i] = np.sum(np.absolute(f2-f1))
  #im=Image.fromarray(img_arr[i-1],'RGB')
  #outfile = os.path.join(image_folder, "file_%04d.jpeg" % i)
  #im = im.convert("RGB")
  #out = im.resize((1920,1440),Image.ANTIALIAS)
  #out.save(outfile, "JPEG", quality=95)
  print('sum for ',i, ' = ',A[i])
#print(np.sum(A))
plt.figure(dpi=1200)
#plt.axis('off')
plt.grid(b=None)
plt.plot(A)
#plt.imshow(img_arr[0], cmap='gray')
plt.show() 

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

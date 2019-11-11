import os
from PIL import Image
from scipy.ndimage import gaussian_filter
import astropy.io
from astropy.visualization import astropy_mpl_style
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
import numpy as np
import cv2
import matplotlib.image as mpimg


class dustDetection:

  def __init__(self, path_arr):
    self.path = path_arr
    self.img_path_arr = []
    self.img_data = dict()
    self.brightened = dict()
    self.noise_removed_array=dict()
    
  def extract_fits(self):
    #print('Extracting all fits image details from:\n', self.path)
    print('Extracting all fits image details...')    
    self.img_path_arr = os.listdir(self.path)
    for i,item in enumerate(self.img_path_arr):
      hdul = fits.open(self.path+item)
      data = hdul[0].data
      image_flipped = np.flip(data,1)    
      self.img_data[self.img_path_arr[i]] = image_flipped[0, :, :]    
    print('Number of images in path:', len(self.img_data))  
    print('Done!')
    
  def brighten(self, img_name, change, visible):
    im1 = Image.fromarray(img_name)
    im2 = im1.point(lambda p: p * change)
    if visible:
      plt.figure(dpi=1200)
      plt.axis('off')
      plt.grid(b=None)
      plt.imshow(im2, cmap='gray')
      plt.show()    
    return np.asarray(im2)
    
  def noise_removal(self,item, visible):
    f = np.fft.fft2(item)
    fshift=np.fft.fftshift(f)
    
    #calculate amplitude spectrum
    mag_spec = 20*np.log(np.abs(fshift))    
    r= f.shape[0]/2     # number of rows/2
    c=f.shape[1]/2      # number of columns/2
    p=3
    n=1 
    fshift2 = np.copy(fshift)    
    # suppress upper part 
    fshift2[int(r-p):int(r+p),0:int(c-n)] = 0.001
    # suppress lower part 
    fshift2[int(r-p):int(r+p), int(c+n):int(c+c)] = 0.001
    # calculate new amplitude spectrum
    mag_spec2 = 20*np.log(np.abs(fshift2))
    inv_fshift=np.fft.ifftshift(fshift2)
    # reconstructing image
    img_recon= np.real(np.fft.ifft2(inv_fshift))
    if visible:
      plt.figure(dpi=1200)
      plt.axis('off')
      plt.grid(b=None)
      plt.imshow(img_recon, cmap='gray')
      plt.show()
    return img_recon  
    
  def brighten_images(self, change = 5.0, visible=0):
    print('Smoothening/Brightening the images...')
    for key, value in self.img_data.items():
      self.brightened[key] = self.brighten(value, change, visible)
    print('Done!')
    
  def noise_remove_folder(self, visible=0):
    print('Removing noise from the images...')
    for key, value in self.brightened.items():
      self.noise_removed_array[key] = self.noise_removal(value, visible)
    print('Done!')
    
  def edge_detect(self, image, visible):
    t = 100
    img = np.uint8(image)
    gray = cv2.cvtColor(src = img, code = cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(src = gray, ksize = (5, 5), sigmaX = 0)
    (t, binary) = cv2.threshold(src = blur,thresh = t, maxval = 255, type = cv2.THRESH_BINARY)
    (_, contours, _) = cv2.findContours(image = binary, mode = cv2.RETR_EXTERNAL,method = cv2.CHAIN_APPROX_SIMPLE)
    print("Found %d objects." % len(contours))
    for (i, c) in enumerate(contours):
      print("\tSize of contour %d: %d" % (i, len(c)))
#   format = np.uint8(image)
#   edge_img = cv2.Canny(format,np.max(format)-100,np.max(format))
    if visible:
      plt.figure(dpi=1200)
      plt.axis('off')
      plt.grid(b=None)
      plt.imshow(edge_img, cmap='gray')
      plt.show()
    return edge_img
    
  def edge_folder(self, path, visible):
    list_all = os.listdir(path)
    for i, img in enumerate(list_all):
      image = Image.open(path+img).convert('L')
      #image = mpimg.imread(path+img)
      #gray = self.rgb2gray(image)
      #image_orig = cv2.imread(img);
      #image = cv2.cvtColor(image_orig, cv2.COLOR_BGR2GRAY)
      #image = self.rgb2gray(image_orig)
      if i == 0:
        self.edge_detect_biary(image, 6, 4, visible) #best=6,4
      else:
        continue
      '''cnt = 0
      for key, value in self.noise_removed_array.items():
        if cnt == 0:
          self.edge_detect_biary(value, 10, 3, visible)
          cnt += 1
        else:
          continue
      '''
  def edge_detect_biary(self, image1, pixel_kernel, pixel_kernel_small, visible):
    #img = np.uint8(image)
    image2 = np.asarray(image1)
    #filter_size = 2*np.ceil(2*4)+1
    image = gaussian_filter(image2,sigma=6, truncate=2) #sigma=6 also 4
    print('shape of image is ', image.shape)    
    m,n = image.shape
    image_mod = np.zeros(shape=[m,n])
    for i in range(pixel_kernel,m-pixel_kernel+1):
      for j in range(pixel_kernel,n-pixel_kernel+1):
        mat_1 = image[i-pixel_kernel:i+pixel_kernel,j-pixel_kernel:j+pixel_kernel]
        count = len(mat_1[mat_1 > image[i,j]])
        if (count >= (0.9 * 1.5 * pixel_kernel * pixel_kernel)):
          image_mod[i][j] = 0
        else:
          image_mod[i][j] = 255
    print('max is ', np.max(image_mod))
    print('min is ', np.min(image_mod))
    if visible:
      plt.figure(1)
      plt.axis('off')
      plt.grid(b=None)
      plt.imshow(np.uint8(image_mod), cmap='gray')
      plt.title('Modified_0')
      plt.show()
    
    image_mod_1 = image_mod
    print('initial min of image_mod_1 is ',np.min(image_mod_1))
    print(image_mod_1.dtype)
    count = 0
    for i in range(pixel_kernel_small, m-pixel_kernel_small+1):
      for j in range(pixel_kernel_small, n-pixel_kernel_small+1):
        if image_mod[i][j] == 0:
          mat_2 = image_mod[i-pixel_kernel_small:i+pixel_kernel_small, j-pixel_kernel_small:j+pixel_kernel_small]
          count1 = len(mat_2[mat_2 < 255])
          if count1 >= 25: 
            count += 1
            image_mod_1[i-1:i+1, j-1:j+1] = 0            
          else:
            image_mod_1[i-1:i+1, j-1:j+1] = 255           
    if visible:
      plt.figure(2)
      plt.axis('off')
      plt.grid(b=None)
      plt.imshow(np.uint8(image_mod_1), cmap='gray')
      plt.title('Modified_1')
      plt.show()

#  def rgb2gray(self, rgb):
#    return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])
    
  def average_dark(self,visible=0):
    m,n=self.img_data[self.img_path_arr[0]].shape
    avg_img=np.zeros((m,n))
    for i in range(len(self.img_data)):
#      if i < 4:
      avg_img+=self.img_data[self.img_path_arr[i]]
      print('number of iteration', i)
    avg_img=avg_img/len(self.img_data)
    #avg_img=avg_img/4
    diff = self.img_data[self.img_path_arr[0]] - avg_img
    if visible:
      plt.figure()
      plt.axis('off')
      plt.grid(b=None)
      plt.imshow(np.uint16(diff), cmap='gray')
      plt.title('Difference image')
      plt.show()
      
      plt.figure()
      plt.axis('off')
      plt.grid(b=None)
      plt.imshow(np.uint16(avg_img), cmap='gray')
      plt.title('average')
      plt.show()
    return avg_img
      
      
      
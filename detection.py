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
#import cv
import matplotlib.image as mpimg


class dustDetection:

  def __init__(self, path_arr, dest_path):
    self.path = path_arr
    self.dest_path= dest_path
    self.img_path_arr = []
    self.img_data = dict()
    self.brightened = dict()
    self.noise_removed_array=dict()
    
  def extract_fits(self):
    #print('Extracting all fits image details from:\n', self.path)
    print('Extracting all fits image details...')    
    self.img_path_arr = sorted(os.listdir(self.path))
    for i,item in enumerate(self.img_path_arr):
      #print(item)
      hdul = fits.open(self.path+item)
      data = hdul[0].data
      image_flipped = np.flip(data,1)    
      self.img_data[self.img_path_arr[i]] = image_flipped[0, :, :]         
    print('Number of images in path:', len(self.img_data))  
    print('Done!')
    return self.img_data
    
  def brighten(self, img_name, visible=0):
    im1 = np.uint16(img_name) 
    plt.figure(dpi=1200)
    plt.axis('off')
    plt.grid(b=None)
    plt.imshow(im1, cmap='gray')
    plt.savefig('/home/large_data/venus_work/fits_code/im.png', dpi = 1200, pad_inches = 0, bbox_inches='tight')
    plt.close()
    im2 = cv2.imread('/home/large_data/venus_work/fits_code/im.png',0)
    #im3= im2/np.linalg.norm(im2)
    equ=cv2.equalizeHist(im2)
    cv2.imwrite('res_one.png',equ)        
    '''    
    mean_bright = np.mean(np.asarray(im1))
    #bright_val= 21000/mean_bright
    print ('mean of original image: ', mean_bright)
    max_bright = np.max(np.asarray(im1))
    min_bright = np.min(np.asarray(im1))
    print(max_bright)
    print(min_bright)
    #im2 = im1.point(lambda p: p * bright_val)
    #mean_bright = np.mean(np.asarray(im2))
    #print ('mean after brightening:', mean_bright)
    #print ('Brightness increased by factor of: ', bright_val)
    '''
    if visible:
      plt.figure(dpi=1200)
      plt.axis('off')
      plt.grid(b=None)
      plt.imshow(equ, cmap='gray')
      plt.show()    
    return np.asarray(equ)
    
  def noise_removal(self,item, visible=0, cnt=0):
    f = np.fft.fft2(item)
    fshift=np.fft.fftshift(f)
    
    #calculate amplitude spectrum
    #mag_spec = 20*np.log(np.abs(fshift))    
    r= f.shape[0]/2     # number of rows/2
    c=f.shape[1]/2      # number of columns/2
    p=1
    n=2
    fshift2 = np.copy(fshift)    
    # suppress upper part 
    fshift2[int(r-p):int(r+p),0:int(c-n)] = 0.001
    # suppress lower part 
    fshift2[int(r-p):int(r+p), int(c+n):int(c+c)] = 0.001
    # calculate new amplitude spectrum
    #mag_spec2 = 20*np.log(np.abs(fshift2))
    inv_fshift=np.fft.ifftshift(fshift2)
    # reconstructing image
    img_recon= np.real(np.fft.ifft2(inv_fshift))
    plt.figure(dpi=1200)
    plt.axis('off')
    plt.grid(b=None)
    plt.imshow(img_recon, cmap='gray')
    plt.savefig(self.dest_path + "/file.png", dpi = 1200, pad_inches = 0, bbox_inches='tight')
    plt.close()
    if visible:
      plt.figure(dpi=1200)
      plt.axis('off')
      plt.grid(b=None)
      plt.imshow(img_recon, cmap='gray')
      plt.show()
    img_idx = self.dest_path+'file.png'
    count_noise=self.edge_detect_binary(img_idx)
    os.remove(img_idx)
    return img_recon,count_noise
    
  def brighten_images(self, visible=0):
    print('Smoothening/Brightening the images...')
    count=1
    for key, value in self.img_data.items():
      if count == 1:
        self.brightened[key] = self.brighten(value, visible)
        count+=1
      else:
        break
      print('Done!')
    
  def noise_remove_folder(self, visible=0):
    print('Removing noise from the images...')
    cnt = 1
    tot = len(self.brightened)
    for key, value in self.brightened.items():    
      print('Current image: ', cnt, ' /', tot)
      self.noise_removed_array[key] = self.noise_removal(value, visible, cnt)
      cnt += 1
    print('Done!')
       
  def edge_detect_binary(self, image1, visible=0, ii=0):
    print('Started creating contours..')
    img1 = cv2.imread(image1, 0)
    m,n = img1.shape
    img = cv2.adaptiveThreshold(img1,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,201,3)
    img = cv2.erode(img, None, iterations=2)
    img = cv2.dilate(img, None, iterations=12)
    cnts = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    img_canny = cv2.Canny(img,np.max(img)-100,np.max(img))
    img_rgb = cv2.cvtColor(img1, cv2.COLOR_GRAY2RGB)
    #print('rgb shape:', img_rgb.shape)
    print('Filling red borders...')
    for i in range(m):
      for j in range(n):
        if img_canny[i,j] == 255:
          img_rgb[i,j,0] = 0
          img_rgb[i,j,1] = 0
          img_rgb[i,j,2] = 255      
    print('Loop done!')
    visible = 1 
    if visible:
      plt.figure(dpi=1200)
      plt.axis('off')
      plt.grid(b=None)
      plt.imshow(np.uint8(img_rgb))
      plt.show()
      cv2.imwrite(self.dest_path+"edges/" + "colour_%03d.png" % ii, img_rgb)
      plt.draw()
      plt.close()
    if visible:
      plt.figure(dpi=1200)
      plt.axis('off')
      plt.grid(b=None)
      plt.imshow(np.uint8(img), cmap='gray')
      plt.show()
      cv2.imwrite(self.dest_path+"binary/"+"binarry_%03d.png" % ii, img)
      plt.draw()
      plt.close()
    return len(cnts)
    
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

    
    
      
      
      
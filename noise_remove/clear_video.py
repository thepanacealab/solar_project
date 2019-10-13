#this program brightens the images from the path folder and then ustilises fourier transform to eliminate dark stripes from the images
#then, it converts the image to jpeg and creates a video

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
import PIL
from PIL import Image


#path_arr=['/home/large_data/venus_work/temp_fits/']
path_arr=['/home/large_data/southpole_data/dmlab/solar/south-pole/K-0/2017/1/21/11/']
#for ii in range(len(path_arr)):
for ii in range(len(path_arr)):
    path_K2017 = path_arr[ii]
    img_path_arr = []
    image_array = []   
    dir_path = '/home/large_data/venus_work/temp1/'
    image_folder = '/home/large_data/venus_work/temp1/'
    final_image_folder = '/home/large_data/venus_work/image1/'
    video_name = '/home/large_data/venus_work/image1/video_bin_'+str(ii)+'.avi'
    video_FourCC = cv2.VideoWriter_fourcc(*'MPEG')
    os.chdir(path_K2017)

    print('Extracting all fits image details from:\n', path_K2017)
    print('Extracting...')
#adding image addresses to path
    for r,d,f in os.walk(path_K2017):
    	for file in f:
    		if '.fits' in file:
    			img_path_arr.append(os.path.join(r,file))
    print(len(img_path_arr))
    print('Extraction finished!')
    
    plt.style.use(astropy_mpl_style)
    
    print('Adding images addresses to an array...')
    for i, item in enumerate(img_path_arr):
      image_file = get_pkg_data_filename(item)
      image_data = fits.getdata(image_file, ext=0)
      #image_transposed = np.transpose(np.asarray(image_data))
      image_transposed = np.flip(image_data,1)
      #height, width, layers = image_transposed.shape 
      image_array.append(image_transposed[0, :, :])
      print(image_transposed.shape)
#      height, width, layers = image_data.shape 
#      image_array.append(image_data[:, :, 0])
    print('All images extracted')
    
    def progress(count, total, status=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))
        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)
        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
        sys.stdout.flush()
#generating lossless images        
    def generate_image(imp, img_path):
        print('Saving images to image_folder...')
        for j in range(len(imp)):
            progress(j,len(imp),'Generating files')
            plt.figure(dpi=1200)
            plt.axis('off')
            plt.grid(b=None)
            plt.imshow(imp[j], cmap='gray')
            plt.savefig(img_path + "/file_%03d.png" % j, dpi = 1200, pad_inches = 0 , bbox_inches='tight')
            plt.close()        

    generate_image(image_array, image_folder)
  
    img_png_path=[]
    print('Extracting all png image paths ', image_folder)
    print('Extracting...')
    for r,d,f in os.walk(image_folder):
    	for file in f:
    		if '.png' in file:
    			img_png_path.append(os.path.join(r,file))
    print('number of png images in folder', len(img_png_path))
    print('Extraction finished!')

  #------------------------------------------------------------------------------------------------
#brightening of the image
    for j in range(len(img_png_path)):
      dark = Image.open(img_png_path[j])
  
  # multiply each pixel by 0.9 (makes the image darker), darker < 1.0 < lighter
      brightened = dark.point(lambda p: p * 3.0)
      plt.figure(dpi=1200)
      plt.axis('off')
      plt.grid(b=None)
      plt.imshow(brightened, cmap='gray')
      plt.savefig(final_image_folder + 'temp_img.png', dpi = 1200, pad_inches = 0, bbox_inches='tight')
      plt.close()
      #smoothened.save(final_image_folder+'temp_img.tiff',pad_inches = 0, bbox_inches='tight')

  #im2.show()
  
  #----------------------------------------------------------------------------------------------
#removing dark stripes
      img_noise=cv2.imread(final_image_folder+'temp_img.png',0)
    #img = cv2.imread('21_1_17_8_59a.tiff',0)
      f=np.fft.fft2(img_noise)
      fshift=np.fft.fftshift(f)
    #calculate amplitude spectrum
      mag_spec = 20*np.log(np.abs(fshift))
    
      r= f.shape[0]/2     # number of rows/2
      c=f.shape[1]/2      # number of columns/2
      p=3
      n=1 
      fshift2 = np.copy(fshift)
    
    # suppress upper part 
      #fshift2[0:int(r-n),int(c-p):int(c+p)] = 0.001
      fshift2[int(r-p):int(r+p),0:int(c-n)] = 0.001
      # suppress lower part 
      #fshift2[int(r+n):int(r+r),int(c-p):int(c+p)] = 0.001
      fshift2[int(r-p):int(r+p), int(c+n):int(c+c)] = 0.001
      # calculate new amplitude spectrum
      mag_spec2 = 20*np.log(np.abs(fshift2))
      inv_fshift=np.fft.ifftshift(fshift2)
    # reconstructing image
      img_recon= np.real(np.fft.ifft2(inv_fshift))
    
      plt.figure(dpi=1200)
      plt.axis('off')
      plt.grid(b=None)
      plt.imshow(img_recon, cmap='gray')
      plt.savefig(final_image_folder + "/file_%03d.png" % j, dpi = 1200, pad_inches = 0, bbox_inches='tight')
      plt.close()
      os.remove(final_image_folder+'temp_img.png') 
      #plt.show()
    
  #-----------------------------------------------------------------------------------------------
#converting to jpeg for video creation  
      
    tiff_for_video = [img for img in os.listdir(final_image_folder) if img.endswith(".png")]
    print(os.path.join(final_image_folder,tiff_for_video[0]))
    [r,c]=(cv2.imread(os.path.join(final_image_folder, tiff_for_video[0]),0)).shape
    for infile in tiff_for_video:
      outfile = os.path.join(final_image_folder, infile[:-4] + "jpeg")
      im = Image.open(os.path.join(final_image_folder,infile))
      #print('image size in final_image_folder', im.size)
      print ("new filename : " + outfile)
      im = im.convert("RGB")
      out = im.resize((r,c),Image.ANTIALIAS)
      out.save(outfile, "JPEG", quality=95)
    

#    print('Deleting *.png files in ', final_image_folder,'...')
#    for file_name in glob.glob("*.png"):
#      os.remove(file_name)
#    print('Deleted .png files in ', final_image_folder)  
    #jpeg_for_video=[]
    jpeg_for_video = [img for img in os.listdir(final_image_folder) if img.endswith(".jpeg")]
    frame = cv2.imread(os.path.join(final_image_folder, jpeg_for_video[0]))
    height, width, layers = frame.shape
    print('frame size', frame.shape)
    print(sorted(jpeg_for_video))
    
    video = cv2.VideoWriter(video_name, video_FourCC, 30, (width, height))
    for image in sorted(jpeg_for_video):
      for jj in range(10):
        print("Writing the image : ", image)

        video.write(cv2.imread(os.path.join(final_image_folder, image)))
    
    cv2.destroyAllWindows()
    video.release()
    
    
    os.chdir(image_folder)
    #    print('Deleting *.png files in ', image_folder,'...')
    #    for file_name in glob.glob("*.png"):
    #      os.remove(file_name)
    #    print('Deleted png files in ', image_folder)
        
    #    os.chdir(final_image_folder)
    #    
    #    print('Deleting *.png files in ', final_image_folder,'...')
    #    for file_name in glob.glob("*.png"):
    #      os.remove(file_name)
    #    print('Deleted .png files in ', final_image_folder)
    #    
    #    print('Deleting *.jpeg files in ', final_image_folder)
    #    for file_name in glob.glob("*.jpeg"):
    #      os.remove(file_name)
    #    print('Deleted .jpeg files in ', final_image_folder)
        
    print('Session completed!!!\nPlease view video in ', final_image_folder)

  
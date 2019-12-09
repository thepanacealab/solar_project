from detection import dustDetection 
import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image

path='/home/large_data/southpole_data/dmlab/solar/south-pole/K-0/2017/1/7/9/'
path1='/home/large_data/venus_work/fits_code/'
folder1=dustDetection(path, path1)
raw_dict=folder1.extract_fits()
length= len(raw_dict)
counter=0

with open('tables_1.txt' ,'w') as out_file:
  out_file.write('image_name,number of contours,number of brightened  contours, number of contours after noiseRemoval\n')
  for key,value in raw_dict.items():
    print (key)
    counter+=1
    print('the number of image: ', counter, ' out of ', length)
    plt.figure(dpi=1200)
    plt.axis('off')
    plt.grid(b=None)
    plt.imshow(value, cmap='gray')
    plt.savefig(path1 + "/file_raw.png", dpi = 1200, pad_inches = 0, bbox_inches='tight')
    plt.close()
    #plt.show()
    #img=Image.fromarray(np.uint16(value))
    img=path1 + '/file_raw.png'
    count_raw=folder1.edge_detect_binary(img)
    print('raw done:', count_raw)
    
    img_bright=folder1.brighten(value)
    plt.figure(dpi=1200)
    plt.axis('off')
    plt.grid(b=None)
    plt.imshow(img_bright, cmap='gray')
    plt.savefig(path1 + "/file_bright.png", dpi = 1200, pad_inches = 0, bbox_inches='tight')
    plt.close()
    
    
    img_bright1=path1 + '/file_bright.png'
    count_bright=folder1.edge_detect_binary(img_bright1)
    print('bright done:', count_bright)
    
    
    temp_img,count_noise=folder1.noise_removal(value)
    print('noise removal done:', count_noise)
    
    
    temp_img1,count_both=folder1.noise_removal(img_bright)
    print('both done:', count_both)
    
    
    out_file.write(key+','+str(count_raw)+','+str(count_bright)+','+str(count_noise)+','+str(count_both)+'\n')
    
with open('tables.txt','r') as in_file, open('tables_total1.txt','a') as out_file:
  #out_file.write('folder,min_raw,max_raw,avg_raw,min_bright,max_bright,avg_bright,min_noise,max_noise,avg_noise,min_both,max_both,avg_both\n')
  
  total_matrix=np.zeros(shape=[len(raw_dict),4])
  print(total_matrix.shape)
  folder_name= path.split('/')[-3:-1]
  print(folder_name)
  for i,line in enumerate(in_file):
    if i==0:
      continue
    else:
      a= line[:-1].split(',')
      print (a)
      total_matrix[i-1,0]=int(a[1])
      total_matrix[i-1,1]=int(a[2])
      total_matrix[i-1,2]=int(a[3])
      total_matrix[i-1,3]=int(a[4])
      
  out_file.write(folder_name[0]+'/'+folder_name[1]+','+str(np.min(total_matrix[:,0]))+','+str(np.max(total_matrix[:,0]))+','+str(np.mean(total_matrix[:,0]))+','+str(np.min(total_matrix[:,1]))+','+str(np.max(total_matrix[:,1]))+','+str(np.mean(total_matrix[:,1]))+','+str(np.min(total_matrix[:,2]))+','+str(np.max(total_matrix[:,2]))+','+str(np.mean(total_matrix[:,2]))+','+str(np.min(total_matrix[:,3]))+','+str(np.max(total_matrix[:,3]))+','+str(np.mean(total_matrix[:,3]))+'\n')
      
      
    
    
    

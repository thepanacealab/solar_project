from detection import dustDetection
import cv2 
import numpy as np 
import matplotlib.pyplot as plt

path='/home/large_data/southpole_data/dmlab/solar/south-pole/K-0/2017/1/7/9/'
path1= '/home/large_data/venus_work/temp_fits/'
folder1=dustDetection(path)
#folder1.extract_fits()
#folder1.brighten_images(5, 0)
#folder1.noise_remove_folder(0)
folder1.edge_folder(path1, 1)

'''


# Read image. 
img = cv2.imread('file_000.png', cv2.IMREAD_COLOR) 

# Convert to grayscale. 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

# Blur using 3 * 3 kernel. 
gray_blurred = cv2.blur(gray, (3, 3)) 

# Apply Hough transform on the blurred image. 
detected_circles = cv2.HoughCircles(gray_blurred, 
				cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
			param2 = 30, minRadius = 1, maxRadius = 10) 

# Draw circles that are detected. 
if detected_circles is not None: 

  # Convert the circle parameters a, b and r to integers. 
  detected_circles = np.uint16(np.around(detected_circles)) 
  
  for pt in detected_circles[0, :]: 
    a, b, r = pt[0], pt[1], pt[2] 
    
    # Draw the circumference of the circle. 
    cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
    
    # Draw a small circle (of radius 1) to show the center. 
    cv2.circle(img, (a, b), 1, (0, 0, 255), 3) 
    plt.figure(dpi=1200)
    plt.imshow(img)
    plt.show()
    #cv2.imshow("Detected Circle", img) 
    #cv2.waitKey(0) 
'''
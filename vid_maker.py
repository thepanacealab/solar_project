#this program creates a lossless video from images

import cv2
import os
from PIL import Image
image_folder = '/home/large_data/venus_work/test/'
video_name = '/home/large_data/venus_work/test/video2.avi'
#print(cv2.__version__)
#
#vid = cv2.VideoCapture('video.mp4')
#if not vid.isOpened():
#   raise IOError("Couldn't open webcam or video")
video_FourCC = cv2.VideoWriter_fourcc(*'MPEG')
#video_fps = vid.get(cv2.CAP_PROP_FPS)
#video_size = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))

#print(video_FourCC)
#print(video_fps)
#print(video_size)


images = [img for img in os.listdir(image_folder) if img.endswith(".tiff")]

for infile in images:
    # print "is tif or bmp"
    outfile = os.path.join(image_folder, infile[:-4] + "jpeg")
    im = Image.open(os.path.join(image_folder,infile))
    print(im.size)
    print ("new filename : " + outfile)
    im = im.convert("RGB")

    out = im.resize((1920,1440),Image.ANTIALIAS)

    out.save(outfile, "JPEG", quality=95)

images = [img for img in os.listdir(image_folder) if img.endswith(".jpeg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape


print(frame.shape)

video = cv2.VideoWriter(video_name, video_FourCC, 30, (width, height))


for j in range(30):
    for image in images:
        print("Writing the image : ", image)
        video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
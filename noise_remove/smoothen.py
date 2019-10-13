
from PIL import Image

# open an image file (.jpg or.png) you have in the working folder
im1 = Image.open("21_1_17_8_59a.tiff")

# multiply each pixel by 0.9 (makes the image darker)
# works best with .jpg and .png files, darker < 1.0 < lighter
# (.bmp and .gif files give goofy results)
# note that lambda is akin to a one-line function
im2 = im1.point(lambda p: p * 3.0)

# brings up the modified image in a viewer, simply saves the image as
# a bitmap to a temporary file and calls viewer associated with .bmp
# make certain you have associated an image viewer with this file type
im2.show()

# save modified image to working folder as Audi2.jpg
im2.save("21_1_17_8_59ab.tiff")
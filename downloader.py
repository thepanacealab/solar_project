# this program is created to upload files from website onto server


import wget
import os
path="/home/large_data/southpole_data/"
os.chdir(path)
url = "http://dmlab.cs.gsu.edu/solar/south-pole/"
wget.download(url,path)

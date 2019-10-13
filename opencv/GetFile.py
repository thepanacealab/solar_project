import os
import fnmatch
import numpy as np

from astropy.io import fits

import traceback 

# Author: Michael Tinglof 6/20/19
#     Class constructor takes a path to a fits file, opens the file, and returns a dictionary 
#     of header data and image data 
    
# @param takes in a path to a fits file 
class GetFile(): 
    def __init__(self, path): 
        self.file_path = path 
        
#     Returns a dictionary of a fits file with the file's header and image data 
#     @param 
#     @returns dictionary with header and image data 
    def getFile(self): 
        try: 
            with fits.open(self.file_path) as hdul: 
                return [hdul[0].header, hdul[0].data]
        except Exception as e: 
            raise FileNotFoundError("Could not open the fits file in get Map %s" % self.file_path)
        return None 
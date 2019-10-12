# this program is created to get information from fits files

import astropy.io
from astropy.io import fits

with fits.open('/home/large_data/southpole_data/dmlab/solar/south-pole/K-0/2017/1/7/9/MOTH.K.I.2017-01-07T09:19:37_l0.fits') as hdulist:  
     hdulist.info()
     for hdu in hdulist:
         print(repr(hdu.header))
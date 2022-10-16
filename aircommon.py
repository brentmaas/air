import numpy as np
from astropy.io import fits

def get_fits_header(fits_file):
    return fits.getheader(fits_file)

def get_fits_data(fits_file):
    return fits.getdata(fits_file)

def write_fits_data(fits_file, data):
    fits.writeto(fits_file, data, overwrite=True)

def create_masterbias_from_fits_files(fits_files):
    biasheader = get_fits_header(fits_files[0])
    masterbias = np.zeros((biasheader["NAXIS2"], biasheader["NAXIS1"]))
    for fits_file in fits_files:
        masterbias += get_fits_data(fits_file)
    masterbias /= len(fits_files)
    return masterbias
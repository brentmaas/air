import numpy as np
from astropy.io import fits

def get_fits_header(fits_file):
    return fits.getheader(fits_file)

def get_fits_data(fits_file):
    return fits.getdata(fits_file)

def write_fits_data(fits_file, data):
    fits.writeto(fits_file, data, overwrite=True)

def create_masterbias_from_fits_files(fits_files):
    bias_header = get_fits_header(fits_files[0])
    masterbias = np.zeros((bias_header["NAXIS2"], bias_header["NAXIS1"]))
    for fits_file in fits_files:
        masterbias += get_fits_data(fits_file)
    masterbias /= len(fits_files)
    return masterbias

def create_masterdark_from_fits_files(fits_files, masterbias_fits=None, exposure_time_key="EXPTIME", gain_key="GAIN"):
    dark_header = fits.getheader(fits_files[0])
    if masterbias_fits is None:
        masterbias = np.zeros((dark_header["NAXIS2"], dark_header["NAXIS1"]))
    dark_data = np.zeros((len(fits_files), dark_header["NAXIS2"], dark_header["NAXIS1"]))
    for i in range(len(fits_files)):
        dark_header = fits.getheader(fits_files[i])
        dark_data[i] = (fits.getdata(fits_files[i]) - masterbias) / dark_header[exposure_time_key] / dark_header[gain_key]
    masterdark = np.median(dark_data, axis=0)
    return masterdark

def create_masterflat_from_fits_files(fits_files, masterbias=None, masterdark=None, exposure_time_key="EXPTIME", gain_key="GAIN", rggb_componentwise=False):
    flat_header = fits.getheader(fits_files[0])
    if masterbias is None:
        masterbias = np.zeros((flat_header["NAXIS2"], flat_header["NAXIS1"]))
    if masterdark is None:
        masterdark = np.zeros((flat_header["NAXIS2"], flat_header["NAXIS1"]))
    flat_data = np.zeros((len(fits_files), flat_header["NAXIS2"], flat_header["NAXIS1"]))
    for i in range(len(fits_files)):
        flat_data[i] = (fits.getdata(fits_files[i]) - masterbias - masterdark * flat_header[exposure_time_key] * flat_header[gain_key]) / flat_header[exposure_time_key] / flat_header[gain_key]
    masterflat = np.median(flat_data, axis=0)
    if rggb_componentwise:
        masterflat /= np.median(masterflat)
    else:
        masterflat[::2,::2] /= np.median(masterflat[::2,::2])
        g_median = np.median(np.append(masterflat[1::2,::2], masterflat[::2,1::2]))
        masterflat[1::2,::2] /= g_median
        masterflat[::2,1::2] /= g_median
        masterflat[1::2,1::2] /= np.median(masterflat[1::2,1::2])
    return masterflat
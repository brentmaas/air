import numpy as np
from astropy.io import fits

def get_fits_header(fits_file):
    return fits.getheader(fits_file)

def get_fits_data(fits_file):
    return fits.getdata(fits_file)

def write_fits_data(fits_file, data, header=None):
    fits.writeto(fits_file, data, header=header, overwrite=True)

def create_masterheader_from_files(fits_files):
    masterheader = fits.getheader(fits_files[0])
    for fits_file in fits_files[1:]:
        header = fits.getheader(fits_file)
        for card in masterheader:
            if not card in header or masterheader[card] != header[card]:
                masterheader.remove(card)
    return masterheader

def create_masterbias_from_bias_files(bias_files):
    bias_header = fits.getheader(bias_files[0])
    masterbias = np.zeros((bias_header["NAXIS2"], bias_header["NAXIS1"]))
    for fits_file in bias_files:
        masterbias += fits.getdata(fits_file)
    masterbias /= len(bias_files)
    return masterbias

def create_masterdark_from_dark_files(dark_files, masterbias=None, exposure_time_key="EXPTIME", gain_key="GAIN"):
    dark_header = fits.getheader(dark_files[0])
    if masterbias is None:
        masterbias = np.zeros((dark_header["NAXIS2"], dark_header["NAXIS1"]))
    dark_data = np.zeros((len(dark_files), dark_header["NAXIS2"], dark_header["NAXIS1"]))
    for i in range(len(dark_files)):
        dark_header = fits.getheader(dark_files[i])
        dark_data[i] = (fits.getdata(dark_files[i]) - masterbias) / dark_header[exposure_time_key] / dark_header[gain_key]
    masterdark = np.median(dark_data, axis=0)
    return masterdark

def create_masterflat_from_flat_files(flat_files, masterbias=None, masterdark=None, exposure_time_key="EXPTIME", gain_key="GAIN", rggb_componentwise=False):
    flat_header = fits.getheader(flat_files[0])
    if masterbias is None:
        masterbias = np.zeros((flat_header["NAXIS2"], flat_header["NAXIS1"]))
    if masterdark is None:
        masterdark = np.zeros((flat_header["NAXIS2"], flat_header["NAXIS1"]))
    flat_data = np.zeros((len(flat_files), flat_header["NAXIS2"], flat_header["NAXIS1"]))
    for i in range(len(flat_files)):
        flat_data[i] = (fits.getdata(flat_files[i]) - masterbias - masterdark * flat_header[exposure_time_key] * flat_header[gain_key]) / flat_header[exposure_time_key] / flat_header[gain_key]
    masterflat = np.median(flat_data, axis=0)
    if rggb_componentwise:
        masterflat[::2,::2] /= np.median(masterflat[::2,::2])
        g_median = np.median(np.append(masterflat[1::2,::2], masterflat[::2,1::2]))
        masterflat[1::2,::2] /= g_median
        masterflat[::2,1::2] /= g_median
        masterflat[1::2,1::2] /= np.median(masterflat[1::2,1::2])
    else:
        masterflat /= np.median(masterflat)
    return masterflat

def create_science_from_light_file(light_file, masterbias=None, masterdark=None, masterflat=None, exposure_time_key="EXPTIME", gain_key="GAIN", do_sky_subtraction=False, rggb_componentwise=False):
    light_header = fits.getheader(light_file)
    if masterbias is None:
        masterbias = np.zeros((light_header["NAXIS2"], light_header["NAXIS1"]))
    if masterdark is None:
        masterdark = np.zeros((light_header["NAXIS2"], light_header["NAXIS1"]))
    if masterflat is None:
        masterflat = np.ones((light_header["NAXIS2"], light_header["NAXIS1"]))
    science_data = (fits.getdata(light_file) - masterbias - masterdark * light_header[exposure_time_key] * light_header[gain_key]) / masterflat / light_header[exposure_time_key] / light_header[gain_key]
    if rggb_componentwise:
        rggb_science_data = np.zeros((3, light_header["NAXIS2"] // 2, light_header["NAXIS1"] // 2))
        rggb_science_data[0] = science_data[::2,::2]
        rggb_science_data[1] = (science_data[1::2,::2] + science_data[::2,1::2]) / 2
        rggb_science_data[2] = science_data[1::2,1::2]
        if do_sky_subtraction:
            rggb_science_data[0] -= np.median(rggb_science_data[0])
            rggb_science_data[1] -= np.median([science_data[1::2,::2], science_data[::2,1::2]])
            rggb_science_data[2] -= np.median(rggb_science_data[2])
        return rggb_science_data
    else:
        if do_sky_subtraction:
            science_data -= np.median(science_data)
        return science_data
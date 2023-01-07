if __name__ == "__main__":
    from aircommon import *
    
    import argparse
    import sys
    import os
    
    parser = argparse.ArgumentParser(description="Commandline interface for Astronomical Image Reducer")
    parser.add_argument("--force-overwrite", help="Ignore confirmation prompts to overwrite existing files.", action="store_true")
    parser.add_argument("--exposure-time-key", help="The FITS header key for exposure time.", type=str, default="EXPTIME")
    parser.add_argument("--gain-key", help="The FITS header key for gain.", type=str, default="GAIN")
    parser.add_argument("--rggb-component-wise", help="Consider all FITS files to use the RGGB Bayer pattern and work component wise.", action="store_true")
    parser.add_argument("--bias", help="Bias FITS files to use for a master bias.", type=str, nargs="+")
    parser.add_argument("--masterbias", help="Master bias FITS file. If --bias is specified, it may be overwritten with their resulting master bias.", type=str)
    parser.add_argument("--dark", help="Dark FITS files to use for a master dark.", type=str, nargs="+")
    parser.add_argument("--masterdark", help="Master dark FITS file. If --dark is specified, it may be overwritten with their resulting master dark.", type=str)
    parser.add_argument("--flat", help="Flat FITS files to use for a master flat.", type=str, nargs="+")
    parser.add_argument("--masterflat", help="Master flat FITS file. If --flat is specified, it may be overwritten with their resulting master flat.", type=str)
    parser.add_argument("--light", help="Light FITS files to reduce to science images.", type=str, nargs="+")
    parser.add_argument("--do-sky-subtraction", help="Perform median sky subtraction on the resulting science images.", action="store_true")
    parser.add_argument("--science", help="Folder to save the resulting science images to.", type=str)
    parser.add_argument("--wcs", help="Try to solve the WCS of the science images.", action="store_true")
    parser.add_argument("--wcs-sciences",  help="Science FITS files to solve WCS for in addition to any resulting science images.", type=str, nargs="+")
    parser.add_argument("--wcs-ignore-failure", help="Ignore confirmation prompts when WCS solving fails.", action="store_true")
    parser.add_argument("--mosaic", help="Mosaic FITS file to write the resulting mosaic to.", type=str)
    parser.add_argument("--mosaic-sciences", help="Science FITS files to use for a mosaic in addition to any resulting science images.", type=str, nargs="+")
    parser.add_argument("--mosaic-coverage", help="FITS file to write the resulting mosaic coverage map to", type=str)
    parser.add_argument("--mosaic-full-coverage-only", help="Set any part of the mosaic that is not fully covered to zero and try to trim unused parts.", action="store_true")
    args = parser.parse_args()
    
    if not args.bias is None:
        print("\n=== Master bias ===")
        
        if args.masterbias is None and args.dark is None and args.flat is None and args.light is None:
            print("No use for master bias found, skipping")
            masterbias = None
        else:
            notexists = []
            for biasfile in args.bias:
                if not os.path.isfile(biasfile):
                    notexists.append(biasfile)
            if any(notexists):
                print("The following bias files could not be found:\n" + "\n".join(notexists))
                exit()
            
            masterbias = create_masterbias_from_bias_files(args.bias)
            print("The master bias has been created")
            
            if not args.masterbias is None and (not os.path.isfile(args.masterbias) or args.force_overwrite or input(f"The master bias file {args.masterbias} already exists, do you want to overwrite it? [y/N] ").lower() == "y"):
                write_fits_data(args.masterbias, masterbias)
                print(f"The master bias has been written to {args.masterbias}")
    elif not args.masterbias is None:
        masterbias = get_fits_data(args.masterbias)
    else:
        masterbias = None
    
    if not args.dark is None:
        print("\n=== Master dark ===")
        
        if args.masterdark is None and args.flat is None and args.light is None:
            print("No use for master dark found, skipping")
            masterdark = None
        else:
            notexists = []
            for darkfile in args.dark:
                if not os.path.isfile(darkfile):
                    notexists.append(darkfile)
            if any(notexists):
                print("The following dark files could not be found:\n" + "\n".join(notexists))
                exit()
            
            masterdark = create_masterdark_from_dark_files(args.dark, masterbias=masterbias, exposure_time_key=args.exposure_time_key, gain_key=args.gain_key)
            print("The master dark has been created")
            
            if not args.masterdark is None and (not os.path.isfile(args.masterdark) or args.force_overwrite or input(f"The master dark file {args.masterdark} already exists, do you want to overwrite it? [y/N] ").lower() == "y"):
                write_fits_data(args.masterdark, masterdark)
                print(f"The master dark has been written to {args.masterdark}")
    elif not args.masterdark is None:
        masterdark = get_fits_data(args.masterdark)
    else:
        masterdark = None
    
    if not args.flat is None:
        print("\n=== Master flat ===")
        
        if args.masterflat is None and args.light is None:
            print("No use for master flat found, skiping")
            masterflat = None
        else:
            notexists = []
            for flatfile in args.flat:
                if not os.path.isfile(flatfile):
                    notexists.append(flatfile)
            if any(notexists):
                print("The following flat files could not be found:\n" + "\n".join(notexists))
                exit()
            
            masterflat = create_masterflat_from_flat_files(args.flat, masterbias=masterbias, masterdark=masterdark, exposure_time_key=args.exposure_time_key, gain_key=args.gain_key, rggb_componentwise=args.rggb_component_wise)
            print("The master flat has been created")
            
            if not args.masterflat is None and (not os.path.isfile(args.masterflat) or args.force_overwrite or input(f"The master flat file {args.masterflat} already exists, do you want to overwrite it? [y/N] ").lower() == "y"):
                write_fits_data(args.masterflat, masterflat)
                print(f"The master flat has been written to {args.masterflat}")
    elif not args.masterflat is None:
        masterflat = get_fits_data(args.masterflat)
    else:
        masterflat = None
    
    if not args.light is None:
        print("\n=== Sciences ===")
        
        if args.science is None and args.mosaic is None:
            print("No use for sciences found, skipping")
            sciences = None
        else:
            os.makedirs(args.science, exist_ok=True)
            
            notexists = []
            for lightfile in args.light:
                if not os.path.isfile(lightfile):
                    notexists.append(lightfile)
            if any(notexists):
                print("The following light files could not be found:\n" + "\n".join(notexists))
                exit()
            
            sciences = []
            for lightfile in args.light:
                science = create_science_from_light_file(lightfile, masterbias=masterbias, masterdark=masterdark, masterflat=masterflat, exposure_time_key=args.exposure_time_key, gain_key=args.gain_key, do_sky_subtraction=args.do_sky_subtraction, rggb_componentwise=args.rggb_component_wise)
                filename = lightfile.replace("\\", "/").split("/")[-1]
                if filename.endswith(".fits"):
                    filename = filename[:-5]
                elif filename.endswith(".fit"):
                    filename = filename[:-4]
                outfile = args.science + "/" + filename + ".Science.fits"
                print(f"The science for light {filename} has been created")
                
                sciences.append(science)
                #Save if WCS doesn't need to be solved later
                if not args.science is None and not args.wcs and (not os.path.isfile(outfile) or args.force_overwrite or input(f"The science file {outfile} already exists, do you want to overwrite it? [y/N] ").lower() == "y"):
                    write_fits_data(outfile, science)
                    print(f"The science for light {filename} has been written to {outfile}")
    else:
        sciences = None
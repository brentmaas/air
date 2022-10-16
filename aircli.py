if __name__ == "__main__":
    from aircommon import *
    
    import argparse
    import sys
    import os
    
    parser = argparse.ArgumentParser(description="Commandline interface for Astronomical Image Reducer")
    parser.add_argument("--force-overwrite", help="Ignore confirmation prompts to overwrite existing files.", action="store_true")
    parser.add_argument("--bias", help="Bias FITS files to use for a master bias.", type=str, nargs="+")
    parser.add_argument("--masterbias", help="Master bias FITS file. If --bias is specified, it may be overwritten with their resulting master bias.", type=str)
    parser.add_argument("--dark", help="Dark FITS files to use for a master dark.", type=str, nargs="+")
    parser.add_argument("--masterdark", help="Master dark FITS file. If --dark is specified, it may be overwritten with their resulting master dark.", type=str)
    parser.add_argument("--flat", help="Flat FITS files to use for a master flat.", type=str, nargs="+")
    parser.add_argument("--masterflat", help="Master flat FITS file. If --flat is specified, it may be overwritten with their resulting master flat.", type=str)
    parser.add_argument("--light", help="Light FITS files to reduce to science images.", type=str, nargs="+")
    parser.add_argument("--science", help="Folder to save the resulting science images to.", type=str)
    parser.add_argument("--wcs", help="Try to solve the WCS of the science images.", action="store_true")
    parser.add_argument("--wcs-sciences",  help="Science FITS files to solve WCS for in addation to any resulting science images.", type=str, nargs="+")
    parser.add_argument("--wcs-ignore-failure", help="Ignore confirmation prompts when WCS solving fails.", action="store_true")
    parser.add_argument("--mosaic", help="Mosaic FITS file to write the resulting mosaic to.", type=str)
    parser.add_argument("--mosaic-sciences", help="Science FITS files to use for a mosaic in addition to any resulting science images.", type=str, nargs="+")
    parser.add_argument("--mosaic-coverage", help="FITS file to write the resulting mosaic coverage map to", type=str)
    parser.add_argument("--mosaic-full-coverage-only", help="Set any part of the mosaic that is not fully covered to zero and try to trim unused parts.", action="store_true")
    args = parser.parse_args()
    
    if not args.bias is None:
        print("\n=== Master bias ===")
        
        if args.masterbias is None and args.dark is None and args.flat is None and args.light is None:
            print("No use for master bias found")
            exit()
        
        notexists = []
        for biasfile in args.bias:
            if not os.path.isfile(biasfile):
                notexists.append(biasfile)
        if any(notexists):
            print("The following bias files could not be found:\n" + "\n".join(notexists))
            exit()
        
        masterbias = create_masterbias_from_fits_files(args.bias)
        print("The master bias has been created")
        
        if not args.masterbias is None and (not os.path.isfile(args.masterbias) or args.force_overwrite or input(f"The master bias file {args.masterbias} already exists, do you want to overwrite it? [y/N] ").lower() == "y"):
            write_fits_data(args.masterbias, masterbias)
            print(f"The master bias has been written to {args.masterbias}")
    elif not args.masterbias:
        masterbias = get_fits_data(args.masterbias)
    else:
        masterbias = None
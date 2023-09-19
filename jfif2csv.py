#!/usr/bin/env python

# 19. September 2023
# Joakim Skjefstad

import pycathx # From same folder

import glob
import os
import csv
import argparse



def folder_to_csv(folder, csv_filename, verbose=False):

    all_images = []

    for f in glob.glob(f"{folder}\**\*.jpg", recursive=True):
        if os.path.isfile(f):
            #jpg_instance = pycathx.CathxImage
            all_images.append((f, pycathx.target_file(f)))
    

    f = open(csv_filename, 'w', newline='')
    writer = csv.writer(f, quotechar='|', quoting=csv.QUOTE_MINIMAL)

    header = ["path", "altitude", "exposure", "aperture", "focus_enc"] # , "analog_gain", "digital_gain" does not seem to change
    writer.writerow(header)

    for image in all_images:
        filename = image[0]
        jfif = image[1]
        fields = [filename, jfif.altitude, jfif.exposure, jfif.aperture, jfif.focus_enc]
        #print(fields)
        writer.writerow(fields)

    f.close()
    print(f"Wrote csv to {csv_filename}")

def main():

    parser = argparse.ArgumentParser(prog='jfif2csv',
                    description='Convert some parameters to csv. Can (will?) be extended to contain all metadata one day.',
                    epilog='For more information, read source code.')

    parser.add_argument("-folder", type=str, nargs='?')
    args = parser.parse_args()

    if args.folder:
        folder = args.folder
        folder_to_csv(folder, "output.csv")
    print("Done, did you get expected output? Remember to add -folder=\"foldername\". Default output is output.csv")

if __name__=='__main__':
    main()
#!/usr/bin/env python

# Python module to read image metadata from Cathx-camera JFIF header
# JFIF header as given by CathX M12 Camera onboard an AUV
#
# 7. March 2023 - Initial
# 19. September 2023 - Updated
# Joakim Skjefstad

import xmltodict
import json
import argparse
import os
import glob

number_of_bytes_to_read = 2048 # We assume all data is in first 2048 bytes

class CathxImage:
    __slots__ = "image_time", "image_date", "acq_index",\
                "position_time", "position_time_received", "position_age",\
                "lat", "long", "altitude", "depth",\
                "pitch", "roll", "yaw",\
                "exposure", "digital_gain", "analog_gain", "sensor_gain",\
                "aperture", "focus", "name", "camera_session_name",\
                "focus_enc",\
                "errors_obj",\
                "software","fpga","pic","serial_number",\
                "json_dict"

    def __init__(self, obj):
        self.json_dict = obj # store a copy of the object

        # Image tag
        self.image_time = obj['image']['@time']
        self.image_date = obj['image']['@date']
        self.acq_index = obj['image']['@acq_index']

        # Position tag
        self.position_time = obj['image']['Position']['@time']
        self.position_time_received = obj['image']['Position']['@received']
        self.position_age = obj['image']['Position']['@age']
        self.lat = obj['image']['Position']['Coords']['@lat']
        self.long = obj['image']['Position']['Coords']['@long']
        self.altitude = obj['image']['Position']['Depth']['@altitude']
        self.depth = obj['image']['Position']['Depth']['@depth']
        self.pitch = obj['image']['Position']['Direction']['@pitch']
        self.roll = obj['image']['Position']['Direction']['@roll']
        self.yaw = obj['image']['Position']['Direction']['@yaw']

        # Acquisition tag
        self.exposure = obj['image']['acquisition']['exposure']
        self.digital_gain = obj['image']['acquisition']['digital_gain']
        self.analog_gain = obj['image']['acquisition']['analog_gain']
        self.sensor_gain = obj['image']['acquisition']['sensor_gain']
        self.aperture = obj['image']['acquisition']['aperture']
        self.focus = obj['image']['acquisition']['focus']
        self.name = obj['image']['acquisition']['name']
        self.camera_session_name = obj['image']['acquisition']['camera_session_name']
        self.focus_enc = obj['image']['acquisition']['focus_enc']

        # Errors tag
        self.errors_obj = obj['image']['errors']

        # Versions tag
        self.software = obj['image']['versions']['software']
        self.fpga = obj['image']['versions']['fpga']
        self.pic = obj['image']['versions']['pic']
        self.serial_number = obj['image']['versions']['serial_number']

    def __str__(self):
        return f'CathxImage: serial_number={self.serial_number} camera_session_name={self.camera_session_name} image_time={self.image_time} lat={self.lat} lon={self.long} altitude={self.altitude} depth={self.depth} exposure={self.exposure} aperture={self.aperture}'

    def get_json_dict(self):
        return self.json_dict
    

def target_file(filename, verbose=False):
    try:
        with open(filename, "rb") as fp:
            header_bytes = fp.read(number_of_bytes_to_read)

            jfif_start = header_bytes.find(b"JFIF")
            xml_start = header_bytes.find(b"<?xml")
            image_start = header_bytes.find(b"<image>")
            image_end = header_bytes.find(b"</image>")

            if not jfif_start:
                print("No jfif start")
                exit("No jfif")

            if not xml_start:
                print("No xml start found")
                exit("No xml")

            if not image_start:
                print("No image start")
                exit("No image start")

            if not image_end:
                print("No image end found")
                exit("No image end")

            xml_string = header_bytes[xml_start:image_end+8].decode("utf-8")
            #print(xml_string)

            json_img_dict = xmltodict.parse(xml_string)

            my_img = CathxImage(json_img_dict)

            if verbose:
                print(filename, my_img)

            json_formatted_str = json.dumps(my_img.get_json_dict(), indent=4)

            if verbose:
                print(json_formatted_str)
            
            return my_img # Return instance

    except FileNotFoundError as err:
        print("File not found")
        print(err)
        exit(-1)


def target_folder(folder, verbose=False):
    for f in glob.glob(f"{folder}\**\*.jpg", recursive=True):
        if os.path.isfile(f):
            target_file(f, verbose)

def main():
    parser = argparse.ArgumentParser(prog='pycathx example',
                    description='Example of .jpg-metadata extraction from CathX-images taken with an AUV.',
                    epilog='For more information, inspect metadata with Irfanview or read source code.')

    parser.add_argument("-filename", type=str, nargs='?')
    parser.add_argument("-folder", type=str, nargs='?')
    parser.add_argument("-verbose", action="store_true")

    args = parser.parse_args()

    verbose = False
    if args.verbose:
        print("Verbose activated")
        verbose = True

    if args.folder:
        folder = args.folder
        target_folder(folder, verbose)

    if args.filename:
        filename = args.filename
    else:
        filename = "sample.jpg"
    
    target_file(filename, verbose)
    print("Finished. No output? Add -verbose")

if __name__=='__main__':
    main()
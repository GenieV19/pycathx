import os
import re
import csv
import xml.etree.ElementTree as ET

# Folder containing your images

# specify missions here if you have already some you have processed or don't want to process. 
missions = ["Mission_59_20250928_1", "Mission_59_20250929_2"]

input_folder = "D:\AUV_Porsanger_2025\{mission_name}\CathxC"
basepath = r"D:\AUV_Porsanger_2025"
output_dir = "C:\Users\gevi\ownCloud\BRP assessments\Snowcrab\GV\PhD\AUV_scripts"



# change the above so I have a base path, mission name, then add the csathx folder - 
# need to ensure only unprocessed mission files are done

# Regex to pull XML metadata block from binary
xml_pattern = re.compile(rb"<\?xml.*?</image>", re.DOTALL)

# Columns in output CSV
fields = [
    "filename",
    "image_time", "image_date", "acq_index",
    "lat", "long", "altitude", "depth",
    "pitch", "roll", "yaw",
    "exposure", "digital_gain", "analog_gain", "sensor_gain",
    "aperture", "focus", "camera_name", "session_name",
    "serial_number"
]

for mission_name in missions:
    input_folder = os.path.join(basepath, mission_name, "CathxC")
    output_csv = os.path.join(output_dir, f"{mission_name}_image_metadata.csv")
    
    rows = []

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jfif", ".jpg", ".jpeg")):
            filepath = os.path.join(input_folder, filename)

            with open(filepath, "rb") as f:
                data = f.read()

            match = xml_pattern.search(data)
            if not match:
                print(f"No XML found in {filename}")
                continue

            xml_data = match.group().decode("utf-8", errors="ignore")
            root = ET.fromstring(xml_data)

            coords = root.find("./Position/Coords")
            depth = root.find("./Position/Depth")
            direction = root.find("./Position/Direction")
            acquisition = root.find("./acquisition")
            versions = root.find("./versions")

            row = {
            "filename": filename,
            "image_time": root.attrib.get("time", ""),
            "image_date": root.attrib.get("date", ""),
            "acq_index": root.attrib.get("acq_index", ""),
            "lat": coords.attrib.get("lat", "") if coords is not None else "",
            "long": coords.attrib.get("long", "") if coords is not None else "",
            "altitude": depth.attrib.get("altitude", "") if depth is not None else "",
            "depth": depth.attrib.get("depth", "") if depth is not None else "",
            "pitch": direction.attrib.get("pitch", "") if direction is not None else "",
            "roll": direction.attrib.get("roll", "") if direction is not None else "",
            "yaw": direction.attrib.get("yaw", "") if direction is not None else "",
            "exposure": acquisition.findtext("exposure", default="") if acquisition is not None else "",
            "digital_gain": acquisition.findtext("digital_gain", default="") if acquisition is not None else "",
            "analog_gain": acquisition.findtext("analog_gain", default="") if acquisition is not None else "",
            "sensor_gain": acquisition.findtext("sensor_gain", default="") if acquisition is not None else "",
            "aperture": acquisition.findtext("aperture", default="") if acquisition is not None else "",
            "focus": acquisition.findtext("focus", default="") if acquisition is not None else "",
            "camera_name": acquisition.findtext("name", default="") if acquisition is not None else "",
            "session_name": acquisition.findtext("camera_session_name", default="") if acquisition is not None else "",
            "serial_number": versions.findtext("serial_number", default="") if versions is not None else "",
            }

            rows.append(row)

# Save to CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Extracted {len(rows)} rows into {output_csv}")


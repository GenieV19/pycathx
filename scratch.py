import re
import xml.etree.ElementTree as ET

file = r"D:\AUV_Porsanger_2025\Mission_59_20250927_2\CathxC\image_D2025-09-27T09-40-00-054590Z_1.jpg"

xml_pattern = re.compile(rb"<\?xml.*?</image>", re.DOTALL)

with open(file, "rb") as f:
    data = f.read()

match = xml_pattern.search(data)
if not match:
    print("❌ No XML metadata found")
else:
    xml_data = match.group().decode("utf-8", errors="ignore")
    root = ET.fromstring(xml_data)

    coords = root.find("./Position/Coords")
    depth = root.find("./Position/Depth")

    print("Image time:", root.attrib.get("image time"))
    print("Date:", root.attrib.get("date"))
    print("Index:", root.attrib.get("acq_index"))
    print("Lat:", coords.attrib.get("lat") if coords is not None else "")
    print("Long:", coords.attrib.get("long") if coords is not None else "")
    print("Depth:", depth.attrib.get("depth") if depth is not None else "")
    print("Altitude:", depth.attrib.get("altitude") if depth is not None else "")

import re
import xml.etree.ElementTree as ET

file = r"D:\AUV_Porsanger_2025\Mission_59_20250927_2\CathxC\image_D2025-09-27T09-40-00-054590Z_1.jpg"

xml_pattern = re.compile(rb"<\?xml.*?</image>", re.DOTALL)

with open(file, "rb") as f:
    data = f.read()

match = xml_pattern.search(data)
if not match:
    print("❌ No XML metadata found")
else:
    xml_data = match.group().decode("utf-8", errors="ignore")
    root = ET.fromstring(xml_data)

    # Debug: print all attributes of root
    print("Root attributes:", root.attrib)

    # Extract values
    print("Image time:", root.attrib.get("time", "MISSING"))
    print("Date:", root.attrib.get("date", "MISSING"))
    print("Index:", root.attrib.get("acq_index", "MISSING"))

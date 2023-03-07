# pycathx

Small python script to read metadata from Cathx camera shots from AUVs. Naive, not much error-checking. Use with care.

---
<?xml version="1.0" encoding="utf-8"?>
<image time="12:32:33.832334" date="2022.11.27" acq_index="35636">
        <Position time="20221127T123233.747Z" received="2022-Nov-27 12:32:33.801059" age="31">
                <Coords long="5.8855731" lat="61.1452155"/>
                <Depth altitude="2.67" depth="1262.94"/>
                <Direction pitch="0.01" roll="-0.03" yaw="84.96"/>
        </Position>
        <acquisition>
                <exposure>1428</exposure>
                <digital_gain>1</digital_gain>
                <analog_gain>6</analog_gain>
                <sensor_gain>4</sensor_gain>
                <aperture>1.4</aperture>
                <focus>249</focus>
                <name>ColorCamera</name>
                <camera_session_name>pic_0</camera_session_name>
                <focus_enc>4129</focus_enc>
        </acquisition>
        <errors/>
        <versions>
                <software>0.938s1</software>
                <fpga>0x02d1</fpga>
                <pic>210</pic>
                <serial_number>238</serial_number>
        </versions>
</image>
---
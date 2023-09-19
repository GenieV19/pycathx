# pycathx

Small python script to read metadata from Cathx camera shots from AUVs. Naive, not much error-checking. Use with care.

Within the first bytes of a jpeg-file, you will see "JFIF" followed by a bit of XML.

This XML contains details including capture time, latitude and longitude according to the internal INS, altitude according to altimeter/DVL/multibeam as well as depth as measured.

Other information includes attitude of the AUV as well as camera details and version numbers.

You may find your transect tag in "camera_session_name". Maybe.

Be warned: Position timestamp does not match perfectly with image capture time. Image is captured after the position is recorded. It will also take time from a position message is received, the delta being up to 20-30 ms or more. By the time the position reaches the payload processor, it is already old - it has an age.

# jfif2csv

Extract some metadata and puts it into output.csv. Can be extended with other parameters.

Use this to analyze altitude, exposure and such, for example. Add argument -folder="subfolder" and it will recursively get data from all jpegs.

```csv
path,altitude,exposure,aperture,focus_enc
cathx\image_D2023-06-20T09-43-05-101411Z_2.jpg,3.23,800,1.5,4222
cathx\image_D2023-06-20T09-43-05-434733Z_0.jpg,3.23,800,1.5,4222
cathx\image_D2023-06-20T09-47-47-432421Z_0.jpg,2.94,800,1.75,4146
cathx\image_D2023-06-20T09-47-47-765761Z_1.jpg,2.91,800,1.75,4168
cathx\image_D2023-06-20T09-47-48-099087Z_2.jpg,2.91,800,1.75,4168
cathx\image_D2023-06-20T09-47-48-432418Z_0.jpg,2.94,800,1.75,4168
cathx\image_D2023-06-20T09-47-48-765757Z_1.jpg,2.94,800,1.5,4168
cathx\image_D2023-06-20T09-47-49-099084Z_2.jpg,2.94,800,1.5,4168
cathx\image_D2023-06-20T09-47-49-432404Z_0.jpg,2.91,800,1.5,4168
cathx\image_D2023-06-19T15-06-18-414079Z_0.jpg,3.93,1261,1.4,4358
cathx\image_D2023-06-19T15-06-18-747419Z_1.jpg,3.86,1261,1.4,4358
cathx\image_D2023-06-19T15-06-19-080750Z_2.jpg,3.86,1221,1.4,4358
cathx\image_D2023-06-19T15-06-19-414086Z_0.jpg,3.81,1221,1.4,4358
cathx\image_D2023-06-19T15-06-19-747410Z_1.jpg,3.74,1184,1.4,4358
cathx\image_D2023-06-19T15-06-28-413998Z_0.jpg,3.51,922,1.4,4258
cathx\image_D2023-06-19T15-06-28-747341Z_1.jpg,3.51,922,1.4,4258
cathx\image_D2023-06-19T15-06-29-080664Z_2.jpg,3.54,922,1.4,4258
cathx\image_D2023-06-19T15-06-29-414001Z_0.jpg,3.54,922,1.4,4258
```


# JFIF Structure
Can be viewed with IrfanView or your favourite hex-editor, we assume is in the beginning 2048 bytes.

```xml
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
```
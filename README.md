Create KML file (and/or CSV file)for all geo-tagged images (jpg or tif) in a directory.

Author:  Gerry Gabrisch GISP (gerry@shuksangeomatics.com)

 
This tool will take a directory of geo-tagged images (including images in any subdirectories) and 
it will create  a KML file or a CSV file in that directory. 

Created with Python 3.4 

This tool requires the following third-party libraries available from PyPi.
Pillow (Python 3 fork of the Python Image Library (PIL)
simplekml


The output KML file can be opened in Google Earth and each image will 
be referenced by a Google Earth icon (a black and white target).  Each 
icon is labeled with the image name.

Clicking on an icon in Google Earth will open a balloon box displaying 
the image, the image path relative to the kml, the image capture date, 
camera azimuth, and GNSS elevation.

The csv file can be imported into QGIS or ArcGIS with coordinates in WGS84 with elevation is height above the WGS84 elipsoid.

User Inputs

1. A directory of images (string)
2. A project name (will be used to name the output files). (string)
3. KML font color (this option is NOT available if you use the code via the GUI only the command line version allows for font color
in hex). (string)
4. Make KML (Boolean)
5. Make CSV (Boolean)


The KML will store relative paths to the images so the directory can me moved or shared.
As of this writing my version of Google Earth Pro does not support relative paths on Ubuntu Linux.


Create_KML_CSV_From_Geotagged_Images.py script can be executed at the command line with the example below.
$python Create_KML_CSV_From_Geotagged_Images2020.py '/home/gerry/PythonScripts/GeoEXIF/testimage' 'yourfilename' 'ff000000' True True

A graphical user interface to Create_KML_CSV_From_Geotagged_Images2020.py is available by executing 
$python geotag_gui.py
or running geotag_gui.py in a Python IDE will open the GUI.


Position accuracy is affected by weather, terrain, atmosphere, satellite availability
and electronics.  The positions recorded by this tool are extracted from the positions
recorded by your device.  Positional accuracy is not guaranteed.  You can improve your
location accuracy by letting your GNSS run prior to capturing images.  Check your location
in a mapping app like Google Maps to ensure your GNSS is recording your correct location
before capturing imagery with your device.


This software is provided AS-IS, without warranty of any kind, expressed or implied, including
but not limited to the warranties of merchantability, fitness for a particular purpose and 
noninfringment.  In no event shall the authors or copyright holders be liable of any claim,
damages, or other liability, whether in an action of contract, tort or otherwise, arising 
from, out of or in connection with the software of the use or other dealings in the software.
It is a copyright violation to distribute this program without permission of the author.

# Geotagged_Image_Tools

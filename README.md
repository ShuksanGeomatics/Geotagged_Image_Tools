Create KML file (and/or CSV file)for all geo-tagged images (jpg or tif) in a directory.
Author:  Gerry Gabrisch GISP (gerry@shuksangeomatics.com)
Python v3.6
Tested and working on Ubuntu 18.04 

 
This tool will take a directory of geo-tagged images (including images in any subdirectories) and 
it will create  a KML file and/or a CSV file in that directory. 

The output KML file can be opened in Google Earth and each image will 
be referenced by a Google Earth icon (a black and white target).  Each 
icon is labeled with the image name.

Clicking on an icon in Google Earth will open a balloon box displaying 
the image.  The balloon box will also include metadata including the image path relative to the KML, the image capture date, 
camera azimuth, and GNSS elevation.

The CSV file can be imported into a GIS using WGS84 with elevation is height above the WGS84 elipsoid (if your images also include elevation in the EXIF).

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`

User Inputs

1. A directory of images (string)
2. A project name (will be used to name the output files). (string)
3. KML font color (NOT optional if you use the GUI -only the command line version allows for font color in hex). (hexidecimal code as as string)
4. Make KML (Boolean)
5. Make CSV (Boolean)


Create_KML_CSV_From_Geotagged_Images.py script can be executed at the command line with the example below.
$python Create_KML_CSV_From_Geotagged_Images2020.py '/home/mycomputer/PythonScripts/GeoEXIF/testimage' 'yourfilename' 'ff000000' True True

A graphical user interface to Create_KML_CSV_From_Geotagged_Images2020.py is available. Open an new bash or cmd in ./geotagged_image_tools and run
$python geotag_gui.py
alternatevely you can also run geotag_gui.py in a Python IDE.


Image location accuracy is affected by terrain, atmosphere, satellite availability
and electronics quality.  The positions displayed by this tool are extracted from the positions
recorded by your GPS enabled camera. You can improve your location accuracy by letting your GNSS 
run prior to capturing images.  Check your location in a mapping app like Google Maps to ensure 
your GNSS is recording your correct location before capturing imagery with your device.


This software is provided AS-IS, without warranty of any kind, expressed or implied, including
but not limited to the warranties of merchantability, fitness for a particular purpose and 
noninfringment.  In no event shall the authors or copyright holders be liable of any claim,
damages, or other liability, whether in an action of contract, tort or otherwise, arising 
from, out of or in connection with the software of the use or other dealings in the software.
It is a copyright violation to distribute this program without permission of the author.

# Geotagged_Image_Tools

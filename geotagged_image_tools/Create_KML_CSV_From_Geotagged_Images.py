#!/usr/bin/python3
'''Created by Gerry Gabrisch (gerry@shuksangeomatics.com)
Creates a KML file or CSV file from a directory of JPG or TIFF files (and any sub-directories) after 
reading the EXIF header information from the files. 
Opening the KML file in Google Earth allows the user to click on a location point and view
the image in Google Earth.  

This script can be run 
1. at a command line (see main() below for more information.
2. In Python IDE software with a few changes in main().
3. Or via the graphic user interface using geotag_gui'''

import sys
import traceback
import os

try:
    
    import PIL
    from PIL import Image
    from PIL.ExifTags import TAGS
    import simplekml
    kml = simplekml.Kml()

    
    def get_exif(fn):
        '''This get the EXIF data...'''
        ret = {}
        i = Image.open(fn)
        try:
            info = i._getexif()
    
            for t, v in info.items():
                try:
                    decoded = TAGS.get(t, t)
                    ret[decoded] = v
                except:
                    pass
            if "GPSInfo" in ret:
                return ret["GPSInfo"]
            else:
                return {}
        except:
            return {}
    def process_gps(tags):
        gps = {}
        if (tags != None) and (1 in tags) and (not tags[1] == "\x00"): # 1 and 3 are not present if the coords keys are not present and will be null if no coords
            #gps["y"] = dmsdec(tags[2][0][0], tags[2][0][1], tags[2][1][0], tags[2][1][1], tags[2][2][0], tags[2][2][1], tags[1])
            #gps["x"] = dmsdec(tags[4][0][0], tags[4][0][1], tags[4][1][0], tags[4][1][1], tags[4][2][0], tags[4][2][1], tags[3])
            gps["y"] = dmsdec(tags[2], tags[1])
            gps["x"] = dmsdec(tags[4], tags[3])            
        return gps
    def dmsdec(coords, o):
        '''Convert the coordinates into a GIS/KML compatible form....'''
        degree = float(coords[0])
        minute = coords[1]/60.0
        second = coords[2]/3600.0
        coord = degree + minute + second
        if(o == "S" or o == "W"):
            coord = coord * -1
        return coord
    def get_exif_data(fname):
        '''Get embedded EXIF image width, height, and data from image file.'''
        ret = {}
        ret2 = {}
        try:
            img = Image.open(fname)
            if hasattr( img, '_getexif' ):
                exifinfo = img._getexif()
                if exifinfo != None:
                    for tag, value in exifinfo.items():
                        
                        decoded = TAGS.get(tag, tag)
                        ret[decoded] = value
        except IOError:
            print ('IOERROR ' + fname)
    
        try:
            return [ret['ImageWidth'], ret['ImageLength'],ret['DateTime']]
        except:
            return [ret['ExifImageWidth'], ret['ExifImageHeight'],ret['DateTimeOriginal']]
    def get_AltAndAzi(fname):
        '''Get the altitude (in WGS84 elipsoid vertical datum) and azimuth (from magnetic north)...'''
        img = PIL.Image.open(fname)
        exif_data = img._getexif()
        exif = {PIL.ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in PIL.ExifTags.TAGS}
        try:
            alt = int(exif['GPSInfo'][6][0]/exif['GPSInfo'][6][1]*3.28084)
        except:
            alt = "No altitude data for this image."
        try:
            azi =  int(exif['GPSInfo'][17][0]/exif['GPSInfo'][17][1])
        except:
            azi = "No camera azimuth data for this image."
        return(alt, azi)
                
    def fDecantonate(s1, s2):
        '''removes the string s1 from the front of string s2, I can't remember why this was an issue?!?!?'''
        s1l = len(s1)
        if s1 == s2[:s1l]:
            return s2[s1l:]
        else:
            return "fDecantonate failed! Strings do not match, decantonation not possible." 
    
    def make_files(inDir, projectName, incolor, make_kml, make_csv):
        outKML = inDir+"/"+ projectName + ".kml"
        outCSV = inDir+"/"+ projectName + ".csv"
        
        
        if make_csv:
            #If users wants a CSV then remove any existing csv file from the directory with the same name, create a new file, and write the csv header.
            #Otherwise the script will append to an existing file.        
            if os.path.isfile(outCSV):
                os.remove(outCSV)
            f = open(outCSV,'a')
            #Create the CSV header...
            f.writelines('x,y,imagename,fullpath,imagedate\n')
             
        #Go throught all the directories and subdirecories starting at the input folder and get the geotag information for each image.
        
        for (dirpath, dirnames, filenames) in os.walk(inDir):
            for inFile in filenames:
                if inFile.endswith('.jpg') or inFile.endswith('.JPG') or inFile.endswith('.tif') or inFile.endswith('.TIF'):
                    if dirpath == inDir:
                        relativePath = inFile
                        fullpath = os.path.join(dirpath,inFile)
                    else:
                        relativePath = os.path.join(fDecantonate(inDir, dirpath),inFile)
                        relativePath = relativePath[1:]
                        fullpath = os.path.join(dirpath,inFile)                 
                    try:
                        aa = get_AltAndAzi(fullpath)
                        exifstuff = get_exif_data(fullpath)
                        theTags = get_exif(fullpath)
                        theCoords = process_gps(theTags)
                        tupleCoords =  (theCoords['x'], theCoords['y'])
                        
                    except:
                        #Some images may not have geotag info so just skip over those....
                        print ("No geotag information.  Image skipped: ", fullpath)
                        
                    else:
                        print ("Creating point data for: ", fullpath)
                        #Google earth is case sensitive. Replace upper case file name extensions with lower case if the suffix is upper case...
                        if inFile.endswith('.JPG'):
                            relativePath = relativePath.replace('.JPG', '.jpg')
                        if inFile.endswith('.TIF'):
                            relativePath = relativePath.replace('.TIF', '.tif')
                            
                        #This stuff will end up in the KML for the user to see if they click the image point in Google Earth...    
                        thetext ='<img src="'+ fullpath + '" height="' + str(exifstuff[1]/4) + '" width="' + str(exifstuff[0]/4)+\
                        '" alt="path failed"/>'+ '<br>Project Name: '+ projectName+ \
                        '<br>Image Capture Date & Time: '+exifstuff[2]+\
                        '<br>Camera Azimuth(deg): '+ str(aa[1])+ \
                        '<br>GPS Elevation(ft):' + str(aa[0])+ \
                        '<br>Image Location and File Name:'+ relativePath +\
                        "<br><br>Geotagged Images to KML & CSV  - Created by Gerry Gabrisch (gerry@shuksangeomatics.com) 2020"
                       
                        #This defines the KML point and how it looks
                        pnt = kml.newpoint(name= inFile, coords=[tupleCoords])
                        pnt.style.iconstyle.icon.href ="http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png"
                        #pnt.style.labelstyle.color = textcolor
                        
                        
                        pnt.style.balloonstyle.text = thetext
                        pnt.style.balloonstyle.bgcolor = simplekml.Color.white
                        pnt.style.balloonstyle.textcolor = simplekml.Color.black
                        
                        if make_csv:
                            #write lines to the CSV
                            f.writelines(str(theCoords['x'])+","+ str(theCoords['y']) +"," + inFile +"," + fullpath +","+  exifstuff[2]+","+ '\n')
                        
                        
        ##If user wants a KML then write the KML>  Otherwise delete the outKML from memory...
        if make_kml:               
            kml.save(outKML)
    
        
        ##If user wants a CSV then close f.
        if make_csv:   
            f.close()
        
        
        print ("Done Without Errors")      
        
except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    print ("PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1]))

def main():
    
    #command line example below...
    #python Create_KML_CSV_From_Geotagged_Images2020.py '/home/gerry/PythonScripts/GeoEXIF/testimage' 'run_as_main' 'ff000000' True True
    #make_files(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])    
    
    ##  To run in an IDE - comment out the command line example above.  Uncomment the code below and add your own parameters
    ##The directory of geotagged images....
    inDir = '/home/gerry/PythonScripts/Geotagged_Image_Tools/tests/test_images'
    #This will be the name of the KML or CSV file created but with the KML or CSV extension
    projectName = 'ran_as_main'
    #This is the KML font color...
    incolor  = 'ff000000'
    #Set to true if you want the KML file...
    make_kml = True
    #Set to true if you want the CSV file...
    make_csv = True
    make_files(inDir, projectName, incolor, make_kml, make_csv)
    ############
    
if __name__ == "__main__":
    main()
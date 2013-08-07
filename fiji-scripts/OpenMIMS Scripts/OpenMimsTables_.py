import com.nrims as nrims

import java.io.File as File
import java.util.ArrayList as ArrayList
import java.lang.Integer as Integer

import sys
from java.lang.System import getProperty
sys.path.append(getProperty("fiji.dir") + "/plugins/Scripts/Plugins/OpenMIMS Scripts/")
from OMUtilities import MultiFileDialog
from OMUtilities import CheckFileLists

import os
import jarray

#hide/show debug prints
verbose = 1 

IJ.log("\n\nStarting OpenMIMSTables")

# The directory containing the .im/.nrrd files.
#imDirName = "/nrims/home3/cpoczatek/Fiji_test/test_images";

# The list of files.
imFileNames = MultiFileDialog("Open Image Files")

if verbose > 0:
  print "Image Files:"
  for i in range(len(imFileNames)):
    print imFileNames[i]

imDirName = os.path.dirname(imFileNames[0])
print "asdf " + imDirName

# The list of roi files (Needs to have same number of entries as .im files above).
roiFileNames = MultiFileDialog("Open ROI Files")

if verbose > 0:
  print "Roi Files:"
  for i in range(len(roiFileNames)):
    print roiFileNames[i]

# The list of files.
#imFileNames = ["test_file.nrrd", "test_file2.nrrd", "test_file3.nrrd"]
# The list of roi files (Needs to have same number of entries as .im files above).
#roiFileNames = ["test_file.rois.zip", "test_file2.rois.zip", "test_file3.rois.zip"]

# List of statistics.
# Others: "mean", "stddev", "median", "N/D", 
#         "min", "max", "sum", "mode", "area", 
#         "group", "roix", "roiy", 
#         "roiwidth", "roiheight"
stats = ["group", "area", "mean", "stddev", "N/D"]

#////////////////////////////
# Initialize stuff.
#////////////////////////////
ui = nrims.UI()
ui.show()

#////////////////////////////
# Loop over files.
#////////////////////////////
for i in range(len(imFileNames)):
  
  imFile = File(imFileNames[i])
  roiFile = File(roiFileNames[i])
  #IJ.log("Opening: "+imFileNames[i])
  ui.openFile(imFile)
  #IJ.log("Opening: "+roiFileNames[i])
  ui.openFile(roiFile)
  
  #////////////////////////////
  # Get the planes.
  #////////////////////////////
  planes = ui.getmimsTomography().getPlanes()

  #////////////////////////////
  # Get the rois.
  #////////////////////////////
  rois = ui.getRoiManager().getAllROIs()

  #////////////////////////////
  # Get images.
  #////////////////////////////
  imageArray = ArrayList()
  
  massimages = ui.getOpenMassImages()
  for j in range(len(massimages)):
    imageArray.add(massimages[j])
  
  
  # Ratio images
  # 0 corresponds to the first mass image (e.g. mass 12.0)
  # 1 corresponds to the second mass image (e.g. mass 13.0)
  ratioProps1 = nrims.RatioProps(1, 0)
  mp1 = nrims.MimsPlus(ui, ratioProps1)
  imageArray.add(mp1)
  IJ.log("Opening ratio: "+mp1.getTitle())

  # Ratio images
  # 2 corresponds to the first mass image (e.g. mass 26.0)
  # 3 corresponds to the second mass image (e.g. mass 27.0)
  ratioProps2 = nrims.RatioProps(3, 2)
  mp2 = nrims.MimsPlus(ui, ratioProps2)
  imageArray.add(mp2)
  IJ.log("Opening ratio: "+mp2.getTitle())

  images = jarray.zeros(imageArray.size(), nrims.MimsPlus)
  images = imageArray.toArray(images)
  
  #////////////////////////////
  # Create and display table.
  #////////////////////////////
  table = nrims.MimsJTable(ui)
  table.setStats(stats)
  table.setRois(rois)
  table.setImages(images)
  table.setPlanes(planes)
  #append=false
  nPlanes = ui.getOpener().getNImages()
  if nPlanes > 1:
       table.createTable(False)
  else:
       table.createSumTable(False)
  #table.showFrame();
  
  csvFileName = os.path.join(imDirName, ui.getImageFilePrefix()+"_data.csv")
  if os.path.exists(csvFileName):
    IJ.log("ERROR: file" + csvFileName + " exists. Skipping.")
  else:
    IJ.log("Writing: " + csvFileName)
    table.writeData(File(csvFileName))
    table.close()
    
  IJ.log("")

ui.closeCurrentImage()
ui.close()
IJ.log("OpenMIMSTables finished.\n\n")

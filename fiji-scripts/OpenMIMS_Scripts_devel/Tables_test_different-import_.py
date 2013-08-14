import com.nrims.UI as UI
import com.nrims.RatioProps as RatioProps
import com.nrims.MimsPlus as MimsPlus
import com.nrims.MimsJTable as MimsJTable

import java.io.File as File
import java.util.ArrayList as ArrayList
import java.lang.Integer as Integer

import jarray

# The directory containing the .im/.nrrd files.
imDirName = "/nrims/home3/cpoczatek/Fiji_test/test_images";

# The list of files.
imFileName = ["test_file.nrrd", "test_file2.nrrd", "test_file3.nrrd"]

# The list of roi files (Needs to have same number of entries as .im files above).
roiFileName = ["test_file.rois.zip", "test_file2.rois.zip", "test_file3.rois.zip"]

# List of statistics.
# Others: "mean", "stddev", "median", "N/D", 
#         "min", "max", "sum", "mode", "area", 
#         "group (table only)", "roix", "roiy", 
#         "roiwidth", "roiheight"
stats = ["mean", "stddev"]

#////////////////////////////
# Initialize stuff.
#////////////////////////////
ui = UI()
ui.show()

#////////////////////////////
# Loop over files.
#////////////////////////////
for i in range(len(imFileName)):
	#where is this going?
	#print "Opening: " #+ imFileName[i] + ", " roiFileName[i]
	
	imFile = File(imDirName, imFileName[i])
	roiFile = File(imDirName, roiFileName[i])
	IJ.log("Opening: "+imFileName[i])
	ui.openFile(imFile)
	IJ.log("Opening: "+roiFileName[i])
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
	ratioProps1 = RatioProps(1, 0)
	mp1 = MimsPlus(ui, ratioProps1)
	imageArray.add(mp1)
	IJ.log("Opening ratio: "+mp1.getTitle())

	# Ratio images
	# 2 corresponds to the first mass image (e.g. mass 26.0)
	# 3 corresponds to the second mass image (e.g. mass 27.0)
	ratioProps2 = RatioProps(3, 2)
	mp2 = MimsPlus(ui, ratioProps2)
	imageArray.add(mp2)
	IJ.log("Opening ratio: "+mp2.getTitle())

	images = jarray.zeros(imageArray.size(), MimsPlus)
	images = imageArray.toArray(images)
	
	#////////////////////////////
	# Create and display table.
	#////////////////////////////
	table = MimsJTable(ui)
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
	IJ.log("Writing: "+imDirName+"/"+ui.getImageFilePrefix()+"_data.csv")
	table.writeData(File(imDirName, ui.getImageFilePrefix()+"_data.csv"))
	table.close()
	IJ.log("")

ui.closeCurrentImage()
ui.close()

import ij as ij
import ij.IJ as IJ
import com.nrims as nrims
import sys
from sys import exit

targets = []
sources = []

ui = nrims.UI.getInstance()
verbose = 1
IJ.log("Starting OpenMIMS Image Registration script")
if ui == None:
	IJ.log("ERROR: No instance of OpenMims window")
else:
	IJ.log("Instructions on how to use:")
	IJ.log("IMPORTANT: It is strongly recommenended that you compress your OpenMIMS images before use.")
	IJ.log("1) Open your target image in File->Open Non-MIMS Image:")
	IJ.log("2) Create two ROI groups in the OpenMIMS Roi Manager called \"source\" and \"target\":")
	IJ.log("3) Select the point ROI tool (right next to the angle tool). Use this to create 3 rois on landmarks of your choice on the non-OpenMIMS image.")
	IJ.log("4) Assign these three ROI's to the \"target\" group using the ROI Manager.")
	IJ.log("5) Create three ROI landmarks on your OpenMIMS images. \nIMPORTANT: these ROI's must be placed in the same order and desired location as the target ROI's \ni.e. the first target ROI you created will be registered to the first source ROI you create, and similarly for the second and third.")
	IJ.log("6) Assign these three ROI's to the \"source\" group using the ROI Manager.")
	IJ.log("7) Run this script.")
	IJ.log("8) If you want to work on all the images simultaneously afterwords, use Analyze->Tools->Synchronize Windows.\n\n")
	massImages =	ui.getOpenMassImages()     # an array of MimPlus object??
	
	if len(massImages) == 0:
		IJ.log("ERROR: There are no OpenMIMS images open to register.")
#		exit()
#		return		# only works in a function, not here
#		sys.exit(0)		 # Preferred technique for quitting a python program, but causes Fiji to quit
#		sys.exit()		 #causes Fiji to quit
#		exit()		 #gives error saying exit is not defined, unless you import exit, then it causes Fiji to quit
#		quit()		 #gives error saying quit is not defined
	else:
		IJ.log("OpenMIMS images found, performing registration...")
		
	for source in massImages:
		#////////////////////////////
		# copy sum and source image 
		# source = image we want to modify through turboreg
		# target = image that we are fitting source to
		# note: setting sum image to first one for testing's sake, ideally we'll find another solution
		#////////////////////////////
		target = ui.getOpenNonMimsImages()[0]
		if target == None:
			IJ.log("ERROR: No non-OpenMIMS image is open. Please open one using File->Open Non-MIMS Image.")
			exit()
		
		sourceHeight = source.getHeight()
		sourceWidth = source.getWidth()
		targetHeight = target.getHeight()
		targetWidth = target.getWidth()
		roiManager = ui.getRoiManager()
		rois = roiManager.getAllROIs()
		for roi in rois:
			if roiManager.getRoiGroup(roi.getName()) == "target" and len(targets) < 3:
				#IJ.log("Target landmark at " + str(roi.getXBase()) + " " + str(roi.getYBase()))
				targets.append(" " + str(roi.getXBase()) + " " + str(roi.getYBase()))
			if roiManager.getRoiGroup(roi.getName()) == "source" and len(sources) < 3:
				sources.append(" " + str(roi.getXBase()) + " " + str(roi.getYBase()))
				#IJ.log("Source landmark at " + str(roi.getXBase()) + " " + str(roi.getYBase()))
		if len(targets) < 3:
			IJ.log("ERROR: Not enough target landmarks.")
			exit()
		if len(sources) < 3:
			IJ.log("ERROR: Not enough source landmarks.")
			exit()
				
#  .nrrd or .im files that have more than one series will have windows titles with spaces in them,
#  and all kinds of other characters like parenthesis and colon that also might not work
#  with TurboReg.   I will have to change the window names in place to something
#  TurboReg can digest, then set the names back again.   Ugh.
		windowName = source.getTitle()
		IJ.log("\nWindow name is " + windowName)
		origWindowName = windowName

#		if windowName.find(" "):
#			windowName = windowName.replace(" ", "")
#			IJ.log("Window name without spaces is " + windowName)
		
		IJ.log("Temporarily renaming image window to a name that will not cause TurboReg to fail:  temporarayWindowName.nrrd")
		source.setTitle("temporarayWindowName.nrrd")
		
		windowName = source.getTitle()
			
		macrocmd =	"-transform -window " + source.getTitle() + " " + str(targetWidth) + " " + str(targetHeight)
		macrocmd = macrocmd + " -affine" + sources[0]	 + targets[0]+ sources[1] + targets[1] + sources[2] + targets[2] +" -showOutput"
		IJ.log("macrocmd being submitted to TurboReg = " + macrocmd + "\n")
		IJ.log("Running affine transform on " + source.getTitle())
		IJ.run("TurboReg ",	 macrocmd)
		output = ij.WindowManager.getImage("Output")
		source.setProcessor(output.getProcessor())
		output.close()
		source.setTitle(origWindowName)
		IJ.log("Restoring window name back to the original:   " + origWindowName)
	IJ.log("\n\nRegistration of all images complete.")

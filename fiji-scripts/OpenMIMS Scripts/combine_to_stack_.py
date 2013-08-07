import com.nrims as nrims
import com.nrims.data as nrimsData
import com.nrims.UI as nrimsUI
import com.nrims.ContrastAdjuster as caadj

import java.io.File as File
import java.util.ArrayList as ArrayList
import java.lang.Integer as Integer

import sys
from java.lang.System import getProperty
sys.path.append(getProperty("fiji.dir") + "/plugins/Scripts/Plugins/OpenMIMS Scripts/")

import os
import jarray

verbose = 1 

IJ.log("\n\nStarting combine nrrds")

ui = nrimsUI.getInstance()
if ui != None:
	IJ.log("Theres an instance")
mimStack = ui.getmimsStackEditing()
imp = ArrayList()
images = ui.getOpenMassImages()
IJ.log(str(len(images)))
#compress the planes
blockSize = images[0].getNSlices()
done = mimStack.compressPlanes(blockSize)
ui.getmimsAction().setIsCompressed(done)
ui.getmimsAction().setBlockSize(blockSize)
images = ui.getOpenMassImages()
#force to 32bit
massCorrection = nrimsData.massCorrection(ui)
massCorrection.forceFloatImages(images)
workStack = ImageStack(images[0].getWidth(), images[0].getHeight())
for i in range(len(images)):
	workStack.addSlice(images[i].getTitle(), images[i].getProcessor())
n = len(images);
finalImage = ImagePlus("Combined image", workStack)
finalImage.setSlice(1)
finalImage.setDimensions(n, 1, 1)
finalImage = CompositeImage(finalImage, 3)
finalImage.setOpenAsHyperStack(True)
for i in range(len(images)):
	finalImage.setC(i+1)
	#IJ.resetThreshold()
	IJ.resetMinAndMax(finalImage)
	#IJ.setMinAndMax(images[i].getProcessor().getMin(), images[i].getProcessor().getMax())
	finalImage.getProcessor().setLut(images[i].getProcessor().getLut())
	IJ.run(finalImage, "Enhance Contrast", "saturated=0.5")
finalImage.show()
mimStack.uncompressPlanes()
#all work is done in first file
    		
import com.nrims as nrims
import com.nrims.data as nrimsData
import com.nrims.UI as nrimsUI

import java.io.File as File
import java.lang as lang
import java.util.ArrayList as ArrayList
import java.lang.Integer as Integer

import sys
from java.lang.System import getProperty
sys.path.append(getProperty("fiji.dir") + "/plugins/Scripts/Plugins/OpenMIMS Scripts/")
import os
import jarray

IJ.log("Starting auto Turbo reg")
ui = nrimsUI.getInstance()

if ui == None:
	IJ.log("No instance of OpenMims window")
else:
	openSum = ui.getOpenSumImages()
	if len(openSum) != 0:

		#copy sum and source image
		#setting sum image to first one for testing's sake
		sumImage = openSum[0]
		target = sumImage.duplicate()
		source = IJ.getImage().duplicate()
		
		#scale image
		targetProcessor = target.getProcessor()
		sourceProcessor = source.getProcessor()
		sourceWidth = sourceProcessor.getWidth()
		sourceHeight = sourceProcessor.getHeight()
		target.setProcessor(targetProcessor.resize(sourceWidth, sourceHeight))
		
		#this causes the turboreg plugin to show these as the first choices for target and source
		#don't know why though, but it works
		target.show()
		source.show()
		IJ.log("Please choose " + source.getTitle() + " as source")
		IJ.log("Please choose " + target.getTitle() + " as target")
		
		#run turboReg
		numImages = WindowManager.getImageCount()
		IJ.run("TurboReg ", "")
		#need to wait while user inputs turboreg options and the plugin runs
		while WindowManager.getImageCount() == numImages:
			i = 0
		
		#save the turboreg output
		workOutput = IJ.getImage().duplicate()
		prefix = ui.getLastFolder() + '/' + ui.getImageFilePrefix()
		FileSaver(workOutput).saveAsTiffStack(prefix + '_reg-output')
		
		#cast sum image and output to RGB
		workOutput.setProcessor(workOutput.getProcessor().convertToRGB())
		target.setProcessor(target.getProcessor().convertToRGB())
		
		#make new image with source on top and target on bottom
		stack = workOutput.createEmptyStack()
		stack.addSlice(workOutput.getProcessor())
		stack.addSlice(target.getProcessor())
		workImage = workOutput.createImagePlus()
		workImage.setStack(stack)
		workImage.setTitle("Registered Image Overlay")
		IJ.getImage().close()
		workImage.show()
		target.close()
		source.close()

		#save final overlayed image
		FileSaver(workImage).saveAsTiffStack(prefix + "_reg-output-overlay")
	

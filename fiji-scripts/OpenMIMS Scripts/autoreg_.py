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

#////////////////////////////
# Get existing instance of OpenMims
#////////////////////////////
IJ.log("Starting auto Turbo reg")
ui = nrimsUI.getInstance()

if ui == None:
IJ.log("No instance of OpenMims window")
  else:
  openSum = ui.getOpenSumImages()
  if len(openSum) != 0:
    #////////////////////////////
    # copy sum and source image 
    # source = image we want to modify through turboreg
    # target = image that we are fitting source to
    # note: setting sum image to first one for testing's sake, ideally we'll find another solution
    #////////////////////////////
    sumImage = openSum[0]
    target = sumImage.duplicate()
    source = IJ.getImage().duplicate()

    #////////////////////////////
    # Scale target image to source size (Ex.sum image to EM image size)
    #////////////////////////////
    targetProcessor = target.getProcessor()
    sourceProcessor = source.getProcessor()
    sourceWidth = sourceProcessor.getWidth()
    sourceHeight = sourceProcessor.getHeight()
    target.setProcessor(targetProcessor.resize(sourceWidth, sourceHeight))

    #note: this causes the turboreg plugin to show these as the first choices for target and source
    #don't know why though, but it works
    target.show()
    source.show()
    #IJ.log("Please choose " + source.getTitle() + " as source")
    #IJ.log("Please choose " + target.getTitle() + " as target")

    #////////////////////////////
    # Run turboReg
    #////////////////////////////
    numImages = WindowManager.getImageCount()
    IJ.run("TurboReg ", "")
		
    #////////////////////////////
    # Wait while user inputs turboreg options and the plugin runs
    #////////////////////////////
    while WindowManager.getImageCount() == numImages:
      i = 0
      output = WindowManager.getImage("Output")
      #IJ.log(str(target.isVisible()) + str(source.isVisible()) + str(output.getTitle()) + str(target.getTitle()))

      #////////////////////////////
      # Check here for whether any of the needed windows have closed. Assume that the user no longer wants to register and quit
      #////////////////////////////
      if target.isVisible() == True and source.isVisible() == True and output != None:
      
        #////////////////////////////
        # grab the turboreg output
        #////////////////////////////   
        workOutput = output.duplicate()
        
        #////////////////////////////
        # Save the turboreg output after flattening to RGB
        #////////////////////////////
        workOutputToSave = output.flatten()
        prefix = ui.getLastFolder() + '/' + ui.getImageFilePrefix()
        FileSaver(workOutputToSave).saveAsTiff(prefix + '_reg-output')

        #////////////////////////////
        # Add output and target slices to stack and create composite image
        #////////////////////////////
        workStack = target.createEmptyStack()
        workStack.addSlice(workOutput.getProcessor())
        workStack.addSlice(target.getProcessor())
        overlay = ImagePlus("TurboReg Composite Overlay", workStack)
        overlay = CompositeImage(overlay, 1)
        overlay.show()

	#////////////////////////////
        # Save final overlayed image
        #////////////////////////////
        overlayToSave = overlay.flatten()
        FileSaver(overlayToSave).saveAsTiff(prefix + "_reg-output-overlay")

	#////////////////////////////
        # Close windows
        #////////////////////////////
        output.setTitle("TurboReg Output")
        workOutput.close()
        target.close()
        source.close()
        workOutputToSave.close()
        overlayToSave.close()
      else:
        target.close()
        source.close()




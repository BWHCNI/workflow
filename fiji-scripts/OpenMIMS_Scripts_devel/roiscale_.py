import com.nrims as nrims
import com.nrims.data as nrimsData
import com.nrims.UI as nrimsUI

import java.io.File as File
import java.util.ArrayList as ArrayList
import java.lang.Integer as Integer
import java.awt.geom.AffineTransform as AfTransform

import sys
from java.lang.System import getProperty
sys.path.append(getProperty("fiji.dir") + "/plugins/Scripts/Plugins/OpenMIMS Scripts/")
import os
import jarray
from java.awt import Polygon
#IJ.log("\n\nStarting roi scale")

#////////////////////////////
# Get existing instance of OpenMims
#////////////////////////////
ui = nrimsUI.getInstance()
if ui == None:
  IJ.log("\nNo instance of OpenMims window")
else:
  #////////////////////////////
  # Check for and open roi managers of OpenMIMS and ImageJ
  #////////////////////////////
  MIMSRoiManager = ui.getRoiManager()
  IJRoiManager = RoiManager.getInstance()
  if IJRoiManager == None:
    IJRoiManager = RoiManager(False)
    if MIMSRoiManager == None:
      MIMSRoiManager = MimsRoiManager(ui)

      workImage = IJ.getImage()
      workProcessor = workImage.getProcessor()
      width = float(workProcessor.getWidth())
      height = float(workProcessor.getHeight())
      images = ui.getOpenMassImages()
      if len(images) != 0:
        #////////////////////////////
        # Use first image as sample size; we're assuming all other mass/sum/ratio/hsi images have same size
        #////////////////////////////
        targetImage = images[0]
        targetProcessor = targetImage.getProcessor()
        targetHeight = float(targetProcessor.getHeight())
        targetWidth = float(targetProcessor.getWidth())

	#////////////////////////////
        # Determine scaling information, scaling target image rois to mass images size.
        #////////////////////////////
        scalingHeight = float(targetHeight/height)
        scalingWidth = float(targetHeight/width)

	#////////////////////////////
        # Loop through rois in IJ roi manager, scale them, then add to OpenMIMS images
        #////////////////////////////
        rois = IJRoiManager.getRoisAsArray()
        for i in range(len(rois)):
          roi = rois[i]
          polygon = roi.getPolygon()
          at = AfTransform.getScaleInstance(scalingHeight, scalingWidth)
          roi = ShapeRoi(at.createTransformedShape(polygon)).shapeToRoi()
          MIMSRoiManager.add(roi)

        #////////////////////////////
        # Update all the images and open the OpenMimsRoi manager
        #////////////////////////////
        ui.updateAllImages()
        MIMSRoiManager.viewManager()

        

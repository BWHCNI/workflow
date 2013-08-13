import com.nrims as nrims
import com.nrims.data as nrimsData

import java.io.File as File
import java.util.ArrayList as ArrayList
import java.lang.Integer as Integer

import sys
from java.lang.System import getProperty
sys.path.append(getProperty("fiji.dir") + "/plugins/Scripts/Plugins/OpenMIMS Scripts/")
#from OMUtilities import MultiFileDialog
#from OMUtilities import CheckFileLists
import javax.swing.JFileChooser as JFileChooser
import java.io.File as File
from ij import IJ
import ij.io.OpenDialog as OpenDialog


import os
import jarray


# Show a jfilecooser and return names of selected
# files
def MultiFileDialog(title):
  #hide/show debug prints
  verbose = 0
  # Choose image file(s) to open
  fc = JFileChooser()
  fc.setMultiSelectionEnabled(True)
  fc.setDialogTitle(title)

  sdir = OpenDialog.getDefaultDirectory()
  if sdir!=None:
    fdir = File(sdir)
  if fdir!=None:
    fc.setCurrentDirectory(fdir)
  
  returnVal = fc.showOpenDialog(IJ.getInstance())
  if returnVal!=JFileChooser.APPROVE_OPTION:
    return
  files = fc.getSelectedFiles()

  paths = []
  for i in range(len(files)):
      paths.append(os.path.join(files[i].getParent(), files[i].getName()))
      
  if verbose > 0:
    for i in range(len(files)):
      path = os.path.join(files[i].getParent(), files[i].getName())
      print "Path: " + path
  
  return paths

  #MimsJFileChooser fc = new MimsJFileChooser(ui);
   #        MIMSFileFilter mff_rois = new MIMSFileFilter("rois.zip");
    #       mff_rois.addExtension("zip");
     #      mff_rois.setDescription("Roi file");
      #     fc.addChoosableFileFilter(mff_rois);
       #    fc.setFileFilter(mff_rois);
        #   fc.setMultiSelectionEnabled(false);

# 
# 
def CheckFileType(files, extension):
  return

originalParent = ""
imFileNames = MultiFileDialog("Open Image Files")
tempFiles = ArrayList()
ui = nrims.UI()
ui.show()
verbose = 1;
IJ.log("\nStarting 'Stack Nrrds'.")
for i in range(len(imFileNames)):
	imFile = File(imFileNames[i])
	directory = imFile.getParent()
	if i == 0:
		originalParent = imFile.getParent()
		originalName = imFile.getName()
	IJ.log("Summing file:" + imFileNames[i])
	name = imFile.getName()
	ui.openFile(imFile)
	mimStack = ui.getmimsStackEditing()
	imp = ArrayList()
	images = ui.getOpenMassImages()
	#compress the planes
       	blockSize = images[0].getNSlices()
       	done = mimStack.compressPlanes(blockSize)
       	#force to 32bit, in case compression didn't
       	massCorrection = nrimsData.massCorrection(ui)
	massCorrection.forceFloatImages(images)
       	
	if done:
		nw = nrimsData.Nrrd_Writer(ui)
		dataFile = nw.save(images, System.getProperty("java.io.tmpdir"), "comp_" + name)
		tempFiles.add(dataFile)
tempFileArray = tempFiles.toArray()
#all work is done in first file
ui.openFile(tempFileArray[0])
for i in range(len(tempFileArray)):
	if i != 0:
		IJ.log("Concating file " + str(i));
		directory = tempFileArray[i].getParent()
		name = tempFileArray[i].getName()
		tempUi = nrims.UI()
		tempUi.openFile(tempFileArray[i])
		tempImage = tempUi.getOpener()
		image = ui.getOpener()
		images = ui.getOpenMassImages()
		mimStack = ui.getmimsStackEditing()
		for j in range(len(images)):
			images[j].setTitle(name)
		if ui.getOpener().getNMasses() == tempImage.getNMasses():
			if mimStack.sameResolution(image, tempImage):
				if mimStack.sameSpotSize(image, tempImage):
					mimStack.concatImages(False, tempUi)
				else:
					IJ.error("Images do not have the same spot size.")
			else:
				IJ.error("Images are not the same resolution.")
		else:
			IJ.error("Two images with the same\nnumber of masses must be open.")
		#kill the temp images and temp ui, then delete the temp file
		tempImages = tempUi.getMassImages()
		for j in range(len(tempImages)):
          		if tempImages[j] != None:
             			tempImages[j].setAllowClose(True)
             			tempImages[j].close()
             	ui.getMimsData().setHasStack(True)
		tempUi = None;
		tempFileArray[i].delete()
nw = nrimsData.Nrrd_Writer(ui)
images = ui.getOpenMassImages()
dataFile = nw.save(images, originalParent, "stack_" + originalName)
ui.setLastFolder(originalParent)
ui.closeCurrentImage()
ui.close()
tempFileArray[0].delete()
IJ.log("Finished 'Stack Nrrds'.\n");


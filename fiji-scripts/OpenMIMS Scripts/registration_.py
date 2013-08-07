from ij import IJ
from ij.plugin import TurboReg
import com.nrims as nrims

import java.io.File as File
import java.util.ArrayList as ArrayList
import java.lang.Integer as Integer
from javax.swing import JScrollPane, JPanel, JComboBox, JLabel, JFrame
from java.awt import Color, GridLayout
from java.awt.event import ActionListener

import sys
from java.lang.System import getProperty
sys.path.append(getProperty("fiji.dir") + "/plugins/Scripts/Plugins/OpenMIMS Scripts/")
from OMUtilities import MultiFileDialog
from OMUtilities import CheckFileLists

import os
import jarray

openImages = ui.getOpenImages()

#Get all open images to list
#Get selection of images
#INSERT: Registration code

panel = JPanel()
sourceImageChooser = JComboBox(openImages)
targetImageChooser = JComboBox(openImages)
panel.add(sourceImageChooser)
panel.add(targetImageChooser)

frame = JFrame("Choose files to register")
frame.getContentPane().add(all)
frame.pack()
frame.setVisible(True)

def registerImages(source, target):
	options = "-align -window " + source.getWindow() + " -window " + target.getWindow() + " scaledRotation -showOutput"
	turboReg = IJ.runPlugIn("TurboReg_", options)
	method = myTurboRegObject.getClass().getMethod("getTransformedImage", null)
	outputImage = (ImagePlus)method.invoke(myTurboRegObject, null)
	

class Listener(ActionListener):
	def __init__(self, source, target):
		self.source = source
		self.target = target
	def actionPerformed(self, event):
		self.source.getSelectedIndex()
		self.target.getSelectedIndex()
		

 Object myTurboRegObject = IJ.runPlugIn("TurboReg_", myTurboRegOptions);

from com.nrims import UI, RatioProps, MimsPlus, MimsJTable

import java.io.File as File
import java.util.ArrayList as ArrayList
import java.lang.Integer as Integer

import sys
from java.lang.System import getProperty
sys.path.append(getProperty("fiji.dir") + "/plugins/Scripts/Plugins/OpenMIMS Scripts/")
from OMUtilities import MultiFileDialog, CheckFileLists

import os
import random
from jarray import array, zeros

#based on javascript example from http://fiji.sc/Scripting_toolbox#Plotting_charts_with_JFreeChart
#
#jfreechart imports
from org.jfree.chart import ChartFactory, ChartFrame
from org.jfree.chart.plot import PlotOrientation, FastScatterPlot
from org.jfree.ui import RectangleInsets
from org.jfree.data.xy import DefaultXYDataset

from java.awt import Color, Rectangle


print "\nStarting 'QSA-ScatterPlot'."
print "Grab images."

#imgA = WindowManager.getImage("25.90:test_file")
#imgB = WindowManager.getImage("26.93/25.90:test_file")

imgA = WindowManager.getImage("12.12:test_file")
imgB = WindowManager.getImage("13.01/12.12:test_file")


ui = UI.getInstance()
rois = ui.getRoiManager().getAllROIs()

print "Create empty dataset"
dataset = DefaultXYDataset()

print "Create ScatterPlot"

chart = ChartFactory.createScatterPlot(
	"Scatter Plot", imgA.getTitle(), imgB.getTitle(),
	dataset, PlotOrientation.VERTICAL,
	True, False, False);

# random test data
#
#print "Add series to dataset"
#npoints = 1000
#data = [[],[]]
#for i in range(npoints):
#	data[0].append(i)
#	data[1].append(2*i+random.gauss(0,50))
#
# this trick is needed to go from a 2D python array 
# to a 2D java array of doubles, see:
# http://fiji.sc/wiki/index.php/Jython_Scripting#Creating_multi-dimensional_native_java_arrays
#twoDimArr = array(data, Class.forName('[D'))

for i in range(len(rois)):
	print "Using roi " + rois[i].getName()
	imgA.setRoi(rois[i])
	imgB.setRoi(rois[i])
	ipA = imgA.getProcessor()
	ipB = imgB.getProcessor()
#	pixA = imgA.getProcessor().getPixels()
#	pixB = imgB.getProcessor().getPixels()
	pixA = []
	pixB = []
	mask = rois[i].getMask()

	r = rois[i].getBounds()
	count = 0;
	for y in range(r.height):
		for x in range(r.width):
			if mask.getPixel(x,y)!=0:
				pA = ipA.getPixelValue(x+r.x, y+r.y)
				pB = ipB.getPixelValue(x+r.x, y+r.y)
				pixA.append(pA)
				pixB.append(pB)
				count = count + 1
	
	print "Added " + str(count) + " pixels"
	arrayA = zeros(len(pixA), 'd')
	arrayB = zeros(len(pixB), 'd')

	for j in range(len(pixA)):
		arrayA[j] = pixA[j]
		arrayB[j] = pixB[j]
	
	print "arrayA.length = " + str(len(pixA)) + ",  arrayA.length = " + str(len(pixB))
	twoDimArr = array([arrayA, arrayB], Class.forName('[D'))

	dataset.addSeries("roi: "+rois[i].getName(), twoDimArr)


# set the background color for the chart...
chart.setBackgroundPaint(Color.white);

plot = chart.getPlot()
plot.setBackgroundPaint(Color.white)
plot.setRangeGridlinesVisible(False)
plot.setAxisOffset(RectangleInsets.ZERO_INSETS)

# Make a buffered image, create imageplus and show
#bi = chart.createBufferedImage(600, 400) 
#imp = ImagePlus("Chart Test", bi)
#imp.show()

# Or show a JFreeChart ChartFrame
frame = ChartFrame("test", chart)
frame.pack()
frame.show()




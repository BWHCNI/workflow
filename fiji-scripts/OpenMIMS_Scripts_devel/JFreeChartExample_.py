import com.nrims.UI as UI
import com.nrims.RatioProps as RatioProps
import com.nrims.MimsPlus as MimsPlus
import com.nrims.MimsJTable as MimsJTable

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

#based on javascript example from http://fiji.sc/Scripting_toolbox#Plotting_charts_with_JFreeChart
#
#jfreechart imports
from org.jfree.chart import ChartFactory
from org.jfree.chart.plot import PlotOrientation
import org.jfree.chart.axis as axis
import org.jfree.chart.encoders as encoders
import org.jfree.chart.renderer.category as category
 
from java.awt import Color
import java.awt.geom as geom
import java.io as io
 
from org.jfree.ui import RectangleInsets
import org.jfree.data.category
from org.jfree.data.statistics import DefaultStatisticalCategoryDataset

# used for svg export
# org.apache.batik.dom
# org.apache.batik.svggen

print "\nStarting 'JFreeChartExample'."

print "Create empty dataset"
dataset = DefaultStatisticalCategoryDataset()
# dataset.add(Mean, StdDev, "Series", "Condition")
print "Add elements to dataset"
dataset.add(15.0, 2.4, "Row 1", "Column 1")
dataset.add(15.0, 4.4, "Row 1", "Column 2")
dataset.add(13.0, 2.1, "Row 1", "Column 3")
dataset.add(7.0, 1.3, "Row 1", "Column 4")
dataset.add(2.0, 2.4, "Row 2", "Column 1")
dataset.add(18.0, 4.4, "Row 2", "Column 2")
dataset.add(28.0, 2.1, "Row 2", "Column 3")
dataset.add(17.0, 1.3, "Row 2", "Column 4")

print "Create LineChart"
chart = ChartFactory.createLineChart(None, "Treatment", "Measurement", dataset, PlotOrientation.VERTICAL, False, True, False)

# set the background color for the chart...
chart.setBackgroundPaint(Color.white);

plot = chart.getPlot()
plot.setBackgroundPaint(Color.white)
plot.setRangeGridlinesVisible(False)
plot.setAxisOffset(RectangleInsets.ZERO_INSETS)

# make a buffered image, create imageplu and show
bi = chart.createBufferedImage(600, 400) 
imp = ImagePlus("Chart Test", bi)
imp.show()






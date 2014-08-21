import com.nrims as nrims
import com.nrims.data as nrimsData
import ij.WindowManager as WindowManager
verbose = 1 


ui = nrims.UI.getInstance()
if ui != None:
	IJ.log("Theres an instance")
image = WindowManager.getCurrentImage();
roiManager = ui.getRoiManager()
roi = roiManager.getRoi()
xy = ui.getRoiManager().getRoiLocation(roi.getName(), 1);
roi.setLocation(xy[0], xy[1]);
image.setRoi(roi)
image.setSlice(1)
stats = image.getStatistics(nrims.MimsJTable.mOptions);
xcenter = stats.xCenterOfMass
ycenter = stats.yCenterOfMass
IJ.log("xcenter: " + str(xcenter))
IJ.log("ycenter: " + str(ycenter))
for i in range(image.getNSlices()):
  xy = ui.getRoiManager().getRoiLocation(roi.getName(), i+1);
  roi.setLocation(xy[0], xy[1]);
  image.setSlice(i+1)
  image.setRoi(roi)
  sliceStats = image.getStatistics(nrims.MimsJTable.mOptions);
  slicexcenter = sliceStats.xCenterOfMass
  sliceycenter = sliceStats.yCenterOfMass
  IJ.log("slicexcenter: " + str(slicexcenter))
  IJ.log("sliceycenter: " + str(sliceycenter))
  xval = xcenter - slicexcenter
  yval = ycenter - sliceycenter
  IJ.log("xvec: " + str(xval))
  IJ.log("yvec: " + str(yval))
  image.getProcessor().translate(xval, yval);
  image.updateAndDraw();
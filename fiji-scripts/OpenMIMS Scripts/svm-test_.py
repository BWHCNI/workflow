import com.nrims as nrims
import com.nrims.segmentation as segmentation
import java.io.File as File
import java.util.ArrayList as ArrayList
import java.lang.Integer as Integer

import jarray
import time


imDirName = "/nrims/home3/cpoczatek/Fiji_test/svm_test"
imFileName = ["080612_8-24-04-10m.im",
"080612_8-24-05-10m.im",
"080612_8-24-06-10m.im",
"080612_8-24-07-10m.im",
"080612_8-24-08-10m.im",
"080612_8-24-09-10m.im"]

modelFileName = "model.MODEL24-4.zip"
minRoiSize = 20

ui = nrims.UI()
ui.show() # :(

for i in range(len(imFileName)):
	#load fiels/setup
	imFile = File(imDirName, imFileName[i])
	IJ.log("Opening: "+imFileName[i])
	ui.openFile(imFile)
	segForm = ui.getmimsSegmentation()
	IJ.log("Loading model: "+modelFileName)
	segmentation.SegFileUtils.load(imDirName+"/"+modelFileName, segForm)
	segForm.updateModelInfo()
	segForm.updateControls()

	#run predition
	images = segForm.getImages()
	colorIndex = segForm.getColorImageIndex()
	localFeatures = segForm.getLocalFeatures()
	segUtil = segmentation.SegUtils.initPrepSeg(images, colorIndex, localFeatures)
        segUtil.execute()
        #wait for segUtil, stupid threads
        while segUtil.getSuccess()==False:
          time.sleep(2)
        IJ.log("segUtil prepSeg done")
        
        segForm.startPrediction(segUtil.getData())        
	#wait for segmentation engine
	while segForm.getActiveEngine().isDone()==False:
          time.sleep(2)
        IJ.log("segForm done")

	#display seg and save as png
	pixels = jarray.zeros(256*256, 'i')
	classColors = segForm.getClassColors()
	classification = segForm.getClassification()
        for i in range(len(pixels)):
            pixels[i] = classColors[classification[i]]
        ui.openSeg(pixels, ui.getImageFilePrefix()+"_seg", ui.getOpener().getHeight(), ui.getOpener().getWidth())
        imp = IJ.getImage()
        FileSaver(imp).saveAsPng(imDirName+"/"+imp.getTitle()+".png")

	#run calc rois
	h = ui.getOpener().getHeight()
	w = ui.getOpener().getWidth()
	a = h*w
	segUtil = segmentation.SegUtils.initCalcRoi(h, w, segForm.getClassNames(), segForm.getClassification(), minRoiSize, a);
        segUtil.execute()
        #wait for segUtil, stupid threads
        while segUtil.getSuccess()==False or segUtil.getClasses()==None:
          #print "sleep..."
          time.sleep(2)
        IJ.log("segUtil calcRoi done")

	predClasses = segUtil.getClasses()
	length = len(predClasses.getClasses())
	rm = ui.getRoiManager()
	for c in range(length):
	  classname = predClasses.getClasses()[c]
          segrois = [] 
          for r in range(len(predClasses.getRois(classname))):
            segrois.append(predClasses.getRois(classname)[r].getRoi())
          grpname = "seg,a"+str(segUtil.getMinSize())+","+classname
          rm.addToGroup(segrois, grpname)

	#save model in case, contains predition
        #???????????

        #save rois
        rm.showFrame()
        path = imDirName + "/" + ui.getImageFilePrefix() + ui.ROIS_EXTENSION
        rm.saveMultiple(rm.getAllROIs(), path, False)
	rm.delete(False)
	
ui.closeCurrentImage()
ui.close()

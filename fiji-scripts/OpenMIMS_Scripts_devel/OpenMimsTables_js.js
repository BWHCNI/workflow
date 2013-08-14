importPackage(Packages.com.nrims);
importClass(java.io.File);
importClass(java.util.ArrayList);
importClass(java.lang.Integer);

// The directory containing the .im files.
imDirName = "/nrims/home3/zkaufman/TEMP";

// The list of files.
imFileName = [
"test_file1.im",
"test_file2.im",
"test_file3.im"
];

// The list of roi files (Needs to have same number of entries as .im files above).
roiFileName = [
"test_file1.rois.zip",
"test_file2.rois.zip",
"test_file3.rois.zip"
];

// List of statistics.
// Others: "mean", "stddev", "median", "N/D", 
//         "min", "max", "sum", "mode", "area", 
//         "group (table only)", "roix", "roiy", 
//         "roiwidth", "roiheight"
stats = ["mean", "stddev"];

////////////////////////////
// Initialize stuff.
////////////////////////////
ui = new UI();
ui.show();

////////////////////////////
// Loop over files.
////////////////////////////
for(var i = 0; i < imFileName.length; i++) {

	imFile = new File(imDirName, imFileName[i]);
	roiFile = new File(imDirName, roiFileName[i]);
	IJ.log("Opening: "+imFile);
	ui.openFile(imFile);
	IJ.log("Opening: "+roiFile);
	ui.openFile(roiFile);
	
	
	////////////////////////////
	// Get the planes.
	////////////////////////////
	planes = ui.getmimsTomography().getPlanes();

	////////////////////////////
	// Get the rois.
	////////////////////////////
	rois = ui.getRoiManager().getAllROIs();

	////////////////////////////
	// Get images.
	////////////////////////////
	imageArray = new ArrayList();
	massimages = ui.getOpenMassImages();
	for (var ii = 0; ii < massimages.length; ii++) {
	   imageArray.add(massimages[ii]);
	} 
	
	// Ratio images
	// 0 corresponds to the first mass image (e.g. mass 12.0)
	// 1 corresponds to the second mass image (e.g. mass 13.0)
	ratioProps1 = new RatioProps(1, 0);
	mp1 = new MimsPlus(ui, ratioProps1);
	imageArray.add(mp1);
	IJ.log("Opening ratio: "+mp1.getTitle());

	// Ratio images
	// 2 corresponds to the first mass image (e.g. mass 26.0)
	// 3 corresponds to the second mass image (e.g. mass 27.0)
	ratioProps2 = new RatioProps(3, 2);
	mp2 = new MimsPlus(ui, ratioProps2);
	imageArray.add(mp2);
	IJ.log("Opening ratio: "+mp2.getTitle());

	images = new java.lang.reflect.Array.newInstance(MimsPlus, imageArray.size());
	images = imageArray.toArray(images);		 		
		
	////////////////////////////
	// Create and display table.
	////////////////////////////
	table = new MimsJTable(ui);
	table.setStats(stats);
	table.setRois(rois);
	table.setImages(images);
	table.setPlanes(planes);
	append=false;
	nPlanes = ui.getOpener().getNImages();
	if (nPlanes > 1)
   		table.createTable(append);
	else
   		table.createSumTable(append);
	table.showFrame();
	IJ.log("Writing: "+imDirName+"/"+ui.getImageFilePrefix()+"_data.csv");
	table.writeData(new File(imDirName, ui.getImageFilePrefix()+"_data.csv"));
	table.close();
	IJ.log("");
}
ui.closeCurrentImage();
ui.close();






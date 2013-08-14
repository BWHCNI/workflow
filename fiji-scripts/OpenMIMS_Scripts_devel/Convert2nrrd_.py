import com.nrims as nrims
import java.io.File as File
import java.util.ArrayList as ArrayList
import java.lang.Integer as Integer

import jarray

# The directory containing the .im/.nrrd files.
imDirName = "/nrims/home3/cpoczatek/Fiji_test/test_images";

# The list of files.
imFileName = ["test_file.nrrd", "test_file2.nrrd", "test_file3.nrrd"]

compress = True

#////////////////////////////
# Initialize stuff.
#////////////////////////////
ui = nrims.UI()
ui.show()

#////////////////////////////
# Loop over files.
#////////////////////////////
for i in range(len(imFileName)):
	imFile = File(imDirName, imFileName[i])
	IJ.log("Opening: "+imFileName[i])
	ui.openFile(imFile)
	if compress:
		stackedit = ui.getmimsStackEditing()
		stackedit.compress(ui.asdfasfasdfasf)

ui.close()
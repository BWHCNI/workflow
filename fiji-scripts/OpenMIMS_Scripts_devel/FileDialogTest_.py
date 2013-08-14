import os
import javax.swing.JFileChooser as JFileChooser
import java.io.File as File

def run():
  #hide/show debug prints
  verbose = 1
  # Choose image file(s) to open
  fc = JFileChooser()
  fc.setMultiSelectionEnabled(True)

  sdir = OpenDialog.getDefaultDirectory()
  if sdir!=None:
    fdir = File(sdir)
  if fdir!=None:
    fc.setCurrentDirectory(fdir)
  
  returnVal = fc.showOpenDialog(IJ.getInstance())
  if returnVal!=JFileChooser.APPROVE_OPTION:
    return
  files = fc.getSelectedFiles()

  if verbose > 0:
    for i in range(len(files)):
      path = os.path.join(files[i].getParent(), files[i].getName())
      print "Path: " + path
  return files
  
run()
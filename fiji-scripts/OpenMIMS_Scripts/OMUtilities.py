# A collection of utility methods related to OpenMIMS scripts
#

import os
import javax.swing.JFileChooser as JFileChooser
import java.io.File as File

from ij import IJ
import ij.io.OpenDialog as OpenDialog

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

# Ensure lists match, for some definition of match...
#
def CheckFileLists(lista, listb):
  return

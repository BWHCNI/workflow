from __future__ import with_statement
import com.nrims as nrims
import com.nrims.data as nrimsData
import time
from datetime import timedelta, datetime, date
import java.io.File as File
import java.util.ArrayList as ArrayList
import java.lang.Integer as Integer
import java.lang.Double as Double

import sys
from java.lang.System import getProperty
sys.path.append(getProperty("fiji.dir") + "/plugins/Scripts/Plugins/OpenMIMS Scripts/")
#from OMUtilities import MultiFileDialog
#from OMUtilities import CheckFileLists
import javax.swing.JFileChooser as JFileChooser
import java.io.File as File
from ij import IJ
import ij.io.OpenDialog as OpenDialog
import ij.gui.YesNoCancelDialog as YesNoCancelDialog
import csv

import os
import jarray
def FolderDialog(title, folder):
  fc = JFileChooser()
  fc.setMultiSelectionEnabled(False)
  fc.setDialogTitle(title)
  fc.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
  fc.setAcceptAllFileFilterUsed(False);
  if folder ==None:
    sdir = OpenDialog.getDefaultDirectory()
  else:
    sdir = folder
  if sdir!=None:
    fdir = File(sdir)
  if fdir!=None:
    fc.setCurrentDirectory(fdir)
  returnVal = fc.showOpenDialog(IJ.getInstance())
  if returnVal!=JFileChooser.APPROVE_OPTION:
    return
  folder = fc.getSelectedFile();
  path = os.path.join(folder.getParent(), folder.getName())
  return path
 
def checkFolder(folder, times, root):
	filenames = os.listdir(folder)
	for i in range(len(filenames)):
		filepath = folder + "/" + filenames[i]
		shortfilepath = filepath[len(root):]
		if os.path.isdir(filepath):
			times = checkFolder(filepath, times, root)
		if filenames[i].endswith('.im') and os.path.isfile(filepath):
			isTemp = filenames[i].startswith("._")
			if isTemp is False:
				imFile = File(filepath)
    				imReader = nrimsData.Mims_Reader(imFile)
    				duration = imReader.getDurationD()
    				startdate = datetime.strptime(imReader.getSampleDate(), "%d.%m.%y")
    				enddate = datetime.strptime(imReader.getSampleDate(), "%d.%m.%y") + timedelta(seconds=int(duration))
    				uniquedays = abs(enddate-startdate).days
    				times[shortfilepath] = [duration, startdate, enddate, uniquedays]
    				imReader.close()
				
				
	return times

def getFolderList(path):
  folders=[]
  while 1:
    path,folder=os.path.split(path)

    if folder!="":
      folders.append(folder)
    else:
      if path!="":
        folders.append(path)
        break
  folders.reverse()
  return folders

verbose = 1;
IJ.log("\nStarting 'Grab MetaData'.")
durations = dict()
chosenFolder = FolderDialog("Choose directory to read .im metadata from", "/nrims/data/")
start = time.time()
durations = checkFolder(chosenFolder, durations, chosenFolder)
end = time.time()
IJ.log("Reading metadata took " + str(end - start) + " seconds.")
targetFolder = FolderDialog("Choose folder to save duration data in", "~")
cfolder, cfilename = os.path.split(chosenFolder)
with open(targetFolder + '/' + cfilename + '.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(["Path", "Filename", "Duration (in s)", "Collaborator", "EXP", "Start (D/M/Y)", "End (D/M/Y)", "Days ran"])
    for key, value in durations.items():
    	folder, filename = os.path.split(key)
	folders = getFolderList(key)
	collaborator = "None";
	EXP = "None";
	if (len(folders) > 2):
	  collaborator = folders[1]
          EXP = folders[2]
   	writer.writerow([folder, filename, value[0], collaborator, EXP, value[1].strftime("%d/%m/%y"), value[2].strftime("%d/%m/%y"), value[3]+1])

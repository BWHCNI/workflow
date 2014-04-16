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
  
def writeToCSV(writer, key, value, shortfilepath):
  fullfolder, fullfilename = os.path.split(shortfilepath)
  folder, filename = os.path.split(key)
  folders = getFolderList(key)
  collaborator = "None";
  EXP = "None";
  i = 0
  if (len(folders) > 2):
    while (i < len(folders) and folders[i] != "MIMS_DATA"):
      i = i + 1
    if (i >= len(folders)):
      i=0
    collaborator = folders[i+1]
    EXP = folders[i+2]
  if value[2] is None:
    value[2] = "N/A"
  else:
    value[2] = value[2].strftime("%y/%m/%d")
  if value[3] is None:
    value[3] = "N/A"
  else:
    value[3] = value[3].strftime("%d/%m/%y")
  if value[4] is None:
    value[4] = "N/A"
  else:
    value[4] = value[4] + 1
  writer.writerow([fullfolder, filename, collaborator, EXP, value[0], value[1], value[2], value[3], value[4]])
def writeToCollabCSV(writer, key, value, shortfilepath):
  fullfolder, fullfilename = os.path.split(shortfilepath)
  folder, filename = os.path.split(key)
  folders = getFolderList(key)
  collaborator = "None";
  EXP = "None";
  i = 0
  if (len(folders) > 2):
    while (i < len(folders) and folders[i] != "MIMS_DATA"):
      i = i + 1
    if (i >= len(folders)):
      i=0
    collaborator = folders[i+1]
    EXP = folders[i+2]
  if value[0] is None:
    value[0] = "N/A"
  else:
    value[0] = value[0].strftime("%y/%m/%d")
  writer.writerow([fullfolder, filename, value[0], value[1], value[2]])
  
def checkFolder(folder, times, root, writer, collabwriter, collaborator):
  filenames = os.listdir(folder)
  for i in range(len(filenames)):
    isTemp = filenames[i].startswith(".")
    if isTemp is False:
      filepath = str(folder) + "/" + str(filenames[i])
      shortfilepath = filepath[len(root):]
      if os.path.isdir(filepath):
        times = checkFolder(filepath, times, root, writer, collabwriter, collaborator)
      if filenames[i].endswith('.im') and os.path.isfile(filepath):
        imFile = File(filepath)
        try:
          imReader = nrimsData.Mims_Reader(imFile)
          duration = imReader.getDurationD()
          dwell = float(imReader.getDwellTime())
          width = float(imReader.getWidth())
          height = float(imReader.getHeight())
          planes = int(imReader.getNImages())
          durationDwell = int(dwell*width*height*planes/1000)
          startdate = None
          enddate = None
          uniquedays = None
          try:
            startdate = datetime.strptime(imReader.getSampleDate(), "%d.%m.%y")
          except:
            IJ.log("Could not read the following startdate: " + str(imReader.getSampleDate()) + ", from " + filepath)
            startdate = None
          try:
            enddate = datetime.strptime(imReader.getSampleDate(), "%d.%m.%y") + timedelta(seconds=int(durationDwell))
          except:
            enddate = None
          if startdate is not None and enddate is not None:
            uniquedays = abs(enddate-startdate).days
          else:
            uniquedays = None
          writeToCSV(writer, filepath, [duration, durationDwell, startdate, enddate, uniquedays], shortfilepath)
          for i in range(uniquedays+1):
            writeToCollabCSV(collabwriter, filepath, [datetime.strptime(imReader.getSampleDate(), "%d.%m.%y") +timedelta(days=int(i)) , duration, durationDwell], shortfilepath)
          imReader.close()
        except:
          IJ.log("Could not read " + str(filepath) + " " + str(sys.exc_info()[0]))
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
targetFolder = FolderDialog("Choose folder to save duration data in", "~")
start = time.time()
cfolder, cfilename = os.path.split(chosenFolder)
with open(targetFolder + '/' + cfilename + '.csv', 'wb') as f:
  writer = csv.writer(f)
  writer.writerow(["Path", "Filename", "Collaborator", "EXP", "Duration (in s)", "Duration (dwell)", "Start(Y/M/D)", "End", "Days ran" ])
  collaborators = os.listdir(chosenFolder)
  for i in range(len(collaborators)):
    filepath = str(chosenFolder) + "/" + str(collaborators[i])
    if not collaborators[i].startswith(".") and os.path.isdir(filepath):
      with open(targetFolder + '/' + collaborators[i] + '.csv', 'wb') as collabf:
        collabwriter = csv.writer(collabf)
        collabwriter.writerow(["Path", "Filename", "Date Run On(Y/M/D)", "Duration (in s)", "Duration (dwell)"])
        checkFolder(chosenFolder + "/" + collaborators[i], durations, chosenFolder, writer, collabwriter, collaborators[i])
end = time.time()
IJ.log("Reading metadata took " + str(end - start) + " seconds.")
